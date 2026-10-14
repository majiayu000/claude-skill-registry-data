---
name: craft-pr-stack
description: Opening a pull request on top of one that has not merged. When a stack earns its merge order, how to rebase a child, and where the child lands when the parent merges.
---

# Skill: Craft PR Stack

> "A stack is a merge order. Impose one only where the work already has one."

## When

| Stack | Branch from `main` |
|---|---|
| The second change needs the first | Neither needs the other |
| Both edit a file every change edits — manifest, lockfile, changelog | They touch different files |

On that second row a green gate is not evidence: each branch passes alone while the merge of both is
wrong.

A stack imposes a merge order, and an order nobody needs is one somebody has to wait for.

## The Protocol

Branch from the open PR you depend on, and target it. Do not branch from `main` and wait.

```bash
gh pr create --base <parent-branch>
```

When the parent moves, replay the child's own commits onto it:

```bash
git rebase --onto <parent-branch> <old-parent-tip> <child-branch>
git push --force-with-lease origin <child-branch>
```

Once the parent is rewritten, nothing computes `<old-parent-tip>`. Read it from the reflog:
`git rev-parse <parent-branch>@{1}`, or `origin/<parent-branch>@{1}` if someone else force-pushed.

## The Landing

Everything above is git and holds anywhere. This section is one forge's behaviour, and the commands
are `gh`. Confirm it on any other before relying on it.

**Merging a parent does not move its children.** The base branch survives the merge, the child stays
aimed at it, and merging the child lands the work on a stale branch instead of the trunk.

**Deleting the base does not move them either — it closes them.** Seen in practice: a base deleted,
and one second later the child closed, still aimed at it. GitHub documents an auto-retarget. Do not
spend a pull request finding out when it applies.

So retarget every child first. Delete the parent branch after, or not at all:

```bash
gh pr edit <child> --base main
```

Then read back where it went. A merge reports that it succeeded, never which branch it succeeded
into:

```bash
gh pr view <child> --json baseRefName,mergedAt
```

## The Anti-Patterns

| Don't | Do | Why |
|---|---|---|
| Merge the parent into the child | Rebase the child onto the parent | A merge puts the parent's diff in the child's review |
| Stack to keep a PR small | Split only what can merge alone | Size is not the virtue. Independence is |
| Add a branch to a waiting stack | Land the bottom first | Every parent rewrite rebases everything above it |
