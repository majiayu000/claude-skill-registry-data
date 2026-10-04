---
license: BSL-1.1
name: dag-orchestrator
description: |
  The intelligence layer of Jury-rig. Decomposes natural language tasks into proposed Hierarchical Task DAGs (HTDAGs), matches subtasks to skills, proposes wave and revision contracts, and expands nodes only when evidence supports a revised graph. Use for 'orchestrate', 'execute DAG', 'parallel agents', 'decompose task', 'coordinate skills'. NOT for single-skill tasks or simple linear workflows.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
  - TodoWrite
  - Grep
  - Glob
metadata:
  recognition-cues: []
  expectancies: []
  decision-cues: []
  adaptive-workarounds: []
  execution-pattern: sequential
  needs-cdm: true
  category: Agent & Orchestration
  tags:
    - dag
    - orchestration
    - task-decomposition
    - parallel-execution
    - htdag
    - adaptive-planning
  io-contract:
    kind: structured
    inputSchema: ./schemas/input.json
    outputSchema: ./schemas/output.json
---

# DAG Orchestrator

Transforms natural-language tasks into proposed agent graphs and execution contracts. Use [Orchestration Authority and Lifecycle](references/orchestration-authority-and-lifecycle.md): a graph is not a running system, and a controller must not claim dispatch, cancellation, join, or effect semantics without receipts from its executor.

## Decision Points

### 1. Initial Decomposition Strategy
```mermaid
flowchart TD
    A[Task contract] --> B[Name outputs, authority, acceptance, and effects]
    B --> F{Requirements or authority unresolved?}
    F -->|Yes| G[Halt for clarification or research]
    F -->|No| C{Artifacts become independent after declared prerequisites?}
    C -->|Yes| D[Propose parallel siblings after prerequisites with join and merge rules]
    C -->|No| E[Propose ordered prerequisites]
```

### 2. AND vs OR Composition Logic
```mermaid
flowchart LR
    A[Parent acceptance condition] --> B{All child receipts required?}
    B -->|Yes| C[AND join with failure policy]
    B -->|No| D{Any child may satisfy a stated criterion?}
    D -->|Yes| E[OR join with independent evaluator]
    D -->|No| F[Declare mixed/fallback semantics and effect containment]
```

### 3. Max Depth Calibration
```mermaid
flowchart TD
    A[Proposed decomposition] --> B{Each leaf has bounded artifact and acceptance test?}
    B -->|No| C[Refine or request missing contract]
    B -->|Yes| D{Depth or fan-out exceeds local resource policy?}
    D -->|Yes| E[Split into phases with revisioned handoff]
    D -->|No| F[Retain explicit graph]
```

### 4. Parallelization Safety Check
```mermaid
flowchart LR
    A[Candidate parallel wave] --> B[Check files, mutable resources, authority, and external effects]
    B --> C{Shared scarce or mutable boundary?}
    C -->|Yes| D[Serialize or grant a scoped lease]
    C -->|No| E[Parallel proposal with cancellation and join policy]
```

### 5. Failure Recovery Strategy
```mermaid
flowchart TD
    A[Executor receipt or timeout] --> B{Effect and completion state known?}
    B -->|No| C[Contain or cancel future work; reconcile before retry or dependent release]
    B -->|Yes| D{Acceptance condition satisfied?}
    D -->|Yes| E[Release dependents under declared policy]
    D -->|No| F[Contain dependents, propose revision, or escalate]
```

## Failure Modes

### Schema Bloat
**Symptoms**: DAG scope prevents clear ownership, contracts, or join semantics under its declared resource policy
**Detection**: A graph cannot state bounded artifacts, contracts, ownership, or join rules under its local resource policy
**Fix**: Split into revisioned phases or reduce scope; node count and estimates are planning inputs, not universal limits.

### Circular Dependencies  
**Symptoms**: Topological sort fails, "cyclic dependency" error in wave computation
**Detection**: Compare the processed-node count from Kahn's algorithm with the total node count, or retain a DFS back-edge witness; an acyclic prefix can exist before a cycle.
**Fix**: Preserve the cycle witness and ask the contract owner to revise the dependency or decompose an explicit intermediate artifact. Never delete an edge merely to make a sort succeed.

### Premature Parallelization
**Symptoms**: File conflicts, race conditions, inconsistent final state  
**Detection**: `if conflictingFiles.length > 0 || inconsistentOutputs`
**Fix**: Add explicit dependencies, use sequential waves for conflicting operations

### Infinite Decomposition
**Symptoms**: Depth keeps increasing, same task fails repeatedly at leaf level
**Detection**: A decomposition repeats the same unresolved obligation without a changed contract or evidence
**Fix**: Halt and request a new requirement, capability, or human decision rather than expanding depth by rule.

### Context Loss Cascade
**Symptoms**: Later waves fail due to missing information from earlier waves
**Detection**: `if waveN.inputs.missing.length > 0`
**Fix**: Ensure explicit context passing between waves, add context aggregation nodes

## Worked Examples

### Example: "Build authentication system for web app"

**Initial Assessment**: This is an illustrative authentication contract. Propose a revisioned graph only after naming its acceptance tests, credential/effect policy, and diagnosed component complexity.

**Wave 0 Decomposition**:
```typescript
// Initial breakdown
subtasks = [
  "Design user data schema",               // skill: database-architect
  "Specify authentication acceptance tests", // skill: test-engineer
  "Create login/signup API candidate",     // skill: api-architect
  "Build frontend auth candidate",         // skill: react-developer
  "Propose credential-policy candidate"     // skill: security-engineer
]
```

**Dependency Analysis**:
- The illustrative data, credential and effect contracts are prerequisites for the acceptance fixtures.
- The acceptance-test specification is a prerequisite for implementation candidates; executed evidence is evaluated before artifacts are accepted.
- API and frontend candidates may run after the frozen interface and fixtures only when their shared resources and effects have a valid coordination policy; their combined artifact is checked before acceptance.

**Illustrative dependency and acceptance graph**:
```mermaid
flowchart TD
    C[Define data, credential, and effect contracts] --> T[Specify acceptance fixtures]
    T --> A[Implement API candidate]
    T --> F[Implement frontend candidate against frozen interface]
    A --> J[Join compatible artifacts with attributed receipts]
    F --> J
    J --> R[Run component and integration checks]
    R --> X{All declared acceptance conditions established?}
    X -->|Yes| D[Accept artifacts under the named policy]
    X -->|No or unknown| E[Preserve findings and revise or escalate]
```

**Execution with Failure**:
```typescript
// An observed failure alone does not establish that decomposition is appropriate.
if (failureDiagnosis.complexityEvidence && effectStatus === "reconciled") {
  // Propose a revision after the task owner confirms the diagnosed complexity,
  // revised graph, authority, and acceptance checks.
  const apiSubtasks = [
    "Define authentication routes",
    "Implement password hashing", 
    "Add session management",
    "Create user CRUD operations"
  ];
  // A separate runner may execute the approved revision and emit receipts.
}
```

**Expert vs Novice**: 
- Novice: Assumes a familiar component order proves safe execution.
- Expert: Names the local contract, verifies prerequisites and effects, evaluates acceptance evidence before release, and revises only from a diagnosed condition.

## Quality Gates

- [ ] All subtasks have identified skill matches or fallback strategy
- [ ] Dependency graph has no cycles (topological sort succeeds)
- [ ] Shared file, semantic, authority, resource and effect requirements have explicit coordination policies; file overlap prediction alone is not sufficient
- [ ] Decomposition depth and wave size comply with a declared local resource policy
- [ ] Critical-path claims distinguish measurements from planning assumptions
- [ ] Executor results include receipt evidence or are explicitly unknown
- [ ] Context passing between waves explicitly defined
- [ ] Failure handling strategy defined for each critical node
- [ ] Resource constraints (memory, tokens, API calls) within limits
- [ ] Cancellation, join, duplicate-dispatch, and external-effect policies are declared

## NOT-FOR Boundaries

**Don't use DAG Orchestrator for**:
- Single-skill tasks → Use direct skill invocation
- Simple workflows whose artifacts, authority, and acceptance can be stated directly → use sequential task calls
- Real-time interactive tasks → Use conversational agents instead
- Tasks requiring human creativity/judgment → Use human-in-loop workflows
- Debugging/troubleshooting → Use diagnostic-specialist skill
- Data analysis/visualization → Use data-analyst skill

**Delegate instead**:
- Code reviews → Use code-reviewer skill
- Writing/editing → Use copywriter or technical-writer  
- Research synthesis → Use research-synthesizer skill
- UI/UX design → Use ui-ux-designer skill
