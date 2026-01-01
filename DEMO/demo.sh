#!/bin/bash

echo "============================================="
echo " GPU Log Regression Analyzer — Demo Runner"
echo "============================================="
echo ""

# -------- FAIL Scenario (New Errors Introduced) --------
echo "===== Scenario 1 — FAIL (New Errors Introduced) ====="
python3 log_reader.py \
  --baseline baseline1.log \
  --newrun  newrun1.log

echo "Exit Code: $?"
echo ""

# -------- PASS Scenario (Only Solved Errors) --------
echo "===== Scenario 2 — PASS (Solved Errors Only) ====="
python3 log_reader.py \
  --baseline baseline2.log \
  --newrun  newrun2.log

echo "Exit Code: $?"
echo ""

# -------- NO CHANGE Scenario --------
echo "===== Scenario 3 — NO CHANGE (Stable State) ====="
python3 log_reader.py \
  --baseline baseline3.log \
  --newrun  newrun3.log

echo "Exit Code: $?"
echo ""

echo "============================================="
echo " Demo Completed"
echo "============================================="
