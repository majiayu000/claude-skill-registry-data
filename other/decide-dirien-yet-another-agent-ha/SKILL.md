---
name: decide
description: >
  Three-agent adversarial debate protocol for strategic decisions.
  Two advocates steelman opposing positions while a moderator
  identifies risks and synthesizes a binding consensus. Use when
  choosing between alternatives, evaluating tradeoffs, or making
  high-stakes decisions.
compatibility: >
  No external tool dependencies. Requires an agent capable of
  spawning parallel sub-agents and performing web research.
---
<!-- Copyright 2025-2026 Richard Shade. Licensed under Apache-2.0. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Adversarial Consensus Protocol

Run a structured three-agent debate to reach consensus on a strategic
decision. Two advocates steelman opposing positions while a moderator
asks hard questions, identifies risks, and synthesizes the binding
consensus.

**Why this works**: adversarial structure surfaces arguments
brainstorming misses. Evidence-grounded research prevents epistemic
closure. Forced concessions in Round 2 prevent entrenchment. The
moderator writes the binding consensus after hearing both sides.

## Pre-flight validation

Before running the debate, verify the input contains a genuine decision
with at least two distinguishable options or courses of action.

If the input is a factual question, explanation request, or
single-option statement, respond directly instead: "This protocol
works best when choosing between alternatives. Could you rephrase
with the options you're weighing, or ask me directly?"

When in doubt, proceed — err on the side of running the debate.

## Phase 0: Research and frame the decision

### Step 0.1: Gather context

Read project documentation and context files to understand the
decision space. Common sources include README, architecture docs,
product docs, recent git history, and any files the user referenced.

### Step 0.2: Identify the two positions

From the decision topic, formulate two clear, opposing positions:

- **Position A**: one side of the decision
- **Position B**: the opposing side

If the topic naturally implies two sides (e.g., "gRPC vs REST"),
use those directly. If the topic is open-ended (e.g., "pricing
strategy"), research the space and formulate the two strongest
opposing approaches.

### Step 0.3: Identify constraints

Extract hard constraints from the user's message or project docs:
budget limits, timeline requirements, team size, technical
constraints, business requirements, non-negotiable values.

### Step 0.4: Present brief

Generate the debate brief before proceeding. Evaluate against three
conditions:

- Can the two positions be stated without significant overlap?
- Is the question genuine (not leading or presupposing an answer)?
- Are there at least two meaningfully distinct outcomes?

If all conditions pass, present the brief and proceed to Phase 1:

```text
Decision: [one-line summary]
Position A: [name] — [one-sentence description]
Position B: [name] — [one-sentence description]
Constraints: [list any hard constraints]
Launching Round 1...
```

If any condition fails, present the brief and ask the user whether to
reframe or proceed as-is.

## Phase 1: Round 1 — position papers

Launch **three agents in parallel**. Each agent runs independently
and cannot read the others' output.

- **Advocate A**: steelman Position A. Research externally to find at
  least 2 supporting sources. Write a comprehensive position paper
  with architecture, implementation plan, costs, timelines, risks,
  and mitigations. Cite sources inline.
- **Advocate B**: steelman Position B with the same structure and
  research requirements as Advocate A.
- **Moderator**: critically examine both positions using external
  counter-evidence. Find at least 2 sources that challenge each
  position. List the 10 hardest questions (5 per position), identify
  the 5 biggest risks per approach, propose a hybrid model, and reach
  a preliminary recommendation.

Compose agent prompts following
`references/debate-prompts.md` — Round 1 section.

### Synthesize Round 1

After all three agents complete, present to the user:

1. **Where all three agree** — table of consensus points
2. **Where they disagree** — table of tensions with each agent's
   position
3. Brief commentary on the key tensions

Then immediately proceed to Round 2.

## Phase 2: Round 2 — forced convergence

Launch **three agents in parallel**. Each agent receives a summary
of the other agents' arguments and must respond.

- **Revised Advocate A**: respond to the strongest challenges from
  Advocate B and the Moderator. Concede valid points honestly, defend
  where Position A remains strongest, and state a revised position.
- **Revised Advocate B**: same structure as Revised A, responding to
  challenges from Advocate A and the Moderator.
- **Consensus Moderator**: drive toward final consensus. Write the
  binding consensus document: the agreed model, resolved tensions,
  execution timeline, 3 key metrics, the single biggest risk, and a
  one-paragraph elevator pitch.

Compose agent prompts following
`references/debate-prompts.md` — Round 2 section.

## Phase 3: Present results

### Step 3.1: Present the consensus

Show the user:

1. Key concessions from each advocate (what changed their minds)
2. The consensus model — the Moderator's final recommendation
3. Structure or plan details (tiers, architecture, timeline)
4. Key metrics to track
5. Biggest risk and mitigation

### Step 3.2: Ask about persistence

Ask the user if they want to save the consensus. Determine the
appropriate file based on the decision type:

- Business decisions → `biz.md`
- Architecture decisions → `ARCHITECTURE.md` or `ADR-NNN.md`
- Product decisions → `PRODUCT.md`
- Strategy → appropriate project document
- Or a new file if none fits

## Orchestrator guidelines

- **Always launch all 3 agents per round in a single step** (parallel)
- **Never edit the agents' arguments** — present them faithfully
- **The Moderator's Round 2 consensus is the binding output** — but
  the user has final authority to override
- **Keep your own commentary brief** — the agents did the thinking;
  you synthesize and present
- **If agents do not converge after Round 2**, highlight the remaining
  disagreement and ask the user to break the tie rather than running
  more rounds
- **Adapt prompt specifics to the domain** — a pricing decision needs
  cost numbers; an architecture decision needs technical tradeoffs
- **Include relevant project context** in every agent prompt — agents
  run in isolation and cannot read each other's output
