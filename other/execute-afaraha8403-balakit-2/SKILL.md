---
name: execute
description: >-
  Asks workers on the current harness to research read-only, then this
  chat does the work. Default roster is the current model on every slot.
  Apply when the user invokes execute or /execute, or wants workers to
  research before this chat writes. Use opinion when nobody should write.
  Use inception to produce the plan first. Use kit-workflows for one-agent
  implementation. Use deep-deliberation for checkpointed decisions.
user-invocable: true
disable-model-invocation: true
invocation-type: manual
version: "1.3.0"
author: "Ali Farahat"
tags: ["orchestration", "multi-model", "execute"]
when_to_use: |
  USE WHEN:
  - The user invokes execute or /execute, or wants workers to research then this chat to do the work.
  - They want parallel research takes, including the current model or the same family on more than one worker.
  DO NOT USE WHEN:
  - Nobody should write (use opinion).
  - They want one agent to just build (use kit-workflows).
  - They want the plan as the deliverable (use inception).
  - The work is a checkpointed design fork (use deep-deliberation).
---

# Execute

> **Leading words:** current first, same-family ok, slug shield,
> auto-pick stays distinct, this chat does the work.

Workers research. This chat does the work. There is no agent-count
flag — pick 2 or 3 from the job (default 3; 2 if the request is small,
local, or mechanical).

## Operating contract

- Do not auto-start this skill. The user must ask for it.
- Current-for-all is the default. Same family may occupy more than one slot when they chose that.
- Auto-pick is the only path that still requires distinct families.
- Do not invent a model name. Use the live list this harness exposes.
- Never write a spawn identifier in a question, option, chat roster, worker prompt, or take label. Map family → live-list name only in the spawn tool's `model` argument. Current → `inherit` (or omit `model`).
- Workers are read-only. A worker that edits files has failed; discard that take.
- This chat writes after the takes. Do not send writes back to workers.
- If this host cannot spawn a child at all, stop. Auto-pick that cannot gather two families: offer Current-for-all or `deep-deliberation`.

## Runtime state

```text
EXECUTE_STATE
host: cursor | claude-code | opencode | copilot | codex | other
agents: 2 | 3
roster: unset | Current,OpenAI,…
takes: 0/N
next_action: one action only
```

## Pipeline

Copy these steps into the todo list verbatim. Skip with `skip: <reason>`.

1. Detect the host. Read [references/hosts.md](references/hosts.md). Build the live spawnable model list. Current-for-all does not need two families.
2. Set `agents` to 3, or 2 if the request is small, local, or mechanical. If the user named models (or current), use that list (2–5) instead of auto-pick. One named model fills every slot.
3. Resolve roster: models the user named, or **Current for all**, or auto-pick, or assign each worker. Announce with **display names** before spawning.
4. Spawn one read-only worker per roster slot. Same prompt. Parallel. Read [references/worker-prompt.md](references/worker-prompt.md).
5. Render labeled takes (`[Current]`, `[OpenAI]`, …). Do not write yet.
6. This chat merges with `[display name]` attribution, does the work, proves the real path.

## Roster

If the user already named 2–5 models that exist on this host, use them.
Same family is allowed. If they named one model, or said **current** /
inherit, fill every slot with that choice.

If the user said **auto-pick** (or chose it), run auto-pick for `agents`
families from [references/hosts.md](references/hosts.md), announce with
display names, then spawn.

Otherwise ask:

```text
prompt: Which models should research?
options:
- Current model for all workers (Recommended)
- Auto-pick distinct families
- I'll assign each worker
- Say this in plain English
allow_multiple: false
```

Option ids: `current`, `auto`, `assign`, `simplify`. Never live-list names.

`Say this in plain English` is a meta question: explain Current vs
auto-pick with display-name examples (never spawn ids), then re-ask.
Do not spawn yet.

If they assign each worker, ask **one question per slot** (not a
multi-select). Each slot's first option is `Current model (Recommended)`,
then one option per remaining family using **display names** and
`fam-*` ids from [references/hosts.md](references/hosts.md). Same
family may be chosen on more than one slot.

No structured question tool → numbered text fallback.

## Write

- Resolve consensus and divergence with `[display name]` attribution.
- Keep valuable minority observations. Reject weak claims explicitly.
- Do the work here. Do not delegate writes back to workers.
- Prove on the real path (or closest executable check). `skip:` if the surface cannot be driven.

## Reply contract

```text
Playbook: execute
roster: Current, OpenAI, Grok
```

Then the labeled takes, what shipped, and how you verified.

## Delegate failure

1. Retry one transient spawn failure.
2. Never invent a missing take.
3. Fewer than two successful takes → stop, ask whether to retry or abort.
