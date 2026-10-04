---
name: generate-closure-report
description: >
  Generates a project closure report aggregating data from charter, plan-fact
  report, risk register, and lessons learned. Last artifact of the Closing phase.
  Summarizes project outcomes, deviations, realized risks, and lessons.
template: closure-report
output_file: closure-report.md
phase: "6 — Closing"
version: 1.0.0
---

# generate-closure-report

## Triggers

**Russian:** «сформируй отчёт о закрытии», «закрой проект», «подготовь closure report», «отчёт о закрытии проекта»
**English:** "generate closure report", "close project", "project closure report", "prepare closure report"

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with `-ru` suffix
- Otherwise → use templates with `-en` suffix

All output (headings, labels, comments, instructions) must match the detected language.

---

## 1. Input Data

| Data | Required | Source | Notes |
|------|:--------:|--------|-------|
| Project charter | yes | knowledge (`project-charter.md`) | Goal, deliverables, team, sponsor, budget, timeline |
| Plan-fact report | yes | knowledge (`plan-fact-report.md`) | Deviation summary, actual dates/budget/scope. If multiple files — use the latest by date |
| Lessons learned | yes | chat | User provides in any format: retrospective results, questionnaire answers, free text. Agent structures and assigns categories |
| Risk register | no | knowledge (`risk-register.md`) | For section 4. If unavailable — agent asks the user about realized risks |
| Open items | no | chat | Tasks/questions remaining after closure. If not provided — replace section with "All items closed" |
| Lessons source | no | chat | `team retrospective` / `questionnaire` / `PM input in chat`. Default: `PM input in chat` |

If required data is missing — request it (system-prompt-draft.md §3.2):

```
To generate the project closure report, the following is needed:
1. Project charter (project-charter.md) — in knowledge or paste in chat.
2. Plan-fact report (plan-fact-report.md) — in knowledge or paste in chat.
3. Project lessons — in any format:
   — team retrospective results;
   — questionnaire answers;
   — free-form description: what went well, what went wrong, what to do differently.
Available data: [list what is present].
Missing: [specify].
```

---

## 2. Execution Algorithm

1. **Verify input data.** Check for minimum: charter, plan-fact report, lessons from user. Missing → request using the template from §1. Do NOT generate a stub report, template, or example — respond ONLY with a data request. Present → step 2.
2. **Structure lessons.** If data is free-form — categorize into: Processes, Technologies, Communications, Resources, Risks. For each lesson — formulate a recommendation. Count: 1 to 5, only those supported by data. Do not pad artificially.
3. **Check data for contradictions.** If charter data conflicts with plan-fact report (e.g., different planned dates or budget) — do NOT choose independently. List the discrepancies, ask which data is current. Exception: if the user explicitly corrects in chat — use the correction.
4. **Read the template** `closure-report` from project knowledge. Select the file with the appropriate language suffix based on Language Detection.
5. **Fill section 1** (general information): planned data from charter, actual data from plan-fact report (summary).
6. **Fill section 2** (project results): list of deliverables from charter (section 2, "Project Result"). Actual status from plan-fact report (scope data) or from user. Split into "Delivered" / "Not delivered / deferred". For each incomplete deliverable — state the reason. If reason not provided — use `[clarify]`.
7. **Fill section 3** (plan-fact deviations): copy the summary table from plan-fact-report.md (section 1). Data: plan, actual, deviation — without recalculation. Rephrase the "Comment" column in a closing tone (1 sentence per metric). At the bottom — reference: "Details — in `plan-fact-report.md`."
8. **Fill section 4** (realized risks):
   - If `risk-register.md` is available → extract risks with status "realized" or mentioned in user data. Verify: each risk in section 4 must have an ID from the register.
   - If `risk-register.md` is unavailable → use data from user. If user did not specify realized risks — ask: "Which planned risks were realized? If none — I will note 'No realized risks'."
   - If no risks occurred → replace the table with: "No realized risks".
9. **Fill section 5** (lessons learned): 1 to 5 lessons, structured in step 2. Category from the reference in §3.
10. **Fill section 6** (open items) and section 7 (closure approval):
    - Section 6: if user provided open items → fill in. If not → replace the table with: "All items closed".
    - Section 7: names from charter (Sponsor, PM). Dates — empty.
11. **Verify the result** against the checklist (section 5 of this spec). Present the result in chat. Format (system-prompt-draft.md §3.4):
    - What was done: "Generated project closure report based on [list sources]".
    - Assumptions: list all (if any).
    - Key outcomes: 1–3 lines — main results (delivered X of Y, budget, timeline).
    - Required: "Approve, provide comments, or reject".
    - Do not show system file paths. Use name only: "Report saved as closure-report.md".
12. **Wait for user response** (system-prompt-draft.md §3.5).
    - Approval → produce the final text.
    - Comments → revise, show updated version. After the 3rd iteration — ask: "Continue revising or finalize the current version?"
    - **After approval:**
      - Offer the user text to insert into log.md and project-state.md (system-prompt-draft.md §11).
      - State: "Closure report approved. Project completed." This is the final skill in the MVP chain — no subsequent tasks.

---

## 3. Section Fill Rules

### Section 1. General Information

- Project goal — from charter (section 1). Copy as-is, do not rephrase.
- Sponsor — from charter (section 5 or header).
- Start and end dates (planned) — from charter (section 3).
- End date (actual) — from plan-fact report (last actual date) or from user. If project closes early — state the actual date with a note.
- Budget (planned) — from charter (section 4). Budget (actual) — from plan-fact report (summary).

### Section 2. Project Results

- **Delivered:** each deliverable from charter (section 2, "Included") that is complete. Format: `deliverable — brief result description`.
- **Not delivered / deferred:** deliverables that are incomplete or deferred. Format: `deliverable — reason: [explanation]`. If reason not provided by user — `[clarify]`.
- Status source: plan-fact report (scope data) > user data in chat.
- If a deliverable is partially complete — list under "Delivered" with a "partial" note and description of what was excluded.

### Section 3. Plan-Fact Deviations

- **Direct transfer** of the summary table from plan-fact-report.md (section 1, 3 rows: timeline, budget, scope). Do not recalculate data.
- "Comment" column — rephrase from plan-fact report in a closing tone. One sentence per metric. Example: "Delay +1 week due to Safari hotfix" → "Project completed with a +1 week delay; root cause — Safari incident during launch phase".
- If budget was absent in plan-fact report — replace the budget row with "Budget — data unavailable".
- Below the table — in italics: *Details — in `plan-fact-report.md`.*

### Section 4. Realized Risks

**Conditional section.**

- If risks were realized — table with columns: ID, Risk, Project Impact, Response Result.
- **ID** — from risk-register.md (if available). If register unavailable — leave empty or assign R1, R2, ...
- **Project Impact** — specific: what happened, what consequences (delay, overrun, scope change).
- **Response Result** — what was done: did the response plan work, what actions were taken.
- If no risks occurred → replace the table with: "No realized risks".
- Do not include risks that were in the register but did not materialize.

### Section 5. Lessons Learned

- 1 to 5 lessons. Count is determined by user data — do not pad artificially.
- Columns: #, Lesson, Category, Recommendation.
- **Category** — from reference: `Processes` / `Technologies` / `Communications` / `Resources` / `Risks`.
- **Lesson** — a fact or observation. Wording: what happened and why it matters.
- **Recommendation** — a concrete action for future projects. Not an abstraction.
- If user provided lessons without categories — agent assigns based on content.

### Section 6. Open Items and Handover

**Conditional section.**

- If open items exist — table: #, Item/Task, Owner, Deadline.
- Owner — from user data. If not specified — `[clarify]`.
- Deadline — specific date (YYYY-MM-DD). If not specified — `[clarify]`.
- If no open items → replace the table with: "All items closed".

### Section 7. Closure Approval

- Sponsor and PM — from charter (section 5). Date — empty (filled upon approval).

### Header Metadata

- `Version`: 1.0
- `Date`: current generation date.
- `File`: `closure-report.md`
- `Document status`: `draft` (on generation). After approval — `approved`.
- `Project manager`: from charter.
- `Lessons source`: from input data. Default: `PM input in chat`.

---

## 4. Placeholder Table

> Placeholders `{{}}` in the template are fill guides, not auto-substitution variables. Replace each with the corresponding value from input data.

| Placeholder | Required | Source | Allowed Values |
|-------------|:--------:|--------|----------------|
| `{{project_name}}` | yes | charter | text |
| `{{date}}` | yes | system | YYYY-MM-DD |
| `{{pm_name}}` | yes | charter | name |
| `{{lessons_source}}` | yes | chat (default: `PM input in chat`) | `team retrospective` / `questionnaire` / `PM input in chat` |
| `{{project_goal}}` | yes | charter (section 1) | text |
| `{{sponsor_name}}` | yes | charter | name |
| `{{planned_start}}` | yes | charter (section 3) | YYYY-MM-DD |
| `{{planned_end}}` | yes | charter (section 3) | YYYY-MM-DD |
| `{{actual_end}}` | yes | plan-fact report / chat | YYYY-MM-DD |
| `{{planned_budget}}` | no | charter (section 4) | number + currency |
| `{{actual_budget}}` | no | plan-fact report | number + currency |
| `{{deliverable_N}}` | yes (≥1) | charter (section 2) | deliverable name |
| `{{status_N}}` | yes | plan-fact report / chat | brief result description |
| `{{excluded_N}}` | no | charter / plan-fact report | undelivered deliverable name |
| `{{reason_N}}` | no | chat / plan-fact report | reason or `[clarify]` |
| `{{planned_duration}}` | yes | plan-fact report (summary) | number + unit |
| `{{actual_duration}}` | yes | plan-fact report (summary) | number + unit |
| `{{delta_time}}` | yes | plan-fact report (summary) | text (e.g., "+1 week (+8%)") |
| `{{comment_time}}` | yes | agent (based on plan-fact report) | closing comment, 1 sentence |
| `{{delta_budget}}` | no | plan-fact report (summary) | text (e.g., "-$3,600 (-4.5%)") |
| `{{comment_budget}}` | no | agent (based on plan-fact report) | closing comment, 1 sentence |
| `{{planned_scope}}` | yes | plan-fact report (summary) | number + unit (deliverables) |
| `{{actual_scope}}` | yes | plan-fact report (summary) | number + unit |
| `{{delta_scope}}` | yes | plan-fact report (summary) | text (e.g., "-1 deliverable") |
| `{{comment_scope}}` | yes | agent (based on plan-fact report) | closing comment, 1 sentence |
| `{{risk_id}}` | no | risk-register / agent | ID (e.g., R001) or empty |
| `{{risk_description}}` | no | risk-register / chat | risk description |
| `{{impact}}` | no | chat / agent | specific project impact |
| `{{response_result}}` | no | chat / agent | response result |
| `{{lesson_N}}` | yes (≥1) | chat (structured by agent) | text — fact/observation |
| `{{category_N}}` | yes | agent | `Processes` / `Technologies` / `Communications` / `Resources` / `Risks` |
| `{{recommendation_N}}` | yes | agent | concrete action |
| `{{open_item_N}}` | no | chat | question or task |
| `{{owner_N}}` | no | chat | owner or `[clarify]` |
| `{{deadline_N}}` | no | chat | YYYY-MM-DD or `[clarify]` |

---

## 5. Validation Checklist

Before presenting the result to the user — verify:

- [ ] All required placeholders replaced with values
- [ ] No `{{}}` placeholders remain in text (except removed optional rows)
- [ ] Section 1: planned data matches charter, actual data matches plan-fact report
- [ ] Section 2: all deliverables from charter listed (delivered + undelivered)
- [ ] Section 2: each undelivered deliverable has a reason (or `[clarify]`)
- [ ] Section 3: data matches plan-fact report summary (no recalculation)
- [ ] Section 3: reference to `plan-fact-report.md` present
- [ ] Section 4: if conditional — correctly filled or replaced with "No realized risks"
- [ ] Section 5: 1 to 5 lessons, each with category and recommendation
- [ ] Section 6: if conditional — correctly filled or replaced with "All items closed"
- [ ] All agent assumptions listed when presenting result
- [ ] Document status = `draft`
- [ ] File: `closure-report.md` stated in header

---

## 6. Dependencies

**Consumes (input):**
- `project-charter.md` — from skill `generate-charter` (goal, deliverables, team, budget, timeline)
- `plan-fact-report.md` — from skill `generate-plan-fact-report` (deviation summary, actual data)
- `risk-register.md` — from skill `generate-risk-register` (optional, for realized risks)
- Lessons and open items — from user (via chat)

**Produces (output):** project closure report — the final artifact. Not consumed by other MVP skills.

In Product 1: additionally consumes data from `generate-questionnaire` (team lessons via questionnaire).

After report approval, user should upload `closure-report.md` to project knowledge for archival.

---

## 7. Example Invocation

**User command:**

> Generate the project closure report. Charter and plan-fact report are in knowledge. Risk register too.
> Lessons:
> — Underestimated DB filter complexity, lost a week. Need to budget buffer for unknown tasks.
> — Formalized change request saved us from scope creep — CEO wanted to add Intercom, but impact assessment stopped it.
> — Safari testing was done only before release — needs to happen earlier.
> Open items:
> — Email integration assigned to Dmitry, deadline July 31.
> — Pricing — on me, by August 1.

**Agent response (after generation):**

> Generated project closure report for "ClientBoard" based on: charter, plan-fact report, risk register, lessons from chat.
>
> Assumptions:
> - Lessons source: PM input in chat.
> - Realized risks identified based on risk-register.md and PM data.
>
> Key outcomes:
> - Delivered 4 of 5 deliverables (email integration deferred).
> - Budget: $76,400 of $80,000 (4.5% savings).
> - Timeline: +1 week (13 instead of 12).
>
> Required: approve, provide comments, or reject.
>
> [report text]

---

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-26 | 1.0 | Skill created. Aggregation from charter + plan-fact report + lessons. Conditional sections 4/6. 1 to 5 lessons |
