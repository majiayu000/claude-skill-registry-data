---
name: build
description: Use when a session opens on a plan file to run, after a clear, or the user says to run or resume a plan, or a decided change this session touches over two files, a dependency, a public signature, a persisted format or security boundary, or is test-first. Not for authoring or repairing a plan, another change of at most two files, a version bump, or an unproven failure.
argument-hint: "[plan path]"
effort: medium
---

# Implementing a plan

## The loop

1. **Find the plan.** Read `references/run-loop.md` for steps 1-6.
2. **Read the frame.**
3. **Ask the branch what landed.** A `Next: none` result goes to step 7.
4. **Form the block.**
5. **Dispatch the unit.**
6. **Route the return.**
7. **The tail.** Read `references/tail.md`: it ends this loop on `verify`.

## No spec

1. **Orient.** A decided change with no plan file reads `references/no-spec.md` for steps 1-8 instead of the loop above. After a compaction, rebuild what landed from the working-tree diff, not memory.
2. **Gate.** Count these facts: over two source, test or config files change; a dependency is added; a public signature changes; a persisted format or security boundary is crossed; orientation missed a required file.
3. **Workspace, then baseline.**
4. **Build.**
5. **Prove.** A risky change reads `references/test-design.md` first. When a symptom survives two fix attempts or a repair crosses a second owner, report both and hand it to `find-cause`.
6. **Project knowledge.** Read `references/project-knowledge.md` when its first line applies.
7. **Fresh eyes.** Read `references/fresh-eyes.md` and run it.
8. **Commit.**

## References

| File | Read it when |
|---|---|
| `references/run-loop.md` | The loop, steps 1-6. |
| `references/run-loop-direct.md` | `references/run-loop.md` step 5, under `Route: direct`. |
| `references/tail.md` | The loop, step 7, once step 3 reports `Next: none`. |
| `references/no-spec.md` | No spec, when there is no plan file. |
| `references/workspace.md` | Step 1 before the first dispatch, or No spec step 3. |
| `references/wave-worktrees.md` | `references/run-loop-direct.md`, for a `Wave:` line; `exo:run-unit` reads it too. |
| `implementer-prompt.md` | Never here: the unit reads it. |
| `drift-repairer-prompt.md` | Never here: the unit reads it. |
| `bug-fixer-prompt.md` | Never here: the loop's step 5 reads it, on a failed check. |
| `review-fixer-prompt.md` | Never here: `verify` step 3 reads it, on a `FINDINGS` verdict with `fix=1` or more. |
| `references/design-tasks.md` | Step 4, for a task with a `Design:` line. |
| `reviewer-prompt.md` | No spec step 7. |
| `references/fresh-eyes.md` | No spec step 7. |
| `references/critique.md` | No spec step 7's last fallback. |
| `references/security.md` | When its first line applies. |
| `references/data-migration.md` | When its first line applies. |
| `references/test-design.md` | When its first line applies. |
| `references/test-first.md` | No spec, test-first work, before naming the first boundary. |
| `references/project-knowledge.md` | No spec step 6, when its first line applies. |
| `references/performance.md` | No spec, speed-only work, before measuring. |
| `../route-skills/references/question.md` | Before asking the user to pick among options. |

Report: `ship`'s overview as this turn's one report, ending with the brief's `## Manual checks`.
