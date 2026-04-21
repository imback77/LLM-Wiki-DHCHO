
import json
import difflib
import os

# Source files
broken_links_file = r"d:\LLM Wiki DHCHO\scratch\unique_broken_links.txt"
valid_filenames_file = r"d:\LLM Wiki DHCHO\scratch\valid_filenames.txt"

# Read lists
with open(valid_filenames_file, 'r', encoding='utf-8') as f:
    valid_names = [line.strip() for line in f if line.strip()]

# Re-read unique broken links if I didn't save them yet.
# I'll just use the list from the previous output.
broken_links = [
    "???략 (Wheel Strategy)", "????주식 ?장", "????주식 ?장 구조", "?이???널_AI",
    "?이?보안 ?렌??2026", "?이?센??(Data Center)", "?이?센???너지 병목", "?롬?트_?젝??방어",
    "?용 ?력??략", "?키링크", "?험 ?계?? (Danger Threshold)", "?험 ?계??Danger Threshold)",
    "?종??스 ?향??분석", "?수???스", "?수???스 (ISU Petasys)", "?거???프??보안",
    "?인보우로보?스", "?버?AI (Sovereign AI)", "?금 ?름 분석 (Money Flow Analysis)",
    "?동???자 분석", "?동???자 분석 (Automated Investment Analysis)", "?율주행", "?이?틱 AI",
    "?이?틱 AI ?율??5?계", "?이?틱 경제", "?도 (India)", "?럼???정부", "?업??AI",
    "?업??AI (Collaborative AI)", "?터 분석 (Sector Analysis)", "?로 ?리?어 (Solopreneur)",
    "?로_?리?어", "?????료", "?스?리?????WSJ)", "?노_바나??2", "?노_바나??2 (Nano Banana 2)",
    "?앤?프", "?이?스케?러", "?이?클로바X", "?이브리???자-AI", "???AI", "?성?자",
    "?성?자 (Samsung Electronics)", "?성SDI", "?마??공정 (Smart Process)", "?이?(Naver)",
    "?적 증명", "?국거래??KRX)", "???이_3.1", "??개발??구씨", "?림?큐리티",
    "?로?이 취약??(Zero-Day Vulnerability)", "?장 주도 ?마 ?스?리", "1??기업",
    "2026-04-15_'미소??가 무서???유 27???안 ?어?던 문제???로",
    "2026-04-16_?로?트??떻??성?고 관리할 ???나??md",
    "2026-04-16_?로??초보 ?용???3분만???내?요 2026 ?전 가?드_?이? ?이?는 AI? ?커머스",
    "2026-04-16_?로??초보??가?드 2026  ???상 ?나??내?요._그린코끼?AI",
    "2026-04-16_??개발??구씨 LLM Wiki GitHub Repo",
    "2026-04-16_??개발??구씨???로?코??LLM Wiki ?리",
    "2026-04-16_Claude ?킬 구축 가?드", "2026-04-16_Google DeepMind SIMA 2 ?이?트",
    "2026-04-16_Google Gemma 4 ?픈?스 모델", "2026-04-16_Perplexity ?이?트 ?랫???벗",
    "2026-04-16_Perplexity, 검?엔진에??AI ?이?트 ?랫?으??벗",
    "2026-04-16_Project Glasswing Anthropic 주도 ?프?웨??보안 ??합",
    "2026-04-16_The-Complete-Guide-to-Building-Skill-for-Claude",
    "2026-04-16_미소??Claude Mythos)가 무서???유", "2026-04-17_Claude Code Design just became UNSTOPPABLE",
    "2026-04-17_Claude Just Changed the Stock Market Forever",
    "2026-04-18_?이?보안?'?험 ?계?? Project Glasswing 출범",
    "2026-04-18_?로???자???토리얼", "2026-04-18_?로???산??극???방법",
    "2026-04-18_AI ?력 공급 가?성 충격 (Power Availability Shock)",
    "2026-04-18_AI ?프???력?관??? 종목.md", "2026-04-18_AI Trading Team with Claude Code",
    "2026-04-18_AI_?용_?황.md", "2026-04-18_Claude Design Anthropic Labs 출시.md",
    "2026-04-19_?????공지???동계획(??.md", "2026-04-19_5 Claude Code skills I use every single day_Matt Pocock.md",
    "2026-04-19_5_Claude_Code_Skills_Matt_Pocock", "2026-04-19_AI_Regulation_Trump_vs_Florida_Special_Session.md",
    "2026-04-19_Andrej_Karpathy_LLM_Wiki_?본_번역", "2026-04-19_Andrej_Karpathy_LLM_Wiki_?본_번역.md",
    "2026-04-19_Anthropic_Claude_Mythos_Security_Implications.md",
    "2026-04-19_AWS_Pearson_AI_Readiness_Report.md", "2026-04-19_dynamic_trend.md",
    "2026-04-19_Lumen_Technologies_CEO_Open_Letter_AI_Agents.md",
    "2026-04-19_PwC_AI_Performance_Study_Economic_Divide.md",
    "2026-04-19_Samsung_Edison_Awards_2026_AI_Innovations.md",
    "2026-04-19_Shift_to_Agentic_AI_Autonomy_Levels.md", "2026-04-19_TSMC_Arizona_Expansion_AI_Chips.md",
    "2026-04-19_US_Tech_AI_Infrastructure_ROI_Anxiety.md",
    "2026-04-19_Zebra_Technologies_Aiva_Health_AI_Nurse_Assistant.md",
    "2026-04-20_?장 ?금 ?향 분석 보안 SW ?반도??비???주", "2026-04-20_Global_Macro_Snapshot",
    "2026-04-20_Market_Flow_Analysis", "2026-04-20_Self_Host_Gemma_4_Cloud_Run",
    "2026-04-20_Vibe_Coding_and_Solo_Business",
    "2026-04-21_?이??도_TCS_?략???트?십_분석", "2026-04-21_dynamic_trend.md",
    "2026-04-21_news_sentiment.md", "2026-04-21_구?_???이_???롬_?_출시_분석",
    "Agentic AI", "Agentic AI (?이?틱 AI)", "AGI", "AI ?자 ?", "AI ?자 ? (AI Trading Team)",
    "AI ?구 경쟁", "AI ?일???랩", "AI ?극??(AI Polarization)", "AI ?리? ?식",
    "AI Readiness", "AI 거버?스", "AI 거버?스 (AI Governance)", "AI 바이???신??자 기회",
    "AI 준비도 (AI Readiness)", "AI??공격 방어 비??", "AI??공격·방어 비??", "Amazon",
    "Anthropic (?트로픽)", "Anthropic Labs", "ANTIGRAVITY", "AWS", "AX",
    "AX (AI Transformation, AI ??환)", "Backlink", "Bugmageddon", "CapEx", "CHIPS Act",
    "Claude Design", "Claude Mythos (?로??미소??", "Claude Mythos 5", "Claude.ai", "COBOL",
    "CoWoS", "Cursor", "Gemini 3.1", "Gemma 4", "Google", "Grill me (?롬?트 기법)",
    "HD???렉?릭", "HD???렉?릭 (HD Hyundai Electric)", "Kate Johnson", "Llama",
    "LLM Wiki ?턴", "LS?렉?릭", "market_structure.md", "Meta", "Microsoft",
    "OpenAI GPT-5.4-Cyber", "Palantir", "Pearson", "PRD", "Project Glasswing", "PwC",
    "raw/articles/2026-04-21_?이? ?도 거? IT기업 ?? 컨설?과 MOU?AI·?라?드·B2C ?? 결합",
    "raw/research/trends/2026-04-20_dynamic_trend.md", "raw/videos/_바이브코??코너_?로?리?어.md",
    "raw/videos/_카파?의 LLM Wiki...브레???리?티.md", "ROI Gap", "ROI Gap (?자 ???익 격차)",
    "SIMA 2", "SK?이?스", "Skills Gap", "TCS (Tata Consultancy Services)", "TDD",
    "wiki/2026-04-17_Google_DeepMind_Robotics_Philosopher", "wiki/2026-04-17_OpenAI_GPT-Rosalind_Cyber",
    "wiki/2026-04-18_?업??AI로의 ?환", "wiki/2026-04-18_?자 컴퓨?과 AI???합",
    "wiki/2026-04-18_AI ?프?? 물리???계", "Zero-Day Clock", "???공지?전?위?회", "구리",
    "공간 지?화", "공간 지?화 (Spatial Intelligence)", "그린코끼?AI", "개인지???(PKM)",
    "멀???이?트 ???트?이??(Multi-Agent Orchestration)", "변?기", "비전 AI 컴패?언",
    "보안 ?프?웨??(Security Software)", "브라??_?합_AI", "문화??부?(Cultural Debt)",
    "바이?코딩", "바이?코딩 (Vibe Coding)", "물리???계", "물리???계 (Physical Limits)",
    "로보?스 AI", "지??관?(Knowledge Management)", "지??복리 (Knowledge Compounding)",
    "코드 기반 ?자??(Code-based Design)", "코드 기반 UI ?성", "주성???어?(Jusung Engineering)",
    "최첨???키?(Advanced Packaging)"
]

mapping = {}

def clean(s):
    # Remove ?, ? and other artifacts to fuzzy match
    res = s.replace('?', '').replace('??', '').replace('?', '').replace('', '')
    return res

for link in broken_links:
    cleaned_link = clean(link)
    if not cleaned_link: continue
    
    # Simple direct match if substring
    matches = [name for name in valid_names if cleaned_link in name]
    
    if matches:
        # Sort by length similarity
        matches.sort(key=lambda x: abs(len(x) - len(link)))
        mapping[link] = matches[0]
    else:
        # Fuzzy match
        close_matches = difflib.get_close_matches(cleaned_link, valid_names, n=1, cutoff=0.3)
        if close_matches:
            mapping[link] = close_matches[0]

# Special overrides
overrides = {
    "??개발??구씨": "시민개발자 구씨",
    "?동???자 분석": "자동화 투자 분석",
    "?이?보안 ?렌??2026": "사이버 보안 트렌드 2026",
    "?버?AI (Sovereign AI)": "AX (AI Transformation, AI 대전환)",
    "?이?틱 AI": "Agentic AI (에이전틱 AI)",
    "?이?(Naver)": "네이버",
    "?국거래??KRX)": "KOSPI 200", 
    "???이_3.1": "Gemini",
    "?적 증명": "지식 복리 (Knowledge Compounding)",
    "???략 (Wheel Strategy)": "휠 전략 (Wheel Strategy)",
    "?이?클로바X": "하이퍼클로바X" # Wait, checking if 하이퍼클로바X is in valid_names
}

mapping.update(overrides)

with open(r"d:\LLM Wiki DHCHO\scratch\link_mapping.json", 'w', encoding='utf-8') as f:
    json.dump(mapping, f, indent=4, ensure_ascii=False)
