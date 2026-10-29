---
name: roundtable
description: "Run a multi-perspective roundtable on a decision: 4 parallel background agents argue it against the actual code with file:line evidence, then their positions are synthesized into consensus, likely, split, and lone-wolf buckets with an action plan. Usage: /roundtable <question or decision>"
---

# Multi-Perspective Decision Debate

Launch 4 parallel background agents that independently analyze the codebase and argue from different perspectives about the topic provided in `$ARGUMENTS`. When all 4 finish, synthesize their positions into a majority-consensus recommendation.

## Setup

Create a per-run directory so concurrent runs don't collide:

```bash
RUN_DIR=$(mktemp -d "${TMPDIR:-/tmp}/roundtable.XXXXXX")
```

Pass the absolute `$RUN_DIR` path to every agent. Each agent writes its position file there.

## Agent Roles

### 1. Product Advocate
Argues from the **user and product** perspective. What matters to the people actually using this? What would they notice? What makes them love it or hate it?

Write position to `$RUN_DIR/product-advocate.md` with:
- Top 3 priorities from user perspective (with reasoning)
- What's NOT worth doing (users wouldn't care)
- Any new issues spotted that users would notice

### 2. Tech Lead
Argues from **engineering quality and maintainability**. What technical debt is dangerous? What bites the team in 3 months?

Write position to `$RUN_DIR/tech-lead.md` with:
- Top 3 technical priorities (with specific file/line references)
- What's NOT worth doing (premature optimization, etc.)
- Risk assessment of the current state

### 3. Devil's Advocate
**Challenges everything.** Questions whether work is actually needed. Asks "who asked for this?" and "what breaks if we don't do it?" Prevents gold-plating.

Write position to `$RUN_DIR/devils-advocate.md` with:
- For each proposed item: fix it, defer it, or close as wontfix? Be harsh.
- The case for "just ship it" vs "keep polishing"
- What work would be unnecessary?

### 4. QA / Reliability Engineer
Argues from **reliability, testing, and production readiness**. What could go wrong in production? What's untested? What pages someone at 2am?

Write position to `$RUN_DIR/qa-reliability.md` with:
- Top 3 reliability concerns
- What testing is missing?
- Specific runtime failure modes found in code

## Instructions

1. Launch all 4 agents in parallel with your runtime's subagent tool, in the background where it supports that (in Claude Code: the Agent tool with `run_in_background: true`). With no subagent tool, write the 4 positions yourself one at a time, each from only its own role's brief, then continue
2. Each agent should read relevant source files, issue trackers if present (e.g. ISSUES.md, BACKLOG.md, BUGS.md), and git history
3. Each writes their position to its designated file in `$RUN_DIR`
4. After all 4 complete, run the synthesis below automatically

**Important**: Each agent must reference actual code, files, and line numbers. No hand-waving. Be specific.

Adapt each agent's prompt to incorporate the specific topic from `$ARGUMENTS` and the current project context.

## Synthesis

1. Read all 4 position files in `$RUN_DIR`:
   - `product-advocate.md`
   - `tech-lead.md`
   - `devils-advocate.md`
   - `qa-reliability.md`

2. If any file is missing or empty, tell the user which agent hasn't reported yet and stop.

3. For each recommendation that appears across the positions, tally votes:
   - **Strong consensus** (3-4 agents agree): DO THIS
   - **Majority** (2 agents agree, others neutral): LIKELY DO THIS
   - **Split** (2v2): resolve the split with reasoning and note the dissent
   - **Lone wolf** (1 agent, others disagree): DEPRIORITIZE unless the argument is compelling

4. Produce a structured output:

```
## Consensus: DO (3+ votes)
- [item]: advocated by [which agents], opposed by [who if any]

## Likely Do (2 votes, no opposition)
- [item]: advocated by [which agents]

## Splits (resolved)
- [item]: [Agent A] says X because Y, [Agent B] says Z because W. Resolution: [choice] because [reasoning]; dissent: [what the other side would watch for]

## Deprioritized (lone wolf or wontfix)
- [item]: only [agent] wanted this, others say [reason]

## Devil's Advocate Highlights
- Key challenges that should be acknowledged even if overruled
```

5. End with a concrete **recommended action plan**: an ordered list of next steps the user can execute, based on consensus items and resolved splits.

6. If `$ARGUMENTS` contains additional context or constraints (e.g., "focus on pre-merge items only"), filter the synthesis accordingly.

### Synthesis rules

- Give credit to each agent's perspective; don't flatten nuance
- If the Devil's Advocate raised a point that no other agent addressed, flag it explicitly
- The synthesis should be actionable, not philosophical
