---
name: agent-creator
description: Create or improve a Claude Code subagent definition under `.claude/agents/<name>.md`. Use when the user explicitly invokes `/agent-creator`, asks to "make an agent", "create a subagent", "add a new agent", "improve this agent", "tweak the code-reviewer agent", or otherwise wants to author/edit project-scope agent markdown files (with YAML frontmatter for `name`, `description`, `tools`, `model`). Walks the user through a structured interview (open conversation → AskUserQuestion for name / triggering style / tool allow-list / model), writes the agent file, and optionally runs a triggering test via `scripts/test_agent_trigger.py`.
---

# Agent Creator

A skill for authoring and improving Claude Code **subagents** — the markdown files under `.claude/agents/<name>.md` that define specialized agents launched via the `Task` tool with a `subagent_type` parameter.

This skill is the agent counterpart to `skill-creator`. It only writes to the **project scope** (`.claude/agents/`); user-scope agents (`~/.claude/agents/`) are out of scope.

> Agents vs skills: a **skill** is a workflow Claude itself follows in the main conversation (loaded into context via SKILL.md). An **agent** is a separately-spawned subprocess with its own context, tool allow-list, and model — invoked via the `Task` tool. Use this skill when the user wants to delegate a self-contained task to a fresh sub-context, not to extend the main conversation's behavior.

---

## When to use this skill

Trigger when the user wants to:

- Create a new agent file (`/agent-creator`, "make an agent for X", "I need a subagent that does Y")
- Improve an existing agent (rewrite the body, tighten triggering, change tool allow-list, swap model)
- Bundle an existing prompt-style instruction set into a reusable agent

If the user is asking for a **skill** (something Claude follows inline) rather than an agent (something spawned via `Task`), redirect them to `skill-creator` instead.

---

## High-level flow

```
Phase 1: Capture intent (open conversation)
   ↓
Phase 2: Structured hearing (AskUserQuestion for name / trigger / tools / model)
   ↓
Phase 3: Draft and write `.claude/agents/<name>.md`
   ↓
Phase 4: (Optional) Trigger test via scripts/test_agent_trigger.py
```

Phases 1 and 2 can interleave — if the user already supplied some answers in the opening message, skip the corresponding AskUserQuestion fields. Treat this as a conversation, not a form.

---

## Phase 1: Capture intent

Read the conversation so far. Often the user has already explained what they want — extract:

- **Purpose**: What task should this agent perform end to end?
- **Trigger context**: When should the main session delegate to this agent?
- **Mode**: New agent vs. improvement of an existing one (check `.claude/agents/` for the target file)
- **Inputs/outputs**: What does the agent receive (file paths? a diff? a question?) and what does it return?

Ask only what is genuinely missing. Aim for 1–3 short clarifying questions before moving on.

For improvement mode:

- Read the existing `.claude/agents/<name>.md` first
- Confirm whether the user wants a small body edit (preserve frontmatter) or a wholesale rewrite (frontmatter + body)
- If only the body changes, **do not** alter `name` / `description` / `tools` / `model` unless the user explicitly asks

---

## Phase 2: Structured hearing

Use **AskUserQuestion** for the four fields below. Skip any field already settled in Phase 1. Present all unresolved fields in a single AskUserQuestion call so the user fills them in one screen.

### Field 1: `name`

Kebab-case, lowercase, descriptive of the role (e.g. `terraform-reviewer`, `pr-summarizer`, `migration-dry-runner`). Must match the filename (`<name>.md`) and the `name:` frontmatter exactly. If the user proposes a name that conflicts with an existing file, surface the conflict and ask whether to overwrite or pick a new name.

### Field 2: Triggering style

How aggressively should the main session delegate to this agent? Pick one — this becomes the leading phrase in the `description` field:

| Style | Description prefix | Example |
|-------|-------------------|---------|
| **Explicit only** | "Use when the user asks to …" | One-shot tools the user invokes by name |
| **Proactive** | "Use PROACTIVELY when …" | Reviewers, validators that should fire on relevant changes |
| **Mandatory** | "MUST BE USED for …" | Gatekeepers (security review, code review on every diff) |

The *why* matters: more aggressive phrases (`MUST BE USED`) cause the main agent to spawn this agent more often, which costs tokens and may produce noise. Default to **proactive** unless the user has a specific reason to escalate.

### Field 3: Tool allow-list

Which Claude Code tools should this agent have? Options to offer:

- **Read-only** (`Read`, `Grep`, `Glob`) — for reviewers, analyzers, planners
- **Read + Bash** (`Read`, `Grep`, `Glob`, `Bash`) — when the agent runs scripts/CLIs but doesn't edit files
- **Read + Write/Edit** (`Read`, `Write`, `Edit`, `Grep`, `Glob`) — for code-modifying agents
- **Full** (`Read`, `Write`, `Edit`, `Bash`, `Grep`, `Glob`) — for build/test fixers and end-to-end runners
- **Custom** — user picks from the full tool list

If the user is unsure, default to the **least-privileged** option that covers the agent's job. Read-only is safer and faster. See `references/tools.md` for the complete tool list and allow-list patterns.

### Field 4: Model

Pick one:

- `haiku` — cheap, fast, fine for narrow mechanical agents (lint fix, file pattern detection)
- `sonnet` — balanced default for most reviewers and runners
- `opus` — for agents that need deep reasoning (architecture, security, complex planning)
- *(omit `model` field)* — inherit the parent session's model

Default to `sonnet` if the user has no preference. See `references/frontmatter.md` for the full frontmatter spec.

---

## Phase 3: Draft and write the agent file

### Body structure

A good agent body has:

1. **Role statement** — one sentence: "You are a …"
2. **When invoked / inputs** — what the agent receives
3. **Process / checklist** — numbered or bulleted steps the agent should follow
4. **Output format** — exactly what to return to the caller (the main session)
5. **(Optional) Project-specific guidelines** — anchored to repo conventions
6. **Language section** (always last) — see below

### Required `## Language` section

Every agent in this repo ends with:

```markdown
## Language

- Internal reasoning and thinking should be in English
- **All user-facing output, reports, and summaries must be written in Japanese**
```

This matches the project-wide policy in `.claude/CLAUDE.md`. Do not omit it — the agent runs in its own context and won't inherit the main session's CLAUDE.md awareness automatically.

### Writing principles

- Prefer the imperative form ("Run git diff", "Check for hardcoded secrets") over passive descriptions.
- Explain *why* a step matters when it isn't obvious — agents read their own prompt as instructions, and a well-motivated step is followed more reliably than an unexplained MUST.
- Keep the body under ~150 lines unless the agent genuinely needs a long checklist. Long bodies dilute attention.
- Don't paste large code samples into the body; the agent has Read access and can pull them on demand.
- Avoid duplicating CLAUDE.md content — the agent reads CLAUDE.md when it triggers, so reasserting "use uv, not pip" is redundant.

### Write the file

Use the `Write` tool to create `.claude/agents/<name>.md`. Frontmatter shape:

```yaml
---
name: <kebab-case-name>
description: <triggering style prefix> <what it does, when to use it>
tools: ["Read", "Grep", "Glob"]
model: sonnet
---
```

Notes:

- `tools` is a JSON array of strings; omit the field entirely to grant all tools (rare; almost always specify a subset).
- `model` is optional; omit to inherit the parent's model.
- `description` is the **only** triggering signal the main session uses to decide whether to spawn this agent — write it as if it's the only thing the main agent will read about the agent. See `references/frontmatter.md` for the full description-writing guide.

After writing, show the user the path and the rendered frontmatter, and ask if they want to test triggering (Phase 4) or stop here.

---

## Phase 4: Optional trigger test

After the file exists, ask via **AskUserQuestion** whether the user wants to verify that the description actually causes the main session to spawn the new agent. This is a quick sanity check, not a full eval.

If yes, run:

```bash
uv run python -m scripts.test_agent_trigger \
  --agent-name <name> \
  --queries-file <path-to-test-queries.json> \
  --runs-per-query 3
```

(Or `python -m` if the project doesn't use `uv` for skill scripts.)

The script reads queries shaped like:

```json
[
  {"query": "review my latest commit for security issues", "should_trigger": true},
  {"query": "what time is it in Tokyo?", "should_trigger": false}
]
```

It spawns `claude -p` for each query with the new agent's description visible to the model, watches the stream-json output for a `Task` tool call whose `subagent_type` matches the agent name, and prints a pass/fail rate. See `scripts/test_agent_trigger.py` for full options.

If the agent is under-triggering (should_trigger queries fail), the description is too narrow — make the trigger phrasing more inclusive or escalate to `Use PROACTIVELY`. If it's over-triggering (should_not_trigger queries fail), the description is too broad — add scoping ("only when …") or specific contextual signals.

### Important caveat: `claude -p` rarely spawns agents

`claude -p` is optimized for short, one-shot responses, so the main agent typically chooses to handle a request inline rather than spawning a subagent — even when the description matches perfectly. Empirically, simple queries like "summarize PR #19" cause `claude -p` to run `gh pr view` directly instead of invoking the `pr-summarizer` agent via `Task`.

This means:

- **Low pass rates from `test_agent_trigger.py` are not necessarily a description problem.** The same agent may trigger reliably in an interactive session where the main agent has more context and reason to delegate.
- **Treat the trigger test as a smoke test for description / parsing / file plumbing**, not as a faithful measurement of how often the agent will fire in real use.
- **For a meaningful trigger signal, write longer / multi-step queries** that the main agent has reason to delegate (e.g. "read all commits on the branch, fill the repo's PR template, propose a label, and check if release-tag is needed"). Single-step queries are a poor test of agent triggering specifically because they're a poor *use* of agents.

The most reliable validation is still **using the agent in a real interactive session** and noting whether the main agent delegates appropriately. Description optimization based purely on `test_agent_trigger.py` results risks overfitting to the script's biases.

For a heavier evaluation loop (multiple iterations with description optimization), `skill-creator/scripts/run_loop.py` mechanics transfer cleanly to agents — but the same caveat applies.

---

## Improving an existing agent

The same flow applies, with these adjustments:

1. Read the existing `.claude/agents/<name>.md` first.
2. Show the user the current content and ask what should change.
3. If only the body changes, edit in place with the `Edit` tool — don't `Write` the whole file (it loses unrelated formatting).
4. If frontmatter changes (especially `description`), strongly consider running Phase 4 afterward — description edits are the most common cause of triggering regressions.
5. Snapshot the original to `/tmp/<name>.md.bak` before invasive rewrites so the user can diff.

---

## Reference files

- `references/frontmatter.md` — Full spec for `name` / `description` / `tools` / `model` fields, including writing-good-descriptions guidance.
- `references/tools.md` — Claude Code tool name list and allow-list patterns by agent type.

Read these on demand when filling Phase 2 fields or when the user asks for details.

---

## Common pitfalls

- **Forgetting the `## Language` section.** Every project agent must end with it.
- **Over-broad tool allow-lists.** Granting `Bash` to a read-only reviewer enlarges blast radius for no benefit.
- **Description that names the *implementation* instead of the *trigger*.** "An agent that uses ripgrep to find TODOs" describes the how; "Use PROACTIVELY when the user asks about outstanding TODOs, FIXMEs, or unfinished work in the codebase" describes the when. The latter triggers reliably; the former does not.
- **Re-stating CLAUDE.md inside the agent.** The agent reads the project CLAUDE.md when it spawns. Pasting its rules into every agent body is duplication that goes stale.
- **Mixing up agents and skills.** If the user wants behavior the *main* conversation should follow, that's a skill — redirect to `skill-creator`.

---

## Language

- Internal reasoning and thinking should be in English
- **All user-facing output, reports, and summaries must be written in Japanese**
