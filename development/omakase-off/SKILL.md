---
name: omakase-off
description: Intercepts build/create/implement requests as an entry gate and offers a choice between brainstorming together or omakase (chef's choice parallel design exploration across 3-5 approaches), then dispatches parallel agents and lets tests pick the winner. Use on any "build X", "create Y", "implement Z", "add feature", or indecision signal ("not sure which approach", "try both") — this skill intercepts all such requests to ensure design exploration is offered before implementation begins.
---

# Omakase-Off

Chef's choice exploration - when you're not sure WHAT to build, explore different approaches in parallel.

**Part of Test Kitchen Development:**
- `omakase-off` - Chef's choice exploration (different approaches/plans)
- `cookoff` - Same design, multiple cooks compete (each creates its own plan from the shared design)

**Core principle:** Let indecision emerge naturally during brainstorming, then implement multiple approaches in parallel to let real code + tests determine the best solution.

## Three Triggers

### Trigger 1: BEFORE Brainstorming

**When:** "I want to build...", "Create a...", "Implement...", "Add a feature..."

**Present:**
```
Before we brainstorm the details, would you like to:

1. Brainstorm together - We'll explore requirements and design step by step
2. Omakase (chef's choice) - I'll generate 3-5 best approaches, implement them
   in parallel, and let tests pick the winner
```

### Trigger 2: DURING Brainstorming (Indecision Detection)

**Detection signals:**
- 2+ uncertain responses in a row on architectural decisions
- Phrases: "not sure", "don't know", "either works", "you pick", "no preference"

**When detected:**
```
You seem flexible on the approach. Would you like to:
1. I'll pick what seems best and continue brainstorming
2. Explore multiple approaches in parallel (omakase-off)
```

### Trigger 3: Explicitly Requested

- "try both approaches", "explore both", "omakase"
- "implement both variants", "let's see which is better"

## Workflow Overview

| Phase | Description |
|-------|-------------|
| **0. Entry** | Present brainstorm vs omakase choice |
| **1. Brainstorm** | Passive slot detection during design |
| **1.5. Decision** | If slots detected, offer parallel exploration |
| **2. Plan** | Generate implementation plan per variant |
| **3. Implement** | Dispatch ALL agents in SINGLE message |
| **4. Evaluate** | Scenario tests → fresh-eyes → judge survivors |
| **5. Complete** | Finish winner, cleanup losers |

See `references/detailed-workflow.md` for full phase details.

## Directory Structure

```
docs/plans/<feature>/
  design.md                  # Shared context from brainstorming
  omakase/
    variant-<slug>/
      plan.md                # Implementation plan for this variant
    result.md                # Final report

.worktrees/
  variant-<slug>/            # Omakase variant worktree
```

## Slot Classification

| Type | Examples | Worth exploring? |
|------|----------|------------------|
| **Architectural** | Storage engine, framework, auth method | Yes |
| **Trivial** | File location, naming, config format | No |

Only architectural decisions become slots for parallel exploration.

## Variant Limits

**Max 5-6 implementations.** Don't do full combinatorial explosion:
1. Identify the primary axis (biggest architectural impact)
2. Create variants along that axis
3. Fill secondary slots with natural pairings

## Critical Rules

1. **Dispatch ALL variants in SINGLE message** - Multiple Task tools, one message
2. **MUST use scenario-testing** - Not manual verification
3. **Fresh-eyes on survivors** - Required before judge comparison
4. **Always cleanup losers** - Remove worktrees and branches
5. **Write result.md** - Document what was tried and why winner won

## Skills Orchestrated

| Dependency | Usage |
|------------|-------|
| `brainstorming` | Modified flow with passive slot detection |
| `writing-plans` | Generate implementation plan per variant |
| `git-worktrees` | Create isolated worktree per variant |
| `parallel-agents` | Dispatch all variant subagents in parallel |
| `scenario-testing` | Run same scenarios against all variants |
| `fresh-eyes` | Quality review on survivors → input for judge |
| `judge` (`test-kitchen:judge`) | **REQUIRED** Phase 4 scoring — invoke fresh to evaluate survivors with 5-criteria framework |
| `finish-branch` | Handle winner (merge/PR), cleanup losers |

## Example Flow

```
User: "I need to build a CLI todo app."

Claude: [Triggers omakase-off]
Before we dive in, how would you like to approach this?
1. Brainstorm together
2. Omakase (chef's choice)

User: "1"

Claude: [Brainstorming proceeds, detects indecision on storage]

You seem flexible on storage (JSON vs SQLite). Would you like to:
1. Explore in parallel - I'll implement both variants
2. Best guess - I'll pick JSON (simpler)

User: "1"

[Creates plans for variant-json, variant-sqlite]
[Dispatches parallel agents in SINGLE message]
[Runs scenario tests on both]
[Fresh-eyes review on survivors]
[Presents comparison, user picks winner]
[Cleans up loser, finishes winner branch]
```
