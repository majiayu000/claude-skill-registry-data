---
name: okr-progress-narrator
description: "Transform raw OKR data (metrics, percentages, notes) from files or pasted text into a readable narrative progress update for stakeholders. Use when preparing weekly or quarterly OKR reports, board updates, or team syncs. Triggers: 'okr update', 'narrate okr progress', 'stakeholder okr update', 'generate okr report', 'okr status update', 'окр апдейт', 'нарратив по OKR', 'прогресс-апдейт для стейкхолдеров', 'оформи OKR', 'прогресс по целям'."
version: 1.0.0
---

# OKR Progress Narrator

This skill takes raw OKR data — tables, lists, or free-form notes with objectives, key results, current values, and targets — and converts them into a structured narrative progress update in `okr-update-YYYY-MM-DD.md`. The output is designed to be shared directly with stakeholders: executive summary, per-objective narrative, KR status table, risks, and next steps.

**Input:**
- OKR data as a file (`.md`, `.txt`, `.csv`) or pasted text in chat
- Optional: period label (Q1 2026, Sprint 12), audience (CEO, board, team), tone

**Output:**
- `okr-update-YYYY-MM-DD.md` — narrative update with executive summary, per-objective sections, and risk block

---

## Language Detection

Detect the user's language from their message and OKR data:
- If Russian (or Cyrillic content): respond and write the output document in Russian, using the output template below with translated section headers (e.g., "Итоговая сводка", "Цели", "Ключевые риски", "Следующие шаги")
- If English: respond and write the output document in English with standard headers
- If ambiguous: use the language of the trigger phrase
- Translate objective/KR names to the output language if the source is mixed-language

---

## Instructions

### Step 1: Validate and Parse Input

1. Identify the input source:
   - **File path provided:** Read the file. Supported formats: `.md`, `.txt`, `.csv`
   - **Text pasted in chat:** Use the message content directly
   - **No input provided:** Ask the user via AskUserQuestion to provide OKR data (file or paste)

2. Parse OKR structure — detect one of these layouts:
   - **Markdown table:** columns map to Objective / Key Result / Current / Target / %Progress / Status / Notes
   - **Indented list:** `Objective:` or `O1:` as headers, `- KR:` or `KR1.1:` as children
   - **CSV/TSV:** use header row to identify columns
   - **Free-form text:** extract Objective/KR pairs using keyword matching (Objective, Goal, KR, Key Result, Target, Цель, КР, Результат)

3. For each Key Result, identify:
   - Name / description
   - Current value (numeric or qualitative)
   - Target value (if present)
   - Direction: whether higher or lower values are better (default: higher is better)
     - If metric name contains keywords like "churn", "rate" (in negative context), "cost", "time", "latency", "errors": assume lower is better
     - Otherwise: higher is better
   - % progress (compute if current + target present):
     - If higher is better: `round(current / target * 100)`
     - If lower is better and current ≤ target: `✅ exceeded (goal met)`
     - If lower is better and current > target: shortfall percentage = `round(((current - target) / target) * 100)` (used to classify severity, not as actual progress)
   - Status (on track / at risk / off track) — use provided value, or derive from % (see Step 2)
   - Notes / context (optional)

4. If file cannot be read or OKR structure is unrecognizable:
   - Stop. Report: "Could not recognize OKR structure in [filename / input]. Please provide data with Objective and Key Result fields."

5. Capture optional parameters:
   - Period: from user message or file metadata (e.g., "Q2 2026", "April")
   - Audience: CEO / board / team / general (default: general)
   - Tone: formal / conversational (default: formal)
   - Focus: all / at-risk-only / highlights-only (default: all)

### Step 2: Classify Status

For each Key Result:

1. If status is explicitly provided in the data → use it as-is
2. If status is absent but a qualitative marker is present (e.g., "done", "completed", "✅", "achieved"):
   - Mark as `✅ exceeded` if the description indicates completion or overachievement
3. If status is absent but notes or context suggest risk (e.g., "blocked", "slipped", "at risk", "delayed", "behind"):
   - Mark as `🟡 at risk` (even if percentage is on track)
   - Exception: if notes clearly describe a temporary issue and the underlying metrics are strong, use percentage-based classification
4. If status is absent but % progress is computable:
   - **For "higher is better" metrics:**
     - Determine metric category and apply appropriate threshold:
       - Business-critical metrics (keywords: "revenue", "MRR", "ARR", "sales", "deal", "customer value", "engagement", "retention", "growth"): ≥ 85% on track
       - All other operational/technical metrics: ≥ 70% on track
     - Based on category:
       - ≥ threshold: `🟢 on track`
       - 50%–(threshold-1)%: `🟡 at risk`
       - < 50%: `🔴 off track`
       - > 100%: `✅ exceeded`
   - **For "lower is better" metrics (e.g., churn, cost, latency):**
     - If current ≤ target: `✅ exceeded` (goal met)
     - If current > target: classify by shortfall percentage = `((current - target) / target) * 100`
       - Shortfall > 20%: `🔴 off track` (significantly worse than target)
       - Shortfall 10–20%: `🟡 at risk` (moderately worse than target)
       - Shortfall ≤ 10%: `🟢 on track` (slightly worse but within acceptable margin)
5. If neither status nor numeric data is available:
   - Mark as `⬜ no data` — do not invent a status

Derive Objective status:
- 🟢 if all KRs are on track or exceeded
- 🟡 if any KR is at risk
- 🔴 if any KR is off track
- ⬜ if all KRs have no data

### Step 3: Generate Narrative

For each Objective:

1. Write a **narrative paragraph** (2–4 sentences):
   - What has been achieved so far
   - What the current state implies (momentum, risk, or completion)
   - If notes/context are available → weave them in naturally
   - Do NOT repeat exact numbers already shown in the KR table
   - Do NOT invent reasons for low progress if not provided in data

2. Adapt to audience:
   - **CEO / board:** 
     - Lead with business impact and strategic implications
     - Skip implementation details, engineering blockers, tactical issues
     - Use outcome-focused language: "revenue target within reach", "market opportunity", "delivery risk identified", "strategic pivot needed"
     - Emphasize why each KR matters to the business
     - For at-risk items: state the business impact and mitigation approach (if known)
   - **Team:** Include operational detail, blockers, dependencies, and next steps if present
   - **General (default):** Neutral business tone. Balanced detail — progress + context without excessive implementation specifics

3. Apply focus filter if specified:
   - `at-risk-only`: include only 🟡 and 🔴 objectives in per-objective sections
   - `highlights-only`: include only 🟢 and ✅ objectives
   - `all` (default): include all objectives

**Edge Cases:**
- KR with % > 100: show as-is, mark `✅ exceeded`, phrase as achievement in narrative (e.g., "exceeded target by X%")
- KR with no numeric data and no notes: write "Data not yet reported for this period"
- All KRs are 🟢 or ✅: omit "Key Risks" section entirely; do not force a risk if none exists
- Only 1 KR with no parent Objective: group under a generic "Overall Metrics" (or in Russian: "Ключевые метрики") objective header; create a single objective section
- Mixed languages in data (EN objective names + RU notes): normalize to the output language (use output language setting from Step 1); translate objective/KR names and notes if needed

### Step 4: Generate Executive Summary

Write 2–4 sentences covering:
1. How many objectives are on track / at risk / off track (e.g., "2 of 3 objectives are on track")
2. Top highlight: the best-performing KR or achieved milestone
3. Top risk: the most critical at-risk or off-track item (skip if none)

Keep the summary self-contained — it should make sense without reading the full document.

### Step 5: Compile Document

Assemble the output using the template below. Apply these rules:
- Omit "Key Risks" section if all KRs are on track (🟢) or exceeded (✅); always include it if any KR is 🟡 or 🔴
- Omit "Next Steps" section if no next-step data, action items, or blockers are present in the input or notes
- Use period label if provided (e.g., "Q2 2026", "April"); otherwise use "Current Period"
- Round all percentages to nearest whole number
- If audience is CEO: ensure narrative is outcome-focused and strategic; remove tactical details

### Step 6: Save Output

1. Write file as `okr-update-YYYY-MM-DD.md` (today's date)
2. Save to:
   - The folder containing the input file (if file was provided)
   - The working directory (if text was pasted)
3. Confirm: "Saved: okr-update-[date].md — [N] objectives, [N] KRs. [N] at risk."

---

## Output Format

```markdown
# OKR Progress Update — [Period]
**Prepared:** YYYY-MM-DD
**Audience:** [if specified]

---

## Executive Summary

[2–4 sentences: overall status, top highlight, top risk]

---

## Objectives

### [Objective 1 Name] — 🟢 On Track

[Narrative paragraph: 2–4 sentences on progress, momentum, notable context]

| Key Result | Current | Target | Progress | Status |
|------------|---------|--------|----------|--------|
| [KR 1.1]   | [value] | [value]| [%]      | 🟢     |
| [KR 1.2]   | [value] | [value]| [%]      | 🟡     |

---

### [Objective 2 Name] — 🔴 Off Track

[Narrative paragraph]

| Key Result | Current | Target | Progress | Status |
|------------|---------|--------|----------|--------|
| [KR 2.1]   | [value] | [value]| [%]      | 🔴     |

---

## Key Risks

| Key Result | Objective | Status | Context |
|------------|-----------|--------|---------|
| [KR name]  | [O name]  | 🔴     | [note]  |

---

## Next Steps

- [Next planned action if present in data]

---
*Generated by okr-progress-narrator · [date]*
```

---

## Negative Cases

- No input provided → ask for OKR data via AskUserQuestion; do not generate a blank document
- File path provided but file does not exist → stop; report exact path checked; ask user to verify
- Input file has no recognizable OKR structure → stop; report the file name; suggest format hint
- All objectives have no data (`⬜`) → generate document but flag in Executive Summary: "No quantitative data available for this period — narrative based on qualitative notes only"
- Period specified but data appears to be from a different period → include a note: "Note: data timestamps suggest this may be from [inferred period]. Review before sharing."
