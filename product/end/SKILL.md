---
name: "Mission Control: End"
description: "Close a run: link the PRs into a stack once they exist, prune each worktree after its session has closed, keep one stack worktree, run the project's checks on the top layer, offer the roadmap follow-ups, archive the ledger"
when_to_use: "From the coordinator session when every task has its PR, or the user says the run is over. Not for landing PRs (pr-land) and not while a crew session is still working."
model: opus
effort: medium
metadata:
  glyph: ᛟ
  family: mission-control
  goblin-spinner: linking the stack|pruning worktrees|archiving the ledger
disable-model-invocation: true
allowed-tools: ["Read", "Bash(python3:*)", "Bash(git:*)", "Bash(gh:*)", "Bash(sh:*)", "Bash(zsh:*)", "AskUserQuestion", "mcp__mission-control__mc_board", "mcp__mission-control__mc_send"]
argument-hint: "(no arguments)"
---

# Mission Control: End

The aftermath, in the order that avoids losing anyone's work. Landing is `pr-land`'s and happens later, at the user's pace; nothing here merges.

## Step 1: Where things stand

`mc_board`, then the config's `stack_status` command (`mc.py --json status` has `config_path`; read `commands.stack_status`). For each crew row: the PR number, its base, whether it is linked, chained or independent and whether the session is still live.

## Step 2: Link the stack

Only when every PR that belongs in it exists and each base is the branch below it. Order bottom to top by PR number and show the command before running it: `gh stack link <bottom> ... <top>`; a bottom PR not based on trunk needs `--base <parent>`. A PR that is independent stays off. The project's stacked-PR rules (the config's `conventions` list names them) win over anything here. Ask once with AskUserQuestion; the approval covers one command. Afterwards, re-run the stack status and relay it.

## Step 3: Worktrees

A feature worktree is pruned only after its session has closed: the board's `live` flag is the test, and a live session's worktree is never touched. For each closed one, from the main checkout: `git worktree remove <path>`, keeping the branch (the PR needs it), then `git worktree prune`. A dirty worktree is shown and left.

When a stack exists, one worktree holds it: `git worktree add <main>/<worktrees.dir>/stack-<n> <top branch>` (or keep one of the pruned ones and rename it on the user's say-so), then `gh stack checkout <top pr>` inside it. Say which worktree is the stack's and that `gh stack up`/`down` move between layers there.

## Step 4: Sync and check

From the stack worktree: `gh stack sync` when trunk moved (show the layers it will force-push first and ask), then the config's `commands.test`, `commands.lint` and `commands.contract` on the top layer. A failure is reported with its output; nothing is pushed over it.

## Step 5: Follow-ups

Everything the run found and did not do (the briefs' "out of scope" lines, the coordinator's notes, a measurement that was inconclusive) is offered to the roadmap: list the items and say `/roadmap:update-tasks` adds them as a batch. Offer, do not run.

## Step 6: Archive

`mc.py end` from this session (it refuses while a slot is held; `/mc release <resource>` first, after asking the holder). The ledger moves to `~/.claude/mission-control/runs/<date>-<name>/`, briefs and log included. Then one closing paragraph for the user: the PRs and their stack, the worktree that remains, what `pr-land` will land in which order and the roadmap items offered.

## Never

Merge anything; prune a worktree whose session is live or whose tree is dirty; `git merge` trunk into a layer; link PRs out of base order; end the run with a slot held without asking its holder.
