---
name: daily-code-review
description: Generate a daily code review report showing stale PRs, items needing your attention, and active work for your team. Use whenever the user asks for a PR report, code review status, daily standup prep, team PR overview, "what needs review", "what's stale", "show me open PRs", "daily review", "PR check", "review report", "what should I look at today", or any question about tracking pull request activity across a team or pod. Also trigger when the user mentions a specific pod name that matches a saved config.
---

# Daily Code Review Report

> **No em-dashes.** Nothing this skill writes may contain an em-dash; use a comma, colon, or parentheses instead. Enforced by a repo hook that flags em-dashes in generated `.md`. See `/flagrare:write-docs`.

Generate a team-wide pull request status report focused on actionable next steps. The report surfaces stale PRs, items needing the runner's personal attention, and a quick FYI on active work, so the reader knows exactly what to do when they open GitHub.

## Setup (first run only)

Team configs live at **`~/.claude/skills/flagrare/daily-code-review/teams/*.json`**: one file per team, outside the plugin tree so they survive plugin updates and reinstalls.

In Bash, expand `~` explicitly: `"$HOME/.claude/skills/flagrare/daily-code-review/teams"`. The directory may not exist yet, `mkdir -p "$HOME/.claude/skills/flagrare/daily-code-review/teams"` before writing.

### Step 1: Migrate legacy configs (one-time)

If the new dir has no team files but the legacy per-plugin dir does, migrate them:

```bash
LEGACY="{skill_directory}/teams"   # old location, lost on plugin reinstall
NEW="$HOME/.claude/skills/flagrare/daily-code-review/teams"
if [ -d "$LEGACY" ] && [ ! -d "$NEW" ]; then
  mkdir -p "$NEW"
  cp "$LEGACY"/*.json "$NEW"/ 2>/dev/null || true
fi
```

Tell the user once: "Migrated your team configs from the old per-plugin location to `~/.claude/skills/flagrare/daily-code-review/teams/` so they survive plugin updates."

### Step 2: Check for existing configs

Check for config files matching `~/.claude/skills/flagrare/daily-code-review/teams/*.json`. If none exist, run the first-time setup flow.

### First-time setup

Use `AskUserQuestion` to collect:

1. **GitHub org**: the GitHub organization to search (e.g., `acme-corp`)
2. **Team name**: a human label for the report header (e.g., `Platform Team`)
3. **Team members**: for each person, their GitHub login and display name. Ask in a single prompt, one member per line, format: `github_login / Display Name`

Save to `~/.claude/skills/flagrare/daily-code-review/teams/{team-name-slug}.json`:

```json
{
  "org": "acme-corp",
  "team_name": "Platform Team",
  "members": [
    { "github_login": "aturing", "display_name": "Alan Turing" },
    { "github_login": "ghopper", "display_name": "Grace Hopper" },
    { "github_login": "dknuth", "display_name": "Don Knuth" }
  ]
}
```

Confirm the config with the user before proceeding.

### Returning user

If exactly one team config exists, use it. If multiple exist, ask which team to report on.

If the user says "add a team" or "edit team," update or create the relevant config file and re-confirm.

## Detect "Me"

Run:

```bash
gh api user --jq '.login'
```

Match against the team members list by `github_login`. If no match, ask the user which member they are, they might be authenticated with a personal account that differs from their team login.

## Data Collection

Use **only** these GitHub API endpoints. The comments API is noisy and `mergeable_state` is unreliable, skip both. Staleness comes from `updated_at` alone.

### Open PRs per member

The search/issues endpoint does NOT return draft status reliably (it comes back null). Run two searches per member to separate drafts from non-drafts:

```bash
gh api "search/issues?q=org:{org}+is:pr+is:open+-is:draft+author:{login}&per_page=100" \
  --jq '.items[] | {number, title, html_url, updated_at, draft: false, repo: (.repository_url | split("/") | last), user: .user.login}'
```

```bash
gh api "search/issues?q=org:{org}+is:pr+is:open+is:draft+author:{login}&per_page=100" \
  --jq '.items[] | {number, title, html_url, updated_at, draft: true, repo: (.repository_url | split("/") | last), user: .user.login}'
```

Run all searches in parallel across team members. Deduplicate by PR number + repo.

### Reviews and requested reviewers

For each PR:

```bash
gh api "repos/{org}/{repo}/pulls/{number}/reviews" \
  --jq '[.[] | select(.user.login | test("\\[bot\\]$") | not) | {user: .user.login, state}]'
```

```bash
gh api "repos/{org}/{repo}/pulls/{number}/requested_reviewers" \
  --jq '{users: [.users[].login], teams: [.teams[].slug]}'
```

Filter out bot reviews (logins ending in `[bot]`), they're noise from CI integrations, not human review activity.

Run these in parallel across PRs where possible. If you hit rate limits, back off and retry.

## Classification

### Staleness thresholds

| Category | Threshold |
|----------|-----------|
| Stale (pod-wide) | `updated_at` > 24 hours ago |
| Needs attention | `updated_at` > 12 hours ago |
| Parked draft | draft + `updated_at` > 30 days ago |

Calculate hours (or days for parked drafts) since `updated_at` relative to now. Round to the nearest whole number.

### Review state

Determine per-PR by reading the reviews list chronologically:

- **Approved**: at least one `APPROVED` review, no subsequent `CHANGES_REQUESTED`
- **Changes requested**: most recent non-dismissed review is `CHANGES_REQUESTED`
- **Pending**: has requested reviewers who haven't submitted a review

Show reviewer names in each state (e.g., "approved by Alice, Bob").

## Report Format

```
# {team_name} Code Review Report: {YYYY-MM-DD}
> Generated for **{display_name}** | {n} open PRs across {m} members
```

### Section 1: Stale PRs (>24h no action)

All open PRs across the team (including drafts) where `updated_at` > 24h. Only exclude drafts older than 30 days, those go in the "Parked Drafts" section instead. Label draft PRs with a `[Draft]` tag so they're visually distinct.

For each PR, show:

| Owner | PR | Hours stale | Review state | Next action |
|-------|-----|-------------|--------------|-------------|
| Display name | [Title](url) | N hours | Approved by X / Changes requested by Y / Pending: Z | One-line recommendation |

Sort by staleness descending. "Next action" should be specific and direct: "Merge, already approved," "Address feedback from Carol," "Needs a reviewer assigned."

If no stale PRs: *"No stale PRs, the team is on top of reviews."*

### Section 2: Needs My Attention (>12h no action)

Two sub-sections:

**PRs I need to review**
PRs where I'm a requested reviewer and haven't submitted a review yet. Show: author, title+URL, hours waiting.

**My PRs needing action**
My own PRs that are approved (merge them!) or have changes requested (address feedback). Show: title+URL, state, hours since last update.

If nothing in either sub-section: *"Nothing needs your attention right now."*

If the user has stale PRs in Section 1 but none qualify here (e.g., all are drafts or pending first review), add a brief note pointing them back: *"Your 3 open PRs are stale but waiting on reviewers or still in draft, see Section 1 above."* This bridges the gap so Section 2 doesn't feel disconnected when all the user's action items are upstream.

### Active (FYI)

My open PRs or pending review requests updated within the last 12 hours. One line each: title, URL, current state. No action needed, just awareness.

If nothing active: omit this section entirely.

### Parked Drafts

Draft PRs from any team member untouched for 30+ days. Show: owner, title+URL, days since update. These are informational, the team may want to close or revive them.

If none: omit this section.

## Output

Always render the full report as formatted markdown in the conversation.

If the user asks to save to a file, write to the path they specify. If they say "save it" without a path, default to `./pr-report-{YYYY-MM-DD}.md`.

## Edge cases

- A PR can appear in both Section 1 (pod-wide stale) and Section 2 (needs my attention). That's expected, different audiences for the same PR.
- If a team member's PRs can't be fetched (permissions, API error), note it in the report footer and continue with the rest.
- If `gh` is not installed or not authenticated, tell the user to run `gh auth login` first.
