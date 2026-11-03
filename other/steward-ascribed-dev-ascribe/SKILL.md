---
name: steward
description: "How to drive a pull request in this repository to mergeable: who merges, how approval works, and what CI here needs. Use when watching, fixing, or answering review on a pull request you opened or were asked to drive."
---

# Driving a pull request here

This repository's work runs from [the project board](https://github.com/orgs/ascribed-dev/projects/1); the [`board`](../board/SKILL.md), [`implement`](../implement/SKILL.md), and [`review`](../review/SKILL.md) skills say who does what. What follows holds for any pull request an agent drives.

- **The author doesn't merge.** A pull request for a card is merged by its reviewer, after the Approve workflow approves the commit it reviewed. Drive yours to green and mergeable, then wait for the review. A pull request with no card waits for the maintainer.
- **Approval comes from Approve.** Agents post as the maintainer, who authors their pull requests, so an agent's review is only ever a comment. A green pull request without an approval from `github-actions[bot]` on its head isn't reviewed yet.
- **A push after approval needs another.** Approve covers one commit. Say in the pull request what the new commits change, so the reviewer's second pass is short.
- **CI here:** the one required check is `all checks`. AGENTS.md lists the checks to run before a push, and its rule for an output change: one a decision accepts gets the label `outputs changed` and a block in the description, per CONTRIBUTING.md.
- **Merge with a merge commit,** never a squash or a rebase, and never rewrite the history of a branch someone else pushed to.
- **Keep the card where it is.** Fixing CI or answering review doesn't move a card. Only the implementor's move to In review, and the merge, do.
