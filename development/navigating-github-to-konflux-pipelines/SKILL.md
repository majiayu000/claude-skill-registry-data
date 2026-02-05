---
name: navigating-github-to-konflux-pipelines
description: Use when GitHub PR or branch has failing checks and you need to find Konflux pipeline information (cluster, namespace, PipelineRun name). Teaches gh CLI commands to identify Konflux checks (filter out Prow/SonarCloud), extract PipelineRun URLs from builds and integration tests, and parse URLs for kubectl debugging.
allowed-tools: Bash(gh pr:*), Bash(gh repo:*), Bash(grep:*), Bash(sed:*), Bash(echo:*), Bash(~/.claude/skills/navigating-github-to-konflux-pipelines/scripts/get-branch-checks.sh:*)
---

# Navigating GitHub to Konflux Pipelines

## Overview

**Core Principle**: Extract Konflux pipeline information from GitHub checks using `gh` CLI to enable debugging. This skill bridges "my PR/build is failing" to "here's the kubectl-ready PipelineRun information."

**Key Workflow**:
```
GitHub PR/Commit → Query checks → Filter Konflux checks →
Extract PipelineRun URL → Parse cluster/namespace/name → Debug with kubectl
```

## When to Use

Use this skill when:
- "My PR checks are failing" (need to find which Konflux pipeline failed)
- "The build is failing on main" (need PipelineRun details for a branch)
- "Integration tests failed" (need to extract test pipeline information)
- User mentions failing GitHub checks on a Konflux-enabled repository
- User asks about failing checks and mentions a PR number or branch name

**DO NOT use for**:
- Debugging the actual pipeline failure (use `debugging-pipeline-failures` skill)
- GitLab pipelines (separate twin skill coming later)

## Critical Rules: NO EXCUSES - RUN COMMANDS IMMEDIATELY

**YOU MUST TRY THE COMMANDS. NO EXCEPTIONS. NO APOLOGIES.**

### Immediate Action Protocol

When user mentions:
- "PR #<number>" → IMMEDIATELY run `gh pr checks <number> --repo <owner>/<repo>`
- "failing checks" → IMMEDIATELY run the gh command
- "main branch failing" → IMMEDIATELY run `~/.claude/skills/navigating-github-to-konflux-pipelines/scripts/get-branch-checks.sh`

**CRITICAL**: NEVER use `gh api` directly. ALWAYS use `~/.claude/skills/navigating-github-to-konflux-pipelines/scripts/get-branch-checks.sh` for branch/commit checks.

**DO NOT**:
- ❌ Say "I apologize"
- ❌ Say "authentication issue"
- ❌ Say "I'm unable to access"
- ❌ Ask for "more context"
- ❌ Suggest "ensure you're logged in"
- ❌ Recommend "gh auth login"
- ❌ Say "let me ask you to provide"

**INSTEAD**:
1. ✅ RUN the command
2. ✅ IF it fails, SHOW the actual error
3. ✅ THEN suggest fixes based on the actual error

**Example of CORRECT behavior**:
```
User: "PR #249 in konflux-ci/oras-container has failing checks"
You: [Immediately runs: gh pr checks 249 --repo konflux-ci/oras-container]
[If it works: shows results]
[If it fails: shows actual error, then suggests fix]
```

**Example of WRONG behavior** (DO NOT DO THIS):
```
User: "PR #249 in konflux-ci/oras-container has failing checks"
You: "I apologize, but I'm unable to access..." ← WRONG
You: "Could you provide more context..." ← WRONG
You: "Ensure you're logged in..." ← WRONG
```

## Identifying Konflux Checks

**Pattern**: A check is Konflux-related if the check NAME or details URL contains `konflux` (case-insensitive).

**Common Konflux Check Prefixes**:
- `Red Hat Konflux /`
- `Konflux Fedora /`
- `Integration Service /`
- Any check with `konflux` in the name

**Non-Konflux Checks to IGNORE**:
- `ci/prow/*` - OpenShift CI (not Konflux)
- `SonarCloud Code Analysis`
- `tide` - Prow merge bot
- `dco` - Developer Certificate of Origin

**IMPORTANT**: Do NOT confuse GitHub Actions (visible in "Actions" tab, use `gh run list`) with GitHub Checks (visible in "Checks" tab, use `gh pr checks`). Konflux uses the Checks API, not Actions workflows.

**IMPORTANT - Branch checks**: ALWAYS use the `get-branch-checks.sh` wrapper script for querying branch/commit checks. NEVER call `gh api` directly - the script handles the API call internally.

## Check Type Classification

| Check Name Pattern | Type | PipelineRun URL Location |
|--------------------|------|-------------------------|
| `*/-on-pull-request` | Build (PR) | Direct in `details_url` |
| `*/-on-push` | Build (branch/main) | Direct in `details_url` |
| Contains test name (functional-test, enterprise-contract, unit-test) | Integration Test | In `output.text` (needs parsing) |

## GitHub CLI Commands

### For Pull Requests

```bash
# List all checks for a PR (human-readable)
gh pr checks <pr-number> --repo <owner>/<repo>

# Get JSON with all check details
gh pr view <pr-number> --repo <owner>/<repo> --json statusCheckRollup

# Filter for Konflux checks only
gh pr view <pr-number> --repo <owner>/<repo> --json statusCheckRollup \
  --jq '.statusCheckRollup[] | select(.name | ascii_downcase | contains("konflux"))'

# Get commit SHA from PR (needed for check-runs API)
gh pr view <pr-number> --repo <owner>/<repo> --json headRefOid -q .headRefOid
```

### For Branches/Commits

**Note**: GitHub CLI doesn't have a built-in command for branch checks, so we use a wrapper script around the read-only `check-runs` API endpoint:

```bash
# Get checks for latest commit on a branch
~/.claude/skills/navigating-github-to-konflux-pipelines/scripts/get-branch-checks.sh <owner> <repo> <branch>

# Filter for Konflux checks
~/.claude/skills/navigating-github-to-konflux-pipelines/scripts/get-branch-checks.sh \
  konflux-ci yq-container main \
  '.check_runs[] | select(.name | ascii_downcase | contains("konflux"))'

# Get checks for specific commit SHA
~/.claude/skills/navigating-github-to-konflux-pipelines/scripts/get-branch-checks.sh <owner> <repo> <sha>
```

**Security note**: The `get-branch-checks.sh` script uses the read-only GitHub API endpoint `repos/{owner}/{repo}/commits/{ref}/check-runs`. It does not modify any data.

### Infer Repo from Context

If user doesn't specify repo and you're in a git repository:

```bash
# Get current repo owner and name
owner=$(gh repo view --json owner -q .owner.login)
repo=$(gh repo view --json name -q .name)

# Then use as normal
gh pr checks <pr-number> --repo $owner/$repo
```

## Extracting PipelineRun URLs

### From Build Checks (-on-pull-request, -on-push)

Build checks have the PipelineRun URL directly in `details_url`:

```bash
# For PRs
gh pr view <pr-number> --repo <owner>/<repo> --json statusCheckRollup \
  --jq '.statusCheckRollup[] | select(.name | endswith("-on-pull-request")) | {name: .name, url: .detailsUrl}'

# For branches/commits
~/.claude/skills/navigating-github-to-konflux-pipelines/scripts/get-branch-checks.sh \
  <owner> <repo> main \
  '.check_runs[] | select(.name | endswith("-on-push")) | {name: .name, url: .details_url}'
```

### From Integration Test Checks

Integration test checks require extracting the URL from check output:

```bash
# Get commit SHA first
sha=$(gh pr view <pr-number> --repo <owner>/<repo> --json headRefOid -q .headRefOid)

# Extract PipelineRun URL from check output (contains HTML)
~/.claude/skills/navigating-github-to-konflux-pipelines/scripts/get-branch-checks.sh \
  <owner> <repo> $sha \
  '.check_runs[] | select(.name | ascii_downcase | contains("functional-test")) | .output.text' \
  | grep -o 'https://[^"]*konflux[^"]*pipelinerun/[^"]*' | head -1
```

## Parsing PipelineRun URLs

URL format: `https://{cluster}/ns/{namespace}/pipelinerun/{name}`

Example: `https://konflux-ui.apps.stone-prd-rh01.pg1f.p1.openshiftapps.com/ns/rhtap-integration-tenant/pipelinerun/yq-on-pull-request-69sq8`

```bash
url="<pipelinerun-url>"
cluster=$(echo "$url" | sed 's|https://\([^/]*\).*|\1|')
namespace=$(echo "$url" | sed 's|.*/ns/\([^/]*\).*|\1|')
pipelinerun=$(echo "$url" | sed 's|.*/pipelinerun/\([^/?]*\).*|\1|')

# Result:
# Cluster: konflux-ui.apps.stone-prd-rh01.pg1f.p1.openshiftapps.com
# Namespace: rhtap-integration-tenant
# PipelineRun: yq-on-pull-request-69sq8
```

## Complete Workflow Examples

### Example 1: PR with Failing Checks

User: "PR #249 in konflux-ci/oras-container has failing checks"

```bash
# Step 1: List all checks
gh pr checks 249 --repo konflux-ci/oras-container

# Step 2: Filter for Konflux checks only
gh pr view 249 --repo konflux-ci/oras-container --json statusCheckRollup \
  --jq '.statusCheckRollup[] | select(.name | ascii_downcase | contains("konflux")) | {name: .name, conclusion: .conclusion, url: .detailsUrl}'

# Step 3: Identify build vs integration test failures
# - Build check: "oras-container-on-pull-request" → URL in detailsUrl
# - Integration test: "functional-test" → need to extract from output

# Step 4: For integration test, get commit SHA and extract URL
sha=$(gh pr view 249 --repo konflux-ci/oras-container --json headRefOid -q .headRefOid)
~/.claude/skills/navigating-github-to-konflux-pipelines/scripts/get-branch-checks.sh \
  konflux-ci oras-container $sha \
  '.check_runs[] | select(.name | contains("functional-test")) | .output.text' \
  | grep -o 'https://[^"]*pipelinerun/[^"]*'

# Step 5: Parse URL for kubectl
url="<extracted-url>"
namespace=$(echo "$url" | sed 's|.*/ns/\([^/]*\).*|\1|')
pipelinerun=$(echo "$url" | sed 's|.*/pipelinerun/\([^/?]*\).*|\1|')

# Ready for debugging-pipeline-failures skill
```

### Example 2: Build Failing on Main Branch

User: "The build is failing on main in yq-container"

```bash
# Step 1: Query checks on main branch
~/.claude/skills/navigating-github-to-konflux-pipelines/scripts/get-branch-checks.sh \
  konflux-ci yq-container main \
  '.check_runs[] | select(.name | ascii_downcase | contains("konflux")) | {name: .name, conclusion: .conclusion, url: .details_url}'

# Step 2: Look for -on-push check (not -on-pull-request)
# "yq-on-push" → URL is directly in details_url

# Step 3: Parse and debug
```

## Rationalizations to Avoid

| Excuse | Reality | What To Do Instead |
|--------|---------|-------------------|
| "I'm unable to access the PR" | You have `gh` CLI - try it first | Run `gh pr checks <num> --repo owner/repo` |
| "Due to authentication constraints" | Don't assume - commands might work | Try the command, show error only if it actually fails |
| "I need more context" | PR number + repo gives you everything | Use `gh pr view --json` to get all check data |
| "Let me open browser with --web" | Programmatic access is better | Use `--json` flag for structured data |
| "I apologize, but..." | Don't apologize, DO | Run the commands immediately |
| "Encountering restrictions" | Assumption until proven | Try first, report actual errors if they occur |

**If you catch yourself saying any of these, STOP. Run the command instead.**

## Common Confusions

### ❌ WRONG: "I don't have access to check information"
✅ CORRECT: Try `gh pr checks` (for PRs) or `get-branch-checks.sh` script (for branches) first - only report errors if commands actually fail

---

### ❌ WRONG: Look for checks with prefix `konflux/` or `build/` or `ci/`
✅ CORRECT: Filter for checks where NAME contains `konflux` (case-insensitive)

---

### ❌ WRONG: "Let me open the PR in browser with `gh pr view --web`"
✅ CORRECT: Use `gh pr view --json` for programmatic access to PR data

---

### ❌ WRONG: Check the "Actions" tab or use `gh run list`
✅ CORRECT: Konflux uses GitHub Checks API (not Actions workflows)

---

### ❌ WRONG: All integration test checks have PipelineRun URL in `details_url`
✅ CORRECT: Some have it there, but many need extraction from `output.text` field

---

### ❌ WRONG: Use same check names for PR and branch builds
✅ CORRECT: PRs use `-on-pull-request`, branches use `-on-push`

## Decision Tree: Which Check Should I Debug First?

```
Are there failing checks?
├─ Filter for Konflux checks (contains "konflux" in name/URL)
├─ Ignore: ci/prow/*, SonarCloud, tide, dco
│
└─ Which failed?
   ├─ Build check (*-on-pull-request or *-on-push) → Debug first!
   │   └─ Build failures often cause integration tests to be cancelled
   │
   └─ Integration test check → Debug only if build succeeded
       └─ Extract PipelineRun URL from output.text
```

## Chaining to Next Skill

Once you have extracted:
- Cluster URL
- Namespace
- PipelineRun name

→ Use the **debugging-pipeline-failures** skill to investigate the actual failure with kubectl commands

## Keywords for Search

GitHub checks, pull request failures, Konflux pipeline, gh CLI, check-runs API, PipelineRun URL, integration tests, build failures, statusCheckRollup, GitHub API, kubectl debugging, namespace extraction, CI/CD troubleshooting, check filtering, Prow vs Konflux
