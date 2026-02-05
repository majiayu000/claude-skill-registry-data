---
name: github-pr-utils
description: Utility scripts for GitHub pull request management. Includes tools for fetching bot-generated review comments (linters, security scanners, dependabot), replying to review threads programmatically, listing merged pull requests with filtering, resolving conversations, and automating PR review workflows. Useful for batch processing comments, CI/CD integration, quality metrics tracking, release notes generation, and automated responses to bot reviewers.
---
# github-pr-utils

A collection of utility scripts for managing GitHub pull requests, including review comment management, merged PR tracking, and automated workflows. These scripts are designed for handling bot-generated review feedback, generating release notes, and automating PR review workflows.

## Requirements

These scripts can be executed in two ways depending on your environment:

### Option 1: Direct Execution (Traditional)

**Requirements:**
- `gh` CLI version 2.60+
- `jq` CLI version 1.6+

**When to use:**
- You have `gh` and `jq` installed on your host system
- You've permisson to run scripts directly
- You prefer traditional shell command execution

### Option 2: Via Gosu MCP Server (run_cli)

**Requirements:**
- Gosu MCP server running and connected
- Tool `mcp__gosu__run_cli` is available on the Gosu MCP server

**When to use:**
- `gh` or `jq` are not installed on your host system
- `gh` CLI is not authenticated on your host system
- You prefer a sandbox environment for command execution

## Available Scripts

### 1. get_pr_bot_review_comments.sh

Fetches all bot-authored review comments for a pull request using the GitHub GraphQL API.

#### Usage

```bash
scripts/get_pr_bot_review_comments.sh [OPTIONS] <owner> <repo> <pr_number>
```

#### Options

- `--exclude-resolved` - Filter out resolved review threads
- `--exclude-outdated` - Filter out outdated review comments
- `--include-github-user login1,login2` - Also include comments from specific GitHub users (comma-separated list)
- `--include-diff-hunk` - Include the diff hunk context for each comment, do use this option unless explicitly requested by user.
- `-h, --help` - Display help message

#### Arguments

- `<owner>` - Repository owner (organization or user)
- `<repo>` - Repository name
- `<pr_number>` - Pull request number

#### Output

Returns a JSON array of review comments with the following structure:
```json
[
  {
    "threadId": "PRRT_...",
    "threadPath": "src/file.go",
    "threadLine": 42,
    "threadStartLine": null,
    "threadOriginalLine": null,
    "threadOriginalStartLine": null,
    "threadIsResolved": false,
    "threadIsOutdated": false,
    "comment": {
      "id": "PRRC_...",
      "databaseId": 123456789,
      "url": "https://github.com/...",
      "createdAt": "2024-01-01T00:00:00Z",
      "updatedAt": "2024-01-01T00:00:00Z",
      "body": "Comment text here",
      "isMinimized": false,
      "minimizedReason": null,
      "outdated": false,
      "path": "src/file.go",
      "position": 42,
      "originalPosition": null,
      "diffHunk": "@@ -40,7 +40,7 @@ ...",
      "author": {
        "__typename": "Bot",
        "login": "bot-name[bot]"
      },
      "commit": {
        "oid": "abc123..."
      }
    }
  }
]
```

#### Examples

**Fetch all bot comments for a PR:**
```bash
scripts/get_pr_bot_review_comments.sh gosu-code gosu-mcp-server 123
```

**Fetch unresolved bot comments:**
```bash
scripts/get_pr_bot_review_comments.sh \
  --exclude-resolved \
  gosu-code gosu-mcp-server 123
```

**Fetch unresolved & not outdated bot comments:**
```bash
scripts/get_pr_bot_review_comments.sh \
  --exclude-resolved \
  --exclude-outdated \
  gosu-code gosu-mcp-server 123
```

**Fetch comments from bot and also non bot users:**
```bash
scripts/get_pr_bot_review_comments.sh \
  --exclude-resolved \
  --include-github-user dependabot,renovate \
  gosu-code gosu-mcp-server 123
```

**Process comments with jq:**
```bash
# Count total bot comments
scripts/get_pr_bot_review_comments.sh gosu-code gosu-mcp-server 123 | jq 'length'

# Extract comment bodies only
scripts/get_pr_bot_review_comments.sh gosu-code gosu-mcp-server 123 | \
  jq -r '.[].comment.body'

# Group comments by file
scripts/get_pr_bot_review_comments.sh gosu-code gosu-mcp-server 123 | \
  jq 'group_by(.threadPath) | map({path: .[0].threadPath, count: length})'
```

#### Common Use Cases

1. **Review Bot Feedback**: Quickly collect all bot-generated comments to address automated review suggestions
2. **Quality Metrics**: Track unresolved bot comments as part of merge criteria
3. **Diff Context Analysis**: Include diff hunks to understand the exact code context for each comment
4. **Multi-Bot Aggregation**: Combine feedback from multiple bot reviewers (e.g., linters, security scanners)

---

### 2. reply_pr_review_comments_thread.sh

Reply to an existing pull request review comment thread using the GitHub REST API.

#### Usage

```bash
scripts/reply_pr_review_comments_thread.sh [OPTIONS] <owner> <repo> <comment_id>
```

#### Options

**Body Input (choose one):**
- `--body "text"` - Inline Markdown body for the reply (prefer to use this unless the text is long or contain special character)
- `--body-file path` - Read reply body from a file
- `--stdin` - Read reply body from STDIN (not recommended to use)

**Additional Options:**
- `--thread-id id` - GraphQL thread node ID (required with `--resolve-thread`)
- `--resolve-thread` - Resolve the review thread after posting (requires `--thread-id`)
- `-h, --help` - Display help message

#### Arguments

- `<owner>` - Repository owner (organization or user)
- `<repo>` - Repository name
- `<comment_id>` - Comment ID (either numeric database ID or GraphQL node ID like `PRRC_*`)

#### Examples

**Reply with inline text:**
```bash
scripts/reply_pr_review_comments_thread.sh \
  --body "Thanks for catching that! Fixed in the latest commit." \
  gosu-code gosu-mcp-server 2451122234
```

**Reply from a file:**
```bash
scripts/reply_pr_review_comments_thread.sh \
  --body-file reply.md \
  gosu-code gosu-mcp-server 2451122234
```

**Compose reply in editor:**
```bash
scripts/reply_pr_review_comments_thread.sh \
  gosu-code gosu-mcp-server 2451122234
```

**Reply with confirmation prompt:**
```bash
scripts/reply_pr_review_comments_thread.sh \
  --body "Updated the implementation." \
  gosu-code gosu-mcp-server 2451122234
```

**Reply and resolve the thread:**
```bash
scripts/reply_pr_review_comments_thread.sh \
  --body "Done! Resolving this thread." \
  --thread-id PRRT_kwDODds1es5e2SRi \
  --resolve-thread \
  gosu-code gosu-mcp-server 2451122234
```

**Dry run to preview:**
```bash
scripts/reply_pr_review_comments_thread.sh \
  --body "Test reply" \
  gosu-code gosu-mcp-server 2451122234
```

#### Common Use Cases

1. **Automated Responses**: Reply to bot comments programmatically (e.g., acknowledging fixes)
2. **Batch Processing**: Loop through multiple comments and reply to each
3. **CI/CD Integration**: Post automated updates from build/test pipelines
4. **Thread Resolution**: Reply and resolve threads in a single operation

---

### 3. list_merged_pr.sh

List merged pull requests with optional filtering by authors and date range. Supports saving PR details to individual markdown files for documentation or release notes.

#### Usage

```bash
scripts/list_merged_pr.sh [OPTIONS]
```

#### Options

**Filtering Options:**
- `-a, --authors USERS` - Comma-separated list of GitHub usernames to filter by
- `-f, --from DATE` - Start date for PR merge filter (YYYY-MM-DD format)
- `-t, --to DATE` - End date for PR merge filter (YYYY-MM-DD format)
- `-d, --days DAYS` - Number of days to look back (alternative to --from), default: 7
- `-r, --repo REPO` - GitHub repository in format "owner/repo", default: current repository

**Output Options:**
- `-s, --save [DIR]` - Save PR details to files (one file per PR), optional directory path, default: ./out
- `-h, --help` - Display help message

#### Output

**Console Output:**
Displays a tab-separated list of PRs with: PR number, title (truncated to 120 chars), author, merge date, and URL.

**File Output (with `--save`):**
Creates one markdown file per PR with the format `PR-{number}-{title}.md` containing:
- PR metadata (author, merge date, URL)
- Full PR description
- List of commits with authors and messages
- Generation timestamp

#### Examples

**List all merged PRs from last 7 days (default):**
```bash
scripts/list_merged_pr.sh
```

**List merged PRs from specific authors:**
```bash
scripts/list_merged_pr.sh --authors "john,jane,bob"
```

**List merged PRs from last 30 days:**
```bash
scripts/list_merged_pr.sh --days 30
```

**List merged PRs within a specific date range:**
```bash
scripts/list_merged_pr.sh --from "2025-10-01" --to "2025-10-31"
```

**Combine filters: specific authors and date range:**
```bash
scripts/list_merged_pr.sh --authors "john,jane" --from "2025-10-01" --to "2025-10-31"
```

**Query a specific repository:**
```bash
scripts/list_merged_pr.sh --repo "owner/repo" --days 30
```

**Save PR details to files in ./out directory:**
```bash
scripts/list_merged_pr.sh --save
```

**Save PR details to custom directory:**
```bash
scripts/list_merged_pr.sh --save /path/to/output --days 30
```

**Process with jq:**
```bash
# Count merged PRs
scripts/list_merged_pr.sh --days 30 | wc -l

# Extract just PR numbers
scripts/list_merged_pr.sh | cut -f1 | sed 's/#//'
```

#### Common Use Cases

1. **Release Notes Generation**: Save PRs from a release period to markdown files for changelog creation
2. **Team Activity Tracking**: Filter by team member usernames to track contributions
3. **Sprint Reports**: Query PRs merged during a sprint date range
4. **Quality Metrics**: Analyze merge patterns and PR velocity over time
5. **Documentation**: Generate detailed PR summaries with full context for auditing

---

## Workflow Examples

### Example 1: Address All Unresolved Bot Comments

```bash
# Fetch all unresolved bot comments
comments=$(scripts/get_pr_bot_review_comments.sh \
  --exclude-resolved \
  gosu-code gosu-mcp-server 123)

# Loop through and reply to each
echo "$comments" | jq -r '.[].comment.databaseId' | while read -r comment_id; do
  scripts/reply_pr_review_comments_thread.sh \
    --body "Addressed in latest commit." \
    gosu-code gosu-mcp-server "$comment_id"
done
```

### Example 2: Generate Summary Report

```bash
# Fetch comments with the entire file diff context
scripts/get_pr_bot_review_comments.sh \
  --exclude-resolved \
  --include-diff-hunk \
  gosu-code gosu-mcp-server 123 > bot_comments.json

# Generate markdown report with from json output
jq -r '.[] | "## \(.threadPath):\(.threadLine)\n\n\(.comment.body)\n\n```diff\n\(.comment.diffHunk)\n```\n"' \
  bot_comments.json > bot_review_summary.md
```

### Example 3: Selective Response by Bot Type

```bash
# Get comments from bots and also `dependabot` user
dependabot_comments=$(scripts/get_pr_bot_review_comments.sh \
  --include-github-user dependabot \
  gosu-code gosu-mcp-server 123)

# Reply to each with specific message
echo "$dependabot_comments" | jq -r '.[].comment.databaseId' | while read -r comment_id; do
  echo "Acknowledged, Will fix this in another PR." | \
  scripts/reply_pr_review_comments_thread.sh \
    --stdin \
    gosu-code gosu-mcp-server "$comment_id"
done
```

### Example 4: Interactive Review Session

```bash
# Fetch all unresolved comments
scripts/get_pr_bot_review_comments.sh \
  --exclude-resolved \
  gosu-code gosu-mcp-server 123 | \
jq -r '.[] | "\n=== \(.threadPath):\(.threadLine) ===\n\(.comment.body)\n\nComment ID: \(.comment.databaseId)"'
```

## Notes

- Both scripts handle pagination automatically for large result sets
- The `get_pr_bot_review_comments.sh` script identifies bots by checking if the author's `__typename` is "Bot" or if the login contains "[bot]"
- Comment IDs can be either numeric database IDs or GraphQL node IDs (starting with "PRRC_" or "PRRT_")
- Thread resolution requires the GraphQL thread ID (format: "PRRT_...")
- All scripts include error checking for GraphQL and REST API responses

## Common Troubleshooting

**Authentication errors:**
Confirm if user is authenticated in the GitHub CLI, if not inform user to login with a credential that have the right access
```bash
gh auth status
```

**Permission errors:**
- Ensure you have write access to the repository
- Check that your GitHub token has the required scopes

---

## Using Scripts via Gosu MCP run_cli tool (Run Option 2)

When `gh` or `jq` are not available on your host system, you can use the Gosu MCP server's `run_cli` tool (tool full name: `mcp__gosu__run_cli`) to execute these scripts in a sandboxed environment where all required tools are available.

### How It Works

The MCP `run_cli` tool:
- Executes scripts in the MCP server's sandbox environment which have access to your current working directory
- Automatically injects `GH_TOKEN` from server configuration for authentication
- Supports all whitelisted programs: `bash`, `gh`, `jq`, `git`, `python3`, and others
- Returns structured execution results with exit codes, stdout, stderr, and timing

### Quick Start

**Step 1: Copy Scripts to Workspace**
```bash
cp -rf ${CLAUDE_PLUGIN_ROOT}/skills/github-pr-utils/scripts ./scripts/
```

**Step 2: Use MCP run_cli Tool**

Basic structure of an MCP `run_cli` call:
```json
{
  "program": "bash",
  "arguments": ["scripts/script-name.sh", "arg1", "arg2", "..."],
  "timeout": 120
}
```

**Step 3: Process Results**

The tool returns:
```json
{
  "exit_code": 0,
  "stdout": "script output here",
  "stderr": "",
  "duration_ms": 1543,
  "truncated": false,
  "stderr_truncated": false
}
```

### MCP Tool Parameters Reference

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `program` | string | Yes | `"bash"` for shell scripts, `"jq"` for JSON processing, `"gh"` for GitHub CLI |
| `arguments` | array | Yes | For bash: `["scripts/script.sh", "args..."]`<br>For jq: `["filter", "file.json"]` |
| `timeout` | number | No | Timeout in seconds (default: 60, max: 300) |
| `environment` | object | No | Additional environment variables (GH_TOKEN auto-injected) |
| `stdin_input` | string | No | String to pipe to stdin (mutually exclusive with stdin_file) |
| `stdin_file` | string | No | File path to read for stdin (mutually exclusive with stdin_input) |
| `output_file` | string | No | Redirect stdout to file (for large outputs > 100KB) |
| `error_file` | string | No | Redirect stderr to file |

**Important Notes:**
- Use `"program": "bash"` only for running `.sh` scripts, not inline bash commands
- Use `"program": "jq"` for JSON processing instead of `bash -c "jq ..."`
- Output is truncated at 100KB unless redirected to file
- All file paths must be relative to workspace directory
- GH_TOKEN is automatically injected for `bash` and `gh` programs
- Default timeout is 60 seconds (increase for long-running operations)

### MCP Tool Specific Notes

When using these scripts via MCP `run_cli`:
- **Automatic Authentication**: GH_TOKEN is automatically injected for `bash` and `gh` programs - no manual `gh auth login` required
- **Sandbox Environment**: Scripts execute in MCP sandbox environment with all file paths relative to workspace root
- **Output Limits**: Stdout and stderr are truncated at 100KB unless redirected to file using `output_file` or `error_file` parameters
- **Timeout Defaults**: Default timeout is 60 seconds, configurable up to 300 seconds for long-running operations
- **File Paths**: All file paths must be relative to workspace directory - absolute paths and path traversal (`../`) are blocked for security
- **Exit Codes**: Always check `exit_code` in response - 0 indicates success, non-zero indicates error, 124 indicates timeout
- **Error Details**: Check `stderr` field in response for error messages when `exit_code` is non-zero

### Script-Specific MCP Examples

#### 1. get_pr_bot_review_comments.sh

**Fetch all bot comments:**
```json
{
  "program": "bash",
  "arguments": [
    "scripts/get_pr_bot_review_comments.sh",
    "gosu-code",
    "gosu-mcp-server",
    "123"
  ],
  "output_file": "bot_comments.json"
}
```

**Fetch unresolved bot comments:**
```json
{
  "program": "bash",
  "arguments": [
    "scripts/get_pr_bot_review_comments.sh",
    "--exclude-resolved",
    "gosu-code",
    "gosu-mcp-server",
    "123"
  ],
  "output_file": "unresolved_comments.json"
}
```

**Fetch unresolved & not outdated comments:**
```json
{
  "program": "bash",
  "arguments": [
    "scripts/get_pr_bot_review_comments.sh",
    "--exclude-resolved",
    "--exclude-outdated",
    "gosu-code",
    "gosu-mcp-server",
    "123"
  ],
  "output_file": "active_comments.json"
}
```

**Include specific GitHub users:**
```json
{
  "program": "bash",
  "arguments": [
    "scripts/get_pr_bot_review_comments.sh",
    "--exclude-resolved",
    "--include-github-user",
    "dependabot,renovate",
    "gosu-code",
    "gosu-mcp-server",
    "123"
  ],
  "output_file": "bot_and_user_comments.json"
}
```

**Process JSON with jq:**
```json
{
  "program": "jq",
  "arguments": ["length", "bot_comments.json"]
}
```

**Extract comment bodies:**
```json
{
  "program": "jq",
  "arguments": ["-r", ".[].comment.body", "bot_comments.json"]
}
```

**Group comments by file:**
```json
{
  "program": "jq",
  "arguments": [
    "group_by(.threadPath) | map({path: .[0].threadPath, count: length})",
    "bot_comments.json"
  ]
}
```

#### 2. reply_pr_review_comments_thread.sh

**Reply with inline text:**
```json
{
  "program": "bash",
  "arguments": [
    "scripts/reply_pr_review_comments_thread.sh",
    "--body",
    "Thanks for catching that! Fixed in the latest commit.",
    "gosu-code",
    "gosu-mcp-server",
    "2451122234"
  ]
}
```

**Reply from file content:**

First, create the reply file:
```json
{
  "program": "bash",
  "arguments": [
    "-c",
    "echo 'Updated the implementation as suggested.' > reply.md"
  ]
}
```

Then reply using the file:
```json
{
  "program": "bash",
  "arguments": [
    "scripts/reply_pr_review_comments_thread.sh",
    "--body-file",
    "reply.md",
    "gosu-code",
    "gosu-mcp-server",
    "2451122234"
  ]
}
```

**Reply and resolve thread:**
```json
{
  "program": "bash",
  "arguments": [
    "scripts/reply_pr_review_comments_thread.sh",
    "--body",
    "Done! Resolving this thread.",
    "--thread-id",
    "PRRT_kwDODds1es5e2SRi",
    "--resolve-thread",
    "gosu-code",
    "gosu-mcp-server",
    "2451122234"
  ]
}
```

**Multiple sequential replies:**

Loop through comment IDs and reply to each:
```json
{
  "program": "bash",
  "arguments": [
    "-c",
    "jq -r '.[].comment.databaseId' bot_comments.json | while read -r id; do scripts/reply_pr_review_comments_thread.sh --body 'Addressed in latest commit.' gosu-code gosu-mcp-server \"$id\"; done"
  ],
  "timeout": 180
}
```

#### 3. list_merged_pr.sh

**List all merged PRs from last 7 days:**
```json
{
  "program": "bash",
  "arguments": ["scripts/list_merged_pr.sh"],
  "output_file": "merged_prs.txt"
}
```

**Filter by specific authors:**
```json
{
  "program": "bash",
  "arguments": [
    "scripts/list_merged_pr.sh",
    "--authors",
    "john,jane,bob"
  ],
  "output_file": "team_prs.txt"
}
```

**List PRs from last 30 days:**
```json
{
  "program": "bash",
  "arguments": [
    "scripts/list_merged_pr.sh",
    "--days",
    "30"
  ],
  "output_file": "monthly_prs.txt"
}
```

**Specific date range:**
```json
{
  "program": "bash",
  "arguments": [
    "scripts/list_merged_pr.sh",
    "--from",
    "2025-10-01",
    "--to",
    "2025-10-31"
  ],
  "output_file": "october_prs.txt"
}
```

**Save PR details to files:**
```json
{
  "program": "bash",
  "arguments": [
    "scripts/list_merged_pr.sh",
    "--save",
    "./out",
    "--days",
    "30"
  ],
  "timeout": 180
}
```

**Query specific repository:**
```json
{
  "program": "bash",
  "arguments": [
    "scripts/list_merged_pr.sh",
    "--repo",
    "owner/repo",
    "--days",
    "30"
  ],
  "output_file": "repo_prs.txt"
}
```

### Advanced Patterns

#### Chaining Multiple Operations

**Fetch comments, then process with jq:**
```json
# Step 1: Fetch comments
{
  "program": "bash",
  "arguments": [
    "scripts/get_pr_bot_review_comments.sh",
    "--exclude-resolved",
    "gosu-code",
    "gosu-mcp-server",
    "123"
  ],
  "output_file": "comments.json"
}

# Step 2: Count comments
{
  "program": "jq",
  "arguments": ["length", "comments.json"]
}

# Step 3: Extract thread IDs
{
  "program": "jq",
  "arguments": ["-r", ".[].threadId", "comments.json"],
  "output_file": "thread_ids.txt"
}
```

#### Error Handling

Always check `exit_code` in the response:
```json
{
  "program": "bash",
  "arguments": ["scripts/get_pr_bot_review_comments.sh", "owner", "repo", "123"],
  "output_file": "comments.json"
}

// Response:
{
  "exit_code": 0,  // 0 = success, non-zero = error
  "stdout": "",
  "stderr": "",
  "duration_ms": 1543,
  "output_file": "comments.json"
}
```

If `exit_code` is non-zero, check `stderr` for error details.

#### Handling Large Outputs

For operations that produce large output (> 100KB), use `output_file`:
```json
{
  "program": "bash",
  "arguments": [
    "scripts/get_pr_bot_review_comments.sh",
    "--include-diff-hunk",
    "gosu-code",
    "gosu-mcp-server",
    "123"
  ],
  "output_file": "large_comments.json",
  "timeout": 120
}
```

Then read the file separately or process it with subsequent `jq` commands.

#### Using stdin_input for Piping

Pass data to program via stdin:
```json
{
  "program": "jq",
  "arguments": [".[] | select(.threadIsResolved == false)"],
  "stdin_input": "[{\"threadId\":\"PRRT_123\",\"threadIsResolved\":false},{\"threadId\":\"PRRT_456\",\"threadIsResolved\":true}]"
}
```

### MCP Troubleshooting

**Script not found error:**
```
exit_code: 127
stderr: "bash: scripts/get_pr_bot_review_comments.sh: No such file or directory"
```
**Solution**: Ensure scripts are copied to workspace directory and path is correct relative to workspace root.

**Output truncated warning:**
```
{
  "exit_code": 0,
  "stdout": "...",
  "truncated": true
}
```
**Solution**: Use `output_file` parameter to redirect output to a file and avoid 100KB truncation limit.

**Timeout error:**
```
exit_code: 124
stderr: "signal: killed"
```
**Solution**: Increase `timeout` parameter (max 300 seconds) for long-running operations.

**Path traversal blocked:**
```
stderr: "Error: path traversal attempt detected"
```
**Solution**: Use relative paths only. Paths like `../` or absolute paths are blocked for security.

**Permission denied errors:**
```
exit_code: 1
stderr: "permission denied: scripts/get_pr_bot_review_comments.sh"
```
**Solutions:**
- Ensure scripts have execute permissions: `chmod +x scripts/*.sh`
- Check file ownership and permissions in the workspace directory

**JSON parsing errors with jq:**
```
exit_code: 1
stderr: "jq: parse error: Invalid JSON"
```
**Solutions:**
- Verify the input file contains valid JSON: `cat file.json | jq .`
- Check that previous command succeeded before piping to jq
- Use `output_file` to inspect intermediate outputs for debugging
