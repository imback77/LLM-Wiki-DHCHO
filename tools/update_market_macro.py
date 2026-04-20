import FinanceDataReader as fdr
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import sys
import io

# 출력 인코딩 설정 (Windows 대응)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def get_latest_value(name, ticker, source='yf'):
    """최신 값을 가져오며 실시간 오류 처리를 강화합니다."""
    try:
        if source == 'yf':
            df = yf.download(ticker, period='5d', progress=False)
            if not df.empty:
                val = df['Close'].iloc[-1]
                # Series일 경우 float 처리
                if isinstance(val, pd.Series):
                    val = val.iloc[0]
                return round(float(val), 2)
        elif source == 'fdr':
            df = fdr.DataReader(ticker)
            if not df.empty:
                val = df['Close'].iloc[-1]
                return round(float(val), 2)
    except Exception as e:
        print(f"⚠️ {name} 수집 실패: {e}")
    return "N/A"

def update_market_macro():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[{today}] 글로벌 매크로 및 리스크 지표 수집 시작 (Sources: Yahoo + KRX)...")

    # 1. 수집 대상 정의 (유효한 티커로 보정)
    tickers = {
        "USD/KRW": ("USDKRW=X", "yf"),
        "US 10Y Yield": ("^TNX", "yf"),
        "KR 3Y Yield": ("KR3YT=RR", "yf"), # Yahoo에서도 가능
        "WTI (Oil)": ("CL=F", "yf"),
        "Copper": ("HG=F", "yf"),
        "VIX (Fear)": ("^VIX", "yf"),
        "SOX (Semiconductor)": ("^SOX", "yf"),
        "KOSPI": ("KS11", "fdr"),
        "KOSDAQ": ("KQ11", "fdr"),
    }

    results = {}
    for name, (ticker, source) in tickers.items():
        results[name] = get_latest_value(name, ticker, source)

    # 2. YAML Frontmatter 생성
    # N/A 값일 경우 기본값 처리
    vix_val = results.get('VIX (Fear)', 0)
    usd_val = results.get('USD/KRW', 0)
    
    yaml_frontmatter = f"""---
date: {today}
type: market_macro
usd_krw: {usd_val if usd_val != 'N/A' else 0}
vix: {vix_val if vix_val != 'N/A' else 0}
us_10y: {results.get('US 10Y Yield', 0)}
oil_wti: {results.get('WTI (Oil)', 0)}
---"""

    # 3. 마크다운 리포트 생성
    summary_data = []
    for k, v in results.items():
        summary_data.append({"지표명": k, "현재값": v})
    
    df_summary = pd.DataFrame(summary_data)
    
    content = f"""{yaml_frontmatter}
# {today} 글로벌 매크로 및 리스크 관리 지표

## 🌍 매크로 요약 (Macro Status)
- **달러/금리**: {usd_val} (환율), {results.get('US 10Y Yield')} (미10년물)
- **시장 지수**: KOSPI {results.get('KOSPI')}, KOSDAQ {results.get('KOSDAQ')}
- **반도체/섹터**: SOX index {results.get('SOX (Semiconductor)')}

---

## 📋 핵심 지표 리스트

{df_summary.to_markdown(index=False)}

---
> **참고**: 데이터는 Yahoo Finance 및 KRX 공식 데이터를 기반으로 추출되었습니다.
"""

    output_dir = "raw/research/macro"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"{today}_macro_status.md")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 매크로 분석 완료: {output_path}")

if __name__ == "__main__":
    update_market_macro()
