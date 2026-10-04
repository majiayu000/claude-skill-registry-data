---
name: knowledge-vault
description: Route end-to-end personal knowledge-base work across setup, intake, organization, growth, projects, self-observation, review, and output. 用于跨阶段知识库任务，或用户不知道该调用哪个 Skill；单一明确任务优先交给对应子 Skill。
---

# Knowledge Vault

Coordinate the suite without loading every subsystem.

## Start

1. Inspect the target directory and its local instructions before asking discoverable questions.
2. Identify the user's current stage: bootstrap, intake, organization, growth, project, reflection, self-observation, Obsidian maintenance, or output.
3. Confirm the concrete outcome and whether the user authorized file writes. Read [references/permission-model.md](references/permission-model.md).
4. Route using [references/workflow-router.md](references/workflow-router.md). Load only the selected workflow.
5. Report what changed, the evidence used, unresolved decisions, and the next useful action.

If an interrupted or partial workflow must continue, read [references/recovery-protocol.md](references/recovery-protocol.md). If the routed child Skill is unavailable, name the missing Skill and provide a bounded preview; do not pretend the full workflow ran.

For first-time or cross-domain interviews, read [references/interview-routing.md](references/interview-routing.md). For advice, read [references/advice-protocol.md](references/advice-protocol.md).

## Shared invariants

- Preserve raw evidence separately from maintained understanding and audience-specific output.
- Search before creating. Prefer a justified update over a duplicate note.
- Separate sourced facts, user statements, user judgments, AI inferences, conflicts, and unknowns.
- Do not treat AI organization as a source, an output as a fact source, or one success as stable mastery.
- Keep optional systems optional. Do not impose a life taxonomy or an Obsidian plugin.
- Preserve user ownership of goals, tradeoffs, disclosure, and final decisions.
