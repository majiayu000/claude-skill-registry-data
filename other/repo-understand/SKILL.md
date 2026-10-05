---
name: repo-understand
description: Use when a learner asks to learn from a repository and the agent must map curriculum structure and prerequisites before teaching.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [onboarding, curriculum-mapping, prerequisite-awareness]
status: stable
---

# Purpose

Create a reliable curriculum map before deep teaching. Prevents shallow file retrieval by forcing the agent to infer learning structure, identify prerequisite dependencies, and recommend coherent starting paths.

# Activation

- User asks to learn a repository, course repo, or technical curriculum. User asks "where should I start?" in a multi-module repo. Agent hasn't established module sequence and prerequisites.
- **Skip if**: user wants a narrow operational task unrelated to learning flow, or repo context is absent and user wants generic theory.
- **Routing**: run before `teach-concept`, `socratic-mode`, `check-understanding`, and `build-with-me` for repo-based learning.

# Inputs

- Repository root and visible structure, high-signal docs (README, syllabus, indexes), learner goal and level signals.

# Workflow

1. **Classify** — Determine repo type: curriculum-first, project-first, reference-first, or hybrid. Identify learning artifacts (lessons, labs, projects, checkpoints).
2. **Map Hierarchy** — Derive module/phase order from folder structure and docs. Produce a phase map with outcomes per phase.
3. **Infer Prerequisites** — For each phase, list conceptual and tooling prerequisites. Mark dependency edges between phases.
4. **Estimate Progression** — Foundational → applied → advanced. Identify transition points where learners often stall.
5. **Synthesize Paths** — Propose 2–3 path variants based on learner goals and level, with tradeoffs and estimated effort.
6. **Checkpoint** — Ask one decision-forcing question to select a path. Do not start deep instruction before the learner selects or confirms.

# Rules

- DO: require a phase map before any deep explanation.
- DO: explain why sequence matters, not just what modules exist.
- DO: provide goal-conditioned paths with tradeoffs — never a single path for all learners.
- DO: surface uncertainty explicitly when repo signals are weak.
- DON'T: quote random files without structural context.
- DON'T: recommend advanced topics before prerequisite chain is visible.
- DON'T: dump long directory trees — cap orientation to phase outcomes and decisions.
- DON'T: invent lessons/modules without evidence — label inferred items as tentative.

# Output

Responses should contain: repo type classification, learner goal/level, curriculum map (phases + outcomes), prerequisite chain, 2–3 recommended paths with tradeoffs, checkpoint question, and next step. Format naturally.

# Checklist

- [ ] Curriculum map includes ordered phases and outcomes.
- [ ] Prerequisite chain is explicit.
- [ ] At least two goal-conditioned paths provided.
- [ ] Checkpoint question asked before deep teaching begins.
