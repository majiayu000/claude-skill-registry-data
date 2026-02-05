---
name: implementation-planner
description: Generate comprehensive implementation plans for features. Use when user requests "help me implement X", "create a plan for X", "break down feature X", "how should I build X", or asks for detailed implementation guidance. Activates for planning requests, not exploratory design discussions.
allowed-tools: Read, Bash, Glob, Grep, Write, TodoWrite
---

# Implementation Planner v5.0

Generate conductor-compatible YAML plans. **Do NOT activate for:** questions, debugging, code reviews.

## Workflow

0. **Analyze** → Detect project type, extract patterns, build `project_context`
1. **Discover** → Agents (`fd '\.md$' ~/.claude/agents`), existing implementations
2. **Design** → Break into tasks, map dependencies, build data flow registry
3. **Implement** → Write `implementation.key_points` FIRST for each task
4. **Criteria** → Derive `success_criteria` FROM key_points (same terminology)
5. **Classify** → CAPABILITY (unit) vs INTEGRATION (cross-component)
6. **Generate** → Output YAML with all required fields
7. **Validate** → `conductor validate <plan>.yaml`

---

## Phase 0: Project Analysis (MUST run first)

Before planning, analyze the project to build `project_context`:

```bash
# 1. Detect project type from manifest files
ls -la *.json *.toml *.mod *.lock *.yaml *.yml 2>/dev/null | head -10

# 2. Read manifest to identify dependencies and scripts
cat package.json 2>/dev/null || cat go.mod 2>/dev/null || cat Cargo.toml 2>/dev/null || cat pyproject.toml 2>/dev/null

# 3. Find test framework from config or existing tests
grep -r "test" --include="*.json" --include="*.toml" -l 2>/dev/null | head -3
fd '_test\.' --type f | head -3   # Go/Rust pattern
fd '\.test\.' --type f | head -3  # JS/TS pattern
fd 'test_' --type f | head -3     # Python pattern

# 4. Learn commit style from recent history
git log --oneline -5

# 5. Discover code quality tools
cat .eslintrc* .prettierrc* rustfmt.toml .golangci.yml pyproject.toml 2>/dev/null | head -20
```

### Store as project_context

After analysis, mentally note:

| Field | Example Values |
|-------|----------------|
| `language` | go, typescript, rust, python, java |
| `manifest_file` | go.mod, package.json, Cargo.toml, pyproject.toml |
| `test_command` | go test ./..., npm test, cargo test, pytest |
| `build_command` | go build ./..., npm run build, cargo build, python -m build |
| `format_command` | gofmt -w ., prettier --write ., cargo fmt, black . |
| `lint_command` | golangci-lint run, eslint ., cargo clippy, ruff . |
| `module_term` | package (Go), module (TS/Rust), package (Python) |

Use `project_context` values throughout the plan instead of hardcoded examples.

---

## Critical Rules

| Rule | Rationale |
|------|-----------|
| **Key points → Criteria** | Every `success_criteria` item MUST trace to a `key_point` using IDENTICAL terms |
| **Data flow deps** | If task B uses function from task A, B must `depends_on: [A]` |
| **Module serialization** | Tasks modifying same module/package need sequential deps |
| **Verify before claiming** | `grep` to confirm existing behavior before writing key_points |
| **Code reuse first** | Search for existing implementations before creating new code |
| **No wrappers without value** | Direct usage preferred over unnecessary abstraction |

**Auto-append to ALL tasks' success_criteria:**
- No TODO comments in production code
- No placeholder types (empty structs/interfaces)
- No unused variables
- All imports from deps resolve

---

## Phase 1-2: Discovery & Design

```bash
fd '\.md$' ~/.claude/agents --type f     # Available agents
ls -la                                    # Codebase structure
cat {manifest_file}                       # From project_context
ls <expected/path> 2>/dev/null            # Verify paths exist
grep -r "pattern" src/ lib/ internal/     # Find existing implementations
```

### Data Flow Registry (CRITICAL)

Build producer/consumer map to ensure correct dependencies:

```yaml
# Comment block at top of plan:
# PRODUCERS: Task 4 → ExtractMetrics, Task 5 → LoadSession
# CONSUMERS: Task 16 → [4, 5, 15]
# VALIDATION: All consumers depend_on producers ✓

# YAML field (validated by Conductor):
data_flow_registry:
  producers:
    FunctionName:
      - task: 4
        description: "Creates this function"
  consumers:
    FunctionName:
      - task: 16
        description: "Uses this function"
```

---

## Phase 3-4: Implementation → Criteria

**Write key_points FIRST, then derive criteria:**

```yaml
implementation:
  approach: |
    Strategy and architectural decisions.
  key_points:
    - point: "EnforceModuleIsolation with git diff"
      details: "Compare modified files against task.Files"
      reference: "src/executor/module_guard.ts"  # Use project's actual paths

# Derived using SAME terminology:
success_criteria:
  - "EnforceModuleIsolation runs git diff, compares against task.Files"
```

**Key point requirements:** Specific (names exact function/type), Verifiable (grep/test), Complete (all requirements).

---

## Phase 5: Classification

| Type | Scope | Criteria Field |
|------|-------|----------------|
| CAPABILITY | What component does alone | `success_criteria` |
| INTEGRATION | How components work together | `integration_criteria` |

**Route by keyword:**
- CLI flags, UI rendering, cross-component calls → `integration_criteria`
- Internal logic, data structures, algorithms → `success_criteria`

**RFC 2119 Routing:**

| Level | Route To | Behavior |
|-------|----------|----------|
| MUST | `test_commands` | Hard gate |
| SHOULD | `success_criteria` | QC reviews |
| MAY | `documentation_targets` | Informational |

---

## YAML Schema

### Root Structure

```yaml
conductor:
  default_agent: general-purpose
  worktree_groups:
    - group_id: "name"
      tasks: [1, 2, 3]
      rationale: "Why grouped"

planner_compliance:
  planner_version: "5.0.0"
  strict_enforcement: true
  required_features: [dependency_checks, test_commands, success_criteria, data_flow_registry, package_guard]

data_flow_registry:
  producers: {}
  consumers: {}

plan:
  metadata:
    feature_name: "Name"
    created: "YYYY-MM-DD"
    target: "Goal"
  context:
    framework: "{language}"           # From project_context
    test_framework: "{test_command}"  # From project_context
  tasks: []
```

### Task Structure

```yaml
- task_number: "1"
  name: "Task name"
  agent: "agent-name"
  files: ["src/path/to/file.ext"]     # Use project's actual structure
  depends_on: []

  success_criteria:
    - "Criterion from key_point 1"
    - "No TODO/placeholder/unused patterns"

  test_commands:
    - "{test_command} {test_path}"    # From project_context

  runtime_metadata:
    dependency_checks:
      - command: "{build_command}"    # From project_context
        description: "Verify build"
    documentation_targets: []

  description: |
    <dependency_verification priority="execute_first">
      <commands># verify deps</commands>
    </dependency_verification>
    <task_description>What to implement.</task_description>

  implementation:
    approach: |
      Strategy.
    key_points:
      - point: "Name"
        details: "What and why"
        reference: "file.ext"

  code_quality:
    pipeline:
      command: "{format_command} && {test_command}"  # From project_context
      exit_on_failure: true

  commit:
    type: "feat"
    message: "description"
    files: ["path/**"]
```

### Cross-File Dependencies

```yaml
depends_on:
  - 4                                    # Same file
  - file: "plan-01-foundation.yaml"      # Different file
    task: 2
```

### Integration Tasks

```yaml
- task_number: "N"
  type: integration
  success_criteria: [...]      # Component-level
  integration_criteria: [...]  # Cross-component
```

---

## TDD Guidance

TDD is RECOMMENDED for component tasks (new logic). Not required for wiring/config/docs.

| Task Type | Testing Approach |
|-----------|------------------|
| New component with logic | TDD preferred - test in same task |
| Wiring/integration | Test-after or integration tests |
| Config/types only | Validation tests if applicable |
| Documentation | None |

When using TDD, include test file in task's `files[]` and test command in `test_commands[]`.

---

## Validation Checklist

```
□ Every key_point has corresponding success criterion (same terms)
□ Every success criterion traces to a key_point
□ Data flow: consumers depend_on all producers
□ Module conflicts serialized via depends_on
□ All file paths verified to exist (or will be created)
□ Integration tasks have both success_criteria AND integration_criteria
□ Every task has: implementation, success_criteria, test_commands, runtime_metadata
```

**Final step:**
```bash
conductor validate docs/plans/<plan>.yaml
```

---

## Post-Validation Checklist (MUST run after conductor validate passes)

Schema compliance verification - MUST check each item:

```
□ planner_compliance.required_features = [dependency_checks, test_commands, success_criteria, data_flow_registry, package_guard]
□ conductor.worktree_groups defined with group_id, tasks, rationale
□ data_flow_registry.producers lists all cross-task data creators
□ data_flow_registry.consumers lists all cross-task data users
□ Every task has commit section with type, message, files
□ Every task has code_quality section with project-appropriate commands
□ plan.metadata has feature_name, created, target
□ plan.context has framework, test_framework (matching project_context)
```

MUST NOT proceed to execution if any checkbox fails.

---

## Common Failures

| Failure | Prevention |
|---------|------------|
| Agent implements wrong thing | Write ALL requirements in key_points |
| QC fails despite working code | Derive criteria FROM key_points |
| Missing dependency | Build producer registry |
| Scope leak | Classify criteria by type |
| Assumed behavior wrong | grep before claiming defaults |
| Wrong test/build commands | Run Phase 0 analysis first |
| Multi-file plan: ~2000 lines max | Split at worktree group boundaries |
