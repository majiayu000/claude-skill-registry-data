---
name: "bitbucket-cloud"
description: "Handle Bitbucket Cloud PR operations. Use for \"PR\", \"pull request\", \"review\" when repo is on bitbucket.org."
---

# Bitbucket Cloud PR Operations

Use `mcp__plugin_bitbucket-plugin__*` MCP tools.

## Step 1: Detect Platform (REQUIRED)

Run `git remote -v` to identify platform:
- `bitbucket.org` → ✅ Bitbucket Cloud (continue)
- `bitbucket.<company>.com` or custom domain → Use `bitbucket-datacenter` skill
- `github.com` → Use `github-pr` skill

**Extract from URL:**
- SSH: `git@bitbucket.org:workspace/repo.git` → workspace=`workspace`, repo=`repo`
- HTTPS: `https://bitbucket.org/workspace/repo.git` → workspace=`workspace`, repo=`repo`

## Output Format

List PRs as table: `| # | Title | Author | Branch | Status | Updated |`
Status: ✅ Open | 📝 Draft | 🔀 Merged | ❌ Declined

## PR Review

1. Fetch PR details + diff
2. Analyze: bugs, security, performance, code quality
3. Present: `## PR Review: #<NUM> - <TITLE>` with Summary, Issues Found (`[file:line]`), Verdict (APPROVE/REQUEST_CHANGES/COMMENT)
4. Post comments/approve if requested
