import FinanceDataReader as fdr
import pandas as pd
import requests
from datetime import datetime
import os
import sys
import json

# 출력 인코딩 설정 (Windows 대응)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def validate_data(df):
    """데이터 정합성을 검증합니다."""
    if df.empty:
        raise ValueError("수집된 데이터가 비어 있습니다.")
    
    # 상한가(30%) 초과 등 이상치 체크 (경고 로그)
    outliers = df[df['ChagesRatio'] > 31]
    if not outliers.empty:
        print(f"⚠️ 경고: 가격 등락률이 비정상적으로 높은 종목이 감지되었습니다: {outliers['Name'].tolist()}")

def update_dynamic_trend():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[{today}] 실시간 자금 동향(Flow) 분석 시작...")

    try:
        # 1. 전체 종목 리스트 및 당일 시세 수집
        print("1. KRX 전 종목 시세 데이터 수집 중...")
        df_krx = fdr.StockListing('KRX')
        validate_data(df_krx)

        # 2. 제미나이 정량 지표 필터링
        # 기준: 거래대금 500억 이상 AND 상승률 5% 이상
        print("2. 거래대금(500억↑) 및 상승률(5%↑) 필터링 중...")
        df_trend = df_krx[
            (df_krx['Amount'] >= 50_000_000_000) & 
            (df_krx['ChagesRatio'] >= 5)
        ].copy()

        if df_trend.empty:
            print("현재 기준에 부합하는 급등 종목이 없습니다. (장이 마감되었거나 활성 거래가 적음)")
            # 빈 파일이라도 생성하거나 종료
        
        # 3. KIND 업종 정보 결합
        print("3. KIND 업종 데이터 결합 중...")
        url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
        resp = requests.get(url)
        resp.encoding = 'cp949'
        df_kind = pd.read_html(resp.text, header=0)[0]
        df_kind = df_kind[['회사명', '종목코드', '업종', '주요제품']]
        df_kind['종목코드'] = df_kind['종목코드'].astype(str).str.zfill(6)

        df_final = pd.merge(df_trend, df_kind, left_on='Code', right_on='종목코드', how='left')
        
        # 4. 데이터 정리
        df_final = df_final[['Name', 'Market', '업종', '주요제품', 'ChagesRatio', 'Amount', 'Marcap', 'Code']]
        df_final = df_final.rename(columns={
            'Name': '종목명',
            'Market': '시장',
            '업종': '업종',
            '주요제품': '세부업종',
            'ChagesRatio': '등락률(%)',
            'Amount': '거래대금',
            'Marcap': '시가총액',
            'Code': '코드'
        })
        
        # 포맷팅
        df_final['거래대금'] = df_final['거래대금'].apply(lambda x: f"{int(x/100000000):,}억" if pd.notnull(x) else "")
        df_final['시가총액'] = df_final['시가총액'].apply(lambda x: f"{int(x/100000000):,}억" if pd.notnull(x) else "")

        # 5. AI 인제스트를 위한 요약 메타데이터
        sector_counts = df_final['업종'].value_counts()
        summary_metadata = {
            "date": today,
            "trend_count": len(df_final),
            "top_amount_stock": df_final.sort_values('거래대금', ascending=False)['종목명'].iloc[0] if not df_final.empty else "N/A",
            "leading_sectors": sector_counts.head(3).to_dict()
        }

        # 6. 파일 저장
        output_dir = "raw/research/trends"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{today}_dynamic_trend.md"
        output_path = os.path.join(output_dir, filename)

        markdown_table = df_final.to_markdown(index=False)
        
        # AI Summary Block
        summary_header = f"""<!-- AI_FLOW_SUMMARY
{json.dumps(summary_metadata, ensure_ascii=False, indent=2)}
AI_FLOW_SUMMARY_END -->"""

        content = f"""# {today} 주식 시장 자금 동향 (Dynamic Trend)

{summary_header}

## ⚡ 시장 요약 (AI Insight)
- **금일 자급 집중 종목**: 총 {len(df_final)}개
- **주도 섹터**: {', '.join(sector_counts.index[:3]) if not sector_counts.empty else '없음'}
- **거래대금 대장주**: {summary_metadata['top_amount_stock']}

> **안내**: 이 데이터는 거래대금 500억 이상, 상승률 5% 이상의 '돈이 몰리는 길목'에 있는 종목들입니다. 
> 지난 데이터와 비교하여 자급의 이동 경로를 분석하는 기초 자료로 활용됩니다.

---

## 📋 자금 집중 종목 리스트

{markdown_table}
"""

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"✅ 동적 트렌드 분석 완료: {output_path}")

    except Exception as e:
        error_log_path = "tools/error.log"
        with open(error_log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] ERROR in update_dynamic_trend: {str(e)}\n")
        print(f"❌ 오류 발생: {e}. 상세 내용은 tools/error.log를 확인하세요.")

if __name__ == "__main__":
    update_dynamic_trend()
