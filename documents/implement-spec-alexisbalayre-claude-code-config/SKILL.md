---
name: implement-spec
description: "Implement the result of /to-spec and /to-tickets in code."
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The tickets live in the configured tracker (IDs from `.env`), or under `docs/plans/<feature-slug>/issues/` when there is no tracker (see `/to-tickets`). If you can't find them, ask the user. `docs/plans/` is never committed, so it exists only in the main checkout: point subagents at it by absolute path.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Steps

1. Read the spec and tickets to understand the task graph.

2. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets - relevant codebase files or external documentation. Ensure the exploration subagent can save files - it should save its markdown notes in a directory outside the repo, accessible by all future subagents. This lets **implementer subagents** focus on implementation rather than exploration.

3. Create the integration branch with `scripts/worktree-create.sh <spec-slug>`. After the first merge in step 5 (a branch with no commits ahead of the trunk can't open a PR), push it and open a **draft** PR marked as closing the spec and tickets. Call the Skill tool with `pr-description` for its title and body only, then open it yourself with `gh pr create --draft`: `pr-description`'s own create step opens a ready PR, which the CI review bills on every push. The CI review skips drafts, so it runs once step 8 marks the PR ready.

4. Use **implementer subagents** to implement each ticket, each in its own worktree on its own branch: `scripts/worktree-create.sh <ticket-slug>`, run from the integration worktree, branches from the integration branch. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and fast-forwards onto it (`git merge --ff-only <integration-branch>`) if not;
   - calls the Skill tool with `tdd` to build the ticket;
   - commits its work on its own branch;
   - merges the integration branch tip into its own branch before reporting done

5. Once an **implementer subagent** completes, merge its work to the integration branch with a **merger subagent**, then push the integration branch. Run mergers one at a time: two in the same integration worktree collide.

6. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. This allows for maximum concurrency.

7. Once all tickets are complete, review the integration branch's diff against the spec and tickets yourself: every acceptance criterion met, nothing built beyond them. Fix any gap in a single **implementer subagent**.

8. Push the integration branch and mark the draft PR ready for review, which starts the CI review (`pr-ci-review`). Wait for it (`gh pr checks <number> --watch`), fix the important findings in the review it posts (that review's, not other comments on the PR) in a single **implementer subagent**, and push. Then resolve each ticket the way the issue tracker closes work.

9. From the integration worktree, where their branches are merged, clean up every **implementer subagent** worktree (`git worktree remove`) and its branch (`git branch -d`).
