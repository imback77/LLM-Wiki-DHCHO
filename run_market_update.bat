@echo off
echo.
echo [LLM Wiki] ==========================================
echo [LLM Wiki] Market Data Update Starting...
echo [LLM Wiki] ==========================================
echo.

echo [1/3] Analyzing Capital Flow (Dynamic Trend)...
python tools/update_dynamic_trend.py

echo.
echo [2/3] Collecting Macro ^& Risk Indicators...
python tools/update_market_macro.py

echo.
echo [3/3] Synthesizing Daily Recap to Wiki...
python tools/ingest_daily_recap.py

echo.
echo [LLM Wiki] ==========================================
echo [LLM Wiki] Update Complete!
echo [LLM Wiki] Check your Obsidian Wiki for the new Recap.
echo [LLM Wiki] ==========================================
echo.
pause
