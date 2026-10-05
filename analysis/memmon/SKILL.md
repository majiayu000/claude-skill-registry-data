---
name: memmon
description: Monitor and act on opencode memory health. Run this skill when you notice opencode feeling slow, suspect a memory leak, want a routine memory check, or are asked to check memory usage. Triggers on phrases like "check memory", "memory leak", "opencode slow", "memory health", "how much memory is opencode using", "is there a leak", "memmon".
---

# memmon — opencode memory monitor

Samples and analyzes the opencode process forest for memory leaks, then acts on the verdict. This skill closes the loop: it does not just report — it takes one logged action based on what it finds.

## Tool location

```
~/.config/opencode/tools/memmon/
├── sampler.sh    — take one memory snapshot
├── analyzer.py   — classify samples as LEAK / SLOW / PLATEAU / TRANSIENT
├── loop.sh       — start / stop / status / analyze the background sampler
```

Runtime data: `~/.local/share/opencode-memmon/` (`samples.csv`, `loop.log`, `loop.pid`)

---

## Step 1 — Check sampler status

```bash
bash ~/.config/opencode/tools/memmon/loop.sh status
```

- If **RUNNING**: proceed to Step 2 (data exists).
- If **not running**: take one manual snapshot first, then proceed.

```bash
bash ~/.config/opencode/tools/memmon/sampler.sh
```

---

## Step 2 — Run the analyzer

Always use `--json` for machine-readable output:

```bash
python3 ~/.config/opencode/tools/memmon/analyzer.py \
  --samples ~/.local/share/opencode-memmon/samples.csv \
  --summary ~/.local/share/opencode-memmon/summary.csv \
  --json
```

Parse the JSON. Apply the decision order in Step 3 strictly — do not infer all-clear from `has_leak:false` alone.

**Before running the analyzer:** check whether opencode is currently running:

```bash
pgrep -x opencode || pgrep -f "opencode"
```

If no opencode PIDs exist, go directly to **STOP** — do not run the analyzer on potentially stale data.

---

## Step 3 — Act / Ask / Stop

**Decision order is strict. Evaluate top-to-bottom and stop at the first matching condition.**

### STOP — opencode not running

If no live opencode PIDs were found in Step 2, skip silently and log:

```
memmon [<timestamp>]: STOP — no opencode processes found. Skipping analysis of existing samples to avoid stale-data alerts.
```

Do not run the analyzer. Do not post Slack. Do not alert.

### ASK — Ambiguous or degraded data

Escalate to the human when any of these are true:
- `samples.csv` is missing, empty, or has fewer than 3 rows
- Analyzer exits with an unexpected error (not exit 0 or exit 2)
- Two consecutive SLOW verdicts on the same role (check `actions.jsonl` for prior SLOW on this role)
- LEAK on `opencode-tui` or `opencode-web` with slope > 200 MiB/hr (abnormally high — may indicate sampler noise rather than a real leak)

**Action:** Surface the raw analyzer output and ask:

```
memmon: uncertain result — [reason]. Raw output: <paste>. Should I take any action?
```

Log to `actions.jsonl` regardless:
```json
{"ts":"<ISO>","verdict":"ASK","reason":"<reason>","action":"asked human"}
```

### ACT — LEAK detected

Condition: `has_leak:true` OR any role verdict is `"LEAK"` in the JSON.

**Action — two steps, both required:**

1. Attempt Slack DM to `@ricardo.santos` via `mcp_hub_slack__conversations_add_message`:

```
*memmon LEAK detected* — <timestamp>

Role: <role>
Worst PID: <worst_pid>
Slope: <worst_slope> MiB/hr

Recommended action: restart opencode or investigate <role> process.
Loop status: <running/stopped>
```

2. Check the Slack tool response. If it returns an error or no `ts` field, do **not** claim success. Log `slack_sent: false, error: <error>` and escalate to ASK.

3. Log to `actions.jsonl`:
```json
{"ts":"<ISO>","verdict":"LEAK","role":"<role>","slope_mb_hr":<n>,"pid":"<pid>","slack_sent":<true|false>,"action":"dm sent or escalated"}
```

**Undo step:** The Slack DM cannot be unsent once delivered, but can be deleted. No process is killed, no file is modified. If sent in error, delete it via Slack and log the correction.

### ACT — SLOW drift

Condition: no LEAK, but any role verdict is `"SLOW"`.

**Action:** Log a watch entry only — no Slack.

```json
{"ts":"<ISO>","verdict":"SLOW","role":"<role>","slope_mb_hr":<n>,"pid":"<pid>","action":"logged watch entry"}
```

Also write a brief inline session note:
```
memmon [<timestamp>]: SLOW drift on <role> (<worst_slope> MiB/hr, pid <worst_pid>). Monitoring — no action required yet.
```

If the prior `actions.jsonl` entry for this role was also SLOW → escalate to ASK instead.

### ACT — PLATEAU / TRANSIENT (all roles)

Condition: every role is `"PLATEAU"` or `"TRANSIENT"` and `has_leak:false`.

**Action:** Log all-clear only.

```json
{"ts":"<ISO>","verdict":"PLATEAU","roles_checked":<n>,"samples":<n>,"action":"all clear"}
```

Brief inline note:
```
memmon [<timestamp>]: all clear — no leak detected. Roles: <list>. Samples: <n>.
```

---

## Step 4 — Durable audit log

**Every run appends one JSONL line to:**

```
~/.local/share/opencode-memmon/actions.jsonl
```

```bash
echo '{"ts":"<ISO>","verdict":"<V>","action":"<a>"}' >> ~/.local/share/opencode-memmon/actions.jsonl
```

This file is the real audit trail. The inline session note is a convenience mirror only — ephemeral and not the source of truth.

**To check for consecutive SLOW on a role before acting:**

```bash
tail -5 ~/.local/share/opencode-memmon/actions.jsonl | grep '"verdict":"SLOW"' | grep '"role":"<role>"'
```

If the previous entry for that role was also SLOW → escalate to ASK.

---

## Worked example

```
$ python3 analyzer.py --json
{
  "has_leak": false,
  "roles": {
    "opencode-tui": {"verdict": "PLATEAU", "worst_slope_mb_hr": 1.2, ...},
    "mcphub":       {"verdict": "SLOW",    "worst_slope_mb_hr": 8.4, ...}
  }
}
```

→ **SLOW on mcphub**: log watch entry, no Slack. If mcphub shows SLOW next run too → ASK.

---

## Thresholds (env overrides)

| Env var               | Default | Meaning                        |
| --------------------- | ------- | ------------------------------ |
| `MEMMON_LEAK_MB_HR`   | 60      | MiB/hr slope → LEAK            |
| `MEMMON_SLOW_MB_HR`   | 6       | MiB/hr slope → SLOW            |
| `MEMMON_MIN_SAMPLES`  | 3       | Minimum samples to classify    |
| `MEMMON_MIN_LEAK_SAMPLES` | 8   | Minimum samples to call LEAK   |
| `MEMMON_WINDOW`       | 3       | Window-min smoothing width     |
