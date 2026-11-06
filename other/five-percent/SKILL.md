---
description: >-
  Ask of a branch's diff what it took as given, down to whether what it edits
  should exist, and post at most three alternative approaches as one review on
  its PR, each inline and graded critical or optional — editing and committing
  nothing. The third `/polish` pass; on its own, `/five-percent [<branch|#PR>]`.
  Use when the operator asks what the change took for granted, or for "the five
  percent".
---

**The pass runs in a fresh subagent, never in the session that wrote the
change**, for `@.claude/skills/polish/SKILL.md`'s reason: the author reads the
diff with the frame that produced it, and the frame is what the pass looks for.
Inside `/polish` that subagent is `/polish`'s own, which loads the procedure as
its third pass, so this file launches one only where no `/polish` is running:

- **`@.claude/skills/go/SKILL.md` Step 4**, on a branch that had no PR when Step
  3 polished it — the pass deferred there, and runs once `/pr` has made one.
- **On the operator's ask**, `/five-percent [<branch|#PR>]` — a target names the
  PR to read, without attaching to it.

Launch one `general-purpose` subagent, in the foreground, whose prompt carries
`@.claude/skills/five-percent/procedure.md` to load and follow, the PR's number,
and the plan under `docs/plans/` when the branch has one — nothing about what
was built or why. Relay its one-line report.

**The proposals are the operator's from the moment they post.** This session
does not act on one, answer it or resolve its thread; an answered proposal
becomes work through `@.claude/skills/handle/SKILL.md`, in a session opened for
it.
