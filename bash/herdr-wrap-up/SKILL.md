---
name: herdr-wrap-up
description: >-
  Wrap up work that ran across many Herdr sessions: inventory its panes,
  worktrees, Docker, processes and browser daemons, remove what can be rebuilt
  or resumed, keep what can't, and report what was freed. Use when asked to
  wrap up a release or a multi-session run, or to clean up after one.
---

# Herdr wrap-up

Work that ran across many Herdr sessions (a release, a merge train, a night of workers) leaves behind panes and agents, git worktrees and branches, Docker stacks and caches, leftover processes and browser daemons. This skill takes an inventory, sorts every item, removes what it sorted for removal in a fixed order, and ends with one report. It acts on its own sort, without a plan file or an approval step.

**The rule:** remove what can be rebuilt or resumed; keep what can't.

Load the `herdr` skill first: it owns the command mechanics and IDs. Continue only when `HERDR_ENV=1`.

## Inputs

- **work**: what is being wrapped up: a release, a run key, a feature. Take it from the user, else from the calling pane's ledger. When neither names it, ask before step 1. This is the only question, and it comes before anything runs.
- **continuing work**: the work that goes on next. Find it from its status and resume files: the ones the user names, else the ledgers' open rows and the work's state directory.

## Steps

1. **Scope.**
   - Ledgers live in `${XDG_STATE_HOME:-$HOME/.local/state}/herdr-orchestration/<run>.md`. In scope are the ones the user names. Otherwise, take the ledger whose rows name `$HERDR_PANE_ID` or the tower that launched it, plus every ledger its rows lead to. Ledger tables differ between runs, so read them as text.
   - Snapshots go in a directory outside every checkout: `W=$(mktemp -d -t herdr-wrap-up)`, then `herdr pane list > "$W/panes-start.json"`.

   Done when the ledgers in scope are listed and the start snapshot exists.

2. **Inventory**, read-only, with [references/inventory.md](references/inventory.md). Done when:
   - every pane has its purpose, its ledger (or none), its status, its memory and its input-box state;
   - every worktree has its branch, merged or not, clean or dirty, its unpushed commits and stashes, and the ignored files worth keeping;
   - every Docker object is grouped by compose project with its size, each named volume's contents are known, and so is the runtime VM's memory;
   - every listening port and leftover process has a known owner;
   - every browser daemon is mapped to its session, the agent that used it last, and its saved login;
   - the baseline disk and memory numbers are saved.

3. **Continuing work.** Read its status and resume files, and list what it needs:
   - panes and sessions;
   - worktrees and branches;
   - stacks, volumes and images;
   - ports and locks;
   - browser logins;
   - tool scripts;
   - scratch directories under `/private/tmp`.

   Done when each of these is either kept, or removed with its exact bring-up command noted for the report's Restart-after.

4. **Sort** every item into keep or remove, with a one-line reason: first by the [keep rules](#keep-rules), then by the rule. Before a pane goes to remove, read its last output for **loose ends**: an unanswered question, an offered follow-up, a file it left behind. Read it with `herdr agent read <pane> --source recent-unwrapped --lines 120`, or `herdr pane read` for a shell. Loose ends go in the report; they do not keep the pane. Done when every item has a verdict and a reason.

5. **Act** in the order of [references/act.md](references/act.md): panes, worktrees, branches, Docker, processes and browser, then the runtime. Each step starts with its re-check. Done when every item sorted remove has been removed, or the run has stopped on a [surprise](#surprises).

6. **Report.** Re-run the inventory and give the one report from [references/report.md](references/report.md). Done when the report has before and after numbers, every item left has its reason, and Restart-after covers each piece of continuing work.

## Keep rules

Keep an item when any of these holds:
- It is the calling pane, the tower that launched it, or a pane the user placed. Pane IDs are never reused, so a pane missing from the start snapshot appeared during the run: the user placed it.
- The work did not start it: a pane, tab or workspace with no row in a ledger in scope. Without ledgers, a pane belongs to the work when its cwd is one of the work's worktrees or its label names the work. The report lists these panes.
- It is continuing work, or continuing work needs it (step 3).
- Its input box holds **unsent input**: text at normal brightness. Claude Code draws its suggestions dim (`ESC[2m`), and those are not input.
- It holds uncommitted or unpushed work: a dirty worktree, commits not on the remote, a stash.
- Its agent is `working` or `blocked`.

Everything else the work created goes by the rule. How the rule sorts the usual items:
- **An unpushed branch:** keep. Nothing else holds its commits.
- **An idle agent's pane:** close. Its transcript is on disk, and the session resumes from it.
- **A database volume of synthetic data, the build cache, scratch images:** remove. A fresh start or the next build makes them again.
- **Files the user may have edited by hand:** keep, and name them in the report.
- **A merged branch still on the remote:** leave it. The remote is shared; the report gives its delete command.
- **Other projects' containers and processes:** leave them.

## Surprises

The run stops on a **surprise**, and only on one:
- a refusal: `git worktree remove` refuses, a close returns `workspace_group_close_required`, a volume is in use, or a command fails in a way act.md does not expect;
- a branch head that moved since the inventory;
- unsent input found at a re-check;
- uncommitted or unpushed work found on an item sorted remove;
- an item the inventory does not list.

On a surprise, leave that item as it is, run nothing further, and give the report with the surprise at the top. The user decides what happens to the item. `--force`, `--group`, `docker volume prune -a` and `docker image prune -a` stay out of the run: each one removes more than the inventory checked.
