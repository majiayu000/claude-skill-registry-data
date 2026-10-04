---
name: generate-project-plan
description: >
  Generates a project plan from the approved charter, scope, and optional
  duration/resource estimates. The plan is the first artifact of the Planning
  phase. Once approved, it unlocks: generate-risk-register (mode: detailed)
  and generate-comm-plan (can run in parallel). Accepts both structured
  estimates and free-form descriptions.
trigger: >
  Command: user asks to create a project plan.
  Context: charter is approved — agent proposes to run.
  Key phrases (RU): «сформируй план проекта», «подготовь план», «составь project plan», «нужен план проекта».
  Keywords (EN): "generate project plan", "create project plan", "build plan", "prepare project plan".
template: project-plan-ru.md
output_file: project-plan.md
phase: "2 — Planning"
version: 1.0.0
---

# generate-project-plan

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with `-ru` suffix
- Otherwise → use templates with `-en` suffix

All output (headings, labels, comments, instructions) must match the detected language.

## Triggers

**Russian:** «сформируй план проекта», «подготовь план», «составь project plan», «нужен план проекта»
**English:** "generate project plan", "create project plan", "build plan", "prepare project plan"

---

## 1. Inputs

| Data | Required | Source | Notes |
|------|:--------:|--------|-------|
| Project charter (project-charter.md) | yes | knowledge or chat | Approved charter. Extract: goal, scope, dates, budget (if present), team, constraints, top-3 risks |
| Duration estimates | no | chat or knowledge | Work package estimates from the user. If absent — agent estimates and marks as assumption |
| Team availability data | no | chat or knowledge | Load by period, constraints (vacations, part-time). If absent — agent distributes evenly, marks as assumption |
| Additional inputs | no | chat | Priorities, external dependencies, technical constraints not included in the charter |

If no charter is available — request it (system-prompt-draft.md §3 p.2):

```
A project plan requires an approved charter (project-charter.md).
Available data: [list what is available].
Charter status: [not started / draft / approved].
If the charter has not been created yet — start with generate-charter.
```

---

## 2. Execution Algorithm

1. **Validate inputs.** Check for an approved charter. Not found → request per §1 template. Do NOT generate a plan without a charter — this breaks the dependency chain. Found → step 2.
2. **Extract data from the charter.** Break down by category: goal, scope (included/excluded), dates (start/end), budget (if specified), team, constraints, risks. Record gaps.
3. **Check data for conflicts.** If charter dates conflict with user-provided duration estimates — do NOT resolve independently. List discrepancies, ask which takes precedence. Exception: if the user explicitly clarifies in chat — use the clarification.
4. **Decompose scope into work packages (WP).** Each deliverable from the charter's "Included" section → one or more WPs. Granularity: a WP is a group of related tasks with a single output. Do NOT decompose to individual tasks — that is Jira level. Assign each WP an ID (WP-001, WP-002, etc.). Group WPs by project phase. After decomposition, count total WPs: if >20 — consolidate adjacent packages within the same phase. WP count must be ≤ 20 for MVP. If consolidation would lose meaning — record as assumption and proceed to step 5.
5. **Set duration for each WP.**
   - Use user-provided estimates if available.
   - If no estimates — assess based on: scope volume, resource count, comparable projects, charter constraints. Mark each such estimate as assumption.
   - Unit: project ≤ 3 months → working days (wd); project > 3 months → weeks (wk). Unit must be consistent within one plan. 1 wk = 5 wd.
   - Verify: sum of critical path durations (accounting for maximum parallelism) ≤ total project duration from charter. If it doesn't fit — record as issue, propose options (parallel execution / scope reduction / resource increase / date shift). Do NOT generate WP dates beyond the charter end_date. If unavoidable — mark affected WPs with `[⚠ exceeds deadline]` and require a decision from the user before finalizing.
6. **Identify dependencies between WPs.** For each related WP pair: dependency type (FS / SS / FF). FS is the default if the relationship is not explicit. Verify no circular dependencies.
7. **Define milestones.** A milestone is a checkpoint marking the achievement of a significant result. A milestone is NOT a task — it has zero duration. It answers "what must be done by this point", not "what needs to be done". What counts as a milestone: phase completion (all WPs in phase closed); delivery of a key deliverable to the customer; external event the project depends on (approval, procurement, integration); go/no-go decision point. What does NOT count as a milestone: completion of a routine WP that is not a deliverable; internal intermediate results without external review; recurring events (weekly status, sprint reviews). Milestones from the charter (section 3) — must be included. ID: M1, M2, etc. Minimum: 3 milestones (start, mid, finish). Maximum: one per phase + key deliverables.
8. **Fill the resource map.**
   - Use availability data if provided.
   - If not — take team from charter (section 5), distribute across WPs by role, treat load as uniform. Mark as assumption.
   - Period columns — actual project months (not fixed).
9. **Read the template** `project-plan-ru.md` (or `project-plan-en.md`) from project knowledge.
10. **Fill the template** per the rules in section 3.
11. **Validate the output** using the checklist (section 5).
12. **Present the output in chat.** Format (system-prompt-draft.md §3 p.4):
    - What was done: "Project plan generated based on [list sources]."
    - Assumptions: list all (duration estimates, resource allocation, etc.).
    - Issues: if found (schedule overrun, insufficient resources).
    - What is required: "Approve, provide comments, or reject."
    - Do not include system paths. Use file name only: "Plan saved as project-plan.md."
13. **Wait for user response** (system-prompt-draft.md §3 p.5).
    - Approval → generate final version.
    - Comments → revise, show updated version. After 3rd iteration — ask: "Continue revising or finalize the current version?"
14. **After approval:**
    - Propose text for the user to insert into log.md and project-state.md (system-prompt-draft.md §11).
    - Notify: "Project plan approved. The following tasks are now available (can run in parallel): generate-risk-register (detailed risk register) and generate-comm-plan (communications plan). Which one to start?" (system-prompt-draft.md §7).

---

## 3. Section Fill Rules

### Header Metadata
- `Version`: 1.0
- `Date`: current generation date.
- `File`: `project-plan.md`
- `Document status`: `draft` (on generation). After approval — `approved`.
- `Source`: list documents used to generate the plan.

### "Project Summary" Section
- Fill from the charter. Fields `Project goal`, `Dates`, `Team`, `Customer`, `PM` — required.
- `Project goal` — from charter section 1 (verbatim or condensed).
- `Dates` — start_date and end_date from charter; duration — calculate.
- `Budget` — from charter section 4 (total amount). If not specified — enter: "not defined". The plan is generated without budget data. This does not block generation.
- `Team` — headcount from charter section 5.
- `Customer` and `PM` — from charter sections 5/8.

### "Phases and Work Packages" Section
Table is the core of the plan.

| Column | Rule |
|--------|------|
| ID | Unique code: WP-001, WP-002, etc. Sequential numbering |
| Phase | Phase name (Initiation, Planning, Development, etc.). Group WPs by phase |
| Work package | Group of related tasks with a single output. NOT an individual task — task-level detail belongs in Jira |
| Owner | Role or name from charter team |
| Duration | Unit selected by project duration: ≤ 3 months → working days (wd); > 3 months → weeks (wk). Consistent unit throughout the plan. Use suffix: "5 wd" or "2 wk". Calculation: 1 wk = 5 wd |
| Start / End | YYYY-MM-DD. Calculate from dependencies and duration. First WP start ≥ charter start_date. Last WP end ≤ charter end_date |
| Dependencies | IDs of predecessor work packages. "—" if none |

- Minimum WPs: one per deliverable from the charter.
- Maximum WPs: no more than 20 for MVP. Consolidate if exceeded.

### "Milestones" Section

| Column | Rule |
|--------|------|
| ID | M1, M2, etc. |
| Milestone | Checkpoint — event marking the achievement of a significant result. Zero duration |
| Date | YYYY-MM-DD. Matches the end date of the corresponding WP or phase |
| Completion criterion | Specific, verifiable condition. Format: "[artifact/result] [action] [by whom]". Example: "Prototype accepted by customer", "API deployed to staging and passed smoke tests" |
| Status | On generation: `not achieved`. Allowed values: `not achieved` / `achieved` / `overdue` |

### "Dependencies" Section
Table details the relationships from the WP table's Dependencies column.

| Column | Rule |
|--------|------|
| Source block | ID of WP that must finish/start |
| Target block | ID of WP that depends on the source |
| Type | FS (Finish-to-Start) — default; SS (Start-to-Start); FF (Finish-to-Finish) |
| Comment | Explanation of the relationship. Required for SS and FF types |

- Verify: no circular dependencies (A→B→C→A).
- Every dependency from the WP table must appear here.

### "Assumptions and Constraints" Section
- **Assumptions:** all agent assumptions (duration estimates, resource allocation, priorities). One item per line.
- **Constraints:** from charter (section 6) + identified during planning.

### "Resource Map" Section

| Column | Rule |
|--------|------|
| Team member | Name from team roster |
| Role | Role from charter |
| Period columns | Project months (adapt to actual dates). Load in % of full working time |
| Constraints / Notes | Vacations, part-time, outsourcing, dual roles |

- Use provided load data if available.
- If not — distribute evenly across WPs, mark as assumption.
- Total load per person per period must not exceed 100% (record as issue if exceeded).

---

## 4. Placeholder Table

> Placeholders `{{}}` in the template are fill-in guides, not auto-substitution variables. Replace each with the corresponding value from the inputs.

| Placeholder | Required | Source | Allowed values |
|-------------|:--------:|--------|----------------|
| `{{project_name}}` | yes | charter | text |
| `{{version}}` | yes | agent | "1.0" on creation |
| `{{date}}` | yes | system | YYYY-MM-DD |
| `{{doc_status}}` | yes | agent | draft / pending approval / approved / revision |
| `{{source_docs}}` | yes | agent | list of input documents |
| `{{project_goal}}` | yes | charter, section 1 | text |
| `{{start_date}}` | yes | charter, section 3 | YYYY-MM-DD |
| `{{end_date}}` | yes | charter, section 3 | YYYY-MM-DD |
| `{{duration}}` | yes | agent (calculate) | "N weeks" or "N months" |
| `{{budget}}` | no | charter, section 4 | number + currency or "not defined" |
| `{{team_size}}` | yes | charter, section 5 | number |
| `{{customer}}` | yes | charter, sections 5/8 | name |
| `{{pm}}` | yes | charter, sections 5/8 | name |
| `{{phase_name}}` | yes (≥1) | agent | project phase name |
| `{{work_package}}` | yes (≥1) | agent / scope | work package description |
| `{{owner}}` | yes | charter / team | role or name |
| `{{wp_duration}}` | yes | user / assumption | number + "wd" or "wk" |
| `{{wp_start}}` | yes | agent (calculate) | YYYY-MM-DD |
| `{{wp_end}}` | yes | agent (calculate) | YYYY-MM-DD |
| `{{wp_dependency}}` | no | agent | WP ID or "—" |
| `{{milestone_name}}` | yes (≥3) | charter + agent | milestone name |
| `{{done_criteria}}` | yes | agent | completion condition: "[result] [action] [by whom]" |
| `{{assumption_N}}` | no | agent | assumption text |
| `{{constraint_N}}` | yes (≥1) | charter | constraint text |
| `{{name_N}}` | no | charter / team | team member name |
| `{{role_N}}` | no | charter / team | role |
| `{{load_period}}` | no | data / assumption | number (% load) |

---

## 5. Validation Checklist

Before presenting the output to the user — verify:

- [ ] Charter used as primary source (no fabricated data)
- [ ] All required placeholders replaced with values
- [ ] No `{{}}` placeholders remain in the text
- [ ] Every deliverable from the charter is covered by at least one WP
- [ ] Dates are consistent: start_date ≤ WP dates ≤ end_date
- [ ] No circular dependencies between WPs
- [ ] Charter milestones included; milestone dates match the end of corresponding WPs/phases
- [ ] Each milestone meets the criteria from §2 p.7: marks phase completion, deliverable handoff, external event, or go/no-go. No "false milestones" (routine WP completion, recurring events)
- [ ] Completion criterion for each milestone is specific and verifiable (contains artifact/result + action + by whom)
- [ ] Sum of durations (accounting for parallelism) ≤ total project duration. If not — recorded as issue
- [ ] Duration unit is consistent throughout the plan (wd or wk) and follows the rule: ≤ 3 months → wd, > 3 months → wk
- [ ] Each resource load ≤ 100% per period (or issue is recorded)
- [ ] All agent assumptions listed in the Assumptions section
- [ ] Document status = `draft`
- [ ] File: `project-plan.md` listed in the header

---

## 6. Dependencies

**Consumes (input):**
- `project-charter.md` (approved) — from skill `generate-charter`
- Optional: duration estimates and team availability data from the user

**Produces (output):** project plan → consumed by skills (system-prompt-draft.md §7):
- `generate-risk-register` (mode: detailed) — phase 2, Planning (parallel with comm-plan)
- `generate-comm-plan` — phase 2, Planning (parallel with risk-register)
- `generate-resource-plan` — phase 2 (Product 1, not MVP)
- `monitor-progress` — phases 4–5 (Product 1)
- `generate-plan-fact-report` — phase 6
- `coordinate-executors` — phases 3, 5 (Product 1)
- `generate-checklist` — phases 5, 6 (Product 1)

After the plan is approved, the user must upload `project-plan.md` to project knowledge so dependent skills can access it.

---

## 7. Example Invocation

**User command:**

> Generate a project plan. The charter is approved and uploaded to knowledge. I don't have duration estimates for work packages — assess based on scope.

**Agent response (after generation):**

> Project plan "[name]" generated based on: project charter (project-charter.md).
>
> Assumptions:
> - Duration of all work packages estimated by the agent based on scope volume and team composition.
> - Team load distributed evenly (no availability data provided).
> - Phase priority: Development → Testing → Launch (standard order for IT projects).
>
> Issues:
> - [Name]'s load exceeds 100% in May (WP-005 + WP-007 in parallel). Options: shift WP-007 to June or add a resource.
>
> Required: approve, provide comments, or reject.
>
> [plan text]

---

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-25 | 1.0 | Skill created. Algorithm: 14 steps. Hybrid duration estimation model. Resource map with fallback to charter data. Milestone definition criteria. Budget is optional |
| 2026-03-26 | 1.1 | §2 p.4: added explicit WP counter — verify ≤20 after decomposition, consolidate adjacent packages if exceeded. §2 p.5: clarified behavior on date conflict — do NOT generate dates beyond end_date; mark affected WPs with ⚠ and require user decision |
| 2026-03-29 | 1.2 | Translated to English. Added Language Detection block and bilingual triggers |
