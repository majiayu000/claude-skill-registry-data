---
name: vibe-cost
description: >
  Tracks and reports token usage and dollar cost across every level of a
  vibe-* project — per task, per session, per feature, per phase, and
  total project spend. Auto-runs at the end of every session with estimates.
  When invoked manually with "cost:" accepts pasted Claude Code /cost output
  for precise numbers. Detects eight waste patterns: CP-01 context overhead,
  CP-02 repeated reads, CP-03 unstructured output, CP-04 parallel multiplication,
  CP-05 low cache hit rate, CP-06 oversized planning, CP-07 environment
  debugging waste (env issues rediscovered each session), CP-08 over-investigation
  (files read before intent confirmed). Max 4 recommendations per session.
  Triggers on "cost:", "how much has this cost", "show cost report",
  "token usage", "what's the spend so far", "is this getting expensive".
  Also auto-invoked at end of vibe-add-feature, vibe-fix-bug, vibe-new-app, vibe-review.
---

# Vibe Cost Skill

Tracks token usage and dollar cost at every granularity level.
Auto-estimates when running automatically. Accepts real numbers on demand.
Shows where the money is going and how to spend less of it.

---

## The principle

You can't optimise what you don't measure.
Most teams using Claude Code have no idea which tasks are burning
the most tokens, whether costs are trending up or down, or
whether a simple prompt change would cut their bill in half.

This skill measures first, then recommends.
Never recommends a change without data to back it.

---

## Two modes

### Mode A — Automatic (end of session)
Triggered automatically by other vibe-* skills at session end.
Uses estimates based on what the session did — files read, tasks completed,
context size, CODEBASE.md length, agent patterns detected.
Precision: ±20-30%. Good enough for trending. Not precise enough for billing.

### Mode B — Precise (manual invocation)
User runs `cost:` and pastes the output of `/cost` from Claude Code.
The skill reads real token counts, calculates exact dollar costs,
compares against estimates, and produces a precise report.
Also available: user can run `cost:` with no paste — skill uses latest estimates.

---

## Step 0 — Detect invocation mode and context

```bash
# Check for existing cost data
ls vibe/cost/ 2>/dev/null && echo "HISTORY EXISTS" || echo "FIRST RUN"

# Read project context
cat CLAUDE.md 2>/dev/null | grep -E "model|MODEL" || echo "model not specified"
cat vibe/TASKS.md 2>/dev/null | head -50
```

**Detect which mode:**
- Called automatically by another skill → Mode A (estimate)
- User typed `cost:` with pasted data → Mode B (precise)
- User typed `cost:` with no data → Mode B using latest estimates, offer to paste

**Detect current model from CLAUDE.md:**
Look for `MODEL=` or `## Model` section.
If not found → use the `DEFAULT_MODEL` from `references/PRICING.md`
(currently `claude-sonnet-5`). Do not hardcode a model here — PRICING.md is the
single source of truth for the lineup, prices, and default.

**Staleness check:** read the "Last updated" date at the top of
`references/PRICING.md`. If it is more than ~90 days old, prepend a one-line
warning to the cost report ("⚠️ Pricing data is N days old — verify at
anthropic.com/pricing") so estimates don't silently drift after a price change.

**Create cost directory if needed:**
```bash
mkdir -p vibe/cost
```

---

## Step 1 — Read session context

Read these files to understand what this session did:

```bash
cat vibe/TASKS.md 2>/dev/null
cat vibe/DECISIONS.md 2>/dev/null | tail -50  # recent decisions only
ls vibe/features/ 2>/dev/null
ls vibe/bugs/ 2>/dev/null
cat vibe/cost/baseline.json 2>/dev/null       # previous session data
cat vibe/cost/history.json 2>/dev/null        # all sessions
```

**Identify what happened this session:**
- Which tasks were completed? (read TASKS.md for [x] items added recently)
- Which feature/bug was being worked on?
- What phase is the project in?
- How large is the current CODEBASE.md? (proxy for context size)
- Were any parallel subagents used? (multiplies token cost)

---

## Step 2 — Calculate costs

Read `references/PRICING.md` before this step.

### Mode A — Estimation

**Estimate input tokens per task type:**

| Task type | Est. input tokens | Reasoning |
|-----------|------------------|-----------|
| Planning task (brainstorm/architect/spec) | 8,000–15,000 | Heavy reading: BRIEF.md, SPEC.md, ARCHITECTURE.md |
| Feature task — small (S) | 10,000–20,000 | CLAUDE.md + CODEBASE.md + feature files |
| Feature task — medium (M) | 20,000–40,000 | Same + more context files |
| Feature task — large (L) | 40,000–80,000 | Large context, many file reads |
| Bug fix — trivial | 8,000–15,000 | CLAUDE.md + affected files |
| Bug fix — significant | 20,000–50,000 | Deep codebase reading |
| Review task | 30,000–60,000 | Reads entire phase output |
| Test generation | 15,000–30,000 | Blast radius analysis |
| Perf audit | 20,000–40,000 | Multi-layer file reads |
| Document generation | 15,000–30,000 | Full codebase scan |

**Estimate output tokens per task type:**

| Task type | Est. output tokens |
|-----------|-------------------|
| Planning/spec writing | 2,000–5,000 |
| Code generation (S) | 500–1,500 |
| Code generation (M) | 1,500–4,000 |
| Code generation (L) | 4,000–10,000 |
| Review report | 1,000–3,000 |
| Test generation | 2,000–6,000 |
| Documentation | 3,000–8,000 |

**Context size multiplier:**
```
CODEBASE.md size → estimate token overhead per session
< 5KB:   +5,000 input tokens (small project)
5-20KB:  +15,000 input tokens (growing project)
20-50KB: +30,000 input tokens (mature project)
50KB+:   +50,000 input tokens (large project — context pressure warning)
```

**Parallel subagent multiplier:**
If `vibe-parallel` was used this session → multiply total by number of Wave 1 subagents.
Each subagent has its own context window, effectively running a full session.

**Calculate session estimate:**
```
session_input_tokens = sum(task_input_estimates) + context_overhead
session_output_tokens = sum(task_output_estimates)
session_cost_estimate = calculate_cost(session_input_tokens, session_output_tokens, model)
```

### Mode B — Precise (pasted /cost data)

Parse the pasted `/cost` output. Format varies slightly by Claude Code version but typically:

```
Total cost:      $X.XX
Total duration:  Xm Xs
Total turns:     N
Input tokens:    X (cache read: X, cache write: X)
Output tokens:   X
```

Extract:
- `total_cost` — dollar amount
- `input_tokens` — total including cache
- `cache_read_tokens` — tokens served from cache (90% cheaper)
- `cache_write_tokens` — tokens written to cache (25% more expensive)
- `output_tokens`
- `duration` — total session time
- `turns` — number of back-and-forth exchanges

**Recalculate with cache breakdown for accuracy:**
```
actual_cost = (
  (input_tokens - cache_read_tokens - cache_write_tokens) * base_input_price
  + cache_read_tokens * (base_input_price * 0.10)
  + cache_write_tokens * (base_input_price * 1.25)
  + output_tokens * output_price
)
```

If pasted cost differs from estimate by > 50% → flag:
> "Actual cost was [higher/lower] than estimated by [X]%. Updating estimation model."
Adjust future estimates based on the delta.

---

## Step 3 — Build cost breakdown

**Per-task breakdown:**
For each task completed this session, assign a cost estimate:

```
Session tasks:
  TASK-001 · Set up FastAPI scaffold        S  ~$0.08
  TASK-002 · Prisma schema design           M  ~$0.15
  TASK-003 · GuardianAgent implementation   L  ~$0.45
  TASK-004 · GuardianVerifier               M  ~$0.18
  TASK-005 · Write tests (blast radius)     M  ~$0.22
```

In Mode B (precise), distribute real cost proportionally by task size:
```
task_cost = (task_size_weight / total_size_weight) * session_total_cost
```
Where S=1, M=2, L=4.

**Per-phase running total:**
Read history.json to get cumulative cost per phase.

```
Phase 1 (foundation):    $2.40  (12 tasks, 4 sessions)
Phase 2 (in progress):   $1.85  (8 tasks, 3 sessions so far)
Phase 3 (not started):   $0.00
Total project to date:   $4.25
```

**Per-feature cost:**
For each feature folder in `vibe/features/`, sum tasks attributed to it:

```
Feature costs:
  auth-system:          $0.85
  guardian-agent:       $1.20  ← most expensive feature so far
  scout-agent:          $0.65
  brand-dna-ui:         $0.55
```

**Trend analysis:**
Compare this session against previous sessions from history.json:

```
Session cost trend:
  Session 1 (brainstorm+arch):  $0.35
  Session 2 (Phase 1 build):    $1.20
  Session 3 (Phase 1 build):    $0.95  ↓ -21%
  Session 4 (this session):     $1.10  ↑ +16%

Trend: costs relatively stable. No significant drift.
```

Flag if any session costs > 2× the average → likely context bloat or
unexpectedly large task in that session.

---

## Step 4 — Identify expensive patterns

Read `references/COST_PATTERNS.md` for the full pattern catalogue.

Analyse this session's cost breakdown to detect:

**CP-01 — Large context overhead (most common)**
Signal: cost per task is unusually high relative to task size
Cause: CODEBASE.md or SPEC.md has grown large and is loaded every turn
Threshold: if context overhead > 40% of session cost → flag

**CP-02 — Repeated file reads**
Signal: multiple tasks reading the same large files
Cause: no caching, each task re-reads ARCHITECTURE.md from scratch
Threshold: >3 tasks reading same file in one session → flag

**CP-03 — Unstructured output**
Signal: output tokens unusually high for task type
Cause: agent generating prose where JSON schema would be 3× more compact
Threshold: output tokens > 2× expected for task size → flag

**CP-04 — Parallel subagent multiplication**
Signal: cost spike on sessions using vibe-parallel
Cause: N subagents × full context = N× the cost
Check: was parallel appropriate here, or could tasks have run sequentially cheaply?

**CP-05 — Missing prompt caching**
Signal: cache_read_tokens near 0 in Mode B data
Cause: CLAUDE.md or system prompt not eligible for caching (changes too frequently)
Threshold: if cache hit rate < 20% on sessions > $1 → flag

**CP-06 — Over-sized planning sessions**
Signal: planning tasks (brainstorm/architect/spec) cost more than build tasks
Cause: too much back-and-forth in planning, context not trimmed between exchanges
Threshold: planning session > $0.50 → flag for review

---

## Step 5 — Generate recommendations

For each detected pattern, generate one specific recommendation:

```
COST RECOMMENDATIONS
────────────────────

💡 [CP-01] Context overhead is 48% of this session's cost
   CODEBASE.md is 38KB — loaded on every task turn.
   Fix: Use vibe-context to load only the relevant section per task.
   Est. saving: ~$0.30/session (~25% reduction)

💡 [CP-03] Output tokens 3× expected on TASK-003
   GuardianAgent prompt asks for prose explanation + JSON.
   Fix: Add response_format={"type":"json_object"} to agent call.
   Remove the "explain your reasoning" instruction — verifier doesn't need it.
   Est. saving: ~$0.15/session on agent tasks

💡 [CP-05] Cache hit rate: 8% (very low)
   CLAUDE.md is modified frequently — disables prompt caching.
   Fix: Split CLAUDE.md into stable sections (never changes) and
   dynamic sections (VIBE_MODE, ACTIVE FEATURE). Cache the stable part.
   Est. saving: ~$0.20/session on large sessions (cache reads = 90% cheaper)

💡 Model consideration (see references/PRICING.md → model selection guide)
   Sessions averaging $0.75 with claude-sonnet-5.
   Tasks TASK-001, TASK-002 (scaffold + schema) are straightforward —
   could run on claude-haiku-4-5 at ~2× lower cost.
   Also try Sonnet 5 at effort:low before switching models — often matches a
   weaker model and keeps one cache namespace.
   Est. saving: ~$0.12/session if routine tasks use Haiku
```

**Never recommend a change without an estimated saving.**
**Never recommend more than 4 fixes per session** — overwhelm = ignored.
**Prioritise by estimated saving** — biggest win first.

---

## Step 6 — Update cost files

```bash
# Update baseline.json with this session
python3 -c "
import json, os
from datetime import datetime
from pathlib import Path

session = {
    'session_id': '[timestamp]',
    'date': '[ISO date]',
    'mode': '[estimate|precise]',
    'trigger': '[auto|manual]',
    'model': '[model name]',
    'tasks_completed': [N],
    'phase': '[Phase N / feature name]',
    'input_tokens': [N],
    'output_tokens': [N],
    'cache_read_tokens': [N],  # 0 if Mode A
    'cache_write_tokens': [N], # 0 if Mode A
    'cost_usd': [N],
    'is_estimate': [True|False],
    'patterns_detected': ['CP-01', 'CP-03'],
    'task_breakdown': {
        'TASK-ID': {'size': 'M', 'cost_usd': N, 'input_tokens': N, 'output_tokens': N}
    }
}

# Save as baseline
Path('vibe/cost/baseline.json').write_text(json.dumps(session, indent=2))

# Append to history
history_path = Path('vibe/cost/history.json')
history = json.loads(history_path.read_text()) if history_path.exists() else []
history.append(session)
history_path.write_text(json.dumps(history, indent=2))
print(f'Cost data saved — session #{len(history)}')
"
```

Also save the full report:
```bash
# vibe/cost/report-[YYYY-MM-DD]-[HH-MM].md
```

---

## Step 6b — Write summary.json for vibe-ledger

After updating history.json, Claude must write `vibe/cost/summary.json` directly.
**Do NOT use a Python template with placeholders. Claude computes all values now and writes the real JSON.**

By this point in the skill, Claude has already read TASKS.md, DECISIONS.md, history.json, and completed the full cost analysis in Steps 1–5. All the information needed is already in context.

**Claude must:**

1. Compute all values from what it already knows
2. Write the file using a Python one-liner with the real JSON string inline

```bash
python3 -c "
from pathlib import Path
import json

summary = SUMMARY_JSON_HERE

Path('vibe/cost/summary.json').write_text(json.dumps(summary, indent=2))
print('summary.json written')
"
```

Where `SUMMARY_JSON_HERE` is replaced with the actual computed dict — real numbers, real strings, no placeholders.

---

**How to compute each field — use real values, not placeholders:**

**`project_name`** — read from the first line of CLAUDE.md (`# ProjectName`) or use the current directory name.

**`build_progress_pct`** — count `[x]` tasks in TASKS.md divided by total tasks (both `[x]` and `[ ]`) × 100. Round to nearest integer.

**`tasks_remaining`** — count `[ ]` items in TASKS.md. If TASKS.md unreadable, use 8 as default.

**`phase_summary`** — one entry per phase found in TASKS.md. Use these exact status values:
- `"complete"` — all tasks in phase are `[x]`
- `"active"` — phase has a mix of `[x]` and `[ ]`
- `"not_started"` — all tasks are `[ ]` or phase not yet started
Sum cost_usd for each phase from history.json sessions whose `phase` field matches.

**`feature_costs`** — group history.json task_breakdown entries into plain English feature areas. Use labels a non-developer would understand (e.g. "Backend APIs", "Frontend screens", "Dev tooling"). Sum cost_usd per group.

**`at_a_glance`** — write 2–3 sentences in plain English. Must mention: total spend, most expensive session and why, whether costs are healthy or concerning. This appears as the opening paragraph of the ledger. Write it as a human would — not as a template.

Example of good at_a_glance:
> "You've spent $4.10 across 7 sessions over 3 days. April 12 was the heavy build day — $3.35 covering all of Phase 1 and Phase 2 backend and frontend. Costs are trending down as the complex work is behind you."

**`session_narratives`** — one paragraph per session ID (key = session_id from history.json). Explain in plain English what happened and why it cost what it did. Use actual task names. 2–3 sentences max. These appear inline under each session row in the ledger.

Example of good session narrative:
> "The most expensive session — 10 tasks including the two most complex features (P2-rides-BE and P2-routes-BE). Cost per task was $0.13, right at the project average despite the session size."

**`recommendations`** — one entry per pattern detected in Step 5. Each must have:
- `code` — CP pattern code (e.g. "CP-01")
- `title` — plain English one-liner, 8–12 words
- `body` — 2–4 sentences explaining the problem and fix. Use specific file names (e.g. "CODEBASE.md is 36KB"). No bullet points.
- `saving` — e.g. "save ~$0.10/session"
- `severity` — `"ok"` (green), `"warn"` (amber), or `"fix"` (red)

**`forecast_narrative`** — 2–3 sentences naming the actual remaining work from TASKS.md. Name real task IDs or phase names. Include the cost range and any saving from fixing caching.

Example:
> "Phase 3 has 8 tasks remaining — polish, tests, and deployment (P3-01 through P3-08). Based on similar M-sized tasks in Phase 2, expect $0.87–$1.23 to finish. Fixing caching before Phase 3 starts could save $0.20–0.40."

---

**If any field truly cannot be determined** — use `null` for numbers, `""` for strings, `[]` for lists. The ledger handles nulls gracefully.

---

## Step 7 — Present the report

```
COST REPORT — [Project Name]
[Mode: Estimated ±25% | Precise (from /cost)]
[Session #N · [date] · [model]]
══════════════════════════════════════════

THIS SESSION
  Input tokens:     [N] ([cache reads: N] [cache writes: N])
  Output tokens:    [N]
  Session cost:     $[X.XX] [estimated | actual]
  Duration:         [Xm Xs]
  Tasks completed:  [N]
  Cost per task:    $[X.XX] average

  Most expensive tasks this session:
    1. [TASK-ID] · [description] · [size] · $[X.XX]
    2. [TASK-ID] · [description] · [size] · $[X.XX]
    3. [TASK-ID] · [description] · [size] · $[X.XX]

PROJECT TOTALS
  Total sessions:   [N]
  Total cost:       $[X.XX] [estimated | mix of estimated + precise]

  By phase:
    Phase 1:        $[X.XX] ([N] sessions) [complete]
    Phase 2:        $[X.XX] ([N] sessions) [in progress]
    Phase 3:        $[X.XX] ([N] sessions) [not started]

  By feature:
    [feature]:      $[X.XX]  ← most expensive
    [feature]:      $[X.XX]
    [feature]:      $[X.XX]

TREND (last 5 sessions)
  [sparkline: ▂▄█▆▅]
  Session [N-4]: $[X.XX]
  Session [N-3]: $[X.XX]
  Session [N-2]: $[X.XX]
  Session [N-1]: $[X.XX]
  This session:  $[X.XX] [↑ +X% | ↓ -X% | → stable]

  [⚠️ Cost spike detected: this session 2× average — see recommendations]
  [✅ Costs stable — within 20% of 5-session average]

RECOMMENDATIONS ([N] found)
  [see Step 5 output — max 4, sorted by saving]

PROJECT COST FORECAST
  Completed: [N]% of planned tasks
  Spent:     $[X.XX]
  Est. remaining at current rate: $[X.XX]
  Est. total project cost:        $[X.XX]

[Mode A footer:]
  ⚠️ These are estimates (±25%). For precise tracking, run /cost in
  Claude Code at session end, then paste with: cost: [paste here]

[Mode B footer:]
  ✅ Precise data from Claude Code /cost output.
  Estimation model updated based on actual vs estimate delta.

Full report: vibe/cost/report-[date]-[time].md
History:     vibe/cost/history.json ([N] sessions)
```

---

## Step 8 — Update vibe docs

**vibe/TASKS.md** — append to "What just happened":
```
💰 Cost tracked — Session #[N]: $[X.XX] [est.|actual]
   Project total: $[X.XX] · Trend: [↑/↓/→]
   vibe/cost/report-[date].md
```

**vibe/DECISIONS.md** — only if a cost recommendation was acted on:
```
---
## [date] — Cost optimisation: [what was changed]
- **Type**: tech-choice
- **Saving**: ~$[X.XX]/session
- **Change**: [what was modified — prompt, model, context strategy]
---
```

---

## Absolute rules

**Estimates are always labelled as estimates.**
Never present an estimate as a precise number.
Always show the ±% uncertainty range.

**Never recommend a change that breaks functionality.**
"Use Haiku instead of Sonnet" is only valid for tasks where
Haiku demonstrably performs well — not for complex reasoning tasks.
If uncertain, frame as "consider testing" not "switch to."

**Trends need at least 3 data points.**
Don't draw trend conclusions from 1-2 sessions.
With < 3 sessions: "Not enough data for trend analysis yet."

**Cost forecasts are rough.**
Project cost forecast assumes current rate continues.
Flag this assumption explicitly — a Phase 3 polish phase is
usually cheaper than a Phase 2 feature build phase.

**Recommendations are optional.**
The user can ignore every recommendation.
Never nag — surface once per session, log to report, move on.
