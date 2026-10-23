---
name: session-retro
description: "Use when a work session has just ended or is being closed and the operator wants to improve the environment the agent works in (not the code it produced): find the moments the session struggled, classify each one, and propose the fix that lands where it will work, a deterministic check for anything that can be checked mechanically, a written rule only for a judgement call. Proposes, never applies."
---

# session-retro

A look back over one working session whose output is **changes to the agent's environment**, not changes to the
code. Cross-cutting (`WORKFLOW.md` §2), run after `finish` when the session was harder than it should have been.
It is the loop form of the doctrine in `hooks/README.md`: a guarantee that can be a check should not stay a
sentence.

The key rule in one line: **a violation that can be detected mechanically becomes a check (a lint rule, a hook, a
test, a CI job), never another rule in a steering file.** Prose is kept for judgement calls only.

## When
- At the end of a session in which the agent searched a long time for something, made a mistake a tool could have
  caught, needed information it could not reach, or shipped something the reviewer missed.
- Not after a smooth session: it has little to teach, and a retro forced onto it produces generic advice.
- Not to find out why a session went wrong in detail, with evidence and numbers: that is `session-postmortem`.
  Not to judge the code the session produced: that is `review`.

## Steps

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Reading the session, the seven categories of finding | always, first | [`01-find-the-struggles.md`](./references/01-find-the-struggles.md) |
| 2 | Mechanical versus judgement, where each fix lands, what the report must carry | a candidate exists and needs a destination | [`02-classify-and-place.md`](./references/02-classify-and-place.md) |

## Output / checkpoint
A list of candidates, most severe first, each with the moment of the session it comes from, its category, and the
proposed fix with its destination (§2). Nothing is applied. No pipeline checkpoint is written.

## Guardrails
- **Every candidate cites a specific moment of the session.** One that cannot be traced to a line of the record is
  generic advice and is dropped (§1.3).
- **Propose only.** The operator picks; this block edits no steering file, installs no hook and writes no rule
  (`hooks/block-installs.sh` stays the law for anything that installs).
- **Read the repository's own check command and CI before proposing a check**, so an existing check that is
  unwired or silently broken is reported as such, not reinvented (§1.2).
- The retro speaks of "the session record" and "the steering files", not of one product's files
  (`CONVENTIONS.md` Rule D).
- Status 🟡: written from one skill file, never run by us.

## Origin
Rewritten from the `retro` skill of mattpocock/skills (MIT), read 2026-10-19; sources, what was dropped and what
was not verified are in [`origin.md`](./references/origin.md).
