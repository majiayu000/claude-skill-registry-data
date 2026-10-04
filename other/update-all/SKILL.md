---
name: update-all
description: Update the jcode fork, skill sources, tools and live configs while preserving custom gate behavior and runtime configuration. Read canonical context and the live checklist first.
version: 1.1.0
---

# update-all

## Read first, do not rediscover

Canonical files live in `~/dotfiles/jcode/`:
- `update-all.sh` is the only updater. Never copy it into the skill folder.
- `skills/update-all/CONTEXT.md` records the last audit, remaining risks and preservation decisions.
- `skills/update-all/SKILL.md` is this procedure.

Run `bash ~/dotfiles/jcode/update-all.sh --context` for paths without doing an update.
Read the context and `~/.agents/skills/update-all/CHECKLIST.md`, then inspect the
current branch/dirty state. Last observed dotfiles branch was DATA, not a contract.

## Execute

```bash
cd ~/dotfiles
bash ./jcode/update-all.sh --parallel --dry-run
bash -x ./jcode/update-all.sh --parallel
```

Only run the second command when an actual update is requested. It can rebase,
build and publish the fork, install tools and update live skills/configs.
`--jcode-only`, `--skills-only`, `--tools-only`, `--config-only` restrict scope.
Without `--parallel`, jobs run serially. `flock` prevents overlapping updater runs.

With `--parallel`, core, skills and tools run independently with private logs and
ledgers. Skill source pulls run concurrently, then sync and babysit regeneration.
Tool jobs are independent except the ordered mise install -> mise use -> herdr
pickr chain. The updater waits for every child. Configs and manifest run after the
barrier only if independent phases succeeded. Failures produce a nonzero exit and
failed ledger entries. Review skipped items too, they may need manual action.

Safety contracts:
- Dirty core or unfinished merge/rebase fails. No automatic stash or reset.
- Rebase the gate branch, build that branch, only then push using an explicit
  `--force-with-lease`. A failed build never publishes the branch.
- Fast-forward pulls override global `pull.rebase=true` and disable autostash.
- Divergent live jcode config is preserved and reported for manual merge, not
  overwritten. This protects live-only runtime keys without adding a TOML parser.
- Dirty dotfiles skips pull/stage/commit/push but can install current configs.
  Branch is detected at runtime. No broad staging or automatic empty commits.
- Dry-run writes only reporting/lock directories, never rebases, stashes, pushes,
  installs tools/configs, copies skills or rewrites the manifest.

## Source-only workers

Sourcing does not run main, parse arguments, set shell options or create files:

```bash
source ~/dotfiles/jcode/update-all.sh
RUN_DIR=$(mktemp -d "$JCODE_SCRATCH_DIR/update-all-worker.XXXXXX")
LOG="$RUN_DIR/update-all.log"
CHECKLIST_TMP="$RUN_DIR/checklist.tsv"
CHECKLIST="$RUN_DIR/CHECKLIST.md"
checklist_init
PARALLEL=1
# Example worker scope. Coordinator must own locking and disjoint phase scopes.
run_jobs update_skills
rc=$?
checklist_write "$rc"
```

`run_jobs` isolates phase failure with errexit in a child. Do not invoke mutating
functions inside `if`/`||` wrappers that disable Bash errexit. Workers do not touch
the shared ledger/log or call main. Coordinator merges their private reports.

## Verify, reload and report

- Read the run log and ledger. Latest aggregate log: `~/.jcode/logs/update-all.log`.
  Per-run logs and per-phase job directories remain in `~/.jcode/logs/update-all-*`.
- Count installed `*/SKILL.md` and manifest data rows, ignoring the table header.
- Check babysit has `SDK_VERSION=latest`, `--harness jcode`, exactly one jcode harness
  note and no unresolved `{{harness}}` placeholder.
- Check `local/turn-end-gate` still carries the required gate functionality and
  `babysitter-gate.sh` / `herdr-agent-state.sh` remain installed.
- Confirm live-only config keys survive. Skipped config divergence is not a merge.
- Reload skills through `skill_manage reload_all`. If core rebuilt successfully,
  coordinate `jcode self-dev --reload` or restart separately. A build is not proof
  that the running server has changed.

Report source commits, failures/skips, exact ledger/log paths and remaining
restart/migration work. Do not claim a dry-run or stub test was a real update.
