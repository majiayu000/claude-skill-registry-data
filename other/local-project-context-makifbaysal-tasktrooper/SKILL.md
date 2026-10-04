---
name: local-project-context
category: tools
description: The local task workspace, the build/test commands the hand-off gate runs, and the file and exploration tools. Use when starting work in a task workspace or before running any build, test or verification command.
---
# Local Project Context

## Overview

You run on a local developer machine, not in a CI/CD pipeline. There is no remote runner that will catch your mistakes later — the build and tests you run in your workspace are the only verification that happens before a human sees the result. Treat your workspace as production's last line of defense.

**Core principle:** Explore before you change; verify in this environment before you claim.

## The environment

- **Task workspace:** each task is worked in a cloned checkout on its own branch. Your working directory is injected into the session context — always use it as the root, never assume paths from another task.
- **Live codebase:** your changes take effect immediately in the workspace. There is no separate deploy step for verification.
- **No inherited state:** if you build or test in this workspace, do it from scratch — never assume a prior session left a build artifact, a running server, or a seeded database.

## Exploration tools (use before changing code)

| Tool | Use for |
|------|---------|
| `codebase_search` | Concept/semantic search — "where is auth handled" |
| `grep_code` | Exact symbol/string — a function name, an error message |
| `get_repo_tree` | Structure and file layout of the repository |
| `get_symbol_skeleton` | A symbol's signature and outline without its full body |
| `expand_symbol_context` | Focused read of a symbol and its surroundings |
| `read_file` | Read a file with line numbers — up to 800 lines per call |
| `run_terminal` | Build, test, run the app, inspect output |

## File tools (use instead of the shell for anything touching a file)

| Tool | Use for |
|------|---------|
| `read_file` | Read with line numbers, whole file in one call |
| `edit_file` | Replace an exact string; `replace_all: true` changes every occurrence at once |
| `edit_lines` | Replace / insert / delete by line number — add a function, an import, remove a block |
| `write_file` | Create a file, or replace one whole |
| `delete_file` | Remove a file or directory |
| `move_file` | Rename or move |

Never `cat`, `sed -n`, `head`, `tail`, `sed -i`, `rm`, `mv` or a heredoc through the shell. A shell read costs a full agent turn per window; a `sed -i` is silent about what it matched, so you spend a second turn grepping to find out whether it worked; and a heredoc mangles backticks, quotes and template literals.

Every file tool reports what it did — the number of occurrences changed, the line numbers, the region as it now reads. **That is your confirmation. Do not grep or re-read the file to check.** One edit is one turn.

In a CLI runtime (Claude Code / Codex / opencode) `read_file`, `edit_file`, `write_file`, `run_terminal`, `grep_code` and `get_repo_tree` are your native Read/Edit/Write/Bash/Grep/Glob — same rules apply.

Find the existing pattern first (the neighboring endpoint, the similar component, the analogous test) and follow it. A parallel convention you invent is a review finding waiting to happen.

## Verification (use before every handoff)

The build gate that runs after your run executes exactly the component's required checks — `list_component_checks` returns them with the local command that reproduces each. Run those commands, not a guessed one. The table below is only the fallback when no checks are mapped:

| Stack | Build | Test |
|-------|-------|------|
| Go | `go build ./... && go vet ./...` | `go test ./...` (or the affected `./path/...`) |
| Java | `./mvnw -q verify` / `./gradlew build` | (included) |
| Web | `npm run build` in the package that holds `package.json` | `npx vitest run` or `CI=1 npm test` — never watch mode |
| Flutter | `flutter analyze` | `flutter test` (a build needs a target: `flutter build apk --debug`, `flutter build web`) |

Full builds and suites outlast `run_terminal`'s 60s default: pass `timeout_seconds` (up to 900). Redirect long output to a file and read its tail (`… > /tmp/test.log 2>&1; tail -80 /tmp/test.log`).

If the build or tests do not pass in this run, the task is not ready to move forward — say what failed.

## Your role

- **Developers:** all of the above — explore, edit, build and test the whole stack.
- **QA:** black-box. Exploration is `get_repo_tree`, `grep_code`, `read_file` only — to find the start command, the port and the route, never the diff, to decide a verdict. The file tools above are still yours for your own scratch work (a fixture, a script), never for product code.
- **Architect at code_review:** read, never run. The code tools above are for reading the diff and the surrounding code; building or testing it yourself is not your job and not your evidence — the developer's run already did that.

## Common Mistakes

- Reasoning about behavior from reading code instead of running it — except at code_review, where reading the diff IS the job.
- Reusing a path or branch name from a previous task's workspace.
- Assuming `npm install` / `go mod download` already ran — check, don't assume.

## Red Flags

- "It built last time" — build again, now (unless you are the architect: you never build).
- "The server should still be running" — never assume; start it.
