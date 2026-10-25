---
name: "Branch: Stack"
description: "Read, link, extend, sync and tidy a GitHub stack without opening or landing a PR: status, link an existing chain, add a layer, sync after trunk or a lower layer moved, tidy stale local tracking"
when_to_use: "When PRs are chained by base but GitHub shows no stack, a stack needs rebasing after main moved or a lower layer changed, a layer's branch is missing locally, a new branch must sit on top of an open PR, or gh stack refuses a command (belongs to multiple stacks, pathspec did not match, already exists in a stack). Opening a layer's PR is pr-create's job; landing one is pr-land's."
model: sonnet
effort: medium
metadata:
  glyph: ᛊ
  family: branch
  goblin-spinner: stacking|linking|rebasing|tidying
disable-model-invocation: true
allowed-tools: ["Read", "EnterWorktree", "Bash(git:*)", "Bash(gh pr list:*)", "Bash(gh pr view:*)", "Bash(gh stack view:*)", "Bash(gh stack link:*)", "Bash(gh stack add:*)", "Bash(gh stack sync:*)", "Bash(gh stack rebase:*)", "Bash(gh stack push:*)", "Bash(gh stack checkout:*)", "Bash(gh stack unstack:*)", "Bash(gh stack up:*)", "Bash(gh stack down:*)", "Bash(gh stack top:*)", "Bash(gh stack bottom:*)", "Bash(~/.claude/library/scripts/stack-status.py:*)", "Bash(~/.claude/library/scripts/checkout-occupied.sh:*)"]
arguments: ["action", "target"]
argument-hint: "status [branch|pr ...] | link <pr|branch> <pr|branch> ... | add <branch> | sync [upstack] | tidy"
---

# Branch: Stack

Everything that changes a stack's shape or keeps it current, and nothing that opens or lands a pull request. `pr-create` opens a layer's PR (with `base <parent>`), `pr-land` lands one (`gh stack merge <pr#> --merge`); this skill hands over to them by name and stops. The facts behind every command here are in `~/.claude/library/references/stacked-prs.md`; read its "Three sources of truth" and "Worktrees: one per stack" sections before the first action.

**Every action starts with the script.** `~/.claude/library/scripts/stack-status.py` reads GitHub's stack field, the PR bases and the local `gh-stack` tracking, and prints one verdict per branch: `linked`, `chained-unlinked`, `independent`, `no-pr`. No action guesses from a base branch.

---

## Step 0: Parse the arguments

`action` is required and is one of `status`, `link`, `add`, `sync`, `tidy`.

| Call | Meaning |
|---|---|
| `status [branch\|pr ...]` | the verdict table for the targets (default: the current branch) and every tracked stack |
| `link <pr\|branch> ... ` | link PRs that already exist into a GitHub stack, bottom to top; a stack number first appends the rest to that stack |
| `add <branch>` | a new branch on top of the current stack, ready for commits and `pr-create` |
| `sync` | trunk moved: cascade-rebase every layer and push |
| `sync upstack` | this layer changed after review: rebase the layers above it and push |
| `tidy` | drop stale stacks from local tracking |

Hard stop on invalid input: print the one-line reason and the usage block, run nothing.

| Invalid call | Reason to print |
|---|---|
| no action | `branch-stack needs an action` |
| `link` with fewer than two targets | `link needs at least two PRs or branches, bottom to top` |
| `add` with no branch | `add needs a branch name` |
| `sync` with anything but `upstack` | `sync takes nothing, or upstack` |
| `tidy` followed by anything | `tidy takes no arguments` |

```text
Usage: /branch-stack status [branch|pr ...]
       /branch-stack link <pr|branch> <pr|branch> ...   (bottom to top; a stack number first appends)
       /branch-stack add <branch>
       /branch-stack sync [upstack]
       /branch-stack tidy
```

---

## Action: `status`

1. `~/.claude/library/scripts/stack-status.py <targets>` (no targets: the current branch). Relay its three sections as they come: the table, the tracked stacks, the next steps.
2. Stop. The map is the output; a "Next" line that names a command is an offer, not an instruction, and the user picks the action.

---

## Action: `link`

For PRs that already exist and are chained by base (`chained-unlinked`), or an unlinked PR to append to a stack.

1. `stack-status.py <every target>`. Stop and say so when any target is `no-pr` (open its PR first: `pr-create base <parent>`; `gh stack link` could push a bare branch and open the PR itself, but with an auto-generated title and none of `pr-create`'s approved body), or is `linked` to a stack other than the one named by a leading stack number (one PR sits in one stack; `tidy` or `gh stack unstack` first is the user's call).
2. Order check: each target's base must be the previous target's branch (the first target's base is the trunk, or the top of the named stack). Out of order: print the chain the bases describe and stop. This check is the protection, since `link` corrects the base of an existing PR that sits in the wrong place (GitHub's `gh-stack` docs say so; v0.1.0's `--help` is silent, so it is treated as true) and would retarget a live PR from a mis-ordered list. The same goes for the bottom target's base: `link` defaults it to the repo's default branch and this skill passes no `--base`, so a bottom PR based on any other trunk stops here with that said.
3. Show the command and ask: `gh stack link <targets>`. The approval covers one command.
4. Run it, then `stack-status.py <targets>` again and relay the table. `link` writes no local tracking, so the rows say "not tracked here"; that is expected, and `gh stack checkout <pr#>` is the step before any `sync`.

---

## Action: `add`

A new layer on top of the stack the current branch belongs to.

1. `stack-status.py`. The current branch must be `linked` and tracked here with its branch present; otherwise print the row's "Next" line (`gh stack checkout <pr#>`, or `link` first) and stop.
2. `git status --porcelain` must be empty, and `~/.claude/library/scripts/checkout-occupied.sh` must exit 0 (another live session in this worktree means stop and say so).
3. `gh stack top` (the new layer goes on the top, never mid-stack), then `gh stack add <branch>`. A branch name keeps the command out of an editor. `-m` creates a commit, so on the clean tree step 2 guarantees it dies with `nothing to commit`; `add -A`/`-u` without `-m` opens an editor and is never run.
4. Close in two lines: the branch exists on top of stack #N and is checked out; commits go here, and `pr-create base <top-layer-branch>` opens its PR when ready.

---

## Action: `sync`

`sync` is a cascade-rebase and a `--force-with-lease` push of every layer. It rewrites SHAs, which is the expected mechanism for a stack (`pr-handle_review`'s carve-out), and it is the one command that must never run blind.

1. `stack-status.py`. The current branch must be `linked`, tracked here, branch present. Missing or untracked: offer `gh stack checkout <pr#>` (it checks branches out, so it is asked, not assumed) and rerun the status after it.
2. `git status --porcelain` empty, `checkout-occupied.sh` exit 0. A dirty tree or another session: stop and say which.
3. **What will move.** For each open layer, bottom to top, `git rev-list --left-right --count origin/<branch>...<branch>` and `git log --oneline --merges origin/<trunk>..<branch>`. Print one table: layer, PR, local vs remote, merge commits. A merge commit on a layer is flattened by the rebase, which is correct (see the reference's "Trunk moved" flow) but must be said before it happens.
4. Ask. The approval names the layers and that they will be force-pushed. Then one of:
   - `sync`: `gh stack sync`
   - `sync upstack`: `gh stack rebase --upstack`, then `gh stack push`
5. **Outcomes.** Read the output as well as the exit code. Exit 0 with `Sync aborted` in the output: local and remote had diverged and nothing moved; say so, print the two chains it shows and stop, since the user decides which side wins. Exit 0 ending `Stack synced` or `Branches synced`: `stack-status.py --open` and relay the table (`Branches synced` means the branches were pushed but GitHub holds no stack object for them). Exit 3 (rebase conflict): `gh stack` has restored every branch; print the files it names and the two ways on, `gh stack rebase` then resolve, `git add`, `gh stack rebase --continue`, or `gh stack rebase --abort`; do not resolve conflicts here without being asked. The `belongs to multiple stacks` message (exit 6 from `view`, exit 2 from `sync` on v0.1.0, so match the text): the checked-out branch is usually the trunk of several stacks; `gh stack checkout <a branch unique to this stack>` and run again, and offer `tidy` only when one of them is stale. Exit 8 (stack locked): another process is mid-command; wait, never delete the lock.

---

## Action: `tidy`

1. `stack-status.py --open`. The "Local Tracking" section marks a stack stale when GitHub reports every PR in it `MERGED` (the tracking file's own flag lags until a `sync`, so the script asks GitHub). A stack with a closed PR, a layer with no PR yet or a state GitHub would not return is **not** stale, and neither is one whose branches are all missing locally but whose PRs are open (its branches come back with `gh stack checkout`).
2. No stale stack: say so and stop.
3. One AskUserQuestion (multi-select) over the stale stacks, each option naming the stack number and its branches.
4. For each approved: `gh stack unstack <n> --local`. `--local` is not optional here: without it the command also unstacks the merged PRs on GitHub, which changes nothing useful and asks GitHub to rewrite closed history.
5. `stack-status.py --open` again; the stale rows are gone.

---

## Red flags

**Never:** `gh stack merge`, `gh pr merge`, `gh pr create` or `gh stack submit` from this skill (the first two are `pr-land`'s, the others `pr-create`'s); `gh stack init` on branches whose PRs already exist (that is `link`); `git merge main` or `git merge <parent>` into a layer (`sync` is the whole point); a `sync` with a dirty tree, with another session in the worktree, or without the "what will move" table; `gh stack modify` or `gh stack switch` (interactive editors that hang); `gh stack add -A`/`-u` without `-m`; `gh stack unstack` without `--local` from `tidy`; `git push --force` by hand (the lease is what makes the rewrite safe); resolving a rebase conflict without being asked; a second worktree for a layer of a stack this session already has a worktree for.

<raw-arguments value="$ARGUMENTS" />
