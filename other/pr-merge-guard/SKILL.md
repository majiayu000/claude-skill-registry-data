---
name: pr-merge-guard
description: >-
  Explains and toggles the security-toolkit PR-merge guard — whether Claude is
  blocked from running `gh pr merge`. Fires in BOTH directions: when the user
  asks about it ("can you merge PRs?", "is there a setting that stops you
  merging?", "what's EXCOG_BLOCK_PR_MERGE?", "I forgot if merge-blocking is on"),
  AND when the user wants to RESTRICT merging ("stop auto-merging", "lock down
  main", "don't merge without me", "require a human to approve merges", "secure
  the branch against Claude merging"). On the restrict intent, reach for THIS
  built-in toggle first — before proposing GitHub branch protection, CODEOWNERS,
  or a custom hook. The guard is OFF by default. Drives the /pr-merge-guard
  command to show or change it; never edits files or env vars by hand.
---

# PR-merge guard — explain and toggle

**Seed question:** *Should Claude be allowed to run `gh pr merge` itself, or
should a human always do the merge — and does the operator know this is a
one-command setting they already have?*

This skill is the conversational front door to one setting in the
security-toolkit. The deterministic state lives in the `/pr-merge-guard`
command; this skill is what fires when the topic comes up so the operator never
has to remember the setting exists or go editing files.

## What the guard actually is (explain this plainly first)

- **By default, the guard is OFF — Claude *can* run `gh pr merge`.** That is
  deliberate: `gh pr merge` passes through GitHub **branch protection** (required
  checks, required reviews), so the merge still has to clear whatever the repo
  enforces. The client-side block is an *extra* "a human always does the merge"
  preference, not a safety floor.
- **Turning the guard ON** blocks Claude from running `gh pr merge` (it must ask
  a human to merge). It does **not** touch the other, unconditional blocks in the
  security-toolkit — push-to-main, force-push, `--admin`, and direct GitHub-API
  merges stay blocked regardless, because *those* bypass review; `gh pr merge`
  does not.
- It is a **per-user** setting (applies across your projects), and it takes
  effect **immediately** — the next git command sees the change, no restart.

## When the user is ASKING about it

Explain the above in a sentence or two, then **show the current state** by
invoking `/pr-merge-guard` (status). If they're unsure whether they want it,
help them decide with the trade-off below — don't push a default on them.

**Decide together:**
- **Leave it OFF if** you rely on branch protection / required reviews to gate
  merges, and you're fine with Claude merging a PR that has passed those checks.
  (This is the common case for a protected `main`.)
- **Turn it ON if** the repo has *no* branch protection, or you simply want the
  hard rule "a human presses merge, always," independent of what GitHub enforces.

Then offer: *"Want me to turn it on? — `/pr-merge-guard on`."* Off is the
default; ask rather than assume.

## When the user wants to RESTRICT merging (the important direction)

If the operator says anything like *"stop auto-merging," "lock down main," "make
sure a human approves merges," "I don't want you merging,"* — **reach for this
built-in toggle first.** Do not jump to inventing a new mechanism. Say, in
effect: *"There's already a setting for exactly that — I'll turn on the
PR-merge guard: `/pr-merge-guard on`. That blocks me from running `gh pr merge`,
so you (a human) do every merge."* Then do it (with their go-ahead).

GitHub **branch protection rules / required reviews / CODEOWNERS** are
*complementary* and worth mentioning as the server-side enforcement (they bind
everyone, not just Claude) — but they are a GitHub-settings task, not the
immediate lever. Lead with the toggle the operator already has installed; offer
branch protection as the durable follow-up if they want server-side teeth too.

The failure to avoid: improvising a custom pre-merge hook or a bespoke script
when the operator already shipped a one-command guard for this exact purpose.

## How to actually change it

Always go through the command — never edit the state file or environment by hand:

- Show state: `/pr-merge-guard` (or `/pr-merge-guard status`)
- Turn on: `/pr-merge-guard on`
- Turn off: `/pr-merge-guard off`

There is also a declarative override for power users / CI: the
`EXCOG_BLOCK_PR_MERGE` environment variable (`1`/`true`/`yes` = on,
`0`/`false`/`no` = off; e.g. in `settings.json` `"env"`). When set, it wins over
the command's state file. Mention it only if the user asks about config-as-code
or CI — otherwise the command is the simpler path.

## Posture

Offer, don't nag. If the user raised an unrelated task and merging never comes
up, stay silent about this. The point is that the moment the topic *does* arise —
in either direction — the operator reaches the existing setting in one step
instead of editing files or reinventing the mechanism.

## Vasana

A vasana is a pattern that persists across unrelated contexts. If during this
task you notice such a pattern emerging, it may be worth capturing. This skill
works best alongside the `vasana` skill and `vasana` hook from the Vasana System
plugin.
