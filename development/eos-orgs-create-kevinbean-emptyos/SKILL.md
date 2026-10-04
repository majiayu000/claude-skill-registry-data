---
name: eos-orgs-create
description: Create a Real Org in `apps/public/standard/company/` by extracting details from the current Claude Code conversation and confirming once. Use when the user says "create an org", "new org", "add a company", "make a team for X", or names a concrete organisation (employer, client, side-project group) that doesn't exist in the system yet. Wraps `POST /orgs/api/orgs` so the same vault note + `orgs:org_created` event fire that the web UI produces. NOT for adding a person to an org that already exists (use eos-orgs-member-add), listing orgs (use eos-orgs-list), or running a scenario against one (use eos-orgs-run-scenario).
---

# EmptyOS Orgs — Create

Create a new Real Org under `apps/public/standard/company/`. Unlike the web UI's AI-form-fill modal, this skill has the current conversation as context — it should pre-fill every field it can infer from chat history, then ask the user to confirm once instead of grilling field-by-field.

The skill writes through the HTTP API (`POST /orgs/api/orgs`) so the vault note, frontmatter shape, and downstream events match the web UI exactly. **Do not write vault notes directly** — that bypasses validation + event emission.

## When to Use

- User says "create an org", "new org for X", "add a company", "make a team for the Y project"
- Conversation has surfaced a real-world organisation (employer, client, side-project, study group) that's worth tracking in the system
- **Not** for Persona Sims — those are scenario sandboxes, created via the web UI's Persona tab
- **Not** for adding members to an existing org — use `eos-orgs-member-add` instead

## Pre-flight

This skill writes through the daemon HTTP API, so the daemon must be reachable first:

- **Daemon up** — `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:9000/orgs/` should print `200`. If not, ask the user to run `restart.bat` — never start/restart the daemon yourself (`.claude/rules/daemon-handling.md`).
- **Auth (private mode)** — read `auth_token` from `emptyos.toml` `[network]` and send `Authorization: Bearer <token>` on every request (`.claude/rules/environment.md`).
- **Non-ASCII bodies** — POST via Python `urllib`, not `curl -d` (Windows cp1252 mangles em-dash / CJK).

## Schema (Real Org, v1)

Exactly the fields `POST /orgs/api/orgs` accepts. Defaults applied server-side when omitted.

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `name` | string | **yes** | — | Display name. Also becomes the slug-id (lowercase, hyphens). |
| `kind` | enum | no | `team` | `team` / `household` / `side-business` / `employer` / `vendor` / `community` / `other` |
| `reality` | enum | no | `real` | `real` (humans) or `virtual` (simulation — but use the web UI for these) |
| `scope` | enum | no | `member` | `member` (internal) or `external` |
| `mission` | string | no | `""` | One sentence. |
| `vision` | string | no | `""` | One sentence. |
| `values` | string | no | `""` | Comma-separated or prose. |
| `culture` | string | no | `""` | Free-form. |
| `roles` | string | no | `""` | Free-form description of org chart shape. |
| `parent` | string | no | `""` | Parent org id, if this is a sub-team. |
| `company_id` | string | no | `""` | Linked org id (e.g. a division's parent company). |

## Process

### Step 1 — Scan the conversation for clues

Don't ask the user anything yet. Read back through the conversation (and any args passed to the skill) and extract:

- **Name** — explicit mentions ("Acme Corp", "the Phoenix team", "Build Club Sydney"). Pick the most-recently-named candidate if multiple appear.
- **Kind** — `employer` for a company you work at; `side-business` for your own venture; `team` for project / squad / sub-group inside a larger org; `community` for meetups / clubs / open-source projects; `household` for family / shared-living; `vendor` for a supplier or contractor relationship; `other` if none fit.
- **Mission / vision / values / culture / roles** — pull verbatim phrases from chat if the user said things like "they focus on X" or "their roles are Y, Z". If nothing surfaced, leave blank — do not invent.
- **Parent / company_id** — only if the user explicitly said "this is part of <other org>" *and* that org already exists (run `GET /orgs/api/orgs` to confirm; do not chain-create parents in one skill invocation).

If `name` is impossible to infer, ask the user for it directly via AskUserQuestion before continuing. Everything else is optional — leave blank rather than guess.

### Step 2 — Render the proposed spec

Print a compact preview block:

```
Proposed org:
  name:       <name>
  kind:       <kind>
  reality:    real
  scope:      member
  mission:    <or "(blank)">
  vision:     <or "(blank)">
  values:     <or "(blank)">
  culture:    <or "(blank)">
  roles:      <or "(blank)">
  parent:     <or "(none)">
  company_id: <or "(none)">
```

### Step 3 — Confirm once

Use AskUserQuestion with three options:

- **"Create as proposed"** — POST the spec as-is.
- **"Edit fields first"** — accept inline corrections from the user, re-render, re-ask.
- **"Cancel"** — abort, no API call.

Do not split this into per-field questions. One confirm beats nine grills.

### Step 4 — Read the auth token + POST

Read `auth_token` from `D:\emptyos\emptyos.toml` (it's the top-level `auth_token = "..."` under `[network]` or root). Pass it as a Bearer header. The skill assumes the daemon is at `http://127.0.0.1:9000`; if `[network] port` differs, read it from the same config.

```bash
TOKEN=$(grep -E '^auth_token' D:/emptyos/emptyos.toml | head -1 | sed 's/.*= *"\(.*\)".*/\1/')
curl -s -X POST http://127.0.0.1:9000/orgs/api/orgs \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '<JSON spec>'
```

Use `python -c "import json; ..."` for the JSON body if the spec contains characters that bash escaping mangles (em-dashes, unicode quotes — see memory `feedback_curl_windows_utf8_bodies`).

On the response:
- `{id, name, vault_path}` → success, capture all three
- `{error: "..."}` → surface the error verbatim, stop the skill, do not retry blindly

### Step 5 — Verify

```bash
curl -s -H "Authorization: Bearer $TOKEN" http://127.0.0.1:9000/orgs/api/orgs/<id>
```

The response should include the org with the fields we sent. If the GET returns 404 or `{error:...}`, the POST silently failed — escalate to the user with both responses so they can diagnose.

### Step 6 — Report

Output to the user:

```
✓ Org created: <name>
  id:         <id>
  vault:      <vault_path>
  edit web:   http://localhost:9000/orgs/?org=<id>

Next:
  • Add members  →  /eos-orgs-member-add <id>
  • Open in web  →  click the URL above
```

Do **not** offer to start a /schedule, do not create follow-up tasks, do not invent next steps that aren't on the list above.

## Verification (end-to-end check after skill run)

The user should see:
1. The web UI at `/company/` lists the new org under "Real Orgs"
2. The vault has a new file at `{vault}/30_Resources/EmptyOS/org/<id>/<id>.md` with the frontmatter we POSTed
3. The system event log shows one `orgs:org_created` event with payload `{id, name}`

If any of these are missing, the org write didn't fully land — check the daemon log at `D:\emptyos\data\daemon.err.log` and surface the diagnosis.

## Anti-patterns

- **Don't** generate mission/vision/values from thin air. Blank is honest; LLM-spun corporate filler is worse than nothing and pollutes the vault.
- **Don't** write the vault file directly with the Write tool. The HTTP path emits events; direct writes are invisible to the rest of the system.
- **Don't** pre-create a parent org "to satisfy the schema". Parent must already exist; if it doesn't, leave parent blank and let the user wire it up afterwards.
- **Don't** use this skill for one-shot scenarios (planning meetings, ideation sims). Those belong in the web UI's Persona Sim tab — they're throwaway by design.
