---
name: security-privacy-review
description: Route threat modeling, prompt-injection defense, and privacy review for trust, authority, and personal-data boundaries.
---

# Security And Privacy Review

Choose one primary mode and read only its workflow. Add modes only when the same change crosses distinct security, AI-authority, or privacy boundaries.

| Mode | Use when | Workflow |
| --- | --- | --- |
| `threat-modeling` | Analyze assets, actors, entry points, trust boundaries, attack paths, controls, or residual risk. | [Threat modeling](references/workflows/threat-modeling.md) |
| `prompt-injection-defense` | Review untrusted content influencing tools, retrieval, hidden instructions, external calls, or writes. | [Prompt-injection defense](references/workflows/prompt-injection-defense.md) |
| `privacy-review` | Review collection, consent, minimization, retention, deletion, exports, subprocessors, or user rights. | [Privacy review](references/workflows/privacy-review.md) |

Do not load sibling workflows or artifacts prospectively. Stop before unauthorized exploitation, personal-data disclosure, production mutation, or legal/compliance conclusions reserved for owners.
