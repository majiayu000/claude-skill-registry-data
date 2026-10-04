---
name: weekly-status-report-generator
description: "Transform raw weekly notes into two reports in one pass: detailed Manager Report and 3-point Skip-Level Brief. Use when sending your weekly update. Triggers: 'write my weekly status report', 'weekly status report', 'напиши мой статус-отчёт', 'еженедельный статус-отчёт', 'преобразуй заметки в отчёт'."
version: 1.0.0
---

# Weekly Status Report Generator

This skill transforms unstructured weekly notes into two ready-to-send status report formats: a detailed Manager Report and a concise 3-point Skip-Level Brief, all in a single pass.

**Input:**
- Raw weekly notes — any format: free text, pasted Slack messages, bullet list, incomplete sentences

**Output:**
- Manager Report: structured markdown with Done, In Progress, Blockers, and Next Week sections
- Skip-Level Brief: 3-point summary (top result, main challenge, next-week focus)

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Accept and Validate Input

1. Accept the user's raw weekly notes (free-form text, bullet list, pasted Slack messages, or any mix).
2. If input is empty or contains only whitespace:
   - Respond: "Paste your weekly notes — tasks, meetings, wins, blockers — and I'll generate both reports. / Вставь заметки недели — задачи, встречи, достижения, блокеры — и я сгенерирую оба отчёта."
   - Stop — do not proceed to extraction.
3. If input is clearly off-topic (e.g., code review, creative writing, unrelated question):
   - Respond: "This skill generates a weekly status report from your notes. Paste your weekly notes to get started. / Этот скилл генерирует статус-отчёт по заметкам рабочей недели. Вставь свои заметки."
   - Stop.

### Step 2: Extract Structured Items

1. Read through the notes and identify:
   - **Done:** completed tasks, shipped deliverables, finished meetings with outcomes, closed items
   - **In Progress:** ongoing work, started but unfinished tasks, running experiments
   - **Blockers:** anything preventing progress, waiting on others, unresolved dependencies
   - **Metrics:** any numeric data mentioned (percentages, counts, amounts) — preserve verbatim
   - **Next Week:** plans, upcoming tasks, scheduled meetings with expected outcomes
2. If no blockers are mentioned: treat Blockers as empty; handle in Step 3.
3. If only future-tense content exists (no completed items): flag it and continue — mark the Done section with "No completed items mentioned."; generate the Next Week section from the notes; prefix the output with: "No completed items found in notes. Manager Report shows only upcoming work."

### Step 3: Generate Manager Report

1. Build a structured markdown section with the heading:
   - EN: **"Status Report — Week of [date]"**
   - RU: **"Статус-отчёт — Неделя [дата]"**
   - If the user did not mention a date, omit it from the heading.
2. Include the following subsections in order:
   - **Done / Выполнено:** bullet list of completed items
   - **In Progress / В работе:** bullet list of ongoing items
   - **Blockers / Блокеры:** bullet list of blockers; if none, write "No blockers this week / Блокеров нет"
   - **Next Week / На следующей неделе:** bullet list of upcoming plans
3. Preserve any numeric metrics verbatim in the relevant section.
4. Each bullet: one item per line, concise and specific.

**Edge Cases:**
- Notes contain only 1–2 items: generate both reports with available data; prefix the output (before the first report heading) with: "Notes are brief — consider adding In Progress or Next Week items for a fuller report."
- Notes are in mixed EN + RU: detect dominant language; generate both formats in dominant language; do not mix languages within a single format.
- Notes contain metric numbers (e.g., "conversion 4.2% → 4.7%"): preserve the metric in the Done section and include it in the Skip-Level top-result bullet.
- Input is very long (>500 words, e.g., Slack export or full meeting notes): extract only week-relevant items; prefix the output with "Extracted weekly status from provided notes."

### Step 4: Generate Skip-Level Brief

1. Build a 3-bullet section with the heading:
   - EN: **"Skip-Level Brief"**
   - RU: **"Краткий апдейт для skip-level"**
2. Each bullet is exactly one sentence, labeled:
   - **Top result / Топ-результат:** the single biggest impact or win of the week
   - **Main challenge / Главная сложность:** the most significant blocker, challenge, or dependency
   - **Next week focus / Фокус следующей недели:** the highest-priority task or goal for the coming week
3. If no blockers were found: rephrase "Main challenge" as the most significant stretch goal or dependency encountered this week.
4. Keep each bullet under 20 words — executive-summary style, factual, no filler.

### Step 5: Output Both Reports

1. Present both reports in a single response, clearly separated.
2. Order: Manager Report first → horizontal rule (`---`) → Skip-Level Brief second.
3. No meta-commentary between or after the two sections — output is copy-paste ready.
4. **Exception — scope or completeness notes:** If a scope note or completeness advisory was triggered (e.g., long input >500 words, only 1–2 items, or future-only notes), place that note as a single line BEFORE the first report heading, not after the last report block. This keeps the two report blocks clean and copy-paste ready while still surfacing the advisory.

---

## Output Format

Single markdown response with two labeled sections:

```markdown
## Status Report — Week of [date]

### Done
- [task or deliverable]

### In Progress
- [ongoing item]

### Blockers
- [blocker] / No blockers this week

### Next Week
- [planned item]

---

## Skip-Level Brief

1. **Top result:** [one sentence — biggest impact or win this week]
2. **Main challenge:** [one sentence — key challenge, blocker, or dependency]
3. **Next week focus:** [one sentence — most important priority ahead]
```

**Russian variant** uses section headers: Выполнено / В работе / Блокеры / На следующей неделе; Skip-Level labels: Топ-результат / Главная сложность / Фокус следующей недели.

**Rules:**
- Manager Report: Done, In Progress, Blockers, and Next Week sections are always present
- Blockers section is always present (write "No blockers this week" if empty — never omit the section)
- Skip-Level Brief: exactly 3 numbered bullets, each labeled
- All metric values from notes preserved verbatim
- No trailing commentary after the last report block (scope/completeness notes appear before the first report heading, not after)

---

## Negative Cases

- **Empty input:** Respond with the bilingual prompt (see Step 1) and stop.
- **Off-topic input:** Explain the skill's purpose and stop (see Step 1).
- **Notes contain only future plans, no past-week data:** Mark Done section as "No completed items mentioned."; prefix output with "No completed items found in notes. Manager Report shows only upcoming work." The Skip-Level third bullet uses available data.
