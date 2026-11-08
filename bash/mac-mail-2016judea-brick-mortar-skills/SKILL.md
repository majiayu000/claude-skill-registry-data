---
name: mac-mail
description: Search and read the email Apple Mail has downloaded to your Mac, straight from its local Envelope Index and .emlx files, read-only. Use when asked "find the invoice from Acme last month", "what did the landlord email about the deposit", "show unread mail from this week", "pull the attachments off that message", or "export this email thread". Works for every account Mail.app syncs (iCloud, Gmail, Exchange, IMAP) with no login or API.
compatibility: macOS; reads local files only; needs Full Disk Access
---

# Mac Mail (local, read-only)

`scripts/mail.py`, Python 3 stdlib only. Search the index first, then open a message by its id.

```bash
python3 scripts/mail.py mailboxes
python3 scripts/mail.py search --from acme --since 2026-09-01 --attachments
python3 scripts/mail.py search --subject invoice --mailbox Inbox --limit 50
python3 scripts/mail.py search --text "security deposit" --unread
python3 scripts/mail.py search --to dana@example.com
python3 scripts/mail.py read 48213                  # headers + plain-text body (--html for raw HTML)
python3 scripts/mail.py attachments 48213 --save ./out
python3 scripts/mail.py thread 48213 --md thread.md  # whole conversation, oldest first
```

Search rows look like `48213 *!  2026-09-14 09:02  Acme Billing <billing@example.com>  Invoice 1042  [INBOX]`
(`*` unread, `!` flagged; the first column is the id).

## Where the data is

- `~/Library/Mail/V<n>/MailData/Envelope Index`: SQLite index of every message. `V10` on current
  macOS; the script takes the highest `V*`. Never hard-code it.
- `~/Library/Mail/V<n>/<account-uuid>/<Mailbox>.mbox/<uuid>/Data/<d>/<d>/Messages/<ROWID>.emlx`:
  the message itself. The id from the index is the file name.
- Attachments of a `.partial.emlx` sit beside it in `.../Data/<d>/<d>/Attachments/<ROWID>/<part>/<file>`.

Index joins: `messages.sender` -> `addresses`, `messages.subject` -> `subjects`,
`messages.mailbox` -> `mailboxes.url`, `messages.summary` -> `summaries` (the preview text),
`recipients(message, address, type)` with type 0 = To, 1 = Cc, `attachments(message, name)`,
`messages.conversation_id` groups a thread. Dates are Unix seconds. `deleted = 1` rows are gone.

## Traps

- **.emlx is not a plain .eml.** Line 1 is the byte length of the RFC 822 message; an Apple plist
  follows it. Read exactly that many bytes after the first newline, then parse with `email`.
- **`.partial.emlx`** means Mail stripped the attachments out to the `Attachments/` folder. A tool
  that only parses MIME parts reports "no attachments".
- **Gmail paths contain `[Gmail]`**, which `glob` treats as a character class. Use `glob.escape`.
- **Gmail labels duplicate messages.** One email sits in All Mail plus each label's mailbox; the
  thread command dedupes by Message-ID.
- **Bodies only exist if Mail downloaded them.** With "Download attachments: None" or a new account,
  the index row exists but the file does not; `read` falls back to the preview summary and says so.
- **Body text search is only over the stored preview** (`summaries`, the first few lines). For a
  full-text hunt, filter with `search` first, then `read` the candidates; or use Spotlight
  (`mdfind -onlyin ~/Library/Mail "kMDItemTextContent == '*phrase*'"`).
- Mailbox urls are percent-encoded (`%5BGmail%5D/All%20Mail`); match on the decoded name.

## Permission (TCC)

`~/Library/Mail` requires Full Disk Access: System Settings > Privacy & Security > Full Disk Access >
add the app running the agent, then restart it. Without it, `Envelope Index` will not open.

## Limits

Read-only; sending or moving mail needs Mail.app or AppleScript. Only mail Mail.app has synced to
this Mac is visible. For Gmail via API instead of Mail.app, use a Gmail skill.
