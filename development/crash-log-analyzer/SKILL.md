---
name: crash-log-analyzer
description: Parse and analyze macOS crash logs to identify crash causes and debugging information
type: skill
language: python
---

# Crash Log Analyzer

Parse macOS `.crash` and `.ips` files to extract useful debugging information.

## Capabilities

- Parse crash report files
- Symbolicate stack traces
- Identify crash type (EXC_BAD_ACCESS, assertion, etc.)
- Extract thread information
- Show crash location and context
- Identify common crash patterns
- Generate crash statistics
- Find duplicate crashes
- Export crash data

## Tools Included

### `crash_analyzer.py`
Python script to parse crash logs

**Commands:**
```bash
# Analyze crash log
./crash_analyzer.py crash.crash

# Symbolicate (requires dSYM)
./crash_analyzer.py crash.crash --dsym PaleoRose.app.dSYM

# Batch analyze directory
./crash_analyzer.py --batch ~/Library/Logs/DiagnosticReports/PaleoRose*

# Export summary
./crash_analyzer.py crash.crash --export-json summary.json

# Find duplicates
./crash_analyzer.py --find-duplicates ~/Library/Logs/DiagnosticReports/
```

## Crash Types Handled

- EXC_BAD_ACCESS (SIGSEGV, SIGBUS)
- EXC_CRASH (SIGABRT)
- Uncaught exceptions
- Assertions
- Watchdog timeouts
- Stack overflow

## Usage

Use when:
- App crashes during testing
- Need to analyze user crash reports
- Debugging difficult-to-reproduce crashes
- Tracking crash patterns
- Preparing crash reports for issues

## Output Format

```
Crash Summary
-------------
Process: PaleoRose
Bundle ID: com.example.paleorose
Version: 1.0.0
Date: 2025-11-08 20:30:15

Crash Type: EXC_BAD_ACCESS (SIGSEGV)
Exception: KERN_INVALID_ADDRESS at 0x0000000000000000

Crashed Thread: 0 (Main Thread)

Stack Trace:
  0  PaleoRose  0x10045a123 -[TableListController tableView:objectValueFor:row:] + 123
  1  AppKit     0x7fff2b3c4567 -[NSTableView _sendDataSourceValue] + 234
  2  AppKit     0x7fff2b3c4890 -[NSTableView reloadData] + 567

Probable Cause: Null pointer dereference in tableNames array access
Recommendation: Add nil check before accessing tableNames[row]
```
