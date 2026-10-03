---
name: loop-station
layer: method
description: Observe the harness itself — (WS1) measure context budget as a deterministic, trendable inventory (tokens per CLAUDE.md / skill / agent, lexical redundancy, per-CI cold-write totals; committed history.jsonl), (WS2) reconstruct the real invocation trace (which skills/agents/tools fired and how they nested) from session transcripts, and (WS-A) roll the per-run CI traces up into a committed weekly usage record (per-skill invocation counts; usage.jsonl) — the usage side of the dead-weight join. Use for "context budget", "how big is CLAUDE.md / our skills", "is the harness bloating", "how do our agent loops actually run", "which skills actually get used", "trace this session", "loop station".
---

# Loop Station — harness observatory (WS1 inventory + WS2 trace)

> WS1 (context-budget inventory) is below; the WS2 invocation trace is the second
> section. Both are producers — WS3 (`pocs/loop-station`) renders them.

# WS1 — context-budget inventory

The first, cheapest layer of the **Loop Station observatory** (epic #926): a
**deterministic** snapshot of how big our always-on harness context is and how
much of it is restated, captured at every merge that touches it. No LLM in this
path — `count_tokens` is free tokenization, not generation — so the trend is
clean and reproducible.

> Boundary: this is the **producer**. The daily one-line readout is WS4
> (housekeeping digest reads the latest record); the rendered view is WS3
> (`pocs/loop-station`); the runtime invocation trace is WS2. Compute stays
> here in the scripts — the view only renders.

## What it measures

Walking root `CLAUDE.md` + every skill (`.claude/skills/**`) + every agent
(`.claude/agents/**`) + each LLM CI workflow's `prompt:` block:

- **tokens per artifact** — via Anthropic `count_tokens` when `ANTHROPIC_API_KEY`
  is set (free, deterministic), else a deterministic lexical heuristic. The
  record carries `tokenizer` so a trend is never silently compared across rulers.
- **lexical redundancy** — shingle-containment (8-word shingles). Corpus % of
  duplicated shingle occurrences (intra- *and* cross-file restatement), each
  file's self-redundancy, and the top restated artifact pairs (e.g. the
  near-duplicate `a11y` / `frontend-review` skills). Lexical, deterministic,
  trendable — escalate to embeddings only if real paraphrase slips through.
- **threshold scorecard** — `length` / `redundancy` / `drift-risk` graded
  green/amber/red by fixed **formulas** in `lib/scorecard.mjs` (not LLM
  judgments). Tune the bands in one place there.
- **cold-write totals** — for each CI workflow that runs `claude-code-action`,
  what it cold-writes per run (always-on `CLAUDE.md` + its own `prompt:` block).
- **budget by harness layer** — `totals.byLayer` rolls each skill/agent's tokens up
  by its `layer:` tag (`method` / `stage` / `stack`; epic #952), with untagged
  artifacts (CLAUDE.md, an un-tagged new skill) bucketed as `unlayered` so the
  per-layer tokens reconcile against `totals.tokens`. Quantifies how much of the
  always-on surface is the portable method vs. the swappable crouton stack.

## Files

| file | role |
|------|------|
| `gather.mjs` | walk + count + score → one JSON record on stdout (`--pretty` adds a summary on stderr) |
| `append-history.mjs` | append the record to `writeups/loop-station/history.jsonl`, idempotent per commit |
| `lib/tokens.mjs` | `count_tokens` with deterministic heuristic fallback |
| `lib/redundancy.mjs` | shingle-containment redundancy + self-redundancy |
| `lib/scorecard.mjs` | threshold bands (the one place to tune) |
| `writeups/loop-station/history.jsonl` | the **committed** trend data (see its README) |

## Run by hand

```bash
node .claude/skills/loop-station/gather.mjs --pretty                       # inspect
node .claude/skills/loop-station/gather.mjs | node .claude/skills/loop-station/append-history.mjs   # record a point
LOOP_STATION_FORCE_HEURISTIC=1 node .claude/skills/loop-station/gather.mjs  # force offline tokenizer (deterministic tests)
```

## In CI

`.github/workflows/loop-station-inventory.yml` runs on **merge to `main`**
path-filtered to `CLAUDE.md` / `.claude/skills/**` / `.claude/agents/**`. It
gathers (with `ANTHROPIC_API_KEY` → `count_tokens`), appends, and commits the new
`history.jsonl` line back with `[skip ci]` and the causing PR recorded — one data
point per relevant merge, with the cause attached, no filler.

---

# WS2 — invocation trace

Reconstructs the **real call tree** of a session — which skills/agents/tools
fired, how they nested, how long sub-agents ran — from Claude Code transcripts.

> **Hard privacy rule:** the trace carries **names + correlation ids + durations
> only**, never a tool's `input` or a `tool_result`'s content. It is runtime
> exhaust → **gitignored**, shipped from CI as an artifact, never committed
> (unlike WS1's `history.jsonl`).

## What it reads

`~/.claude/projects/<slug>/<session>.jsonl` (+ its `subagents/agent-*.jsonl`).
Two transcript layouts are auto-detected — the parser handles both because
Claude Code has shipped both:

- **inline** (current local schema) — sub-agents are `isSidechain` records in the
  main transcript; skills tag their calls with `attributionSkill`. Nesting comes
  from the `parentUuid` tree + those markers.
- **files** (the proven prototype layout) — each sub-agent is its own
  `subagents/agent-*.jsonl`, linked to its spawning Agent call by global
  start-time order (robust for sync *and* async agents), carrying durations.

Both reconstruct **2+-level recursion** (agent→agent→…) to the correct depth.

## Files

| file | role |
|------|------|
| `parse-transcripts.mjs` | **claude harness:** parse one Claude Code session → `trace.jsonl` of `{ts,kind,name,parent,depth,agentId?,durMs?}` (also importable: `parseSession()`) |
| `pi-telemetry.mjs` | **pi harness (#944):** adapt pi.dev telemetry (native session JSONL + subagent meta, per `writeups/architecture/pi-telemetry-schema.md`) → the SAME WS2 event shape **and** the #883 ledger slice. `buildPiTrace(dir)` / `runOutcomeToLedgerRecord(outcome)`; CLI: `node pi-telemetry.mjs <dir> [--ledger]` |
| `pi-telemetry.test.mjs` | runs the adapter against the real captured fixtures (`pocs/loop-station/data/pi-telemetry-sample/`); asserts the ledger slice passes the real `eval-ledger/schema.mjs` validator + payload-freeness |
| `collect-traces.mjs` | CI collector — discover the run's session across all project dirs, tag events with the run id, write one NDJSON file (meta header + tagged events) for artifact upload |
| `lib/parse-transcripts.test.mjs` | fixtures for both layouts, 2-level recursion, payload-freeness, defensiveness |

### Harness parity (#944)

WS2 reads whichever harness is active. The data seam (`pocs/loop-station/scripts/prepare-data.mjs`)
branches on `AGENT_HARNESS`: `pi` → `pi-telemetry.mjs` (live `PI_TELEMETRY_DIR` of subagent metas,
else the committed real sample); anything else → the claude transcript parser. **One feed, two
consumers:** the same pi telemetry yields the WS2 trace **and** the `{model,cost,turns,wall}` slice
for the #883 run-outcome ledger — so the cost ledger *consumes* pi telemetry, it doesn't re-derive
it. Note: pi's WS2 trace is **agent-granularity** today (one node per subagent); tool-level nesting
arrives when pi-otel spans are actually collected (schema doc §3, not yet wired).

## Run by hand

```bash
node .claude/skills/loop-station/parse-transcripts.mjs --out trace.jsonl   # latest session
node .claude/skills/loop-station/parse-transcripts.mjs <session> --json     # inspect
node .claude/skills/loop-station/collect-traces.mjs --out loop-station-trace.jsonl
```

## In CI

Every Claude-agent workflow ships its trace via the composite action
**`./.github/actions/loop-station-trace`** (one `uses:` step after the agent,
`if: always()`, tolerant — never fails the job it rides along with). Each
ephemeral runner ships its trace tagged by `run_id`; the weekly WS-A rollup
(below) aggregates the artifacts. The pi workflows are excluded — their trace
comes from pi telemetry (#944), not Claude transcripts.

---

# WS-A — cross-run usage rollup (#1064)

Turns the per-run trace artifacts (which otherwise expire unread) into a
**committed, trendable usage fact**: per-skill/agent invocation counts across
all CI runs in a window. This is the usage side of the dead-weight join — the
observatory panel (#1065) and the advisor's dead-weight rule (#1066) read it.

> Privacy line: raw traces stay gitignored/artifact-only (WS2 rule). What gets
> committed is the **aggregate** — names + counts, the same granularity
> `history.jsonl` commits for size. The record carries `source: 'ci-rollup'`
> and `scope: 'pipeline'` so a consumer can't over-read it: **0 means "never
> fired in CI"**, not "never used" (interactive coverage is #1067).

## Files

| file | role |
|------|------|
| `aggregate-usage.mjs` | N trace NDJSON files → ONE usage record (counts per name, runs, workflows, first/lastSeen). Importable `aggregate(texts, opts)`. Zero input ⇒ a visible meta-only record, never silence |
| `append-usage.mjs` | append the record to `writeups/loop-station/usage.jsonl`, **idempotent per ISO week** (exports `isoWeek()`) |
| `lib/aggregate-usage.test.mjs` | counting, attribution, meta-only-on-empty, scope fields, week-key idempotence |
| `writeups/loop-station/usage.jsonl` | the **committed** usage trend (one record per week) |

## Run by hand

```bash
node .claude/skills/loop-station/aggregate-usage.mjs --window 7 trace1.jsonl trace2.jsonl \
  | node .claude/skills/loop-station/append-usage.mjs
```

## In CI

`.github/workflows/loop-station-usage.yml` runs **weekly** (Mondays 06:41 UTC,
before the advisor): list the window's `loop-station-trace-*` artifacts →
download → aggregate → append → commit back `[skip ci]`. Fail-loud contract
(#1037): a listing failure **fails the job** (an outage must not read as a
quiet week); zero artifacts appends a meta-only record (a gap you can see).

---

# WS5 — advisor (state → actionable ticket)

Turns the observatory from numbers-to-look-at into decisions. An agent reviews the
inventory state and, **only when something's actionable**, files a single GitHub
issue assigned to the maintainer with concrete recommendations.

> Two layers, kept separate: deterministic **numbers → the WS4 digest** (no LLM);
> qualitative **remarks → a ticket** (this). The LLM never touches the trend and
> only *recommends* — epic #926's observatory-not-builder boundary holds.

## Files

| file | role |
|------|------|
| `advisor.mjs` | **deterministic gate** — reads `history.jsonl` + `usage.jsonl`, surfaces candidate findings (scorecard reds, sharp always-on growth, redundancy jumps, dead-weight skills), decides `actionable`. No LLM, no issue. Importable `analyze()` / `usageCoverage()`. |
| `lib/advisor.test.mjs` | findings logic (reds flag, growth flags, cross-tokenizer deltas are NOT compared, dead-weight coverage gates, deterministic) |
| `.github/workflows/loop-station-advisor.yml` | weekly: run the gate → **only if actionable** invoke `claude-code-action` to open/update ONE `loop-station-advisor` issue assigned to `pmcp` |

### Dead-weight rule (#1066)

Joins WS1 size × WS-A usage: an **oversized skill** (≥ the scorecard's artifact
amber band) that **provably never fired** becomes one `dead-weight` finding
listing the candidates. "Provably" is gated — the rule judges ONLY when the
usage rollup covers **≥ 60 cumulative days AND ≥ 5 observed runs** (tune in
`ADVISOR`); anything thinner stays silent with `usage.why` naming the reason,
because "no data" must never read as "dead". Evidence carries
`scope: 'pipeline'` — 0 means *never fired in CI*, not never used (#1067).

## Why the gate is deterministic

The cheap deterministic pass decides *whether to bother the human* (and whether to
spend an LLM call) — so the model runs only on a real signal, never on a quiet
week, and the trend numbers stay LLM-free. Deltas are compared **only within the
same tokenizer** (a heuristic→anthropic switch isn't real growth).

## Run by hand

```bash
node .claude/skills/loop-station/advisor.mjs --pretty   # see findings + actionable verdict
```

---

# WS6 — accountability scoreboard (#1570)

The reviewer-vs-author lens: every **confirmed defect** is a severity-weighted,
zero-sum-ish transaction — **−w to the author flow, +w to the gate that caught it**
— and a clean merge earns its author +1. Turns review gates and coding agents into
opposing teams so we can see who ships clean and which gates actually earn their keep.

> Boundary holds: a new *lens* over existing data, not a new pipeline. It joins the
> **findings** ledger (`writeups/loop-station/findings.jsonl`) × the run-outcome
> **eval-ledger** (`writeups/reports/eval-ledger.jsonl`, #883). The tally is
> deterministic arithmetic — no LLM. Severity comes from the gate's own rating.

## The asymmetric model (decided on #1570)

| Event | Author | Catcher | Gate that missed it |
|---|--:|--:|--:|
| Defect caught in review | −w | +w | — |
| Clean merge, stays clean | +1 | 0 | — |
| Defect escaped, caught later | −w·2 | +w | −w |
| Flag rejected (false-positive) | 0 | −w (noise) | — |

`w` is severity-weighted (`critical 5 / high 3 / medium 2 / low 1`). A find scores
**only once confirmed** (fix merged / reverted / `lgtm`) — unconfirmed = `pending`.

**Two lanes (`class`).** `defect` (default) = a correctness/security/a11y/convention failure —
the main board. `quality` = a preference on *correct* code (a `/simplify` cleanup) — a
**separate low-weight lane** that never touches an author's defect Net/Rate (so it can't
punish verbose-but-correct code or drown the defect signal). A quality gate captures on any
change (`capture-finding.mjs --gate simplify --class quality`), not just 🔴 critical.

## Files (live in `scripts/eval-ledger/` with the ledger they join)

| file | role |
|------|------|
| `findings-schema.mjs` | finding record shape + `validate()` + `transactionsFor()` (the scoring rules — tune weights here) + `dedupKey()` |
| `append-finding.mjs` | validate + append ONE finding to `findings.jsonl` (idempotent via `dedupKey`; `--check` / `--no-dedup`) |
| `accountability.mjs` | join findings × ledger → two leaderboards (markdown / `--json` / `--html`); importable `tally()` |
| `capture-finding.mjs` | gate-side: a `<gate>-verdict.json` → a pending finding **candidate** (only for 🔴 critical) |
| `ingest-findings.mjs` | rollup-side: resolve candidates by PR-merge fact (merged → confirmed · closed → drop · open → skip); importable `resolveCandidates()` |
| `reconcile-findings.mjs` | rollup-side: reverted eval-ledger rows → escaped-defect findings; importable `reconcile()` |
| `accountability.test.mjs` | pins the arithmetic + reconcile + candidate resolution (19 tests) |

## Capture in CI (#1570)

Two deterministic sources feed `findings.jsonl` — **no LLM, no CI state machine**:

1. **PR gates** (`frontend-review` / `a11y` / `red-team`) upload a finding **candidate**
   artifact (`loop-station-finding-*`) whenever they flag a 🔴 critical. Confirmation is
   the **durable PR-merge fact**: merged ⇒ the blocking defect was fixed ⇒ a *confirmed
   caught* defect; closed ⇒ dropped; open ⇒ left for a later run.
2. **Reverts** — a `reverted` run in the eval-ledger ⇒ a *confirmed escaped* defect.

`.github/workflows/loop-station-findings.yml` (merge-to-`main` + weekly, mirrors
`loop-station-usage.yml`) downloads the candidates, resolves them, runs `reconcile`, and
commits new findings to `main`. **Only this main-context job writes the committed ledger** —
a PR-branch gate run never does. Rendered in `pocs/loop-station` (the `AccountabilityBoard`
panel, staged by its `prepare-data.mjs`).

## Run by hand

```bash
node scripts/eval-ledger/accountability.mjs            # the two leaderboards
node scripts/eval-ledger/append-finding.mjs --gate code-review --severity high \
  --status confirmed --confirmed_via fix-merged --author_flow task-worker --author_ref <PR-url>
```
