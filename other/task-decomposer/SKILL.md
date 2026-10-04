---
name: task-decomposer
license: Apache-2.0
description: Breaks natural-language problem descriptions into sub-tasks suitable for DAG nodes. The entry point of the meta-DAG. Identifies phases, dependencies, parallelization opportunities, and vague/pluripotent nodes that can't yet be specified. Uses domain meta-skills when available. Activate on "decompose task", "break down problem", "plan workflow", "what are the steps", "sub-tasks", "task breakdown". NOT for executing the decomposed tasks (use dag-runtime), building the DAG structure (use dag-planner), or matching skills to nodes (use dag-skills-matcher).
allowed-tools: Read,Grep,Glob
argument-hint: '[problem-description]'
metadata:
  tags:
    - task
    - decomposer
    - decompose-task
    - break-down-problem
    - plan-workflow
  pairs-with:
    - skill: output-contract-enforcer
      reason: Decomposed tasks define output schemas that the enforcer validates between nodes
    - skill: skillful-subagent-creator
      reason: Decomposed tasks map to subagent specializations with curated skill sets
    - skill: human-gate-designer
      reason: Task decomposition identifies which stages need human review gates
category: Agent & Orchestration
tags:
  - task-decomposition
  - planning
  - subtasks
  - agents
  - orchestration
---

# Task Decomposer

Breaks natural-language problems into sub-tasks suitable for DAG nodes. The first step of the meta-DAG: before you can build or execute a DAG, you need to understand what the pieces are.

## Decision Points

```
1. DOMAIN CLASSIFICATION
   ├─ Contains {"build", "implement", "code", "app"} → Use software-project-decomposition
   ├─ Contains {"research", "analyze", "report"} → Use research-synthesis-decomposition
   ├─ Contains {"design", "UI", "prototype"} → Use product-design-decomposition
   ├─ Contains {"data", "model", "train", "ML"} → Use ml-project-decomposition
   └─ No clear domain signals → Zero-shot decomposition

2. SUB-TASK GRANULARITY
   ├─ Can one agent complete in one call? → Correct granularity
   ├─ Requires multiple agent calls/skills? → Split into smaller sub-tasks
   └─ Too trivial (open file, read line)? → Merge with adjacent sub-task

3. DEPENDENCY DETECTION
   ├─ B needs A's output data? → Create data dependency A→B
   ├─ B needs A's knowledge/decisions? → Create knowledge dependency A→B
   ├─ A and B share no inputs/outputs? → Mark as parallelizable
   └─ Circular reference detected? → Invalid, restructure phases

4. VAGUENESS CLASSIFICATION
   ├─ Can specify concrete steps now? → Create concrete sub-task
   ├─ Depends on upstream discoveries? → Create vague node with 3+ potential paths
   └─ Requires human decision? → Mark as human-gate candidate

5. COMPLEXITY ESTIMATION
   ├─ Single skill, clear inputs/outputs? → Mark as "simple" (Tier 1 model)
   ├─ 2-3 skills, moderate reasoning? → Mark as "moderate" (Tier 2 model)
   └─ Complex reasoning, multiple domains? → Mark as "complex" (Tier 3 model)
```

## Failure Modes

| Anti-Pattern | Symptom | Diagnosis | Fix |
|-------------|---------|-----------|-----|
| **Sequential Fallacy** | All tasks form single chain, no parallelism | Missed independent work streams | Identify tasks with no shared inputs/outputs, mark parallelizable |
| **Premature Specification** | Concrete details for tasks depending on undone research | Forcing certainty where none exists | Convert to vague nodes with potential paths |
| **Granularity Mismatch** | Sub-tasks either trivial (1-line) or massive (whole project) | Wrong decomposition level | Apply one-agent-one-call rule for sizing |
| **Circular Dependencies** | Task A needs B's output, B needs A's output | Invalid dependency graph | Restructure into sequential phases or split conflated tasks |
| **Domain Blindness** | Generic decomposition for specialized domain (e.g., treating ML project like web app) | Missed domain-specific phase patterns | Re-classify domain, apply appropriate meta-skill |

## Worked Examples

### Example 1: Software Project - "Build a URL shortener API"

**Step 1: Domain Classification**
- Keywords: "build", "API" → software-project-decomposition
- Load phases: [requirements, design, implement, test, deploy]

**Step 2: Phase Application**
- Requirements: Concrete (can specify API endpoints now)
- Design: Concrete (database schema, API structure)
- Implement: Vague (depends on design decisions)
- Test: Vague (depends on implementation approach)
- Deploy: Concrete (standard containerization)

**Step 3: Sub-task Creation**
```yaml
phase_1_requirements:
  - id: "api-spec"
    type: concrete
    description: "Define REST endpoints, request/response schemas"
    complexity: simple

phase_2_design:
  - id: "data-model"
    type: concrete
    description: "Design database schema for URLs, clicks, users"
    complexity: moderate
  
  - id: "system-architecture"
    type: concrete
    description: "Choose tech stack, define service boundaries"
    complexity: moderate

phase_3_implement:
  - id: "core-logic"
    type: vague
    depends_on: ["data-model", "system-architecture"]
    potential_paths:
      - "Microservices with Redis cache"
      - "Monolith with in-memory cache"
      - "Serverless with DynamoDB"
```

**Step 4: Dependency Mapping**
- api-spec → data-model (knowledge dependency)
- data-model + system-architecture → core-logic (data dependency)
- api-spec and data-model parallelizable (no shared inputs)

**Expert insight**: Novice would make implementation concrete too early. Expert keeps it vague until design completes.

### Example 2: Research Project - "Analyze remote work impact on productivity"

**Step 1: Domain Classification**
- Keywords: "analyze", "research" → research-synthesis-decomposition
- Load phases: [scope, gather, analyze, synthesize, report]

**Step 2: Critical Decisions**
- Scope concrete: Can define research questions now
- Gather vague: Data sources depend on scoping decisions
- Analysis vague: Methods depend on what data we find

**Step 3: Decomposition**
```yaml
phase_1_scope:
  - id: "research-questions"
    type: concrete
    description: "Define 3-5 specific research questions about remote work productivity"

phase_2_gather:
  - id: "data-collection"
    type: vague
    depends_on: ["research-questions"]
    potential_paths:
      - "Academic papers + industry reports"
      - "Survey new dataset of remote workers"
      - "Interview case studies from companies"

phase_3_analyze:
  - id: "statistical-analysis"
    type: vague
    depends_on: ["data-collection"]
    potential_paths:
      - "Quantitative analysis if numerical data"
      - "Qualitative coding if interview data"
      - "Meta-analysis if literature review"
```

**Expert insight**: Research decomposition keeps analysis methods vague until data characteristics are known. Novice would prematurely commit to statistical methods.

## Quality Gates

**Task decomposition is complete when**:

- [ ] Every vague node has 3+ potential paths listed
- [ ] No concrete sub-task requires more than 3 skills
- [ ] All dependencies form valid DAG (no cycles)
- [ ] At least 30% of sub-tasks are parallelizable
- [ ] Each sub-task has clear output description
- [ ] Domain meta-skill selected (or justified why zero-shot)
- [ ] Complexity estimates assigned (simple/moderate/complex)
- [ ] Total estimated cost under $5 for initial wave
- [ ] Critical path identified (longest dependency chain)
- [ ] Human gates marked for irreversible decisions

## NOT-FOR Boundaries

**This skill should NOT be used for**:
- **DAG Structure Building**: Once you have sub-tasks, use `dag-planner` to create node/edge graph
- **Task Execution**: Use `dag-runtime` to actually run the decomposed tasks
- **Skill Assignment**: Use `dag-skills-matcher` to assign specific skills to each node
- **Project Management**: For tracking progress/deadlines, use project management tools
- **Code Generation**: This creates task plans, not code. Use appropriate coding skills for implementation
- **Data Processing**: This plans data workflows, doesn't process data. Use data analysis skills for execution

**Delegation rules**:
- For executing any decomposed sub-task → Use appropriate domain skill
- For building DAG from sub-tasks → Use `dag-planner`
- For assigning skills to nodes → Use `dag-skills-matcher`
- For runtime orchestration → Use `dag-runtime`