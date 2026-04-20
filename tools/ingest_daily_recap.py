import os
import re
import yaml
from datetime import datetime
import sys

# 출력 인코딩 설정 (Windows 대응)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def parse_yaml_from_md(file_path):
    """마크다운 파일에서 YAML Frontmatter를 추출합니다."""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        match = re.search(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if match:
            return yaml.safe_load(match.group(1))
    return {}

def update_wiki_index(date_str, title):
    """위키 인덱스 및 로그를 업데이트합니다."""
    log_path = "wiki/log.md"
    index_path = "wiki/index.md"
    
    # 1. Log Update
    log_entry = f"| {date_str} | Market | {title} | [Link]({date_str}_Market_Recap.md) | 완료 |\n"
    if os.path.exists(log_path):
        with open(log_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    # 2. Index Update (간소화된 로직 - 최근 5개 항목 유지 등은 생략)
    # 실제로는 특정 섹션에 추가하는 로직이 필요할 수 있음

def ingest_daily_recap():
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"[{today}] 위키 데일리 리캡 합성 시작...")

    trend_file = f"raw/research/trends/{today}_dynamic_trend.md"
    macro_file = f"raw/research/macro/{today}_macro_status.md"

    trend_meta = parse_yaml_from_md(trend_file)
    macro_meta = parse_yaml_from_md(macro_file)

    if not trend_meta and not macro_meta:
        print("수집된 데이터가 없습니다. 먼저 데이터 수집 스크립트를 실행하세요.")
        return

    # 합성 리포트 생성
    wiki_path = f"wiki/{today}_Market_Recap.md"
    
    # 등락 화살표 로직 (단순 구현)
    vix_status = "⚠️ 주의" if macro_meta.get('vix', 0) > 20 else "🟢 안정"
    exchange_status = "⚠️ 고환율" if macro_meta.get('usd_krw', 0) > 1350 else "🟢 양호"

    content = f"""---
date: {today}
tags: [market_pulse, macro, flow]
---
# {today} 주식 시장 데일리 리캡 (Double Brain)

## 📌 주요 시장 코멘트
- **시장 심리**: {vix_status} (VIX: {macro_meta.get('vix')})
- **수급 환경**: {exchange_status} (환율: {macro_meta.get('usd_krw')})
- **주도 테마**: {', '.join(trend_meta.get('leading_sectors', [])) if trend_meta.get('leading_sectors') else '탐지되지 않음'}

---

## 🌎 글로벌 매크로 & 리스크
| 항목 | 수치 | 상태 |
| :--- | :--- | :--- |
| **원/달러 환율** | {macro_meta.get('usd_krw')} | {exchange_status} |
| **VIX 지수** | {macro_meta.get('vix')} | {vix_status} |
| **미국 10년물** | {macro_meta.get('us_10y')}% | - |
| **WTI 유가** | ${macro_meta.get('oil_wti')} | - |

---

## ⚡ 동적 자금 동향 (Flow Top Pick)
금일 거래대금이 폭발하며 상승한 주요 종목 리스트입니다. (자세한 내용은 [[{today}_dynamic_trend.md|상세 파일]] 참조)

- **수급 집중 종목**: {trend_meta.get('trend_count')}개 발견
- **대장주**: {trend_meta.get('top_amount_stock')}

---

## 🔗 연관 지식 엔진
- [[시장 주도 테마 히스토리]]
- [[자금 흐름 분석 (Money Flow Analysis)]]
- [[섹터 분석 (Sector Analysis)]]

---
> **AI 가이드**: 이 리포트는 자동화된 분석 엔진에 의해 생성되었습니다. 
> 상세한 종목 분석이 필요하면 위키 내 각 종목 엔티티를 참조하세요.
"""

    with open(wiki_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    update_wiki_index(today, "주식 시장 데일리 리캡")
    print(f"✅ 위키 인제스트 완료: {wiki_path}")

if __name__ == "__main__":
    ingest_daily_recap()
