---
name: vibe-ledger
description: >
  Generates a full project cost report as a self-contained HTML file from
  vibe/cost/history.json. Opens automatically in the browser. Tracks spend
  per session, per task, per phase, and per day. Shows task size breakdown
  (S/M/L avg costs), session burn with dot indicators, token composition,
  efficiency metrics, waste pattern advice, and project cost forecast.
  All plain English — readable by non-technical stakeholders.
  Triggered automatically at the end of every cost: session.
  Also triggers on "ledger:", "generate ledger", "show cost report",
  "open ledger", "cost report", "how much have I spent", "show me the report".
  Requires vibe/cost/history.json to exist — run cost: first if it doesn't.
  Zero dependencies — uses Python stdlib only, works on any machine.
---

# Vibe Ledger

Generates a visual cost report from your project's cost history.
Reads `vibe/cost/history.json`. Writes `vibe/cost/ledger/index.html`. Opens in browser.

**No dependencies. No installs. Works on Mac, Linux, and Windows.**

---

## When this runs

**Automatically** — vibe-cost calls this at the end of every session after writing history.json.

**Manually** — when the user says:
- `ledger:` — regenerate and open
- `show cost report` / `open ledger` / `generate ledger`
- `how much have I spent` — if history.json exists

---

## Step 1 — Check history.json exists

```bash
ls vibe/cost/history.json 2>/dev/null && echo "EXISTS" || echo "MISSING"
```

If missing:
> "No cost history found yet. Run `cost:` after your next session to start tracking,
> then `ledger:` to generate the report."

Stop here if missing.

---

## Step 2 — Run the generator

```bash
# Resolve the generator across install layouts (flat install or plugin marketplace)
GEN=$(ls ~/.claude/skills/vibe-ledger/scripts/generate.py \
         ~/.claude/plugins/marketplaces/*/skills/vibe-ledger/scripts/generate.py 2>/dev/null | head -1)
python3 "$GEN"
```

The script:
1. Finds `vibe/cost/history.json` from the current project directory
2. Computes all metrics — totals, averages by task size, day breakdowns, efficiency ratios
3. Generates `vibe/cost/ledger/index.html` — self-contained, no external dependencies
4. Opens it in the default browser automatically
5. Prints a summary to the terminal

---

## Step 3 — Confirm to user

After the script runs, tell the user:

> "Ledger generated — opening in your browser.
>
> **[Project name]** · [N] sessions · [N] tasks · **$[X.XX]** total
> Report: `vibe/cost/ledger/index.html`
>
> Run `ledger:` any time to refresh it with the latest data."

---

## What the report shows

**Header** — project name, total cost, session count, date range, build progress

**Stat cards** — avg cost per task, avg cost by size (S/M/L), peak session, cache savings

**At a glance** — plain English summary: what was built, what it cost, whether costs are healthy

**Day by day** — cost per day with ASCII block bars

**Task size breakdown** — S/M/L cost totals with percentage of total spend

**Session burn table** — each session with dot indicators (each dot ≈ cost/7), colour-coded:
- Green = on track
- Red = peak session
- Amber = output-heavy (CP-03)
- Blue = review session

**Token composition** — reading vs writing cost in plain terms ("reading costs $X of your $Y")

**Efficiency metrics** — tokens per task, read-to-write ratio, code written per dollar

**Top 5 most expensive tasks** — with size, phase, input and output tokens

**Advice cards** — plain English explanations of waste patterns detected, with specific fixes

**Forecast** — remaining cost estimate based on avg task cost × tasks remaining

---

## Output files

```
vibe/cost/
├── history.json          ← source data (written by cost:)
└── ledger/
    └── index.html        ← generated report (open this)
```

`index.html` is a single self-contained file (all data + CSS + JS inlined) — share
it by just sending the file. It renders fully offline; the only network use is the
optional VT323/Share Tech Mono web font, which gracefully falls back to the system
`monospace` if there's no connection (the layout and numbers are unaffected).

---

## Updating the report

Every `cost:` session automatically regenerates the ledger.
Or run `ledger:` manually any time to refresh from the current history.json.

The report always reflects the complete project history — not just the last session.

---

## Troubleshooting

**"vibe/cost/history.json not found"**
→ You haven't run `cost:` yet in this project. Run it after your next session.

**"history.json is empty"**
→ The file exists but has no sessions. Run `cost:` at the end of a session to populate it.

**"python3: command not found"**
→ Python is not installed. Install from python.org — it's free and takes 2 minutes.
   On most Macs and Linux machines, `python3` is already available.

**Report opens but looks wrong**
→ Try opening `vibe/cost/ledger/index.html` directly in Chrome or Firefox.
   The VT323 font requires an internet connection to load from Google Fonts.
   If offline, it falls back to Share Tech Mono or monospace — same layout, different font.
