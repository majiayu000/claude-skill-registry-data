---
name: bitbucket
description: "REQUIRED helper functions (never raw curl), workspace/repo_slug patterns, suggestion block syntax for code review"
connection_type: bitbucket
preload: false
---

# Bitbucket CLI Skill

Execute Bitbucket helper functions with proper authentication via OAuth token.

**You must source the helpers before use:**

```bash
source ./_skills/connections/bitbucket/bitbucket/scripts/bitbucket_helpers.sh
```

## CLI Tips

### NEVER USE RAW CURL OR DIRECT API CALLS

**DO NOT write raw curl/HTTP requests like:**

```bash
# ❌ WRONG - Never do this
curl -s -H "Authorization: Bearer ${BITBUCKET_TOKEN}" "https://api.bitbucket.org/2.0/..."
```

**ALWAYS use the provided helper functions:**

```bash
# ✅ CORRECT - Use helper functions
bitbucket_test                              # Test connection
bitbucket_user                              # Get current user
bitbucket_pr myworkspace myrepo 123         # Get PR details
```

The helper functions handle authentication, error handling, retries, and output formatting automatically.

### CRITICAL: Workspace and Repo Slug Parameters

**ALL commands require explicit `workspace` and `repo_slug` as parameters.**

```bash
bitbucket_pr myworkspace myrepo 123        # Get PR details
bitbucket_pr_diff myworkspace myrepo 123   # Get PR diff
```

### Code Review Helper Functions (Bitbucket)

**Inline comment with suggestion block:**

````bash
bitbucket_create_pr_comment myworkspace myrepo 123 "file.py" 45 'Comment text

```suggestion
fixed code
```
'
````

- Use single quotes to preserve backticks literally - NO escaping needed

**Discussion comment (not line-specific):**

```bash
bitbucket_create_pr_discussion myworkspace myrepo 123 'Overall review summary'
```

### Suggestion Block Syntax (CRITICAL)

**✅ CORRECT - Single quotes preserve backticks:**

````bash
bitbucket_create_pr_comment myworkspace myrepo 123 "src/app.py" 45 '🔴 CRITICAL: Issue

```suggestion
if not input:
    raise ValueError("Required")
```
'
````

**❌ WRONG - Escaped backticks break rendering:**

```bash
bitbucket_create_pr_comment myworkspace myrepo 123 "src/app.py" 45 "\`\`\`suggestion
code
\`\`\`"
```

**Key rules:**

- Use single quotes to wrap comment body containing markdown
- Backticks inside single quotes are literal - write them normally
- NEVER escape backticks with backslashes (\\`) - this breaks Bitbucket's markdown parser
- Triple backticks for suggestion blocks must be literal: ` ```suggestion`

### Essential Read Commands

**Connection and user info:**

```bash
bitbucket_test                              # Test connection
bitbucket_user                              # Get current user info
bitbucket_workspaces                        # List accessible workspaces
```

**Repository info:**

```bash
bitbucket_repo myworkspace myrepo           # Get repository details
bitbucket_repos myworkspace                 # List repositories in workspace
bitbucket_branches myworkspace myrepo       # List branches
```

**Pull request info:**

```bash
bitbucket_pr myworkspace myrepo 123                # Get PR details
bitbucket_pr_diff myworkspace myrepo 123           # Get PR diff
bitbucket_pr_comments myworkspace myrepo 123       # Get PR comments
```

**Pipeline info:**

```bash
bitbucket_pipeline myworkspace myrepo PIPELINE_UUID           # Get pipeline details
bitbucket_pipeline_steps myworkspace myrepo PIPELINE_UUID     # Get pipeline steps
```

### Supported Parameters Reference

#### bitbucket_pr - Get pull request details

**Required parameters:**
1. `workspace` : Workspace slug
2. `repo_slug` : Repository slug
3. `pr_id` : Pull request ID

**Example:**
```bash
bitbucket_pr myworkspace myrepo 123
```

#### bitbucket_pr_diff - Get pull request diff

**Required parameters:**
1. `workspace` : Workspace slug
2. `repo_slug` : Repository slug
3. `pr_id` : Pull request ID

**Returns:** Unified diff text

#### bitbucket_pr_comments - Get PR comments

**Required parameters:**
1. `workspace` : Workspace slug
2. `repo_slug` : Repository slug
3. `pr_id` : Pull request ID

**Returns:** JSON array of comment objects

#### bitbucket_repos - List repositories

**Required parameters:**
1. `workspace` : Workspace slug

**Optional parameters:**
- Second param: Results per page (default: 25)

**Example:**
```bash
bitbucket_repos myworkspace 50  # Get up to 50 repos
```

### Write Commands (Code Review)

#### bitbucket_create_pr_comment - Inline code comment

**Required parameters:**
1. `workspace` : Workspace slug
2. `repo_slug` : Repository slug
3. `pr_id` : Pull request ID
4. `file_path` : Path to file (e.g., 'src/app.py')
5. `line_number` : Line number on NEW side of diff
6. `body` : Comment text (use single quotes for markdown)

**Example with suggestion:**
````bash
bitbucket_create_pr_comment myworkspace myrepo 123 "src/auth.py" 45 'Add input validation

```suggestion
if not validate_input(data):
    raise ValueError("Invalid input")
```
'
````

#### bitbucket_create_pr_discussion - General PR comment

**Required parameters:**
1. `workspace` : Workspace slug
2. `repo_slug` : Repository slug
3. `pr_id` : Pull request ID
4. `body` : Comment text

Use this for:
- Overall review summaries
- General feedback that doesn't apply to specific lines

**Example:**
```bash
bitbucket_create_pr_discussion myworkspace myrepo 123 'Code Review Summary

Looks good overall:
- 3 files reviewed
- 2 inline comments posted
- Ready for merge'
```

#### bitbucket_update_comment - Update existing comment

**Required parameters:**
1. `workspace` : Workspace slug
2. `repo_slug` : Repository slug
3. `pr_id` : Pull request ID
4. `comment_id` : Comment ID to update
5. `body` : New comment text

#### bitbucket_delete_comment - Delete comment

**Required parameters:**
1. `workspace` : Workspace slug
2. `repo_slug` : Repository slug
3. `pr_id` : Pull request ID
4. `comment_id` : Comment ID to delete

### Key Rules

1. **ALWAYS use helper functions for code review inline comments** - Use `bitbucket_create_pr_comment`
2. **Always specify workspace and repo_slug** - Every command needs them
3. **For general operations**: Use helper functions (list, view, etc.)
4. **Write operations**: All require user approval
5. **Suggestion blocks**: Must use helper functions with single quotes
6. **Multi-repo**: Use explicit workspace/repo for each command:
   ```bash
   bitbucket_pr workspace1 frontend-repo 45
   bitbucket_pr workspace1 backend-repo 67
   ```

### Errors

| Problem                       | Solution                                               |
| ----------------------------- | ------------------------------------------------------ |
| **"401 Unauthorized"**        | Token expired, refresh OAuth token                     |
| **"404 Not Found"**           | Check workspace/repo_slug spelling                     |
| **"Rate limit exceeded"**     | Helper auto-retries, wait a few seconds                |
| **"line not in diff"**        | Use `bitbucket_create_pr_discussion` instead           |
| **Empty response**            | Check if PR/resource exists                            |

### Critical Operations

**⚠️ NEVER do these without explicit user instruction:**

- `bitbucket_delete_comment` - Only on explicit request
- Any operation that modifies PR state - Only on explicit request

### API Notes

- Bitbucket Cloud API 2.0 is used
- All responses are paginated (helper handles this)
- Rate limiting: 1000 requests/hour per user
- Token expiration: OAuth tokens expire, helper shows warning

## Output Format

Present results as a structured report:
```
Bitbucket Report
════════════════
Resources discovered: [count]

Resource       Status    Key Metric    Issues
──────────────────────────────────────────────
[name]         [ok/warn] [value]       [findings]

Summary: [total] resources | [ok] healthy | [warn] warnings | [crit] critical
Action Items: [list of prioritized findings]
```

Target ≤50 lines of output. Use tables for multi-resource comparisons.

## Anti-Hallucination Rules

1. **NEVER assume resource names** — always discover via CLI/API in Phase 1 before referencing in Phase 2.
2. **NEVER fabricate metric names or dimensions** — verify against the service documentation or `--help` output.
3. **NEVER mix CLI commands between service versions** — confirm which version/API you are targeting.
4. **ALWAYS use the discovery → verify → analyze chain** — every resource referenced must have been discovered first.
5. **ALWAYS handle empty results gracefully** — an empty response is valid data, not an error to retry.

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "I'll skip discovery and check known resources" | Always run Phase 1 discovery first | Resource names change, new resources appear — assumed names cause errors |
| "The user only asked for a quick check" | Follow the full discovery → analysis flow | Quick checks miss critical issues; structured analysis catches silent failures |
| "Default configuration is probably fine" | Audit configuration explicitly | Defaults often leave logging, security, and optimization features disabled |
| "Metrics aren't needed for this" | Always check relevant metrics when available | API/CLI responses show current state; metrics reveal trends and intermittent issues |
| "I don't have access to that" | Try the command and report the actual error | Assumed permission failures prevent useful investigation; actual errors are informative |

