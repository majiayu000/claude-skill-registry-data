---
name: env-toolchain
description: "Use for env toolchain recipes when optimizing a Coworld player."
---

# Environment & toolchain — recipes

On-demand recipes (28). Each is a trigger→action heuristic; pull the relevant one when its situation arises. Tier tags and ⚠ (unverified) as in AGENTS.md.

#### 1. Redirect every tool's cache out of ~/.cache and home before running in a sandbox
`generic`

Sandboxed lint/test/build runs fail when tools write caches outside writable roots, and the failure is mistakable for a code error. Redirect each: `UV_CACHE_DIR=<writable temp>` for uv (default ~/.cache/uv is blocked, failing `uv run` with 'Operation not permitted'), `RUFF_CACHE_DIR=.ruff_cache` for ruff, Nim's cache with `--nimcache:nimcache` or `--nimcache:/private/tmp/<name>_nimcache` (default ~/.cache/nim is blocked), and build output to /private/tmp when the configured dir is unwritable. In parallel compiles give each concurrent build its OWN temp cache - two compiles sharing one cache corrupt the object set and break linking. Pin a project-specific UV_CACHE_DIR for build/ship/tournament loops to keep the cache isolated and reproducible.
  <sub>sources: archive/cogames_playground/alpha_cog/experiments/notebook/submissions/, codex:019dfe75-7dd6-7dd3-90af-84bb28fda415, codex:019e00c0-d889-7d72-9781-3e90e7c1c7b9, codex:019e037c-5f9b-7ad1-8bf3-539709c4da15 (+7)</sub>

#### 2. Invoke coworld/cogames through the workspace and verify the installed version - global/stale tools silently drift
`loop`

Never run a bare global `coworld`/`cogames`: it may be missing from PATH, be a STALE uv-tool install (e.g. 0.1.1 silently passing manifests current versions reject), or point at a Metta checkout wanting a private GitHub dep and trigger a build. Use `uv run coworld ...` or the repo-local editable install from packages/coworld, verify the active source with `uv run python -c "import coworld; print(coworld.__file__)"`, and to validate manifests `uv tool reinstall` the standalone tool to current. The installed uv-tool CLI lives at ~/.local/share/uv/tools/coworld/ and can fail to import (e.g. ModuleNotFoundError httpx). `coworld play` signature drifted: 0.1.1/0.1.2 accept only the manifest while 0.1.3+ accepts a player-image positional plus --variant; as of 0.1.3 softmax-cli became a mandatory dep so the `coworld[auth]` bracket is now a no-op warning (keep a `>=0.1.1` floor to float the 0.1.x head). A `uv sync` replaces an editable overlay with the PyPI version - re-apply the overlay after each sync. Confirm installed versions before scripting (one latest pair: coworld 0.1.20, softmax-cli 0.26.19).
  <sub>sources: archive/cogames_playground/bulbacog/designs/COWORLD_MIGRATION.md, archive/cogames_playground/docs/coworld_cli.md, players_checkouts/players/users/james/personal_cogs/among_them/README., players_checkouts/players/users/james/personal_cogs/among_them/guided_ (+10)</sub>

#### 3. A venv console-script shebang bakes an absolute Python path - renaming a uv project routes commands to the wrong env
`generic` · **negative result**

A virtualenv console script (e.g. .venv/bin/cogames) hardcodes its Python's absolute path, so moving/renaming a uv project directory silently routes commands to the WRONG environment - changing the policies/missions list or surfacing phantom built-in policies. Renaming after `uv init` leaves the old name in pyproject.toml, uv.lock, .venv/pyvenv.cfg, ~40 console-script shebangs, and activation scripts. Fix by regenerating in place: `uv venv --allow-existing --prompt <new-name> .venv` then `uv sync --reinstall`, rename in pyproject.toml, `uv lock` (do not hand-edit generated scripts); verify with `head -1 .venv/bin/<tool>`. When a console script's environment is in doubt, invoke `uv run python -m <module> ...` and do not write doc claims off a bare console script until the shebang is verified.
  <sub>sources: archive/cogames_playground/alpha_cog/docs/cogames-policy-api.md, archive/cogames_playground/alpha_cog/docs/research-sources.md, alpha_cog/AGENTS.md, opencode:ses_223dc7136ffeCr4ZslnR426sVG (+1)</sub>

#### 4. Trust the installed binary/source over docs - PyPI releases, READMEs, and version strings all drift
`loop`

Treat onboarding docs (AGENTS.md/README) and public PyPI/docs as suspect and verify against the actual binary before scripting. Documented launch flags (--address/--port/--config) were rejected as 'Unknown option' while the runtime reads env vars (COGAME_HOST/COGAME_PORT/COGAME_CONFIG_URI); Among Them's AGENTS.md named a nonexistent quick_player.nim (real tool: tools/quick_run.nim). The PyPI cogames release drifts from the main-branch README (cogames issue #6): list what the CLI actually registers via `cogames missions`/`cogames play --help` (game renamed cogs_vs_clips -> cogsguard; full quickstart only ran on `cogames[neural]==0.25.7`), and the README lives in the standalone Metta-AI/cogames repo (the metta/packages/cogames path 404s). Mechanics drift too: installed cogsguard is a territory-control game, not the old sparse heart-production description. Version strings even lie about artifact equality - a mettagrid 0.26.17 inside a Docker image can ship modules (live_episode.py send_final) the identically-numbered PyPI wheel omits. Python version floors drift too ('3.12 required' became '3.11-3.12'); check the framework's actual requires-python. For the crewrift-upload Next.js project, read node_modules/next/dist/docs/ rather than training-data Next.js knowledge - the pinned version has breaking API changes.
  <sub>sources: archive/cogames_playground/alpha_cog/docs/cogs-v-clips-rules.md, archive/cogames_playground/bulbacog/designs/COWORLD_MIGRATION.md, archive/cogames_playground/bulbacog/designs/LOCALIZATION_ROOT_CAUSE_RE, coworld-source-repos.crewrift-upload/optimizers/AGENTS.md (+5)</sub>

#### 5. Install monorepo games from their git pin, not a PyPI extra - the extra resolves only inside the workspace
`loop` · **negative result** · ⚠ _session-derived, unverified_

`pip install cogames[cogsguard]` (or any `cogames[<game>]` extra) fails or SILENTLY DOWNGRADES the resolver to an older cogames version, because that extra only resolves inside the monorepo where tool.uv.sources maps it to a git URL. The downgrade does not hard-fail - uv/pip emit a 'does not have an extra named X' warning then quietly install an older version, so always confirm with `uv pip list | grep cogames` (`cogames --version` is unimplemented). Install instead via the git pin, e.g. `uv pip install "cogsguard @ git+https://github.com/Metta-AI/cogame-cogsguard.git@<sha>"`, and install cogames itself from the local metta checkout (not PyPI) for the newest game support. Error/help text suggesting `pip install <pkg>[<extra>]` is broken for PyPI installers; point users at the canonical git URL (e.g. a STANDALONE_GAMES registry table) and trace the full extra -> tool.uv.sources -> release-workflow chain before deleting a 'stale' extra.
  <sub>sources: opencode:ses_22033c323ffeaukf7T2ZfJOoMR, opencode:ses_2240b911bffeRPYWAkhpoMH1eS, opencode:ses_225b0e431ffeBSef5TF1fgbUHN, opencode:ses_225c247a2ffeNgrsANZfMMyih3 (+1)</sub>

#### 6. Torch-backed cogames policies need the [neural] extra; with torch missing, agents crash silently on first tick
`loop` · **negative result** · ⚠ _session-derived, unverified_

The built-in cogames policies starter/neural/LSTM/baseline (anything using StatefulAgentPolicy) `import torch` on their first step, so a plain `pip install cogames` then `-p starter` fails with ModuleNotFoundError torch - but in interactive/autopilot mode the symptom is the session dying the instant you press input, NOT an obvious torch error. Install `cogames[neural]` (or `uv add`) for those policies. To verify the harness/match loop works while isolating the ~2GB torch dependency, first run a torch-free built-in policy like `noop` or `random`, or substitute a torch-free random-walk policy for lightweight debug tools.
  <sub>sources: opencode:ses_1fa66f0b7ffeIF47rk2pDlz4RX, opencode:ses_225b0e431ffeBSef5TF1fgbUHN, opencode:ses_225c247a2ffeNgrsANZfMMyih3, opencode:ses_225cf8c2bffeE4X8j8tNQm7Dc2</sub>

#### 7. Coworld/cogames auth is softmax login under uv, and SSO tokens expire ~12h - refresh before any live run
`loop`

Coworld/cogames auth comes from `softmax login` (a separate binary, not `cogames auth login`), which must run inside `uv run` from a repo with `coworld[auth]` installed so the softmax package is importable; `cogames auth status` may just tell you to run `softmax login`, and that binary may be absent in the project venv ('Failed to spawn: softmax'). Older tools expose `load_current_token(server=...)` not `load_current_cogames_token` (AttributeError on load = old tool). inference/league SSO tokens via the softmax profile last ~12 hours, so run `aws sso login --profile softmax` (or `softmax login`) within that window before any live LLM/Coworld run - a run that 'should just work' can fail purely on an expired session. Confirm which CLI owns login before writing docs that assume it.
  <sub>sources: bitworld/among_them/players/mod_talks/scripts/launch_mod_talks_llm_loc, player_labs/.claude/skills/coworld-episode-artifacts/SKILL.md, player_labs/.claude/skills/coworld-experience-requests/SKILL.md, opencode:ses_21e7dd4d4ffewtISu38YXrsOgs (+1)</sub>

#### 8. Leave the worktree carrying only source/test/doc changes - clean tool-dropped artifacts and gitignore run outputs first
`generic` · ⚠ _session-derived, unverified_

Clean generated artifacts tooling drops: `python -m py_compile` leaves `__pycache__` dirs in git status (a narrow non-forced removal works even when broad `rm -rf` is sandbox-blocked); `nim c -r` drops a compiled test executable next to the source; aborted installs leave stray virtualenvs. Add `tmp/` and `coworld download` outputs (`coworld/`, `episodes/`, `coworld-episode-results/`) to `.gitignore` BEFORE running discovery so large artifacts that ledgers reference are neither deleted nor committed. When borrowing an opponent bot from another checkout whose AGENTS.md says run-from-source, compile it into a temp dir with isolated build/cache outputs so you neither pollute that repo's tree nor rely on stale binaries.
  <sub>sources: claude-code:b09cd025-18e0-41cc-abe0-039562b0ab0d, codex:019e05c8-e30b-7572-b5e2-066b8440e3e4, codex:019e05eb-dbd6-76f0-8bf4-3ef821cb7cc6, codex:019e06a0-5754-74e0-baf2-771853591aaa (+2)</sub>

#### 9. Coworld images are amd64-only - run under Rosetta with raised timeouts; arm64 player only speeds cold-start, not episodes
`loop` · **negative result**

Coworld game and player images are amd64-only, so on Apple Silicon they run under slow Rosetta emulation: enable Docker Desktop Rosetta amd64 emulation, keep DOCKER_DEFAULT_PLATFORM=linux/amd64 (skipping it causes platform warnings and game-container failures), raise harness timeouts well above defaults, and treat the platform-mismatch warning as cosmetic. Building a player for native arm64 speeds cold-start ~2.7x but does NOT improve steady-state tick rate or end-to-end episode time, because the bottleneck is the amd64 game container running mettagrid under Rosetta and the 0.02 s/step config pace-caps the sim; use arm64 for fast iteration feedback, not long-episode timing.
  <sub>sources: archive/cogames_playground/docs/coworld_cli.md, metta/agent-plugins/kitchensink/skills/ks.coworld-player-gotchas/SKILL, claude-code:4ec865f5-bcbc-44f1-b109-a27d69f55506, claude-code:67ff1fe3-48c0-4738-b7fb-8b994e567434 (+2)</sub>

#### 10. Backgrounded `&` servers die with the tool timeout; `timeout` exit 124 on a player is SUCCESS
`generic` · ⚠ _session-derived, unverified_

A long-running game server/match backgrounded with `&` inside a shell-tool call does NOT survive the tool's timeout - the whole process group is SIGTERM'd when the shell wrapper is killed. To outlive the timeout, detach with nohup (output to a log) and poll the log for readiness before launching players, or use the harness's real background-run mechanism. Conversely, exit code 124 from the `timeout` command wrapping a long-lived player is a SUCCESS signal: it means the process stayed alive the full window (connected and played), not that it crashed.
  <sub>sources: opencode:ses_1fb1d9989ffeYXiew23WUqo2hw, opencode:ses_200deb284ffe7RFSHqkkWQqwAx</sub>

#### 11. Read all config from env at the program edge, force the intended LLM provider, and keep secrets off disk
`generic`

Resolve all configuration (provider credentials, model id, deadlines, toggles, engine WebSocket URL) from environment variables into an immutable config object at the program edge (e.g. CrewborgConfig.from_env at startup), validating values there so bad input fails fast; behavior leaves must not call os.environ, especially per-tick, and never put literal secrets in source/docs. Honor env vars like COGAMES_ENGINE_WS_URL so a cloned agent stays drop-in compatible. With multiple LLM provider credentials present, auto-detection may pick the wrong one - explicitly force the intended provider (MODTALKS_PROVIDER_OPENAI=1 or --llm-provider:openai) and confirm which is selected when debugging missing LLM behavior. Keep provider keys out of hosted applications; use the native sidecar endpoint. For Crewrift, use `anthropic/claude-haiku-4.5`; keep the policy pod below 1,800 quota-weighted tokens per episode across all calls (input + cache-write + 5 × output tokens). Image labeling inputs still need PNG/JPEG/GIF/WebP bytes.
  <sub>sources: bitworld/among_them/players/mod_talks/DESIGN.md, players_checkouts/players/tools/cogbase/docs/designs/maker_v1_design.m, players_checkouts/players/users/james/personal_cogs/infinite_blocks/py, players_checkouts/players_2/players/crewrift/crewborg/docs/designs/con (+5)</sub>

#### 12. Verify git state before reasoning about it in monorepo workspaces - fetch first, check the mainline name, scope to the package
`generic` · ⚠ _session-derived, unverified_

Verify git state before reasoning about it in multi-package workspaces. (1) When local tracking info self-contradicts (in-sync while origin is ahead, or wildly behind), suspect stale remote refs and `git fetch` first - do not trust `git branch -vv` counts against an unfetched remote. (2) Verify the actual mainline branch name before checkout/pull: the crewrift repo's mainline is `master`, not `main`. (3) `git diff --stat`/status from a parent root vs a package subdir give different, misleading pictures (already-committed files appear 'changed' from the root) - scope git status/diff to the package directory and verify against HEAD. For bulbacog the git root is the bulbacog/ subdirectory, not the top-level cogames_playground; anchor git/pytest/commit commands inside it.
  <sub>sources: auggie:e251085a-b35d-4171-8dbd-d006b8bc2bd9, codex:019e28a2-f81d-79b1-a7f7-5f6583c280f1, codex:019e28e9-6b45-7c02-b4c7-bb9b0f44e022, codex:019e8ae0-d849-7d12-9a7c-2b5e09ba75cf (+1)</sub>

#### 13. Scope lint/format to files you touched, but run the real formatter on NEW files before trusting a green local run
`generic` · ⚠ _session-derived, unverified_

Scope formatting/lint to files you touched in a package with pre-existing style debt; do not broad-format the repo. Full-repo Ruff fails on legacy debt (E402/F401/F541, __future__/docstring ordering) and `ruff format --check` is untrustworthy on a never-clean package (flags dozens of unrelated files) - rely on `ruff check` plus scoped tests (Ruff may not be installed by default). BUT do run the project's real formatter on the NEW files you add, because CI lint rejects unformatted new packages even when logic passes. A markdown-only change can still trip a pre-push lint hook (e.g. `metta lint` needing uninstalled node_modules/pnpm); skipping with `--no-verify` for docs-only is a judgment call - flag it explicitly for human re-lint rather than silently skipping.
  <sub>sources: codex:019e1914-2445-7fa2-af5e-8d3ca4d01c57, codex:019e28a2-f81d-79b1-a7f7-5f6583c280f1, codex:019eaee5-b54e-79f2-bf0f-ac59a6a1eae2, opencode:ses_225b0e431ffeBSef5TF1fgbUHN</sub>

#### 14. Run offline/tool-only dependencies via `uv run --with` or a dependency group, not in runtime deps
`generic` · ⚠ _session-derived, unverified_

For a uv-managed player project, run an offline tool needing an extra dependency without polluting runtime deps by using an ephemeral env (`uv run --with pygame python tool.py`), or make it repeatable via a separate dependency group (`uv add --group tools pygame` then `uv run --group tools python tool.py`) - mirroring the runtime-vs-offline asset separation in the dependency manifest.
  <sub>sources: auggie:02627f61-aac0-42a0-a290-3595e010abba</sub>

#### 15. Docker gotchas: orbstack/cask daemon start, ECR/ghcr auth, stale download cache, and leaked containers/workspaces
`loop`

Coworld CLI needs a running Docker daemon: on macOS via OrbStack the active context is 'orbstack' (socket ~/.orbstack/run/docker.sock) - start it with `orb start`, not assuming Docker is broken; the cask install needs its privileged plugin dir pre-created then the socket awaited. Auth pitfalls: pulling a newer policy image from ghcr.io/metta-ai needs `docker login ghcr.io` with a PAT (unauth = 403), and a 403 from public.ecr.aws during `coworld download crewrift` is a stale cached ECR-Public token poisoning anonymous pulls - fix with `docker logout public.ecr.aws`. coworld's download cache is keyed on file existence, not version or whether images still exist, so a prune (OrbStack auto-clears between sessions) leaves dangling tags while download reports 'already downloaded'; an 'image is not available locally ...:downloaded' error with manifest 401 noise is the pruned-image case (the 401 is a red herring) - fix with `coworld download <name> --refresh`. coworld also leaks containers and the coworld-local network on SIGKILL and accumulates GB of ~/coding/metta/tmp/coworld-play-<random>/ workspaces; periodically sweep `docker ps -a --filter name=coworld-` and `find ~/coding/metta/tmp -type d -name 'coworld-play-*' -mtime +1 -delete`. When blocked on an unpullable image, proceed with the cached older one and flag the version gap.
  <sub>sources: archive/cogames_playground/docs/coworld_cli.md, metta/agent-plugins/kitchensink/skills/ks.coworld-player-gotchas/SKILL, personal_labs/crewrift_lab/lessons_archive/TENTATIVE_LESSONS-20260612-, claude-code:d48f9347-7884-4ea2-8659-230051d86410 (+1)</sub>

#### 16. git worktree-based sub-agents need an initialized, committed repo first
`generic` · **negative result** · ⚠ _session-derived, unverified_

`git worktree add` (and worktree-based codex/sub-agent setup) fails on a directory that is not yet a git repo with 'fatal: invalid reference: HEAD'. Initialize and commit the project before delegating to a worktree-based sub-agent; the failure surfaces only when the orchestrator tries to create the isolated worktree.
  <sub>sources: claude-code:db8f623e-c8c0-4195-b1d8-8a8d30fdc4a7</sub>

#### 17. Nim policy gotchas: explicit re-imports, var-capturing closures illegal, relative imports resolve against --path
`generic` · ⚠ _session-derived, unverified_

Language closure/memory rules force structural choices: in Nim a nested helper capturing a `var` state object is illegal, so lift it to a top-level proc. Nim does not re-export imported symbols, so a module calling another's procs (e.g. openTrace/closeTrace/TraceLevel) must add its OWN import even if a sibling already imports it. Nim relative imports resolve against the `--path:` directories / compilation entry point, so a module that compiles standalone can break when built as a library (a mode under modes/ importing perception/data worked from one directory but failed from the package root until made relative `../perception/data`) - after adding cross-package imports, build BOTH standalone and as the library/package, not just one.
  <sub>sources: codex:019dfe75-7dd6-7dd3-90af-84bb28fda415, opencode:ses_2044035bcffeRp9M35307uA4gR, opencode:ses_21b475c59ffeOFBSt0jbwsGras</sub>

#### 18. For a compiled-language player, treat 'compile clean + diff review' as the minimum validation gate
`generic` · ⚠ _session-derived, unverified_

For a compiled-language player (e.g. Nim), the cheapest fast validation loop is the compiler's type/parse check (`nim check`) plus a final diff review for accidental edits; indentation/syntax errors in an off-side-rule language are easy to introduce and a check catches them before any episode run. Treat 'compile clean + diff review' as the minimum gate before attempting a behavior run.
  <sub>sources: codex:019e0392-8fae-7b13-80e7-525df2e3de2f</sub>

#### 19. Isolate test failures that are not yours: collection-time noise, parent-branch regressions, blocked private deps
`generic` · **negative result**

Failures during pytest collection often come from unrelated legacy code, not your test: a package rename (top-level `perception` -> `orpheus.perception`) leaves a stale tests/conftest that fails at COLLECTION time and breaks a brand-new narrowly-scoped test, because pytest loads tests/conftest.py before collecting anything - update the conftest import and run the targeted test files directly instead of the full suite. This repo's parallel/import plugin chokes on module-level dataclass declarations in test files during collection; avoid them or run with `-n0`. Configure `norecursedirs` to skip the archive/ tree, since archived tests import packages that no longer resolve. A CI Python-test failure on a stacked PR may belong to the PARENT branch - inspect which file fails first and fix it on the parent, asserting the actual required-parameter message rather than a brittle literal like `--league`. metta pytest can be blocked by a private Git dep fetch (e.g. cortical) even outside the sandbox; fall back to the focused file with the local venv (`../.venv/bin/python -m pytest <file> -v -n0`) plus a direct toy-example run, and report the wrapper was blocked. Refresh node_modules against pnpm-lock.yaml before the CI lint entrypoint, or a stale JS install blocks the Python lint step that runs through it.
  <sub>sources: players_checkouts/players/archive/README.md, codex:019e012e-626f-7081-91fb-fccc04e39010, codex:019e0142-683b-72a2-b8b7-d3f985d5e433, codex:019e18d7-532e-7540-82ea-9abe1726aec7</sub>

#### 20. Clean up stranded match infra, never broad-pkill, and parameterize the live-match port
`loop`

Multiple agents may run live game servers/bots on one machine, and orphaned subprocesses survive a normal launcher kill and pollute the next run by contaminating lobby state. Never use a broad `pkill -f`: track your own PIDs and only force-kill processes you started (by process-name match), and treat unexpected lobby occupancy or port contention as a stale-process artifact. Make the live-match port a configurable flag (default 2000) and use an isolated/parameterized port range (e.g. 9100-9199) rather than a hardcoded port that forces kill-and-retry cycles. Between coworld/local runs, use a fresh run directory after a failure so a broken trace does not contaminate analysis: stopping a play command leaves a stranded game container (whose 'RuntimeError: Game container exited with status 137' is from killing it, NOT a bot crash), leftover filler bots, and port-bound servers, and a server can auto-enter a fresh lobby and log a second game. Before a fresh diagnostic run, kill leftovers, verify with `pgrep` nothing remains, and analyze only the single intended match's artifacts.
  <sub>sources: bitworld/among_them/players/mod_talks/LLM_SPRINTS.md, codex:019e131a-1bb0-7400-b54a-f208202b291d, codex:019e2819-d56b-72f3-9349-60fc965b6ed2, opencode:ses_1ffe75d89ffeHvW4p2ARluHh51 (+3)</sub>

#### 21. The Coworld Optimizer runs on Bun with two env files and two dev modes - and needs coworld_setup before episodes
`loop`

The optimizer's host-dev stack is Bun, NOT npm (`bun install`, `bun run db:push`/`db:seed`, `bun run dev web` on :3000, `bun run worker`, `bun run mcp:http` on :3100; follow docs/local-development.md; a new shell may lack bun on PATH even when services run - use ~/.bun/bin/bun; the Docker image still builds reproducibly from package-lock.json via `npm ci`). It reads TWO env files - Docker Compose reads `.env` (COAGENT_*_DIR, DOCKER_SOCKET_PATH, DOCKER_DEFAULT_PLATFORM, COWORLD_RUNNER_HOST) while Next.js reads `.env.local`; do not conflate them. Postgres runs on host port 5433 (avoiding system 5432); keep COWORLD_RUNNER_HOST=host.docker.internal or replay URLs point at the wrong host. Two dev modes: Host dev (Next.js+worker on host, Postgres in Docker; best for app edits) and Docker Compose dev (all containerized; best for validating the shipped image, where the web container serves a build frozen at image-build time so UI edits need `docker compose up --build web` or `bun run dev:live` for hot reload). When DATABASE_URL points at the default local DB and COAGENT_SKIP_LOCAL_SERVICES is unset, first page load auto-starts Compose Postgres (pgvector/pgvector:pg16), pushes the Drizzle schema, and seeds; set COAGENT_SKIP_LOCAL_SERVICES=1 to suppress. The web app runs without auth for UI/agents/tasks/local data - only episode execution, league sync, game download, hosted replay, and policy upload need `uv run softmax login`. Coworld CLI workflows require Python 3.12 + uv specifically (3.14 with no python3.12 won't satisfy). Crucially, a policy in the dropdown does NOT mean Crewrift is runnable: a fresh install has no game, so episodes/evals report 'manifest not found' - run the one-shot setup first (`bun run setup:coworld crewrift` / MCP coworld_setup {slug:'crewrift'}), which checks auth+Docker, downloads the game+baseline, pulls images (first amd64 pull is minutes), and syncs the DB, returning a runnable game id; it is async and returns needsAuth if unauthenticated.
  <sub>sources: coworld-source-repos.crewrift-upload/optimizers/.cursor/skills/downloa, coworld-source-repos.crewrift-upload/optimizers/.cursor/skills/mcp-opt, coworld-source-repos.crewrift-upload/optimizers/CLAUDE.md, coworld-source-repos.crewrift-upload/optimizers/skills/optimizer-mcp/S (+5)</sub>

#### 22. Bootstrap a coworld migration with GLOBAL uv-tool installs so the CLI exists before the dependency swap lands
`loop` · ⚠ _session-derived, unverified_

Chicken-and-egg at the start of a coworld migration: Phase 0 discovery needs the coworld CLI but Phase 1 is what adds it to the project. Resolve by installing coworld[auth] and softmax-cli as GLOBAL uv tools (from local metta source if needed) so the CLI is available outside the player's venv before the dependency swap lands; do not pollute the player pyproject.toml just to run discovery.
  <sub>sources: claude-code:b09cd025-18e0-41cc-abe0-039562b0ab0d</sub>

#### 23. Open /dev/tty for curses TUIs so they work under piped/redirected harnesses
`generic` · **negative result** · ⚠ _session-derived, unverified_

curses `cbreak()`/`getch()` fails when stdin/stdout are not a real TTY (a subagent piping the command, or the cogames/Rich framework having grabbed the terminal). Open /dev/tty directly for the curses terminal so input works even when stdout is redirected, fall back gracefully when no TTY exists, and do not conclude a curses TUI is broken just because it fails under a piped test harness.
  <sub>sources: opencode:ses_1fa66f0b7ffeIF47rk2pDlz4RX</sub>

#### 24. Budget a long, CLI-configurable startup timeout for a native game server's cold first compile
`loop` · ⚠ _session-derived, unverified_

Budget a long, CLI-configurable server-startup timeout (e.g. 90s default) for the first run of a native game server, because the first compile (e.g. Nim) is slow and a short timeout will flake on cold starts.
  <sub>sources: codex:019e06a0-5754-74e0-baf2-771853591aaa, opencode:ses_2251f2219ffe0h3Sjj47eVLHrt</sub>

#### 25. Keep source ASCII-only and make session-id paths filesystem-portable
`generic`

Avoid non-ASCII section markers (e.g. the paragraph/section sign) in source files for encoding/portability: reference design-doc sections in plain ASCII inside code comments while keeping the special character only in the Markdown design doc. Likewise make session IDs filesystem-portable by replacing ':' with '-' in ISO8601 timestamps so paths are valid on Windows.
  <sub>sources: bitworld/among_them/players/modulabot/TRACING.md, opencode:ses_21b02c437ffeor4lV5Nb4Cec7y</sub>

#### 26. Run Crewrift locally via Nim+nimby; its local config differs from tournament, and teardown must be server-first
`crewrift`

To run Crewrift locally without Docker: install Nim and sync the lockfile (`nimby use 2.2.10; nimby sync -g nimby.lock`), start the server with COGAME_HOST/COGAME_PORT/COGAME_CONFIG_URI pointing at the repo config.json via `nim r src/crewrift.nim`, build the example bot `nim c players/notsus/notsus.nim`, and run at least 8 bots each connecting to ws://localhost:2000/player?slot=$i&token=$token. The local config.json deliberately differs from tournament: maxGames 1 with a kill cooldown of 100 ticks (SHORTER than the manifest default of 500, so local kill-cooldown timing does NOT match tournament when tuning imposter aggression); a fixed deterministic 8-slot roster of 6 crew + 2 imposters with slots 6 and 7 always imposters (pink/orange); and non-secret placeholder dev tokens (do not treat as secrets, but do not reuse the pattern for hosted sessions). Stop the game server BEFORE killing agent clients to dodge an upstream cleanup bug: killing clients with pending whispers first makes Sim.tickWhispers clear pendingWhisperEntry on an already-disconnected player and crash. A standalone bot with its own reconnect loop is more resilient for long runs than a multi-process launcher that propagates a GUI flag to all children and kills all of them when any one exits.
  <sub>sources: bitworld/among_them/players/mod_talks/DESIGN.md, bitworld/among_them/players/mod_talks/LLM_SPRINTS.md, coworlds/coworld-crewrift/README.md, coworlds/coworld-crewrift/config.json (+1)</sub>

#### 27. Build Nim bindings at Docker image-build time; locally the Nim build runs lazily on first import
`loop`

When building a Nim-backed Coworld player image, compile the Nim bindings at image-build time: `apt-get install build-essential` (Nim emits C that gcc compiles) and ca-certificates (nimby uses HTTPS), pip install the players package with its cogames extra, then run the build module which downloads the pinned Nim toolchain via nimby, syncs nimby.lock, and compiles the importable module; expect a multi-minute first build for the toolchain download, later builds fast. For local non-Docker dev the Nim build runs lazily the first time any wrapper imports the compiled module, so the Nim toolchain must be on the host; the build script auto-installs Nim via nimby into ~/.nimby/ and is safe to re-run.
  <sub>sources: players/cogsguard/nim/README.md</sub>

#### 28. This game's play CLI uses -s/--steps (not seed) and --seed has no short flag; use no-render for ~25x batch speedup
`loop`

This game's play CLI uses `-s/--steps` for max episode steps and `--seed` (no short flag) for the RNG seed; do not confuse `-s` for seed. Use the no-render mode to skip GUI rendering for a large (~25x) speedup when batch-running.
  <sub>sources: alpha_cog/AGENTS.md, alpha_cog/CODE-SUMMARY-key-scripts.md</sub>
