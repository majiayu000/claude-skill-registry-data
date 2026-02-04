---
name: jean-claude
description: "This skill should be used when the user asks to search/send/draft email, check calendar, create events, schedule meetings, find/upload/share Drive files, read/edit Google Docs, read spreadsheet data, send texts/iMessages, send WhatsApp messages, send Signal messages, check messages, or create reminders. Manages Gmail, Google Calendar, Google Drive, Google Docs, Google Sheets, iMessage, WhatsApp, Signal, and Apple Reminders."
---

# jean-claude - Gmail, Calendar, Drive, Docs, Sheets, iMessage, WhatsApp, Signal & Reminders

Manage Gmail, Google Calendar, Google Drive, Google Docs, Google Sheets,
iMessage, WhatsApp, Signal, and Apple Reminders using the CLI tools in this plugin.

**Command prefix:** `uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude `

## What This Does (For First-Time Users)

When a user asks about email, calendar, or messages and hasn't used jean-claude
before, explain briefly:

> I can connect to your email, calendar, and messaging apps to help you:
>
> - Read and send emails, manage drafts
> - Check your calendar, create events, respond to invitations
> - Send and read iMessages, WhatsApp, or Signal messages
> - Find and manage files in Google Drive
> - Create reminders
>
> This requires a one-time setup where you'll grant permissions. Want me to
> help you get started?

Don't overwhelm new users with service lists. Focus on what they asked about.
If they asked "can you check my email?", mention email capabilities. If they
asked about calendar, focus on that.

## Session Start (Always Run First)

**Every time this skill loads, run status with JSON output first:**

```bash
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude status --json
```

### If Status Command Fails

If the status command fails entirely (not just showing services as disabled):

**"uv: command not found"** — The uv package manager isn't installed. Tell the
user:

> jean-claude requires the `uv` package manager. Let me install it for you.

Then run:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After installation, restart the terminal or source the shell config
(`source ~/.zshrc` on macOS, `source ~/.bashrc` on Linux).

**Other errors** — The plugin may be misconfigured. Check that
`${CLAUDE_PLUGIN_ROOT}` resolves to a valid path containing a `pyproject.toml`.

### Branching Based on Status

**If `setup_completed: false`** — This is a new user. Skip personalization
skills (they won't have any yet) and go straight to onboarding:

```bash
cat ${CLAUDE_PLUGIN_ROOT}/skills/jean-claude/ONBOARDING.md
```

Follow the onboarding guide to help set up services. After setup completes:

```bash
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude config set setup_completed true
```

Then **re-run status** and continue to the `setup_completed: true` branch below.
This ensures you have fresh status info and can proceed with the user's original
request.

**If `setup_completed: true`** — Check for partial setup and load personalization:

1. **Check for missing services** — Look at `services.<name>` in the JSON. If
   the user asks for a service that shows `authenticated: false` or
   `enabled: false`, guide them through just that service's setup from
   ONBOARDING.md. After partial setup completes, continue to step 2.

2. **Load personalization skills** — Check if user skills like `managing-messages`
   exist (look at available skills for anything mentioning inbox, email, message,
   or communication). If found, load them—user preferences override defaults.

3. **Offer to create preferences** — If no personalization skill was found in
   step 2, offer to create one after completing the user's immediate request.
   See [PREFERENCES.md](PREFERENCES.md) for the creation flow. Don't interrupt
   the user's task—help them first, then offer.

4. **Proceed with the user's request** — Execute whatever task prompted loading
   this skill (check inbox, send message, etc.).

### Understanding the Status

For users with setup complete, interpret the status output to understand their
workflow. Run human-readable status if needed for counts:

```bash
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude status
```

**Gmail:**
- **13 inbox, 11 unread** → inbox zero person, wants to triage everything
- **2,847 inbox, 89 unread** → not inbox zero, focus on recent/unread/starred
- **5 drafts** → has pending drafts to review or send

**Calendar:**
- **3 today, 12 this week** → busy schedule, may need help with conflicts
- **0 today** → open day, good time for focused work

**Reminders:**
- **7 incomplete** → has pending tasks, may want to review or complete them

**Messaging:**
- **54 unread across 12 WhatsApp chats** → active messaging, may want summary
- **1,353 unread across 113 iMessage chats** → backlog, focus on recent/important

### Refreshing State

When users ask for updates ("what's new", "anything else in my inbox", "check my
messages again"), re-fetch current data rather than working from earlier results.
Inbox state changes constantly — new emails arrive, messages get read on other
devices.

```bash
# Re-fetch inbox for email updates
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail inbox -n 20

# Re-sync WhatsApp for message updates
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude whatsapp messages --unread
```

## Safety Rules (Non-Negotiable)

These rules apply even if the user explicitly asks to bypass them:

1. **Never send an email without explicit approval.** Show the full email
   (recipient, subject, body) to the user and receive explicit confirmation
   before calling `jean-claude gmail draft send`.

2. **Limit bulk sending.** Avoid sending emails to many recipients at once.
   Prefer drafts for review.

3. **Load prose skills when drafting.** Before composing any email or message,
   load any available skills for writing prose, emails, or documentation.

4. **Never send an iMessage without explicit approval.** Show the full message
   (recipient, body) to the user and receive explicit confirmation before
   calling `jean-claude imessage send`.

5. **Double-check iMessage recipients.** iMessage sends are instant and cannot
   be undone. Verify the phone number or chat ID before sending.

6. **Never send to ambiguous recipients.** When resolving contacts by name,
   if multiple contacts or phone numbers match, the command will fail with a
   list of options. This is intentional—always use an unambiguous identifier
   (full name or phone number) rather than guessing.

7. **Never send a WhatsApp message without explicit approval.** Show the full
   message (recipient, body) to the user and receive explicit confirmation
   before calling `jean-claude whatsapp send`.

8. **Verify WhatsApp recipients carefully.** WhatsApp sends are instant and
   cannot be undone. Always confirm the phone number before sending.

9. **Never send a Signal message without explicit approval.** Show the full
   message (recipient, body) to the user and receive explicit confirmation
   before calling `jean-claude signal send`.

10. **Verify Signal recipients carefully.** Signal sends are instant and cannot
    be undone. Always confirm the recipient UUID before sending.

**Email workflow:**

1. Load any available prose/writing skills
2. **If replying to an infrequent contact:** Research first (see "Composing Correspondence")
3. Compose the email content (iterate internally before presenting)
4. Show the user: To, Subject, and full Body
5. Ask: "Send this email?" and wait for explicit approval
6. Call `jean-claude gmail draft send DRAFT_ID`
7. If replying, archive the original: `jean-claude gmail archive THREAD_ID`

**iMessage workflow:**

1. Load prose skills if composing a longer message
2. Compose the message content
3. Show the user: Recipient (phone or chat name) and full message
4. Ask: "Send this message?" and wait for explicit approval
5. Pipe message body to `jean-claude imessage send RECIPIENT`

**WhatsApp workflow:**

1. Load prose skills if composing a longer message
2. Compose the message content
3. Show the user: Recipient (phone number with country code) and full message
4. Ask: "Send this WhatsApp message?" and wait for explicit approval
5. Pipe message body to `jean-claude whatsapp send RECIPIENT`

**Signal workflow:**

1. Load prose skills if composing a longer message
2. Compose the message content
3. Show the user: Recipient (name or UUID) and full message
4. Ask: "Send this Signal message?" and wait for explicit approval
5. Pipe message body to `jean-claude signal send RECIPIENT`

## Personalization

**After setup is complete**, load personalization skills before messaging actions.

This step is handled in the "Branching Based on Status" section above. If you
already loaded personalization skills during session start, skip this section.

If you're returning to messaging after doing other tasks in the same session,
check if personalization skills were loaded. If not:

1. **List available skills** — check descriptions for skills mentioning:
   inbox, email, message, communication, contacts, or similar
2. **Load matching user skills** using the Skill tool BEFORE proceeding
3. **Only then** fetch messages or compose drafts

User skills override any defaults below. They may define:
- Priority contacts and relationships
- Triage rules (what to archive, what needs attention)
- Response tone and style
- Default message counts

Use these defaults in lieu of any user preferences:

### Email Defaults
- Fetch both read and unread messages (context helps)
- Present messages neutrally — don't assume priority
- No automatic archiving without user guidance

### iMessage Defaults
- Prioritize known contacts over unknown senders

### Response Drafting Defaults
- Load prose/writing skills before composing
- No assumed tone or style — ask if unclear
- Show full message for approval before sending

### Presenting Messages

When showing messages (inbox, unread, search results), use a numbered list so
the user can reference items by number: "archive 1, reply to 2", "star 3 and 5".

**Always include dates conversationally.** Check today's date before formatting:

```bash
date "+%Y-%m-%d %H:%M %Z"  # Current date/time for reference
```

**Date formatting rules:**
- **< 1 hour ago**: "35 min ago" — recency is the signal
- **Today** (> 1 hour): "today at 9:15 AM" — not "3 hours ago"
- **Yesterday**: "yesterday at 2:30 PM"
- **This week**: "Thursday at 4:30 PM" (day name, not date)
- **Beyond this week**: "Dec 15" or "Nov 15 at 3pm" (if time matters)

**Why not "X hours ago" for everything recent?** Relative times answer "how
recent?" — useful for urgent/time-sensitive items. But for most messages,
the user wants to know *which day*, not do mental math. "2.5 hours ago" for
a newsletter is less useful than "this morning" or "today at 10am".

**Example** (assuming today is Sunday, Dec 29):
```
1. **DoorDash** (35 min ago) — Your order from Superba
   Order confirmed for pickup...

2. **Squarespace** (yesterday at 9:15 AM) — Domain transfer rejected
   The transfer for fitzalanhoward.uk was rejected...

3. **GitHub** (Friday at 4:30 PM) — PR merged: fix-auth-flow
   Your pull request was merged...

4. **Goodreads** (today at 10:30 AM) — Book newsletter
   Your weekly reading digest...

5. **Jordan Lee** (Nov 15) — Forwarded: Fellowship nomination
   To discuss...
```

Use "today/yesterday" and day names — these are natural mental anchors. Only
use "X minutes ago" when recency itself is actionable (< 1 hour).

### Marking Messages as Read

When you show the full body of a message to the user — not just the snippet
from a list — mark it as read. The user has effectively read it.

**Mark as read when:**
- Reading the full email body (via `gmail get` or reading the cached body file)
- Creating a reply or forward (you read the original to compose the response)
- The user explicitly asks to read a specific message

**Don't mark as read when:**
- Showing inbox/search results (snippets only)
- Listing messages without showing full content

This applies across messaging services:
- Gmail: `jean-claude gmail mark-read THREAD_ID`
- iMessage: `jean-claude imessage mark-read CHAT_ID`
- WhatsApp: `jean-claude whatsapp mark-read CHAT_ID`

### Availability Questions

When a message asks about availability ("Are you free Tuesday?", "Which works
better — the 6th or 8th?"), check the calendar and include the answer:

<example>
<bad>

```
1. Alex Chen (yesterday at 12:24 PM) — "Re: Dinner in Jan"
   He's asking: Tuesday the 6th or Thursday the 8th?
```

</bad>
<good>

```
1. Alex Chen (yesterday at 12:24 PM) — "Re: Dinner in Jan"
   He's asking: Tuesday the 6th or Thursday the 8th?
   → You're free both evenings. Thursday has a 3pm meeting that ends at 4.
```

</good>
</example>

The user shouldn't have to ask "what's on my calendar those days?" as a
follow-up. If someone's asking about dates, checking availability is the
obvious next step — do it proactively. Check calendars where the user has
events (see "Choosing the Right Calendar").

## Proactive Follow-Through

Complete tasks fully. Don't stop early and ask if you should continue.

### Research Questions

When the user asks about facts—names, relationships, dates, contact info—do the
research immediately. Don't say "I don't know" based on limited context.

- **"What's Marco's wife's name?"** → Search emails and messages from Marco, look
  for mentions of family, check calendar invites for +1s, etc.
- **"When did I last talk to Sarah?"** → Search messages and emails, report what
  you found
- **"What's Tom's phone number?"** → Search contacts, emails, messages for phone
  numbers associated with Tom

The user asked a question. They want an answer, not a report that you don't
have enough context. Use the tools available to find it.

If you search thoroughly and find nothing, say so: "I searched your emails and
messages with Marco but didn't find any family names mentioned."

<example>
<bad>

User: "What are Marco's wife & kid's names?"

Agent: "I don't know—the message from Marco didn't mention names. Want me to
search your emails or messages for more context?"

</bad>
<good>

User: "What are Marco's wife & kid's names?"

Agent: _searches emails from/to Marco, searches messages, looks for birth
announcements, wedding invites, etc._

"From your email history with Marco:
- Wife: Sofia Martinez
- Daughter: Isabella ('Bella'), born January 4, 2017"

</good>
</example>

### Reading Content

When the user asks to read or review something, include all related content:

- **"Read the email from X"** → Fetch the email, read the body, AND if it has
  attachments (PDFs, images), download and read them without asking
- **"Check my messages"** → If messages contain images, view them and describe
  what they show
- **"Look at the calendar invite"** → Open the attachment or linked document

Don't stop at metadata and ask "want me to download the attachment?" — that's
asking the user to do your job. The user said "read the email," not "list the
email's attachments."

<example>
<bad>

User: "read the amex email"

Agent: _fetches email metadata_

"The AMEX email has a PDF attachment (claim_docs.pdf, 28KB). Want me to download it?"

</bad>
<good>

User: "read the amex email"

Agent: _fetches email, downloads PDF, reads it_

"AMEX sent claim documents for #12266792. The PDF contains:
- Claim form to fill out
- Instructions to mail to [address]
- Supporting documentation requirements"

</good>
</example>

## Composing Correspondence

For infrequent contacts — people the user doesn't interact with regularly —
understand the relationship before drafting. Skip this for close friends, family,
or frequent correspondents where context is obvious.

### Research First

When replying to an infrequent contact (catching up, introductions, social
correspondence), research before drafting:

1. **Search email history** — When did they last correspond? What did they discuss?
2. **Search the web** — If unfamiliar, who is this person? What do they do?
3. **Report context** — Tell the user what you found before showing a draft

<example>
<bad>

User: "Reply to Alex's email"

Agent: _immediately drafts reply_

"Draft:
Hi Alex,
Thanks for reaching out! The AI coding tool sounds right up my alley. Happy to
connect with Jordan.
Best, Max"

</bad>
<good>

User: "Reply to Alex's email"

Agent: _searches email history and web_

"Alex Chen — you last emailed him 8 months ago about the open-source project.
He's a research scientist at a major tech company, one of the original authors.
Before that you collaborated on a conference tutorial in 2019.

His email mentions Jordan Lee, who I found on LinkedIn is a former startup
engineer now building an AI tool..."

[Then proceeds to draft with this context]

</good>
</example>

The user shouldn't need to ask "when did I last talk to them?" or "who is this
person?" — do that research proactively.

### Address the Person, Not the Issue

Customary emails — introductions, catching up, social correspondence — are about
the relationship, not transactions.

<example>
<bad>

"The AI coding tool sounds right up my alley."

Why it fails:
- Centers the user's interests, not the relationship
- The agent hasn't researched Jordan's actual work
- Transactional — jumps straight to business

</bad>
<good>

"I'm glad to see the project continues to thrive. Hope all's well with you —
would enjoy catching up soon."

Why it works:
- Reciprocal — acknowledges what matters to Alex
- Relational — about the person, not the introduction
- Warm without being hollow

</good>
</example>

**The principle:** For social correspondence, address the person before addressing
whatever they asked about.

### Iterate Before Presenting

Drafts deserve thought. Don't produce one immediately and present it.

**Internal iteration process:**

1. Research the relationship (see above)
2. Consider the tone — formal? warm? brief?
3. Draft internally, critique it: "If this email is bad, why?"
4. Revise, then present

For important correspondence, explain your reasoning or offer alternatives:
"I went with a warm but brief tone since you haven't talked in 8 months. Want
something more formal?"

### Vocabulary

Avoid hollow words that signal low engagement. Check the user's personalization
skill for specific vocabulary preferences.

**The test:** If a phrase could apply to anyone, it says nothing.

- "Nice to hear from you" → could be sent to anyone
- "I'm glad to see the project continues to thrive" → specific to this person

When drafting, ask: is this specific to this person and this relationship?

## Setup

### Prerequisites

This plugin requires `uv` (Python package manager). If not installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Google Workspace

Credentials stored in `~/.config/jean-claude/`. First-time setup:

```bash
# Full access (read, send, modify)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude auth

# Or read-only access (no send/modify capabilities)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude auth --readonly

# Check authentication status and API availability
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude status

# Log out (remove stored credentials)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude auth --logout
```

This opens a browser for OAuth consent. Credentials persist until revoked.

**If you see "This app isn't verified":** This warning appears because
jean-claude uses a personal OAuth app that hasn't gone through Google's
(expensive) verification process. It's safe to proceed:

1. Click "Advanced"
2. Click "Go to jean-claude (unsafe)"
3. Review and grant the requested permissions

The "unsafe" label just means unverified, not malicious. The app only accesses
the specific Google services you authorize.

To use your own Google Cloud credentials instead (if default ones hit the 100
user limit), download your OAuth JSON from Google Cloud Console and save it as
`~/.config/jean-claude/client_secret.json` before running the auth script. See
README for detailed setup steps.

### Feature Flags (WhatsApp & Signal)

WhatsApp and Signal are **disabled by default**. These services require
compiling native binaries (Go for WhatsApp, Rust for Signal), and we want
jean-claude to work smoothly for Gmail/Calendar users without those toolchains.
Enable explicitly if you need messaging:

```bash
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude config set enable_whatsapp true
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude config set enable_signal true
```

The `status` command shows whether each service is enabled or disabled.

### WhatsApp

WhatsApp requires enabling the feature flag, a Go binary, and QR code
authentication. First-time setup:

```bash
# Build the Go CLI (requires Go installed)
cd ${CLAUDE_PLUGIN_ROOT}/whatsapp && go build -o whatsapp-cli .

# Authenticate with WhatsApp (scan QR code with your phone)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude whatsapp auth

# Check authentication status
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude status
```

The QR code will be displayed in the terminal and saved as a PNG file. Scan it
with WhatsApp: Settings > Linked Devices > Link a Device.

Credentials are stored in `~/.config/jean-claude/whatsapp/`. To log out:

```bash
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude whatsapp logout
```

### Signal

Signal requires enabling the feature flag, a Rust binary, and QR code linking.
First-time setup:

```bash
# Build the Rust CLI (requires Rust/Cargo and protobuf installed)
cd ${CLAUDE_PLUGIN_ROOT}/signal && cargo build --release

# Link as a secondary device (scan QR code with your phone)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude signal link

# Check authentication status
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude status
```

The QR code will be displayed in the terminal. Scan it with Signal on your
phone: Settings > Linked Devices > Link New Device.

Credentials are stored in `~/.local/share/jean-claude/signal/`.

## Gmail

### Reading Emails

See "Personalization" section for default behaviors and user skill overrides.

1. **List/search** returns compact JSON with summaries and file paths
2. **Read the body file** directly with `cat` if you need the full body

**Search/Inbox response schema:**

```json
{
  "messages": [
    {
      "id": "19b29039fd36d1c1",
      "threadId": "19b29039fd36d1c1",
      "from": "Name <email@example.com>",
      "to": "recipient@example.com",
      "cc": "other@example.com",
      "subject": "Subject line",
      "date": "Tue, 16 Dec 2025 21:12:21 +0000",
      "snippet": "First ~200 chars of body...",
      "labels": ["INBOX", "UNREAD"],
      "file": "~/.cache/jean-claude/emails/email-19b29039fd36d1c1.json"
    }
  ],
  "nextPageToken": "abc123..."
}
```

**Split file format:** Each email creates three files in `~/.cache/jean-claude/emails/`:
- `email-{id}.json` — Metadata (queryable with `jq`)
- `email-{id}.txt` — Plain text body (readable with `cat`/`less`)
- `email-{id}.html` — HTML body when present (viewable in browser)

The JSON includes `body_file` and `html_file` paths. HTML contains unsubscribe links.

The `nextPageToken` field is only present when more results are available. Use
`--page-token` to fetch the next page:

```bash
# First page
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail search "is:unread" -n 50

# If nextPageToken is in the response, fetch next page
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail search "is:unread" -n 50 \
  --page-token "TOKEN_FROM_PREVIOUS_RESPONSE"
```

### Search Emails

```bash
# Inbox emails from a sender
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail search "in:inbox from:someone@example.com"

# Limit results with -n
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail search "from:newsletter@example.com" -n 10

# Unread inbox emails
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail search "in:inbox is:unread"

# Shortcut for inbox
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail inbox
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail inbox --unread
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail inbox -n 5

# Inbox also supports pagination
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail inbox --unread -n 50 --page-token "TOKEN"
```

Common Gmail search operators: `in:inbox`, `is:unread`, `is:starred`, `from:`,
`to:`, `subject:`, `after:2025/01/01`, `has:attachment`, `label:`

### Get a Single Message

```bash
# Get message by ID (writes full body to ~/.cache/jean-claude/emails/)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail get MESSAGE_ID
```

Use this when you have a specific message ID and want to read its full content.

### Drafts

All draft commands read body from stdin. Create uses flags for metadata.

**IMPORTANT: Use heredocs, not echo.** Claude Code's Bash tool has a known bug
that escapes exclamation marks ('!' becomes '\!'). Always use heredocs:

```bash
# Create a new draft
cat << 'EOF' | uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft create --to "recipient@example.com" --subject "Subject"
Message body here!
EOF

# Create with CC/BCC
cat << 'EOF' | uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft create --to "recipient@example.com" --subject "Subject" --cc "cc@example.com"
Multi-line message body here.
EOF

# Reply to a message (body from stdin, preserves threading, includes quoted original)
cat << 'EOF' | uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft reply MESSAGE_ID
Thanks for your email!
EOF

# Reply with custom CC
cat << 'EOF' | uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft reply MESSAGE_ID --cc "manager@example.com"
Thanks for the update!
EOF

# Forward a message (TO as argument, optional note from stdin)
cat << 'EOF' | uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft forward MESSAGE_ID someone@example.com
FYI - see below!
EOF

# Forward without a note
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft forward MESSAGE_ID someone@example.com < /dev/null

# Reply-all (includes all original recipients)
cat << 'EOF' | uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft reply-all MESSAGE_ID
Thanks everyone!
EOF

# List drafts
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft list
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft list -n 5

# Get draft (writes metadata to .json and body to .txt)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft get DRAFT_ID

# Update draft body (from stdin)
cat ~/.cache/jean-claude/drafts/draft-DRAFT_ID.txt | uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft update DRAFT_ID

# Update metadata only
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft update DRAFT_ID --subject "New subject" --cc "added@example.com"

# Update both body and metadata
cat body.txt | uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft update DRAFT_ID --subject "Updated"

# Send a draft (after approval)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft send DRAFT_ID

# Delete a draft
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft delete DRAFT_ID
```

**Iterating on long emails:** For complex emails, use file editing to iterate
with the user without rewriting the full email each time:

1. Create initial draft using heredoc (see examples above)
2. Get draft files: `jean-claude gmail draft get DRAFT_ID` (writes `.json` and `.txt`)
3. Use Edit tool to modify `~/.cache/jean-claude/drafts/draft-DRAFT_ID.txt`
4. Update draft: `cat ~/.cache/jean-claude/drafts/draft-DRAFT_ID.txt | jean-claude gmail draft update DRAFT_ID`
5. Show user, get feedback, repeat steps 3-4 until approved

**Verifying important drafts:** For important emails, read the draft back after
creating it to confirm formatting is correct:

```bash
# Create draft
cat << 'EOF' | uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft create --to "..." --subject "..."
Email body here!
EOF

# Verify the draft content (check for escaping issues like \!)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail draft get DRAFT_ID
cat ~/.cache/jean-claude/drafts/draft-DRAFT_ID.txt
```

This catches any escaping bugs before sending.

### Manage Threads and Messages

Most commands operate on threads (matching Gmail UI behavior). Use `threadId` from
inbox/search output. Star/unstar operate on individual messages (use `latestMessageId`).

```bash
# Star/unstar (message-level - use latestMessageId)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail star MSG_ID1 MSG_ID2 MSG_ID3
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail unstar MSG_ID1 MSG_ID2

# Archive/unarchive (thread-level - use threadId)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail archive THREAD_ID1 THREAD_ID2 THREAD_ID3
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail archive --query "from:newsletter@example.com" -n 50
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail unarchive THREAD_ID1 THREAD_ID2 THREAD_ID3

# Mark read/unread (thread-level - use threadId)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail mark-read THREAD_ID1 THREAD_ID2
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail mark-unread THREAD_ID1 THREAD_ID2

# Trash (thread-level - use threadId)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail trash THREAD_ID1 THREAD_ID2 THREAD_ID3
```

**Which ID to use:**
- Thread operations (archive, mark-read, trash): use `threadId`
- Message operations (star): use `latestMessageId`
- Use `--query` for pattern-based operations (archive supports this)

### Attachments

```bash
# List attachments for a message
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail attachments MESSAGE_ID

# Download an attachment (saved to ~/.cache/jean-claude/attachments/)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail attachment-download MESSAGE_ID ATTACHMENT_ID filename.pdf

# Download to specific directory
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail attachment-download MESSAGE_ID ATTACHMENT_ID filename.pdf --output ./
```

### Unsubscribing from Newsletters

Unsubscribe links are in the HTML file, not the plain text. Note: HTML files are
only created when the email has HTML content (most newsletters do).

```bash
# Search HTML body for unsubscribe links (if HTML file exists)
grep -oE 'https?://[^"<>]+unsubscribe[^"<>]*' ~/.cache/jean-claude/emails/email-MESSAGE_ID.html
```

**Decoding tracking URLs:** Newsletters often wrap links in tracking redirects.
URL-decode to get the actual destination:

```python
import urllib.parse
print(urllib.parse.unquote(encoded_url))
```

**Completing the unsubscribe:**
- Mailchimp, Mailgun, and similar services work with browser automation
- Cloudflare-protected sites (Coinbase, etc.) block automated requests — provide
  the decoded URL to the user to click manually

### Labels

List all Gmail labels to get label IDs for filtering:

```bash
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail labels
```

Returns system labels (INBOX, SENT, TRASH, etc.) and custom labels (Label_123...).

### Filters

Filters automatically process incoming mail based on criteria.

```bash
# List all filters
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail filter list

# Get a specific filter
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail filter get FILTER_ID

# Delete a filter
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail filter delete FILTER_ID
```

**Creating filters** — query + label operations:

```bash
# Archive (remove INBOX label)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail filter create \
    "to:reports@company.com" -r INBOX

# Star and mark important
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail filter create \
    "from:boss@company.com" -a STARRED -a IMPORTANT

# Mark as read (remove UNREAD label)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail filter create \
    "from:alerts@service.com" -r UNREAD

# Forward
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gmail filter create \
    "from:vip@example.com" -f backup@example.com
```

**Common labels:** `INBOX`, `UNREAD`, `STARRED`, `IMPORTANT`, `TRASH`, `SPAM`,
`CATEGORY_PROMOTIONS`, `CATEGORY_SOCIAL`, `CATEGORY_UPDATES`

**Custom labels:** Use `gmail labels` to get IDs like `Label_123456`.

## Calendar

All calendar commands return JSON.

### Multiple Calendars

By default, commands operate on the primary calendar. Use `--calendar` to work
with other calendars.

```bash
# List available calendars
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal calendars
```

Returns:
```json
[
  {"id": "user@gmail.com", "name": "Personal", "primary": true, "accessRole": "owner"},
  {"id": "work@company.com", "name": "Work Calendar", "primary": false, "accessRole": "writer"},
  {"id": "family@group.calendar.google.com", "name": "Family", "primary": false, "accessRole": "owner"}
]
```

Use `--calendar` with any command to specify a different calendar:

```bash
# List events from a specific calendar
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal list --calendar work@company.com

# Create event on another calendar
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal create "Team Sync" \
  --start "2025-01-15 14:00" --calendar work@company.com

# Search by calendar name (case-insensitive substring match)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal list --calendar "Family"
```

The `--calendar` flag accepts:
- Calendar ID (email or group calendar ID)
- Calendar name (case-insensitive substring match)
- `primary` (default)

If a name matches multiple calendars, the command fails with a list of options.

**Multiple calendars in one query:** The `list`, `search`, and `invitations`
commands accept multiple `--calendar` flags to query across calendars:

```bash
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal list --from 2025-01-15 --to 2025-01-15 \
  --calendar "Personal" --calendar "Work"
```

Each event includes `calendar_id` and `calendar_name` in the output.

### Choosing the Right Calendar

The status command shows calendar participation metrics:

```
Max @ Personal (primary) (24 upcoming: 10 yours, 14 invited) [owner]
ursgwynn@gmail.com (26 upcoming: 2 yours, 7 invited) [writer]
Roos family (81 upcoming: 3 invited) [owner]
Max @ TGS (44 upcoming, 0 yours) [freeBusyReader]
team.interintellect@gmail.com (27 upcoming, 0 yours) [reader]
```

- **X yours** — Events where user is the organizer
- **X invited** — Events where user is an attendee
- **0 yours** — May indicate a "block" calendar (someone else's schedule)

**Which calendars to check:**

This is a judgment call. The metrics help but don't tell the whole story — a
spouse's calendar might show "yours" counts because the user invited them to
things, but that doesn't make it the user's availability.

Check user preferences (personalization skills) for guidance on which calendars
represent the user's own schedule vs calendars they just view. When in doubt,
ask.

**Checking availability:**

Use multiple `--calendar` flags to query several calendars at once:

```bash
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal list --from 2025-01-07 --to 2025-01-07 \
  --calendar "Max @ Personal" --calendar "Roos family"
```

Each event includes `calendar_id` and `calendar_name` showing which calendar it
came from.

**Creating events:**

Use the primary calendar unless:
- User explicitly names a different calendar ("put it on the family calendar")
- Context suggests a specific calendar (work event → work calendar)
- User preferences specify defaults for certain event types

### Proactive Calendar Management

When creating or updating calendar events, proactively add useful information:

- **Add attendees** — If the user mentions meeting someone, add them to the
  invite. Look up their email from previous events or contacts.
- **Add locations** — If the user mentions a place, add the full address. Search
  for the venue to get the complete address.
- **Add video links** — For remote meetings, include the video call link if
  known.

Don't just create a bare event title. A calendar invite should have everything
attendees need to show up prepared.

### Calendar Safety (Non-Negotiable)

**Dates are high-stakes. Mistakes waste people's time and cause confusion.**

1. **Never guess dates from relative terms.** When the user says "Sunday",
   "next week", or "tomorrow", explicitly calculate the date:
   ```bash
   date -v+0d "+%A %Y-%m-%d"  # Today's date and day of week
   ```
   Then verify: "Sunday is 2025-12-28 — creating the event for that date."

2. **Never hallucinate email addresses.** If the user says "add Ursula", look
   up her email (search contacts, check previous calendar events, or ask).
   Never invent addresses like `ursula@domain.com`.

3. **Verify after creating.** After `gcal create`, immediately run `gcal list`
   for that date to confirm the event appears on the correct day. If wrong,
   delete and recreate before telling the user it's done.

4. **Show what you're creating.** Before running `gcal create`, state:
   - Event title
   - Date and time (with day of week)
   - Attendees (with their actual email addresses)
   - Location (with full address)

5. **Confirm ambiguous locations.** When adding a location, if the place name
   could refer to multiple locations (chains, common names, multiple branches),
   ask the user which one before setting it. "SVB" could mean San Vicente
   Bungalows in West Hollywood or Santa Monica—don't guess.

**Example workflow:**
```
User: "Add a meeting with Alice for next Tuesday at 2pm"

1. Check today's date: date -v+0d "+%A %Y-%m-%d"  → "Friday 2025-12-26"
2. Calculate: next Tuesday = 2025-12-30
3. Look up Alice's email (search contacts or ask user)
4. State: "Creating 'Meeting with Alice' for Tuesday 2025-12-30 at 2pm,
   inviting alice@example.com"
5. Create the event
6. Verify: gcal list --from 2025-12-30 --to 2025-12-30
7. Confirm to user only after verification
```

**Example: location disambiguation:**
```
User: "Add the address to the dinner invite — it's at SVB"

1. Search for the event to update
2. Note: "SVB" is ambiguous (San Vicente Bungalows has locations in West
   Hollywood and Santa Monica)
3. Ask: "Which SVB location? West Hollywood (845 N San Vicente Blvd) or
   Santa Monica?"
4. Wait for user response before updating
```

### List Events

```bash
# Today's events
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal list

# Next 7 days
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal list --days 7

# Date range
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal list --from 2025-01-15 --to 2025-01-20
```

### Create Events

```bash
# Simple event
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal create "Team Meeting" \
  --start "2025-01-15 14:00" --end "2025-01-15 15:00"

# With attendees, location, and description
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal create "1:1 with Alice" \
  --start "2025-01-15 10:00" --duration 30 \
  --attendees alice@example.com \
  --location "Conference Room A" \
  --description "Weekly sync"

# All-day event (single day)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal create "Holiday" \
  --start 2025-01-15 --all-day

# Multi-day all-day event
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal create "Vacation" \
  --start 2025-01-15 --end 2025-01-20 --all-day
```

### Search & Manage Events

```bash
# Search (default: 30 days ahead)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal search "standup"
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal search "standup" --days 90

# Update
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal update EVENT_ID --start "2025-01-16 14:00"

# Delete
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal delete EVENT_ID --notify
```

### Invitations

List and respond to calendar invitations (events you've been invited to).

**Recurring events:** The invitations command collapses recurring event
instances into a single entry. Each collapsed entry includes:
- `recurring: true` - indicates this is a recurring series
- `instanceCount: N` - number of pending instances
- `id` - the parent event ID (use this to respond to all instances at once)

Responding to a parent ID accepts/declines all instances in the series.
Responding to an instance ID (if you have one) affects only that instance.

```bash
# List all pending invitations (no time limit by default)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal invitations

# Limit to next 7 days
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal invitations --days 7

# Show all individual instances (don't collapse recurring events)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal invitations --expand

# Accept an invitation (or all instances if recurring)
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal respond EVENT_ID --accept

# Decline an invitation
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal respond EVENT_ID --decline

# Tentatively accept
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal respond EVENT_ID --tentative

# Respond without notifying organizer
uv run --project ${CLAUDE_PLUGIN_ROOT} jean-claude gcal respond EVENT_ID --accept --no-notify
```

## Other Platforms

Load these platform-specific guides as needed:

```bash
# Messaging
cat ${CLAUDE_PLUGIN_ROOT}/skills/jean-claude/platforms/imessage.md
cat ${CLAUDE_PLUGIN_ROOT}/skills/jean-claude/platforms/whatsapp.md
cat ${CLAUDE_PLUGIN_ROOT}/skills/jean-claude/platforms/signal.md

# Google Workspace (non-Gmail)
cat ${CLAUDE_PLUGIN_ROOT}/skills/jean-claude/platforms/drive.md
cat ${CLAUDE_PLUGIN_ROOT}/skills/jean-claude/platforms/docs.md
cat ${CLAUDE_PLUGIN_ROOT}/skills/jean-claude/platforms/sheets.md

# Apple
cat ${CLAUDE_PLUGIN_ROOT}/skills/jean-claude/platforms/reminders.md
```

**When to load:** Load the relevant platform file when the user asks about that
service. For example, if they ask "send a WhatsApp message", load whatsapp.md
first.

**Safety rules still apply:** The messaging safety rules in this file (never
send without approval, verify recipients) apply to all messaging platforms.

## Location Context

When you need the user's location for "near me" queries or search context, use
these sources in order of reliability:

1. **User preferences** — Check if the user has a home/work location in their
   personalization skills or previous conversations

2. **Recent calendar events** — Search for events with locations (home address,
   frequent venues, school addresses reveal neighborhood)

3. **System timezone** — Narrows to region (e.g., America/Los_Angeles → US West Coast)

4. **IP geolocation** (last resort) — Can be inaccurate:
   ```bash
   curl -s ipinfo.io/json | jq '{city, region, country, loc}'
   ```
   This often returns a nearby city rather than the actual location (e.g., shows
   "La Puente" for someone in Santa Monica). Treat as approximate region only.

When using any inferred location, state your assumption so the user can correct
it: "I see you're in the LA area based on your calendar — searching there."

## Learning from Corrections

When users correct your drafts or behavior, these are opportunities to learn
preferences and save them to their preferences skill file.

**Examples of learnable corrections:**
- "Actually, sign it 'Best' not 'Cheers'" → sign-off preference
- "Always CC my assistant on work emails" → email rule
- "Don't use exclamation marks" → tone preference
- "My mom's new number is..." → contact update

**Not everything is a preference.** One-off corrections like "make this email
shorter" or "add more detail here" are situational, not preferences.

### Confirmation Mode (Default)

When the user corrects something that seems like a preference:

1. Make the correction
2. Offer to save it: "Want me to remember this for next time?"
3. If yes, update the skill file in `~/.claude/skills/managing-messages/SKILL.md`

### Auto-Learn Mode

After a few corrections, offer to enable auto-learning:

> I've saved a few preferences now. Want me to automatically save corrections
> like these going forward? I'll still tell you when I do.

If enabled, add this to their preferences file:

```markdown
## Meta

Auto-learn: enabled
```

**When auto-learn is enabled:**

1. Recognize correction as a preference
2. Update the skill file
3. Briefly confirm: "Noted—I'll sign emails 'Best' from now on."

**What to auto-learn:** Sign-off changes, tone corrections, contact updates,
phrase preferences, CC/BCC rules.

**What NOT to auto-learn** (always ask first): Anything affecting recipients,
major workflow changes, deletions from preferences.

## Reporting Issues

When you encounter technical difficulties that suggest a problem with the
jean-claude library (not user configuration), offer to file a GitHub issue.

**Signs of a library problem:**
- Unexpected exceptions or stack traces from jean-claude code
- API responses that don't match documented schemas
- Commands that worked before suddenly failing
- Behavior that contradicts the documentation

**Not library problems** (don't offer to file):
- Authentication failures (user needs to re-auth)
- Permission errors (user needs to grant access)
- Network issues or user configuration problems

When you hit what looks like a bug:

> I ran into an issue that looks like a bug in jean-claude. Want me to create
> a GitHub issue so the maintainers can fix it? I'll show you the report first
> and remove any personal information.

Only proceed if user agrees. See [ISSUES.md](ISSUES.md) for the full guide on
scrubbing personal info, formatting the issue, and submitting via `gh` or
pre-filled URL.
