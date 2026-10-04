---
name: north-star-metric-auditor
description: "Audit a North Star Metric against 4 criteria and propose 2–3 business-model-fit alternatives. Use when evaluating your NSM, choosing a new metric, or preparing a strategy review. Triggers: 'audit north star metric', 'is my NSM correct', 'аудит north star metric', 'проверь нашу NSM'."
version: 1.0.0
---

# North Star Metric Auditor

This skill audits a North Star Metric (NSM) against 4 standard criteria and proposes 2–3 alternative candidates calibrated to the stated business model.

**Input:**
- Current NSM (metric name; optionally, how it is measured)
- Business model description (1–3 sentences: product type, revenue model, core user value)
- Optional: strategic focus area (growth / retention / monetisation)

**Output:**
- Markdown audit report: criteria table with 4 ratings, overall verdict (Strong / Acceptable / Weak), 2–3 alternatives with trade-offs, and a single actionable recommendation

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Parse Input

1. Extract the NSM name and measurement definition (if provided).
   - If no NSM provided: stop and ask for it **in the user's language** (per Language Detection). EN: "Please share your current North Star Metric. Example: 'weekly active users'." RU: «Укажи свою текущую North Star Metric. Например: „количество еженедельно активных пользователей“.»
2. Extract the business model description.
   - If missing: ask one focused question before continuing to Step 4 (alternatives): "What is your product type and how do you earn revenue?"
3. Extract optional strategic focus if stated (growth / retention / monetisation).

### Step 2: Audit Against 4 Criteria

Evaluate the NSM against each criterion. For each, assign a rating (**Strong**, **Acceptable**, or **Weak**) and write 1–2 sentences of concrete justification tied to the stated NSM and business model.

1. **Customer Value:** Does the metric capture the moment users receive the product's core value? A strong NSM rises when users succeed, not just when they open the app.
2. **Revenue Predictability:** Does growth in this metric reliably predict long-term revenue growth or retention? Lagging financial output metrics score Weak here.
3. **Team Actionability:** Can the product team directly influence this metric through product decisions? Metrics driven primarily by external factors (seasonality, macro) score lower.
4. **Leading Indicator:** Is this an early signal of future success rather than a trailing summary of past results? Revenue and profit are classic lagging metrics and score Weak.

**Edge Cases:**
- Multiple metrics provided: audit each against all 4 criteria; rank by overall verdict; recommend the strongest.
- Composite metric (e.g., "engagement score = sessions × depth"): evaluate as one unit; note in Criterion 3 that composites score lower on actionability and flag measurement complexity.
- Pre-PMF product: note NSM is most useful post-PMF; suggest an activation event as an interim proxy; complete the audit normally.

### Step 3: Deliver Overall Verdict

1. Count Strong / Acceptable / Weak ratings across the 4 criteria.
2. Assign verdict:
   - **Strong** — 3–4 Strong, no Weak
   - **Acceptable** — mix of Strong/Acceptable, at most 1 Weak
   - **Weak** — 2+ Weak ratings
3. Write one sentence summarising the main strength (if Strong/Acceptable) or the main weakness (if Weak/Acceptable).

### Step 4: Propose Alternatives

1. Generate 2–3 alternative NSM candidates calibrated to the stated business model, prioritising candidates that score stronger on the criteria where the current NSM is Weak.

   Common candidates by model:
   - **B2B SaaS subscription** → seats activated, time-to-value, feature adoption depth
   - **B2C freemium** → weekly engaged users, activation rate, habit-loop completions
   - **Marketplace** → successful transactions, GMV per active user, repeat purchase rate
   - **Content/media** → weekly content-consuming sessions, content completion rate

2. For each alternative:
   - *Why it fits:* how it addresses the main weakness of the current NSM
   - *Potential downside:* one measurement challenge or structural risk

### Step 5: Recommend

1. If current NSM is **Strong**: recommend keeping it; optionally suggest one measurement improvement.
2. If **Acceptable** or **Weak**: recommend switching to the top-ranked alternative; add one concrete next step (e.g., "instrument the event in analytics within 2 weeks").

---

## Negative Cases

- **No metric provided:** Stop and ask **in the user's language** (per Language Detection). EN: "Please share your North Star Metric. Example: 'weekly active users' or 'monthly active listeners'." RU: «Укажи свою North Star Metric. Например: „количество еженедельно активных пользователей“.»
- **Financial metric as NSM (revenue, MRR, GMV, profit):** Warn: "Revenue is an output metric — it reflects past decisions and is hard to act on directly. A strong NSM should predict revenue, not be revenue." Then complete the audit (revenue scores Weak on criteria 1, 3, 4) and propose alternatives.
- **Vague input (e.g., "engagement" with no definition):** Ask: "How do you measure engagement? (e.g., DAU, average session length, feature X activations)" before proceeding.

---

## Output Format

Respond in the user's language with this structure:

```
## [Аудит North Star Metric / North Star Metric Audit]: [Metric name]

### [Оценка по 4 критериям / Criteria Assessment]

| [Критерий / Criterion] | [Оценка / Rating] | [Обоснование / Justification] |
|------------------------|-------------------|-------------------------------|
| [Ценность для пользователя / Customer Value] | Strong / Acceptable / Weak | [1–2 sentences] |
| [Предиктивность роста / Revenue Predictability] | Strong / Acceptable / Weak | [1–2 sentences] |
| [Управляемость командой / Team Actionability] | Strong / Acceptable / Weak | [1–2 sentences] |
| [Опережающий индикатор / Leading Indicator] | Strong / Acceptable / Weak | [1–2 sentences] |

### [Итоговый вердикт / Overall Verdict]: [Strong / Acceptable / Weak]
[1 sentence: main strength or weakness]

---

### [Альтернативные кандидаты / Alternatives] ([бизнес-модель / business model]: [model])

#### 1. [Metric name]
- **[Почему подходит / Why it fits]:** ...
- **[Потенциальный минус / Potential downside]:** ...

#### 2. [Metric name]
- **[Почему подходит / Why it fits]:** ...
- **[Потенциальный минус / Potential downside]:** ...

#### 3. [Metric name] *(optional)*
- **[Почему подходит / Why it fits]:** ...
- **[Потенциальный минус / Potential downside]:** ...

---

### [Рекомендация / Recommendation]
[Keep current NSM or switch to alternative #N with one concrete next step]
```

**Field rules:**
- Rating values: Strong / Acceptable / Weak only (no other values)
- Justification: specific to the stated NSM and business model (no generic statements)
- Alternatives: calibrated to the stated business model
- Recommendation: one sentence with a specific, actionable next step
