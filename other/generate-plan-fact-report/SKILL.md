---
name: generate-plan-fact-report
description: >
  Generates a plan-vs-actual report comparing planned and actual project data
  across three dimensions: timelines, budget, and scope (deliverables).
  Part of the Closing phase. Output feeds into generate-closure-report.
  Format: .md, manual data input via chat.
trigger: >
  Triggers RU: «сформируй план-факт», «подготовь отчёт план/факт», «сравни план и факт».
  Triggers EN: "generate plan-fact report", "plan vs actual", "variance report".
output_file: plan-fact-report.md
phase: "6 — Closing"
version: 1.0.0
---

# generate-plan-fact-report

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with `-ru` suffix
- Otherwise → use templates with `-en` suffix

All output (headings, labels, comments, instructions) must match the detected language.

## Triggers

**Russian:** «сформируй план-факт», «подготовь отчёт план/факт», «сравни план и факт»
**English:** "generate plan-fact report", "plan vs actual", "variance report"

## 1. Input Data

| Data | Required | Source | Notes |
|------|:--------:|--------|-------|
| Project plan | yes | knowledge (`project-plan.md`) | Milestones, timelines, budget. If budget is missing — Section 3 is not generated |
| Actual data | yes | chat | User provides: actual milestone completion dates, actual costs by budget line, deliverable status. Free-form — agent structures it |
| Project charter | no | knowledge (`project-charter.md`) | For deliverables list (Section 1, scope). If unavailable — request the list from the user |
| Report type | no | chat | `interim` (default) or `final`. Affects header label only — logic is identical |

If required data is missing — request it:

```
To generate the plan-vs-actual report, the following are needed:
1. Project plan (project-plan.md) — in knowledge or paste into chat.
2. Actual data — in any format:
   — milestone completion dates (completed, not completed, actual date);
   — actual costs by budget line;
   — which deliverables have been delivered and which have not.
Available: [list what is present].
Missing: [specify].
```

---

## 2. Execution Algorithm

1. **Check input data.** Verify project plan and actual data are present. Missing → request using the template in §1. Do NOT generate a placeholder report. Present → proceed to step 2.
2. **Structure actual data.** If free-form — organize across three dimensions: timelines (milestone dates), budget (costs by line), scope (deliverables). Note ambiguities and clarify with the user.
3. **Check for data conflicts.** If plan data in chat conflicts with `project-plan.md` — do NOT resolve independently. List the conflicts and ask which data is current. Exception: if the user explicitly corrects the plan in chat — apply the correction.
4. **Determine report period.** From actual data: project start → date of last recorded fact. If the user specified a period explicitly — use it.
5. **Read the template** `plan-fact-report-ru.md` or `plan-fact-report-en.md` from project knowledge (based on detected language).
6. **Extract planned data** from `project-plan.md`: milestones with dates, budget lines with amounts, deliverables list.
7. **Compare plan vs. actual.** For each row: calculate variance (absolute and %), assign status per §3 reference table.
8. **Fill template sections** per Section 3 rules.
9. **Evaluate whether Section 4 is needed.** Check statuses for all three dimensions independently: Timelines, Budget, Scope. Scope is a full dimension equal to timelines and budget. If at least one of the three has status `attention` or `critical` (including scope with incomplete deliverables) → fill Section 4. Only if all three are `on track` → remove Section 4 entirely.
10. **Validate the result** using the checklist in Section 5.
11. **Present the result in chat:**
    - What was done: "Plan-vs-actual report generated for period [dates] based on [list sources]."
    - Assumptions: list all (if any).
    - Key variances: brief (1–3 lines) — main discrepancies and their statuses.
    - Required action: "Approve, revise, or reject."
    - Do not include internal file paths. Filename only: "Report saved as plan-fact-report.md."
12. **Wait for user response.**
    - Approval → finalize the document.
    - Revisions → revise and present updated version. After the 3rd iteration — ask: "Continue revising or lock current version?"
13. **After approval:**
    - Offer the user text for `log.md` and `project-state.md`.
    - Always notify, regardless of report type and variance statuses: "Plan-vs-actual report approved. Next task available: generate-closure-report (project closure report). Start?"

---

## 3. Section Fill Rules

### Reference: Variance Status Calculation

Applied to each parameter in Section 1 (summary) and to rows in Sections 2–3.

| Variance, % (absolute value) | Status |
|------------------------------|--------|
| ≤ 10% | `on track` |
| 11–25% | `attention` |
| > 25% | `critical` |

Sign convention: positive = overrun / delay / shortfall; negative = savings / ahead of schedule / surplus.

### Section 1. Summary

Three rows — aggregated variances across three dimensions.

- **Timelines:** Plan — total project duration (working days or calendar days). Actual — actual duration as of report date. If project is not complete — show actual duration with note "project not complete."
- **Budget:** Plan — total from `project-plan.md` (or `project-charter.md`). Actual — sum of actual costs. Currency from input data.
- **Scope:** Unit — **number of deliverables** from project charter (`project-charter.md`, Section 2 "Project Deliverables"). Plan — total count. Actual — delivered count. If charter unavailable — request the deliverables list from the user.

For each row: calculate absolute variance, variance %, status per reference table.

**Summary commentary** — required text block after the table. 1–2 sentences per dimension: nature of variance and its cause. If status is `on track` — state the fact without detailed analysis.

### Section 2. Timelines

Row-by-row comparison of milestones from `project-plan.md`.

- Include **all** milestones from the plan — not only completed ones.
- If a milestone is not complete — enter `not complete` in "Actual Date." Variance — dash.
- Variance in days: `actual_date - planned_date`. Positive = delay, negative = ahead of schedule.
- "Variance reason" — fill from user-provided actual data. If reason not stated — enter `[clarify]`.

### Section 3. Budget

Row-by-row comparison of cost lines from `project-plan.md` (or `project-charter.md`).

- Include **all** cost lines from the plan. If no actual data for a line — actual = 0, note "data not provided" in comment.
- Last row — **Total**: sum of all rows. Verify: total actual = sum of actual rows.
- If a cash flow plan (breakdown by period) is unavailable — use linear distribution of budget over project duration, note `estimated` in comment. State as assumption.
- Currency — uniform across the entire report, from input data.

**If budget is missing** from the project plan and charter — Section 3 is not generated. Replace with note: "Budget section not included: planned budget data unavailable." In the summary (Section 1), replace the budget row with: "Budget — data unavailable."

### Section 4. Recommendations / Next Steps

**Conditional section.** Generate only if at least one of the three dimensions (Timelines, Budget, Scope) has status `attention` or `critical`. Scope is an independent dimension — its `critical`/`attention` status triggers Section 4 independently, even if timelines and budget are on track. If all three are `on track` — remove Section 4 entirely.

- For each variance with status `attention` or `critical` — formulate a recommended action.
- Specify the owner (from project data) and deadline (if determinable from context). If not — `[clarify]`.
- Minimum 1 recommendation per `critical` variance.

### Header Metadata

- `Version`: 1.0
- `Date`: current generation date
- `File`: `plan-fact-report.md`
- `Document status`: `draft` (at generation). After approval — `approved`.
- `Period`: `{{start_date}} — {{end_date}}`
- `Report type`: `interim` or `final` (from input; default `interim`)
- `Planned data source`: filename (e.g. `project-plan.md`)
- `Actual data source`: source description (e.g. "PM data provided in chat")

---

## 4. Placeholder Reference

> Placeholders `{{}}` in the template are fill targets, not auto-substitution variables. Replace each with the corresponding value from input data.

| Placeholder | Required | Source | Allowed Values |
|-------------|:--------:|--------|----------------|
| `{{project_name}}` | yes | plan / charter | text |
| `{{date}}` | yes | system | YYYY-MM-DD |
| `{{start_date}}` | yes | plan / chat | YYYY-MM-DD |
| `{{end_date}}` | yes | chat | YYYY-MM-DD |
| `{{report_type}}` | yes | chat (default: interim) | `interim` / `final` |
| `{{source_plan}}` | yes | context | filename of planned data source |
| `{{source_fact}}` | yes | context | description of actual data source |
| `{{planned_duration}}` | yes | plan | number + unit (days / working days) |
| `{{actual_duration}}` | yes | actual | number + unit |
| `{{delta_time}}` | yes | calculated | signed number |
| `{{delta_time_pct}}` | yes | calculated | signed % |
| `{{status_time}}` | yes | calculated | `on track` / `attention` / `critical` |
| `{{currency}}` | yes | plan / chat | currency symbol (₽, $, €) |
| `{{planned_budget}}` | no | plan | number |
| `{{actual_budget}}` | no | actual | number |
| `{{delta_budget}}` | no | calculated | signed number |
| `{{delta_budget_pct}}` | no | calculated | signed % |
| `{{status_budget}}` | no | calculated | `on track` / `attention` / `critical` |
| `{{planned_scope}}` | yes | charter / plan | number (deliverable count) |
| `{{delivered_scope}}` | yes | actual | number (delivered count) |
| `{{delta_scope}}` | yes | calculated | signed number |
| `{{delta_scope_pct}}` | yes | calculated | signed % |
| `{{status_scope}}` | yes | calculated | `on track` / `attention` / `critical` |
| `{{milestone_name}}` | yes (≥1) | plan | milestone name |
| `{{planned_date}}` | yes | plan | YYYY-MM-DD |
| `{{actual_date}}` | no | actual | YYYY-MM-DD or `not complete` |
| `{{delta_days}}` | no | calculated | signed day count or dash |
| `{{reason}}` | no | actual / agent | text or `[clarify]` |
| `{{cost_item}}` | no | plan | cost line name |
| `{{planned_cost}}` | no | plan | number |
| `{{actual_cost}}` | no | actual | number |
| `{{delta}}` | no | calculated | signed number |
| `{{delta_pct}}` | no | calculated | signed % |
| `{{comment}}` | no | actual / agent | text |
| `{{total_plan}}` | no | calculated | sum of planned rows |
| `{{total_fact}}` | no | calculated | sum of actual rows |
| `{{total_delta}}` | no | calculated | difference of totals |
| `{{total_delta_pct}}` | no | calculated | % variance of total |
| `{{issue_N}}` | no | agent | issue / observation description |
| `{{action_N}}` | no | agent | recommended action |
| `{{owner_N}}` | no | project data | owner or `[clarify]` |
| `{{deadline_N}}` | no | agent | deadline or `[clarify]` |

---

## 5. Validation Checklist

Before presenting the result to the user — verify:

- [ ] All required placeholders replaced with values
- [ ] No `{{}}` placeholders remaining in the text (except removed optional rows)
- [ ] Report period is valid: start_date < end_date
- [ ] Section 1 (summary) contains exactly 3 rows: timelines, budget, scope (if budget missing — 2 rows + note)
- [ ] Variance statuses calculated per §3 reference table (≤10% / 11–25% / >25%)
- [ ] Section 2: all milestones from the plan included (not only completed)
- [ ] Section 2: incomplete milestones show "not complete," variance is a dash
- [ ] Section 3: total = sum of rows (verify arithmetic)
- [ ] Section 3: if budget missing — section replaced with note
- [ ] Section 4: present if any `attention`/`critical` variances; absent if all `on track`
- [ ] All agent assumptions listed when presenting the result
- [ ] Document status = `draft`
- [ ] File: `plan-fact-report.md` stated in header

---

## 6. Dependencies

**Consumes (input):**
- `project-plan.md` — from skill `generate-project-plan` (milestones, budget, timelines)
- `project-charter.md` — from skill `generate-charter` (deliverables for scope metric)
- Actual data — from the user (via chat)

**Produces (output):** plan-vs-actual report → consumed by:
- `generate-closure-report` — Phase 6, Closing

After approval, the user must upload `plan-fact-report.md` to project knowledge so it is available for `generate-closure-report`.

---

## 7. Usage Example

**User command:**

> Generate a plan-vs-actual report. Project plan is in knowledge. Actual data:
> — M1 (Go/No-Go): completed 11.04, on time.
> — M2 (Plan approved): completed 25.04, on time.
> — M3 (Prototype): completed 12.05, 3-day delay — design approval.
> — M4 (Development): not complete.
> — Budget: AWS — $10,400 (planned $8,000), design — $10,000 (on plan), rest on plan.
> — Deliverables: 3 of 5 delivered.

**Agent response (after generation):**

> Plan-vs-actual report generated for period 07.04.2026 — 12.05.2026 based on: project-plan.md (knowledge), actual data from chat.
>
> Assumptions:
> - Budget lines without explicit data: actual = planned.
> - Duration: actual — 35 days (from start to report date), planned — 63 days (full project). Project not complete.
>
> Key variances:
> - Scope: 3/5 deliverables (−40%) — status `critical`.
> - AWS budget: +$2,400 (+30%) — status `critical`.
>
> Required: approve, revise, or reject.
>
> [report text]

---

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-27 | 1.1 | §2 step 9: scope is an independent trigger for Section 4 (all three dimensions listed explicitly); §2 step 13: generate-closure-report offer is mandatory regardless of statuses; §3 Section 4: clarified that scope independently activates the section |
| 2026-03-26 | 1.0 | Skill created. Output format .md. Status calculation rules, conditional Section 4, scope metric — deliverables |
