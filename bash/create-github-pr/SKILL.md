---
name: create-github-pr
description: Create GitHub pull requests with deterministic commands, transient failure recovery, and content validation. Use when creating a pull request to ensure the final PR body on GitHub matches what was intended.
disable-model-invocation: true
allowed-tools: Bash, Read, Write, Glob, Grep
---

# Create GitHub Pull Request

Create GitHub pull requests reliably by writing the body to a file first, creating the PR from that
file, and validating the result. This workflow avoids the subshell and quoting pitfalls that cause
silent content loss.

## Workflow

Follow these steps for **every** PR you create. Do not skip or combine steps.

### Step 1: Write the body to a temp file

Write the complete PR body to a Markdown file under `/tmp/`. Use a descriptive filename
(e.g., `/tmp/gh-pr-add-widget.md`). This is now the **source of truth** for what the PR body
should contain.

Do NOT use inline `--body "$(cat <<'EOF' ... EOF)"` or `--body "$(subcommand)"` patterns.
Subshells can silently return empty on transient network failures, wiping the entire body.

### Step 2: Create the PR

Use `--body-file` to pass the body:

```bash
gh pr create \
  --title "Your title here" \
  --body-file /tmp/gh-pr-add-widget.md
```

Capture the output URL and extract the PR number. If the command fails entirely (non-zero exit),
retry up to 2 times with a 5-second pause between attempts.

### Step 3: Validate the created PR

Run the validation script, passing the PR number and the source-of-truth file:

```bash
python3 .claude/skills/create-github-pr/scripts/validate_pr.py <pr-number> /tmp/gh-pr-add-widget.md
```

The script fetches the live PR body from GitHub and compares it against the file. It exits 0 if
they match, or exits 1 with a diff showing exactly what diverged.

### Step 4: If validation fails, repair and re-validate

If the script reports a mismatch:

1. **Repair**: `gh pr edit <number> --body-file /tmp/gh-pr-add-widget.md`
2. **Re-validate**: Run the validation script again.
3. If it still fails after 2 repair attempts, stop and report the failure to the user.

### Step 5: Clean up

After the PR is created and validated, delete the temp file:

```bash
rm /tmp/gh-pr-*.md
```

## Updating an existing PR

When modifying an existing PR's body, follow the same file-first pattern:

1. Fetch the current body to a file: `gh pr view <number> --json body --jq .body > /tmp/gh-pr-<number>-current.md`
2. **Validate the fetch succeeded**: Check that the file is non-empty and starts with expected content. If the file is empty or clearly truncated, retry the fetch up to 2 times before proceeding.
3. Edit the file (append, modify, etc.)
4. Apply: `gh pr edit <number> --body-file /tmp/gh-pr-<number>-current.md`
5. Validate with the script, using the edited file as the source of truth
6. If validation fails, repair and re-validate as in Step 4
