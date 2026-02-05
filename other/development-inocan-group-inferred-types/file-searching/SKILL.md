---
name: file-searching
description: Regex-based file search across repository contents using gh-grep extension. Use when searching code files for patterns, not issue content.
---

# File Search with Regex

**Capability:** Regex-based file content search across GitHub repositories using gh-grep

**When to use:** Searching repository files (code, docs, configs) - NOT issues

**Installation Required:** `gh extension install k1LoW/gh-grep`

---

## Key Distinction

```
┌─────────────────────────────────────────────────────┐
│                  SEARCH DECISION                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  gh search issues  →  Search ISSUES/PRs            │
│  (searching-issues skill)                           │
│                                                     │
│  gh grep          →  Search FILES (code, docs)     │
│  (THIS skill)                                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Quick Commands

### Basic File Search

```bash
# Search in repository
gh grep "authentication" --owner myorg --repo myrepo

# Search with regex
gh grep "Bug.*critical" --owner myorg --repo myrepo

# Search specific file types
gh grep "API_KEY" --owner myorg --repo myrepo --include "*.env*"

# Case-insensitive search
gh grep -i "password" --owner myorg --repo myrepo
```

### Common Patterns

```bash
# Find function definitions
gh grep "function.*login" --owner myorg --repo myrepo

# Find TODO comments
gh grep "TODO:" --owner myorg --repo myrepo --include "*.js,*.ts"

# Find environment variables
gh grep "process\.env\." --owner myorg --repo myrepo

# Find imports
gh grep "^import.*axios" --owner myorg --repo myrepo
```

---

## Flags & Options

### Output Control

```bash
# Show line numbers
gh grep "error" --owner myorg --repo myrepo --line-number

# Show file names only
gh grep "config" --owner myorg --repo myrepo --files-with-matches

# Limit results
gh grep "api" --owner myorg --repo myrepo --max-count 10
```

### File Filtering

```bash
# Include specific files
gh grep "test" --owner myorg --repo myrepo --include "*.test.js"

# Exclude files
gh grep "console" --owner myorg --repo myrepo --exclude "node_modules/*"

# Multiple file types
gh grep "interface" --owner myorg --repo myrepo --include "*.ts,*.tsx"
```

### Search Scope

```bash
# Search specific branch
gh grep "feature" --owner myorg --repo myrepo --branch develop

# Search multiple repositories
for repo in repo1 repo2 repo3; do
  gh grep "authentication" --owner myorg --repo $repo
done
```

---

## Regex Patterns

### Common Regex

```bash
# Exact word match
gh grep "\bpassword\b" --owner myorg --repo myrepo

# Start of line
gh grep "^export" --owner myorg --repo myrepo

# End of line
gh grep ";$" --owner myorg --repo myrepo --include "*.js"

# Optional characters
gh grep "colou?r" --owner myorg --repo myrepo

# Character classes
gh grep "[0-9]{3}-[0-9]{4}" --owner myorg --repo myrepo
```

### Advanced Patterns

```bash
# Function with any parameters
gh grep "function \w+\(.*\)" --owner myorg --repo myrepo

# Multiword match
gh grep "error.*handler" --owner myorg --repo myrepo

# Negation (find lines WITHOUT pattern)
gh grep "import" --owner myorg --repo myrepo | grep -v "node_modules"
```

---

## Common Workflows

### 1. Security Audit

```bash
# Find hardcoded secrets
gh grep "api_key.*=.*['\"]" --owner myorg --repo myrepo --include "*.js,*.ts,*.py"

# Find password patterns
gh grep -i "password\s*=\s*['\"][^'\"]+['\"]" --owner myorg --repo myrepo

# Find environment variable leaks
gh grep "AWS_SECRET" --owner myorg --repo myrepo
```

### 2. Code Quality Check

```bash
# Find TODO/FIXME comments
gh grep -i "TODO|FIXME" --owner myorg --repo myrepo

# Find console.log statements
gh grep "console\.log" --owner myorg --repo myrepo --include "*.js,*.ts"

# Find deprecated APIs
gh grep "deprecated" --owner myorg --repo myrepo --include "*.md"
```

### 3. Dependency Analysis

```bash
# Find specific package usage
gh grep "import.*lodash" --owner myorg --repo myrepo

# Find external API calls
gh grep "axios\.|fetch\(" --owner myorg --repo myrepo

# Find database queries
gh grep "SELECT.*FROM" --owner myorg --repo myrepo
```

### 4. Documentation Search

````bash
# Find markdown links
gh grep "\[.*\]\(.*\)" --owner myorg --repo myrepo --include "*.md"

# Find code examples in docs
gh grep "^```" --owner myorg --repo myrepo --include "*.md"

# Find heading references
gh grep "^#{1,3} " --owner myorg --repo myrepo --include "*.md"
````

---

## Multi-Repository Search

```bash
#!/bin/bash
# Search across multiple repositories

PATTERN="authentication"
OWNER="myorg"
REPOS=("repo1" "repo2" "repo3")

for repo in "${REPOS[@]}"; do
  echo "=== Searching $repo ==="
  gh grep "$PATTERN" --owner "$OWNER" --repo "$repo" --line-number
  echo ""
done
```

---

## Performance Considerations

**Speed:**

- gh-grep searches via GitHub API (network latency)
- Faster than cloning repos for quick searches
- Slower than local grep for large codebases

**Rate Limits:**

- GitHub API rate limits apply
- Authenticated requests: 5,000/hour
- Consider caching results for repeated searches

**Best Practices:**

1. **Specific patterns** - Narrower regex = fewer results = faster
2. **File filters** - Use `--include` to reduce search scope
3. **Limit results** - Use `--max-count` for quick verification
4. **Batch searches** - Search multiple patterns in one pass

---

## Comparison: gh grep vs gh search issues

| Feature          | gh grep                | gh search issues |
| ---------------- | ---------------------- | ---------------- |
| **Searches**     | Repository files       | Issues/PRs       |
| **Regex**        | ✅ Full regex support  | ❌ No regex      |
| **Wildcards**    | ✅ Yes                 | ❌ No            |
| **Context**      | ✅ Line-based          | ❌ No context    |
| **File types**   | ✅ Filter by extension | N/A              |
| **Installation** | Extension required     | Native           |
| **Use case**     | Code/docs search       | Issue/PR search  |

---

## Limitations

- **No local search** - Always queries GitHub API
- **Branch-specific** - Searches one branch at a time
- **No multiline** - Pattern must match within single line
- **Rate limits** - API quota applies
- **No content display** - Shows matches, not full file content

---

## Tool Selection

- **Search repository FILES** → Use `gh grep` (this skill)
- **Search Issues/PRs** → Use `gh search issues` (searching-issues skill)
- **AI-powered operations** → Use `gh models` (ai-assisted-operations skill)

---

**Installation:** `gh extension install k1LoW/gh-grep`

**Maintenance Status:** Actively maintained (211 stars, updated daily)

**Full Extension Guide:** [GITHUB_CLI_EXTENSIONS.md](/docs/research/GITHUB_CLI_EXTENSIONS.md)
