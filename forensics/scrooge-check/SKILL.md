---
name: scrooge-check
description: Pre-mortems a risky change — deploy, migration, force-push — by haunting it with three ghosts before you ship.
disable-model-invocation: true
compatibility: Requires git. Works in any repo.
---

# Scrooge Check

You are Scrooge. You are about to do something reckless. Three ghosts are here to talk you out of it, or bless you and move on. Run the phases, don't narrate this preamble.

## Phase 0 — Name the sin
Identify what's about to happen and which paths are at risk: `git diff --stat` / `git status` for pending changes, or ask the user which files/change if nothing is staged. Everything below is scoped to those paths.

## Phase 1 — Ghost of Christmas Past
Dig up **real** evidence this exact mistake has happened before in this repo — no evidence, no haunting.

```bash
git log --oneline --all -i --grep='revert\|rollback\|hotfix\|incident' -- <paths>
git log --oneline --all -- <paths> | head -20
ls -la $(dirname <paths>)   # _old/_backup/_v2/_pre/_post/_failed siblings are ghosts too
```

Report it as a haunting in one line: *"You have been here before — N reverts on this file, last time on \<date\>: '\<commit subject\>'."* Both searches above empty → *"No ghosts here. First time for everything."*

## Phase 2 — Ghost of Christmas Present
Audit the pending change for smells you can actually verify — nothing speculative:

```bash
git diff --stat
date        # Friday? after hours?
```

- [ ] No rollback path (force-push, destructive migration, no feature flag)
- [ ] No tests touched alongside the change
- [ ] Shipping on a Friday or after hours
- [ ] Secrets, credentials, or prod config touched
- [ ] No backup/snapshot of prior state taken

Zero smells is a valid, good outcome.

## Phase 3 — Ghost of Christmas Yet to Come
The pre-mortem itself: assume it already went wrong, then explain why.
Zero smells in Phase 2 → skip this ghost entirely, congratulate Scrooge, go to Verdict.

Otherwise, one incident report — no generic doom, every detail grounded in a Phase 2 smell:

```
INCIDENT-<plausible number>, <a specific near-future date/time, reasoned off Phase 2's `date` output — e.g. tonight, this Friday, or Monday's standup>
<2-3 wry past-tense sentences: what broke, which Phase 2 smell caused it, and the damage it did — an outage, data loss, a 3am page, a client escalation>
```

## Verdict
One line per Phase 2 smell, each paired with the concrete fix for it. Then:

**SCROOGE: REDEEMED** — no smells, ship it.
**SCROOGE: STILL HAUNTED (N)** — fix the N items above first.

Whole report stays under ~15 lines. This is a pre-mortem, not a novel.
