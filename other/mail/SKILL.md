---
name: Mail
description: Execute email operations with platform-specific optimizations and security protocols.
author: 무펭이 🐧
---

## Platform Detection & Routing

**macOS**: Use Apple Mail SQLite queries (100x faster than AppleScript).

**Cross-platform**: Use himalaya CLI for full IMAP/SMTP operations.

**Never mix approaches** in same task. Commit to one to avoid state conflicts.

## Apple Mail SQLite Gotchas

**Query path**: `~/Library/Mail/V*/MailData/Envelope\ Index`

**Key tables**: `messages` (subject, sender, date_received), `addresses`, `mailboxes`.

**Force sync first**: `osascript -e 'tell app "Mail" to check for new mail'`. SQLite reads stale data otherwise.

**Recent mail filter**: `WHERE date_received > strftime('%s','now','-7 days')`

**Join pattern**: messages→addresses on `message_id` for sender lookup.

**Attachments**: Check `messages.attachment_count > 0`, files in `~/Library/Mail/V*/MAILBOX/Messages/`.

## himalaya CLI Patterns

**Install**: `cargo install himalaya` or `brew install himalaya`.

**Always use**: `--output json` flag for programmatic parsing.

**List emails**: `himalaya envelope list -o json` (NOT `message list`).

**Folder operations**: `himalaya message move <id> <folder>` - folder names are case-sensitive.

**Cache refresh**: Run `himalaya folder list` after server-side folder changes.

## Send Protocol

**Draft-review-send workflow**: Compose → show user full content → send after explicit OK.

**Reply threading**: Include `In-Reply-To` and `References` headers or thread breaks.

**himalaya send**: `himalaya message send` reads RFC 2822 from stdin.

**SMTP rejection**: Some servers reject if From header doesn't match authenticated user.

## Credential Management

**macOS Keychain**: `security add-internet-password -s imap.gmail.com -a user@gmail.com -w 'app-password'`

**Gmail/Google Workspace**: Requires App Password with 2FA enabled, NOT regular password.

**OAuth tokens**: himalaya supports XOAUTH2 via token_cmd in config.toml.

## Thread Intelligence

**Thread by In-Reply-To chain**, not subject matching. "Re:" prefix is unreliable.

**Polling intervals**: 15-30 min max. Use `himalaya envelope watch` for real-time when available.

---
> 🐧 Built by **무펭이** — [무펭이즘(Mupengism)](https://github.com/mupeng) 생태계 스킬
