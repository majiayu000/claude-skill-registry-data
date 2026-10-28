---
name: rule-next
description: Pick the rulings that hold the top open rows, research prior art for each, put them to the owner, file the picks with `fli decide`, and hand back a `fix:loop` command for the rows they unblock. Use when asked to get the next batch ready.
disable-model-invocation: true
---

# Rule next

The step between `frame-next` (a question gets options) and `fix:loop` (a row gets built). The output is one `bun run fix:loop -- --lanes N --ids …` command whose every row can be built without the owner being asked anything else. Arguments: none, or the rows already in a running or just-handed-back loop, to leave out.

## 1. Pick

About seven rows. Rank the open rows in `fli next`, `fli decisions` and `ISSUES.md` by severity (S1, then S2), then by how many other rows each one blocks. A row whose ruling is already filed is build-ready and goes straight into the batch. A row held by an open ruling brings that ruling into the hearing. **Show the list, with one line per row on why it made the cut, before researching**, so the owner can redirect it.

## 2. Verify

For each ruling, re-probe its paper bullet (`IDEAS/owed-rulings.md` and the others `fli decisions` names) against the tree. Check that the file, function and failure it describes still exist, with `rg` and by running the probe the bullet states. A bullet the tree contradicts goes back to `frame-next`, not to the owner.

## 3. Prior art

**The owner refuses a technical recommendation that has no precedent behind it.** Run at most 3 research agents in parallel, model sonnet, web only, told "do not spawn sub-agents". Every claim needs a source URL, and inference is marked as inference. Vendor source beats vendor docs. For each ruling, the report says which product does each option. An option the paper missed (D1199's Meteor mergebox) or precedent that runs against the recommendation (D1121's parent-restarts-child) is said plainly in the question, not smoothed over.

## 4. Ask

Every ruling goes through AskUserQuestion, at most 4 per call. The recommended option comes first, labeled "(Recommended)", and the precedent goes in the question text. **When the owner answers with a question about cost or scale, measure it**: write a scratch bench in the scratchpad (bun:sqlite, RSS for memory), show a table of the numbers, then ask that ruling again.

## 5. File

`fli decide <slug> <letter> --section "<DECISIONS.md ## section>"`. The slug is the `owed-rulings:fjs-dNNNN-…` key that `fli decisions` prints, and a bare `FJS-D` id is refused. The section is the one where that package's recent rulings sit. Pass `--why` when the pick goes against the recommendation, amends an option, or was weighed with numbers worth keeping.

**After an amended pick, read the ruling's `###` heading.** Decide copies the option text as written, so a heading can still say the thing the owner changed (D1200's key said "the email" after the owner picked "the email+IP pair"). Patch the heading to match the amendment. Then run `fli register:check` and compare its error count with the count before the first decide; a new error is this session's to fix. Commit nothing.

## 6. Hand back

- **A table** of ruling, pick, and the row it unblocks (with its package).
- **Collisions**: rows that will edit the same file, which means rebases between lanes.
- **Undocumented behavior** any pick rests on, and the test that should pin it.
- **Other sessions' work**: whose uncommitted changes sit in the packages this batch touches, from `git status`. The tree is shared, so a whole-file restore or a stash takes someone else's work with it.
- **The command**: `bun run fix:loop -- --lanes N --ids …`, with one lane per package where that holds.
