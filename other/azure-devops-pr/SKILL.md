---
name: azure-devops-pr
description: Use when working with an Azure DevOps pull request - creating or opening one, fetching PR details, reading review threads, implementing requested changes, or replying to comments. Auto-discovers the PR from the current Git branch. Also use when reaching the Azure DevOps API is itself the problem - an HTML sign-in page or HTTP 203 where JSON was expected, a jq parse error against dev.azure.com, 401/403, VS403403, TF400813/TF401019, an anonymous authenticatedUser, a PAT rejected as a bearer token, or a missing credential in a sandbox.
---

# Azure DevOps Pull Request

## Overview

Reference for interacting with Azure DevOps PRs via the REST API v7.0 — creating them, and working through their review.

Two things drive most wrong conclusions:

- **Azure DevOps does not answer unauthenticated calls with 401.** It answers with a sign-in page and HTTP 200 or 203. An unauthenticated session therefore looks like a parsing bug, not an auth failure.
- **Two auth schemes, not one.** A PAT goes in Basic auth; an Entra token goes in Bearer. Using the wrong one produces that same sign-in page.

## Workflow

0. **Establish access as a verified state, before touching the PR.** Access is a tuple — credential variable, auth scheme, base URL, routing identifiers — not just "a token." Resolve all of it in one bounded pass:

   ```bash
   SKILL_DIR=<directory containing this SKILL.md>
   source "$SKILL_DIR/ado-access.sh"
   ado_discover                     # org, project, repo, branch from the git remote
   ado_resolve                      # credential + scheme + base URL + identity probe
   ado_gate                         # active PR for this branch; sets ADO_PR_ID
   ```

   **Creating a PR?** `ado_gate` exits `3` (no active PR — access works). Stop here and follow [create-pr.md](create-pr.md).

   `ado_resolve` probes `/_apis/connectionData` and checks **who** came back — a 200 carrying an anonymous identity is a failure, not a success. **Until `ado_gate` prints a PR id, you do not have PR access** — except exit `3`, which proves access and means no PR is open yet. If any step fails, its error maps to exactly one corrective action in the decision table in [access.md](access.md). Take that action; do not try other credentials, headers, or api-versions. The one thing worth checking first is the base URL `ado_resolve` printed: if it is not a `dev.azure.com` host, something else answered and its error is not Azure DevOps' — see [access.md](access.md#the-base-url-is-part-of-the-diagnosis).

1. **Read the review** — `ado_threads`, then filter: `isDeleted != true` AND `status == "active"`.
2. **For each active thread** — read `comments[0].content`; if `threadContext` is present, open `filePath` at `rightFileStart.line`.
3. **Implement the change.** Always before step 4 — never mark a thread fixed on intent.
4. **Reply, then close** — `ado_reply <threadId> <comments[0].id> "<what you did>"`, then `ado_thread_status <threadId> fixed`.
5. **Confirm** — re-fetch threads; none should remain active.

Auth, discovery, and the error decision table: [access.md](access.md).

## Helper functions

All are defined by `ado-access.sh`. Review helpers need a passed gate; creation helpers need only `ado_resolve`.

| Call | Does |
|---|---|
| `ado_discover` | Parse org/project/repo/branch from `origin`. No network |
| `ado_resolve` | Pick credential, infer scheme, probe identity |
| `ado_gate [prId]` | Find the active PR for the branch, or adopt a given id. Exit `3` = none open |
| `ado_default_branch` | Repo default branch — the usual PR target |
| `ado_branch_pushed` | Remote branch exists and equals local HEAD |
| `ado_create_pr <target> <title> <descFile> [workItemId…]` | Create a **draft** PR, link work items, print the web link |
| `ado_publish_pr [prId]` | Draft → ready for review |
| `ado_web_url [prId]` | Browser link (the API's `url` is a REST link) |
| `ado_pr` | PR details |
| `ado_threads` | All comment threads |
| `ado_reply <threadId> <parentCommentId> <markdown>` | Reply in a thread |
| `ado_thread_status <threadId> <status>` | Set thread status |
| `ado_nono_route` | Show the nono credential route for dev.azure.com (diagnosis only) |
| `ado_api <METHOD> <path> [json]` | Anything else, project-scoped |

`ado_api` appends `api-version=7.0` unless the path already carries one and classifies every response before printing it. It sends its body verbatim — build JSON with `json.dumps`, as `ado_reply` and `ado_create_pr` do. Prefer it over hand-rolled `curl`: a raw `curl | jq` against dev.azure.com turns an auth failure into a parse error.

## API Reference

Base URL: `https://dev.azure.com/{org}/{project}/_apis` — the project segment is required for every git route.

The repository identifier in the path can be the repo **name** (from the remote URL) or the GUID `id` returned in any PR response.

---

### Find the PR for a branch

```
GET /git/repositories/{repo}/pullrequests
    ?searchCriteria.sourceRefName=refs/heads/{branch}
    &searchCriteria.status=active
    &api-version=7.0
```

Take `value[0].pullRequestId`. Empty `value` means no open PR for this branch — that is an answer, not an error.

---

### Create a PR

```
POST /git/repositories/{repo}/pullrequests?api-version=7.0

{
  "sourceRefName": "refs/heads/{branch}",
  "targetRefName": "refs/heads/{target}",
  "title": "…",
  "description": "… (max 4000 chars)",
  "isDraft": true,
  "workItemRefs": [{ "id": "1234" }]
}
```

Publish a draft: `PATCH /git/repositories/{repo}/pullrequests/{prId}` with `{ "isDraft": false }`. Templates are not applied by the API. Full workflow: [create-pr.md](create-pr.md).

---

### Get PR details

```
GET /git/repositories/{repo}/pullrequests/{prId}?api-version=7.0
```

| Field | Meaning |
|-------|---------|
| `pullRequestId` | numeric PR ID |
| `title` | PR title |
| `description` | PR body (markdown) |
| `status` | `active` / `completed` / `abandoned` |
| `sourceRefName` | source branch as `refs/heads/{branch}` |
| `targetRefName` | target branch |
| `reviewers[].vote` | `10` approved, `5` approved w/ suggestions, `0` no vote, `-5` waiting, `-10` rejected |
| `reviewers[].displayName` | reviewer name |

---

### List comment threads

```
GET /git/repositories/{repo}/pullrequests/{prId}/threads?api-version=7.0
```

Response: `{ "value": [ Thread, … ] }`

| Field | Meaning |
|-------|---------|
| `id` | thread ID |
| `status` | `active`, `fixed`, `wontFix`, `closed`, `byDesign`, `pending` |
| `isDeleted` | skip if `true` |
| `threadContext` | present for code comments (see below) |
| `comments[0]` | root comment (the original request or question) |
| `comments[0].id` | needed as `parentCommentId` when replying |
| `comments[0].content` | text of the comment (markdown) |
| `comments[0].author.displayName` | who wrote it |

Code comment location (`threadContext`):

| Field | Meaning |
|-------|---------|
| `filePath` | repo-relative path, e.g. `/src/foo.py` |
| `rightFileStart.line` | first line in the new file version |
| `rightFileEnd.line` | last line |

---

### Add a reply to a thread

```
POST /git/repositories/{repo}/pullrequests/{prId}/threads/{threadId}/comments?api-version=7.0

{
  "content": "Done — extracted the logic into `bar.py:42`.",
  "parentCommentId": {comments[0].id}
}
```

---

### Update thread status

```
PATCH /git/repositories/{repo}/pullrequests/{prId}/threads/{threadId}?api-version=7.0

{ "status": "fixed" }
```

Valid statuses: `active` · `fixed` · `wontFix` · `closed` · `byDesign` · `pending`

---

### Create a new thread (optional)

```
POST /git/repositories/{repo}/pullrequests/{prId}/threads?api-version=7.0

{
  "comments": [{ "parentCommentId": 0, "content": "Your comment here.", "commentType": 1 }],
  "status": "active"
}
```

Add `threadContext` to anchor the thread to a file/line.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Treating an HTML response or `jq` parse error as a tooling problem | It is an auth failure. Return to `ado_resolve` ([access.md](access.md)) |
| Sending a PAT as `Authorization: Bearer` | PATs use Basic auth with an empty username. `ado_resolve` infers this from the credential |
| Sending `AZURE_BEARER_TOKEN` to dev.azure.com | That is an ARM-audience token. Wrong audience; it will never work here |
| Treating `$AZURE_DEVOPS_EXT_PAT` as a PAT when it is byte-identical to `$NONO_PROXY_TOKEN` | It is a nono *phantom token*, not a PAT. It goes out as `Bearer`, not Basic — `ado_resolve` prints `nono phantom token` when it detects this ([access.md](access.md#proxy-injected-credentials--the-phantom-token-pattern)) |
| Sending no `Authorization` at all in a sandbox, expecting the proxy to supply it | The proxy replaces a *validated phantom*; it never conjures one. A missing header fails identically to a wrong one |
| Guessing why a credential variable is empty in a sandbox | Depends on the route's `credential_key` (`ado_nono_route`): a `cmd://` route is not active this session; any other key's secret failed to load. Report it; do not hand-send `$NONO_PROXY_TOKEN` |
| Reading a sandbox `503 CaptureFailed` as an outage | The host-side `cmd://` capture failed, usually an expired login (e.g. `az login`). The user fixes the login, you retry — no restart |
| Reading a sandbox `401` as a dead credential | Check the body's shape first: `typeKey`/`typeName` present = Azure DevOps answered, so the phantom was fine; a bare `{"error":"Unauthorized"}` = the proxy refused it |
| Using org-level base URL for git routes | Base must include the project: `.../dev.azure.com/{org}/{project}/_apis/...` |
| Branch ref without prefix | Use `refs/heads/{branch}`, not the bare branch name |
| Wrong `parentCommentId` | Must be `comments[0].id` (e.g. `1`), never `0` or `null` |
| Treating `ado_gate` exit `3` as a failure when creating a PR | It means access works and nothing is open — the expected state. Continue with [create-pr.md](create-pr.md) |
| Creating a PR without `isDraft`, or publishing without being asked | Always draft first; `ado_publish_pr` only on explicit approval |
| Showing the response's `url` as the PR link | That is a REST URL. Use `ado_web_url` |
| Expecting the PR template to be applied on create | Only the web UI applies it. Fill it into the description yourself |
| Marking a thread fixed before implementing | Implement first, then set status |
| Skipping `isDeleted: true` threads | Always filter them out — they are not actionable |
| Running `az repos` inside the sandbox | `~/.azure` is not writable; the CLI dies before parsing. Use the REST helpers |
