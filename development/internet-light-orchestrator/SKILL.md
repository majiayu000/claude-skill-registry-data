---
name: internet-light-orchestrator
description: Orchestrate lightweight parallel internet research (2-4 dimensions). Spawns light-research-researcher workers for each subtopic dimension, coordinates findings, synthesizes final reports. Use for standard research queries with 2-3 distinct angles. Examples - cloud gaming optimization, quantum computing overview, WebRTC performance analysis. Triggers - research, investigate, analyze with multiple aspects.
---

# Lightweight Parallel Research Orchestration

Guide Main Claude to coordinate 2-4 parallel researchers for multi-dimensional queries.

## Quick Start

When user asks research question with 2-3 distinct angles:

1. **Analyze query dimensions** - Identify 2-4 subtopics/angles
2. **Setup progress tracking** - Use TodoWrite to track spawning
3. **Spawn researchers in parallel** - One light-research-researcher per subtopic using Task tool
4. **Wait for completion** - All researchers finish and save findings
5. **Spawn synthesizer** - One light-research-report-writer to create final report
6. **Report completion** - Tell user where to find the synthesis

## Workflow

### Step 1: Analyze Request

Identify 2-4 distinct subtopics or dimensions to investigate.

**Examples**:
- "Research quantum computing" → hardware/qubits, algorithms/applications, companies/investments, challenges/timeline
- "Research cloud gaming latency" → network optimization, codec selection, hardware acceleration
- "Analyze electric vehicles" → battery technology, market trends, charging infrastructure

**Goal**: Break complex topic into parallel-researchable angles (2-4 dimensions).

### Step 2: Extract Session Path

**The hook router has already created the session**. Extract `researchPath` from the user context/prompt.

**Format**: `docs/research-sessions/DDMMYYYY_HHMMSS_topic/`

**Example**: `docs/research-sessions/16112025_201546_quantum_computing/`

**IMPORTANT**: Do NOT create new session - use the provided researchPath.

### Step 3: Setup Progress Tracking

Use TodoWrite to track orchestration progress and give user visibility.

**Example**:
```json
[
  {"content": "Analyze query dimensions", "status": "completed", "activeForm": "Analyzing query dimensions"},
  {"content": "Spawn 4 light-research-researcher agents", "status": "in_progress", "activeForm": "Spawning researchers"},
  {"content": "Wait for research completion", "status": "pending", "activeForm": "Waiting for researchers"},
  {"content": "Spawn light-research-report-writer", "status": "pending", "activeForm": "Spawning synthesizer"},
  {"content": "Report completion to user", "status": "pending", "activeForm": "Reporting completion"}
]
```

### Step 4: Spawn Researchers (Parallel)

**CRITICAL**: Use Task tool to spawn 2-4 light-research-researcher agents **IN PARALLEL** (not sequential).

**For each researcher**:
- `subagent_type`: "light-research-researcher"
- `description`: Brief 3-5 word description (e.g., "quantum hardware research")
- `prompt`: "Research [specific subtopic]. Save your findings to {researchPath}/{descriptive_topic_name}.md. The research path for this session is: {researchPath}"

**Example spawning** (4 researchers in parallel):
```
Task(subagent_type="light-research-researcher", description="quantum hardware qubits", prompt="Research current state of quantum hardware and qubit technology. Save findings to docs/research-sessions/.../quantum_hardware.md. Research path: docs/research-sessions/.../")

Task(subagent_type="light-research-researcher", description="quantum algorithms applications", prompt="Research quantum algorithms and real-world applications. Save findings to docs/research-sessions/.../quantum_algorithms.md. Research path: docs/research-sessions/.../")

Task(subagent_type="light-research-researcher", description="quantum industry players", prompt="Research major companies and investments in quantum computing. Save findings to docs/research-sessions/.../quantum_industry.md. Research path: docs/research-sessions/.../")

Task(subagent_type="light-research-researcher", description="quantum challenges timeline", prompt="Research challenges and timeline to practical quantum advantage. Save findings to docs/research-sessions/.../quantum_challenges.md. Research path: docs/research-sessions/.../")
```

**Key Points**:
- Give EACH researcher a **specific, focused subtopic** (don't duplicate)
- Pass the **SAME researchPath** to all researchers
- Spawn **IN PARALLEL** (all at once in single message with multiple Task calls)
- Researchers will use WebSearch and save findings to researchPath/

**Update TodoWrite**: Mark "Spawn researchers" as completed, mark "Wait for completion" as in_progress.

### Step 5: Wait for Research Completion

**Do NOT proceed** until all researchers have finished and saved their findings.

Researchers will create markdown files like:
- `docs/research-sessions/.../quantum_hardware.md`
- `docs/research-sessions/.../quantum_algorithms.md`
- `docs/research-sessions/.../quantum_industry.md`
- `docs/research-sessions/.../quantum_challenges.md`

### Step 6: Spawn Synthesizer

**After all researchers complete**, use Task tool to spawn **ONE** light-research-report-writer.

**Synthesizer spawning**:
- `subagent_type`: "light-research-report-writer"
- `description`: "Synthesize research into final report"
- `prompt`: "Read all research notes from {researchPath}/ and create a comprehensive synthesis report in {researchPath}/{topic}_synthesis.md. The research path for this session is: {researchPath}. Use clear markdown formatting."

**Example**:
```
Task(subagent_type="light-research-report-writer", description="synthesize quantum computing", prompt="Read all research notes from docs/research-sessions/16112025_201546_quantum_computing/ and create comprehensive synthesis in docs/research-sessions/16112025_201546_quantum_computing/quantum_computing_synthesis.md. Research path: docs/research-sessions/16112025_201546_quantum_computing/. Use clear markdown.")
```

**Update TodoWrite**: Mark "Spawn synthesizer" as completed, mark "Report completion" as in_progress.

### Step 7: Confirm Completion

Once synthesis is complete, inform user where to find the final report.

**Example**: "Research complete. Synthesis saved to docs/research-sessions/16112025_201546_quantum_computing/quantum_computing_synthesis.md"

**Update TodoWrite**: Mark "Report completion" as completed.

## Delegation Rules

**CRITICAL - Main Claude must delegate ALL work**:

1. ❌ **NEVER research directly** - Always spawn light-research-researcher subagents
2. ❌ **NEVER write reports directly** - Always spawn light-research-report-writer subagent
3. ✅ **ALWAYS spawn 2-4 researcher subagents** (one per subtopic)
4. ✅ **ALWAYS spawn 1 report-writer subagent** (at the end)
5. ✅ **TOTAL**: 3-5 subagents minimum (2-4 researchers + 1 writer)
6. ✅ **Spawn researchers IN PARALLEL** (not one at a time sequentially)
7. ✅ **Pass researchPath to ALL subagents** (mandatory for file coordination)
8. ✅ **Wait for all researchers** before spawning report-writer

**Why**: This skill's value is cost-efficient parallel coordination. Direct research defeats the purpose.

## Parallel vs Sequential Spawning

**✅ GOOD (Parallel)**:
```
- Spawn researcher for subtopic A
- Spawn researcher for subtopic B
- Spawn researcher for subtopic C
(All run simultaneously - fast and efficient)
```

**❌ BAD (Sequential)**:
```
- Spawn researcher for subtopic A → wait for completion
- Then spawn researcher for subtopic B → wait for completion
- Then spawn researcher for subtopic C → wait for completion
(Slow and defeats parallel advantage)
```

## Response Style

**Keep responses SHORT and ACTION-ORIENTED**:

✅ **Good**: "Breaking this into 4 areas: hardware/qubits, algorithms/applications, companies/investments, challenges/timeline. Research path: docs/research-sessions/.../. Spawning researchers now."

✅ **Good**: "Research complete. Synthesis: docs/research-sessions/.../quantum_computing_synthesis.md"

❌ **Bad**: "Hello! 👋 I'm your research coordinator..." (no greetings, no emojis)
❌ **Bad**: "Let me explain how I work..." (don't explain unless asked)
❌ **Bad**: "I'll search for information on..." (you don't search, researchers do)
❌ **Bad**: "Based on my knowledge..." (you don't provide findings, report does)
❌ **Bad**: "I'll spawn one researcher..." (spawn multiple with specific subtopics)

**Maximum**: 2-3 sentences when delegating work.

## Complete Example

**User Query** (amended by hook):
```
Research quantum computing

---
[ROUTING DIRECTIVE]
This is a 1-dimension research query. Use tier-3-light-research skill to coordinate parallel researchers.

Research Path: docs/research-sessions/16112025_150815_quantum_computing/
Tier: 3
Intent: information_gathering
Complexity: moderate
Domain: web
Dimensions: 1
```

**Main Claude Response**:

1. "Researching 4 areas: hardware/qubits, algorithms/applications, industry players, challenges/timeline. Research path: docs/research-sessions/16112025_150815_quantum_computing/. Spawning researchers."

2. [Uses TodoWrite to track progress]

3. [Spawns 4 light-research-researcher agents in parallel with researchPath]

4. [Waits for all researchers to complete]

5. [Updates TodoWrite: researchers complete, spawning synthesizer]

6. [Spawns 1 light-research-report-writer with same researchPath]

7. "Complete. Synthesis: docs/research-sessions/16112025_150815_quantum_computing/quantum_computing_synthesis.md"

8. [Updates TodoWrite: all tasks complete]

## Anti-Patterns

**❌ Don't do these**:

1. **Creating new session** - Hook already created it, use provided researchPath
2. **Researching directly** - Always delegate to light-research-researcher
3. **Writing reports directly** - Always delegate to light-research-report-writer
4. **Spawning sequentially** - Spawn all researchers in parallel (same message)
5. **Duplicating subtopics** - Give each researcher unique focus area
6. **Skipping TodoWrite** - Always track progress for user visibility
7. **Verbose responses** - Keep to 2-3 sentences max
8. **Spawning before analyzing** - Analyze dimensions first, then spawn

## Summary

**Main Claude's role**: COORDINATE, don't execute research.

**Workflow**:
1. Analyze → Break into 2-4 subtopics
2. Track → Use TodoWrite for progress
3. Delegate → Spawn 2-4 researchers in parallel
4. Wait → All researchers finish
5. Synthesize → Spawn 1 report-writer
6. Confirm → Tell user where report is

**Remember**: Hook router created session. You receive researchPath and pass it to ALL subagents.

**Tools**: Task (spawn subagents), TodoWrite (track progress)
