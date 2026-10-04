---
name: owasp-update
description: >
  Update the local OWASP cheat sheet cache. Use when the user explicitly runs /owasp-update
  to refresh cached OWASP Cheat Sheet Series content for the current project's language.
allowed-tools: Bash Read
---

# OWASP Cache Update

Fetch or refresh OWASP Cheat Sheet Series content for the current project.
This skill is user-invoked only (`/owasp-update`). It never runs automatically.

## Workflow

### 1. Detect Project Language

Scan the project for language signals:

| Language | Detection signals |
|---|---|
| Python | `*.py`, `requirements.txt`, `Pipfile`, `pyproject.toml`, `poetry.lock`, `uv.lock` |
| JavaScript/TypeScript | `*.js`, `*.ts`, `package.json`, `tsconfig.json`, `next.config.*` |
| Go | `*.go`, `go.mod`, `go.sum` |
| Java | `*.java`, `pom.xml`, `build.gradle`, `build.gradle.kts` |
| C# | `*.cs`, `*.csproj`, `*.sln`, `global.json` |

If multiple languages detected, update cache for all of them.
If no language detected, inform user and exit.

### 2. Read Reference File

Load `.claude/skills/owasp-guard/references/<language>.md` to get the list
of required cheat sheet filenames for the detected language.

### 3. Check What Needs Updating

Read `.claude/skills/owasp-guard/cache/last_updated.json` (create if missing).

**Primary — GitHub API** (requires `api.github.com`):

```bash
curl -s "https://api.github.com/repos/OWASP/CheatSheetSeries/git/trees/master?recursive=1" \
  > /tmp/owasp_tree.json
```

Check truncation:
```bash
jq -e '.truncated == false' /tmp/owasp_tree.json
```

If exit code non-zero (truncated or request failed), skip to timestamp fallback for all sheets.

For each required cheat sheet `<FILENAME>`, get its blob SHA:
```bash
jq -r '.tree[] | select(.path == "cheatsheets/<FILENAME>") | .sha' /tmp/owasp_tree.json
```

Compare result against `commit_sha` in `last_updated.json`:
- Equal → skip
- Different, empty, or stored value is null → fetch

On curl failure, inform user once:
> "GitHub API (`api.github.com`) not reachable. Using timestamp fallback.
> Allow `api.github.com` for accurate staleness checks."

**Fallback — Timestamp**: If `fetched_at` older than 90 days, or file missing on disk → fetch.

### 4. Fetch Updated Sheets

For each sheet that needs updating:

```bash
curl -s "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/cheatsheets/<FILENAME>"
```

Save to `.claude/skills/owasp-guard/cache/<FILENAME>`.

Update `last_updated.json` entry:
```json
{
  "<FILENAME>": {
    "commit_sha": "<SHA or null>",
    "fetched_at": "<ISO 8601>"
  }
}
```

### 5. Report

Print summary:
- Language(s) detected
- Sheets checked vs. sheets updated
- Any sheets that failed to fetch
- Timestamp of update

Example:
> OWASP cache updated for Python. Checked 18 sheets: 3 updated, 15 already current, 0 failed.
