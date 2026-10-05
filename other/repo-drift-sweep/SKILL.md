---
name: repo-drift-sweep
description: Use when performing a scheduled or requested repository drift sweep — stale docs, duplicated or unclear config, missing tests, or messy scripts — and syncing docs/ with the implementation.
argument-hint: "[--report-only]"
---

# Repo Drift Sweep

**Core principle:** Once a week, find where the repo has rotted, fix the worst 3
things, prove each fix with a verifier, get it reviewed by a *fresh* sub-agent
context, and open a PR. The Top-3 report is the primary deliverable — it ships
even if `--report-only` is passed.

This skill **orchestrates** two existing skills instead of reinventing them:
- `code-review` — 5-lens review in parallel sub-agents (isolated contexts).
- `new-pr` — PR creation.

---

## Workflow

```
[1] BASELINE     branch off main, get diff range
      ▼
[2] SCAN         5 parallel sub-agents, one per drift category (read-only)
      ▼
[3] RANK         score → Top 3 candidates (path, risk, verifier)  ← primary output
      ▼   (stop here if --report-only — no branch, no edits)
[4] FIX          apply the candidate's fix on the branch
      ▼
[5] VERIFY       verifier must pass; else swap in next-ranked until 3 verified
                 (if <3 can be verified → stop, no PR)
      ▼
[6] REVIEW       invoke `code-review` (fresh sub-agents)  → fix Critical+Important
      ▼
[7] PR           invoke `new-pr` with the report embedded in the body
```

---

## Step 1 — Baseline

```bash
git fetch origin
BASE_SHA=$(git merge-base HEAD origin/main)
SWEEP_DATE=$(git log -1 --format=%cd --date=format:%Y-%m-%d)   # reproducible; not `date`
```

**If `--report-only`:** do NOT create a branch or edit anything. Run Steps 2–3
only, print the report, and stop.

**Otherwise**, create the working branch. The short base-SHA suffix makes the
name unique as `main` advances; the guard handles a same-week re-run on the
same base:

```bash
BRANCH="drift-sweep/${SWEEP_DATE}-$(git rev-parse --short origin/main)"
git show-ref --quiet "refs/heads/$BRANCH" && BRANCH="${BRANCH}-r2"   # re-run guard
git switch -c "$BRANCH" origin/main
```

---

## Step 2 — Scan (5 parallel sub-agents)

Dispatch all five **in one message** using whatever sub-agent tool the runtime
exposes (the `Task`/`Agent` tool) with a read-only `Explore`-type agent — it
must not edit. Each category gets its own bounded, fresh context. Each agent
returns a list of findings, one object per finding:

```
{ paths: [...], category, evidence, proposed_fix, risk: Low|Med|High, verifier }
```

`verifier` is a concrete command/check that **fails if the fix is wrong** — it
is what makes the fix safe to ship.

| Category | Detection | Verifier |
|---|---|---|
| **Stale docs** (incl. doc-sync over ALL of `docs/`) | For each doc→code mapping below, `rg` the symbols / paths / config keys a doc cites; flag any that no longer exist in code. Run across every `docs/` subdir. | cited symbol/path exists (`rg`), OR doc edited to match current code |
| **Duplicated config** | Cross-`rg` keys/values across `config/**` + `app_config` defaults; flag a key defined in ≥2 places with no single source of truth | value resolves once; `cargo build -p app_config` and config loads |
| **Unclear config** | Config keys with no inline comment AND not documented anywhere in `docs/` | each flagged key gains a comment or a doc line |
| **Missing tests** | Crates/modules with logic but no/empty `tests/`; design docs describing untested invariants (backtest fill models, OrderBook SeqLock race, data-ingestion WAL replay) | new test compiles + passes `cargo test -p <crate>` |
| **Messy scripts** | `scripts/*.sh` missing `set -euo pipefail`; scripts referenced nowhere (`rg <name>`); undocumented | `shellcheck` clean / script referenced / removed-with-zero-refs |

### Doc → code map (give this to the Stale-docs agent)

| Doc area | Maps to code |
|---|---|
| `docs/GENERAL_ARCHITECTURE.md` (threading, schema, protocols) | `trading-core/`, `data-ingestion/`, `ch-client` migrations |
| `docs/design/orderbook` | `services/crates/orderbook` |
| `docs/design/risk` | `services/crates/risk` |
| `docs/design/backtest` | `backtest-engine` |
| `docs/strategies/*` | `services/crates/strategies` (Avellaneda-Stoikov, GLFT, HMM regime) |
| config sections in any doc | `config/**` + `services/crates/app_config/src/config.rs` |

---

## Step 3 — Rank → Top 3

Score each finding on three 1–3 axes and rank by **impact × confidence ÷ risk**:

- **impact** — 1 low / 2 moderate / 3 high (blast radius if left unfixed)
- **confidence** — 1 possible / 2 likely / 3 verified drift
- **risk** — 1 docs-or-comment only / 2 config-or-test / 3 behaviour-affecting

Tie-breakers, in order: higher confidence, then lower risk, then path A→Z. Take
the top 3 and emit the report (the deliverable — print it even on
`--report-only`):

```
## Repo Drift Sweep — <SWEEP_DATE>

### Top 3 Cleanup Candidates
| # | Path(s) | Category | Risk | Verifier |
|---|---------|----------|------|----------|
| 1 | …       | …        | Low/Med/High | <command/check> |
| 2 | …       | …        | …    | … |
| 3 | …       | …        | …    | … |
```

**If `--report-only`: stop here.** No edits, no branch, no PR.

---

## Step 4 — Fix all 3

Apply the `proposed_fix` for each candidate on the branch. Keep each fix
surgical — touch only what the finding names (match surrounding style; don't
"improve" adjacent code).

---

## Step 5 — Verify & backfill to three

Run each candidate's `verifier`. A fix ships **only if its verifier passes**.

If a candidate's verifier can't pass, **revert that candidate and pull in the
next-ranked finding** from Step 3 — fix it (Step 4) and verify — repeating until
**three verified fixes** are staged. If the ranked findings run out before three
pass, **stop without opening a PR**: print the report and what blocked each
attempt. The PR ships exactly three verified fixes — never a partial set, never
an unverified change.

---

## Step 6 — Review (separate context)

Invoke the **`code-review`** skill on the branch diff:

```bash
HEAD_SHA=$(git rev-parse HEAD)   # BASE_SHA from Step 1
```

Its 5 lenses run as fresh sub-agents — isolated from the context that wrote the
fixes (this is the "different sub-agent" requirement). Fix all **Critical** and
**Important** issues before continuing; re-run the affected verifiers.

---

## Step 7 — PR

Commit, then invoke the **`new-pr`** skill.

- **Title:** `chore: weekly repo-drift sweep <SWEEP_DATE>`
- **Body** must embed:
  - the Top-3 report table,
  - each candidate's verifier result (all three must be **pass**),
  - the `code-review` confidence table.

---

## Scheduling (ensure once, then verify)

This skill is meant to run weekly. Ensure a `/schedule` cloud routine exists
whose prompt is `repo-drift-sweep`, and verify its next run — idempotent, so
re-running this section never creates a duplicate:

1. List routines. Find one whose prompt targets this skill.
2. **If present:** confirm cron `0 2 * * 1` (Mon 09:00 Asia/Saigon = 02:00 UTC)
   and that `next_run_at` is the upcoming Monday; update if either has drifted.
3. **If absent:** create it — cron `0 2 * * 1`, repo default branch, prompt
   `repo-drift-sweep`.
4. Report the resulting `next_run_at` so the schedule is verifiable.

The sweep itself uses only git, `gh`, file tools, `cargo`, `shellcheck`, and
sub-agents — no interactively-authenticated MCP server — so it works in
headless/cron runs. Inspect the opened PR before merging; this skill never
merges.
