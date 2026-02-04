---
name: best-practices-extractor
description: Extract and generate coding best practices from PR review comments. Use when the user asks to "extract best practices", "analyze PR comments", "generate coding standards", "create best practices from PRs", or "update coding guidelines from reviews".
version: 1.0.0
---

# Best Practices Extractor

Extract coding best practices from PR review comments and codebase analysis to generate `.claude/best-practices/` documentation.

## When to Use

- Initial setup of coding standards for a project
- Regular updates to capture new team feedback
- Analyzing PR comments to document patterns
- Generating best practices from code review history

## Extraction Methods

All outputs are saved to `.claude/pr-review-comments/`.

### Method 1: Incremental Update (Recommended)

For regular updates - fast and tracks state:

```bash
cd plugin/skills/best-practices-extractor
bash scripts/incremental_update.sh OWNER REPO_NAME
```

First run does full extraction; subsequent runs fetch only new PRs.

**Output**: `.claude/pr-review-comments/{repo}_inline_comments.ndjson`

### Method 2: Full Extraction

For first-time setup or comprehensive analysis:

```bash
bash scripts/extract_pr_comments.sh REPO_NAME
```

**Output**: `.claude/pr-review-comments/{repo}_inline_comments.ndjson`

### Method 3: Sort by File Tree

Organize extracted comments by directory structure:

```bash
bash scripts/sort_comments_by_filetree.sh .claude/pr-review-comments/{repo}_inline_comments.ndjson
```

**Output**: `.claude/pr-review-comments/sorted/`

## Generating Best Practices

After extracting comments:

1. **Identify patterns** - Look for recurring feedback themes
2. **Categorize** - Group by type (naming, error-handling, type-safety, etc.)
3. **Create documentation** - Generate `.claude/best-practices/` files

### Output Structure

```
.claude/best-practices/
├── README.md              # Index
├── naming-conventions.md
├── error-handling.md
├── type-safety.md
├── testing.md
└── ...
```

### Guideline Format

Each guideline should include:

```markdown
## [Number]. [Title]

**Guideline:** [Clear statement]

**Why:** [Impact explanation]

**Example:**
```typescript
// Good
{example}

// Bad
{counter_example}
```

**Source:** PR #{number}
```

## Prerequisites

- **GitHub CLI (`gh`)**: Authenticated - check with `gh auth status`
- **jq**: JSON processor - check with `jq --version`

## Integration

This skill **generates** best practices. The `code-reviewer` agent and `/4_review` command **validate** against them.

Workflow:
1. Extract PR comments (this skill)
2. Analyze and generate `.claude/best-practices/`
3. Reviews automatically validate against best practices

## Additional Resources

- **`references/default-categories.md`** - Example category definitions
- **`references/scripts-guide.md`** - Detailed script documentation
