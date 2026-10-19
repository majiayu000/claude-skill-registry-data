---
name: tooling-analysis
description: "Use for reusable tooling analysis recipes in software and coding-agent work."
---

# Tooling & analysis — recipes (generic tier)

On-demand recipes (5). Trigger→action heuristics; pull the relevant one when its situation arises.

#### 1. Render traces human-readably, store them in a stable repo dir, and confirm the specific bot is wired
`generic` · ⚠ _session-derived, unverified_

Ship a small formatter/viewer alongside raw JSONL traces -- raw JSONL is hard to scan and a trace is only useful if a human or agent can read it. Store traces in a stable, documented repo-relative directory (e.g. traces/ under the player package), never /tmp, where temp traces get wiped and the next session's tooling won't look. Observability is per-bot, not a framework property: in Among Them, evidencebot_v2 wrote no trace files (only a stdout 'frames dropped' line) while siblings mod_talks and modulabot each had a dedicated trace.nim -- before trying to 'read the traces,' confirm the specific player has tracing wired, since empty trace files despite a visibly-acting bot means broken plumbing, not behavior; verify which directory actually receives traces.
  <sub>sources: opencode:ses_21a708a4dffeBXpeHY15fnGABP, opencode:ses_1fecece4dffe779FmeajgdwhMD, opencode:ses_200be1a72ffevDDc1PULNNG9UF</sub>

#### 2. Commit cheap provenance, gitignore regenerable artifacts in a replay cache
`generic`

When building a replay-cache/analysis tool, extract a small per-episode metadata file (seed, map size, scores, split assignments, game/agent stats) at download time and store it separately from the multi-MB compressed replay so list/analyze commands run without decompressing. Commit the small index.json and metadata/ (they document what has been reviewed) but gitignore the large reproducibly-downloadable raw replays (~2-5 MB each compressed) -- commit cheap provenance, not bulky regenerable artifacts. Match project CLI conventions (argparse add_subparsers, sys.exit(main()), a _REPO_ROOT import shim, ThreadPoolExecutor for I/O-bound downloads, as in ab.py).
  <sub>sources: archive/cogames_playground/alpha_cog/docs/league-replay-tool-design.md</sub>

#### 3. Scope a regression with git first; watch for shadowed functions, unresolved diff paths, hidden test collection, and over-broad edits
`generic` · ⚠ _session-derived, unverified_

When a bot misbehaves or you suspect upstream broke tooling, scope the window with git BEFORE reading game logic: list commits since a known-good date and classify each diff (decision-logic vs packaging; policy-API / env-config / tournament-runner / CLI). Eliminate behavior-neutral commits fast -- changes entirely inside build-flag-guarded blocks (`when defined(...)`) or FFI-only export renames don't affect the default run path, and most monorepo commits are server-side. A locally-defined function can silently shadow an imported one of the same name (a compile-time currentSourcePath()-based gameDir() shadowing an imported getCurrentDir()-based one) -- grep the file for a same-named local def before tracing the import. An empty/surprising `git diff` may mean the path arg did not resolve to a real tree (running `git diff HEAD -- among_them/guided_bot` from inside among_them silently diffs a nonexistent path) -- verify cwd and path resolution. To find the PR that introduced a contract, search stable code identifiers (env-var/constant names) in the code, not PR title/body words; a public name can be renamed within the same PR, so read current `main`. A broken import path can silently hide a test suite by preventing COLLECTION (three files using bare `from perception import` vs `from orpheus.perception import` dropped ~1200 lines / 151 tests) -- check collected-vs-passing counts, not just pass counts. A search-and-replace whose oldString recurs can match the LAST occurrence and delete a much larger span (file shrank 2237->1401 lines, ~836 lost) -- uniquely anchor oldString and verify line-count deltas after large edits.
  <sub>sources: opencode:ses_200be1a72ffevDDc1PULNNG9UF, opencode:ses_201bc0c24ffe4uYJuw52Gs42LG, opencode:ses_201972733ffexPIP9mq6yEDpqJ, opencode:ses_200deb284ffe7RFSHqkkWQqwAx (+3)</sub>

#### 4. Recover interfaces from bytecode/git history, fix import cycles without copied constants, clean generator debris, and rebase stacks
`generic`

If a session times out mid-rewrite and leaves a Python module deleted, the surviving __pycache__/<name>.cpython-3XX.pyc (from an earlier import) is the best recovery source -- it preserves function names, imports, constants, and line numbers, so reconstruct from it rather than stubbing. When tooling targets a .gitignore'd framework dir, read the API from GIT HISTORY, not the working tree (the ignored dir held only cached bytecode while the real source lived in history); and beware implicit layout conventions in path resolution -- a resolver computed package_source_root = framework_dir.parent/'src', so --agent-framework-dir /x/coborg_framework silently implied /x/src/cogames_agents/..., invisible until it resolves to a stale checkout, so make adjacent-layout assumptions explicit in errors and docs. Avoid copying numeric constants to dodge an import cycle: put shared constants in a tiny dependency-free module and re-export through the package's constants module. Clean engine-checkout debris immediately -- a temporary generator with a misparsed arg wrote a stray file literally named `--` into the engine root; detect/remove such debris and harden arg parsing (read the last arg so both invocation forms are safe). Graphite non-interactive submit aborts when a stacked branch's PR is already merged but trunk lacks it; `gt sync` to update main, `gt move` the branch onto fresh main, and resubmit. To recover deleted files with exact prior content, restore from the commit BEFORE the deletion: verify the file exists at <delete-commit>^ then run git checkout <delete-commit>^ -- <path>, confirm fidelity by matching restored line counts against the deletion commit's diff stats (note git checkout <commit> -- <path> auto-stages; git reset HEAD <path> to unstage).
  <sub>sources: codex:019e05ca-d8e8-7d02-adf9-43354a64543b, codex:019e1940-5a75-7f51-b057-63f894ddb061, codex:019e147f-2fcd-7e83-93ab-fab57ce504b4, codex:019eaee5-b54e-79f2-bf0f-ac59a6a1eae2 (+2)</sub>

#### 5. Coerce forwarded kwargs to declared types (bool before int); deep-merge config tweaks
`generic`

When a runner forwards CLI kwargs as kw.<name>=<value> strings, coerce each string to the declared dataclass/field type before applying it, and check bool BEFORE int (bool is an int subclass, so 'True' coerces wrong otherwise). Route nested config via a prefix like section__<field>, and WARN rather than error on unknown knobs, since a sweep/orchestration harness often shares one kwarg set across multiple consumers. Prefer a launcher that deep-merges an inline JSON config tweak with the defaults (e.g. --config-json '{...}') so you can change one field without re-specifying the full config; keep named-preset, full-file, and inline-JSON config inputs mutually exclusive.
  <sub>sources: optimizers/.cursor/skills/scripted-navigation/SKILL.md, optimizers/.cursor/skills/scripted-navigation/reference.md, players_checkouts/players/users/james/personal_cogs/persephone/GAME_AP, players_checkouts/players/users/james/personal_cogs/persephone/README.</sub>
