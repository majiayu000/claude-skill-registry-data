---
name: agent-creator-codex
description: Guide for creating custom subagents for OpenAI Codex (standalone TOML files in .codex/agents/ or ~/.codex/agents/, each with name, description, and developer_instructions). Use this skill whenever a user wants to build, configure, review, or modify a Codex agent, choose fields (model, model_reasoning_effort, developer_instructions, and the other keys a role file can actually set), tune the [agents] table in config.toml (concurrency, default subagent model), or troubleshoot a Codex agent that is not found, never spawned, on the wrong model, or unexpectedly writing files or missing MCP servers. ALWAYS load this skill before writing or debugging Codex agent files.
license: MIT
---

# Codex Agent Creator

Codex custom agents ("subagents") are standalone **TOML** files. Each file defines one agent
and is loaded as a configuration layer for the sessions Codex spawns. Unlike Claude Code and
Copilot agents there is no Markdown body: the system prompt is the `developer_instructions`
string inside the TOML.

> [!IMPORTANT]
> A role file customizes the child; it never replaces the parent session's authority.
> Codex applies only a **bounded set** of keys from it (see [What a Role File Can Set](#what-a-role-file-can-set)).
> `sandbox_mode`, `approval_policy`, and `mcp_servers` parse without error but are
> **ignored**. The child runs under the parent session's sandbox, approvals, and MCP servers.
>
> Codex only delegates when asked. It never spawns a subagent on its own initiative unless
> the prompt, an applicable `AGENTS.md`, or a skill requests delegation. An agent file that
> loads correctly can still sit unused. See [Invocation](#invocation).
>
> The official subagents page says the same: `sandbox_mode`, `approval_policy`,
> `model_provider`, and `mcp_servers` in a custom agent file "don't override the parent
> configuration". The Codex source and its tests at `rust-v0.163.0` agree: a role "must not
> control" them. See [What a Role File Can Set](#what-a-role-file-can-set).

Verified against **Codex CLI 0.163.0** (released 2026-10-15, the latest stable release when
this skill was last reviewed).

Official docs: <https://developers.openai.com/codex/subagents> (redirects to
`learn.chatgpt.com/docs/agent-configuration/subagents`). Config keys:
<https://developers.openai.com/codex/config-reference>.

---

## When to Use This Skill

- Creating a new Codex agent file
- Choosing or fixing fields, and knowing which ones Codex actually applies
- Setting spawn limits and defaults in the `[agents]` table of `config.toml`
- Diagnosing an agent that is not found, never delegated to, or running with the wrong model
  or permissions
- Reviewing an agent file before committing it to a repository

For Codex *settings* generally (approvals, profiles, providers, hooks), read the Codex config
reference. For repository-wide instructions, use `AGENTS.md`, not an agent file.

---

## Quick Decision Guide

| Need | Approach |
|---|---|
| Isolated context, narrower tools, or a different model for a side task | **Custom agent** (this skill) |
| Instructions every session in a repo should follow | `AGENTS.md` |
| Reusable procedure the main agent loads on demand | Skill (`SKILL.md`) |
| Parallel work with no custom behavior | Built-in `default`, `worker`, or `explorer` |
| A role defined next to other config in one file | `[agents.<name>]` table in `config.toml` |

---

## Agent File Format

```toml
name = "pr_explorer"
description = "Read-only codebase explorer for evidence gathering. Use before proposing changes."
model = "gpt-6-luna"
model_reasoning_effort = "high"
developer_instructions = """
Stay in exploration mode. Trace real execution paths, cite files and symbols,
and avoid proposing fixes. You never edit files. Prefer fast search over broad scans.
"""
```

Required fields. A file that omits or blanks any of them is **ignored with a warning**, not
rejected loudly (see [Load Failures](#load-failures)):

| Field | Purpose |
|---|---|
| `name` | The identifier Codex uses to spawn or refer to the agent. Authoritative over the filename |
| `description` | Guidance shown when Codex chooses an agent: what it does and when to use it |
| `developer_instructions` | The agent's system-prompt-level instructions. Must not be blank |

Everything else is optional. Load `references/config-reference.md` for the full field list
and the `[agents]` table.

Rules that avoid load failures:

1. Valid TOML. Use `"""` multi-line strings for `developer_instructions`.
2. Keep `name` unique across project and personal scope (files are discovered recursively). Use `snake_case` or `kebab-case`
   consistently and match the filename to it (`pr_explorer.toml`).
3. Top-level keys go **before** any `[table]` header. A key placed after a `[table]` header
   belongs to that table, not to the agent.
4. Field names are `snake_case`, and unknown keys make the whole file invalid. Do not carry
   over `disallowedTools`, `tools`, or `permissionMode`; Codex has no such keys.

---

## What a Role File Can Set

Verified in the Codex source at tag `rust-v0.163.0` (`codex-rs/core/src/agent/role.rs`,
described there as "bounded agent-role overrides"), and by the upstream test
`codex-rs/core/src/agent/role_tests.rs`, which asserts the role layer holds none of
`openai_base_url`, `chatgpt_base_url`, `model_provider`, `approval_policy`, `sandbox_mode`,
`notify`, `apps`, or `mcp_servers`:

| Key | Effect on the spawned agent |
|---|---|
| `developer_instructions` | Replaces the role's instructions |
| `model`, `model_reasoning_effort` | Applied, and locked: the spawn UI tells the model these "cannot be changed" |
| `model_reasoning_summary`, `model_verbosity`, `personality` | Applied |
| `features.<name> = false` | Disables only `shell_tool`, `apps`, `plugins`, `memories` (legacy key `memory_tool`), `request_permissions_tool` |
| `skills.config` entries with `enabled = false`, `skills.bundled.enabled = false`, `skills.include_instructions = false` | Disables inherited skills. Cannot enable anything |

Every other key, including `sandbox_mode`, `approval_policy`, `mcp_servers`, `web_search`,
`features.<name> = true`, and `service_tier`, is dropped. The spawn code applies the root session's
service tier after the role, so a role-file `service_tier` never survives (the official page
says the same: "The service tier also follows the root session's preference"). The file still
loads, so nothing warns you. Configure sandbox, approvals, and MCP servers on the **parent** session or its config.

---

## Where Agent Files Live

| Scope | Location |
|---|---|
| Project | `.codex/agents/` (loaded **only when the project is trusted**) |
| Personal | `~/.codex/agents/` (`$CODEX_HOME/agents/`) |
| Config table | `[agents.<name>]` in `config.toml`, with `config_file` pointing at a TOML layer |

Built-in agents `default`, `worker`, and `explorer` can be overridden by defining a custom
agent with the same name.

> [!NOTE]
> Two files with the same `name` in one directory: Codex warns and drops the duplicate.
> The same `name` in project and personal scope raises no warning, and the winner could not
> be observed without a model call. Keep names unique across scopes.

---

## Model and Reasoning Effort

```toml
model = "gpt-6-luna"
model_reasoning_effort = "high"   # low | medium | high | xhigh | max | ultra (model dependent)
```

Precedence: the role file's `model` and `model_reasoning_effort` are applied **after** the
spawn-time and `[agents]` values, so they win over an explicit spawn value and over
`agents.default_subagent_model` / `agents.default_subagent_reasoning_effort`. Those defaults
only apply to roles that do not set the field. A role file that sets only `model` keeps the
effort already resolved (spawn value, then `[agents]` default, then the parent's, or the
chosen model's default effort when a spawn value or `[agents]` default selected the model
without one), so set `model_reasoning_effort` too when that model does not support the
inherited level. If an agent runs on an unexpected model, the usual causes are a different
role being spawned, the role file failing to load (check the startup warnings), or the model
or effort being rejected by the account.

Valid model names and effort levels depend on the account and Codex build. Run
`codex debug models` to list the catalog and each model's supported effort levels.

---

## Sandbox, Approvals, and MCP

A role file **cannot** set any of these. Codex copies the parent's live runtime policy onto
the child, so:

- The child inherits the parent's sandbox policy, approval mode, and MCP servers.
- `--yolo` and `/permissions` changes on the parent apply to spawned agents.
- `sandbox_mode` in a role file parses (an invalid value still produces a load warning) and
  then has no effect. A "read-only" reviewer is read-only only if the parent session is.
- MCP servers a role needs must be configured in the parent's `config.toml`. List them as a
  prerequisite in the agent's documentation, and name them in `developer_instructions`.
- To keep a role from writing, say so in `developer_instructions` and start the parent
  read-only (`codex --sandbox read-only`). To keep it from running commands at all, set
  `features.shell_tool = false` in the role file.
- In interactive CLI sessions, approval requests from inactive agent threads can surface in
  the main view. Press `o` to inspect the request before approving.

Avoid `danger-full-access` on any parent session that spawns agents you did not write.

---

## Invocation

Codex delegates when one of these is true:

- **Explicit request.** Ask for it: "Spawn one `pr_explorer` per module and summarize."
- **Instruction-based.** An applicable `AGENTS.md` or skill tells Codex to delegate.

In ChatGPT Work (the hosted web surface), Ultra intelligence level can also delegate
proactively. The subagents page says local Codex releases spawn agents only after a direct
request or applicable project or skill instructions.

To make an agent get used, name it in the request or in `AGENTS.md`, and write a
`description` that names the trigger. Good: "Read-only reviewer. Use after any change under
`src/auth/`". Bad: "Helps with code".

Global limits live in `config.toml`:

```toml
[agents]
enabled = true                         # multi-agent tools on/off (default true)
max_concurrent_threads_per_session = 4 # spawned threads, excluding the primary
default_subagent_model = "gpt-6-luna"
default_subagent_reasoning_effort = "medium"
```

`agents.max_threads` is the legacy alias for `max_concurrent_threads_per_session`; the public
config reference lists it. `agents.interrupt_message` (default `true`) controls whether a
model-visible message is recorded when an agent turn is interrupted.
`agents.max_depth` limits nesting for V1 agent threads and is ignored by V2.
`agents.job_max_runtime_seconds` is a removed setting kept as a no-op. Neither of those two
is in the public config reference; both are accepted without error in 0.163.0.

> [!WARNING]
> Under `[agents]`, any key Codex does not know is parsed as a role table. A typo such as
> `max_thread = 3` is a **fatal** startup error (`failed to load bootstrap configuration`,
> caused by ``invalid type: integer `3`, expected struct AgentRoleToml in `agents` ``),
> unlike a bad agent file, which is only skipped.

---

## Writing the Prompt (`developer_instructions`)

The agent sees this text plus whatever the spawn request passes it. It does not see the
parent conversation. Write it so it works from a delegation message alone:

1. **Role** in one sentence.
2. **Scope**: what it reads, what it may change, what it must not touch.
3. **Method**: the steps or checks, in order of importance.
4. **Return format**: exactly what the parent needs back (findings with `path:line`, a diff
   summary, pass/fail).
5. **Stop conditions**: when to return instead of continuing.

Narrow, opinionated agents work best. Split a "does everything" agent into a reader and a
writer. Load `references/agent-examples.md` for complete files.

---

## Creating an Agent: Step-by-Step

### Step 1: Plan

1. One sentence for the role, and what it does **not** do.
2. Scope: project (`.codex/agents/`, committed for the team) or personal (`~/.codex/agents/`).
3. Model and effort (cheaper and lower for read-heavy exploration; stronger for design and
   review), then what the **parent** session must provide: sandbox policy and MCP servers.

### Step 2: Write the File

Create `.codex/agents/<name>.toml`. Start from `references/agent-examples.md` and delete
fields you do not need. Fewer keys means fewer surfaces that can misbehave.

### Step 3: Validate

```bash
python scripts/validate-agent.py .codex/agents/pr_explorer.toml
python scripts/validate-agent.py .codex/agents/          # a whole directory
python scripts/validate-agent.py .codex/agents/ --strict # warnings fail too
```

The bundled script (path relative to this skill's directory) uses only the Python 3.11+
standard library. It checks that the TOML parses, the three required fields are present and
non-blank, keys are known and correctly cased, enum values are valid, and names are unique
and match the filename.

### Step 4: Test

1. Start a new session so the file is picked up. Load warnings print at session start.
   `codex doctor` lists them under `startup warning` without starting a session or calling a
   model (it also exits nonzero when no credentials are found, which is unrelated).
2. Ask for the agent by name: "Use `pr_explorer` to trace how login is handled."
3. Confirm the model and effort it actually got, using the session's agent view.
4. Give it a task it should refuse and confirm both the parent's sandbox and the role's
   instructions hold.

---

## Load Failures

Codex does **not** stop on a bad agent file. It prints
`warning: Ignoring malformed agent role definition: <reason>` and carries on without that
agent, so the agent is simply missing. Verified against codex-cli 0.163.0 with `codex doctor`:

| Defect | Codex message (abridged) |
|---|---|
| TOML syntax error | `failed to parse agent role file at <path>: TOML parse error at line N, column M` |
| Unknown or camelCase key | ``failed to deserialize agent role file at <path>: unknown field `maxTurns` `` |
| `tools = [...]` list | `data did not match any variant of untagged enum WebSearchToolConfigInput` (`tools` is a table in Codex) |
| Bad `sandbox_mode` | ``unknown variant `root`, expected one of `read-only`, `workspace-write`, `danger-full-access` `` |
| Missing `name` | ``agent role file at <path> must define a non-empty `name` `` |
| Missing `description` | ``agent role `x` must define a description`` |
| Missing `developer_instructions` | ``agent role file at <path> must define `developer_instructions` `` |
| Blank `developer_instructions` | ``agent role file at <path>.developer_instructions cannot be blank`` |
| Same `name` twice in one directory | ``duplicate agent role name `x` discovered in <dir>`` |
| `[agents.x].config_file` missing | ``agents.x.config_file must point to an existing file at <path>: No such file or directory`` |

Not checked at load: an unrecognized `model_reasoning_effort` value, and a `name` that differs
from the filename. A project-scope file in an **untrusted** project is skipped without any
warning. Run the validator, then confirm with `codex doctor`.

---

## Troubleshooting

Load `references/troubleshooting.md` for the full symptom-to-cause table. Most common:

| Symptom | Likely cause |
|---|---|
| Agent missing, with a `Ignoring malformed agent role definition` warning at start | Bad TOML, unknown key, or missing or blank `name`, `description`, or `developer_instructions` |
| Project agent missing, no warning | The project is not trusted; project-scope agents load only for trusted projects |
| Agent never spawned | Nothing asked for delegation, or `description` is vague. Name the agent in the request or `AGENTS.md` |
| Wrong model or effort | A different role was spawned, the role file failed to load, or the account rejected the model. The role file outranks spawn values and `[agents]` defaults |
| Agent wrote files despite `sandbox_mode = "read-only"` | Role files cannot set the sandbox; the child uses the parent's policy. Start the parent read-only |
| MCP server missing | `mcp_servers` in a role file is ignored. Configure the server in the parent's `config.toml` |

---

## Security Considerations

- **Least privilege lives on the parent.** Start the parent session read-only unless the task edits. A role file cannot restrict or widen the sandbox.
- **Role files cannot widen authority.** They can only add instructions, pick a model, and
  disable features. Sandbox, approvals, and MCP servers always come from the parent.
- **Project agents are instructions the repository author controls.** They load only in
  trusted projects. Read `developer_instructions` in any agent file you did not write before
  trusting the repository, since the parent's authority is what the agent will use.
- **Secrets.** Keep MCP tokens in the parent config as environment-variable references, never
  in agent files or their instructions.

---

## Reference Files

| File | When to Load |
|---|---|
| `references/config-reference.md` | Every field, allowed values, the `[agents]` table, `[agents.<name>]` roles, resolution order |
| `references/agent-examples.md` | Complete read-only, implementer, and config-table role examples |
| `references/troubleshooting.md` | Symptom-to-cause tables for load, delegation, model, sandbox, and MCP problems |
| `scripts/validate-agent.py` | Validator for a file or directory of Codex agent TOML |

---

## Official Documentation

| Resource | URL |
|---|---|
| Subagents | <https://developers.openai.com/codex/subagents> |
| Config reference | <https://developers.openai.com/codex/config-reference> |
| AGENTS.md | <https://developers.openai.com/codex/guides/agents-md> |
