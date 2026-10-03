---
name: re-specialize
description: "Incremental re-specialization — re-scans the project and updates only auto-generated zones in CLAUDE.md and agents"
user-invocable: true
workflow:
  version: 1
  steps:
    - id: read-current
      role: system
      intent: "Read current CLAUDE.md and agent files to identify existing zones."
      produces: [current-claude-md, current-agents]
    - id: explore-project
      role: system
      intent: "Scan project for current stack, dependencies, architecture, conventions."
      produces: [detected-stack, detected-architecture, detected-conventions]
      gate: true
    - id: check-zones
      role: system
      intent: "Check if CLAUDE.md has guild zone markers. If not, offer to inject them."
      requires: [current-claude-md]
      produces: [zone-status]
      gate: true
    - id: regenerate-zones
      role: tech-lead
      intent: "Generate new content for each auto zone based on fresh project scan. Present diff to user."
      requires: [current-claude-md, detected-stack, detected-architecture, detected-conventions, zone-status]
      produces: [updated-claude-md, zone-diffs]
      model-tier: reasoning
    - id: update-agents
      role: tech-lead
      intent: "Update agent-context zones in agent files with fresh project context."
      requires: [detected-stack, detected-architecture, detected-conventions]
      produces: [updated-agents]
      model-tier: execution
    - id: confirm
      role: system
      intent: "Present summary of changes and get user confirmation."
      requires: [zone-diffs, updated-agents]
      produces: [confirmation]
      gate: true
    - id: commit
      role: system
      intent: "Commit re-specialized files."
      requires: [updated-claude-md, updated-agents, confirmation]
      produces: [re-specialize-commit]
---

# Re-Specialize

Incrementally updates auto-generated content in CLAUDE.md and agent files
without touching user customizations. Uses protected zone markers to identify
what can be safely regenerated.

## When to use

- When project dependencies have changed (new framework, updated versions)
- When architecture has evolved (new patterns, restructured folders)
- When agents need refreshed context about the project
- Periodically to keep CLAUDE.md in sync with the actual codebase

## Process

### Step 1 -- Read current state

Read CLAUDE.md and all agent files in `.claude/agents/`:

- Identify existing zone markers (`<!-- guild:auto-start:ID -->` / `<!-- guild:auto-end:ID -->`)
- Note which zones exist and their current content
- Identify any user customizations outside of zones

### Step 2 -- Explore the project

Same exploration as guild-specialize:

- Scan dependency files for current stack and versions
- Analyze project structure and architecture patterns
- Detect code conventions from linter/formatter configs
- Check environment variable examples

### Step 3 -- Check zone markers

If CLAUDE.md has zone markers, proceed to regeneration.

If CLAUDE.md does NOT have zone markers (legacy project):

- Offer to inject markers around the auto-generated sections
- Show the user where markers would be placed
- Require explicit confirmation before modifying
- If user declines, abort gracefully

### Step 4 -- Regenerate zone content

Invoke the Tech Lead agent using Task tool with `model: "opus"` (reasoning tier):

- Generate fresh content for each zone based on the project scan
- Compare new content with existing zone content
- Present a diff for each zone to the user
- Only replace zones where content has actually changed

Zones to regenerate:

| Zone ID        | Content                                    |
|----------------|--------------------------------------------|
| `structure`    | Project folder structure with descriptions |
| `architecture` | Architecture patterns and design decisions |
| `conventions`  | Code conventions from linter/formatter     |
| `env-vars`     | Environment variables from .env.example    |

### Step 5 -- Update agent context

Invoke the Tech Lead agent using Task tool with `model: "sonnet"` (execution tier):

- For each agent in `.claude/agents/*.md`, update the `agent-context` zone
- If no `agent-context` zone exists, append one at the bottom
- Preserve everything outside the zone (role definition, process, rules)

### Step 6 -- Confirm changes

Present a summary:

```text
Re-specialization complete for [project-name]

Zones updated:
- structure: [changed/unchanged]
- architecture: [changed/unchanged]
- conventions: [changed/unchanged]
- env-vars: [changed/unchanged]

Agents updated: [count] of [total]

Review the changes above. Confirm to commit.
```

### Step 7 -- Commit

Commit all changes as an atomic commit:

```bash
git add CLAUDE.md .claude/agents/*.md
git commit -m "chore: re-specialize via guild-re-specialize"
```

## Important Notes

- NEVER modify content outside of zone markers
- NEVER read real `.env` files -- only `.env.example`
- If a zone's content hasn't changed, skip it (no-op)
- Present diffs before applying changes
- User confirmation is required before committing
