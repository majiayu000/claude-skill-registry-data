---
name: handoff
description: Write a curated, size-capped handoff file that carries task state from this session to a fresh one. Run only when the user invokes /handoff.
license: MIT
disable-model-invocation: true
---

# Handoff

Write one live file, `.agent-output/handoff.md`, so a fresh session can pick up this
task where it stopped. Overwrite any previous handoff. The file holds task state only,
not durable facts: those belong in the harness's memory feature.

## 1. Check that the path is ignored

A handoff can hold proprietary context, so never write it to a path git would stage.
Run this before the first write, from inside the repository:

```bash
git check-ignore -q .agent-output/handoff.md
```

- **Exit 0 (ignored):** continue to step 2.
- **Exit 1 (not ignored):** stop and ask which the user prefers. Write nothing until they
  answer.
  - **A.** Create `.agent-output/` and add `.agent-output/` to the repository's
    `.gitignore`. This is a tracked change that every contributor receives.
  - **B.** Append `.agent-output/` to the file printed by
    `git rev-parse --git-path info/exclude`. This is untracked and applies to this clone
    only.
- **Not a git repository** (the command reports that): continue to step 2. There is
  nothing to ignore.

## 2. Gather the header facts

- Timestamp: `date -u +%Y-%m-%dT%H:%M:%SZ`
- Branch: `git symbolic-ref --short -q HEAD`. If that prints nothing, use `(detached)`.
  Outside a git repository, use `(none)`.

## 3. Write the file

Create `.agent-output/` if it does not exist, then write the file in this shape. The
header lines must keep this exact form, because the session-start hook reads the
`Branch:` line.

```markdown
# Handoff

Written: <timestamp>
Branch: <branch>

## Goal and current state
## Decisions
## Gotchas and dead ends
## Next step
## In-flight work
## Open questions
```

- **Goal and current state:** what the task is and how far it got.
- **Decisions:** each decision with the reason for it.
- **Gotchas and dead ends:** approaches already tried and why they failed.
- **Next step:** the exact next action, specific enough to start without re-deriving it.
- **In-flight work:** uncommitted or half-done changes, by file.
- **Open questions:** what still needs an answer, and from whom.

Rules:

- Keep the whole file to about 100 lines. Cut to fit.
- Leave out anything a fresh session can derive from `git log`, `git diff`, or the code.
- Leave out durable facts and preferences. They belong in memory, not here.
- Never include credentials, tokens, or secrets.
- Omit a section only if it is truly empty. Write `None` rather than inventing content.

## 4. Report back

Tell the user the path, the line count, and that the file is meant to be reviewed before
use. Suggest `/clear` when they are ready to continue in a fresh session. Do not run it
for them.
