---
license: BSL-1.1
name: windags-architect
description: Build WinDAGs — the orchestration platform where AI agents accumulate genuine expertise through DAGs of skillful agents. Covers DAG design, execution engines, meta-DAG architecture, skill selection, dynamic mutation, visualization, and deployment. Activate on "windags", "agent DAG", "DAG of agents", "workflow orchestration", "agent pipeline", "dynamic DAG", "meta-DAG", "build windags", "implement windags". NOT for understanding WHY decisions were made (use windags-avatar), creating individual skills (use skill-architect), or managing skill libraries (use windags-librarian).
allowed-tools: Read,Write,Edit,Bash,Grep,Glob
argument-hint: '[problem-description] [mode: local|web|embedded]'
metadata:
  tags:
    - windags
    - architect
    - agent-dag
    - dag-of-agents
category: Agent & Orchestration
tags:
  - windags
  - architecture
  - system-design
  - platform
  - meta
---

# WinDAGs Architect — V3

Build WinDAGs: directed acyclic graphs of skillful agents that accumulate genuine expertise. Each node is an agent with curated skills; each edge is a typed dependency. The system builds DAGs, executes them in waves, mutates them at runtime, evaluates quality across four layers, and crystallizes reusable skills from execution data.

## DECISION POINTS

### 1. Execution Mode Selection

```
Problem type assessment:
├── Simple task (< 5 nodes, single domain)
│   ├── If user has CLI access → Use local mode
│   └── If web interface needed → Use embedded mode
├── Medium task (5-20 nodes, 2-3 domains)
│   ├── If team collaboration needed → Use web mode
│   ├── If execution history important → Use web mode
│   └── If isolated/private → Use local mode
└── Complex task (20+ nodes, multiple domains)
    ├── If distributed execution needed → Use web mode
    ├── If real-time monitoring required → Use web mode
    └── If cost optimization critical → Use web mode with smart routing
```

### 2. DAG Architecture Pattern Selection

```
Problem complexity:
├── Sequential chain (A→B→C)
│   ├── If error-prone steps → Add approval gates between nodes
│   └── If simple pipeline → Use basic data-flow edges
├── Fan-out pattern (A→[B,C,D]→E)
│   ├── If independent work streams → Use parallel execution
│   ├── If failure domains overlap → Isolate to separate waves
│   └── If results must merge → Add aggregator node
├── Iterative refinement (A→B→C→B)
│   ├── If quality improvement loop → Use loop_back mutation
│   ├── If human oversight needed → Add approval gates
│   └── If automatic iteration → Use quality threshold triggers
└── Multi-stage validation (parallel checks)
    ├── If binary validation → Use Floor/Wall evaluation only
    ├── If process quality matters → Enable Ceiling evaluation
    └── If stress testing needed → Monitor Envelope metrics
```

### 3. Node Commitment Level Assignment

```
Task certainty assessment:
├── COMMITTED (implementation clear)
│   ├── If skill signature known → Direct skill assignment
│   ├── If template available → Use template with parameters
│   └── If standard pattern → Apply seed template
├── TENTATIVE (approach unclear)
│   ├── If 2-3 viable approaches → Create parallel exploration nodes
│   ├── If dependency on prior results → Mark as vague node
│   └── If expert consultation needed → Add human approval gate
└── EXPLORATORY (research needed)
    ├── If domain expertise required → Use research-synthesis template
    ├── If multiple unknowns → Break into sub-DAG
    └── If high uncertainty → Add PreMortem analysis
```

### 4. Circuit Breaker Configuration

```
Risk assessment:
├── Node-level breakers
│   ├── If node failure rate > 20% → Set 3-attempt limit with escalation
│   ├── If expensive model calls → Set cost threshold per node
│   └── If time-sensitive → Set timeout with fallback skill
├── Skill-level breakers
│   ├── If skill success rate < 60% → Disable for 1 hour, use backup
│   ├── If skill shows degrading performance → Trigger Thompson sampling reset
│   └── If skill causes cascade failures → Add to temporary blacklist
└── Model-level breakers
    ├── If API rate limits hit → Route to secondary provider
    ├── If model availability < 90% → Use tier fallback (Sonnet→Haiku)
    └── If cost drift > 30% of budget → Switch to cheaper model tier
```

### 5. Mutation Trigger Conditions

```
Execution state analysis:
├── Quality below threshold (< 0.6 floor score)
│   ├── If single node failure → Try replace_node with different skill
│   ├── If edge protocol mismatch → Try add_edge for missing dependency
│   └── If topology issue → Try split_parallel for ambiguous task
├── Resource constraints hit
│   ├── If cost exceeds budget → Try remove_node for redundant tasks
│   ├── If time exceeds deadline → Try split_parallel for faster execution
│   └── If model availability issues → Try replace_node with different model tier
└── Escalation ladder exhausted
    ├── If 3+ mutation attempts failed → escalate_human with full context
    ├── If critical path blocked → escalate_human with options
    └── If novel failure pattern → escalate_human for learning
```

## FAILURE MODES

### 1. Shared Failure Domain Coupling
**Detection**: Multiple nodes fail simultaneously with correlated error patterns
**Symptoms**: Wave fails entirely when one node fails; cascade failure rate > 15%
**Fix**: Implement failure domain isolation (BC-PLAN-003). Separate nodes using same provider/model/skill into different waves. Add circuit breakers at provider level.

### 2. Over-Vague Node Paralysis
**Detection**: >30% of nodes remain vague after 2 wave completions; planning time exceeds execution time
**Symptoms**: "Analysis paralysis" in Wave 1; Decomposer creates vague nodes instead of commitments
**Fix**: Force commitment threshold: If Pass 1 recognition < 0.6, escalate to human. Use domain meta-skills to add structure. Apply seed templates for common patterns.

### 3. Thompson Sampling Cold Start Bias
**Detection**: New skills selected despite poor performance; selection algorithm ignores obvious quality signals
**Symptoms**: Repeatedly selecting untested skills over proven ones; ignoring Haiku ranking confidence
**Fix**: Implement warm-start Beta priors from skill signature similarity. Trust Haiku ranking at cold start (Alpha=5, Beta=1). Only apply Thompson perturbation after 10+ executions.

### 4. Meta-DAG Recursion Loops
**Detection**: Mutator creates mutations that trigger more mutations; execution never stabilizes
**Symptoms**: >5 mutation cycles in single DAG; Mutator modifies its own topology
**Fix**: Implement mutation depth limits (max 3 per DAG). Prevent meta-agent self-modification. Add "mutation storm" detection with automatic escalation.

### 5. Quality Evaluation Overhead Spiral
**Detection**: Stage 2 (Ceiling) evaluation costs exceed node execution costs; evaluation time > 40% of total runtime
**Symptoms**: Expensive quality checks on trivial nodes; Ceiling evaluation triggered inappropriately
**Fix**: Tune conditional trigger: `failureProbability × downstreamWaste > reviewCost`. Skip Ceiling for nodes with < $0.01 downstream impact. Use Haiku for Ceiling evaluation on low-stakes nodes.

### 6. Skill Selection Cascade Shortcuts
**Detection**: Embedding narrowing bypassed; Thompson sampling applied to full 191-skill library
**Symptoms**: Selection time > 2 seconds per node; poor skill matches despite good library coverage
**Fix**: Enforce 3-step cascade: embeddings → Haiku → Thompson. Never skip Step 1 unless library < 15 skills. Log cascade timing and enforce budget limits per step.

### 7. Wave Planning Dependency Violations
**Detection**: Nodes in Wave N depend on incomplete nodes from Wave N+1; topological sort failures
**Symptoms**: Deadlock during wave execution; "circular dependency" errors in scheduler
**Fix**: Validate wave assignments with strict topological ordering. Prevent vague nodes from creating forward dependencies. Use Kahn's algorithm validation before wave execution starts.

## WORKED EXAMPLES

### Example 1: Simple Code Review DAG

**Problem**: "Review this pull request for security issues and code quality"

**Decision Process**:
1. **Mode selection**: Local (private code) → Use local execution mode
2. **Architecture**: Sequential with validation → A→B→C pattern with approval gate
3. **Commitment levels**: All COMMITTED (standard templates available)

**DAG Construction**:
```typescript
const dag = builder('code-review-pr')
  .skillNode('security-scan', 'security-auditor')  // Wave 0
  .skillNode('quality-check', 'code-reviewer')     // Wave 1
    .dependsOn('security-scan')
  .skillNode('summary', 'review-synthesizer')      // Wave 2
    .dependsOn('quality-check')
  .approvalGate('human-review', {                  // Wave 3
    prompt: 'Approve changes?',
    options: [
      { id: 'approve', label: 'LGTM', action: 'approve' },
      { id: 'revise', label: 'Needs work', action: 'revise', branchTo: 'quality-check' }
    ]
  }).dependsOn('summary')
```

**Execution Flow**:
- Wave 0: security-auditor scans code (Floor: pass, Wall: pass) → 3 vulnerabilities found
- Wave 1: code-reviewer analyzes quality (Floor: pass, Wall: pass) → 2 style issues found
- Wave 2: review-synthesizer creates summary (Floor: pass, Ceiling triggered due to human dependency)
- Wave 3: Human approves with minor revisions → triggers loop_back to quality-check

**Expert vs Novice**: Expert catches that security scan should use Sonnet (complex reasoning), while quality-check can use Haiku (pattern matching). Novice uses same model for all nodes.

### Example 2: Vague Node Resolution with Trade-offs

**Problem**: "Design and implement a caching layer for our API"

**Decision Process**:
1. **Mode selection**: Medium complexity + team collaboration → Use web mode
2. **Architecture**: Fan-out with convergence → Research→[Design,Impl]→Integration
3. **Commitment levels**: Mixed (COMMITTED research, TENTATIVE design choices)

**Initial DAG** (with vague nodes):
```typescript
const dag = builder('api-caching-layer')
  .skillNode('requirements', 'system-analyst')                    // Wave 0 - COMMITTED
  .vagueNode('cache-strategy', {                                  // Wave 1 - TENTATIVE
    role_description: 'Choose caching strategy (Redis/Memcached/in-memory)',
    dependency_list: ['requirements']
  })
  .vagueNode('implementation', {                                  // Wave 2 - EXPLORATORY
    role_description: 'Implement chosen caching solution',
    dependency_list: ['cache-strategy']
  })
  .skillNode('integration', 'integration-tester')                 // Wave 3 - COMMITTED
    .dependsOn('implementation')
```

**Wave-by-Wave Resolution**:

**Wave 0**: system-analyst produces requirements (recognition = 0.95 → plan Wave 1 immediately)

**Wave 1**: cache-strategy node needs resolution
- Domain recognition: "distributed systems" → use `distributed-systems-architect` skill
- Trade-off analysis reveals 3 options: Redis (high performance), Memcached (simple), in-memory (low latency)
- Decision: Redis for distributed setup
- Node becomes COMMITTED with skill assignment

**Wave 2**: implementation node needs resolution  
- Previous results show Redis choice → use `redis-implementation` skill
- Parallel approach detected → split into [config-setup, client-integration]
- Apply split_parallel mutation to create 2 nodes

**Expert vs Novice**: Expert recognizes that cache-strategy requires trade-off analysis and uses expensive model (Sonnet) for decision quality. Novice assigns cheap model and gets poor architectural decisions. Expert also anticipates implementation complexity and pre-plans for split_parallel mutation.

### Example 3: Mutation Trigger with Circuit Breaker

**Problem**: "Analyze customer churn data and recommend retention strategies"

**Scenario**: Mid-execution, data-analyzer node fails repeatedly due to malformed data

**Initial Failure**:
- Node: data-analyzer (skill: statistical-analyzer, model: Sonnet)
- Error: "Cannot parse CSV format" (3 attempts, all Floor failures)
- Circuit breaker: Node-level breaker trips after 3 attempts

**Mutation Decision Tree**:
```
Failure analysis:
├── Error type: Data format issue (not reasoning failure)
│   ├── Try replace_node with data-preprocessing skill
│   └── If still fails → Try add_node for format conversion
├── Check dependencies: Previous node output format unknown
│   ├── Try add_edge for explicit format specification
│   └── If format mismatch → Try split_parallel for multiple parsers
└── Resource check: Still within budget and time limits
    └── Apply mutation, don't escalate yet
```

**Mutation Applied**: replace_node
- Old: data-analyzer using statistical-analyzer
- New: data-analyzer using data-preprocessing-pipeline  
- Result: Floor pass (data parsed), Wall pass (format correct)
- Continue with original DAG topology

**Quality Check**: Stage 2 evaluation triggered (high downstream impact)
- Ceiling evaluation: Good (proper statistical methods applied)
- Envelope stress: Normal (no resource strain)
- Continue to next wave

**Expert vs Novice**: Expert recognizes data format issues early and chooses data-preprocessing skill. Expert also sets appropriate circuit breaker thresholds (3 attempts for data issues, 1 attempt for API issues). Novice doesn't differentiate error types and applies wrong mutation.

## QUALITY GATES

- [ ] DAG has valid topological ordering (no cycles detected)
- [ ] All nodes have skill assignments or vague node specifications
- [ ] Wave assignments respect failure domain isolation (no shared providers in same batch)
- [ ] Circuit breakers configured for all expensive operations (>$0.05 per call)
- [ ] Stage 1 evaluation (Floor+Wall) enabled for all nodes
- [ ] Stage 2 evaluation (Ceiling) conditional trigger properly configured
- [ ] Mutation depth limits set (max 3 mutations per DAG execution)
- [ ] Human escalation triggers defined for ladder exhaustion
- [ ] Cost budgets and time limits configured per execution mode
- [ ] Meta-DAG agents properly isolated (no self-modification paths)

## NOT-FOR BOUNDARIES

**Do NOT use windags-architect for**:

- **Understanding constitutional decisions** → Use `windags-avatar` for ADR provenance, tradition attribution, and constitutional details
- **Creating individual skills** → Use `skill-architect` for YAML skill creation, L3 procedural content, and skill validation
- **Managing skill libraries** → Use `windags-librarian` for skill discovery, curation, and library organization
- **Rendering static diagrams** → Use `mermaid-graph-renderer` for flowcharts and visual documentation
- **Debugging specific skill failures** → Use `cognitive-debugger` for task analysis and error diagnosis
- **Cost optimization alone** → Use `llm-cost-optimizer` for model selection and provider routing
- **Real-time monitoring** → Use `windags-observer` for execution monitoring and alerting

**Delegate instead when**:
- User asks "why was this decision made?" → `windags-avatar`
- User wants to create a new skill → `skill-architect`  
- User needs skill recommendations → `windags-librarian`
- User wants execution insights → `windags-observer`