---
name: judge-grounding
description: Grade ONE product-model grounding doc (a domain.md, capability.md, functionality.md or epic) for whether a stranger could understand it, and write the verdict JSON. It holds the grounding judge's rubric (five criteria), its prompt and its verdict shape — the one source for them (ADR 039 §7). It runs inside an isolated, clean-context judge sub-agent that is handed only the doc, its parent doc when there is one, and the kind's per-section guidance; it never sees the brief or the author's reasoning. It only scores and evidences each criterion; the deterministic gate (grounding_gate.py, all-pass) decides pass or fail. Use when a play's content-quality eval judges a grounding doc it wrote.
user-invocable: false
model: sonnet
allowed-tools: Read, Write
---

# judge-grounding

The linter (`lint_grounding.py`) proves a grounding doc has the right *shape*. This skill
judges whether the *content* is understandable — the judgment a script cannot make. It is an
LLM-as-judge: a second model reads the doc and scores it against the bar in the grounding
content standard (`standards/schemas/product-os/grounding/_content-standard.md`).

This skill is the one source for the rubric, the judge prompt and the verdict shape. A play
does not restate them, and does not read them from memory: it dispatches a judge sub-agent,
and the sub-agent runs this skill.

## Input

The doc, its parent when there is one, and the kind's guidance for the doc's own stage — and only these
(plus where to write the verdict):

| Field | Required | Description |
|-------|----------|-------------|
| `doc` | yes | The grounding doc under test (the file the play wrote this run). |
| `parent_doc` | no | Its parent: a capability's domain, a functionality's capability. Only for `depth_gradient`. |
| `guidance` | yes | The kind's guidance for the doc's own stage — its per-section guidance, the stage's heading contract and the every-stage agent intent, cut from the kind's template by the play's `guidance_block.py --stage` (never the gold example), as `template-manager` put it in the issue's short-term memory. |
| `kind` | yes | `domain`, `capability`, `functionality` or `epic`. |
| `out_verdict` | yes | Where to write the verdict JSON. |

The guidance tells the judge what each section is *meant* to hold, so it judges a section
against its intended depth, not an invented one. The judge is NOT given the template's gold
example: handing it the answer turns judgment into pattern-matching.

Calibration finding (v1): without the section guidance, a skeptical judge over-penalizes
sections that are brief on purpose. For example, it demands a "why" on every functionality
line when a capability's Functionalities section is by design a brief linked index (the
detail lives in the child docs). Or it asks a functionality to be written as a user story,
when our rules say a functionality is a function, not a story. The guidance closes that gap.

## Process

### What the judge scores (5 criteria)

Link integrity is NOT here — it is mechanical, and the linter already does it. The judge
scores meaning:

1. **completeness** — every required section is substantive, not a placeholder.
2. **self_explanation** — each item carries the *why* or the implication, not just the
   *what*. "Local fixtures only" fails; the version that says *why* passes.
3. **discreteness_form** — discrete points, not flowing story-prose; Agile forms where
   required (acceptance as Given/When/Then; a functionality states the function's behavior,
   never "as a user I want…").
4. **depth_gradient** — detail INCREASES from parent to child. Judged only when the parent
   doc is supplied (capability vs its domain, functionality vs its capability); `na`
   otherwise (a domain has no parent; an epic is a delivery overlay).
5. **stranger_test** — the overall gate: a cold reader with no prior context can explain the
   node's *what*, *why*, and *edges* from this doc alone.

### The judge prompt

Judge the doc as this prompt says:

> You are a skeptical reviewer grading ONE product-model grounding doc for whether a
> stranger could understand it. You see the doc (and its parent doc if provided) and the
> guidance for this doc kind at its stage, which tells you what each section is meant to
> hold — judge each section against THAT, not against an expectation you invent. You do
> NOT see the brief that produced it or any author reasoning — if you find yourself
> filling in understanding the doc does not state, that is the doc failing, not you.
> Default every criterion to **fail** unless the doc clearly earns a pass.
>
> Score each criterion below for the doc. For each, return: the verdict
> (pass | fail | na), the exact text you judged (quote it), and — if not a pass — the
> concrete change that would make it pass. Be specific; "improve wording" is not a fix.
>
> Criteria (definitions above): completeness, self_explanation, discreteness_form,
> depth_gradient (na unless a parent doc is given), stranger_test.
>
> Return ONLY a JSON object in the verdict shape. No prose outside the JSON.

Read only `doc`, `parent_doc` and `guidance`. Do not open the brief, other docs, or memory.

## Output

Write exactly this shape to `out_verdict`, and nothing else:

```json
{
  "doc": "<path>",
  "kind": "domain|capability|functionality|epic",
  "criteria": [
    {"id": "completeness",      "verdict": "pass|fail|na", "evidence": "<quote>", "fix": "<concrete fix or empty>"},
    {"id": "self_explanation",  "verdict": "pass|fail|na", "evidence": "<quote>", "fix": ""},
    {"id": "discreteness_form", "verdict": "pass|fail|na", "evidence": "<quote>", "fix": ""},
    {"id": "depth_gradient",    "verdict": "pass|fail|na", "evidence": "<quote>", "fix": ""},
    {"id": "stranger_test",     "verdict": "pass|fail|na", "evidence": "<quote>", "fix": ""}
  ]
}
```

The judge does NOT decide overall pass or fail. It only scores and evidences. The gate decides,
so the judge cannot wave a doc through with a self-declared "overall: pass". The gate rule —
all-pass over the five criteria, failing closed on a missing criterion — is in
`standards/rules/grounding-eval.md`, run by each play's `grounding_gate.py`.

## Boundaries

- Writes only `out_verdict`.
- Never sees the play's context, the brief, or the author's reasoning: clean context is what
  stops context bleed and reward hacking.
- Never fixes the doc. The play's rewrite loop does, from the `fix` fields.
