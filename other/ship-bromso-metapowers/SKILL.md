---
description: Finish a development branch — merge, create PR, or clean up
---

# Ship

Finish the work on "$ARGUMENTS". Verify tests pass, then choose how to ship: merge locally, create a PR, keep the branch, or discard.

## Prerequisites

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

## Output

No artifact — executes the chosen shipping action and reports the result to the user.
