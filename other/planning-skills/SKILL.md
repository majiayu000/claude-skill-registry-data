---
name: planning-skills
description: >
  Planning, brainstorming, and implementation plans for creative work, features, components. MUST use before any creative work. Covers ideation, spec writing, sequential and parallel plan execution, and subagent-driven development.
---

# Planning & Ideation

Meta-skill consolidating planning and ideation expertise. Each sub-skill below is a
full standalone skill with its own instructions, scripts, and references.
Match the user's intent to the most specific sub-skill, then read its
SKILL.md and follow its instructions completely.

## Sub-Skills

### brainstorming
- **Description:** You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation.
- **Path:** `.subSkills/brainstorming/SKILL.md`

### writing-plans
- **Description:** Use when you have a spec or requirements for a multi-step task, before touching code
- **Path:** `.subSkills/writing-plans/SKILL.md`

### executing-plans
- **Description:** Use when you have a written implementation plan to execute in a separate session with review checkpoints
- **Path:** `.subSkills/executing-plans/SKILL.md`

### subagent-driven-development
- **Description:** Use when executing implementation plans with independent tasks in the current session
- **Path:** `.subSkills/subagent-driven-development/SKILL.md`

## Routing Instructions

1. Read the user's request carefully.
2. Match their intent against the sub-skill descriptions above — treat each
   description exactly as you would a top-level skill description.
3. Read the matched sub-skill's SKILL.md at the given path and follow its
   instructions completely — including any scripts, references, or workflows
   it defines.
4. If the intent clearly spans multiple sub-skills, start with the primary
   match and note the others for follow-up.
5. If no specific sub-skill matches but the request is clearly in this domain,
   use the default sub-skill.
6. **Default sub-skill:** brainstorming

## Disambiguation

- **"I want to build X" / "Let's create X" / "Add feature X"** — Route to **brainstorming** first. The brainstorming skill has a hard gate that prevents implementation until a design is approved. Writing-plans comes after brainstorming produces a spec.
- **"I have a plan, execute it" / "Run this plan"** — If subagents are available and tasks are independent, route to **subagent-driven-development**. Otherwise route to **executing-plans**.
- **"Write a plan for X"** — If a spec/design already exists, route to **writing-plans**. If no spec exists yet, route to **brainstorming** first.
- **"Execute this plan in parallel"** — Route to **subagent-driven-development**.
- **"Execute this plan step by step"** — Route to **executing-plans**.
