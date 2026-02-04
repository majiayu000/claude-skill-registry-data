---
name: fundamentals-analysis
description: Analyzes a company's fundamental performance, growth drivers, and risks using verified financial data and text evidence. Use this when asked to research a stock's business model, revenue segments, or quarterly performance.
allowed-tools: [execute_python, execute_bash]
---

# Fundamentals Analysis

## Usage
To perform a fundamental analysis on a company, execute the Python script in this directory.

**Command:**
```bash
python skills/fundamentals/run_analysis.py --ticker <TICKER> --focus "<FOCUS_AREA>" --horizon "<TIME_HORIZON>"
```

**Parameters:**
- `ticker`: The stock symbol (e.g., AAPL).
- `focus`: Specific area to investigate (e.g., "services revenue", "China risks"). Default: "growth drivers".
- `horizon`: Time period (e.g., "1 year", "short term"). Default: "1 year".

## Output
The script returns a JSON object containing:
- `financials_summary`: Quantitative data from the SQL database.
- `drivers`: Key growth drivers backed by text evidence.
- `risks`: Key risks backed by text evidence.

## Example
```bash
python skills/fundamentals/run_analysis.py --ticker AAPL --focus "services revenue" --horizon "1 year"
```

## Environment Requirements
- Python 3.12+
- Access to `research.db` SQLite database
- Neo4j GraphRAG instance running (default: bolt://localhost:7687)
- Environment variables: NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD (optional, defaults provided)
