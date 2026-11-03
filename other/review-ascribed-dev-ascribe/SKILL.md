---
name: review
description: "Review a pull request for a card that is In review on Ascribe's project board, then approve it with the Approve workflow and merge it once nothing blocking is left. Use when a thread is started to review a card, or asked to review a pull request from the board."
---

# Reviewing a card

A reviewer gets one card in **In review** and owns its last move: it merges, and GitHub moves the card to Done. Nobody else merges an agent's pull request, and the reviewer merges only what it approved.

[The `board` skill](../board/SKILL.md) says how to approve and merge.

Start a workflow with the GitHub MCP tool `actions_run_trigger`, never `gh workflow run`; the `board` skill has the details.

## Steps

1. **Find the pull request:** the one that closes the card's issue. Read the issue, the description, and the whole diff.
2. **Check it against [AGENTS.md](../../../AGENTS.md)** and the checklist in [project-docs/checklists.md](../../../project-docs/checklists.md) that fits, and against what the issue asked for. Run what you need to believe it: the tests it adds, the command it changes.
3. **Check what the change records:** the two rules the `change record` job checks, and the two it can't ([CONTRIBUTING.md](../../../CONTRIBUTING.md#what-ci-checks-a-pull-request-records) says what each means):
   - It fails when a contract changed with no decision in `project-docs/decisions/`. When it passes, check that the decision the pull request adds is the one that accepts its change to the contract.
   - It warns when the source changed and no entry was added in `changes/`, unless the description has a `Not user-visible:` line. Whether there's a warning or such a line, judge it yourself: a change a user would notice with no entry or no page under `docs/content/` updated is blocking, and so is a `Not user-visible:` line that isn't true.
   - **A behavior change comes with a conformance case** in `tests/conformance/cases/`. Look for one deliberately: no check finds it missing, and a behavior change without one is blocking.
   - **A clean-up is labeled `optimization`,** so CI compares its outputs with the base's. The comparison runs only with the label, so a pull request meant to change no output and not labeled has proved nothing: ask for the label, and treat it as blocking until the `outputs unchanged` job has passed.
4. **Account for every generated file it changes.** Run `node scripts/repo-docs/generated.ts` on the pull request's branch: it lists each changed file that a test run with `ASCRIBE_BLESS=1`, `cargo insta`, or another generator writes, and what writes it, from the tables in [ARCHITECTURE.md](../../../ARCHITECTURE.md#ascribe_bless1). For each one, say in the review why it changed (files that changed for one reason can share a line): which change to its source it follows from, and that the commands the description names would write it. Flag, as blocking, a generated file whose change nothing in the pull request explains (an output change nobody meant is what "A clean-up changes no output" in AGENTS.md stops), and a generated file the description's commands don't account for. Rerun a command when the diff is too large to read line by line, and compare.
5. **Write one review,** with a comment on each line that needs one. Mark each comment as blocking or not. Blocking means wrong, unsafe, against a rule in AGENTS.md, or missing what the issue asked for. A preference isn't blocking; say it once, or not at all.
6. **Wait for the implementor** when anything is blocking. Subscribe to the pull request; each push wakes you. Review the new commits, and resolve each thread the push fixed.
7. **Approve and merge** when nothing blocking is left, CI is green on the head, and there's no merge conflict:
   - run Approve with the head commit you reviewed, and check that its run passed;
   - merge with a merge commit, giving the same commit, so a push since your review stops the merge.

If the merge is refused because the head moved, review the new commits and approve again.

## Judgment

- Review what the pull request says it does, not the pull request you'd have written.
- A change to a contract, an output, or `project-docs/outside.md` that the issue didn't ask for is blocking until the maintainer agrees to it, in the issue or the pull request. Ask them there, and don't merge until they answer.
- Don't push to the implementor's branch. Say what to change.
