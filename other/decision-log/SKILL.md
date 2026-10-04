---
name: decision-log
description: "Extracts structured decisions from meeting notes, Slack threads, or email
  chains and maintains a decision log separate from action items. Each decision is captured
  with context, alternatives considered, participants, date, and related tasks or risks.
  Supports two modes: new log creation and append to an existing log with deduplication.
  Use when you want to capture decisions from a meeting, update decision log, log decisions,
  extract decisions from discussion, build decision registry, add decisions to log."
version: 1.0.0
---

# Skill: decision-log

Extracts decisions from meeting notes, messages, and threads and builds a structured log —
separate from action items. Supports two modes: new log creation and appending to an
existing log with deduplication.

---

## Triggers

**Russian:** «зафиксируй решения», «залоги решения», «decision log», «лог решений», «извлеки решения из встречи», «обнови лог решений», «добавь решения в лог», «запиши решения»
**English:** "log decisions", "decision log", "extract decisions", "capture decisions from meeting", "update decision log", "add to decision log", "decisions from this meeting"

---

## Language Detection

Determine the language of the user's first message — it sets the language for the entire
conversation, output, and template.

| Input language | Output language | Template |
|----------------|-----------------|----------|
| Russian | Russian | `decision-log-template.ru.md` |
| English | English | `decision-log-template.md` |

---

## Input

**Required:**
- Text from a meeting, Slack thread, email chain, or meeting notes (any format)

**Optional:**
- Existing decision log (table or cards) — for append mode

**Parameters (specified explicitly or selected in Step 1):**
- Output format: `table` (markdown table) or `cards` (markdown cards)
- Mode: `new` (new log) or `append` (add to existing log)

## Output

A structured decision log in the chosen format.

Each record contains 6 fields:
1. **Decision** — precise formulation of the decision (1–2 sentences)
2. **Context** — why it was made: constraints, rationale, trigger
3. **Alternatives** — what was considered and why rejected (if mentioned)
4. **Participants** — who was involved in making the decision
5. **Date** — date (if stated in the text; otherwise blank)
6. **Related** — linked tasks, risks, dependencies (if mentioned)

---

## Instructions

### Step 1 — Determine mode and format

Determine mode and format from the request context:

| Condition | Mode | Action |
|-----------|------|--------|
| Only source text provided | `new` | Create log from scratch |
| Source text + existing log provided | `append` | Add new records |
| Format not specified | — | Ask the user |

If the output format is not specified explicitly, ask in the user's language:
- EN: "Which format do you prefer: table (one row per decision) or cards (one block per decision)?"
- RU: "Какой формат предпочтительнее: таблица (одна строка на решение) или карточки (отдельный блок на каждое решение)?"

Wait for the answer before processing.

### Step 2 — Extract decisions

Scan the text and identify all points where a decision was made.

**Decision signals** (as opposed to action items or information):
- Choice between options: "decided to use X instead of Y"
- Stated position: "agreed that...", "confirmed...", "approved..."
- Change of approach: "switching to...", "dropping..."
- Prioritization: "focusing on X, deferring Y"
- Implicit agreement: a clear brief response ("ok", "yeah", "sounds fine", "agreed",
  «ок», «хорошо», «договорились») to a proposal involving a choice — only if context
  makes it clear which option was accepted

**Do NOT extract:**
- Action items ("Ivan will do this by Friday")
- Informational statements with no choice involved
- Open questions and hypotheses

Fill in all 6 fields for each decision found. If a field is not mentioned in the text —
leave it blank or use a dash.

### Step 3 — Deduplication (append mode only)

Compare extracted decisions against the existing log.

Consider records duplicates if:
- The decision wording matches in meaning (different words are acceptable)
- Context and date match

When a duplicate is detected:
- Do not add the record again
- Note in the output: "[duplicate, skipped: brief wording]"

### Step 4 — Generate output

Use headings and labels matching the determined output language.

**Format `table` — EN:**

```markdown
| # | Decision | Context | Alternatives | Participants | Date | Related |
|---|----------|---------|--------------|--------------|------|---------|
| 1 | ... | ... | ... | ... | ... | ... |
```

**Format `table` — RU:**

```markdown
| # | Решение | Контекст | Альтернативы | Участники | Дата | Связанные |
|---|---------|----------|--------------|-----------|------|-----------|
| 1 | ... | ... | ... | ... | ... | ... |
```

**Format `cards` — EN:**

```markdown
### Decision 1: [short title]

- **Decision:** ...
- **Context:** ...
- **Alternatives:** ...
- **Participants:** ...
- **Date:** ...
- **Related:** ...
```

**Format `cards` — RU:**

```markdown
### Решение 1: [краткое название]

- **Решение:** ...
- **Контекст:** ...
- **Альтернативы:** ...
- **Участники:** ...
- **Дата:** ...
- **Связанные:** ...
```

After the output, add a brief summary: how many decisions found, how many are new
(in append mode), how many duplicates skipped.

---

## Templates

The skill uses files from `templates/`:

| File | Language | Purpose |
|------|----------|---------|
| `templates/decision-log-template.md` | EN | Blank log template (English) |
| `templates/decision-log-template.ru.md` | RU | Blank log template (Russian) |

---

## Constraints

- Does not extract action items — that is a separate domain
- Does not integrate with external systems directly (task trackers, messengers)
- Text input only — audio, video, and images are not supported
- Does not assess the quality or correctness of decisions
- Does not make recommendations or suggest alternatives
- If the source text contains no decisions — reports this explicitly and does not generate
  empty records
