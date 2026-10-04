---
name: onboarding-plan-30-60-90
description: "Generate a 30-60-90 day onboarding plan from the manager's perspective — goals, key contacts, milestones, success metrics per phase. Use when onboarding a new hire without HR support. Triggers: 'create 30-60-90 day plan', 'onboarding plan', 'план адаптации 30-60-90', 'план онбординга'."
version: 1.0.0
---

# Onboarding Plan 30-60-90

Generates a structured 30-60-90 day onboarding plan for a new hire from the manager's perspective. Takes role details and 3–5 key priorities as input; outputs a phased markdown document with goals, key contacts, learning milestones, and a success metric per phase — ready to share with the new hire or save in a project folder.

**Input:**
- New hire role title and level (required)
- 3–5 role priorities or must-learn areas (required)
- Team context: team size, reporting line, key collaborators (optional)
- Start date and work format — Remote / Hybrid / Onsite (optional)

**Output:**
- Markdown onboarding plan with three phase sections (30 / 60 / 90 days)

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check that at least a role title is provided.
   - If input is empty or only whitespace, or contains no identifiable role title: stop and respond (bilingual): "Укажи должность и 3–5 ключевых приоритетов роли. / Provide the role title and 3–5 key priorities for the role."
   - If role title is present but priorities are missing: proceed; use generic role-appropriate milestones and add a note at the top of the plan: "Add role-specific priorities to tailor the learning milestones per phase."

2. Detect scope mismatch:
   - If user asks for an IT/HR checklist (equipment provisioning, system access, HR paperwork): respond: "Этот скилл создаёт план адаптации для руководителя, а не чеклист для HR или IT. / This skill generates a manager-facing onboarding plan, not an IT or HR setup checklist."
   - If user provides details for multiple hires at once: generate plan for the first hire only; note: "Сгенерировал план для первого сотрудника. Повтори запрос с данными следующего. / Generated plan for the first hire. Repeat with the next hire's details."

### Step 2: Extract and Structure Inputs

1. Parse the following fields from the user's input:
   - **Role title** — e.g., "Product Manager", "Senior Developer"
   - **Level** — Junior / Middle / Senior / Lead / Director / VP / C-level
   - **New hire name** — optional; use "New Hire" as placeholder if not given
   - **Start date** — optional
   - **Work format** — Remote / Hybrid / Onsite; default to "Hybrid" if not specified
   - **Team context** — team size, reporting line, key collaborators (optional)
   - **Role priorities** — extract 3–5 must-learn areas from user's notes

2. Flag if level is Senior / Director / VP / C-level → apply leadership adjustment in Step 3.

### Step 3: Generate the Three-Phase Plan

For each phase, produce four sub-sections: Goals, Key Contacts, Learning Milestones, Success Metric. Use the role priorities from Step 2 to populate learning milestones — not generic filler.

**Phase 1 — First 30 Days: Orient**
- Goals: 2 learning goals (understand team structure and core tools; map key stakeholders) + 1 performance goal (small, visible output)
- Key Contacts: 4–6 contacts with role, purpose of meeting, and timing (Week 1 through Week 4)
- Learning Milestones: 4–6 checkboxes drawn directly from role priorities
- Success Metric: 1 concrete, measurable indicator of phase completion

**Phase 2 — Days 31–60: Contribute**
- Goals: 2 learning goals (deeper domain knowledge; understand cross-team dependencies) + 1 performance goal (own a deliverable or recurring process independently)
- Key Contacts: 2–3 additional contacts (extended team, skip-level, external partners)
- Learning Milestones: 3–4 checkboxes (deeper skills from priorities)
- Success Metric: 1 concrete, measurable indicator

**Phase 3 — Days 61–90: Own**
- Goals: 1 learning goal (strategic context, full role scope) + 2 performance goals (own end-to-end delivery; propose 1 improvement)
- Key Contacts: 1–2 contacts (leadership, external stakeholders, peers from adjacent teams)
- Learning Milestones: 2–3 checkboxes (strategic or advanced skills)
- Success Metric: 1 concrete, measurable indicator

**Leadership adjustment** (Senior / Director / VP / C-level):
- Phase 1 goals: emphasize org-political mapping and stakeholder alignment, not just tool learning
- Phase 2 goals: include quick-win identification and first visible leadership contribution
- Phase 3 goals: include team strategy, OKR ownership, or hiring decisions

**Remote adjustment** (work format = Remote):
- Replace in-person contact suggestions with async-first equivalents (Slack intros, async onboarding docs, virtual coffee chats)
- Flag remote-specific tools in milestones (async comms tools, documentation standards)

### Step 4: Format and Output

1. Output the complete plan using the structure defined in the Output Format section below.
2. Use the detected language for all section headers:
   - EN: Phase 1 — First 30 Days: Orient / Phase 2 — Days 31–60: Contribute / Phase 3 — Days 61–90: Own
   - RU: Фаза 1 — Первые 30 дней: Ориентация / Фаза 2 — Дни 31–60: Вклад / Фаза 3 — Дни 61–90: Владение
3. Output the plan directly — no meta-commentary or explanation between sections.

---

## Output Format

Single markdown document with a title block and three phase sections:

```markdown
# Onboarding Plan: [Role Title] — [Name or "New Hire"]

**Start Date:** [date or TBD]
**Work Format:** [Remote / Hybrid / Onsite]

---

## Phase 1 — First 30 Days: Orient

**Goals:**
- [Learning goal 1]
- [Learning goal 2]
- Performance goal: [small, visible output by day 30]

**Key Contacts:**
| Name / Role | Purpose | When |
|-------------|---------|------|
| [Direct Manager] | Clarify expectations and success criteria | Week 1 |
| [Teammate 1] | Understand team workflows and day-to-day | Week 1–2 |
| [Cross-func Partner] | Map dependencies | Week 2–3 |
| [Senior Stakeholder] | Understand business context | Week 3–4 |

**Learning Milestones:**
- [ ] [Tool or process from role priorities]
- [ ] [Domain knowledge area 1]
- [ ] [Domain knowledge area 2]
- [ ] [Domain knowledge area 3]

**Success Metric:** [Concrete, measurable indicator of phase completion]

---

## Phase 2 — Days 31–60: Contribute

[same structure as Phase 1]

---

## Phase 3 — Days 61–90: Own

[same structure as Phase 1]
```

English uses English section headers throughout. Russian uses Russian headers (Фаза 1 — Первые 30 дней: Ориентация, Фаза 2 — Дни 31–60: Вклад, Фаза 3 — Дни 61–90: Владение).

---

## Negative Cases

- **Empty input, only whitespace, or no role title detected:** Respond (bilingual): "Укажи должность и 3–5 ключевых приоритетов роли. / Provide the role title and 3–5 key priorities for the role."
- **Role title present but priorities missing:** Proceed with generic role-appropriate milestones; add a note at the top of the plan: "Add role-specific priorities to tailor the learning milestones per phase."
- **IT/HR checklist request:** Clarify that this skill generates a manager-facing onboarding plan, not an IT setup or HR paperwork checklist.
- **Multiple hires at once:** Generate plan for the first hire only; prompt user to repeat for the next hire.
