---
name: implement
description: "Implement an issue from Ascribe's project board: build the change, open the pull request, move the card to In review, and answer the review. Use when a thread is started to implement a card that is In progress, or asked to pick up an issue from the board."
---

# Implementing a card

An implementor gets one card, already moved to **In progress** by the coordinator, and owns one move: **In progress → In review**. It also owns its pull request until it merges: CI, conflicts, and the reviewer's comments are its work. It never approves or merges its own pull request.

[The `board` skill](../board/SKILL.md) says how to move a card.

Start a workflow with the GitHub MCP tool `actions_run_trigger`, never `gh workflow run`; the `board` skill has the details.

## Steps

1. **Read the issue** and its comments. If triage or the maintainer answered a question there, the answer is part of the ask.
2. **Read [AGENTS.md](../../../AGENTS.md)** and the checklist in [project-docs/checklists.md](../../../project-docs/checklists.md) that fits the change. They hold the rules a reviewer checks against.
3. **Build the change** on the thread's branch, with its tests, its conformance case for a behavior change, its docs page, and its changelog entry in `changes/` (never an edit to `CHANGELOG.md`), as AGENTS.md says; a change no user would notice says so in the description instead, in a `Not user-visible:` line ([CONTRIBUTING.md](../../../CONTRIBUTING.md#what-ci-checks-a-pull-request-records)). Run `pnpm check:all`, which runs every check CI runs, before pushing.

   A new diagnostic takes a code from the issue's `Reserved codes:` line, in order, and never the next free number after `main`'s last (decision [#982](../../../project-docs/decisions/982-reserved-diagnostic-codes.md)). Codes it doesn't use stay unused; don't hand them back. If the card needs a diagnostic it has no reserved code for, ask on the issue for more codes and build the rest while triage answers. When merging `main` brings in another branch's diagnostics, keep both sides' entries in `crates/ascribe-core/data/diagnostics.toml`, sorted by code; nothing is renumbered.
4. **Open the pull request** with the repository's template. Put `Closes #N` in the description, so the merge closes the issue and GitHub moves the card to Done. Under **Generated files**, name each command you ran that rewrote one (`ASCRIBE_BLESS=1 cargo test -p ascribe-cli docs`, `cargo insta review`, and so on), so the reviewer can rerun it, and say why its output changed. `node scripts/repo-docs/generated.ts` lists the generated files the branch changes; each should follow from a command you name. Write "None" when it lists none.
5. **Watch the pull request:** subscribe to its activity. Fix CI until it's green.
6. **Move the card to In review** once CI is green. Not before: a red pull request in review wastes the reviewer's pass. Then say so in a new reply in your thread, with the pull request's link, and don't only edit an earlier message: an edit notifies no one, so no reviewer is started for the card.
7. **Answer the review.** The reviewer's comments arrive as pull request events. Fix what's blocking, push, and reply on each thread. Say in a reply when you don't make a change, and why. Leave the card in In review; the reviewer looks again at each push.

## When it's not one pull request

If the work turns out bigger than the issue said, ship the first useful part, say in the pull request what's left, and open an issue for the rest, in Backlog. Don't widen the pull request.

If the issue can't be done as written, because it contradicts a contract or needs a decision, comment on the issue saying what's needed, and stop. Leave the card in In progress, and say so in the thread.
