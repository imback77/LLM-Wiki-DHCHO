import streamlit as st
import os
import sys
import pandas as pd
import textwrap

# Add the dashboard path to sys.path so we can import services
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from services.wiki_parser import WikiParser
from services.kis_api import KisApi, SectorAnalyzer

st.set_page_config(page_title="LLM Wiki x KIS Dashboard", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for Dark Mode & Glassmorphism ---
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    * { font-family: 'Pretendard', 'Inter', sans-serif; }
    .glass-card {
        background: rgba(22, 27, 34, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .glass-card:hover { transform: translateY(-5px); border-color: rgba(0, 230, 118, 0.5); }
    .stock-name { font-size: 1.5rem; font-weight: 700; margin-bottom: 5px; color: #ffffff; }
    .stock-code { color: #8b949e; font-size: 0.9rem; }
    .sector-badge { background-color: #1f6feb; color: white; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; font-weight: 600; display: inline-block; margin-bottom: 10px; }
    .price-label { font-size: 0.9rem; color: #8b949e; margin-top: 10px; }
    .price-value { font-size: 1.2rem; font-weight: 600; color: #e6edf3; }
    .price-value.profit { color: #00E676; }
    .price-value.loss { color: #FF1744; }
    .reasoning { font-size: 0.85rem; color: #a5d6ff; background: rgba(165, 214, 255, 0.1); padding: 8px; border-radius: 6px; margin-top: 5px; border-left: 3px solid #1f6feb; }
    .dip-alert { border: 2px solid #00E676; box-shadow: 0 0 15px rgba(0, 230, 118, 0.3); }
    .sidebar .sidebar-content { background-color: #161b22; }
</style>
""", unsafe_allow_html=True)

# --- Data Fetching ---
@st.cache_data(ttl=60, show_spinner=False)
def load_wiki_data():
    wiki_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    parser = WikiParser(wiki_path)
    return parser.get_tracked_stocks()

@st.cache_data(ttl=10, show_spinner=False) # Refresh API data frequently
def load_live_targets(target_codes):
    """Fetches real-time KIS API data ONLY for the selected AI targets."""
    api = KisApi()
    is_connected = api.get_access_token()
    if not is_connected:
        return False, {}
    prices = api.get_bulk_prices(target_codes)
    return is_connected, prices

@st.cache_data(ttl=60, show_spinner=False)
def load_static_status():
    """Reads the static daily closing prices and change rates from the batch scanner."""
    import json
    status_path = os.path.join(os.path.dirname(__file__), 'data', 'watchlist_status.json')
    if os.path.exists(status_path):
        with open(status_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

loader_placeholder = st.empty()
loader_placeholder.markdown("""
<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; height: 50vh;">
    <div class="custom-loader"></div>
    <div style="margin-top: 20px; color: #a0aec0; font-family: 'Inter', sans-serif; letter-spacing: 2px;">SYNCING MARKET DATA...</div>
    <style>
    .custom-loader {
      border: 4px solid rgba(255, 255, 255, 0.1);
      border-left-color: #00ffcc;
      border-radius: 50%;
      width: 50px;
      height: 50px;
      animation: spin 1s linear infinite;
    }
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    </style>
</div>
""", unsafe_allow_html=True)

stocks = load_wiki_data()
static_status = load_static_status()

# Load targets early to fetch live prices
targets_path = os.path.join(os.path.dirname(__file__), 'data', 'ai_targets.json')
ai_targets = []
if os.path.exists(targets_path):
    with open(targets_path, 'r', encoding='utf-8') as f:
        ai_targets = json.load(f)

target_codes = [t['code'] for t in ai_targets]
api_connected, live_prices = load_live_targets(target_codes)

# Sector Analysis using static daily data
static_prices = {s['code']: {'change_rate': s['change_rate'], 'volume': s['volume']} for s in static_status}
sector_df = SectorAnalyzer.calculate_sector_metrics(stocks, static_prices)

# Clear the custom loader once data is fetched
loader_placeholder.empty()

# Initialize AI Analyzer for Token Diet Logic
from services.ai_analyzer import AiAnalyzer
ai_root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ai_analyzer = AiAnalyzer(ai_root_path)

# --- Sidebar ---
with st.sidebar:
    st.title("🛰️ Command Center")
    st.markdown("---")
    st.subheader("API Status")
    if api_connected:
        st.markdown("KIS API: 🟢 Connected")
    else:
        st.markdown("KIS API: 🔴 Disconnected (Check .env)")
    
    if ai_analyzer.is_configured:
        st.markdown("Gemini AI: 🟢 Linked")
    else:
        st.markdown("Gemini AI: 🔴 Disconnected")
    st.markdown("Wiki DB: 🟢 Linked")
    
    st.markdown("---")
    st.subheader("Filters")
    sectors = list(set([s['sector'] for s in stocks]))
    sectors.sort() # Sort alphabetically for better UX
    selected_sector = st.selectbox("섹터 필터", sectors)

# --- Hero Section: Sector Rotation & Actionable Dips ---
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("🔄 일일 순환매 동향 (전일 종가 기준)")
    if not sector_df.empty:
        display_df = sector_df[['sector', 'avg_change_rate', 'total_volume']].rename(
            columns={'sector': '섹터', 'avg_change_rate': '평균 등락률(%)', 'total_volume': '총 거래량'}
        )
        st.dataframe(
            display_df.style.format({
                '평균 등락률(%)': '{:.1f}',
                '총 거래량': '{:,.0f}'
            }),
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("API 연동 시 섹터별 거래량/등락률 계산 결과가 표시됩니다.")

@st.dialog("🤖 AI 심층 분석 리포트")
def show_ai_analysis(dip):
    with st.spinner("Gemini API가 딥 분석을 수행 중입니다..."):
        result = ai_analyzer.get_dip_analysis(
            stock_name=dip['name'],
            stock_code=dip['code'],
            entry_price=dip['entry_price'],
            current_price=dip['current_price'],
            sector=dip['sector'],
            wiki_content=dip['content']
        )
        st.markdown(result)

with col2:
    st.subheader("🚨 AI 선정 오늘의 타겟 (Target Dips)")
    
    if not ai_targets:
        st.info("오늘의 AI 타겟이 없습니다. (저녁 8시 이후 batch_scanner.py를 실행하세요)")
    else:
        st.success(f"🔥 AI가 선정한 오늘 노려볼 타겟 종목 {len(ai_targets)}개입니다!")
        target_cols = st.columns(len(ai_targets) if len(ai_targets) <= 3 else 3)
        for i, target in enumerate(ai_targets[:3]):
            with target_cols[i % 3]:
                # Find current live price
                price_data = live_prices.get(target['code'], {})
                cp = price_data.get('current_price', 0)
                cr = price_data.get('change_rate', 0.0)
                ep = target['predicted_entry_price']
                
                # Highlight if within 2% of AI predicted entry
                is_dip = False
                if ep > 0 and cp > 0:
                    is_dip = abs(cp - ep) / ep <= 0.02
                    
                alert_class = "dip-alert" if is_dip else ""
                
                html_target = f"""
<div class="glass-card {alert_class}" style="margin-bottom: 10px;">
    <div class="stock-name">{target['name']}</div>
    <div>현재가: <b class="price-value profit">₩{cp:,}</b> ({cr}%)</div>
    <div>진입가(AI): ₩{int(ep):,}</div>
    <div class="reasoning" style="font-size: 0.8rem; margin-top: 8px;">{target['rationale']}</div>
</div>
"""
                st.markdown(html_target, unsafe_allow_html=True)
                
                if st.button("🤖 수동 분석 업데이트", key=f"ai_btn_{target['code']}"):
                    # Find matching wiki content if any
                    wiki_content = next((s['content'] for s in stocks if s['code'] == target['code']), "")
                    target_dip = {'name': target['name'], 'code': target['code'], 'entry_price': ep, 'current_price': cp, 'sector': 'AI Target', 'content': wiki_content}
                    show_ai_analysis(target_dip)

st.markdown("---")

# --- Watchlist List View ---
st.title("📋 추적 종목 (전일 종가 기준)")

display_stocks = [s for s in static_status if s['sector'] == selected_sector]

if not display_stocks:
    st.info("해당 섹터의 종목 데이터가 없습니다. 저녁 8시 이후 batch_scanner.py를 실행하여 데이터를 갱신하세요.")
else:
    import pandas as pd
    df = pd.DataFrame(display_stocks)
    df = df[['name', 'code', 'close', 'change_rate', 'volume']].rename(
        columns={'name': '종목명', 'code': '종목코드', 'close': '전일 종가(₩)', 'change_rate': '등락률(%)', 'volume': '거래량'}
    )
    st.dataframe(
        df.style.format({
            '전일 종가(₩)': '{:,.0f}',
            '등락률(%)': '{:.1f}',
            '거래량': '{:,.0f}'
        }),
        hide_index=True,
        use_container_width=True
    )
