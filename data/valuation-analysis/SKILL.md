---
name: valuation-analysis
description: Constructs valuation models and price targets for a company using DCF, multiples, and scenario analysis. Use this when asked about "fair value", "target price", "is it cheap/expensive", or "valuation".
allowed-tools: [execute_python, execute_bash]
---

# Valuation Analysis

## Usage
To generate a valuation model for a company, execute the Python script in this directory.

**Command:**
```bash
python skills/valuation/run_valuation.py --ticker <TICKER> --horizon "<TIME_HORIZON>"
```

**Parameters:**
- `ticker`: The stock symbol (e.g., AAPL).
- `horizon`: Time period (e.g., "1 year", "18 months"). Default: "1 year".

## Output
Returns a JSON object with:
- `valuation_range`: Low, Base, and High price targets with methodology.
- `assumptions`: Key assumptions driving the model (e.g., revenue growth rates, discount rates) with evidence citations.
- `sensitivity`: A sensitivity matrix showing how price targets change under different scenarios.

## Example
```bash
python skills/valuation/run_valuation.py --ticker AAPL --horizon "1 year"
```

## Environment Requirements
- Python 3.12+
- Access to `research.db` SQLite database
- Neo4j GraphRAG instance running (default: bolt://localhost:7687)
- Environment variables: NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD (optional, defaults provided)
