---
name: generate-risk-register
description: >
  Generates a risk register from project charter (initial mode) or enriches it
  with project plan data (detailed mode). Two modes: initial — phase 1 after
  charter approval; detailed — phase 2 after project plan approval.
trigger: >
  Command: user asks to generate or update the risk register.
  Context: charter approved (initial) or project plan approved (detailed) — agent suggests running the skill.
  Keywords RU: «сформируй реестр рисков», «подготовь risk register», «обнови реестр рисков».
  Keywords EN: "generate risk register", "create risk register", "update risk register".
template: risk-register-en.md
output_file: risk-register.md
phase: "1 — Initiation (initial), 2 — Planning (detailed)"
version: 1.0.0
---

# generate-risk-register

## Triggers

**Russian:** «сформируй реестр рисков», «подготовь risk register», «обнови реестр рисков»
**English:** "generate risk register", "create risk register", "update risk register"

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with `-ru` suffix
- Otherwise → use templates with `-en` suffix

All output (headings, labels, comments, instructions) must match the detected language.

---

## 1. Input Data

### Initial mode (phase 1)

| Data | Required | Source | Notes |
|------|:--------:|--------|-------|
| Project charter (project-charter.md) | yes | knowledge | Primary context: goal, scope, timeline, budget, constraints, assumptions |
| Project type / industry | no | chat or knowledge | Used to select industry-typical risks. If not specified — agent infers from charter |
| Additional context | no | chat | User comments on specific risks |

### Detailed mode (phase 2)

| Data | Required | Source | Notes |
|------|:--------:|--------|-------|
| Project charter (project-charter.md) | yes | knowledge | Project context |
| Project plan (project-plan.md) | yes | knowledge | WBS, timeline, resources, dependencies — source of new risks |
| Risk register v1 (risk-register.md) | yes | knowledge | Output of initial mode — base for update |
| Additional context | no | chat | New risks identified by the user |

If required data is missing — request using this template:

```
To generate the risk register, the following is required:
— Initial mode: approved project charter (project-charter.md).
— Detailed mode: charter + project plan (project-plan.md) + current risk register (risk-register.md).
Available data: [list what is available].
Missing: [be specific].
```

---

## 2. Execution Algorithm

1. **Determine mode.** If the user has not specified — infer from context: project plan present → detailed, charter only → initial. If ambiguous — ask.
2. **Verify input data.** Minimum data for the selected mode is present → step 3. Missing → request using the template from §1. Do NOT generate a placeholder or sample register.
3. **Read the template** `risk-register-ru.md` or `risk-register-en.md` from project knowledge (based on detected language).
4. **Identify risks.**
   - **Initial:** Analyze the charter from scratch — goal, scope (included and excluded), timeline, budget, constraints, assumptions, team composition. For each charter section evaluate: what could go wrong? Use categories from the reference table (§3). Recommended count: 5–10 risks. Do not automatically copy the top-3 risks from the charter — perform an independent analysis (charter risks may enter the register if confirmed by analysis).
   - **Detailed:** Use register v1 as the base. Analyze the project plan: WBS (which work packages are highest risk?), critical path, dependencies, resource constraints. Add new risks. Update assessments of existing risks (probability/impact may have changed). For each risk — link to WP-xxx from the plan, assign a specific owner from project-plan. Specify actions concretely.
5. **Assess each risk** using the scale from the reference table (§3): category, probability (H/M/L), impact (H/M/L), level, strategy (Avoid/Mitigate/Transfer/Accept). Level is calculated strictly by the table below — not by intuition or proximity to adjacent cells:

   | Probability | Impact | Level |
   |-------------|--------|-------|
   | H | H | Critical |
   | H | M | **High** |
   | M | H | **High** |
   | H | L | Medium |
   | M | M | Medium |
   | L | H | Medium |
   | M | L | Low |
   | L | M | Low |
   | L | L | Low |

   **Common error:** H×M and M×H are High, not Medium. Verify every risk against this table before recording in the register.

6. **Fill the register table** following the rules in §3.
7. **Fill the risk matrix.** For each risk, perform 3 steps:
   - (a) Read from the table: probability → this is the ROW of the matrix; impact → this is the COLUMN of the matrix.
   - (b) Find the cell at the intersection of that row and column → write the ID.
   - (c) Verify: matrix row = probability from the table? matrix column = impact from the table? If not — correct.

   **Common error:** for risks with L (low) probability, the ID is incorrectly placed in the "Medium" row instead of "Low". Verify each L-probability risk separately.
8. **Validate the result** using the checklist (§5).
9. **Present the result in chat.** Format:
   - What was done: "Risk register generated (mode: initial/detailed) based on [list sources]."
   - Number of risks: N (including critical: M).
   - Assumptions (if any).
   - Action required: "Approve, provide comments, or reject."
   - Do not include system file paths.
   - [register content]
10. **Wait for user response.**
    - Approval → produce final text.
    - Comments → revise, show updated version. After 3rd iteration — ask: "Continue revising or finalize current version?"
11. **After approval — complete both steps:**
    - Provide the user with text to insert into log.md and project-state.md.
    - Propose the specific next skill. This is a mandatory part of the response — without it the skill chain breaks. Use these exact phrases:
      - **Initial:** "Risk register approved. Next task: **generate-project-plan** (project plan). Start?"
      - **Detailed:** "Risk register updated. Next task: **generate-comm-plan** (communication plan). Start?"

---

## 3. Filling Rules

### Header metadata
- `Version`: 1.0 (initial) or 2.0 (detailed when updating v1).
- `Date`: current generation date (YYYY-MM-DD).
- `File`: `risk-register.md`.
- `Document status`: `draft` (at generation). After user approval — `approved`.
- `Mode`: `initial` or `detailed`.
- `Source`: list source files (e.g., "project-charter.md" or "project-charter.md, project-plan.md, risk-register.md v1").

### Register table

The table contains exactly 10 columns (no more, no less): ID, Risk, Category, Probability, Impact, Level, Strategy, Actions, Owner, Status. Adding extra columns is prohibited — it breaks compatibility with the template and other skills. The difference between modes is in the depth of content:

| Column | Initial | Detailed |
|--------|---------|----------|
| ID | R001, R002, ... | Retain IDs from v1 for existing risks. New risks — next sequential number |
| Risk | Wording: "Event → consequence for the project" | Same, refine wording if needed |
| Category | From reference table (see below) | Same |
| Probability | H/M/L | Reassess using plan data |
| Impact | H/M/L | Reassess using plan data |
| Level | Per matrix (see below) | Recalculate |
| Strategy | From reference table (see below) | Refine if needed |
| Actions | Brief, 1–2 sentences | Specific steps linked to WP-xxx from the plan |
| Owner | PM (default) or "assign during planning" | Specific team member from project-plan |
| Status | `open` | `open` / `in progress` / `closed` / `triggered` |

### Category reference table

| Category | Description | Examples |
|----------|-------------|---------|
| Technical | Technologies, architecture, integrations | System incompatibility, architecture errors |
| Resource | People, competencies, availability | Loss of key specialist, skill gaps |
| External | Factors outside team control | Regulatory changes, competitor actions |
| Organizational | Processes, communication, decision-making | Approval delays, priority conflicts |
| Financial | Budget, pricing, ROI | Budget overrun, contractor rate changes |

### Assessment scale

| Rating | Probability | Impact |
|--------|-------------|--------|
| H (High) | >60% — likely to occur | Critical: schedule slip >2 weeks, budget >20%, scope substantially changes |
| M (Medium) | 30–60% — may occur | Significant: schedule 1–2 weeks, budget 10–20%, scope partially affected |
| L (Low) | <30% — unlikely | Minor: schedule <1 week, budget <10%, scope unaffected |

### Risk level matrix (probability × impact)

|  | L (impact) | M (impact) | H (impact) |
|--|-----------|-----------|-----------|
| **H (prob.)** | Medium | High | Critical |
| **M (prob.)** | Low | Medium | High |
| **L (prob.)** | Low | Low | Medium |

### Strategy reference table

| Strategy | When to apply | Example action |
|----------|---------------|---------------|
| Avoid | The risk cause can be eliminated | Reject a risky technology |
| Mitigate | Probability or impact can be reduced | Prototyping, schedule buffer |
| Transfer | Consequences can be shifted to another party | Insurance, outsourcing, fixed-price contract |
| Accept | Response cost > damage, or risk is outside team control | Monitor without active steps, budget reserve |

### Risk matrix (visualization)
Place risk IDs in the matrix cells from the template. Each risk goes into one cell corresponding to its probability and impact assessment.

---

## 4. Placeholder Table

> Placeholders `{{}}` in the template are fill-in guides, not auto-substitution variables. Replace each with the corresponding value from the input data.

| Placeholder | Required | Source | Allowed values |
|-------------|:--------:|--------|---------------|
| `{{project_name}}` | yes | project charter | text |
| `{{version}}` | yes | agent | `1.0` (initial), `2.0` (detailed when updating v1) |
| `{{date}}` | yes | system | YYYY-MM-DD |
| `{{mode}}` | yes | agent / user | `initial` or `detailed` |
| `{{source_docs}}` | yes | agent | list of source files |
| `{{risk_description}}` | yes (≥5 for initial, ≥ count in v1 for detailed) | agent | wording: "event → consequence" |
| `{{category}}` | yes | agent | one of the 5 categories from the reference table |
| `{{level}}` | yes | agent | Critical / High / Medium / Low (per matrix) |
| `{{strategy}}` | yes | agent | Avoid / Mitigate / Transfer / Accept |
| `{{actions}}` | yes | agent | text, 1–2 sentences (initial) or specific steps with WP-xxx (detailed) |
| `{{owner}}` | yes | agent / project-plan | name or role. Initial: PM by default. Detailed: specific team member |

---

## 5. Validation Checklist

Before presenting the result to the user — verify:

- [ ] All required placeholders replaced with values
- [ ] No `{{}}` placeholders remaining in the text
- [ ] Mode (initial/detailed) specified in the header
- [ ] Initial: ≥5 risks covering ≥3 categories from the reference table
- [ ] Detailed: all risks from v1 are present (updated or closed) + new risks from the plan
- [ ] Each risk: wording is "event → consequence", not just a topic
- [ ] Assessments are consistent: for EACH risk calculate the level using the table in §2 step 5 and COMPARE with the recorded value. Special attention: H×M=High (not Medium), M×H=High (not Medium)
- [ ] Strategy matches context (not "Accept" for a critical risk without justification)
- [ ] Detailed: each risk linked to WP-xxx, owner is a specific person
- [ ] Risk matrix is filled in, IDs match the table
- [ ] **Matrix-table synchronization (element by element):** for EACH risk write the triple: ID → probability from table → matrix row; ID → impact from table → matrix column. If row ≠ probability or column ≠ impact — CORRECT. Special attention: risks with L probability frequently end up in the "Medium" row
- [ ] All agent assumptions listed in the response
- [ ] Document status = `draft`

---

## 6. Dependencies

**Consumes (input):**
- `project-charter.md` ← generate-charter (both modes)
- `project-plan.md` ← generate-project-plan (detailed only)
- `risk-register.md` v1 ← generate-risk-register initial (detailed only)

**Produces (output):** `risk-register.md` → consumed by:
- `generate-project-plan` — for incorporating risks during planning (if initial)
- `generate-closure-report` — for final analysis (if detailed)

After the register is approved, the user must upload `risk-register.md` to the project knowledge base so it is available to dependent skills.

---

## 7. Usage Examples

### Initial (phase 1)

**User command:**

> Generate the risk register. Project charter is in knowledge.

**Agent response (after generation):**

> Risk register generated (mode: initial) based on: project-charter.md.
>
> Identified 7 risks (critical: 1, high: 2, medium: 3, low: 1). Categories covered: Technical, Resource, External, Organizational.
>
> Assumptions:
> - Project type inferred as "IT product launch" from the charter description.
> - All risk owners set to PM (to be specified in detailed mode after the project plan is ready).
>
> Action required: approve, provide comments, or reject.
>
> [register content]

### Detailed (phase 2)

**User command:**

> Update the risk register. Project plan and current register are in knowledge.

**Agent response (after generation):**

> Risk register updated (mode: detailed) based on: project-charter.md, project-plan.md, risk-register.md v1.
>
> Risks in register: 11 (was 7). New: 4 (from WBS and resource plan analysis). Updated assessments: R003 escalated to "High" (external contractor dependency identified). All risks linked to work packages, owners assigned.
>
> Assumptions:
> - Owners assigned based on roles from project-plan.md.
>
> Action required: approve, provide comments, or reject.
>
> [register content]

---

## Change Log

| Date | Version | Change |
|------|---------|--------|
| 2026-03-29 | 2.0 | Translated to English per translation-rules.md. Language Detection block and bilingual triggers added. Template references updated to -ru/-en suffixes |
| 2026-03-26 | 1.2 | Based on benchmark v1.1 results (96.1%, 3 failures — all D_logic): added explicit level calculation table (9 combinations) in §2 step 5 with emphasis on H×M=High; strengthened §2 step 7 (3-step matrix fill procedure with L-probability warning); strengthened §5 step 7 (row-by-row level verification) and §5 step 11 (element-by-element verification with triple extraction) |
| 2026-03-25 | 1.1 | Based on benchmark results (94.7%, 4 failures): strengthened §2 step 11 (mandatory next skill recommendation with exact phrasing), added matrix-table synchronization check in §5 and §2 step 7, fixed 10-column constraint in §3 with prohibition on adding columns |
| 2026-03-25 | 1.0 | Skill created |
