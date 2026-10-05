---
name: lesson-plan
description: Use when structuring a multi-session learning roadmap with milestones, gates, and pacing calibrated to learner level and goal.
version: 1.1.0
authors:
  - edu-agent-skills contributors
tags: [onboarding, planning, curriculum, pacing]
status: stable
---

# Purpose

Create a coherent learning roadmap that sequences sessions, defines milestones with verifiable gates, and prevents random topic jumping. Gives the learner a clear path from current level to stated goal.

# Activation

- Learner has a defined goal + time constraint ("interview in 2 weeks", "learn this repo in a month"). Multiple sessions planned with non-trivial sequencing. `repo-understand` produced a curriculum map needing personalization. Learner asks "where do I start and how do I get to X?"
- **Skip if**: one-off session with no continuity. Learner needs immediate help on a specific concept/bug. Plan already exists and is current.
- **Routing**: run `repo-understand` and `find-your-level` first if repo context or level is unknown. Revise plan when: learner stalls 2+ sessions, goal changes, or weak areas accumulate faster than planned.

# Inputs

- Learner goal (specific, time-bounded), level (from `find-your-level`), available sessions/time budget, known constraints (weak areas, learning style), repo/domain scope.

# Plan Structure

Three layers: **Phases** (thematic blocks) → **Sessions** (individual units with focus + gate) → **Gates** (acceptance criteria before advancing).

# Workflow

1. **Decompose Goal** — Restate as a specific, observable outcome (not "learn ML" but "train and evaluate a classifier on custom dataset"). Identify 3–5 sub-goals.
2. **Check Prerequisites** — For each sub-goal: list prerequisites, check which are confirmed, flag gaps as early sessions.
3. **Define Phases** — Group sub-goals into 2–4 phases. Each phase has a coherent outcome and takes 2–5 sessions. Order so each phase's output feeds the next.
4. **Sequence Sessions** — Break each phase into sessions. Each has: primary topic, skill(s) to use, gate criterion. Max 2 heavy concepts per session.
5. **Set Gates** — Measurable acceptance criteria per session: "can explain X mechanism," "passes challenge-generator at intermediate tier," "completes repo exercise." Gates prevent surface-level advancement.
6. **Add Buffers** — 1 revision session per 4–5 sessions. Define re-plan triggers: 2 consecutive gate failures → revise plan.
7. **Get Buy-In** — Present as a proposal. Ask: "Does this pacing feel right?" Adjust before finalizing.

# Rules

- DO: gates are non-negotiable — don't advance before gate is passed.
- DO: prerequisite gaps always get sessions before dependent content.
- DO: include buffer sessions and explicit re-plan triggers.
- DO: present as proposal with learner input, not a mandate.
- DON'T: pack more than 2 major concepts per session — cognitive overload kills retention.
- DON'T: scope-creep beyond the stated goal — every session must link to a sub-goal.
- DON'T: treat the plan as static — revise when real outcomes differ from projections.

# Output

Responses should contain: goal + level + session budget, sub-goals, prerequisite status, phase breakdown (sessions with topics/skills/gates), buffer sessions, re-plan triggers, and proposal confirmation prompt. Format naturally.

# Checklist

- [ ] Goal is specific and observable.
- [ ] Every session has an explicit gate.
- [ ] No session has more than 2 major concepts.
- [ ] Buffer sessions and re-plan triggers included.
- [ ] Plan presented as proposal with learner confirmation.
