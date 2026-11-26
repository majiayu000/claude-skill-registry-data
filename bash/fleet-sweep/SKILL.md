---
name: fleet-sweep
description: Clean up after a coordinator's fleet. Finds and removes finished delegates' tabs, worktrees, branches and processes, and asks the user about the rest. Use at a coordinator's start, after compaction or a restart, when a delegate settles or a PR merges, and before each status reply.
---

# Fleet sweep

Clean up without being asked. The sweep script decides what is safe to
delete. Act on its verdicts in the turn you see them, and ask the user only
about what would lose work.

`<scripts>` below is this skill's `scripts/` folder.

## When

Sweep at Start, after compaction or a restart, whenever the fleet watcher
fires, and before every status reply. The sweep before each reply catches a
merged PR the watcher was not given. Clean up a delegate in the same turn
its task finishes, so no finished delegate waits for a later sweep.

## Run the report

```bash
<scripts>/sweep.py report <repo>... [--base <branch>]... [--keep <path>]...
```

Pass the domain's main checkouts, any base branches beyond the remote's
default, and the checkouts that must stay, such as a long-lived release
worktree. The backlog's Boundary section holds this line; add it when
missing. The report takes about half a minute and changes nothing but the fast-forward below. Each row
starts with a verdict:

| Verdict | Meaning | Do |
|---|---|---|
| SAFE | Finished, and nothing would be lost | Remove it this turn, without asking |
| CLOSE | Finished, but a session still runs there | Close it when it is your delegate, then remove |
| ASK | Removing it would lose work, or a process the report can't place still runs there | One batched ask to the user |
| KEEP | In use: open PR, live work, base branch or keep list | Nothing |
| MAIN | A main checkout the report fast-forwarded, or could not and says why | Tell the user about a checkout it could not move |

With `fast_forward_main_checkouts` set in the coordinator's config, the report
first fetches each main checkout's remote and runs `git merge --ff-only` when the
checkout is on the default branch, has no tracked changes and has no local
commits. It prints the old and new hash, or a MAIN row saying why it left the
checkout alone. Untracked files do not block it.

Remove every SAFE row, whoever made it: SAFE means nothing would be lost.
CLOSE and ASK rows are yours to act on only when the backlog's handles name
them. The others belong to the user's own sessions or another coordinator:
name them in your reply and leave them.

A sweep is done when every SAFE row is gone, every CLOSE row of yours is
gone, and every ASK row of yours is asked about, in this reply or already in
the backlog.

## Act on each verdict

**SAFE worktree:** `sweep.py remove <worktree>`. It checks again for
uncommitted files, commits on no remote or base, a live session and running
processes, and refuses on any of them. Then it moves the worktree's ignored
files to `<main checkout>/.scratch/parked/<worktree name>/`, at the same
paths: `.scratch/`, `.env`, `evals/results/` and the like. It drops what
`is_build_output` in parking.py calls build output, such as `node_modules/`,
`out/` and `*.log`, except inside a `.scratch/` folder, and prints what it
dropped. When that folder exists, the new one's name ends in
`-<YYYYMMDD-HHMMSS>`. Then it removes the worktree and deletes its branch.
It prints the new path and the branch's hash: put both in the backlog's
Done line. Each parked folder holds a `.parked-at` file with the time it was
parked. Nothing in this skill deletes parked folders, so a scheduled
clean-up of the user's, or the user, removes old ones.
Remove worktrees only this way. `--discard-untracked` is the one way to drop
files: use it only for a detached worktree you made yourself whose only
changes are untracked files.

**SAFE landed branches:** `sweep.py prune-branches <repo> --list` lists
local branches whose PR merged or whose work is on a base branch.
`sweep.py prune-branches <repo> <branch>...` deletes the ones you name and
prints each hash. Delete them all, and put the hashes in the backlog's Done
line. Remote branches stay.

**SAFE process:** a process whose folder was deleted, such as a browser
daemon or an `expect` session left by a worktree you removed. Stop it by
PID with `kill <pid>`.

**SAFE ended-delegate records:** `sweep.py prune-ended` removes each
record in the coordinator's `<state_dir>/ended/`, from every domain, whose
PR merged or closed, or whose worktree is gone with no open PR. It prints
each one's name, domain, program and session id. `--list` prints them
and removes nothing. `delegate_end.py --resume` can no longer find a
removed delegate. `claude --resume <session id>` still opens its session.

**CLOSE**, when the backlog holds its handle:

1. Read its `REPORT.md` and its inbox items, which `fleet_status.py` lists.
   Move each open item that its landing did not settle into the backlog.
2. End it with the coordinator skill's
   `scripts/delegate_end.py <name> --now`, adding `--relayed` once its
   inbox items are in yours. That stops its process, closes its tab and
   writes an ended record, so the fleet watcher prints no `gone` line for
   it. A watcher armed with a list of delegates is stopped and armed again
   without this one.
3. Its session stays resumable with `claude --resume <session id>`.
   `sweep.py prune-ended` removes its ended record once the worktree is
   gone.
4. Remove everything its `REPORT.md` lists under "Made outside the
   worktree": stop processes by PID or port, kill tmux sessions by name,
   close browser tabs, release virtual machines, delete simulators with
   `xcrun simctl delete <udid>`, and delete folders.
5. Delete the files you made for the task outside the worktree, such as a
   brief or diff in the main checkout's `.scratch/`.
6. Run `sweep.py remove` on its worktree.

A CLOSE row without your handle is the user's session or another
coordinator's. Name it in your reply and leave it.

**ASK rows:** batch them into one ask, largest first, each with what would
be lost. A worktree with commits on no remote is real work: ask whether to
push it, park it, or delete it. To delete it, park it, then `git branch -D`
the branch and put its hash in the backlog's Done line. Scratch folders the
report lists are shared across domains; delete the ones your delegates'
reports list as theirs, and ask about the rest once, not at every sweep.
Entries under 100 MB share one row, "N smaller entries untouched 7+ days".
The report leaves out `.scratch/parked/`. iOS simulators over 500 MB are
listed only with `--simulators`, for domains that build iOS apps.

## Parking

A parked task keeps its branch and its `.scratch/`.
`sweep.py remove <worktree> --park` allows commits on no remote, keeps the
branch, and moves ignored files as every removal does. For a detached
worktree it first creates the branch `parked/<worktree name>` at its HEAD
and prints it. Deleting a branch the same day you park it is not parking:
either keep the branch or move the task to Done.

## Report what you removed

In the same turn, move the finished items to the backlog's Done section and
tell the user in one line what you removed and how much disk it freed,
leaving out the files that moved to `parked/`. List CLOSE rows that aren't
yours and the open ask, if any.
