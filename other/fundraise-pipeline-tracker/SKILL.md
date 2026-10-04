---
name: fundraise-pipeline-tracker
description: "Build a structured investor pipeline from pasted notes: Tier 1/2/3, per-investor status, next steps, follow-up priorities. Zero CRM. Bilingual EN/RU. Triggers: 'fundraise pipeline', 'track my investors', 'who should I follow up with', 'pipeline инвесторов', 'трекинг раунда', 'кому пора следить по инвесторам'."
version: 1.0.0
---

# Fundraise Pipeline Tracker

This skill assembles a structured investor pipeline from pasted meeting notes and round context for founders raising without a CRM. From raw investor notes, it generates a tiered pipeline (Tier 1/2/3), per-investor detail (status, next step, why us, feedback), and a prioritised Needs Action list separating "overdue next steps" from "gone silent."

**Input:**
- Pasted investor notes (free-form meeting notes, email summaries, bullet lists)
- Optional: round context (stage, target raise, timeline)

**Output:**
- Markdown document: Pipeline Table → Per-Investor Detail → Needs Action list

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check if the user has provided investor notes (any non-empty text describing investors).
   - If input is empty or whitespace only: stop and respond with the bilingual prompt:
     > "Вставь заметки по инвесторам (имя, фирма, статус, что обсуждали). / Paste your investor notes (name, firm, status, what was discussed)."
   - If the input looks like a pitch deck, financial model, or investor update email rather than tracking notes: redirect (see Negative Cases).

2. Extract optional round context if provided: stage (pre-seed / seed / Series A / other), target raise amount, timeline, lead status.

### Step 2: Parse Investor Entries

1. Identify each distinct investor mentioned in the notes.
   - Extract per investor: name, firm, investor type (VC / angel / strategic / family office / unknown).
   - Note the date of last contact if explicitly mentioned or inferable (e.g., "met last Monday", "Jun 12 call").
   - If no dates are present anywhere: flag this for Step 4.

2. Extract engagement signals for each investor:
   - Positive: term sheet, due diligence request, second meeting, "very interested", lead intent.
   - Neutral: first meeting done, intro made, pending follow-up.
   - Negative: passed, no response noted, "not the right time."
   - Silent: note says no reply, user says they haven't heard back.

### Step 3: Classify Investors into Tiers

Assign each investor exactly one tier based on engagement signals:

| Tier | Criteria |
|------|----------|
| Tier 1 | High engagement: term sheet / due diligence / lead candidate / strong positive signal from recent meeting |
| Tier 2 | Active but early: first meeting done, follow-up pending, warm but uncommitted |
| Tier 3 | Speculative or inactive: intro stage, not yet contacted, long silent, explicit pass |

If signals are ambiguous, default to the lower tier and note the uncertainty inline.

### Step 4: Extract Per-Investor Fields

For each investor, populate these fields (leave blank with note if information is not in the notes):

- **Status** — Current stage: first meeting / second meeting / due diligence / term sheet / passed / silent / not contacted
- **Next Step** — Specific action and deadline if mentioned (e.g., "Send cap table by Jun 28")
- **Why Us** — What resonated or what the investor expressed interest in
- **Feedback** — Objections, concerns, questions, or asks raised

**Edge Cases:**
- EC1 — No dates/timestamps in notes: classify by status signals only; add note: "Last-contact dates not found — silent/overdue detection based on explicit notes only."
- EC2 — Only one investor in notes: generate single-investor pipeline; place in Tier 1 by default; skip the tiering table; produce full per-investor detail.
- EC3 — Conflicting signals (warm response noted, but also "no reply for weeks" with a date): place in Tier 1 pipeline AND add to "Gone Silent" section with an inline conflict note.
- EC4 — Notes in mixed EN + RU: detect dominant language; generate output in dominant language; preserve investor names, firm names, and amounts as-is.
- EC5 — 20+ investors: process all; add executive summary card at top: totals by tier, total active vs. silent, top 3 critical actions.

### Step 5: Identify Follow-Up Priorities

1. **Overdue Next Steps** — investors where a Next Step was noted and either: (a) a deadline was given that has passed relative to the report date, or (b) the user explicitly marks it as overdue.
2. **Gone Silent** — investors where: (a) last-contact date is available and 14+ days have passed with no response signal, or (b) notes explicitly say "no reply" / "went quiet" / "не отвечает."
3. Sort overdue items by days overdue (longest first), then by tier. Sort silent items by days since last contact (longest first).

### Step 6: Generate the Document

Produce a single markdown document with three clearly labelled sections in the order below.

Use Russian section headers if the output language is Russian (see Output Format for both variants).

---

## Negative Cases

- **Empty input:** Respond with the bilingual prompt from Step 1.
- **Pitch deck or financial model pasted instead of investor notes:** Respond: "Это похоже на питч-дек или финансовую модель, а не трекинг инвесторов. Вставь заметки по встречам или статусы по инвесторам. / This looks like a pitch deck or financial model, not investor tracking notes. Paste meeting notes or investor statuses instead."
- **User asks to write an investor update email or newsletter:** Respond: "Этот скил строит статус-трекер, а не апдейт для инвесторов. Для ежемесячного апдейта инвесторов используй investor-update-composer. / This skill builds a pipeline tracker, not investor update messages. For a monthly investor update, use an investor-update-composer skill."

---

## Output Format

Single markdown document, three sections. Section headers in English or Russian depending on detected output language.

```markdown
# Investor Pipeline — [Round Stage] Round
**Report Date:** [date or "not provided"]
**Round:** [stage] | **Target:** [amount or "—"] | **Timeline:** [period or "—"]
**Investors tracked:** [N] | **Tier 1:** [N] | **Tier 2:** [N] | **Tier 3:** [N] | **Needs action:** [N]

---

## Pipeline Table

| Investor | Firm | Type | Tier | Status | Next Step | Why Us | Feedback |
|----------|------|------|------|--------|-----------|--------|----------|
| Jane Smith | Acme Ventures | VC | 1 | Due diligence | Send cap table by Jun 28 | Strong PMF signal | Wants 12-mo forecast |
| Ivan Petrov | — | Angel | 2 | First meeting done | Follow up — no reply 10d | Product demo impressed | Ticket size unclear |

---

## Per-Investor Detail

### Jane Smith — Acme Ventures (Tier 1)
- **Status:** Due diligence
- **Next Step:** Send cap table by Jun 28 ⚠️ overdue
- **Why Us:** Strong PMF signal, market size fit confirmed
- **Feedback:** Wants 12-month forecast; concerned about churn metric

---

## Needs Action

### 🔴 Overdue Next Steps
1. **Jane Smith (Acme Ventures)** — Send cap table. Due Jun 28 (overdue 2d)

### 🟡 Gone Silent
2. **Ivan Petrov** — No reply in 10 days. Last contact: Jun 13. Send follow-up.
```

**Russian section headers (use when output language is Russian):**
- "# Воронка инвесторов — Раунд [стадия]"
- "## Таблица пайплайна"
- "## Детали по инвестору"
- "## Требует внимания"
- "### 🔴 Просроченные next-step"
- "### 🟡 Потерял ответ"

**Field rules:**
- Blank fields: use "—" (do not leave empty cells)
- Next Step with deadline: include deadline date; mark "⚠️ overdue" if past
- Tier 3 investors may be collapsed into a brief table row only (no Per-Investor Detail section unless user requests it)
- Executive summary card (for 20+ investors): add above Pipeline Table with total outstanding, bucket distribution, top 3 critical actions
