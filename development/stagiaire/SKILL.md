---
name: stagiaire
version: 0.1.0
license: MIT
description: Use when the current session needs an answer or a work product from a model on ANOTHER vendor's stack - a second opinion from a different model family, a cheap fast model for bulk work, or a cross-model review - by dispatching that vendor's own CLI as a one-shot worker. Triggers include "ask grok/composer/gemini/claude/codex what it thinks", "get a second opinion from a different model", "cross-model review", "run this by another model", "poll several models". No orchestration framework required; if a Brigade roster exists, prefer `brigade run --worker` instead.
---

# stagiaire

A stagiaire is a cook visiting from another kitchen. This skill dispatches one-shot workers on other vendors' CLIs: the user's own logins, one model call per dispatch, no API keys, no framework. Each invocation below is the exact argv that works headless, including the flag that stops that CLI from silently doing nothing.

**Precondition:** the CLI must already be installed and authenticated by the user. Never run a login flow, never touch auth files, never fall back to an API key. If a CLI is missing or logged out, report it and move on to the vendors that work.

## The dispatch table

Run these with the task text substituted. Every one returns the worker's answer on stdout.

| Vendor / model | Write-capable dispatch | Read-only dispatch |
|---|---|---|
| Cursor (composer, grok, gpt, claude families) | `cursor-agent --model <id> -p --output-format text -f "<task>"` | same with `--mode plan --trust` instead of `-f` |
| Grok CLI (grok.com login) | `grok -m grok-4.5 -p "<task>" --always-approve` | `grok -m grok-4.5 -p "<task>" --permission-mode plan` |
| Codex (ChatGPT login) | `codex exec --sandbox workspace-write -m <model> "<task>"` | `codex exec --sandbox read-only -m <model> "<task>"` |
| Claude Code | `claude --model <id> --permission-mode bypassPermissions -p "<task>"` | `claude --model <id> -p "<task>"` (plain `-p` cannot edit files) |
| Antigravity (Google login) | `agy --model "<display name>" --add-dir <dir> --dangerously-skip-permissions --print "<task>"` | `agy --model "<display name>" --sandbox --print "<task>"` |
| Ollama | `ollama run <model> "<task>"` | same (prompt-only, no tools) |
| opencode (ChatGPT login) | `opencode run -m <provider>/<model> "<task>"` | same, instruct read-only in the prompt |
| pi (ChatGPT login) | `pi --model openai-codex/<model>:<tier> -p "<task>"` | `pi --tools read,grep,find,ls --model openai-codex/<model> -p "<task>"` |

Model ids: `cursor-agent models`, `agy models`, `grok models`, `opencode models`, `ollama list`. Codex reasoning effort is per-run config: `codex exec -c model_reasoning_effort=<none|low|medium|high|xhigh> -m <model> "<task>"`.

## The traps, one per CLI

Each of these was found by a dispatch that looked successful and was not. Check for them before trusting a result.

- **cursor-agent exits 0 when it refuses.** In a directory it has not trusted, headless `cursor-agent -p` prints a refusal and exits clean. Always pass `-f` (write) or `--trust` (plan). And Cursor's composer models emit empty text in `--mode plan`: their findings go into a plan artifact, not stdout. Benchmark or query composer models in write mode with a do-not-modify instruction.
- **grok stops silently at the first tool-approval gate.** Headless `grok -p` without `--always-approve` no-ops after its preamble and exits 0.
- **codex refuses non-git directories.** `Not inside a trusted directory and --skip-git-repo-check was not specified.` Dispatch from inside a git repo.
- **plain `claude -p` cannot edit files.** Permission prompts have no terminal to land on, so write tasks die quietly. Add `--permission-mode bypassPermissions` only when the task genuinely needs writes, and prefer an isolated working copy when you do.
- **agy print mode has its own 5-minute clock.** `--print-timeout 12m` for thinking-heavy tasks, or the run dies before the model finishes. Model pins are the full display string, parentheses included: `agy --model "Gemini 3.5 Flash (Low)"`.
- **pi's system prompt does not name the model, and bad tier suffixes pass through.** Identity self-reports hallucinate (a gpt-5.6-sol run claimed to be GPT-5.2). Verify at the request layer, not by asking. An invalid `:tier` suffix becomes a literal model id the backend rejects, while valid tiers (`off` through `max`) are parsed and applied. pi serves gpt-5.6-luna where opencode cannot.
- **opencode can edit the wrong project, on both versions.** Workers non-deterministically apply edits to a previously registered project instead of their own directory (anomalyco/opencode#36498). Seen on the v2 beta (3/10 runs) and on stable 1.17.18 (overwrote canonical files in a real multi-job run, though a minimal repro passes). Do not trust opencode-native isolated file-editing workers on any version. For dispatch, one-shot read tasks are fine, and empty output with exit 0 usually means the model slug is broken upstream, not that the model had nothing to say.

## Orchestrating instead of dispatching once

For a chef-and-workers setup where a primary model plans, fans out, and synthesizes, opencode's agent config does it natively. Two rules make it safe and cheap:

1. **Strip the chef's write tools.** `"tools": { "write": false, "edit": false, "patch": false }` on the primary agent. The orchestrator thinks and dispatches. Only worker CLIs touch files. A model that cannot write cannot wreck a tree no matter what goes wrong upstream.
2. **Pin thinking per subagent, not per model.** Subagents accept `"options": { "reasoningEffort": "<tier>" }`, and the same model at different tiers behaves like different workers. Getting the tier wrong is self-documenting: pass an unsupported value and the error lists the supported ones.

```json
{
  "agent": {
    "chef": {
      "mode": "primary",
      "model": "openai/gpt-5.6-sol",
      "prompt": "You orchestrate. Dispatch native subagents via the task tool; reach other vendors with the bash commands you were given. Never answer worker questions yourself.",
      "options": { "reasoningEffort": "high" },
      "tools": { "write": false, "edit": false, "patch": false }
    },
    "fast":     { "mode": "subagent", "model": "openai/gpt-5.6-sol", "description": "Sol, thinking off",  "options": { "reasoningEffort": "none" } },
    "deep":     { "mode": "subagent", "model": "openai/gpt-5.6-sol", "description": "Sol, deep",         "options": { "reasoningEffort": "xhigh" } }
  }
}
```

Give the chef the dispatch table above in its prompt for the cross-vendor seats, and tell it to run them one at a time.

## Rules

- One dispatch, one worker, one answer. Do not chain a second model call to "clean up" a worker's output. Report it as received.
- Identify the worker when it matters. A model asked "which model are you" through the wrong flag path answers as the wrong model, which is how misconfigured dispatch gets caught.
- Respect the user's metering. Flat-rate logins first. If two lanes serve the same model, use the flat one (Cursor serves grok-4.5 and several claude models, so a Cursor subscription may cover what a metered lane would charge).
- Read-only means the CLI enforces it, not the prompt, wherever the table offers a real sandbox flag. Prompt-level read-only is a request, not a guarantee.
- If dispatches are becoming a routine part of the workflow, that is a roster: [brigade](https://github.com/escoffier-labs/brigade) keeps the seats in one TOML file and `brigade run --worker <seat>` replaces every incantation above with one flag.
