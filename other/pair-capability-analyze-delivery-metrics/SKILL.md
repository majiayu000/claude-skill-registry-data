---
name: pair-capability-analyze-delivery-metrics
description: "Generates the delivery/AI-metrics retro panel for a period — bug resolution time, PR lead time, process adoption — computed from the adopted PM tool/code host against the delivery-metrics guideline (definitions, aggregation, low-sample rule, bug mapping) and written as ONE period-keyed panel under .pair/working/reports/metrics/: headline numbers + trend first, raw breakdowns collapsed, idempotent by period key. Invoke on demand for a retro or a periodic delivery review ('delivery metrics for July', 'how long are bugs taking', 'AI metrics report'); cadence stays the caller's concern, an automation loop may drive it. Report-only: writes exactly that panel — no adoption content, no backlog items, no merge authority. Tool-agnostic by construction: adding a tracker touches adoption/KB only, never this skill."
version: 0.1.0
author: Foomakers
---

# /pair-capability-analyze-delivery-metrics — Delivery & AI Metrics Panel

Measure how AI-assisted delivery actually performed over a period and render it as one panel: **bug resolution time**, **PR lead time**, **process adoption** — the R9.5 trio, under the Delivery pillar of the [quality model](../../../.pair/knowledge/guidelines/quality-assurance/quality-model.md) (§7, _AI metrics / retro_).

**The definitions are not here.** Every metric definition, clock, aggregation rule, low-sample threshold, bug mapping and per-tool field mapping lives in the [delivery-metrics guideline](../../../.pair/knowledge/guidelines/quality-assurance/delivery-metrics.md) (D17/D21) — this skill _applies_ them. Adding a metric family or a tracker is a guideline/adoption change, never a change to this skill (R2.12).

**Report-only, one file.** The panel is an operational artifact under `.pair/working/` (D14): no adoption content, no backlog items, no verdict, no merge authority. It reports what other capabilities already produced, and reads its sources read-only — it never writes to the tracker.

## Arguments

| Argument  | Required | Description                                                                                                                                                                   |
| --------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$period` | No       | The reporting window as a period key — `YYYY-MM`, `YYYY-Wnn`, or `YYYY-MM-DD_YYYY-MM-DD` (default: the current calendar month).                                                 |
| `$output` | No       | Directory the panel is written to. Default: `.pair/working/reports/metrics/`, honoring the project's `working_path` override (one knob, not two — the report-panel convention). |

## Rule Set

Every rule resolves through the standard **Argument > Adoption > KB default** cascade:

1. **KB default** — the [delivery-metrics guideline](../../../.pair/knowledge/guidelines/quality-assurance/delivery-metrics.md) (metric set, clocks, median/p75 aggregation, the `N < 5` low-sample rule, per-tool field mapping) plus the [report-panel convention](../../../.pair/knowledge/guidelines/collaboration/working-area.md) (period key, path, in-place idempotency, headline-first, coverage rules).
2. **Tool routing (adoption)** — the PM tool and code host, resolved through [way-of-working / PM-tool + code-host resolution](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/way-of-working-pm-resolution.md): item-side inputs come from the PM tool, PR-side inputs from the code host (identical in a single-tool project). Each tool's mechanics live in its own `*-implementation.md` adapter.
3. **Project delta (adoption)** — an optional `## Delivery Metrics` section in `tech/way-of-working.md`: `bug-label` / `bug-type`, `exclude-authors`, `adoption-signals`. Delta-only; absent keys fall back to the guideline's per-tool defaults.

A missing or malformed adoption file is treated as absent: warn, fall back to the KB default, and continue — adoption absence never halts a run.

## Algorithm

### Step 0: Load the Metric Definitions (BLOCKING prerequisite)

1. **Check**: Does the [delivery-metrics guideline](../../../.pair/knowledge/guidelines/quality-assurance/delivery-metrics.md) resolve (KB installed)?
2. **Act**: If it is **missing**, **HALT**: _"Delivery-metric definitions not found — install/bootstrap the KB (`quality-assurance/delivery-metrics.md`) before running analyze-delivery-metrics."_ The clocks, the aggregation and the low-sample threshold are the rule set, not defaults this skill invents; a "bug resolution time" computed from a guessed clock is a number nobody can compare across periods.
3. **Verify**: The metric set, the aggregation rules, the bug-mapping order and the per-tool field mapping are loaded, and the report-panel convention is available (absent ⇒ apply the mechanics summarized in Step 6 and note the reduced reference).

### Step 1: Resolve the Period and the Panel Path

1. **Act**: Resolve `$period` to a **period key** in one of the convention's normalized forms — `YYYY-MM` (default: the current calendar month), `YYYY-Wnn`, `YYYY-MM-DD_YYYY-MM-DD` — applying the convention's **normalization rule** (a range spanning exactly a calendar month or ISO week collapses to the shorter form), then derive the window's start/end in **UTC**.
2. **Act**: Derive the **previous window of equal length** — the trend comparison's population — resolving it **per key form** exactly as the guideline defines (a `YYYY-MM` key compares against the whole preceding calendar month, `YYYY-Wnn` against the preceding ISO week, and only an explicit range is measured by day count). The rule lives there; this step applies it.
3. **Act**: Resolve the panel path: `$output` (default `.pair/working/reports/metrics/`, honoring `working_path`) + `<period-key>-delivery-metrics.md`.
4. **Verify**: Exactly one period key, one window, one previous window and one panel path. An unparseable `$period` → ask for the intended window; never guess a period silently.

### Step 2: Resolve the Rule Set and the Tools

1. **Act**: Read the KB default (Rule Set layer 1), then the adoption layers 2–3, skipping any file that does not exist.
2. **Act**: Resolve the **PM tool** and the **code host** by name, and select each one's adapter for the field mapping. Absent `code-host` ⇒ the code host **is** the PM tool (single-tool path).
3. **Act**: Resolve the **bug mapping** (adoption `bug-label`/`bug-type`, else the tool's native defect marker), the **author exclusions** (default: bot accounts) and the **adoption signals** the project declares.
4. **Act**: Record the **resolved inputs** for the panel's provenance line: PM tool + code host, the guideline's revision, the adoption file's revision.
5. **Verify**: An effective rule set exists with every value traceable to a layer; adoption absence is logged as "KB defaults only", never as an error.

### Step 3: Confirm the Tools Answer (HALT before any write)

1. **Act**: Issue one bounded read per resolved tool for the window (per its adapter).
2. **Act**: **PM tool or code host unreachable** — error, auth failure, permission denied — → **HALT** with the tool named and the reason, having written **nothing**: no panel, no partial file, and no touch to a panel already on disk for this or any other period. A half-collected window would report a low median as delivery improvement.
3. **Act**: Keep "unreachable" apart from "has no such surface". A tracker with **no PR surface at all** (e.g. a filesystem backlog with no code host declared) is a **data gap**, not a failure: the PR-side families read `not available` for the period and the run continues.
4. **Verify**: Every resolved tool answered, or the run halted with nothing written; a legitimately absent surface is recorded as `not available` rather than halting.

### Step 4: Collect the Window's Items

1. **Act**: Collect, per the adapter field mapping: **issues closed inside the window** (population for defects), **pull requests merged inside the window**, the **closed-unmerged** PR count (excluded from lead time — they never shipped), and the sources each declared adoption signal reads.
2. **Act**: Process the window **item by item** (batching tracker reads as convenient), retaining per item only what the metrics and the panel rows need — timestamps, the mapping verdict, the flags — and **discarding the payload before moving to the next**. Context stays flat regardless of how many items the period holds, so window size is never a reason to refuse a panel. Announce the counts found and **continue without waiting**: this skill is non-interactive and may run unattended.
3. **Act**: **Coverage** — when the run cannot process every item of the window (executor limits, an unreadable item, pagination exhausted), keep going and record the shortfall: `N of M processed`, the reason, and the unprocessed ids. Those ids are named in the panel's `Coverage` line **and nowhere else** — no per-item row exists for an item that was never processed, and it counts in no figure.
4. **Act**: Collect the **previous window** the same way, retaining only what the trend needs (the per-family medians), so the comparison is computed from the same definitions rather than read from an older panel (a stale panel would carry a different rule-set revision).
5. **Verify**: Both windows are collected, every retained item carries the fields its family needs, closed-unmerged PRs are counted as excluded rather than dropped silently, and any shortfall has its ids recorded for the `Coverage` line.

### Step 5: Map the Defects

1. **Act**: Apply the guideline's mapping order to every closed issue in the window, first hit wins: the **adoption declaration** (`bug-label` / `bug-type`), else the **tool's native defect marker**, else **unmapped**.
2. **Act**: An **unmapped** issue is counted as a **generic issue**, never as a bug, and its count is carried into the panel (`N issues unmapped — counted as generic`). Silence here is the harmful case: a generic issue counted as a defect inflates the figure, one dropped hides work, and neither is visible without the count.
3. **Act**: **Reopened issues** — the last close inside the window is the resolution event, and the reopen count travels with the row: one row per issue, never one per close.
4. **Act**: Count the defects **still open at period end** separately. They have no resolution time, so they are outside the median — and stated, so a period that resolved nothing cannot read as a period with no defects.
5. **Verify**: Every closed issue is exactly one of `defect | generic (unmapped) | generic (mapped non-defect)`, each with its source of truth; reopen and still-open counts are recorded.

### Step 6: Compute the Three Families

1. **Act**: Compute per family, applying the guideline's rules (never a threshold of this skill's own):
   - **Bug resolution time** — `median (p75)` of `closed − created` over the window's defects, plus the reopen count and the still-open count.
   - **PR lead time** — `median (p75)` of `merged − opened` over the window's merged PRs, plus the median draft share where the tool exposes the draft transition, the excluded-author count, and the closed-unmerged count.
   - **Adoption** — each declared signal as a ratio over the period. A signal whose source is absent reads **`not available`**, never `0%`: zero claims the process was skipped, `not available` says the tools cannot answer.
2. **Act**: **Trend** — each family's median against the previous window's, as a signed delta plus direction. No comparable predecessor ⇒ `no trend — first period`.
3. **Act**: **Low sample** — fewer than the guideline's threshold (`N < 5`) in a family ⇒ report the **raw values and the count**, state `low sample (N < 5)`, and compute **no trend** for it. A trend drawn from three items is noise presented as a signal, so the warning travels with the figure wherever it appears, not in a footnote.
4. **Act**: **Zero items** in a family ⇒ `no data for the period` for that family, with the reason (empty population vs. absent source). The panel is still produced.
5. **Verify**: Each family holds either a figure with its trend, or an explicit `low sample` / `no data` / `not available` state with a reason — and every threshold, clock and aggregation used is the guideline's. No family is left blank, and no trend exists beside a low-sample figure.

### Step 7: Render and Write the Panel

The panel's path, period key, in-place idempotency, headline-first shape, empty-period, not-writable and coverage behavior all follow the one [report-panel convention](../../../.pair/knowledge/guidelines/collaboration/working-area.md) — shared with the cost panel, one reports-area pattern for the whole KB. That guideline is **authoritative**; the mechanics below are the beats this step acts on, and on any conflict the guideline wins.

1. **Act**: Render **headline-first** (D22): the three headline figures with their trends at the top, readable in about one screen, then the per-defect, per-PR and per-signal breakdowns in collapsed `<details>` sections. The headline also carries the population, the exclusions (closed-unmerged, excluded authors), the unmapped count, the still-open count, and a link to the [delivery-metrics guideline](../../../.pair/knowledge/guidelines/quality-assurance/delivery-metrics.md) for the definitions — the panel points at them instead of restating them.
2. **Act**: Record the **input provenance** in the headline: the resolved PM tool and code host, the guideline's revision, the adoption file's revision. A resolved-input revision keeps `same inputs ⇒ same content` intact; a wall-clock `generated at` line would break it and is never added.
3. **Act**: Write to the Step 1 path, creating the directory when absent. The **period key** identifies the file: a re-run for the same period **updates that panel in place** — one file per period, never a second file, never appended. This is the direct write of an operational artifact (D14), the same exception the cost panel and the security audit use; no adoption content is ever written here.
4. **Act**: **Coverage never regresses.** Before overwriting, read the panel already at that path and compare, for the same period and the same input revision, **how many items each panel actually processed** (the headline's processed count on both sides — not which one looks complete: an open period's denominator grows, so a panel that was complete when written can cover fewer items than a later partial one). If the panel on disk processed **more**, keep it: either merge in the rows this run adds where they are separable **and recompute the headline over the union** (every figure recounted, every merged-in id struck from the unprocessed list, so no table contradicts the line above it), or leave the file untouched. Report the shortfall in the run output, not in the file.
5. **Act**: **Empty period** — still render and write the panel, headlined `no data for the period` **with the reason** the inputs are absent (no defects closed and no PRs merged in the window; or a window whose only PRs were closed unmerged, which the headline states as `Excluded: N closed unmerged` rather than contradicting itself). A partly-empty window keeps the families that do have data and marks the others per Step 6.4.
6. **Act**: **Partial coverage** — write the panel with `Coverage: N of M items processed`, the reason, and the unprocessed ids **all in that one headline line**, which is the only place they appear: an unprocessed item gets no row and counts in no figure. A partial panel keyed to the full period is legitimate exactly while it says so.
7. **Act**: **Reports area not writable** (read-only checkout, permissions): present the panel **inline** in the output with a save hint; the run succeeds.
8. **Verify**: Exactly one panel exists for the period at the resolved path (created, updated in place, or deliberately kept by the no-regression rule), or the inline degradation was reported instead; the headline carries the provenance line, the definitions link, and — whenever fewer than all items were processed — the `Coverage` line with its unprocessed ids. The panel on disk is never less complete than it was before the run.

### Step 8: Emit the Run Output

1. **Act**: Render the run block per Output Format below — the period, the three families, the panel's disposition, the data state.
2. **Verify**: The output names exactly one panel path and one disposition, states every degradation that fired, and asserts no verdict: this skill reports, it blocks nothing and it writes nothing else.

## Output Format

```text
DELIVERY METRICS (report-only — writes exactly one file: the period panel):
├── Period:   [<period-key>] — [start .. end, UTC]
├── Bugs:     [<median> (p75 <p75>) over N defects — <trend> | low sample (N < 5) — raw values | no data — <reason>]
├── PRs:      [<median> (p75 <p75>) over N merged — <trend> | low sample (N < 5) — raw values | no data — <reason>] (N closed unmerged, N excluded authors)
├── Adoption: [process N% · classification N% · review N% | not available — <which signal, why>]
├── Mapping:  [N defects, N generic, N unmapped — counted as generic]
├── Panel:    [.pair/working/reports/metrics/<period-key>-delivery-metrics.md — created | updated in place | kept (existing panel covers more of the period — no coverage regression) | inline (reports area not writable)]
└── Data:     [ok | partial — Coverage N of M | no data for the period — <reason>]
```

The panel itself (headline-first, D22):

```markdown
# Delivery Metrics — <period-key>

**Bug resolution**: <median> (p75 <p75>) <trend> · **PR lead time**: <median> (p75 <p75>) <trend> · **Adoption**: process N% · classification N% · review N%
**Population**: N defects closed, N PRs merged (<start> .. <end>, UTC) · **Excluded**: N closed unmerged, N excluded authors · **Unmapped**: N counted as generic · **Open at period end**: N defects
**Coverage**: N of M items processed — <reason> — unprocessed: #ID, #ID (omit the whole line when N = M; the unprocessed ids live here and nowhere else — such an item gets no row below and counts in no figure above)
**Inputs**: PM tool <name> + code host <name> · definitions `delivery-metrics.md` @ <revision> · adoption `tech/way-of-working.md` @ <revision> (resolved inputs, not a run timestamp)

_Definitions, clocks and aggregation rules: `.pair/knowledge/guidelines/quality-assurance/delivery-metrics.md` (linked relative to the panel). Figures are medians with p75 beside them, never means; a family under 5 items reads `low sample` and carries no trend._

<details>
<summary>Bug resolution — per defect</summary>

| Issue | Created | Closed | Resolution | Reopened | Mapped by |
| ----- | ------- | ------ | ---------- | -------- | --------- |
| #ID | <ts> | <ts> | <hours> | N | [adoption `bug-label` | tool default | unmapped → generic] |

</details>

<details>
<summary>PR lead time — per PR</summary>

| PR | Opened | Merged | Lead time | Draft share | Author |
| -- | ------ | ------ | --------- | ----------- | ------ |
| #ID | <ts> | <ts> | <hours> | [N% | not exposed] | [human | excluded (bot)] |

</details>

<details>
<summary>Adoption — per signal</summary>

| Signal | Ratio | Numerator / denominator | Source |
| ------ | ----- | ----------------------- | ------ |
| process coverage / classification coverage / review coverage | [N% | not available] | N / N | <tool + field> |

</details>
```

An **empty window** renders the same panel with the headline `no data for the period` plus the reason and no breakdown tables. A window whose items could not all be processed still writes its panel, carrying the `Coverage` line — there is no window size that produces no panel — except where a **more complete** panel for the same period already exists, which is kept instead (Step 7.4).

## Composition Interface

**Standalone**: this skill composes nothing and is composed by nothing. It consumes what other capabilities already produced (tracker items, PR bodies, review checks) and hands back the panel path.

- **Trigger, by design: on demand only** — a human runs it for a retro or a periodic delivery review, and the `next` catalog row is its discovery surface. **Cadence stays the caller's concern** (D18): an automation loop may drive it every period, and nothing here schedules anything.
- **Not a review input.** It is a retro artifact over a window of _merged_ work, not a judgment on one change — `review` never composes it, and no merge decision reads it. A single PR's own risk/cost assessment is `classify`'s and `assess-cost`'s.
- **Non-interactive**: every step continues on the information it has (announcing counts rather than asking), so an unattended run never stalls waiting for an answer. The one stop is Step 3's HALT, and Step 1's request for an intended window when `$period` cannot be parsed.

## Edge Cases

- **Sparse period** (few defects/PRs): the figure is reported with `low sample (N < 5)` and **no trend** — the panel never draws a trend line through three points (Step 6.3).
- **Empty period**: the panel is written, headlined `no data for the period` with the reason — never a silent skip and never a failed run (Step 7.5).
- **PM tool or code host unreachable**: **HALT** with the tool and reason, **nothing written** — no panel, no partial file (Step 3.2).
- **Tracker with no PR surface** (filesystem backlog, no code host): PR-side families read `not available`; the run continues and the panel says which surface was missing (Step 3.3).
- **Unlabeled bug issues**: the adoption-declared mapping applies, else the tool's native defect marker, else the issue is counted as **generic** with the count stated in the panel (Step 5).
- **Reopened issue**: one row, resolution measured to the last close inside the window, reopen count carried on the row (Step 5.3).
- **PR closed without merging**: excluded from lead time and counted as `closed unmerged` in the headline — it never shipped, so it has no lead time (Step 4.1).
- **Large window**: no item cap and no refusal — items are processed one at a time and discarded once their row is retained (Step 4.2).
- **Partial re-run over a more complete panel**: the in-place update is skipped, the existing panel kept, and the shortfall reported in the run output (Step 7.4).
- **Adoption signal source absent** (no PR template, tag projection off, review check unregistered): that ratio reads `not available`, never `0%` (Step 6.1).
- **Reports area not writable**: the panel is presented inline with a save hint; the run succeeds (Step 7.7).

## Graceful Degradation

See [graceful degradation](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/graceful-degradation.md) (adoption file missing → run against KB defaults) for the standard scenarios. Additional cases:

- **delivery-metrics guideline absent** (KB partially installed): **HALT** (Step 0) — the clocks, aggregation and thresholds _are_ the rule set, so a "resolution time" computed without them is a number nobody can compare. Report which file to install.
- **working-area guideline absent**: apply the panel mechanics as summarized in Step 7 (period-keyed filename, in-place update, headline-first, coverage rules) and note the reduced reference — never HALT.
- **No `## Delivery Metrics` adoption section**: run on the per-tool defaults for the bug mapping and the author exclusions, and say so in the panel's provenance line.
- **PM tool unreachable**: HALT with nothing written (Step 3.2) — a panel over the items that happened to be reachable would misreport every median.

## Notes

- **Report-only, one file** — the period panel under `.pair/working/reports/metrics/` (D14 operational artifact). No adoption content, no backlog items, no verdict, no merge authority; the sources are read read-only, including the tracker.
- **The definitions live in the guideline** (D17/D21). Adding a metric family or a tracker is a guideline/adoption change; this skill's steps stay the same (R2.12).
- **Idempotent by period key** — see the [idempotency convention](../../../.pair/knowledge/guidelines/technical-standards/ai-development/skill-conventions/idempotency.md): a re-run for the same period updates that one panel in place, and the same inputs produce the same content.
- **D22** (headline in ~1 screen + collapsed details) is the rendering shape both the run output and the panel honor.
