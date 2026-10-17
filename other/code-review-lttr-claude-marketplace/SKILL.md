---
name: code-review
description: Review code changes from current branch, an Azure DevOps PR, a git ref, or a diff/patch file. Trigger when user says "review this", "code review", "/df:code-review", or provides a PR id/URL, ticket URL, git ref, or diff path. Read-only — never posts comments.
---

# Code Review

Single entry point. Detect input source, produce a diff file, then run the review pipeline.

## Input Detection

Argument is `$ARGUMENTS` (may be empty).

| Form                                                            | Source                                 |
| --------------------------------------------------------------- | -------------------------------------- |
| empty                                                           | current branch vs base (master/main)   |
| `staged`                                                        | `git diff --staged`                    |
| numeric (`12345`)                                               | Azure DevOps PR id                     |
| URL containing `_git/.../pullrequest/<id>`                      | Azure DevOps PR URL                    |
| URL containing `_workitems/edit/<id>` or ticket id mapped to PR | resolve work item → PR via `az boards` |
| path ending `.diff` or `.patch`                                 | local diff file                        |
| anything else                                                   | treat as git ref (branch / sha / tag)  |

Ambiguous → ask user. Do NOT guess.

## Workflow

### 1. Resolve input → diff file path + metadata

#### empty

```bash
base=$(git rev-parse --verify master 2>/dev/null && echo master || echo main)
cur=$(git branch --show-current)
[ "$cur" = "$base" ] && abort "On base branch ($base). Switch to a feature branch."
git diff "$base"...HEAD > "/tmp/review-diff-$(date +%s).diff"
files=$(git diff --name-only "$base"...HEAD)
title="$cur"
```

#### `staged`

```bash
git diff --staged > "/tmp/review-diff-staged-$(date +%s).diff"
files=$(git diff --staged --name-only)
title="staged changes"
```

#### PR id / PR URL

Extract numeric id from URL if needed. Then:

```bash
az repos pr show --id <id> --output json
az repos pr diff --id <id> > "/tmp/review-diff-pr-<id>.diff"
```

Title/description/author/targetRefName from `pr show` output. Skip if status `completed`/`abandoned`, title has `[WIP]`/`[Draft]`, author is bot, or only auto-generated files changed.

#### Work item / ticket URL

```bash
az boards work-item show --id <ticket-id> --expand relations -o json
```

Find related PR via relations of type `ArtifactLink` containing `pullrequest`. If multiple → ask user which. Then proceed as PR id.

#### `.diff` / `.patch` path

Use file as-is. Parse changed files from diff headers (`+++ b/...`).

#### git ref

```bash
git diff "<ref>"...HEAD > "/tmp/review-diff-ref-$(date +%s).diff"
files=$(git diff --name-only "<ref>"...HEAD)
title="HEAD vs <ref>"
```

### 2. Diff size guard

```bash
n=$(wc -l < <(echo "$files"))
```

If `n > 50` → warn user, ask: proceed full / filter to paths / abort.

### 3. Run pipeline

Read `references/pipeline.md` and execute Phases 1–4 with:

- `DIFF_FILE` = path from step 1
- `CHANGED_FILES` = list from step 1
- `TITLE` / `META` = title + (PR description, author, targetRefName) when available

### 4. Save output

If `.aiwork/` protocol present, follow it. Otherwise:

```bash
slug=$(echo "$title" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | cut -c1-40)
mkdir -p ".aiwork/$(date +%F)_${slug}"
```

Save review markdown to `.aiwork/{date}_{slug}/review.md`. If a folder for this branch/ticket already exists, place it there.

## Notes

- Read-only. Never posts PR comments. For comments use `pr-comments` skill.
- Pipeline detail lives in `references/pipeline.md` — load only when running review.
- `az repos pr` requires the `azure-devops` az extension.
