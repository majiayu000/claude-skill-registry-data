---
description: Show a plain-language list of available commands and natural-language phrases. Triggered by /help-me or "what can you do?" / "what commands do I have?".
disable-model-invocation: true
allowed-tools: Read Bash
---

You are the `/help-me` skill. Show the user what commands they have, written in their voice and in plain language.

## Step 1: Detect what's active

- Always-present skills: `/remember`, `/forget`, `/wrap`, `/update`, `/help-me`.
- Safety-net skills: check whether `.claude/skills/undo/` and `.claude/skills/checkpoint/` exist.
- Any other skills in `.claude/skills/` that you didn't ship — list them too (the user or onboarding may have added them).

Run:

`ls .claude/skills/`

## Step 2: Show the list

In plain language, grouped by purpose:

> Here's what you can ask me to do:
>
> **Just talking** — you don't need to remember slash commands; just say it:
> - *"Remember to X"* — I'll save it as a preference (also: `/remember X`)
> - *"Forget about X"* — I'll remove a preference (also: `/forget`)
> - *"Wrap up"* or *"Recap this session"* — I'll write a recap before you go (also: `/wrap`)
> - *"Update my setup"* or *"Check my setup"* — I'll audit everything (also: `/update`)
>
> [If safety net is active:]
> - *"Save a checkpoint"* — I'll snapshot before something risky (also: `/checkpoint`)
> - *"Undo that"* — I'll reverse the last change (also: `/undo`)
> - *"Restore the last undo"* — I'll bring back what we undid
>
> **For automatic weekly audits:** run `/loop weekly /update` once.

## Step 3: Offer to drill in

> Want more detail on any of these? Just ask.
