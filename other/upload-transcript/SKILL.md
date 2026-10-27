---
name: upload-transcript
description: >
  Upload a Claude session transcript (.jsonl) to a deployed ace-web via /api/ingest/upload.
  Auto-discovers Claude Code's session log when no path is given. Used by /ace:run --ace-web-url.
disable-model-invocation: false
---

# upload-transcript

POSTs a `.jsonl` transcript file to `<base-url>/api/ingest/upload` so the
deployed ace-web can render it as a chat Session. Authenticates with a
Bearer token (`ACE_WEB_PAT_TOKEN`). That's ACE's own ace-web token by default,
written by `/ace:setup`, or yours if minted via `/ace:ace-web-pat-mint`.

**This skill is opt-in and is never invoked implicitly.** A transcript is
the operator's full working record, so publishing it is always a
deliberate act. `/ace:run` dispatches this skill only when the operator
passed `--ace-web-url URL` or set `ACE_WEB_UPLOAD_SESSIONS=1`
(`commands/run.md` step 1a); a human may also invoke it directly. The
presence of `ACE_WEB_PAT_TOKEN` does **not** enable it — that credential
is provisioned by `/ace:setup` for everyone, and treating it as consent
silently enrolled every operator until 2026-07-28. Enforced by
`test/session-upload-opt-in.test.ts`.

## Inputs

- `base_url` — deployed ace-web URL, e.g. `https://labs.connect.dimagi.com/ace`.
- `ACE_WEB_PAT_TOKEN` — env var; ACE's own ace-web token by default
  (`/ace:setup`), or yours via `/ace:ace-web-pat-mint`. Lives as a local-only secret in
  `${CLAUDE_PLUGIN_DATA}/.env` (preserved by `/ace:setup --force-env`,
  which snapshots the local-only marker block — the vault does not hold
  this key). The
  resulting Session is attributed to whichever human signed in to
  ace-web at mint time.

Optional:

- `transcript_path` — filesystem path to a `.jsonl` file. When omitted,
  the skill auto-discovers Claude Code's current session log at
  `~/.claude/projects/<encoded-cwd>/<session-uuid>.jsonl` (newest
  `.jsonl` under the encoded-cwd dir — same lookup `claude --resume`
  uses). Pass an explicit path to override (e.g. when the operator
  wrote stream-json to a custom file via
  `claude -p --output-format stream-json > <file>`).
- `opp_slug` — ACE opportunity slug to link the transcript to. When set,
  the resulting Session is surfaced under the opp in the Workbench's
  "linked chats" panel for that step. Strongly recommended when invoked
  from `/ace:run --ace-web-url`.
- `opp_run_id` — the run-id (e.g. `20260502-1830`) for multi-run layout opps;
  omit for legacy flat opps (see `## Payload fields` below).
- `opp_step_skill` — if the transcript is scoped to a single skill
  invocation (e.g. just the `idea-to-pdd` run, not the full `/ace:run`
  lifecycle), set this so the linkage points at the specific step.
- `ace_root_folder_id` — the Drive root folder id this plugin writes
  opps under (typically `$ACE_DRIVE_ROOT_FOLDER_ID` from `.env`). When
  sent and matching a Workspace's `drive_root_folder_id` on the
  ace-web side, the upload is attributed to that workspace and
  appears in its linked-chats panel. If absent, the upload is stored
  as an orphan (workspace=NULL) — functional but not attributed.

## Payload fields

When invoked from the orchestrator with both `<opp>` and `<run-id>` in
context (the multi-run layout introduced 2026-05-02), send BOTH:

- `opp_slug`: the opp folder name (e.g. `turmeric`).
- `opp_run_id`: the run-id (e.g. `20260502-1830`).
- `opp_step_skill` (optional): the skill that triggered the upload.

For legacy flat opps (no `runs/` subfolder), send `opp_slug` only and
omit `opp_run_id`. The ace-web ingest endpoint accepts either shape.

## Steps

1. **Resolve transcript path.** If the caller passed `transcript_path`,
   use it. Otherwise auto-discover via:

   ```bash
   ls -t "$HOME/.claude/projects/$(pwd | sed 's|/|-|g')"/*.jsonl 2>/dev/null | head -1
   ```

   That's the directory Claude Code writes per-session JSONL logs to;
   the newest file is the live one for the current session (same
   discovery `claude --resume` uses). The path is `~/.claude/projects/`
   followed by the cwd with `/` replaced by `-`, then a
   `<session-uuid>.jsonl`. Works identically for interactive sessions
   and headless `claude -p` runs — Claude writes the same per-session
   log either way.

   If neither an explicit path nor an auto-discovered file exists,
   stop with a single `[INFO]` log line "no transcript file found
   under <encoded-cwd>; skipping upload" and return success — callers
   like `/ace:run --ace-web-url` should NOT treat this as a failure.

2. **Verify preconditions.**
   - The resolved `transcript_path` exists and is non-empty.
   - `ACE_WEB_PAT_TOKEN` is set in the environment. If absent, instruct
     the operator to run `/ace:ace-web-pat-mint` and stop.
   - `base_url` does not end in a trailing slash; strip if present.
   If any fail, stop and report which precondition failed.

3. **POST `<base-url>/api/ingest/upload`** with:
   - the PAT on STDIN via `-H @-`, never `-H "Authorization: Bearer $TOK"` in
     argv — that publishes the live token to `ps` (ace#1114 C1). Auth (no
     cookies, no CSRF — the django-ninja router's `session_auth`
     accepts the Bearer PAT)
   - `-F "opp_slug=<slug>"` (if provided)
   - `-F "opp_run_id=<run_id>"` (if provided; format `YYYYMMDD-HHMM` for multi-run opps)
   - `-F "opp_step_skill=<skill>"` (if provided)
   - `-F "ace_root_folder_id=<id>"` (if `$ACE_DRIVE_ROOT_FOLDER_ID` is
     set; omit the field entirely if not — never send empty)
   - `-F "file=@<transcript_path>;type=application/x-ndjson"` **— this
     part MUST come LAST, after every form field.**
   Expect 201. On non-201, print the response body and fail.

   **File part ordering is load-bearing (jjackson/ace#780).** The ingest
   endpoint is Django Ninja (`apps/ingest/api.py`: `file: UploadedFile =
   File(...)` + `Form(...)` fields), and Django's `MultiPartParser`
   streams parts in order. When the (multi-MB) `file` part is sent
   FIRST and the small form fields trail it, ninja's resolver fails to
   bind `file` and rejects the whole request with HTTP 422
   `{"loc":["file","file"],"msg":"Field required"}` — even though the
   file is present. Putting `file` LAST (all `-F "<form-field>=..."`
   first, then `-F "file=@..."`) makes ninja bind it and the upload
   succeeds. This is why the official ace-web `cli.py` uploader works
   (httpx `data=` form fields are serialized before the `files=` part)
   while a file-first `curl -F` 422s. Protocol (`--http1.1` vs HTTP/2)
   and the `Expect:` header are NOT the cause — only part order is.

4. **Return** the `session_slug` from the 201 response body as the
   skill's output. The response body is a flat object with
   `session_slug`, `messages_imported`, `cli_session_id`, `opp_slug`,
   `opp_run_id`, `opp_step_skill`, and `cost_breakdown` at the top
   level (no `{data: {...}}` envelope). Callers (e.g.
   `/ace:run --ace-web-url`) can log the resulting URL:
   `<base-url>/chat/<session_slug>`.

## Shell reference

```bash
[ -n "$ACE_WEB_PAT_TOKEN" ] || { echo "ACE_WEB_PAT_TOKEN not set; run /ace:ace-web-pat-mint"; exit 2; }

# auto-discover transcript path if caller didn't pass one
if [ -z "${TRANSCRIPT_PATH:-}" ]; then
  TRANSCRIPT_PATH=$(ls -t "$HOME/.claude/projects/$(pwd | sed 's|/|-|g')"/*.jsonl 2>/dev/null | head -1)
  [ -n "$TRANSCRIPT_PATH" ] || { echo "[INFO] no transcript file found under encoded-cwd; skipping upload"; exit 0; }
fi
[ -s "$TRANSCRIPT_PATH" ] || { echo "transcript_path empty: $TRANSCRIPT_PATH"; exit 3; }

# REDACT before upload (security audit 2026-07-31, D1). The raw session log
# contains the stdout of every Bash call — and ACE routinely reads
# $CLAUDE_PLUGIN_DATA/.env, ~/.ace/*-session.json, and curls with Bearer
# headers, so uploading it verbatim publishes live credentials to ace-web.
# Scrub secret-shaped strings into a temp copy and upload THAT, never the
# original. lib/redact-secrets.ts is unit-tested; this is a thin wrapper.
REDACTED_PATH="$(mktemp -t ace-transcript-redacted).jsonl"
npx tsx "${CLAUDE_PLUGIN_ROOT:-.}/scripts/redact-transcript.ts" "$TRANSCRIPT_PATH" "$REDACTED_PATH" \
  || { echo "redaction failed — refusing to upload un-redacted transcript"; exit 5; }

# upload — optional opp/run/step linkage surfaces under that opp in
# the Workbench's linked-chats panel. Omit any field you don't have.
# IMPORTANT: build the form fields FIRST and append the file part LAST.
# The django-ninja endpoint 422s ("file: Field required") if the file
# part precedes the form fields (jjackson/ace#780).
UPLOAD_ARGS=()
[ -n "${OPP_SLUG:-}" ]       && UPLOAD_ARGS+=(-F "opp_slug=$OPP_SLUG")
[ -n "${OPP_RUN_ID:-}" ]     && UPLOAD_ARGS+=(-F "opp_run_id=$OPP_RUN_ID")
[ -n "${OPP_STEP_SKILL:-}" ] && UPLOAD_ARGS+=(-F "opp_step_skill=$OPP_STEP_SKILL")
[ -n "${ACE_DRIVE_ROOT_FOLDER_ID:-}" ] && UPLOAD_ARGS+=(-F "ace_root_folder_id=$ACE_DRIVE_ROOT_FOLDER_ID")
# file part MUST be last — upload the REDACTED copy, not $TRANSCRIPT_PATH
UPLOAD_ARGS+=(-F "file=@$REDACTED_PATH;type=application/x-ndjson")

# Scratch response file: `mktemp`, never a fixed /tmp literal (ace#1046) —
# /tmp is shared across macOS users, so `-o` can fail EACCES while the
# follow-up read silently returns another session's response body (and here
# that would mean publishing the WRONG session slug).
RESP_JSON="$(mktemp "${TMPDIR:-/tmp}/ace-upload-resp-XXXXXX.json")"
# The PAT goes in on STDIN, never in argv (ace#1114 C1): `curl -H "Authorization:
# Bearer $TOK"` publishes the live token to `ps` for the duration of the call.
# curl reads a header from stdin with `-H @-`.
HTTP=$(printf '%s\n' "Authorization: Bearer $ACE_WEB_PAT_TOKEN" | curl -sS -o "$RESP_JSON" -w '%{http_code}' \
  -H @- \
  -X POST "$BASE_URL/api/ingest/upload" \
  "${UPLOAD_ARGS[@]}")
# 409 = identical content already uploaded; treat as idempotent success.
[ "$HTTP" = "201" ] || [ "$HTTP" = "409" ] || { echo "upload $HTTP"; cat "$RESP_JSON"; exit 4; }

# extract session slug — response is flat (no `{data: {...}}` envelope)
SLUG=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1]))['session_slug'])" "$RESP_JSON")
echo "Uploaded. View at $BASE_URL/chat/$SLUG"
```

## Failure modes

| HTTP | Cause | Remedy |
|------|-------|--------|
| 401  | `ACE_WEB_PAT_TOKEN` missing, revoked, or wrong | Re-run `/ace:ace-web-pat-mint`. Check `bin/ace-doctor`'s `[Auth liveness]` block. |
| 403  | Token authenticated but user lacks permission | Confirm the human you minted as has access in ace-web. |
| 409  | Transcript already uploaded (duplicate `cli_session_id` or content hash) | Expected on re-runs; treat as success for idempotency. As of ace-web PR #275 the dedup check falls back to raw-byte sha256 when the transcript has no `cli_session_id` — the case for Claude Code interactive session logs, which record `sessionId` (camelCase) instead of the headless `session_id` (snake_case) stream-json shape. Both shapes ingest cleanly; 409 just means a prior run already uploaded the same bytes. |
| 422 `{"loc":["file","file"],"msg":"Field required"}` | The `file` multipart part was sent BEFORE the form fields | Reorder so every `-F "<form-field>=..."` precedes `-F "file=@..."` (the file part must be LAST). This is the #1 cause of a silent upload failure from `/ace:run --ace-web-url` — the file IS present, ninja just won't bind it when it leads. See jjackson/ace#780 + Step 3. |
| 422 (other `loc`) | Malformed `opp_slug` / `opp_run_id` / `opp_step_skill` | Each field must match `[A-Za-z0-9_.-]{1,64}`. Whitespace, slashes, or empty-after-strip values are rejected. Fix the form value and retry. |

## Reference

- ace-web `docs/architecture/cli-credentials.md` — broader auth model
  context.
- ace-web `apps/auth/cli_authorize_views.py` — the `/auth/cli/authorize/`
  endpoint that mints the PAT (gh-style loopback flow).
- ace-web `apps/auth/models.py:32-67` — `PersonalToken` model.
- ace-web `apps/auth/token_backend.py` — Bearer PAT authentication.
- ace-web `apps/ingest/api.py` defines the upload endpoint — a **Django
  Ninja v2** router (`router = Router(auth=session_auth)`; route `upload(request,
  file: UploadedFile = File(...), opp_slug: str | None = Form(None), ...)`).
  `session_auth` accepts the Bearer PAT. The endpoint migrated off the old
  DRF `apps/ingest/views.py` (`MultiPartParser`/`IsAuthenticated`) — the
  practical consequence for clients is the file-part-LAST ordering
  requirement documented in Step 3 (jjackson/ace#780).
- ace-web `apps/ingest/cli.py` — the canonical `ace-upload` client
  (httpx; `data=` form fields serialize before the `files=` part, which
  is why it never hits the ordering 422).
- `commands/ace-web-pat-mint.md` — the mint slash-command.
