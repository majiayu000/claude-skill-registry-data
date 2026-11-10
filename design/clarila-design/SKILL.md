---
name: clarila-design
description: "Design or assess the interface and interaction needed by a specific issue. Use for user flows, screen states and accessibility decisions, not general implementation or unrequested redesign."
---

# Resolve the interaction design

Read the [shared workflow contract](../clarila/references/contract.md) before substantive work. This skill is part of the locally installed Clarila suite. Its source is in `~/Developer/skills`; resolve sibling skills relative to this directory.

## Procedure

1. Read product acceptance and inspect the current interface or supplied design. For a narrow edit or exact reference, retain the specified fonts, assets, controls, layout and dimensions outside the requested change; recover the actual reference source before claiming exact parity. For greenfield work, choose subject-specific tokens and an intentional visual direction, then critique the rendered result against the brief. Follow the existing design system and relevant UI skills when available.
2. Map the main interaction and loading, empty, error, success and keyboard/accessibility states that matter to this issue.
3. Propose concrete layout, hierarchy, copy and behavior decisions with their user consequence. Keep the change proportionate.
4. Use actual screenshots or a clearly labelled design artifact for comparison. Generated design imagery is a proposal, never app verification.
5. Hand off implementation-ready decisions and visual acceptance criteria.

## Specify the interaction contract

For the affected interaction, describe the triggering action, visible state, focus/keyboard behavior and recovery action. Include asynchronous results, failed saves or disappearing selections when those states can occur. Keep drafts and useful cached content available through recoverable failures.

Tie layout and copy decisions to the existing components and design tokens. Give the engineer observable acceptance examples and identify any decision still dependent on Product or a real runtime. Label proposed visual artifacts with their intended source and state.

For hierarchy, responsive structure, typography or a stateful overlay/form, read [interaction design decisions](references/interaction-design.md). Select `visual-design`, `layout`, `typography` or `accessibility` through the [expert catalog](../clarila/references/expertise.md) for the unresolved decision; retain the user's design constraints and existing system over an expert's aesthetic defaults.

## Synchronization and handoff

Resolve the same issue/workspace/session association before substantive work, including direct invocation. Read and update the private handoff described in the shared contract using available native file tools. Record the actual stage, source, findings, evidence, outcome and next action. If no native session identity is available, retain an unbound record.

## Deliverable

Return the intended interaction, relevant screen states, design decisions and visual acceptance checks.

Load only the relevant specialist from the [catalog](../clarila/references/catalog.md). Missing tools change the available evidence, never its meaning.
