---
name: favorite-harness
description: Look up the user's preferred coding-agent harness, model, effort, and autonomous launch command. Use when choosing or launching a coding agent or when another routing skill needs defaults; do not use as an orchestration workflow.
---

# Favorite harness

This skill selects defaults; it does not orchestrate or launch by itself. Match rows top-to-bottom, and preserve each table value the user did not explicitly override. When a caller launches, use the complete autonomous command shown.

| Job | Harness | Model | Effort |
|---|---|---|---|
| Orchestration | Claude | Opus 5.5 | xhigh |
| Final review, security review | Claude | Opus 5.5 | high; Fable 5.1 xhigh for the hardest cross-cutting reasoning or a high-stakes security audit |
| Implementation | Codex | GPT-6 Sol | high; stuck → xhigh; still stuck → GPT-6 Astra high |
| Tests, retrieval, checking, creating issues | Cursor Agent | Grok 4.6 | high; medium if mechanical |
| Observation (an `auto-improve` observer, polling a transcript for hours) | Claude | Opus 5.5 | medium; Cursor Agent Grok 4.6 high once its spend runs high |
| Anything that is not tool/repo work | Kimi Code CLI | K3 | max |

```bash
# Claude — Opus 5.5 xhigh (orchestration); high (review); medium (observers)
claude --model opus --effort xhigh --dangerously-skip-permissions
claude --model opus --effort high --dangerously-skip-permissions
claude --model opus --effort medium --dangerously-skip-permissions

# Claude — Fable 5.1 xhigh (hardest reasoning, high-stakes security audit)
claude --model fable --effort xhigh --dangerously-skip-permissions

# Codex — GPT-6 Sol high (stuck → xhigh); Astra high as the last step
codex -m gpt-6-sol --approve-for-me -c 'model_reasoning_effort="high"'
codex -m gpt-6-sol --approve-for-me -c 'model_reasoning_effort="xhigh"'
codex -m gpt-6-astra --approve-for-me -c 'model_reasoning_effort="high"'

# Cursor Agent — Grok 4.6 high (mechanical → medium); never a *-fast variant
agent --model cursor-grok-4.6-high --yolo --sandbox disabled
agent --model cursor-grok-4.6-medium --yolo --sandbox disabled

# Kimi Code CLI — K3 max. No launch-time effort flag; send /effort max once idle.
kimi -m k3 --yolo
```

In Herdr, `--kind` is `claude` / `codex` / `cursor` / `kimi`. Pass everything after the executable after `--`. See `herdr-orchestration` for the refused-launch fallback.

Opus 5.5 thinks more per turn than Fable at the same effort name, so carry an effort level across models only through this table. When a Claude session reports "Switched to" an older model (a safety flag), report it; the work did not run on the model this table picked.

Grok 4.7 (`grok-4.7-*`, no `cursor-` prefix) is opt-in: per task it costs about twice as much as 4.6, and Cursor subagents set to it silently run on Auto.

Never pin max or ultra on any model, or Grok xhigh. Do not put Kimi on a tool loop.
