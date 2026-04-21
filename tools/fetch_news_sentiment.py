import warnings
# 경고 메시지 무시 (특히 google-generativeai의 지원 중단 경고)
warnings.filterwarnings("ignore", category=FutureWarning)

import os
import json
import requests
import feedparser
from datetime import datetime
import sys
import re
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

def fetch_naver_news(client_id, client_secret, query, display=50):
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    params = {
        "query": query,
        "display": display,
        "sort": "sim"
    }
    
    try:
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code == 200:
            items = resp.json().get('items', [])
            return [{"title": re.sub(r'<[^>]*>', '', item['title']), "link": item['link']} for item in items]
        else:
            print(f"⚠️ 네이버 API 오류: {resp.status_code}")
            return []
    except Exception as e:
        print(f"⚠️ 네이버 수집 중 예외 발생: {e}")
        return []

def fetch_rss_news(rss_urls):
    headlines = []
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:20]:
                headlines.append({"title": entry.title, "link": entry.link})
        except Exception as e:
            print(f"⚠️ RSS 수집 오류 ({url}): {e}")
    return headlines

def clean_headlines(headlines):
    seen = set()
    unique = []
    noise_keywords = ["[포토]", "게시판", "인사", "부고", "재배포 금지"]
    
    for h in headlines:
        clean_title = h['title'].strip()
        if clean_title in seen:
            continue
        if any(nk in clean_title for nk in noise_keywords):
            continue
        seen.add(clean_title)
        unique.append(h)
    return unique

def analyze_with_gemini(api_key, headlines):
    """Gemini API를 사용하여 뉴스 헤드라인을 분석합니다."""
    print("4. Gemini AI를 통한 시장 심리 분석 중...")
    genai.configure(api_key=api_key)
    # 환경에 따라 모델명이 다를 수 있으므로 안정적인 'gemini-flash-latest' 사용
    model = genai.GenerativeModel('gemini-flash-latest')
    
    headlines_text = "\n".join([f"- {h['title']}" for h in headlines])
    
    prompt = f"""
다음은 오늘자 주식 시장 관련 뉴스 헤드라인들입니다. 이를 분석하여 투자에 도움이 되는 심리적 데이터와 테마를 추출해주세요.

[뉴스 헤드라인]
{headlines_text}

[요구사항]
1. 오늘 시장의 '심리 점수'를 1점(매우 비관)에서 10점(매우 낙관) 사이로 책정하고 짧은 이유를 적어주세요.
2. 오늘 뉴스에서 가장 두드러지는 '주요 테마 3-5개'를 뽑아주세요.
3. 전체 뉴스를 관통하는 '핵심 키워드' 5~7개를 리스트업 해주세요.
4. 결과는 반드시 한국어 Markdown 형식으로 출력해주세요.
5. 출력 형식의 시작은 아래와 같은 YAML Frontmatter를 포함해야 합니다:
---
date: {datetime.now().strftime("%Y-%m-%d")}
type: news_sentiment
sentiment_score: [점수]
leading_themes: ["테마1", "테마2", ...]
---
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"⚠️ Gemini 분석 중 오류 발생: {e}")
        return None

def fetch_news_sentiment():
    today = datetime.now().strftime("%Y-%m-%d")
    config = load_config()
    if not config:
        return

    print(f"[{today}] 뉴스 수집 및 자율 분석 시작...")
    
    all_headlines = []
    client_id = config['naver_api']['client_id']
    client_secret = config['naver_api']['client_secret']
    queries = ["주식 특징주", "국내 증권 시장"]
    
    for q in queries:
        all_headlines.extend(fetch_naver_news(client_id, client_secret, q))
    
    all_headlines.extend(fetch_rss_news(config['rss_feeds']))
    cleaned = clean_headlines(all_headlines)
    print(f"3. 데이터 정제 완료 (총 {len(cleaned)}개 헤드라인)")

    # 1. Raw 데이터 저장
    output_dir = "raw/research/news"
    os.makedirs(output_dir, exist_ok=True)
    raw_path = os.path.join(output_dir, f"{today}_news_raw.md")
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(f"# {today} 수집 뉴스 원본 리스트\n\n")
        for i, h in enumerate(cleaned, 1):
            f.write(f"{i}. {h['title']} ([링크]({h['link']}))\n")
    
    # 2. Gemini 자율 분석
    gemini_key = config.get('gemini_api', {}).get('key')
    if gemini_key:
        analysis_report = analyze_with_gemini(gemini_key, cleaned)
        if analysis_report:
            analysis_path = os.path.join(output_dir, f"{today}_news_sentiment.md")
            with open(analysis_path, "w", encoding="utf-8") as f:
                f.write(analysis_report)
            print(f"✅ AI 분석 완료: {analysis_path}")
        else:
            print("⚠️ AI 분석 보고서 생성 실패")
    else:
        print("⚠️ Gemini API 키가 설정되지 않아 자율 분석을 건너뜜")

if __name__ == "__main__":
    fetch_news_sentiment()
