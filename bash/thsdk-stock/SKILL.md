---
name: "thsdk-stock"
description: "Fetch stock market data via thsdk: realtime quotes, intraday data, historical K-lines for A-shares, HK/US stocks, futures, forex."
---

# thsdk Stock Skill

Use this skill when a task requires fetching market data with `thsdk`.
The current `thsdk` PyPI package exposes `THS`, not `Tdx`.

## Activation Keywords
- `thsdk`
- `通达信`
- `股票数据`
- `实时行情`
- `历史K线`

## Tools Used
- `exec`
- `read`
- `write`

## Installation

Prefer a project-local virtual environment:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install thsdk
```

If `pip` is blocked by the system Python, do not force-install globally. Use the virtualenv.

## When to use which script
- Realtime order-book style quote or intraday snapshot: `scripts/fetch_realtime.py`
- Historical K-line bars: `scripts/fetch_history.py`
- Offline validation in restricted environments: `scripts/test_thsdk.py`
- Runnable examples: `examples/example_usage.py`

## Usage Patterns

### 1. Fetch realtime data
```bash
.venv/bin/python scripts/fetch_realtime.py --code SZ300033 --mode depth --pretty
```

If the environment cannot import `thsdk`, validate with mock data:

```bash
python3 scripts/fetch_realtime.py --code SZ300033 --mock --pretty
```

### 2. Fetch intraday timeline
```bash
.venv/bin/python scripts/fetch_realtime.py --code SZ300033 --mode intraday --pretty
```

### 3. Fetch historical K-line data
```bash
.venv/bin/python scripts/fetch_history.py \
  --code SZ300033 \
  --interval day \
  --count 30 \
  --adjust forward \
  --pretty
```

### 4. Fetch a bounded time range
```bash
.venv/bin/python scripts/fetch_history.py \
  --code SZ300033 \
  --interval 60m \
  --start 2026-03-01 \
  --end 2026-03-18T15:00:00 \
  --pretty
```

### 5. Run the offline test suite
```bash
python3 scripts/test_thsdk.py
```

## Instructions for Agents

1. Confirm whether the user wants realtime data or historical K-line data.
2. Prefer a local virtualenv and install `thsdk` there. Do not modify the system Python.
3. Use `THS()` as the client entrypoint. If login credentials exist, inject them:

```bash
export THS_USERNAME=your_username
export THS_PASSWORD=your_password
export THS_MAC=your_mac
```

4. For historical K-line queries, use `ths.klines(...)`.
5. For realtime data, prefer:
   - `ths.depth(...)` for 5-level order book
   - `ths.intraday_data(...)` for minute timeline
6. Treat SDK responses as `success/error/data/extra` objects.
7. Normalize output to plain JSON-serializable dictionaries before returning.
8. If runtime cannot import `thsdk`, suggest `--mock` for local validation only.
9. For code lookup, use `ths.search_symbols(...)` then feed `THSCODE` into queries.

## Examples

### Example 1: Fetch realtime depth data

```python
from thsdk import THS

with THS() as ths:
    response = ths.depth("SZ300033")
    if response.success:
        print(response.data)
```

### Example 2: Fetch historical K-lines

```python
from thsdk import THS

with THS() as ths:
    response = ths.klines(
        "SZ300033",
        interval="day",
        count=30,
        adjust="forward"
    )
    if response.success:
        for bar in response.data:
            print(f"{bar['时间']}: {bar['收盘价']}")
```

### Example 3: Search for a stock code

```python
from thsdk import THS

with THS() as ths:
    response = ths.search_symbols("同花顺")
    if response.success:
        for item in response.data:
            print(f"{item['THSCODE']}: {item['名称']}")
```

## Notes
- `thsdk` on PyPI requires Python 3.9+.
- Guest accounts may exist but can be limited in permission or latency.
- In restricted environments without network access, use `--mock` for testing.