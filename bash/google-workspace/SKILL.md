---
name: google-workspace
description: >-
  Gmail, Calendar, Drive, Docs, Sheets, Contacts, and Google Chat via OAuth and
  the bundled Python CLI (scripts/google_api.py). Use when the user mentions
  Gmail, Google Calendar, Drive, Sheets, Docs, Chat, Workspace, or invokes
  /google-workspace_*.
disable-model-invocation: true
---

### TO COPY

# google-workspace

Per-workspace registration slice. OAuth JSON files live in `{SKILL_PATH}/`.

## Working directory

Placeholders changed by `/meta-skills` at copy time (NAME => {PLACEHOLDER}):

IS_GLOBAL => {IS_GLOBAL}
TYPE_OF_AI_TOOLS => {TYPE_OF_AI_TOOLS}
SKILL_PATH => {SKILL_PATH}

```bash
export CURRENT_SKILL_DIRECTORY="{SKILL_PATH}"
~/.meta-skills/.venv/bin/python ~/.meta-skills/skills/productivity/google/google-workspace/scripts/setup.py --check
```

##### END TO COPY

# google-workspace

## When to use

Use for Google Workspace API work. Trigger phrases: "check my email", "create calendar event", "upload to Drive", "update Sheet", "Google Docs", "Google Chat", "Chat space", `/google-workspace_gmail_*`, `/google-workspace_calendar_*`, `/google-workspace_chat_*`.

`setup.py` / `google_api.py` resolve credentials via SkillCred — do not `source` `.env` in the shell (not portable across Windows, macOS, and Linux).

Library scripts: `~/.meta-skills/skills/productivity/google/google-workspace/`.

## Slash commands

### Setup

| Slash | CLI | Description |
|-------|-----|-------------|
| `/google-workspace_setup_check` | `python scripts/setup.py --check` | Auth status |
| `/google-workspace_setup_client-secret` | `python scripts/setup.py --client-secret PATH` | Store OAuth client JSON |
| `/google-workspace_setup_auth-url` | `python scripts/setup.py --auth-url [--services …]` | Print OAuth URL (scopes: `references/oauth-services.md`) |
| `/google-workspace_setup_auth-code` | `python scripts/setup.py --auth-code CODE` | Exchange code for token |
| `/google-workspace_setup_stop-http-local` | `python scripts/setup.py --stop-http-local` | Kill leftover `http-local.py` servers |
| `/google-workspace_setup_revoke` | `python scripts/setup.py --revoke` | Revoke + delete token |
| `/google-workspace_setup_install-deps` | `python scripts/setup.py --install-deps` | Install Python deps |

### Gmail

| Slash | CLI | Description |
|-------|-----|-------------|
| `/google-workspace_gmail_search` | `python scripts/google_api.py gmail search QUERY [--max N]` | Search messages |
| `/google-workspace_gmail_get` | `python scripts/google_api.py gmail get MESSAGE_ID` | Read message |
| `/google-workspace_gmail_send` | `python scripts/google_api.py gmail send --to … --subject … --body …` | Send email |
| `/google-workspace_gmail_reply` | `python scripts/google_api.py gmail reply MESSAGE_ID --body …` | Reply in thread |
| `/google-workspace_gmail_labels` | `python scripts/google_api.py gmail labels` | List labels |
| `/google-workspace_gmail_modify` | `python scripts/google_api.py gmail modify MESSAGE_ID [--add-labels …] [--remove-labels …]` | Change labels |

### Calendar

| Slash | CLI | Description |
|-------|-----|-------------|
| `/google-workspace_calendar_list` | `python scripts/google_api.py calendar list [--start …] [--end …]` | List events |
| `/google-workspace_calendar_create` | `python scripts/google_api.py calendar create --summary … --start … --end …` | Create event |
| `/google-workspace_calendar_delete` | `python scripts/google_api.py calendar delete EVENT_ID` | Delete event |

### Drive

| Slash | CLI | Description |
|-------|-----|-------------|
| `/google-workspace_drive_search` | `python scripts/google_api.py drive search QUERY [--max N]` | Search files |
| `/google-workspace_drive_get` | `python scripts/google_api.py drive get FILE_ID` | File metadata |
| `/google-workspace_drive_upload` | `python scripts/google_api.py drive upload PATH [--name …] [--parent ID]` | Upload |
| `/google-workspace_drive_download` | `python scripts/google_api.py drive download FILE_ID [--output PATH]` | Download / export |
| `/google-workspace_drive_create-folder` | `python scripts/google_api.py drive create-folder NAME [--parent ID]` | Create folder |
| `/google-workspace_drive_share` | `python scripts/google_api.py drive share FILE_ID --email … --role reader` | Share |
| `/google-workspace_drive_delete` | `python scripts/google_api.py drive delete FILE_ID [--permanent]` | Trash / delete |

### Contacts / Sheets / Docs

| Slash | CLI | Description |
|-------|-----|-------------|
| `/google-workspace_contacts_list` | `python scripts/google_api.py contacts list [--max N]` | List contacts |
| `/google-workspace_sheets_get` | `python scripts/google_api.py sheets get SHEET_ID RANGE` | Read range |
| `/google-workspace_sheets_update` | `python scripts/google_api.py sheets update SHEET_ID RANGE --values '[[…]]'` | Write range |
| `/google-workspace_sheets_append` | `python scripts/google_api.py sheets append SHEET_ID RANGE --values '[[…]]'` | Append rows |
| `/google-workspace_sheets_create` | `python scripts/google_api.py sheets create --title …` | New spreadsheet |
| `/google-workspace_docs_get` | `python scripts/google_api.py docs get DOC_ID` | Read doc |
| `/google-workspace_docs_create` | `python scripts/google_api.py docs create --title … [--body …]` | New doc |
| `/google-workspace_docs_append` | `python scripts/google_api.py docs append DOC_ID --text …` | Append text |

### Google Chat

| Slash | CLI | Description |
|-------|-----|-------------|
| `/google-workspace_chat_spaces` | `python scripts/google_api.py chat spaces [--max N] [--filter …]` | List spaces / teams |
| `/google-workspace_chat_get-space` | `python scripts/google_api.py chat get-space SPACE_ID` | Space details |
| `/google-workspace_chat_messages` | `python scripts/google_api.py chat messages SPACE_ID [--max N]` | List messages |
| `/google-workspace_chat_get-message` | `python scripts/google_api.py chat get-message SPACE_ID MESSAGE_ID` | Read one message |
| `/google-workspace_chat_send` | `python scripts/google_api.py chat send SPACE_ID --text …` | Send a message |

Named teams only: `--filter 'spaceType = "SPACE"'`. Enable the **Google Chat API** in Cloud Console before first use. After adding Chat scopes, re-run OAuth (`--auth-url` / `--auth-code`).

## How to run

1. Set `CURRENT_SKILL_DIRECTORY` to `{SKILL_PATH}`, then run scripts from `~/.meta-skills/skills/productivity/google/google-workspace/`.
2. First use: `/google-workspace_setup_check`. If not authenticated, run setup below.
3. Run the CLI for the slash command; parse JSON output.

### First-time OAuth (agent-driven)

1. Ask which services (values + scopes: local `references/oauth-services.md`): `email`, `calendar`, `drive`, `sheets`, `docs`, `chat`, `contacts`, or `all`.
2. User creates a Desktop OAuth client in [Google Cloud Console](https://console.cloud.google.com/apis/credentials), enables the needed APIs (**including Google Chat API** if using Chat), downloads `client_secret.json`.
3. `python scripts/setup.py --client-secret /path/to/client_secret.json`
4. `python scripts/setup.py --auth-url --services …` → send the printed auth URL to the user.
5. User pastes redirect URL or code → `python scripts/setup.py --auth-code "…"`
6. `python scripts/setup.py --check` → expect `AUTHENTICATED`

References in this skill folder:
- `--services` / OAuth scopes → `references/oauth-services.md`
- Gmail search operators → `references/gmail-search-syntax.md`

## Notes

- Confirm with the user before **send/reply**, **calendar create/delete**, **Drive share/delete**, **Sheets/Docs write**, or **Chat send**.
- Calendar times must be ISO 8601 with timezone offset or `Z`.
- Prefer trash (`drive delete`) over `--permanent`.
- Chat space ids accept bare ids (`AAAA`) or resource names (`spaces/AAAA`).
- Optional: if `gws` is on `PATH`, `google_api.py` may use it; same token file next to `SKILL.md`.
- Never commit `google_token.json` / `google_client_secret.json` / `google_oauth_pending.json`.
