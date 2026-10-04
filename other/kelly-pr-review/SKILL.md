---
name: kelly-pr-review
description: GitHub pull request review desk (Busabase App-in-Skill) using the gh CLI for real GitHub access, an AirApp review UI for human approval, and a trusted gh pr review execution step. Use when the user invokes /kelly-pr-review or $kelly-pr-review, asks to review GitHub PRs, generate a PR review batch, approve/comment/request changes through the review UI, or execute approved GitHub reviews.
metadata:
  category: platform
  tags:
    - risk:gated-write
    - surface:busabase
    - surface:github
  busabase:
    template: true
    folderSlug: kelly-pr-review
    resources:
      - reviews
      - settings
    risk: gated-write

---

# Kelly PR Review

## App UI Screenshots

<table>
  <tr>
    <td width="50%"><img src="assets/screenshots/overview.webp" alt="Kelly PR Review overview"></td>
    <td width="50%"><img src="assets/screenshots/needs-review.webp" alt="Kelly PR Review needs review"></td>
  </tr>
  <tr>
    <td><strong>Overview</strong><br>Pull request review desk with repository filters, status counts, and reviewer configuration.</td>
    <td><strong>Needs review</strong><br>Pull request review with findings, risk signals, review body, and suggested actions.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/ready.webp" alt="Kelly PR Review ready to approve"></td>
    <td width="50%"><img src="assets/screenshots/blocked-security.webp" alt="Kelly PR Review blocked review"></td>
  </tr>
  <tr>
    <td><strong>Ready to approve</strong><br>Approval-focused review where checks pass and the final recommendation is ready to send.</td>
    <td><strong>Blocked review</strong><br>Security-sensitive PR scenario with unresolved risk, blocking rationale, and reviewer handoff details.</td>
  </tr>
  <tr>
    <td width="50%"><img src="assets/screenshots/needs-test.webp" alt="Kelly PR Review merged PR needs test"></td>
    <td width="50%"><img src="assets/screenshots/tested.webp" alt="Kelly PR Review tested verification"></td>
  </tr>
  <tr>
    <td><strong>Needs test</strong><br>Merged pull request waiting for human verification with a required test note or evidence link.</td>
    <td><strong>Tested</strong><br>Post-merge verification record showing the test note that proves a human checked the change.</td>
  </tr>
</table>

## Overview

Use this skill as a GitHub pull request review desk backed by the `gh` CLI
and Busabase. `scripts/generate_review_batch.mjs` gathers PRs with `gh`,
scores risk, proposes a review action, and writes the resulting queue into
Busabase; the AirApp shows it for human approval (approve / comment /
request changes / block / needs_review); `scripts/execute_decisions.mjs`
later submits only approved decisions with the real `gh pr review` command.

Default behavior is AirApp-first. Unless the user explicitly asks only for
explanation, generate or refresh the batch and give the user the clickable
AirApp URL (or the local preview URL when local preview is explicitly
requested). Use chat-only mode only when the user says "纯聊天", "chat only",
"不要打开 UI", or similar.

**The AirApp itself never calls GitHub.** It reads and writes Busabase
records only — no merge, close, comment, review submission, or repository
mutation happens from the browser. Both `gh` CLI directions (reading PRs in,
submitting approved reviews out) are genuinely trusted-process-only, since a
browser cannot invoke a local CLI: `scripts/generate_review_batch.mjs`
ingests PR data via `gh` into Busabase, and `scripts/execute_decisions.mjs`
is the one place that actually calls `gh pr review` for an approved item.

## Mandatory Dependencies

1. Read and follow `$kelly-app-skill-creator` for product behavior, visual
   quality, responsive layout, and the complete canonical `content/kelly-pr-review-app/` artifact.
2. Read and follow `$busabase` for connection, target Space, node discovery,
   ChangeRequests, review, and merge behavior.
3. Read and follow `$busabase-app-creator` for resource modeling, AirApp
   runtime limits, security, validation, and deployment.

If a dependency is unavailable, preserve this skill's local artifact and
product contracts, stop before the unavailable Busabase operation, and
report the exact missing dependency. Do not invent a second data backend.

## Private Configuration

Private config is optional and consumed only by the trusted scripts (never
by the AirApp browser). By default `scripts/generate_review_batch.mjs` uses
the current `gh` authenticated account and searches open PRs requesting
`@me` across accessible repositories. Use private config only for repo
filters, reviewers, default review policy, and risk rules. Do not hardcode
personal repositories or tokens into committed files.

Config priority:

1. `KELLY_PR_REVIEW_CONFIG=/absolute/path/to/config.json`
2. `skills/kelly-pr-review/config.local.json`
3. `~/.config/kelly-pr-review/config.json`
4. gh defaults (no config found)

Env priority:

1. Existing system environment variables
2. `KELLY_PR_REVIEW_ENV_FILE=/absolute/path/to/.env`
3. repository root `.env`
4. `skills/kelly-pr-review/.env.local`
5. `~/.config/kelly-pr-review/.env`

Secrets should live in env files only. Usually `gh auth login` is enough, so
this skill does not require a token in config. The resolved config is also
written to Busabase's `kelly-pr-review-profile` settings row (see
`references/ui-schema.md`) so the AirApp can display it — the AirApp never
writes that row itself.

## Busabase Resources

Two Bases under one application Folder (`kelly-pr-review`), declared in
`content/kelly-pr-review-app/app/js/config.js` and the generated template sidecars under `content/`:

- `reviews`: the pull request review queue — GitHub PR metadata, risk,
  proposed action, workflow `status`, editable `review-body`, the human
  verdict fields (`decision-action`/`decision-note`/`decided-at`), execution
  result (`execution-status`/`execution-detail`), and post-merge test
  verification (`tested`/`test-note`/`test-evidence`).
- `settings`: one row per `kind` — `kelly-pr-review-profile` (reviewer,
  repos, query, review policy, style, written only by
  `scripts/generate_review_batch.mjs --apply`) and `kelly-pr-review-lock`.

Resources provision lazily through an idempotent Busabase ChangeRequest the
first time the app runs in a Space; see `references/ui-schema.md` for exact
field shapes. Workflow-status bucketing and the review-ref numbering are
computed client-side from the `reviews` Base on every read — they are never
stored.

## Workflow

1. Check `gh auth status`. If not authenticated, stop and ask the user to
   authenticate with `gh auth login`.
2. Run `node scripts/generate_review_batch.mjs --apply` to gather PRs with
   `gh` and write/refresh the review queue in Busabase. Use `--sample`
   instead of a real `gh` read only when the user explicitly wants to
   preview the UI with fake data. Omit `--apply` to see a dry-run preview
   first.
3. Classify status (assigned by the generator, refined by the human in the
   UI):
   - `needs_review`: user or agent needs to inspect before deciding.
   - `to_approve`: agent proposes a concrete review action.
   - `approved`: user approved an action in the UI.
   - `done`: review action already executed or intentionally no-op.
   - `blocked`: missing access, too risky, failing preconditions, or too
     large to review safely.
4. Give the user the AirApp URL (or local preview URL) to review the queue.
5. For an item moved to a different status by the human, no re-drafting is
   needed here — the agent may still edit `review-body` before the next
   decision if asked.
6. On "execute" / "submit approved reviews": run
   `node scripts/execute_decisions.mjs --apply` to re-read approved items
   from Busabase and submit the real `gh pr review` call for each, one item
   at a time. Omit `--apply` first to see the dry-run command list.

## Review Actions

Supported approved actions, submitted by `scripts/execute_decisions.mjs`:

- `approve`: `gh pr review <number> --approve --body-file <tmp>`
- `comment`: `gh pr review <number> --comment --body-file <tmp>`
- `request_changes`: `gh pr review <number> --request-changes --body-file <tmp>`
- `no_action`: write execution detail only; no GitHub call.
- `needs_review` or `block`: never execute (status stays out of `approved`).

Never merge, close, push, edit branches, rerun workflows, or dismiss
reviews from this skill.

## Safety Rules

- Require explicit AirApp (or chat) approval — writing `status: "approved"`
  onto a review record — before any `gh pr review` call.
- `scripts/execute_decisions.mjs` re-reads each record immediately before
  executing it, so a revoked approval or an already-executed item is never
  submitted to GitHub twice.
- Keep review bodies human-editable in the UI and quote only necessary
  source excerpts.
- Mark security, auth, billing, schema migration, destructive data,
  generated-code-heavy, and large-diff PRs as risky.
- If the review confidence is low, propose `comment` or `needs_review`, not
  approval.
- Treat GitHub tokens and Busabase credentials as secrets; never commit
  them. The trusted scripts read `BUSABASE_BASE_URL`/`BUSABASE_API_KEY`/
  `BUSABASE_SPACE_ID` from the environment, never the AirApp's session.

## Useful Commands

```bash
node skills/kelly-pr-review/scripts/generate_review_batch.mjs --apply
node skills/kelly-pr-review/scripts/generate_review_batch.mjs --sample
node skills/kelly-pr-review/scripts/execute_decisions.mjs
node skills/kelly-pr-review/scripts/execute_decisions.mjs --apply
pnpm --dir skills/kelly-pr-review/content/kelly-pr-review-app dev
```

In normal use, invoke `/kelly-pr-review`, let the skill generate/refresh the
batch, and open the AirApp.
