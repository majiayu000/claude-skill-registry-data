---
name: agent-creator-opencode
description: Guide for creating custom agents for the OpenCode CLI, V2 (default) and V1. Use this skill whenever a user wants to build, configure, convert, or modify an OpenCode agent — including writing agent Markdown files, configuring agents in opencode.json, setting up permissions, migrating V1 agents to V2, designing primary/subagent workflows, or structuring multi-agent orchestration patterns. ALWAYS load this skill before working on OpenCode agent files.
---

# OpenCode Agent Creator

Custom OpenCode agents combine a system prompt, model, permissions, and display
details into a named assistant profile. They are defined as Markdown files or as
entries in `opencode.json(c)`.

Official docs: V2 <https://opencode.ai/v2/docs/agents/> · V1 <https://opencode.ai/docs/agents/>

---

## Step 0 — Pick the format version

**Native V2 is the default output.** Produce V1 only when:

- The user says they are on OpenCode V1, or
- The existing config or agent files the new agent sits beside are V1-shaped.

Detect the shape from what is already there:

| V1 signals | V2 signals |
|---|---|
| `agent` map, `prompt`, `permission` map, `disable`, `variant`, `temperature`, `top_p`, `maxSteps`, `tools`, `bash` / `task` keys | `agents` map, `system`, `permissions` array of `{action, resource, effect}`, `disabled`, `model: ...#variant`, `request`, `shell` / `subagent` actions |

> [!IMPORTANT]
> Each agent must be **entirely one format**. V2 tolerates V1 and V2 fields side
> by side at the top level of a config file, but it does not infer formats inside
> an individual agent. Never mix `permission` with `permissions`, or `prompt` with
> `system`, in one agent. V1 cannot read native V2 files, so do not convert files
> a V1 install still uses.

If the user asks to convert V1 agents, load `references/v2/migration.md`.

---

## Quick Decision Guide

| Goal | Approach |
|---|---|
| User-selectable main agent | `mode: primary` (V2 default for a new custom agent) |
| Specialist launched by another agent | `mode: subagent` |
| Works both ways | `mode: all` (V1 default when `mode` is omitted) |
| Shared across all projects | `~/.config/opencode/agents/<name>.md` |
| Scoped to one project | `.opencode/agents/<name>.md` |
| Customizing a built-in agent | Config entry with the built-in's ID |

**Always set `mode` explicitly** — the default differs between V1 (`all`) and
V2 (`primary`).

---

## V2 format (default)

Markdown — frontmatter holds the fields, the body is the system prompt:

```markdown
---
description: Reviews code for quality and best practices. Does not modify files.
mode: subagent
model: github-copilot/claude-sonnet-5
permissions:
  # Catch-all deny first: V2 starts from allow-all, so unlisted actions
  # (subagent, skill, web, question, shell) would otherwise stay open.
  - action: "*"
    resource: "*"
    effect: deny
  - action: read
    resource: "*"
    effect: allow
  - action: glob
    resource: "*"
    effect: allow
  - action: grep
    resource: "*"
    effect: allow
  - action: shell
    resource: "git diff *"
    effect: allow
---

You are a code reviewer. Focus on security, performance, and maintainability.
Provide specific, actionable feedback. Do not make changes.
```

JSON/JSONC — under `agents`, with the prompt in `system`:

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "agents": {
    "code-reviewer": {
      "description": "Reviews code for quality and best practices",
      "mode": "subagent",
      "model": "github-copilot/claude-sonnet-5",
      "system": "You are a code reviewer. Do not make changes.",
      "permissions": [
        { "action": "*", "resource": "*", "effect": "deny" },
        { "action": "read", "resource": "*", "effect": "allow" },
        { "action": "glob", "resource": "*", "effect": "allow" },
        { "action": "grep", "resource": "*", "effect": "allow" }
      ]
    }
  }
}
```

V2 essentials (details in `references/v2/`):

- Fields: `description`, `mode`, `model` (`provider/model#variant`), `system`
  (JSON only), `permissions`, `steps`, `hidden`, `color` (six-digit hex),
  `disabled`, `request`.
- `permissions` is an ordered list; **last match wins**; put broad rules first.
  Actions include `read`, `edit` (covers write and patch), `glob`, `grep`,
  `shell`, `subagent`, `skill`, `question`, `webfetch`, `websearch`,
  `external_directory`, and `<server>_<tool>` for MCP tools.
- Per-agent `temperature` / `top_p` / provider options go in `request.body`, but
  V2 **does not send `request` yet**. Use a model variant instead.
- `hidden: true` also removes the agent from the subagent catalog. Do not hide a
  subagent an orchestrator must discover.
- Built-ins: `build`, `plan` (primary); `general`, `explore` (subagent). No
  `scout` in V2.

## V1 format (when required)

```markdown
---
description: Reviews code for quality and best practices. Does not modify files.
mode: subagent
model: anthropic/claude-sonnet-5
temperature: 0.1
permission:
  "*": deny          # default for every tool; specific keys below override it
  read: allow
  glob: allow
  grep: allow
  list: allow
  bash:
    "*": deny
    "git diff*": allow
---

You are a code reviewer. Provide specific, actionable feedback. Do not make changes.
```

V1 JSON uses `agent.<name>` with `prompt` (supports `{file:./path}` relative to
the config file). V1 permission keys are `bash`, `task`, `edit`, and so on, in a
map; `tools` is deprecated. Built-ins: `build`, `plan`, `general`, `explore`,
`scout`. Details in `references/v1/`.

---

## Creating an Agent: Step-by-Step

### Step 1 — Decide version, mode, and scope

- Version: Step 0 above.
- Primary: the main agent for a session. Subagent: runs in a child session,
  launched by another agent (V2 `subagent` tool, V1 Task tool or `@mention`).
- Scope: project `.opencode/agents/` for repo-specific, global
  `~/.config/opencode/agents/` for personal tools. The file name (V2: path
  relative to `agents/`) becomes the agent ID; use lowercase kebab-case.

### Step 2 — Write the prompt

- Open with one sentence stating the agent's role
- List what the agent does and what it does NOT do
- Be specific about output format and behavior constraints
- Aim for under 2000 tokens
- Write a precise `description`; the model uses it to choose subagents

### Step 3 — Configure permissions

- Start restrictive with a catch-all deny (V2: `action: "*"`, `resource: "*"`;
  V1: `"*": deny`), then allow only the actions the role needs. Denying just
  `edit` and `shell` is not restrictive: both formats still allow any action no
  rule mentions, including `subagent` (V1: `task`), `skill`, `question`,
  `webfetch`, and `websearch`
- Use per-command shell rules for surgical control; a V2 pattern ending in
  `" *"` also matches the bare command
- For orchestrators, deny `subagent` (V1: `task`) with `"*"` first, then allow
  specific agent IDs
- Subagents cannot launch subagents at the default nesting depth of one

### Step 4 — Choose the model (required unless told otherwise)

- **Always set an explicit `model`** unless the user asks to omit it and inherit
- Match the model to the role (see `references/models.md`); lighter models for
  cheap subagents, stronger ones for coding, orchestration, and deep reasoning
- **Never auto-select extreme-cost models** (Opus fast mode, Fable, and others
  listed in `references/models.md`) without explicit user cost acceptance
- V2: only add `#variant` if that variant exists for the model; an unknown
  variant is an error

### Step 5 — Create the file

- Markdown: `.opencode/agents/<kebab-case-name>.md`
- Do not add a `system` (V2) or `prompt` (V1) field to Markdown frontmatter; the
  body is the prompt

### Step 6 — Test it

- V2: start OpenCode in the project, confirm the agent is listed and its model
  resolves (`/models`), then ask the primary agent to use the subagent
- V1: `opencode agent create` scaffolds interactively; invoke with `@agent-name`

---

## Prompt Writing Tips

- **Role first**: "You are a database migration specialist."
- **Explicit negatives**: "Do not create files. Do not run migrations automatically."
- **Output format**: Describe what a good response looks like
- **Scope creep prevention**: State what is out of scope
- In V2, project instructions (`AGENTS.md`), skills, and references are still
  added when an agent sets its own prompt, so do not repeat repo rules in the
  agent. V2 reads `AGENTS.md` only, not `CLAUDE.md`

---

## Reference Map (load only what's needed)

Do **not** load every reference up front. Pick by version and task:

| Task | V2 (default) | V1 |
|---|---|---|
| Fields, types, defaults, locations, built-ins | `references/v2/agents.md` | `references/v1/properties.md` |
| Permission rules, actions, defaults, external dirs | `references/v2/permissions.md` | `references/v1/permissions.md` |
| Full working agent templates | `references/v2/examples.md` | `references/v1/examples.md` |
| Converting V1 agents to V2 | `references/v2/migration.md` | — |
| Model IDs, variants, cost gating (both versions) | `references/models.md` | `references/models.md` |
