---
name: python-monitoring-trace
description: Use when you need a detailed execution trace of a Python script using sys.monitoring, including logging every operation with include/exclude event controls.
---

# Python Monitoring Trace

- Run the helper with `python scripts/monitor_trace.py path/to/script.py -- arg1 arg2`.
- List available events with `--list-events` and choose events by name.
- Include only specific events with `--include LINE,INSTRUCTION` (comma-separated or repeatable).
- Exclude events with `--exclude C_RETURN,C_RAISE` (comma-separated or repeatable).
- Write logs to a file with `--output trace.log`; omit `--output` to write to stdout.
