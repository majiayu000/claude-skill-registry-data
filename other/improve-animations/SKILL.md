---
name: improve-animations
description: Survey a codebase's animation and motion code as a senior motion advisor, then produce a prioritized audit and self-contained implementation plans for other agents (or cheaper models) to execute. Read-only on source code — it plans improvements, it does not apply them. Use when the user asks to "improve the animations", "audit the motion", "make this app feel better", or wants a roadmap of animation fixes rather than a review of a single diff.
---

# Improving Animations

An advisor skill modeled on the audit-then-plan workflow: use the capable model for the part where judgment compounds — understanding the codebase's motion, deciding what's worth fixing, writing the spec — and hand execution to any agent, including cheaper models.

It does ONE thing: survey animation and motion code, then produce prioritized findings and implementation plans. It does not review a single diff (that's `review-animations`), and it does not implement fixes itself.


## Dynamic Resources (Progressive Disclosure)

This skill is large. To save context, its detailed instructions are split into separate files in the `resources/` directory.
**You MUST use your `view_file` tool to read the relevant file when you reach that stage of the process.**

- **[resources/operating_posture.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/improve-animations/resources/operating_posture.md)**: Read this to understand Operating Posture.
- **[resources/hard_rules.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/improve-animations/resources/hard_rules.md)**: Read this to understand Hard Rules.
- **[resources/workflow.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/improve-animations/resources/workflow.md)**: Read this to understand Workflow.
- **[resources/invocation_variants.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/improve-animations/resources/invocation_variants.md)**: Read this to understand Invocation Variants.
- **[resources/tone.md](file:///D:/GIT/graph-orchestrator-smolagents/skills/improve-animations/resources/tone.md)**: Read this to understand Tone.
