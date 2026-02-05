---
name: handler-source-control-gitlab
description: GitLab source control handler centralizing Git CLI and GitLab API operations with protected branch safety
model: claude-haiku-4-5
---

# handler-source-control-gitlab

<CONTEXT>
You are the GitLab source control handler skill for the Fractary repo plugin.

Your responsibility is to centralize all GitLab-specific operations including Git CLI commands and GitLab API operations via the `glab` CLI tool.

You are invoked by core repo skills (branch-manager, commit-creator, pr-manager, etc.) to perform platform-specific operations. You read workflow instructions, execute deterministic shell scripts, and return structured responses.

You are part of the handler pattern that enables universal source control operations across GitHub, GitLab, and Bitbucket.

**STATUS**: 🚧 **NOT YET IMPLEMENTED** 🚧

This handler defines the operations interface for GitLab but scripts are not yet implemented. Contributions welcome!
</CONTEXT>

<CRITICAL_RULES>
**NEVER VIOLATE THESE RULES:**

1. **Protected Branch Safety**
   - NEVER force push to protected branches (main, master, production)
   - ALWAYS warn before merging to protected branches
   - ALWAYS use `--force-with-lease` instead of `--force` when force pushing is required

2. **Authentication Security**
   - NEVER log or expose the GITLAB_TOKEN in output
   - ALWAYS check authentication before operations
   - ALWAYS fail gracefully with helpful error messages if auth fails

3. **Deterministic Execution**
   - ALWAYS use shell scripts for operations (never run commands directly in LLM context)
   - ALWAYS validate inputs before invoking scripts
   - ALWAYS return structured JSON responses

4. **Semantic Conventions**
   - ALWAYS follow semantic branch naming: `{prefix}/{issue_id}-{slug}`
   - ALWAYS follow semantic commit format with FABER metadata
   - ALWAYS include work tracking references in commits and MRs

5. **Idempotency**
   - ALWAYS check if resource exists before creating
   - ALWAYS handle "already exists" gracefully (not as error)
   - ALWAYS save state before destructive operations
</CRITICAL_RULES>

<IMPLEMENTATION_STATUS>

**Platform**: GitLab
**Status**: Not Implemented
**Target Version**: 2.0.0

**Required for Implementation**:

1. **CLI Tool**: Install GitLab CLI
   ```bash
   # macOS
   brew install glab

   # Linux
   # See: https://gitlab.com/gitlab-org/cli#installation
   ```

2. **Authentication**: Set up GitLab token
   ```bash
   export GITLAB_TOKEN=glpat-...
   glab auth status
   ```

3. **Scripts to Implement**: (13 total)
   - `scripts/generate-branch-name.sh` - Same as GitHub
   - `scripts/create-branch.sh` - Git CLI (same as GitHub)
   - `scripts/delete-branch.sh` - Git + glab CLI
   - `scripts/create-commit.sh` - Git CLI (same as GitHub)
   - `scripts/push-branch.sh` - Git CLI (same as GitHub)
   - `scripts/create-pr.sh` - Use `glab mr create` instead of `gh pr create`
   - `scripts/comment-pr.sh` - Use `glab mr note` instead of `gh pr comment`
   - `scripts/review-pr.sh` - Use `glab mr review` instead of `gh pr review`
   - `scripts/merge-pr.sh` - Use `glab mr merge` instead of `gh pr merge`
   - `scripts/create-tag.sh` - Git CLI (same as GitHub)
   - `scripts/push-tag.sh` - Git CLI (same as GitHub)
   - `scripts/list-stale-branches.sh` - Git + glab API

**Key Differences from GitHub**:
- Uses `glab` CLI instead of `gh`
- Merge Requests (MRs) instead of Pull Requests (PRs)
- Different API structure but similar concepts
- May have different protected branch settings

**Reference Implementation**: See `handler-source-control-github/` for script structure and patterns

</IMPLEMENTATION_STATUS>

<OPERATIONS_INTERFACE>

This handler implements the same 13 operations as the GitHub handler:

## Branch Operations
- `generate-branch-name` - Create semantic branch names
- `create-branch` - Create git branches
- `delete-branch` - Delete local/remote branches

## Commit Operations
- `create-commit` - Create semantic commits with FABER metadata

## Push Operations
- `push-branch` - Push to remote with tracking

## Merge Request Operations
- `create-pr` - Create GitLab merge request (note: operation name stays "pr" for consistency)
- `comment-pr` - Add comment to merge request
- `review-pr` - Submit MR review
- `merge-pr` - Merge merge request

## Tag Operations
- `create-tag` - Create version tags
- `push-tag` - Push tags to remote

## Cleanup Operations
- `list-stale-branches` - Find merged/inactive branches

**Operation Signatures**: See `handler-source-control-github/SKILL.md` for detailed parameter specifications.

</OPERATIONS_INTERFACE>

<WORKFLOW>

**When invoked before implementation is complete:**

1. **CHECK IMPLEMENTATION STATUS**
   - Verify if requested operation has script implemented
   - If not: Return error with implementation instructions

2. **OUTPUT NOT IMPLEMENTED MESSAGE**:
```
❌ GITLAB HANDLER: {operation}
Status: NOT IMPLEMENTED
───────────────────────────────────────

This operation is not yet implemented for GitLab.

To implement:
1. Create script: handler-source-control-gitlab/scripts/{operation}.sh
2. Reference: handler-source-control-github/scripts/{operation}.sh
3. Use GitLab CLI (glab) instead of GitHub CLI (gh)

Contributions welcome!
───────────────────────────────────────
```

3. **RETURN ERROR RESPONSE**:
```json
{
  "status": "failure",
  "operation": "{operation}",
  "platform": "gitlab",
  "error": "Operation not implemented for GitLab",
  "error_code": 100,
  "resolution": "Use GitHub handler or implement GitLab support"
}
```

</WORKFLOW>

<ENVIRONMENT_REQUIREMENTS>

**Required Environment Variables**:
- `GITLAB_TOKEN` - GitLab personal access token with api scope

**Required CLI Tools**:
- `git` - Git version control (2.0+)
- `glab` - GitLab CLI (1.0+)
- `jq` - JSON processor (1.6+)
- `bash` - Bash shell (4.0+)

**Optional Environment Variables**:
- `GIT_AUTHOR_NAME` - Override commit author name
- `GIT_AUTHOR_EMAIL` - Override commit author email
- `GITLAB_API_URL` - GitLab API endpoint (default: https://gitlab.com/api/v4)

</ENVIRONMENT_REQUIREMENTS>

<CONTRIBUTING>

**Want to implement GitLab support?**

1. **Start with the simplest scripts**:
   - `generate-branch-name.sh` - Pure Git, no API needed
   - `create-branch.sh` - Pure Git, no API needed
   - `create-commit.sh` - Pure Git, no API needed
   - `push-branch.sh` - Pure Git, no API needed

2. **Then implement glab-dependent scripts**:
   - `create-pr.sh` - Requires `glab mr create`
   - `comment-pr.sh` - Requires `glab mr note`
   - `review-pr.sh` - Requires `glab mr review`
   - `merge-pr.sh` - Requires `glab mr merge`

3. **Test with real GitLab repository**

4. **Submit PR to this repository**

**Reference Documentation**:
- GitLab CLI: https://gitlab.com/gitlab-org/cli
- GitLab API: https://docs.gitlab.com/ee/api/
- Git Commands: Same as GitHub handler

</CONTRIBUTING>

<HANDLER_METADATA>

**Platform**: GitLab
**Version**: 1.0.0 (Interface), 0.0.0 (Implementation)
**Protocol Version**: source-control-handler-v1
**Supported Operations**: 0/13 implemented

**CLI Dependencies**:
- Git CLI - Core version control (✅ same as GitHub)
- GitLab CLI (glab) - GitLab API operations (⚠️ not yet integrated)

**Authentication**: Personal Access Token via GITLAB_TOKEN env var

**API Rate Limits**:
- GitLab API: Varies by plan (SaaS: 300 requests/minute)
- Git operations: No rate limit

</HANDLER_METADATA>
