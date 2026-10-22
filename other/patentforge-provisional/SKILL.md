---
name: patentforge-provisional
description: Use this skill when the user wants to turn an invention idea into a structured invention disclosure, prior art search strategy, claim candidates, and provisional patent draft package. This skill is for patent drafting assistance only and must not provide legal advice or guarantee patentability.
version: 1.1.0
---

# PatentForge Provisional

## Validation Checklist

- [ ] The output matches the skill's intended task and platform.
- [ ] Required inputs, assumptions, and uncertainty are explicit.
- [ ] Safety, scope, and source limits are respected.
- [ ] The response follows the requested format or the skill's default output format.
- [ ] The result is practical enough to use without another cleanup pass.

## Purpose

Turn a raw invention idea into a structured draft package that helps the user organize facts, frame novelty, prepare prior art search directions, draft claim candidates, and assemble a provisional patent working draft for attorney review.

This skill is a drafting and organization aid only. It does not provide legal advice, legal conclusions, or any guarantee about patentability, allowance, validity, enforceability, or filing outcomes.

## When To Use

- The user has a rough invention idea and needs a structured invention disclosure.
- The user wants targeted follow up questions before drafting.
- The user wants a prior art search strategy with keyword groups and possible CPC areas.
- The user wants claim candidates framed as drafting aids only.
- The user wants a provisional patent draft package for internal review or attorney review.

## When Not To Use

- The user asks whether an invention is patentable, enforceable, or likely to be allowed.
- The user wants legal advice, legal strategy, or filing advice that should come from a registered patent attorney.
- The user wants direct Patent Center submission automation.
- The user asks for non patent legal work such as contracts, licensing terms, or infringement analysis.
- The invention is too vague to identify a problem, mechanism, or technical components.

## Required Safety Rules

- Never say the invention is patentable.
- Never say claims will be allowed.
- Never say filing this will protect the invention.
- Never tell the user to file without attorney review.
- Never say the output is legal advice.
- Always state that this is not legal advice.
- Always state that prior art results are not exhaustive.
- Always state that claim candidates are drafting aids only.
- Always state that a registered patent attorney should review before filing.
- Always state that the user is responsible for final Patent Center submission.

Read these support files when needed:

- Detailed safety rules: [docs/safety-rules.md](docs/safety-rules.md)
- Full workflow: [docs/workflow.md](docs/workflow.md)
- Output validation: [docs/validation-checklist.md](docs/validation-checklist.md)
- Templates: [templates/](templates)
- Schemas: [schemas/](schemas)

## Invention Intake Workflow

1. Capture the raw invention idea in the user's own words.
2. Ask only the targeted follow up questions needed to remove ambiguity.
3. Cover these required questions if the user has not already answered them:
   - What problem does the invention solve?
   - Who experiences the problem?
   - What existing solutions are known?
   - What makes this different?
   - What are the main components?
   - How does each component interact?
   - What is the preferred embodiment?
   - What alternative embodiments exist?
   - Is this hardware, software, process, system, material, or combination?
   - What drawings would help explain it?
   - What commercial use cases exist?
   - What must remain confidential?
4. Convert the answers into a structured invention disclosure.
5. Identify the core technical field, the problem, the mechanism, and the likely point of novelty.

Use [templates/invention-disclosure.md](templates/invention-disclosure.md) and [schemas/invention-disclosure.schema.json](schemas/invention-disclosure.schema.json) when drafting or validating the disclosure.

### Intake Modes By Invention Type

Adapt the follow-up questions to what is being invented instead of asking the same list every time:

- **Hardware**: materials, tolerances, assembly order, physical interfaces, what the drawings must show at component level
- **Software**: data flow, algorithm steps, system architecture, what runs where, and which steps are more than abstract ideas implemented on a computer
- **Process**: ordered steps, required conditions, inputs and outputs at each step, and which step ordering or condition is the candidate novelty
- **Mixed**: split the questions by aspect and keep the hardware and software novelty candidates separately identified, since they may support different claims

### Inventor Interview Mode

When the user starts with a very rough idea or says they do not know where to begin, switch to one-question-at-a-time intake:

1. Ask the single most clarifying question first, usually the problem or the mechanism.
2. Reflect the answer back into the growing disclosure so the user sees it take shape.
3. Continue until the required intake questions are covered, skipping any the user already answered implicitly.
4. Offer to switch to full-package drafting once the disclosure has a problem, mechanism, components, and at least one novelty candidate.

### Confidentiality Scrub

Before the final package is assembled, scan the disclosure and draft for material that should not leave the user's hands:

- customer, supplier, and partner names
- internal project codenames, pricing, or business metrics
- trade secrets that are not needed to enable the invention, such as tuning values or process recipes beyond the preferred embodiment

List each flagged item with a suggested generic replacement, such as "a logistics customer" for a named company. Let the user decide; do not silently remove technical content, because the provisional must still enable the invention.

## Prior Art Workflow

1. Extract the key technical components and their interactions.
2. List novelty candidates as specific features, workflows, structures, or combinations.
3. Build prior art search terms using:
   - problem focused terms
   - structure or component terms
   - function or outcome terms
   - synonym and variant terms
   - competitor or market terms if known
4. Suggest possible CPC search areas at a high level.
5. Record similar references, similarity notes, novelty risks, and obviousness risks.
6. State clearly that prior art results are directional and not exhaustive.

Use [templates/prior-art-report.md](templates/prior-art-report.md) and [schemas/prior-art-report.schema.json](schemas/prior-art-report.schema.json).

## Claim Candidate Workflow

1. Identify the invention concept that appears most likely to support broad coverage.
2. Draft one or more independent claim candidates across the relevant formats:
   - system
   - method
   - apparatus or device
   - computer implemented process if applicable
3. Draft dependent claim candidates that narrow or strengthen fallback positions.
4. Separate essential elements from optional implementation details.
5. Add claim risk notes where a feature may be common, functional only, or too narrow.
6. Label all claims as drafting aids only.

Use [templates/claim-candidates.md](templates/claim-candidates.md) and [schemas/claim-set.schema.json](schemas/claim-set.schema.json).

### Claim Narrowing Mode

When the user wants fallback positions, produce narrowing candidates grouped by what does the narrowing so the fallback ladder is visible:

- **Structure**: added or more specific components and their connections
- **Workflow**: added steps, step ordering, or conditions
- **Material or parameter choice**: specific materials, ranges, or thresholds, flagged as the narrowest tier
- **Optional feature set**: features from alternative embodiments that could rescue a claim if the core is found in prior art

Order each group from broadest to narrowest and note which dependent candidates pair naturally with which independent claim. Label everything as drafting aids only.

### Figure Prompt Generator

When the user wants drawings prepared, convert the disclosure into figure prompts a sketch artist, CAD tool, or diagram generator can act on:

- one prompt per figure in the figure list: concept overview, component or exploded views, and flow diagrams for processes
- each prompt names the components to show, their spatial or logical relationships, and the reference numerals to label
- keep prompts factual descriptions of the disclosed invention; do not introduce elements the disclosure does not support

## Provisional Draft Workflow

1. Convert the invention disclosure into a provisional style draft.
2. Write these sections:
   - title
   - technical field
   - background
   - summary
   - brief description of drawings
   - detailed description
   - example embodiments
   - advantages
   - variations
   - claim style appendix
   - abstract
3. Generate a figure list from the described components, flows, and embodiments.
4. Generate a manual Patent Center filing checklist.
5. Generate attorney review notes that highlight open issues, gaps, and risk areas.

Use [templates/provisional-application.md](templates/provisional-application.md), [templates/filing-checklist.md](templates/filing-checklist.md), and [templates/attorney-review-notes.md](templates/attorney-review-notes.md).

## Final Output Format

Always return the final package in this structure:

```markdown
# PatentForge Provisional Draft Package

## 1. Invention Disclosure

## 2. Technical Summary

## 3. Problem Solved

## 4. Existing Solutions

## 5. Novel Feature Candidates

## 6. Component Breakdown

## 7. Prior Art Search Strategy

## 8. Possible CPC Search Areas

## 9. Claim Candidates

## 10. Provisional Patent Draft

## 11. Figure List

## 12. Patent Center Filing Checklist

## 13. Attorney Review Notes

## 14. Required Disclaimer
```

Populate each section with concrete content. Do not claim certainty where the facts are incomplete.

## Mandatory Disclaimer

Every final output must include language equivalent to all of the following:

- This is not legal advice.
- Prior art results are not exhaustive.
- Claim candidates are drafting aids only.
- A registered patent attorney should review before filing.
- The user is responsible for final Patent Center submission.

## Help And Examples

If the user is not sure how to use this skill, asks what it needs, or asks for examples:

- Explain in plain language what this skill can do.
- Tell the user the minimum input needed for a useful first pass.
- Show the example prompts below.
- Offer the fastest next prompt the user can send.

Minimum useful input:

- An invention summary with the problem, approach, and what seems novel.

Example prompts:

- `Use patentforge-provisional to turn this invention idea into an invention disclosure and prior art plan.`
- `Help me draft a provisional package for this automation concept with claim candidates and open risks.`
- `Show me the fastest example prompt for using this skill with a rough invention summary.`

