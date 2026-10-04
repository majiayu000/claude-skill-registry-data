---
name: create-github-issue
description: Create GitHub issues with deterministic commands, transient failure recovery, and content validation. Use when creating one or more GitHub issues to ensure the final issue body on GitHub matches what was intended.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Create GitHub Issue

Create GitHub issues reliably by writing the body to a file first, creating the issue from that file,
and validating the result. This workflow avoids the subshell and quoting pitfalls that cause silent
content loss.

## Workflow

Follow these steps for **every** issue you create. Do not skip or combine steps.

### Step 1: Write the body to a temp file

Write the complete issue body to a Markdown file under `/tmp/`. Use a descriptive filename
(e.g., `/tmp/gh-issue-audit-hooks.md`). This is now the **source of truth** for what the issue
should contain.

Do NOT use inline `--body "$(cat <<'EOF' ... EOF)"` or `--body "$(subcommand)"` patterns.
Subshells can silently return empty on transient network failures, wiping the entire body.

### Step 2: Create the issue

Use `--body-file` to pass the body:

```bash
gh issue create \
  --title "Your title here" \
  --body-file /tmp/gh-issue-audit-hooks.md \
  --label "label1,label2"
```

Capture the output URL. If the command fails entirely (non-zero exit), retry up to 2 times with a
5-second pause between attempts.

### Step 3: Validate the created issue

Run the validation script, passing the issue number and the source-of-truth file:

```bash
python3 .claude/skills/create-github-issue/scripts/validate_issue.py <issue-number> /tmp/gh-issue-audit-hooks.md
```

The script fetches the live issue body from GitHub and compares it against the file. It exits 0 if
they match, or exits 1 with a diff showing exactly what diverged.

### Step 4: If validation fails, repair and re-validate

If the script reports a mismatch:

1. **Repair**: `gh issue edit <number> --body-file /tmp/gh-issue-audit-hooks.md`
2. **Re-validate**: Run the validation script again.
3. If it still fails after 2 repair attempts, stop and report the failure to the user.

### Step 5: Clean up

After all issues are created and validated, delete the temp files:

```bash
rm /tmp/gh-issue-*.md
```

## Updating an existing issue

When appending or modifying an existing issue's body, follow the same file-first pattern:

1. Fetch the current body to a file: `gh issue view <number> --json body --jq .body > /tmp/gh-issue-<number>-current.md`
2. **Validate the fetch succeeded**: Check that the file is non-empty and starts with expected content (e.g., `## Problem`). If the file is empty or clearly truncated, retry the fetch up to 2 times before proceeding.
3. Edit the file (append, modify, etc.)
4. Apply: `gh issue edit <number> --body-file /tmp/gh-issue-<number>-current.md`
5. Validate with the script, using the edited file as the source of truth
6. If validation fails, repair and re-validate as in Step 4

## Batch creation

When creating multiple issues, process them sequentially — create, validate, then move to the next.
Do NOT create issues in parallel; transient failures are harder to diagnose and recover from when
interleaved. You may prepare all temp files in parallel, but issue creation must be serial.

## Labels

If your issue needs labels that may not exist yet, create them first:

```bash
gh label create "label-name" --description "Description" --color "0E8A16" 2>/dev/null || true
```

The `|| true` ensures idempotency if the label already exists.
