---
name: gh-cli
description: >
  Drive the GitHub CLI (gh) to review a pull request — fetch the diff and
  context, post inline review comments anchored to specific diff lines,
  open conceptual conversation threads, and submit a verdict
  (APPROVE / REQUEST_CHANGES / COMMENT). Use when reviewing or commenting
  on a GitHub PR. Triggers on: gh, github cli, pull request, pr review,
  post pr comment, gh api, review github pr.
---

## gh CLI — PR review & commenting

Everything here drives `gh` via the shell. `gh api repos/{owner}/{repo}/...`
auto-expands `{owner}`/`{repo}` from the current clone — in the URL **path**
and in `-F`/`--field` values (**not** `-f`/`--raw-field`, which sends the
literal string, and **not** inside an `--input` JSON body). Set
`GH_REPO=OWNER/REPO` or pass `-R OWNER/REPO` when outside the repo.

### 0. Auth check (do this first)
```bash
gh auth status              # must be authenticated; token needs `repo` scope to post reviews
ME=$(gh api user -q .login) # your login — used for the self-PR fallback below
```

### 1. Resolve the target
```bash
PR=42
gh pr view "$PR" --json number,title,state,isDraft,author,headRefName,baseRefName,headRefOid,url,mergeable
HEAD_SHA=$(gh pr view "$PR" --json headRefOid -q .headRefOid)   # commit_id for review comments
AUTHOR=$(gh pr view "$PR" --json author -q .author.login)
```

### 2. Fetch context (read-only)
```bash
gh pr diff "$PR"                                              # unified diff (the change to review)
gh api --paginate repos/{owner}/{repo}/pulls/$PR/files        # per-file patch hunks — validate comment line numbers against these
gh pr checks "$PR"                                            # CI status (evidence, not a finding to re-derive)

# Existing feedback — read before posting so you never duplicate a point:
gh api --paginate repos/{owner}/{repo}/pulls/$PR/comments     # inline review comments
gh api --paginate repos/{owner}/{repo}/pulls/$PR/reviews      # prior reviews
gh api --paginate repos/{owner}/{repo}/issues/$PR/comments    # conversation comments

# Linked issue (acceptance criteria) — PRs link via "Closes #N":
gh pr view "$PR" --json body,closingIssuesReferences
gh issue view <N> --json number,title,body,state,labels
```

### 3. Post inline comments + verdict in ONE review (the reliable path)
Bundle every line-anchored comment and the verdict into a single
`POST .../pulls/<PR>/reviews` call. The nested `comments[]` array can't be
built with `-f`/`-F`, so pass raw JSON. Build it with `jq` (safest — it
escapes bodies for you) **or** a quoted heredoc, then `--input`.

Write the static `comments[]` array with a **quoted** heredoc (so backticks
and `$` in bodies stay literal), then let `jq` inject the **computed**
`commit_id` and `event` — never hardcode the verdict, or you'll post
`REQUEST_CHANGES` on a self-PR (422). `$EVENT` and `$HEAD_SHA` come from
steps 1 and 5; on your own PR `$EVENT` is `COMMENT`.
```bash
cat > /tmp/comments.json <<'JSON'
[
  { "path": "src/auth.ts", "line": 88, "side": "RIGHT",
    "body": "**🔴 CRITICAL — SQL injection.** userId is concatenated into the query; use a bound parameter (see suggestion)." },
  { "path": "src/api.ts", "start_line": 20, "start_side": "RIGHT", "line": 23, "side": "RIGHT",
    "body": "**🟠 MAJOR — unhandled rejection.** Wrap this block in try/catch and return a 5xx." },
  { "path": "src/old.ts", "line": 7, "side": "LEFT",
    "body": "**🟡 MINOR** — comment on a *deleted* line (LEFT = original file)." }
]
JSON
jq -n \
  --arg sha   "$HEAD_SHA" \
  --arg event "$EVENT" \
  --arg body  "## diff-reviewer verdict: $EVENT — see inline comments + threads." \
  --slurpfile comments /tmp/comments.json \
  '{commit_id:$sha, event:$event, body:$body, comments:$comments[0]}' \
  | gh api repos/{owner}/{repo}/pulls/$PR/reviews --input -
```
> `jq` escapes the bodies and injects the real `$HEAD_SHA`/`$EVENT`, so the
> verdict always matches step 5 (and the self-PR fallback). Keep `{owner}`/
> `{repo}` in the URL — they don't expand inside the JSON.

**Line/side rules (getting these wrong → HTTP 422):**
- `path` — repo-relative file path.
- `line` — the line number **in the file** the comment targets; for a
  multi-line comment it is the **last** line of the range.
- `side` — `RIGHT` = added/unchanged (new file; the default), `LEFT` =
  deleted (original file). Use `LEFT` for removed lines.
- Multi-line comment → **also** set `start_line` + `start_side` (the first
  line/side; `start_line < line`). Single-line → omit both.
- The target line **must be part of the diff** (an added/changed/context
  line inside a hunk) — validate against `pulls/$PR/files` patch hunks
  first, or the whole call 422s.
- `event`: `APPROVE` | `REQUEST_CHANGES` | `COMMENT`. `body` is **required**
  for `REQUEST_CHANGES`/`COMMENT`. Omitting `event` leaves the review
  **PENDING** (unsubmitted, no notification) — don't forget to submit.

**Proposed fixes — suggestion blocks.** When the fix is a local edit,
include a suggestion block in the comment `body` so the author applies it in
one click. The body is a JSON string, so the block is a `\n`-delimited
fenced section like this (literal newlines shown for clarity):

````text
**🔴 CRITICAL — SQL injection.** Use a parameterised query:

```suggestion
  const rows = await db.query('SELECT * FROM users WHERE id = $1', [userId]);
```
````
In JSON that body becomes:
`"...Use a parameterised query:\n\n```suggestion\n  const rows = ...\n```"`
(the suggestion replaces exactly the commented line(s)).

### 4. Post a conceptual (non-line) thread
For findings not tied to one line — architecture, missing tests, PR scope:
```bash
gh pr comment "$PR" --body "**🟠 MAJOR — no tests for the new auth path.** AC-3 requires a failing-login test; none added. ..."
```

### 5. Verdict & self-PR fallback
The `event` on the review **is** the verdict. But you **cannot** `APPROVE`
or `REQUEST_CHANGES` your **own** PR (GitHub returns 422). Branch on it:
```bash
if [ "$ME" = "$AUTHOR" ]; then
  EVENT="COMMENT"          # always allowed on your own PR; still carries inline comments + summary
else
  EVENT="REQUEST_CHANGES"  # or APPROVE / COMMENT per the findings
fi
```
- 🔴 present → `REQUEST_CHANGES` (or `COMMENT` if self-PR).
- only 🟡/🟢 → `COMMENT`.
- clean / nits only → `APPROVE` (non-author).

### Gotchas
- Prefer the **reviews** endpoint over `POST .../pulls/$PR/comments` — the
  standalone comments endpoint frequently 422s even with valid line/side.
- `{owner}`/`{repo}` expand in the URL path and in `-F`/`--field` values
  (**not** `-f`/`--raw-field`, which is literal), and **not** inside `--input`
  JSON — keep them in the path.
- `position` (diff-offset anchoring) is **deprecated** — always use `line`/`side`.
- Pass `commit_id = $HEAD_SHA`; a stale SHA marks comments "outdated".
- Throttle bulk posts — review creation sends notifications and can hit a
  secondary rate limit.
- Never echo the token; `repo` scope is required to post (read-only → 403).
- **De-dup across runs:** comments are not idempotent — a second run re-posts
  everything. Stamp each comment body with a `<!-- diff-reviewer -->` marker,
  and in step 2 skip any finding whose file+line already carries that marker in
  the fetched `pulls/$PR/comments`.
- **Secret in the diff?** Redact the value in the comment (`AKIA****`) and do
  **not** put the secret in a ```` ```suggestion ```` block — that would
  republish it. Recommend rotation + history removal.
- **Staged / silent option:** omit `event` to create the review **PENDING**
  (no notification). You can show the human the rendered review on GitHub, then
  submit it via `POST .../pulls/$PR/reviews/$REVIEW_ID/events` with the chosen
  event — a belt-and-suspenders complement to the in-chat preview gate.
