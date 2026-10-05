---
name: agent-copy
description: Use when the user asks to copy, install, refresh, or update a repo-root AGENTS.md file from their canonical global instruction source. Also use when the user says "agent copy" or wants a repo-local AGENTS.md with global operating rules plus project-specific guidance.
metadata:
  short-description: Copy canonical instructions into a repo and append repo-specific guidance
---

# Agent Copy

This skill creates or refreshes a repo-root `AGENTS.md` file by copying the user's canonical global agent instructions, then appending a repo-specific guide for the current project.

Architecture:

```text
canonical global instructions -> repo-local AGENTS.md -> repo-specific tail
```

Use one `agent-copy` skill for this workflow. Do not create separate runtime-specific variants such as `agent-copy-codex`, `agent-copy-claude`, or `agent-copy-cursor`; change the source path instead.

Default source:

- `$HOME/.codex/AGENTS.md`

Default target:

- `./AGENTS.md`

Codex is the default because this repo demonstrates a Codex-first setup. If the user's canonical instructions live somewhere else, use that source path instead. Examples include a Claude project instruction file, an OpenCode context file, or another agent-compatible global instruction file.

Only `AGENTS.md` files should be created, copied, or updated unless the user explicitly asks for another instruction file.

## Core Rule

The repo-root `./AGENTS.md` file must:

1. Start with an exact copy of the selected canonical global instruction source.
2. Append a repo-specific tail section titled `## Repo-Specific Guide`.
3. Include only repo facts from filesystem inspection or the user's answers.
4. Mark unknowns as `TBD - ask the user before implementing this area.`

Do not paraphrase, summarize, or partially copy the canonical source file.

## Workflow

### 1. Confirm The Canonical Source File

Check for the default source:

```bash
test -f "$HOME/.codex/AGENTS.md" && echo "$HOME/.codex/AGENTS.md"
```

If the file does not exist and the user wants Codex as the canonical source, tell the user to install the repo's root `AGENTS.md` template into their Codex root first:

```bash
mkdir -p "$HOME/.codex"
cp AGENTS.md "$HOME/.codex/AGENTS.md"
```

If the user is not using Codex, ask for the exact path to their equivalent canonical instruction file before copying anything.

### 2. Ground In The Repo

Run before editing:

```bash
pwd
git status --short --branch
git branch --show-current
git remote -v
find . -maxdepth 2 -type f \( -name 'package.json' -o -name 'pnpm-lock.yaml' -o -name 'package-lock.json' -o -name 'yarn.lock' -o -name 'pyproject.toml' -o -name 'requirements.txt' -o -name 'go.mod' -o -name 'Cargo.toml' -o -name '.env.example' -o -name 'README.md' -o -name 'DESIGN.md' \) -print
find . -maxdepth 3 \( -name AGENTS.md -o -name CLAUDE.md \) -print
```

Scan and read existing repo docs/manifests before writing repo-specific details.

### 3. Preserve Existing Repo-Specific Content

If `./AGENTS.md` already exists:

- Read it first.
- Preserve useful repo-specific guidance unless the user asked to replace it.
- Refresh the global preamble from the selected canonical source.
- Keep the repo-specific tail after the global preamble.

If existing repo instructions conflict with the selected canonical source, keep the canonical source rules unless the user explicitly says the repo is an exception.

### 4. Write The Repo-Specific Tail

Append this section after the global preamble. Populate known fields from the user's project description, `README.md`, `DESIGN.md`, package manifests, lockfiles, env examples, app directory structure, existing scripts, and tests.

Never invent production credentials, live deployment state, database schema, auth policy, or external integrations.

```md
## Repo-Specific Guide

### Project Overview

### Product Goal

### Audience / Users

### Key Directories / Docs / Scripts

### Stack / Architecture

### Local Dev Commands

### Build / Test / Verification

### Branch / Git Workflow

### Boundaries / Do Not Touch

### Implementation Notes
```

## Verification

After writing:

```bash
SOURCE_AGENTS="${SOURCE_AGENTS:-$HOME/.codex/AGENTS.md}"
head -n "$(wc -l < "$SOURCE_AGENTS")" ./AGENTS.md | cmp "$SOURCE_AGENTS" -
rg -n "Repo-Specific Guide|Project Overview|Product Goal|Stack / Architecture|Build / Test / Verification|Boundaries / Do Not Touch|Implementation Notes" ./AGENTS.md
git status --short --branch
```

If a non-default source was used, set `SOURCE_AGENTS` to that path before verification.

Report whether the global preamble verification passed.

## Handoff

Final response should include:

- files created or updated
- which canonical source file was used
- whether the global preamble matches the source
- which repo-specific sections were populated
- which sections remain blank or need user confirmation
- current git status

Commit only when the user explicitly asked for commit/push or the current task includes publishing.
