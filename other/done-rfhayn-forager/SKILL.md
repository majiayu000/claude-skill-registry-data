---
name: done
description: "Wrap up work on a milestone or session. Chains review → journal → commit → PR → milestone-complete. Interactive — each step asks before proceeding. TRIGGER when the user says \"done\", \"I'm done\", \"wrap up\", \"finish up\", \"all done\", \"ship it\", \"let's wrap\", \"ready to merge\", or any request to complete and finalize work."
---

# Done — Wrap Up Work

Run each step in order. Present the output of each step and ask the user before proceeding to the next. Any step can be skipped.

## Step 1: Review

Run `/review` to check for convention violations, code quality, and documentation currency.

**If review finds issues**: Stop the chain. Tell the user what needs to be fixed. They can re-run `/done` after fixing.

**If review passes**: Show the summary and ask: "Review passed. Continue to journal entry? (y/skip)"

## Step 2: Development Journal

Run `/dev-journal` to write or update today's session narrative.

Show the journal entry preview and ask: "Journal updated. Continue to commit? (y/skip)"

## Step 3: Commit

Run `/commit` to create a commit following project conventions.

Show the commit message and ask: "Committed. Continue to create PR? (y/skip)"

## Step 4: Pull Request

Run `/pr` to create a pull request with the project format.

Show the PR URL and ask: "PR created. Is this a full milestone completion? (y/skip)"

If the user says skip, jump to Step 6 (release) — they're done with the session but the milestone isn't complete.

## Step 5: Milestone Complete

Run `/milestone-complete [<identifier>]` (accepts both legacy `M#.#.#` and new OpenSpec change-ids via shared utility at `.claude/skills/_shared/milestone-format.sh`) to:
- Update `docs/current-story.md` with completion
- Clean up the branch-specific next-prompt file
- Update the priority queue

Show the updates and confirm completion.

## Summary

After completing (or skipping) all steps, show:

```
Session Wrap-Up
===============
✓ Review:     [passed / skipped / issues found]
✓ Journal:    [updated / skipped]
✓ Commit:     [hash] [message first line] / skipped
✓ PR:         [URL] / skipped
✓ Milestone:  [completed / skipped]

[Any remaining notes or follow-up items]
```

## Rules

- **Review failures stop the chain** — don't commit code that fails review
- **Each step is optional** — the user can skip any step
- **Don't push without asking** — `/commit` creates but does not push
- **Journal before commit** — ensures the journal is captured in the commit
