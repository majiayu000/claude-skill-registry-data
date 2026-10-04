---
name: agent-manager
description: Creates, lists, and removes custom project-specific agents. Custom agents are stored in .claude/crew-agents/ and registered in crew-team.json for routing.
---

# Agent Manager - Custom Agent Creation

Manages project-specific custom agents that extend the built-in CodeCrew team.

## When to Activate

- User runs `/crew agent create|list|remove`

## Storage

Custom agents are stored in `.claude/crew-agents/` (project-local directory, NOT in the plugin's `agents/` directory). This keeps custom agents project-specific and avoids conflicts with plugin updates.

## Subcommands

### `create "name" --model <tier> --description "desc"`

Creates a new custom agent definition.

**Required arguments:**
- `name` — Agent name (alphanumeric + hyphens, e.g., "api-specialist")
- `--model` — Model tier: `sonnet` or `haiku` (Opus reserved for CEO)
- `--description` — What this agent specializes in

**Process:**

1. Validate the name is unique (not already in crew-team.json)
2. Create directory `.claude/crew-agents/` if it doesn't exist
3. Generate the agent file `.claude/crew-agents/{name}.md` using the appropriate template:

**Sonnet agent template:**
```markdown
---
name: crew-{name}
description: {user's description}
model: sonnet
---

You are the **{Name}** at CodeCrew. {user's description}.

## INDEX-FIRST PROTOCOL (MANDATORY)

**INDEX-FIRST**: Read `.claude/crew-index.json` → `crew-symbols.json` → then only specific lines from source files. Never read entire files.

## Your Responsibilities

1. {Edit this section to define specific responsibilities}
2. {Add more as needed}

## Output Format

When done, report:
- What you changed (file paths + summary)
- FILES_MODIFIED: {list}
- Confidence level: high | medium | low
- Any concerns or dependencies
```

**Haiku agent template:**
```markdown
---
name: crew-{name}
description: {user's description}
model: haiku
---

You are the **{Name}** at CodeCrew. {user's description}.

## INDEX-FIRST PROTOCOL (MANDATORY)

**INDEX-FIRST**: Read `.claude/crew-index.json` → `crew-symbols.json` → then only the lines you need. Never read entire files.

## Your Tasks

- {Edit this section to define specific tasks}
- If the task is too complex, report: "ESCALATE: Needs senior-dev"

## Output

FILES_MODIFIED: {list}
CONFIDENCE: {high | medium | low}
```

4. Register the agent in `.claude/crew-team.json`:
```json
"custom-{name}": {
  "model": "{tier}",
  "active": true,
  "role": "{description}",
  "custom": true,
  "definitionPath": ".claude/crew-agents/{name}.md"
}
```

5. Confirm to user:
```
Agent "{name}" created ({tier}) — .claude/crew-agents/{name}.md
Edit definition to customize. Auto-registered in routing.
```

### `list` — List All Agents

1. Read `.claude/crew-team.json`
2. Display all agents (built-in + custom):

```
Agents:

  Built-in:
    ceo (opus)              Active - Triage, decompose, delegate
    vp-engineering (sonnet) Active - Architecture, tech decisions
    ...

  Custom:
    api-specialist (sonnet) Active - Expert in REST API layer
    db-optimizer (haiku)    Active - Database query optimization
```

If no custom agents: "No custom agents. /crew agent create to add one."

### `remove "name"` — Remove a Custom Agent

1. Validate the agent exists in crew-team.json and has `"custom": true`
2. Cannot remove built-in agents — if attempted: "Can't remove built-in agent. Use /crew config to disable."
3. Remove the agent entry from `.claude/crew-team.json`
4. Delete the agent file `.claude/crew-agents/{name}.md`
5. Confirm: `"Custom agent '{name}' removed."`

## Integration with Task Routing

The task-router and lite-router should check `.claude/crew-team.json` for custom agents:

1. When classifying a task, check if any custom agent's description keywords match the task
2. Custom agents can be inserted into routing chains:
   - If `model: haiku` → can replace junior-dev for matching tasks
   - If `model: sonnet` → can replace senior-dev for matching tasks
3. Custom agents follow the same dispatch protocol (Index-First, skill injection, self-contained prompts)

Example: If a custom "api-specialist" agent exists with description "Expert in REST API layer", and the user runs `/crew task "fix the API endpoint for users"`, the router may choose api-specialist over senior-dev since it's more specialized.
