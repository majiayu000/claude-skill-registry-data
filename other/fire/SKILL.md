---
name: fire
version: 0.1.0
license: MIT
description: Use when a written implementation plan is ready to execute, when the user says "fire", "execute the plan", "build it", or hands over a plan file to implement. The step after recipe.
---

# fire

The expeditor calls "fire" and the line cooks the order: exactly as the ticket reads, station by station, nothing leaving the pass unchecked and nothing improvised on the line. This skill executes a written implementation plan task by task. The plan is the ticket; its checkboxes are the board.

## Preconditions

- A plan with discrete tasks exists ([recipe](../recipe/SKILL.md)'s output, or equivalent). No plan? Run recipe first; fire cooks what is written, it does not compose.
- Never on the default branch. Create a feature branch (`fire/<plan>-<date>`), or isolate in a worktree: prefer the harness's native worktree tool; fall back to `git worktree add` only without one, and verify the worktree directory is gitignored first.
- Green baseline. Run the suite before touching anything and read the output; on a failing baseline, stop and report, because you cannot tell new breakage from old.

## Read the ticket before firing

Read the entire plan critically against the actual code before executing anything. Stale line numbers, helpers the plan names that the code lacks, tasks that contradict each other: find them now, while the tree is clean, not mid-task with it half-changed. Surface concerns and get them resolved before task 1. A plan that references structure that does not exist is a planning gap that goes back to its author, not an invitation to improvise.

## Execution

Two modes, same discipline. Pick brigade mode when subagents are available and the plan has more than a couple of tasks; solo otherwise.

- **Brigade mode:** dispatch a fresh implementer subagent per task, one at a time, in plan order. Give it the full task text and the scene-setting context in the prompt; never make it read the plan file. Read its diff and test output between tasks before dispatching the next. Implementer-only is the default; add reviewer passes for high-risk work or when asked, not as ceremony on every task.
- **Solo mode:** execute inline, treating each task boundary as a checkpoint: tests green, committed, boxes ticked, then the next.

Per task, either mode:

1. Follow the steps exactly, including the run-it-watch-it-fail steps. They are how you tell a broken step from a broken codebase.
2. Verify as the plan specifies and read the output. Evidence, not assertion.
3. Commit per task as the plan says.
4. Tick the task's checkboxes in the plan file. The plan is the live worklist; an executed plan with clean checkboxes is a board nobody can read.
5. Blocked, or reality diverges from the plan? A moved line number or renamed local is a plan typo: fix the plan's reference and continue. A missing helper, absent module, or contradicted design is structural: stop the task, revert any partial change, and take it back to the plan's author. Never blind-retry, and never invent API surface the plan does not define; in brigade mode, a blocked subagent gets something changed (more context, a smaller piece, a more capable model) before any redispatch.

Execute continuously. No "should I continue?" between tasks and no progress check-ins; the user asked for the plan to be executed. The only stops are: a structural divergence, a blocker you cannot resolve, verification that fails twice on focused attempts, or the last task done.

## The finish

After the last task:

1. Run the full suite one last time and read the output ([check](../check/SKILL.md)). Failing? Fix before offering anything.
2. Present exactly these options and wait:
   1. Merge back to the base branch locally (re-verify the suite on the merged result before calling it done)
   2. Push and open a pull request ([pass](../pass/SKILL.md) gates the filing)
   3. Keep the branch as-is
   4. Discard the work (requires the user to type `discard`; show what gets deleted first)
3. Cleanup: remove a worktree only for options 1 and 4, only if fire created it, and only after stepping out of it. Options 2 and 3 keep the worktree alive for iteration. Never remove a workspace the harness manages.

## Rules

- The plan is the contract. Steps execute as written; disagreement with the plan is a conversation with its author, not a silent rewrite.
- Never skip a watch-it-fail step because the implementation "obviously" works, and never weaken a test to get to green.
- One implementer at a time. Tasks in one plan share state by design; parallel execution of independent work is [stations](../stations/SKILL.md)' job, not fire's.
- Checkbox state is part of the deliverable. Tick as you go, not in a batch at the end.
- Flagging a deviation in the final report is not the same as stopping at it. The author decides about structural changes before they are built, not after.

## Common mistakes

- Executing on the default branch because the plan looked small.
- Skipping the critical read, then meeting the plan's stale assumptions mid-task with the tree half-changed.
- Silently inventing the helper the plan references but the code lacks, then calling it "honoring the plan's intent". That is design-by-improvisation; the plan author never saw the design.
- Leaving every checkbox unticked, so nobody, including the resumed session after a crash, can tell where execution stopped.
- Ending with "done" on the feature branch instead of the four finish options.
- Pausing between tasks to ask whether to continue, when the instruction was to execute the plan.
