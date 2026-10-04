---
name: campaign-retrospective-writer
description: "Analyse a completed marketing campaign and produce a structured retrospective: goal vs. result, channel breakdown, what worked/didn't, recommendations, and trend line. Triggers: 'write campaign retrospective', 'campaign debrief', 'напиши ретро по кампании', 'разбор кампании'."
version: 1.0.0
---

# Campaign Retrospective Writer

Этот скилл собирает структурный ретро-разбор завершённой маркетинговой кампании на основе вставленных метрик и заметок. Результат: 6-секционный Markdown-документ — цель/факт, разбор по каналам, что сработало/нет, гипотезы причин, рекомендации и строка тренда.

**Ввод:**
- Метрики и/или заметки по завершённой кампании (свободный текст, paste)
- Опционально: цель, тип кампании, период, каналы

**Вывод:**
- Markdown-ретро с 6 разделами

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check if the user provided any campaign data (metrics, notes, results)
   - If input is empty: **stop**. Return bilingual prompt:
     > «Вставьте метрики или заметки по завершённой кампании.  
     > Paste metrics or notes from a completed campaign.»
   - Do not proceed to Step 2

2. Check if the campaign appears to be **active** (ongoing, in-progress language such as "we are running", "current campaign")
   - If yes: warn the user before proceeding:
     > «Кампания выглядит активной — ретро эффективнее после завершения. Продолжить? /  
     > Campaign appears ongoing — retrospectives are more useful after completion. Continue?»
   - Wait for confirmation before proceeding

### Step 2: Extract Campaign Context

1. Parse the input for:
   - Campaign name or type (email, paid, event, content, SMM, or other)
   - Campaign goal (target metric and value)
   - Period (start date — end date)
   - Channels used

2. If any of these are missing and not inferable from the input:
   - Ask for missing context in a single consolidated prompt (do not ask field by field)
   - Example: «Укажите: (1) тип кампании, (2) цель, (3) период, (4) каналы — или то, что помните.»

**Edge Cases:**
- EC3: Multiple campaigns in one input → ask which one to process; if no answer, process the first one and add note: «Обработана первая кампания; укажите название для остальных.»
- EC4: Mixed-language input (EN + RU) → respond in the language of the majority; at 50/50 — respond in the language of the latest user message

### Step 3: Build Goal vs. Result Table

1. Extract key campaign metrics from the input (CTR, conversions, reach, revenue, etc.)
2. For each metric, record: target value | actual value | delta (%)
3. If target was not stated: mark goal column as «—»
4. If actual value is missing: mark as «н/д» / «n/a» — **never invent numbers**

**Edge Cases:**
- EC2: Only qualitative notes, no numeric metrics → populate table with «н/д» in numeric cells; add note: «Числовые метрики не предоставлены — дополните таблицу вручную.»

### Step 4: Build Channel Breakdown Table

1. For each channel identified in Step 2:
   - List the key metric for that channel (e.g., Email → open rate; Paid → CPC; SMM → engagement rate)
   - Record the result
   - Mark as ✅ (worked) or ❌ (didn't work) based on input context or goal achievement
2. If only one channel: single-row table is valid

**Edge Cases:**
- EC1: Only quantitative data (no qualitative context) → complete the table; mark «What Worked» section as «Добавьте качественный контекст вручную.»
- EC2: Only qualitative notes, no numeric results → mark the Result column as «н/д» / «n/a» for all channels; still assign ✅/❌ based on qualitative context where possible.

### Step 5: Generate What Worked / What Didn't + Hypotheses

1. Create two lists based on the input and the Channel Breakdown table:
   - **What Worked**: positive outcomes with an explicit hypothesis of cause
   - **What Didn't Work**: underperforming areas with an explicit hypothesis of cause
2. Mark every hypothesis with the label **(гипотеза)** / **(hypothesis)** — never present hypotheses as facts
3. Minimum 1 item in each list; if the input doesn't support separation, write: «Недостаточно данных — дополните вручную.»

### Step 6: Write Recommendations

1. Generate three sub-lists based on Steps 4 and 5:
   - **Повторить / Repeat**: what worked and should be replicated
   - **Изменить / Adjust**: what showed promise but needs refinement
   - **Убрать / Drop**: what didn't work and should be removed

### Step 7: Add Trend Line

1. Write exactly **one line** summarising the campaign for cross-campaign tracking:
   - Format: `[Campaign name/type] [period]: [key metric], [delta vs. prev if known] — [1-line takeaway]`
   - Example: `Email Q2-2026: CTR 2.4%, +0.6% vs. Q1 — A/B subject line test drove the uplift`
2. If no previous campaign data is available: omit delta; note «нет данных для сравнения / no prior data»

---

## Negative Cases

- **Empty input (NEG1):** No metrics or notes provided → stop immediately (see Step 1)
- **Active campaign (NEG2):** Campaign appears ongoing → warn + require confirmation before proceeding
- **No channels identified:** Cannot determine any channel from input → ask in Step 2 consolidated prompt
- **Goal only, no results:** If user provides only the goal with no actuals → produce template with «н/д» cells; note that ретро requires actual results to be meaningful

---

## Output Format

Output a Markdown document with this structure:

```
## Campaign Retrospective: [Campaign Name]

**Тип / Type:** [email / paid / event / content / SMM / other]
**Период / Period:** [YYYY-MM-DD — YYYY-MM-DD]
**Каналы / Channels:** [comma-separated list]

---

### 1. Goal vs. Result

| Метрика / Metric | Цель / Goal | Факт / Actual | Δ% |
|-----------------|-------------|---------------|----|
| [metric]        | [target]    | [actual]      | [+/-%] |

---

### 2. Channel Breakdown

| Канал / Channel | Ключевая метрика / Key Metric | Результат / Result | Итог / Verdict |
|----------------|------------------------------|-------------------|----------------|
| [channel]      | [metric]                     | [value]           | ✅ / ❌ |

---

### 3. What Worked
- [outcome] — **(гипотеза / hypothesis): [reason]**

### 4. What Didn't Work
- [outcome] — **(гипотеза / hypothesis): [reason]**

---

### 5. Recommendations

**Повторить / Repeat:** [list]
**Изменить / Adjust:** [list]
**Убрать / Drop:** [list]

---

### 6. Trend Line
`[Campaign name] [period]: [key metric], [delta] — [1-line takeaway]`
```

**Field rules:**
- All numeric cells with missing data: «н/д» / «n/a» (never invent values)
- Hypotheses always labelled **(гипотеза)** / **(hypothesis)**
- Trend Line is exactly one line
- Section headers are bilingual (RU/EN) when responding in Russian; English-only when responding in English
