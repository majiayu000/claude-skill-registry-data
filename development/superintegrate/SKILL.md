---
name: superintegrate
description: "Integrate code-complete superRA work. Requires superRA:using-superra. Use for result protection, base sync, codebase-fit refactors, permanent records, cleanup, or PR preparation."
---

# superintegrate — the INTEGRATE phase

Takes a reproducibility-verified branch through five steps:

```
Protect              -> choose results, permanent documentation, and protection
Sync                 -> bring the branch onto the current base via semantic-merge
Mature & Consolidate -> write the permanent record, mature the task tree, and
                        review both into one temporary refactoring task
Integrate            -> approve, execute, and verify that refactoring task
Finish               -> final freshness check, PR or fast-forward, and cleanup

Any step -> superplan §User Feedback and Changing the Task Tree
           when scope, methodology, task structure, or task status changes materially
```

**Announce at start:** "I'm using the superintegrate skill to prepare this work for integration."

## Step References

Load each step's reference on entry — each is self-contained:

| Step | Load |
|---|---|
| Protect | `references/protect.md` |
| Sync | `references/sync.md` |
| Mature & Consolidate | `references/mature-consolidate.md` |
| Integrate | `references/integrate.md` |
| Finish | `references/finish.md` |

## Stop Points

Run the entered step's local gates; never redo task-local approvals outside the affected frontier. No progress checkboxes — progress is recovered from commits and task statuses. INTEGRATE is one multi-step phase, so commit subjects carry the step in scope per `using-superra` §Commits: `integrate(<step>): <summary>`, `<step>` ∈ `protect | sync | fit | mature | finish`. The `integrate(protect)` commit records the researcher-confirmed permanent-record, consolidation, and protection choices even when Protect changes no files.

Legitimate stop points:

- **Protect:** result, documentation, and protection choices, before permanent documentation is written.
- **Sync:** target base confirmation when no prior decision records it; intent-changing conflicts from `semantic-merge`.
- **Integrate:** the researcher reviews the protected record and derived refactoring task together before execution. A requested or discovered change altering the protected record returns to Mature & Consolidate.
- **Finish:** hard blockers only, e.g. the target base advancing again after Integrate.

## Dispatch Convention

**Load `superRA:agent-orchestration` before writing any dispatch prompt.** Task-scoped dispatches use the Stage values in `superRA:using-superra` §Skill-Load Manifest; never restate load lists in prompts.

Any REVISE verdict at any step: adjudicate per `agent-orchestration` §Handling Reviewer Feedback, iterate to APPROVE.

Non-trivial Sync: `Stage: sync` with generic sync author / sync reviewer agents and the relevant `semantic-merge` mode reference. Trivial Sync: inline (`references/sync.md` Step 3).
