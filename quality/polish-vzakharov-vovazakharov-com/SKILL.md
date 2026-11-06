---
description: >-
  Run the standard quality passes over work just done — `/dry`, then
  `/tend-prose`, committing what they change, then `/five-percent`, posting its
  alternatives as a PR review — scoped to what the branch has changed since it
  was last polished. These are the passes `/go` runs at its
  Step 3; this skill is how work that never went through `/go` gets them. Invoke
  as `/polish [focus guidance]`, or `/polish full` to re-read the branch's whole
  diff against its base rather than only what it changed since the last polish
  commit.
  Use when the operator says "polish this", "tidy this up", or "run the checks
  that come after `/go`".
---

**The passes run in a fresh subagent, never in the session that loads this
skill.** That session is usually the work's author, reading the diff with the
change's history in mind, so a comment narrating the edit, or two blocks it
remembers as different, reads fine to it and not to a reviewer. A subagent has
only the diff and the plan, as the reviewer will.

So launch one `general-purpose` subagent, in the foreground
(`run_in_background: false`) since it edits, commits and pushes the working
tree, and touch nothing until it returns. Its prompt carries:

- `@.claude/skills/polish/passes.md`, to load and follow — the whole procedure,
  which this session does not read;
- the argument, verbatim;
- the plan under `docs/plans/`, when the branch has one, as the record of
  intent.

Nothing else: no account of what was built or why.

**It reports, and the session relays.** Answer the intent questions this
session's context settles and act on them, committed under the type the edit
would carry anyway: a `polish:` subject would put the edit below the next run's
floor (`passes.md` § "The floor"), unreviewed. The rest go to the operator with
`/dry`'s calls.

**Putting back what a run changed, on the operator's ask, is itself a `polish:`
commit** — `polish: restore <what>`. That run already read what it restores, so
the commit becoming the next run's floor keeps the cut from being made again. It
goes straight on top of the run: anything committed in between would sink below
the floor with it, unreviewed.

## Where it runs

- **`@.claude/skills/go/SKILL.md` Step 3** — after implementing, before the PR.
- **`@.claude/skills/finalize/SKILL.md`, ahead of its numbered steps** — the
  backstop for work that reached a PR without passing through `/go`. That skill
  owns why it goes first.
- **On the operator's ask**, at any point in a session — the entry the other two
  exist to make unnecessary and routinely don't. A task asked for and done
  directly ends with the passes unrun unless someone names them.
- **`@.claude/skills/update-muthur/SKILL.md` Step 8**, over a port.
