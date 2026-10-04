---
name: hermes-gpt-lane
description: Load when Claude, Codex, Antigravity, or another external agent needs to call Hermes GPT as a worker, ask it to use Hermes-native tools/memory/gateway context, or hand work back to the Hermes GPT profile. Covers `hermes --profile gpt -z`, toolset/skill selection, and safe gateway boundaries.
metadata:
  targets:
    - codex
    - claude
    - antigravity
    - hermes-default
    - hermes-gpt
    - claude-hermes
---
# Hermes GPT lane

Use this when the current agent needs Hermes GPT specifically, not just another LLM: Hermes memory/session context, Hermes tool wrappers, Skillshare/Hermes skills, Telegram/Discord context, cron, mem0, local gateway knowledge, or Kosta-specific operating rules.

## Default one-shot pattern

Run from the relevant repo/workdir so Hermes loads local AGENTS.md/project context:

```bash
hermes --profile gpt -z "<self-contained task prompt>"
```

For narrower, cheaper calls, restrict toolsets and preload the relevant skill:

```bash
hermes --profile gpt -t terminal,file -s meta-tools__skillshare -z "<task prompt>"
```

For interactive local work, use:

```bash
hermes --profile gpt chat -q "<initial query>"
```

## Prompt contract

Tell Hermes GPT what role it should play, the cwd/repo, exact scope, and what evidence to return. Ask for concise final output plus verification handles: file paths, commands run, tests, URLs, or logs. If Hermes reports a side effect, verify it from the parent agent before telling Kosta it succeeded.

## Gateway safety

Do not ask Hermes GPT to restart the same live Telegram/Discord gateway from a gateway-driven conversation. From local shell/SSH/tmux, service operations are allowed when appropriate, but still require user approval for gateway lifecycle actions.

## When to use

Use Hermes GPT for Kosta-specific local ops, multi-tool Hermes workflows, Skillshare/Hermes config, memory-aware answers, Telegram/Discord surfaces, and tasks where Hermes' curated skills matter more than raw model capability. For isolated code generation, Codex or Claude may be cheaper and cleaner.
