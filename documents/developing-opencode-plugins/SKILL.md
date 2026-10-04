---
name: developing-opencode-plugins
description: Use when working on OpenCode plugins or skills (creating, modifying, testing, releasing, or maintaining) - provides streamlined workflows, patterns, and reference for the complete OpenCode plugin and skill lifecycle
metadata:
  last_updated: "2026-06-04"
---

# Developing OpenCode Plugins

## Overview

This skill provides efficient workflows for creating OpenCode plugins and skills. OpenCode has two distinct extensibility layers — **skills** (markdown instruction sets) and **plugins** (npm/Bun packages) — and this skill covers both.

## When to Use

Use this skill when:
- Creating a new OpenCode skill from scratch
- Writing an OpenCode plugin (npm/Bun package using `@opencode-ai/plugin`)
- Adding custom commands, agents, or hooks to an OpenCode config
- Troubleshooting skill or plugin loading issues
- Understanding OpenCode's extensibility architecture
- Releasing a skill or plugin (versioning, distribution)

**For comprehensive official documentation**, use the `working-with-opencode` skill to access full docs.

## Quick Reference

| Need to... | Read This |
|-----------|-----------|
| Understand skill format and paths | `references/skill-structure.md` |
| Write skills that trigger reliably | `references/skills-for-opencode.md` |
| Build an npm/Bun plugin | `references/plugin-structure.md` |
| Choose skill vs plugin | `references/common-patterns.md` |
| Debug loading issues | `references/troubleshooting.md` |

## OpenCode Extensibility Model

OpenCode has **two distinct extension mechanisms** — choose based on what you need:

| Layer | Format | When to Use |
|-------|--------|-------------|
| **Skill** | `SKILL.md` markdown + frontmatter | Instruction sets, workflows, domain knowledge |
| **Plugin** | npm/Bun package with `@opencode-ai/plugin` | Tool integrations, database connections, infrastructure |

Most use cases only need skills. Plugins are for connecting external systems.

## Skill Development Workflow

### Phase 1: Plan

1. Define the skill's purpose — what problem does it solve?
2. Choose trigger conditions — when should an agent invoke it?
3. Decide on content structure — quick reference + workflow, or reference library?

### Phase 2: Create Structure

```
.opencode/skills/              # project-level skills
└── my-skill/
    ├── SKILL.md               # required
    └── references/            # optional — referenced from SKILL.md
        └── detailed-guide.md

# OR for a standalone shareable skill:
my-skill/
├── SKILL.md
└── references/
```

### Phase 3: Write SKILL.md

```markdown
---
name: my-skill
description: Use when [specific trigger] — [what it provides]
---

# My Skill

## Overview

What this skill does in 1–2 sentences.

## When to Use

- Scenario A
- Scenario B

## Workflow

[Step-by-step instructions or reference tables]
```

See `references/skills-for-opencode.md` for description writing patterns that trigger reliably.

### Phase 4: Register the Skill

**Project-level** (`.opencode/skills/my-skill/SKILL.md`):
Skills in `.opencode/skills/` are auto-discovered when opencode runs in that directory.

**Global** (`~/.config/opencode/skills/my-skill/SKILL.md`):
Available in every session.

**Via opencode.json** (additional paths or remote URLs):
```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": {
    "paths": ["/path/to/skills-dir"],
    "urls": ["https://example.com/.well-known/skills/"]
  }
}
```

**External auto-loaded paths** (no config needed):
- `~/.agents/skills/<name>/SKILL.md`
- `~/.claude/skills/<name>/SKILL.md`

### Phase 5: Test

Start opencode in the project directory. The skill will be available immediately. Invoke it by name or describe a task that matches its trigger description.

### Phase 6: Release and Distribute

For a shareable skill, host it as a GitHub repo or publish to a skills registry. Users can load it via:
```json
{
  "skills": {
    "urls": ["https://raw.githubusercontent.com/you/your-skill/main/.well-known/skills/"]
  }
}
```

## Plugin Development Workflow (npm/Bun)

Plugins are full npm packages. Use them when you need to integrate external tools, databases, or infrastructure.

### Phase 1: Create Plugin Package

```bash
mkdir my-plugin && cd my-plugin
cat > package.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "type": "module"
}
EOF
bun add @opencode-ai/plugin
```

### Phase 2: Write the Plugin

`plugin.ts`:
```typescript
import type { Plugin } from "@opencode-ai/plugin"

export default function myPlugin({ project, client, $, directory, worktree }) {
  return {
    // Register custom tools, hooks, etc.
  }
}
```

See `references/plugin-structure.md` for the full Plugin API.

### Phase 3: Load the Plugin

**Local plugin** (project-level):
```json
{
  "plugin": ["/absolute/path/to/my-plugin/plugin.ts"]
}
```

**npm package**:
```json
{
  "plugin": ["my-plugin-package-name"]
}
```

OpenCode runs `bun install` automatically for npm packages; cached in `~/.cache/opencode/node_modules/`.

### Phase 4: Test and Iterate

OpenCode hot-reloads plugin changes in dev mode. Start with a minimal plugin and add tools one at a time.

## Custom Commands

Custom commands are markdown files in `.opencode/command/` or `~/.config/opencode/command/`:

```
.opencode/
└── command/
    └── my-command.md   # invoked as /my-command in the TUI
```

`my-command.md`:
```markdown
Summarize the git log since the last tag and draft a changelog entry.
Focus on user-facing changes. Ignore merge commits.
```

See `references/` for live examples from the OpenCode repo itself.

## Agents

Agents are specialized AI personas with focused system prompts:

```
.opencode/
└── agent/
    └── my-agent.md    # the agent's system prompt
```

Reference in `opencode.json`:
```json
{
  "agent": {
    "my-agent": {
      "model": "anthropic/claude-sonnet-4-6",
      "description": "Specialized agent for X"
    }
  }
}
```

## Critical Rules

1. **Skills are markdown** — `SKILL.md` with YAML frontmatter; no code
2. **Plugins are npm/Bun** — TypeScript packages using `@opencode-ai/plugin`
3. **Config is validated strictly** — `opencode.json` fails on unknown keys; always use `$schema`
4. **No hot-reload for config** — restart opencode after changing `opencode.json`
5. **Global config is `~/.config/opencode/`** — NOT `~/.opencode/` (that's legacy)

## Resources in This Skill

- `references/skill-structure.md` — Skill directory layout, SKILL.md format, registration paths
- `references/skills-for-opencode.md` — Description writing, trigger patterns, AGENTS.md
- `references/plugin-structure.md` — Plugin package format, `@opencode-ai/plugin` API
- `references/common-patterns.md` — Skill vs plugin decision matrix, pattern examples
- `references/troubleshooting.md` — Debug guide for loading, trigger, and config issues

## Cross-References

Use the `working-with-opencode` skill for deep dives into:
- `skill-customize-opencode.md` — Full config schema and skill path reference
- `v2-config.md` — opencode.json spec
- `v2-instructions.md` — Session instructions / AGENTS.md format
- `effect-SKILL.md` — Live example skill from the OpenCode repo
- `command-commit.md`, `command-changelog.md` — Live command examples
