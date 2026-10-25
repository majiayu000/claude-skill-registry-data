---
name: agent-creator-claudecode
description: Guide for creating custom subagents for Claude Code (Markdown files in .claude/agents/ or ~/.claude/agents/ with YAML frontmatter). Use this skill whenever a user wants to build, configure, review, or modify a Claude Code agent, choose frontmatter fields (tools, disallowedTools, model, permissionMode, skills, mcpServers, hooks, memory, isolation), or troubleshoot an agent that does not load, is never delegated to, has the wrong tools or model, or ignores a frontmatter field. ALWAYS load this skill before writing or debugging Claude Code agent files.
license: MIT
---

# Claude Code Agent Creator

Claude Code custom agents ("subagents") are Markdown files with YAML frontmatter. The
frontmatter sets identity and capabilities; the body is the agent's system prompt. The same
file can run as a delegated subagent, be @-mentioned, or run as the whole session with
`claude --agent <name>`.

> [!IMPORTANT]
> Claude Code **silently ignores** frontmatter fields it does not recognize, and silently
> **skips** whole files with certain problems. A typo produces no error. Run the bundled
> validator (see [Validate](#step-4-validate)) instead of trusting that a file loaded.

Official docs: <https://code.claude.com/docs/en/sub-agents> · every docs page is also
available as Markdown by appending `.md` to its URL.

---

## When to Use This Skill

- Creating a new Claude Code agent file
- Choosing or fixing frontmatter fields
- Diagnosing an agent that is not found, never auto-delegated, has no tools, runs on the
  wrong model, or whose hooks/MCP servers do not run
- Reviewing an agent file before committing it to a repository

For Claude Code *settings* (permissions, hooks in `settings.json`, MCP config), use
`client-config-claudecode` instead.

---

## Quick Decision Guide

| Need | Approach |
|---|---|
| Isolated context and restricted tools for a side task | **Subagent** (this skill) |
| Reusable instructions loaded into the main conversation | Skill (`SKILL.md`) |
| A different persona for a whole session | Subagent run with `claude --agent <name>` |
| Deterministic action on a lifecycle event | Hook |
| Side task that needs the full conversation so far | Fork (built in, no file; `/subtask <task>`, see `references/tools-reference.md`) |
| One-off or scripted agent, nothing saved to disk | `--agents` JSON flag |

---

## Agent File Format

```markdown
---
name: code-reviewer
description: Reviews code for quality and security. Use proactively after code changes.
tools: Read, Grep, Glob
model: sonnet
---

You are a code reviewer. When invoked, analyze the changes and give specific,
actionable feedback on quality, security, and best practices.
```

Rules that cause silent failures when broken:

1. The opening `---` must be the **first line** of the file.
2. `name` and `description` are the only required fields. A file with no `name` is treated
   as documentation, not an agent.
3. `name` must not start with `-` and must not contain `:` (reserved for plugin-scoped
   names such as `my-plugin:reviewer`).
4. Multi-word field names are **camelCase** and case-sensitive: `disallowedTools`,
   `maxTurns`, `permissionMode`. `disallowed-tools` or `max_turns` is ignored.
5. YAML must parse. One bad indent means no fields are read and the file is skipped.

> [!TIP]
> Load `references/frontmatter-reference.md` for every field, its allowed values, the
> minimum Claude Code version where one applies, and per-scope caveats.

---

## Where Agent Files Live

| Scope | Location | Priority |
|---|---|---|
| Managed (organization) | `.claude/agents/` inside the managed settings directory | 1 (highest) |
| CLI flag | `--agents '<json>'` (session only, not saved) | 2 |
| Project | `.claude/agents/` (found by walking up from the working directory) | 3 |
| User | `~/.claude/agents/` (all projects) | 4 |
| Plugin | `<plugin>/agents/` | 5 (lowest) |

Same `name` in several scopes: the highest priority wins. Nested project directories: the
one closest to the working directory wins. Two files with the same `name` in one directory
tree: only one loads, chosen by filesystem order, so keep names unique.

Claude Code watches `.claude/agents/` and `~/.claude/agents/`, so edits apply within
seconds. **Restart** for the first agent file in a directory that did not exist when the
session started, for anything under an `--add-dir` directory, and under
`--disable-slash-commands`.

---

## Tools

```yaml
tools: Read, Grep, Glob            # allowlist (comma-separated string or YAML list)
disallowedTools: Write, Edit       # denylist, applied first
```

- Omit both: the agent inherits every tool available to subagents, including MCP tools.
- Both set: `disallowedTools` is removed first, then `tools` resolves against what remains.
- MCP: `mcp__github` or `mcp__github__*` selects a whole server; `mcp__*` in
  `disallowedTools` removes all MCP tools.
- `Bash(git push *)` in `disallowedTools` removes **all** of Bash. To block only some
  commands, add a `permissions.deny` rule in settings.
- A `tools` list that resolves to nothing (typo, unavailable tool) makes Claude Code refuse
  to launch the agent with "would be spawned with zero tools".
- Background subagents (the default in interactive sessions) get a reduced built-in tool
  set, so the same file can behave differently in the foreground.
- `Agent(worker, reviewer)` restricts spawnable types **only** when the file runs as the
  main session via `--agent`. Inside a subagent the parenthesized list is ignored.

> [!TIP]
> Load `references/tools-reference.md` for tool names, what is removed from every
> subagent, the background-tool list, and MCP patterns.

Apply least privilege: start read-only (`Read, Grep, Glob`) and add `Edit`, `Write`, or
`Bash` only when the role needs them.

---

## Model

```yaml
model: sonnet          # alias: sonnet | opus | haiku | fable
model: claude-opus-5-5 # full model ID
model: inherit         # main conversation's model
```

Resolution order: per-invocation `model` parameter, then frontmatter `model`, then the
`CLAUDE_CODE_SUBAGENT_MODEL` environment variable, then the main conversation's model.
Setting `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1` overrides the frontmatter for every subagent.
Confirm the model an agent actually got with `/tasks` while it runs.

A family alias (`opus`) resolves to the main conversation's exact model when the two are
the same family, including any `[1m]` context suffix.

---

## Other Fields at a Glance

| Field | Purpose |
|---|---|
| `permissionMode` | `default` (alias `manual`), `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`. The parent session's mode can override it |
| `maxTurns` | Stop after N agentic turns; output is returned marked partial and can be resumed |
| `skills` | Skill names whose full content is preloaded at startup (first 32 distinct names) |
| `mcpServers` | Server names (shared connection) or inline definitions (scoped to this agent) |
| `hooks` | `PreToolUse`, `PostToolUse`, `Stop` (becomes `SubagentStop`) scoped to this agent |
| `memory` | `user`, `project`, or `local` persistent memory directory |
| `background` | `true` always runs it in the background |
| `effort` | `low`, `medium`, `high`, `xhigh`, `max` |
| `isolation` | `worktree` runs it in a temporary git worktree |
| `omitClaudeMd` | `true` skips user, project, and local CLAUDE.md |
| `color` | `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, `cyan` |
| `initialPrompt` | First user turn when the file runs as the main session agent |
| `experimental` | `{cacheTtl: 5m \| 1h}` prompt cache lifetime |
| `autoCompactWindow` | Auto-compact earlier than the main conversation's window: a token count from `100000` to `1000000` (v2.1.296+; `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, when set, wins) |

Plugin agents ignore `hooks`, `mcpServers`, `permissionMode`, and `initialPrompt`. Copy the
file into `.claude/agents/` if you need them.

---

## Writing the `description`

`description` is what Claude reads to decide whether to delegate. State what the agent does
**and when to use it**. Add "use proactively" to encourage automatic delegation. A vague
description means the agent is never chosen; an over-broad one means it is chosen for
unrelated work. Keep it short: combined descriptions of all your agents over 15,000 tokens
trigger a startup warning (every agent still loads). Multi-line descriptions using YAML
folded style (`description: >`) work.

---

## Writing the Prompt Body

The body **replaces** the default Claude Code system prompt for that agent. The agent
receives only this prompt plus environment details (working directory), not the parent
conversation. CLAUDE.md files (and `AGENTS.md` loaded as project instructions) and the git
status still load unless `omitClaudeMd: true`.

Because the agent has no conversation history, write the body so it works from a
delegation prompt alone: define its role, scope, what it must not do, and what it should
return. For principles and anti-patterns, load `references/prompt-writing-guide.md`.

---

## Creating an Agent: Step-by-Step

### Step 1: Plan

1. One sentence for the role.
2. List responsibilities and what it does **not** do.
3. Pick the scope (project for team use, user for personal).
4. Pick the minimum tool set, then the model (cheaper for read-only research, stronger for
   design or review).

### Step 2: Create the File

- Interactively: run `/agents` in Claude Code and choose **Create new agent**, or ask
  Claude to write one.
- Manually: create `.claude/agents/<name>.md` (project) or `~/.claude/agents/<name>.md`
  (user). Prefer lowercase-with-hyphens filenames; the filename does not have to match
  `name`.

### Step 3: Write Frontmatter and Prompt

Start from `references/read-only-agent-example.md` or
`references/worktree-implementer-example.md`, then trim fields you do not need. Fewer
fields means fewer silent-failure surfaces.

### Step 4: Validate

```bash
python scripts/validate-agent.py .claude/agents/my-agent.md
python scripts/validate-agent.py .claude/agents/          # a whole directory
claude plugin validate .claude/agents                    # Claude Code's own YAML check (v2.1.233+)
```

The bundled script (path relative to this skill's directory) needs `pyyaml`. It reports
the silent-skip conditions, unknown or mis-cased fields with a "did you mean" hint, bad
enum values, and fields that are ignored in the chosen scope. `claude plugin validate`
only catches YAML that does not parse and does not flag a missing `name`.

### Step 5: Test

1. Ask for the agent by name, or @-mention it: `@agent-code-reviewer look at auth`.
2. Run `claude --debug` to see load errors that are otherwise silent.
3. Check `/tasks` for the model actually used.
4. Exercise a task the agent should refuse and confirm the tool restrictions hold.

---

## Troubleshooting

Load `references/troubleshooting.md` for the full symptom-to-cause table. The five most
common:

| Symptom | Likely cause |
|---|---|
| Agent not listed at all | Missing `name`, opening `---` not on line 1, `name` starting with `-` or containing `:`, no `description`, or YAML that does not parse |
| Agent listed but a field has no effect | Field name mis-cased or misspelled (silently ignored), or field ignored for plugin agents |
| "would be spawned with zero tools" | Every `tools` entry is misspelled, unavailable to subagents, or removed by `disallowedTools` |
| Never delegated automatically | Vague `description`; add "use proactively" and name the trigger |
| Frontmatter hooks or inline MCP servers do nothing | Project folder not trusted, or the agent is a plugin agent |

---

## Security Considerations

- **Least privilege.** Read-only agents cannot modify files. Use `tools` as an allowlist.
- **`permissionMode: bypassPermissions`** only takes effect if the parent session is
  already in that mode. Never rely on it, and never set it in a shared agent file.
- **Project agents can run code.** Frontmatter `hooks` and inline `mcpServers` from
  `.claude/agents/` load only after the folder is trusted. Review them in any agent file
  you did not write.
- **Hooks do not replace deny rules.** Use `permissions.deny` for hard command blocks.
- **Secrets.** Do not hardcode credentials in `mcpServers`; use environment variables.

---

## Reference Files

| File | When to Load |
|---|---|
| `references/frontmatter-reference.md` | Every field, allowed values, version requirements, `--agents` JSON, plugin restrictions |
| `references/tools-reference.md` | Tool names, removed and background tool sets, MCP patterns, `Agent(type)`, permission modes |
| `references/troubleshooting.md` | Symptom-to-cause tables for load, tool, model, hook, MCP, memory, and delegation problems |
| `references/prompt-writing-guide.md` | Prompt body structure, `description` writing, anti-patterns |
| `references/read-only-agent-example.md` | Minimal read-only reviewer |
| `references/worktree-implementer-example.md` | Implementer with worktree isolation, hooks, memory, preloaded skills |
| `scripts/validate-agent.py` | Frontmatter validator for a file or directory |

---

## Official Documentation

| Resource | URL |
|---|---|
| Create custom subagents | <https://code.claude.com/docs/en/sub-agents> |
| Tools reference | <https://code.claude.com/docs/en/tools-reference> |
| Errors reference | <https://code.claude.com/docs/en/errors> |
| Permission modes | <https://code.claude.com/docs/en/permission-modes> |
| Hooks | <https://code.claude.com/docs/en/hooks> |
| Plugin components (agents) | <https://code.claude.com/docs/en/plugins/components#agents> |
