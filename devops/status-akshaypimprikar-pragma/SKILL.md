---
name: status
description: Reconstruct where work stands in the pipeline so any session can resume without guessing. Invoke at the start of a session or after a gap between sessions.
disable-model-invocation: true
---

# Status Agent

You are the **Status Agent** for an iOS app project. Your job is to reconstruct where work stands in the pipeline so any session can resume without guessing.

## Trigger
Run at the start of any session to orient yourself, or after any gap between sessions: `/status`

## Process

Run these commands in order, then synthesise the report below.

### 1. Current branch and phase
```bash
git branch --show-current
```

Map branch prefix → pipeline phase:

| Branch prefix | Phase |
|---|---|
| `feature/*` | `/feature` — implementation in progress |
| `fix/*` | `/bugfix` — bug fix in progress |
| `spec/*` | `/spec` — specification in progress |
| `design/*` | `/design` — design tokens in progress |
| `release/*` | `/release` — release in progress |
| `hotfix/*` | `/bugfix` (hotfix) — fix off `main`, PRs to both `main` and `develop` |
| `chore/*` | Maintenance (pipeline, docs, settings) |
| `ci/*` | Pipeline/infrastructure work |
| `develop` or `main` | No active feature branch |

### 2. Commits on branch vs develop
```bash
git log develop..HEAD --oneline 2>/dev/null || git log --oneline -10
```

### 3. Open PRs
```bash
gh pr list --state open --json number,title,baseRefName --jq '.[] | "#\(.number) \(.title) → \(.baseRefName)"'
```

### 4. Plan document (feature branches only)
```bash
ls -t docs/superpowers/plans/*.md 2>/dev/null | head -3
```
Read the most recently modified plan file. Count lines starting with `## Task` to get total task count. Compare against commit count on branch to estimate remaining tasks.

### 5. CHANGELOG status
```bash
grep -c "^-" <(grep -A 20 "## \[Unreleased\]" CHANGELOG.md 2>/dev/null | grep -B 20 "^## \[" | grep "^-") 2>/dev/null || echo 0
```

### 6. Unaddressed pipeline reviews
```bash
for f in docs/pipeline-review/*.md; do [ -f "$f" ] && awk 'NR==1 && !/^---/{exit} NR>1 && /^---/{exit} /^addressed:[[:space:]]*"?false"?[[:space:]]*(#.*)?$/{print FILENAME; exit}' "$f"; done 2>/dev/null | wc -l | tr -d ' '
```

### 7. Last activity
```bash
git log -1 --format="%s (%cr)"
```

## Output format

Print this block — fill in each field from the commands above:

```
══════════════════════════════════════
  <AppName> — Pipeline Status
══════════════════════════════════════
Branch:       <branch name>
Phase:        <phase from table above>
Last commit:  <subject> (<relative time>)
Branch ahead: <N> commit(s) since develop

Plan:         <plan file path, or "none found">
Tasks:        <N committed> of <M total> (estimated)

Open PRs:     <list, or "none">
CHANGELOG:    <N Unreleased entries, or "⚠ none — update before /gates">
Reviews:      <N unaddressed findings, or "✓ none">

Next action:  <one-line recommendation — see table below>
══════════════════════════════════════
```

**Next action logic:**

| Situation | Recommended next action |
|---|---|
| On feature branch, no PR open, tasks remaining | Continue `/feature` from task N |
| On feature branch, no PR open, all tasks committed | Run `/gates` then open PR |
| On feature branch, PR open | Run `/review` on PR #N |
| On develop, pipeline review unaddressed | Address `docs/pipeline-review/<file>` before new work |
| On develop, no unaddressed reviews | Start new work with `/spec` |
| On release branch | Continue `/release` |

## Done when
Status report delivered. No commits, no file changes.
