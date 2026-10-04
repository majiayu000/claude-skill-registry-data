---
name: use-coding-agents
description: >
  How to use the coding agents installed on this machine (claude, codex, droid,
  grok, hermes, opencode, copilot, pi) as plain sub-agents in orchestrated
  workflows: one headless invocation, one prompt in, one result out. Deliberately
  ignores each CLI's own orchestration features (droid --mission, codex
  multi_agent, hermes delegation/moa/kanban, grok --agents, opencode personas).
  The orchestrator is whatever session is running the skill; the CLIs are
  interchangeable workers. Use when the user asks "which agent should run this",
  "fan out workers", "run X headless", or when a lifeos skill (overnight,
  timeboxed-iterating, workgraph, gauntlet, bughunt, dark-factory) needs to launch
  an agent CLI.
---

# Use Coding Agents — Installed CLIs as Plain Sub-agents

Validated on `fedora` 2026-09-04 by running each command on a minimal prompt (write one file, or
reply OK). `pop-os` is set up identically via `control/install.sh`. Run `hostname` first.
Re-run `<agent> --help` before relying on any flag not listed here.

## Principle

Every agent here is a **worker**: it receives a prompt, edits files in one directory, commits,
prints a result, exits. Nothing more.

- **Do not use the CLIs' own orchestration features.** No `droid --mission`, no codex
  `multi_agent`, no hermes `delegate_task` / `moa` / `kanban`, no `grok --agents`, no opencode
  personas. Those are unvalidated here, spend tokens invisibly, and hide state from the orchestrator.
- **The orchestrator is the session running this skill** (normally claude via the Agent tool or a
  lifeos skill). It plans units, writes prompts, launches workers, reads short results.
- Workers are interchangeable. Pick by availability and cost, not by feature.

## Workers

| Agent    | Invocation                                                | Auto-approve                                   | Status 2026-09-04 |
|----------|-----------------------------------------------------------|------------------------------------------------|-------------------|
| claude   | `claude -p "<prompt>"`                                    | `--dangerously-skip-permissions`               | PASS |
| codex    | `codex exec "<prompt>"` (or prompt on stdin)              | `--dangerously-bypass-approvals-and-sandbox`   | PASS |
| droid    | `droid exec "<prompt>"`                                   | `--skip-permissions-unsafe` (not with `--auto`) | PASS |
| grok     | `grok -p "<prompt>"`                                      | `--always-approve`                             | PASS |
| grokc    | `COLORTERM=truecolor grokc -p "<prompt>"`                 | built in (podman, `$PWD` only)                 | PASS |
| opencode | `opencode run "<prompt>"`                                | `--auto` (without it a permission prompt hangs a headless run) | PASS (default model now `openrouter/~anthropic/claude-sonnet-latest`, github-copilot disabled in `control/config/opencode.jsonc`) |
| pi       | `pi -p "<prompt>"`                                        | none needed                                    | PASS, local model, slow |
| hermes   | `hermes -z "<prompt>" --in <dir>`                         | `--yolo`                                       | FLAKY: `write_file` fails (`DaemonThreadPoolExecutor ... _initializer`); 1262 commits behind |
| copilot  | `copilot -p "<prompt>" -s`                                | `--allow-all`                                  | FAIL: no auth; needs interactive `/login` |

Facts from `--help`: grok 1.0.13 has no `--check` / `--best-of-n`; droid rejects `--auto` together
with `--skip-permissions-unsafe`; hermes restores the previous session's cwd unless `--in` is given.

### Getting the result back

| Agent    | Machine-readable result                              |
|----------|------------------------------------------------------|
| claude   | `--output-format json` (with `-p`)                    |
| codex    | `-o <file>` writes the last message; `--json` for JSONL events |
| droid    | `-o json`                                            |
| grok     | `--output-format json`, or `--json-schema '<schema>'` |
| opencode | `--format json`                                      |
| pi       | `--mode json`                                        |

Simplest contract, works everywhere: tell the worker to write its output to a file and print one
line `DONE|BLOCKED|FAILED <reason>`. Read the file, not the transcript.

### Cheaper / capped variants (validated)

Use when a unit is small. Same worker, fewer tokens:

- claude: `--model haiku --max-turns N` (do not add `--bare` or `--setting-sources ""`; both drop auth)
- codex: `-c model_reasoning_effort=low` (`minimal` is rejected)
- droid: `-r low -m claude-haiku-4-5-20251001`
- grok: `--max-turns N --no-subagents --disable-web-search`
- opencode: `--variant minimal`
- pi: `--thinking off`

### Listing and picking models

Validated 2026-09-04. Pass the id with the agent's model flag (`--model` / `-m`).

| Agent    | List available models                                   | Default today                 | Flag |
|----------|---------------------------------------------------------|-------------------------------|------|
| claude   | no list command; aliases `fable`, `opus`, `sonnet`, `haiku` or a full id like `claude-fable-5-1` | account default | `--model` |
| codex    | `codex debug models` (JSON catalog, 9 entries: gpt-5.6-sol/terra/luna, gpt-5.5, gpt-5.4, gpt-5.4-mini, gpt-5.3-codex-spark, …) | `gpt-5.6-sol` (`~/.codex/config.toml`) | `-m` |
| droid    | no list command; `/model` in the TUI. Custom/local models are the `customModels` entries in `~/.factory/settings.json` (ollama qwen3, glm-4.7-flash, kimi-k2.7-code, …) | `gpt-5.6-sol` | `-m` |
| grok     | `grok models` (7 entries, grok-4.6 default, grok-4.5, …) | `grok-4.6`                    | `-m` |
| opencode | `opencode models` (379 entries as `provider/model`; `openrouter/~anthropic/...` ids need the tilde) | `openrouter/~anthropic/claude-sonnet-latest` (`control/config/opencode.jsonc`) | `-m` |
| pi       | `pi --list-models [search]` (table with context/max-out/thinking columns) | `harbor-llamacpp` Qwen3-Coder-Next Q8 (`~/.pi/agent/settings.json`) | `--model` |
| hermes   | `hermes model` (interactive picker; `--refresh` re-fetches each provider's `/v1/models`); `hermes config get model` prints the default | `deepseek/deepseek-v4-flash-0731` via `nous` | `-m` |
| copilot  | no list command; `/model` in the TUI                    | account default               | `--model` |

### Isolation

Two workers must never write the same file in the same tree. Use a worktree per worker:
`claude -w <name>`, `droid -w <name>`, `grok -w <name>`, `hermes --worktree`; for codex, opencode,
copilot, pi run `git worktree add` first and `cd` into it. (Worktree flags checked in `--help` only.)

### Resume instead of restart

`claude --resume <id>`, `codex exec resume --last`, `droid exec -s <id>`, `grok -r <id>`,
`hermes --resume <s>`, `opencode run -s <id>`, `copilot --continue`, `pi -c`. Resume a BLOCKED
worker with the missing fact rather than re-dispatching cold.

## Fan-out pattern

```bash
d=$(mktemp -d /tmp/orch-<slug>-XXXX)
cat > "$d/preamble.md" <<'P'
You are working on <project> at <code_path>.
Read CLAUDE.md / AGENTS.md / README.md first if present.
Commit with clear messages when done. Do not ask questions.
Do not start or reinstall opencode.service; the OpenCode daemon is retired.
Write your result to <unit_file> and print ONLY one line: DONE|BLOCKED|FAILED <reason>.
P
cd <code_path>
claude -p "$(cat $d/preamble.md $d/unit-1.md)" --dangerously-skip-permissions        > $d/1.log 2>&1 &
codex exec --dangerously-bypass-approvals-and-sandbox < <(cat $d/preamble.md $d/unit-2.md) > $d/2.log 2>&1 &
droid exec --skip-permissions-unsafe -f <(cat $d/preamble.md $d/unit-3.md)          > $d/3.log 2>&1 &
grok -p "$(cat $d/preamble.md $d/unit-4.md)" --always-approve -w unit-4             > $d/4.log 2>&1 &
opencode run "$(cat $d/preamble.md $d/unit-5.md)" --auto                          > $d/5.log 2>&1 &
wait; tail -n1 $d/*.log
```

Prompts live on disk and are dispatched by path. The orchestrator authors nothing itself
(same discipline as `timeboxed-iterating`).

## Rules

- **Plain workers only.** If you reach for a CLI's mission / delegation / persona feature, stop and
  fan out from the orchestrator instead.
- **One unit, one directory, one commit** per worker. Merge worktrees afterwards.
- **Logs under `/tmp` or the scratchpad**, never in the repo.
- **Cap loops** with `--max-turns` where it exists, otherwise a turn budget in the prompt.
- **Bypass flags only** in a worktree, in `grokc`, or in a repo you can `git reset`.
- **Backlog.md stays human.** Workers do not touch `backlog/tasks/`.
- **Smoke tests are one word.** Validate a recipe with "Reply with the single word OK." only.
- **Do not invent flags.** Not in this file → run `--help` and paste the real one.

## Related skills

- `overnight` — dispatch approved work items to these workers in the background
- `timeboxed-iterating`, `workgraph`, `workmachine`, `gauntlet`, `dark-factory`, `bughunt` — orchestration loops that use these workers
