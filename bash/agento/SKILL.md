---
name: agento
description: "Use when the user types /agento <command> [args]: routes an Agento command to its skills/agento/commands/<name>.md and runs it inline or through its custom agent."
argument-hint: "<command> [args]"
user-invocable: true
disable-model-invocation: true
---

# Agento command router

Routes `/agento <name> [args]` in every session (Copilot and Local) to the
command file `skills/agento/commands/<name>.md` and runs it inline or through its
custom agent. Follow the steps below in order.

## 1. Parse

The first whitespace token of the arguments is the command name; the rest is the
command's argument, passed on unchanged. With no arguments, list the commands
(step 4) and stop.

## 2. Redirect rule

A name carrying a `.prompt.md`, `.prompt`, or `.md` suffix — or a leading `/` — is
the canonical command written in an old form. Strip the suffix and any leading
`/`, say in one sentence which canonical command it is read as
("Reading `/agento <name>.prompt` as `/agento <name>`."), and proceed without
asking.

## 3. Root discovery

`<agento-root>` is the path in the session context line
`Agento CLI: node <agento-root>/scripts/agento.mjs` when that line is present.
Otherwise it is the `realpath` of this skill's directory, two levels up: the
user-level link `~/.copilot/skills/agento` points at `<clone>/skills/agento`, so
the clone is the real path of the skill directory's parent's parent. Confirm
`<agento-root>/skills/agento/commands/` exists.

## 4. Resolve

Read `<agento-root>/skills/agento/commands/<name>.md`. If it is missing, reply
with the valid names — the basenames of
`<agento-root>/skills/agento/commands/*.md`, each printed as
`/agento <name>` — and stop. Never guess a closest match.

## 5. Dispatch

The command file's `agent:` frontmatter decides how it runs:

| `agent:` | Mode |
| --- | --- |
| missing or `agent` | inline |
| `📋 Agento Planner`, `🏛️ Agento Architect`, `🛠️ Agento Mechanic`, `🤖 Agento Autopilot` | inline, as that agent |
| `🔨 Agento Builder`, `🔍 Agento Reviewer` | subagent |

- **Inline** (missing or `agent`): follow the command file's body as this turn's
  instructions, with the argument as its argument.
- **Inline, as that agent**: first read the agent's `.github/agents/*.agent.md`
  (matched by its `name:`) and follow its body as the operating rules, then the
  command body. Where the agent needs `ask-questions` or `browser` and the tool is
  absent, its §10 fallback applies (numbered questions in chat; headless verify).
- **Subagent**: run `node <agento-root>/scripts/agento.mjs models pins`, take the
  agent's pin (`builder` / `reviewer`), and invoke the agent with the subagent tool
  available — `task` (Copilot) with `copilotModel` as its `model`, or `runSubagent`
  (Local) with `subagentModel` as its `model`, omitting the model when it is `null`
  — passing the command body and the argument. Relay the subagent's final message
  verbatim, including its receipt and result lines and its command blocks.

Whichever mode applies, the dispatched command's §9 receipt line must be printed verbatim as visible text, before any question or other output.

## 6. No own receipt

The router adds no receipt or result line of its own; the dispatched command owns
§9. The router's own outputs are only the redirect sentence and the unknown-name
list.
