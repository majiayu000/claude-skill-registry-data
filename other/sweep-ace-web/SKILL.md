---
name: sweep-ace-web
description: >
  Bulk-delete uploaded chat sessions from a deployed ace-web, after a report and your approval.
disable-model-invocation: false
---

# sweep-ace-web

**Bulk wipe**, not orphan sweep. Lists every `Session` in workspaces where the
caller is Owner or Editor on the deployed ace-web, prints the plan grouped by
workspace, prompts the human, then deletes all approved ids in one call.
CASCADE on the ace-web side handles `IngestUpload`, `Message`,
`SessionParticipant`, `ShareToken`, and `Draft` rows.

This skill does **not** consult the live-set. The user has explicitly opted
into wiping all visible sessions; opp-orphan filtering is not its job.

## Inputs

- `ACE_WEB_BASE_URL` — env var; deployed ace-web base URL (no trailing slash).
  Defaults to `https://labs.connect.dimagi.com/ace` to match
  `--ace-web-url` elsewhere in the plugin.
- `ACE_WEB_PAT_TOKEN` — env var; ACE's own ace-web token by default (written by `/ace:setup`),
  or yours if you minted one with `/ace:ace-web-pat-mint`. The sweep is scoped
  to whichever workspaces that identity belongs to on the ace-web side.
- `sweepFolder` — timestamped sweep folder created by the orchestrator
  (e.g. `ACE/_sweep/<timestamp>/`). Products land here.
- `mode` — `recommend` (default) | `execute`. In `recommend` the skill is
  **report-only**: list + render the plan + return it; **no delete call**.
  In `execute` it deletes only `approvedIds`. The human-confirmation gate
  between the two is the orchestrator's job — see
  `agents/sweep.md § Human-confirmation gate`.
- `approvedIds` (`execute` mode only) — the exact session ids the human
  approved in chat. Delete nothing outside this set.

No `liveSetPath` input. If the orchestrator built one for a sibling sweep,
ignore it.

## Products

- `<sweepFolder>/ace-web-sessions.md` — human-readable plan grouped by
  workspace, with totals at the top.
- `<sweepFolder>/ace-web-sessions.yaml` — machine-readable session list (for
  replay).
- `<sweepFolder>/ace-web-sessions-result.yaml` — written post-execution with
  `deleted` count and `failed[]` rows (if any).

## Process

1. **Verify preconditions.**
   - `ACE_WEB_PAT_TOKEN` set; if missing, stop and instruct the operator to
     run `/ace:ace-web-pat-mint`.
   - `ACE_WEB_BASE_URL` resolved (env var or default). Strip any trailing slash.
   - `sweepFolder` provided by the orchestrator. If absent, abort — the
     skill must not invent its own.

2. **GET `<ACE_WEB_BASE_URL>/api/sessions/sweep`** with
   `-H "Authorization: Bearer $ACE_WEB_PAT_TOKEN"`. Expect 200. Response shape:

   ```yaml
   sessions:
     - id: int
       slug: str
       title: str
       source: "web" | "upload"
       status: "active" | "archived" | "imported"
       opp_slug: str            # may be ""
       opp_run_id: str          # may be ""
       workspace_slug: str
       message_count: int
       upload_count: int
       created_at: ISO-8601
       updated_at: ISO-8601
   total_raw_bytes: int
   ```

   On 401, instruct the operator to re-mint the PAT. On any other non-200,
   print the body and abort.

3. **Render the report.** Group rows by `workspace_slug`. Per-workspace
   section shows: row count, source breakdown (`upload` vs `web` count),
   opp linkage breakdown (with-opp vs unlinked count), and a short table of
   the first 30 rows for that workspace (slug, source, opp_slug, title,
   updated_at). Headline: "ace-web sweep plan — N sessions across M
   workspaces; T MB of raw transcripts." `drive_create_file` to
   `<sweepFolder>/ace-web-sessions.md` and the YAML peer
   `ace-web-sessions.yaml`. The YAML must contain every row in full (not
   truncated) so a replay knows exactly which ids to send.

4. **Recommend — stop here in `mode: recommend`.** Return the plan to the
   orchestrator: the full session-id list (this is a **bulk wipe** — every
   session the PAT can write to, not an orphan-filtered subset; say so
   plainly so the human understands the scope) + per-workspace counts +
   the report Drive link + the reversibility note (delete CASCADEs through
   `IngestUpload`, `Message`, `SessionParticipant`, `ShareToken`, `Draft` —
   **not reversible**). **Issue no delete call.** Do not try to prompt the
   human from this skill — a dispatched subagent can't reach them; the
   orchestrator runs the confirmation gate (see
   `agents/sweep.md § Human-confirmation gate`). If the human declines at
   that gate, the orchestrator never dispatches the execute pass.

## Execute phase (`mode: execute` only)

Runs only when the orchestrator re-dispatches with `mode: execute` +
`approvedIds` (the session ids the human approved in chat — typically all,
but honor a subset if that's what was approved).

5. **POST `<ACE_WEB_BASE_URL>/api/sessions/sweep/delete`** with
   `-H "Content-Type: application/json"`,
   `-H "Authorization: Bearer $ACE_WEB_PAT_TOKEN"`, and
   `{"session_ids": [<approvedIds>...]}` as the body. Expect 200. Response shape:

   ```yaml
   deleted: int
   failed:
     - session_id: int
       reason: "not_found" | "forbidden" | "db_error: <msg>"
   ```

   Write the response to `<sweepFolder>/ace-web-sessions-result.yaml` with
   `decision: "approved"` for downstream summary.

6. **Report.** Return a short summary block:

   ```
   ace-web sweep — N approved, K deleted, F failed
     deleted: K sessions across <M> workspaces
     failed:  F items (see ace-web-sessions-result.yaml)
   ```

## Shell reference

```bash
[ -n "$ACE_WEB_PAT_TOKEN" ] || { echo "ACE_WEB_PAT_TOKEN not set; run /ace:ace-web-pat-mint"; exit 2; }
BASE_URL="${ACE_WEB_BASE_URL:-https://labs.connect.dimagi.com/ace}"
BASE_URL="${BASE_URL%/}"

# Scratch response files: `mktemp`, never a fixed /tmp literal (ace#1046) —
# /tmp is shared across macOS users, so `-o` can fail EACCES while the
# follow-up `cat` silently returns another session's response body.
LIST_JSON="$(mktemp "${TMPDIR:-/tmp}/ace-sweep-list-XXXXXX.json")"
DEL_JSON="$(mktemp "${TMPDIR:-/tmp}/ace-sweep-del-XXXXXX.json")"

# 1. List
HTTP=$(curl -sS -o "$LIST_JSON" -w '%{http_code}' \
  -X GET "$BASE_URL/api/sessions/sweep" \
  -H "Authorization: Bearer $ACE_WEB_PAT_TOKEN")
[ "$HTTP" = "200" ] || { echo "list $HTTP"; cat "$LIST_JSON"; exit 3; }

# 2. (Render + approval handled by the agent calling drive_create_file)

# 3. Delete — agent constructs IDS from approved list
HTTP=$(curl -sS -o "$DEL_JSON" -w '%{http_code}' \
  -X POST "$BASE_URL/api/sessions/sweep/delete" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACE_WEB_PAT_TOKEN" \
  -d "{\"session_ids\": [$IDS]}")
[ "$HTTP" = "200" ] || { echo "delete $HTTP"; cat "$DEL_JSON"; exit 4; }
```

## Failure modes

| HTTP | Cause | Remedy |
|------|-------|--------|
| 401  | `ACE_WEB_PAT_TOKEN` missing/revoked | Re-run `/ace:ace-web-pat-mint`. |
| 422  | Body shape invalid (non-int ids) | Verify the YAML round-trip; ids must be JSON integers. |
| 200 with `failed[]` populated | Per-row failures (e.g. session removed between list and delete, or workspace role changed mid-sweep) | Treat `not_found` as success-equivalent for idempotency. Re-run on `db_error`. `forbidden` means the user's role changed during the sweep. |

## Implementation notes for agents

- `Session` is the only ORM aggregate root. The ace-web endpoint relies on
  Django's `on_delete=CASCADE` to drop `IngestUpload`, `Message`, `Draft`,
  `SessionParticipant`, and `ShareToken` rows. Do not attempt to delete
  those individually.
- Workspace scoping happens server-side via the PAT's user's
  `WorkspaceMembership` rows. The skill never sends a workspace filter —
  the server already knows what the caller can write to.
- The list endpoint is unpaginated by design. If a deployment ever
  accumulates enough sessions to make a single 200 unwieldy, surface that
  back to the ace-web team rather than papering over it client-side.
- `total_raw_bytes` is summed from `IngestUpload.raw_bytes` server-side.
  Display as MB in the report headline (`bytes / 1048576`).

## Related skills

- `sweep-opp-runs` is the other sweep that ignores the live-set (retention,
  not orphan). Same shape: list → render → approve → execute.
- `upload-transcript` is the inverse atom — it's how the sessions wiped by
  this skill got there in the first place.
