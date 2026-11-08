---
name: super-linting
description: Set up local development linting by picking the right linters for each file type a project uses, then recording them as required pre-commit checks in AGENTS.md / CLAUDE.md and a `make lint` target. Uses the super-linter project as the live source of truth for which linters are current and popular per language. Use this skill whenever the user wants to add, choose, configure, or standardize linters for local development; asks "what linter should I use for X"; wants the agent to lint files before committing; sets up AGENTS.md/CLAUDE.md linting rules; or mentions super-linter, linting setup, pre-commit linting, or keeping linters up to date. This is for LOCAL developer/agent linting, not for authoring CI workflows.
license: MIT
---

# Super-Linting: local linters for every file type

Pick the right linter for each file type a project uses, then make those linters a required step before every commit — written as instructions the agent will follow in the project's agent guide, plus a `make lint` command a human can run.

## How linting gets enforced (default vs opt-in)

The **default** enforcement is soft and zero-install: a `## Linting` section in AGENTS.md/CLAUDE.md that tells the agent to lint before committing, backed by a `make lint` target. This is enough for most projects and adds no git machinery.

A git **pre-commit hook** is a stronger, harder gate (it blocks the actual `git commit`), but it's extra setup the user didn't necessarily ask for. So **do not add a git hook or a `pre-commit`-framework config by default.** After you've written the agent-guide contract, ask the user whether they want it:

> "I've set up linting as instructions in your agent guide + `make lint`. Want me to also add a real git pre-commit hook that blocks commits when a linter fails, or is relying on the agent (and `make lint`) enough for you?"

Only wire up `.githooks/` + a `make hooks` target (or a `.pre-commit-config.yaml`) if the user opts in. The point is to not surprise the user with git hooks they didn't request.

The goal is a tight local feedback loop: catch lint problems while code is being written, not in CI. This skill is **not** about building CI workflows (use the `github-actions-workflow-pro` skill for that). It is about equipping the agent and the human with the linters that fit _this_ project, drawn from the [super-linter](https://github.com/super-linter/super-linter) project's curated list so the recommendations stay current.

## Why super-linter as the source

super-linter aggregates the popular, well-maintained linters the community actually uses, organized by language. Rather than guessing or relying on a stale memory of "the Python linter," consult super-linter's live list so recommendations track what the ecosystem has moved to (for example, ruff's rise in Python). super-linter is the _catalog_; this skill turns that catalog into concrete local install + run commands and bakes them into the project's agent guide.

## Workflow

### 1. Decide scope — which file types matter

- If there's active work in progress (a feature being built, files in `git status`, files the user just asked you to create), scope to **those** file types. You only need linters for what's actually being written.
- If the user is setting up linting fresh for a repo, scan the project tree for the file types present and cover all of them.

Map the file extensions you find to languages. Use the extension → language table in `references/linter-commands.md` — super-linter organizes everything by language, not extension, so this mapping is the bridge.

### 2. Get the current linters from super-linter

Fetch the live super-linter list so the recommendation reflects today's ecosystem, not a cached guess:

- WebFetch `https://raw.githubusercontent.com/super-linter/super-linter/main/README.md` and read the **`## Supported linters and formatters`** table. The README is large and may truncate, so target that section specifically (prompt the fetch for "the Supported linters and formatters table rows for <languages>").
- Each row is `Language | Linters | Formatters`, with linter names as Markdown links to their home pages. Use it to confirm the current linter(s) for each language you care about.

If the fetch fails or is unavailable, fall back to the snapshot in `references/linter-commands.md` and say you used the offline fallback so the user knows it may lag the live list.

### 3. Choose linters: primary + optional

For each language, recommend **one primary linter** to install and run now — the canonical, lowest-friction choice (e.g. Python → `ruff`, Go → `golangci-lint`, Shell → `shellcheck`, YAML → `yamllint`, Dockerfile → `hadolint`, Markdown → `markdownlint`). `references/linter-commands.md` marks the primary pick per language.

List the _other_ linters super-linter runs for that language as **optional extras** the user can add later, but don't install everything by default — a wall of linters is the fastest way to get linting abandoned. Note any formatter (e.g. `black`, `prettier`, `terraform fmt`) separately, since formatting and linting are different jobs.

### 4. Check what's installed, then propose installs

Check whether each chosen linter is already on the system (e.g. `command -v ruff`). For anything missing, present the install command from `references/linter-commands.md`. Prefer the install method that matches the project and platform; on macOS, Homebrew is a good default when the linter offers it.

**Ask before installing anything.** Present the list of linters and their install commands, and let the user confirm. Don't silently install a pile of tools.

### 5. Write the linting contract into AGENTS.md / CLAUDE.md

This is the part that makes linting "required." Add (or update) a `## Linting` section in the project's agent guide so every future agent session runs the linters before committing. Detect the right file: if `AGENTS.md` or `CLAUDE.md` exists, edit it (note they may be symlinked — edit the real file). If neither exists, ask whether to create `AGENTS.md`.

Use this structure:

```markdown
## Linting

Before committing, lint every file type you changed and fix what the linter reports. Commits should be made only after the relevant linters pass. Run `make lint` to check everything at once.

| File type              | Linter     | Run                  |
| ---------------------- | ---------- | -------------------- |
| Python (`.py`)         | ruff       | `ruff check <files>` |
| Shell (`.sh`)          | shellcheck | `shellcheck <files>` |
| YAML (`.yml`, `.yaml`) | yamllint   | `yamllint <files>`   |

Optional extra linters available for this project: <list, or "none">.
```

Keep the table to the file types this project actually uses. Phrase it as a clear expectation with the reason (lint before commit so problems are caught locally), not a rigid wall of MUSTs.

### 6. Add a `make lint` target and document it

Give humans one command. Add a `lint` target to the `Makefile` (create the Makefile if there isn't one) that runs each chosen linter across the repo:

```makefile
.PHONY: lint
lint: ## Run all project linters
	ruff check .
	shellcheck **/*.sh
	yamllint .
```

Then document `make lint` in `README.md` so a human knows it exists. Match the repo's existing Makefile and README style if present.

Keep the Makefile to the `lint` target by default. Only add a `hooks` target (and the `.githooks/` hook it installs) if the user opted into a git pre-commit hook per the enforcement question above.

### 7. Summarize and offer the hook

Tell the user what you did: which file types you found, which linters you chose (primary vs optional) and why, what's installed vs still needs installing, and which files you edited (AGENTS.md/CLAUDE.md, Makefile, README.md). Call out anything you used the offline fallback for. Then ask the enforcement question from the top of this skill — whether they want a git pre-commit hook on top of the agent-guide contract, or prefer to rely on the agent + `make lint`. Don't add the hook unless they say yes.

## Reference

`references/linter-commands.md` — extension → language map, and per-language primary linter, install command(s), and local run command. This is the practical layer super-linter's README doesn't provide (it lists linters but not how to install or invoke them locally). Read it whenever you need an install or run command, or the file-type mapping.
