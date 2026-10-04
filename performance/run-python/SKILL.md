---
name: run-python
description: Execute Python snippets for data filtering, aggregation, and cross-tool joins. Use when you need to sort, filter, compute derived metrics, or combine data from multiple tool calls.
---

# run_python — Sandbox Reference

## Available helpers

These are the ONLY callable names. **Do not use tool names** (e.g. `fetch_latest_feed`, `search_openrouter_models` — those are tool names, not Python functions).

| Helper | Returns |
|--------|---------|
| `fetch_benchmarks(query='', limit=50)` | list of dicts: `name, provider, quality, coding, math, speed_tps, input_per_1m, output_per_1m, context_k` |
| `fetch_news(days_back=1, include_hype=False, query='', limit=50, since=None, until=None)` | list of dicts: `title, source, date, url, summary` |
| `fetch_openrouter(query='', limit=50)` | list of dicts: `id, name, provider, context_k, input_per_1m, output_per_1m` |
| `fetch_image_models(limit=30)` | list of dicts: `name, provider, elo, cost` |
| `fetch_video_models(limit=20)` | list of dicts: `name, provider, elo` |

## Sandbox rules

- **No `import` statements** — `__import__` is blocked. Standard libs (`json`, `re`, `math`, `datetime`, `collections`) are already available.
- **No network access** — only the helpers above can fetch data.
- **Use `print()` for output** — return values are ignored. Print only what matters.
- **Keys may be missing** — use `.get('key')` not `['key']` to avoid KeyError on sparse data.

## Common patterns

**Top models for coding:**
```python
models = fetch_benchmarks(limit=100)
coding = [m for m in models if m.get('coding')]
for m in sorted(coding, key=lambda x: x['coding'], reverse=True)[:10]:
    print(m['name'], 'coding=' + str(m['coding']), 'general=' + str(m.get('quality', '?')))
```

**Price/quality ratio:**
```python
models = fetch_benchmarks(query='anthropic', limit=50)
for m in models:
    q = m.get('quality') or 0
    cost = m.get('output_per_1m') or 0
    if q and cost:
        print(m['name'], 'ratio=' + str(round(q / cost, 1)), 'q=' + str(q), '$' + str(cost) + '/1M')
```

**Date-range news:**
```python
items = fetch_news(days_back=30, since='2026-02-01', until='2026-02-10', limit=100)
print(len(items), 'items in range')
for it in items[:10]:
    print('[' + (it.get('date') or '')[:10] + ']', it.get('title', '?'))
```

**Cross-tool join (benchmarks × OpenRouter):**
```python
bench = fetch_benchmarks(limit=30)
or_models = fetch_openrouter(query='openai', limit=50)
or_ids = {m.get('id', '').lower() for m in or_models}
for b in bench[:10]:
    available = any(b['name'].lower() in oid for oid in or_ids)
    print(('[OR]' if available else '[  ]'), b['name'], 'q=' + str(b.get('quality', '?')))
```

## What to use for each question

| Question type | Use `coding` | Use `quality` | Use `math` |
|---------------|-------------|---------------|-----------|
| Best for code generation | ✓ | – | – |
| Best overall / general | – | ✓ | – |
| Best for math/science | – | – | ✓ |
| Best value (general) | – | ✓ | – |
