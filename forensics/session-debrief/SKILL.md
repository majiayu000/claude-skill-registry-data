---
name: session-debrief
description: >
  Use at every unit close, after the merge and before the report: record
  WC-worthy output with the global w-conatus skill, without asking again; say
  what was left out and why.
---

# Session debrief (the WC recording step)

The debrief is a step in the unit's close. **It is not a summary of the final answer.**
It counts what the unit actually produced, classifies it, records
the WC-worthy parts with the global `w-conatus` skill, and hands the report
what was recorded — or why nothing was.

It is this repository's form of the HQ debrief's classification step: the same
count-then-classify-then-commit order, with one target (WC) instead of HQ and
WC, because this repository's work is personal open source. This repository
creates **no company HQ record** — no worklog, plan, graph, or decision entry.

## When it runs

After the unit's end conditions stand — the merge that `session-unit`
requires, or the earlier stop the `user-turn:` named — and **before the final report**.
The owned worktree still exists at this point: the count below reads it, and
`session-unit` cleans the tree up after this step. The session runs it itself,
on every completed unit, without the user asking for it and without a new
turn.

A unit that produced nothing worth keeping still runs it: `no record needed`
with the reason it was decided is a legal result, and a better one than a
fabricated note.

## Where records go

WC only: `$W_CONATUS_ROOT` (default `~/Infocz/Projects/w-conatus`), through
the global **`w-conatus`** skill — its `capture` and `commit` modes, ontology
v2, `sources:` prefixes, and typed-relation floor. That skill owns how to
write; this file owns when and what to classify.

## Count first, from evidence

Do not recall the unit from the conversation; read it:

```sh
git -C "$WT" log --oneline origin/main..HEAD
gh pr view <n> --repo innocarpe/deepseek-build --json title,body,mergedAt,mergeCommit
git -C "$WT" status --short
```

Then walk the conversation for the signals:

| Signal | Likely record |
|---|---|
| A **user correction** of the session's behavior, or rework it caused | an incident line — WC `10_daily/` (or `20_work/active/` when it has its own next action) |
| A **judgment that flipped** (assumed X, measured Y) | correct the note that carries the wrong version; a `50_learn/` concept when the path transfers |
| A **procedure that survived a real run** and will be used again | `60_playbooks/` |
| A **concept** the unit explained ("why does it behave this way") | `50_learn/<area>/` |
| A **decision** with the alternatives it dropped | `70_decisions/` |
| Something **still unknown or blocked** | `80_gaps/` |
| Only meaningful in this conversation, or already recorded | nothing — say why |

**Repetition is the gate for lessons.** A lesson moves into a playbook,
concept, or decision only when the unit gives evidence it repeats: the same
thing happened before, was measured more than once, or the user corrected the
same behavior twice. A single occurrence is an incident line, or `00_inbox/`
when unsure. Do not invent candidates or lessons to fill the step.

## The close authorizes the writes

When the classification says record, capture and commit in the same turn —
**do not ask again**. The unit's close is the authorization; "WC에 넣을까요?" is
the round-trip this step exists to remove. The w-conatus ask-first list still
stands for it: missing or unclear root, structural changes (new top-level
folder, new type), bulk digests, and secrets whose redaction would change
what the note says.

## Write, verify, commit

1. **Look before you write.** `python3 scripts/search.py "<words>"` in WC,
   open the one or two closest notes, and choose update over new (C011). A new
   note gets its inbound link from the nearest sibling in the same turn (C022).
2. **Grade first.** Secrets, tokens, and PII never enter notes; this repo's
   personal scope does not change that (w-conatus "Never do these" §2,
   AGENTS.md §3.2 N-grade).
3. **Sources carry the unit** — `repo:innocarpe/deepseek-build <path>` or
   `exp:` with the command that showed it; free text fails lint (C005).
4. **Verify.** `python3 scripts/build-index.py`, then `bash scripts/verify.sh`
   (or `lint.py`); fix red before committing.
5. **Commit atomically** per concern with the w-conatus `commit` mode. The WC
   tree is shared with other sessions: stage with pathspecs, never
   `git add -A`, and leave a sibling's dirty file alone.
6. **Fail-close on the root.** If WC cannot be resolved and verified (no
   `AGENTS.md` and `90_meta/` under `$W_CONATUS_ROOT`), write nowhere else and
   do not report the unit done — the report carries the blocker.

## Report

The debrief contributes one line to the report `session-unit` defines:

- what was recorded — WC absolute paths and commit SHAs, or
- `no record needed` and the reason it was decided.

Never end the debrief silently: "nothing to record" without the reason is not
a result.

## Anti-patterns

| Don't | Why |
|---|---|
| Summarize the final answer and call it the debrief | The step counts and classifies; the summary already exists |
| Write a note to fill the step | `no record needed` is a result; a fabricated lesson is noise in a shared vault |
| Copy the unit's own artifacts (PR body, CHANGELOG line) into WC | They already have a home; WC keeps what transfers |
| Record "PR #123 is open" | Transient state; WC notes are read later |
| Ask whether to record | The close authorizes it |
| Write outside WC because the root was unclear | Fail-close: report the blocker instead |

## Done means

- [ ] Ran after the end conditions stood and before the report
- [ ] Counted the unit from commands, not recall
- [ ] Each candidate passed the duplicate, grade, and repetition checks
- [ ] Records committed atomically in WC, or `no record needed` with its reason
- [ ] The report names paths and SHAs, or the reason
