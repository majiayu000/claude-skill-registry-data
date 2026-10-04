---
name: generate-charter
description: >
  Generates a project charter from brief, stakeholder answers, and constraints.
  The charter is the first artifact of the Initiation phase. Once approved,
  it unlocks dependent tasks: generate-risk-register, generate-project-plan,
  generate-estimate. Accepts both structured briefs and free-form notes.
trigger: >
  Command: user requests a project charter.
  Context: user has provided project data — agent suggests running the skill.
  Keywords RU: «сформируй устав», «подготовь устав проекта», «создай charter».
  Keywords EN: "generate charter", "create project charter", "build charter".
template: project-charter.md
output_file: project-charter.md
phase: "1 — Initiation"
version: 1.0.0
---

# generate-charter

## Triggers

**Russian:** «сформируй устав», «подготовь устав проекта», «создай charter», «нужен устав проекта»
**English:** "generate charter", "create project charter", "build charter", "draft project charter"

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with `-ru` suffix
- Otherwise → use templates with `-en` suffix

All output (headings, labels, comments, instructions) must match the detected language.

---

## 1. Inputs

| Data | Required | Source | Notes |
|------|:--------:|--------|-------|
| Project data | yes | chat or knowledge | Brief, free-form description, answers to questions, or unstructured notes. Agent extracts and structures independently |
| Stakeholder answers | no | chat or knowledge | Completed questionnaire or free-form answers. If absent — agent extracts from general project description |
| Project constraints | no | chat or knowledge | Budget, timeline, technical, organizational. If not provided separately — agent extracts from general description |
| Team composition | no | chat or knowledge | If provided — fill Section 5. If absent — keep only Sponsor and PM rows |
| Market context | no | chat or knowledge | Used to refine goal statement and risks |

If required data is missing — request it (system-prompt-draft.md §3 p.2):

```
To generate a charter, I need project information in any format:
a ready brief, answers to questions, a free-form description, or a set of key points.
Minimum to start: project goal and at least one of: timeline, budget, scope.
Available data: [list what is present].
Missing for the charter: [specify].
```

---

## 2. Execution Steps

1. **Check inputs.** Verify that project data (in any form) is present. If missing → request using the template in §1. Do NOT generate a placeholder charter, template, or example — respond ONLY with the data request. If present → step 2.
2. **Structure inputs.** If data is free-form — extract and categorize: goal, scope, timeline, budget, team, constraints, risks. Note ambiguities and gaps; clarify with the user selectively. Do not ask for everything at once — request only what is strictly required for the charter. When computing dates from relative timelines ("12 weeks from April 7") — calculate exactly: start + N×7 days = end. Do not round.
3. **Check for contradictions.** If one parameter (budget, timeline, scope) appears with conflicting values across sources — do NOT choose a value independently. List the contradictions and ask the user which data is current. Exception: if the user explicitly clarifies outdated brief data in chat — treat the clarification as authoritative.
4. **Read the template** `project-charter.md` from project knowledge.
5. **Extract data from sources.** For each placeholder (Section 4) — find the value in inputs. Priority: explicit user data > brief > agent assumption.
6. **Fill template sections** following the rules in Section 3.
7. **Validate the result** using the checklist (Section 5).
8. **Show the result in chat.** Format (system-prompt-draft.md §3 p.4):
   - What was done: "Charter generated for project [name] based on: [list sources]."
   - Assumptions: list all (if any).
   - What is required: "Approve, provide comments, or reject."
   - Do not include system file paths. Use filename only: "Charter saved as project-charter.md".
9. **Wait for user response** (system-prompt-draft.md §3 p.5).
   - Approval → produce the final document.
   - Comments → revise and show updated version. After the 3rd iteration — ask: "Continue revising or finalize the current version?" (this is not a hard limit — user may request more iterations).
10. **After approval:**
    - Offer the user text to paste into log.md and project-state.md (system-prompt-draft.md §11).
    - Notify: "Charter approved. Next available task: generate-risk-register (initial risk register). Start?" (system-prompt-draft.md §7).

---

## 3. Section Fill Rules

### Section 1. Project Goal
- Extract from stakeholder answers or free-form description (block "Goals and Expectations").
- Format: 1–3 sentences. What is being done, why, and what the outcome is.
- If the user specified success metrics — include them.

### Section 2. Project Result (Scope)
- **Included:** specific deliverables from inputs. Each item is a measurable result.
- **Excluded:** explicit out-of-scope items from stakeholder answers ("we are NOT doing..."). If not specified — formulate based on context and record as an assumption.

### Section 3. Timeline and Milestones
- Dates from inputs.
- Milestones: tie to key deliverables from Section 2. Minimum: start, intermediate checkpoints, launch.
- If no exact dates — use relative timelines (week N) and record the assumption.

### Section 4. Budget
- Fill from stakeholder data on budget and resources.
- Add rows per number of budget line items in inputs. Last row is the total.
- If breakdown is absent — state the total as a single row and record the assumption: "Budget breakdown by line item was not provided."
- "Notes" column — for explanations and sources of figures.

### Section 5. Team and Roles
- Fill from team composition (if provided).
- Required roles: Sponsor, PM.
- If composition is not provided — keep Sponsor and PM rows only; do not add others.

### Section 6. Constraints and Assumptions
- **Constraints:** from constraint data + identified from project description.
- **Assumptions:** all assumptions made by the agent during filling (e.g., "budget breakdown not provided", "out-of-scope items determined by agent").

### Section 7. Key Risks (Top 3)
- Identify exactly 3 most probable/impactful risks based on project context. The charter is a strategic document for approval, not a risk register. Full detail will be in risk-register.md (next skill). If more than 3 risks are identified — mention in assumptions: "3 key risks selected from N identified. Remaining risks — in the risk register."
- Rating: H (High) / M (Medium) / L (Low) — for both probability and impact.
- For each — briefly describe mitigation.
- Note: "Details — in risk-register.md" (to be created by the next skill).

### Section 8. Approval
- Fill names from Section 5 (Sponsor, PM). Date — leave blank (filled upon approval).

### Header Metadata
- `Version`: 1.0
- `Date`: current generation date.
- `File`: `project-charter.md`
- `Document Status`: `draft` (at generation). After user approval — `approved`.
- `Project Manager`: from inputs.

---

## 4. Placeholder Table

> Placeholders `{{}}` in the template are fill targets, not auto-substitution variables. Replace each with the corresponding value from inputs.

| Placeholder | Required | Source | Allowed Values |
|-------------|:--------:|--------|----------------|
| `{{project_name}}` | yes | project data | text |
| `{{date}}` | yes | system | YYYY-MM-DD |
| `{{pm_name}}` | yes | project data / team | name |
| `{{project_goal}}` | yes | project data | text, 1–3 sentences |
| `{{deliverable_N}}` | yes (≥1) | project data | specific result |
| `{{out_of_scope_N}}` | yes (≥1) | project data / assumption | what is NOT included |
| `{{start_date}}` | yes | project data | YYYY-MM-DD |
| `{{end_date}}` | yes | project data | YYYY-MM-DD |
| `{{milestone_N}}` | yes (≥1) | project data / section 2 | milestone name |
| `{{date_N}}` | yes | project data | YYYY-MM-DD or "week N" |
| `{{launch_date}}` | yes | project data | YYYY-MM-DD |
| `{{cost_item_N}}` | no | project data | budget line item |
| `{{amount_N}}` | no | project data | number + currency |
| `{{note_N}}` | no | agent | line item explanation |
| `{{total_budget}}` | yes | project data | number + currency |
| `{{sponsor_name}}` | yes | project data | name |
| `{{role_N}}` | no | team | role name |
| `{{name_N}}` | no | team | name |
| `{{responsibility_N}}` | no | team | area of responsibility |
| `{{constraint_N}}` | yes (≥1) | project data | text |
| `{{assumption_N}}` | no | agent | text (formulated by agent) |
| `{{risk_N}}` | yes (≥3) | agent | risk description |
| `{{mitigation_N}}` | yes (≥3) | agent | mitigation description |

---

## 5. Validation Checklist

Before showing the result to the user — verify:

- [ ] All required placeholders replaced with values
- [ ] No `{{}}` placeholders remain in the text (except removed optional rows)
- [ ] Project goal is specific and measurable
- [ ] Scope contains both "Included" (≥1) and "Excluded" (≥1)
- [ ] Dates are consistent: start_date < milestone_dates < end_date
- [ ] Budget: total = sum of rows (or single row with total amount)
- [ ] Risks: exactly 3, with probability and impact ratings, with mitigation
- [ ] All agent assumptions listed in Section 6
- [ ] Document status = `draft`
- [ ] File: `project-charter.md` stated in header

---

## 6. Dependencies

**Consumes (input):** project data from the user — via chat or knowledge.

**Produces (output):** project charter → consumed by skills (system-prompt-draft.md §7):
- `generate-risk-register` (mode: initial) — phase 1, Initiation
- `generate-project-plan` — phase 2, Planning
- `generate-estimate` — phase 1 (Product 1, non-MVP)

After charter approval, the user must upload `project-charter.md` to project knowledge to make it available to dependent skills.

---

## 7. Example

**User command:**

> Generate a project charter. Brief, stakeholder answers, and constraints are in project knowledge.

**Agent response (after generation):**

> Charter generated for project "[name]" based on: brief, stakeholder answers, constraints.
>
> Assumptions:
> - Out-of-scope items determined by agent based on context (not explicitly stated by stakeholder).
> - Budget breakdown by line item was not provided — total amount stated.
>
> Required: approve, provide comments, or reject.
>
> [charter text]

---

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-25 | 1.0 | Skill created. Reference SKILL.md for remaining MVP skills |
| 2026-03-25 | 1.1 | Based on benchmark results (3 tests, 6 runs). Added: step 3 — contradiction check; strengthened guard rail for missing data (step 1); explanation of "exactly 3 risks" constraint (§3 section 7); prohibition of file paths in response (step 8); exact date calculation (step 2) |
