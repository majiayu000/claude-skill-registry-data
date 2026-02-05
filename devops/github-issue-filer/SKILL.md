---
name: github-issue-filer
description: File AnyPod GitHub issues (bug or feature) with the official templates and publish them through the gh CLI.
---

# GitHub Issue Filer

## What This Skill Delivers

Files bug reports and feature requests in `thurstonsand/anypod` using the repository’s issue templates.

Use this skill whenever someone needs to create a GitHub issuefor a bug or feature.

## How to Use the Skill

### 1. Pick the template
- Bug report → pass `bug`
- Feature request → pass `feature`
- Inspect the current fields anytime:
  ```bash
  ./.claude/skills/github-issue-filer/scripts/create_issue.py bug --describe
  ```

### Command options
- `--summary`: Replaces `<summary>` in the template title (e.g., `[bug] <summary>`).
- `--data-file`: Provide a path to the JSON payload instead of piping it via STDIN.
- `--describe`: Prints the field list (identifier, description, optional flag, type, options) so you can see which inputs are available.

### 2. Gather inputs
- Capture a concise summary to replace `<summary>` in the template title (e.g., “downloads stall on restart”).
- Required fields:
  - Bug: `happened` (what went wrong)
  - Feature: `problem` (why the change matters)
- If the user did not provide information for the optional fields (logs, YAML, environment, sources, etc.), ask them if they want to include this info. If the user declines, move on—do not block.
- Keep answers short, remove secrets, and paste raw text; the script will format it.
- Need a reminder of available fields? Run `create_issue.py bug|feature --describe` for the relevant template.

### 3. Build the JSON payload
Create a JSON object whose keys match the template IDs.

Example bug payload:
```json
{
  "happened": "testing out this template",
  "expected": "as expected",
  "steps": "1. start container\n2. call endpoint",
  "source": "X/Twitter",
  "version": "nightly",
  "env": "TrueNAS SCALE",
  "feed_yaml": "feeds:\n  myfeed:\n    url: https://...",
  "logs": "error lines here"
}
```
Example feature payload:
```json
{
  "problem": "listeners can’t filter Patreon tiers",
  "solution": "allow tier filter per feed",
  "sources": ["Patreon"],
  "context": "original request in Discord #support"
}
```
If the conversation already contains these facts, extract them yourself instead of re-asking.

### 4. Run `create_issue.py`
Execute the helper with the template name, summary, and JSON payload via STDIN:
```bash
./.claude/skills/github-issue-filer/scripts/create_issue.py \
  bug \
  --summary "downloads stall on restart" <<'JSON'
{...payload...}
JSON
```
Feature example:
```bash
./.claude/skills/github-issue-filer/scripts/create_issue.py \
  feature \
  --summary "make Patreon feeds filter tiers" <<'JSON'
{...feature payload...}
JSON
```

### 5. Share the result
Return the printed URL (and, if helpful, the confirmation output).
