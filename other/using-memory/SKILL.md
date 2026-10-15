---
name: using-memory
description: Use when working with the auto-memory system. What goes in / stays out / how to update.
---

# Using the auto-memory system

The harness on this machine maintains a memory directory at
`~/.claude/projects/<project-slug>/memory/`.
`MEMORY.md` inside that directory is the index. Individual memory files live alongside it. Memory is loaded into Claude's context at session start - so its quality directly affects every future answer.

## When to trigger
- The user states a durable preference, role, or working style.
- The user corrects something Claude got wrong and wants the correction to stick.
- A project-specific fact emerges that is not in CLAUDE.md (and should not be, e.g. machine paths).
- You hit a piece of memory that is wrong or stale.

## What belongs in memory

Four categories. Use the same tags as filenames or front-matter so future-you can sort them.

- **user** - the user's role, preferences, working style, recurring conventions. Example: "Prefers terse PR descriptions, no emojis."
- **feedback** - corrections from past sessions. Example: "When asked to 'run tests', means the integration suite, not unit tests."
- **project** - long-lived facts about a specific project that are not yet in its CLAUDE.md. Example: "The `analytics` service deploys via the `legacy` pipeline, not Argo."
- **reference** - pointers to external resources Claude should consult. Example: "Internal API docs at https://wiki.example.com/api - requires VPN."

Memory entries are short. One claim per entry, with enough context to be useful out of session.

## What does NOT belong in memory

- **Code patterns.** If you want to remember "use repository pattern", that lives in CLAUDE.md or a skill. Code patterns rot. Read the code.
- **Git history.** Use `git log`. Do not duplicate commit messages into memory.
- **Ephemeral state.** "Currently debugging issue X" - this dies with the session, not in long-term memory.
- **Anything CLAUDE.md already covers.** Project conventions go in CLAUDE.md; user preferences go in memory. Do not duplicate.
- **Secrets.** Tokens, keys, passwords - never. Memory files are plain text on disk.
- **Speculation.** Only record observations or stated preferences, not guesses about what the user "probably wants".

## Conflicts: file state wins

When memory contradicts the actual codebase or settings on disk, treat the file as truth. The memory entry is stale.

- Verify the file/setting.
- If file wins, update or delete the memory entry to match.
- If memory wins (rare - it usually means the file was changed by accident), confirm with the user before "fixing" the file.

Never act on a stale memory entry without re-confirming against the file.

## Updating memory

The harness writes most entries automatically, but you can and should edit them when:

- You discover an entry is wrong. Fix it now, not later.
- An entry is too vague to be useful. Rewrite with specifics.
- An entry has been superseded by a newer fact. Either edit in place or delete and add a new one.

Edit with the `Edit` tool against the absolute memory path. Keep entries short and dated when the time matters ("As of 2026-03, the staging cluster is in us-east-2").

## Expiry

Memory entries do not have a TTL. You are the GC.

- Any time you notice an entry is no longer true, delete it.
- Any time you read a memory file and think "this is irrelevant now", delete it.
- Better empty than wrong.

## Working with `MEMORY.md`

`MEMORY.md` is the index Claude scans first. Keep it tight:

- One line per memory file: filename + a 5-10 word summary of what it contains.
- Group by category (user / feedback / project / reference).
- Sort by recency or relevance, not alphabetically - newest at top is fine.

Do not put long content directly in `MEMORY.md`. Put it in a sub-file and reference it from the index.

## Workflow when adding a new entry

1. Decide the category. If you cannot, it probably does not belong in memory.
2. Look for an existing file in that category. If one fits, append to it; do not spray new files.
3. Write the entry as a single short paragraph or bullet. State the claim, then the context.
4. Update `MEMORY.md` if you created a new file.

## Workflow when reading memory

1. Trust the index, but verify load-bearing claims against current files.
2. If a claim looks wrong, do not pretend you did not see it - investigate.
3. Quote memory claims back to the user only when relevant to the current task. Do not narrate the entire memory dump.

## Red flags

- A memory file over ~200 lines. Split or prune.
- Two entries that contradict each other. Resolve immediately - the user is getting inconsistent answers across sessions.
- Memory entries that read like a journal ("Today we worked on ..."). Either extract a durable fact or delete.
- Memory entries quoting code blocks. Move to a skill or CLAUDE.md.
- Memory entries that duplicate CLAUDE.md content. Pick one home and link the other.
- Entries with no context, e.g. just "yes" or "use option B" - meaningless out of session. Rewrite with the surrounding decision.

## References

- Memory directory: `~/.claude/projects/<project-slug>/memory/`
- Index file: `MEMORY.md` in that directory.
- `skill-creator` - durable behavioral guidance often belongs in a skill, not memory.
- `lean-context` - memory loads into every session, so keep it as small as possible.
