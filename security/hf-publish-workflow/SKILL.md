---
name: hf-publish-workflow
description: Automate Hugging Face model/dataset/space publishing from PowerShell with one-time auth, README card generation, `hf upload` commands, and optional `--create-pr` review flow. Use when users ask to log in to Hugging Face CLI, publish artifacts, add or update model/dataset/space cards, wire a reusable profile publish function (for example `scbe-hf-publish`), or troubleshoot common `hf` command usage.
---

# HF Publish Workflow

Publish artifact folders to Hugging Face repos with consistent auth checks, card updates, and safe upload defaults.

## Quick Start

Run these checks first:

```powershell
hf auth login
hf auth whoami
hf version
```

Use `hf version` and not `hf --version`.

## Publish Flow

1. Confirm repo type: `model`, `dataset`, or `space`.
2. Confirm the target repo id in `owner/name` format.
3. Generate or refresh `README.md` card content before upload.
4. Upload with an ISO timestamp commit message.
5. Use PR mode (`--create-pr`) when a review gate is desired.

Use these base commands:

```powershell
# Model
hf upload owner/repo . . --commit-message "publish: model $(Get-Date -Format s)"

# Dataset
hf upload owner/repo . . --repo-type=dataset --commit-message "publish: dataset $(Get-Date -Format s)"

# Space
hf upload owner/repo . . --repo-type=space --commit-message "publish: space $(Get-Date -Format s)"
```

Use PR mode when needed:

```powershell
hf upload owner/repo . . --create-pr --commit-message "publish via PR"
```

## README Generation

Generate the card before upload. Include:

- Summary of the artifact and problem domain
- Intended use and limitations
- Security notes (no secrets, deterministic tests)
- Repro steps
- License and citation
- Discoverability tags

When frontmatter is requested, read `references/card-frontmatter.md` and select the section matching repo type.

## Reusable PowerShell Function

Use `assets/scbe-hf-publish.ps1` as the canonical function definition.

To install:

```powershell
notepad $PROFILE
# Paste file contents from assets/scbe-hf-publish.ps1
. $PROFILE
```

## Output Rules

- Emit exact commands with concrete repo name and type.
- Prefer `--create-pr` when user asks for safer publish or review gating.
- Keep commit messages explicit and timestamped when no user message is provided.
- Refuse to expose tokens or embed secrets in files.
