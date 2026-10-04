---
name: log-analyzer
description: Parse and analyze common log formats (nginx, syslog, application)
activation_keywords: [log, logs, analyze, parse log, error log, access log]
---

# Log Analyzer Skill

Provides log parsing and analysis capabilities:
- Parse common log formats: nginx access/error, syslog, Apache, application JSON logs
- Extract structured fields from log lines
- Filter logs by level, time range, or pattern
- Summarize log statistics (error counts, top IPs, etc.)

Use `builtin_log_analyzer` tool with fields:
- `operation`: one of "parse", "filter", "summarize"
- `log_content`: the log content to analyze
- `format`: (optional) log format hint: "nginx", "syslog", "apache", "json", "auto"
- `filter_level`: (optional) for "filter" operation: "debug", "info", "warn", "error", "fatal"
