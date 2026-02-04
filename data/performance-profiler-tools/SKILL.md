---
name: performance-profiler-tools
description: Python tools for analyzing Instruments traces and performance data
type: skill
language: python
---

# Performance Profiler Tools

Analyze Instruments trace files and performance data.

## Capabilities
- Parse Instruments .trace files
- Extract Time Profiler data
- Analyze Allocations data
- Generate performance reports
- Compare trace files
- Identify performance regressions
- Calculate time percentages
- Find memory growth patterns

## Tools
`instruments_analyzer.py` - Parse Instruments traces

## Commands
```bash
# Analyze trace
./instruments_analyzer.py analyze app.trace

# Compare traces
./instruments_analyzer.py compare --baseline baseline.trace --current current.trace

# Find hot paths
./instruments_analyzer.py hotpaths app.trace --threshold 5%

# Memory analysis
./instruments_analyzer.py memory app.trace
```

## Output
```
Performance Analysis
===================
Total Time: 2.45s
Top Methods:

1. drawRect: (456ms, 18.6%)
2. calculateStatistics (234ms, 9.5%)
3. readFromStore (198ms, 8.1%)

Recommendations:
- Cache drawRect results
- Optimize calculateStatistics algorithm
- Add index to database query
```

## Complements
`performance-profiler` agent (launches Instruments)
