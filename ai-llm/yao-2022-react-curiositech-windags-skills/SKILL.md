---
license: Apache-2.0
name: yao-2022-react
description: Prompting paradigm combining reasoning traces with actions for LLM agents to interact with external tools
category: Research & Academic
tags:
  - react-prompting
  - reasoning
  - acting
  - llm-agents
  - tool-use
---

# ReAct: Reasoning-Action Synergy

## When to Use This Skill

Load this skill when addressing agent architecture design, debugging agent failures, designing information retrieval strategies, or making agent decision-making interpretable to humans.

## Decision Points

### 1. Knowledge Source Selection
```
IF agent expresses uncertainty (hedges, "I'm not sure", "might be")
   → THEN trigger external action (search, API call, retrieval)
IF agent states facts with high confidence AND domain is within training
   → THEN allow internal reasoning to continue
IF previous action returned "not found" or empty results
   → THEN reason about query reformulation strategy
IF factual accuracy is mission-critical (medical, legal, financial)
   → THEN default to external grounding regardless of confidence
```

### 2. Reasoning Density Control
```
IF task requires strategic planning or goal decomposition
   → THEN insert sparse, high-level thoughts at decision points
IF simple execution with known action sequence
   → THEN skip reasoning, execute actions directly
IF debugging failure or exception handling needed
   → THEN add reasoning trace to expose decision logic
IF token budget is constrained
   → THEN limit thoughts to: goal decomposition, search reformulation, exception handling
```

### 3. Failure Recovery Strategy
```
IF action returns unexpected result or error
   → THEN add thought analyzing what went wrong + corrective strategy
IF agent enters repetitive loop (same action 3+ times)
   → THEN force reasoning step: "Why am I stuck? What should I try instead?"
IF search returns empty/irrelevant results
   → THEN reason about query reformulation before next search
IF hallucinated information detected
   → THEN immediately insert retrieval action to verify facts
```

### 4. Multi-Step Task Orchestration
```
IF complex task with 4+ subtasks
   → THEN start with thought decomposing into subgoals
IF current subtask complete
   → THEN add thought tracking progress: "Done with X, now need Y"
IF environment state changed unexpectedly
   → THEN reason about how this affects remaining plan
IF stuck on subtask for 3+ actions
   → THEN reason about alternative approaches or skipping
```

## Failure Modes

### 1. **Reasoning Without Grounding** (Hallucination Spiral)
**Symptoms**: Agent confidently states facts, builds elaborate reasoning chains, but information is fabricated
**Detection Rule**: IF reasoning contains specific facts not verifiable through actions AND no recent external grounding
**Fix**: Insert retrieval actions at uncertainty points; verify facts before building on them

### 2. **Dense Narration Overhead** (Token Waste)
**Symptoms**: Thought at every step describing obvious actions or restating observations
**Detection Rule**: IF >60% of tokens are reasoning AND thoughts don't contain strategic decisions
**Fix**: Limit thoughts to: goal decomposition, search reformulation, exception handling, progress tracking

### 3. **Action Tunneling** (No Strategic Planning)
**Symptoms**: Agent immediately starts acting without decomposing complex tasks, gets stuck or inefficient
**Detection Rule**: IF complex multi-step task AND first action is attempted execution (not planning)
**Fix**: Force initial thought decomposing goal into subgoals and strategy

### 4. **Loop Trap** (Repetitive Failure)
**Symptoms**: Same action repeated 3+ times with same failure result, no learning from feedback
**Detection Rule**: IF identical action-observation pair occurs 3 consecutive times
**Fix**: Insert reasoning step analyzing why approach isn't working + alternative strategy

### 5. **Search Strategy Blindness** (Query Reformulation Failure)
**Symptoms**: Empty search results followed by identical or minimally different queries
**Detection Rule**: IF search returns "not found" AND next search query has >80% word overlap
**Fix**: Add explicit reasoning about why search failed + systematic query reformulation strategy

## Worked Examples

### Example 1: QA Task with Strategic Information Gathering
**Task**: "What is the elevation of the birthplace of the director of the movie 'Inception'?"

**Expert Trajectory**:
```
Thought 1: This requires finding: (1) director of Inception, (2) director's birthplace, (3) elevation of that place. Let me start with the director.
Action 1: Search[Inception movie director]
Observation 1: Christopher Nolan directed Inception (2010)...
Thought 2: Got it - Christopher Nolan. Now I need his birthplace.
Action 2: Search[Christopher Nolan birthplace]
Observation 2: Christopher Nolan was born in Westminster, London, England
Thought 3: Now I need the elevation of Westminster, London. This might be tricky since it's a district.
Action 3: Search[Westminster London elevation above sea level]
Observation 3: Westminster, London is approximately 24 meters (79 feet) above sea level
Thought 4: Found it. The elevation is 24 meters or 79 feet.
```

**Novice Mistakes**: Would search "Inception director birthplace elevation" immediately, get confused results mixing multiple concepts. Expert decomposes systematically and verifies each fact before building on it.

### Example 2: Error Recovery with Trade-off Analysis
**Task**: "Put a clean knife in the countertop" (ALFWorld navigation)

**Expert Recovery Trajectory**:
```
Action 1: take knife 1
Observation 1: You pick up the knife 1
Action 2: clean knife 1 with sinkbasin 1
Observation 2: Nothing happens.
Thought 1: Cleaning failed. I'm probably not at the right location. I need to navigate to the sinkbasin first, then clean the knife.
Action 3: go to sinkbasin 1
Observation 3: On the sinkbasin 1, you see a dishsponge 1, and a lettuce 1.
Action 4: clean knife 1 with sinkbasin 1
Observation 4: You clean the knife 1 using the sinkbasin 1.
Thought 2: Great! Now I have a clean knife. I need to find a countertop to place it on.
```

**Key Decision**: Expert recognizes failed action immediately, reasons about spatial requirements, adjusts strategy. Shows how external feedback corrects internal assumptions.

### Example 3: Multi-hop Reasoning with Confidence Monitoring
**Task**: "Were Scott Derrickson and Ed Wood of the same nationality?"

**Expert Trajectory**:
```
Thought 1: I need to find the nationality of both Scott Derrickson and Ed Wood, then compare them.
Action 1: Search[Scott Derrickson nationality]
Observation 1: Scott Derrickson is an American film director and screenwriter...
Thought 2: Scott Derrickson is American. Now I need Ed Wood's nationality.
Action 2: Search[Ed Wood nationality filmmaker]
Observation 2: Edward Davis Wood Jr. was an American filmmaker...
Thought 3: Ed Wood was also American. Both are American, so yes, they were the same nationality.
```

**Confidence Signal**: Expert searches for both facts despite potentially "knowing" Ed Wood is American, ensuring verification rather than risking hallucination.

## Quality Gates

- [ ] Each reasoning step addresses a specific decision point (goal decomposition, search reformulation, exception handling)
- [ ] Uncertain facts are verified through external actions before being used in subsequent reasoning
- [ ] Failed actions trigger corrective reasoning that analyzes root cause and alternative strategies
- [ ] Multi-step tasks begin with explicit goal decomposition into subgoals
- [ ] Search queries are reformulated when previous searches return empty/irrelevant results
- [ ] Reasoning traces are sparse (≤40% of total tokens) and strategic rather than descriptive
- [ ] Repetitive action loops are broken by reasoning steps that analyze why the approach isn't working
- [ ] External grounding occurs at least once every 3-4 reasoning steps for factual claims
- [ ] Complex tasks show clear progress tracking between subgoals in reasoning traces
- [ ] Final answer is directly supported by observable evidence from actions, not just internal reasoning

## NOT-FOR Boundaries

**Do NOT use ReAct for**:
- Simple, single-step tasks where immediate action is sufficient → Use direct action execution instead
- Creative writing or open-ended generation where grounding constrains desired output → Use pure chain-of-thought instead
- Highly structured API interactions with predetermined workflows → Use programmatic workflows instead
- Real-time systems where reasoning latency is prohibitive → Use learned policies or reactive systems instead
- Tasks requiring extensive mathematical computation → Use specialized math tools with minimal reasoning overhead instead

**Delegate to other skills when**:
- Task needs mathematical reasoning: Use `mathematical-reasoning-strategies` 
- Task is pure information synthesis: Use `chain-of-thought-reasoning`
- Task needs code generation: Use `code-generation-workflows`
- Task requires creative ideation: Use `creative-generation-techniques`