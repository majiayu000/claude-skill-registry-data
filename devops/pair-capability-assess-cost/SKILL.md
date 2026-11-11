---
name: pair-capability-assess-cost
description: "Assesses the financial exposure of a change as a chromatic cost class (green/yellow/orange/red) against the KB cost-signal catalog resolved through the project's stack/architecture/infrastructure adoption, in two modes — review/refinement classification and period cost-monitoring reports: `$mode: classify` — the review/refinement-time class, output-only, emitted as the cost dimension of the classification matrix (1-line verdict + collapsed details, D22) for /pair-capability-classify and /pair-process-review to consume; `$mode: report` — bidirectional cost monitoring over a period's merged PRs (predicted class vs. real signals, drift flagged, deploy-match when telemetry exists), rendered as a consolidated panel written to .pair/working/reports/cost/, idempotent by period key. Multi-provider by construction: adding a provider touches adoption/KB only, never this skill."
version: 0.3.0
author: Foomakers
---

# /pair-capability-assess-cost — Cost Assessment

Assess the financial exposure of a change in two modes, both resolved from the same rule set — the [quality model](../../../.pair/knowledge/guidelines/quality-assurance/quality-model.md) (§2 Cost pillar, §3.3 Cost class) plus the [cost-assessment guideline](../../../.pair/knowledge/guidelines/quality-assurance/cost-assessment.md), the single home of the cost-signal catalog, the general + provider-specific heuristics (AWS first), and the cost gotchas:

- **`classify`** (default) — the chromatic **cost class** (`green` / `yellow` / `orange` / `red`) of the cost signals present in the diff (or, at refinement, the story scope). Output-only.
- **`report`** — **bidirectional cost monitoring** over a period: each _merged_ PR's refinement-time _predicted_ class against its _real_/observed cost signals, drift flagged, rendered as a consolidated panel in the reports working area.

**Classification mode writes no files.** It emits the cost dimension of the classification matrix and nothing else: it **creates no backlog items and never blocks** a PR or merge (it has no such authority — the merge decision stays with `/pair-process-review`, exactly as the `assess-security` sibling reports a verdict but never blocks). The cost class it computes is consumed by `/pair-capability-classify` and `/pair-process-review`; the skill never interprets or acts on its own verdict. Report mode is the skill's only writer, and it writes exactly one file: the period panel (Step 11) — no adoption content, no issues, ever.

**Provider-agnostic core (R2.13).** No provider names are hardcoded in this skill. Which heuristics apply is selected by the project's `tech-stack.md` / `architecture.md` / `infrastructure.md` adoption files (Q3); the catalog and per-provider heuristics live in the guideline (D17/D21). Adding a provider is an adoption/KB change (a new per-provider section or an adoption link), never a change to this skill.

## Arguments

| Argument  | Required | Description                                                                                                                              |
| --------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `$mode`   | No       | `classify` (**the default**) — class of one diff/story (output-only). `report` — period cost monitoring panel. `report` runs **only when explicitly asked for** (`$mode: report`) or when a reporting window is given; every other invocation classifies, a bare one included. |
| `$diff`   | No       | Classification mode. The PR/branch diff to classify. Default when invoked by `/pair-process-review` or against a branch: the current diff.            |
| `$story`  | No       | Classification mode. A story/issue to classify from its declared scope instead of a diff — the refinement-time (shift-left) path, mirroring the risk matrix built twice. |
| `$scope`  | No       | Classification mode. Area/package to scope the scan (default: the whole diff/story). Package-scoped only — never narrows the rule set, only the surface scanned. |
| `$period` | No       | Report mode. The monitored window as a period key — `YYYY-MM`, `YYYY-Wnn`, or `YYYY-MM-DD_YYYY-MM-DD` (default: the current calendar month). An explicit `$period` implies `report`. |
| `$output` | No       | Report mode. Directory the panel is written to. Default: `.pair/working/reports/cost/` (D14 — report path override). **Not a mode signal**: supplied without `$mode: report`/`$period` it is _ignored_, and the run says so (Step 1.4) rather than dropping it silently. |

`$diff` and `$story` are mutually exclusive inputs; exactly one surface is classified per `classify` run. Neither provided → auto-detect: a PR/diff in context (i.e. invoked by `/pair-process-review`) → `$diff`; a story in context (i.e. invoked by `/pair-process-refine-story`/`/pair-capability-classify` in refinement) → `$story`.

## Rule Set

Every rule resolves through the standard **Argument > Adoption > KB default** cascade of the quality model (§quality-model.md resolution order):

1. **KB default** — [quality-model.md](../../../.pair/knowledge/guidelines/quality-assurance/quality-model.md) §3.3 (class = highest detected signal; class token `cost:green|yellow|orange|red`) + the [cost-assessment guideline](../../../.pair/knowledge/guidelines/quality-assurance/cost-assessment.md) (the signal catalog, the general heuristics, the per-provider heuristics starting with AWS, the gotchas).
2. **Provider selection (adoption)** — read `tech-stack.md`, `architecture.md`, `infrastructure.md`: the declared cloud/provider (e.g. AWS) selects which per-provider heuristics in the guideline apply. A provider the guideline does not cover in-tree is reached via an **adoption link** the adoption file supplies (fallback/extension — no skill change, Q3).
3. **Project delta (adoption)** — `tech/risk-matrix.md` `## Overrides` may tune cost thresholds (e.g. reclassify a shared path); absent ⇒ KB defaults apply completely (D21).

A missing/malformed adoption file is treated as absent: warn and fall back to KB defaults (D21) — never HALT on adoption absence.

## Algorithm

### Step 0: Load the Quality Model (BLOCKING prerequisite)

1. **Check**: Does [quality-model.md](../../../.pair/knowledge/guidelines/quality-assurance/quality-model.md) resolve (KB installed)?
2. **Act**: If it is **missing**, **HALT** — the quality model is a prerequisite, not a default this skill can invent. Report: _"Quality model not found — install/bootstrap the KB (`quality-model.md` §3.3) before running assess-cost."_
3. **Verify**: The Cost class section (§3.3) and the [cost-assessment guideline](../../../.pair/knowledge/guidelines/quality-assurance/cost-assessment.md) are loaded.

### Scoped Context (package-local override)

Opt-in. When the central adoption file carries a `## Package-Local Adoption` router, resolve the rule set per [scoped context resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/scoped-context-resolution.md) (diff-scoped here: globals + `<pkg>/.pair/` of the packages the diff touches, nothing else); report a central↔local conflict, a dangling router entry, and — when the [complexity signals](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/package-local-adoption.md#activation-proposal) fire — PROPOSE the override and wait for approval, never activate. No router ⇒ unchanged behaviour.

### Step 1: Detect Mode

1. **Check**: Is `$mode` provided?
2. **Skip**: If provided, use it. Proceed to Step 2.
3. **Act**: Not provided → `report` **only when a `$period` is given**; **otherwise `classify`**, the default. A bare invocation with no surface named (`/pair-capability-assess-cost` on the current branch) is a `classify` run against that branch's diff — the absence of `$diff`/`$story` is _never_ by itself a reason to enter `report`, which is the only file-writing mode and never runs implicitly.
4. **Act**: **`$output` is not a mode signal.** `$output` is report-mode-only, but supplying it does _not_ select `report` (that would let the only file-writing mode start from a path argument). In a `classify` run an explicit `$output` is ignored **with a warning** naming it — _"`$output` ignored — classification mode writes no files; pass `$mode: report` (or a `$period`) to produce a panel"_ — never dropped in silence.
5. **Act**: **The ignore-with-warning rule is symmetric.** It binds in **both** directions, so no argument is ever dropped in silence: a report-only argument (`$output`) supplied to `classify` warns as above, and a classify-only argument (`$diff`, `$story`, `$scope`) supplied to `report` warns the same way, naming it — _"`$scope` ignored — report mode aggregates the whole period from merged PRs, it does not scope by path; drop it, or run `$mode: classify` to assess that scope"_. Silence here is the harmful case: `$mode: report $period: 2026-07 $scope: apps/website` would otherwise render a whole-repo panel while the caller believes it is scoped, and nothing in the artifact contradicts them.
6. **Verify**: Mode is set — exactly one mode runs per invocation, `report` was either asked for by name or implied by an explicit `$period`, and **every** argument the selected mode does not use was reported as ignored, whichever direction the mismatch runs in.

### Step 2: Resolve the Rule Set

1. **Act**: Read the KB default (§3.3 + cost-assessment guideline), then the adoption files (Rule Set layers 2–3), skipping any that don't exist.
2. **Act**: Select the applicable per-provider heuristics from the declared stack/infrastructure (e.g. AWS); for a provider only reachable via an adoption link, resolve that link.
3. **Verify**: Effective catalog + heuristics assembled. Adoption absence is logged as "KB defaults only", not an error.
4. **Act**: Route by mode — `classify` → Step 3; `report` → Step 7.

## Classification Mode (one diff or story)

### Step 3: Resolve the Surface

1. **Act**: Determine the surface: `$diff` (touched files/hunks) or `$story` (declared scope — infra/service load the story introduces), narrowed by `$scope` if given.
2. **Verify**: A concrete surface (file set or story scope) is resolved.

### Step 4: Scan for Cost Signals

1. **Act**: Scan the surface against the cost-signal catalog (maintained in the [cost-assessment guideline](../../../.pair/knowledge/guidelines/quality-assurance/cost-assessment.md)) — e.g. paid-SDK imports (payment/LLM/messaging providers), API-key env vars, IaC/provisioning changes, cron/scheduled jobs, queues/pipelines, media processing, LLM calls. For each hit, record the signal, its location, and the class it maps to per the guideline's heuristics (general + the selected provider's).
2. **Act**: **Unresolvable cost surface** (unknown tech whose cost profile the catalog + adoption cannot resolve): record it as an **unknown-surface** hit and assign it **orange** — the conservative, visible middle-high, never silently green (edge case: "unknown surface" flag).
3. **Verify**: Every touched cost-relevant surface has a signal, a location, and a mapped class; unknown surfaces are flagged, not dropped.

### Step 5: Compute the Class

1. **Act**: **Cost class = the highest detected signal** across all hits (§3.3). **No signal detected ⇒ `green`** with rationale _"no cost surface touched"_.
2. **Act**: In refinement (`$story`) the class is the shift-left, declared value; in review (`$diff`) it is the observed value — carried in the same compiled matrix as its own class (never folded into the risk `max`, §3.2), tag token `cost:green|yellow|orange|red`.
3. **Verify**: Exactly one class computed, with a 1-line rationale and the detected-signals list.

### Step 6: Emit the Verdict

1. **Act**: Render the 1-line class + rationale and the collapsed `<details>` signals table per Output Format below — **output-only, no files written**. This is embedded by the caller into the classification matrix's cost dimension (D22 — verdict in ~1 line, details in `<details>`), consumed by `/pair-capability-classify` and shown by `/pair-process-review`.
2. **Verify**: Verdict emitted. A `red` (or flagged unknown-surface) class is reported for the caller's attention; the skill itself blocks nothing — the merge decision stays `/pair-process-review`'s.

## Report Mode (period cost monitoring)

Report mode covers the quality model's cost-monitoring requirements **R6.3** (predicted vs. real cost per change) and **R6.4** (drift in cost prediction surfaced periodically, not per-PR) — named in the [quality model](../../../.pair/knowledge/guidelines/quality-assurance/quality-model.md) §3.3 ("Cost monitoring (R6.3/R6.4) → `assess-cost` report mode"), which points here for their application.

It **aggregates and compares**; the classification criteria are **not redefined** here. Each PR's real class comes from re-running the classification path (Steps 3–5 — surface, scan, compute; emission is report mode's own, Step 11) over that PR's merged diff, and each PR's predicted class is read from what **refinement** already recorded (Step 8.2.1's precedence rule) — the catalog/heuristics stay in the guideline (D17/D21), so monitoring can never drift from classification.

The panel's path, period key, in-place idempotency, headline-first shape, empty-period and not-writable behavior all follow the one **report-panel convention** in [working-area.md](../../../.pair/knowledge/guidelines/collaboration/working-area.md) ("Report Panels — Period Key and Idempotent Update") — shared with the delivery/AI-metrics panels, one reports-area pattern for the whole KB. That guideline is **authoritative**: Steps 7 and 11 below _summarize_ only the mechanics they act on, and on any conflict the guideline wins.

### Step 7: Resolve the Period and the Panel Path

1. **Act**: Resolve `$period` to a **period key** in one of the convention's normalized forms — `YYYY-MM` (default: the current calendar month), `YYYY-Wnn`, or `YYYY-MM-DD_YYYY-MM-DD` — applying the convention's **normalization rule** (a range spanning exactly a calendar month or ISO week collapses to the shorter form) so one window has exactly one key, then derive the window's start/end dates from it.
2. **Act**: Resolve the panel path: `$output` (default `.pair/working/reports/cost/`, honoring the project's `working_path` override) + `<period-key>-cost-panel.md`.
3. **Verify**: Exactly one period key, one window and one panel path resolved. An unparseable `$period` → ask for the intended window; never guess a period silently.

### Step 8: Collect the Period's Merged PRs

1. **Act**: Read the window's **merged PRs** — closed PRs whose **merge** date falls inside the window — from the code host / PM tool: resolution: see [way-of-working / PM-tool resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/way-of-working-pm-resolution.md). Read-only: report mode never writes to the tracker.

   **Closed-unmerged PRs are excluded** (abandoned/rejected/superseded). A PR closed without merging has **no merged diff**, so Step 9.1 cannot derive a `real` class for it: it never shipped, and counting it would pollute both the drift count and the class distribution with a non-event. They are not rendered as rows and not counted anywhere in the panel; the headline states how many the window held (`**Excluded**: N closed unmerged`) so the exclusion is visible rather than a silent gap between the tracker's "closed" count and the panel's.

   **Window size (context safety without a refused panel).** Step 9.1 re-classifies **every** merged diff in the window, so the work grows with the PR count — but the consolidated panel is **always produced**, including for the default window (the current calendar month, which on an active repo routinely holds 50–100+ merged PRs). Process the window **PR by PR** (batching the tracker reads as convenient — no batch size is prescribed here): per PR retain only its panel row (id, predicted, real, drift, deploy match, top real signal) and **discard the diff before moving to the next**, so context stays flat regardless of how many PRs the period holds. The bound rests on that retain-and-discard rule, not on any batch constant. There is **no per-run PR cap**: sharding a month into per-week sub-windows would yield 4–5 panels instead of the one consolidated view the period is supposed to have, and refusing to write is exactly the "silent skip / failed run" the panel convention rules out. Announce the count found (`N merged PRs in <period-key>`) and **continue without waiting** — informational only, never a prompt and never a refusal: report mode is non-interactive and may be invoked unattended (Composition Interface), so a run that waited for an answer would stall forever.

   **Never a _silently_ truncated panel.** If a run cannot process every merged PR of the window (executor limits reached, a diff unreadable, tracker pagination exhausted), the panel is still written and its headline states the shortfall explicitly — `**Coverage**: N of M merged PRs processed` plus the reason **and the unprocessed ids, all in that one line** (Step 11.5). That line is the **single** place an unprocessed PR is named: it gets **no per-PR row** (no processed diff ⇒ no `real` class to put in one), exactly as a closed-unmerged PR is counted in the headline without a row. Truncation is legitimate only when it is visible where the figures are read; a partial panel that looks complete would under-report drift.

2. **Act**: For each PR collect (a) the **predicted** cost class, resolved by the precedence rule in 8.2.1 below; (b) the surface needed to derive the **real** class (the merged diff); (c) the deploy reference, if the project declares deploy/billing telemetry in `infrastructure.md` (Step 9.2).

   **8.2.1 — Predicted-class precedence (the prediction is _refinement-time only_).** In this order, first hit wins:

   1. The **story-side** classification matrix's cost row, or the **story's** `cost:*` tag when the project projects it (§5) — the shift-left value `/pair-process-refine-story` recorded _before_ any code existed. This is the prediction. **Resolving the PR to its story** (in this order, first hit wins): the PR body's **`**Story/Epic:**` line** (pr-template); a **linked issue** on the PR (closing keyword / tracker link); a **`US-<id>` token in the branch name** (branch-template `feature/US-<id>-<slug>`). This resolution is the prerequisite for precedence 1 — without it the story-side matrix is unreachable even when it exists.
   2. The **PR body's** matrix row (or the PR's `cost:*` label) **only when it still carries the refinement value copied at publish time** — i.e. review did not touch it.
   3. Otherwise → **`no prediction — real only`** (8.3), never a fabricated match.

   **When no story resolves**, record the row's reason as **`prediction source unresolved`** (still a `no prediction — real only` row) and count it separately from PRs whose story _was_ reachable and carried no cost class. The two are different diagnoses and Step 11.3's headline must not conflate them: `cost was never assessed` is a process finding, an unresolved story link is a **traceability** finding (missing `Story/Epic:` line / link / branch token) — reporting the second as the first hides real predictions behind "cost was never assessed".

   **Never read the review-time class as the prediction.** `/pair-process-review` re-derives cost from the merged diff and, on a raise, **overwrites the PR-description matrix row in place and re-applies the projected `cost:*` label** — so a review-touched PR body/label holds the _review_ class, which is the same computation Step 9 performs. Pairing them would report `match` for every re-classified PR and make the drift invisible (refinement said green, review raised to orange ⇒ the row must read `under-predicted`, not `match`). A PR body row is therefore usable as the prediction only when the refinement value is provably intact — the story record still holds it, or the review record states the pre-raise value; when neither does, the row is `no prediction — real only`, not a guess.
3. **Verify**: Every **merged** PR of the window is in the set (closed-unmerged ones counted as excluded, not as rows), any PR the run could not process is named in the panel's `**Coverage**` line — there and nowhere else, never as a per-PR row and never dropped — and every predicted value present came from refinement (never from review). A PR whose prediction is missing — cost never assessed, story unresolvable, or only a review-time class recoverable — is **retained** and marked `no prediction — real only` with its reason: never dropped, silently or otherwise, and never paired against a review-time class.

### Step 9: Pair Predicted vs. Real (bidirectional)

1. **Act**: For each PR, derive the **real** class by running the classification path (Steps 3–5 only — surface, scan, compute; Step 6's per-run verdict block is _not_ emitted here, report mode emits the panel instead) over its merged diff, then place it beside the predicted class — the bidirectional view: what refinement expected vs. what the merged change actually carries.
2. **Act**: **Deploy match** — rules, APIs, windows and permissions live in the [cost & billing telemetry guideline](../../../.pair/knowledge/guidelines/quality-assurance/quality-monitoring/cost-billing-telemetry.md) (`guidelines/quality-assurance/quality-monitoring/cost-billing-telemetry.md`); this step applies them and holds no provider knowledge (R2.13). Read the **`## Cost & Billing Telemetry`** section of `infrastructure.md` once per run, then per PR:
   - **Matched path** — declaration complete (every required key per the guideline): resolve the PR's merge commit to the **first deployment that shipped it into the declared environment** (the guideline's deterministic multi-deployment rule), then record the **observed cost movement** = the delta in the declared billing metric for the deployed service between **equal-length** windows before and after that deployment, exactly as the guideline defines. Call only what the declared source kinds name in the guideline, with the **minimum read-only** permission it documents; never read, write or echo a credential, and never record one in the panel.
   - **Degraded path (permanent, the supported default)** — declaration absent or incomplete: the row reads `not available — no deploy telemetry declared` (naming the missing keys when incomplete). Never a fabricated or inferred match.
   - **Distinct reasons**, never collapsed into the declaration case: `not available — no deployment found` (no shipped deployment for the merge commit in the declared environment); `not available — billing window not yet consolidated` (the post window is still provisional — never a partial delta presented as final); `not available — not attributable (shared service)` (the metric covers more than the deployed change; a merge spanning services yields one row per attributable service). A **half-resolved** match (one half reachable, the other not) reads `not available — <which half> unreachable`, never a partial claim.
   - A provider price change inside a window is stated in the panel as a **confounder**, not a prediction error.
   - **Report mode never blocks** a merge or a release: any failure here degrades the row, nothing else.

3. **Verify**: Each row has a predicted value (or `no prediction — real only` + its reason), a real value, and a deploy-match value (or `not available`).

### Step 10: Flag Drift

1. **Act**: Drift = predicted ≠ real. Direction is what matters: **under-predicted** (real higher than predicted — e.g. predicted green, real red) is the actionable direction and is flagged first; **over-predicted** (real lower) is reported as calibration signal, not an alarm.

   **Drift is measured against the _current_ rule set.** `real` is re-derived at run time through Step 2's catalog/adoption (today's files), while each prediction was made against the catalog as it stood at refinement. A **cost-catalog or adoption change inside the window** — a new signal, a new provider heuristic, a tuned threshold — therefore shows up as drift even where every prediction was correct when made. Name it: the panel states the confounder whenever the window is being read as a calibration signal, and a systematic one-direction shift right after a catalog change should be read as a catalog delta first, a prediction problem second.

2. **Act**: Aggregate the headline: PRs monitored, closed-unmerged excluded, drifted (under / over), `no prediction — real only` (split by reason — never assessed vs. `prediction source unresolved`), class distribution predicted vs. real, and the largest drifts.

   **What the figures count: the _processed_ PRs (N).** `**Monitored**`, the drift counts, the `no prediction` split and the class distribution are all over the N PRs this run actually classified. The found count M appears **only** in the `**Coverage**` line (Step 11.5), which is what qualifies N — so the panel never mixes a "found" denominator into figures derived from processed rows.

3. **Verify**: Every **processed** PR is exactly one of `match | under-predicted | over-predicted | no prediction`. A merged PR the run could not process is a **fifth, separately counted member — `unprocessed`** — named only in the `**Coverage**` line and excluded from `**Monitored**`, from drift and from the class distribution. It is **never** folded into `no prediction`: that figure means "measured, but nothing was predicted for it", and padding it with PRs that were never measured at all would corrupt exactly the numbers the `**Coverage**` line exists to qualify (and re-conflate the 8.2.1 diagnoses).

### Step 11: Render and Write the Consolidated Panel

1. **Act**: Render the **consolidated panel** headline-first per the convention (D22): the headline block at the top, the per-PR and per-class breakdowns in collapsed `<details>` sections. The headline states the **current-catalog caveat** from Step 10.1 (drift measured against today's rule set; catalog changes inside the window are a confounder) so the figures are never read as pure prediction quality.

   **Rule-set provenance (makes that caveat falsifiable).** The headline also records the **resolved rule-set revision** — the revision (commit or version) of the cost catalog and of the adoption files Step 2 resolved `real` through. Without it, a `2026-07` panel regenerated after a catalog change is indistinguishable in provenance from the pre-change one, so a reader cannot tell whether a jump in under-predicted rows is the confounder the caveat warns about or real drift. This is a **resolved input**, not a wall clock: it satisfies the convention's provenance bullet and keeps `Same inputs ⇒ same content` (a `generated at` timestamp would break it, and is never added).
2. **Act**: Write it to the panel path from Step 7, creating the directory when absent. Per the convention, the **period key** identifies the file: a re-run for the same period **updates that panel in place** — one file per period, never a second file, never appended. This is a direct write of an operational artifact (D14), the same exception `/pair-capability-assess-security`'s audit and `/pair-capability-assess-coupling`'s full scope use; no adoption content is ever written here.

   **Coverage never regresses** (the convention's _no coverage regression_ rule). The in-place update is **not unconditional**: read the panel already at that path first and compare, for the same period and the same `**Rule set**` revision, **how many PRs each panel actually processed** — the existing panel's `**Monitored**` count against this run's. **Completeness is not the comparison basis**: while a calendar month is still open its denominator grows, so a panel written mid-month with no `**Coverage**` line (complete _as of then_) can cover fewer PRs than a later run reporting `**Coverage**: 40 of 73`. Keeping the earlier one because it reads "complete" would discard the strictly better result; the processed count is the only basis that survives a moving denominator, and it is readable from either panel's headline. If the panel on disk processed **more**, do **not** overwrite it — **keep it**, one of two ways: either merge in the rows this run adds where they are separable **and recompute the headline over the union of processed PRs** (`**Monitored**`, `**Coverage**`, `**Drift**` and the class distribution all recounted, and every merged-in id struck from the unprocessed list — a PR that now has a row must never still be named as unprocessed in the line above it), or leave the file untouched. Either way report the shortfall in the run output (Step 11.5), not in the file. Failure case this rules out: a run writes `Coverage` omitted / `**Drift**: 12` over 73 of 73 PRs, then a context-tight re-run processes 40 and overwrites it with `**Coverage**: 40 of 73` / `**Drift**: 6` — same inputs, different content, the fuller figures gone, and a reader comparing months reads a drop in drift that is purely a run artifact.
3. **Act**: **No cost data** — render and write the panel with the headline `no cost data for this period` plus the reason, rather than failing; cost monitoring depends on cost having been assessed, so it says so. Two **distinct** shapes — the headline must never be contradicted by the table under it:
   - **Empty window — no merged PR at all**: `no cost data for this period — no merged PRs in the window` (naming the closed-unmerged ones excluded, if any). The headline _is_ the whole panel; no per-PR table follows. The literal says _merged_, not _closed_: a window holding 3 abandoned PRs and 0 merged renders `**Excluded**: 3 closed unmerged` right under it, which a "no closed PRs" headline would contradict.
   - **Merged PRs but no prediction on any of them**: `no cost data for this period — no _predicted_ cost data, so drift is not computable; N real-only rows below`, plus the reason **split by diagnosis** (Step 8.2.1): _cost was never assessed_ (e.g. Tag Projection not activated, quality-model §5) vs. _`prediction source unresolved`_ (the PR carried no `Story/Epic:` line, link or `US-<id>` branch token, so the story-side matrix was unreachable — a traceability gap, not evidence that cost went unassessed). Reporting the second as the first is forbidden: it hides predictions that exist. The real-only rows **are** listed (every PR stays `no prediction — real only`, per Step 8.3), and the qualifier is **required**: a bare "no cost data" headline above a table of real classes contradicts itself and costs the panel its credibility.
4. **Act**: **Reports area not writable** (read-only checkout, permissions): present the panel **inline** in the output and tell the human where to save it; the run still succeeds.
5. **Act**: **Incomplete coverage** (Step 8.1: a merged PR of the window could not be processed — executor limits, unreadable diff, tracker pagination): still **write the panel** — unless 11.2's no-regression rule keeps a more complete one — with `**Coverage**: N of M merged PRs processed`, the reason, and the unprocessed ids **all in that single headline line**, which is where unprocessed PRs are named and the only place: they get no per-PR row and count as `unprocessed`, outside `**Monitored**`, drift and the class distribution (Step 10.3). A partial panel keyed to the full period is acceptable only while it says so in the headline; it is never presented as complete, it never replaces a panel that already covers more of the same period (Step 11.2 — the shortfall is reported in the run output instead), and the run is never refused over window size.
6. **Verify**: Exactly one panel exists for the period at the resolved path (created, updated in place, or deliberately left as-is by the no-regression rule), or the inline degradation was reported instead; when fewer than all merged PRs were processed, the headline carries the `**Coverage**` line with its unprocessed ids, and the panel on disk is never less complete than it was before the run.

## Output Format

### Classification Mode

```text
COST ASSESSMENT (output-only — no files written):
├── Class:    [green | yellow | orange | red] — [1-line rationale]
├── Surface:  [diff | story #ID | scope <area>]
├── Signals:  [N detected — N unknown-surface]
├── Rule Set: [KB default | + provider <name> | + adoption tech/risk-matrix.md]
└── Feeds:    Cost dimension of the classification matrix (quality-model §3.3) — own class, not part of the risk max

<details>
<summary>N cost signals</summary>

| Signal | Location | Class | Notes |
| ------ | -------- | ----- | ----- |
| [signal] | [file:location] | [green|yellow|orange|red] | [provider heuristic / unknown-surface] |
...

</details>
```

No signal detected renders as: `Class: green — no cost surface touched` with an empty (or omitted) signals table.

### Report Mode

```text
COST REPORT (report mode — writes exactly one file: the period panel):
├── Period:   [<period-key>] — [start .. end]
├── PRs:      [N merged monitored (of M in the window — coverage line in the panel when N < M) — N with a prediction, N no prediction — real only (N never assessed, N prediction source unresolved); N closed unmerged excluded]
├── Drift:    [N drifted — N under-predicted, N over-predicted | none] (vs. the CURRENT catalog, <catalog-revision>)
├── Deploy:   [N matched | not available — <reason per Step 9.2>]
├── Panel:    [.pair/working/reports/cost/<period-key>-cost-panel.md — created | updated in place | kept (existing panel covers more of the period — no coverage regression) | inline (reports area not writable)]
└── Data:     [ok | no cost data for this period — cost never assessed / Tag Projection not activated / prediction source unresolved]
```

The panel itself (headline-first, D22):

```markdown
# Cost Panel — <period-key>

**Monitored**: N merged PRs (<start> .. <end>) · **Drift**: N (N under-predicted, N over-predicted) · **No prediction**: N (N never assessed, N prediction source unresolved) · **Excluded**: N closed unmerged · **Deploy match**: N matched | not available
**Coverage**: N of M merged PRs processed — <reason> — unprocessed: #ID, #ID (omit the whole line when N = M; the unprocessed ids live here and nowhere else — an unprocessed PR gets no per-PR row and is counted in neither the drift figures nor the distribution below)
**Rule set**: cost catalog `cost-assessment.md` @ <revision> + adoption `tech/risk-matrix.md` @ <revision> — the resolved inputs `real` was derived from (provenance, not a run timestamp)

_Drift is measured against the **current** cost catalog/adoption (Step 10.1), i.e. the revision above: a catalog change inside the window shifts `real` for predictions that were correct when made — compare this line across re-runs to tell that confounder apart from real drift._

<details>
<summary>Per-PR predicted vs. real</summary>

| PR | Predicted | Real | Drift | Deploy match | Top real signal |
| -- | --------- | ---- | ----- | ------------ | --------------- |
| #ID | [green|yellow|orange|red | no prediction — real only (never assessed \| prediction source unresolved)] | [green|yellow|orange|red] | [match | under-predicted | over-predicted | no prediction] | [matched | not available] | [signal @ file:location] |
...

</details>

<details>
<summary>Class distribution — predicted vs. real</summary>

| Class | Predicted | Real |
| ----- | --------- | ---- |
| green / yellow / orange / red | N | N |

</details>
```

An **empty window** renders the same panel with the headline `no cost data for this period — no merged PRs in the window` and no per-PR table. **Merged PRs but no predictions** renders the qualified headline `no cost data for this period — no _predicted_ cost data, so drift is not computable; N real-only rows below`, with the reason split into _never assessed_ vs. _`prediction source unresolved`_, _followed by_ the real-only per-PR table (Step 11.3). A window whose PRs could not all be processed still writes its panel, carrying the `**Coverage**: N of M merged PRs processed` line with the unprocessed ids in it (Step 11.5) — there is no window size that produces no panel — except where a **more complete** panel for the same period already exists, which is kept rather than overwritten (Step 11.2).

## Composition Interface

When composed by `/pair-process-review` (review-time cost dimension):

- **Input**: the reviewing skill invokes `/pair-capability-assess-cost` against the PR diff (`$diff`).
- **Output**: returns the class + collapsed signals (Output Format above). The caller embeds it into the review report's cost section (1 line + `<details>`, D22) and feeds the class into `/pair-capability-classify`'s cost dimension.
- **Persistence**: none — this skill writes nothing.

When composed by `/pair-process-refine-story` / `/pair-capability-classify` (shift-left, refinement):

- Classifies from `$story` scope, producing the declared cost class carried in the story-body matrix — the review pass may only confirm-or-raise it, never lower it (D17 "built twice": the class is estimated from story context at refinement and re-derived from the diff at review — the more conservative of the two wins).

When invoked **independently** (`/pair-capability-assess-cost` on a branch or story): full one-shot classification, verdict returned to the developer.

In **report mode** the skill is standalone: it composes nothing and is composed by nothing — it consumes what classification mode and the quality model already produced (predicted classes recorded at refinement, merged PRs from the tracker) and hands back the panel path. **Trigger, by design: on demand only** — a human (or an automation loop) runs `/pair-capability-assess-cost $mode: report` when the period's monitoring is wanted, and the `next` catalog row is its discovery surface. No in-tree caller invokes it, and none is planned here; should a cadence be wanted later, the retro/metrics flow (#222) is the intended driver and this section is where that caller gets listed. Cadence stays the caller's concern (D18).

> Review-side wiring — `/pair-capability-assess-cost` listed as a Composed Skill of `/pair-process-review` (its Step 2.5, Cost Assessment) and the `### Cost` section of the code-review template — **landed in #228** and is in-tree. Review-time classification is `classify` mode; report mode adds nothing to that wiring and depends on nothing further.

## Edge Cases

- **No cost-relevant change**: class `green`, rationale "no cost surface touched".
- **Unresolvable cost surface** (unknown tech): class `orange` with an explicit **unknown-surface** flag — conservative and visible, never silently green (Step 4.2).
- **Quality model missing**: **HALT** with a pointer to install/bootstrap the KB (Step 0) — the model is a prerequisite, not something this skill invents.
- **Provider not covered in-tree**: resolved via the adoption link the adoption file supplies (fallback/extension) — no skill change (Q3).
- **Adoption file missing/malformed**: warn, fall back to KB defaults (D21) — never a HALT.
- **No cost data in the monitored period** (report mode): the panel is still written, headlined `no cost data for this period` **with the reason qualifying which shape it is** — an empty window (no merged PRs), or merged PRs with no _predicted_ class (cost never assessed, or the prediction source unresolved), in which case the real-only rows are still listed under the qualified headline — graceful, never a failure (Step 11.3).
- **PR closed without merging** (report mode): **excluded** — no merged diff exists, so no `real` class can be derived; it is counted as `**Excluded**: N closed unmerged` in the headline and contributes to neither drift nor the class distribution (Step 8.1).
- **PR with no predicted class** (report mode): retained as `no prediction — real only`, contributing to the real-class distribution but not to drift — never dropped from the panel. Applies equally when only a **review-time** class is recoverable: that class is the same computation as `real`, so it is not a prediction (Step 8.2.1).
- **PR whose story cannot be resolved** (report mode): `no prediction — real only` with the reason `prediction source unresolved` — counted and reported _separately_ from "cost was never assessed", because the missing thing is the PR→story link (`Story/Epic:` line, linked issue, `US-<id>` branch token), not the assessment (Step 8.2.1).
- **Large window** (report mode): no PR cap and no refusal — PRs are processed one at a time, each diff discarded once its row is retained, so the default monthly window still yields one consolidated panel (Step 8.1). If some PR could not be processed, the panel is written **with** `**Coverage**: N of M merged PRs processed` and the unprocessed ids in that line, which is their only rendering (no per-PR row, counted as `unprocessed`) — never a silently truncated panel (Steps 10.3, 11.5).
- **Partial re-run over a more complete panel** (report mode): the in-place update is **skipped** — a run whose coverage is lower than the existing panel's for the same period and rule-set revision keeps that panel (merging its own new rows where separable) and reports the shortfall in the run output instead; a 40-of-73 re-run never overwrites a 73-of-73 panel (Step 11.2).
- **No deploy telemetry** (report mode): the deploy-match dimension reads `not available — no deploy telemetry declared` for the whole period rather than fabricating a match — the permanent, supported default; with telemetry declared, an unresolved PR carries its own distinct reason (Step 9.2).
- **Report-only argument in a classify run** (`$output` without `$mode: report`/`$period`): ignored **with a warning** naming it — never silently dropped, and never a reason to enter report mode (Step 1.4).
- **Reports area not writable** (report mode): the panel is presented inline with a save hint; the run succeeds (Step 11.4).

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (guideline missing → minimal assessment against §3.3 alone, ask directly; adoption file missing → run against KB defaults; PM tool unreachable → n/a in `$diff` mode) for the standard scenarios. Additional cases:

- **cost-assessment guideline absent** (KB partially installed): assess against quality-model §3.3's inline signal list only, and note the reduced catalog in the output rather than HALTing.
- **`/pair-capability-classify` not available** (independent invocation): the class is still emitted; it simply isn't folded into a compiled matrix by a caller — the developer reads the verdict directly.
- **PM tool unreachable in report mode**: **HALT** with no partial panel written — a panel covering only the PRs that happened to be reachable would misreport drift. Classification mode is unaffected (it never reads the tracker).
- **Window larger than one run can finish** (report mode): degrade by **writing the panel anyway** with the `**Coverage**: N of M merged PRs processed` line, the reason and the unprocessed ids (Step 11.5) — unlike an unreachable tracker, the PRs that were read are real data, and the shortfall is stated where the figures are read instead of costing the period its panel. The one exception is a panel already on disk with **higher** coverage for the same period: it is kept and the shortfall goes to the run output only (Step 11.2), because degrading must never destroy figures a previous run had.
- **working-area guideline absent** (KB partially installed): apply the convention as summarized in Steps 7 and 11 (period-keyed filename, in-place update, headline-first) and note the reduced reference — never HALT.

## Notes

- **Classification mode writes no files** — the strict output-only convention of the assess-\* family; the class is data for `/pair-capability-classify`/`/pair-process-review`, never an action this skill takes. **Report mode writes exactly one file**: the period panel under `.pair/working/reports/cost/` (D14 operational artifact — the same exception `/pair-capability-assess-security`'s audit and `/pair-capability-assess-coupling`'s full scope use). No adoption content and no backlog items in either mode.
- **Never blocks** — no merge authority in either mode; a `red` class or a flagged drift is a signal for the caller, not a gate this skill enforces.
- **Idempotent** — see [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md): classification mode computes a fresh class every run against the current diff/story by design (signals change commit to commit), no cached verdict; report mode is idempotent **by period key** — a re-run for the same period updates that one panel in place (never a second file).
- **Provider-agnostic** — adding a provider is an adoption/KB change (a per-provider section in the guideline, or an adoption link), never a change to this skill (R2.13).
- **D22** (1-line verdict + collapsed details): a project-level rendering decision the caller honors; this skill emits in that shape.
