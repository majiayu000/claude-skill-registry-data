---
name: opinion
description: >-
  Asks workers on the current harness the same question and returns
  labeled takes. Default roster is the current model on every slot.
  Nobody writes project files. Optional --agents N (default 3, min 2,
  max 5). Apply when the user invokes opinion or /opinion, wants other
  takes, or says auto-pick. Use execute when this chat should do the work
  after the takes. Use deep-deliberation for checkpointed decisions. Use
  blinded-eval to A/B a skill change.
user-invocable: true
disable-model-invocation: true
invocation-type: manual
version: "1.2.0"
author: "Ali Farahat"
tags: ["orchestration", "multi-model", "opinion"]
when_to_use: |
  USE WHEN:
  - The user invokes opinion or /opinion, wants parallel takes, or says auto-pick without asking to write.
  - They want parallel takes, including the current model or the same family on more than one worker.
  DO NOT USE WHEN:
  - This chat should do the work after the takes (use execute).
  - The work is a checkpointed design fork (use deep-deliberation).
---

# Opinion

> **Leading words:** current first, same-family ok, slug shield,
> auto-pick stays distinct, labeled takes, no writes.

Workers answer the same request. This chat does not edit the project.

## User input

```text
$ARGUMENTS
```

Optional `--agents N` (also `--n N`, or a lone integer). Default **3**.
Clamp to 2–5. Strip the flag from the question text. If the user already
named models (or current), use that list and ignore `--agents`. One
named model fills every slot.

## Operating contract

- Do not auto-start this skill. The user must ask for it.
- Current-for-all is the default. Same family may occupy more than one slot when they chose that.
- Auto-pick is the only path that still requires distinct families.
- Do not invent a model name. Use the live list this harness exposes.
- Never write a spawn identifier in a question, option, chat roster, worker prompt, or take label. Map family → live-list name only in the spawn tool's `model` argument. Current → `inherit` (or omit `model`).
- Workers are read-only. A worker that edits files has failed; discard that take.
- Do not write project files. If the user wanted the work done, use `execute`.
- If this host cannot spawn a child at all, stop. Auto-pick that cannot gather two families: offer Current-for-all or `deep-deliberation`.

## Runtime state

```text
OPINION_STATE
host: cursor | claude-code | opencode | copilot | codex | other
agents: 2-5
roster: unset | Current,OpenAI,…
takes: 0/N
next_action: one action only
```

## Pipeline

Copy these steps into the todo list verbatim. Skip with `skip: <reason>`.

1. Parse `--agents` (default 3, clamp 2–5). Detect the host. Read [references/hosts.md](references/hosts.md). Build the live spawnable model list. Current-for-all does not need two families.
2. Resolve roster: models the user named, or **Current for all**, or auto-pick `agents` families, or assign each worker. Announce with **display names** before spawning.
3. Spawn one read-only worker per roster slot. Same prompt. Parallel. Read [references/worker-prompt.md](references/worker-prompt.md).
4. Render labeled takes (`[Current]`, `[OpenAI]`, …). Stop. Do not merge into one verdict. Do not write files.

## Roster

If the user already named 2–5 models that exist on this host, use them.
Same family is allowed. If they named one model, or said **current** /
inherit, fill every slot with that choice.

If the user said **auto-pick** (or chose it), run auto-pick for `agents`
families from [references/hosts.md](references/hosts.md), announce with
display names, then spawn.

Otherwise ask:

```text
prompt: Which models should answer?
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

## Reply contract

```text
Playbook: opinion
roster: Current, OpenAI, Grok
```

Then the labeled takes. No files changed.

## Delegate failure

1. Retry one transient spawn failure.
2. Never invent a missing take.
3. Fewer than two successful takes → stop, ask whether to retry or abort.
