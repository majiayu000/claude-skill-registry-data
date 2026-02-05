---
name: socratic-ideation-tree
description: Transform abstract goals into concrete, actionable tasks through Socratic questioning and hierarchical decomposition. Use when users need to (1) break down complex projects into manageable parts, (2) clarify vague ideas into specific implementations, (3) generate systematic project structures, (4) explore multiple solution paths, (5) create task hierarchies for any domain (software, business, personal goals, research, construction). Triggers include requests to "break down", "decompose", "plan", "structure", "ideate", "brainstorm systematically", or transform ideas into actionable tasks.
---

# Socratic Ideation Tree

Transform abstract intentions into concrete implementations through systematic questioning and hierarchical decomposition.

## Core Pattern

```
Abstract → Specific → Implementation → Tasks
```

Domain applications:
- **Software**: Project → Features → Architecture → Code Tasks
- **Research**: Question → Hypotheses → Experiments → Procedures
- **Business**: Strategy → Initiatives → Projects → Deliverables
- **Personal**: Vision → Goals → Habits → Actions

## Project Structure

```
project-name/
├── INTENT.md              # Core values, constraints, success criteria
├── ideas/
│   ├── idea-1/
│   │   ├── IDEA.md        # Concept definition
│   │   └── tasks/
│   │       ├── task-1/
│   │       │   ├── TASK.md
│   │       │   └── subtasks/
│   │       │       ├── subtask-1.md
│   │       │       └── subtask-2.md
│   │       └── task-2/
│   ├── .idea-2/           # Dot-prefix = auto-generated, pending review
│   │   └── .IDEA.md
│   └── idea-3/
└── .feedback.md           # Track rejected suggestions patterns
```

**Dot-prefix convention**: Files/folders prefixed with `.` are auto-generated suggestions pending user review. Remove the `.` prefix to promote into the main tree.

## Phase 1: Intent Crystallization

Ask 3-5 questions to understand project essence:

1. **Vision**: "What transformation are you achieving? What does success look like?"
2. **Values**: "What principles must this honor? What's non-negotiable?"
3. **Context**: "What resources, skills, or limitations shape this?"
4. **Motivation**: "Why does this matter? What problem does it solve?"
5. **Scope**: "What's the timeframe? What defines 'done'?"

### INTENT.md Template

```markdown
# Project Intent: [Name]

## Vision
[End state description]

## Core Values
- [Principle 1]: [Why it matters]
- [Principle 2]: [Why it matters]

## Constraints
- Time: [Deadline]
- Resources: [Budget, team, tools]
- Scope: [Boundaries]

## Success Metrics
- [ ] [Quantifiable outcome 1]
- [ ] [Qualitative outcome 2]

## Context
[Background, current state]

## Decision Log
- [Date]: [Decision and rationale]
```

## Phase 2: Idea Generation

For each approach to achieving intent, ask:

1. **Approach**: "What are 3-5 different ways to achieve this?"
2. **Differentiation**: "What makes each unique? What tradeoffs exist?"
3. **Feasibility**: "Which approaches best fit your constraints?"

### IDEA.md Template

```markdown
# Idea: [Name]

## Concept
[One paragraph description]

## Why This Approach
- Aligns with [value] because...
- Fits within [constraint] via...

## Key Components
1. [Component]: [Purpose]
2. [Component]: [Purpose]

## Dependencies
- Requires: [Prerequisites]
- Assumes: [Conditions]

## Risk Assessment
- Primary risk: [Risk]
- Mitigation: [Strategy]

## Next Steps
- [ ] [Action item]
```

## Phase 3: Task Decomposition

Apply Socratic decomposition to each component:

1. **Implementation**: "What specific steps make this real?"
2. **Sequence**: "What must happen first? What can be parallel?"
3. **Definition**: "How will you know each step is complete?"
4. **Skill**: "What knowledge or tools does each step require?"

### TASK.md Template

```markdown
# Task: [Name]

## Objective
[Single sentence]

## Acceptance Criteria
- [ ] Given [context], when [action], then [outcome]
- [ ] [Measurable result]

## Implementation Approach
[Technical/practical approach]

## Dependencies
- Blocked by: [Previous tasks]
- Blocks: [Future tasks]
- Requires: [Resources]

## Estimated Effort
[Time or complexity]

## Subtasks
1. [ ] [Atomic action]
2. [ ] [Atomic action]

## Notes
[Design decisions, rationale]
```

## Phase 4: Iterative Refinement

Continue decomposition until tasks are:
- **Atomic**: Single responsibility, clear completion
- **Estimable**: Can assign time/effort confidently
- **Testable**: Clear pass/fail criteria
- **Assignable**: Can delegate to person or tool

## Suggestion Protocol

At each response, offer 2-3 alternative paths:

```markdown
## Suggested Next Steps

**Option A: [Direction]**
- Focus: [Priority]
- Next question: [Exploration]
- Tradeoff: [Sacrifice]

**Option B: [Direction]**
- Focus: [Different priority]
- Next question: [Different exploration]
- Tradeoff: [Different sacrifice]
```

## Auto-Ideation

For autonomous exploration of branches, see [references/auto-ideate.md](references/auto-ideate.md).

Key behaviors:
- Creates `.` prefixed files/folders in main tree (e.g., `ideas/.new-approach/`)
- User removes `.` prefix to promote suggestions
- Tracks patterns in `.feedback.md` at project root

## Anti-Patterns to Avoid

1. **Premature Specificity**: Don't detail implementation before understanding intent
2. **Analysis Paralysis**: Limit to 3-5 options per decision point
3. **Flat Hierarchy**: Maintain clear parent-child relationships
4. **Orphan Tasks**: Every task must connect to an idea and intent
5. **Vague Completion**: Every item needs clear "done" criteria

## Quick Start

```bash
# Initialize project
mkdir project-name && cd project-name
touch INTENT.md
mkdir ideas

# Create idea
mkdir -p ideas/approach-1/tasks
touch ideas/approach-1/IDEA.md

# Create task with subtasks
mkdir -p ideas/approach-1/tasks/task-1/subtasks
touch ideas/approach-1/tasks/task-1/TASK.md
```

## Additional References

- **Workflow patterns**: See [references/workflows.md](references/workflows.md) for sequential, conditional, and parallel patterns
- **Output templates**: See [references/output-patterns.md](references/output-patterns.md) for domain-specific templates
