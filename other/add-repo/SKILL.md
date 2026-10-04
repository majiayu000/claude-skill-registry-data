---
name: add-repo
description: Register a new sub-repo in the knowledge base.
---

# add-repo

Adds a new sub-repo to the harness: updates **local** `repos/repos.json` (gitignored), clones, generates knowledge YAML.

If `repos/repos.json` is missing, copy `repos/repos.json.example` to `repos/repos.json` and edit entries there. Do not commit `repos/repos.json`.

## When to Use

- Bringing a new repository under Agent Forge management

## Steps

### 1. Resolve location

Accept HTTPS, SSH URL, or local path. Extract repo name from URL (last segment without .git).

### 2. Check for duplicates

```bash
cat repos/repos.json | jq '.repos[] | select(.name == "<repo-name>")'
```

If already exists: report and stop.

### 3. Update repos.json

Add: `{"name":"<name>","url":"<url>","defaultBranch":"main"}`

### 4. Clone

```bash
bun run repo init --repo <repo-name> --human
```

### 5. Generate knowledge

```bash
/sync-knowledge <repo-name>
```
