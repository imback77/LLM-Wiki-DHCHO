import os
import sys
import time
import json
import pandas as pd
import google.generativeai as genai

# Fix Windows encoding issue for emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Add the dashboard path to sys.path
dashboard_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dashboard_path)

from services.kis_api import KisApi
from services.wiki_parser import WikiParser

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def run_technical_scan():
    print("🚀 [Step 1] KIS API 통합시세(KRX+NXT) 기반 수학적 눌림목 스캐닝 시작...")
    
    api = KisApi()
    if not api.get_access_token():
        print("❌ KIS API 토큰 발급 실패. 스크립트를 종료합니다.")
        return []

    wiki_path = os.path.abspath(os.path.join(dashboard_path, '..'))
    parser = WikiParser(wiki_path)
    stocks = parser.get_tracked_stocks()
    
    candidates = []
    all_status = []
    
    for i, stock in enumerate(stocks):
        code = stock['code']
        print(f"[{i+1}/{len(stocks)}] {stock['name']} 분석 중...", end='\r')
        
        df = api.get_historical_prices(code)
        time.sleep(0.06) # Rate limit protection
        
        if df.empty or len(df) < 20:
            continue
            
        # Calculate Technical Indicators
        df['20MA'] = df['close'].rolling(window=20).mean()
        df['RSI'] = calculate_rsi(df['close'], period=14)
        
        latest = df.iloc[-1]
        close_price = latest['close']
        ma20 = latest['20MA']
        rsi = latest['RSI']
        
        # Calculate change rate from previous day
        if len(df) >= 2:
            prev_close = df.iloc[-2]['close']
            change_rate = ((close_price - prev_close) / prev_close) * 100
        else:
            change_rate = 0.0
            
        # Save to global status dict
        all_status.append({
            'name': stock['name'],
            'code': code,
            'sector': stock['sector'],
            'close': int(close_price),
            'change_rate': round(change_rate, 2),
            'volume': int(latest['volume'])
        })
        
        if pd.isna(ma20) or pd.isna(rsi):
            continue
            
        # 1차 필터링 조건: 주가가 20일선 근처(±3% 이내)이거나 과매도(RSI < 45) 구간인 경우
        dist_to_ma = abs(close_price - ma20) / ma20
        if dist_to_ma <= 0.03 or rsi < 45:
            candidates.append({
                'name': stock['name'],
                'code': code,
                'sector': stock['sector'],
                'close_price': close_price,
                'ma20': ma20,
                'rsi': rsi,
                'momentum': stock.get('entry_reason', '')
            })
            
    # Save the global status to JSON
    status_path = os.path.join(dashboard_path, 'data', 'watchlist_status.json')
    with open(status_path, 'w', encoding='utf-8') as f:
        json.dump(all_status, f, ensure_ascii=False, indent=4)
        
    print(f"\n✅ [Step 1 완료] 총 {len(candidates)}개의 1차 눌림목 후보군 도출 성공.")
    return candidates

def run_ai_prediction(candidates):
    if not candidates:
        print("❌ 1차 후보군이 없습니다.")
        return
        
    print(f"\n🧠 [Step 2] Gemini AI에게 내일의 타겟 종목(Top 3) 및 타점 예측 의뢰 중...")
    
    # Load Gemini config
    config_path = os.path.join(dashboard_path, '..', 'tools', 'config.json')
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
        api_key = config.get("gemini_api", {}).get("key")
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-flash-latest')
    
    candidates_text = ""
    for c in candidates:
        candidates_text += f"- [{c['sector']}] {c['name']} (현재가: {int(c['close_price']):,}원, 20일선: {int(c['ma20']):,}원, RSI: {c['rsi']:.1f})\n"
        candidates_text += f"  모멘텀: {c['momentum']}\n"
        
    prompt = f"""
    당신은 딥러닝 기반의 최상위 주식 트레이더입니다. 
    오늘 오후 8시 NXT(Nextrade) ATS 거래까지 마감된 후, 기술적으로 눌림목(20일선 근접 또는 과매도)에 도달한 후보군 {len(candidates)}개입니다.
    
    [후보군 데이터]
    {candidates_text}
    
    [요청 사항]
    위 후보군 중 내일 장(익일)에서 반드시 노려야 할 **최선호 타겟 종목 3개**를 선정해 주세요.
    응답은 반드시 아래 JSON 포맷으로만 작성해주세요. (다른 설명은 절대 금지)
    
    [
      {{
        "code": "종목코드(6자리)",
        "name": "종목명",
        "predicted_entry_price": 내일 노려볼 매수 진입가(숫자),
        "predicted_target_price": 1차 단기 목표가(숫자),
        "rationale": "이 가격을 진입가로 설정한 이유 및 상승 모멘텀 (2문장 이내)"
      }}
    ]
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Remove markdown code block wrappers if any
        if text.startswith("```json"):
            text = text[7:-3]
        elif text.startswith("```"):
            text = text[3:-3]
            
        targets = json.loads(text.strip())
        
        # Save to targets.json
        out_path = os.path.join(dashboard_path, 'data', 'ai_targets.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(targets, f, ensure_ascii=False, indent=4)
            
        print(f"✅ [Step 2 완료] AI가 선정한 내일의 타겟 종목이 {out_path}에 저장되었습니다!")
        for t in targets:
            print(f"🎯 {t['name']}: 진입가 {t['predicted_entry_price']:,}원 -> 목표가 {t['predicted_target_price']:,}원")
            
            # Auto-generate or update the markdown file in the Wiki root
            md_path = os.path.join(dashboard_path, '..', f"{t['name']}.md")
            if os.path.exists(md_path):
                import frontmatter
                with open(md_path, 'r', encoding='utf-8') as fm_file:
                    post = frontmatter.load(fm_file)
                
                post.metadata['종목코드'] = t['code']
                post.metadata['진입가'] = t['predicted_entry_price']
                post.metadata['목표가1'] = t['predicted_target_price']
                post.metadata['진입가_선정이유'] = t['rationale']
                
                with open(md_path, 'w', encoding='utf-8') as fm_file:
                    fm_file.write(frontmatter.dumps(post))
            else:
                content = f"""---
종목코드: '{t['code']}'
진입가: {t['predicted_entry_price']}
목표가1: {t['predicted_target_price']}
진입가_선정이유: "{t['rationale']}"
추적상태: "추적중"
---

# {t['name']}
> 이 문서는 `batch_scanner.py`에 의해 자동 생성된 AI 타겟 종목 문서입니다.

## 🎯 AI 선정 이유
{t['rationale']}

---
*장중 실시간 대시보드의 Target Dips 레이더망에서 진입가 도달 여부를 감시합니다.*
"""
                with open(md_path, 'w', encoding='utf-8') as fm_file:
                    fm_file.write(content)
            
            print(f"   => 📄 {t['name']}.md 위키 문서 자동 업데이트 완료!")
            
    except Exception as e:
        print(f"❌ AI 예측 중 오류 발생: {e}")
        print("Raw response:", response.text)

if __name__ == "__main__":
    cands = run_technical_scan()
    run_ai_prediction(cands)
