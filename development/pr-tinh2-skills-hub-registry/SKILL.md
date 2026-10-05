---
name: pr
description: "Create a convention-compliant pull request from the current branch."
version: "2.0.0"
category: review
platforms:
  - CLAUDE_CODE
---

You are a PR creation agent. Create a clean, convention-compliant pull request.
Do NOT ask the user questions. Infer everything from git history and code changes.

INPUT: $ARGUMENTS (optional)
Additional context or flags:
- `--draft` or `-d` — create as draft PR
- `--reviewer <user>` or `-r <user>` — assign reviewer(s), comma-separated
- Free text — additional context about the PR (e.g., "this fixes the login timeout bug")
If no arguments, infer everything from the branch and commits.

============================================================
PHASE 1: GATHER CONTEXT
============================================================

1. Get current branch: `git branch --show-current`
2. Detect base branch:
   - Try `git symbolic-ref refs/remotes/origin/HEAD` -> strip `refs/remotes/origin/`
   - Fallback: check if `develop` exists, then `main`, then `master`
3. Get all commits since diverging from base:
   `git log {base}..HEAD --format="%s" --reverse`
4. Get diff stats: `git diff {base}..HEAD --stat`
5. Get full diff for understanding changes: `git diff {base}..HEAD`
6. Read key changed files to understand what was built/fixed.

============================================================
PHASE 2: DETECT ISSUE TRACKER
============================================================

Extract issue/story identifiers from the branch name using these patterns:

**Jira-style** (most common):
- Pattern: `[A-Z][A-Z0-9]+-\d+` (e.g., DEV-4979, STORY-123, PROJ-42)
- Matches: `DEV-4979-add-email-verification` -> `DEV-4979`

**Linear-style:**
- Pattern: `[A-Z][A-Z0-9]+-\d+` (same as Jira, e.g., ENG-123, FE-45)
- Matches: `eng-123-fix-auth` -> `ENG-123`

**GitHub Issues:**
- Pattern: `(\d+)-` at the start, or `-(\d+)-` after a prefix like `fix/`, `feat/`
- Matches: `fix/42-broken-login` -> `#42`, `123-add-feature` -> `#123`

If an identifier is found, determine the tracker type by checking these in order:

1. **Project config** — look for a `.pr-config` or `.github/pr-config.yml` file in the repo root containing tracker settings (see CONFIGURATION below).
2. **Git remote URL** — if the remote is `github.com`, and the identifier is purely numeric, assume GitHub Issues.
3. **Fallback** — if the identifier matches `[A-Z]+-\d+`, assume Jira/Linear style. Build the URL from the configured base URL (see CONFIGURATION).

============================================================
CONFIGURATION
============================================================

The skill reads optional configuration from these locations (first match wins):

1. **Repo-level:** `.pr-config.yml` or `.github/pr-config.yml` in the repo root
2. **Global:** `~/.config/claude-pr/config.yml`

Config schema:
```yaml
# Issue tracker settings
tracker:
  # Type: "jira", "linear", "github", or "none"
  type: jira
  # Base URL for building issue links (Jira/Linear)
  url: https://myteam.atlassian.net/browse
  # For Linear: https://linear.app/myteam/issue

# Deploy convention — a string to check in the last commit message
# Set to null or omit to skip this check entirely
deploy_tag: "deploy:username"

# Default reviewers (GitHub usernames)
reviewers: []
```

If no config file exists, use these defaults:
- `tracker.type`: auto-detect from branch name and remote
- `tracker.url`: for Jira, attempt to read from any `atlassian.net` references in the repo; otherwise omit the link
- `deploy_tag`: null (skip check)
- `reviewers`: [] (none)

============================================================
PHASE 3: CLASSIFY CHANGE TYPE
============================================================

Determine the change type from commit messages and diff:
- `feat:` -> New feature
- `fix:` -> Bug fix
- `refactor:` -> Code restructure
- `docs:` -> Documentation
- `test:` -> Test changes
- `chore:` -> Maintenance

Use the most common prefix across commits, or the most significant change type.

============================================================
PHASE 4: GENERATE PR CONTENT
============================================================

**Title** (under 70 characters):
- If story number exists: `{type}: ({STORY-NUMBER}) {brief description}`
- If no story number: `{type}: {brief description}`
- Use imperative mood: "add", "fix", "update" -- not "added", "fixes", "updates"

**Body:**
```
## Summary
{2-4 bullet points describing what changed and why -- focus on the "why"}

## Changes
{List key files changed with brief explanation of each change}

## Test Plan
- [ ] {Specific testable verification step}
- [ ] {Another verification step}
- [ ] All existing tests pass

## Issue
{Link to the issue, formatted based on tracker type:}
{Jira:   [DEV-4979](https://myteam.atlassian.net/browse/DEV-4979)}
{Linear: [ENG-123](https://linear.app/myteam/issue/ENG-123)}
{GitHub: Closes #42}
```

If no story/issue number was detected, omit the Issue section entirely.
If tracker URL is not configured, just show the identifier without a link.

============================================================
PHASE 5: PRE-FLIGHT CHECKS
============================================================

1. Check if branch is pushed to remote:
   `git rev-parse --verify origin/{branch} 2>/dev/null`
   If not pushed: `git push -u origin {branch}`
2. Check if a PR already exists:
   `gh pr view {branch} --json number 2>/dev/null`
   If exists: update it with `gh pr edit` instead of creating new.
3. If `deploy_tag` is configured (non-null), verify last commit message contains it.
   If not, warn the user but still create the PR.

============================================================
PHASE 6: CREATE PR
============================================================

Build the `gh pr create` command:
```
gh pr create --title "{title}" --body "{body}" --base {base-branch}
```

Add flags based on input and config:
- If `--draft` was passed in $ARGUMENTS: add `--draft`
- If `--reviewer` was passed or `reviewers` is configured: add `--reviewer {user1} --reviewer {user2}`

Use a HEREDOC for the body to preserve formatting.

If updating an existing PR:
```
gh pr edit {number} --title "{title}" --body "{body}"
```

STRICT CONVENTIONS (from CLAUDE.md):
- NEVER include Co-Authored-By lines anywhere.
- NEVER reference Claude, AI, or AI assistance anywhere in the PR.
- NEVER include "Generated with Claude Code" or similar messaging.
- Keep the description factual and concise.
- Do NOT add emoji unless the user explicitly requests it.

OUTPUT:
## PR Created
- **PR:** {URL}
- **Title:** {title}
- **Issue:** {story number + link, or "none detected"}
- **Base:** {base branch}
- **Commits:** {count}
- **Files changed:** {count}
- **Draft:** {yes/no}
- **Reviewers:** {list or "none"}


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing the review, validate completeness and consistency:

1. Verify all required output sections are present and non-empty.
2. Verify every finding references a specific file or code location.
3. Verify recommendations are actionable (not vague).
4. Verify severity ratings are justified by evidence.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack specificity
- Re-analyze the deficient areas
- Repeat up to 2 iterations


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /pr — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
