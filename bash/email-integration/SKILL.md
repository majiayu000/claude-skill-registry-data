---
name: email-integration
description: |
  Integrates with any IMAP/SMTP mail server (Gmail, Outlook, Naver, Kakao, custom servers, etc.).
  Use when the user wants to read, send, search, reply to, or manage emails.
  Primary path: validate_config + email_client.py (hidden password setup via setup_account.py).
  If Python/config/IMAP auth fails, fall back to browser saved-login webmail (Gmail/Outlook) via
  browser-session-assist and use_profile=true after explicit user confirmation.
  Triggers: "메일 보여줘", "이메일 확인", "send email", "받은 편지함", "메일 보내줘", "메일 검색".
---

# Email Integration

Interact with mail on behalf of the user. Prefer **IMAP/SMTP scripts** when they work; use **browser profile webmail** only as fallback.

## Path conventions

Paths are relative to this skill's Base Directory. Replace `<skill-base-dir>` with its absolute path in commands.

- On Linux/macOS, use `python3` if `python` is unavailable.
- Always quote paths: `"<skill-base-dir>/scripts/..."`.

## Security (mandatory)

- **NEVER** ask for passwords in chat or display `~/.libragent/email_config`
- Collect password only via a single hidden shell prompt; persist with `setup_account.py`
- If the user pastes a secret in chat, do not echo it—run setup immediately
- Browser fallback: **never** set `use_profile=true` without explicit user confirmation (see `browser-session-assist`)

## Decision tree

1. **Try IMAP script path** (steps 1–4 below).
2. **On failure** that blocks scripts, offer browser fallback (do not loop forever on setup):
   - `python` / `python3` missing
   - config missing/corrupt and user declines password setup, or setup/auth fails
   - IMAP/SMTP auth failure, app-password / Modern Auth blocked
3. If user agrees → follow [references/browser-fallback.md](references/browser-fallback.md) (uses `browser-session-assist`).
4. If `createSession` reports no imported profile → guide Settings import; if Google block → Open to sign in; then retry browser path.
5. If user declines all paths → explain IMAP setup vs Saved browser logins and stop.

## Workflow (IMAP primary)

### 1. Detect config

```bash
python "<skill-base-dir>/scripts/validate_config.py"
```

- Exit `0` → configured, go to step 3
- Exit `1` → not configured, go to step 2 (or offer browser fallback if user prefers)
- Exit `2` → corrupt config, go to step 2 with `--reset`

### 2. Setup (first time or reset)

See [references/setup-flow.md](references/setup-flow.md) for the PowerShell two-step pattern and preset/custom domain commands.

### 3. Dispatch action

Classify the request and call `email_client.py`:

| Action | When | Command |
|---|---|---|
| `read_inbox` | Browse inbox | `--action read_inbox [--limit N] [--filter unread\|today\|all]` |
| `read_email` | Full content by UID | `--action read_email --uid <UID>` |
| `send_email` | Compose/send/reply | `--action send_email --to ... --subject ... --body ... [--reply-to-uid <UID>]` |
| `search_email` | Keyword/sender/date | `--action search_email --query "<IMAP search>"` |
| `manage_email` | Mark/move/delete | `--action manage_email --uid <UID> --op <mark_read\|mark_unread\|move\|delete>` |

Search query examples: see [references/request-patterns.md](references/request-patterns.md).
Server presets: see [references/server-profiles.md](references/server-profiles.md).

Draft vague compose requests yourself; confirm with the user before sending.
For bulk delete/move, confirm count first.

### 4. Present results

See [references/output-format.md](references/output-format.md). Errors: [references/error-handling.md](references/error-handling.md).

## Browser fallback

See [references/browser-fallback.md](references/browser-fallback.md) and skill `browser-session-assist`.
