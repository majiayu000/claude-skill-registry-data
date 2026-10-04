---
name: llm-vision-convergence-loop
description: Use when an LLM judge (vision or text) is the acceptance gate for subjective quality (render realism, design polish, doc quality) — run a fresh-context, schema-validated, two-consecutive-approvals-at-one-content-hash loop instead of trusting a single score.
stacks: [python, any]
domains: [any]
phases: [dev, gate]
tags: [llm-as-judge, vision, convergence, evaluation, rubric, noise-floor]
scope: kit
---
**When to use.** Any gate where the pass/fail judgment is an LLM's. *Why:* judge scores carry a
measurable noise floor (we measured ±0.29 mean and MAJOR/MINOR severity flips on byte-identical
images); a single APPROVE is a coin flip near the bar.

**Procedure.**
1. Pin a rubric (hash it); build an evidence pack; compute a content hash over everything that
   produced the evidence. Run cheap mechanical probes first — don't spend a judge round on what a
   histogram can reject.
2. Spawn a **fresh-context** reviewer per round from ONE canonical prompt template, instantiated
   verbatim (only verdict filename + date substituted). Never freehand the prompt — a freehand round
   produced a schema-invalid verdict and was voided.
3. Validate the verdict mechanically (rubric hash, content hash, every dimension with evidence,
   mandatory defect sweep); a schema hole is a rejection, never a silent pass.
4. Converge on **two consecutive APPROVEs at one content hash**. Triage findings: real → fix;
   contradicted-by-evidence → decide-and-log the contradiction; lottery re-draw on multiply-approved
   content → decide-and-log citing the approval history. Every dismissal gets a written rationale.
5. **Done when:** the recorder (not you) prints converged, the noise-floor caveat is disclosed to the
   human owner, and every probe that guarded a fixed defect class is pinned so it can't silently
   regress.

**Knowledge:** FIELD-KNOWLEDGE-NOTHOMEWRECKER.md §F1.
