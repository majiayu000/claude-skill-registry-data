---
name: write-commit
description: Writes a commit message in the repo's own convention, validated and saved to .workflow/<KEY>/commit.txt. Use when asked to commit, or to write or fix a commit message.
---

# write-commit

```
wb <args>    # wb not on PATH: python <this skill's directory>/../../lib/wb.py <args>
```

This skill writes the message. Committing stays the user's call: the CLI prints
the command and runs it only for an explicit `--execute`.

## Steps

1. **Learn the house style.** `commit convention`. It reports what this repo
   already does — conventional commits, ticket-prefixed subjects, or free-form —
   from its own history, plus the author identity and whether it matches the
   context. Follow it; a message in a different style is noise in the log
   forever. If it reports `free-form` and the team has decided to adopt a style,
   record it once with `commit convention --set <style>` — do not impose one
   silently.

2. **See what changed.** `git diff` for the files, `review context` if you need
   the zones. If a plan exists: `sdd get <KEY> --section summary` gives the
   objective in one line.

3. **Write it.**
   - Subject: imperative, specific, under 72 characters, no trailing period.
     "fix expired coupon charging the card" — not "fixes" and not "bug fix".
   - Body, when the change is not self-evident: **why**, not what. The diff
     already says what. Wrap at 72.
   - Reference the ticket key if the repo's history does.
   - `BREAKING CHANGE:` in the body if a contract changed.

4. **Check it.** Write the draft to a file, then
   `commit check --file <path> --key <KEY>`. On pass with a key it is saved to
   `.workflow/<KEY>/commit.txt`; on failure nothing is saved and the reasons
   are listed. Fix the message, not the check.

5. **Hand it over.** Show the message. `git commit <KEY>` prints the exact
   commit command, carrying the saved message and the author the context
   expects; add `--execute` only if the user asked you to commit. It refuses on
   a protected branch and with nothing staged — choosing what goes in a commit
   stays theirs.

## Rules

- **One logical change per commit.** If the subject needs an "and", it is
  probably two commits.
- **Never describe what you did not do.** No "add tests" in the subject when no
  test file changed.
- **No unfinished markers.** `wip`, `fixup!` and `squash!` are rejected.
- **Never put a credential in a message.** The check refuses anything that looks
  like one.
