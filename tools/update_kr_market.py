import FinanceDataReader as fdr
import pandas as pd
import requests
from datetime import datetime
import os
import sys

# 출력 인코딩 설정 (Windows 환경 대응)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def update_market_stucture():
    print("1. 한국거래소(KRX) 시가총액 데이터 수집 중...")
    try:
        # FDR을 사용하여 Marcap 정보가 포함된 전체 리스트 확보
        df_krx = fdr.StockListing('KRX')
        
        # 시장별 시가총액 상위 종목 추출
        df_kospi = df_krx[df_krx['Market'] == 'KOSPI'].sort_values('Marcap', ascending=False).head(200)
        df_kosdaq = df_krx[df_krx['Market'] == 'KOSDAQ'].sort_values('Marcap', ascending=False).head(150)
        df_target = pd.concat([df_kospi, df_kosdaq], ignore_index=True)
    except Exception as e:
        print(f"FDR 데이터 수집 실패: {e}")
        return

    print("2. KRX KIND 시스템에서 업종 정보 상세 수집 중...")
    try:
        # KIND에서 업종 정보가 포함된 상장법인 목록 직접 호출
        url = 'https://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
        resp = requests.get(url)
        resp.encoding = 'cp949' # 한국거래소 표준 인코딩
        df_kind = pd.read_html(resp.text, header=0)[0]
        
        # 병합을 위한 컬럼 정리
        df_kind = df_kind[['회사명', '종목코드', '업종', '주요제품']]
        df_kind['종목코드'] = df_kind['종목코드'].astype(str).str.zfill(6)
    except Exception as e:
        print(f"KIND 데이터 수집 실패: {e}")
        return
    
    print("3. 데이터 병합 및 구조화 진행 중...")
    # 종목코드를 기준으로 시장 데이터와 업종 데이터 병합
    df_final = pd.merge(df_target, df_kind, left_on='Code', right_on='종목코드', how='left')
    
    # 최종 컬럼 선정 및 이름 변경
    df_final = df_final[['Name', 'Market', '업종', '주요제품', 'Close', 'Marcap', 'Code']]
    df_final = df_final.rename(columns={
        'Name': '종목명',
        'Market': '시장',
        '업종': '업종',
        '주요제품': '세부업종',
        'Close': '현재가',
        'Marcap': '시가총액',
        'Code': '코드'
    })
    
    # 천단위 콤마 포맷팅
    df_final['현재가'] = df_final['현재가'].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "")
    df_final['시가총액'] = df_final['시가총액'].apply(lambda x: f"{int(x):,}" if pd.notnull(x) else "")
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 4. 토큰 다이어트를 위한 AI 요약 메타데이터 생성
    summary_info = {
        'total_count': len(df_final),
        'kospi_count': len(df_kospi),
        'kosdaq_count': len(df_kosdaq),
        'top_5': df_final['종목명'].head(5).tolist(),
        'sectors': df_final['업종'].value_counts().head(5).to_dict()
    }
    
    print("4. 마크다운 리포트 생성 중...")
    # 마크다운 테이블 변환
    markdown_table = df_final.to_markdown(index=False)
    
    # AI가 토큰을 아끼며 읽을 수 있는 요약 헤더 삽입
    summary_header = f"""<!-- AI_SUMMARY_START
{{
  "updated_at": "{today}",
  "total_stocks": {summary_info['total_count']},
  "market_split": "KOSPI 200 / KOSDAQ 150 (Proxy by Marcap)",
  "top_companies": {summary_info['top_5']},
  "major_sectors": {list(summary_info['sectors'].keys())}
}}
AI_SUMMARY_END -->"""

    content = f"""# KOSPI 200 & KOSDAQ 150 구조화 데이터

{summary_header}

> **시스템 안내**: 이 파일은 `tools/update_kr_market.py`에 의해 자동 관리됩니다. 
> 한국거래소(KRX)의 시가총액 순위와 KIND 업종 분류를 결합한 데이터입니다.
> **최종 업데이트**: {today}

## 📊 시장 요약 (AI 브리핑)
- **대상 범위**: KOSPI 200 및 KOSDAQ 150 (시총 상위 기준 대용치)
- **주요 섹터 분포**: {', '.join(list(summary_info['sectors'].keys()))}
- **상위 5대 종목**: {', '.join(summary_info['top_5'])}

---

## 📋 상세 종목 리스트

{markdown_table}
"""

    output_path = "raw/research/market_structure.md"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 업데이트 완료: {output_path} (총 {len(df_final)}개 종목)")

if __name__ == "__main__":
    update_market_stucture()
