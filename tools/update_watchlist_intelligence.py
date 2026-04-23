import os
import json
import requests
import re
import sys
from datetime import datetime
import google.generativeai as genai

# 출력 인코딩 설정 (Windows 대응)
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    if not os.path.exists(config_path):
        print(f"❌ 설정 파일을 찾을 수 없습니다: {config_path}")
        return None
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_watchlist():
    watchlist_path = "raw/notes/관심종목.md"
    if not os.path.exists(watchlist_path):
        print(f"❌ 관심종목 파일을 찾을 수 없습니다: {watchlist_path}")
        return {}

    with open(watchlist_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 섹터별 종목 파싱 (정규표현식 활용)
    sectors = {}
    sector_blocks = re.split(r'## [^ ]+ 섹터 \d+: ', content)[1:]
    sector_names = re.findall(r'## [^ ]+ 섹터 \d+: ([^( \n]+)', content)

    for name, block in zip(sector_names, sector_blocks):
        # 테이블에서 종목명 추출 ( | 1 | 종목명 | 코드 | ... )
        stocks = re.findall(r'\| \d+ \| ([^|]+) \| ([^|]+) \|', block)
        sectors[name.strip()] = [{"name": s[0].strip(), "code": s[1].strip()} for s in stocks]
    
    return sectors

def fetch_naver_news(client_id, client_secret, query, display=10):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {
        "query": query,
        "display": display,
        "sort": "sim" # 정확도순으로 가져와서 노이즈 제거
    }
    
    try:
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code == 200:
            items = resp.json().get('items', [])
            return [{"title": re.sub(r'<[^>]*>', '', item['title']), "link": item['link']} for item in items]
        return []
    except Exception:
        return []

def analyze_watchlist_sentiment(api_key, sector_data):
    """섹터별 수집된 뉴스를 Gemini로 분석합니다."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 분석 대상 텍스트 구성
    context_text = ""
    for sector, news_list in sector_data.items():
        if not news_list: continue
        context_text += f"\n### 섹터: {sector}\n"
        for item in news_list:
            context_text += f"- [{item['stock']}] {item['title']}\n"

    if not context_text:
        return "오늘 내 관심 종목과 관련된 특이 뉴스가 발견되지 않았습니다."

    prompt = f"""
당신은 전문 주식 분석가입니다. 아래는 사용자의 '관심 종목 86개' 중 오늘 뉴스가 포착된 종목들입니다.
눌림목 매매 전략(1~5일 스윙) 관점에서 어떤 종목이 오늘 '기회' 혹은 '리스크'가 있는지 분석해주세요.

[오늘의 관심주 뉴스]
{context_text}

[요구사항]
1. **Highlight**: 오늘 가장 강력한 모멘텀이 발생한 종목 3개를 뽑아 이유를 설명하세요.
2. **Caution**: 악재성 공시나 뉴스가 뜬 종목이 있다면 주의 사항을 적어주세요.
3. **Sector Flow**: 현재 어느 섹터로 수급이 몰리는지 분석하세요.
4. **Action Plan**: 내일 장에서 주목해야 할 매매 시나리오를 짧게 제안하세요.
5. 반드시 한국어 Markdown 형식으로 작성하세요.

출력 시작은 반드시 아래 YAML Frontmatter를 포함하세요:
---
date: {today}
type: watchlist_intelligence
hot_stocks: [종목1, 종목2, ...]
---
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ 분석 중 오류 발생: {e}"

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    config = load_config()
    if not config: return

    print(f"🚀 [{today}] 관심종목 인텔리전스 가동...")
    
    # 1. 관심종목 로드
    sectors = parse_watchlist()
    if not sectors: return
    
    client_id = config['naver_api']['client_id']
    client_secret = config['naver_api']['client_secret']
    
    # 2. 종목별 뉴스 검색 (토큰 다이어트: 종목별 3개씩만)
    print("🔍 관심종목 뉴스 필터링 중 (86개 종목 스캐닝)...")
    sector_news_map = {}
    total_found = 0
    
    for sector, stocks in sectors.items():
        sector_news_map[sector] = []
        for stock in stocks:
            # 검색어 최적화: "종목명 주가" or "종목명 특징주"
            news = fetch_naver_news(client_id, client_secret, f"{stock['name']} 특징주", display=3)
            if news:
                for n in news:
                    n['stock'] = stock['name']
                    sector_news_map[sector].append(n)
                    total_found += 1
        print(f"   - {sector} 섹터 완료")

    print(f"✅ 필터링 완료: 총 {total_found}개의 관련 뉴스 포착")

    # 3. Gemini 자율 분석
    gemini_key = config.get('gemini_api', {}).get('key')
    if gemini_key and total_found > 0:
        report = analyze_watchlist_sentiment(gemini_key, sector_news_map)
        
        # 4. 리포트 저장
        output_dir = "raw/research/watchlist"
        os.makedirs(output_dir, exist_ok=True)
        report_path = os.path.join(output_dir, f"{today}_Watchlist_Alerts.md")
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"✨ 분석 보고서 생성 완료: {report_path}")
    else:
        print("💡 분석할 만한 특이 사항이 없습니다.")

if __name__ == "__main__":
    main()
