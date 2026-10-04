---
name: worktree-dispatch
description: "Main worktree stays on main. Open grok or dsb in that worktree. A brief cannot shrink the user's turn."
---

# Worktree dispatch (control-tower checkout)

The primary checkout is the control tower. Its checked-out branch is `main`.
Code changes happen in a linked worktree — **one worktree = one branch = one PR.**
([AGENTS.md](../../AGENTS.md) §Control-tower checkout).

## The main worktree stays on `main`

On 2026-09-26 `./scripts/release.sh 6.0.2` ran in the primary checkout. The
script executed `git checkout -b chore/release-6.0.2` there, and the
maintainer's main worktree was still on that branch after the release had
merged. The sentence above was already in this file. It did not stop the
checkout. `scripts/lib/refuse-primary-checkout.sh` now makes `release.sh`
exit before it can edit or switch that tree. `scripts/test-refuse-primary-checkout.sh`
pins the refusal.

- The only git write in the primary checkout is `git pull --ff-only origin main`,
  and only when the branch is already `main` and no tracked file is changed.
- If you find it on another branch and `git status --porcelain --untracked-files=no`
  is empty, put it back: `git checkout main` then `git pull --ff-only origin main`.
  If anything tracked is dirty, stop and report. Do not commit there to finish
  the move.
- A branch, a commit, and `release.sh` go in a linked worktree. Without Orca:
  `git worktree add -b <type>/<slug> <path> origin/main`.
- Do not `git checkout -b` in the primary checkout. That is the move the guard
  exists to stop.

This skill is the worktree lifecycle. Launching the agent tab — grok, codex,
claude, or dsb — is [`orca-tab`](../orca-tab/SKILL.md). Do not run
`orca skills get orca-cli` to open a tab or launch an agent. If a flag in
either skill is rejected, read only that command's `--help` and retry once.

Variables used below:

| Name | Value |
|------|-------|
| `TOWER` | Primary checkout: `dirname "$(git rev-parse --path-format=absolute --git-common-dir)"` — the same answer from the primary checkout or any worktree (`--show-toplevel` would give a worktree's own path, which `--repo path:` rejects) |
| `WT_ID` | Orca worktree id `<repoId>::<path>` — always the whole value |
| `WT` | Worktree path |
| `H` | Orca terminal handle of the agent tab |

## 0. Before you create one

- **Is someone already on it?**
  `orca worktree list --repo path:"$TOWER" --json` shows every worktree with its
  branch and card comment. Do not open a second worktree for a unit that has
  one, and do not touch another session's worktree.

- **Never decide another worktree is abandoned from a tool that only sees Orca
  tabs.** `orca terminal list --worktree <id>` and the whole-list `worktreeId`
  match both returned **0 terminals** for a worktree whose agent was mid-build
  at that moment (2026-09-25, Orca `1.4.210`): that session ran in a plain
  terminal on another tty, not an Orca tab. A zero there means *you cannot see
  it*, not *nobody is there*. Reading activity from it has already produced a
  wrong report that another session's in-flight work was abandoned.

  Use a signal that reads the machine, in this order:

  | Signal | Reads | Weakness |
  |---|---|---|
  | `pgrep -fl "/deepseek-build/<slug>"` | live processes whose argv or cwd names the tree | an idle agent waiting on the model may hold no matching child |
  | `git -C "$WT" log -1 --format=%ad` + `git -C "$WT" status --short` | last commit time and uncommitted work | a session can be thinking for minutes with no new commit |
  | `orca worktree list … .workspaceStatus` | Orca's own card state | reads `in-progress` even for trees nobody has touched since creation |
  | `orca terminal list --worktree <id>` | Orca tabs only | **misses sessions outside Orca** |

  **Treat "no signal" as unknown, not as idle.** When two of the four disagree,
  or when the last commit is recent, **ask the owning session** — a question
  costs a minute; deleting or rebasing under a live session destroys work with
  no undo. This is the same fail-close rule as everywhere else in the harness:
  an unmeasurable state is not a passing one.

- **Does this unit build vendored Grok?** It does if anything it runs calls
  `cargo` in `third_party/grok-build` — directly, or through a script
  (`rg -l grok-build scripts/` lists them: `build-grok-pager.sh`,
  `cache-guard.sh`, `test-grok-vendor-offline.sh`, the `test-path-a-*` scripts, …).
  Those units run **one at a time across all worktrees** (cold build 30–60+ min
  per tree). A quick check for a build in
  flight: `pgrep -fl 'grok-build/target'` (the rustc and build-script
  processes carry that output path; the parent `cargo` does not). It is a
  hint, not a lock — `./scripts/vendor-build.sh status` reads every worktree's
  target and exits 1 while any of them is building; when in doubt, ask the
  other sessions.
- **Warm this worktree's target, never another's.** Each worktree builds
  `third_party/grok-build` in its own `target/`. One `CARGO_TARGET_DIR` shared
  by two worktrees makes them write the same artifact names, and cargo decides
  freshness by mtime alone, so the worktree with the older sources gets the
  other's code from a no-op build — measured 2026-09-27, worktree B's
  `cargo test` finished in 0.35 s and ran worktree A's binary. Run vendored
  cargo through the wrapper, which pins this worktree's target and seeds a cold
  one once from the sibling whose recorded sources differ least:

  ```sh
  ./scripts/vendor-cargo.sh test -p xai-grok-pager --lib
  ./scripts/vendor-cargo.sh check -p xai-grok-shell --all-targets
  ```

  It ignores a `CARGO_TARGET_DIR` the environment carries, caps jobs at 4, and
  refuses to start while another worktree's vendored build is in flight
  (`--allow-concurrent` goes through the memory gate as a second build at
  `-j 2`). The scripts that build under `third_party/grok-build` pin the same
  target themselves, so exporting the old shared path cannot reintroduce it.
- **Compile gate before the full test build.** `cargo check -p <pkg>
  --all-targets` skips codegen and link. Measured 2026-09-26: one
  `cargo test -p xai-grok-pager --lib` round spent **~17 min** to reach an
  `E0425` in test code.
- **Verification scope.** `cargo fmt --all -- --check` locally (cheap); clippy
  for the crates you touched (`cargo clippy -p <pkg> -- -D warnings`). The
  workspace-wide clippy (`cargo clippy --workspace -- -D warnings`) runs on
  PR CI — read it there and fix red. Full test suite once at the end; use a
  test filter while iterating.
- **`cargo` on PATH.** The dsb tool shell can lack it (measured 2026-09-26,
  this workspace): `export PATH="$HOME/.cargo/bin:$PATH"` first.
  `scripts/build-grok-pager.sh` exports that itself.
- **Queue tools.** `./scripts/vendor-build.sh status` reads every worktree's
  queue — holders, waiters, elapsed, command, worktree, plus host
  free / swap / load5m and the memory-gate verdict (exit 1 while busy).
  `./scripts/vendor-build.sh run -- <cmd>` passes a free queue through as-is
  and otherwise starts only when the memory gate passes, with
  `CARGO_BUILD_JOBS=2`; denied, status is printed and nothing starts
  (`prune` clears old `~/.cache/dsb-vendor-targets` copies from the retired
  shared-target escape hatch). Never call cargo from inside a cargo build or
  test on one target — that is a real lock cycle, and nothing under
  `third_party/grok-build` does it today.

## 1. Open the worktree with the agent already in it

A unit has started when `orca terminal list` for that worktree shows a tab
whose screen is `dsb` or `grok` (or `codex` / `claude` when the user named
them), working on the brief. A card whose only tab is a shell `❯` has not
started.

On 2026-09-26 the bare create below left `pin-tower-main`,
`ci-cache-and-coverage`, and `deepseek-native-depth-6-1-0` as that shell.
The grok tabs that wrote the code were on the primary checkout. Orca on
iOS showed the same empty cards. The commands live in
[`orca-tab`](../orca-tab/SKILL.md). Do not restate them, and do not run
`orca skills get orca-cli`.

- The user named `grok`, or named `codex` or `claude`: `orca-tab` §2.
  One `worktree create --agent <that name> --prompt …`. Do not also run a
  bare create.
- The user named `dsb` or `deepseek-build`, or named no agent: `orca-tab`
  §3. `create` opens one shell; send `dsb` into that shell. Do not
  `terminal create` a second tab. `--agent dsb` is rejected. This repo's
  unnamed session is `dsb`. `grok` is the other session used here. Do not
  launch `codex` or `claude` unless the user named them.
- The worktree already exists and only has a shell: send `dsb` or `grok`
  into that shell. Do not add a tab, and do not create a second tree.
- A prompt-only tab sitting next to the agent: close that tab
  (`orca terminal close --terminal <shell> --tab`) after the agent screen
  shows it is working. One worktree, one tab.

**Handoff when the session that creates the worktree already runs
elsewhere.** The create is bare, the driving tab stays on the original
checkout, and the new card holds one shell `❯`. Measured 2026-09-26:
`vendor-suite-contract` was created that way and 28 files were modified from
the creating tab by path — the empty-card defect this section exists for.
Handoff is part of the create:

1. Open the owning session in the new worktree at once — `orca-tab` §1 when a
   tab is already there, §3 when the launcher shell is the only tab.
2. Hand over the in-flight state in the brief: files already changed, commits
   already made, anything unpushed, and the plan being followed.
3. Stop driving that path. The creating session reads the worktree at most;
   the tab inside it owns the unit from here.

`<slug>` has no type prefix (`provider-retry-backoff`). Orca turns `/` into
`-`. `--no-parent` unless the unit stacks. Omit `--base-branch` so the base
is `origin/main`. `--setup skip` unless the unit needs the repo bootstrap.
`run` starts `npm install` and fails loudly when that version's prebuilt
asset is not published yet (measured: `deepseek-build-6.0.0-darwin-arm64.tar.gz`
404). Keep `result.worktree.id`. The agent handle is that worktree's one tab.

The bare create opens one launcher shell (`run` also opens `Setup`).
That shell becomes the session when `dsb` or `grok` runs in it. A second
tab is the bug. Read a tab before `terminal close`. Closing is not
undoable.

`./scripts/check-worktree-ownership.sh` reads every worktree of this repo and
exits 1 when one holds dirty work with no agent tab — the handoff defect
above, read from `orca terminal list` title/preview.

## 2. Name the branch

Orca names the branch after the worktree (plus any branch prefix in the user's
Orca settings). Rename it to [branches.md](../../docs/contributing/branches.md)
form **before the first push**:

```sh
git -C "$WT" branch -m "<type>/<slug>"    # feat | fix | docs | spec | chore | ci | refactor | test
git -C "$WT" branch --show-current
git -C "$WT" config user.email             # the identity you commit to this repo with
```

Orca can keep showing the old branch name for a moment. Address the worktree by
`id:` or `path:`, not `branch:`.

## 3. The agent in the worktree writes the unit

The tower does not implement the diff. `git -C "$WT"` from the tower is for
status, the merge, and cleanup. Writing the files from the tower is how the
card stays a shell while a grok tab on `main` does the work. That is the
2026-09-26 shape, and it is not a unit.

The agent tab is §1. The brief it receives:

What a brief carries:

- **user-turn** — the first line of the brief file is `user-turn:` plus the
  user's sentence, verbatim. That sentence is the done-condition.
- **Unit** — the outcome in one sentence, PR kind and title, branch name,
  `Depends on #N` if stacked
- **Boundaries** — which worktree is theirs; the primary checkout and other
  worktrees are off-limits; the one-Grok-build-at-a-time rule
- **Harness** — follow `AGENTS.md`, `skills/session-unit`,
  `skills/orca-tab`, and `skills/pr-authoring`; `gh` with `--repo` and a
  per-command token; push to `origin`
- **Language** — a delegated run answers in the language its brief *asks for*,
  and `AGENTS.md` alone is not reliable there: subagent runs from the same batch
  on 2026-09-25, with near-identical English briefs, came back 0%, 0%, 1%, 98%.
  Put the language instruction where that run cannot miss it — the brief itself.
  Write the brief in Korean with the technical detail inline, or open it with
  `보고·진행 메모는 한국어로` before switching to English. A delegated run's
  report is human-facing session text too.
- **Authority** — the default close is `session-unit` (PR, CI, merge commit,
  report). Withhold the PR, the merge, or `skills/release` only when
  `user-turn:` says so. Before send, `scripts/check-session-close.sh brief <file>`
  must pass. Do not send a brief it rejects, and do not copy a release lane
  ban out of an older prompt.
- **Report** — the shape in `session-unit`. Do not restate it here.

Then mark the card so other sessions can see the state:
`orca worktree set --worktree "id:$WT_ID" --comment "<one-line state>" --json`

### Watching a dispatched unit — the spinner glyphs are not a contract

If you wait for the agent to finish, **do not decide it from a spinner
character**. Every glyph used here (`⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏`) is a frame index, not a state, and a
pattern that lists a few of them silently reports "idle" on the frames it did
not list.

**Measured 2026-09-25.** A monitor watched a `grok` tab and declared it done
because its glyph list missed the frame on screen — while the tab showed
`⠦ Thinking… 5.2s ⇣141k`, mid-task, and the agent went on to write its report.
The false positive arrived 10 minutes into the run.

What works instead:

```sh
orca terminal read --terminal "$H" --json | python3 -c "
import json,sys
d=json.load(sys.stdin)
tail = '\n'.join(d['result']['terminal']['tail'][-6:])
busy = ('Thinking' in tail) or ('Waiting for response' in tail) or ('stop]' in tail)
print('busy' if busy else 'idle')
"
```

Match the **words** the agent prints (`Thinking…`, `Waiting for response…`) and
the presence of the `[stop]` affordance — not the glyph. Then require the idle
reading twice in a row before declaring the unit finished, because a single
sample lands between frames.

**Better still: watch the artifact, not the screen.** A unit that writes files
is finished when the files change and stop changing; `git -C "$WT" status` is
harder to misread than a TUI. Use the screen to confirm, not to decide.




## 4. Merge and clean up

**This step is part of the unit** (AGENTS.md §One session, one unit). Once the
checks pass and the body meets the bar, merge and clean up in the same session —
do not leave a green PR for a later prompt.

**Order: merge, then `session-unit`'s debrief, then this cleanup block.** The
debrief counts with `git -C "$WT"` and fails on a removed tree.

```sh
GH_TOKEN="$(gh auth token --user <account>)" gh pr merge <n> --repo innocarpe/deepseek-build --merge --delete-branch
gh pr view <n> --repo innocarpe/deepseek-build --json state,mergeCommit   # state must read MERGED
git -C "$WT" status --short                          # must print nothing
orca terminal list --worktree "id:$WT_ID" --json      # see what is actually open
orca terminal close --worktree "id:$WT_ID" --all --json
orca worktree rm --worktree "id:$WT_ID" --json
```

`orca worktree rm` also deletes the local branch, but only when Orca can prove
it is merged. GitHub deletes the remote branch on merge (repo setting).
`--force` removes a dirty tree; use it only after reading what is dirty.

**`--all` closes the launcher and setup tabs too**, which is usually what you
want at the end of a unit — but read the list first if any tab might hold
unsent work.

Then refresh the tower — only when it is on `main` with no changes to tracked
files:

```sh
if [ -n "$(git -C "$TOWER" status --porcelain --untracked-files=no)" ]; then
  echo "tower has uncommitted changes; not moving it:"
  git -C "$TOWER" status --short --untracked-files=no
elif [ "$(git -C "$TOWER" branch --show-current)" != main ]; then
  git -C "$TOWER" checkout main
  git -C "$TOWER" pull --ff-only origin main
else
  git -C "$TOWER" pull --ff-only origin main
fi
```

Untracked files do not block the pull, and they should not: OS or tool
markers (for example a Spotlight `.metadata_never_index`) would otherwise
stop every refresh. `pull --ff-only` already refuses by itself if an incoming
file would overwrite an untracked one.

Never remove a worktree another session created or is still using, even when
it looks finished — ask its session first. If "it looks finished" came from
`orca terminal list` showing nothing, re-read §0: that command returned 0 for a
worktree whose agent was mid-build (2026-09-25).

## Anti-patterns

| Don't | Why |
|-------|-----|
| Edit, commit, or `git checkout -b` in the primary checkout | That tree stays on `main`. On 2026-09-26 `release.sh` left it on `chore/release-6.0.2` |
| Run `release.sh` in the primary checkout | The script refuses (`scripts/lib/refuse-primary-checkout.sh`) and exits 1 |
| `orca worktree create` with no agent, then edit from the tower | The card stays a shell prompt. On 2026-09-26 three worktrees looked empty in Orca, including on iOS |
| A shell tab and a `dsb` tab in the same worktree | Send `dsb` into the shell. Do not open a second tab. Close a leftover prompt once the agent is on screen |
| Re-run `create` because you could not parse the handle | The side effect already happened; ask `terminal list` instead |
| `orca skills get orca-cli` before launching grok or dsb | The recipes are in `orca-tab`. The full guide is what stalls the turn |
| `terminal send … --enter` right after `tui-idle` without reading the screen | A first-run dialog swallows the brief and exits the agent (`orca-tab` §4) |
| `cd "$WT"` and keep working | The next command meant for the tower runs in the tree, or the reverse |
| `gh auth switch` | Flips the active account for every session on the machine |
| Two vendored Grok builds at once | 30–60+ min cold each; parallel builds starve each other |
| `export CARGO_TARGET_DIR=<another worktree>/third_party/grok-build/target` | One target, two worktrees: cargo writes the same artifact names and its mtime-only freshness hands the older-sourced tree the other's code (measured 2026-09-27). Use `scripts/vendor-cargo.sh` |
| `--name feat/x` | Becomes `feat-x`; name the worktree by slug and rename the branch |
| Report a worktree as "no active session" from `orca terminal list` alone | It returned 0 for a live, mid-build worktree (§0); that report tells the owner to abandon in-flight work |
| `worktree rm --force` on a tree you did not read | Deletes uncommitted work with no undo |
