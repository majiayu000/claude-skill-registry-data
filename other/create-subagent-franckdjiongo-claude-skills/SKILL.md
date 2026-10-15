---
name: create-subagent
description: Use this skill whenever the user wants to create, scaffold, generate, or define a new subagent (also called "agent" or "agent .md") for Claude Code — anything that produces a file in `.claude/agents/` or `~/.claude/agents/`. Triggers on phrases like "create a subagent", "new agent", "add an agent for X", "scaffold an agent", "make me a code-reviewer agent", "build a migration agent", "spawn an isolated worker for Y", "I need an agent that runs in its own context", "agent .md file", "@agent setup", "user-level agent", "project-level agent", "convert this skill into a subagent", "split this work into a fresh agent", or whenever the user describes a recurring specialist task that should run with its own context window. ALSO triggers when the user says they want to "delegate" something repeatable, when they complain that some workflow is flooding their main context, or when they ask "should this be a skill or a subagent". This skill is DISTINCT from skill-creator — skills teach the *current* context how to do something; subagents *delegate* work to a fresh isolated context and return only a summary. The skill first helps the user pick the right primitive (skill vs subagent vs agent team), then produces a single well-formed `.claude/agents/<name>.md` with Opus 4.7-appropriate frontmatter (`tools`, `model`, `effort`, `memory`, `isolation`, `permissionMode`, `hooks`, `mcpServers`, `skills`), warns when the target is a plugin (plugin agents cannot declare `hooks`, `mcpServers`, or `permissionMode`), and generates concrete smoke-test invocation examples. Do NOT use this skill if the user wants a workflow loaded into the current context (use skill-creator) or a long-running multi-session team (point them at agent teams instead).
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# create-subagent

<!-- runtime-slot:intro -->
Scaffold a single, well-formed Claude Code subagent file with sensible defaults. The skill walks through three phases: **triage** (is a subagent really the right primitive?), **interview** (collect what's needed to choose defaults), and **scaffold** (write the file plus a smoke test).

The goal is one focused file at `.claude/agents/<name>.md` (project) or `~/.claude/agents/<name>.md` (user-global), not a sprawling configuration. Subagents are most useful when small and pointed.
<!-- /runtime-slot:intro -->

## Why this skill exists, separately from skill-creator

<!-- runtime-slot:compare -->
Skills and subagents are sometimes confused because both are markdown files with YAML frontmatter. They aren't the same thing:

| | Skill | Subagent |
|---|---|---|
| Where it runs | The current conversation | A fresh, isolated conversation |
| What returns to the parent | Inline instructions, side effects in this turn | Only the final summary message |
| Context cost on the parent | Body is loaded into the active window when triggered | Near-zero — the work happens elsewhere |
| Best for | Reusable procedures, reference packs, bounded how-tos | Verbose research, isolated review, long-running specialists |
| File location | `.claude/skills/<name>/SKILL.md` | `.claude/agents/<name>.md` |
| Authoring tool | `skill-creator` | this skill |

If the user describes "a way to teach Claude how to do X every time", that's a skill. If they describe "a worker that goes off, does X, and reports back", that's a subagent. If they describe "several agents collaborating across sessions", that's agent teams (out of scope here).
<!-- /runtime-slot:compare -->

## Phase 1 — Triage

Before writing anything, decide what the user actually wants. Ask only the questions you need. Cheap reframings beat scaffolding the wrong artifact.

Use these signals:

<!-- runtime-slot:triage-fit -->
- **Subagent fits when:** the task is self-contained, produces verbose intermediate output, runs read-only research, needs different tool restrictions than the main conversation, or accumulates memory across sessions about a specific concern.
<!-- /runtime-slot:triage-fit -->
- **Skill fits better when:** the user wants procedures that should run *in* the current conversation, the work needs frequent back-and-forth with the parent, or the artifact's main purpose is to teach a workflow.
<!-- runtime-slot:triage-team -->
- **Agent team fits better when:** the user describes multiple workers running in parallel and *talking to each other*, or workers that span separate sessions. Subagents only work within a single session and cannot spawn other subagents.

If subagent is wrong, say so plainly and redirect:
- *"This sounds more like a skill — the work needs to happen in your current conversation. Want me to invoke `skill-creator` instead?"*
- *"This sounds like agent teams — multiple workers coordinating. Read `/agents` and the agent teams docs; this skill only handles single-session subagents."*
<!-- /runtime-slot:triage-team -->

Only proceed once subagent is the right call.

## Phase 2 — Interview

Collect just enough to choose defaults. Pull what you can from conversation context first; ask only what's missing. A short, well-targeted volley beats a long form.

Required:

<!-- runtime-slot:interview-fields -->
1. **Name** — lowercase-hyphenated, e.g. `migrator`, `plugin-reviewer`, `formula-auditor`. If the user proposes spaces, capitals, or underscores, normalize and confirm.
2. **One-paragraph purpose** — what triggers this subagent and what it returns. This becomes the `description` field, which is the *only* signal Claude uses to decide when to delegate. Keyword-dense and explicit beats elegant.
3. **Scope** — project (`.claude/agents/`), user (`~/.claude/agents/`), or part of a plugin. Default to project unless the user clearly wants it across all their projects.

Helpful but not always required (use sensible defaults if the user doesn't care):

4. **What the subagent reads / writes** — drives the `tools` (allowlist) or `disallowedTools` (denylist) decision and the `permissionMode`.
5. **Should it modify the working tree?** — drives `isolation: worktree` vs default.
6. **Does it need to remember things across runs?** — drives `memory: project|user|local`.
7. **Are there skills it should preload?** — drives the `skills` list.
8. **Does it need MCP tools the parent doesn't have?** — drives `mcpServers`.
9. **Does any tool call need conditional validation?** — drives frontmatter `hooks`.
10. **Is latency or cost critical?** — drives `model: haiku` vs `sonnet` vs `inherit`.
<!-- /runtime-slot:interview-fields -->

## Phase 3 — Scaffold

<!-- runtime-slot:scaffold -->
Produce one file at the chosen path with frontmatter, system prompt, and an invocation example. Keep the body short and focused — the subagent receives *only* its system prompt plus environment basics, not Claude Code's full system prompt, so every line earns its place.

### Default choices and why

When the user doesn't specify, prefer these defaults. They reflect the Opus 4.7 reality that subagents under-trigger by default and that small, sharp definitions outperform sprawling ones.

| Field | Default | Reasoning |
|---|---|---|
| `model` | omit (inherits) | Most subagents should match the session model. Override to `haiku` only when the work is genuinely simple and high-volume, or to `sonnet`/`opus` when stronger reasoning is required. |
| `tools` | omit (inherit all) for action agents; explicit allowlist for read-only specialists | Allowlists are the right default for reviewers, auditors, and researchers — they fail safe. Inheritance is the right default for implementers because tool restrictions are fiddly to maintain. |
| `permissionMode` | omit | Inherit from the session. Set `plan` only for explicitly read-only research agents; reach for `bypassPermissions` only with a deliberate reason and a warning to the user. |
| `effort` | omit (inherits) | Override only when the subagent's task is meaningfully harder or easier than the session default. |
| `isolation` | omit | Add `worktree` only when the agent makes file changes that should stay quarantined until the user reviews them (long migrations, risky refactors). |
| `memory` | omit | Add `project` when the agent will accumulate codebase-specific knowledge across runs; `user` when the knowledge generalizes across projects. |
| `color` | omit | Cosmetic. Add only if the user asks. |
| `background` | omit | Default foreground. Set `true` only when the agent is meant to run concurrently and the user explicitly wants that. |
| `disallowedTools` | omit | Reach for this only when the user wants "everything *except* these few" — easier to reason about than enumerating an allowlist. |

### Plugin constraints — warn explicitly

If the user says the agent will ship inside a plugin, warn before writing:

> Plugin-shipped agents **silently ignore** `hooks`, `mcpServers`, and `permissionMode`. If you need any of those, either ship the agent at user/project scope (`.claude/agents/` or `~/.claude/agents/`), or note in the plugin's README that those fields must be added by the consumer after install.

Don't suppress the fields silently — keep them in the file with a comment explaining the constraint, so the user understands what they lose if they install via plugin.

### File template

The minimal valid form:

```markdown
---
name: <kebab-case-name>
description: <one paragraph, keyword-dense, explaining when Claude should delegate to this agent>
---

<system prompt body — what the agent is, when it runs, the workflow it follows, and the report format it returns>
```

Add fields above as needed. For a typical scaffolded read-only researcher:

```markdown
---
name: dataverse-migrator
description: Long-running Dataverse migration specialist. Use proactively when the user asks to migrate, port, or restructure Dataverse tables, columns, relationships, or solution layers. Returns a migration plan plus a status summary; does not push changes without confirmation.
tools: Read, Grep, Glob, Bash
model: inherit
memory: project
isolation: worktree
---

You are a senior Power Platform engineer specializing in Dataverse migrations.

When invoked:
1. Read the current solution structure under `solutions/` and the migration target under `docs/migration/`.
2. Check your memory for prior migration patterns and known gotchas in this codebase.
3. Produce a migration plan: phases, tables touched, breaking changes, rollback notes.
4. Stop and return the plan. Do not execute writes without an explicit go-ahead.

Update your memory after each run with patterns you saw, schemas that surprised you, and anything that should inform the next migration.

Report format:
- **Plan:** numbered phases with one-line rationale each
- **Risks:** bulleted list, severity-tagged
- **Open questions:** what you'd need clarified before executing
```

For canonical templates (read-only researcher, code reviewer, isolated implementer with worktree, hook-validated worker, memory-backed specialist), see `references/templates.md`. For the full frontmatter field reference (defaults, allowed values, plugin constraints), see `references/frontmatter.md`.
<!-- /runtime-slot:scaffold -->

<!-- runtime-slot:body -->
### System-prompt body — what to write

The body becomes the agent's system prompt. Treat it as a focused job description, not a procedures manual.

Include:

- **Identity** — one sentence on what the agent is.
- **Trigger conditions** — when it gets invoked. (Mostly redundant with `description` but reinforces behavior.)
- **Workflow** — numbered steps the agent follows on each invocation.
- **Constraints** — what it must not do (e.g., "do not run `terraform apply` without confirmation").
- **Report format** — exactly what the parent wants back. Subagents return a single message; structuring it improves downstream usefulness.

Avoid:

- Repeating Claude Code's general behavior — the agent already inherits the platform.
- Long lists of tools available — `tools` frontmatter handles that.
- Defensive scaffolding ("double-check before returning"). Opus 4.7 follows literal instructions and will waste tokens on checks that aren't load-bearing. Only include verification steps when they actually matter.
<!-- /runtime-slot:body -->

### Smoke test

<!-- runtime-slot:smoke-test -->
After writing the file, hand the user a concrete invocation that exercises the agent. Three patterns:

1. **Natural language** — Claude decides whether to delegate.
   ```
   Use the <name> subagent to <small task that exercises the workflow>.
   ```
2. **@-mention** — guarantees this specific subagent runs.
   ```
   @"<name> (agent)" <task prompt>
   ```
3. **CLI** — for testing the agent as the main thread.
   ```
   claude --agent <name>
   ```

Pick the smoke test that proves the agent's *typical* invocation works — not its hardest possible task. The point is to confirm the file loads, the description triggers, and the workflow runs end-to-end.

Reminder for the user: subagents authored by editing files directly require restarting the session before they load. Subagents created via `/agents` apply immediately.
<!-- /runtime-slot:smoke-test -->

### Validation checklist before declaring done

<!-- runtime-slot:validation -->
Before telling the user the agent is ready, run through:

- [ ] File exists at the expected path (`.claude/agents/<name>.md` or `~/.claude/agents/<name>.md`).
- [ ] `name` is lowercase-hyphen, unique within scope (check with `ls`).
- [ ] `description` mentions the concrete *triggering phrases* a user would say, not just the agent's identity. Under-triggering is the most common failure mode.
- [ ] If `tools` is set, every listed tool is one Claude Code actually exposes (Read, Edit, Write, Bash, Grep, Glob, MCP tools, `Agent(...)` for spawn restrictions, etc.).
- [ ] If shipped in a plugin: `hooks`, `mcpServers`, `permissionMode` are either absent or accompanied by a comment noting they'll be ignored.
- [ ] System prompt body is under ~80 lines unless complexity truly demands more.
- [ ] Smoke test command was provided to the user.
- [ ] If the user just wrote the file by hand: remind them to restart the Claude Code session.
<!-- /runtime-slot:validation -->

## A note on global vs project scope

<!-- runtime-slot:scope -->
The user's word for "globally" usually means `~/.claude/agents/<name>.md`. That's the right call when the agent's value is the same across every codebase the user opens (e.g., a personal `mac-debug` agent, a `git-historian`, a generic `pdf-extractor`). If the agent's knowledge is codebase-specific (it understands *this* repo's plugin conventions, *this* team's style guide, *this* product's data model), put it in the project at `.claude/agents/` and check it into version control. Global agents shadow project agents when names collide, so don't reuse names across scopes.
<!-- /runtime-slot:scope -->
