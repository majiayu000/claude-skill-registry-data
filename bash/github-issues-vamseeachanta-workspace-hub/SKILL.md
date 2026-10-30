---
name: github-issues
description: Create, manage, triage, and close GitHub issues. Search existing issues, add labels, assign people, and link to PRs. Works with gh CLI or falls back to git + GitHub REST API via curl.
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, Issues, Project-Management, Bug-Tracking, Triage]
    related_skills: [github-auth, github-pr-workflow]
---
## Implementation authority

The task request or standing authority authorizes implementation, including substantial work; no separate user plan approval, approval label or local marker is required. Complete planning, TDD and adversarial review, and resolve required domain decisions and blocking findings. Honor explicit planning-only requests. Consequential actions outside existing authority require matching explicit authorization. Implementation authority alone does not authorize publication, deployment, access changes or destructive actions; verify action/destination authority and reuse it when already provided. Preserve owner-controlled approval history without self-labeling.


# GitHub Issues Management

Create, search, triage, and manage GitHub issues. Each section shows `gh` first, then the `curl` fallback.

## Prerequisites

- Authenticated with GitHub (see `github-auth` skill)
- Inside a git repo with a GitHub remote, or specify the repo explicitly

### Private repository authorization

Deckhand retired 2026-10-18 (deckhand issue 599). The former bot scope shims and
gateway identity variables no longer apply.
Use the GitHub authentication prerequisite above. If authorized GitHub access
fails, report that access gap and keep direct issue state unverified. Durable
repository handoffs may supply clearly labeled secondary evidence. A private
repository 404
does not establish absence; do not bypass authorization controls.

### Setup

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
elif [ -n "${GITHUB_TOKEN:-}" ]; then
  AUTH="curl"
else
  echo "Authenticate with gh or export GITHUB_TOKEN explicitly before using curl fallbacks." >&2
  exit 1
fi

REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

Do not scrape tokens from local Hermes environment files, Git credential stores, or shell history in reusable issue scripts. Prefer `gh` authentication; use REST fallbacks only when `GITHUB_TOKEN` is already explicitly present in the environment.

---

## 1. Viewing Issues

**With gh:**

```bash
gh issue list
gh issue list --state open --label "bug"
gh issue list --assignee @me
gh issue list --search "authentication error" --state all
gh issue view 42
```

**With curl:**

```bash
# List open issues
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/issues?state=open&per_page=20" \
  | python3 -c "
import sys, json
for i in json.load(sys.stdin):
    if 'pull_request' not in i:  # GitHub API returns PRs in /issues too
        labels = ', '.join(l['name'] for l in i['labels'])
        print(f\"#{i['number']:5}  {i['state']:6}  {labels:30}  {i['title']}\")"

# Filter by label
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/issues?state=open&labels=bug&per_page=20" \
  | python3 -c "
import sys, json
for i in json.load(sys.stdin):
    if 'pull_request' not in i:
        print(f\"#{i['number']}  {i['title']}\")"

# View a specific issue
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42 \
  | python3 -c "
import sys, json
i = json.load(sys.stdin)
labels = ', '.join(l['name'] for l in i['labels'])
assignees = ', '.join(a['login'] for a in i['assignees'])
print(f\"#{i['number']}: {i['title']}\")
print(f\"State: {i['state']}  Labels: {labels}  Assignees: {assignees}\")
print(f\"Author: {i['user']['login']}  Created: {i['created_at']}\")
print(f\"\n{i['body']}\")"

# Search issues
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/issues?q=authentication+error+repo:$OWNER/$REPO" \
  | python3 -c "
import sys, json
for i in json.load(sys.stdin)['items']:
    print(f\"#{i['number']}  {i['state']:6}  {i['title']}\")"
```

## 2. Creating Issues

### Recommended pre-create workflow for feature issues

Before creating a new feature issue, do a quick grounding pass to avoid duplicates and align with repo taxonomy:

0. If the user's request is to convert notes into issues across multiple repos, first classify each candidate issue by canonical home before creating anything:
   - client-sensitive engagement notes, follow-up wording, pilot selection, and knowledge-base governance → private/client wiki or engagement repo;
   - engineering calculations, solver workflows, report-generation patterns, and model-readiness gaps → engineering/model repo;
   - public/regional data, field economics, HSE/safety datasets, and portfolio screening → data repo.
   Produce a routing summary with repo buckets before or alongside issue bodies so the user can audit placement.
1. Search existing issues by the key nouns/phrases in the request. Use broad searches first, then exact-title filtering if needed. `gh --jq` is not the standalone `jq` CLI and does not accept `--arg`; for exact title checks, pipe JSON to Python or `jq` yourself, for example:

   ```bash
   TITLE='feat(area): concise issue title'
   gh issue list --state all --limit 200 --json number,title,url \
     | python3 -c 'import json,os,sys; title=os.environ["TITLE"]; [print(f"#{i[\"number\"]}\t{i[\"url\"]}") for i in json.load(sys.stdin) if i["title"] == title]'
   ```

   If a duplicate-check command errors, stop and repair the check or verify by another broad search before creating issues; do not silently continue on a broken duplicate guard.
2. Inspect existing labels in the repo and reuse the closest category/priority labels.
3. If the feature touches an existing initiative, reference the parent/related issue numbers in the body.
4. If an existing open issue already substantially covers the requested feature, prefer updating that issue instead of creating a duplicate. Add a clarifying comment to expand scope, adjust labels if needed, and link any companion cadence/governance issue rather than opening a second overlapping feature ticket.
5. Prefer writing the body to a temp markdown file and using `--body-file` for long, structured issue descriptions.
6. If you are creating a linked issue tree (parent + children), render any placeholders like `<PARENT_ISSUE>` / `<QUEUE_ISSUE>` into temporary files before calling `gh issue create`. Do not rely on post-hoc mental substitution.
7. After creation or update, immediately verify the final artifact's title, labels, URL, and rendered body.
8. If GitHub issue access is blocked (for example, private repo token lacks `repository.issues` and `gh issue list/create` returns `GraphQL: Resource not accessible by personal access token`), do not stop with only a verbal plan. Preserve the work in a durable issue packet plus an executable creation script:
   - write a repo-routed markdown packet containing every issue title, target repo, labels, body, and acceptance check;
   - write a `scripts/create-...-issues.sh` helper using `gh issue create --repo <owner/repo> --body-file ...`;
   - use only labels you have verified exist, or fall back to broadly available labels such as `enhancement` / `documentation` when label access cannot be audited;
   - run `bash -n` on the helper and count expected issue entries versus `create_issue` calls;
   - report the exact GitHub access blocker and the command to run after access is fixed.
9. When the issue work also commits plan/report artifacts, verify both local and remote repository state before claiming closeout: pushed `HEAD`, local `origin/main`, remote `refs/heads/main`, ahead/behind count, and tracked worktree cleanliness. Do not treat a local commit hash alone as enough evidence.
9. If push emits GitHub-side ref-lock/cannot-lock-ref noise during closeout, do not assume success or failure from the warning. Re-query remote and tracking refs; only call it benign when `HEAD == origin/<branch> == remote refs/heads/<branch>` and ahead/behind is `0 0`.
10. If ending a session with a linked issue tree, produce a restart-safe closeout: issue states/gate labels, artifact paths, validation results, pushed commits, remote-ref sync evidence, and preserved unrelated worktrees. See `references/issue-tree-exit-closeout.md`.
11. If you accidentally create an issue with unresolved placeholders, fix it immediately with `gh issue edit --body-file ...` and then re-verify the rendered body.
12. For layered architecture/governance issue trees, see `references/layered-architecture-review-issue-tree.md`; it includes parent/child issue structure, data/execution/report layer scope, and the rule that output/report residency must mirror input/data residency unless an explicit promotion gate says otherwise.
13. When researching a user-referenced incident from another chat/channel, distinguish the observed runtime/chat failure from adjacent GitHub asset/workflow issues. Use `references/incident-to-issue-evidence-research.md` to search session history, inspect candidate issue bodies/comments, extract evidence, and explicitly report any gap where no direct issue exists.
14. Before closing layered architecture contract implementation issues, run the closeout checks in `references/layered-architecture-contract-closeout.md`; in particular, schema readiness gates must reject placeholder checksums and any unresolved adversarial `MAJOR` blocks commit/close.
14. For per-machine repository placement decisions, create one decision issue per machine in the user's requested order and do not perform repo moves/deletes/sync changes inside issue creation. Use `references/machine-repo-placement-decision-issues.md` for the reusable issue body shape and verification checklist. Keep delegation/dispatch strategy independent from repo placement unless a separate approved delegation plan explicitly requires otherwise; repo placement should be justified by locality, canonical source of truth, storage footprint, sync/backup risk, licensed tooling, and machine role. When the first machine issue establishes the baseline, include a completion note/acceptance criterion that the story leaves a reusable pattern for consistent tier-1 repo folder structure, methodical primary/reference placement decisions, and repo harness/file ecosystem handling through a single repo-tracked authority.
15. For revisions to completed/closed work, prefer a new open revision issue with a parent link-back comment when the closed issue should remain the baseline trace. Use `references/closed-issue-revision-thread.md` for the body shape and verification checklist.

Example:

```bash
# 1) Search for nearby issues first
gh issue list --limit 50 --search "llm-wiki OR document intelligence OR resource intelligence OR standards"

# 2) Inspect repo labels
gh label list

# 3) Draft structured body in a file
cat > /tmp/feature-issue.md <<'EOF'
## Summary
<feature summary>

## Why
<why now>

## Scope
- <item>
- <item>

## Deliverables
- <artifact>
- <artifact>

## Related
- Parent: #123
- Related: #456
EOF

# 4) Create with explicit labels
gh issue create \
  --title "feat(area): concise issue title" \
  --body-file /tmp/feature-issue.md \
  --label enhancement \
  --label priority:medium

# 5) Verify the final artifact
gh issue view <new-number> --json number,title,url,labels,body
```

**With gh:**

```bash
gh issue create \
  --title "Login redirect ignores ?next= parameter" \
  --body "## Description
After logging in, users always land on /dashboard.

## Steps to Reproduce
1. Navigate to /settings while logged out
2. Get redirected to /login?next=/settings
3. Log in
4. Actual: redirected to /dashboard (should go to /settings)

## Expected Behavior
Respect the ?next= query parameter." \
  --label "bug,backend" \
  --assignee "username"
```

**With curl:**

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues \
  -d '{
    "title": "Login redirect ignores ?next= parameter",
    "body": "## Description\nAfter logging in, users always land on /dashboard.\n\n## Steps to Reproduce\n1. Navigate to /settings while logged out\n2. Get redirected to /login?next=/settings\n3. Log in\n4. Actual: redirected to /dashboard\n\n## Expected Behavior\nRespect the ?next= query parameter.",
    "labels": ["bug", "backend"],
    "assignees": ["username"]
  }'
```

### Bug Report Template

```
## Bug Description
<What's happening>

## Steps to Reproduce
1. <step>
2. <step>

## Expected Behavior
<What should happen>

## Actual Behavior
<What actually happens>

## Environment
- OS: <os>
- Version: <version>
```

### Feature Request Template

```
## Feature Description
<What you want>

## Motivation
<Why this would be useful>

## Proposed Solution
<How it could work>

## Alternatives Considered
<Other approaches>
```

## 3. Managing Issues

### Plan-review closeout for gated work

When an issue-scoped plan has been written and adversarial-reviewed, close the planning gate transactionally before reporting success:

1. Commit and push the plan plus durable review artifacts first.
2. Post a GitHub issue comment with plan path, review artifact paths, verdict summary, validation commands, and pushed commit hash.
3. Move labels from the planning intake state to `status:plan-review`.
4. Re-query the issue and verify the expected label and comment URL.
5. State that labels record visibility; task/standing authority authorizes implementation without separate approval, after review and required domain decisions. Preserve planning-only scope limits.

If adversarial reviewers return `MAJOR` findings but the user explicitly asked to post/re-post the plans for their review, it is still valid to label the issues `status:plan-review` after the reviews complete. Do not soften the verdicts. The issue comment and plan summary must say that the plans have unresolved blocking findings or domain decisions. Stop affected implementation until those are resolved; task/standing authority covers subsequent implementation without a separate plan-approval step.

For multi-issue re-review batches, use one consistent issue comment shape across all issues: review command/date, provider list, per-provider artifact paths and verdicts, consolidated disagreement artifact, gate state, and pushed commit hash. This makes the user-review queue scannable and prevents one issue from silently drifting from the others.

Use `--body-file` for the comment body so paths, backticks, and verdict tables do not trigger shell quoting issues.

### Removing a child issue from an active issue tree

When the user removes a machine/workstream/deliverable from scope, do not only close the child issue. Keep the parent and child synchronized:

1. Update the parent issue body first: remove the child from the active checklist and add an explicit `Out of scope / removed` note preserving the child issue number and rationale.
2. Post a child closeout comment before closing, using the race-safe pattern: result, user direction/evidence, actions taken, residual scope, and how to reintroduce the work later.
3. Close the child with `--reason "not planned"`.
4. Replace planning labels with terminal labels where the repo taxonomy supports it, e.g. remove `status:needs-plan`, add `dispatch:done` or `wontfix`.
5. Comment on the parent with a concise scope-update note.
6. Verify both sides: child `stateReason: NOT_PLANNED`, closeout comment present, parent active checklist no longer includes the child, and parent body preserves the out-of-scope rationale.

See `references/issue-tree-scope-removal.md` for reusable comment templates and verification criteria.

### User approval reconciliation for gated plans

When the user explicitly approves a `status:plan-review` issue but includes correction notes, treat approval as a reconciliation transaction, not a bare label flip:

1. Update the plan artifact first so the user's corrections are durable in the implementation contract.
2. Commit and push the plan update before changing gate labels.
3. Post an issue comment recording the exact approval notes, plan path, and commit hash.
4. Preserve the verified owner approval event as history; do not self-label `status:plan-approved`. No approval-label transition is required for implementation.
5. Re-query the issue and verify title, URL, open state, and final labels before reporting success.
6. Keep the user-correction notes scoped to the implementation plan; do not silently mutate repository layout, move data, or delete aliases unless the approved plan explicitly includes that execution step.

Owner-controlled approval records remain authentic history. Agents never self-label `status:plan-approved`; reviewer APPROVE resolves review findings but grants no new task authority.

### Add/Remove Labels

**With gh:**

```bash
gh issue edit 42 --add-label "priority:high,bug"
gh issue edit 42 --remove-label "needs-triage"
```

**With curl:**

```bash
# Add labels
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42/labels \
  -d '{"labels": ["priority:high", "bug"]}'

# Remove a label
curl -s -X DELETE \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42/labels/needs-triage

# List available labels in the repo
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/labels \
  | python3 -c "
import sys, json
for l in json.load(sys.stdin):
    print(f\"  {l['name']:30}  {l.get('description', '')}\")"
```

### Assignment

**With gh:**

```bash
gh issue edit 42 --add-assignee username
gh issue edit 42 --add-assignee @me
```

**With curl:**

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42/assignees \
  -d '{"assignees": ["username"]}'
```

### Commenting

#### Interactive clarification threads

When an issue is being used as a live review/clarification thread, keep the GitHub discussion actionable and correction-friendly:

1. Post user corrections back to the issue as concise decision bullets, not as a long narrative.
2. When the user asks for unresolved blockers, post one consolidated comment with only the open confirmations/blockers; do not mix in already-settled decisions except as short context.
3. End interpretation comments with an explicit correction invitation, e.g. "Please correct if any part of this interpretation is wrong."
4. Prefer issue comments for engineering review clarifications so the user can edit/respond inline and the implementation plan has a durable trace.
5. Separate defaults from ranges/comparison cases. Example: "default = 3.08 kn; plots may show 0–4 kn; 4 kn is range upper bound, not default."

**With gh:**

```bash
gh issue comment 42 --body "Investigated — root cause is in auth middleware. Working on a fix."
```

For multiline comments or bodies containing backticks / code spans, prefer a body file to avoid shell command-substitution and quoting problems:

```bash
cat > /tmp/issue-comment.md <<'EOF'
Quick triage update:

- `scheduler_config.yml` is missing the job entry
- recommend adding test coverage for registration/config loading
EOF

gh issue comment 42 --body-file /tmp/issue-comment.md
```

If `gh issue comment` returns a transient GitHub 5xx/504 timeout, treat success as unknown rather than blindly resubmitting. First query recent comments for a unique marker from the body; only retry if the marker is absent.

```bash
MARKER='unique marker from your comment'
if ! gh issue view 42 --comments --json comments --jq '.comments[-10:][].body' | grep -F "$MARKER" >/dev/null; then
  gh issue comment 42 --body-file /tmp/issue-comment.md
fi
```

**With curl:**

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42/comments \
  -d '{"body": "Investigated — root cause is in auth middleware. Working on a fix."}'
```

### Closing and Reopening

**With gh:**

```bash
gh issue close 42
gh issue close 42 --reason "not planned"
gh issue reopen 42
```

**With curl:**

```bash
# Close
curl -s -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42 \
  -d '{"state": "closed", "state_reason": "completed"}'

# Reopen
curl -s -X PATCH \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/42 \
  -d '{"state": "open"}'
```

### Linking Issues to PRs

Issues are automatically closed when a PR merges with the right keywords in the body:

```
Closes #42
Fixes #42
Resolves #42
```

To create a branch from an issue:

**With gh:**

```bash
gh issue develop 42 --checkout
```

**With git (manual equivalent):**

```bash
git checkout main && git pull origin main
git checkout -b fix/issue-42-login-redirect
```

## 4. Issue Triage Workflow

When asked to triage issues:

1. **List untriaged issues:**

```bash
# With gh
gh issue list --label "needs-triage" --state open

# With curl
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/issues?labels=needs-triage&state=open" \
  | python3 -c "
import sys, json
for i in json.load(sys.stdin):
    if 'pull_request' not in i:
        print(f\"#{i['number']}  {i['title']}\")"
```

2. **Read and categorize** each issue (view details, understand the bug/feature)

3. **Apply labels and priority** (see Managing Issues above)

4. **Assign** if the owner is clear

5. **Comment with triage notes** if needed

## 5. Bulk Operations

For batch operations, combine API calls with shell scripting:

**With gh:**

```bash
# Close all issues with a specific label
gh issue list --label "wontfix" --json number --jq '.[].number' | \
  xargs -I {} gh issue close {} --reason "not planned"
```

**With curl:**

```bash
# List issue numbers with a label, then close each
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/$OWNER/$REPO/issues?labels=wontfix&state=open" \
  | python3 -c "import sys,json; [print(i['number']) for i in json.load(sys.stdin)]" \
  | while read num; do
    curl -s -X PATCH \
      -H "Authorization: token $GITHUB_TOKEN" \
      https://api.github.com/repos/$OWNER/$REPO/issues/$num \
      -d '{"state": "closed", "state_reason": "not_planned"}'
    echo "Closed #$num"
  done
```

## Quick Reference Table

| Action | gh | curl endpoint |
|--------|-----|--------------|
| List issues | `gh issue list` | `GET /repos/{o}/{r}/issues` |
| View issue | `gh issue view N` | `GET /repos/{o}/{r}/issues/N` |
| Create issue | `gh issue create ...` | `POST /repos/{o}/{r}/issues` |
| Add labels | `gh issue edit N --add-label ...` | `POST /repos/{o}/{r}/issues/N/labels` |
| Assign | `gh issue edit N --add-assignee ...` | `POST /repos/{o}/{r}/issues/N/assignees` |
| Comment | `gh issue comment N --body ...` | `POST /repos/{o}/{r}/issues/N/comments` |
| Close | `gh issue close N` | `PATCH /repos/{o}/{r}/issues/N` |
| Search | `gh issue list --search "..."` | `GET /search/issues?q=...` |
