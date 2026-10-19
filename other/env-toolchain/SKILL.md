---
name: env-toolchain
description: "Use for env toolchain recipes in scripted Coworld policy optimization."
---

# Environment & toolchain — recipes (loop tier)

On-demand recipes (12). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Invoke coworld/cogames through the workspace and verify the installed version - global/stale tools silently drift
`loop`

Never run a bare global `coworld`/`cogames`: it may be missing from PATH, be a STALE uv-tool install (e.g. 0.1.1 silently passing manifests current versions reject), or point at a Metta checkout wanting a private GitHub dep and trigger a build. Use `uv run coworld ...` or the repo-local editable install from packages/coworld, verify the active source with `uv run python -c "import coworld; print(coworld.__file__)"`, and to validate manifests `uv tool reinstall` the standalone tool to current. The installed uv-tool CLI lives at ~/.local/share/uv/tools/coworld/ and can fail to import (e.g. ModuleNotFoundError httpx). `coworld play` signature drifted: 0.1.1/0.1.2 accept only the manifest while 0.1.3+ accepts a player-image positional plus --variant; as of 0.1.3 softmax-cli became a mandatory dep so the `coworld[auth]` bracket is now a no-op warning (keep a `>=0.1.1` floor to float the 0.1.x head). A `uv sync` replaces an editable overlay with the PyPI version - re-apply the overlay after each sync. Confirm installed versions before scripting (one latest pair: coworld 0.1.20, softmax-cli 0.26.19).
  <sub>sources: archive/cogames_playground/bulbacog/designs/COWORLD_MIGRATION.md, archive/cogames_playground/docs/coworld_cli.md, players_checkouts/players/users/james/personal_cogs/among_them/README., players_checkouts/players/users/james/personal_cogs/among_them/guided_ (+10)</sub>

#### 2. Install monorepo games from their git pin, not a PyPI extra - the extra resolves only inside the workspace
`loop` · **negative result** · ⚠ _session-derived, unverified_

`pip install cogames[cogsguard]` (or any `cogames[<game>]` extra) fails or SILENTLY DOWNGRADES the resolver to an older cogames version, because that extra only resolves inside the monorepo where tool.uv.sources maps it to a git URL. The downgrade does not hard-fail - uv/pip emit a 'does not have an extra named X' warning then quietly install an older version, so always confirm with `uv pip list | grep cogames` (`cogames --version` is unimplemented). Install instead via the git pin, e.g. `uv pip install "cogsguard @ git+https://github.com/Metta-AI/cogame-cogsguard.git@<sha>"`, and install cogames itself from the local metta checkout (not PyPI) for the newest game support. Error/help text suggesting `pip install <pkg>[<extra>]` is broken for PyPI installers; point users at the canonical git URL (e.g. a STANDALONE_GAMES registry table) and trace the full extra -> tool.uv.sources -> release-workflow chain before deleting a 'stale' extra.
  <sub>sources: opencode:ses_22033c323ffeaukf7T2ZfJOoMR, opencode:ses_2240b911bffeRPYWAkhpoMH1eS, opencode:ses_225b0e431ffeBSef5TF1fgbUHN, opencode:ses_225c247a2ffeNgrsANZfMMyih3 (+1)</sub>

#### 3. Torch-backed cogames policies need the [neural] extra; with torch missing, agents crash silently on first tick
`loop` · **negative result** · ⚠ _session-derived, unverified_

The built-in cogames policies starter/neural/LSTM/baseline (anything using StatefulAgentPolicy) `import torch` on their first step, so a plain `pip install cogames` then `-p starter` fails with ModuleNotFoundError torch - but in interactive/autopilot mode the symptom is the session dying the instant you press input, NOT an obvious torch error. Install `cogames[neural]` (or `uv add`) for those policies. To verify the harness/match loop works while isolating the ~2GB torch dependency, first run a torch-free built-in policy like `noop` or `random`, or substitute a torch-free random-walk policy for lightweight debug tools.
  <sub>sources: opencode:ses_1fa66f0b7ffeIF47rk2pDlz4RX, opencode:ses_225b0e431ffeBSef5TF1fgbUHN, opencode:ses_225c247a2ffeNgrsANZfMMyih3, opencode:ses_225cf8c2bffeE4X8j8tNQm7Dc2</sub>

#### 4. Coworld/cogames auth is softmax login under uv, and SSO tokens expire ~12h - refresh before any live run
`loop`

Coworld/cogames auth comes from `softmax login` (a separate binary, not `cogames auth login`), which must run inside `uv run` from a repo with `coworld[auth]` installed so the softmax package is importable; `cogames auth status` may just tell you to run `softmax login`, and that binary may be absent in the project venv ('Failed to spawn: softmax'). Older tools expose `load_current_token(server=...)` not `load_current_cogames_token` (AttributeError on load = old tool). inference/league SSO tokens via the softmax profile last ~12 hours, so run `aws sso login --profile softmax` (or `softmax login`) within that window before any live LLM/Coworld run - a run that 'should just work' can fail purely on an expired session. Confirm which CLI owns login before writing docs that assume it.
  <sub>sources: bitworld/among_them/players/mod_talks/scripts/launch_mod_talks_llm_loc, player_labs/.claude/skills/coworld-episode-artifacts/SKILL.md, player_labs/.claude/skills/coworld-experience-requests/SKILL.md, opencode:ses_21e7dd4d4ffewtISu38YXrsOgs (+1)</sub>

#### 5. Coworld images are amd64-only - run under Rosetta with raised timeouts; arm64 player only speeds cold-start, not episodes
`loop` · **negative result**

Coworld game and player images are amd64-only, so on Apple Silicon they run under slow Rosetta emulation: enable Docker Desktop Rosetta amd64 emulation, keep DOCKER_DEFAULT_PLATFORM=linux/amd64 (skipping it causes platform warnings and game-container failures), raise harness timeouts well above defaults, and treat the platform-mismatch warning as cosmetic. Building a player for native arm64 speeds cold-start ~2.7x but does NOT improve steady-state tick rate or end-to-end episode time, because the bottleneck is the amd64 game container running mettagrid under Rosetta and the 0.02 s/step config pace-caps the sim; use arm64 for fast iteration feedback, not long-episode timing.
  <sub>sources: archive/cogames_playground/docs/coworld_cli.md, metta/agent-plugins/kitchensink/skills/ks.coworld-player-gotchas/SKILL, claude-code:4ec865f5-bcbc-44f1-b109-a27d69f55506, claude-code:67ff1fe3-48c0-4738-b7fb-8b994e567434 (+2)</sub>

#### 6. Docker gotchas: orbstack/cask daemon start, ECR/ghcr auth, stale download cache, and leaked containers/workspaces
`loop`

Coworld CLI needs a running Docker daemon: on macOS via OrbStack the active context is 'orbstack' (socket ~/.orbstack/run/docker.sock) - start it with `orb start`, not assuming Docker is broken; the cask install needs its privileged plugin dir pre-created then the socket awaited. Auth pitfalls: pulling a newer policy image from ghcr.io/metta-ai needs `docker login ghcr.io` with a PAT (unauth = 403), and a 403 from public.ecr.aws during `coworld download crewrift` is a stale cached ECR-Public token poisoning anonymous pulls - fix with `docker logout public.ecr.aws`. coworld's download cache is keyed on file existence, not version or whether images still exist, so a prune (OrbStack auto-clears between sessions) leaves dangling tags while download reports 'already downloaded'; an 'image is not available locally ...:downloaded' error with manifest 401 noise is the pruned-image case (the 401 is a red herring) - fix with `coworld download <name> --refresh`. coworld also leaks containers and the coworld-local network on SIGKILL and accumulates GB of ~/coding/metta/tmp/coworld-play-<random>/ workspaces; periodically sweep `docker ps -a --filter name=coworld-` and `find ~/coding/metta/tmp -type d -name 'coworld-play-*' -mtime +1 -delete`. When blocked on an unpullable image, proceed with the cached older one and flag the version gap.
  <sub>sources: archive/cogames_playground/docs/coworld_cli.md, metta/agent-plugins/kitchensink/skills/ks.coworld-player-gotchas/SKILL, personal_labs/crewrift_lab/lessons_archive/TENTATIVE_LESSONS-20260612-, claude-code:d48f9347-7884-4ea2-8659-230051d86410 (+1)</sub>

#### 7. Clean up stranded match infra, never broad-pkill, and parameterize the live-match port
`loop`

Multiple agents may run live game servers/bots on one machine, and orphaned subprocesses survive a normal launcher kill and pollute the next run by contaminating lobby state. Never use a broad `pkill -f`: track your own PIDs and only force-kill processes you started (by process-name match), and treat unexpected lobby occupancy or port contention as a stale-process artifact. Make the live-match port a configurable flag (default 2000) and use an isolated/parameterized port range (e.g. 9100-9199) rather than a hardcoded port that forces kill-and-retry cycles. Between coworld/local runs, use a fresh run directory after a failure so a broken trace does not contaminate analysis: stopping a play command leaves a stranded game container (whose 'RuntimeError: Game container exited with status 137' is from killing it, NOT a bot crash), leftover filler bots, and port-bound servers, and a server can auto-enter a fresh lobby and log a second game. Before a fresh diagnostic run, kill leftovers, verify with `pgrep` nothing remains, and analyze only the single intended match's artifacts.
  <sub>sources: bitworld/among_them/players/mod_talks/LLM_SPRINTS.md, codex:019e131a-1bb0-7400-b54a-f208202b291d, codex:019e2819-d56b-72f3-9349-60fc965b6ed2, opencode:ses_1ffe75d89ffeHvW4p2ARluHh51 (+3)</sub>

#### 8. The Coworld Optimizer runs on Bun with two env files and two dev modes - and needs coworld_setup before episodes
`loop`

The optimizer's host-dev stack is Bun, NOT npm (`bun install`, `bun run db:push`/`db:seed`, `bun run dev web` on :3000, `bun run worker`, `bun run mcp:http` on :3100; follow docs/local-development.md; a new shell may lack bun on PATH even when services run - use ~/.bun/bin/bun; the Docker image still builds reproducibly from package-lock.json via `npm ci`). It reads TWO env files - Docker Compose reads `.env` (COAGENT_*_DIR, DOCKER_SOCKET_PATH, DOCKER_DEFAULT_PLATFORM, COWORLD_RUNNER_HOST) while Next.js reads `.env.local`; do not conflate them. Postgres runs on host port 5433 (avoiding system 5432); keep COWORLD_RUNNER_HOST=host.docker.internal or replay URLs point at the wrong host. Two dev modes: Host dev (Next.js+worker on host, Postgres in Docker; best for app edits) and Docker Compose dev (all containerized; best for validating the shipped image, where the web container serves a build frozen at image-build time so UI edits need `docker compose up --build web` or `bun run dev:live` for hot reload). When DATABASE_URL points at the default local DB and COAGENT_SKIP_LOCAL_SERVICES is unset, first page load auto-starts Compose Postgres (pgvector/pgvector:pg16), pushes the Drizzle schema, and seeds; set COAGENT_SKIP_LOCAL_SERVICES=1 to suppress. The web app runs without auth for UI/agents/tasks/local data - only episode execution, league sync, game download, hosted replay, and policy upload need `uv run softmax login`. Coworld CLI workflows require Python 3.12 + uv specifically (3.14 with no python3.12 won't satisfy). Crucially, a policy in the dropdown does NOT mean Crewrift is runnable: a fresh install has no game, so episodes/evals report 'manifest not found' - run the one-shot setup first (`bun run setup:coworld crewrift` / MCP coworld_setup {slug:'crewrift'}), which checks auth+Docker, downloads the game+baseline, pulls images (first amd64 pull is minutes), and syncs the DB, returning a runnable game id; it is async and returns needsAuth if unauthenticated.
  <sub>sources: coworld-source-repos.crewrift-upload/optimizers/.cursor/skills/downloa, coworld-source-repos.crewrift-upload/optimizers/.cursor/skills/mcp-opt, coworld-source-repos.crewrift-upload/optimizers/CLAUDE.md, coworld-source-repos.crewrift-upload/optimizers/skills/optimizer-mcp/S (+5)</sub>

#### 9. Bootstrap a coworld migration with GLOBAL uv-tool installs so the CLI exists before the dependency swap lands
`loop` · ⚠ _session-derived, unverified_

Chicken-and-egg at the start of a coworld migration: Phase 0 discovery needs the coworld CLI but Phase 1 is what adds it to the project. Resolve by installing coworld[auth] and softmax-cli as GLOBAL uv tools (from local metta source if needed) so the CLI is available outside the player's venv before the dependency swap lands; do not pollute the player pyproject.toml just to run discovery.
  <sub>sources: claude-code:b09cd025-18e0-41cc-abe0-039562b0ab0d</sub>

#### 10. Budget a long, CLI-configurable startup timeout for a native game server's cold first compile
`loop` · ⚠ _session-derived, unverified_

Budget a long, CLI-configurable server-startup timeout (e.g. 90s default) for the first run of a native game server, because the first compile (e.g. Nim) is slow and a short timeout will flake on cold starts.
  <sub>sources: codex:019e06a0-5754-74e0-baf2-771853591aaa, opencode:ses_2251f2219ffe0h3Sjj47eVLHrt</sub>

#### 11. Build Nim bindings at Docker image-build time; locally the Nim build runs lazily on first import
`loop`

When building a Nim-backed Coworld player image, compile the Nim bindings at image-build time: `apt-get install build-essential` (Nim emits C that gcc compiles) and ca-certificates (nimby uses HTTPS), pip install the players package with its cogames extra, then run the build module which downloads the pinned Nim toolchain via nimby, syncs nimby.lock, and compiles the importable module; expect a multi-minute first build for the toolchain download, later builds fast. For local non-Docker dev the Nim build runs lazily the first time any wrapper imports the compiled module, so the Nim toolchain must be on the host; the build script auto-installs Nim via nimby into ~/.nimby/ and is safe to re-run.
  <sub>sources: players/cogsguard/nim/README.md</sub>

#### 12. This game's play CLI uses -s/--steps (not seed) and --seed has no short flag; use no-render for ~25x batch speedup
`loop`

This game's play CLI uses `-s/--steps` for max episode steps and `--seed` (no short flag) for the RNG seed; do not confuse `-s` for seed. Use the no-render mode to skip GUI rendering for a large (~25x) speedup when batch-running.
  <sub>sources: alpha_cog/AGENTS.md, alpha_cog/CODE-SUMMARY-key-scripts.md</sub>
