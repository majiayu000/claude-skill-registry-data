---
name: kanso-handoff
description: "Use when the user wants the current session's context packaged for the next one: \"package this session\", \"carry this context over\", \"before I /clear\", \"handoff\", \"save where we are\", \"compact this into a prompt for next time\". Writes one dense, machine-readable file and prints the resume line. Not for durable repo guidance (kanso-context) or permanent solution notes."
argument-hint: "[optional: focus, e.g. \"just the auth work\"]"
allowed-tools: Bash(git *) Bash(rg *) Bash(mkdir *)
---

# kanso-handoff

Packages what this session knows into `.claude/handoff.md` so `/clear` costs nothing. The file is a baton, not a log: each run overwrites the last, the next session reads it and continues, and nothing else is kept.

The audience is the next agent session, not a person. Density beats politeness; a fact the next session must not re-derive beats a paragraph about how it was derived. Everything in `kanso-principles` about earning lines applies double here, because every line of the handoff is paid for at the start of every future turn.

## What goes in

Header first, one line: date, branch, `HEAD` short sha. The next session diffs against this to detect drift since the handoff.

Then these sections, each optional, each tight. `$ARGUMENTS` may narrow the pack to one strand of a mixed session.

| Section | Holds | Rule |
|---|---|---|
| Goal | The task, one or two sentences, user's point of view | Present tense, no history |
| State | Done and verified / done but unverified / not started | Verified means a command ran and passed, nothing softer |
| Decisions | Each with its one-line reason | A decision without the why gets re-litigated next session |
| Files | Load-bearing paths, one line each | Repo-relative; say what each is, not what happened to it |
| Open threads | Numbered next steps, most important first | Imperative, self-contained |
| Dead ends | What was tried and abandoned, and why | Saves the next session from retrying it |
| Verify | Exact commands with expected outcomes | Runnable as written |

## What stays out

- Transcript narration. "We then discussed" is the failure mode; the next session was not there and does not care.
- Anything git already records. The diff is in git; the handoff carries what the diff cannot say.
- **Secrets, always.** No tokens, keys, or credentials, even when they appeared in the session. Name where a secret lives (`op://...`, an env var) rather than what it is.
- Unfounded certainty. Anything not verified is written as unverified.
- Durable knowledge. Repo guidance belongs in AGENTS.md via `kanso-context`; solved-problem notes belong to a memory tool. The handoff dies at the next overwrite.

## The ceiling

150 lines, hard. Context research is unambiguous that long context files degrade the agents reading them. When over, cut in this order: Dead ends, Files detail, State detail. Never cut Decisions or Open threads; those two sections are the reason the file exists.

## The run

1. Distil the session into the format above. Resolve relative dates to absolute. Check the result against the ceiling.
2. `mkdir -p .claude` if needed; write `.claude/handoff.md`, replacing any previous handoff without ceremony.
3. If the repo tracks `.claude/` and `handoff.md` is not ignored, say so once and suggest the `.gitignore` line. Warn, do not block: a committed handoff is untidy, not dangerous.
4. End with exactly this, and no report:

```
Handoff written to .claude/handoff.md (<n> lines). After /clear or in a new session, paste:

Read .claude/handoff.md and continue.
```

## What this skill never does

- Append or archive. One file, overwritten. History is git's job.
- Write a secret into the file, whatever the session contained.
- Pad the pack toward the ceiling. A ten-line handoff for a ten-line session is correct.
- Touch AGENTS.md, CLAUDE.md, or any durable context file.
- Editorialise. The pack states; it does not persuade.
