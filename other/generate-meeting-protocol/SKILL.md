---
name: generate-meeting-protocol
description: >
  Generates a meeting protocol from free-form notes. Extracts decisions, action items,
  and plan changes. If project plan is available — links changes to WP-xxx/Mx IDs.
  Phase 3 artifact, but usable in any phase. Independent skill with no upstream dependencies.
trigger: >
  Command: user asks to generate a meeting protocol.
  Context: user provides meeting notes or summary — agent offers to run.
  Keywords (RU): «оформи протокол», «протокол встречи», «обработай заметки со встречи».
  Keywords (EN): "generate meeting protocol", "meeting notes", "meeting minutes".
template: meeting-protocol-{lang}.md
output_file: meeting-protocol-{date}.md
phase: "3 — Prototyping (universal, applicable in any phase)"
version: 1.0.0
---

# generate-meeting-protocol

## Triggers

**Russian:** «оформи протокол», «протокол встречи», «обработай заметки со встречи»
**English:** "generate meeting protocol", "meeting notes", "meeting minutes"

---

## Language Detection

Determine the language of the user's request:
- If the request is in Russian → use templates with `-ru` suffix
- Otherwise → use templates with `-en` suffix

All output (headings, labels, comments, instructions) must match the detected language.

---

## 1. Input Data

| Data | Required | Source | Notes |
|------|:--------:|--------|-------|
| Meeting notes | yes | chat or knowledge | Any format: bullet points, free text, chat copy, voice dictation. Agent structures the content independently |
| Project plan | no | knowledge | If available — agent links changes to plan element IDs (WP-xxx, Mx). If not — describes changes as text |
| Meeting context | no | chat | Meeting type, participants, date — if not included in the notes |

If required data is missing — request it (system-prompt-draft.md §3 p.2):

```
To generate a protocol, meeting notes are required — in any format:
bullet points, free text, chat copy, voice dictation (as text).
Minimum to start: what was discussed and what decisions/tasks were recorded.
Available data: [list what is available].
Missing: [specify].
```

---

## 2. Execution Algorithm

1. **Validate input data.** Check if notes are present. If not → request using the template from §1. Do NOT generate a placeholder protocol — respond ONLY with the data request.
2. **Extract meeting metadata.** From notes or context: date, participants, topic, meeting type, facilitator. What cannot be extracted — ask the user specifically. Minimum to proceed: meeting date.
3. **Structure the content.** Extract from notes and categorize:
   - **Agenda** — topics that were discussed.
   - **Decisions** — recorded decisions (IDs: D001, D002, ...).
   - **Action items** — actions with owners and deadlines (IDs: A001, A002, ...).
   - **Plan changes** — if notes imply changes to timelines, scope, or resources.
   - **Open issues** — unresolved questions requiring further discussion.
4. **Verify action item completeness.** Each action item (A00x) must include: description, owner, deadline. If deadline/owner is missing from the notes — mark as `[clarify]` and record in assumptions.
5. **Determine plan changes (section 5).** Rules:
   - If project plan is available in knowledge → find affected elements, specify IDs (WP-xxx, Mx). Columns: "Was" (from plan) → "Becomes" (from notes) → "Basis" (decision ID D00x).
   - If project plan is NOT available → describe changes as text without IDs. Record assumption: "Project plan not provided — element IDs not specified."
   - If no plan changes → delete section 5.
6. **Determine conditional sections (5, 6, 7).** Delete a section if no data is available for it:
   - Section 5 "Plan Changes" — delete if notes contain no plan-level changes.
   - Section 6 "Open Issues" — delete if all issues are resolved.
   - Section 7 "Next Meeting" — delete if date/topic were not discussed.
7. **Read the template** `meeting-protocol-{lang}.md` from project knowledge.
8. **Fill template sections** per the rules in section 3.
9. **Validate the result** using the checklist (section 5).
10. **Show the result in chat.** Format (system-prompt-draft.md §3 p.4):
    - What was done: "Protocol generated for meeting [date] based on: [notes source]."
    - Key outcomes: N decisions, M action items, K plan changes (or "no changes").
    - Assumptions: list all.
    - `[clarify]` markers: list if any.
    - Next step: "Approve, provide feedback, or reject."
    - Do not include system paths. Use filename only: "Protocol: meeting-protocol-YYYY-MM-DD.md".
11. **Wait for user response** (system-prompt-draft.md §3 p.5).
    - Approval → produce final text.
    - Feedback → revise, show updated version. After 3rd iteration — ask: "Continue revising or finalize current version?"
12. **After approval:**
    - Propose text for insertion into log.md and project-state.md (system-prompt-draft.md §11).
    - If section 5 contains changes — recommend: "The protocol includes project plan changes. Consider updating project-plan.md."

---

## 3. Section-Filling Rules

### Header Metadata

- `meeting_title`: meeting topic — extract from notes or ask.
- `project_name`: from session context.
- `meeting_date`: YYYY-MM-DD.
- `File`: `meeting-protocol-YYYY-MM-DD.md` (substitute meeting date).
- `Document status`: `draft` (at generation). After approval — `approved`.
- `meeting_type`: meeting type (see type reference below). If not specified — infer from note content, record as assumption.
- `facilitator`: from notes. If not specified — `[clarify]`.
- `Scribe`: `AI agent` (always).
- `source_notes`: where the notes came from (e.g. "PM notes", "Slack copy", "voice dictation").

**Meeting type reference (guidance):**

| Type | Description | Typical sections |
|------|-------------|-----------------|
| Planning | Sprint, iteration, or phase planning | 2, 3, 4, 5 |
| Status | Progress sync | 2, 3, 4, 6 |
| Demo/Review | Results demonstration | 2, 3, 4, 5 |
| Retrospective | Team retrospective | 2, 3, 4, 6 |
| Decision-making | Go/No-Go, option selection | 2, 3, 5 |
| Ad-hoc | Unplanned, focused on a specific issue | 2, 3, 4 |

> The reference is a guide, not a constraint. Sections are determined by note content, not meeting type.

### Section 1. Participants

- Extract from notes: names, roles.
- Attendance: default "yes" if mentioned in notes. If absence is noted — "no".
- If participant list is not in the notes — ask the user.

### Section 2. Agenda

- Extract discussed topics from notes.
- Statuses: `discussed` (has a decision/conclusion), `deferred` (not discussed, postponed), `dropped` (closed/no longer relevant).
- Sequential numbering: 1, 2, 3...

### Section 3. Key Decisions

- IDs: `D001`, `D002`, ... — sequential numbering.
- Decision: exact formulation — what was decided. Specific, no vague language.
- Initiator: who proposed/championed the decision (from notes). If unknown — `[clarify]`.
- Status: `accepted` (final) or `deferred` (needs more information/discussion).

### Section 4. Action Items

- IDs: `A001`, `A002`, ... — sequential numbering.
- Each action item: a specific action (not a process).
- Owner: from notes. If not specified — `[clarify]`.
- Deadline: specific date (YYYY-MM-DD) or relative deadline. If not specified — `[clarify]`.
- Priority: `H` (high) / `M` (medium) / `L` (low). Determined by context: proximity to next milestone, criticality, urgency mentions. If cannot be determined — `M` (assumption).

### Section 5. Project Plan Changes (conditional)

- **Delete the section** if notes contain no changes to timelines, scope, resources, or project milestones.
- **If project plan is available:** in the "What changed" column, specify the plan element ID: `WP-xxx` (work package) or `Mx` (milestone). "Was" — value from plan. "Becomes" — from notes. "Basis" — decision ID (D00x) that triggered the change.
- **If plan is NOT available:** describe the change as text (without IDs). Assumption: "Plan element IDs not specified — project plan not provided."

### Section 6. Open Issues (conditional)

- **Delete the section** if all agenda items are resolved and there are no deferred topics.
- Format: bulleted list. Each item — a specific question requiring a decision or information.

### Section 7. Next Meeting (conditional)

- **Delete the section** if next meeting date/topic were not discussed.
- If only date or only topic was discussed — fill in what is known, mark the other as `[clarify]`.

---

## 4. Placeholder Reference

> Placeholders `{{}}` in the template are filling guides, not auto-substitution variables. Replace each one with the corresponding value from the input data.

| Placeholder | Required | Source | Allowed values |
|-------------|:--------:|--------|----------------|
| `{{meeting_title}}` | yes | notes / chat | text — meeting topic |
| `{{project_name}}` | yes | session context | text |
| `{{meeting_date}}` | yes | notes / chat | YYYY-MM-DD |
| `{{meeting_type}}` | yes | notes / agent | see type reference §3 or custom |
| `{{facilitator}}` | yes | notes | name or `[clarify]` |
| `{{source_notes}}` | yes | agent | description of notes source |
| `{{participant_name}}` | yes (≥1) | notes | participant name |
| `{{role}}` | yes (≥1) | notes / context | project role |
| `{{agenda_item}}` | yes (≥1) | notes | topic formulation |
| `{{decision}}` | no | notes | decision formulation |
| `{{initiator}}` | no | notes | name or `[clarify]` |
| `{{action_item}}` | no | notes | specific action |
| `{{owner}}` | no | notes | name or `[clarify]` |
| `{{deadline}}` | no | notes | YYYY-MM-DD / relative deadline / `[clarify]` |
| `{{change_item}}` | no | notes + plan | element ID (WP-xxx/Mx) or text |
| `{{old_value}}` | no | project plan | value from plan |
| `{{new_value}}` | no | notes | new value |
| `{{open_question}}` | no | notes | question formulation |
| `{{next_meeting_date}}` | no | notes | YYYY-MM-DD or `[clarify]` |
| `{{next_meeting_topic}}` | no | notes | text |

---

## 5. Validation Checklist

Before showing the result to the user — verify:

- [ ] All required placeholders replaced with values
- [ ] No `{{}}` placeholders remaining in text (except `[clarify]`)
- [ ] Meeting date is present and correct
- [ ] Agenda: ≥1 item, each with a status
- [ ] Decisions (if any): IDs sequential (D001, D002, ...), formulations specific
- [ ] Action items (if any): IDs sequential (A001, A002, ...), each with owner, deadline, priority (or `[clarify]`)
- [ ] Section 5: deleted if no changes. If present and plan is available — plan element IDs (WP-xxx/Mx) specified. Each change linked to a decision (D00x)
- [ ] Section 6: deleted if no open issues
- [ ] Section 7: deleted if not discussed
- [ ] All agent assumptions and `[clarify]` markers listed when delivering the result
- [ ] Document status = `draft`
- [ ] Filename in header = `meeting-protocol-YYYY-MM-DD.md`

---

## 6. Dependencies

**Consumes (input):**
- Meeting notes — from user (via chat or knowledge)
- `project-plan.md` — project plan (optional, for ID linking)

**Produces (output):** meeting protocol → consumed by (system-prompt-draft.md §7):
- `generate-project-plan` — if section 5 contains changes, the plan needs updating
- Does not block other skills. Independent artifact.

**Note:** this skill is not part of a fixed chain. It can be invoked in any project phase when meeting notes are available.

After approval, the user needs to upload `meeting-protocol-{date}.md` to project knowledge (if required by other tasks).

---

## 7. Call Example

**User command:**

> Оформи протокол. Заметки со встречи:
> - были Алексей, Елена, я
> - обсудили результаты прототипа — решили идти с вариантом B
> - Елена подготовит финальный дизайн до 15 апреля
> - сроки MVP сдвигаются на 2 недели из-за доработок
> - следующая встреча — 10 апреля, обсуждение плана

**Agent response:**

> Сформирован протокол встречи 2026-04-03 на основе: заметки PM (чат).
>
> Итоги: 1 решение, 1 задача, 1 изменение в плане.
>
> Допущения:
> - Тип встречи: «Демо/ревью» (определён по содержанию — обсуждение результатов прототипа).
> - Ведущий: [уточнить] (не указан в заметках).
> - Приоритет задачи A001: В (привязана к ближайшей вехе MVP).
> - План проекта не предоставлен — изменения описаны текстом, ID элементов не указаны.
>
> Требуется: утвердить, внести замечания или отклонить. Уточнить: ведущий встречи.
>
> [текст протокола]

---

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-26 | 1.0 | Skill created. Free-form input. Conditional sections 5/6/7 with deletion rules. ID linking when plan is available. Meeting type reference. 20 placeholders |
| 2026-03-28 | 1.1 | Translated to English. Added Language Detection block and bilingual triggers |
