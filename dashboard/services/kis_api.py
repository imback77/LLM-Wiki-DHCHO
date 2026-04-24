import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv

class KisApi:
    def __init__(self):
        # Use a specific path for .env to ensure it's loaded properly regardless of cwd
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
        load_dotenv(env_path, override=True)
        self.app_key = os.getenv("KIS_APP_KEY")
        self.app_secret = os.getenv("KIS_APP_SECRET")
        self.domain = os.getenv("KIS_DOMAIN", "https://openapi.koreainvestment.com:9443")
        self.access_token = None
        self.headers = {}
        
    def get_access_token(self):
        """Fetches the OAuth access token from KIS"""
        if not self.app_key or self.app_key.startswith("여기에"):
            print("⚠️ KIS_APP_KEY가 .env 파일에 설정되지 않았습니다. 실시간 가격 대신 더미 데이터를 반환합니다.")
            return False

        url = f"{self.domain}/oauth2/tokenP"
        headers = {"content-type": "application/json"}
        body = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }
        
        try:
            res = requests.post(url, headers=headers, data=json.dumps(body))
            if res.status_code == 200:
                self.access_token = res.json().get("access_token")
                self.headers = {
                    "content-type": "application/json; charset=utf-8",
                    "authorization": f"Bearer {self.access_token}",
                    "appkey": self.app_key,
                    "appsecret": self.app_secret,
                    "tr_id": "FHKST01010100" # 주식현재가 시세 tr_id
                }
                return True
            else:
                print(f"Failed to get token: {res.text}")
                return False
        except Exception as e:
            print(f"API Connection Error: {e}")
            return False

    def get_current_price(self, stock_code: str):
        """Fetches current price and metrics for a specific stock"""
        if not self.access_token:
            # Return dummy data if API is not configured
            return {
                "current_price": 0,
                "change_rate": 0.0,
                "volume": 0
            }

        url = f"{self.domain}/uapi/domestic-stock/v1/quotations/inquire-price"
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": stock_code
        }
        
        try:
            res = requests.get(url, headers=self.headers, params=params)
            if res.status_code == 200:
                data = res.json().get("output", {})
                return {
                    "current_price": int(data.get("stck_prpr", 0)), # 현재가
                    "change_rate": float(data.get("prdy_ctrt", 0.0)), # 전일 대비 율
                    "volume": int(data.get("acml_vol", 0)) # 누적 거래량
                }
            else:
                return {"current_price": 0, "change_rate": 0.0, "volume": 0}
        except Exception:
            return {"current_price": 0, "change_rate": 0.0, "volume": 0}

    def get_bulk_prices(self, stock_codes: list):
        """Fetches prices for multiple stocks strictly honoring the 20 requests/sec limit"""
        import time
        results = {}
        for code in stock_codes:
            results[code] = self.get_current_price(code)
            time.sleep(0.06) # ~16 requests per second max to avoid IP block/rate limit
        return results

    def get_historical_prices(self, stock_code: str):
        """
        Fetches the last 30 days of daily price data for technical analysis.
        Automatically reflects KRX and NXT (Nextrade ATS) integrated closing prices 
        when queried after 8:00 PM.
        """
        if not self.access_token:
            return pd.DataFrame()

        url = f"{self.domain}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        import datetime
        now = datetime.datetime.now()
        end_date = now.strftime("%Y%m%d")
        start_date = (now - datetime.timedelta(days=45)).strftime("%Y%m%d") # Fetch 45 days to ensure 30 trading days

        headers = self.headers.copy()
        headers["tr_id"] = "FHKST03010100" # 국내주식 기간별 시세 (일/주/월/년)

        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": stock_code,
            "FID_INPUT_DATE_1": start_date,
            "FID_INPUT_DATE_2": end_date,
            "FID_PERIOD_DIV_CODE": "D",
            "FID_ORG_ADJ_PRC": "0" # 수정주가 반영
        }
        
        try:
            res = requests.get(url, headers=headers, params=params)
            if res.status_code == 200:
                data = res.json().get("output2", [])
                if not data:
                    return pd.DataFrame()
                
                df = pd.DataFrame(data)
                df = df[['stck_bsop_date', 'stck_clpr', 'acml_vol']]
                df.columns = ['date', 'close', 'volume']
                df['close'] = df['close'].astype(float)
                df['volume'] = df['volume'].astype(int)
                df = df.sort_values('date').reset_index(drop=True)
                return df
            else:
                return pd.DataFrame()
        except Exception:
            return pd.DataFrame()

class SectorAnalyzer:
    @staticmethod
    def calculate_sector_metrics(tracked_stocks: list, live_prices: dict):
        """
        Calculates sector rotation metrics using Pandas.
        Zero token consumption.
        """
        if not tracked_stocks or not live_prices:
            return pd.DataFrame()
            
        data = []
        for stock in tracked_stocks:
            code = stock['code']
            price_data = live_prices.get(code, {})
            data.append({
                'name': stock['name'],
                'code': code,
                'sector': stock['sector'],
                'entry_price': stock['entry_price'],
                'current_price': price_data.get('current_price', 0),
                'change_rate': price_data.get('change_rate', 0.0),
                'volume': price_data.get('volume', 0)
            })
            
        df = pd.DataFrame(data)
        
        # Calculate Sector Averages
        if df.empty: return df
        
        sector_metrics = df.groupby('sector').agg(
            avg_change_rate=('change_rate', 'mean'),
            total_volume=('volume', 'sum'),
            stock_count=('code', 'count')
        ).reset_index()
        
        # Sort by best performing sector today
        sector_metrics = sector_metrics.sort_values(by='avg_change_rate', ascending=False)
        return sector_metrics
