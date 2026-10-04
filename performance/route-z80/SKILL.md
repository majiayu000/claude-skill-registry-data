---
name: route-z80
description: Select one specialist for natural-language Z80/ZX requests, even when the match is unambiguous, including observed unresolved failures, audits, products, documentation, delivery, organization, size, and performance. Use also to choose a skill. Skip when a specialist is explicit or an ordinary known-cause task belongs to workflow.
---

# Route Z80

Select the domain by requested outcome. `$workflow` separately owns execution
effort; do not load its routes during domain selection.

## Selection

1. Honor an explicitly named skill unless it conflicts with the requested
   outcome; explain a material conflict instead of silently substituting.
2. Identify the requested deliverable, not repository keywords or incidental
   implementation steps.
3. Select one primary route from the table and load only that sibling skill.
4. Use a second specialist only for a separate explicit objective or when the
   primary specialist uncovers a material blocker owned by that domain.

Select an unambiguous match immediately. If size, structure, and performance
appear together as alternatives without a primary outcome, remain in `route-z80`
and ask one focused question. Alternatives are not competing acceptance criteria.

| Requested outcome / boundary | Route |
| --- | --- |
| Send named files/directories through BridgeZX, including build artifacts. Building or changing them is a separate objective. | [`send-bridgezx`](../send-bridgezx/SKILL.md) |
| Start, resume, implement, diagnose, validate, or hand off an existing program's **Spectranext cartridge consumer port** through its external pipeline. | [`port-spectranext`](../port-spectranext/SKILL.md) |
| Explicit product initiative needing specification and milestones, or an active develop dossier. A routine feature, plan, or implementation alone does not qualify. | [`develop-z80`](../develop-z80/SKILL.md) |
| Create, restructure, review, or synchronize public repository documentation, including one README. | [`document-z80`](../document-z80/SKILL.md) |
| Diagnose, or diagnose and repair, one observed failure with unresolved causality, conflicting evidence, or a failed evidence-supported fix. Includes regression against a known baseline. | [`debug-z80`](../debug-z80/SKILL.md) |
| Preventive or broad read-only correctness audit: ABI, ISR, memory, firmware, toolchain, or hardware risks, without one failure driving the investigation. | [`audit-z80`](../audit-z80/SKILL.md) |
| Map or reorganize ownership, dependencies, modules, source layout, banks, overlays, or runtime placement. | [`organize-z80`](../organize-z80/SKILL.md) |
| Size or memory footprint is the sole acceptance metric; prove net byte savings. | [`shrink-z80`](../shrink-z80/SKILL.md) |
| Improve acceptable behavior: identify bottlenecks and rank speed, size, RAM, rendering, latency, or competing metrics. | [`optimize-z80`](../optimize-z80/SKILL.md) |
| An ordinary bounded fix whose cause is already established, implementation, review, refactor, test, build, source comment, agent instructions, or non-repository prose without a specialist evidence question. | [`workflow`](../workflow/SKILL.md) |

`Spectranext` is not shorthand for the ZX Spectrum Next platform. Generic Next
products follow the product/workflow rows; changes to the cartridge pipeline
itself follow their engineering outcome, not the consumer-port route.
Unresolved Z80 failures use `debug-z80` rather than a generic debugging workflow.

## Handoff

State the selected route in one sentence and continue with it. Do not request
confirmation for an unambiguous selection, summarize unused skills, or load
every sibling `SKILL.md`.
