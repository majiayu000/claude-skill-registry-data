---
name: gitlab
description: "REQUIRED helper functions (never raw curl), project_id patterns, suggestion block syntax with offset notation"
connection_type: gitlab
preload: false
---

# GitLab CLI Skill

Execute GitLab helper functions and git commands with proper authentication.

**You must source the helpers before use:**

```bash
source ./_skills/connections/gitlab/gitlab/scripts/gitlab_helpers.sh
```

## CLI Tips

### NEVER USE RAW CURL OR DIRECT API CALLS

**DO NOT write raw curl/HTTP requests like:**

```bash
# ❌ WRONG - Never do this
curl -s --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" "${GITLAB_HOST}/api/v4/..."
```

**ALWAYS use the provided helper functions:**

```bash
# ✅ CORRECT - Use helper functions
gitlab_user                         # Get current user
gitlab_projects                     # List projects
gitlab_mr $PROJ MR_IID             # Get MR details
```

The helper functions handle authentication, error handling, and output formatting automatically.

### CRITICAL: Project ID as First Parameter

**ALL commands require explicit `project_id` as the FIRST parameter.**

```bash
PROJ=$(gitlab_project_id "org/repo")  # Get project ID
gitlab_mr $PROJ 123                    # Use in commands
```

### Code Review Helper Functions (GitLab)

**Inline comment with suggestion block:**

````bash
gitlab_create_diff_note $PROJ MR_IID "file.py" LINE 'Comment text

```suggestion:-0+2
fixed code line 1
fixed code line 2
````

' "LINE_TYPE"

````
- `LINE_TYPE`: "new" for added lines, "old" for removed
- Use single quotes to preserve backticks literally - NO escaping needed
- Offset notation `-X+Y`: remove X lines above, add Y lines below

**Discussion comment:**
```bash
gitlab_create_mr_discussion $PROJ MR_IID 'Comment text'
````

### Suggestion Block Syntax (CRITICAL)

**✅ CORRECT - Single quotes preserve backticks with offset notation:**

````bash
gitlab_create_diff_note $PROJ 45 "src/app.py" 10 '🔴 CRITICAL: Issue

```suggestion:-0+1
if not input.strip():
    raise ValueError("Required")
````

' "new"

````

**❌ WRONG - Escaped backticks break rendering:**
```bash
gitlab_create_diff_note $PROJ 45 "src/app.py" 10 "\`\`\`suggestion:-0+1
code
\`\`\`" "new"
````

**Key rules:**

- Use single quotes to wrap comment body containing markdown
- Backticks inside single quotes are literal - write them normally
- NEVER escape backticks with backslashes (\\`) - this breaks GitLab's markdown parser
- Triple backticks must include offset notation: ` ```suggestion:-X+Y`
- Offset notation: `-X` (lines to remove above) `+Y` (lines to add below)

### Essential Read Commands

**MR info:**

```bash
gitlab_mr $PROJ MR_IID                         # Get MR metadata
gitlab_mr_diff $PROJ MR_IID                    # Get full diff
gitlab_mr_diff $PROJ MR_IID --summary          # Get diff summary (fast)
gitlab_mr_diff $PROJ MR_IID --filter "\.py$"   # Filter by file pattern
```

**List with filters:**

```bash
gitlab_mrs $PROJ --state merged --author-username john
gitlab_issues $PROJ --state opened --assignee-username jane --labels "bug"
gitlab_pipelines $PROJ --status running --ref main
```

**Other info:**

```bash
gitlab_mr_commits $PROJ MR_IID                    # List MR commits
gitlab_mr_changes $PROJ MR_IID [per_page] [page]  # List changed files
gitlab_mr_discussions $PROJ MR_IID                 # List discussion threads
gitlab_mr_discussion $PROJ MR_IID DISCUSSION_ID   # Get specific thread
gitlab_mr_diff_metadata $PROJ MR_IID              # Get SHA refs for diff comments
gitlab_mr_approval_status $PROJ MR_IID            # Check merge readiness
gitlab_commits $PROJ [ref] [per_page] [page]      # List commits on branch
gitlab_branches $PROJ                              # List branches
gitlab_file $PROJ FILE_PATH [ref]                  # Get file content
```

**CI/CD info:**

```bash
gitlab_pipeline $PROJ PIPELINE_ID                  # Get pipeline details
gitlab_jobs $PROJ PIPELINE_ID                      # List pipeline jobs
gitlab_job_log $PROJ JOB_ID                        # Get job trace/log output
gitlab_pipeline_failures $PROJ PIPELINE_ID         # List failed jobs in pipeline
gitlab_job_failure_summary $PROJ JOB_ID            # Analyze job failure with log tail
gitlab_pipeline_history $PROJ [ref] [per_page]     # Recent pipelines on branch
gitlab_compare_pipelines $PROJ [ref]               # Compare latest failed vs successful
gitlab_ci_stats $PROJ [per_page]                   # Pipeline success/failure rates
```

### Supported Parameters Reference

#### gitlab_mrs - List merge requests

**Supported parameters:**
- `--state` : opened | closed | merged | all (default: opened)
- `--author-username` : Filter by author username
- `--assignee-username` : Filter by assignee username
- `--labels` : Comma-separated labels (e.g., "bug,critical")
- `--search` : Keyword search in title/description
- `--per-page` : Results per page (default: 20, max: 100)

**NOT SUPPORTED (will cause error):**
- `--created-after` / `--created-before` - Date filtering not available
- `--updated-after` / `--updated-before` - Date filtering not available
- `--milestone` - Milestone filtering not supported
- Alternative: Use `--search` with date in text, or filter results post-fetch

**Example:**
```bash
# ✅ Correct
gitlab_mrs $PROJ --state merged --author-username john --per-page 50

# ❌ Wrong - unsupported flags
gitlab_mrs $PROJ --created-after "2026-01-01"  # ERROR: Unknown flag
```

#### gitlab_issues - List issues

**Supported parameters:**
- `--state` : opened | closed | all (default: opened)
- `--assignee-username` : Filter by username
- `--labels` : Comma-separated labels
- `--search` : Keyword search
- `--per-page` : Results per page

**NOT SUPPORTED:**
- `--created-after` / `--created-before` - Not available
- `--milestone` - Not supported
- `--author` - Use `--search` instead

#### gitlab_mr_diff - Get MR diff

**Supported parameters:**
- `--summary` : Show file paths and stats only (fast, recommended for large MRs)
- `--filter PATTERN` : Regex pattern to filter files (e.g., `\.py$` for Python only)

**NOT SUPPORTED:**
- `--context` : Context lines not configurable
- `--unified` : Diff format not changeable

#### gitlab_mr_commits - List MR commits

**Supported parameters:**
- No additional flags supported (project_id and MR_IID only)

#### gitlab_pipelines - List pipelines

**Supported parameters:**
- `--status` : running | pending | success | failed | canceled | skipped
- `--ref` : Branch or tag name
- `--per-page` : Results per page

**NOT SUPPORTED:**
- `--created-after` / `--created-before` - Not available
- `--user` - Not supported

#### gitlab_branches - List branches

**Supported parameters:**
- `project_id` : Numeric project ID (required)

**NOT SUPPORTED:**
- `--search` : Not implemented
- `--per-page` : Not implemented
- `--sort` : Sorting not configurable
- `--order` : Ordering not available

#### gitlab_pipeline_history - Pipeline history for a branch

**Positional parameters:**
- `project_id` : Numeric project ID (required)
- `ref` : Branch/tag name (default: main)
- `per_page` : Results per page (default: 10)

#### gitlab_ci_stats - CI/CD success/failure rates

**Positional parameters:**
- `project_id` : Numeric project ID (required)
- `per_page` : Sample size of recent pipelines (default: 50)

#### gitlab_commits - List commits on a branch

**Positional parameters:**
- `project_id` : Numeric project ID (required)
- `ref` : Branch/tag name (default: main)
- `per_page` : Results per page (default: 20)
- `page` : Page number (default: 1)

#### gitlab_mr_changes - List changed files in an MR

**Positional parameters:**
- `project_id` : Numeric project ID (required)
- `mr_iid` : Merge request IID (required)
- `per_page` : Changes per page (default: 100)
- `page` : Page number (default: 1)
- `all_pages` : Fetch all pages, true/false (default: false)

### Parameter Validation Rules

**BEFORE executing any gitlab_* helper function:**

1. **Check this SKILL.md** - Verify the flag is listed in "Supported parameters"
2. **If flag not listed** - Assume it's unsupported, don't guess
3. **If unsure** - Use the basic command first, then check error message
4. **Alternative approaches**:
   - Post-fetch filtering: Get all results, filter in your script
   - Search text workarounds: Use `--search` with date/milestone text
   - Direct API: For very specific needs, consider raw GitLab API calls (not recommended)

**Common mistake pattern:**
```bash
# User asks: "List MRs from January 2026"
# ❌ WRONG: Assume date filtering exists
gitlab_mrs $PROJ --created-after "2026-01-01"  # Will fail

# ✅ CORRECT: Check SKILL.md first, then use supported approach
gitlab_mrs $PROJ --state all --per-page 100 | grep "2026-01"
# OR: Fetch recent MRs and filter by parsing JSON output
```

### Essential Write Commands (Require Approval)

**MR operations:**

```bash
gitlab_update_mr $PROJ MR_IID --title "New Title" --description "Updated" --labels "ready"
gitlab_merge_mr $PROJ MR_IID       # Merge MR
gitlab_close_mr $PROJ MR_IID       # Close MR
gitlab_reopen_mr $PROJ MR_IID      # Reopen MR
gitlab_approve_mr $PROJ MR_IID     # Approve MR
```

**Issue operations:**

```bash
gitlab_create_issue $PROJ --title "Bug fix" --description "Details" --labels "bug,critical"
gitlab_update_issue $PROJ ISSUE_IID --title "New Title" --description "Updated" --labels "bug,feature"
gitlab_close_issue $PROJ ISSUE_IID        # Close issue
gitlab_reopen_issue $PROJ ISSUE_IID       # Reopen issue
```

**Pipeline operations:**

```bash
gitlab_trigger_pipeline $PROJ [ref]       # Trigger new pipeline (default ref: main)
gitlab_retry_pipeline $PROJ PIPELINE_ID   # Retry all failed jobs in pipeline
gitlab_cancel_pipeline $PROJ PIPELINE_ID  # Cancel running pipeline
gitlab_retry_job $PROJ JOB_ID            # Retry a specific failed job
gitlab_cancel_job $PROJ JOB_ID           # Cancel a specific running job
gitlab_play_job $PROJ JOB_ID             # Trigger a manual/gated job
```

**MR/Issue comment operations:**

```bash
gitlab_create_mr $PROJ SOURCE TARGET TITLE [DESC]           # Create merge request
gitlab_add_mr_comment $PROJ MR_IID BODY                     # Add comment to MR
gitlab_add_issue_comment $PROJ ISSUE_IID BODY                # Add comment to issue
gitlab_add_discussion_note $PROJ MR_IID DISCUSSION_ID BODY   # Reply to discussion thread
gitlab_update_discussion $PROJ MR_IID DISCUSSION_ID BODY     # Update first note in thread
```

**Branch operations:**

```bash
gitlab_create_branch $PROJ BRANCH_NAME [ref]  # Create branch (default ref: main)
```

### CI/CD Pipelines

**Workflow: Debug a failed pipeline**

```bash
# 1. Find recent failed pipelines
gitlab_pipelines $PROJ --status failed --ref main

# 2. List failed jobs in that pipeline
gitlab_pipeline_failures $PROJ PIPELINE_ID

# 3. Get failure details and error log
gitlab_job_failure_summary $PROJ JOB_ID

# 4. Retry the failed job (or retry entire pipeline)
gitlab_retry_job $PROJ JOB_ID
```

**Pipeline inspection (read):**

| Command | Purpose |
|---------|---------|
| `gitlab_pipeline $PROJ PID` | Get pipeline details (status, ref, SHA) |
| `gitlab_jobs $PROJ PID` | List all jobs in a pipeline |
| `gitlab_job_log $PROJ JOB_ID` | Get job trace/log output |
| `gitlab_pipeline_failures $PROJ PID` | List only failed jobs with failure reasons |
| `gitlab_job_failure_summary $PROJ JOB_ID` | Job metadata + last 50 lines of log |
| `gitlab_pipeline_history $PROJ [ref] [per_page]` | Recent pipelines on a branch |
| `gitlab_compare_pipelines $PROJ [ref]` | Compare latest failed vs last successful |
| `gitlab_ci_stats $PROJ [per_page]` | Success/failure rates over recent pipelines |

**Pipeline control (write — requires approval):**

| Command | Purpose |
|---------|---------|
| `gitlab_trigger_pipeline $PROJ [ref]` | Trigger a new pipeline run |
| `gitlab_retry_pipeline $PROJ PID` | Retry all failed jobs in pipeline |
| `gitlab_cancel_pipeline $PROJ PID` | Cancel a running pipeline |
| `gitlab_retry_job $PROJ JOB_ID` | Retry a specific failed job |
| `gitlab_cancel_job $PROJ JOB_ID` | Cancel a specific running job |
| `gitlab_play_job $PROJ JOB_ID` | Trigger a manual/gated job |

### Key Rules

1. **ALWAYS use helper functions for code review inline comments** - Use `gitlab_create_diff_note` with offset notation
2. **Always get project_id first** - Use `PROJ=$(gitlab_project_id "org/repo")`
3. **PROJECT_ID is first parameter** - Every command needs it as first arg
4. **Suggestion blocks require offset notation** - Format: `suggestion:-X+Y` (X lines above, Y lines below)
5. **Write operations**: All require user approval
6. **Multi-repo**: Use variables:
   ```bash
   FRONTEND=$(gitlab_project_id "org/frontend")
   BACKEND=$(gitlab_project_id "org/backend")
   gitlab_mr $FRONTEND 45
   gitlab_mr $BACKEND 67
   ```

### Errors

| Problem                     | Solution                                              |
| --------------------------- | ----------------------------------------------------- |
| **"project not found"**     | Use `gitlab_project_id "org/repo"` to get correct ID  |
| **"line not in diff"**      | Use `gitlab_create_mr_discussion` instead             |
| **"authentication failed"** | Token auto-configured, verify project is accessible   |
| **Response too large**      | Use summary mode: `gitlab_mr_diff $PROJ MR --summary` |
| **"job not retryable"**     | Check job status with `gitlab_jobs` first — only failed jobs can be retried |
| **"pipeline not found"**    | Use `gitlab_pipelines` to list correct pipeline IDs |

### Critical Operations

**⚠️ NEVER do these without explicit user instruction:**

- `gitlab_approve_mr` - Only on explicit request
- `gitlab_merge_mr` - Only on explicit request
- `gitlab_close_mr` / `gitlab_close_issue` - Only on explicit request
- `gitlab_delete_branch` - Only on explicit request
- `gitlab_trigger_pipeline` - Triggers a new pipeline run
- `gitlab_cancel_pipeline` / `gitlab_cancel_job` - Interrupts running work
- `gitlab_play_job` - Triggers a manual/gated job
- `gitlab_create_branch` - Creates a branch

## Output Format

Present results as a structured report:
```
Gitlab Report
═════════════
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

