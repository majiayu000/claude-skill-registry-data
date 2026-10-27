---
description: Generate a comprehensive repo recap (PRs, issues, releases) ready to share with the team. Pass "fr" for French output (default is English).
allowed-tools: Bash Read Grep
disable-model-invocation: true
---

# Repo Recap

Generate a structured recap of the repository state: open PRs, open issues, recent releases, and executive summary. Output is formatted as Markdown with clickable GitHub links, ready to share.

## Language

- Check the argument passed to this skill
- If `fr` or `french` → produce the recap in French
- If `en`, `english`, or no argument → produce the recap in English (default)

## Preconditions

Before gathering data, verify:

```bash
git rev-parse --is-inside-work-tree
gh auth status
```

If either fails, stop and tell the user what's missing.

## Steps

### 1. Gather Data

Run these commands in parallel via `gh` CLI:

```bash
# Repo identity (for links)
gh repo view --json nameWithOwner -q .nameWithOwner

# Open PRs with metadata
gh pr list --state open --limit 50 --json number,title,author,createdAt,changedFiles,additions,deletions,reviewDecision,isDraft

# Open issues with metadata
gh issue list --state open --limit 50 --json number,title,author,createdAt,labels,assignees

# Recent releases (for version history)
gh release list --limit 5

# Recently merged PRs (for contributor activity)
gh pr list --state merged --limit 10 --json number,title,author,mergedAt
```

Note: `author` in JSON results is an object `{login: "..."}` — always extract `.author.login` when processing.

### 2. Determine Maintainers

To distinguish "our PRs" from external contributions:

```bash
gh api repos/{owner}/{repo}/collaborators --jq '.[].login'
```

If this fails (permissions), fallback: authors with write/admin access are those who merged PRs recently. When in doubt, ask the user.

### 3. Analyze and Categorize

#### PRs — Categorize into 3 groups:

**Our PRs** (author is a repo collaborator):

- List with PR number (linked), title, size (+additions, files count), status

**External — Reviewable** (manageable size, no major blockers):

- Additions ≤ 1000 AND files ≤ 10
- No merge conflicts, CI not failing
- Include: PR link, author, title, size, review status, recommended action

**External — Problematic** (any of: too large, CI failing, overlapping, merge conflict):

- Additions > 1000 OR files > 10
- OR CI failing (reviewDecision = "CHANGES_REQUESTED" or checks failing)
- OR touches same files as another open PR (= overlap)
- Include: PR link, author, title, size, specific problem, action taken/needed

**Size labels** (use in "Size" column for quick visual triage):

| Label | Additions |
| ----- | --------- |
| XS    | < 50      |
| S     | 50-200    |
| M     | 200-500   |
| L     | 500-1000  |
| XL    | > 1000    |

Format: `+{additions}, {files} files ({label})` — e.g., `+245, 2 files (S)`

#### Detect overlaps:

Two PRs overlap if they modify the same files. Use `changedFiles` from the JSON data. If >50% file overlap between 2 PRs, flag both as overlapping and cross-reference them.

#### Flag clusters:

If one author has 3+ open PRs, note it as a "cluster" with suggested review order (smallest first, or by dependency chain).

#### Issues — Categorize by status:

- **In progress**: has an associated open PR (match by PR body containing `fixes #N`, `closes #N`, or same topic)
- **Quick fix**: small scope, actionable (bug reports, small enhancements)
- **Feature request**: larger scope, needs design discussion
- **Covered by PR**: an existing PR addresses this issue (link it)

### 4. Derive Recent Releases

From `gh release list` output, extract version, date, and name. List the 5 most recent.

If no releases found, check merged PRs for release-please pattern (title matching `chore(*): release *`) as fallback.

### 5. Executive Summary

Produce 5-6 bullet points:

- Total open PRs and issues count
- Active contributors (who has the most PRs/issues)
- Main risks (oversized PRs, CI failures, merge conflicts)
- Quick wins (small PRs ready to merge — XS/S size, no blockers)
- Bug fixes needed (regressions, critical bugs)
- Our own PRs status

### 6. Format Output

Structure the full recap as Markdown with:

- `# {Repo Name} — Recap {date}` as title (EN) or `# {Repo Name} — Récap au {date}` (FR)
- Sections separated by `---`
- All PR/issue numbers as clickable links: `[#123](https://github.com/{owner}/{repo}/pull/123)` for PRs, `.../issues/123` for issues
- Tables with Markdown pipe syntax for all listings
- Bold for emphasis on actions and risks
- Cross-references between related PRs and issues (e.g., "Covered by [#131](link)")

**Empty data handling**:

- 0 open PRs → display "No open PRs." (EN) or "Aucune PR ouverte." (FR)
- 0 open issues → display "No open issues." (EN) or "Aucune issue ouverte." (FR)
- 0 releases → display "No recent releases." (EN) or "Aucune release récente." (FR)

### 7. Copy to Clipboard

After displaying the recap, automatically copy it to clipboard:

```bash
clip() {
  if command -v pbcopy &>/dev/null; then pbcopy
  elif command -v xclip &>/dev/null; then xclip -selection clipboard
  elif command -v wl-copy &>/dev/null; then wl-copy
  else cat
  fi
}
```

Confirm with: "Copied to clipboard." (EN) or "Copié dans le presse-papier." (FR)

## Output Template (EN)

```markdown
# {Repo Name} — Recap {date}

## Recent Releases

| Version | Date | Highlights |
| ------- | ---- | ---------- |

---

## Open PRs ({count} total)

### Our PRs

| PR  | Title | Size | Status |
| --- | ----- | ---- | ------ |

### External — Reviewable

| PR  | Author | Title | Size | Status | Action |
| --- | ------ | ----- | ---- | ------ | ------ |

### External — Problematic

| PR  | Author | Title | Size | Problem | Action |
| --- | ------ | ----- | ---- | ------- | ------ |

---

## Open Issues ({count} total)

| #   | Author | Topic | Priority |
| --- | ------ | ----- | -------- |

---

## Executive Summary

- **Point 1**: ...
- **Point 2**: ...
```

## Notes

- Always use `gh` CLI (not GitHub API directly, except for collaborators list)
- Derive repo owner/name from `gh repo view`, don't hardcode
- Keep tables compact — truncate long titles if needed (max ~60 chars)
- Cross-reference overlapping PRs/issues whenever possible
- `author` in gh JSON is an object — always use `.author.login`
