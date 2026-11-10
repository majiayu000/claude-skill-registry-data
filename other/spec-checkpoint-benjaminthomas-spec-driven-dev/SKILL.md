---
name: spec-checkpoint
description: >
  Create a comprehensive checkpoint commit with detailed analysis of all changes. Use this skill
  when the user says "checkpoint", "commit everything", "save my progress", "create a commit",
  or wants to stage and commit all current changes with a well-crafted message. Also use when
  the user says "/spec-checkpoint" (or their host's equivalent invocation syntax) or asks to
  snapshot current work. This skill stages all changes and creates a descriptive commit — it
  does not push.
license: MIT
---

# Checkpoint Commit

Create a checkpoint commit that captures all current changes — but only after the code passes lint, type check, and build.

## Project config (read first)

Load `.spec-driven.yml`: walk up from the current directory to the home folder, and the first one
found wins (a `multi-repo` config only applies inside the repos it lists). If none is found, check
`~/.spec-driven/workspaces.json`, which maps each multi-repo config to its repo paths. Use the config
whose repos contain the current directory, because a workspace's repos can live in unrelated folders. Its values beat anything
you would detect or assume. This skill uses `commands` (lint/typecheck/test/build), `git.commit_style`, and `layout`/`repos`.

**Multi-repo:** run this in every listed repo that has changes, making one commit per repo with the same subject. **Monorepo:** run the checks for the packages that changed, or the root commands if that's how the repo works.

**No config?** If the `spec-setup` skill is available, run it first, then continue here. If it
isn't, detect what this skill needs from the repo, ask about anything ambiguous, and offer to save
the answers to `.spec-driven.yml` (keys: `layout`, `repos`, `tracker`, `git`, `commands`,
`specs_dir`).

## Instructions

### Step 1: Analyze Changes

Run these commands to understand the full picture:

1. `git status` — see all tracked and untracked files
2. `git diff` — see detailed changes in tracked files
3. `git diff --cached` — see already-staged changes
4. `git log -5 --oneline` — understand this repo's commit message style

### Step 2: Quality Checks

Use `commands` from `.spec-driven.yml`. For any that are missing, find the repo's own lint, typecheck, test, and build commands — `package.json` scripts (with the
repo's package manager), `Makefile`, `pyproject.toml`, `Cargo.toml`, CI config, or `CLAUDE.md`/
`AGENTS.md`. Run each one the repo has; skip (and say so) any it doesn't. If any fail, fix the
issues before proceeding — do not skip or ignore failures.

Iterate until every check passes cleanly. Only then move to the next step.

### Step 3: Stage Everything

Stage all changes — tracked modifications, deletions, and new untracked files:

```bash
git add -A
```

Then review `git status` again. If anything staged looks like it could hold secrets —
`.env*`, `*.pem`, `*_rsa`, `credentials.json`, `secrets.*`, or an unfamiliar filename that might
contain an API key — unstage it (`git restore --staged <file>`) and tell the user what was
excluded and why, rather than committing it silently. Don't rely on the filename alone for
anything you don't recognize; skim its diff if you're unsure.

### Step 4: Craft the Commit Message

Write a commit message in the config's `git.commit_style` (`conventional` → `feat: …`, `ticket` → `STP-123: …` using the ticket ID from the branch name, `freeform`). Without config, follow the project's existing conventions (observed from `git log`). Structure:

- **First line**: clear, concise summary in imperative mood (50-72 chars)
  - Use conventional commit prefixes where the project uses them: `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`, etc.
- **Body** (separated by blank line): a short TL;DR of the changes — 1-3 sentences max. No bullet lists, no file-by-file breakdowns, no lengthy explanations.
- **Footer**: co-author attribution, naming whichever agent/model is actually running this
  skill — never hardcode a specific vendor or model name, since this skill runs under many
  different hosts

### Step 5: Commit

Create the commit using a heredoc for proper formatting:

```bash
git commit -m "$(cat <<'EOF'
{first line}

{tldr}

Co-Authored-By: {agent name} <noreply@example.com>
EOF
)"
```

Fill in `{agent name}` with whatever the current agent/model actually identifies as (e.g. "Claude", "Codex", "Cursor Agent") — if your host has no clean way to identify itself, omit the footer entirely rather than guessing.

### Step 6: Report

Display:
- The commit hash and message summary
- Files changed count
- Insertions/deletions summary

## Important

- Stage and commit everything except files that look like secrets or credentials (see Step 3) — check contents, not just filenames, before assuming something is safe to commit
- If the repo has no git history, run `git init` first
- All quality checks (lint, type-check, build) MUST pass before committing — fix issues, don't skip them
- Keep the commit body short — a TL;DR, not an essay
- Follow the project's existing commit conventions (check the log first)
- Do not push — only commit locally
