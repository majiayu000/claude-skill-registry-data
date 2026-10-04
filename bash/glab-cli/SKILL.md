---
name: glab-cli
description: >
  Drive the GitLab CLI (glab) to review a merge request — fetch the diff and
  context, post inline discussion comments anchored to specific diff lines
  (via a position object), open conceptual resolvable threads, and express a
  verdict with approve / revoke + a summary thread. Use when reviewing or
  commenting on a GitLab MR. Triggers on: glab, gitlab cli, merge request,
  mr review, post mr comment, glab api, review gitlab mr.
---

## glab CLI — MR review & commenting

Everything drives `glab` via the shell. `glab api` expands placeholders from
the current repo's git remote: `:fullpath` (URL-encoded project path),
`:id`, `:branch`, etc. Outside a repo, use a URL-encoded path
(`group%2Fsubgroup%2Fproject`). `glab api` has **no** `-R` flag.

> **Flag inversion vs `gh`/curl:** in `glab`, `-F`/`--field` = typed
> (bool/int/placeholder), `-f`/`--raw-field` = string. This is the OPPOSITE
> of `gh api`. And inline positioned comments need `--form` (see §3).

### 0. Auth check (do this first)
```bash
glab auth status            # exit 0 = authenticated; token needs `api` scope (read_api can't post/approve)
# self-managed: glab auth status --hostname gitlab.example.com
```

### 1. Resolve identifiers
Endpoints take the MR **iid** (the per-project `!123` number), never the
global id.
```bash
MR_IID=$(glab mr view --output json | jq -r '.iid')          # MR for the checked-out branch
# or by branch: glab api "projects/:fullpath/merge_requests?source_branch=$(git branch --show-current)&state=opened" | jq -r '.[0].iid'
AUTHOR=$(glab mr view "$MR_IID" --output json | jq -r '.author.username')
```

### 2. Fetch context (read-only)
```bash
glab mr view "$MR_IID" --output json     # metadata incl. diff_refs, sha, draft, state
glab mr diff "$MR_IID"                    # unified diff (the change to review)
# Per-file diffs with old_path/new_path + hunks — use to compute new_line/old_line:
glab api "projects/:fullpath/merge_requests/$MR_IID/diffs" --paginate

# Existing feedback — read before posting so you never duplicate a point:
glab api "projects/:fullpath/merge_requests/$MR_IID/discussions" --paginate
glab api "projects/:fullpath/merge_requests/$MR_IID/pipelines"            # CI status (latest first)
```
Linked Jira ticket: parse the MR title/description for the issue key, then
use the **`ticket`** skill (Jira MCP) or the `jira` CLI to read the
acceptance criteria.

### 3. Get the position SHAs (required for inline comments)
Inline (positioned) comments need `base_sha`, `start_sha`, `head_sha` from
the MR's `diff_refs`:
```bash
eval "$(glab api projects/:fullpath/merge_requests/$MR_IID \
  | jq -r '.diff_refs | "BASE_SHA=\(.base_sha) START_SHA=\(.start_sha) HEAD_SHA=\(.head_sha)"')"
```
> `diff_refs` is **empty right after MR creation** and fills in
> asynchronously. Poll until `.base_sha` is non-null before posting
> positioned comments, or you'll send empty SHAs and get a 400.

### 4. Post an inline (line-anchored) comment — MUST use `--form`
The `position` hash only decodes from real multipart fields. Use `--form`
for every part — **not** `-F`/`-f`/`--input` (with those, `position[...]`
keys are silently dropped and the comment becomes a non-inline note or 400s):
```bash
glab api -X POST "projects/:fullpath/merge_requests/$MR_IID/discussions" \
  --form "body=**🔴 CRITICAL — SQL injection.** userId is concatenated into the query; use a bound parameter." \
  --form "position[position_type]=text" \
  --form "position[base_sha]=$BASE_SHA" \
  --form "position[start_sha]=$START_SHA" \
  --form "position[head_sha]=$HEAD_SHA" \
  --form "position[new_path]=src/auth.rb" \
  --form "position[old_path]=src/auth.rb" \
  --form "position[new_line]=88"
```
**Required `position[*]` fields:**
- `position_type=text`
- `base_sha`, `start_sha`, `head_sha` (from §3)
- `new_path` **and** `old_path` — both required, even when unchanged; equal
  unless the file was renamed (`old_path` = pre-change, `new_path` = post).

**Line rule (wrong → 400 "Note {position} is invalid"):** `new_line`/`old_line`
are absolute 1-based **file** line numbers (not diff offsets):
- **Added** line (green, new file only) → set `new_line` only, omit `old_line`.
- **Deleted** line (red, old file only) → set `old_line` only, omit `new_line`.
- **Context** line (unchanged, in both) → set **both** `new_line` and `old_line`.

**Proposed fixes — suggestion blocks.** Put a GitLab suggestion in the body
so the author can apply it. The block is fenced ` ```suggestion:-0+0 ` and
replaces the commented line:

````text
**🔴 CRITICAL — SQL injection.** Use a bound parameter:

```suggestion:-0+0
  rows = db.exec_params('SELECT * FROM users WHERE id = $1', [user_id])
```
````

### 5. Post a conceptual (non-line) resolvable thread
Same endpoint, **no** position → a resolvable thread (unlike `glab mr note`,
which is a non-resolvable comment). Plain body is fine with `-f`:
```bash
glab api -X POST "projects/:fullpath/merge_requests/$MR_IID/discussions" \
  -f body="**🟠 MAJOR — missing tests.** AC-3 needs a failing-login test; none added. ..."
```
Reply into / resolve a thread:
```bash
glab api -X POST "projects/:fullpath/merge_requests/$MR_IID/discussions/$DISCUSSION_ID/notes" -f body="Follow-up."
glab api -X PUT  "projects/:fullpath/merge_requests/$MR_IID/discussions/$DISCUSSION_ID" -F resolved=true
```

### 6. Verdict (GitLab has no native review event)
Express the verdict as a **summary thread** + the approval state:
```bash
# Always: post a summary discussion with the verdict + counts.
glab api -X POST "projects/:fullpath/merge_requests/$MR_IID/discussions" \
  -f body="### diff-reviewer verdict: REQUEST CHANGES — 2 critical, 3 major. See inline threads."

# APPROVE (clean / nits only):
glab mr approve "$MR_IID"                  # optionally -s "$HEAD_SHA" to pin to the reviewed commit
# REQUEST CHANGES: leave unresolved threads and ensure you're NOT approving;
# revoke a prior approval of your own if present:
glab mr revoke "$MR_IID"                   # removes YOUR approval only
```
- 🔴 present → REQUEST CHANGES (summary thread, do not approve; revoke if needed).
- only 🟡/🟢 → COMMENT (summary thread, no approval change).
- clean / nits only → APPROVE.

### Gotchas
- **`--form` for inline, `-f`/`-F` for plain bodies.** Don't mix `--form`
  with `--field`/`--raw-field`/`--input` (glab forbids it).
- `-F` = typed, `-f` = string — **opposite of `gh`**. Use `-F resolved=true`
  for the boolean.
- Poll `diff_refs` until populated; it's empty just after MR creation.
- `new_path` **and** `old_path` are both required even when not renamed.
- Use the MR **iid** (`!123`), not the global MR id.
- URL-encode the project path (`%2F`) when not using `:fullpath`; outside a
  repo `:fullpath` is unavailable.
- Approval is **best-effort**: a project may disable approvals or forbid the
  author/bot from approving (401/403) — surface the error, don't fail the
  whole review.
- Never echo the token; `api` scope is required to post/approve.
- **Bulk-post caution:** unlike GitHub (which bundles all inline comments into
  one review call), GitLab needs a **separate `POST .../discussions` per inline
  finding** — each one notifies subscribers and can trip GitLab rate limits.
  Throttle, keep the count proportionate, and surface the comment count in the
  preview so the user sees how many requests they're approving.
- **De-dup across runs:** discussions are not idempotent. Stamp each comment
  body with a `<!-- diff-reviewer -->` marker and skip findings whose file+line
  already carry it in the fetched discussions before re-posting.
- **Secret in the diff?** Redact the value (`AKIA****`) and do **not** put the
  secret in a ```` ```suggestion ```` block — that republishes it. Recommend
  rotation + history removal.
