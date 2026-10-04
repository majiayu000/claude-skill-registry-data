---
name: win-loss-debrief-writer
description: "Generate a structured win/loss debrief from closed deal notes: decision drivers, objections, competitive context, repeat/fix actions, deal trend row. No CRM. Triggers: 'win loss debrief', 'analyze this deal', 'we lost a deal help me understand why', 'разбор сделки', 'win/loss разбор', 'мы проиграли сделку — почему'."
version: 1.0.0
---

# Win/Loss Debrief Writer

This skill generates a structured win/loss debrief from closed deal notes for sales managers, founders, and account executives. Paste notes from any source (meeting notes, emails, CRM export, call transcript), and receive a full debrief with decision drivers, objections, competitive context, repeat/fix recommendations, and a single trend row ready to copy into a deal log.

**Input:**
- Pasted deal notes (free-form: meeting notes, emails, CRM export, Slack messages, call transcript excerpt)
- Optional: outcome (WON / LOST), deal size, industry, customer name, competitor name

**Output:**
- Single structured markdown document — five analysis sections + one trend row

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check whether the user has pasted deal notes.
   - If input is empty or whitespace only: respond billingually — "Вставь заметки по сделке (имя клиента, итог, что обсуждали). / Paste your deal notes (client name, outcome, what was discussed)." Then stop.

2. Detect content type.
   - If the pasted content looks like a proposal, quote, or forward-looking sales document (not closed-deal retrospective): respond — "Это похоже на коммерческое предложение, а не заметки по закрытой сделке. Для составления КП используй proposal-and-quote-drafter. / This looks like a proposal, not closed deal notes. For creating proposals, use proposal-and-quote-drafter." Then stop.
   - If the user is asking to write follow-up emails or active outreach: respond — "Этот скилл создаёт разбор закрытой сделки, а не активные follow-up письма. / This skill analyzes closed deals — not active follow-ups." Then stop.

3. Check for multiple deals in one paste.
   - If multiple deals are clearly delineated: process the first one; note — "Multiple deals detected — processed first entry. Paste one deal at a time for full analysis."

---

### Step 2: Identify Deal Outcome

1. Extract the outcome from notes or metadata: **WON**, **LOST**, or both perspectives.
2. If outcome is ambiguous or not stated: label outcome as "Outcome: unclear". Generate both WON and LOST variants for the Repeat/Fix section. Add a bilingual prompt: "Confirm outcome to refine Repeat/Fix section: WON or LOST? / Уточни итог сделки для раздела Что повторить / исправить: выиграна или проиграна?"
3. Extract metadata if present: customer/prospect name, deal size, industry, timeline, competitor.

---

### Step 3: Extract Decision Drivers

1. Identify the factors that influenced the buyer's final decision.
   - Look for signals in the notes: price mentions, feature comparisons, support or relationship references, timing, internal politics, budget constraints.
2. List 1–3 drivers, each as a concrete one-liner.
   - If no drivers can be extracted: mark as "Not available from notes."

---

### Step 4: Extract Objections Encountered

1. Find every objection raised during the deal cycle.
   - Look for phrases like "too expensive," "not sure about," "concerns about," "problem with," "competitor offers."
2. For each objection, extract:
   - The objection itself
   - How it was handled (if mentioned)
   - Status: **Resolved** / **Unresolved** / **Unknown**
3. If no objections found: note "None mentioned in notes."

---

### Step 5: Map Competitive Context

1. Identify competitors mentioned in the notes (by name or description).
   - If only a name is mentioned with no detail: note "limited competitor context — name only"; add "Research opportunity: build battlecard for [name]."
2. Record:
   - Competitor name(s) or "unknown" if not mentioned
   - Their edge (what they offered that you didn't)
   - Your edge (what you offered that they didn't)
   - Battlecard gap (what you lacked to counter them, or "none identified")
3. If no competitor mentioned: fill with "not mentioned" — never omit the section silently.

---

### Step 6: Generate Repeat / Fix Recommendations

1. Based on the outcome:
   - **WON**: List 1–3 things to repeat in future deals (what worked).
   - **LOST**: List 1–3 things to change or fix in future deals (what failed or was missing).
   - **Unclear or both**: Generate both Repeat and Fix sub-sections.
2. Recommendations must be specific and actionable (not "communicate better" — instead "introduce executive sponsor before final proposal stage").

---

### Step 7: Generate Trend Row

1. Produce a single copy-paste line summarising the deal for a running log or spreadsheet.
   - Format: `[Date] | [Customer] | [WON/LOST] | [Size] | [Competitor] | [Top Driver] | [Key Fix/Repeat]`
   - Use "—" for any field not available in the notes.
2. Add the prefix: `> Copy this line into your deal log or spreadsheet:`

---

### Step 8: Assemble and Output

1. Compile all sections into a single structured markdown document (see Output Format).
2. Translate all section headers if output language is Russian.
3. Validate:
   - Outcome is labeled (WON / LOST / Unclear)
   - Decision Drivers: at least 1 item or explicit "Not available from notes"
   - Objections table: present, with "None mentioned in notes" if empty
   - Competitive Context: present with explicit "unknown" or "not mentioned" values
   - Repeat/Fix: tailored to outcome
   - Trend row: produced as single line with available fields

**Edge Cases:**
- Notes very sparse (1–2 sentences): generate what's possible; mark unfilled fields explicitly as "Not available from notes"; append "Add more deal context for richer analysis."
- Notes in mixed EN + RU: detect dominant language; output in dominant language; preserve company names, person names, deal amounts as-is.

---

## Output Format

Single markdown document with this structure:

```markdown
# Win/Loss Debrief — [Customer/Prospect Name]
**Outcome:** [WON / LOST / Unclear]
**Date:** [date if available]
**Deal Size:** [amount or scope if available]
**Competitor:** [name(s) or "not mentioned"]

---

## Decision Drivers
What drove the final decision (buyer's perspective):
1. [Driver 1]
2. [Driver 2]
3. [Driver 3 if applicable]

## Objections Encountered
| Objection | How Handled | Status |
|-----------|-------------|--------|
| [e.g., "Too expensive"] | [e.g., "Offered payment plan"] | Resolved / Unresolved / Unknown |

## Competitive Context
- **Competitor:** [name or "unknown"]
- **Their edge:** [what they offered that you didn't]
- **Your edge:** [what you offered that they didn't]
- **Battlecard gap:** [what you lacked to counter them]

## What to Repeat / Fix
**[If WON] Repeat next time:**
- [e.g., "Executive sponsorship introduced early in the cycle"]

**[If LOST] Fix next time:**
- [e.g., "Address pricing objection with ROI calculator before final proposal"]

## Trend Row
> Copy this line into your deal log or spreadsheet:

`[Date] | [Customer] | [WON/LOST] | [Size] | [Competitor] | [Top Driver] | [Key Fix/Repeat]`
```

**Russian variant:** Use Russian section headers — Разбор win/loss / Факторы решения / Возражения / Конкурентный контекст / Что повторить / исправить / Строка тренда.

---

## Negative Cases

- **Empty input:** Respond bilingually listing required fields. Stop.
- **Proposal or quote pasted (not closed deal):** Redirect to proposal-and-quote-drafter. Stop.
- **User asks for follow-up email writing:** Redirect to a dedicated email skill. Stop.
