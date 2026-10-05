---
name: prod-ux-review
description: Review a production UX checkout harness run against the deployed Studio (daikonic). Use after `pnpm --filter @rune-langium/studio run test:prod-ux` (or test:prod-smoke) completes, when the user asks to review/triage a prod checkout run, or when a nightly prod-ux artifact needs auditing. Consumes report/run-manifest.json + screenshots + traces and produces a severity-ranked UX review with per-journey verdicts.
---

# Production UX Checkout Review

You are auditing a run of the production UX checkout harness
(spec: `docs/superpowers/specs/2026-07-16-prod-ux-checkout-harness.md`) against
the deployed Studio. Your deliverable is a **review report**, not fixes — do
not modify code unless the user asks afterward.

## Inputs

Locate the evidence bundle (default `apps/studio/test/prod-ux/report/`, or the
path the user gives you):

1. `run-manifest.json` — per-journey verdicts, checkpoints, console/network
   noise, per-operation timings (with budgets), `typeClosure` records,
   embedded `opLog` streams, soft findings. **This is your index; read it
   first.**
2. `screenshots/<journey>/…png` — read them; do not review blind.
3. Playwright HTML/JSON report + traces (`trace.zip` on retried tests).
4. `axe/J17/attempt<N>/` raw checkpoint results when J17 ran. Read endpoint
   verification output separately. The harness records soft findings in the
   manifest; it does not maintain a `known-issues.json` ledger.

If the manifest is missing, fall back to the Playwright report alone and say so
prominently — the run predates or bypassed the evidence collector.

## Review procedure

Work journey-by-journey in manifest order. For each journey produce a verdict
you *verified*, which may disagree with the harness's own verdict — say so when
it does.

### 1. Gate on freshness first (J0)

If the live commit ≠ master, or `verify-production.sh` has FAILs, every later
finding may just be staleness. Classify the whole run as **STALE-DEPLOY** and
review the rest only as "behavior of the stale deploy," clearly labeled.
Cloudflare Pages never rolls back on failed builds — check whether the *latest*
deploy attempt failed, leaving prod silently stuck.

### 2. Triage failures — classify before judging

For every FAIL/DEGRADED/BLOCKED journey, assign exactly one class:

- **regression** — feature broke in prod. Evidence: assertion + screenshot +
  console/network record agree. Highest severity.
- **corpus-drift** — an anchor type/namespace moved in a curated rebuild. The
  harness itself only reports a bare `FAIL` for an anchor-existence failure —
  it does not classify corpus-drift automatically. You (the reviewer) assign
  `BLOCKED(corpus-drift)` by verifying the anchor against the live curated
  manifest. Fix is an `anchors.ts` update, not app code.
- **known-issue** — the manifest's soft finding names an understood, still
  applicable limitation. Verify its current behavior and any linked GitHub
  issue; do not infer an expiry date or issue URL from the finding ID alone.
- **flake/infra** — passed on retry, or failure is a timeout with no
  corroborating console/network evidence. Check the trace before concluding
  flake; two consecutive runs flaking the same step is a regression until
  proven otherwise. A journey record's `retry` (>0) plus its `previousAttempts`
  array (the superseded earlier attempt(s), each with its own verdict/evidence)
  is exactly the manifest evidence for "passed on retry, not cleanly" — check
  both before defaulting a PASS to clean.
- **harness-bug** — selector rot, race in the spec itself (e.g. asserting
  before a hydration wait). The trace's action log usually shows this.

For any Worker-backed failure (`/api/parse`, `/api/codegen`, curated
endpoints): **pull Cloudflare function logs first** before hypothesizing —
never diagnose Worker behavior from the browser side alone.

### 3. UX audit of screenshots (including PASSING journeys)

Assertions prove function; screenshots prove *experience*. For every
checkpoint image check:

- layout integrity — no clipped/overflowing panels, no dockview panes collapsed
  to zero, no overlapping chrome; the single-topbar contract holds (exactly one
  AppHeader, correct per-perspective title/actions);
- theme consistency — check the theme actually available in the run; look for unstyled flashes,
  hairline borders missing outside studio scope, tokens rendering as raw
  fallbacks;
- state correctness — empty states only where content is genuinely absent
  (an empty Inspector on a hydrated namespace is a regression even if no
  assertion fired); spinners present during load checkpoints and absent after;
- text quality — truncation, missing i18n keys, `undefined`/`[object Object]`
  leaking into UI;
- graph readability — Structure view nodes laid out (not stacked at origin),
  edges attached.

Report anything a user would notice, even under a PASS verdict.

### 4. Noise & performance trends

- Console errors/warnings and failed first-party requests on *passing*
  journeys are findings (severity by content: CSP violations, React warnings,
  unhandled rejections rank above noisy 3rd-party).
- **Timings:** walk the manifest's per-operation timing table
  (`startPageInteractive`, `workspaceOpen`, `modelLoad`, per-namespace
  `hydration`, `formRender`, `functionExecute`, per-target `codegen`,
  per-format `importPreview`/`importMerge`, `reloadRestore`). Flag every entry
  over its `budgetMs`; compare against the previous run's manifest when
  available and call out >25% regressions even under budget. J18's
  `typeClosureWalkMs` is recorded per-root inside each `typeClosure` entry
  rather than this opLog-sourced table and carries no `budgetMs` — compare it
  across runs the same way, but don't expect a budget flag on it. When an
  entry is opLog-sourced, use the journey's `opLog` and the correlated
  Worker-side log line (`x-studio-op-id`) to attribute slowness to
  client vs Worker before speculating.
- **Type-closure mapping (J18):** each `typeClosure` array entry is a
  `TypeClosureRecord` (`rootFqn`, `rootKind: 'curated' | 'scratch'`,
  `visitedCount`, `mappedCount`, `unmapped: string[]`, `hydrationsTriggered`,
  `truncated`, `typeClosureWalkMs`) — one per root, two entries total. The
  harness itself only hard-fails on a non-empty `unmapped` for the
  **scratch** root (an unambiguous regression: mapping/hydration/form
  pipeline); a non-empty `unmapped` on the **curated** root is recorded as a
  soft finding (`typeClosure-curated-unmapped`), never a hard failure — first
  check the fqn against the live curated manifest — present there ⇒
  regression; absent ⇒ corpus-drift (anchors/closure update). Also check
  `visitedCount` didn't collapse (a closure that visited 3 types when the
  previous run visited 80 means the walk silently stopped — a harness or
  hydration bug, not a pass) and whether `truncated` is `true` (hit the
  150-node cap; also surfaced as a `typeClosure-truncated` soft finding).
  `typeClosureWalkMs` is recorded per-root inside the record itself, not as a
  separate opLog-sourced timing-table entry.
- **opLog streams:** scan embedded `opLog` entries for `warn`/`error` levels on
  passing journeys; verify the Activity/Output panel screenshots actually show
  the operation stream (an empty Activity panel after a CDM load means the
  logging pipeline itself regressed). Enforce the **superset-of-toasts
  invariant**: any toast visible in a checkpoint screenshot (or recorded by the
  harness) must have a matching opLog entry — a toast without one means the
  toast→log mirror in `StudioToastProvider` regressed, which silently
  un-audits every future notification; rank that as a regression even though
  no user-visible feature broke.
- Axe: `critical` should already have failed the run; enumerate `serious` with
  the offending selector and screenshot.

### 5. Reconcile soft findings

List manifest soft findings that still reproduce, those that no longer reproduce,
and recurring limitations missing from the current manifest. Check linked GitHub
issues when available; do not infer enrollment or expiry dates from finding IDs.

## Output format

Produce one report (markdown; save alongside the bundle as `REVIEW.md` and
present it in your reply):

```markdown
# Prod UX Checkout Review — <runId>
**Deploy:** <liveCommit> (current with master: yes/no) · **Run verdict:** GREEN | DEGRADED | RED | STALE-DEPLOY
**Journeys:** N pass / N degraded / N fail / N blocked

## Findings (severity-ranked)
### F1 — [regression] <one-line defect statement>
- Journey/checkpoint, evidence (screenshot path, trace, console line, CF log line)
- User impact · Suggested owner-fix direction (1–2 sentences, no patches)

## Journey table
| J | Title | Harness verdict | Reviewed verdict | Class | Notes |

## UX observations (non-blocking)
## Timings vs budget
## Soft-finding reconciliation
## Suggested follow-ups (ordered; which findings warrant GitHub issues)
```

Severity order: regression in a core loop (load/edit/persist/export) >
regression elsewhere > unresolved known issue > a11y serious > UX observation >
noise. Rank findings most-severe-first; when drafting issues, group findings
sharing one root cause into one issue — fix patterns, not symptoms.

## Telemetry mode (real-user behavior review)

When given a **fleet rollup / session digests** (from
`pnpm --filter @rune-langium/studio run telemetry:digest`, i.e. the telemetry
worker's `GET /v1/digest`) instead of — or alongside — a harness bundle:

- Skip the screenshot/assertion steps (there are none); the digest uses the
  same op vocabulary and budgets as the run manifest. Reconcile signatures
  with prior rollups and manifest soft findings when those are available.
- Triage **signatures, not events**: for each error/warn signature, classify
  with the same 5-class taxonomy, prioritized by affected-session count and
  the `new-in-this-deploy` flag (a low-volume signature that appeared with
  the current deploy outranks a high-volume signature seen in prior rollups).
- Timing review runs on the per-op p50/p95-vs-budget table; flag ops whose
  p95 crossed budget or whose violation rate rose vs the prior rollup.
- Drill down via the sampled sessionIds/opIds on a signature → correlated CF
  Worker log lines (`x-studio-op-id`) before hypothesizing about cause.
- When both a harness manifest and a rollup are available (nightly combined
  review), cross-reference them: a harness FAIL matching a fleet signature is
  confirmed user impact (raise severity); a fleet signature with no harness
  coverage is a **harness gap finding** — name the missing journey.

## Rules

- Every claim must cite evidence you actually opened (screenshot, trace,
  manifest field, CF log). No verdict from the harness is trusted unverified.
- Do not re-run the harness or "fix" prod-side anything during review; the
  review is read-only. Proposing an `anchors.ts` update or a follow-up issue is
  output, not an edit you make.
- Do not reply to bot/PR comments as part of this workflow.
- If the bundle is partial (missing screenshots for a journey, no traces),
  degrade gracefully and list the gaps in the report header — an evidence gap
  in a FAIL journey makes it **unverifiable**, not green.
