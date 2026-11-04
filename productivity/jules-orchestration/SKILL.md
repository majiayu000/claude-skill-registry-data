---
name: jules-orchestration
description: Dispatch and manage Google Jules coding sessions via the Jules REST API using the JULES_API_KEY environment variable — without an interactive `jules login`. Use when the user wants to offload a scoped task to Jules, orchestrate Jules, or review/open Jules sessions. Note the API key auth (x-goog-api-key header), session lifecycle, AUTO_CREATE_PR, and the always-review-before-merge rule (Jules has clobbered external fixes by rebasing from a stale view).
---

# Jules REST API Orchestration

Google Jules is an async coding agent with a REST API. With `JULES_API_KEY` in the
environment you can dispatch, monitor, and manage sessions entirely via curl — no
interactive `jules` CLI login needed (the `jules login` OAuth browser flow is
often the blocker; the API key short-circuits it).

A repo-local guide exists: `docs/guides/jules-rest-api.md` (nursultan-web).

> **Security**: never print the key value. Reference it as `$JULES_API_KEY`
> (a ~53-char key from https://jules.google.com/settings).

## When to use

Use when the user asks to run/offload a scoped task to Jules or review a
Jules session/PR. Ideal: a bounded, mechanical, test-only task you can review
— point Jules at the backlog entry / repo docs for setup notes.

## Base + auth — WORKING (verified)

```
BASE=https://jules.googleapis.com/v1alpha
AUTH="x-goog-api-key: $JULES_API_KEY"
curl -H "$AUTH" "$BASE/sources?pageSize=50"          # connected GitHub repos
curl -H "$AUTH" "$BASE/sessions?pageSize=10"          # list sessions
curl -H "$AUTH" "$BASE/sessions/$ID"                  # get one session/state
```

`nursultan-web` and `belpolsim` are connected sources (checked 2026-08-05).

## Dispatch a task (auto-opens a PR)

```bash
curl -X POST -H "$AUTH" -H "Content-Type: application/json" \
  -d '{
    "prompt": "<precise task; read the relevant backlog entry for setup notes>",
    "title": "Short title (CODE-01)",
    "sourceContext": {
      "source": "sources/github/<owner>/<repo>",
      "githubRepoContext": { "startingBranch": "main" }
    },
    "automationMode": "AUTO_CREATE_PR",
    "requirePlanApproval": false
  }' \
  "$BASE/sessions"
```

Response has `name` = `sessions/<id>`.

## Lifecycle states

`QUEUED → PLANNING → AWAITING_PLAN_APPROVAL → IN_PROGRESS → COMPLETED | FAILED`
Also `PAUSED`, `AWAITING_USER_FEEDBACK`.

## Manage

```bash
curl -X POST -H "$AUTH" -H "Content-Type: application/json" \
  -d '{"prompt":"<follow-up>"}' "$BASE/sessions/$ID:sendMessage"
curl -X POST -H "$AUTH" -H "Content-Type: application/json" \
  -d '{}' "$BASE/sessions/$ID:approvePlan"    # only if requirePlanApproval=true
curl -X DELETE -H "$AUTH" "$BASE/sessions/$ID"  # abandon
```

## Operating rules — READ THIS BEFORE USE

- **One session → one PR → one issue/backlog item** for a single, scoped task;
  prefer test-only / mechanical work — architecture and concurrency-critical
  changes stay with a human reviewer.
- **Never auto-merge a Jules PR** — review the diff + CI first, as with any PR.
- **Clobber risk (Aug 2025 session):** Jules has reverted external fixes by
  REBUILDING from a stale view on its own PR (re-pushing and deleting fixes).
  If its head branch is actively moving, check it matches the current main
  before trusting it; consider rebuilding the change on a clean branch and
  closing the bot PR (pattern: #895 → #905) rather than fighting the bot.
- Do NOT dispatch a task the user or another agent is already doing in parallel
  (conflicting work on the same files).

## Known limitation (verified 2026-08-05, GOAL-01)

`sendMessage` does NOT transition a session out of `AWAITING_USER_FEEDBACK`.
The message is delivered (a `userMessaged` activity appears) and `updateTime`
advances, but the session stays in the feedback state and the agent does not
resume — there is NO documented `resume`/`provideFeedback` endpoint. If a
session needs user feedback, the sendMessage answers it only via the web UI
(jules.google) not the REST API. Work a stuck session has already done is held
in its (unreachable) VM: if the agent created a branch but did not push it, the
branch does NOT appear on the origin — the partial work is not recoverable
from the repo. Plan tasks so a session can run to COMPLETION without asking
the user questions (e.g. set "proceed unless <explicit blocker>" in the
prompt), or expect to finish the work yourself if it stalls.

## Reference

- Repo guide: `docs/guides/jules-rest-api.md`
- Session-notes doc: `$HOME/projects/belpolsim/docs/process/JULES.md` (label-triggered
  GitHub Actions usage; this skill covers the direct REST-API path).
- API docs: https://jules.google/docs/api/reference/overview