# GPU Log Regression Analyzer

## Description

A lightweight Python utility to compare GPU validation logs across
baseline and new simulation runs. It identifies new failures, solved
errors, and persistent issues, and produces a structured regression
summary for validation engineers.

## Why This Tool Exists

- manual log comparison is slow & error-prone

- engineers need quick regression triage

- this helps decide PASS / FAIL faster

## Features

- Counts frequency of each unique error string

- Detects:

  - New errors

  - Solved errors

  - Persistent errors

- Handles empty files safely

- Provides deterministic PASS / FAIL policy

- CLI interface using argparse

## How to run

```Terminal/CMD
python3 ./v1.0.1/log_reader.py --baseline baseline.log --newrun newrun.log
```

## PASS / FAIL Policy

The regression verdict is determined using the following rules:

- New errors introduced in the new run → **FAIL**
- Errors that disappear or reduce in count → **SOLVED**
- Errors that appear in both runs with the same frequency → **PERSISTENT**
- No change in error behavior → **NO CHANGE**

## Sample Output

```Python
Comparison Report
-------------------

New Error:
         New allocator fault : 1

Solved Errors:
         Timeout : 1
         Regression : 1

Unchanged Errors:


FINAL VERDICT
---------------
FAIL
```

## Summary-Only Mode

By default, the tool prints a full comparison report.
To print only the final verdict and exit code:

```Terminal/CMD
  --summary
```

## Exit Status Codes

The tool returns deterministic process exit codes to support CI pipelines and automated triage:

| Verdict   | Meaning                     | Exit Code |
| --------- | --------------------------- | :-------: |
| PASS      | Only solved errors detected |     0     |
| FAIL      | New errors introduced       |     1     |
| NO CHANGE | Error behaviour unchanged   |     2     |

## Demo (Run Pre-Configured Test Scenarios)

This project includes a demo runner that executes three validation scenarios — FAIL, PASS, and NO CHANGE — using prepared log files.

### On Linux / macOS

```Terminal/CMD
./DEMO/demo.sh
```

### On Windows (Untested)

```Terminal/CMD
cd DEMO
demo.bat
```

## Input Assumptions

- Logs follow the `[ERROR] message` format
- Comparison is strictly string-based
- Different error codes are treated as distinct error signatures
- The tool does not normalize, tokenize, or cluster messages

## Versioning

```makefile
Version: v1.0.1
Status: Stable (Validated across 8 scenarios)
```

## Validation Coverage

The tool has been tested across the following scenarios:

- No-change runs
- Solved-only cases
- New-error introduction
- Clean baseline → new failures
- Mixed solved + new failures
- Empty new-run logs
- Logs with no errors
- Similar error strings treated as distinct entries

## Roadmap

- optional CSV / JSON output

- logging class for better formatting

- config-based policy tuning

- support warning-level analysis

## Design Philosophy

This tool is intentionally designed as a **lightweight and deterministic regression-analysis utility** — not an automated testing framework or log-mining engine. The focus is on correctness, clarity, and reliability over complexity or optimization.

The comparison model is **string-exact and frequency-based** by design. Error messages are treated as distinct logical identifiers without normalization or clustering, ensuring predictable, transparent behavior during validation workflows. All outcomes are deterministic and reproducible — no heuristics, inference, or hidden interpretation layers are used.

Edge-case handling prioritizes **safety and failure-awareness**. Empty files, logs with no errors, and clean baseline runs are handled explicitly rather than silently ignored, ensuring that regression verdicts remain meaningful and auditable.

Overall, the tool aims to support **fast triage and engineering judgment**, providing a clear separation of new, solved, and persistent failures — while keeping policy behavior explicit, explainable, and easy to reason about.
