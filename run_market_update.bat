@echo off
echo.
echo [LLM Wiki] ==========================================
echo [LLM Wiki] Market Data Update Starting...
echo [LLM Wiki] ==========================================
echo.

echo [1/6] Scanning KIS + NXT Daily Dips (AI Target)...
python dashboard/services/batch_scanner.py

echo.
echo [2/6] Collecting News ^& Market Sentiment (Naver ^& RSS)...
python tools/fetch_news_sentiment.py

echo.
echo [3/6] Analyzing Capital Flow (Dynamic Trend)...
python tools/update_dynamic_trend.py

echo.
echo [4/6] Collecting Macro ^& Risk Indicators...
python tools/update_market_macro.py

echo.
echo.
echo [5/6] Synthesizing Daily Recap to Wiki...
python tools/ingest_daily_recap.py

echo.
echo [6/6] Generating Watchlist Intelligence...
python tools/update_watchlist_intelligence.py

echo.
echo [LLM Wiki] ==========================================
echo [LLM Wiki] Update Complete!
echo [LLM Wiki] Check your Obsidian Wiki for the new Recap.
echo [LLM Wiki] ==========================================
echo.
pause
