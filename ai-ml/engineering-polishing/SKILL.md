---
name: engineering-polishing
description: Polish, locally restructure, or translate source notes into English engineering manuscript prose while preserving evidence boundaries. Use when the user asks to improve English academic style, paragraph flow, claim strength, anti-AI wording, terminology consistency, hedging, clarity, or publication-ready expression for existing engineering conference or journal paper content. Do not use for creating a new section argument, figure/table-only work, reviewer responses, or readiness validation.
---

# Engineering Polishing

Use this skill after the paper's claim and evidence are known. It improves
English manuscript prose without hiding structural or evidence problems.

## Core Stance

- Final output defaults to English manuscript prose.
- Do not invent facts, references, mechanisms, experiments, numbers, novelty, or
  limitations.
- Do not polish a broken argument as if it were correct.
- Diagnose the failure mode before rewriting.
- Preserve technical terms, variables, units, metric definitions, and evidence
  boundaries.
- Prefer restrained, concrete academic English over promotional language.

## Boundaries

- If the paragraph lacks a stable claim-evidence structure, first return a logic
  diagnosis and do not present polished prose as final.
- Use `engineering-writing` when the user needs a new section argument,
  contribution map, or full paper structure.
- Use `engineering-figure-table` for captions, figure/table roles, or visual
  consistency.
- Use `engineering-response` for comments and response letters.
- Use `engineering-validation` for build checks or readiness claims.

## When to Open Extra Files

| File | Open when |
|---|---|
| [references/fact-boundary.md](references/fact-boundary.md) | The source is a rough skeleton, non-English notes, or evidence is incomplete |
| [references/paragraph-function.md](references/paragraph-function.md) | Identifying paragraph job before rewriting |
| [references/engineering-topic-modules.md](references/engineering-topic-modules.md) | Polishing control, algorithm, data-driven, materials, process, or multi-physics paragraphs |
| [references/list-handling.md](references/list-handling.md) | Skill-specific list cleanup examples |
| [references/paragraph-flow.md](references/paragraph-flow.md) | Paragraphs feel unclear, repetitive, poorly ordered, or hard to follow |
| [references/claim-strength.md](references/claim-strength.md) | Claims may overstate evidence, causality, robustness, generalization, or novelty |
| [references/claim-strength-diff.md](references/claim-strength-diff.md) | Comparing source and rewrite to ensure polish did not strengthen claims |
| [references/anti-ai-prose.md](references/anti-ai-prose.md) | Text sounds generic, repetitive, slogan-like, template-like, or model-generated |
| [references/style-guardrails.md](references/style-guardrails.md) | Need sentence-level academic English, transitions, hedging, terminology, or mechanics |
| [references/source-notes.md](references/source-notes.md) | Non-English or rough notes must become English manuscript prose |
| [references/source-note-expansion-check.md](references/source-note-expansion-check.md) | A rewrite may have introduced facts not present in source notes |
| [references/whole-paper-style-drift.md](references/whole-paper-style-drift.md) | Multiple sections may sound inconsistent, overly smooth, or template-like |
| [references/examples.md](references/examples.md) | Needing before/after examples or output behavior examples |
| [references/failure-modes.md](references/failure-modes.md) | Handling requests to strengthen unsupported claims or hide weak evidence |
| [../_shared/evidence-boundary.md](../_shared/evidence-boundary.md) | The rewrite may change factual scope or claim strength |
| [../_shared/claim-strength.md](../_shared/claim-strength.md) | A local claim needs verb or novelty calibration |
| [../_shared/ai-assisted-writing-policy.md](../_shared/ai-assisted-writing-policy.md) | Polished prose may hide AI-smell, unverified facts, or disclosure risk |
| [../_shared/list-to-argument.md](../_shared/list-to-argument.md) | Source prose is a list rather than a paragraph argument |
| [../_shared/non-english-source-notes.md](../_shared/non-english-source-notes.md) | Source notes include assumptions or non-English shorthand |
| [../_shared/output-mode.md](../_shared/output-mode.md) | The user asks for output only |
| [../_shared/sentence-role-and-story-flow.md](../_shared/sentence-role-and-story-flow.md) | Checking whether each sentence is necessary, connected, and non-redundant |
| [../_shared/terminology-ledger.md](../_shared/terminology-ledger.md) | User asks for varied wording around technical terms |

## Workflow

1. Identify the section and paragraph job.
2. Apply fact-boundary checks when source notes are thin.
3. Diagnose the main problem:
   paper logic, section job, paragraph flow, claim/evidence mismatch, or
   sentence style.
4. Fix higher-level logic before sentence polish.
5. Run a sentence-role check: each sentence must be necessary, placed correctly,
   connected to its neighbors, and bounded by evidence.
6. Run a claim-strength diff against the source before accepting stronger verbs.
7. Preserve source facts and evidence boundaries.
8. Rewrite in English with concrete subjects, varied sentence shapes, and
   calibrated verbs.
9. Report any claim that still needs evidence.

A paragraph has a stable claim-evidence structure only when at least three of
these are clear: paragraph job, main claim, evidence anchor, and boundary. If
fewer than three are clear, diagnose first and do not present polished prose as
final.

## Default Output

```text
Diagnosis
- Paragraph job:
- Main issue:
- Evidence risk:

Before / After / Rationale
| Source sentence or span | Revised sentence or span | Rationale | Fact/evidence risk |

Claim-strength diff
| Source claim | Revised claim | Strength change | Allowed? | Reason |

Sentence role audit
| Sentence/span | Job | Needed because | Connection to previous/next | Evidence boundary | Action |

Polished version
[English prose]

Unsupported claims
- ...
```

If the user asks for output only, return only the polished prose unless doing so
would hide unsupported claims or unverified evidence.
