---
name: writing-skills
description: How to properly create and structure Claude Code skills in this project. Use when adding a new skill, restructuring existing skills, or reviewing skill quality.
---

# Writing Claude Code Skills

How to create properly structured skills for this project.

## Directory structure

Each skill lives in its own directory under `.claude/skills/`:

```
.claude/skills/<skill-name>/SKILL.md
```

- The directory name is the skill's identifier (lowercase, hyphens, max 64 chars)
- The file inside **must** be called `SKILL.md` (uppercase)
- Do NOT use flat `.md` files directly in `.claude/skills/` — they won't be discovered

## Required frontmatter

Every `SKILL.md` must start with YAML frontmatter between `---` markers:

```yaml
---
name: my-skill-name
description: One-line summary of what this skill does and when to use it.
---
```

### Frontmatter fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Recommended | Display name, becomes the `/command`. Falls back to directory name if omitted. |
| `description` | Recommended | What the skill does. Claude uses this to decide when to auto-invoke. |
| `disable-model-invocation` | No | Set `true` to prevent Claude from auto-loading. User must invoke with `/name`. Good for side-effect operations like deploy or review workflows. |
| `user-invocable` | No | Set `false` to hide from the `/` menu. Claude can still use it as background knowledge. Good for reference material. |
| `allowed-tools` | No | Tools Claude can use without permission when this skill is active. |
| `argument-hint` | No | Hint for arguments, e.g., `[issue-number]` or `[filename]`. |
| `context` | No | Set to `fork` to run in a forked subagent context. |
| `agent` | No | Which subagent type to use when `context: fork`. |
| `model` | No | Model to use when this skill is active. |

### String substitutions available in skill content

- `$ARGUMENTS` — All arguments passed when invoking
- `$ARGUMENTS[N]` or `$N` — Specific argument by index
- `${CLAUDE_SESSION_ID}` — Current session ID

## Choosing invocation settings

Pick the right combination based on the skill's purpose:

| Skill type | Settings | Example |
|------------|----------|---------|
| **Task procedure** (user runs it) | Default (both flags omitted) | `schema-implementation` |
| **Manual-only workflow** (side effects, dangerous) | `disable-model-invocation: true` | `pr-review-workflow` |
| **Reference knowledge** (Claude reads as needed) | `user-invocable: false` | `orchestrator-permissions` |
| **Fully automatic** (Claude picks up and uses) | Default | `github-issues-comments` |

## Writing effective content

### Structure

1. Start with a one-line summary of what the skill does
2. Use `## Headings` to break into logical sections
3. For task procedures: use numbered steps (`## Step 1:`, `## Step 2:`)
4. For reference material: use categorized sections with tables
5. Include code examples with language hints in fenced blocks

### Descriptions matter

Claude uses the `description` field to decide when to auto-invoke a skill. Write it well:

- **Good**: `How to create well-formatted GitHub issues and comments without shell escaping problems. Use when creating issues, editing issue bodies, commenting on issues/PRs, or creating pull requests via the gh CLI.`
- **Bad**: `GitHub stuff`

If Claude doesn't use a skill when it should, make the description more specific with trigger keywords. If it triggers too often, narrow the description or add `disable-model-invocation: true`.

### Keep it focused

- One skill per concern — don't combine unrelated topics
- Keep `SKILL.md` under 500 lines
- If you have extensive reference material, put it in supporting files alongside `SKILL.md` and reference them from the main file

### Include what NOT to do

Documenting anti-patterns is as valuable as documenting the correct approach. Use a "What NOT to do" or "Common mistakes" section to capture lessons learned.

## Existing skills in this project

| Skill | Purpose | Invocation |
|-------|---------|------------|
| `schema-implementation` | Procedure for implementing a new schema.org type | User + Claude |
| `pr-review-workflow` | PR review procedure for Copilot agent PRs | Manual only |
| `orchestrator-permissions` | Allowed/blocked Bash commands in orchestrator | Reference only |
| `github-issues-comments` | Creating issues/comments without escaping bugs | User + Claude |
| `journal-entries` | How to write reflective journal entries | Reference only |
| `writing-skills` | This skill — how to write skills | User + Claude |
| `ts-schema-implementation` | Procedure for implementing a TS schema.org type | User + Claude |
| `tool-creation-guidelines` | Best practices for tools that parse/analyze code (AST over regex) | Reference only |
| `orchestrator-prompt-editing` | How to modify the orchestrator system prompt (human-only) | Reference only |
| `model-upgrade` | Checklist for changing the default Copilot agent model | Reference only |

When adding a new skill, update this table.
