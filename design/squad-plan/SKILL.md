---
name: squad-plan
description: Generate a parallel workstream plan for multi-agent Claude Code work. Decomposes a feature into independent workstreams, each ownable by a separate Claude Code instance. Saves to claude/tasks/ACTION_PLAN.md.
---

# Squad Plan Skill

Generate a detailed parallel execution plan for multi-agent work on a complex feature.

## When to Use
- Task touches ≥3 independent components/files
- Components don't share mutable state during the task
- Estimated single-agent time > 15 minutes
- Each subtask can own a distinct file set (no overlap)

## Protocol

### Phase 1: Analyze the Task

1. Read `CLAUDE.md` and `claude/architecture.md` for project context
2. Break down the task into independent subtasks
3. Identify natural parallelism boundaries (frontend/backend, services, features, layers)
4. Map dependencies — what must complete before something else starts
5. Identify shared resources requiring coordination (DB schemas, API contracts, shared types)

### Phase 2: Design Workstreams (2-5 workstreams)

For each workstream:
- **Workstream ID & Title** — e.g., "WS1: API Layer"
- **Objective** — what this workstream accomplishes
- **Files/Components owned** — specific parts of the codebase
- **Tasks** — numbered checklist items with expected outcomes and verification steps
- **Dependencies** — which tasks from other workstreams must complete first
- **Deliverables** — what this workstream produces for others to consume

### Phase 3: Integration Strategy

1. Define integration points between workstreams
2. Create integration test checklist
3. Specify merge order (which branch merges first)
4. Define smoke test for the combined result

### Phase 4: Write ACTION_PLAN.md

Save to `claude/tasks/ACTION_PLAN.md`:

```markdown
# ACTION_PLAN — [Feature Name]

## Overall Objective
[Clear statement of the goal]

## Workstream Definitions

### WS1: [Title]
**Objective:** [Goal]
**Files:** [List]

#### Tasks
- [ ] Task 1: [Description]
- [ ] Task 2: ...

**Dependencies:** None (can start immediately)
**Delivers to:** WS2 needs [output] from Task 3

### WS2: [Title]
...

## Integration Points
- [ ] [Integration task 1]

## Testing Strategy
- [ ] Unit tests per workstream
- [ ] Integration tests after merge
- [ ] End-to-end smoke test
```

## Usage with Multiple Claude Code Instances

After generating, assign instances:
```
"You are the Backend Developer. Execute Workstream WS1 from claude/tasks/ACTION_PLAN.md."
"You are the Frontend Developer. Execute WS2, noting you depend on WS1 Task 3."
```

Each instance reads `CLAUDE.md` for project standards and follows the Explore-Plan-Act workflow.
