---
name: wrap-up
description: |
  Session-closeout audit — check for unfinished work before ending a conversation, then give a
  clear verdict. ALWAYS use this skill when the user asks "can we close this chat?", "is there
  anything else left for us to do?", "are we done?", "anything outstanding?", "safe to close?",
  "wrap up", or any variation of wanting to end the session and confirm nothing is left hanging.
  Distinct from `reflect`, which saves lessons to the knowledge base — wrap-up only reports what
  is unfinished and writes nothing.
license: MIT
metadata:
  author: Nicholas Sollazzo
  version: "3.0.0"
---

# Wrap-Up

Audit the session for loose ends, then deliver a verdict in the format below. Be honest — a missed loose end discovered tomorrow is worse than one more row in the table.

## 1. Load the output rules

Apply this kit's `answer-first` rules to this skill's output — in its **single-reply mode**:
verdict first, no preamble, no recap, no closers, cap lists at 5, matter-of-fact tone. Load
`answer-first/SKILL.md` from this kit and follow its Rules section. Do **not** adopt its session
persistence — the user asked to close a chat, not to change your format from here on.

## 2. Audit (silent — none of this goes in the reply)

**Scope: THIS conversation only.** Every item you report must trace to something
done, touched, or promised in this chat. Pre-existing state — dirty files you
didn't edit, PRs you didn't open or work on, other people's branches, project
backlog, memory-file TODOs, recalled `<system-reminder>` context — is OUT OF
SCOPE even when it looks urgent. If you can't point at the turn in this session
that created or committed to it, it does not go in the table. Mentioning it
anyway is the failure mode this rule exists to prevent.

Verify with commands, don't recall from memory:

1. **In-flight work** — subagents, background shells, workflows, monitors, scheduled wakeups *started in this session*. Pending task notifications count as unfinished.
2. **Git** — `git status` + `git log @{u}..`, filtered to paths this session edited and commits this session authored. Ignore unrelated dirty files and pre-existing unpushed commits.
3. **PRs** — only PRs opened, pushed to, reviewed, or babysat in this session. CI running? Review pending? Merged but deploy unverified?
4. **Promised-but-undone** — scan this conversation for "I'll do X", deferred requests, agreed follow-ups not executed.
5. **Knowledge worth persisting** — did this session produce a non-obvious lesson, gotcha, or decision that isn't captured anywhere? Do NOT triage or write it here. If yes, it becomes ONE table row: Item `unsaved session lessons`, State `now`, Fix `run reflect`. The `reflect` skill owns classification, targets, and the approval gate.

If unrelated state is genuinely alarming (e.g. a destructive uncommitted change
you didn't make), it gets at most one line under the table prefixed
`FYI (not this session):` — never a numbered row, never in the count.

## 3. Verdict — use one of these two shapes verbatim

Hard cap: **12 lines total**. No intro sentence. No "I checked X, Y, Z." No closing offer.

### Nothing outstanding

```
SAFE TO CLOSE — <what the session shipped, ≤12 words>
```

One line. Stop there.

### Items remain

```
NOT DONE — <N> open

| # | Item | State | Fix |
|---|------|-------|-----|
| 1 | <≤6 words> | now / safe / you | <≤8 words> |

Next: <one action, under 2 minutes>
```

- Max **5 rows**, most urgent first. More than 5 → keep the top 5, add one line: `+<N> minor (ask to list)`.
- `State` is exactly one of:
  - `now` — quick, I can do it this turn
  - `safe` — survives the session ending (bot-babysat PR, running cron), no action needed
  - `you` — only the user can decide or act
- `Next:` names ONE thing. If any `now` rows exist, it's an offer to run them — propose, never auto-execute.

Nothing else. No paragraph explaining the table.
