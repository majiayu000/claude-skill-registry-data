---
name: update-readme
description: >-
  Load this skill when a change alters how someone installs, runs, or configures the project (a new
  feature, command, setup step, dependency, environment variable, or public API) and README.md must
  catch up. Trigger on "update the readme", "document this feature". Not for bug fixes or refactors.
disable-model-invocation: false
user-invocable: true
compatibility: >-
  Requires the git CLI on PATH and a git working tree, to read what changed via `git diff` and
  `git status`. Nothing else is needed - the output is Markdown.
license: Apache-2.0
---

# Update README

Keep the project's README.md accurate after a significant change. Prefer surgical edits over
rewrites. Do nothing when nothing material changed.

## Procedure

### 1. Pass the significance gate

Before touching the README, confirm at least one applies:

- New user-facing feature, command, flag, or endpoint
- Installation, build, or run instructions changed
- Dependencies, runtime versions, or environment variables changed
- Configuration file format or required config keys changed
- Project structure changed in a way a new contributor needs to know
- Public API (exported functions, CLI surface, HTTP routes) changed
- Project purpose, name, or scope changed

If none apply, stop (see Stop conditions).

### 2. Discover

1. Find the README: check `README.md` at root, then `readme.md`, `README.rst`, `docs/README.md`. If
   none exists and the change is significant, create `README.md` at root.
2. Understand what changed: `git diff HEAD~1 HEAD` or `git status` + `git diff`. Look at changed
   files, new top-level files, changes to the project's dependency/build manifest (e.g.
   `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `*.csproj`), new CLI args, route
   definitions, `.env.example`.
3. Read the current README fully before editing.

### 3. Edit the sections the diff touches

Only update sections the diff touches:

- Title/tagline (scope changed)
- Features/What it does (new capability)
- Installation (deps or steps changed)
- Quick start/Usage (entry command or basic flow changed)
- Configuration (env vars or config keys changed)
- API reference/Commands (public surface changed)
- Project structure (top-level layout changed)
- Requirements/Prerequisites (runtime version or system deps changed)

Do not touch license, contributing guidelines, acknowledgments, or badges, unless the change
specifically requires it.

### 4. Check what the README still claims

Mentioning the new feature is half the job. The other half is the claims the diff made false. Grep
the README for every name the diff removed or renamed (command, flag, env var, route, file path,
config key) and fix each hit. Check each example command and path in the sections you touched
against the current code.

## Rules

- **Surgical edits.** Update only sections affected by the change. Never rewrite the whole README
  when a few edits suffice.
- **Match existing voice.** Preserve tone, heading style, formatting conventions, and keep the prose
  plain and technical.
- **Update in place.** No "Recent changes" section: that is `CHANGELOG.md`.
- **No speculation.** Only document what you can verify from the code.
- **Keep examples runnable.** Flags, args, and paths must match current code.
- **Update the table of contents** if one exists and you added or removed a section.
- Never delete existing content unless it is factually wrong.
- Never commit or push. The caller owns commit order, and a README edit lands in the change's own
  commit.
- In a monorepo, update only the READMEs affected by the change.

## Stop conditions

- No item of the significance gate applies → respond with
  `No README update needed — change is internal/minor.` and stop.
