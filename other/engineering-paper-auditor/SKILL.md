---
name: engineering-paper-auditor
description: Audit English engineering manuscripts like a strict reviewer without drafting final prose. Use when the user asks to review, diagnose, critique, find paper weaknesses, check claim-evidence logic, inspect section boundaries, identify overclaims, assess figures/tables against claims, or produce a paper-quality action list before writing, polishing, response drafting, or validation.
---

# Engineering Paper Auditor

Use this skill to find manuscript weaknesses before rewriting. It does not
produce final paper prose; it produces a prioritized audit and repair plan.

## Core Stance

- Audit before rewriting.
- Findings must be tied to manuscript text, source evidence, figures/tables, or
  explicitly missing inputs.
- Do not invent missing experiments, references, mechanisms, line numbers, or
  completed edits.
- Separate paper-quality blockers from style notes.
- If the user asks whether the manuscript is ready, hand off to
  `engineering-validation` for build, citation, and final-readiness checks.

## Boundaries

- Use `engineering-writing` after audit findings have been turned into section
  rewrite tasks.
- Use `engineering-polishing` only after claim/evidence structure is stable.
- Use `engineering-figure-table` for detailed caption, table, or visual redesign.
- Use `engineering-response` for reviewer/advisor comment replies.
- Use `engineering-validation` for readiness, build, reference, and final status.

## When to Open Extra Files

| File | Open when |
|---|---|
| [references/audit-rubric.md](references/audit-rubric.md) | Running a full manuscript or section audit |
| [references/examples.md](references/examples.md) | Needing concrete audit output examples |
| [references/failure-modes.md](references/failure-modes.md) | Avoiding audit overreach, rewriting, or unsupported conclusions |
| [references/story-continuity-audit.md](references/story-continuity-audit.md) | Auditing whether paper sections form a coherent story |
| [references/paragraph-to-paragraph-transition-audit.md](references/paragraph-to-paragraph-transition-audit.md) | Paragraphs are individually plausible but the section feels jumpy |
| [references/claim-resurrection-audit.md](references/claim-resurrection-audit.md) | Abstract, Discussion, or Conclusion may revive unsupported claims |
| [references/scored-audit-mode.md](references/scored-audit-mode.md) | The user explicitly asks for scores, a review panel, or reviewer simulation |
| [../_shared/story-spine.md](../_shared/story-spine.md) | Full-paper or multi-section audit needs story dependency checks |
| [../_shared/evidence-boundary.md](../_shared/evidence-boundary.md) | Any claim may exceed available evidence |
| [../_shared/claim-strength.md](../_shared/claim-strength.md) | Auditing novelty, robustness, causality, or generalization language |
| [../_shared/citation-boundary.md](../_shared/citation-boundary.md) | Related Work, citations, or source support are part of the audit |
| [../_shared/ai-assisted-writing-policy.md](../_shared/ai-assisted-writing-policy.md) | The audit may need to flag AI-smell, disclosure, or author-verification risk |
| [../_shared/list-to-argument.md](../_shared/list-to-argument.md) | A section reads like a list rather than an argument |
| [../_shared/sentence-role-and-story-flow.md](../_shared/sentence-role-and-story-flow.md) | A paragraph may contain redundant, misplaced, missing, or disconnected sentences |
| [../_shared/terminology-ledger.md](../_shared/terminology-ledger.md) | Terms, metrics, categories, or method names drift across sections |

## Workflow

1. Identify the audit scope: full paper, section, figure/table set, response
   package, or claim-evidence map.
2. Extract the paper's one-sentence thesis and stated contributions if present.
3. Build a story-spine audit before local style findings.
4. Build a claim-evidence audit table.
5. Check section jobs: Abstract, Introduction, Related Work, Methods,
   Experiments, Discussion, Conclusion.
6. Check figure/table responsibility against the claims they are asked to
   support.
7. Audit sentence roles when a paragraph is unclear: every sentence must be
   necessary, placed correctly, connected to neighboring sentences, and bounded
   by evidence.
8. Flag overclaims, missing anchors, section drift, table narration, caption
   overreach, sentence redundancy, terminology drift, and unsupported readiness
   claims.
9. Produce a prioritized action list and route each action to the correct skill.

## Scored Audit Mode

Off by default. Use it only when the user explicitly asks for scores, a
review panel, or reviewer simulation; otherwise keep the unscored verdict
vocabulary. The protocol, lens table, and band anchors are in
[references/scored-audit-mode.md](references/scored-audit-mode.md).

- Three reviewer lenses pass independently: method rigor, experimental
  evidence, contribution and positioning.
- Bands are heuristic triage anchored to listed findings, not acceptance
  predictions; no weighted total is produced.
- Material that was not inspected is `CANNOT_DETERMINE`, not a low band.

## Default Output

```text
Audit verdict
- Overall status: PASS / PASS_WITH_BLOCKERS / CANNOT_DETERMINE
- Highest-risk issue:
- Not verified:

Claim-evidence audit
| Claim | First stated | Method anchor | Experiment anchor | Figure/table anchor | Status | Repair route |

Story-spine findings
| Node | Present? | Evidence anchor | Break risk | Repair route |

Section-boundary findings
| Location | Symptom | Why it matters | Repair route |

Sentence role findings
| Sentence/span | Job | Needed because | Connection issue | Evidence boundary | Action |

Figure/table findings
| Item | Claim requested | Evidence visible/tabulated | Must not claim | Repair route |

Prioritized action list
| Priority | Action | Owner skill | Required input | Stop condition |
```
