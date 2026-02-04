---
name: code-standards
description: Extract and maintain company-specific coding best practices from PR review comments. Use when the user requests to analyze PR comments from a repository to generate best practices documentation, or when implementing features and needs to reference established coding standards. Triggers include requests like "analyze PR comments and create best practices", "extract coding standards from repo X", or "check if this code follows our best practices".
---

# Code Standards Skill

> **⚠️ DEPRECATED**: This skill has been split into two focused skills for better organization and clarity:
>
> - **`best-practices-extractor`** - Extract best practices from PR comments
> - **`code-compliance`** - Validate code against best practices
>
> **Migration Guide**: See `SKILLS_MIGRATION_GUIDE.md` for details.
>
> **This skill is maintained for backwards compatibility but will be removed in a future release.**

## Overview

This skill helps you build and maintain a living documentation of your team's coding best practices by analyzing PR review comments. It extracts patterns, categorizes feedback, and creates structured markdown files that can serve as reference documentation for future development work.

## Workflow Decision Tree

**When to use this skill:**

1. **Generating Best Practices** (First time or periodic updates)
   - User says: "Analyze PR comments in repo X and create best practices"
   - User says: "Extract coding standards from our repository"
   - User says: "Update our best practices documentation"
   → Follow the [Generation Workflow](#generation-workflow)

2. **Referencing Existing Best Practices** (During development)
   - User says: "Implement feature Y following our best practices"
   - User says: "Check if this code follows our standards"
   - User says: "What are our naming conventions?"
   → Follow the [Reference Workflow](#reference-workflow)

## Generation Workflow

Use this workflow to collect PR comments and generate best practices documentation.

### Step 1: Collect PR Comments

Use the provided extraction script or GitHub CLI commands to fetch review comments efficiently.

**⚡ Recommended: Use the Extraction Script**

The fastest way to collect all PR inline comments is using the provided script:

```bash
# Run from this skill's directory
bash scripts/extract_pr_comments.sh REPO_NAME

# Examples:
bash scripts/extract_pr_comments.sh backend
bash scripts/extract_pr_comments.sh vscode-extension
bash scripts/extract_pr_comments.sh ts-agent
```

**What the script does:**
- Fetches all PRs from `earlyai/{REPO_NAME}`
- Extracts inline code review comments from each PR
- Outputs NDJSON format with all comment metadata
- Shows progress as it processes PRs
- Saves to `{REPO_NAME}_inline_comments.ndjson`

**Output format (one JSON object per line):**
```json
{
  "repo": "backend",
  "owner": "earlyai",
  "pr_number": 1207,
  "comment_id": 2645175276,
  "review_id": 3610363001,
  "in_reply_to_id": null,
  "file": "src/components/Dashboard.tsx",
  "line": 30,
  "original_line": 30,
  "side": "RIGHT",
  "diff_hunk": "@@ -42,7 +42,7 @@ ...",
  "author": "reviewer",
  "body": "Consider using a more descriptive variable name here",
  "created_at": "2025-12-24T08:55:51Z",
  "updated_at": "2025-12-24T08:56:28Z",
  "url": "https://github.com/earlyai/backend/pull/1207#discussion_r2645175276"
}
```

**Prerequisites:**
- GitHub CLI (`gh`) must be installed and authenticated
- `jq` must be installed (Windows: `C:\Users\ItamarZand\bin\jq.exe`)

---

**⚡⚡ NEW: Incremental Updates (Recommended for existing repositories)**

If you've already extracted PR comments before, use the incremental update script to fetch only NEW PRs since your last update:

```bash
# Run incremental update
bash scripts/incremental_update.sh OWNER REPO_NAME

# Examples:
bash scripts/incremental_update.sh earlyai backend
bash scripts/incremental_update.sh myorg frontend
```

**What the incremental update does:**
- Tracks the last update timestamp in `.state.json`
- Fetches only PRs merged since last update (uses GitHub search `merged:>=DATE`)
- Much faster than full extraction (processes only 3-5 new PRs instead of 100+)
- Saves to `{REPO}_inline_comments_incremental.ndjson`
- Updates state file with statistics

**First run behavior:**
- If no previous state exists, runs full extraction automatically
- Saves state for future incremental runs
- Next runs will be incremental

**Output example:**
```
╔════════════════════════════════════════╗
║  Incremental PR Comment Update         ║
╚════════════════════════════════════════╝

Repository: earlyai/backend

📅 Last update: 2025-12-20T10:00:00Z
   Fetching only NEW PRs merged after this date...

📊 Found 3 new merged PRs

🔍 Extracting comments from new PRs...

  ✓ PR #1234: 5 comments
  ✓ PR #1235: 2 comments

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Incremental Update Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📈 Statistics:
   New PRs processed: 3
   Comments extracted: 7
   Output file: backend_inline_comments_incremental.ndjson

💾 State updated. Next run will start from: 2025-12-28T10:30:00Z
```

**When to use incremental vs. full:**
- **Incremental:** Regular updates (weekly/monthly), existing repositories
- **Full:** First time setup, major retrospectives, or reset needed

---

**Step 1b: Sort Comments by File Tree (Recommended)**

After extracting comments, organize them into a folder structure matching the repo:

```bash
# Run from the repo directory
bash scripts/sort_comments_by_filetree.sh COMMENTS_FILE [REPO_PATH]

# Examples:
bash scripts/sort_comments_by_filetree.sh backend_inline_comments.ndjson /path/to/backend
bash scripts/sort_comments_by_filetree.sh vscode-extension_inline_comments.ndjson .
```

**What the script does:**
- Creates `pr-review-comments/` folder in the repo
- Groups comments by file path into matching folder structure
- Creates `comments.json` in each directory with only its comments
- Generates `summary.json` with statistics

**Output structure:**
```
repo/pr-review-comments/
├── summary.json                              # Overall statistics
├── prisma/
│   └── comments.json                         # Comments for prisma/ files
├── src/
│   ├── core/
│   │   ├── config/
│   │   │   └── comments.json                 # Comments for src/core/config/
│   │   └── utils/
│   │       └── comments.json
│   ├── telemetry/
│   │   └── comments.json                     # 23 comments for telemetry files
│   └── ...
```

**Each `comments.json` contains:**
```json
{
  "directory": "src/telemetry",
  "generated_at": "2025-12-28T...",
  "comment_count": 23,
  "files": ["src/telemetry/ai-cost-telemetry.service.ts"],
  "comments": [
    {
      "file": "src/telemetry/ai-cost-telemetry.service.ts",
      "filename": "ai-cost-telemetry.service.ts",
      "comments": [
        {
          "pr_number": 1104,
          "author": "reviewer",
          "body": "Comment text...",
          "line": 45,
          "created_at": "2025-11-10T18:13:08Z",
          "url": "https://github.com/..."
        }
      ]
    }
  ]
}
```

**summary.json contains:**
- Total comments and files
- Comments grouped by directory
- Top commented files
- Comments by author

This is useful for:
- Identifying hotspots (files with most comments)
- Finding patterns by module/directory
- Generating per-directory best practices
- Keeping review feedback alongside the code

---

**Alternative: Manual Collection Methods**

If you need more control or want to customize the collection:

**Method A: Filter PRs with comments first**

```bash
# 1. Get all PRs and save to file
gh pr list \
  --repo OWNER/REPO \
  --state merged \
  --limit 100 \
  --json number,title,author,url,createdAt \
  > prs_list.json

# 2. For each PR, check if it has comments (quick check)
# Only save those that have actual comments
cat prs_list.json | jq -r '.[].number' | while read pr_num; do
  echo "Checking PR #$pr_num..."
  comments=$(gh api repos/OWNER/REPO/pulls/$pr_num/comments)

  # Only save if not empty
  if [ "$comments" != "[]" ]; then
    echo "  ✓ Found comments in PR #$pr_num"
    echo "$comments" > "comments_${pr_num}.json"
  fi
done

# 3. Combine all comments into structured format
```

**Method B: Use GraphQL for smart filtering**

```bash
# Get only PRs that have reviews or comments
gh api graphql -f query='
{
  repository(owner: "OWNER", name: "REPO") {
    pullRequests(first: 100, states: MERGED, orderBy: {field: UPDATED_AT, direction: DESC}) {
      nodes {
        number
        title
        url
        author { login }
        reviews(first: 1) { totalCount }
        reviewThreads(first: 1) { totalCount }
      }
    }
  }
}' | jq '.data.repository.pullRequests.nodes[] | select(.reviews.totalCount > 0 or .reviewThreads.totalCount > 0)'
```

**Method C: Try reviews endpoint (alternative)**

```bash
# Sometimes feedback is in PR reviews, not inline comments
gh api repos/OWNER/REPO/pulls/PR_NUMBER/reviews

# Reviews have a body with general feedback
# Plus they can reference specific commits/files
```

**Windows-specific notes:**
- Git Bash might rewrite paths with leading slashes
- Solution: Use `repos/...` instead of `/repos/...`
- Or use PowerShell: `gh api "repos/owner/repo/pulls/123/comments"`

**Common filters:**

- **By author**: Add `--author username` to PR list command
- **By state**: `--state open|closed|merged|all`
- **Limit**: `--limit N` to control how many PRs to fetch
- **Date range**: `--search "merged:>=2024-01-01"`

**What Claude Code should do:**

1. **Phase 1: Discovery**
   - Get list of all relevant PRs
   - Quick check which ones have comments/reviews
   - Filter to only PRs with actual feedback

2. **Phase 2: Collection**
   - Fetch comments only from PRs that have them
   - Try both `/comments` and `/reviews` endpoints
   - Collect all data efficiently

3. **Phase 3: Structuring**
   - Combine all data into structured JSON:
   ```json
   {
     "repo": "owner/repo",
     "collected_at": "2024-12-24T10:00:00Z",
     "total_prs_checked": 100,
     "prs_with_comments": 15,
     "pr_comments": [
       {
         "pr_number": 123,
         "pr_title": "Add feature X",
         "pr_author": "username",
         "pr_url": "https://github.com/owner/repo/pull/123",
         "comments": [
           {
             "body": "Consider using a more descriptive variable name here",
             "path": "src/components/Dashboard.tsx",
             "line": 45,
             "author": "reviewer",
             "diff_hunk": "@@ -42,7 +42,7 @@ ..."
           }
         ]
       }
     ]
   }
   ```

4. **Save to file**: `pr_comments.json`

**Example user requests:**
- "Collect PR comments from earlyai/backend efficiently"
- "Find all PRs with review comments in the last 50 merged PRs"
- "Get comments only from PRs that have actual feedback"
- "Fetch PR reviews (not just inline comments)"

**Performance tips:**
- Most PRs have 0 inline comments - filter first!
- Use GraphQL to check comment counts before fetching
- Try `/reviews` endpoint if `/comments` returns empty
- Batch API calls to respect rate limits

**Prerequisites:**
- GitHub CLI (`gh`) must be installed
- User must be authenticated (`gh auth status` shows logged in)
- User must have access to the repository

**Note:** Claude Code runs in the user's terminal, so if `gh` is already configured, it will work automatically.

### Step 2: Analyze and Categorize

After collecting PR comments, analyze them to extract and categorize best practices.

**Analysis Process:**

1. **Load the comments file**
   - Read the `{REPO}_inline_comments.ndjson` file created in Step 1
   - Each line is a JSON object with comment metadata
   - Extract all comment bodies, file paths, and diff hunks

2. **Identify patterns and categorize**
   - Look for recurring themes across comments
   - Group similar feedback together
   - Create logical categories based on the patterns found

3. **Extract actionable guidelines**
   - For each category, create clear, actionable best practices
   - Include rationale (why it matters)
   - Add code examples where comments provided them
   - Reference specific PRs where the pattern appeared

**Common Categories to Look For:**

Depending on the codebase, typical categories include:
- **Code Organization & Architecture** - Component structure, module boundaries, file organization
- **Naming Conventions** - Variable, function, component, and file naming patterns
- **Error Handling** - Try-catch patterns, error messages, logging strategies
- **Testing & Test Coverage** - Unit test patterns, test organization, edge cases
- **Performance & Optimization** - Unnecessary re-renders, query optimization, caching
- **Security** - Input validation, auth patterns, secure data handling
- **Code Style & Formatting** - Indentation, line length, import organization
- **Documentation** - Comments, function docs, README quality
- **Type Safety** - TypeScript usage, type definitions, avoiding `any`
- **React/Component Patterns** - Component composition, hooks, state management (if applicable)
- **API Design** - Endpoint design, request/response structures
- **Database & Queries** - Query optimization, schema design

**For each best practice item, include:**

```markdown
## [Number]. [Short Descriptive Title]

**Guideline:** [Clear, actionable statement of what to do]

**Why:** [Brief explanation of why this matters - impact on code quality, maintainability, performance, etc.]

**Example:**
```[language]
// Good example or pattern from comments
```

**References:** [List of PR numbers where this came up, e.g., #123, #456]

---
```

**Creating Best Practices Files:**

1. **Create directory structure:**
   ```
   best-practices/
   ├── README.md                    # Index file
   ├── code-organization.md
   ├── naming-conventions.md
   ├── error-handling.md
   └── ...
   ```

2. **One file per category** - Name files using lowercase-with-hyphens

3. **Consistent format** - Follow the template above for each practice

4. **Generate index** - Create README.md listing all categories with links

**Example user requests:**
- "Analyze the collected comments and create best practices"
- "Read backend_inline_comments.ndjson and generate coding standards"
- "Extract best practices from the PR comments we collected"
- "Create best-practices/ folder from the comments data"

### Step 3: Review and Refine

After generation:

1. **Review the generated files** in `best-practices/` directory in the repo
2. **Check the categorization** - verify categories make sense for your project
3. **Validate guidelines** - ensure extracted practices are accurate
4. **Add manual refinements** - edit files to add context or examples
5. **Commit to repository** - version control the best practices

**Skill folder structure:**
```
.claude/skills/code-standards/   # This skill folder
├── SKILL.md                     # This file
├── scripts/
│   ├── extract_pr_comments.sh       # PR comments extraction script
│   └── sort_comments_by_filetree.sh # Sort comments by file tree
└── references/
    └── default-categories.md    # Category examples
```

**Generated output in repo:**
```
your-repo/
├── pr-review-comments/          # Generated by sort script
│   ├── summary.json             # Overall statistics
│   ├── src/
│   │   ├── core/config/
│   │   │   └── comments.json    # Comments for this directory
│   │   └── telemetry/
│   │       └── comments.json
│   └── ...
└── best-practices/              # Generated from analysis
    ├── README.md                # Index of all categories
    ├── code-organization.md     # Architecture patterns
    ├── naming-conventions.md    # Naming standards
    ├── error-handling.md        # Error handling practices
    ├── testing.md               # Testing patterns
    └── ...                      # Additional categories
```

## Reference Workflow

Use this workflow when implementing features or reviewing code.

### During Development

**Reference best practices files** when working on code:

```bash
# Read specific category
view best-practices/naming-conventions.md

# Reference multiple categories
view best-practices/react-patterns.md
view best-practices/testing.md
```

**Example user requests:**
- "Implement the user dashboard following our best practices"
- "What are our error handling standards?"
- "Show me our React component patterns"
- "Check if this code follows our naming conventions"

### Code Review Mode

When reviewing or validating code:

1. **Load relevant best practices** based on the code domain
2. **Compare against guidelines** in the best practices files
3. **Provide specific feedback** referencing the documented standards
4. **Suggest improvements** aligned with team practices

**Example user requests:**
- "Review this component against our React patterns"
- "Does this error handling follow our standards?"
- "Validate this API implementation against our guidelines"

## Category Reference

For details on common categories that may emerge from PR comments, see:
- [references/default-categories.md](references/default-categories.md)

This reference provides examples of typical categories but the actual categories should be determined by your repository's specific comments.

## Best Practices for Using This Skill

### When to Regenerate Best Practices

- **Initial Setup**: First time creating standards for a project
- **Quarterly Reviews**: Regular updates to capture evolving standards
- **After Major Changes**: When team or tech stack changes significantly
- **New Team Members**: To onboard engineers with current practices

### Collecting Comments Strategically

1. **Start with your own PRs** (--author flag) to focus on feedback you've received
2. **Focus on merged PRs** (--state merged) for accepted patterns
3. **Use reasonable limits** (50-100 PRs) to balance coverage and noise
4. **Expand gradually** to include team-wide PRs for comprehensive standards

### Maintaining Best Practices

- **Version control**: Commit best-practices/ directory to your repo
- **Regular updates**: Run collection + analysis quarterly or semi-annually
- **Team review**: Have team validate generated guidelines
- **Living documentation**: Encourage team to propose updates via PRs
- **Reference in PRs**: Link to specific guidelines in code review comments

## Common Use Cases

### Use Case 1: Onboarding New Engineers

**Scenario**: New team member joining the project

**Workflow**:
1. Generate current best practices from recent PRs
2. Share `best-practices/` directory as onboarding material
3. Reference specific files during code reviews
4. Use as teaching tool for team conventions

### Use Case 2: Establishing Coding Standards

**Scenario**: Team wants to formalize informal practices

**Workflow**:
1. Collect comments from past 6 months of PRs
2. Generate best practices across all team members
3. Review with team and refine
4. Adopt as official coding standards

### Use Case 3: Code Review Consistency

**Scenario**: Ensuring consistent feedback across reviewers

**Workflow**:
1. Generate best practices from all reviewers' comments
2. Use as reference during code reviews
3. Point to specific guidelines when giving feedback
4. Reduce subjective "I prefer..." comments

### Use Case 4: Migration Guidance

**Scenario**: Migrating to new framework or patterns

**Workflow**:
1. Initially focus on migration-related PR comments
2. Generate best practices for new patterns
3. Update as migration progresses
4. Serve as migration playbook for team

## GitHub CLI Commands Reference

This skill uses GitHub CLI (`gh`) commands directly instead of scripts for maximum flexibility.

### Key Commands

**List Pull Requests:**
```bash
# Basic listing
gh pr list --repo owner/repo

# With filters
gh pr list --repo owner/repo \
  --state merged \
  --limit 50 \
  --author username \
  --json number,title,author,createdAt,url

# Search by date
gh pr list --repo owner/repo \
  --search "merged:>=2024-01-01" \
  --json number,title,author,createdAt,url
```

**Get PR Review Comments:**
```bash
# Get comments for specific PR
gh api /repos/owner/repo/pulls/123/comments

# Get comments with pagination
gh api /repos/owner/repo/pulls/123/comments --paginate

# Format output
gh api /repos/owner/repo/pulls/123/comments | jq '.'
```

**Useful `jq` Operations:**

```bash
# Extract PR numbers from list
gh pr list --repo owner/repo --json number | jq -r '.[].number'

# Count total comments
gh api /repos/owner/repo/pulls/123/comments | jq '. | length'

# Filter comments by author
gh api /repos/owner/repo/pulls/123/comments | jq '[.[] | select(.user.login=="username")]'

# Extract just comment bodies
gh api /repos/owner/repo/pulls/123/comments | jq -r '.[].body'
```

**Complete Collection Pattern:**

```bash
# 1. Get PR list
gh pr list --repo owner/repo --state merged --limit 50 --json number > pr_numbers.json

# 2. Collect comments for all PRs
echo '{"pr_comments": []}' > pr_comments.json
for pr in $(jq -r '.[].number' pr_numbers.json); do
  echo "Fetching PR #$pr..."
  gh api "/repos/owner/repo/pulls/$pr/comments" >> comments_raw.json
done

# 3. Process and combine into final format
# (Claude Code will handle the JSON processing and formatting)
```

**Authentication Check:**
```bash
# Verify gh is authenticated
gh auth status

# If needed, login
gh auth login
```

## Troubleshooting

### GitHub CLI Not Found
If `gh` command is not available:
```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Windows
winget install GitHub.cli
```

### GitHub CLI Not Authenticated
Check authentication status:
```bash
gh auth status
```

If not authenticated:
```bash
gh auth login
```

### No or Few Inline Comments Found

This is common! Many teams don't use inline code review comments extensively. Try these alternatives:

**1. Check PR Reviews (general feedback):**
```bash
# Reviews often contain valuable feedback in the body
gh api repos/owner/repo/pulls/PR_NUMBER/reviews

# Reviews have:
# - state: APPROVED, CHANGES_REQUESTED, COMMENTED
# - body: General feedback text
# - Aggregate feedback across files
```

**2. Check issue/PR comments:**
```bash
# General discussion comments on the PR
gh api repos/owner/repo/issues/PR_NUMBER/comments
```

**3. Analyze commit messages:**
```bash
# Sometimes feedback is incorporated in commit messages
gh api repos/owner/repo/pulls/PR_NUMBER/commits
```

**4. Focus on PRs that were revised:**
```bash
# PRs with multiple commits often had feedback incorporated
gh pr list --repo owner/repo --json number,commits | jq '.[] | select(.commits | length > 3)'
```

**5. Look at closed/rejected PRs:**
```bash
# Sometimes valuable patterns emerge from rejected approaches
gh pr list --repo owner/repo --state closed --search "is:unmerged"
```

**Alternative approach - Direct codebase analysis:**

If there aren't many PR comments, analyze the codebase directly:
- Look for common patterns in the code
- Check ESLint/Prettier configs
- Read existing documentation
- Analyze naming conventions from actual code
- Extract patterns from test files

### Rate Limiting
If you hit GitHub API rate limits:
- Wait for rate limit to reset (check with `gh api rate_limit`)
- Reduce the number of PRs being fetched
- Space out requests over time

### jq Not Available
If `jq` is not installed (for JSON processing):
```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt install jq

# Windows
winget install jqlang.jq
```

### Category Duplication
If generated categories overlap:
- Edit best-practices files manually to merge
- Consider which practices belong together
- Refine category definitions in future iterations

### Analysis Quality
If the extracted best practices don't capture the essence:
- Review the JSON file to ensure comments were collected correctly
- Provide more specific guidance about what categories to look for
- Focus on a smaller set of high-quality PRs rather than many low-quality ones
- Filter by specific file types or areas of the codebase
