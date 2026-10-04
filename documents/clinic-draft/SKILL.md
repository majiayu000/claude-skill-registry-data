---
name: clinic-draft
version: 1.0.0
description: Draft a legal document — a pleading, motion, brief section, or contract clause — with verified citations, flagged assumptions, and mandatory supervisor review before filing.
author: matrixx0070
tags: [legal-clinic, drafting, pleading, motion, citation-check, supervision]
capabilities: []
---

## When to use
Use this when you need to produce actual legal text — a complaint, a motion, a section of a brief, or a contract clause — for a clinic matter. It keeps your drafting honest: every proposition tied to authority you have read, every gap marked as an assumption, and nothing filed until a supervising attorney signs off.

**Not for:** gathering the facts you will plead (use clinic-cold-start-interview), reshaping an existing template (use clinic-customize), or setting the filing deadline the draft must meet (use clinic-deadlines).

## Method
1. State the document's purpose, forum, standard of review, and required elements before writing a word.
2. Outline the argument or clause structure and map each point to the facts and to specific authority.
3. Draft section by section; where a fact is unconfirmed or a legal call is unresolved, insert a bracketed [ASSUMPTION] or [SUPERVISOR] flag instead of glossing over it.
4. Verify EVERY citation against the actual source — case exists, holding supports the proposition, quotation is exact, still good law.
   **Decision point:** if you cannot independently confirm a citation, remove it — never file authority you have not read. ABA Op. 512 makes candor to the tribunal your duty; hallucinated cases have sanctioned real lawyers.
5. Read the draft against the required elements and the opposing view; note weaknesses for your supervisor.
6. Submit the draft with its flags and citation list to the supervising attorney; do not file or send until reviewed. Independent filing would be UPL under Rule 5.5.

## Example
> Immigration clinic: you draft the argument section of a brief. Each legal standard cites a case you pulled and read; a still-pending country-conditions fact is marked [ASSUMPTION — confirm exhibit]; a discretionary-relief question you are not authorized to resolve is marked [SUPERVISOR]. You attach a citation checklist and route it up before anything is filed.

## Pitfalls
- Citing a case from memory or a tool's suggestion without reading it — the classic hallucinated-authority sanction.
- Burying assumptions in confident prose instead of flagging them.
- Putting client-identifying facts into an external GenAI drafting tool — Rule 1.6; ABA Op. 512 confidentiality duty.
- Treating a polished draft as final — nothing is filed or sent without supervisor review.

## Output format
```
DOCUMENT: <type> | FORUM: <court/matter>
PURPOSE / STANDARD: ...
DRAFT:
  <section text with inline [ASSUMPTION] / [SUPERVISOR] flags>
CITATION CHECK:
  - <cite> : read [ ] supports proposition [ ] good law [ ]
OPEN ASSUMPTIONS: ...
WEAKNESSES NOTED FOR SUPERVISOR: ...
SUPERVISOR REVIEW: [ ] required before filing
```

## Reference
- Model Rule 1.1 (competence), 3.3 (candor to the tribunal), 5.5 (UPL — supervised filing only).
- Rule 1.6 (confidentiality); ABA Formal Opinion 512 — verify all citations, protect client data, maintain candor when using GenAI.
- Clinic norm: no document is filed or sent to a client or court without supervising-attorney review.
