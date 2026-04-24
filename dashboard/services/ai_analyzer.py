import os
import json
import google.generativeai as genai

class AiAnalyzer:
    def __init__(self, root_path: str):
        # Read the gemini api key from tools/config.json
        config_path = os.path.join(root_path, "tools", "config.json")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                api_key = config.get("gemini_api", {}).get("key")
                if api_key:
                    genai.configure(api_key=api_key)
                    self.model = genai.GenerativeModel('gemini-flash-latest')
                    self.is_configured = True
                else:
                    self.is_configured = False
        except Exception as e:
            print(f"Error loading Gemini config: {e}")
            self.is_configured = False

    def get_dip_analysis(self, stock_name: str, stock_code: str, entry_price: float, current_price: float, sector: str, wiki_content: str) -> str:
        if not self.is_configured:
            return "⚠️ Gemini API가 설정되지 않았습니다. `tools/config.json`을 확인해주세요."

        prompt = f"""
        당신은 전문 주식 트레이더이자 AI 애널리스트입니다.
        현재 '{stock_name}({stock_code})' 종목이 사용자가 설정한 진입가(눌림목)에 도달했습니다.
        아래 정보를 바탕으로 현재 진입이 유효한지, 기술적/펀더멘털 관점에서 짧고 굵게 코멘트해주세요.

        [종목 정보]
        - 섹터: {sector}
        - 목표 진입가: {entry_price:,}원
        - 현재가: {current_price:,}원
        
        [위키에 기록된 최근 인사이트 요약]
        {wiki_content}

        [요청 사항]
        1. 현재 가격대에서의 매수 매력도 (1~5점)
        2. 해당 섹터의 최근 모멘텀을 고려한 리스크 요인 1가지
        3. 단기 트레이딩 전략 제안 (1~3문장)
        """

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ AI 분석 중 오류 발생: {e}"
