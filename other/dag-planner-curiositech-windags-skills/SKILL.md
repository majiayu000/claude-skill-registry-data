---
license: BSL-1.1
name: dag-planner
description: Builds, validates, schedules, and dynamically modifies DAG execution graphs. Decomposes problems into nodes with dependencies, performs topological sorting, detects cycles, resolves conflicts, and schedules wave-based parallel execution. Use when designing a DAG structure, validating dependencies, planning execution order, or modifying a DAG at runtime. Activate on "build DAG", "plan workflow", "DAG dependencies", "topological sort", "schedule execution", "modify DAG", "replan". NOT for executing DAGs (use dag-runtime), validating outputs (use dag-quality), or matching skills to nodes (use dag-skills-matcher).
allowed-tools: Read,Write,Edit,Grep,Glob
metadata:
  category: DAG Framework
  tags:
    - dag
    - planner
    - build-dag
    - plan-workflow
    - dag-dependencies
category: Agent & Orchestration
tags:
  - dag
  - planning
  - decomposition
  - strategy
  - orchestration
---

# DAG Planner

Builds, validates, schedules, and dynamically modifies DAG execution graphs for complex multi-step tasks.

## Decision Points

### 1. When to decompose a task into DAG nodes
```
Problem complexity assessment:
├── Single coherent output from one skill → No DAG needed (use direct skill)
├── 2-3 sequential steps, linear dependency → Simple pipeline (3-5 nodes)
├── Multiple parallel paths with convergence → Complex DAG (5-15 nodes)
└── Unclear requirements or multiple approaches → Start with vague nodes, refine later
```

### 2. Choosing node types by certainty level
```
Node type decision tree:
├── If task is well-defined with known skills → agent node
├── If task is unclear but bounded → vague node (refine during execution)  
├── If requires human judgment/approval → human-gate node
└── If task needs external system → agent node with tool restrictions
```

### 3. Determining granularity (critical decision)
```
Node size assessment:
├── If completable in 1 LLM call with 1-3 skills → Good granularity
├── If requires 5+ sequential LLM calls → Split into multiple nodes
├── If output is 1-2 simple values → Too granular, merge with parent
└── If node does "everything" → Too coarse, decompose further
```

### 4. Handling conflicts and dependencies
```
Dependency resolution:
├── Data dependency (B needs A's output) → Direct edge A→B
├── Resource conflict (both modify same file) → Serialize into different waves
├── Ordering constraint (B after A for logic) → Add ordering edge A→B
└── Optional dependency (B benefits from A but can run without) → Parallel with optional input
```

### 5. Dynamic modification triggers
```
Modification decision tree:
├── If node repeatedly fails → Replace node (different skill/model/approach)
├── If output quality insufficient → Add quality gate node after current
├── If gap discovered in coverage → Insert new node in dependency chain  
├── If path proves unnecessary → Remove node and reconnect edges
└── If multiple approaches needed → Fork into parallel paths, converge later
```

## Failure Modes

### Schema Drift
**Symptoms**: Downstream nodes fail with "missing field" or "unexpected format" errors
**Detection**: If >50% of nodes in a wave fail with schema violations
**Diagnosis**: Node output schemas don't match downstream input expectations
**Fix**: Halt execution, audit all schemas in the dependency chain, add adapter nodes if needed

### Circular Dependency Trap
**Symptoms**: Topological sort fails, no nodes have in_degree=0 after some are processed
**Detection**: Validation throws CycleError during DAG build phase
**Diagnosis**: Implicit dependency created a cycle (often through shared resources)
**Fix**: Trace cycle using Kahn's algorithm state, break weakest dependency (usually resource conflicts)

### Granularity Explosion  
**Symptoms**: DAG has >20 nodes for simple task, execution overhead dominates work time
**Detection**: If node_count > 3 × estimated_complexity_score
**Diagnosis**: Over-decomposed trivial operations into separate nodes
**Fix**: Merge adjacent nodes with single dependencies, combine related operations

### Ghost Dependencies
**Symptoms**: Nodes wait indefinitely, execution stalls despite no explicit blocking
**Detection**: If wave scheduling shows nodes stuck in higher waves despite dependencies met
**Diagnosis**: Hidden dependencies through shared mutable state not modeled as edges
**Fix**: Audit all file I/O and shared resources, add explicit edges or resource locks

### Wave Starvation
**Symptoms**: Later waves have 1-2 nodes while early waves are overloaded
**Detection**: If max_wave_size / min_wave_size > 5 and total_waves > 3
**Diagnosis**: Poor dependency structure creates artificial serialization
**Fix**: Identify independent sub-paths, restructure to enable more parallelization

## Worked Examples

### Example 1: Simple Analysis Task
**Problem**: "Analyze customer feedback and generate recommendations"

**Decomposition Process**:
1. **Assess complexity**: Multiple data sources + analysis + synthesis → Medium complexity DAG
2. **Initial nodes**: 
   - collect_feedback (agent: data-collector)
   - analyze_sentiment (agent: text-analyzer) 
   - generate_recommendations (agent: strategic-advisor)
3. **Dependencies**: collect → analyze → recommendations (linear)
4. **Validation**: No cycles, 3 waves
5. **Expert insight**: Novice would create single "analyze_everything" node; expert separates concerns

**Final DAG**:
```yaml
nodes:
  - id: collect_feedback
    type: agent
    skills: [data-collector]
    output_schema: {feedback_items: array, metadata: object}
    wave: 1
  
  - id: analyze_sentiment  
    type: agent
    skills: [text-analyzer]
    depends_on: [collect_feedback]
    output_schema: {sentiment_scores: array, themes: array}
    wave: 2
    
  - id: generate_recommendations
    type: agent  
    skills: [strategic-advisor]
    depends_on: [analyze_sentiment]
    wave: 3
```

### Example 2: Complex Research Task
**Problem**: "Research market trends, analyze competitors, and create strategy presentation"

**Key Decisions**:
- **Parallelization opportunity**: Market research and competitor analysis are independent → parallel waves
- **Human gate needed**: Strategy requires business judgment → human-gate node
- **Resource conflict**: Both research tasks write to shared analysis.md → serialize or separate files

**Decomposition reasoning**:
1. Identify independent paths: market_research ∥ competitor_analysis
2. Both feed into strategy_synthesis
3. Human validation before final presentation
4. Expert catches: Presentation creation can start before human approval if we assume approval

**Final structure**: 4 waves, 2 parallel paths converging, 1 human gate

### Example 3: Dynamic Replanning Scenario  
**Initial plan**: Simple linear DAG for code review
**Runtime issue**: Code quality gate fails repeatedly
**Replanning decision**:
1. **Diagnose**: Quality threshold not met after 3 attempts
2. **Fork approach**: Add parallel path with different code analysis method
3. **Convergence**: Both paths feed into synthesis node that picks best result
4. **New structure**: Original linear becomes forked DAG with quality comparison

**Expert insight**: Novice would just retry same approach; expert recognizes need for alternative path

## Quality Gates

- [ ] Every node has explicit input_schema and output_schema defined
- [ ] All dependencies are explicitly modeled as edges (no hidden shared state)  
- [ ] DAG passes cycle detection (topological sort completes successfully)
- [ ] No node requires >3 skills or >5 minute estimated runtime
- [ ] Wave distribution is reasonable (no wave has >3x nodes of smallest wave)
- [ ] Resource conflicts are identified and resolved (files, APIs, external systems)
- [ ] All vague nodes have refinement criteria specified
- [ ] Human-gate nodes have clear approval criteria and timeout policies
- [ ] Estimated total runtime is <10x single-agent equivalent approach
- [ ] Each node's purpose can be explained in one sentence

## NOT-FOR Boundaries

**Do NOT use dag-planner for**:
- **Single-step tasks**: If only one skill needed → use skill directly
- **Pure sequential pipelines**: If no parallelization possible → use simple workflow  
- **Real-time execution**: For running the DAG → use `dag-runtime` instead
- **Output validation**: For checking node results → use `dag-quality` instead  
- **Skill selection**: For picking skills for nodes → use `dag-skills-matcher` instead
- **Data transformation**: For ETL-style operations → use data pipeline tools
- **User interface flows**: For UI workflows → use frontend orchestration tools

**Delegate to**:
- `dag-runtime`: For executing planned DAGs
- `dag-quality`: For validating node outputs  
- `dag-skills-matcher`: For selecting appropriate skills for each node
- `workflow-simple`: For linear 2-3 step processes
- Direct skill calls: For single-step tasks