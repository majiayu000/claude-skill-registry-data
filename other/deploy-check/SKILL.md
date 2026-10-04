---
name: deploy-check
description: Deployment-readiness verdict for a diff range — green (merge is the whole deploy), yellow (order matters; sequenced runbook), or red (not safe to land as-is; restructure, usually expand/contract). Use before merging or deploying when a change touches migrations, env vars, crons/workers, queues, caches, or API contracts — or when the user asks how to deploy safely, whether a migration runs before or after merge, or what to watch after a deploy. Invoked by `land-pr` before gate 2 when its impact scan flags anything.
---

# Deploy check

Reads a diff range, checks it against the repo's deployment facts, and returns a **verdict**: green, yellow, or red. The runbook is the payload when it's yellow; the veto is the payload when it's red. This skill never merges, migrates, or deploys — it plans and warns.

**Input**: a diff range, defaulting to `<base>...HEAD` (same base detection as `land-pr`). Callers — land-pr, a hotfix, a standalone "how do I deploy this?" — may pass another range.

**Anti-goal**: ceremony in the green case. When nothing deployment-sensitive is in the diff, the entire output is one line — "deploy-check: green — merge is the whole deploy story" — and you're out.

## The organizing question

Everything hangs off one compatibility question: **during the rollout window, will old code run correctly against the new schema, and new code against the old schema?** Migration ordering, env-var timing, worker pausing, and expand/contract all fall out of it. Answer it first; the verdict follows.

## Facts file: `DEPLOYMENT.md`

Deployment mechanics are per-repo; read them from a source of truth, never infer them run to run.

- **First run in a repo** (no `DEPLOYMENT.md` at the repo root): interview the user once — what triggers deploys (auto on merge to main?), migration command and where it runs, where env vars are set, what crons/workers/queues exist, rollback method, and any tables where locking or duration matters (scale). Write the answers to `DEPLOYMENT.md` with a `## Gotchas` section (empty is fine) and a `Verified: <date>` stamp.
- **Later runs**: read it instead of asking. **Distrust it cheaply first**: does the migration command still exist in `package.json` (or equivalent)? Do the listed crons/workers still appear in the repo? A fact that fails verification gets re-asked and rewritten — a runbook built on a stale premise is worse than a question.
- **After a yellow/red deploy that surfaced something** ("the ALTER on `enquiries` locked 40s", "worker needs manual restart after env change"), append it to `## Gotchas`. Later runbooks cite matching gotchas inline.

A repo's own deploy docs (AGENTS.md pointers, runbooks) outrank this file — read them first and let `DEPLOYMENT.md` cache only what they don't cover.

## Workflow

### Step 1: Scan the range

Read the diff for deployment-sensitive signals:

- Migrations — and whether each is additive (new column/table/index) or destructive/renaming (drop, rename, type change, NOT NULL on an existing column). Backfills hiding inside migrations count as migrations *and* as long-running operations.
- New env-var reads not present in `.env.example` / deploy config.
- Cron, worker, queue, or job changes — especially payload shape changes (old workers picking up new payloads is the classic).
- Cache key or serialization format changes.
- API contract changes consumed by things that don't deploy atomically (mobile apps, webhooks, other services).

**Done when** every file in the range is accounted for as either inert or classified under a signal. No signals → **green**, one line, stop.

### Step 2: Answer the compatibility question

For each signal, decide: is there any ordering of (env vars, migration, merge/deploy, worker restart) under which old and new code both run correctly during the window?

- Yes, and order matters → **yellow**.
- Yes, and order doesn't matter → still **green** (say why in one extra line).
- No — e.g. a rename or drop combined with auto-deploy-on-merge → **red**. Do not produce a "safe" runbook for an unsafe change. Recommend the restructuring instead — usually an expand/contract split into two PRs — and, when invoked from `land-pr`, feed the verdict back into its Step 2: this is a landing-strategy change, not a footnote.

Scale is a red trigger too: an operation that's safe on a small table but locks one listed in `DEPLOYMENT.md`'s scale answers goes red (or yellow with an explicit off-peak / online-migration step), citing the fact.

### Step 3: Runbook — yellow only

An ordered, concrete sequence using the facts file's actual commands — "run `pnpm db:migrate` on the prod box", not "run your migrations". Typical spine: set env vars → pause affected crons/workers → run additive migration → merge (deploy) → resume/restart workers → cleanup. Env vars always precede the code that reads them (missing env var = crash loop). Cite matching gotchas beside the step they bear on.

**End with a verify tail** — a runbook without one is a takeoff checklist with no landing:

- What confirms health: health endpoint, Sentry quiet for N minutes, the cron actually fired on schedule, migration row counts.
- Rollback: "to revert, X — migration Y is/isn't reversible."

**Done when** every signal from Step 1 appears in the sequence or is explicitly called inert, and the tail names both a health check and a rollback.

### Step 4: Report

Lead with the verdict line, then the runbook (yellow) or the restructuring recommendation (red). Offer to append any newly surfaced gotcha to `DEPLOYMENT.md` once the deploy has actually run.
