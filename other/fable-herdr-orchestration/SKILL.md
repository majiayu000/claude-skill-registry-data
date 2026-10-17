---
name: fable-herdr-orchestration
description: Orchestrate Fable and Codex workers through Herdr with explicit model and effort routing.
disable-model-invocation: true
---

# Fable Herdr Orchestration

Read `~/.agents/skills/herdr-orchestration/SKILL.md` and follow all of it, including worker agent, worker permissions, topology, the dispatch loop, and completion and cleanup; it sets `disable-model-invocation`, so reach it by file rather than through the skill tool. If that path does not exist, try `../herdr-orchestration/SKILL.md` relative to this file. If neither resolves, say that the orchestration layer is not installed and stop; do not proceed on this file alone.

This skill binds that one to Fable and Codex, exercising its "a binding skill pins one" exception: the worker CLI is pinned per role in the table below and does not track the host agent. The sections below override that skill only where they conflict; everything it says otherwise still applies, including its requirement to state the resolved agent in the first status report; state each role's model and effort there too, since this skill pins them.

## Control tower

Treat the current Fable session as the control tower. Run it from a trusted directory with:

```bash
claude --model fable --effort xhigh --dangerously-skip-permissions
```

`herdr pane current --current` reports the agent kind but not the model, so read this session's own launch line with `ps -o command= -p $PPID` and confirm it carries `--model fable`. If it does not, give the command above to the user and stop. If the launch line cannot be read at all, say so and ask the user to confirm before dispatching anything.

## Role binding

Bind the capability roles from `herdr-orchestration` to these agents:

| Role | Agent |
|---|---|
| **Control tower** | Fable, xhigh — the current session. |
| **Default worker** | Codex GPT-6 Sol, xhigh. |
| **Specialist worker** | Fable, xhigh, for architecture or synthesis that benefits from a second Fable perspective, the hardest cross-cutting reasoning, recovery from stalled work, or an independent final review. |
| **Maximum worker** | Codex GPT-6 Astra, high, for the hardest isolated implementation, debugging, or adversarial review. |

The `-m` values in the launch commands below are literal model ids, not display names: "Codex GPT-6 Sol" is `gpt-6-sol` and "Codex GPT-6 Astra" is `gpt-6-astra`.

Start uncertain work at `xhigh`. Reserve the maximum worker for work whose observed difficulty or stakes justify its cost. When escalating, choose the maximum worker for isolated execution and a Fable specialist for cross-cutting reasoning.

## Launch commands

Start workers with `herdr agent start <name> --kind <kind> --pane <pane-id> -- <agent-args>`. `--kind` selects the executable, so pass each command below without its leading executable name as the arguments after `--`:

```bash
# Default worker — Codex Sol, xhigh
codex -m gpt-6-sol --approve-for-me -c 'model_reasoning_effort="xhigh"'

# Maximum worker — Codex Astra, high
codex -m gpt-6-astra --approve-for-me -c 'model_reasoning_effort="high"'

# Specialist worker — Fable, xhigh
claude --model fable --effort xhigh --dangerously-skip-permissions
```

A default Codex worker therefore starts as:

```bash
herdr agent start impl-1 --kind codex --pane <pane-id> -- -m gpt-6-sol --approve-for-me -c 'model_reasoning_effort="xhigh"'
```

For Codex, `-c key=value` overrides one config value for that worker without changing global config. Values are parsed as TOML, so string values retain their inner quotes.

The permission and sandbox flags in these commands come verbatim from the launch matrix at `~/.agents/skills/herdr-orchestration/references/agent-launch.md`; that file, not this one, defines what they do. The model and effort flags are this binding's own.
