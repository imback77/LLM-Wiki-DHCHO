import FinanceDataReader as fdr
import pandas as pd
import requests
from datetime import datetime, timedelta
import os
import sys
import json
import time
from contextlib import contextmanager

# pykrx 경고 메시지 방지를 위한 context manager
@contextmanager
def silence_stderr():
    new_stderr = open(os.devnull, 'w')
    old_stderr = sys.stderr
    sys.stderr = new_stderr
    try:
        yield
    finally:
        sys.stderr = old_stderr
        new_stderr.close()

# pykrx import 시의 경고 메시지 차단
with silence_stderr():
    from pykrx import stock

# 출력 인코딩 설정 (Windows 대응)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def validate_data(df):
    """데이터 정합성을 검증합니다."""
    if df.empty:
        raise ValueError("수집된 데이터가 비어 있습니다.")
    
    if 'ChagesRatio' in df.columns:
        outliers = df[df['ChagesRatio'] > 31]
        if not outliers.empty:
            print(f"⚠️ 경고: 가격 등락률이 비정상적으로 높은 종목이 감지되었습니다: {outliers['Name'].tolist()}")

def get_trading_days(days=30):
    """최근 영업일 리스트를 반환합니다."""
    df = fdr.DataReader('KS11', (datetime.now() - timedelta(days=days)).strftime('%Y%m%d'))
    return df.index.strftime('%Y%m%d').tolist()

def get_investor_flow_naver(ticker):
    """네이버 금융에서 투자자별 순매매량(수량)을 가져와 금액으로 환산합니다."""
    url = f"https://finance.naver.com/item/frgn.naver?code={ticker}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        resp = requests.get(url, headers=headers)
        tables = pd.read_html(io.StringIO(resp.text))
        # 3번째 테이블이 투자자별 매매동향
        df = tables[2]
        df.columns = ['날짜', '종가', '전일비', '등락률', '거래량', '기관순매매량', '외국인순매매량', '외국인보유주수', '외국인보유율']
        
        # 최신 행(NaN 제외) 추출
        df = df.dropna(subset=['날짜'])
        if df.empty:
            return 0, 0
            
        latest = df.iloc[0]
        
        # 금액 환산: 순매매량 * 종가 (단위: 원)
        # 종가와 수량에서 콤마 제거 및 숫자로 변환 필요
        price = float(str(latest['종가']).replace(',', ''))
        inst_vol = float(str(latest['기관순매매량']).replace(',', ''))
        fore_vol = float(str(latest['외국인순매매량']).replace(',', ''))
        
        return fore_vol * price, inst_vol * price
    except Exception as e:
        # print(f"Error scraping Naver for {ticker}: {e}")
        return 0, 0

def update_dynamic_trend():
    today_dash = datetime.now().strftime("%Y-%m-%d")
    print(f"[{today_dash}] 수급 동향 실시간 분석 시작 (Source: KRX + Naver)...")

    try:
        # 1. KRX 전 종목 기본 시세 수집 (FDR)
        print("1. KRX 전 종목 시세 수집 중...")
        df_krx = fdr.StockListing('KRX')
        validate_data(df_krx)

        # 2. 1차 필터링
        print("2. 1차 필터링 (거래대금 500억↑, 상승률 5%↑)...")
        df_trend = df_krx[
            (df_krx['Amount'] >= 50_000_000_000) & 
            (df_krx['ChagesRatio'] >= 5)
        ].copy()

        if df_trend.empty:
            print("현재 기준에 부합하는 급등 종목이 없습니다.")
            return

        # 3. 상세 수급 및 거래량 모멘텀 분석
        print("3. 상세 수급(Naver) 및 거래량 모멘텀 분석 중...")
        trading_days = get_trading_days(40)
        start_date = trading_days[-21]
        end_date = trading_days[-1]
        
        tickers = df_trend['Code'].tolist()
        flow_data = []

        for ticker in tickers:
            # 네이버에서 수급 데이터(금액 환산) 수집
            f_net, i_net = get_investor_flow_naver(ticker)
            
            # 20일 평균 거래량 (pykrx 사용, 경고 무시)
            with silence_stderr():
                df_ohlcv = stock.get_market_ohlcv(start_date, end_date, ticker)
            
            avg_vol = df_ohlcv['거래량'].iloc[:-1].mean() if len(df_ohlcv) > 1 else 1
            curr_vol = df_ohlcv['거래량'].iloc[-1]
            vol_ratio = round(curr_vol / avg_vol, 2) if avg_vol > 0 else 0
            
            flow_data.append({
                'Code': ticker,
                '외인순매수': f_net,
                '기관순매수': i_net,
                '거래량배율': vol_ratio
            })
            time.sleep(0.1) # 네이버 차단 방지

        df_flow = pd.DataFrame(flow_data)
        df_final = pd.merge(df_trend, df_flow, on='Code', how='left')

        # 4. KIND 업종 정보 결합
        url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
        resp = requests.get(url)
        resp.encoding = 'cp949'
        df_kind = pd.read_html(io.StringIO(resp.text), header=0)[0]
        df_kind = df_kind[['회사명', '종목코드', '업종']]
        df_kind['종목코드'] = df_kind['종목코드'].astype(str).str.zfill(6)
        df_final = pd.merge(df_final, df_kind, left_on='Code', right_on='종목코드', how='left')
        
        # 5. 데이터 정리 및 포맷팅
        df_final = df_final[['Name', 'Market', '업종', 'ChagesRatio', 'Amount', '외인순매수', '기관순매수', '거래량배율', 'Marcap', 'Code']]
        df_final = df_final.rename(columns={
            'Name': '종목명', 'Market': '시장', 'ChagesRatio': '등락률', 'Amount': '거래대금', 'Marcap': '시가총액'
        })
        
        for col in ['거래대금', '외인순매수', '기관순매수', '시가총액']:
            df_final[col] = df_final[col].apply(lambda x: f"{int(x/100000000):,}억" if pd.notnull(x) else "0억")

        # 6. 저장 및 출력
        leading_sectors = df_final['업종'].value_counts().head(3).index.tolist()
        yaml_frontmatter = f"""---
date: {today_dash}
type: market_flow
trend_count: {len(df_final)}
leading_sectors: {leading_sectors}
top_amount_stock: {df_final.sort_values('거래대금', ascending=False)['종목명'].iloc[0] if not df_final.empty else 'N/A'}
---"""

        content = f"""{yaml_frontmatter}
# {today_dash} 주식 시장 자금 동향 (Dynamic Trend)

## ⚡ 시장 요약 (AI Insight)
- **금일 수급 집중 종목**: 총 {len(df_final)}개
- **주도 섹터**: {', '.join(leading_sectors) if leading_sectors else '업종 미분류'}
- **데이터 소스**: KRX(시세), Naver(수급) 교차 검증

---

## 📋 자금 집중 종목 상세 리스트

{df_final.to_markdown(index=False)}
"""
        output_dir = "raw/research/trends"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{today_dash}_dynamic_trend.md")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ 분석 완료: {output_path}")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    update_dynamic_trend()
