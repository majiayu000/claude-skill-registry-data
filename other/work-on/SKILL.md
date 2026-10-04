---
name: work-on
description: Carry a spec or tickets through implementation, polish, and PRs in one workflow.
argument-hint: "[--no-pr] [--ship]"
disable-model-invocation: true
---

You **author** a workflow and report on what it returns. The work is the spec or tickets the user has provided; each **work item** runs through the **chain** in its own agents, and your context holds only the results.

`--ship` needs a PR: refuse it alongside `--no-pr`.

## 1. Map the work

Each ticket is one work item, with the spec as context when there is one. A spec without tickets is one work item.

Find each work item's **blockers** per `/supervise`'s frontier rules. A blocker is **done** when its PR has merged; one outside the batch that is not done keeps its dependents blocked.

Done when every work item is on the **frontier** or names every blocker it waits on.

## 2. Author the script

Read the `SKILL.md` of `/polish` and `/ship-it`, and ship-it's `references/judge.md`. They are the source of truth for their stages: the script encodes their orchestration.

### Translation

Workflow agents are **leaves**: they have no Agent tool and no way to reach the user. So the script makes every dispatch, and each brief answers the questions its skill would put to the user.

- Each sub-agent a skill dispatches becomes an `agent()` call, briefed as the skill says.
- The skill's own orchestrator work (polish's scoping, triage, and round planning; ship-it's readiness check and acting on the verdict) becomes an `agent()` call that returns its result through a schema.
- The skill's loops, exits, and carried state become script control flow. Polish's ledger and fixtures live in the script and ride into every brief that needs them.
- Polish's `/mattpocock-skills:code-review` pass becomes two parallel `agent()` calls, one for its Spec axis and one for its Standards axis, each briefed per that skill.

Every brief names the work item, its worktree and branch, the spec, and the skill step it performs, so the agent reads that step at the source.

### The chain

Each work item runs in one worktree on its own branch, cut from the freshly fetched base when the work item starts. `isolation: 'worktree'` gives each agent a fresh tree, so it cannot carry a work item across stages.

For each work item, in order:

1. **Implement.** Use `/mattpocock-skills:tdd` where possible. The seams the spec names count as agreed; where it names none, the agent picks them and reports its choice. Run typechecking and single test files regularly, and the full test suite once at the end. Commit to the work item's branch.
2. **Polish.** `/polish`, translated, with the work item as its spec.
3. **Open the PR**, unless `--no-pr`. `/open-pr --capture --annotate`, as a draft when polish left an **ask** open.
4. **Ship**, with `--ship` and a PR that is not a draft. Wait for checks; when one fails, an agent fixes it and pushes, then wait again, for at most 2 fixes. Then `/ship-it --comment`, translated, with polish's report as its evidence.

A stage that fails ends its work item's chain.

### Scheduling

Start every work item on the frontier at once. With `--ship`, when a work item merges, start each work item whose blockers are now all done.

### Return

Per work item: its outcome (merged, held, not ready, draft, PR open, branch only, failed at a stage, or still blocked), its PR or branch, and every stage's report, including polish's report and the judge's verdict.

Done when the script carries the chain, the scheduling, and the return for every work item.

## 3. Launch

Run Workflow with the script, passing the work items and their blockers in `args`.

Done when the workflow returns.

## 4. Report

- One line per work item: its id, outcome, and PR or branch. A failure names the stage and why.
- `## Needs you`: grouped by work item with its PR. Polish's asks with their candidate fixes, recommendation first; polish's defers; ship-it's holds with their citations; and each **not ready** PR's failing conditions.

Then stop.
