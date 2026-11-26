---
name: "gh-issue-push"
description: "Create a GitHub issue in the current repository."
---

# gh-issue-push command

Apply this command workflow. Treat any text after its invocation as the command input.

Create a GitHub issue in the current repository.

## Input

$ARGUMENTS

## Steps

1. Detect the repo: run `gh repo view --json nameWithOwner -q .nameWithOwner` and use the result as `<owner>/<repo>` for all `gh` commands.
2. Determine type from the input: keywords like "bug", "fix", "broken", "crash" → bug; otherwise → enhancement.
3. **Trace what the change touches.** Before drafting, identify every file and field affected — not just the primary target. The executor will do exactly what the issue says and nothing else, so anything omitted will be missed.
   - Read the files involved to understand their structure.
   - `grep` for identifiers, names, or values being added, changed, renamed, or deleted. Search the full project, not just the obvious files.
   - For each hit, note the file path, the field or line, and what needs to change.
   - Check for status fields, summary fields, titles, index entries, cross-reference IDs, and out_of_scope references — these are the most commonly missed.
4. Draft a concise title and well-structured body.
   - **Bug**: problem, expected vs actual behavior, reproduction steps if provided.
   - **Enhancement**: description and acceptance criteria.
   - **Both**: include a "Files to Create/Modify" section listing every file. Under each file, list the specific fields or lines to change. If a value appears in multiple places in the same file, list each occurrence.
   - **Code issues**: include an `Estimated LOC:` line — the model's prediction of production lines of code (and test lines if separable). This is the estimate of record; the actual count is captured at completion by `/gh-issue-pop`, so estimation accuracy can be tracked over time.
5. Create the issue:
   ```
   gh issue create --repo <owner>/<repo> --title "<title>" --body "<body>" --label "<bug|enhancement>"
   ```
6. Report the issue URL.
