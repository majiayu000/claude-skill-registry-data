---
name: parallel-work
description: Run several Claude agents or branches on OpenAlgo Desktop at the same time without breaking each other. Use when starting work in a worktree, spawning agents in parallel, building or testing while other agents build, writing a test that spawns the app binary, merging a branch into master, resolving conflicts in the registration files (state.rs, lib.rs, routes/mod.rs, middleware.rs, server/tests.rs, migrations.rs), renumbering a migration, freeing disk space in the shared target directory, or pausing unfinished work.
---

# Parallel agents and branches

Several agents work on this repo at once, each in its own git worktree, all
building into one Cargo target directory and pushing to one `master`. Most
damage comes from three things: one agent's process or build being killed or
replaced by another's, a merge that drops one side of a registration file,
and two branches claiming the same migration number.

## 1. Worktrees

- One worktree per agent or topic, under `.claude/worktrees/<name>`
  (gitignored), on its own branch: `git worktree add .claude/worktrees/<name> -b <branch> origin/master`.
  `git worktree list` shows who is where.
- Work only inside your worktree. Never `cd` into the main checkout or
  another agent's worktree to run git there, and never `git stash` there: the
  stash stack is shared by every worktree. Set work aside with a WIP commit
  instead (section 7).
- A worktree has no `node_modules`; run `npm ci` in it when you need the
  frontend toolchain, or run node tools from the main checkout's copy
  (`.claude/skills/chart-indicator` and `openscript` scripts already fall back
  to it). A worktree has no `dist/` either; Rust builds embed `../dist`
  (`src-tauri/src/server/spa.rs`), so create the placeholder CI uses:
  `mkdir -p dist && test -f dist/index.html || echo '<!doctype html><title>ci</title>' > dist/index.html`
  (`dist/` is gitignored).
- The web checkout `/Users/openalgo/openalgo-desktop/openalgo` is read-only
  for everyone.

## 2. The shared target directory and its hazard

Every worktree builds into the same directory, so dependencies compile once:

```bash
export CARGO_TARGET_DIR=/Users/openalgo/openalgo-desktop/openalgo-desktop/src-tauri/target
```

Consequences:

- **Builds queue.** "Blocking waiting for file lock on build directory" is
  another agent's build. Wait; do not delete the lock, do not kill the other
  cargo.
- **`target/debug/openalgo-desktop` belongs to whoever built last.** A test
  that executes the binary may run another checkout's build, with another
  checkout's code, possibly the full app. A test that spawns the binary must:
  1. use `env!("CARGO_BIN_EXE_openalgo-desktop")` (never a hand-built path);
  2. start the child with `env_clear()` and a fresh temporary `HOME`,
     `USERPROFILE`, `APPDATA`, `LOCALAPPDATA`, `XDG_DATA_HOME`,
     `XDG_CONFIG_HOME`, `TMPDIR`, so even a wrong binary cannot reach the
     trader's data folder (`~/Library/Application Support/com.openalgo.desktop`
     on macOS);
  3. use ephemeral ports (bind `127.0.0.1:0`), never 5000/8765 (the
     maintainer's web) or 5500/8766 (the development ports);
  4. hold the child in a guard whose `Drop` kills and reaps it, with a
     timeout on every wait;
  5. probe first that the binary is what the test expects, and stop it the
     moment it logs the app start line (`Starting OpenAlgo Desktop`).

  `src-tauri/tests/it/mcp_subcommand.rs` (`Guard`, `APP_START_LINE`) does all
  five; copy it.
- **In-process tests are the default.** Integration tests run the server
  in-process on ephemeral ports (`tests/it/broker_session_e2e.rs`
  `free_port`, `pin_ports`). Never run the app binary, in any mode or
  subcommand, against the real data folder. To click through the UI, use
  `cargo run --example dev_server` (`src-tauri/examples/dev_server.rs`: a
  throwaway data folder, an in-memory keystore, port 5500). Only one process
  can hold 5500 or 8766; a "port in use" dialog means a dev server or a test
  child is still running: `lsof -nP -iTCP:5500 -sTCP:LISTEN` before anything
  else.
- **Measurements.** Tests that count descriptors or memory re-run alone via
  `crate::isolated!` (`tests/it/isolate.rs`); other agents' builds on the
  same machine still add noise, so a borderline number is re-run, not
  trusted.

## 3. Never kill broadly

No `pkill`, `killall`, `pkill -f cargo` or `pkill -f openalgo`: they kill
other agents' builds, test runs and servers. Stop only a process you started,
by the PID you recorded, or let your own guard drop it. To see what is
running, read-only: `pgrep -fl 'cargo|rustc|openalgo-desktop'`.

## 4. Merging to master through a temporary worktree

Never merge in your feature worktree and never in the main checkout.

```bash
git fetch origin
git worktree add .claude/worktrees/merge-<topic> origin/master      # detached at master
cd .claude/worktrees/merge-<topic>
git merge --no-ff <branch> -m "merge: <what the branch delivers>"
# resolve conflicts (section 5), then the full gates:
mkdir -p dist && test -f dist/index.html || echo '<!doctype html><title>ci</title>' > dist/index.html
npm ci
(cd src-tauri && cargo fmt --all --check)
(cd src-tauri && cargo clippy --all-targets --locked -- -D warnings)
(cd src-tauri && cargo test --locked)                 # the full suite: lib, it, doc
npx tsc -b
npx vitest run
npx biome ci ./src
python3 scripts/ci/code_health.py --base-ref origin/master   # CLAUDE.md, Code health
gitleaks git --no-banner -c .github/gitleaks.toml --log-opts="origin/master..HEAD" .
git push origin HEAD:master
cd - && git worktree remove .claude/worktrees/merge-<topic>
```

If the push is rejected because master moved, fetch, merge `origin/master`
into the merge worktree, rerun the gates, push again. If GitHub rejects
pushes with server errors, a merge through
`gh api repos/marketcalls/openalgo-desktop/merges -f base=master -f head=<branch>`
works; then confirm the resulting tree SHA (`git rev-parse origin/master^{tree}`
after a fetch) matches the tree you tested (`git rev-parse HEAD^{tree}`). A red gate is fixed on
the branch (or in the merge commit when it is a conflict artefact), never
skipped. CI (`.github/workflows/ci.yml`) reruns everything on four
platforms; a local pass on macOS is necessary, not sufficient.

Merge commits follow the existing style (`merge: <topic>`), with the
attribution lines the session requires.

## 5. Conflicts in the registration files: keep both sides

Parallel features each add a line to the same lists. Both lines belong in the
result; a conflict here is almost never either/or.

| File | What both sides add |
| --- | --- |
| `src-tauri/src/state.rs` | fields on `AppState`, their construction in `open_*`, their `shutdown().await` in `AppState::shutdown` |
| `src-tauri/src/lib.rs` | `pub mod` lines, start-up calls in `run()` setup |
| `src-tauri/src/server/routes/mod.rs` | `pub mod` lines and each module's `table()` in the route table |
| `src-tauri/src/server/middleware.rs` | `csrf_exempt` paths |
| `src-tauri/src/server/tests.rs` | entries in `public_route_list_is_exactly_the_reviewed_one` (the list is ordered as `routes::table()` emits it: re-run the test and copy the order it reports) |
| `src-tauri/src/db/sqlite/migrations.rs` | `run_rust_migration` lines (section 6) |
| `src-tauri/src/brokers/mod.rs`, `catalog.rs` | `pub mod`, registry lines, match arms |
| `src-tauri/tests/it/main.rs` | `mod` lines, kept alphabetical |
| `src/App.tsx`, navigation config | routes and menu entries |

After resolving, build and run the guard tests
(`cargo test --locked --lib server::tests`) before anything else: they catch
a route that lost its access level or a public route nobody reviewed.

## 6. Migration numbering across branches

Migrations are named, numbered and recorded by name in the `migrations` table
(`run_rust_migration(conn, "077_mcp", ..)` in
`src-tauri/src/db/sqlite/migrations.rs`); the list runs in source order.
Two branches that both add `078_*` merge without a textual conflict and both
run, but the numbering no longer says the order and the next branch will
collide again. When merging, the branch merged later renumbers:

1. take the next free number after everything on master;
2. rename it in `migrations.rs` (the name string and, for an inline
   migration, the `mNNN_` function name);
3. update the doc comment of the module that owns it, which names the
   migration (`/// Migration \`075_scalping\`` in `scalping/store.rs`; also
   `strategy/store.rs`, `strategy/book.rs`, `chartink/store.rs`,
   `mcp/store.rs`, `trading/runner/store.rs` and several files in
   `db/sqlite/`): `grep -rn '<old number>_' src-tauri/src` finds them all;
4. never rename a migration that has shipped in a release (it is recorded
   by name on traders' machines); renumber only unreleased ones;
5. if the renamed migration already ran on a developer database under its
   old name, it runs again under the new one: migrations must be idempotent
   (check before altering, never clobber a user value), which is the rule
   anyway. Add a migration test on a populated database if there is none.

DuckDB (Historify) has its own list in `src-tauri/src/db/duckdb/migrations.rs`.

## 7. Pausing: save to `wip/<topic>`

Unfinished work is pushed, not left in a worktree that may be cleaned up:

```bash
git add -A && git commit -m "wip: <topic>: <state, what is next>"
git push origin HEAD:wip/<topic>
```

`wip/*` branches (`origin/wip/nubra-otp`, `origin/wip/batchb-consolidation`)
never merge as they are: the work resumes on a proper branch, squashing or
rewording the WIP commits, and the `wip/` branch is deleted after the merge
(`git push origin --delete wip/<topic>`).

## 8. Disk space

The shared target grows by a full copy of this crate's artefacts for every
worktree path that builds it (paths differ, so hashes differ), plus
incremental caches. Check before a large build:

```bash
df -h /Users/openalgo
du -sh /Users/openalgo/openalgo-desktop/openalgo-desktop/src-tauri/target
du -sh .claude/worktrees/*/src-tauri/target 2>/dev/null     # worktrees that built without CARGO_TARGET_DIR
```

- Remove finished worktrees: `git worktree remove .claude/worktrees/<name>`
  (only your own; `git worktree list` marks locked ones in use), then
  `git worktree prune`.
- Delete a stray per-worktree `src-tauri/target` that was built without
  `CARGO_TARGET_DIR`.
- The shared folder grows past 30 GB. When free disk drops below about
  8 GB and no build is running, delete the entries of `target/debug/deps`
  and `target/debug/build` older than the current session, and
  `target/debug/incremental`. Under a running build delete nothing (at most
  per-crate `incremental/*` folders untouched for hours when disk is critical)
  (`find "$CARGO_TARGET_DIR/debug/deps" -maxdepth 1 -mmin +<minutes> ...`;
  list before deleting). Never delete the whole folder, and never
  `cargo clean` it, while other agents build (`pgrep -fl 'cargo|rustc'`):
  it pulls files from under their links and forces every agent into a full
  rebuild.
- A build that fails with linker or "No space left on device" errors on a
  near-full disk is a disk problem: report the disk state rather than
  retrying.
