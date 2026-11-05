---
name: concept-design
description: "Use only when explicitly invoked for software design, specifications, implementation, review, refactoring, or explanation with Daniel Jackson's concepts and synchronizations. Put functionality in independent modules and coordination in explicit rules to make software more modular, transparent, and easier to understand and change. Check CONCEPT.md/SYNCS.md structure and generate Mermaid relationship maps."
metadata:
  language: en
  translation_of: concept-design-cn
  version: "2.0.1"
---

# Concept Design — Modular, Legible Software

Define the useful behavior before choosing its implementation.

Adapts ideas from **WYSIWID** (Meng & Jackson, MIT).

Software structure should directly express behavior observable to users.
Concepts define independent functionality; synchronization rules define how concepts work together.
It should be possible to locate the corresponding concepts and rules when understanding or changing a behavior.

## Start from the need

- Name the beneficiary and the observable result they need.
- A concept provides independent behavior for one purpose.
- Its state and actions define allowed behavior.
- Its operational principle (OP) explains a representative history that fulfills the purpose.
- An OP does not specify every behavior or guarantee progress.
- Each concept instance owns its state.
- Concepts MUST NOT invoke one another or read one another's state.
- External identities carry no assumed fields from another concept.
- Put application coordination in external synchronization rules.
- Composition MAY restrict behavior but MUST preserve each concept's contract.

## Test the argument

- State the claim, its evidence, and the assumptions it needs.
- Find a scenario that would make the claim false.
- Compare alternatives, including no change.
- If fixes fail under the same assumption, re-examine that assumption.
- Check that the contract supports the OP.
- Check that the OP serves the purpose.
- Check application scenarios separately from concept correctness.
- State required timing, failure, and consistency assumptions.
- A missing decision stays open; an absent test stays unverified.

## Make each decision once

- Distinguish `confirmed`, `proposed`, `inferred`, and `open` statements.
- A proposal or inference MUST NOT become a confirmed requirement by transcription.
- Keep one authoritative definition of each model element.
- Reuse confirmed decisions until requirements or evidence justify revisiting them.
- Before adding a mechanism, check whether removing a rule or responsibility would preserve the required behavior.
- Preserve behavior during refactoring; identify intentional redesign separately.

## Choose the work

These are prompt selectors, not installed shell commands:

```text
$concept-design [design|settle|prd|build|review|guard|refine|explain] [scope and request]
$concept-design guard [audit|concept|drift|pipeline|sync|map] [scope]
```

Infer the mode from the request when omitted.
If intent is unclear, inspect read-only before asking about a blocking choice.
Read only the selected workflow.
Continue already authorized work when it crosses modes.

| Mode | Read when needed | Result |
| --- | --- | --- |
| `design` | [Design](references/design.md) | Concepts, composition, and decisions |
| `settle` | [Settle](references/settle.md) | Discussion consolidated with decision status |
| `prd` | [Specifications](references/prd.md) | Confirmed model and acceptance recorded |
| `build` | [Implementation](references/build.md) | Scoped implementation, structural review, or refactoring |
| `review` | [Review](references/review.md) | Read-only findings with evidence |
| `guard` | [Maintenance](references/guard/workflow.md) | Coverage, backfill, drift, pipeline, or a concept and synchronization diagram |
| `refine` | [Refinement](references/refine.md) | A proposal or authorized design correction |
| `explain` | [Explanation](references/explain/workflow.md) | A source-backed view of behavior |

Review, audit, drift, and plan-only requests MUST remain read-only.
Other modes write only within the requested scope.
A backfill MUST separate observed code, inferred purpose, defects, and confirmed requirements.
MUST NOT change a specification to conceal a code defect.

## Specifications and checks

Diagrams MUST use Mermaid code blocks in Markdown.
Use the [CONCEPT/SYNCS format](references/spec-format.md) when writing or comparing specifications.

```sh
python3 <skill-directory>/scripts/concept_lint.py <CONCEPT.md-or-SYNCS.md> [more-files] --json
```

A syntax result does not establish purpose fulfillment, contract conformance, or runtime correctness.
[Sources and local conventions](references/sources.md).
