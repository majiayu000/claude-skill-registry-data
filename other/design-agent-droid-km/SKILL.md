---
name: "Design Agent Droid"
description: "Run a focused UI polish or mockup-to-implementation pass through Factory/Droid using the custom droid `design-agent-droid`. Prefer GLM-5V Turbo when available; current working fallback/default is GLM-5.1 on the coding-plan endpoint."
alwaysAllow: ["Bash"]
---

# Design Agent Droid

Use this skill when you, the orchestrating agent, need to launch Factory/Droid for a visual-first UI pass.

## What this skill is for
This is an orchestrator-facing launch skill. It tells the current agent how to route the task, shape the prompt, and choose the right Droid-side worker.

Use it to:
- choose the correct Droid agent/droid
- shape the delegation prompt for visual/design work
- avoid generic coding-agent prompting when the task is really UI/UX polish

Do not tell the downstream Droid worker to load, activate, or read this skill itself unless the user explicitly wants that. The normal flow is:
1. You read this skill.
2. You launch Droid correctly.
3. The Droid worker does the task using its own droid instructions.

## Default workflow
1. Inspect the current UI first.
2. Name the design intent before editing.
3. Make the smallest coherent improvement pass.
4. Verify desktop/mobile and important interaction states.
5. Report what changed, why it helped, and what still needs another pass.

## Preferred agent
On Factory/Droid, prefer the custom droid:

- `design-agent-droid`

## Model guidance
- GLM-5V Turbo remains the preferred visual model family when accessible.
- On this setup, the current working fallback/default is GLM-5.1 via the Z.ai coding endpoint.
- Do not block the task just because GLM-5V is quota- or plan-gated.

## Recommended prompt shape
"Use design-agent-droid for a UI polish pass on <surface>. Inspect the current UI or screenshots first, state the design intent, make the smallest high-leverage improvements, then report visual QA findings, interaction QA findings, and remaining weaknesses."

## Output checklist
- Design intent summary
- Top UI/UX issues found
- Concrete changes recommended or applied
- Breakpoint and interaction QA notes
- Remaining risks / next pass
