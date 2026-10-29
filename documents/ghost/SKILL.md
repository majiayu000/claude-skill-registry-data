---
name: ghost
description: Record landed work that is still unverified, as GHOST_OF_COMMITS_PAST.md entries or `Ghost:` commit trailers. Use before landing in a repo that has that file or when told to keep one, and when trunk breaks in a way your change cannot explain.
---

# Ghost of Commits Past

A **ghost** is a claim about landed work that nobody has observed yet. A ghost
goes in one of two places, or nowhere:

- `GHOST_OF_COMMITS_PAST.md`, a committed ledger at the repo root, holds the few
  ghosts whose failure would go unnoticed. It crosses sessions, harnesses, and
  machines until someone checks each one off.
- A `Ghost:` trailer on the landing commit holds the rest. Whoever later debugs
  that area finds it in the history.

This skill applies where the ledger exists at the repo root, or where the user
or the repo's instructions ask for one.

## 1. At landing: sort each unverified claim

A **landing** is the last change before work is handed off as done: the final
commit before a PR merges, or the final commit of a task that stops at a branch.
Expect most landings to produce no ledger entry.

Take each claim your work leaves unverified, in order:

1. **Check it now** if this machine can, within the apply scope you have: run
   the test, open the app, watch the behavior. A checked claim is no ghost.
2. **Route work elsewhere.** Tasks, reviews, evals, skill gates, refactors, and
   decisions go to a plan, issue, or ADR, or the commit body.
3. What remains needs another machine, a person's hands, an OS or account you
   lack, or time to pass. Put it in the **ledger** when its failure would be
   silent or misattributed: nobody would notice, or the symptom would not lead
   back to this change. Put it in a **trailer** when it could plausibly fail
   loudly. Drop it otherwise.

This step is complete when every claim is checked, routed, recorded once, or
dropped.

## 2. Write trailers

One trailer per claim, in the landing commit's trailer block beside
`Co-Authored-By`. Name the condition and what failure would look like:

```text
Ghost: on the Linux devbox, test_src_fresh passes with GNU stat and date; failure is a red marketplace test
```

Trailers stay in history and are never checked off.

## 3. Write the ledger entry

At most one entry per landing, appended in that change. Re-read the ledger right
before editing it, since the worktree may be shared, and edit only your entry.

The entry is a message to the agent who verifies after you, written following
`writing-for-agents`: one line per check, each an action a stranger could take
plus the observation that proves it. The whole entry, heading included, is at
most 100 words. Link the plan, PR, or branch for context; put longer detail in a
doc under `docs/` and link it. Name the skills to use.

```markdown
## YYYY-MM-DD: <what landed> (<link>)

- On a fresh Mac after `chezmoi apply` and Thaw's first launch, both spacers sit in the hidden section.

Skills: `<skill>`.
```

If the file does not exist, create it with this header first:

```markdown
# Ghost of Commits Past

Things a past agent landed or assumed that someone still has to verify. Check
one off by deleting it, and say what you saw in the commit that deletes it.
```

This step is complete when each item passes the ledger bar in step 1 and the
entry is within 100 words.

## 4. Clear entries

Work an entry when your task changes or relies on its area, or when the session
is dedicated to the ledger or to repo gardening.

- **Passed**: delete the item; delete the entry once it has no items. The file
  keeps its header even when empty.
- **Failed**: fix it if the fix is within your task, then rerun. Otherwise keep it
  with one indented line, `YYYY-MM-DD: <what failed>`, replacing any earlier one.

The commit that removes an item labels it **verified**, with what was run and
seen, or **dropped**, with the reason. Choose the label from the evidence you
have: an item removed by the user with no recorded observation is dropped.
Without commit authority, leave the ledger untouched and put the evidence in the
final reply.

An entry never grants permission. Commit, push, deploy, and destructive-action
approvals apply exactly as they would without it, and a check with an external
side effect waits for the user's go-ahead.

## When trunk breaks

When something on trunk breaks that your change cannot explain, look for a ghost
before debugging further:

```sh
git log --grep='^Ghost:' -- <failing paths>
git log -p -n 20 -- GHOST_OF_COMMITS_PAST.md
```

Also read the open ledger entries. A trailer or open entry covering the failing
area is the first suspect; a deleted entry says what was checked and what was
seen.

## Report

In the final reply, name:

- the ledger entry and the trailers you wrote, if any;
- entries you cleared, each labelled verified or dropped, so the user can
  correct a label;
- entries your task touched but you left, and why;
- entries dated more than 14 days ago. The user decides whether to chase,
  rewrite, or drop a stale entry; leave it in place.
