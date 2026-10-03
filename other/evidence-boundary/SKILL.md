---
name: evidence-boundary
description: Use when an AI delivery conclusion depends on partial, indirect, inherited, mock, local, visual, or otherwise limited evidence.
---

# Evidence Boundary

## Core Principle

Evidence is a boundary, not a slogan. A conclusion may only cover what the evidence directly proves.

## Evidence Classes

| Evidence | Can Support | Cannot Support |
| --- | --- | --- |
| Route reachable | The route loads under tested conditions. | The workflow is usable or business-correct. |
| Single surface check | That exact surface passed the stated assertion. | All similar surfaces passed. |
| Mock data render | The UI can render a synthetic shape. | Real business rules, permissions, or data lifecycles work. |
| Static scan | Certain text or code patterns are absent or present. | Runtime behavior is correct. |
| Visual screenshot | Layout at one viewport and data state. | Keyboard flow, permissions, or hidden states. |
| Prior receipt | What was previously asserted by that receipt. | New or uncovered behavior. |

## Procedure

1. Name the claim being made.
2. List the evidence references.
3. For each evidence reference, state:
   - scope covered,
   - assertion level,
   - fact source,
   - freshness,
   - blind spots.
4. Downgrade any claim that exceeds the evidence.
5. Record missing evidence before assigning acceptance or owner conclusions.

## Supported Claim Levels

| Claim Level | Use When |
| --- | --- |
| `observed` | A concrete signal was seen, but no broader assertion is made. |
| `route_reachable` | Navigation reached the tested route. |
| `surface_checked` | A named surface passed named assertions. |
| `workflow_checked` | A multi-step workflow passed with stated data and role assumptions. |
| `accepted_scope_limited` | Acceptance is bounded to listed dimensions only. |
| `not_supported` | Evidence is insufficient for the proposed claim. |

## Output Contract

```md
claim:
evidence_refs:
covered_scope:
unsupported_scope:
missing_evidence:
safe_wording:
must_not_claim:
```

## Common Mistakes

- Treating reachability as usability.
- Treating one successful example as class-wide proof.
- Treating mock rendering as real data correctness.
- Inheriting a conclusion from another receipt without checking its scope.
- Saying a capability is shared merely because a shared-looking file exists.

## Safe Wording Pattern

Use: "Evidence supports X under Y conditions; it does not yet support Z."

Avoid: "The feature works" when only one route, data shape, viewport, or assertion was checked.
