---
name: env-toolchain
description: "Use for reusable env toolchain recipes in software and coding-agent work."
---

# Environment & toolchain — recipes (generic tier)

On-demand recipes (15). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Redirect every tool's cache out of ~/.cache and home before running in a sandbox
`generic`

Sandboxed lint/test/build runs fail when tools write caches outside writable roots, and the failure is mistakable for a code error. Redirect each: `UV_CACHE_DIR=<writable temp>` for uv (default ~/.cache/uv is blocked, failing `uv run` with 'Operation not permitted'), `RUFF_CACHE_DIR=.ruff_cache` for ruff, Nim's cache with `--nimcache:nimcache` or `--nimcache:/private/tmp/<name>_nimcache` (default ~/.cache/nim is blocked), and build output to /private/tmp when the configured dir is unwritable. In parallel compiles give each concurrent build its OWN temp cache - two compiles sharing one cache corrupt the object set and break linking. Pin a project-specific UV_CACHE_DIR for build/ship/tournament loops to keep the cache isolated and reproducible.
  <sub>sources: archive/cogames_playground/alpha_cog/experiments/notebook/submissions/, codex:019dfe75-7dd6-7dd3-90af-84bb28fda415, codex:019e00c0-d889-7d72-9781-3e90e7c1c7b9, codex:019e037c-5f9b-7ad1-8bf3-539709c4da15 (+7)</sub>

#### 2. A venv console-script shebang bakes an absolute Python path - renaming a uv project routes commands to the wrong env
`generic` · **negative result**

A virtualenv console script (e.g. .venv/bin/cogames) hardcodes its Python's absolute path, so moving/renaming a uv project directory silently routes commands to the WRONG environment - changing the policies/missions list or surfacing phantom built-in policies. Renaming after `uv init` leaves the old name in pyproject.toml, uv.lock, .venv/pyvenv.cfg, ~40 console-script shebangs, and activation scripts. Fix by regenerating in place: `uv venv --allow-existing --prompt <new-name> .venv` then `uv sync --reinstall`, rename in pyproject.toml, `uv lock` (do not hand-edit generated scripts); verify with `head -1 .venv/bin/<tool>`. When a console script's environment is in doubt, invoke `uv run python -m <module> ...` and do not write doc claims off a bare console script until the shebang is verified.
  <sub>sources: archive/cogames_playground/alpha_cog/docs/cogames-policy-api.md, archive/cogames_playground/alpha_cog/docs/research-sources.md, alpha_cog/AGENTS.md, opencode:ses_223dc7136ffeCr4ZslnR426sVG (+1)</sub>

#### 3. Trust the installed binary/source over docs - PyPI releases, READMEs, and version strings all drift
`generic`

Treat onboarding docs (AGENTS.md/README) and public package/docs pages as suspect and verify against the actual binary/source before scripting. Documented launch flags can be rejected as 'Unknown option' while the runtime reads env vars instead; tool names in docs can be nonexistent. A PyPI/package release can drift from the main-branch README, so list what the CLI actually registers via its own `--help`/subcommands; mechanics drift too (a renamed or re-themed game). Version strings even lie about artifact equality -- an identically-numbered Docker image and PyPI wheel can ship different modules. Language/runtime version floors drift ('3.12 required' becomes '3.11-3.12'); check the actual requires-python. For a pinned framework dependency, read its bundled node_modules/docs rather than training-data knowledge, because the pinned version may have breaking API changes.
  <sub>sources: archive/cogames_playground/alpha_cog/docs/cogs-v-clips-rules.md, archive/cogames_playground/bulbacog/designs/COWORLD_MIGRATION.md, archive/cogames_playground/bulbacog/designs/LOCALIZATION_ROOT_CAUSE_RE, coworld-source-repos.crewrift-upload/optimizers/AGENTS.md (+5)</sub>

#### 4. Leave the worktree carrying only source/test/doc changes - clean tool-dropped artifacts and gitignore run outputs first
`generic` · ⚠ _session-derived, unverified_

Clean generated artifacts tooling drops: `python -m py_compile` leaves `__pycache__` dirs in git status (a narrow non-forced removal works even when broad `rm -rf` is sandbox-blocked); `nim c -r` drops a compiled test executable next to the source; aborted installs leave stray virtualenvs. Add run-output directories to `.gitignore` BEFORE running a step that produces them, so large artifacts that ledgers reference are neither deleted nor committed. When borrowing code from another checkout whose docs say run-from-source, build it into a temp dir with isolated build/cache outputs so you neither pollute that repo's tree nor rely on stale binaries.
  <sub>sources: claude-code:b09cd025-18e0-41cc-abe0-039562b0ab0d, codex:019e05c8-e30b-7572-b5e2-066b8440e3e4, codex:019e05eb-dbd6-76f0-8bf4-3ef821cb7cc6, codex:019e06a0-5754-74e0-baf2-771853591aaa (+2)</sub>

#### 5. Backgrounded `&` servers die with the tool timeout; `timeout` exit 124 on a player is SUCCESS
`generic` · ⚠ _session-derived, unverified_

A long-running server/process backgrounded with `&` inside a shell-tool call does NOT survive the tool's timeout -- the whole process group is SIGTERM'd when the shell wrapper is killed. To outlive the timeout, detach with nohup (output to a log) and poll the log for readiness before depending on it, or use the harness's real background-run mechanism. Conversely, exit code 124 from the `timeout` command wrapping a process you expect to stay alive is a SUCCESS signal: it means the process ran the full window, not that it crashed.
  <sub>sources: opencode:ses_1fb1d9989ffeYXiew23WUqo2hw, opencode:ses_200deb284ffe7RFSHqkkWQqwAx</sub>

#### 6. Read all config from env at the program edge, force the intended LLM provider, and keep secrets off disk
`generic`

Resolve all configuration (provider credentials, model id, deadlines, toggles, engine WebSocket URL) from environment variables into an immutable config object at the program edge (e.g. CrewborgConfig.from_env at startup), validating values there so bad input fails fast; behavior leaves must not call os.environ, especially per-tick, and never put literal secrets in source/docs. Honor env vars like COGAMES_ENGINE_WS_URL so a cloned agent stays drop-in compatible. With multiple LLM provider credentials present, auto-detection may pick the wrong one - explicitly force the intended provider (MODTALKS_PROVIDER_OPENAI=1 or --llm-provider:openai) and confirm which is selected when debugging missing LLM behavior. Keep provider keys out of hosted applications; use the native sidecar endpoint. For Crewrift, use `anthropic/claude-haiku-4.5`; keep the policy pod below 1,800 quota-weighted tokens per episode across all calls (input + cache-write + 5 × output tokens). Image labeling inputs still need PNG/JPEG/GIF/WebP bytes.
  <sub>sources: bitworld/among_them/players/mod_talks/DESIGN.md, players_checkouts/players/tools/cogbase/docs/designs/maker_v1_design.m, players_checkouts/players/users/james/personal_cogs/infinite_blocks/py, players_checkouts/players_2/players/crewrift/crewborg/docs/designs/con (+5)</sub>

#### 7. Verify git state before reasoning about it in monorepo workspaces - fetch first, check the mainline name, scope to the package
`generic` · ⚠ _session-derived, unverified_

Verify git state before reasoning about it in multi-package workspaces. (1) When local tracking info self-contradicts (in-sync while origin is ahead, or wildly behind), suspect stale remote refs and `git fetch` first - do not trust `git branch -vv` counts against an unfetched remote. (2) Verify the actual mainline branch name before checkout/pull: the crewrift repo's mainline is `master`, not `main`. (3) `git diff --stat`/status from a parent root vs a package subdir give different, misleading pictures (already-committed files appear 'changed' from the root) - scope git status/diff to the package directory and verify against HEAD. For bulbacog the git root is the bulbacog/ subdirectory, not the top-level cogames_playground; anchor git/pytest/commit commands inside it.
  <sub>sources: auggie:e251085a-b35d-4171-8dbd-d006b8bc2bd9, codex:019e28a2-f81d-79b1-a7f7-5f6583c280f1, codex:019e28e9-6b45-7c02-b4c7-bb9b0f44e022, codex:019e8ae0-d849-7d12-9a7c-2b5e09ba75cf (+1)</sub>

#### 8. Scope lint/format to files you touched, but run the real formatter on NEW files before trusting a green local run
`generic` · ⚠ _session-derived, unverified_

Scope formatting/lint to files you touched in a package with pre-existing style debt; do not broad-format the repo. Full-repo Ruff fails on legacy debt (E402/F401/F541, __future__/docstring ordering) and `ruff format --check` is untrustworthy on a never-clean package (flags dozens of unrelated files) - rely on `ruff check` plus scoped tests (Ruff may not be installed by default). BUT do run the project's real formatter on the NEW files you add, because CI lint rejects unformatted new packages even when logic passes. A markdown-only change can still trip a pre-push lint hook (e.g. `metta lint` needing uninstalled node_modules/pnpm); skipping with `--no-verify` for docs-only is a judgment call - flag it explicitly for human re-lint rather than silently skipping.
  <sub>sources: codex:019e1914-2445-7fa2-af5e-8d3ca4d01c57, codex:019e28a2-f81d-79b1-a7f7-5f6583c280f1, codex:019eaee5-b54e-79f2-bf0f-ac59a6a1eae2, opencode:ses_225b0e431ffeBSef5TF1fgbUHN</sub>

#### 9. Run offline/tool-only dependencies via `uv run --with` or a dependency group, not in runtime deps
`generic` · ⚠ _session-derived, unverified_

For a uv-managed player project, run an offline tool needing an extra dependency without polluting runtime deps by using an ephemeral env (`uv run --with pygame python tool.py`), or make it repeatable via a separate dependency group (`uv add --group tools pygame` then `uv run --group tools python tool.py`) - mirroring the runtime-vs-offline asset separation in the dependency manifest.
  <sub>sources: auggie:02627f61-aac0-42a0-a290-3595e010abba</sub>

#### 10. git worktree-based sub-agents need an initialized, committed repo first
`generic` · **negative result** · ⚠ _session-derived, unverified_

`git worktree add` (and worktree-based codex/sub-agent setup) fails on a directory that is not yet a git repo with 'fatal: invalid reference: HEAD'. Initialize and commit the project before delegating to a worktree-based sub-agent; the failure surfaces only when the orchestrator tries to create the isolated worktree.
  <sub>sources: claude-code:db8f623e-c8c0-4195-b1d8-8a8d30fdc4a7</sub>

#### 11. Nim policy gotchas: explicit re-imports, var-capturing closures illegal, relative imports resolve against --path
`generic` · ⚠ _session-derived, unverified_

Language closure/memory rules force structural choices: in Nim a nested helper capturing a `var` state object is illegal, so lift it to a top-level proc. Nim does not re-export imported symbols, so a module calling another's procs (e.g. openTrace/closeTrace/TraceLevel) must add its OWN import even if a sibling already imports it. Nim relative imports resolve against the `--path:` directories / compilation entry point, so a module that compiles standalone can break when built as a library (a mode under modes/ importing perception/data worked from one directory but failed from the package root until made relative `../perception/data`) - after adding cross-package imports, build BOTH standalone and as the library/package, not just one.
  <sub>sources: codex:019dfe75-7dd6-7dd3-90af-84bb28fda415, opencode:ses_2044035bcffeRp9M35307uA4gR, opencode:ses_21b475c59ffeOFBSt0jbwsGras</sub>

#### 12. For a compiled-language player, treat 'compile clean + diff review' as the minimum validation gate
`generic` · ⚠ _session-derived, unverified_

For a compiled-language player (e.g. Nim), the cheapest fast validation loop is the compiler's type/parse check (`nim check`) plus a final diff review for accidental edits; indentation/syntax errors in an off-side-rule language are easy to introduce and a check catches them before any episode run. Treat 'compile clean + diff review' as the minimum gate before attempting a behavior run.
  <sub>sources: codex:019e0392-8fae-7b13-80e7-525df2e3de2f</sub>

#### 13. Isolate test failures that are not yours: collection-time noise, parent-branch regressions, blocked private deps
`generic` · **negative result**

Failures during pytest collection often come from unrelated legacy code, not your test: a package rename (top-level `perception` -> `orpheus.perception`) leaves a stale tests/conftest that fails at COLLECTION time and breaks a brand-new narrowly-scoped test, because pytest loads tests/conftest.py before collecting anything - update the conftest import and run the targeted test files directly instead of the full suite. This repo's parallel/import plugin chokes on module-level dataclass declarations in test files during collection; avoid them or run with `-n0`. Configure `norecursedirs` to skip the archive/ tree, since archived tests import packages that no longer resolve. A CI Python-test failure on a stacked PR may belong to the PARENT branch - inspect which file fails first and fix it on the parent, asserting the actual required-parameter message rather than a brittle literal like `--league`. metta pytest can be blocked by a private Git dep fetch (e.g. cortical) even outside the sandbox; fall back to the focused file with the local venv (`../.venv/bin/python -m pytest <file> -v -n0`) plus a direct toy-example run, and report the wrapper was blocked. Refresh node_modules against pnpm-lock.yaml before the CI lint entrypoint, or a stale JS install blocks the Python lint step that runs through it.
  <sub>sources: players_checkouts/players/archive/README.md, codex:019e012e-626f-7081-91fb-fccc04e39010, codex:019e0142-683b-72a2-b8b7-d3f985d5e433, codex:019e18d7-532e-7540-82ea-9abe1726aec7</sub>

#### 14. Open /dev/tty for curses TUIs so they work under piped/redirected harnesses
`generic` · **negative result** · ⚠ _session-derived, unverified_

curses `cbreak()`/`getch()` fails when stdin/stdout are not a real TTY (a subagent piping the command, or the cogames/Rich framework having grabbed the terminal). Open /dev/tty directly for the curses terminal so input works even when stdout is redirected, fall back gracefully when no TTY exists, and do not conclude a curses TUI is broken just because it fails under a piped test harness.
  <sub>sources: opencode:ses_1fa66f0b7ffeIF47rk2pDlz4RX</sub>

#### 15. Keep source ASCII-only and make session-id paths filesystem-portable
`generic`

Avoid non-ASCII section markers (e.g. the paragraph/section sign) in source files for encoding/portability: reference design-doc sections in plain ASCII inside code comments while keeping the special character only in the Markdown design doc. Likewise make session IDs filesystem-portable by replacing ':' with '-' in ISO8601 timestamps so paths are valid on Windows.
  <sub>sources: bitworld/among_them/players/modulabot/TRACING.md, opencode:ses_21b02c437ffeor4lV5Nb4Cec7y</sub>
