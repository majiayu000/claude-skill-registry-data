---
name: session-summary
description: "User-invoked session handoff. `/session-summary pause` writes a structured resume file capturing what the session was doing, what changed, what was decided, and what is unfinished, folding any summary already there into a shorter form above it. `/session-summary resume` reads that file back and reports it as a few bullets, without starting any work it names. Invoked explicitly by name only. Never write or read the resume file on your own initiative, and never at the end of an ordinary task."
user-invocable: true
---

# session-summary

**Carry a work stream across restarts. `pause` writes the handoff; `resume` reads it back.**

This skill is explicit-invoke only. A session ending, a task finishing, or a context window filling up are not triggers on their own.

## Invocation

```
/session-summary pause     # write the handoff
/session-summary resume    # read it back and report it
```

An invocation with no argument, or an unrecognized one, is a request to say which of the two was meant rather than to guess. Writing a handoff when the user wanted to read one destroys the file they were asking for.

## The file

```
.agents/session-resume/resume.md
```

One file, holding the current session at the top and the sessions before it, compressed, below. Create the directories if they are missing.

`.agents/` is already excluded from git in a project `claudex apply` has been run in, so the file never reaches a commit. Outside such a project, write it anyway and say in one line that the path is not excluded, so the user can decide before it shows up in `git status`.

## pause

### The budget

The whole file runs to about 5,000 tokens. That budget is available and using it is fine; padding to reach it is not.

**No file exists yet.** The whole budget belongs to this session.

**A file already exists.** The write is additive. What is there is rewritten shorter to make room, and this session goes in above it, because the value of the file is a continuous work stream rather than a snapshot of the newest session alone. The split depends on how much this session did against what is already recorded.

| This session | Already recorded | This session gets |
|---|---|---|
| Substantial: its own branch, its own decisions, work still open | 30-40% | 60-70% |
| Small: a follow-up, a fix, a few files, a question answered | 50-60% | 40-50% |

Compression is rewriting, not truncation. What survives is the decisions, the rejected approaches, the user's rulings, and the identifiers a future session would have to rediscover. What goes first is the step-by-step of how something finished got finished, since a completed feature does not need its history retold. When several prior sessions are already stacked, they share that one allowance and the oldest loses detail first.

### How long this session's part should be

- **Finished**: the outcome, where it landed, and the decisions worth not re-litigating. Usually a few hundred words.
- **Unfinished**: everything a fresh session would otherwise have to rediscover, meaning the exact state of the last thing tried, the commands that worked, the paths in flight, and the approaches already ruled out. This is where the budget goes, because rediscovering it costs far more than writing it down.
- **Blocked**: as above, plus what the block is and what would clear it.

### Structure

```markdown
# Session resume: <one line naming the work>

## State
<complete | in progress | blocked> - one sentence.

## What we set out to do
The task as the user framed it, including constraints they stated.

## Where it landed
Branch, PR, files changed, commands that worked. Exact names and paths.

## Decisions
What was decided and why. Include what was considered and rejected, and
anything the user overruled, with their reason.

## Open
Only when the state is not complete: what is unfinished, what has been
tried, what the next step is.

## Specifics to carry forward
Paths, commands, IDs, URLs, flags, versions - verbatim.

---

# Earlier: <one line naming it> (<state>)
The compressed form of what the file already held, newest first.
```

Drop a section that has nothing real in it. An empty heading reads as a gap in the work rather than as an omission in the summary.

### Rules

Record only what happened. An invented detail is worse than a missing one, because the next session acts on it without knowing to check.

Quote commands, paths, and identifiers verbatim rather than describing them. A resumed session will paste them, and a paraphrased command fails in a way that is slow to diagnose.

Keep rejected approaches and the reason they were rejected. Re-deriving a discarded approach is the most common way a resumed session wastes its first half hour.

Keep decisions the user overruled, in their words. Those are the ones a fresh session is most likely to walk back into.

Write the state of the work, not the story of the session. The order things were tried in rarely matters; what is true now always does.

Say what is uncertain when something is uncertain, rather than presenting a guess as settled. A summary that reads as more resolved than the work actually is sends the next session off confidently in the wrong direction.

### Reporting

After writing, report the path and the state in one line. The file's content does not need repeating back, because the user is about to restart rather than read it in this session.

## resume

Read `.agents/session-resume/resume.md`, then report it as 3 to 5 short bullets and stop there. One bullet each for what was done, what state it is in, and what is left over is the whole of it.

```
- Landed the comment-rule narrowing on `fix/comment-rules`, PR #32, merged.
- `main` is at `2fb2e47`, tree clean.
- Left over: `cmd/launch.go:26-27` still wrapped across two lines, unruled.
- The local checkout runs the pre-merge rules until the binary is rebuilt.
```

Resuming reads context in and nothing else. The file names unfinished work because a future session may need it, not because reading the file is permission to start it. Picking up a task listed there, opening the files it mentions, or running the next step it describes all wait for the user to ask in this session.

When the file is missing, say so and stop. There is nothing to reconstruct, and inferring the previous session from the repository produces a confident summary of the wrong thing.
