---
description: Write down where this stretch of work stopped, so the next session continues instead of restarting. Use at the end of a working session, or when handing the repository to someone else.
disable-model-invocation: true
---

# Record where this session got to

A session record answers one question for whoever opens this repository next: **what was in
flight, and what was in the way.** It is not a diary and it is not a changelog — the commit history
already covers what happened.

## When to write one

At the end of a stretch of work that did not finish. That is the case worth recording.

Do not write one when the work completed cleanly and left nothing outstanding — an empty record is
worse than none, because the next session reads it and learns nothing while paying for it.

One record per session. If you are updating something you wrote earlier in the same session,
edit that file rather than adding a second.

## Where it goes

```
.chamnan/sessions/YYYY-MM-DD-short-slug.md
```

The date first, so the directory sorts chronologically and the newest record is the last line of
an `ls`. The slug is a few words about the task, lowercase and hyphenated.

This is **not** `STATE.md`, and the difference matters:

| | |
|---|---|
| `.chamnan/STATE.md` | one file, overwritten. What is true about this repository's work **right now**. |
| `.chamnan/sessions/` | many files, kept. Where **a particular session** got to and what it left. |

Update `STATE.md` if the picture of current work changed. Write a session record if a stretch of
work stopped partway. They are often both, and they are not the same file.

## The format

```markdown
# Short title of what you were doing

## Done
- What actually landed. One line each.

## Remaining
- What was next, specifically enough to pick up cold.

## Files
- `path/to/file.py` — what changed in it, in a few words

## Decisions
- What was decided and **why**. The why is the part that is expensive to reconstruct.

## Blockers
- What stopped progress, and what would unblock it.
```

Every heading is optional except the title. Leave out a section rather than filling it with a dash.

## Write the identifiers out, every time

The one rule worth following even when it feels pedantic. A session record's whole job is to survive
a gap — a compaction, a night, a different machine — and what a compaction destroys is specifically
the identifiers. Measured: an LLM summarization pass recovers about **63% of facts**, and the named
failure is paraphrase — `src/middleware/auth.ts:52` comes back as "the auth middleware file", and
`Error: ECONNREFUSED 127.0.0.1:5432` as "a database connection error". The sentence still reads
correctly. The navigation is gone, and so is the ability to search for it.

So write the thing itself, not a description of it:

| write | not |
|---|---|
| `src/cascade.py:214`, in `run_cloud_pool_cascade` | "the cascade timeout code" |
| `npm run test:integration -- --grep auth` | "the integration tests" |
| commit `a29362d` | "the churn ranking change" |
| `ECONNREFUSED 127.0.0.1:5432` | "a connection error" |
| 8,878 bytes of a 9,000-byte ceiling | "close to the limit" |

An exact string can be grepped by the next session. A paraphrase can only be guessed at, and it
survives summarization looking like it is still useful, which is worse than being dropped.

**Only `## Remaining` and `## Blockers` are injected into the next session**, along with the title
and date. Everything else is there for a person reading the file. So put real content under those
two headings and keep them specific: "finish the parser" is not something a cold session can act
on; "`extract_regex` returns the wrong arg list for Kotlin extension functions — see the failing
check in tests/run_tests.py" is.

## What not to put in it

- **No credentials, tokens, hostnames or connection strings.** These files are committed. The
  session-start hook redacts what it injects, but that does not clean the file on disk.
- No pasted conversation. Write the conclusion, not the transcript.
- No file contents. Name the file and say what changed.

## Housekeeping

Records older than `session_retention_days` (30 by default) are deleted automatically the next
time `chamnan-map` or `chamnan-report` runs. Raise it in `.chamnan/config.json` if a longer memory
is useful, or set `"resume": false` to switch the whole thing off.
