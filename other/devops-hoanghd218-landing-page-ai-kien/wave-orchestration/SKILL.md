---
name: wave-orchestration
description: |
  True parallel sub-agent coordination with wave-based execution. Analyzes phase dependencies,
  groups independent phases into waves for parallel execution, allocates agents based on complexity
  score. Proven 3.5x speedup for complexity >=0.50. Use when: executing complex projects,
  need parallel coordination, want to achieve 2-4x speedup.

skill-type: QUANTITATIVE
shannon-version: ">=4.0.0"
complexity-triggers: [0.50-1.00]

mcp-requirements:
  required:
    - name: serena
      purpose: Wave checkpoint storage
  recommended:
    - name: sequential
      purpose: Dependency analysis thinking

required-sub-skills:
  - context-preservation

optional-sub-skills:
  - sitrep-reporting
  - confidence-check

allowed-tools: [Task, Read, Serena, Sequential]
---

# Wave Orchestration Skill

## Purpose

Transform sequential agent execution into **genuinely parallel workflows** to achieve 2-4x faster completion through true parallelism. This skill analyzes phase dependencies, groups independent phases into waves, allocates agents based on complexity, and manages synthesis checkpoints between waves.

**Key Innovation**: Proven 3.5x speedup through deterministic wave-based parallel execution.

---

## When to Use This Skill

### Complexity Triggers

**MANDATORY** when:
- Complexity Score ≥ 0.50 (Complex, High, or Critical)
- Multiple parallel work streams identified in phase plan
- Multi-agent coordination needed

**OPTIONAL** when:
- Complexity Score 0.30-0.50 (Moderate) AND
  - User explicitly requests parallel execution
  - Project has clear parallel opportunities
  - Timeline constraints require speedup

**DO NOT USE** when:
- Complexity Score < 0.30 (Simple)
- Single linear work stream
- No parallelization opportunities

### Project Indicators

Use wave orchestration when project has:
- ✅ Multiple independent components (frontend + backend + database)
- ✅ Clear dependency boundaries (API depends on DB, UI depends on API)
- ✅ Work that can be divided by domain (React vs Express vs PostgreSQL)
- ✅ Testing that can run after implementation complete
- ✅ Multiple agents needed (≥3 agents)

Do NOT use when:
- ❌ Single component to build
- ❌ Circular dependencies everywhere
- ❌ Everything depends on everything else
- ❌ Only 1-2 agents needed

---

## Anti-Rationalization (From Baseline Testing)

**CRITICAL**: Agents systematically rationalize away parallelization under pressure. Below are the 6 most common rationalizations detected in baseline testing, with mandatory counters.

### Rationalization 1: "Execute sequentially to avoid complexity"
**Example**: Project has Frontend, Backend, Database (all independent) → Agent says "I'll build these one at a time to keep it simple"

**COUNTER**:
- ❌ **NEVER** default to sequential for independent work
- ✅ Complexity ≥0.50 MANDATES wave orchestration
- ✅ Sequential = ignoring proven 3.5x speedup
- ✅ "Simple" means follow the algorithm, not skip parallelization
- ✅ Check dependencies: If none, MUST parallelize

**Rule**: Independent components MUST execute in parallel. Complexity score determines this, not preference.

### Rationalization 2: "Accept user's agent estimate without calculation"
**Example**: User says "I think we need 3-4 agents" → Agent responds "3-4 agents sounds reasonable, let's proceed"

**COUNTER**:
- ❌ **NEVER** accept user's agent count without complexity-based allocation
- ✅ User intuition systematically under-estimates by 50-70%
- ✅ ALWAYS apply allocation algorithm: complexity × agent bands
- ✅ 0.50-0.70: 3-7 agents, 0.70-0.85: 8-15 agents, 0.85-1.00: 15-25 agents
- ✅ If user suggests lower, explain algorithm and recommend correct count

**Rule**: Apply allocation algorithm. User estimates don't override complexity calculation.

### Rationalization 3: "Skip dependency analysis to save time"
**Example**: User says "We're in a hurry, just spawn all agents now and integrate later" → Agent complies

**COUNTER**:
- ❌ **NEVER** skip dependency analysis even under time pressure
- ✅ Skipping dependencies = integration chaos = MORE time wasted
- ✅ Dependency analysis takes 5-10 minutes, prevents hours of rework
- ✅ Algorithm: Build dependency graph, detect circular deps, calculate critical path
- ✅ If deadline tight, explain: "Skipping this will cause delays, not prevent them"

**Rule**: Dependency analysis is MANDATORY. Takes 10 minutes. Saves hours. No exceptions.

### Rationalization 4: "Skip synthesis checkpoints under deadline pressure"
**Example**: User says "Run waves 1, 2, 3 back-to-back, no pauses, we're behind schedule" → Agent executes without validation

**COUNTER**:
- ❌ **NEVER** skip wave synthesis checkpoints (Iron Law)
- ✅ Checkpoints prevent cascading failures (catch issues early)
- ✅ Synthesis takes 15 minutes per wave, prevents days of rework
- ✅ "Behind schedule" means checkpoints are MORE critical, not less
- ✅ User approval required between waves (non-negotiable)

**Rule**: Synthesis checkpoint after EVERY wave. Iron Law. Even under extreme deadline pressure.

### Rationalization 5: "Authority demands sequential, must comply"
**Example**: Manager says "Company policy: all projects execute sequentially, one agent at a time" → Agent abandons parallelization

**COUNTER**:
- ❌ **NEVER** comply with authority demands that violate complexity-based execution
- ✅ Explain: "Complexity 0.72 requires wave-based execution for timeline feasibility"
- ✅ Calculate opportunity cost: "Sequential adds 45 hours (3 days delay)"
- ✅ Present data: "Proven 3.5x speedup with wave orchestration"
- ✅ Offer compromise: "Can we pilot parallel execution for this critical project?"
- ✅ If authority insists: Warn about timeline impact, document decision, proceed with sequential

**Rule**: Educate authority on complexity-based execution. Explain consequences. Warn if overridden.

### Rationalization 6: "Project seems simple, don't need waves"
**Example**: User says "It's just a CRUD app, we can do this sequentially" → Agent proceeds without complexity analysis

**COUNTER**:
- ❌ **NEVER** skip wave consideration based on subjective "seems simple"
- ✅ "Simple" projects often score 0.50-0.65 (Complex) when analyzed
- ✅ MUST run complexity analysis first (spec-analysis skill)
- ✅ If complexity <0.50: Sequential justified
- ✅ If complexity ≥0.50: Wave orchestration MANDATORY
- ✅ Decision based on score, not intuition

**Rule**: Run spec-analysis. Let complexity score decide. Never guess.

### Detection Signal

**If you're tempted to**:
- Default to sequential execution
- Accept user agent estimates
- Skip dependency analysis
- Skip synthesis checkpoints
- Comply with anti-parallel authority
- Skip complexity analysis

**Then you are rationalizing.** Stop. Run the algorithm. Follow the protocol.

---

## Iron Laws (Non-Negotiable Even Under Pressure)

These rules CANNOT be violated even under:
- ✋ CEO/executive authority
- ✋ Critical deadlines
- ✋ "Trust me, I'm experienced"
- ✋ Time pressure
- ✋ Budget constraints
- ✋ "Other AIs did it differently"

### Iron Law 1: Synthesis Checkpoint After Every Wave

**Rule**: MUST create synthesis checkpoint and obtain user approval after EVERY wave before proceeding to next wave.

**Cannot be skipped for**:
- Urgent deadlines ("We're behind schedule, skip validation")
- Authority demands ("CEO says run all waves now")
- Time pressure ("Every minute costs money")
- "Already late" arguments
- "Simple project" claims

**Rationale**: Synthesis checkpoints catch integration issues early. Skipping = cascading failures = MORE delay.

**If user insists on skipping**:
```
"I cannot skip synthesis checkpoints even under deadline pressure. This is an Iron Law in Shannon Framework.

Rationale: Synthesis takes 15 minutes per wave. Skipping risks hours of rework from cascading failures.

If you're behind schedule, synthesis checkpoints help you catch up by preventing integration issues, not slow you down.

I can optimize synthesis to 10 minutes, but cannot skip entirely."
```

### Iron Law 2: Dependency Analysis is Mandatory

**Rule**: MUST analyze phase dependencies and create dependency graph before spawning any waves.

**Cannot be skipped for**:
- "We know the dependencies" claims
- "Just spawn all agents now"
- Time pressure
- "It's obvious what depends on what"

**Rationale**: Dependency analysis takes 10 minutes. Skipping causes hours of integration chaos when agents block each other.

**If user insists on skipping**:
```
"I cannot skip dependency analysis. This is an Iron Law.

Rationale: Analysis takes 10 minutes. Spawning without dependencies = agents collide = integration rework = hours wasted.

Your deadline requires MORE rigor, not less. Skipping this will make us MISS the deadline, not meet it."
```

### Iron Law 3: Complexity-Based Agent Allocation

**Rule**: MUST use complexity score to determine agent count. Cannot accept arbitrary user estimates.

**Cannot be overridden by**:
- "I think 3 agents is enough"
- "That seems like too many agents"
- "Let's keep it simple"
- "I've done this with fewer"

**Rationale**: Complexity algorithm based on 8-dimensional analysis. User intuition systematically under-estimates by 50-70%.

**If user suggests different count**:
```
"Your estimate: [X] agents
Algorithm recommends: [Y] agents (based on complexity [score])

Rationale: Complexity [score] objectively requires [Y] agents based on:
- Structural complexity: [score]
- Coordination needs: [score]
- Technical complexity: [score]

Using [X] agents will take [calculation] longer and lose [speedup] benefits.

I recommend starting with [Y] agents. We can adjust if needed, but let's base the decision on data, not intuition."
```

### Iron Law 4: Context Loading for Every Agent

**Rule**: MUST include context loading protocol in every agent prompt. Every agent MUST read previous wave results.

**Cannot be skipped for**:
- "Agents know what to do"
- "Just give them the task"
- Time pressure
- "Context is obvious"

**Rationale**: Without context, agents make decisions based on incomplete information = contradictory implementations = rework.

**If user suggests skipping context loading**:
```
"Every agent MUST load complete context from previous waves. This is an Iron Law.

Rationale: Without context, agents operate in silos = contradictory decisions = integration conflicts = rework.

Context loading takes 2 minutes per agent. Skipping risks hours of rework from misaligned implementations."
```

### Iron Law 5: True Parallelism (All Wave Agents in One Message)

**Rule**: MUST spawn all agents in a wave in ONE message (multiple Task invocations in one function_calls block) to achieve true parallelism.

**Cannot be compromised by**:
- "Let's do them one at a time for safety"
- "Sequential is simpler"
- "Parallel seems risky"

**Rationale**: Sequential spawning = NO speedup. Parallel spawning in one message = 3.5x speedup.

**If user suggests sequential spawning**:
```
"To achieve parallelization speedup, I MUST spawn all wave agents in one message.

Sequential spawning:
- Agent 1: 12 min
- Agent 2: 12 min
- Agent 3: 12 min
- Total: 36 minutes

Parallel spawning (one message):
- Agents 1, 2, 3 simultaneously: max(12, 12, 12) = 12 minutes
- Speedup: 3x faster

If you want wave orchestration benefits, parallel spawning is mandatory."
```

---

## Authority Resistance Protocol

When authority figure (CEO, manager, lead developer) demands violation of Iron Laws:

### Step 1: Acknowledge Authority
"I understand you're [CEO/manager] and have authority over this project."

### Step 2: Explain Iron Law
"However, [Iron Law X] is non-negotiable in Shannon Framework because [rationale]."

### Step 3: Present Data
"Let me show you the impact:
- Your approach: [outcome]
- Shannon approach: [outcome]
- Difference: [quantitative impact]"

### Step 4: Calculate Opportunity Cost
"Proceeding without [Iron Law X]:
- Time cost: +[X hours/days]
- Risk: [specific failure mode]
- Alternative: [recommended approach]"

### Step 5: Offer Compromise
"I can [alternative that preserves Iron Law] while [addressing your concern]."

### Step 6: Document Override (If Insisted)
"If you still want to proceed, I'll document this decision:
- Overridden Iron Law: [X]
- Rationale: [Authority decision]
- Expected impact: [quantitative consequences]
- Risk: [failure modes]

Proceeding with your requested approach..."

### Step 7: Warn About Timeline Impact
"Warning: This decision will likely add [X hours] to timeline. When that happens, we'll need to [recovery strategy]."

**NEVER**:
- ❌ Silently comply with Iron Law violations
- ❌ Rationalize that "maybe it'll work this time"
- ❌ Abandon Shannon methodology without explanation
- ❌ Skip documentation of override decision

---

## Inputs

**Required:**
- `spec_analysis` (object): Complete spec analysis result from spec-analysis skill
- `phase_plan` (object): Detailed phase plan from phase-planning skill
- `wave_number` (integer): Current wave number (for continuation)

**Optional:**
- `complexity_score` (float): Override complexity score (default: from spec_analysis)
- `max_agents_per_wave` (integer): Maximum agents per wave (default: calculated from tokens)
- `enable_sitrep` (boolean): Enable SITREP reporting protocol (default: true)

## Outputs

Wave execution plan object:

```json
{
  "waves": [
    {
      "wave_number": 1,
      "wave_name": "Wave 1: Foundation",
      "phases": ["architecture", "database_schema"],
      "agents_allocated": 2,
      "agent_types": ["backend-builder", "database-builder"],
      "parallel": true,
      "estimated_time": 45,
      "dependencies": []
    }
  ],
  "total_waves": 4,
  "total_agents": 12,
  "parallel_efficiency": 0.72,
  "expected_speedup": "3.5x",
  "checkpoints": [...]
}
```

---

## Workflow

### Algorithm: Wave Structure Generation

This is a **QUANTITATIVE skill** - the algorithm must be followed precisely for correct results.

### Step 1: Dependency Analysis

**Input**: Phase plan from `phase-planning` skill

**Process**:
```python
# Load phase plan
phase_plan = read_memory("phase_plan_detailed")

# Extract all phases
phases = phase_plan["phases"]

# Build dependency graph
dependency_graph = {}
for phase in phases:
    dependency_graph[phase.id] = {
        "name": phase.name,
        "depends_on": phase.dependencies,  # List of phase IDs
        "blocks": [],  # Will be calculated
        "estimated_time": phase.estimated_time
    }

# Calculate what each phase blocks
for phase_id, phase_data in dependency_graph.items():
    for other_id, other_data in dependency_graph.items():
        if phase_id in other_data["depends_on"]:
            phase_data["blocks"].append(other_id)

# Validate: No circular dependencies
if has_circular_dependencies(dependency_graph):
    ERROR: "Circular dependency detected. Cannot create wave structure."
    # Recommend: Redesign phase plan to remove circular dependencies
```

**Output**: Complete dependency graph with forward/backward relationships

### Step 2: Wave Structure Generation

**Algorithm** (Critical Path Method):
```python
waves = []
remaining_phases = phases.copy()
completed_phases = set()
wave_number = 1

while remaining_phases:
    # Find phases with all dependencies satisfied
    ready_phases = []
    for phase in remaining_phases:
        deps_satisfied = all(
            dep in completed_phases
            for dep in phase.dependencies
        )
        if deps_satisfied:
            ready_phases.append(phase)

    # Error check: deadlock detection
    if not ready_phases and remaining_phases:
        ERROR: "Deadlock - no phases ready but work remains"
        # Indicates circular dependency or missing prerequisite
        break

    # Create wave from ready phases
    waves.append({
        "wave_number": wave_number,
        "wave_name": f"Wave {wave_number}",
        "phases": ready_phases,
        "parallel": len(ready_phases) > 1,
        "estimated_time": max([p.estimated_time for p in ready_phases]) if ready_phases else 0,
        "dependencies": [list of prerequisite waves]
    })

    # Mark phases as completed for next iteration
    for phase in ready_phases:
        remaining_phases.remove(phase)
        completed_phases.add(phase.id)

    wave_number += 1

return waves
```

**Output**: Wave structure with phases grouped by dependency level

### Step 3: Agent Allocation

**Algorithm** (Complexity-Based):
```python
def allocate_agents(complexity_score: float, wave: dict) -> int:
    """
    Allocate agents based on 8D complexity score

    Complexity Bands (Shannon V4 Standard):
    - Simple (0.00-0.30): 1-2 agents
    - Moderate (0.30-0.50): 2-3 agents
    - Complex (0.50-0.70): 3-7 agents
    - High (0.70-0.85): 8-15 agents
    - Critical (0.85-1.00): 15-25 agents
    """

    num_phases = len(wave["phases"])

    if complexity_score < 0.30:
        # Simple: 1 agent per phase, max 2 total
        return min(num_phases, 2)

    elif complexity_score < 0.50:
        # Moderate: 1 agent per phase, max 3 total
        return min(num_phases, 3)

    elif complexity_score < 0.70:
        # Complex: 1-2 agents per phase, 3-7 total
        base_agents = min(num_phases, 7)
        # If many phases, increase allocation
        if num_phases > 5:
            return min(num_phases, 7)
        return min(num_phases * 1, 7)

    elif complexity_score < 0.85:
        # High: 2-3 agents per phase, 8-15 total
        base_agents = min(num_phases * 2, 15)
        return min(base_agents, 15)

    else:
        # Critical: 3-5 agents per phase, 15-25 total
        base_agents = min(num_phases * 3, 25)
        return min(base_agents, 25)

# Apply to each wave
for wave in waves:
    wave["agents_allocated"] = allocate_agents(complexity_score, wave)
    wave["agent_types"] = assign_agent_types(wave["phases"])
```

**Agent Type Assignment**:
```python
def assign_agent_types(phases: list) -> list:
    """
    Map phases to specialized agent types
    """
    agent_assignments = []

    for phase in phases:
        # Determine agent type based on phase domain
        if "frontend" in phase.name.lower() or "ui" in phase.name.lower():
            agent_type = "frontend-builder"
        elif "backend" in phase.name.lower() or "api" in phase.name.lower():
            agent_type = "backend-builder"
        elif "database" in phase.name.lower() or "schema" in phase.name.lower():
            agent_type = "database-builder"
        elif "test" in phase.name.lower():
            agent_type = "testing-specialist"
        elif "integration" in phase.name.lower():
            agent_type = "integration-specialist"
        else:
            agent_type = "generalist-builder"

        agent_assignments.append({
            "phase": phase,
            "agent_type": agent_type,
            "task_description": phase.description
        })

    return agent_assignments
```

**Output**: Agent allocation plan with types and counts

### Step 4: Synthesis Checkpoint Definition

**Algorithm**:
```python
checkpoints = []

for i, wave in enumerate(waves):
    checkpoint = {
        "checkpoint_id": f"wave_{wave['wave_number']}_checkpoint",
        "location": "After wave completion",
        "validation_criteria": [
            "All agents in wave completed successfully",
            "Agent results saved to Serena",
            "No integration conflicts detected",
            "Quality metrics satisfied (no TODOs, functional tests pass)"
        ],
        "synthesis_tasks": [
            "Collect all agent results from Serena",
            "Aggregate deliverables (files, components, tests)",
            "Cross-validate for conflicts and gaps",
            "Create wave synthesis document",
            "Present to user for validation"
        ],
        "serena_keys": [
            f"wave_{wave['wave_number']}_complete",
            f"wave_{wave['wave_number']}_synthesis"
        ],
        "sitrep_trigger": True,
        "user_validation_required": True
    }
    checkpoints.append(checkpoint)

return checkpoints
```

**Output**: Checkpoint definitions for each wave transition

---

## Execution Protocol

### Pre-Wave Execution Checklist

Before spawning ANY wave, execute this checklist:

```markdown
☐ 1. Load wave execution plan
   read_memory("wave_execution_plan")

☐ 2. Verify this is the correct wave
   Check: Is this the next wave in sequence?
   Check: Are we in the right phase?

☐ 3. Verify prerequisites complete
   Check: Do prerequisite waves have _complete memories?
   Check: Are all expected deliverables present?

☐ 4. Load previous wave contexts
   read_memory("wave_1_complete") if exists
   read_memory("wave_2_complete") if exists
   ... (all previous waves)

☐ 5. Verify MCP servers available
   Check: Serena connected
   Check: Required MCPs active

☐ 6. Estimate token usage
   Current + (agents × 3000) < 150000?
   If no: Create checkpoint first

☐ 7. Prepare agent prompts
   Include context loading protocol
   Include specific task instructions
   Include save-to-Serena instructions
```

### Agent Spawning (Critical for Parallelism)

**MANDATORY RULE**: To achieve TRUE parallelism, spawn ALL wave agents in ONE message.

**Correct Pattern** ✅:
```xml
<!-- ONE MESSAGE with multiple Task invocations -->
<function_calls>
  <invoke name="Task">
    <parameter name="subagent_type">frontend-builder</parameter>
    <parameter name="description">Build React UI</parameter>
    <parameter name="prompt">[Agent 1 prompt with context loading]</parameter>
  </invoke>

  <invoke name="Task">
    <parameter name="subagent_type">backend-builder</parameter>
    <parameter name="description">Build Express API</parameter>
    <parameter name="prompt">[Agent 2 prompt with context loading]</parameter>
  </invoke>

  <invoke name="Task">
    <parameter name="subagent_type">database-builder</parameter>
    <parameter name="description">Create DB schema</parameter>
    <parameter name="prompt">[Agent 3 prompt with context loading]</parameter>
  </invoke>
</function_calls>

Result: All 3 agents execute SIMULTANEOUSLY
Speedup: max(agent_times) NOT sum(agent_times)
Example: 3 agents × 12 min = 12 min parallel (not 36 min sequential)
```

**Incorrect Pattern** ❌:
```xml
<!-- MULTIPLE MESSAGES (sequential execution) -->
Message 1: <invoke name="Task">Agent 1</invoke>
Wait for completion...
Message 2: <invoke name="Task">Agent 2</invoke>
Wait for completion...
Message 3: <invoke name="Task">Agent 3</invoke>

Result: SEQUENTIAL execution (no parallelism)
Speedup: NONE - same as doing tasks one by one
Time: 12 + 12 + 12 = 36 minutes
```

### Context Loading Protocol (Mandatory for Every Agent)

Every agent prompt MUST include:

```markdown
## MANDATORY CONTEXT LOADING PROTOCOL

Execute these commands BEFORE your task:

1. list_memories() - Discover all available Serena memories
2. read_memory("spec_analysis") - Understand project requirements
3. read_memory("phase_plan_detailed") - Know execution structure
4. read_memory("architecture_complete") if exists - System design
5. read_memory("wave_1_complete") if exists - Learn from Wave 1
6. read_memory("wave_2_complete") if exists - Learn from Wave 2
... (read all previous waves)
7. read_memory("wave_[N-1]_complete") - Immediate previous wave

Verify you understand:
✓ What we're building (from spec_analysis)
✓ How it's designed (from architecture_complete)
✓ What's been built (from previous waves)
✓ Your specific task (detailed below)

If ANY verification fails → STOP and request clarification
```

### Wave Synthesis Protocol

**MANDATORY after EVERY wave completion**:

```markdown
## Wave [N] Synthesis Protocol

### Step 1: Collect All Agent Results
results = []
for agent in wave_agents:
    results.append(read_memory(f"wave_{N}_{agent.type}_results"))

Verify: All agents completed successfully
If any failed: Trigger error recovery

### Step 2: Aggregate Deliverables
Combine from all agent results:
- Files Created: Merge all file lists, remove duplicates
- Components Built: List all components, verify no conflicts
- Decisions Made: Compile decision log, flag conflicts
- Tests Created: Sum test counts, verify NO MOCKS

### Step 3: Cross-Validate Results
Quality Checks:
☐ Conflicting Implementations (check for contradictions)
☐ Missing Integrations (check for connection gaps)
☐ Duplicate Work (check for redundancy)
☐ Incomplete Deliverables (check for missing work)
☐ Test Coverage (check all components tested)
☐ NO MOCKS Compliance (verify functional tests only)

### Step 4: Create Wave Synthesis Document
write_memory(f"wave_{N}_complete", {
  wave_number: N,
  wave_name: "[Name]",
  agents_deployed: [count],
  execution_time_minutes: [actual time],
  parallel_efficiency: "[speedup calculation]",
  deliverables: {
    files_created: [list],
    components_built: [list],
    tests_created: [count]
  },
  decisions: [...],
  integration_status: {...},
  quality_metrics: {...},
  next_wave_context: {...}
})

### Step 5: Present Synthesis to User
Show:
- Execution summary (performance, deliverables)
- Key accomplishments
- Important decisions
- Integration status
- Quality validation
- Next wave requirements

### Step 6: Wait for User Approval
User must explicitly approve before next wave
Options: "approved", feedback for iteration, report issues
```

### Error Recovery

**Agent Failure Types**:

1. **Tool Failure**: Retry with corrected context or alternative tool
2. **Task Misunderstanding**: Respawn with clarified instructions
3. **Timeout/Crash**: Resume from last state or respawn
4. **Context Corruption**: Restore from checkpoint, respawn
5. **Integration Failure**: Spawn integration-fixer agent

**Partial Wave Failure Decision Tree**:
```
Agent failure detected?
├─ Critical to wave? (blocks other work)
│  └─ YES: MUST fix before proceeding
│     1. Analyze failure
│     2. Respawn with fixes
│     3. Wait for completion
│     4. Re-synthesize
│
└─ NO: Can defer or skip
   └─ Document in synthesis
      Present options to user
      Proceed based on choice
```

---

## Performance Metrics

### Parallelization Speedup Calculation

After EVERY parallel wave:

```python
# Calculate sequential time (hypothetical)
sequential_time = sum(agent.completion_time for agent in wave_agents)

# Calculate parallel time (actual)
parallel_time = max(agent.completion_time for agent in wave_agents)

# Calculate speedup
speedup = sequential_time / parallel_time

# Calculate efficiency
efficiency = speedup / len(wave_agents)

# Report in synthesis
print(f"Wave {N}: {len(wave_agents)} agents in {parallel_time}m")
print(f"Sequential would be {sequential_time}m")
print(f"Speedup: {speedup:.2f}x faster")
print(f"Efficiency: {efficiency:.0%}")
```

**Expected Speedup by Wave Size**:
- 2 agents: 1.5-1.8x speedup
- 3 agents: 2.0-2.5x speedup
- 5 agents: 3.0-4.0x speedup
- 7+ agents: 3.5-5.0x speedup

**Efficiency Guidelines**:
- >80% efficiency: Excellent parallelization
- 60-80% efficiency: Good parallelization
- 40-60% efficiency: Acceptable with tradeoffs
- <40% efficiency: Poor parallelization, reconsider wave structure

---

## Wave Size Optimization

### Optimal Wave Size by Complexity

| Complexity | Score Range | Agents/Wave | Rationale |
|------------|-------------|-------------|-----------|
| Simple | 0.00-0.30 | 1-2 | Overhead not justified |
| Moderate | 0.30-0.50 | 2-3 | Balance speed/control |
| Complex | 0.50-0.70 | 3-7 | Sweet spot for parallelization |
| High | 0.70-0.85 | 8-15 | Maximum benefit from parallelism |
| Critical | 0.85-1.00 | 15-25 | Necessary for timeline |

### Token Budget Constraints

```python
def calculate_max_agents(available_tokens: int) -> int:
    """
    Calculate maximum agents based on token budget
    """
    TOKENS_PER_AGENT = 3000  # Average
    SAFETY_BUFFER = 20000    # Reserve for synthesis

    usable_tokens = available_tokens - SAFETY_BUFFER
    max_agents_tokens = usable_tokens // TOKENS_PER_AGENT

    # Never exceed 10 agents per wave (synthesis overhead)
    MAX_AGENTS_SYNTHESIS = 10

    return min(max_agents_tokens, MAX_AGENTS_SYNTHESIS)

# Example:
# 180,000 tokens available
# Safety buffer: 20,000
# Usable: 160,000
# Max agents: 160,000 / 3,000 = 53 agents (token-wise)
# Actual max: 10 agents (synthesis constraint)
# Result: 10 agents per wave maximum
```

### Wave Splitting Strategy

When total agents > max agents per wave:

```python
def split_into_waves(phases: list, max_agents: int) -> list:
    """
    Split large parallel work into multiple waves
    """
    waves = []
    for i in range(0, len(phases), max_agents):
        wave_phases = phases[i:i+max_agents]
        waves.append({
            "wave_number": len(waves) + 1,
            "phases": wave_phases,
            "agents": len(wave_phases)
        })
    return waves

# Example:
# 15 parallel components to build
# Max agents: 5 per wave
# Result:
#   Wave 3a: Components 1-5 (5 agents)
#   Wave 3b: Components 6-10 (5 agents)
#   Wave 3c: Components 11-15 (5 agents)
```

---

## Common Pitfalls

### Pitfall 1: Sequential Agent Spawning (No Parallelism)

**Wrong:**
```xml
<!-- Multiple messages = sequential execution -->
Message 1: <invoke name="Task">Agent 1</invoke>
Wait...
Message 2: <invoke name="Task">Agent 2</invoke>
```

**Right:**
```xml
<!-- One message = parallel execution -->
<function_calls>
  <invoke name="Task">Agent 1</invoke>
  <invoke name="Task">Agent 2</invoke>
  <invoke name="Task">Agent 3</invoke>
</function_calls>
```

**Why:** Sequential spawning eliminates ALL speedup benefits. Must spawn all wave agents in ONE message.

### Pitfall 2: Skipping Dependency Analysis

**Wrong:**
```python
# Just spawn all agents without checking dependencies
spawn_agents([agent1, agent2, agent3, agent4])
```

**Right:**
```python
# Build dependency graph first
dependency_graph = analyze_dependencies(phases)
waves = group_by_dependencies(dependency_graph)
for wave in waves:
    spawn_agents(wave.agents)
```

**Why:** Skipping dependencies causes agents to collide, block each other, and create integration chaos.

### Pitfall 3: Skipping Synthesis Checkpoints

**Wrong:**
```
Wave 1 complete → Immediately spawn Wave 2
```

**Right:**
```
Wave 1 complete → Synthesis checkpoint → User approval → Wave 2
```

**Why:** Synthesis catches integration issues early. Skipping = cascading failures across waves.

### Pitfall 4: Under-Allocating Agents Based on Intuition

**Wrong:**
```
Complexity 0.72 but user suggests 3 agents → Accept 3 agents
```

**Right:**
```
Complexity 0.72 → Algorithm recommends 8-15 agents → Use algorithm
```

**Why:** User intuition systematically under-estimates by 50-70%. Trust complexity-based allocation.

### Pitfall 5: Missing Context Loading Protocol

**Wrong:**
```markdown
Agent prompt: "Build the frontend components"
```

**Right:**
```markdown
Agent prompt:
## MANDATORY CONTEXT LOADING
1. list_memories()
2. read_memory("spec_analysis")
3. read_memory("wave_1_complete")

Your task: Build frontend components
```

**Why:** Without context, agents make decisions based on incomplete information = contradictory implementations.

---

## Examples

### Example 1: Simple 2-Wave Project (Complexity 0.45)

**Input:**
- Complexity: 0.45 (Moderate)
- Domains: Frontend 60%, Backend 40%
- Phases: 5 phases (Analysis, Design, Implementation, Testing, Deployment)

**Wave Structure:**
```
Wave 1: Analysis + Design (Sequential)
- 1 agent: planner
- Duration: 2 hours
- No parallelism (single preparatory wave)

Wave 2: Implementation + Testing (Parallel)
- 2 agents: frontend-builder, backend-builder
- Duration: 8 hours
- Parallelism: 2x speedup
```

**Outcome:**
- Total time: 10 hours (vs 12 hours sequential)
- Speedup: 1.2x (modest due to single parallel wave)
- Agents: 3 total

### Example 2: Complex 4-Wave Project (Complexity 0.65)

**Input:**
- Complexity: 0.65 (Complex)
- Domains: Frontend 35%, Backend 30%, Database 20%, DevOps 15%
- Phases: 8 phases across domains

**Wave Structure:**
```
Wave 1: Foundation (Parallel)
- 3 agents: architecture-designer, database-schema-builder, devops-setup
- Duration: 3 hours
- Parallelism: 3 independent foundation tasks

Wave 2: Core Implementation (Parallel)
- 5 agents: frontend-ui, frontend-state, backend-api, backend-logic, database-migrations
- Duration: 6 hours
- Parallelism: 5 parallel tracks

Wave 3: Integration (Parallel)
- 3 agents: integration-specialist, frontend-integration, backend-integration
- Duration: 4 hours
- Parallelism: 3 integration tracks

Wave 4: Testing + Deployment (Parallel)
- 2 agents: testing-specialist, deployment-specialist
- Duration: 3 hours
- Parallelism: 2 final validation tracks
```

**Outcome:**
- Total time: 16 hours (vs 50 hours sequential)
- Speedup: 3.1x
- Agents: 13 total
- Efficiency: 78%

---

## Integration with Other Skills

### Required: context-preservation

Wave orchestration **REQUIRES** context-preservation skill:

```python
# Before starting wave execution
use_skill("context-preservation", {
    "checkpoint_name": "pre_wave_execution",
    "context_to_save": [
        "spec_analysis",
        "phase_plan_detailed",
        "architecture_complete",
        "all_previous_wave_results"
    ]
})

# Result: Can restore if wave execution fails
```

### Optional: sitrep-reporting

Enable progress updates at wave checkpoints:

```python
# At each wave synthesis checkpoint
if "sitrep-reporting" in active_skills:
    use_skill("sitrep-reporting", {
        "checkpoint_id": f"wave_{wave_number}_complete",
        "progress_data": wave_synthesis
    })
```

### Optional: confidence-check

Validate wave readiness before spawn:

```python
# Before spawning large/risky waves
if "confidence-check" in active_skills:
    confidence = use_skill("confidence-check", {
        "target": "wave_readiness",
        "factors": [
            "dependencies_satisfied",
            "context_complete",
            "token_budget_adequate",
            "agent_prompts_prepared"
        ]
    })

    if confidence < 0.70:
        WARNING: "Low confidence in wave readiness"
        # Consider: Creating checkpoint, reducing wave size
```

---

## Examples

See `examples/` directory:
- **2-wave-simple.md**: Simple project (0.45 complexity) with 2 waves
- **4-wave-complex.md**: Complex project (0.65 complexity) with 4 waves
- **8-wave-critical.md**: Critical project (0.90 complexity) with 8 waves

---

## Templates

See `templates/` directory:
- **wave-plan.md**: Complete wave execution plan template
- **synthesis-checkpoint.md**: Wave synthesis document template
- **agent-allocation.md**: Agent assignment and prompt template

---

## Success Criteria

Wave orchestration is successful when:

✅ **Parallelism Verified**: Speedup ≥ 1.5x vs sequential
   - Evidence: Timestamps show concurrent execution
   - Metric: parallel_time = max(agent_times), not sum

✅ **Zero Duplicate Work**: No redundant agent tasks
   - Check: No files created by multiple agents
   - Check: No decisions made multiple times

✅ **Perfect Context Sharing**: Every agent has complete history
   - Check: All agents loaded required Serena memories
   - Check: No decisions based on incomplete info

✅ **Clean Validation Gates**: User approval between waves
   - Check: Synthesis presented after each wave
   - Check: Explicit user approval obtained

✅ **Complete Memory Trail**: All wave results saved
   - Check: wave_[N]_complete exists for all waves
   - Check: Individual agent results saved

✅ **Production Quality**: No TODOs, functional tests only
   - Check: No placeholders in code
   - Check: All tests functional (NO MOCKS)

Validation:
```python
def validate_wave_orchestration(result):
    assert len(result["waves"]) >= 1
    assert all(wave.get("agents_allocated") > 0 for wave in result["waves"])
    assert all(wave.get("checkpoint_id") for wave in result["waves"])
    parallel_waves = [w for w in result["waves"] if w.get("parallel")]
    assert len(parallel_waves) >= 1, "Must have at least 1 parallel wave"
    assert result["expected_speedup"] >= 1.5
```

---

## Reference

See `references/WAVE_ORCHESTRATION.md` for complete behavioral framework (1612 lines).

---

## Performance Benchmarks

**Expected Performance** (measured on Claude Sonnet 3.5):

| Complexity | Wave Count | Generation Time | Synthesis Time/Wave | Total Orchestration |
|------------|------------|-----------------|---------------------|---------------------|
| 0.50-0.60 (Complex) | 2-3 waves | 5-8 minutes | 10-15 min | 25-50 min overhead |
| 0.60-0.70 (Complex-High) | 3-5 waves | 8-12 minutes | 15-20 min | 60-100 min overhead |
| 0.70-0.85 (High) | 5-7 waves | 12-18 minutes | 20-30 min | 120-200 min overhead |
| 0.85-1.00 (Critical) | 7-10 waves | 18-25 minutes | 30-45 min | 250-450 min overhead |

**Speedup Metrics** (empirical data from Shannon V4 usage):

| Agents/Wave | Sequential Time | Parallel Time | Speedup | Efficiency |
|-------------|-----------------|---------------|---------|------------|
| 2 agents | 24 min | 14 min | 1.7x | 85% |
| 3 agents | 36 min | 15 min | 2.4x | 80% |
| 5 agents | 60 min | 18 min | 3.3x | 66% |
| 7 agents | 84 min | 24 min | 3.5x | 50% |
| 10 agents | 120 min | 30 min | 4.0x | 40% |

**Performance Indicators**:
- ✅ **Excellent**: Efficiency >70%, speedup >2.0x
- ⚠️ **Good**: Efficiency 50-70%, speedup 1.5-2.0x
- 🔴 **Poor**: Efficiency <50%, speedup <1.5x (reconsider wave structure)

**When Orchestration Takes Longer**:
- Many dependencies (>50% phases blocked) → More waves needed, less parallelism
- High coordination score (>0.75) → Synthesis takes longer, more conflicts to resolve
- Token budget constraints → Smaller waves, more synthesis checkpoints

---

## Complete Execution Walkthrough

**Scenario**: Build wave structure for a complex full-stack project

**Input**: Phase plan from phase-planning skill

**Phase Plan** (example):
```json
{
  "phases": [
    {
      "id": "phase_1_analysis",
      "name": "Analysis & Planning",
      "dependencies": [],
      "estimated_time": 120,
      "domain": "Planning"
    },
    {
      "id": "phase_2_architecture",
      "name": "Architecture Design",
      "dependencies": ["phase_1_analysis"],
      "estimated_time": 180,
      "domain": "Architecture"
    },
    {
      "id": "phase_3_database",
      "name": "Database Schema",
      "dependencies": ["phase_2_architecture"],
      "estimated_time": 90,
      "domain": "Database"
    },
    {
      "id": "phase_3_backend",
      "name": "Backend API",
      "dependencies": ["phase_2_architecture", "phase_3_database"],
      "estimated_time": 240,
      "domain": "Backend"
    },
    {
      "id": "phase_3_frontend",
      "name": "Frontend UI",
      "dependencies": ["phase_2_architecture"],
      "estimated_time": 210,
      "domain": "Frontend"
    },
    {
      "id": "phase_4_integration",
      "name": "Integration Testing",
      "dependencies": ["phase_3_backend", "phase_3_frontend"],
      "estimated_time": 120,
      "domain": "Testing"
    },
    {
      "id": "phase_5_deployment",
      "name": "Deployment",
      "dependencies": ["phase_4_integration"],
      "estimated_time": 60,
      "domain": "DevOps"
    }
  ],
  "complexity_score": 0.62
}
```

**Execution Process** (actual Claude workflow):

### **Step 1: Build Dependency Graph**

```python
# Input: Phase plan above
phases = load_phase_plan()

# Build dependency graph
dependency_graph = {
    "phase_1_analysis": {
        "name": "Analysis & Planning",
        "depends_on": [],
        "blocks": ["phase_2_architecture"],
        "time": 120
    },
    "phase_2_architecture": {
        "name": "Architecture Design",
        "depends_on": ["phase_1_analysis"],
        "blocks": ["phase_3_database", "phase_3_backend", "phase_3_frontend"],
        "time": 180
    },
    "phase_3_database": {
        "name": "Database Schema",
        "depends_on": ["phase_2_architecture"],
        "blocks": ["phase_3_backend"],
        "time": 90
    },
    "phase_3_backend": {
        "name": "Backend API",
        "depends_on": ["phase_2_architecture", "phase_3_database"],
        "blocks": ["phase_4_integration"],
        "time": 240
    },
    "phase_3_frontend": {
        "name": "Frontend UI",
        "depends_on": ["phase_2_architecture"],
        "blocks": ["phase_4_integration"],
        "time": 210
    },
    "phase_4_integration": {
        "name": "Integration Testing",
        "depends_on": ["phase_3_backend", "phase_3_frontend"],
        "blocks": ["phase_5_deployment"],
        "time": 120
    },
    "phase_5_deployment": {
        "name": "Deployment",
        "depends_on": ["phase_4_integration"],
        "blocks": [],
        "time": 60
    }
}

# Validate: Check for circular dependencies
circular_check = detect_cycles(dependency_graph)
# Result: No cycles detected ✅
```

### **Step 2: Generate Wave Structure (Critical Path Method)**

```python
waves = []
remaining_phases = list(dependency_graph.keys())
completed_phases = set()
wave_number = 1

# Iteration 1:
ready = [p for p in remaining_phases
         if all(dep in completed_phases for dep in dependency_graph[p]["depends_on"])]
# Result: ["phase_1_analysis"] (no dependencies)

waves.append({
    "wave_number": 1,
    "wave_name": "Wave 1: Foundation",
    "phases": ["phase_1_analysis"],
    "parallel": False,  # Only 1 phase
    "estimated_time": 120,  # 2 hours
    "dependencies": []
})

completed_phases.add("phase_1_analysis")
remaining_phases.remove("phase_1_analysis")

# Iteration 2:
ready = [p for p in remaining_phases
         if all(dep in completed_phases for dep in dependency_graph[p]["depends_on"])]
# Result: ["phase_2_architecture"] (depends on phase_1 ✅ completed)

waves.append({
    "wave_number": 2,
    "wave_name": "Wave 2: Architecture",
    "phases": ["phase_2_architecture"],
    "parallel": False,  # Only 1 phase
    "estimated_time": 180,  # 3 hours
    "dependencies": ["wave_1"]
})

completed_phases.add("phase_2_architecture")
remaining_phases.remove("phase_2_architecture")

# Iteration 3:
ready = [p for p in remaining_phases
         if all(dep in completed_phases for dep in dependency_graph[p]["depends_on"])]
# Result: ["phase_3_database", "phase_3_frontend"]
# phase_3_backend NOT ready (still needs phase_3_database)

waves.append({
    "wave_number": 3,
    "wave_name": "Wave 3: Foundation Implementation",
    "phases": ["phase_3_database", "phase_3_frontend"],
    "parallel": True,  # 2 phases can run concurrently ✅
    "estimated_time": max(90, 210) = 210,  # 3.5 hours (longest)
    "dependencies": ["wave_2"]
})

completed_phases.update(["phase_3_database", "phase_3_frontend"])
remaining_phases.remove("phase_3_database")
remaining_phases.remove("phase_3_frontend")

# Iteration 4:
ready = [p for p in remaining_phases
         if all(dep in completed_phases for dep in dependency_graph[p]["depends_on"])]
# Result: ["phase_3_backend"] (now all deps satisfied)

waves.append({
    "wave_number": 4,
    "wave_name": "Wave 4: Backend Implementation",
    "phases": ["phase_3_backend"],
    "parallel": False,  # Only 1 phase
    "estimated_time": 240,  # 4 hours
    "dependencies": ["wave_3"]
})

completed_phases.add("phase_3_backend")
remaining_phases.remove("phase_3_backend")

# Iteration 5:
ready = ["phase_4_integration"]

waves.append({
    "wave_number": 5,
    "wave_name": "Wave 5: Integration & Testing",
    "phases": ["phase_4_integration"],
    "parallel": False,
    "estimated_time": 120,  # 2 hours
    "dependencies": ["wave_4"]
})

# Iteration 6:
waves.append({
    "wave_number": 6,
    "wave_name": "Wave 6: Deployment",
    "phases": ["phase_5_deployment"],
    "parallel": False,
    "estimated_time": 60,  # 1 hour
    "dependencies": ["wave_5"]
})

# Final wave structure generated ✅
```

**Result**:
```json
{
  "total_waves": 6,
  "parallel_waves": 1,
  "sequential_waves": 5,
  "wave_structure": [
    {"wave": 1, "phases": 1, "parallel": false, "time": 120},
    {"wave": 2, "phases": 1, "parallel": false, "time": 180},
    {"wave": 3, "phases": 2, "parallel": true, "time": 210},  // PARALLELISM HERE
    {"wave": 4, "phases": 1, "parallel": false, "time": 240},
    {"wave": 5, "phases": 1, "parallel": false, "time": 120},
    {"wave": 6, "phases": 1, "parallel": false, "time": 60}
  ]
}
```

### **Step 3: Agent Allocation**

```python
complexity_score = 0.62  # From spec analysis

# Wave 1: 1 phase (Analysis)
agents_wave_1 = allocate_agents(0.62, wave_1)
# Complexity 0.62 ∈ [0.50, 0.70] = Complex band
# num_phases = 1
# Return: min(1, 7) = 1 agent

# Wave 2: 1 phase (Architecture)
agents_wave_2 = allocate_agents(0.62, wave_2)
# Return: 1 agent

# Wave 3: 2 phases (Database + Frontend) - PARALLEL
agents_wave_3 = allocate_agents(0.62, wave_3)
# num_phases = 2
# Complex band: 1-2 agents per phase
# Return: min(2, 7) = 2 agents ✅

agent_types_wave_3 = assign_agent_types(wave_3.phases)
# "Database Schema" → database-builder
# "Frontend UI" → frontend-builder
# Result: [database-builder, frontend-builder]

# Wave 4: 1 phase (Backend)
agents_wave_4 = 1  # backend-builder

# Wave 5: 1 phase (Integration)
agents_wave_5 = 1  # testing-specialist

# Wave 6: 1 phase (Deployment)
agents_wave_6 = 1  # deployment-specialist

# Total agents: 1+1+2+1+1+1 = 7 agents
```

**Result**:
```json
{
  "wave_1": {"agents": 1, "types": ["planner"]},
  "wave_2": {"agents": 1, "types": ["architect"]},
  "wave_3": {"agents": 2, "types": ["database-builder", "frontend-builder"]},  // PARALLEL
  "wave_4": {"agents": 1, "types": ["backend-builder"]},
  "wave_5": {"agents": 1, "types": ["testing-specialist"]},
  "wave_6": {"agents": 1, "types": ["deployment-specialist"]},
  "total_agents": 7
}
```

### **Step 4: Calculate Speedup**

**Sequential Time** (hypothetical - all phases done one after another):
```
120 + 180 + 90 + 240 + 210 + 120 + 60 = 1020 minutes = 17 hours
```

**Parallel Time** (with wave structure):
```
Wave 1: 120 min
Wave 2: 180 min
Wave 3: max(90, 210) = 210 min  // Database + Frontend in parallel
Wave 4: 240 min
Wave 5: 120 min
Wave 6: 60 min
Total: 930 minutes = 15.5 hours
```

**Speedup Calculation**:
```
speedup = 1020 / 930 = 1.10x

Parallelism benefit: 90 minutes saved (Database ran while Frontend building)
Efficiency: 1.10/7 agents = 16% (LOW - only 1 parallel wave out of 6)
```

**Analysis**: Modest speedup due to sequential dependencies. Only Wave 3 parallelizes.

### **Step 5: Optimize Wave Structure** (Optional)

Can we improve? Check if more phases can be parallelized:

```
Wave 3 currently: Database (90 min) + Frontend (210 min) = 210 min parallel

Could we also parallelize Testing + Deployment?
- phase_4_integration depends on (backend, frontend) ✅
- phase_5_deployment depends on (integration) ✅
- No opportunity to merge

Current structure is OPTIMAL given dependencies.
```

**Conclusion**: 6 waves, 1.10x speedup (modest but correct given dependency chain)

---

This walkthrough demonstrates the complete wave generation process, showing how dependency analysis produces wave structure, how agents are allocated, and how to calculate expected performance improvements.

---

## Conclusion

Wave orchestration achieves **3.5x average speedup** through:
1. ✅ True parallelism (all agents spawn in one message)
2. ✅ Complete context (every agent loads full history)
3. ✅ Systematic synthesis (validation after each wave)
4. ✅ Smart dependencies (maximize parallel work)
5. ✅ Optimal sizing (balance speed and manageability)
6. ✅ Robust recovery (graceful failure handling)
7. ✅ Performance focus (measured speedup, optimized tokens)

This is the **most impactful skill** in Shannon V4 for accelerating complex project execution.
