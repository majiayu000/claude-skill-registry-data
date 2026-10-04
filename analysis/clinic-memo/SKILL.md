---
name: clinic-memo
version: 1.0.0
description: Draft an internal legal research memo for the supervising attorney with verified authority and flagged open questions.
author: matrixx0070
tags: [legal-clinic, research-memo, work-product, analysis, citations, supervision]
capabilities: []
---

## When to use
Use this when the supervising attorney needs an internal research memo on a discrete legal question in a clinic matter — the classic Question Presented, Brief Answer, Facts, Analysis, Conclusion structure. This is attorney work product: it informs the supervisor's judgment, not the client directly.

**Not for:** completing forms (use clinic-form-generation), client-facing explanations (use clinic-plain-language-letters), or delivering conclusions to the client as advice — students analyze under supervision and cannot give independent legal advice (Rule 5.5).

## Method
1. Frame the Question Presented narrowly around the facts and the governing law; a vague question yields a useless memo.
2. State the material facts from the file. Redact or use placeholders for client identifiers before touching any external or GenAI tool (Rule 1.6).
3. Research and read the primary authority yourself.
   **Decision point:** if a GenAI tool supplied a case, statute, or quote, verify it in an authoritative reporter before it enters the memo — do not cite anything you have not confirmed exists and says what you claim (ABA Op. 512; Rule 1.1). A citation you cannot verify is deleted, not softened.
4. Analyze: apply law to facts, address counterarguments, and note where authority is thin or split.
5. Mark every unresolved issue explicitly as an OPEN QUESTION for the supervisor.
6. Write the Brief Answer and Conclusion last, and label the whole document internal work product.

## Example
> Question Presented: Under [state] law, does a tenant who withheld rent after a documented habitability defect have a defense to the landlord's unlawful-detainer action? You confirm each cited case in the reporter, note that one appellate district is unsettled as an OPEN QUESTION, and route the memo to the supervising attorney.

## Pitfalls
- Citing a case or quote a GenAI tool produced without confirming it in a real reporter.
- Burying an unresolved issue instead of flagging it as an OPEN QUESTION.
- Putting client-identifying facts into an external tool (Rule 1.6).
- Writing the memo as if it were advice to the client rather than internal work product (Rule 5.5).

## Output format
```
INTERNAL WORK PRODUCT — MATTER <id>
TO: <supervising attorney>   FROM: <student>   DATE: <date>
QUESTION PRESENTED:
BRIEF ANSWER:
FACTS:
ANALYSIS:
CONCLUSION:
OPEN QUESTIONS: <list>
AUTHORITIES VERIFIED: yes/no
```

## Reference
- ABA Formal Op. 512: verify every GenAI-sourced authority; guard confidentiality and candor.
- Model Rules 1.1 (competence), 1.3 (diligence), 1.6 (confidentiality), 5.5 (supervised practice only).
- Clinic norm: memo is internal work product reviewed by the supervising attorney.
