---
name: triage
description: "Triage Ascribe's project board: decide which Backlog issues are ready for an implementor, move them to Ready, and ask on the rest. Use when a thread is started to triage the board, when the board routine fires, or when asked which issues are ready to work on."
---

# Triaging the board

Triage owns one move: **Backlog → Ready**. It reads every card in Backlog, moves the ones an implementor can start on without asking anything, and leaves the rest with a question. It doesn't start implementors; the coordinator does, from what triage reports.

[The `board` skill](../board/SKILL.md) says how to read the board and move a card.

Start a workflow with the GitHub MCP tool `actions_run_trigger`, never `gh workflow run`; the `board` skill has the details.

## Steps

1. **Read the board,** and list the Backlog cards that are issues. Draft items and pull requests aren't triage's to move.
2. **Read each issue** with its comments, through the GitHub MCP tools or `gh api repos/ascribed-dev/ascribe/issues/N` and `.../comments`. Skip one whose last comment is a question from triage that nobody has answered.
3. **Decide whether it's ready.** It's ready when all of these hold:
   - it's one pull request's worth of work, or says which part comes first;
   - it says what done looks like: the behavior, the output, or the page that changes;
   - nothing it needs is waiting on another open issue or pull request;
   - it doesn't ask for a decision only the maintainer can make: a change to a contract (see AGENTS.md's "Contracts don't move"), a new dependency outside the repository, or anything in `project-docs/outside.md`.
4. **Move the ready cards to Ready,** all in one run of Board.

   First, **reserve the diagnostic codes** of each ready card that adds a diagnostic, so two pull requests cut from the same `main` never take the same code (decision [#982](../../../project-docs/decisions/982-reserved-diagnostic-codes.md)). Count the diagnostics the card needs from the issue and a look at the checks it changes, and add one or two when unsure. Take the codes after the highest of these, in order:

   - the last `code` in `crates/ascribe-core/data/diagnostics.toml` on `main`;
   - the highest code in any issue's reservation, open or closed: search the repository's issues for `"Reserved codes"` and read the matching comments;
   - the highest code an open pull request adds to `diagnostics.toml`, for one opened before codes were reserved.

   Then comment on the issue, on a line of its own, `Reserved codes: ASC286–ASC288` (one code is `Reserved codes: ASC286`). Reserve for each card before the next, so two cards in one run never share a code; one triage at a time runs, so two runs don't race.
5. **Comment on each card that isn't ready,** once, with the one thing that would make it ready, phrased as a question the maintainer can answer in a line. Leave it in Backlog.
6. **Report, in the thread:** the cards moved to Ready, oldest first, each as `#N title` with a `Touches:` line under it, then the cards left with a question. The coordinator starts implementors from that list, so put nothing else in it.

   The `Touches:` line names the folders, modules, or spec sections the card will mostly change, at module depth, not a whole crate: `crates/ascribe-check/src/page/`, `SPEC §7`. It's a best guess from the issue and a look at the code, in one line. Leave out what nearly every card touches: `changes/`, generated references, and `project-docs/surface.md`. When the card is a phase of a plan, say which plan and phase, and whether the plan lets it run alongside another phase:

   ```
   #995 Board: don't start cards that touch the same files at the same time
   Touches: .claude/skills/triage/, .claude/skills/board/
   ```

   The coordinator uses that line to keep two cards that change the same module from running at once ([the `board` skill](../board/SKILL.md#start-cards-that-dont-collide)).

## More codes for a card in progress

An implementor that needs more diagnostics than its card reserved asks on the issue, and builds the rest while it waits. Each run, search the open issues for such a question with no answer, and answer each with a new `Reserved codes:` line, picked as in step 4. Don't move the card; it stays where it is.

## Judgment

- Prefer leaving a card in Backlog with a good question to moving a vague one. An implementor who has to guess builds the wrong thing, and the review costs more than the question.
- A bug report with a reproduction is ready; the fix is the deliverable.
- Don't rewrite an issue to make it ready. Ask its author.
- Don't move a card back out of Ready, In progress, or In review. Those belong to other roles.
