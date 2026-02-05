---
name: rules-repo-conventions
description: Apply Rules Repository conventions and forward-only workflow. Use when generating or editing docs, prompts, or code in projects that consume this repository or when this repository is the active workspace. Ensure Pact → Rules → Guides → Implementation links are created and updated, and prefer linking to submodule guides over duplicating content.
---

# Rules Repository Conventions

This Skill encodes the essential conventions for working with this repository (as a submodule or directly) so Claude can apply them automatically.

## Instructions
1. Load and apply the repository root skills catalog: see [skills.md](../../../../skills.md).
2. Honor RULES.md anchors for behavior and technical commitments:
   - [./RULES.md#4-behavioral-agreements](../../../../RULES.md#4-behavioral-agreements)
   - [./RULES.md#5-technical-commitments](../../../../RULES.md#5-technical-commitments)
   - [./RULES.md#document-modularity-policy](../../../../RULES.md#document-modularity-policy)
   - [./RULES.md#6-forward-only-change-policy](../../../../RULES.md#6-forward-only-change-policy)
3. Close loops between artifacts:
   - Pact → Rules → Guides → Implementation, and back-links from Implementation to its source guide and rule.
4. Link discipline:
   - Use relative paths; do not place project-specific docs inside the Rules Repository submodule directory when used downstream.
5. Observability defaults:
   - Prefer wiring to the Observability index and relevant guides: [generative/platform/observability/README.md](../../../../generative/platform/observability/README.md).
6. When adding new topic docs under generative/:
   - Add the entry to the nearest topic index README and cross-link to related guides.
7. When updating structure/content:
   - Apply the Forward-Only policy in one change: update or remove conflicting docs and links; no compatibility stubs.

## Examples
- When scaffolding a new host project README, include links to PACT.md, RULES.md, GUIDES.md, IMPLEMENTATION.md, and the Rules Repository submodule path.
- When creating a new Observability guide, add it to [generative/platform/observability/README.md](../../../../generative/platform/observability/README.md) and cross-link from related platform indexes.

## Validation Checklist
- Links resolve and remain relative
- Loop closure present (forward/back links)
- No project-specific files placed inside the submodule directory
- Forward-only edits applied (no legacy anchors retained)

## See also
- Repository skills catalog — [skills.md](../../../../skills.md)
- Enterprise RULES — [RULES.md](../../../../RULES.md)
- Platform Observability — [generative/platform/observability/README.md](../../../../generative/platform/observability/README.md)
