---
name: development-ship
description: Finish a development branch once the tests pass — merge locally, push and open a pull request, keep it, or discard it. Use when the work is done and the user asks to merge, open the PR, wrap up or clean up the branch. Not for checking the code first; see /development-review.
metadata:
  argument-hint: "[project]"
  stack-aware: true
---

# Ship

Finish the work on "$ARGUMENTS". Verify tests pass, then choose how to ship: merge locally, create a PR, keep the branch, or discard.

## Prerequisites

**Stack.** Before you build, test, lint, run or generate code, read the `Stack` section of the project's `AGENTS.md`, or of `CLAUDE.md` when `AGENTS.md` has none. Use its commands exactly as written, its `layout` for where files go and its `rules` as requirements. If it names a `profile`, also read the file `<profile>.md` in the `stacks` folder of this skill's bundled references for the full commands, layout and rules; the project's own keys win where both speak. If there is no `Stack` section, run the `singular-detect` skill, state what you inferred in one line, and offer to write the section with `singular-init`. Never assume a package manager, test runner or formatter the project did not declare.

None — this is a utility skill that runs when development is complete.

## Process

1. **Verify readiness:**
   - Run the project's full test suite
   - All tests must pass — if any fail, stop and report
   - Check for uncommitted changes — commit or stash first

2. **Present shipping options to the user:**

   **Option 1: Merge locally**
   - Merge the branch into main/master
   - Delete the feature branch
   - Push to remote

   **Option 2: Push and create PR**
   - Push the branch to remote
   - Create a pull request with summary and test plan
   - Keep the branch for review

   **Option 3: Keep as-is**
   - Don't merge or push — keep the branch for more work later

   **Option 4: Discard**
   - Delete the branch and all changes
   - Requires explicit confirmation from the user

3. **Execute the chosen option:**
   - Follow the steps for the selected option
   - Report the result (PR URL, merge commit, etc.)

## References

- `references/stacks/bun-react-ts.md` and `references/stacks/rust-gpui.md`: the shipped stack profiles

## Output

No artifact — executes the chosen shipping action and reports the result to the user.
