---
name: parallel-task-format
short: Task specification format for parallel agents
description: Compact YAML format for defining parallel task specifications with scope, boundaries, and agent assignments. Use when creating task files for parallel development.
when: User wants to create task specifications, define task boundaries and scope, structure task files for agents, or understand the task YAML format
---

# Task Specification Format

Compact YAML format for parallel task files in `parallel/TS-XXXX-slug/tasks/`.

## Complete Task Example

```yaml
---
id: task-001
component: users
wave: 1
deps: []
blocks: [task-004, task-005]
agent: python-experts:django-expert
tech_spec: TS-0042
contracts: [contracts/types.py, contracts/api-schema.yaml]
---
# task-001: User Management

## Scope
CREATE: apps/users/{models,views,serializers,urls}.py, apps/users/tests/*.py
MODIFY: config/urls.py
BOUNDARY: apps/orders/*, apps/products/*, apps/*/migrations/*

## Requirements
- User model with email authentication
- UserSerializer with explicit fields
- UserViewSet (list, retrieve, create, update)
- Email uniqueness validation

## Checklist
- [ ] Model matches UserDTO in contracts/types.py
- [ ] API matches /api/users/* in contracts/api-schema.yaml
- [ ] pytest apps/users/ passes
- [ ] mypy apps/users/ passes
- [ ] ruff check apps/users/ passes
- [ ] No files modified outside scope
```

## YAML Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Task identifier (task-NNN or task-NNN-component) |
| `component` | Yes | System component name |
| `wave` | Yes | Dependency wave number (1, 2, 3...) |
| `deps` | Yes | Task IDs this depends on (empty list `[]` if none) |
| `blocks` | No | Task IDs this blocks (optional) |
| `agent` | Yes | Recommended agent type |
| `tech_spec` | No | Tech Spec ID (if applicable) |
| `contracts` | Yes | Contract files to reference (relative paths) |

## Scope Section Format

Use compact notation with three directives:

### CREATE
Files to create (use glob patterns):
```
CREATE: apps/users/{models,views,serializers,urls}.py, apps/users/tests/*.py
```

### MODIFY
Existing files to modify:
```
MODIFY: config/urls.py, config/settings.py
```

### BOUNDARY
Files NOT to touch (owned by other tasks):
```
BOUNDARY: apps/orders/*, apps/products/*, apps/*/migrations/*
```

## Task Naming Convention

```
task-{number}-{component}.md

Examples:
- task-001-users.md
- task-002-products.md
- task-003-orders.md
- task-004-api.md
- task-005-integration.md
```

## Agent Type Selection

| Task Files | Agent | Description |
|------------|-------|-------------|
| `apps/*/models.py`, `apps/*/views.py` | `python-experts:django-expert` | Django models, views, serializers |
| `api/*.py`, `routers/*.py` | `python-experts:fastapi-expert` | FastAPI endpoints |
| `src/components/*.tsx` | `frontend-experts:react-typescript-expert` | React components |
| `**/test_*.py`, `**/tests/*.py` | `python-experts:python-testing-expert` | Python tests |
| `*.spec.ts`, `*.test.tsx` | `frontend-experts:playwright-testing-expert` | TypeScript/E2E tests |
| `terraform/`, `docker-compose.yml` | `devops-data:devops-expert` | Infrastructure |
| Integration, architecture | `devops-data:cto-architect` | Cross-cutting concerns |

## Contract References

Contracts are in the same parallel directory:
```
parallel/TS-0042-slug/
  contracts/
    types.py        # Reference as: contracts/types.py
    api-schema.yaml # Reference as: contracts/api-schema.yaml
  tasks/
    task-001-users.md
```

## Wave Dependencies

Tasks in Wave N can only depend on tasks in Waves 1 to N-1:

```
Wave 1: task-001, task-002 (no dependencies, run in parallel)
Wave 2: task-003 (depends on task-001, task-002)
Wave 3: task-004 (depends on task-003)
```

### deps vs blocks

- `deps`: Tasks that MUST complete before this task starts
- `blocks`: Tasks that CANNOT start until this task completes

Both express the same relationship from different perspectives:
```yaml
# task-001
blocks: [task-003]

# task-003
deps: [task-001]
```

## Requirements Section

Clear, actionable requirements:

```markdown
## Requirements
- Implement `User` model with fields: `email`, `username`, `password`, `is_active`
- Create `UserSerializer` with all User fields (hide password)
- Implement `UserViewSet` with: list, retrieve, create, update
- Add email validation and uniqueness constraint
- Test coverage: minimum 85%
```

## Checklist Section

Verification criteria:

```markdown
## Checklist
- [ ] Model matches DTO in contracts/types.py
- [ ] API matches schema in contracts/api-schema.yaml
- [ ] pytest apps/users/ passes
- [ ] mypy apps/users/ --strict passes
- [ ] Coverage >= 85%
- [ ] No files modified outside scope
```

## Why Compact Format?

1. **Token efficiency**: Less tokens for agent context
2. **Faster parsing**: YAML frontmatter is standard
3. **Clear boundaries**: Scope section is scannable
4. **Actionable checklist**: Verification is explicit

## Validation Rules

Before using tasks:

- [ ] Every task has unique `id`
- [ ] Every task has `agent` assigned
- [ ] Every task has `contracts` referenced
- [ ] Every task has BOUNDARY section
- [ ] No circular dependencies in `deps`
- [ ] Wave numbers are sequential (1, 2, 3...)
- [ ] Wave 1 tasks have `deps: []`

## Output Format

The Output Format JSON block is **not included in task files**. It's a static template that the `parallel-prompt-generator` skill automatically adds to every generated prompt.

See the `parallel-prompt-generator` skill for the complete prompt template including the Output Format section.
