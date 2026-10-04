---
name: calendar-mgmt
description: |
  Google Calendar integration for end-user schedule management at runtime.
  Use when the user wants to view, create, update, or delete calendar events, or get a week summary
  ("show my schedule", "book a meeting tomorrow at 3pm", "what's on my calendar this week").
  MVP supports Google Calendar API (OAuth2). On first use, guide Google Cloud OAuth setup,
  collect client_secret via hidden shell prompt, run setup.py --oauth, and store tokens in
  ~/.libragent/calendar_config.json. Not for LibrAgent agent cron automation (schedule / loop) or completion waits (call-me-back).
  Triggers on: "일정 보여줘", "캘린더 확인", "미팅 예약", "show my calendar", "schedule a meeting".
---

# Calendar Management

Manage the **user's** Google Calendar from LibrAgent — read and write events, summarize the week.

This is an **end-user daily work** skill (like `email-integration`, `telegram-cli`, `x-cli`). It is not for LibrAgent internal development or agent-only cron tasks.

## Not This Skill

| Skill | Use for |
| --- | --- |
| **schedule** / **loop** | Wake an assistant on a clock/cron (automation harness) |
| **call-me-back** | Resume this session on process/kanban/webhook completion |
| **email-integration** | Mail read/send (IMAP/SMTP; browser `use_profile` webmail fallback) |
| **recruit** / **boost** | Create or strengthen assistant configurations |

**CalDAV** (Nextcloud, Apple, Fastmail) is planned for a later release. MVP is **Google Calendar API only**.

## Path conventions

Paths are relative to this skill's Base Directory. Replace `<skill-base-dir>` with its absolute path in commands.

## Security (mandatory)

- **NEVER** ask for `client_secret`, access tokens, or refresh tokens in chat
- **NEVER** display or repeat `~/.libragent/calendar_config.json`
- Collect `client_secret` only via a **single hidden shell prompt** (`requireUserInput=true`, `inputType=password`), then pass `--client-secret-env LIBRAGENT_GOOGLE_CLIENT_SECRET`
- If the user pastes a secret in chat, do not echo it — run setup immediately

## Prerequisites

```bash
pip install google-auth google-auth-oauthlib google-api-python-client
```

On Linux/macOS use `pip3` if `pip` is unavailable.

## Workflow

### 1. Detect config

```bash
python "<skill-base-dir>/scripts/validate_config.py"
```

| Exit code | Meaning | Next step |
| --- | --- | --- |
| `0` | Connected | Step 3 |
| `1` | Not configured | Step 2 |
| `2` | Incomplete / expired / corrupt | Step 2 (see `action` in JSON) |

### 2. Setup (first time or re-auth)

See [references/google-setup.md](references/google-setup.md) for Google Cloud Console steps and [references/setup-flow.md](references/setup-flow.md) for the LibrAgent hidden-prompt pattern.

**Summary:**

1. User creates a **Desktop OAuth client** in Google Cloud (Calendar API enabled).
2. Collect `client_id` in chat (not secret).
3. Hidden prompt → set `LIBRAGENT_GOOGLE_CLIENT_SECRET`.
4. Run OAuth:

```bash
python "<skill-base-dir>/scripts/setup.py" \
  --client-id "YOUR_CLIENT_ID.apps.googleusercontent.com" \
  --client-secret-env LIBRAGENT_GOOGLE_CLIENT_SECRET \
  --oauth
```

Re-auth only (credentials already saved):

```bash
python "<skill-base-dir>/scripts/setup.py" --oauth
```

Reset and reconnect:

```bash
python "<skill-base-dir>/scripts/setup.py" \
  --reset \
  --client-id "..." \
  --client-secret-env LIBRAGENT_GOOGLE_CLIENT_SECRET \
  --oauth
```

A browser window opens for Google consent. Tokens persist under `~/.libragent/calendar_config.json`.

### 3. Dispatch action

Classify the request and call `calendar_cli.py`:

| Action | When | Command |
| --- | --- | --- |
| `week_summary` | "이번 주 일정", "my week" | `--action week_summary [--timezone Asia/Seoul]` |
| `list_events` | Range listing | `--action list_events --from ISO --to ISO [--limit N]` |
| `get_event` | One event by ID | `--action get_event --event-id ID` |
| `create_event` | Book / schedule | `--action create_event --title T --start ISO --end ISO [--location L] [--description D] [--attendees a@b.com,c@d.com]` |
| `update_event` | Reschedule / edit | `--action update_event --event-id ID [--title] [--start] [--end] ...` |
| `delete_event` | Cancel | `--action delete_event --event-id ID` |

Use RFC 3339 datetimes (e.g. `2026-06-12T15:00:00+09:00`). For all-day events add `--all-day` and use `YYYY-MM-DD` dates.

Examples: [references/request-patterns.md](references/request-patterns.md).

**Before create/update/delete:** confirm title, time, and timezone with the user when the request is ambiguous.

### 4. Present results

Format for humans per [references/output-format.md](references/output-format.md). Errors: [references/error-handling.md](references/error-handling.md).

## Config shape

```json
{
  "provider": "google",
  "google": {
    "client_id": "...",
    "client_secret": "...",
    "tokens": { }
  },
  "caldav": null
}
```

`caldav` is reserved for a future release.

## Guidelines

- **User calendar, not agent cron** — distinguish from `schedule` skill.
- **OAuth is multi-step** — similar friction to `telegram-cli`, not `email-integration` app passwords.
- **No Gmail API synergy in v1** — email uses IMAP; cross-skill "mail → event" uses agent reasoning, not shared tokens.
- **Confirm destructive actions** — delete and attendee-affecting updates.
- **Timezone explicit** — ask or infer user timezone for `week_summary` and new events.

## Builtin Tools

| Step | Tool |
| --- | --- |
| Validate config | `workspace__runCommand` → `validate_config.py` |
| Setup / OAuth | `workspace__runCommand` → `setup.py` |
| Calendar ops | `workspace__runCommand` → `calendar_cli.py` |
| Open OAuth help URL | `browser` (optional, user-facing docs only) |

## References

- [google-setup.md](references/google-setup.md) — Google Cloud OAuth client setup
- [setup-flow.md](references/setup-flow.md) — hidden prompt + setup commands
- [request-patterns.md](references/request-patterns.md) — natural language → actions
- [output-format.md](references/output-format.md) — presentation guidelines
- [error-handling.md](references/error-handling.md) — recovery steps
- [caldav-setup.md](references/caldav-setup.md) — future CalDAV (not in MVP)
