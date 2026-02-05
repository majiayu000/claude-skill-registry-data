---
name: zte-progression
description: Guide progression from In-Loop to Out-Loop to Zero-Touch Engineering. Use when assessing agentic maturity, planning ZTE progression, or identifying requirements for autonomous operation.
allowed-tools: Read, Grep, Glob
---

# ZTE Progression Skill

Guide teams through the three levels of agentic coding: In-Loop, Out-Loop, and Zero-Touch Engineering.

## When to Use

- Assessing current agentic maturity level
- Planning progression to higher automation
- Identifying blockers to ZTE adoption
- Building confidence for autonomous operation

## Core Concepts

### Three Levels

| Level | Presence KPI | Description |
| --- | --- | --- |
| In-Loop | Constant | Interactive prompting |
| Out-Loop | 2 (prompt + review) | AFK agents with review |
| Zero-Touch | 1 (prompt only) | Full automation |

### Progression Requirements

**In-Loop -> Out-Loop:**

- Workflows succeed on first attempt
- Tests catch issues reliably
- Similar tasks repeat frequently

**Out-Loop -> ZTE:**

- 90%+ success rate
- Review catches nothing new
- Tests provide safety net

## Assessment Workflow

### Step 1: Identify Current Level

Search for agentic workflow indicators:

```markdown
Look for:
- Manual prompting patterns (In-Loop)
- Automated workflows with review (Out-Loop)
- Fully automated shipping (ZTE)
```

### Step 2: Analyze Success Metrics

Review KPI data if available:

```markdown
Check @agentic-kpis.md or equivalent:
- Attempt counts
- Success streaks
- Review catch rates
```

### Step 3: Identify Blockers

Common blockers to progression:

| Blocker | Mitigation |
| --- | --- |
| Low test coverage | Improve tests before progressing |
| Inconsistent success | Analyze failures, improve prompts |
| Review catches issues | Tests need to catch these first |
| No rollback capability | Add before enabling ZTE |

### Step 4: Recommend Next Steps

Based on current level, recommend:

**At In-Loop:**

- Start with Out-Loop for chores
- Build workflow automation
- Establish review process

**At Out-Loop:**

- Track review catch rate
- Build confidence with simple tasks
- Consider ZTE for high-confidence areas

**Near ZTE:**

- Enable for chores first
- Expand progressively
- Monitor continuously

## Key Memory References

- @zte-progression.md - Three levels definition
- @zte-confidence-building.md - Building ZTE confidence
- @agentic-kpis.md - KPI tracking
- @composable-primitives.md - Workflow building blocks

## Output Format

Provide assessment:

```markdown
## ZTE Assessment

**Current Level:** [In-Loop | Out-Loop | ZTE]
**Problem Classes Assessed:** [chores, bugs, features]

### Indicators Found
- [Evidence of current level]

### Blockers to Progression
- [Identified blockers]

### Recommendations
1. [Specific next step]
2. [Specific next step]

### Target Timeline
- [Realistic progression timeline]
```

## Anti-Patterns to Identify

- Skipping levels (Out-Loop before tests exist)
- All-or-nothing thinking (must ZTE everything)
- Ignoring failure signals (pushing forward despite issues)
- Review theater (reviewing without catching anything)

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
