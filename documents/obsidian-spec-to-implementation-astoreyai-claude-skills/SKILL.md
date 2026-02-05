---
name: obsidian-spec-to-implementation
description: Transforms product or technical specifications into concrete implementation plans and task notes within Obsidian. Parses spec documents, extracts requirements, creates structured implementation plans with linked tasks, and manages development workflow from requirements to completion using markdown files and frontmatter.
---

# Spec to Implementation

Transforms specifications into actionable implementation plans with progress tracking. Locates spec notes, extracts requirements, breaks down into task notes, and manages implementation workflow within your Obsidian vault.

## Quick Start

When asked to implement a specification:

1. **Locate spec**: Search vault for specification note
2. **Read spec**: Parse specification content and frontmatter
3. **Extract requirements**: Structure requirements from spec
4. **Create implementation plan**: Generate plan note with structured breakdown
5. **Create task notes**: Generate individual task notes linked to plan
6. **Track progress**: Update task statuses and maintain progress log

## Implementation Workflow

### Step 1: Locate the specification

```bash
# Search for spec by name or content
grep -r "specification_title" /path/to/vault/
find /path/to/vault -name "*spec*.md"

# Or search using tags
grep -l "#spec" /path/to/vault/**/*.md
```

Look for notes with:
- `#spec` or `#specification` tags
- `type: specification` in frontmatter
- Spec-related folder locations (e.g., `/specs/`, `/requirements/`)

If spec location is ambiguous, ask user for the file path or note name.

### Step 2: Read and analyze specification

```bash
# Read the spec note
cat /path/to/vault/specs/feature-name.md
```

Parse specification content:
- **Frontmatter**: Extract metadata (title, date, status, owner)
- **Functional requirements**: User stories, features, workflows, data needs
- **Non-functional requirements**: Performance, security, scalability
- **Acceptance criteria**: Testable conditions and completion definitions
- **Dependencies**: External systems, other features, blockers

See [reference/spec-parsing.md](reference/spec-parsing.md) for detailed parsing patterns.

### Step 3: Create implementation plan

Generate a structured plan note with:

1. Plan metadata (frontmatter)
2. Specification link
3. Requirements summary
4. Technical approach
5. Implementation phases with tasks
6. Dependencies and risks
7. Timeline and milestones
8. Success criteria

Use plan template from [reference/implementation-plan-template.md](reference/implementation-plan-template.md).

### Step 4: Generate implementation plan note

```bash
# Create plan note
touch /path/to/vault/plans/feature-name-implementation.md
```

**Frontmatter structure:**
```yaml
---
type: implementation-plan
spec: "[[specs/feature-name]]"
status: planning
created: 2025-10-20
updated: 2025-10-20
owner: "[[people/developer-name]]"
priority: high
tags:
  - plan
  - implementation
  - project-name
---
```

**Content structure:**
- Link back to spec: `Related Specification: [[specs/feature-name]]`
- Phases with checkboxes for visual progress tracking
- Task breakdown with links to task notes
- Dependencies and blockers section

See [reference/standard-implementation-plan.md](reference/standard-implementation-plan.md) for complete template.

### Step 5: Create task notes

For each task in the plan:

```bash
# Create task note
touch /path/to/vault/tasks/task-name.md
```

**Task note frontmatter:**
```yaml
---
type: task
plan: "[[plans/feature-name-implementation]]"
spec: "[[specs/feature-name]]"
status: todo
priority: high
estimate: 2d
assignee: "[[people/developer-name]]"
created: 2025-10-20
tags:
  - task
  - feature-name
  - component-name
---
```

**Task note content:**
- Task description and context
- Acceptance criteria (checklist)
- Technical approach
- Dependencies
- Progress log section

Link tasks bidirectionally:
- Task → Plan: `Part of [[plans/feature-name-implementation]]`
- Plan → Task: `- [ ] [[tasks/implement-api-endpoint]]`

See [reference/task-creation.md](reference/task-creation.md) for detailed task patterns.

### Step 6: Track progress

**Update task status:**
```yaml
---
status: in-progress  # todo → in-progress → review → done
progress: 60%
updated: 2025-10-20
---
```

**Add progress notes:**
```markdown
## Progress Log

### 2025-10-20 15:30
- ✅ Completed database schema design
- 🔄 Working on API endpoint implementation
- ⏭️ Next: Add request validation
- 🚧 Blocker: Waiting for API key from external service
```

**Update implementation plan:**
- Check off completed tasks: `- [x] [[tasks/design-database-schema]]`
- Update phase progress percentages
- Add milestone completion notes
- Adjust timeline if needed

See [reference/progress-tracking.md](reference/progress-tracking.md) for tracking patterns.

## Vault Organization

**Recommended folder structure:**
```
vault/
├── specs/              # Specification notes
├── plans/              # Implementation plans
├── tasks/              # Task notes
├── people/             # Team member notes
└── projects/           # Project MOCs (Maps of Content)
```

**Alternative using project folders:**
```
vault/
└── projects/
    └── feature-name/
        ├── spec.md
        ├── implementation-plan.md
        └── tasks/
            ├── task-1.md
            └── task-2.md
```

## Spec Analysis Patterns

**Functional Requirements**: Extract user stories, feature descriptions, workflows, data requirements, integration points

**Non-Functional Requirements**: Identify performance targets, security requirements, scalability needs, availability, compliance

**Acceptance Criteria**: Define testable conditions, user validation points, performance benchmarks, completion definitions

See [reference/spec-parsing.md](reference/spec-parsing.md) for detailed parsing techniques.

## Task Breakdown Strategies

**By Component**: Database schema → API endpoints → Frontend components → Integration → Testing

**By Feature Slice**: Vertical slices through the stack (e.g., complete auth flow, data entry workflow, report generation)

**By Priority**: 
- P0 (must have): Core functionality
- P1 (important): Enhanced features
- P2 (nice to have): Optional improvements

## Progress Tracking Patterns

**Daily Updates** (active work):
- Add progress log entry
- Update task status in frontmatter
- Note completed items and current focus
- Document blockers

**Milestone Updates** (major progress):
- Check off tasks in implementation plan
- Add milestone summary to plan note
- Update timeline if needed
- Link to deliverables (PRs, designs)

**Status Transitions**:
- `todo` → `in-progress`: Add start note
- `in-progress` → `review`: Add completion note
- `review` → `done`: Add final note with deliverables

## Linking Strategy

**Forward Links** (from spec):
```markdown
## Implementation
- Plan: [[plans/feature-name-implementation]]
- Tasks: [[tasks/task-1]], [[tasks/task-2]]
```

**Backward Links** (to spec):
```markdown
## Specification
Related to: [[specs/feature-name]]
```

**Bidirectional traceability**: Maintain links in both directions for easy navigation using Obsidian's backlinks pane.

## Dataview Queries

Use Dataview plugin to generate dynamic views:

**All tasks for a plan:**
```dataview
TABLE status, priority, assignee, estimate
FROM "tasks"
WHERE plan = [[plans/feature-name-implementation]]
SORT priority DESC, status ASC
```

**Progress dashboard:**
```dataview
TABLE 
  length(filter(file.tasks, (t) => t.completed)) as "Done",
  length(filter(file.tasks, (t) => !t.completed)) as "Remaining",
  round(length(filter(file.tasks, (t) => t.completed)) / length(file.tasks) * 100) + "%" as "Progress"
FROM "plans"
WHERE type = "implementation-plan"
```

## Best Practices

1. **Maintain bidirectional links**: Link spec ↔ plan ↔ tasks
2. **Use consistent frontmatter**: Standardize fields across all notes
3. **Break down into small tasks**: Each task completable in 1-2 days
4. **Extract clear acceptance criteria**: Define "done" explicitly
5. **Tag systematically**: Use consistent tags for filtering
6. **Update progress regularly**: Daily notes for active work
7. **Use checklists**: Visual indicators in markdown
8. **Link deliverables**: PRs, designs, docs link back to tasks

## Graph View Benefits

Obsidian's graph view visualizes relationships:
- Spec at center with plan and tasks radiating outward
- Connected tasks show dependencies
- Tag-based clustering shows project groupings

## Common Issues

**"Can't find spec"**: 
- Search by tag: `#spec`
- Search by folder: `/specs/`
- Search content: `grep -r "feature name"`
- Ask user for file path

**"Multiple specs found"**: 
- Show options to user
- Use most recently modified
- Search by more specific terms

**"Spec unclear"**: 
- Note ambiguities in plan
- Create clarification tasks
- Add questions section

**"Requirements conflicting"**: 
- Document conflicts in plan
- Create decision task
- Link to decision log

**"Scope too large"**: 
- Break into multiple specs
- Create phases in plan
- Prioritize must-haves

## Scripts

The `scripts/` directory contains utilities:

**create_task.py**: Generate task note from template
**update_status.py**: Batch update task statuses
**progress_report.py**: Generate progress summary from tasks
**link_validator.py**: Check for broken links between notes

See individual scripts for usage.

## Examples

Complete workflow examples in [examples/](examples/):
- [examples/api-feature.md](examples/api-feature.md) - API feature implementation
- [examples/ui-component.md](examples/ui-component.md) - Frontend component
- [examples/database-migration.md](examples/database-migration.md) - Schema changes

## Advanced Features

For additional patterns, templates, and techniques:
- [reference/spec-parsing.md](reference/spec-parsing.md) - Detailed parsing methods
- [reference/task-creation.md](reference/task-creation.md) - Task note patterns
- [reference/progress-tracking.md](reference/progress-tracking.md) - Tracking strategies
- [reference/implementation-plan-template.md](reference/implementation-plan-template.md) - Full plan template
