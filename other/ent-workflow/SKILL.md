---
name: ent-workflow
description: OpenSpec workflow and task delegation patterns. Spec-driven development with artifact creation, task tracking, and validation.
triggers:
  - ent-workflow
  - openspec
  - change proposal
  - spec workflow
  - artifact workflow
  - delegation
---

## Role

Guide through OpenSpec CLI workflows and proper task delegation patterns using the Task tool.

## OpenSpec CLI Workflow

OpenSpec uses **artifacts** to structure work:
- **proposal.md** - What and why (requirements, scope, approach)
- **tasks.md** - Implementation checklist
- **specs/** - Delta specs (changes to main specs)
- **implementation** - The actual code

Always use the `openspec` CLI via Bash, not MCP tools.

### Creating Changes

```bash
# Initialize OpenSpec in a project (if needed)
openspec init

# Create a new change
openspec new change add-feature-name

# Fast-forward: create all artifacts in one go
# This creates proposal.md, tasks.md, and any needed specs
openspec ff add-feature-name

# OR: Incremental artifact creation
openspec continue add-feature-name  # Creates next artifact
```

### Working with Artifacts

```bash
# Show change status and artifacts
openspec show add-feature-name

# Show specific artifact
openspec show add-feature-name --artifact proposal
openspec show add-feature-name --artifact tasks

# Get instructions for creating next artifact
openspec instructions add-feature-name

# Validate change structure
openspec validate add-feature-name
```

### Viewing Changes

```bash
# List all active changes
openspec list

# List specs
openspec list --specs

# Show change with all artifacts
openspec show add-feature-name --format markdown

# Check artifact completion status
openspec status add-feature-name
```

### Implementation

```bash
# Task implementation is guided by tasks.md
# After implementation, sync delta specs to main specs
openspec sync add-feature-name
```

### Archiving

```bash
# Verify before archive (checks all artifacts exist and are valid)
openspec validate add-feature-name

# Archive completed change
openspec archive add-feature-name
```

### Schema Management

```bash
# List available workflow schemas
openspec schemas

# Show template paths for a schema
openspec templates --schema default
```

## Workflow Patterns

### Pattern 1: Quick Feature (Fast-Forward)

```bash
# 1. Create change and all artifacts at once
openspec new change add-login-validation
openspec ff add-login-validation

# 2. Review generated artifacts
openspec show add-login-validation

# 3. Implement tasks from tasks.md

# 4. Archive when done
openspec archive add-login-validation
```

### Pattern 2: Incremental (Step-by-Step)

```bash
# 1. Create change directory
openspec new change refactor-auth

# 2. Create proposal first
openspec continue refactor-auth

# 3. Create tasks
openspec continue refactor-auth

# 4. Create specs if needed
openspec continue refactor-auth

# 5. Implement

# 6. Archive
openspec archive refactor-auth
```

### Pattern 3: Spec Updates

```bash
# 1. Create change for spec updates
openspec new change update-api-spec

# 2. Fast-forward to create artifacts
openspec ff update-api-spec

# 3. Edit delta specs in openspec/changes/update-api-spec/specs/

# 4. Sync to main specs
openspec sync update-api-spec

# 5. Archive
openspec archive update-api-spec
```

## Task Delegation Patterns

Most work should happen inline in the main conversation, where skills auto-activate. Spawn subagents via the Task tool when context isolation, parallel work, or a different model tier is needed.

### When to Delegate to Subagents

- **Context isolation** — verbose output (large codegen, deep search) that would pollute main context
- **Parallel work** — multiple independent tasks can run simultaneously
- **Different model tier** — task needs opus reasoning or haiku speed
- **Tool restrictions** — read-only exploration (use Explore agent type)

### Delegation by Task Type

| Task Type | Approach | If Subagent: Model + Type |
|-----------|----------|---------------------------|
| Write/modify code | Inline (skills auto-activate) | sonnet, general-purpose |
| Design architecture | Inline or subagent for isolation | opus, general-purpose |
| Break feature into tasks | Inline | sonnet, general-purpose |
| Quick triage | Inline | haiku, Explore |
| Fix a bug | Inline (debug-core skill activates) | sonnet, general-purpose |
| Debug concurrency/perf | Inline or subagent | opus, general-purpose |
| Write/fix tests | Inline (go-test skill activates) | sonnet, general-purpose |
| Review code | Subagent (read-only) | opus, Explore |
| Code investigation | Subagent (read-only) | haiku/sonnet, Explore |
| Verify requirements | Subagent (read-only) | opus, Explore |

### Subagent Invocation Examples

```
# Read-only exploration
Task(model: "haiku", subagent_type: "Explore", prompt: "...")

# Standard implementation
Task(model: "sonnet", subagent_type: "general-purpose", prompt: "...")

# Deep analysis or review
Task(model: "opus", subagent_type: "Explore", prompt: "...")
```

### Safety Checkpoints

Before irreversible operations:
1. Verify backups exist
2. Confirm user intent for destructive ops
3. Run validation before deployment
4. Test rollback procedures
5. Document decision and reasoning

## Common Pitfalls

### OpenSpec
1. **Don't duplicate OpenSpec functionality** - Always use `openspec` CLI
2. **Don't skip validation** - Always run `openspec validate` before archiving
3. **Don't manually move archives** - Use `openspec archive`
4. **Don't forget to sync specs** - Use `openspec sync` to update main specs

### Delegation
1. **Don't over-delegate** - Prefer inline work; subagents cost ~4x more tokens
2. **Don't skip handoff context** - When delegating, include clear requirements
3. **Don't assume state** - Always verify current state before acting
4. **Don't ignore blockers** - Escalate promptly when stuck

## Examples

### OpenSpec Workflow

<example>
<input>Create a new change for adding user authentication</input>
<output>
I'll create a new OpenSpec change for user authentication:

```bash
openspec new change add-user-authentication
```

Now I'll fast-forward to create all artifacts:

```bash
openspec ff add-user-authentication
```

This creates:
- `openspec/changes/add-user-authentication/proposal.md`
- `openspec/changes/add-user-authentication/tasks.md`
- Any needed specs in `openspec/changes/add-user-authentication/specs/`

Let me show the current status:

```bash
openspec show add-user-authentication
```
</output>
</example>

<example>
<input>What's the status of my current changes?</input>
<output>
Let me list all active changes:

```bash
openspec list
```

To see artifact completion status for a specific change:

```bash
openspec status change-name
```
</output>
</example>

## References

- OpenSpec CLI: `openspec --help`
- Change commands: `openspec change --help`
- Artifact workflow: `openspec instructions --help`
- Schemas: `openspec schemas`
