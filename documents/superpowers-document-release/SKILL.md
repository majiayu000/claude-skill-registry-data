---
name: superpowers-document-release
description: >
  Post-ship documentation update. Reads all project docs, cross-references the diff,
  updates README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md, polishes CHANGELOG voice,
  cleans up TODOS, and optionally bumps VERSION. Use after /superpowers-finishing-a-development-branch
  completes or after a significant PR lands.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---

> **DEPRECATED** — use `/document-release` instead. This skill is a legacy alias and will be removed in a future cleanup.
# Document Release — Post-Ship Doc Sync

**Purpose:** After code ships, update all project documentation to reflect what
actually changed. README, ARCHITECTURE, CONTRIBUTING, CLAUDE.md, CHANGELOG, TODOs.

---

## Step 1: Diff Analysis

```bash
git diff --stat $(git merge-base HEAD main 2>/dev/null || git log --oneline -1 | cut -d' ' -f1)^
git diff --name-only
```

Classify changes:
- **New files added** — document these
- **Modified files** — check if they have corresponding docs
- **Deleted files** — remove from docs
- **Config changes** — update relevant docs

---

## Step 2: Per-File Documentation Audit

For each doc file, determine if it needs updates:

### README.md
Check: Does the diff introduce new features, commands, or setup steps?
- New CLI commands → add to "Usage" or "Commands" section
- New prerequisites → add to "Requirements" or "Setup"
- New environment variables → add to "Configuration"
- Breaking changes → add to "Migration" or "Breaking Changes"

### ARCHITECTURE.md
Check: Does the diff change system design, data flow, or component relationships?
- New services/endpoints → add to architecture diagram or component list
- Changed data flows → update ASCII diagrams
- New dependencies → add to dependency section

### CONTRIBUTING.md
Check: Does the diff introduce new build steps, test commands, or conventions?
- New test commands → add to "Testing" section
- New code conventions → add to "Style Guide"
- New tooling → add to "Development Setup"

### CLAUDE.md
Check: Does the diff change project-specific conventions, commands, or structure?
- New file types or directories → document in "Project Structure"
- Changed commands → update "Available Commands"
- New patterns → add to "Conventions"

### Other .md files
Check: Any other documentation files in the repo?
```bash
find . -maxdepth 2 -name "*.md" -not -path "./node_modules/*" -not -path "./.git/*" | head -20
```
Review each for relevance to the diff.

---

## Step 3: Apply Auto-Updates

For each clear factual correction (use Edit tool):
- Adding new commands to README
- Adding new prerequisites to setup docs
- Removing references to deleted files
- Updating file paths that changed
- Adding new environment variables

**Rule:** If the correction is factually clear (new file exists → add to docs), just do it. If it's interpretive (should the tone change? does this feature need a paragraph?), ask.

---

## Step 4: Ask About Risky Changes

Present questionable changes via individual AskUserQuestion calls:

For narrative/rewrite decisions, each gets its own question:
- Should a new section be added to README?
- Should ARCHITECTURE.md be reorganized?
- Does this warrant an entirely new doc?

Format:
1. **Re-ground:** What changed and which doc it touches
2. **Simplify:** What the doc currently says vs what it would say
3. **Recommend:** `RECOMMENDATION: Choose X`
4. **Options:** A) Apply change B) Skip C) Write draft and review

---

## Step 5: CHANGELOG Voice Polish

Check if CHANGELOG.md exists. If yes:

**CRITICAL rule:** Never clobber existing CHANGELOG entries. Only polish the wording of the entry you just added.

Look at the current entry:
- Is the language specific? ("Fixed bug #123" vs "Fixed issues")
- Is it actionable? (does a developer reading this know what changed?)
- Is the tone consistent with the rest of the file?

If the wording needs polish, use Edit tool. If the content is missing detail, add it.

If CHANGELOG.md doesn't exist, ask via AskUserQuestion:
> "No CHANGELOG found. Should I create one?"

---

## Step 6: Cross-Doc Consistency

Check for:
1. **Discoverability:** If a new feature exists in code, can you find it in docs? (grep for it)
2. **Consistency:** Does the same information appear in multiple places? Are they consistent?
3. **VERSION alignment:** If CHANGELOG exists, does it reference the current version?

```bash
grep -r "VERSION" . --include="*.md" --include="*.json" --include="*.toml" --include="*.yml" 2>/dev/null | grep -v node_modules | grep -v ".git/" | head -10
```

---

## Step 7: TODOs.md Cleanup

Check for TODOs addressed by this diff:
```bash
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.py" --include="*.go" --include="*.rb" 2>/dev/null | grep -v node_modules | grep -v ".git/"
```

For each completed TODO found in code:
- Mark it as done in TODOs.md (if the file exists)
- Note: "[RESOLVED by PR #N]"

Check TODOs.md for items that this PR should have addressed:
- Any TODO that matches a changed file? → ask via AskUserQuestion: "Should this TODO be marked complete?"
- Any TODO that conflicts with the new code? → flag

Check TODOs.md for stale items:
- Any TODO that is no longer relevant? → ask via AskUserQuestion: "Should this stale TODO be removed?"

---

## Step 8: VERSION Bump Question

**Never bump VERSION without asking.**

Check current version:
```bash
cat VERSION 2>/dev/null || grep '"version"' package.json 2>/dev/null || grep "version" pyproject.toml 2>/dev/null | head -1
```

Ask via AskUserQuestion:
> "What type of version bump does this PR warrant?
> - A) PATCH (bug fix, no new features) — 1.2.3 → 1.2.4
> - B) MINOR (new feature, backward compatible) — 1.2.3 → 1.3.0
> - C) MAJOR (breaking change) — 1.2.3 → 2.0.0
> - D) No version bump needed"

---

## Step 9: Commit & Push

### Stage by name
```bash
git add README.md
git add ARCHITECTURE.md
git add CHANGELOG.md
git add CLAUDE.md
git add TODOs.md
git status
```

### Commit
```bash
git commit -m "$(cat <<'EOF'
docs: update documentation for recent changes

- Updated [list of changes]
- Bumped VERSION to X.Y.Z [if applicable]
- Cleaned up TODOs [if applicable]

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
EOF
)"
```

### Push
```bash
git push
```

### PR body update (if PR exists)
```bash
gh pr view --json body -q .body 2>/dev/null
```
If a PR exists, check if the doc changes should be mentioned in the body. Edit via `gh pr edit`.

---

## Doc Health Summary

Output a summary:
```
DOCUMENTATION RELEASE SUMMARY
=============================
Site/Repo: {repo}
Branch: {branch}

Files updated: N
  - README.md: {changes}
  - ARCHITECTURE.md: {changes}
  - CHANGELOG.md: {changes}
  - CLAUDE.md: {changes}
  - TODOs.md: {changes}

TODOs resolved: N
TODOs removed: N
Stale TODOs flagged: N

VERSION bumped: {yes/no} → {version}
Commit: {hash}
```

---

## Completion Status

- **DONE** — All docs updated, committed, pushed
- **DONE_WITH_CONCERNS** — Docs updated but some decisions deferred
- **BLOCKED** — Git state prevents safe commits
- **NEEDS_CONTEXT** — No diff available or no docs found
