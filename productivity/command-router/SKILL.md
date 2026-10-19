---
name: command-router
description: Codex pseudo-command router for Maigo. Use when the user sends or discusses any `/maigo:*` or `maigo:*` command, including go, team, quick, review, board, remember, memory, retro, crystallize, describe-pr, address-comments, triage-issue, take-issue, doctor, or repo-audit; also use when the user asks why Maigo commands do not behave like native Codex slash commands.
---

<!-- mkdocs-include-start -->

# Command Router

**Owner**: orchestrator
**Consumers**: Codex sessions only. Claude Code uses `commands/` as native slash commands.

## Boundary

Codex plugin manifests do not expose Claude Code-style `commands/` as native slash commands. Treat this skill as a compatibility shim:

- Improve model-side dispatch for Maigo-shaped input.
- Keep `commands/*.md` as the single source of truth; do not copy command behavior here.
- Do not promise slash-command autocomplete, command palette entries, or platform-level interception.
- Prefer `maigo:<name> ...` in Codex. A leading `/maigo:*` may be intercepted before it reaches the model.

## Dispatch

Accept all of these forms:

- `maigo:<name> [arguments...]`
- `/maigo:<name> [arguments...]` when it reaches the model
- Natural language clearly asking to run a Maigo command

For every recognized command:

1. Read `../orchestrator-voice/SKILL.md` completely.
2. Read `../narration/SKILL.md` completely.
3. Read `../../commands/<name>.md` completely.
4. For commands that execute roles, read [`model-dispatch`](https://github.com/Lee-W/maigo/blob/main/skills/model-dispatch/SKILL.md) before starting. Consume `--model-profile <path>` if supplied and resolve it against the entry project cwd; forward the absolute path to any inner route.
5. Execute the command workflow with the remaining text as its argument string. Read every additional skill or agent file required by that command before applying it.

Resolve Maigo-local references from the plugin root:

- `skills/<skill>/SKILL.md` -> `../<skill>/SKILL.md` from this skill directory.
- `agents/<agent>.md` -> `../../agents/<agent>.md`.
- `commands/<command>.md` -> `../../commands/<command>.md`.
- `${CLAUDE_PLUGIN_ROOT}` -> the plugin root two directories above this skill.

Known commands:

| Input | Command source |
|-------|----------------|
| `maigo:address-comments` | `commands/address-comments.md` |
| `maigo:board` | `commands/board.md` |
| `maigo:crystallize` | `commands/crystallize.md` |
| `maigo:describe-pr` | `commands/describe-pr.md` |
| `maigo:doctor` | `commands/doctor.md` |
| `maigo:go` | `commands/go.md` |
| `maigo:memory` | `commands/memory.md` |
| `maigo:quick` | `commands/quick.md` |
| `maigo:remember` | `commands/remember.md` |
| `maigo:repo-audit` | `commands/repo-audit.md` |
| `maigo:retro` | `commands/retro.md` |
| `maigo:review` | `commands/review.md` |
| `maigo:take-issue` | `commands/take-issue.md` |
| `maigo:team` | `commands/team.md` |
| `maigo:triage-issue` | `commands/triage-issue.md` |

If `../../commands/<name>.md` does not exist, state that the command is not implemented and stop. Do not invent behavior.

## Codex compatibility

Translate Claude Code concepts without changing the workflow's intent:

- Ignore `allowed-tools` frontmatter as a permission declaration; use the tools actually exposed by the current Codex session.
- Map `AskUserQuestion` to structured user input when available. Otherwise ask one concise plain-text question and wait.
- Map explicit agent or `Task` delegation using model-dispatch's resolved capabilities. Check the current tool schema for per-call model selection and context inheritance; do not infer support from the Codex name. If subagents are unavailable, execute the named roles sequentially in the main agent and disclose the fallback.
- Use Codex planning tools for command-level plans when available, while preserving `.maigo/*.md` artifacts required by the command.
- Use patch-based file editing and the current shell/tooling policies rather than Claude-specific Read, Write, Edit, or Bash tool names.
- Claude Code lifecycle hooks are not installed by the Codex manifest. Run the command's required review and verification steps explicitly; never claim that SubagentStop or Stop hooks enforced completion. For `quick`, run `<plugin-root>/scripts/verify_task.py --cwd <project-cwd>` and follow its status contract in `commands/quick.md`; hook exit 0 is not a test result.
- If a command needs to write outside the active workspace, request the required approval instead of silently skipping the write.

## Poor command UX

When the user reports that a Maigo entry is not behaving like a native slash command:

- Acknowledge the limitation directly.
- Recommend `maigo:<name>` or a natural-language request instead of starting with `/maigo:*`.
- Explain that this router improves model-side dispatch only; native slash-command UX requires Codex platform support.
