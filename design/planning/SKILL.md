---
name: planning
description: Plan a new Bar Ticket feature
argument-hint: Branch name | Feature description
---

## Context
Parse $ARGUMENTS to get the following values:
- [branch-name]: The name of the branch and PR title
- [feature-description]: A description of the feature to plan

# Plan a new Bar Ticket feature

**Invocation:** `/plan [branch-name] [feature-description]`

**Purpose:** Spawns the bar-ticket-feature-planner agent to conduct an interactive planning session, ask clarifying questions, and produce a detailed implementation plan.

## What it does

1. Takes a branch name and initial `[feature-description]`
2. **Spawns the bar-ticket-feature-planner agent** which:
   - Asks clarifying questions about feature scope and technical approach
   - Presents multiple choice answers with custom input options
   - Analyzes the Bar Ticket architecture and affected components
   - Designs the technical solution aligned with existing patterns
   - **Spawns the bar-ticket-site-developer agent if website changes are needed**
   - Generates a comprehensive plan with both app and website sections
3. Returns a detailed plan that you can review and refine
4. Saves the plan to `.claude/plans/` for future reference

## Prerequisites

- Branch name follows Night District conventions: `feat/`, `fix/`, `change/`, `test/`, `design/`
- Have a rough idea of what you want to build (details refined during planning)

## Usage

```bash
/plan feat/dark-mode "Add dark mode support"
```

The bar-ticket-feature-planner agent will:

1. **Ask clarifying questions:**
   - Where should this be implemented? (app/website/both)
   - What's the primary technical challenge?
   - Which components are affected?
   - Are there performance constraints?
   - Is this a user-facing feature or internal improvement?

2. **Reference Bar Ticket architecture:**
   - Identify affected services (FileWatcher, TodoParser, GitHubClient, etc.)
   - Check existing patterns (Observable ViewModels, SwiftData persistence, etc.)
   - Consider Dynamic Island UI implications
   - Plan state management changes

3. **Spawn sub-agents as needed:**
   - Automatically spawn bar-ticket-site-developer if website changes needed
   - Get specific website recommendations integrated into final plan

4. **Deliver a complete plan:**
   - Feature summary and scope
   - Technical architecture with design rationale
   - Phased implementation steps (specific files, code patterns)
   - Testing strategy
   - Website updates (if applicable)
   - Git workflow and deployment notes

## Plan output

The generated plan includes:

1. **Feature Summary** — One-sentence distillation of what you're building
2. **User Value** — Why this feature matters
3. **Technical Components Affected** — Which services/views/models change
4. **Implementation Approach** — High-level design and patterns
5. **Specific Tasks** — Numbered, concrete tasks with file paths
6. **Dependencies & Risks** — External dependencies, edge cases
7. **Testing Strategy** — How to validate the feature
8. **Bar Ticket Website** — If applicable, specific website changes with code examples
9. **Git Workflow** — Branch naming and commit message format

## Plan attributes

Each plan markdown file includes:

```markdown
---
branch: feat/feature-name
description: What this feature does
date: 2026-04-05
scope: app | website | both
technical_approach: [key decisions from planner]
---
```

## Example workflow

```
/plan feat/dynamic-island-animation "Improve notch animation performance"

[bar-ticket-feature-planner agent starts interactive session]

❓ Where is the performance issue?
→ ☑️ Notch state transitions are janky on older Macs

❓ What's the target frame rate?
→ 60 FPS (CADisplayLink requirement)

❓ Should we optimize rendering or caching?
→ Both: predictive state caching + GPU-optimized animations

[agent analyzes DynamicNotchKit and NotchViewModel]

[agent spawns bar-ticket-site-developer to plan performance demo updates]

📋 Plan created: .claude/plans/feat-dynamic-island-animation.md

✓ Problem identified and architecture designed
✓ 8 implementation tasks with file paths
✓ Website updates planned (performance metrics demo)
✓ Ready to develop on feat/dynamic-island-animation
```

## How the agent works

The bar-ticket-feature-planner agent:
- Reads Bar Ticket codebase to understand current architecture
- References CLAUDE.md for conventions and patterns
- Asks structured questions with predefined answers + custom option
- Maps feature requirements to concrete code changes
- Considers integration points between services
- Plans testing strategy (notched/non-notched Macs, etc.)
- Optionally spawns bar-ticket-site-developer for website planning
- Documents all decisions with rationale

See `.claude/agents/bar-ticket-feature-planner.md` for agent instructions and `.claude/skills/planning/questions.md` for the full question list the agent uses.
