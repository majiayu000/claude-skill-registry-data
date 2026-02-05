---
name: consulting-agents
description: Use when you need information you don't have, expertise outside your comfort zone, or fresh eyes on code - dispatches agents to research, advise, or review. NOT for implementation delegation (see subagent-driven-development).
version: 2.0.0
---

# Consulting Agents

## The Trigger

**Use this skill when you think:**
- "I need to find something in this codebase"
- "I'm not sure about the best approach here"
- "I want a second opinion on this code/design"
- "I need to research how X works"

**Ask yourself:** "Do I need information, expertise, or a fresh perspective?" If yes → consult an agent.

**NOT for:** Implementation work. If you need code written, see `subagent-driven-development` or `parallel-agent-orchestration`.

## Core Principle

Agents provide **fresh context** for focused tasks. You own the through-line understanding. Agents research, advise, and review.

**No blocking authority.** Agents provide input, you decide.

## When to Consult

| Need | Agent Type | Example |
|------|-----------|---------|
| Find files/components | `codebase-locator` | "Find authentication middleware" |
| Analyze code deeply | `codebase-analyzer` | "How does the caching layer work?" |
| Find similar patterns | `codebase-pattern-finder` | "Find OAuth implementations to reference" |
| Research external docs | `web-search-researcher` | "Best practices for JWT refresh tokens" |
| Domain expertise | `general-purpose` with domain focus | "Review for security issues" |
| Code review | `general-purpose` | "Review this PR for quality" |
| Design validation | `general-purpose` | "Is this architecture sound?" |

## Task Prompt Pattern

**Domain-focused task wording > specialist identity.**

Instead of: "You are a security expert..."
Use: "Review this code for security issues: authentication, authorization, input validation, SQL injection, XSS"

The domain focus triggers expertise without the overconfidence trap.

### Dynamic Role (When Needed)

When consultation needs a clear vantage point, add a role:

```
**Role:** Staff Infrastructure Engineer focused on failure-mode analysis.

**Task:** Review this retry logic for...
```

Keep roles scoped to the consultation. Recompute for each new agent.

## Task Prompt Iteration Protocol

**Before dispatching, refine the prompt:**

1. **Draft task** with what you want and domain concerns
2. **Ask the agent:** "I'm planning to task you with [X]. What additional context would help?"
3. **Agent responds** with needs (usually 1-2 iterations)
4. **Update prompt** with requested info
5. **Confirm:** "Does this have everything needed?"
6. **Dispatch to fresh context** with refined prompt

**Why fresh context:** Same model, clean slate = no accumulated assumptions.

## Parallel Discovery

**Discovery can run in parallel easily** - no commit coordination needed.

Dispatch multiple agents in a SINGLE message when tasks are orthogonal:

```
[In one message, dispatch:]
- codebase-locator: "find authentication entry points"
- codebase-locator: "find session management"
- codebase-locator: "find authorization code"
- general-purpose: "review auth architecture for security concerns"

→ All 4 run concurrently
→ You synthesize results
```

**When to parallelize discovery:**
- Multiple searches needed
- Different review perspectives on same code (security, performance, UX)
- Research from multiple sources
- Any orthogonal read-only operations

**Synthesis required:** You (or a coordinating agent) must synthesize parallel results. Parallel agents catch task-specific issues but miss integration concerns.

## Synthesis Layer

**Problem:** Parallel agents miss how pieces connect.

**Options:**
1. **You synthesize** (default for 2-4 agents)
2. **Coordinating agent** reviews all results (for 5+ agents)
3. **Two-phase:** Parallel task reviews, then integration review

**Decide who synthesizes before parallelizing.**

## Report Format

Agents write to `~/.claude/scratchpad/`:

```
{timestamp}-{project-slug}-{agent-type}-{task-slug}.md
```

**Report structure:**
```markdown
# Task: [What you asked]

## Executive Summary
[2-3 sentences: findings + recommendation]

## Findings
[Detailed analysis with evidence]

## Recommendations
[Specific actionable suggestions]

## References
[Files examined, sources consulted]
```

**Objectivity required:** Focus on technical facts, not quality judgments. Avoid superlatives.

## Related Skills

| Skill | Use When |
|-------|----------|
| `domain-review-before-implementation` | About to dispatch implementation agent - mandatory review first |
| `subagent-driven-development` | Executing plan tasks sequentially with review gates |
| `parallel-agent-orchestration` | 3+ independent implementation tasks in parallel |

**This skill (consulting-agents):** Research, expertise, review - agents advise, you decide.

**Those skills:** Implementation delegation - agents write code.

## Decision Matrix

**Consult when:**
- ✅ Need information
- ✅ Want expert opinion
- ✅ Need code review
- ✅ Validating approach
- ✅ Pattern discovery

**Don't consult, implement directly when:**
- ❌ You have the info already
- ❌ Simple/obvious task
- ❌ Need tight context continuity

**Don't consult, delegate implementation when:**
- Task is well-scoped with clear acceptance criteria
- Fresh context beneficial
- See `subagent-driven-development` or `parallel-agent-orchestration`

## Red Flags

**Never:**
- Give agents blocking authority (you decide)
- Skip reading agent reports
- Parallelize without deciding who synthesizes

**Always:**
- Use domain-focused task wording over specialist identity
- Iterate on task prompts before dispatching
- Synthesize parallel results (don't just aggregate)
- Maintain final decision authority

## Why Fresh Context + Domain Focus Works

**Experimental finding:** General-purpose agents with domain-focused tasks outperform specialist agents.

**Why specialists underperform:**
1. **Overconfidence trap** - "You are an expert" → commits to role → doesn't use tools → misses things
2. **Narrow focus** - Specialists focus on "hard problems" → miss systematic concerns

**What works:**
- Fresh context = clean slate
- Domain-focused task = triggers expertise without identity baggage
- No identity claim → agent naturally uncertain → uses tools → catches more
