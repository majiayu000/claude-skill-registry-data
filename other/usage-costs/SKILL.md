---
name: usage-costs
version: "1.0.0"
description: "Report AI token usage and estimated costs. Use when: owner asks about costs today/yesterday/this week, per session, or per model. Shows main session, cron jobs, and subagents. Answers: 'how much did today cost?', 'how much was this session?', 'what was last week's spend?'"
---

# Usage Costs Skill

Reports token usage and estimated costs from OpenClaw sessions.

---

## Load Local Context
```bash
CONTEXT_FILE="/path/to/workspace/skills/usage-costs/.context"
[ -f "$CONTEXT_FILE" ] && source "$CONTEXT_FILE"
# Provides: $OWNER_PHONE, $PRICING_INPUT, $PRICING_OUTPUT, $PRICING_CACHE_READ
```

---

## Data Sources

1. **Live sessions** → `openclaw status --deep` (current token counts per session)
2. **Cron run history** → `/path/to/openclaw/cron/runs/*.jsonl` (usage field per run)
3. **Token history** → `/path/to/workspace/data/token-history.jsonl` (daily aggregates)

---

## Pricing (claude-sonnet-4-6, as of 2026-04)

| Type | Price |
|---|---|
| Input | $3.00 / 1M tokens |
| Output | $15.00 / 1M tokens |
| Cache read | $0.30 / 1M tokens |
| Cache write | $3.75 / 1M tokens |

---

## Step 1 — Live Session Report

```bash
# Get current session token counts
openclaw status --deep 2>/dev/null | grep -E "agent:main|direct|cached" | head -20
```

Parse output: each row has `session_key | kind | age | model | tokens`.

---

## Step 2 — Cron History Report

```python
#!/usr/bin/env python3
import json, glob, os
from datetime import datetime, timezone, timedelta

def get_cron_usage(days_back=1):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    cutoff_ts = cutoff.timestamp() * 1000

    total_input = 0
    total_output = 0
    runs = []

    for f in glob.glob('/path/to/openclaw/cron/runs/*.jsonl'):
        job_name = os.path.basename(f).replace('.jsonl', '')
        with open(f) as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                    if d.get('ts', 0) >= cutoff_ts and 'usage' in d:
                        inp = d['usage'].get('input_tokens', 0)
                        out = d['usage'].get('output_tokens', 0)
                        total_input += inp
                        total_output += out
                        runs.append({
                            'job': d.get('name', job_name),
                            'input': inp,
                            'output': out,
                            'ts': d['ts']
                        })
                except:
                    pass

    return total_input, total_output, runs

inp, out, runs = get_cron_usage(days_back=1)
cost = (inp / 1_000_000 * 3) + (out / 1_000_000 * 15)
print(f"Cron tokens (last 24h): {inp:,} in / {out:,} out")
print(f"Estimated cost: ${cost:.2f}")
print(f"Runs: {len(runs)}")
```

---

## Report Formats

### "How much did today cost?"
```
📊 Cost Report — 2026-04-04

Main session: ~276K tokens (100% cached)
Cron runs: 25 runs | X in / Y out tokens
Subagents: N sessions | X tokens

Estimated total: ~$Z
(Cron: $A | Subagents: $B | Main session: estimated $C)

Note: Main session cost is estimated — cache reduces actual cost by ~90%.
```

### "How much this week?"
- Read from `/path/to/workspace/data/token-history.jsonl`
- Sum daily entries for the last 7 days
- Show per-day breakdown + total

### "How much was this session?"
- Run `openclaw status --deep`
- Find `agent:main:main` row → tokens field
- Calculate: input_cost + output_cost (apply cache discount if cached%)

---

## Save Daily Report

Append to `/path/to/workspace/data/token-history.jsonl`:

```json
{"date": "2026-04-04", "input": 133, "output": 17376, "cache_read": 900000, "cost_usd": 0.54, "cron_runs": 25, "subagent_runs": 4}
```

---

## Cost Extraction Script (from session jsonl files)

This is the authoritative method for extracting real costs — works for Anthropic/Claude models:

```python
python3 -c "
import json, glob, os
from datetime import datetime, timezone

sessions_dir = '/path/to/openclaw/agents/main/sessions'
files = glob.glob(f'{sessions_dir}/*.jsonl')
today = datetime.now(timezone.utc).date()
total_cost = 0
total_cache_write = 0
total_cache_read = 0
sessions_today = 0

for fpath in files:
    mtime = datetime.fromtimestamp(os.path.getmtime(fpath), tz=timezone.utc).date()
    if mtime != today:
        continue
    sessions_today += 1
    with open(fpath) as f:
        for line in f:
            try:
                l = json.loads(line)
                if l.get('type') == 'message' and l.get('message',{}).get('role') == 'assistant':
                    u = l['message'].get('usage',{})
                    total_cost += u.get('cost',{}).get('total',0)
                    total_cache_write += u.get('cacheWrite',0)
                    total_cache_read += u.get('cacheRead',0)
            except: pass

print(f'Today: {sessions_today} sessions — \${total_cost:.2f}')
print(f'Cache writes: {total_cache_write:,} tokens')
print(f'Cache reads: {total_cache_read:,} tokens')
"
```

**⚠️ Provider compatibility:**
- ✅ Works for: Anthropic Claude (sonnet, haiku, opus)
- ❌ Does NOT work for: Google Gemini, OpenAI GPT — cost field is empty
- For Google/OpenAI agents: use provider billing dashboard directly

---

## Trigger Phrases
"how much did today cost?"
"how much was this session?"
"how much this week?"
"show me costs"
- "usage report"
- "token usage"
