---
name: ai-council-review
description: >-
  Convene a council of ~4 frontier models via the OpenRouter API for
  independent parallel reviews of a PR, plan doc, or files, then synthesize
  agreements and dissents in-session. Use for high-stakes or contested
  changes, before irreversible decisions, or when one extra model's opinion
  is not enough — costs real money per run. Triggers on /ai-council-review,
  "council review", "panel review", "multi-model review", "review with
  multiple models", "ask several models", "get a third opinion",
  "high-stakes review", "openrouter review". For a quick single-model
  second opinion, use ai-review instead.
globs: []
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: "0.4.0"
compatibility: Claude Code, Cursor
---

# AI Council Review

Several frontier models review the same material in parallel — blind to each
other — via one API (OpenRouter). A dispatch script handles fan-out, cost
gating, and clustering; **you** synthesize, because you can do the one thing
the council cannot: verify findings against the actual repository.

This is the heavyweight sibling of `ai-review` (single model, ~$0.03). A
council run costs real money — from well under a cent (`budget`) to over $1
(`flagship`, which trips the confirmation gate on anything beyond a small
diff). See the per-preset tables in README.md for exact pricing. Use it for
high-stakes decisions, not routine diffs.

## Data leaves the machine — confirm before first dispatch

Everything submitted (diffs, plan docs, file contents) is sent to the
OpenRouter API and forwarded to **multiple third-party model providers**
(different companies, different data-retention policies). For private or
proprietary code this means unreleased source leaves the machine.

- Before the FIRST council run in a session, confirm with your human partner
  that sending this content to external providers is acceptable — especially
  in private repos or anything under NDA. Consent given for this repo earlier
  in this session carries over; do not re-ask per run.
- Reduce exposure: review the diff, not the whole tree; never include `.env`
  files, credentials, or customer data in the input.
- Account-wide tightening: OpenRouter privacy settings (disable logging,
  restrict to ZDR-eligible providers).

## Prerequisites

- Node.js >= 20 (`node --version`)
- `AI_COUNCIL_OPENROUTER_API_KEY` exported — the council's own variable, so
  it can hold a dedicated, budget-capped key rather than whatever generic key
  a shell happens to export (get one: <https://openrouter.ai/keys>).
  `OPENROUTER_API_KEY` still works as a fallback, and a run that falls back
  says so on stderr. The script reads the key from the environment only and
  never prints it. If neither is set, dispatch exits with code 4 — ask your
  human partner; do NOT hunt for keys in keychains, dotfiles, or session
  archives.

## CRITICAL rules

- **Never fabricate or substitute a council opinion.** If members fail or
  quorum is not met, report that and offer the `ai-review` fallback — do not
  write "what the model would probably say", and do not pass your own review
  off as a member's.
- **Never pass `--yes` on your own.** `--yes` asserts that your human partner
  saw the printed cost estimate and approved it *in this session*. Budget
  gate refusals (exit 3) are a stop, not an obstacle to route around.
- **Never skip the synthesis protocol.** Raw per-model output is not the
  deliverable; the verified, dissent-preserving report is.

## Workflow

Script: `${CLAUDE_SKILL_DIR}/scripts/council.mjs` (always via this absolute
path — never a relative `./scripts/...`).

### 1. Classify

| Input | Flags | Rubric |
|---|---|---|
| GitHub PR | `--pr <N>` | `--rubric code` |
| Unstaged / staged / branch diff | *(default)* / `--staged` / `--branch [base]` | `--rubric code` |
| Plan or design doc | `<file>` or `--plan <file>` | `--rubric plan` |
| Any other document/files | `<file...>` or `--input-file <f>` | `--rubric doc` |

Preset: the default preset is already the code-review roster (`--rubric
code` needs no flag). For `plan`/`doc` rubrics, use `--preset prose` — the
prior default roster, better suited to prose than the codex-tuned default.
`--models a,b,c` overrides for custom councils.

`--personas` runs the council in **coverage mode**: each member gets a
distinct focus lens (correctness, security, design, testing, operations)
on top of the shared rubric. This trades consensus signal for breadth —
agreement counting is invalid across different assignments, and the
synthesis protocol switches to coverage mode. Prefer it for broad material
(a large plan, a many-concern diff); prefer the identical-rubric default
when the question is "is this correct?" and agreement should mean
something.

### 2. Estimate (spend-free)

```bash
node ${CLAUDE_SKILL_DIR}/scripts/council.mjs review <flags> --dry-run
```

Show the user the per-model table and total. If the estimate exceeds the
confirmation threshold (default $1), you MUST get an explicit go-ahead in
this session before step 3.

### 3. Dispatch (1–10 minutes — run in background)

```bash
node ${CLAUDE_SKILL_DIR}/scripts/council.mjs review <same flags> [--yes]
```

The script fans out in parallel, retries once on 429/5xx, aborts hung
members at the timeout, persists everything, and prints `RUN_DIR=<path>` as
its last line.

| Exit | Meaning | Your move |
|---|---|---|
| 0 | Quorum met (check `degraded` in manifest) | Synthesize (step 4) |
| 1 | Usage/input error (bad slug, empty diff, oversized payload) | Fix per the message; slug errors include suggestions — update roster, retry |
| 2 | Quorum failed | Report which members failed and why; offer `ai-review` fallback; do NOT synthesize or self-substitute |
| 3 | Budget gate blocked (nothing sent) | Relay the estimate to your human partner; only proceed how they decide |
| 4 | API key missing/rejected | Ask your human partner to set `AI_COUNCIL_OPENROUTER_API_KEY` (or `OPENROUTER_API_KEY`) |

### 4. Synthesize

Follow `${CLAUDE_SKILL_DIR}/references/synthesis.md` step by step. Core
moves: members are **anonymized** (`member-A`…) — do not open
`roster-key.json` until the report step; agreement is counted over
delivered members; parse-failed members' raw text is read and included; top
findings are **verified against the actual repo** before being reported;
dissent is preserved as contested items and minority reports; ranking is
`verified > severity > agreement > confidence`.

### 5. Report

Write `report.md` into the run dir per
`${CLAUDE_SKILL_DIR}/references/report-template.md`; give the user the
condensed version in chat with actual vs estimated cost. Then record the
verification outcomes (`outcomes record`, synthesis protocol step 8) — the
archive is what makes future rosters evidence-based.

### 6. Optional: post to the PR

Only on explicit user request, post findings with `gh pr comment` (or a
formal review via `gh api`). The script never posts anywhere.

## Cost pattern: two-stage triage (optional)

A suggestion for material that may not need a frontier council — nothing
enforces it:

1. Run `--preset budget` (3 cheaper members) first, or `--preset crowd` (6
   members) for broader coverage at still-modest cost.
2. Escalate to `default`/`max` **only if** the budget/crowd run produced
   majors/blockers or contested clusters — objective properties of
   `clusters.json`, not a feeling.
3. A clean budget/crowd run (approvals + nits) is a result: report it and
   stop.

Each stage passes the same estimate and consent gates; escalation is a
second run with its own estimate. Prior art: cascade cost controls
(cheap-first with objective escalation triggers).

## Re-reviewing after fixes

Each cluster in `clusters.json` has a `fingerprint` stable across runs
(built from files + title tokens, not member labels or line numbers). When
a council run follows an earlier run of the same material:

1. Compare fingerprints against the previous run's `clusters.json`; classify
   clusters as **new / persisting / resolved**. Fingerprints are a hint —
   confirm matches semantically before reporting them.
2. **Stuck rule**: if the same blocking findings (by fingerprint) survive
   two consecutive runs, do not propose a third run — the council has said
   what it has to say. Recommend human judgment on the persisting blockers
   instead. (Cost/termination gate from prior art; see README provenance.)

## Configuration

Precedence: flags > `AI_COUNCIL_*` env > repo `.ai-council.json` >
`~/.config/ai-council-review/config.json` > bundled
`references/presets.json` (presets: `default`, `code`, `prose`, `budget`,
`crowd`, `max`, `flagship`, `smoke` — see README.md for per-preset rosters
and pricing; scalars: `budgetUsd`, `confirmThresholdUsd`, `timeoutMs`,
`quorum`, `preset`, `reasoningEffort`, `providerSort`).

`reasoningEffort` (`--reasoning-effort` / `AI_COUNCIL_REASONING_EFFORT`,
bundled default `"medium"`) sets `reasoning.effort` on every request — but
only to models that advertise `"reasoning"` in the live catalog's
`supported_parameters`; sending it to a model that doesn't support it is a
400, not a graceful ignore, so dispatch gates it per-member. Set to `"none"`
to disable reasoning outright, or `"low"` for the cheapest/fastest council
presets. `providerSort` (`--provider-sort` / `AI_COUNCIL_PROVIDER_SORT`,
bundled default `"throughput"`) sets `provider.sort` — a routing hint, not a
model capability, so it's sent to every member unconditionally.

Useful env: `OPENROUTER_BASE_URL` (testing), `COUNCIL_TIMEOUT_MS`,
`REVIEW_BASE_BRANCH` (for `--branch`).

Run artifacts live under `~/.local/state/ai-council-review/<repo>/<run-id>/`
(override: `--out`). They contain the reviewed source — treat as sensitive;
never commit them.

## Inspecting the roster

```bash
node ${CLAUDE_SKILL_DIR}/scripts/council.mjs models                 # current council + live pricing
node ${CLAUDE_SKILL_DIR}/scripts/council.mjs models --verify a,b    # diagnose slugs
```

Model slugs churn. When dispatch exits 1 with "Unknown model slug", the fix
is a roster update (config override or a patch to `references/presets.json`)
— pick the suggested replacement closest in capability.
