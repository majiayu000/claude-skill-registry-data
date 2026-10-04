---
name: agent-room
description: "Multi-agent discussion rooms — debate or poll a problem from multiple perspectives. Standalone or invoked by other skills as a sub-routine. Mode=debate: N agents argue in rounds, converge. Mode=poll: N agents independently analyze, aggregate by consensus. Not for implementation (use system-architecture). Not for verification (use review-chain). For clarifying requirements first, see discover. For decomposing work after a decision, see task-breakdown."
argument-hint: "[problem or decision to analyze]"
allowed-tools: Read Grep Glob Bash WebSearch WebFetch
user-invocable: true
license: MIT
metadata:
  author: hungv47
  version: "2.0.0"
  budget: standard
  estimated-cost: "$0.15-0.50"
promptSignals:
  phrases:
    - "debate this"
    - "get perspectives"
    - "discuss this from multiple angles"
    - "pros and cons"
    - "multiple viewpoints"
  allOf:
    - [multiple, perspective]
  anyOf:
    - "debate"
    - "discuss"
    - "perspective"
    - "consensus"
    - "viewpoint"
    - "pros"
    - "cons"
  noneOf:
    - "code review"
    - "quality check"
  minScore: 6
routing:
  intent-tags:
    - debate
    - consensus
    - perspectives
    - multi-agent
    - agent-room
    - discuss
    - chatroom
  position: horizontal
  produces:
    - meta/agent-room-report.md
  consumes: []
  requires: []
  defers-to:
    - skill: review-chain
      when: "user wants to verify existing code/output quality, not analyze a decision"
    - skill: system-architecture
      when: "user wants to design a system, not debate options"
  parallel-with: []
  interactive: false
  estimated-complexity: heavy
---

# Agent Room

*Meta — Stochastic Multi-Agent Discussion. View a problem through multiple expert perspectives via debate or polling.*

**Core Question:** "What do multiple perspectives converge on — and where do they genuinely disagree?"

This is the centralized **multi-perspective analysis** capability. When any skill needs debate, consensus, or multiple viewpoints on a decision, it invokes agent-room. Structured decomposition work (like task-breakdown) may retain specialized agents for their domain.

---

## Two Entry Points

### 1. Standalone (user invokes directly)
User runs `/agent-room "Should we use a monorepo or polyrepo?"` — the skill runs a full debate or poll session.

### 2. Sub-routine (another skill invokes mid-flow)
The `discover` skill hits a complex decision during conversation. It invokes agent-room with the specific decision framed, waits for the result, then continues the conversation.

**Sub-routine protocol** (for invoking skills):
```
1. Frame the specific decision as a clear problem statement
2. Include relevant context gathered so far
3. Invoke agent-room with mode (debate/poll) and agent count
4. Receive the report: consensus, disagreements, recommendation
5. Integrate the recommendation into the ongoing conversation
6. The agent-room report is ephemeral — it lives in context, not necessarily on disk
```

When invoked as a sub-routine, skip writing the report to disk unless the user asks. The value is the insight, not the artifact.

---

## Critical Gates

1. **Choose the right mode** — debate for trade-off decisions, poll for filtering hallucinations and finding consensus. Default to debate (richer output for fewer agents).
2. **Problem must be specific** — N agents on a fuzzy prompt wastes tokens. If vague, ask the user to sharpen before spawning.
3. **Agents must produce structured output** — freeform prose can't be aggregated.
4. **Cost scales with agent count** — 3 debate agents x 3 rounds ~ $0.30-0.50. 10 poll agents ~ $0.30-0.50. Default to sonnet unless user requests opus.

---

## Mode Routing

| Keywords | Mode |
|----------|------|
| "debate", "argue", "discuss", "chatroom", "trade-off" | **Debate** |
| "consensus", "poll", "vote", "what do agents think", "multiple opinions" | **Poll** |
| Ambiguous | Default to **Debate** |

---

## Mode A: Debate

Spawn N agents (default 3) into a shared conversation. Each reads the full chat history before responding — building on, challenging, or refining previous contributions.

**Why it works:** Sequential handoffs lose context. A shared conversation preserves reasoning chains and enables genuine debate. When Agent A says "this needs a queue" and Agent B says "a simple loop is fine," that disagreement is more valuable than either agent's solo answer.

### A1. Parse the Request

Extract:
- **Problem/question** to debate
- **Agent count N** — default 3 (override: "have 5 agents debate")
- **Round count R** — default 3 (override: "debate for 5 rounds")
- **Agent roles** — user may specify. If not, assign diverse defaults.

### A2. Assign Agent Roles

Each agent gets a distinct perspective to maximize productive disagreement.

**Software engineering:**
1. **Architect** — systems, interfaces, scalability, long-term maintainability
2. **Pragmatist** — shipping fast, minimal complexity, "good enough" solutions
3. **Critic** — edge cases, failure modes, security holes, unstated assumptions

**Product/design:**
1. **User advocate** — UX, simplicity, delight
2. **Business strategist** — revenue, growth, competitive advantage
3. **Engineer** — technical feasibility and cost

**Strategy/decisions:**
1. **Optimist** — opportunity, upside, reasons to act
2. **Skeptic** — risk, downside, reasons to wait
3. **Synthesizer** — middle path, integrates both perspectives

For N > 3, add roles that create productive tension with existing ones.

**Constraint-assignment for divergence** — when the debate is about design or architecture (not strategy), assign each agent a structural constraint instead of (or in addition to) a perspective. This mechanically forces different solutions rather than hoping for them:
- Agent 1: "Minimize surface area — aim for the fewest possible methods/endpoints"
- Agent 2: "Maximize flexibility — support the widest range of use cases"
- Agent 3: "Optimize for the most common case — make the 80% path trivially simple"
- Agent 4 (if N > 3): "Take inspiration from [specific paradigm/library the user knows]"

Constraint-assigned agents produce genuinely different designs. Perspective-assigned agents tend to converge on similar designs with different justifications.

### A3. Run Debate Rounds

**Round 1 — Opening positions.** Agent prompt:
```
You are {role}: {role_description}

PROBLEM:
{problem}

CONTEXT:
{context}

This is Round 1 of a multi-agent debate. State your initial position.
Be specific — propose actual solutions, not vague principles. Take a clear stance.
Other agents will challenge you in subsequent rounds.

Communication discipline:
- No performative agreement: never open with "Great point" or "I appreciate X's perspective"
- State disagreements directly: "That approach fails because [X]" not "While that has merit..."
- No hedging: "This will break under load" not "This might potentially have scaling concerns"

Respond in this format:
POSITION: [One-sentence stance]
REASONING: [3-5 key points]
PROPOSAL: [Concrete recommendation]
CONCERNS: [What could go wrong with your approach]

Write your response directly — do not write to any files.
```

**Rounds 2+ — Debate.** Agent prompt:
```
You are {role}: {role_description}

PROBLEM:
{problem}

PREVIOUS DISCUSSION:
{all previous round entries}

This is Round {N}. Read the previous discussion carefully.

1. Respond to the strongest counterargument against your position
2. Identify where you AGREE with other agents (concede good points)
3. Identify where you still DISAGREE and why
4. Refine your proposal based on the discussion

Do NOT repeat your previous position. Engage with what others said.
Change your mind if they made a better argument.
Do NOT soften disagreements with praise. "I appreciate Agent A's point, but..." is sycophancy disguised as discourse. State the disagreement directly.

Respond in this format:
AGREEMENTS: [What other agents got right]
DISAGREEMENTS: [Where you still differ and why]
REFINED PROPOSAL: [Updated recommendation]
CONFIDENCE: [1-10]

Write your response directly — do not write to any files.
```

**After each round:**
1. Collect all agent responses
2. Check for convergence: if all agents agree (confidence 8+, proposals aligned), stop early
3. Otherwise continue to next round

### A4. Synthesize

After the last round, you (the orchestrator) read the full debate and synthesize:

- **Where did agents converge?** — high-confidence conclusions
- **Where did they remain split?** — genuine trade-offs the user must decide
- **What concerns were raised but unresolved?** — risks to monitor
- **Did any agent change their mind?** — mind-changes are strong signals

---

## Mode B: Poll

Spawn N agents (default 10) with identical context and varied framings. Each independently analyzes and produces structured output. Aggregate by consensus, divergence, and outlier.

**Why it works:** Exploits stochastic variation. Like polling 10 experts separately. Filters hallucinations and individual biases. Divergences reveal genuine judgment calls.

### B1. Design Structured Output Schema

Each agent must return structured output that can be mechanically compared:

| Output Type | When | Schema |
|-------------|------|--------|
| **Ranking** | Predefined options | "Rank these 5 options 1-5" |
| **Recommendation** | Open-ended | "Top 3 recommendations with confidence 1-10" |
| **Binary** | Yes/no decision | "YES or NO, top 3 reasons" |
| **Scoring** | Multi-criteria | "Score each option 1-10 on [criteria]" |

### B2. Generate Framing Variations

N slightly different prompts. Core problem + schema identical — only framing varies:

1. Neutral baseline
2. Risk-averse analyst
3. Growth-oriented strategist
4. Contrarian (challenge conventional wisdom)
5. First-principles reasoner
6. User-empathy focus
7. Resource-constrained optimizer
8. Long-term (5-year) optimizer
9. Data-driven (measurable only)
10. Systems thinker (second/third-order effects)

For N < 10, use the first N. For N > 10, cycle.

### B3. Spawn All N Agents in Parallel

One-pass — no convergence detection. Independent samples give better statistical signal than iterative refinement.

### B4. Aggregate Results

**Rankings:** Borda count (1st = N points, 2nd = N-1, etc.)
**Recommendations:** Group similar, count occurrences. Consensus (70%+), Divergence (40-69%), Outlier (<40%).
**Scoring:** Mean, median, standard deviation. Flag high-variance options.
**Binary:** Count YES/NO, summarize strongest arguments from each side.

---

## Report

When standalone (or when explicitly requested), write to `.agents/meta/agent-room-report.md`:

```markdown
---
skill: agent-room
version: 1
date: {YYYY-MM-DD}
status: final
---

# Agent Room Report

**Problem**: {problem}
**Mode**: {debate | poll}
**Agents**: {N} | **Rounds**: {R, debate only}
```

**Debate sections:** Participants, Consensus, Key Disagreements, Recommended Action, Unresolved Risks, Debate Highlights.

**Poll sections:** Consensus (X+/N agreed), Divergences (split X/Y), Outliers (Z/N), Raw Rankings/Scores.

When invoked as sub-routine: return the synthesis inline, skip disk write.

---

## Configuration

| Parameter | Default | Override |
|-----------|---------|---------|
| mode | debate | "poll this" / "debate this" |
| N | 3 (debate) / 10 (poll) | "5 agents" / "15 agents" |
| R | 3 | "debate for 5 rounds" (debate only) |
| model | sonnet | "use opus" |
| roles | auto | "have a DBA, a frontend dev, and a DevOps engineer debate" |

---

## Edge Cases

- **Vague problem**: Ask user to sharpen before spawning. Don't burn tokens on vagueness.
- **N < 2 (debate) or N < 3 (poll)**: Warn user — debate needs 2+, poll needs 3+.
- **Unanimous agreement round 1**: Stop early. Report consensus. Valid and cheap.
- **Deadlock after R rounds**: Report honestly. The finding IS that no dominant answer exists.
- **Even poll split**: Report the split. No forced tiebreaker.
- **Agent goes off-topic**: Exclude from synthesis, note effective N.
- **Existing report**: Overwrite — these are ephemeral analysis artifacts.

---

## Cost Considerations

- 3 sonnet agents x 3 rounds (debate): ~$0.30-0.50
- 10 sonnet agents (poll): ~$0.30-0.50
- Opus multiplies ~10x — only use when explicitly requested
- Early convergence saves cost
- For binary decisions, 5 poll agents usually suffices

## Chain Position

Standalone skill — can be invoked by any other skill as a sub-routine for multi-perspective decisions. Typical callers: `solution-design`, `system-architecture`, `discover`.
