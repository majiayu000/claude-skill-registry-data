---
name: imap-watchdog
description: "Build silent IMAP email watchdogs that check Gmail for new messages from specific senders, track state across runs, cross-reference Sent folder, create drafts, and output Discord-formatted reports."
version: 1.0.0
author: Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [imap, email, watchdog, gmail, cron, discord, notification]
    triggers: [email watchdog, imap monitor, gmail check, builder email, email alert, draft response, silent watchdog]
    related_skills: [discord-report-format, cronjob]
---
# IMAP Email Watchdog Pattern

Build silent `no_agent` cron jobs that monitor a Gmail inbox for new messages from known contacts, skip already-handled threads, and optionally draft responses.

## Architecture

```
cron job (no_agent: true)
  └── script.py (stdout delivered to Discord on change)
       ├── IMAP connect → UID search (INBOX)
       ├── Filter: known senders, skip auto-replies
       ├── Cross-reference: Sent folder for existing replies
       ├── Draft: save to [Gmail]/Drafts (optional)
       ├── Track: persist UID + Message-ID state
       └── Output: Discord markdown or silent exit
```

## Core Pattern

### 1. State Tracking (never re-report)

Use a persistent JSON state file for two pieces of data:

```
.builder_watchdog_state.json
{
  "last_uid": 15432,       # Highest IMAP UID processed
  "reported_ids": [...]    # Last 500 Message-IDs already reported
}
```

**Key methods:**
```python
def load_state(key, default=None):
    sf = os.path.join(SCRIPT_DIR, ".watchdog_state.json")
    if os.path.exists(sf):
        try:
            with open(sf) as f:
                return json.load(f).get(key, default)
        except Exception:
            pass
    return default

def save_state(key, value):
    sf = os.path.join(SCRIPT_DIR, ".watchdog_state.json")
    state = {}
    if os.path.exists(sf):
        try:
            with open(sf) as f:
                state = json.load(f)
        except Exception:
            pass
    state[key] = value
    with open(sf, "w") as f:
        json.dump(state, f)
```

### 2. UID-Based Search (performance)

Use IMAP UIDs instead of date-based search. UIDs are monotonically increasing and persist across sessions.

```python
mail.select("INBOX")
# Only search recent messages for speed
since = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%d-%b-%Y")
status, uid_data = mail.uid("search", None, f'(SINCE {since})')
uid_list = uid_data[0].split()
new_uids = [u for u in uid_list if int(u) > last_uid]
```

**Performance rules:**
- Limit search to last 7 days (not ALL)
- Cap at 30 newest UIDs per run
- Fetch headers first (lightweight), full body only for qualifying emails
- Add a timeout check: `if time.time() - start_time > 90: break`
- Each UID fetch should use `(BODY.PEEK[HEADER.FIELDS (...)]`) for headers

### 3. Sent Folder Cross-Reference

Check `[Gmail]/Sent Mail` for replies to the same thread to avoid re-drafting:

```python
def check_replied_in_sent(mail, thread_id, from_addr):
    """Returns True if we've already replied to this thread."""
    mail.select('"[Gmail]/Sent Mail"')
    # Strategy 1: Search by thread reference ID
    if thread_id and len(thread_id) > 8:
        status, data = mail.search(None, f'TEXT "{thread_id[:40]}"')
        if status == "OK" and data[0].split():
            mail.select("INBOX")
            return True
    # Strategy 2: Search by recipient email
    addr_match = re.search(r'<?([\w.+-]+@[\w.-]+)>?', from_addr)
    if addr_match:
        status, data = mail.search(None, f'TO "{addr_match.group(1)}"')
        if status == "OK" and data[0].split():
            mail.select("INBOX")
            return True
    mail.select("INBOX")
    return False
```

### 4. Auto-Reply Filtering

Skip delivery status, out-of-office, and auto-reply emails:

```python
sl = subject.lower()
if any(k in sl for k in [
    "out of office", "auto-reply", "auto reply", "automatic reply",
    "delivery status", "returned mail", "undelivered", "mailer-daemon",
]):
    continue
```

### 5. Body Extraction with Quote Stripping

```python
def extract_body(msg, max_chars=600):
    """Get clean body, stripping quoted replies."""
    # ... get raw body from message ...
    lines = []
    in_quote = False
    for line in body.split("\n"):
        s = line.strip()
        if s.startswith(">") or re.match(r"^On\s+.+\s+wrote:$", s):
            in_quote = True; continue
        if re.match(r"^(Sent from|Get Outlook|Disclaimer)", s, re.I):
            in_quote = True; continue
        if s == "":
            in_quote = False; continue
        if not in_quote:
            lines.append(s)
    text = " ".join(lines) if lines else body
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(". ", 1)[0] + "."
    return text
```

### 6. Draft Creation via IMAP APPEND

Save draft responses directly to `[Gmail]/Drafts`:

```python
def create_draft_mail(to_addr, subject, reply_body, in_reply_to=None, references=None):
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{SENDER_NAME} <{EMAIL_ADDR}>"
    msg["To"] = to_addr
    msg["Subject"] = f"Re: {subject.removeprefix('Re: ')}"
    msg["Date"] = formatdate(localtime=True)
    if in_reply_to:
        msg["In-Reply-To"] = in_reply_to
    if references:
        msg["References"] = references
    msg.attach(MIMEText(reply_body, "plain", "utf-8"))
    return msg

def save_draft(mail, msg):
    mail.select("[Gmail]/Drafts")
    status, _ = mail.append("[Gmail]/Drafts", "\\Draft", None, msg.as_bytes())
    mail.select("INBOX")
    return status == "OK"
```

### 7. Silent Watchdog Output

When nothing new is found, produce **zero stdout** (the cron scheduler delivers nothing in `no_agent` mode). When there IS something to report, format per the `discord-report-format` skill. No blank lines between items.

```python
# Example: only print when there's new data
if not new_replies:
    return  # silent exit

parts = [f"\u2757 **Report | {count} new**"]
parts.append("\u2500" * 40)
# ... items with no blank lines between them ...
parts.append("\u2500" * 40)
parts.append(f"\U0001F50D Checked {timestamp}")
print("\n".join(parts))
```

## Pitfalls

- **IMAP SECURITY**: Gmail requires an App Password. Store in the script or pass via env var. Do not use your main Google password.
- **UID vs SEQ**: Always use `mail.uid()` methods (UID-based), not bare `mail.search()` (sequence-number-based). UIDs are stable across sessions.
- **Sent folder name**: May be `[Gmail]/Sent Mail` (most providers), `[Gmail]/Sent`, or just `Sent`. Gmail's English name is `[Gmail]/Sent Mail`.
- **Drafts folder name**: `[Gmail]/Drafts` for Gmail. Other providers may vary.
- **Rate limiting**: Gmail IMAP allows ~2000 connections per day. A 30-minute watchdog uses 48/day. Keep it under 200 for safety.
- **Timeout guard**: Gmail IMAP can stall on slow connections. Set per-operation timeouts and a global wall-clock timeout (90s recommended).
- **State file corruption**: JSON state files can corrupt on crash. Use atomic write (write to temp, rename) for production.
- **Encoding issues**: Always use `errors="replace"` when decoding email payloads. Some emails have malformed charset headers.
- **Multi-part email bodies**: Walk parts and prefer text/plain over text/html. Fall back to HTML cleaning if no plain text is found.

## Cron Setup

```yaml
# In config.yaml cron job definition:
cronjob action='create' \
  name='Builder Email Watchdog' \
  schedule='every 30m' \
  script='watch_builder_emails.py' \
  no_agent=true \
  deliver='origin'
```

The script path must resolve under `~/AppData/Local/hermes/scripts/` (relative) or be an absolute path.
