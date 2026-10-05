---
name: committing-staged-with-message
description: Generate commit message for staged changes, pause for approval, then commit. Stage files first with `git add`, then run this skill.
compatibility: Designed for Claude Code
metadata:
  model: haiku
  argument-hint: (no arguments needed)
  disable-model-invocation: true
  allowed-tools: Bash, Read, Glob, Grep
  stability: stable
  content-hash: sha256:a5e26885892265711ffcd5041fa0f6311b36aaa05d2f49b3c1343348ca953a4f
---

# Commit Staged with Generated Message

## Step 1: Analyze Staged Changes

Run using the Bash tool:

- `git diff --staged --name-only` — list staged files
- `git diff --staged --stat` — diff stats summary
- `git log --oneline -5` — recent commit style

**Size guard**: If `--stat` shows >10 files or >500 lines changed, skip full
diff and rely on `--stat` + `--name-only`. Otherwise also run `git diff --staged`
for detailed review.

## Step 2: Generate Commit Message

Read `.gitmessage` for format (conventional commits: `type[(scope)][!]: description`).

**Body guidelines (keep concise — no padding):**

1. **What changed**: bullet points per logical group
2. For large changes, include diff stats summary as last line

Keep the message laser-focused. Don't repeat the subject line in the body.
Small changes (1-2 files, <50 lines) need only a subject line, no body.

## Step 3: Pause for Approval

**Please review the commit message.**

- **Approve**: "yes", "y", "commit", "go ahead"
- **Edit**: Provide your preferred message
- **Cancel**: "no", "cancel", "stop"

## Step 4: Commit

Once approved:

- `git commit --gpg-sign -m "[message]"` — GPG signature mandatory
- `git status` — verify success
