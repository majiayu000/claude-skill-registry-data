---
name: browser-transcript-mining
description: Mine a dump of production `web-browser` subagent transcripts (jsonl) for browser-harness friction — soft failures, workarounds, missing tools, misleading output. Deterministic stats + compact traces first, then Lane A (Opus reads whole sessions with screenshots, open rubric, discovery) and Lane B (Sonnet classifies compact traces against a closed taxonomy, prevalence). Use when a new transcript dump arrives, after shipping a harness fix to see if the metric moved, or when someone asks "where does the browser harness waste the agent's steps".
---

# Browser transcript mining

Turns a zip of `web-browser` subagent transcripts into a ranked list of harness
bugs and optimization opportunities, cheaply enough to re-run on every dump. The
rationale, data facts and pipeline design are in
[docs/browser-transcript-mining.md](../../../docs/browser-transcript-mining.md);
the first run's report is
[docs/browser-harness-friction-themes-2026-09.md](../../../docs/browser-harness-friction-themes-2026-09.md).

The pieces, all under `scripts/`:

| Script | Stage | What it does |
|---|---|---|
| `stats.py <work>` | 0 | One streaming pass: tool-call histogram, hard-error strings, result sizes, token totals, `browser_run` subcommands, soft-error keywords. Writes `per_file.json`. |
| `signals.py <work>` | 0 | Behavioral signals: workaround phrases in assistant text, identical consecutive calls, tool bigrams, errors by tool, sample `browser_run`/`browser_eval` inputs, final-message outcome keywords. |
| `compact.py <work> [N]` | 0 | Each transcript → `traces/<agent>.txt` (one line per call, screenshots dropped, ~170× smaller) and `sessions.jsonl` with per-session metrics and a heuristic friction score. |
| `by_era.py <work>` | 1 | Counts error patterns per harness era (pre/post the 2026-06-12 audit) so already-fixed themes don't rank. |
| `cost_estimate.py <work>` | – | Token and $ estimate for reviewing sessions as-is (text + images) with Opus. |
| `lane_a_prep.py <work>` | 2A | Samples 200 post-audit sessions in three strata, renders each as review-ready markdown parts + extracted PNGs under `laneA/rendered/`, bin-packs them into agent batches, writes `laneA/review-args.json` and `laneA/synthesis-args.json`. |
| `lane-a-review.workflow.js` | 2A | Workflow: one Opus agent per batch reads whole sessions and writes `laneA/findings/<agent>.md` + structured findings. |
| `lane_a_aggregate.py <work> [task-output.json]` | 2A→3 | Extracts the workflow result, writes `laneA/aggregate.md`, `laneA/findings.rows.json`, and per-area slices under `laneA/by_area/`. |
| `lane-a-synthesis.workflow.js` | 3 | Workflow: one Opus agent per area clusters findings into themes (`laneA/themes/<area>.md`), then one merge agent ranks and writes `laneA/themes.md`. |
| `lane-b-triage.workflow.js` | 2B | Workflow: Sonnet classifies compact traces against a closed taxonomy → strict JSON per session. Not yet exercised end to end. |

The Python scripts are analysis prototypes (no Zod; they never write to the app's
DB or config). The `.workflow.js` files run only through the Workflow tool.

## Prerequisites

- The transcript zip. Layout: `{host}/{agent}/{session_id}/agent-{id}.jsonl` plus
  `MANIFEST.csv` (columns include `dest_key`, `host`, `agent`, `session_id`,
  `description`). Each line is a Claude Code transcript record; browser tools are
  `mcp__browser__browser_*`.
- Python 3.10+, no third-party packages. `jq` helps for spot checks.
- A work dir with room for ~2× the zip (unzipped data + rendered sessions).
  Use the session scratchpad unless the user names a location.

## Procedure

### 1. Unpack and get the deterministic picture (~5 min, zero LLM tokens)

```bash
WORK=<scratchpad>/mining; mkdir -p "$WORK/data"
unzip -q -o <dump.zip> -d "$WORK/data"
S=.claude/skills/browser-transcript-mining/scripts
python3 $S/stats.py   "$WORK" > "$WORK/stats.txt"
python3 $S/signals.py "$WORK" > "$WORK/signals.txt"
python3 $S/compact.py "$WORK"          # traces/ + sessions.jsonl
python3 $S/by_era.py  "$WORK"
```

Read `stats.txt` and `signals.txt` in full. What to look for:

- `browser_run` subcommand histogram = the missing-tool list.
- Top `is_error` strings, then the same strings split by era in `by_era.py`
  output. A pattern that is large pre-audit and near zero after is already fixed.
- Identical consecutive calls (polling by snapshot), snapshot→screenshot pairs,
  workaround phrases.

Edit `by_era.py`'s `PATS` table when a new error string matters; edit the era cut
dates when a new harness batch ships (`git log --date=short -- agent-container/src/tools/browser.ts agent-container/src/browser-digest.ts agent-container/src/snapshot-format.ts`).

Sanity-check a few compact traces (`traces/<agent>.txt`) before spending tokens:
the `[REPEAT]`, `[SNAP->SHOT]`, `[REF-NOT-IN-LAST-SNAPSHOT]`, `[UNCHANGED?]`
flags should line up with what you see in the raw jsonl.

### 2. Lane A — discovery (Opus reads whole sessions)

```bash
MINING_REPO=$(pwd) python3 $S/lane_a_prep.py "$WORK"
```

Prints the strata counts, the token estimate, and the batch count. Strata:
67 highest detector density, 66 long sessions (≥40 calls) with friction below
median, 67 uniformly random. Infra-dominated sessions and sessions with fewer
than 8 calls are excluded. Change `N`, the strata sizes, or the `BUDGET`/`MAX_PER`
bin-packing constants at the top of the script if the budget differs.

Launch the review with the Workflow tool: `scriptPath` =
`scripts/lane-a-review.workflow.js`, `args` = the contents of
`$WORK/laneA/review-args.json`. Expect ~80 agents, ~17M subagent tokens, ~50 min
for 200 sessions. Each agent grounds itself in
`agent-container/src/web-browser-agent-prompt.md`, `agent-container/docs/browser-use.md`
and `agent-container/src/tools/browser.ts`, reads its sessions' parts and screenshots,
writes `laneA/findings/<agent>.md`, and returns structured findings.

When it completes, save the task output and aggregate:

```bash
python3 $S/lane_a_aggregate.py "$WORK" <path to the Workflow task .output json>
```

Spot-check two findings files (one from the `random` stratum) before synthesis;
they should cite call numbers, quote harness text verbatim, and separate
site-side blockers from harness friction. Then launch the synthesis workflow:
`scriptPath` = `scripts/lane-a-synthesis.workflow.js`, `args` = contents of
`$WORK/laneA/synthesis-args.json`. Expect 14 agents, ~2.5M tokens, ~50 min. The
merge agent writes `$WORK/laneA/themes.md`: executive summary, ranked themes
with exemplars and proposed fixes, prompt guidance that cost time, what the
harness got right, not-harness, and measurement hooks for new detectors.

Verify any code claim the report makes (it cites `file:line`) before repeating it.

### 3. Lane B — measurement (Sonnet classifies compact traces)

Run after lane A so the taxonomy includes what lane A found. Build the agent list
from `sessions.jsonl` (post-audit, `tools >= 8`), then launch the Workflow with
`scriptPath` = `scripts/lane-b-triage.workflow.js` and args
`{tracesDir, agents, outDir, taxonomy, perAgent}`. ~10 traces per Sonnet agent.
Aggregate the returned `sessions` by category and stratum for prevalence.

### 4. Close the loop

- Every theme in `themes.md` marked new or variant gets a rule in the
  deterministic pass (a `PATS` entry in `by_era.py` or a flag in `compact.py`).
- Put the report under `docs/` with the dump date in the filename.
- After a fix ships, re-run step 1 on the next dump and compare per-era counts.

## Costs (first run, 2026-09-10, 1,188 transcripts / 1.8 GB)

| Step | Tokens | Wall clock |
|---|---|---|
| stats + signals + compact + by_era | 0 | ~5 min |
| Lane A review, 200 sessions, Opus | 16.7M | 52 min |
| Lane A synthesis, Opus | 2.5M | 50 min |
| Lane B, all post-audit traces, Sonnet (estimate) | ~3M | — |

## Gotchas

- `compact.py <work> N` rewrites `sessions.jsonl` with only N rows. Use the limit
  only for a smoke test, then rerun without it.
- Rendered sessions are split into ≤1200-line parts and lines wrapped at 1900
  chars because the Read tool truncates longer lines; a `⏎` marks a wrap.
- Workflow scripts cannot use `Date.now()`/`Math.random()` and have no filesystem
  access; everything path-shaped goes through `args` (the prep script writes them).
- Six sessions in the first dump exceeded 250k tokens alone; the bin-packer gives
  those their own agent. Anything past ~600k text tokens should be split by turn
  ranges before review.
- Reviewer wasted-call estimates double count across themes. Rank by distinct
  sessions affected × severity; use wasted calls as a tiebreaker only.
- Exclude the pre-audit era (before 2026-06-15 in the first dump) from LLM lanes
  or the top theme will be a bug that is already fixed.
