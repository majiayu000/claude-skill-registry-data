---
name: proposal-and-quote-drafter
description: "Draft a client proposal and quote from discovery call notes or a brief. Turns raw, unstructured notes into scope, deliverables, timeline, three pricing packages, and a cover letter. Use when writing a client proposal, preparing a quote, или отправляешь КП после звонка. Triggers: 'write a client proposal', 'draft proposal and quote', 'turn my notes into a proposal', 'напиши предложение клиенту', 'пропозал и смета'."
version: 1.0.0
---

# Proposal and Quote Drafter

This skill turns raw notes from a discovery call or client brief into a complete, client-ready proposal: executive summary, scope, deliverables, timeline, three pricing packages, and a cover letter. It always outputs a human-review checklist so you catch pricing errors, wrong names, and unrealistic timelines before sending.

**Input:**
- Unstructured notes from a discovery call or client brief (pasted as text, any format, RU or EN)

**Output:**
- Full proposal document (Markdown)
- Cover letter (email-ready text block, 5–7 sentences)
- Human-review checklist (≥4 checkbox items)

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Validate Input

1. Check that the user has provided discovery notes or a brief.
   - If input is empty or fewer than 5 words: stop. Return: "Notes are too sparse to build a proposal. Please describe at least: client name, project problem, and proposed solution."
   - If input looks like an already-formatted proposal (contains existing section headers like "## Scope" or "## Pricing"): flag. Return: "This looks like an existing proposal. For revision, describe what to change. This skill generates from raw notes, not from existing documents." Stop.

2. Detect output language.
   - If the user's notes are predominantly in Russian → respond in Russian.
   - If the user explicitly requests a language (e.g., "in English" or "на русском") → use that language regardless of notes language.
   - Default: match the dominant language of the notes.

### Step 2: Parse Notes

Extract the following from the raw notes:

1. **Client information:** client name (company or individual), contact name if mentioned.
2. **Project type:** what kind of service or product is being proposed (e.g., website redesign, marketing campaign, consulting engagement).
3. **Pain points / problem:** what the client wants to solve or achieve.
4. **Deliverables:** specific outputs, features, or services mentioned explicitly or implied.
5. **Timeline:** deadlines, milestones, or constraints mentioned. If none found → note as [TIMELINE].
6. **Budget signals:** pricing, ranges, or constraints mentioned. If none found → mark as [PRICE] and proceed to Step 3.

**Edge Cases:**
- If notes are very sparse (<20 words but not empty): generate a proposal with `[FILL IN]` placeholders for each missing element. Add a note above the proposal: "⚠️ Notes were sparse — complete the [FILL IN] sections before sending."
- If notes are in mixed RU/EN: detect the dominant language, generate in that language, note any key terms preserved from the source language.

### Step 3: Build Pricing Packages

1. Based on the deliverables extracted in Step 2, construct three pricing tiers:
   - **Basic:** Core deliverable only. Fastest/smallest scope.
   - **Standard:** Full deliverable as described. Recommended tier.
   - **Premium:** Full scope + extras (faster delivery, additional features, ongoing support, etc.).

2. If budget signals were found in notes → use them as anchors for pricing.
3. If no budget signals → use `[PRICE]` placeholders for all three tiers. Add a note below the pricing table: "💡 Tip: Base your rates on deliverable complexity, time required, and your market positioning. A common starting point: hourly rate × estimated hours."

### Step 4: Draft the Proposal Document

Generate the full proposal using the output format below. Fill all extracted fields. Use `[FILL IN]` for any section where data was not available in the notes.

Sections to generate:
1. Executive Summary (2–3 sentences: client problem + proposed solution)
2. Scope / Deliverables (bullet list of all deliverables)
3. Timeline (milestones or phases; use `[TIMELINE]` if unknown)
4. Pricing Packages (Basic / Standard / Premium table)
5. Next Steps (what happens after the client accepts)

### Step 5: Draft the Cover Letter

Write an email-ready cover letter (5–7 sentences, no markdown headings inside):
- Open by referencing the discovery call or brief
- State the main value proposition in 1 sentence
- Invite the client to review the proposal and ask questions
- Close with a specific call to action (e.g., "Let's schedule 30 minutes this week to go over the details")

Match the tone and language of the proposal.

### Step 6: Generate Human-Review Checklist

Append a review checklist with at least 4 items. The checklist must include:
- [ ] Verify all pricing figures are accurate and reflect your actual rates
- [ ] Verify client name and company name are spelled correctly
- [ ] Confirm timeline is realistic given your current workload
- [ ] Check that legal/contractual terms match your standard agreement

Add additional items if the notes contain specific risks (e.g., if the client mentioned a hard deadline, add a check for that date).

---

## Output Format

Respond with three labeled sections in this order:

```
## [Client name] — Proposal

**Client:** [name]
**Date:** [today's date]
**Project:** [project title]

---

### Executive Summary
[2–3 sentences: client problem + proposed solution]

### Scope / Deliverables
- [Deliverable 1]
- [Deliverable 2]
- ...

### Timeline
[Milestones or phases, or [TIMELINE] if unknown]

### Pricing Packages

| Package | Price | Includes |
|---------|-------|----------|
| Basic | [PRICE] | [core items] |
| Standard | [PRICE] | [full scope] |
| Premium | [PRICE] | [full scope + extras] |

### Next Steps
[What happens after the client accepts — e.g., "Sign the agreement and pay a 30% deposit to start"]

---

## Cover Letter

[Email-ready text, 5–7 sentences, no headers inside]

---

## ⚠️ Human Review Checklist
- [ ] Verify all pricing figures are accurate
- [ ] Verify client name and company name are spelled correctly
- [ ] Confirm timeline is realistic given your current workload
- [ ] Check legal/contractual terms match your standard agreement
- [ ] [Additional item if context warrants]
```

**Field rules:**
- Use `[FILL IN]` for missing required fields.
- Use `[PRICE]` for missing pricing with the rate-setting tip below the table.
- Cover letter must not contain markdown headings (it is email-ready text).
- Checklist must have ≥4 checkbox items; add more if context warrants.

---

## Negative Cases

- **Empty input (< 5 words):** Stop. Return: "Notes are too sparse to build a proposal. Describe at least: client name, project problem, and proposed solution."
- **Input is an existing proposal:** Flag and stop. Return: "This looks like an existing proposal. For revision, describe what needs to change. This skill generates from raw notes."
- **Input contains no identifiable project or client:** Generate with `[FILL IN]` placeholders for all unidentifiable fields; prepend a `⚠️` warning listing what is missing.
