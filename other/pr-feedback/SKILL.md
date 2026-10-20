---
name: pr-feedback
description: Address and resolve PR review feedback — find threads, classify findings, fix or reply, resolve threads via GitHub GraphQL, and know when NOT to re-request review.
---

# PR Feedback — Address & Resolve

Playbook for the `pr_review` phase (and any post-PR-creation feedback loop). Covers the exact mechanics learned on real frndOS PRs: how to find every thread, classify each finding, apply fixes, reply, and formally resolve — plus the traps (no REST resolve API, reply-vs-overwrite, don't-trigger-re-review).

## When to use

- Owner/bot posted review comments on an open PR (`pr_review` phase: poll, classify, fix, resolve, loop).
- User says "address PR feedback", "resolve all threads", or PR shows `CHANGES_REQUESTED`.

## Workflow

### Step 1 — Inventory feedback

```bash
# PR-level comments (challenge/overview comments)
gh pr view <n> --repo <owner/repo> --json comments,reviews,reviewDecision \
  -q '{decision: .reviewDecision, comments: [.comments[] | {author: .author.login, body: .body}]}'

# Inline review threads (the code-level findings)
gh api repos/<owner/repo>/pulls/<n>/comments \
  --jq '.[] | {id: .id, path: .path, line: .line, body: .body[0:200]}'

# Formal thread state (resolved/outdated) — GraphQL ONLY, no REST equivalent
gh api graphql -f query='query { repository(owner:"O", name:"R") { pullRequest(number:N) {
  reviewThreads(first:50) { nodes { id isResolved isOutdated comments(first:1) { nodes { body } } } } } } }'
```

Check every service PR in the feature — `pr_urls` in `.workflow-state.json` lists them (api, web, ai-service, data-service).

### Step 2 — Classify each thread

| Class | Action |
|---|---|
| must-fix (security, data-loss, crash path, wrong behavior) | Fix code, push, reply, resolve |
| nit / style / low | Fix if cheap, else reply with rationale + resolve |
| question / design concern | Reply with decision + rationale; fix only if it changes the decision |
| already-correct claim (reviewer misread) | Reply with the fact (e.g. "social-listening IS in the 7 tabs"), resolve |

For each finding reply with the SPECIFIC fix, not "done". Template: `Fixed: <what changed> — <why>. Verified: <how>`.

### Step 3 — Fix code

1. Apply fixes on the feature branch.
2. Verify locally: lint the changed files, re-run the affected command, confirm the guard/behavior both directions (e.g. prod-block exits non-zero AND local passes).
3. Commit with `fix(<scope>): PR review — <summary>`, push.

Gotchas that bit us before:

- **Env guard fail-open:** `env('APP_ENV', '')` passes when APP_ENV is unset. Fail closed: `getenv('APP_ENV') ?: config('app.env', 'production')`, and treat empty string as production (`?: 'production'`). Raw `env('APP_ENV')` is NULL when APP_ENV lives only in `.env` — config fallback keeps local runs working.
- **Idempotent seeding on refresh:** `updateOrCreate` overwrites existing rows' real ids (e.g. `fivetran_connection_id`). Use `firstOrNew` + set demo ids only when `!$row->exists`.
- **Async CH mutations:** `ALTER … DELETE` is async; it can execute AFTER the follow-up INSERT and reap fresh rows. Wait for mutations (scoped to your tables via `system.mutations WHERE database/table`) before inserting.
- **Unique-constraint collisions:** core+extended rows sharing `(brand, platform, connection_index)` — extended must take `max+1` and reuse existing rows by their real identity column.

### Step 4 — Reply + resolve

GitHub has **no REST endpoint to resolve threads** — only the `resolveReviewThread` GraphQL mutation:

```bash
# reply on a thread (or PATCH body — see trap below)
gh api -X PATCH repos/<owner/repo>/pulls/comments/<comment-id> \
  -f body="Fixed: <what> — <why>. Verified: <how>."

# resolve every unresolved thread
for tid in $(gh api graphql -f query='query{repository(owner:"O",name:"R"){pullRequest(number:N){reviewThreads(first:50){nodes{id isResolved}}}}}' \
  --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved==false) | .id'); do
  gh api graphql -f query="mutation{resolveReviewThread(input:{threadId:\"$tid\"}){thread{isResolved}}}"
done
```

Reply to PR-level comments too: `gh api repos/<owner/repo>/issues/<n>/comments -f body="..."` (PR comments live under the issues endpoint).

### Step 5 — Re-review policy

**Do NOT re-request review unless the user explicitly says so.** Default: fix, reply, resolve, then stop. The owner/bot re-reviews on their own schedule. (`request-reviewers` / re-request is only for when the user asks.)

## Traps (all hit in real sessions)

- `PATCH /pulls/comments/{id}` **overwrites** the comment body — the bot's original finding text is lost (author attribution stays the bot's). Prefer a reply comment (`POST /pulls/{n}/comments` with `in_reply_to`) when you want history preserved; PATCH is fine when the final word per thread is enough.
- `isResolved` only exists in GraphQL `reviewThreads`; REST `gh pr view` cannot show it.
- Shell quoting: GraphQL mutation strings with `$tid` inside double quotes — use single-quoted heredoc-free one-liners or a script file.
- `sed` with `/` in replacement text breaks — use `|` delimiters or avoid sed for such patches.
- Threads on a push that changed the diff become `isOutdated: true` — still resolve them explicitly; outdated ≠ resolved.

## Verification checklist (before declaring done)

- [ ] Every thread: fixed or replied with rationale.
- [ ] Every thread: `isResolved == true` (GraphQL check).
- [ ] PR-level comments answered.
- [ ] Fixes verified locally (both guard directions, idempotent re-run).
- [ ] No re-review requested (unless user said so).
- [ ] Track file updated with the review round + fixes.

## References

- Phase machine: `.agents/skills/workflow/SKILL.md` — `pr_review` is run by the orchestrator, which loads this skill for the mechanics
- Security audit before opening PRs: the external `security-reviewer` skill (`npx skills add https://github.com/jeffallan/claude-skills --skill security-reviewer`), run during `pr_submission`, not here
- Commit conventions: `AGENTS.md` → "Commit Messages"
