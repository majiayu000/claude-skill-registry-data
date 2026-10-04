---
name: apple-mail
description: Use when asked to check, search or read email, including finding old messages in a large or multi-account archive, or listing and saving attachments. Covers live Mail.app queries via AppleScript and searching the on-disk .emlx store directly, with Mail.app closed. READ ONLY — no sending or modifying emails.
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/agent-skills
  version: "1.3.0"
---

# Apple Mail (Read Only)

Read email two ways: **Mail.app AppleScript** for live state and attachments, and
**`ripgrep` over the on-disk `.emlx` files** for searching large archives.
**No sending or modifying emails.**

## Prerequisites

**AppleScript path:**

- Mail.app running and logged in
- Automation permissions granted (System Settings → Privacy & Security → Automation → Terminal/Claude Code → Mail)
- If first access attempt times out, ask user to check for macOS permission dialog

**Archive-search path:** Full Disk Access for the calling terminal app (System
Settings → Privacy & Security → Full Disk Access). Mail.app need not be running.

## Reliability: always wrap osascript with timeout + retry

Apple Mail's AppleScript bridge hangs intermittently — sometimes for minutes — even on simple queries. The AppleScript-internal `with timeout of N seconds` does NOT kill a wedged osascript process. **Always wrap calls with shell-level `timeout` and retry on failure.**

Pattern:

```bash
# Run osascript with 15s shell timeout, retry up to 3 times with 2s backoff.
mail_query() {
  local script="$1" attempt
  for attempt in 1 2 3; do
    result=$(timeout 15 osascript -e "$script" 2>&1) && { echo "$result"; return 0; }
    sleep 2
  done
  echo "ERROR: Mail query failed after 3 attempts" >&2
  return 1
}

# Usage: per-account queries only — see "Do not query `inbox` directly" below.
mail_query 'tell application "Mail" to return unread count of mailbox "INBOX" of account "ACCOUNT"'
```

Reasonable defaults for a single small account: **15s timeout, 3 retries, 2s
sleep**. A large IMAP account (thousands of messages) needs much more for any
query that *enumerates* messages — measured up to ~90s for one `whose` count on
a ~2400-message Gmail INBOX. `${CLAUDE_SKILL_DIR}/scripts/mail-across-accounts.sh`
(below) already budgets 120s per call for this. If all retries fail, report the
failure and move on — never block a briefing on Mail.

**Prefer a property read over a `whose` clause wherever one exists.** `unread
count` is served from Mail's own index and does not walk the mailbox; `count
(messages … whose read status is false)` walks every message. This is not a
micro-optimisation — see the wedge measurement below.

## Do not query `inbox` directly

`inbox` (unqualified, no account) is unified in **membership** — it does
contain every account's mail — but not in **order**: it is grouped
contiguously by account, newest-first only *within* each account's segment,
in an order unrelated to account-creation order. `message 1 of inbox` is
therefore the newest message in whichever account happens to sort first, not
the newest message overall — this is how a positional read of `inbox` ends up
silently covering one account. Worse, a `whose` clause over `inbox` (e.g.
`whose read status is false`) has to walk every account and can exceed
AppleScript's 120s event timeout on a large multi-account store, failing
with `-1712` outright rather than just being slow. Measured 2026-09-07: that
query did not return within 90s and left Mail.app **wedged** — every
subsequent query timed out until `killall Mail && open -a Mail`. Treat it as
a hang risk, not a latency cost.

### The one exception: `unread count of inbox`

The ban above is about *enumeration and ordering*, so it does not apply to
`unread count of inbox`, which is a property read. Measured on the same store,
same day:

| query | result | time |
|---|---|---|
| `unread count of inbox` | 2243 | 0.11s |
| `count (messages of inbox whose read status is false)` | — | no answer in 90s, wedged Mail |

It is also **correct**, checked rather than assumed: the five per-account
property reads (OFFICE 0, mfa 492, iCloud 152, Gmail 1599, KTE 0) sum to
exactly 2243, and on the two accounts small enough to test both ways the two
forms agreed (KTE 0, iCloud 152). So for a *total unread number* the unified
property is the right call. Per-account iteration is still required whenever
you need the messages themselves — which account a message belongs to, or any
positional read — because that is what the ordering bug breaks.

Every recipe below queries a named account's mailbox instead. Use
`${CLAUDE_SKILL_DIR}/scripts/mail-across-accounts.sh` for the common jobs
(it iterates accounts sequentially, with per-call timeout + retry already
handled) or the inline per-account pattern shown in each recipe.

## Account & Machine Context

See `docs/email-accounts.md` for which accounts are configured on which machines.

## Commands

### List accounts

```bash
osascript -e 'tell application "Mail" to get name of every account'
```

### Count unread messages (all accounts)

```bash
"${CLAUDE_SKILL_DIR}/scripts/mail-across-accounts.sh" unread
```

Prints one `account, unread, total` row per account plus a `TOTAL` row. An
account whose query fails is reported as `ERROR` on stderr and excluded from
`TOTAL` — never silently counted as 0, since that is indistinguishable from
"actually empty". Single account, inline:

```bash
osascript -e 'tell application "Mail" to return unread count of mailbox "INBOX" of account "ACCOUNT"'
```

### Recent messages across all accounts (last 10)

```bash
"${CLAUDE_SKILL_DIR}/scripts/mail-across-accounts.sh" recent 10
```

Collects the newest messages from each account and merge-sorts by date, so
this is the 10 most recent messages overall — not the 10 most recent in
whichever account happens to come first. Single account, inline:

```bash
osascript -e 'tell application "Mail"
  set recentMsgs to messages 1 thru 10 of mailbox "INBOX" of account "ACCOUNT"
  repeat with msg in recentMsgs
    set msgInfo to "From: " & (sender of msg) & " | Subject: " & (subject of msg) & " | Date: " & (date sent of msg)
    log msgInfo
  end repeat
end tell'
```

### Get message content by index

Message 1 is the most recent **within that account's mailbox**, not overall —
find the account and index first (`recent` above, or `search` below), then
read it:

```bash
osascript -e 'tell application "Mail"
  set msg to message 1 of mailbox "INBOX" of account "ACCOUNT"
  return "From: " & (sender of msg) & "\nSubject: " & (subject of msg) & "\nDate: " & (date sent of msg) & "\n\n" & (content of msg)
end tell'
```

### Search messages by subject (all accounts)

```bash
"${CLAUDE_SKILL_DIR}/scripts/mail-across-accounts.sh" search "keyword"
```

Searches every account's INBOX; matches come back as a
`date, account, sender, subject` TSV. Single account, inline:

```bash
osascript -e 'tell application "Mail"
  set foundMsgs to (messages of mailbox "INBOX" of account "ACCOUNT" whose subject contains "keyword")
  count foundMsgs
end tell'
```

### Search and read first match (one account)

```bash
osascript -e 'tell application "Mail"
  set foundMsgs to (messages of mailbox "INBOX" of account "ACCOUNT" whose subject contains "keyword")
  if (count foundMsgs) > 0 then
    set msg to item 1 of foundMsgs
    return "From: " & (sender of msg) & "\nSubject: " & (subject of msg) & "\nDate: " & (date sent of msg) & "\n\n" & (content of msg)
  else
    return "No messages found"
  end if
end tell'
```

To find which account the match is in first, run **Search messages by
subject** above, then read it here with that account name.

### Search across all mailboxes (not just INBOX)

Only for small stores or a handful of accounts. For old mail, or once the account
count climbs, this becomes unusable — use **Searching large archives** below instead.

```bash
osascript -e 'tell application "Mail"
  set foundMsgs to (messages of every mailbox of every account whose subject contains "keyword")
  -- Can take well over a minute across many accounts and large mailboxes;
  -- see "Do not query `inbox` directly" above for the timeout this risks.
end tell'
```

### List mailboxes for an account

```bash
osascript -e 'tell application "Mail" to get name of every mailbox of account "Gmail"'
```

### List attachments

Find the account first (`search` above), then, one account at a time:

```bash
osascript -e 'tell application "Mail"
  set msg to item 1 of (messages of mailbox "INBOX" of account "ACCOUNT" whose subject contains "invoice")
  set out to ""
  repeat with a in (mail attachments of msg)
    set out to out & (name of a) & " [" & (file size of a) & " bytes]" & linefeed
  end repeat
  return out
end tell'
```

### Save attachments

Build the file target **outside** the `tell` block — via a handler called with `my`, so it still works inside a loop. This example is scoped to one account; run once per account (or loop over `mail-across-accounts.sh accounts`) if the message could be in any of them:

```bash
osascript <<'EOF'
on posixTarget(p)
  return POSIX file p
end posixTarget

set outDir to "/tmp/attachments/"   -- must already exist
tell application "Mail"
  repeat with m in (messages of mailbox "INBOX" of account "ACCOUNT" whose subject contains "invoice")
    repeat with a in (mail attachments of m)
      save a in (my posixTarget(outDir & (name of a)))
    end repeat
  end repeat
end tell
EOF
```

`outDir` must already exist — `save` into a missing directory fails with the uninformative `-10000 AppleEvent handler failed`, which says nothing about the path. `mkdir -p` first.

Attachment names often contain `:` (e.g. `SOA-2026-08-02-12:20:06.xlsx`). It saves fine, but Finder and many tools render it as `/` — sanitize with `text item delimiters` if the name is going anywhere else.

Fallback: `source of msg` returns the raw MIME, so Python's `email` module can extract parts without AppleScript at all. Useful when a mailbox is wedged or names need heavy cleanup.

That fallback still goes through Mail. To skip it entirely, the same message is already on disk as an `.emlx` file — see **Searching large archives** below, which parses it with the same `email` module and no `tell` block at all.

## Gotchas inside `tell application "Mail"`

Both of these have one root cause: **unqualified terms resolve against Mail's dictionary, not AppleScript's.**

**1. `POSIX file` fails.** Written inside the block it errors `-1728 Can't get POSIX file "…"` — Mail tries to resolve it as one of its own objects. Coerce outside the block or via `my` (see above). Note the error names the path, so it reads like a missing-file problem; it isn't.

**2. Ordinary variable names are reserved.** These all fail inside the block, with `-10003`, `-10006`, or the unguessable `Can't set «constant ldaslsba» to …`:

`base` · `name` · `subject` · `content` · `file` · `path` · `index` · `size` · `date` · `text` · `character`

Prefix them — `basePath`, `msgSubject`, `outFile`. The failure is a *syntax* error at compile time for some (`base`, `file`, `date`, `text`, `character`) and a *runtime* error for others (`name`, `subject`, `content`, `index`, `size`), so a script can parse cleanly and still blow up mid-loop.

## Searching large archives

**Use this path to find old mail, or when the account count is high.** Cross-account
AppleScript search degrades badly as accounts accumulate, and the bridge hangs
intermittently besides (see *Reliability: always wrap osascript with timeout +
retry*).

The two paths are complements, not rivals — AppleScript still owns live state
(unread counts, recent inbox, account and mailbox names) and attachment
extraction, which the on-disk path cannot do. Use this one to *locate* a message
across a large archive; use AppleScript to act on it once found.

Mail stores each message as an `.emlx` file under `~/Library/Mail/`, so `ripgrep`
searches the whole archive directly. This is read-only: it never opens Mail.app.

### 1. Confirm the store is readable — do this first

Both of the failure modes below return **zero results, not an error**. Establish
that you can actually read the files before believing any empty result:

```bash
rg --files ~/Library/Mail -g '*.emlx' | wc -l
```

A count of 0, or a permission error, means the search is blind — not that the
archive is empty. Reading `~/Library/Mail` requires **Full Disk Access** for the
calling terminal app (System Settings → Privacy & Security → Full Disk Access).

### 2. Search

```bash
rg -il --no-messages 'search\.term' ~/Library/Mail -g '*.emlx' > /tmp/matches.txt
wc -l < /tmp/matches.txt
```

- Search `~/Library/Mail`, not `~/Library/Mail/V10` — the version directory changes
  across macOS releases and more than one can coexist.
- `-g '*.emlx'` **already includes `*.partial.emlx`**; no second glob is needed.
- Use `-F` for a literal term. Email addresses and domains contain regex
  metacharacters (`.`, `+`), so `rg -ilF 'name+tag@example.com'` avoids surprises.
- Drop `--no-messages` on the first run. It suppresses genuine read errors, which
  is exactly how a permissions problem disguises itself as "no such mail."

### 3. Triage the hits

Do not pull headers out with `grep`. Roughly a quarter of `Subject:` headers are
MIME-encoded (`=?UTF-8?B?...?=`) and a fifth are folded across continuation lines,
so a line-oriented `grep`/`cut` pipeline returns mojibake and truncated subjects.
The bundled parser decodes both:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/emlx.py" list < /tmp/matches.txt
```

Prints one TSV row per message — `UTC date, from, subject, flags, path` — sorted
oldest first. The date column is UTC precisely so it stays sortable with `sort`.

### 4. Read one message

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/emlx.py" show /path/to/123.emlx
```

Decoded headers plus the body, preferring `text/plain` and falling back to
`text/html` — a tenth of messages have no plain-text part at all, so a
plain-text-only extraction silently prints nothing for them.

### `.emlx` format

A byte-count line, then the RFC822 message, then an XML plist trailer. The count
is why the message must be sliced out before parsing rather than fed to an
RFC822 parser whole.

### `*.partial.emlx` — include them

Mail writes `.partial.emlx` when it has not downloaded the entire message. They
can be a large share of the archive, and **they are worth searching**: headers and
text body are normally present and intact.

What they lack is attachment payloads. Such a part keeps its headers and carries
`X-Apple-Content-Length`, but its body is empty — measured here as attachments only
(`application/pdf`, `image/png`, `image/jpeg`, `application/pgp-signature`). So a
term that exists only inside an attachment will not match locally. `emlx.py` flags
these as `NOT-DOWNLOADED:<type>`; open the message in Mail.app to fetch the rest.

Note this bounds what a local grep can find in general: attachment text is
base64-encoded even in fully-downloaded messages, so it never matches a plaintext
search regardless. Searching *inside* attachments is a separate job — extract them
first with **Save attachments** above, then search the extracted files.

### Spotlight does not work here

```bash
mdfind -onlyin ~/Library/Mail 'some term you know exists'   # → 0
```

`~/Library/Mail` is not Spotlight-indexed on current macOS. **`mdfind` returns 0
for every query, and 0 reads as "no such mail" when it actually means "no index."**
Do not use `mdfind` to conclude a message does not exist, and do not treat its
silence as evidence.

Volume-level indexing being enabled is not evidence the mail store is indexed —
these two commands distinguish the cases in seconds:

```bash
mdutil -s /                                          # "Indexing enabled." — volume is fine
mdls -name kMDItemTextContent /path/to/some.emlx     # (null) — yet no text was indexed
```

## Common Mistakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `mdfind -onlyin ~/Library/Mail` returns 0 | The Mail store is not Spotlight-indexed — never a negative result | Search the `.emlx` files with `rg`; confirm with `mdls -name kMDItemTextContent` |
| `rg` over `~/Library/Mail` returns 0 | No Full Disk Access, and `--no-messages` hid the errors | Run `rg --files ~/Library/Mail -g '*.emlx' \| wc -l` first; grant Full Disk Access |
| Subjects appear as `=?UTF-8?B?...?=` | Raw `grep` does not decode MIME-encoded headers | Use `emlx.py list` |
| Subject is cut off mid-sentence | Header folded onto a continuation line; `grep -m1` took only the first | Use `emlx.py list` |
| Message found, but body prints empty | Message has no `text/plain` part | Use `emlx.py show`, which falls back to `text/html` |
| Term is known to be in the mail but does not match | It lives in an attachment — absent in `.partial.emlx`, base64 elsewhere | Extract via **Save attachments**, then search those files; check for the `NOT-DOWNLOADED` flag |
| Cross-account AppleScript search hangs | Impractical across many accounts | Use **Searching large archives** |
| `-1728 Can't get POSIX file "…"`, or `Can't set «constant ldaslsba» to …` | Unqualified terms resolve against Mail's dictionary | See **Gotchas inside `tell application "Mail"`** |
| Unread/message count looks implausibly low for a known-active account | Read `message 1 of inbox`, or a `whose` filtered on unqualified `inbox` — see **Do not query `inbox` directly** | Query `mailbox "INBOX" of account "NAME"`, or use `mail-across-accounts.sh` |
| `-1712 AppleEvent timed out` on a `whose` query | The query ran over unqualified `inbox`, which fans out to every account | Same fix — scope to one account, or use `mail-across-accounts.sh` |
| Several `osascript` calls issued at once all time out | Mail's AppleScript bridge serializes; concurrent calls contend | Iterate accounts sequentially, one `osascript` call at a time |

## Notes

- `inbox` (unqualified) is unified in *membership* across accounts but not in
  *order* — see **Do not query `inbox` directly**. Query a named account's
  mailbox instead.
- Messages are indexed newest-first **within one account's mailbox only**;
  there is no single index that is newest-first across accounts
- `content of msg` returns plain text body; `source of msg` returns raw MIME
- Large mailboxes can be slow — use `whose` clauses to filter
- Timeout: a `with timeout of N seconds` wrapper only raises AppleScript's
  *internal* event timeout — it does not recover a wedged `osascript`
  process. Always pair it with a shell-level `timeout` (see **Reliability**)

## Self-Improvement

If you encounter an AppleScript pattern that fails, a macOS behavior change, or missing guidance in this skill, don't just work around it — fix the skill:

1. **Create a PR** from a fresh worktree of `https://github.com/eins78/agent-skills` on a new branch, fixing the issue directly
2. **Or file an issue** on `https://github.com/eins78/agent-skills` with: what failed, the actual behavior, and the suggested fix

Never silently work around a skill gap. The fix benefits all future sessions.
