---
name: pull
description: Pull request and merge request management. Use when user asks to view PR/MR comments, review feedback, iterate on changes, manage remote branches, or work with GitHub/GitLab pull requests.
---
<!-- @agent-architect owns this file. Delegate changes, don't edit directly. -->

<announcement>
"I'm using the pull skill to manage PR/MR feedback and iteration."
</announcement>

<pr_discovery>
Get PR details: gh pr view [number] --json number,title,state,body,reviewDecision,reviews,comments
List open PRs: gh pr list --json number,title,author,reviewDecision
Current branch PR: gh pr view --json number,title,state,reviewDecision
</pr_discovery>

<fetching_comments>
All PR comments (review + general): gh api repos/{owner}/{repo}/pulls/{number}/comments --jq '.[] | {path, line, body, user: .user.login, created: .created_at}'
General PR comments: gh api repos/{owner}/{repo}/issues/{number}/comments --jq '.[] | {body, user: .user.login, created: .created_at}'
Review summaries: gh pr view [number] --json reviews --jq '.reviews[] | {author: .author.login, state, body}'
Pending review threads: gh api repos/{owner}/{repo}/pulls/{number}/comments --jq '[.[] | select(.in_reply_to_id == null)] | group_by(.path) | .[] | {file: .[0].path, comments: [.[] | {line, body, user: .user.login}]}'
</fetching_comments>

<understanding_feedback>
Categorize comments: blocking (request changes), suggestions (nice-to-have), questions (need response), nits (style/minor). Prioritize blocking comments. Identify patterns across multiple comments. Note which reviewer made each comment for context.
</understanding_feedback>

<iteration_workflow>
1. Fetch all comments and reviews for the PR
2. Group by file and categorize by severity
3. Address blocking comments first
4. For each change: make edit, verify it works, commit with reference to feedback
5. Respond to questions in PR if needed
6. Push changes and request re-review if appropriate
</iteration_workflow>

<commit_messages>
Reference the feedback: fix(component): address review - use const instead of let
For multiple items: fix: address PR feedback - use consistent naming, add error handling, remove dead code
</commit_messages>

<responding_to_comments>
Reply to comment: gh api repos/{owner}/{repo}/pulls/{number}/comments/{comment_id}/replies -f body="Done in [commit]"
Resolve thread: gh api graphql -f query='mutation { resolveReviewThread(input: {threadId: "PRRT_xxx"}) { thread { isResolved } } }'
Get thread IDs: gh api graphql -f query='query { repository(owner: "{owner}", name: "{repo}") { pullRequest(number: {number}) { reviewThreads(first: 50) { nodes { id isResolved comments(first: 1) { nodes { body } } } } } } }'
General reply: gh pr comment [number] --body "Addressed feedback in latest commits"
</responding_to_comments>

<checking_ci>
CI status: gh pr checks [number]
Wait for CI: gh pr checks [number] --watch
Failed check details: gh run view [run_id] --log-failed
</checking_ci>

<requesting_re_review>
After addressing feedback: gh pr edit [number] --add-reviewer [username]
Or comment: gh pr comment [number] --body "@reviewer Ready for another look"
</requesting_re_review>

<owner_repo_detection>
Get from current repo: gh repo view --json owner,name --jq '"\(.owner.login)/\(.name)"'
Or parse from remote: git remote get-url origin | sed 's/.*github.com[:/]\(.*\)\.git/\1/'
</owner_repo_detection>

<red_flags>
Never dismiss reviews without addressing concerns. Always verify CI passes before requesting re-review. Don't mark conversations resolved without actually fixing the issue.
</red_flags>
