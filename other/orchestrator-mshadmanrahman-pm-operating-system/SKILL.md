---
name: orchestrator
description: "Wave-based parallel agent execution with manifest communication. Decomposes complex work into 3+ parallel sub-agent streams, coordinates handoffs, and triggers strategic compaction between phases. Use when a task needs multiple agents working simultaneously."
---

# Wave Orchestrator Skill

Coordinates complex, multi-step work through waves of parallel sub-agents. Each wave runs independent agents simultaneously. Between waves, the orchestrator reads manifests, updates the plan, and optionally compacts.

## When to Activate

- Task requires 3+ independent work streams
- User says "orchestrate", "run waves", "parallel execute"
- Complex task that would consume too much context if done linearly

## Architecture

```
Main Session (Lean Orchestrator)
  |
  +-- Wave 1: Research & Discovery
  |     +-- Agent A --> manifests/{date}/agent-a.jsonl
  |     +-- Agent B --> manifests/{date}/agent-b.jsonl
  |
  +-- [Read manifests, update plan, /compact if needed]
  |
  +-- Wave 2: Analysis & Decisions
  |     +-- Agent C --> manifests/{date}/agent-c.jsonl
  |
  +-- [Read manifests, update plan, /compact if needed]
  |
  +-- Wave 3: Output & Delivery
        +-- Agent D --> manifests/{date}/agent-d.jsonl
```

## Protocol

### Step 1: Decompose

Break the user's request into work streams:
1. List all distinct tasks
2. Identify dependencies (what must complete before something else starts)
3. Group into waves: independent tasks share a wave, dependent ones go to later waves

### Step 2: Prepare Manifest Directory

```bash
mkdir -p _context/manifests/$(date -u +%Y-%m-%d)
```

### Step 3: Read the Manifest-Writer Protocol

```bash
cat _context/protocols/manifest-writer.md
```

This protocol gets injected into every sub-agent prompt.

### Step 4: Build Sub-Agent Prompts

For each agent in the wave, construct a prompt:

```
You are: {agent-name}
Task: {specific task description}
Scope: {files/areas to focus on}

{task-specific instructions}

---
MANIFEST PROTOCOL:
Write your findings to: _context/manifests/{date}/{agent-name}.jsonl
{content of _context/protocols/manifest-writer.md}
---
```

### Step 5: Execute Wave

Spawn all agents in the wave simultaneously using the Task tool:

```yaml
Task:
  description: "{agent-name}: {3-5 word summary}"
  subagent_type: "general-purpose"  # or specific type
  prompt: "{constructed prompt from Step 4}"
```

Launch all wave agents in a SINGLE message (parallel tool calls).

### Step 6: Between Waves

After all agents in a wave return:

1. **Read manifests**: For each agent's manifest file, extract summaries
2. **Check for blockers**: Look for `type: "error"` or `status: "blocked"` entries
3. **Update plan**: Adjust next wave based on findings
4. **Compact if needed**: If tool calls are high or context feels heavy, run `/compact` with a summary of what's been accomplished and what's next
5. **Launch next wave**

### Step 7: Consolidate

After all waves complete:

```markdown
## Orchestration Complete

### Waves Executed: {N}
### Agents Spawned: {N}

### Results
- {Agent A}: {1-line summary from manifest}
- {Agent B}: {1-line summary from manifest}

### Follow-ups
- {Any followup entries from manifests}

### Manifests
All details at: _context/manifests/{date}/
```

## Wave Planning Guide

| Wave | Purpose | Agent Types |
|------|---------|-------------|
| 1: Research | Gather info, read files, search | Explore, file-analyzer |
| 2: Analysis | Process findings, plan | code-analyzer, planner |
| 3: Implementation | Write code, create files | general-purpose |
| 4: Verification | Test, review | test-runner, code-reviewer |

Not every task needs all 4 waves. Use the minimum needed.

## Rules

- The orchestrator NEVER does deep research itself. Delegate everything.
- Maximum 4 waves per orchestration. If more needed, break into separate orchestrations.
- Maximum 4 agents per wave. More than that is hard to coordinate.
- If a wave has only 1 agent, skip wave structure and just run the agent directly.
- Keep main session context lean: read manifests, do not replay full agent outputs.
- Between waves, consider if `/compact` would help. Use the strategic-compact decision guide.
- If all agents in a wave report success, move on quickly. Only pause for errors/blockers.

## Progressive Context Retrieval

Solves the "context problem" in multi-agent workflows where subagents don't know what context they need until they start working.

### The Problem

Subagents are spawned with limited context. Standard approaches fail:
- **Send everything**: Exceeds context limits
- **Send nothing**: Agent lacks critical information
- **Guess what's needed**: Often wrong

### The Solution: 4-Phase Iterative Loop

```
DISPATCH -> EVALUATE -> REFINE -> LOOP (max 3 cycles)
```

**Phase 1: DISPATCH** - Initial broad query to gather candidate files using patterns, keywords, and excludes.

**Phase 2: EVALUATE** - Score retrieved content for relevance (0-1 scale):
- High (0.8-1.0): Directly implements target functionality
- Medium (0.5-0.7): Contains related patterns or types
- Low (0.2-0.4): Tangentially related
- None (0-0.2): Not relevant, exclude

**Phase 3: REFINE** - Update search criteria based on evaluation:
- Add new patterns discovered in high-relevance files
- Add terminology found in codebase (first cycle often reveals naming conventions)
- Exclude confirmed irrelevant paths
- Target specific gaps identified during evaluation

**Phase 4: LOOP** - Repeat with refined criteria (max 3 cycles). Stop when 3+ high-relevance files found with no critical gaps.

### Integration with Agent Prompts

```markdown
When retrieving context for this task:
1. Start with broad keyword search
2. Evaluate each file's relevance (0-1 scale)
3. Identify what context is still missing
4. Refine search criteria and repeat (max 3 cycles)
5. Return files with relevance >= 0.7
```

### Best Practices

1. Start broad, narrow progressively
2. Learn codebase terminology from first cycle
3. Track what's missing explicitly to drive refinement
4. Stop at "good enough": 3 high-relevance files beats 10 mediocre ones
5. Exclude confidently: low-relevance files won't become relevant
