---
name: "bitbucket-datacenter"
description: "Handle Bitbucket Data Center/Server PR operations. Use for \"PR\", \"pull request\", \"review\" when repo is on self-hosted Bitbucket (NOT bitbucket.org)."
---

# Bitbucket Data Center PR Operations

Use `mcp__plugin_bitbucket-datacenter-plugin__*` MCP tools.

## Step 1: Detect Platform (REQUIRED)

Run `git remote -v` to identify platform:
- `bitbucket.<company>.com` or custom domain → ✅ Bitbucket DC (continue)
- `bitbucket.org` → Use `bitbucket-cloud` skill
- `github.com` → Use `github-pr` skill

**Extract from URL:**
- SSH: `git@bitbucket.company.com:7999/PROJ/repo.git` → workspace=`PROJ`, repo=`repo`
- HTTPS: `https://bitbucket.company.com/scm/PROJ/repo.git` → workspace=`PROJ`, repo=`repo`

## Output Format

List PRs as table: `| # | Title | Author | Branch | Status | Updated |`
Status: ✅ Open | 📝 Draft | 🔀 Merged | ❌ Declined

## PR Review

1. Fetch PR details + diff
2. Analyze: bugs, security, performance, code quality
3. Present: `## PR Review: #<NUM> - <TITLE>` with Summary, Issues Found (`[file:line]`), Verdict (APPROVE/REQUEST_CHANGES/COMMENT)
4. Post comments/approve if requested
