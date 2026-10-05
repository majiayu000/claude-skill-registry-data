---
name: teach-concept
description: Use when explaining a technical concept and adapting depth, pacing, and examples to the learner's readiness.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [teaching, incremental-learning, active-recall]
status: stable
---

# Purpose

Explain technical concepts correctly, incrementally, and adaptively. Build from definition to application in one teaching arc.

# Activation

- User asks for explanation of a concept, pattern, algorithm, or system behavior.
- User asks "why" or "how" questions requiring conceptual grounding.
- User is struggling to connect theory to code.
- **Skip if**: user wants only a command/answer with no teaching, or explicitly declines teaching.
- **Routing**: run `repo-understand` first if repo context exists but isn't mapped. Hand off to `check-understanding` after major explanations.

# Inputs

- Target concept, learner level signals, prior conversation context, relevant repo/project context.

# Workflow

1. **Calibrate** — Infer learner level from prompt and prior turns. State assumptions; keep first explanation conservative.
2. **Anchor** — Give a short definition and one core intuition sentence.
3. **Concrete Example** — One practical code or system example before any abstraction. Prefer the learner's current project/repo.
4. **Deepen** — Add one layer of complexity at a time. Introduce terminology only when needed. Explain tradeoffs and failure cases, not just happy path.
5. **Recall Check** — Ask a reasoning question requiring explanation, not repetition. If confusion appears, simplify and reframe with a new analogy.
6. **Transfer** — Give one small implementation or debugging task to apply the concept.

# Rules

- DO: one core idea per step; example before abstraction; verify understanding before escalating.
- DO: ground examples in the learner's project/repo when possible.
- DO: explain tradeoffs and failure cases alongside happy-path behavior.
- DON'T: dump multiple concepts at once — cap each response to one primary concept plus one extension.
- DON'T: end without an active-recall question and a transfer task.
- DON'T: skip the concrete example — no abstract-only teaching.
- DON'T: keep teaching at the same level if learner asks repeated clarifications — run a calibration checkpoint and reduce depth.

# Output

Responses should contain: context (concept + assumed level), explanation (definition + intuition), example (concrete code/system), checkpoint (reasoning question), and next step (application exercise). Format naturally — don't force rigid templates.

# Checklist

- [ ] Learner level assumption is explicit.
- [ ] At least one concrete example included before abstraction.
- [ ] Active-recall checkpoint present.
- [ ] Transfer task assigned.
