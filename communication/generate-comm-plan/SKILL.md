---
name: generate-comm-plan
description: >
  Generates a communication plan from project charter, project plan, and stakeholder data.
  Includes stakeholder matrix (influence/interest), communication matrix, and escalation rules.
  Phase 2 artifact. In MVP stakeholders are extracted from charter; in P1 — from stakeholder-map.md.
trigger: >
  Command: user requests to generate a communication plan.
  Context: project plan is approved — agent offers to run this skill.
  Keywords RU: «сформируй план коммуникаций», «подготовь comm-plan», «кому и как коммуницировать».
  Keywords EN: "generate comm plan", "create communication plan", "build comm plan".
template: comm-plan.md
output_file: comm-plan.md
phase: "2 — Planning"
version: 1.0.0
---

# generate-comm-plan

## Triggers

**Russian:** «сформируй план коммуникаций», «подготовь comm-plan», «кому и как коммуницировать»
**English:** "generate comm plan", "create communication plan", "build comm plan"

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with `-ru` suffix
- Otherwise → use templates with `-en` suffix

All output (headings, labels, comments, instructions) must match the detected language.

## 1. Inputs

| Data | Required | Source | Notes |
|------|:--------:|--------|-------|
| Project charter | yes | knowledge or chat | Source of stakeholders (section 5 "Team and Roles"), goals, scope, constraints |
| Project plan | yes | knowledge or chat | Source of milestones, phases, work blocks — for binding communications to events |
| Stakeholder data | no | chat or knowledge | Additional stakeholders not listed in the charter. In P1 — `stakeholder-map.md` |
| Channel preferences | no | chat | Communication channels used by the team (Slack, Teams, Email, Meets, etc.) |

If required data is missing — request it (system-prompt-draft.md §3.2):

```
To generate the communication plan, the following are needed:
— Project charter (project-charter.md) — source of team, goals, constraints
— Project plan (project-plan.md) — source of milestones and phases
Available: [list what is present].
Missing: [be specific].
```

If the project plan does not yet exist — respond: "The communication plan depends on the project plan. Recommend running generate-project-plan first."

---

## 2. Execution Algorithm

1. **Validate inputs.** Check for charter + project plan. If missing → request using the template from §1. Do NOT generate a placeholder plan — respond ONLY with the data request.
2. **Extract stakeholders from charter.** From section 5 "Team and Roles" + section 1 "Goal" (client, sponsor). Add from project context: external stakeholders (customers, contractors, legal, finance) if mentioned in constraints, risks, or scope.
3. **Build preliminary stakeholder list.** For each: role, influence rating (H/M/L), interest rating (H/M/L), strategy (per matrix in §3). Mark ratings as agent assumptions.
4. **Show preliminary list to user.** Format:

```
Preliminary stakeholder list (extracted from charter):
| ID | Role | Name | Influence | Interest | Strategy |
[table]
Assumption: influence/interest ratings assigned by agent based on role and context.
Supplement or correct the list — after confirmation I will generate the full plan.
```

5. **Wait for confirmation or corrections.** Corrections → update list. Confirmation → step 6.
6. **Read template** `comm-plan.md` from project knowledge.
7. **Build communication matrix.** Mandatory minimum (§3 section 2). Additional entries — based on project context (milestones, external stakeholders, specifics).
8. **Build escalation rules.** Based on risks from charter and project constraints. Minimum 3 rules.
9. **Fill template sections** per rules in section 3.
10. **Validate result** against checklist (section 5).
11. **Show result in chat.** Format (system-prompt-draft.md §3.4):
    - What was done: "Communication plan generated based on [list sources]."
    - Assumptions: list all.
    - Required action: "Approve, provide feedback, or reject."
    - Do not include system file paths. Use filename only: "Plan saved as comm-plan.md."
12. **Wait for user response** (system-prompt-draft.md §3.5).
    - Approval → generate final version.
    - Feedback → revise and show updated version. After 3rd iteration — ask: "Continue revising or lock current version?"
13. **After approval:**
    - Propose text for the user to insert into log.md and project-state.md (system-prompt-draft.md §11).
    - Notify: "Communication plan approved. All Phase 2 artifacts are complete (project plan, risk register, communication plan)." (or specify which are still missing).

---

## 3. Section Filling Rules

### Section 1. Stakeholders

- Source: confirmed list from algorithm step 5.
- ID: `S01`, `S02`, ... — sequential numbering.
- Required roles: Sponsor, Client (internal), PM. Others — per context.

**Influence/Interest matrix → strategy:**

| Influence \ Interest | High | Medium | Low |
|---|---|---|---|
| **High** | Manage actively | Manage actively | Keep satisfied |
| **Medium** | Keep informed | Keep informed | Monitor |
| **Low** | Keep informed | Monitor | Monitor |

**Rating scale:**

| Level | Influence (description) | Interest (description) |
|---|---|---|
| H (High) | Makes key decisions, controls budget, can block the project | Actively participates, invested in outcomes, regularly requests status |
| M (Medium) | Influences specific areas (technical decisions, resources), does not block | Interested in certain aspects, periodically involved |
| L (Low) | Does not influence project decisions, executes tasks | Minimal interest, engaged on request |

### Section 2. Communication Matrix

- ID: `C01`, `C02`, ... — sequential numbering.
- Audience: references to stakeholder IDs from section 1.

**Mandatory minimum communications:**

| Type | Audience | Default Frequency |
|---|---|---|
| Sponsor status report | Sponsor (+ Client) | Weekly |
| Sprint/iteration planning | Team | On event (sprint start) |
| Sprint demo/review | Sponsor, Client, Tech Lead | On event (sprint end) |
| Escalation (critical issues) | Sponsor | On event |

Additional communications — per context: client sync, external stakeholder alignment, financial report, customer updates.

**Reference values:**

| Column | Allowed values |
|---|---|
| Format | Meeting, Report, Notification, Presentation, Letter |
| Channel | Email, Meeting (online), Meeting (offline), Chat, Meeting (online/offline) |
| Frequency | Daily, Weekly, Bi-weekly, Monthly, On event, On demand, One-time |
| Artifact | Filename from the system: `weekly-status.md`, `meeting-protocol-{date}.md`, `progress-report-{date}.md`, `deviation-report-{date}.md` or `—` if no artifact is produced |

### Section 3. Escalation Rules

- Minimum 3 escalation rules.
- Required situation types: schedule deviation, budget overrun, blocking issue.
- Additional — per context (incident, stakeholder refusal, legal issue).
- Thresholds: determine based on project scale. If not specified — formulate as assumption.
- Channel: for critical situations — multiple channels (Email + Meeting or Chat + Email).
- Response time: tie to severity (blocking — hours, deviation — days).

### Header Metadata

- `Version`: 1.0
- `Date`: current generation date.
- `File`: `comm-plan.md`
- `Document status`: `draft` (at generation). After approval — `approved`.
- `Source`: list the files used as input.

---

## 4. Placeholder Table

> Placeholders `{{}}` in the template are fill-in guides, not auto-substitution variables. Replace each with the corresponding value from the input data.

| Placeholder | Required | Source | Allowed values |
|---|:---:|---|---|
| `{{project_name}}` | yes | charter | text |
| `{{version}}` | yes | agent | `1.0` on creation |
| `{{date}}` | yes | system | YYYY-MM-DD |
| `{{source_docs}}` | yes | agent | list of source files |
| `{{role}}` | yes (≥3) | charter / user data | functional role |
| `{{name}}` | yes (≥3) | charter / user data | name / position |
| `{{strategy}}` | yes (≥3) | agent (per matrix §3) | Manage actively, Keep informed, Keep satisfied, Monitor |
| `{{comm_name}}` | yes (≥4) | agent | communication name |
| `{{format}}` | yes | agent | see reference §3 section 2 |
| `{{channel}}` | yes | agent / user data | see reference §3 section 2 |
| `{{frequency}}` | yes | agent | see reference §3 section 2 |
| `{{owner}}` | yes | charter / user data | name of responsible person |
| `{{artifact}}` | no | agent | system filename or `—` |
| `{{threshold}}` | yes (≥3) | project data / assumption | numeric threshold + unit |
| `{{stakeholder_id}}` | yes (≥3) | section 1 | `S01`, `S02`, ... |
| `{{deadline}}` | yes (≥3) | agent | response time (hours/days) |

---

## 5. Validation Checklist

Before showing result to user — verify:

- [ ] All required placeholders replaced with values
- [ ] No `{{}}` placeholders remaining in text
- [ ] Stakeholders: ≥3 (Sponsor, Client, PM), each with H/M/L rating and strategy
- [ ] Strategy matches the influence/interest matrix (§3 section 1)
- [ ] Communication matrix: ≥4 entries (mandatory minimum), each with audience (ID), format, channel, frequency
- [ ] Artifacts in matrix — real system filenames (not arbitrary labels)
- [ ] Escalation rules: ≥3, with thresholds, channels, and response time
- [ ] Escalation thresholds appropriate for project scale
- [ ] All agent assumptions listed when delivering result
- [ ] Document status = `draft`
- [ ] Header metadata filled in

---

## 6. Dependencies

**Consumes (input):**
- `project-charter.md` — project charter (skill generate-charter)
- `project-plan.md` — project plan (skill generate-project-plan)
- In P1: `stakeholder-map.md` — stakeholder map (skill generate-stakeholder-map)

**Produces (output):** communication plan → consumed by (system-prompt-draft.md §7):
- `send-email` (module) — defines recipients and mailing frequency (P1)

After plan approval, the user must upload `comm-plan.md` to project knowledge.

---

## 7. Usage Example

**User command:**

> Сформируй план коммуникаций. Устав и план проекта — в knowledge.

**Agent response (step 4 — preliminary list):**

> Stakeholders extracted from charter:
>
> | ID | Role | Name | Influence | Interest | Strategy |
> |---|---|---|---|---|---|
> | S01 | Sponsor | Алексей Воронов, CEO | H | H | Manage actively |
> | S02 | Client | Елена Морозова, Head of CS | H | H | Manage actively |
> | S03 | PM | Кирилл Ругалёв | M | H | Keep informed |
>
> Assumption: influence/interest ratings assigned based on roles.
> Supplement the list or correct the ratings.

**After approval (step 11):**

> Communication plan "ClientBoard" generated based on: project-charter.md, project-plan.md.
>
> Assumptions:
> - Stakeholder influence/interest ratings assigned by agent based on roles.
> - Budget escalation threshold: >10% of total (not specified in charter).
> - Communication channels: Email + online meetings (preferences not specified).
>
> Required: approve, provide feedback, or reject.
>
> [plan text]

---

## Change Log

| Date | Version | Change |
|------|---------|--------|
| 2026-03-26 | 1.0 | Skill created. Hybrid stakeholder model (extraction + clarification). Mandatory minimum of 4 communications. Reference values dictionary. Table of 16 placeholders |
