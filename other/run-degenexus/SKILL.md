---
name: run-degenexus
description: Project-specific run and verify recipe for the DegenExus CLI/TUI simulator.
disable-model-invocation: true
when_to_use: Invoke explicitly when a user asks how to run, smoke-test, or verify DegenExus locally.
---

# Run DegenExus

## Environment assumptions

```bash
python -m venv .venv
pip install -r requirements.txt
```

## Smoke commands

```bash
python src/main.py --cycles 1 --no-dashboard --symbols AAPL,SPY
python src/main.py --list-agents
```

## Verification commands

```bash
python -m compileall -q src/
python -m pytest tests/ -v
python -m pytest tests/ --cov=src --cov-report=term-missing
```

## Caveats

- yfinance and network-backed feeds may degrade in offline environments; document fallback behavior instead of treating network unavailability as a product failure.
- This project is a simulator/research environment. Do not represent any command as placing real trades.
