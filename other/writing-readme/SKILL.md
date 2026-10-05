---
name: writing-readme
description: Generate or update README.md files across three scopes — repo (with project-type detection), account (GitHub user profile), and org (organization profile). Use when creating, updating, or aligning a README to org conventions.
compatibility: Designed for Claude Code
metadata:
  argument-hint: <scope> [target]
  allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebFetch, Agent
  stability: stable
  content-hash: sha256:ac8830d64c179b095cb8713a541ea88ffeb5fcd32ad15f2ac6fa10e7cc5991d6
---

# Write README

**Scope**: $ARGUMENTS

Generate or update a README.md following scope-specific best practices.

## Phase 1: Detect Scope

Parse `$ARGUMENTS` to determine scope:

- `repo` (default) — README.md for a code repository in the current directory
- `repo <owner/repo>` — README.md for a specific remote repository
- `account <username>` — profile README for a GitHub user (`<username>/<username>/README.md`)
- `org <orgname>` — organization profile README (`.github/profile/README.md`)

If no scope is given, default to `repo` for the current working directory.

## Phase 2: Gather Context

### For `repo`

1. Read existing README.md (if any)
2. Detect project type:
   - `action.yml` / `action.yaml` exists → GitHub Action
   - `pyproject.toml` / `setup.py` → Python library
   - `package.json` → Node.js/TypeScript
   - `Cargo.toml` → Rust
   - `go.mod` → Go
3. Read project manifest for name, version, description, license
4. Scan source tree: `src/`, `lib/`, main entry points
5. Read LICENSE file
6. Check for existing docs: CONTRIBUTING.md, AGENTS.md, docs/

### For `account`

1. `gh api users/<username>` — bio, company, location, blog
2. `gh repo list <username> --limit 30 --json name,description,stargazerCount,primaryLanguage` — repos sorted by stars
3. Read existing `<username>/<username>/README.md` if it exists
4. Identify top 3-5 repos by stars or recent activity

### For `org`

1. `gh api orgs/<orgname>` — description, blog, location
2. `gh repo list <orgname> --limit 50 --json name,description,isPrivate,stargazerCount,primaryLanguage` — public repos
3. Read existing `.github/profile/README.md` or `.github/readme.md`
4. Group repos by domain/purpose
5. Identify pinned repos if any

## Phase 3: Apply Template

See `references/readme-templates.md` for the four template snippets and per-scope conventions (GitHub Action, Library/Application, Account, Organization). Repo READMEs follow the [qte77 doc-structure canon](https://github.com/qte77/qte77/blob/main/docs/doc-structure.md): value-first order Hero → Badges → What → How → Why → Refs → License → tail; badges License → Version → CI (static `blue` / native status, Version linked to `CHANGELOG.md`).

Pick the template matching the scope detected in Phase 1 and the project type detected in Phase 2.

## Phase 4: Generate

1. Draft the README applying the appropriate template
2. Verify all links resolve
3. Present the draft to the user for review
4. Write the file after user approval

## Rules

- Never add content the project doesn't have
- Keep descriptions factual — pull from existing docs, manifests, and code
- Don't add emojis unless the user requests them
- Prefer brevity — every sentence should earn its place
- For org READMEs: omit private repos unless the user explicitly asks
- License file is always `LICENSE` (never `LICENSE.md`)
- Repo READMEs derive from the qte77 doc-structure canon — never invent a divergent structure
