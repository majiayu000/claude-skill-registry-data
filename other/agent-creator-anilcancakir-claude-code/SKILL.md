---
name: agent-creator
description: "Create or audit a Claude Code subagent: tools, model and effort, permissions, memory, isolation, and the system-prompt body."
when_to_use: "Use when writing, editing or debugging a subagent definition."
---

# Agent Creator

You are about to write or edit a Claude Code custom subagent another Claude will delegate to. An agent is a markdown file that becomes a named worker the orchestrator can spawn with the Agent tool: the parent fills in `subagent_type`, `prompt`, and optional `description`, `name`, `run_in_background`, `isolation`; Claude Code spawns a fresh isolated context, injects the agent's body as the system prompt, and runs the agent until completion. The agent returns its final message to the parent as the tool result.

This skill is the playbook for designing tool restrictions, choosing model and effort, picking `permissionMode`, adding `memory`, preloading `skills`, structuring the system-prompt body, and routing the storage choice. Target is Opus 5.5. Same patterns work for Sonnet 5.5 at lower cost and for Haiku 4.5, which supports no effort parameter.

## Three jobs, not one

Writing a custom subagent splits into three tasks. Conflating them is the most common authoring mistake.

1. **Surrounding skill shape.** File location, scope, naming, frontmatter parsing. Same rules as any markdown config. Route through `ac:skill-creator` for the broader file-shape decisions (scope, name validation, char budget).
2. **Agent-specific shape.** Tool allowlist/denylist, model and effort, `permissionMode`, `memory`, `skills:` preload, `isolation`, `background`. This file teaches that.
3. **System-prompt body content.** The markdown the orchestrator injects as the agent's system. This is a prompt. Route through `ac:prompt-writer` (architecture, snippets, anti-patterns, Opus 5 tuning) for the body, and apply the five-section pattern from `${CLAUDE_SKILL_DIR}/references/system-prompt-structure.md` for the shape.

A great agent body inside the wrong shape (wrong tools, wrong model, wrong permission mode) returns useless work. A modest body inside the right shape returns sharp results every time.

## What an agent actually is, mechanically

Source of truth: `tools/AgentTool/loadAgentsDir.ts`, `tools/AgentTool/builtInAgents.ts`, `tools/AgentTool/built-in/<name>.ts`, `utils/plugins/loadPluginAgents.ts`, `tools/AgentTool/prompt.ts` in the CC source.

The lifecycle:

1. **Discovery.** At session start, the loader walks managed > `--agents` CLI flag > `.claude/agents/` (project, walks up from cwd) > `~/.claude/agents/` (user) > `<plugin>/agents/` > built-in. Higher-priority definitions override lower ones with the same name (`tools/AgentTool/loadAgentsDir.ts:200-220`, agents in later groups overwrite earlier in the map). Directories added with `--add-dir` are NOT scanned for agents; only file access is granted there. To share an agent across projects, use `~/.claude/agents/` or ship it via a plugin. SDK callers can disable all built-ins by setting `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1` in non-interactive mode.
2. **Parsing.** Each file's YAML frontmatter is parsed; the markdown body becomes the agent's system prompt. Plugin agents auto-namespace as `<plugin>:<agent-name>`.
3. **Listing.** Built-in plus active custom agents are summarized in the orchestrator's `Agent` tool description: `- {agentType}: {whenToUse} (Tools: {toolsDescription})`. The orchestrator decides delegation based on these lines.
4. **Spawn.** Orchestrator calls `Agent({subagent_type, prompt, ...})`. Claude Code creates a fresh isolated context, applies the agent's tool restrictions, model, effort, permission mode, hooks, and any preloaded skills.
5. **Substitution (plugin agents only).** `&#36;{CLAUDE_PLUGIN_ROOT}` and `&#36;{user_config.X}` are substituted in the system prompt for plugin agents. Non-plugin agents get no substitution; the body is injected verbatim.
6. **Execution.** The agent runs as its own LLM loop. It receives the agent's body as system, the parent's `prompt` as the first user turn. CLAUDE.md is auto-loaded into its context unless the definition sets `omitClaudeMd: true` (user and plugin frontmatter since Claude Code 2.1.271; managed instructions still load). It saves the hierarchy's tokens on read-only agents that need no commit, PR or lint rules, and it drops every project rule the agent would inherit, so the body has to carry any it still needs. A subagent CAN spawn other subagents when `Agent` is in its tool set, which it is whenever the definition uses a `disallowedTools` denylist rather than a `tools:` allowlist. Decide that per agent; `references/tool-restrictions.md` carries the measurement and the two ways to deny it.
7. **Return.** The agent's final assistant message returns to the parent as the `Agent` tool result. Intermediate tool calls and reasoning stay in the agent's context, not the parent's.

The parent never sees the agent's tool calls or scratch work; only the final summary. This is the central value: context isolation.

## Decision flow

Route by the user's request.

```
Is a custom subagent the right tool at all?
├── Built-in (Explore / Plan / general-purpose) already fits → use it. Not a custom agent. (on an `/ac:install` setup Explore and Plan are disabled; use `ac:explore` or `general-purpose`)
├── Repeatable workflow, no isolation needed → SKILL (route through `ac:skill-creator`).
├── User-typed `/name [args]` action → COMMAND (route through `ac:command-creator`).
├── Always-on enforcement → HOOK (route through `update-config`).
├── Single fact, not behavior → CLAUDE.md (route through `ac:claude-md-rules-creator`).
└── Recurring task that benefits from isolated context, custom tools, or distinct model → AGENT, continue.

Where does the agent live?
├── Project-scoped → `.claude/agents/<name>.md` (commit to share with team)
├── Personal cross-project → `~/.claude/agents/<name>.md`
├── Plugin-distributed → `<plugin>/agents/<name>.md` (auto-namespaced `<plugin>:<name>`)
├── Org-wide enforced → managed dir
└── One-off (no persistence) → `--agents` JSON flag

Is this an audit or fix of an existing agent?
├── YES → `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` first, then specific reference as needed.
└── NO  → walk the Workflow below.
```

For everything outside agent-specific concerns (file naming, char budget, generic frontmatter parsing), defer to `ac:skill-creator` rather than duplicating that material here.

## Frontmatter: minimal by default

A working agent needs only `name` + `description`. Everything else is opt-in.

> **Escape convention used in this documentation.** This SKILL.md is itself a skill body inside a plugin. The Claude Code loader substitutes the plugin-root token, the skill-directory token, the session-id token, and the full-arguments token on every invocation. To document those tokens without corrupting the docs, this file uses the HTML entity `&#36;` standing in for the dollar sign whenever a token name is being NAMED rather than USED. Real path references (the skill-directory token followed by a slash and a relative path) stay literal so the loader resolves them to actual files the model can Read. In your own agent body, agents do NOT support full-arguments substitution or shell injection (only the plugin-context tokens). For plugin agents, write a plain dollar sign for `&#36;{CLAUDE_PLUGIN_ROOT}` and `&#36;{user_config.X}`. Non-plugin agents get no substitution at all; every token stays literal.

| Field | Required? | When to set |
|-------|-----------|-------------|
| `name` | yes | always; lowercase letters and hyphens, unique within scope |
| `description` | yes | always; this is the trigger surface the orchestrator reads to decide delegation |
| `tools` | optional | the agent should use only a specific subset of tools (allowlist). Omit to inherit every tool. Comma-separated string or YAML list. |
| `disallowedTools` | optional | the agent should inherit most tools but be denied a few (denylist). Applied first, then `tools` filters the remainder. |
| `model` | optional | the agent needs a specific model (`sonnet`/`opus`/`haiku`, full ID like `claude-opus-5`, or `inherit`). Default: `inherit`. |
| `effort` | optional | the agent needs a different reasoning budget than the session (`low`/`medium`/`high`/`xhigh`/`max`). Omit for a Haiku 4.5 agent; that model does not support the parameter. |
| `permissionMode` | optional, NON-PLUGIN ONLY | the agent should run with a specific permission mode (`default`/`acceptEdits`/`auto`/`dontAsk`/`bypassPermissions`/`plan`). Ignored in plugin agents. |
| `maxTurns` | optional | the agent should stop after N agentic turns. Positive integer. |
| `skills` | optional | named skills to preload into the agent's context at startup (full content injected, not just made available). |
| `mcpServers` | optional, NON-PLUGIN ONLY | MCP servers scoped to this agent. Inline definitions or names of already-configured servers. Ignored in plugin agents. |
| `hooks` | optional, NON-PLUGIN ONLY | lifecycle hooks scoped to the agent. Same shape as project hooks. Ignored in plugin agents. |
| `memory` | optional | persistent memory scope (`user`/`project`/`local`). Creates a directory the agent reads and updates across runs. Auto-injects Read/Write/Edit tools. |
| `background` | optional | `true` to always spawn this agent in the background by default. |
| `isolation` | optional | `worktree` to spawn the agent in a temporary git worktree, isolated from the main checkout. |
| `color` | optional | display color in the task list (`red`/`blue`/`green`/`yellow`/`purple`/`orange`/`pink`/`cyan`). |
| `initialPrompt` | optional, MAIN-AGENT MODE | first user turn auto-prepended when this agent runs as the main session via `--agent`. |
| `requiredMcpServers` | optional | array of MCP server name patterns that must be configured for the agent to appear in the listing. Per `loadAgentsDir.ts:233-242`, agents missing required servers are filtered out (case-insensitive substring match). |

Anti-pattern: copying every optional field "just in case". Each unused field adds noise. A focused research agent usually needs just `name` + `description` + `tools` + `model`. A reviewer that updates a knowledge base adds `memory:`. Reach further only for specific needs.

**Plugin-agent security boundary**: per `utils/plugins/loadPluginAgents.ts:161-168`, plugin agents silently ignore `permissionMode`, `hooks`, and `mcpServers`. If your agent needs those, ship it as a user/project agent under `.claude/agents/`, not via a plugin. Plugins are third-party marketplace code; install-time trust boundaries cover plugin-level hooks/MCP, but per-agent escalation through a buried agent file is not allowed.

## Tool access

Three patterns cover almost every case. Detail and copy-paste templates: `${CLAUDE_SKILL_DIR}/references/tool-restrictions.md`.

### Allowlist (most restrictive, recommended for focused agents)

```yaml
tools: Read, Grep, Glob, Bash
```

Agent can only use the listed tools. Default for read-only research agents.

### Denylist (start broad, subtract dangerous tools)

```yaml
disallowedTools: Write, Edit, NotebookEdit
```

Agent inherits every tool the parent has, minus the denied set. Useful for "do anything except touch files".

### Both (rare, when you need allowlist plus exclusions)

When both are set, `disallowedTools` is applied first to the inherited pool, then `tools` filters that pool. Tools listed in both are removed.

### Restricting subagent spawning

The Agent tool is itself a tool, and it reaches subagents too: an agent declaring only a `disallowedTools` denylist inherits `Agent` and will spawn children on an Opus-tier model. So this matters for main-thread agents run via `claude --agent <name>` AND for every subagent you write. See `references/tool-restrictions.md` for the measurement:

```yaml
tools: Agent(worker, researcher), Read, Bash
```

`Agent(x, y)` is an allowlist: only `worker` and `researcher` types can be spawned. To allow any: `Agent` without parentheses. To block all spawning: omit `Agent` from `tools`.

## Model and effort

```yaml
model: sonnet      # or opus, haiku, <full-model-id>, inherit
effort: high       # or low, medium, xhigh, max
```

Defaults: `model: inherit` (same as parent), no effort override.

Picking:

- **Haiku**: fast and cheap. Right for read-only search agents, classification, lookup. Built-in Explore uses Haiku (external builds). Note it supports no `effort` value, so do not pair `model: haiku` with `effort:`.
- **Sonnet**: balanced. Right for code review, analysis, anything intelligence-sensitive but bounded.
- **Opus**: deep reasoning. Right for architecture review, multi-file refactors, adversarial review (challenger pattern).
- **Inherit**: when the agent's quality should track the session's model choice.

Set `effort: high` only for agents that do deep work in one shot (a `plan-deep-review` agent, a `feasibility` analyst). Most agents inherit fine.

## Permission mode

Non-plugin agents can set `permissionMode`. Plugin agents ignore the field.

| Mode | Behavior |
|------|----------|
| `default` | Standard prompts for new permissions |
| `acceptEdits` | Auto-accept file edits and common filesystem commands in working dirs |
| `auto` | Background classifier reviews each command |
| `dontAsk` | Auto-deny new prompts; only pre-approved tools work |
| `bypassPermissions` | Skip prompts entirely; CC still protects `.git`, `.claude`, `.vscode`, `.idea`, `.husky` |
| `plan` | Read-only exploration mode |

Parent precedence rule: if the parent session uses `bypassPermissions` or `acceptEdits`, that takes precedence and the agent cannot downgrade. If the parent uses `auto`, the agent's `permissionMode` is ignored entirely and the classifier evaluates the agent's calls.

For most agents, leave `permissionMode` unset and rely on `tools`/`disallowedTools` to constrain capability. Reach for permission mode only when the agent should run with looser-than-default automation (`acceptEdits` for an autonomous-edit agent the user trusted at install time, `dontAsk` for a strict read-only researcher).

## Memory, skills preload, isolation

Detail: `${CLAUDE_SKILL_DIR}/references/memory-and-skills.md`.

### Persistent memory

```yaml
memory: project    # or user, local
```

Creates a directory the agent reads at startup and writes to during work:

- `user` -> `~/.claude/agent-memory/<name>/`
- `project` -> `.claude/agent-memory/<name>/` (commit to share)
- `local` -> `.claude/agent-memory-local/<name>/` (gitignored by default)

When memory is enabled:

- Read, Write, Edit are auto-injected into the agent's tool list if those were missing.
- The first 200 lines (or 25KB) of `MEMORY.md` in the memory directory is added to the agent's system prompt.
- The body should include explicit instructions to update memory ("save what you learned to your memory after the task").

Memory makes the agent stateful across runs. Use for code-reviewers, debuggers, domain analysts that benefit from accumulated knowledge.

### Skill preloading

```yaml
skills:
  - api-conventions
  - error-handling-patterns
```

The full content of each named skill is injected into the agent's system context at startup. The agent gets the skill's body, not just the option to invoke it. Subagents do NOT inherit skills from the parent conversation; you must list every skill the agent needs.

Cannot preload skills with `disable-model-invocation: true` (security: those skills opted out of programmatic invocation).

### Worktree isolation

```yaml
isolation: worktree
```

Agent runs in a temporary git worktree, isolated from the main checkout. The worktree is auto-cleaned if the agent makes no changes; if it changes files, the worktree path and branch are returned in the tool result.

Use for agents that should not touch the main checkout, or for parallel agents that need separate working copies.

## System-prompt body

The body is the agent's system prompt. Treat it like any other system prompt and route through `ac:prompt-writer` for principles.

Skill-creator's standing body conventions all apply: persona at the top, static rules before dynamic, XML tags when needed, no aggressive caps (state the rule plain and explain the why), positive instructions over negative-only.

The single most useful agent-body convention is the **five-section format** (extracted from the prior `ac` MVP's 15 agents, applies to almost every focused agent):

```markdown
## Identity

One or two sentences describing who the agent is and what it returns. Anchors the lens.

## Execution

Numbered steps the agent follows. Reads first, then acts. Sub-numbers for parallel steps.

## Output Format

Exact markdown shape the agent returns. Locked headers, citation format, length cap. The orchestrator parses this; commit to one shape.

## Failure Conditions

What makes the response BAD. "FAILED if: <list of quality-gate violations>." The agent self-checks against these before returning.

## Constraints

Hard rules. Scope limits. Tool restrictions explicit again ("Read-only, no Write or Edit"). Evidence requirements.
```

Detail and three worked structures (read-only researcher, code reviewer, action-taking debugger): `${CLAUDE_SKILL_DIR}/references/system-prompt-structure.md`.

## Plugin paths and substitutions

Plugin agents get one substitution pass before the system prompt is injected (`utils/plugins/loadPluginAgents.ts:113-123`):

- `&#36;{CLAUDE_PLUGIN_ROOT}` resolves to the plugin's root directory. Use this when a plugin agent needs to reference bundled files: `Read &#36;{CLAUDE_PLUGIN_ROOT}/templates/foo.md`.
- `&#36;{user_config.X}` resolves to the value of the `X` key in the plugin's `userConfig` (sensitive keys resolve to a placeholder).

Non-plugin agents (`.claude/agents/`, `~/.claude/agents/`) get NO substitution. Tokens stay literal in the system prompt.

Agents do NOT support `&#36;ARGUMENTS` or `&#36;{CLAUDE_SKILL_DIR}` (those are skill and command tokens). Agents also do NOT support shell injection (`` \!`<cmd>` ``); the agent system prompt is injected verbatim after the plugin substitution pass.

## Workflow

Walk these in order. Each step assumes the previous resolved.

### 1. Capture intent

Always-needed questions:

- What does the agent do, in one sentence?
- Is it read-only or does it modify files?
- What model and effort fit?
- Project, user, or plugin scope?

Conditional questions (ask only when intent surfaces a need):

- Tool restrictions? Ask if the agent should be constrained (read-only researcher, no-network, no-MCP).
- Memory? Ask if the agent benefits from accumulated knowledge across runs.
- Preloaded skills? Ask if there are domain-specific skill bodies the agent should start with.
- Permission mode? Ask only if the parent's default mode is wrong for this agent's role.
- Worktree isolation? Ask if the agent should not touch the main checkout.

Do not pre-ask about every optional field; pull each in only when intent makes it relevant.

### 2. Pick scope

`.claude/agents/` for team-shared agents in a repo. `~/.claude/agents/` for cross-project personal agents. `<plugin>/agents/` for distribution. `--agents` JSON flag for one-off testing.

### 3. Draft the frontmatter

Minimal:

```yaml
---
name: <kebab-case-name>
description: <Role noun. Use this when <situation>. Returns <shape>.>
---
```

Add fields only when the conditional questions surfaced a reason. The "Frontmatter: minimal by default" table above lists each field with its trigger condition.

`description` is the trigger surface; the orchestrator decides whether to delegate based on this line alone. Write it the way Claude Code writes its built-in agents: a role noun, one "Use this when..." sentence, then what it returns ("Software architect agent for designing implementation plans. Use this when you need to plan the implementation strategy for a task. Returns step-by-step plans..."). About 200 characters: leave mechanics to the body but name the knob a caller sets in the brief (the built-in Explore names its breadth levels). An agent only a skill or command spawns ends with "Spawned only by <caller>; not for general tasks." so the main thread does not pick it up directly. Skip "use proactively": on Opus 5.5 the Agent tool description already reads "Reach for this when the task matches an available agent type".

### 4. Write the body

Five-section pattern (above) unless the agent is genuinely trivial. For each section, name the **success criterion**: how does the agent know it has fulfilled this section? The Output Format section is locked; the orchestrator parses the agent's response and downstream work fails if shape drifts.

Hand off the prompt-writing details to `/ac:prompt-writer` after picking the shape.

### 5. Verify

Before shipping:

1. **Frontmatter parses.** `name` is lowercase + hyphens, `description` is a string, `tools`/`disallowedTools` use the right format.
2. **Triggering reads cleanly.** Read `description` aloud. Would the orchestrator know when to delegate to this agent based on this line?
3. **Tool restrictions match the body.** If the body says "Read-only research", `tools` is an allowlist excluding Write/Edit. If the body uses Bash for git status, `Bash` is in `tools`.
4. **Output Format is parseable.** The shape the agent returns is consistent enough that the parent can act on it without follow-up questions.
5. **Test invocation.** Have the orchestrator delegate to the agent in a fresh session with a typical request. Does the agent return the expected shape?

Worked examples that pass all gates: `${CLAUDE_SKILL_DIR}/references/examples.md`.

### 6. Iterate

| Symptom | Fix |
|---------|-----|
| Orchestrator never delegates | Name the situation more exactly in the "Use this when" sentence, or name the agent in CLAUDE.md for the work it owns |
| Orchestrator delegates too aggressively | Tighten `description`: remove broad keywords; specify when NOT to use |
| Agent does the wrong thing | Strengthen the body: clearer Identity, explicit steps, lock the Output Format |
| Agent writes files when it should not | Add `disallowedTools: Write, Edit, NotebookEdit` (or use `tools:` allowlist) |
| Agent times out / runs forever | Set `maxTurns` (positive integer) |
| Agent forgets context across runs | Add `memory: project` (or user/local) and instruct the body to update it |
| Agent re-discovers known patterns every time | Preload domain skills via `skills:` field |
| Agent prompts user repeatedly during run | Adjust `permissionMode` to `acceptEdits` or `dontAsk` (non-plugin only) |
| Spawning agents from within an agent fails | The agent's `tools:` allowlist omits `Agent`, or its `disallowedTools` denies it. Add `Agent` to the allowlist if nesting is wanted and budgeted; otherwise keep it out and have the parent orchestrate |

Deeper symptom-to-fix mapping: `${CLAUDE_SKILL_DIR}/references/anti-patterns.md`.

## Sibling skills (route the surrounding shape)

| Producing | Route shape through | Use this skill for |
|---|---|---|
| The surrounding file-shape (scope, name, char budget) | `ac:skill-creator` | Agent-specific concerns (tools, model, memory, body structure) |
| The system-prompt body itself | `ac:prompt-writer` | The five-section pattern and per-section guidance (this file) |
| A slash command that delegates to an agent | `ac:command-creator` | Whether to write a custom agent at all (vs a forked-skill command) |
| CLAUDE.md or `.claude/rules/<topic>.md` | `ac:claude-md-rules-creator` | Whether the work should be persistent context vs an isolated agent |
| Hook configuration | `update-config` | Whether the work should be deterministic enforcement vs an agent's negotiated behavior |

When the user request implies any of the rows above, do both: invoke the matching creator for shape, and keep this skill loaded for what is still agent-shaped.

## Built-in agents to know

Read `${CLAUDE_SKILL_DIR}/references/builtin-catalog.md` for full details. Quick reference:

- **Explore** (Haiku, read-only), file search and codebase analysis. Built-in tools-restriction pattern to copy.
- **Plan** (inherit, read-only), software architect for implementation plans. Plan-mode delegation target.
- **general-purpose** (inherit, all tools), multi-step research and modification. Default for fork mode.
- **claude-code-guide** (Haiku, web-fetch + read), answers user questions about CC, Agent SDK, and Claude API.
- **statusline-setup** (Sonnet), configures status line.
- **verification** (feature-flagged), runtime observation pattern.

When designing a custom agent, check whether a built-in already fits. If yes, use it.

## Quick template

Full annotated blank template: `${CLAUDE_SKILL_DIR}/assets/AGENT.template.md`.

Minimal form (covers most agents):

```markdown
---
name: <kebab-case-name>
description: <Role noun. Use this when <situation>. Returns <shape>.>
model: <sonnet | haiku | opus | inherit>
---

## Identity
<One or two sentences: who the agent is and what it returns.>

## Execution
1. <Step 1: read first>
2. <Step 2: act precisely>
3. <Step 3: verify>

## Output Format
<Locked markdown shape with citations / verdict / length cap.>

## Failure Conditions
FAILED if: <list of quality-gate violations the agent self-checks against>.

## Constraints
<Hard rules. Scope limits. Evidence requirements.>
```

## Pre-flight checklist

Always check:

- [ ] File at the right scope (managed / project / user / plugin).
- [ ] Filename = agent name (lowercase, hyphens, max 64 characters, no `claude` or `anthropic`).
- [ ] Frontmatter has `name` and `description`. Other fields only when the agent needs them.
- [ ] `description` is a role noun, one "Use this when" sentence and what it returns, about 200 characters.
- [ ] No cargo-culted optional fields (each present field has a specific reason).

Check only the items that apply to the agent's specific shape:

- [ ] (If `tools:` is set) it lists the tools the body actually uses (allowlist).
- [ ] (If `disallowedTools:` is set) it lists the tools the body avoids (denylist).
- [ ] (If `model:` is set) the choice matches the agent's complexity tier.
- [ ] (If `memory:` is set) the body includes instructions to update memory after the task.
- [ ] (If `skills:` is set) all listed skills exist and have `disable-model-invocation: false`.
- [ ] (If `permissionMode:` is set) the agent is NOT a plugin agent (plugins ignore it).
- [ ] (If `hooks:` or `mcpServers:` is set) the agent is NOT a plugin agent.
- [ ] (If `isolation: worktree`) the agent's work makes sense in an isolated checkout.
- [ ] Body uses the five-section pattern (Identity / Execution / Output Format / Failure Conditions / Constraints).
- [ ] Output Format is locked: the orchestrator can parse the agent's return without follow-up questions.
- [ ] Body passes the `ac:prompt-writer` audit: no aggressive caps unless safety-critical, positive instructions, explained why.
- [ ] Test invocation in a fresh session: orchestrator delegates correctly, agent returns the right shape.

## References

| File | Load when... |
|---|---|
| `${CLAUDE_SKILL_DIR}/references/frontmatter.md` | Designing or auditing frontmatter: every field, valid values, plugin-agent restrictions. |
| `${CLAUDE_SKILL_DIR}/references/system-prompt-structure.md` | Writing the body: the five-section pattern in depth, per-section guidance, three worked structures. |
| `${CLAUDE_SKILL_DIR}/references/tool-restrictions.md` | Choosing tool allowlist/denylist; `Agent(x, y)` patterns; conditional Bash via PreToolUse hooks. |
| `${CLAUDE_SKILL_DIR}/references/memory-and-skills.md` | Setting up persistent memory or preloading skills; auto-injected tools, MEMORY.md format. |
| `${CLAUDE_SKILL_DIR}/references/builtin-catalog.md` | Case studies from built-in agents (Explore, Plan, general-purpose, claude-code-guide). |
| `${CLAUDE_SKILL_DIR}/references/examples.md` | Five worked agents at different complexity tiers, ready to copy and adapt. |
| `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` | Diagnosing a misbehaving agent or auditing one before shipping. |
| `${CLAUDE_SKILL_DIR}/assets/AGENT.template.md` | Starting a new agent from a blank annotated template. |

For surrounding skill shape, invoke `/ac:skill-creator`. For the prompt body itself, invoke `/ac:prompt-writer`. Sibling-skill files cannot be read by path from here, since the install layout is unknown at author time; invocation is the portable form.

Canonical Anthropic documentation, served as raw markdown by appending `.md` to the URL:

- Subagents: `https://code.claude.com/docs/en/sub-agents.md`
- Skills (for the `skills:` preload field): `https://code.claude.com/docs/en/skills.md`
- Plugins (for plugin-agent restrictions and the plugin-root substitution): `https://code.claude.com/docs/en/plugins.md`
- Permission modes: `https://code.claude.com/docs/en/permission-modes.md`
- Hooks: `https://code.claude.com/docs/en/hooks.md`

When canonical docs conflict with observed CLI behavior, trust the live binary.
