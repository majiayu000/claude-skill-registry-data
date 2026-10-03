---
name: profile-routing
description: Route Agency work to the named Hermes profile whose professional ownership best matches the required outcome, then let Fleet resolve that stable profile identity to an eligible live node or place it when necessary.
---
# Profile Routing

Use when assigning or reassigning work across Hermes Agency profiles, including distributed execution under Hermes Fleet.

## Procedure
1. Start from the outcome the task must produce, not from keywords in its title. Identify the decision, artifact, implementation, review, or validation responsibility that actually needs an owner.
2. Inspect the complete Agency catalog and relevant role descriptions/boundaries before considering where anything is installed. Professional ownership is chosen from the Agency catalog, not from the local machine's current profile inventory.
3. Prefer the narrowest specialist that fully owns the work. Use a broader role only when the task genuinely spans that broader role's authority, not because the correct specialist happens to be absent from the current node.
4. Distinguish neighboring roles explicitly before routing ambiguous work. Examples include Product Manager vs Technical Lead, Software Architect vs Systems Architect, Backend vs Data/Database/Infrastructure, Product Designer vs UI/UX/Brand, Code Reviewer vs QA vs Security Reviewer, and Marketing Strategy vs Copy/Content/Social.
5. Use the smallest capable team. Add another profile only when it contributes distinct expertise, independent validation, or a real downstream deliverable.
6. When operating through Hermes Kanban, assign durable work to the named profile and preserve the task body, constraints, dependencies, attachments, and acceptance evidence needed by that worker.
7. If a task contains multiple independently owned outcomes, decompose it before routing instead of assigning a multi-role blob to one specialist.
8. After selecting the professional profile, resolve execution separately. Under Fleet, ask the live profile-presence/placement layer for nodes advertising that stable profile identity and filter/select nodes using Fleet's health, capacity, policy, and availability rules.
9. If the selected Agency profile exists in the catalog but no eligible node currently advertises it ready, do not substitute another profession merely because it is installed. Request Fleet to locate an eligible existing placement or install/place the profile on a suitable node, then route after readiness is advertised.
10. If delivery or node health fails after placement, preserve the same professional owner and let Fleet retry/reselect an eligible node according to runtime policy rather than changing professions to solve a transport problem.
11. Re-route to a different profile only when evidence shows the original professional ownership was wrong or the task's required outcome changed. Preserve completed work and handoff context.
12. Only when the Agency catalog itself lacks a specialization that cleanly owns the capability should the Orchestrator identify the closest legitimate owner and the missing specialization explicitly. Do not invent a profile name or silently expand another role's authority.

## Decision rules
- Professional profile selection happens before node selection.
- Local installation state never determines professional ownership.
- Fleet owns live profile presence, node eligibility, capacity, placement, retry, and transport selection.
- Ownership beats keyword matching.
- Named Agency roles remain accountable even if they use bounded within-lane subagents internally.
- A reviewer is not the implementer, and an implementer does not become the independent reviewer of its own work merely because it can inspect it.
- Cross-functional ambiguity should be resolved by splitting decisions according to authority, not by choosing the most senior-sounding title.

## Quality gate
Routing is correct when each task has one accountable stable Agency profile whose profession genuinely owns the requested outcome, neighboring-role confusion has been resolved, the team is no larger than necessary, the worker receives sufficient context, and runtime availability is resolved by Fleet without changing professional ownership simply because a particular node lacks the profile.