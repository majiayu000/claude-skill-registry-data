---
name: interview-debrief-synthesizer
description: "Synthesize notes from several interviewers into one comparable debrief: evidence vs impression, attributed, plus disagreements and unprobed competencies. Use after interviews. Triggers: 'interview debrief', 'synthesize interview notes', 'сведи заметки с интервью', 'дебриф по кандидату'."
version: 1.0.0
---

# Interview Debrief Synthesizer

This skill consolidates raw, inconsistently formatted notes from several interviewers into one comparable debrief. It separates what the candidate actually said or did (evidence) from evaluative claims with nothing behind them (impression), attributes every item to the interviewer who observed it, surfaces where interviewers contradict each other, and names the competencies nobody probed.

**Input:**
- Pasted interview notes from one or more interviewers — any mix of prose, bullets, ratings, fragments; RU, EN, or mixed
- Optional: a scorecard or role requirements; candidate names if several candidates are in play

**Output:**
- A single markdown debrief: evidence by competency, comparison matrix, disagreements, unprobed competencies, decision draft

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check that interview notes were actually provided.
   - If the message is empty or contains no notes: **stop**. Ask for the interview notes and, optionally, the scorecard. Produce no partial debrief.
   - If the input is a CV/resume or a job description rather than interview notes: **stop**. State the mismatch — this skill synthesizes what interviewers observed and cannot substitute a debrief from a resume. Name the correct input.

2. Determine the scope:
   - **One candidate** (default) — the matrix will be interviewers × competencies
   - **Several candidates** — the matrix will be candidates × competencies

**Edge Cases:**
- If notes cover several candidates interleaved: group by candidate first. Any block that cannot be attributed to a candidate with confidence goes under `unattributed` — never assign it by guessing.

### Step 2: Segment by Interviewer

1. Split the pasted text into per-interviewer blocks. Use names, headers, initials, or formatting shifts as boundaries.
2. Attribute every block to a named source.
3. Where a block has no author, label it `source not stated`. **Never guess an author** — attribution is what makes the debrief usable, and a wrong attribution is worse than none.
4. Record the interviewer count; it drives Step 5.

### Step 3: Establish the Competency Frame

1. If the user supplied a scorecard or role requirements: use those competencies **verbatim** as the frame. Label the frame `scorecard`.
2. If not: derive the frame from what the notes actually discuss. Label it `derived from notes — no scorecard provided`.
3. Carry the frame label into the output header — the reader must know whether "not probed" is measured against an authoritative list or against an inferred one.

**Edge Cases:**
- With a derived frame, state explicitly in the "Not probed" section that the list is incomplete: there is no authoritative set of competencies to compare against.

### Step 4: Classify Evidence vs. Impression

1. Go statement by statement through every interviewer block.
2. Classify each as:
   - **Evidence** — a concrete thing the candidate said, did, built, or decided. Quote it or paraphrase closely.
   - **Impression** — an evaluative claim (`strong`, `not senior enough`, `great culture fit`, `7/10`) with no observation attached.
3. **Never promote an impression into evidence by inventing a supporting detail.** If an interviewer wrote "strong system design" and nothing else, that is an impression, full stop.
4. Map each evidence item onto the competency frame, keeping the interviewer attribution attached.
5. For each competency, note whether it carries evidence, impressions only, or nothing.

For the classification rule, the ambiguous middle (a rating carrying a one-clause justification), and worked RU/EN examples, read `references/evidence-vs-impression.md`.

**Edge Cases:**
- Ratings on incompatible scales (1–5, ✓/✗, "yes with reservations"): report each in its **original form with its scale noted**. Never normalize onto a common scale, never average.
- Notes that are almost entirely impressions: produce the debrief with a near-empty evidence block and **lead with that finding** — the decision currently has no evidentiary basis. Then list, per interviewer, what they would need to be asked to convert their impression into evidence.
- Mixed-language notes: output in the language of the request, but quote each piece of evidence **in its original language** so nothing is distorted by translation.
- A statement whose grounds are a protected attribute (age, marital status, nationality, gender, health, pregnancy, religion): **do not classify it as evidence or impression and do not map it onto the competency frame.** Exclude it here, at classification time — it surfaces only as a Risks flag in the decision draft (Step 7, see Negative Cases).

### Step 5: Surface Disagreements

1. Compare interviewers competency by competency.
2. Flag a disagreement where:
   - two interviewers reach opposite conclusions on the same competency, or
   - two interviewers read the *same* behaviour differently (the more valuable case — the observation matches, the interpretation does not).
3. State both readings side by side with attribution.
4. **Do not resolve the disagreement.** Instead, phrase the one question that would settle it.

**Edge Cases:**
- Only one interviewer: omit this section entirely and replace it with a one-line note that cross-interviewer comparison is not possible with a single source. Do not invent a second perspective.

### Step 6: List Unprobed Competencies

1. Take the competency frame from Step 3.
2. List every competency that no interviewer touched — not "assessed weakly", but genuinely not covered.
3. For each, suggest what a follow-up conversation would need to ask.

### Step 7: Draft the Decision Write-Up

1. **Rests on:** the evidence-backed findings only.
2. **Still unknown:** gaps from Step 6 and unresolved disagreements from Step 5.
3. **Risks:** bias and protected-attribute flags (see Negative Cases).
4. End by leaving the decision to the user. **Emit no numeric score, no ranking, no hire/no-hire verdict.**

---

## Negative Cases

- **No notes provided / empty message:** Stop before producing any artifact. Ask for the interview notes and, optionally, the scorecard.
- **Resume or job description instead of interview notes:** Stop. State that this skill synthesizes interviewer observations and cannot build a debrief from a resume. Name the correct input.
- **Protected attributes used as grounds for assessment** (age, marital status, nationality, gender, health, pregnancy, religion): exclude that reasoning from the evidence and decision blocks. Flag it under **Risks** as an assessment resting on a protected attribute that should be excluded from the decision. Never carry it forward as a competency finding.
- **User asks for a final score, a ranking, or "just tell me who to hire":** deliver the debrief as specified and state plainly that the skill surfaces evidence and gaps, not a verdict — numeric scoring on a handful of notes would be false precision. Point at the open questions that would actually move the decision.

---

## Output Format

One markdown document. **All section headings are rendered in the language of the request** — nothing is hardcoded to English. Use this heading mapping:

| Section | English | Russian |
|---------|---------|---------|
| H2 title | Debrief: {candidate} — {role} | Дебриф: {кандидат} — {роль} |
| Header line | Sources / Competency frame | Источники / Рамка компетенций |
| 1 | Evidence by competency | Свидетельства по компетенциям |
| 2 | Comparison matrix | Матрица сравнения |
| 3 | Where interviewers disagree | Где интервьюеры расходятся |
| 4 | Not probed | Не проверено |
| 5 | Decision draft | Черновик решения |

Structure:

```markdown
## Debrief: {candidate} — {role}
Sources: {N} interviewers ({names}) · Competency frame: {scorecard | derived from notes}

### Evidence by competency

**{Competency}**
- {observed behaviour, quoted or closely paraphrased} — *{interviewer}*
- {…}
> Impression only, no evidence: {claim} — *{interviewer}*

### Comparison matrix

| | {Competency A} | {Competency B} |
|---|---|---|
| {candidate / interviewer} | {evidence, short} | — not probed |

### Where interviewers disagree

**{Competency}** — {Interviewer A}: {reading}. {Interviewer B}: {opposite reading}.
→ Question that would settle it: {question}

### Not probed

- {Competency} — nobody covered it. A follow-up would need to ask: {question}

### Decision draft

**Rests on:** {evidence-backed findings}
**Still unknown:** {gaps and unresolved disagreements}
**Risks:** {protected-attribute or bias flags, if any}

The decision is yours — this is the basis for it, not the verdict.
```

**Field rules:**
- Every evidence item ends with an attribution in italics, or the explicit label `source not stated`
- Impressions appear in blockquotes under their competency, never mixed into the evidence bullets
- Matrix cells carry short evidence, not scores; an untouched competency renders as `— not probed`
- Matrix orientation: candidates × competencies when several candidates are in play, interviewers × competencies for a single candidate
- The disagreement section always ends with a question, never with a resolution
- The decision draft never contains a score, a rank, or a verdict

For the full skeleton with both matrix variants and the single-interviewer degradation, read `references/debrief-template.md`.

---

## Key References

- **references/evidence-vs-impression.md**: The classification rule with worked RU/EN examples, the ambiguous middle (rating + one-clause justification), and the rule against inventing supporting detail. Consult during Step 4.
- **references/debrief-template.md**: Full output skeleton — multi-candidate matrix, single-candidate matrix, single-interviewer degradation, and the impressions-only variant. Consult during Step 7.
