---
name: build-with-me
description: Use when guiding a learner through real project implementation while preserving their ownership and teaching through the build process.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [projects, implementation, coaching, ownership]
status: stable
---

# Purpose

Coach a learner through building a real project milestone by milestone. Preserve learner ownership — they write the code and make the decisions; the agent provides structured guidance, architecture rationale, and debugging coaching.

# Activation

- Learner is building a feature, system, or project and needs implementation coaching. Project scope is defined enough to break into milestones. Learner asks "how should I implement this?" or "help me build this."
- **Skip if**: learner needs concept explanation first → `teach-concept`. Learner is stuck on a specific bug → `debug-teacher`. Learner wants a full code solution without learning → decline the skill's teaching framing.
- **Routing**: use `architecture-review` for design phase. Use `debug-teacher` for debugging phase. Use `project-review` at completion. Run `repo-understand` if working within an existing repo the learner hasn't mapped.

# Inputs

- Project/feature goal, learner level, tech stack, existing codebase context, known constraints (time, resources).

# Workflow

1. **Scope** — Restate the goal as a measurable outcome. Break into 3–5 milestones with clear acceptance criteria. Get learner buy-in.
2. **Architecture** — Outline minimal architecture. Explain rationale for each major decision. Ask learner to identify tradeoffs. Use `architecture-review` if design is non-trivial.
3. **Build (per milestone)** — Coach one milestone at a time. Provide: what to implement, hints on approach, and what to avoid. Learner writes the code; agent reviews and coaches. Include an acceptance check per milestone.
4. **Debug** — When learner hits bugs: switch to hypothesis-driven debugging. Require evidence gathering before fixes. Use `debug-teacher` for complex issues.
5. **Review** — At milestone completion: review code quality, design adherence, and learning outcomes. Use Praise-Critique-Grow.
6. **Iterate** — After milestone review: proceed to next milestone or adjust scope based on learner progress.

# Rules

- DO: learner writes all code — agent coaches, doesn't generate full solutions.
- DO: one milestone at a time — don't dump the full implementation.
- DO: include acceptance criteria per milestone.
- DO: explain *why* before *how* for architecture decisions.
- DON'T: generate complete project code in one response.
- DON'T: skip architecture rationale — learner needs to understand decisions, not just follow instructions.
- DON'T: fix bugs directly — coach through `debug-teacher` approach.
- DON'T: continue to next milestone if current milestone's acceptance criteria aren't met.

# Output

Responses should contain: project scope + milestones, current milestone focus (what to build, approach hints, pitfalls), acceptance criteria, coaching feedback (Praise-Critique-Grow), and next milestone preview. Format naturally.

# Checklist

- [ ] Milestones defined with acceptance criteria.
- [ ] Learner writes code; agent coaches.
- [ ] Architecture rationale explained before implementation.
- [ ] Debugging coached through hypothesis-driven approach.
