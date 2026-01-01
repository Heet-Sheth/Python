@echo off

echo =============================================
echo  GPU Log Regression Analyzer — Demo Runner
echo =============================================
echo.

REM -------- FAIL Scenario (New Errors Introduced) --------
echo ===== Scenario 1 — FAIL (New Errors Introduced) =====
python log_reader.py ^
  --baseline baseline1.log ^
  --newrun   newrun1.log

echo Exit Code: %ERRORLEVEL%
echo.

REM -------- PASS Scenario (Only Solved Errors) --------
echo ===== Scenario 2 — PASS (Solved Errors Only) =====
python log_reader.py ^
  --baseline baseline2.log ^
  --newrun   newrun2.log

echo Exit Code: %ERRORLEVEL%
echo.

REM -------- NO CHANGE Scenario --------
echo ===== Scenario 3 — NO CHANGE (Stable State) =====
python log_reader.py ^
  --baseline baseline3.log ^
  --newrun   newrun3.log

echo Exit Code: %ERRORLEVEL%
echo.

echo =============================================
echo  Demo Completed
echo =============================================
pause
