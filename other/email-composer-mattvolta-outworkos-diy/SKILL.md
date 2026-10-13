---
name: email-composer
description: "Composes, drafts, and sends emails via Gmail. Enforces natural writing style (no em dashes, no AI tells), proper threading, and correct signature handling. Use whenever drafting, replying to, or sending any email."
argument-hint: "[reply-to thread or new email subject]"
---

# Email Composer

## Purpose

Handle all email composition. Ensures emails read naturally, thread correctly, and preserve the user's Gmail signature.

## Runtime Context

Before composing any email, retrieve the current user's profile via Supabase MCP `execute_sql`:

```sql
SELECT email, display_name, scheduling_link, domain, preferences
FROM user_profiles WHERE user_id = auth.uid()
```

Use these values throughout — never hardcode emails, names, or domains.

- **Sender email**: Use `email` from `user_profiles`
- **Scheduling link**: Use `scheduling_link` from `user_profiles`
- **User's domain**: Use `domain` from `user_profiles`
- **Display name**: Use `display_name` from `user_profiles`
- **Supabase project ID**: Read from `$SUPABASE_PROJECT_ID` environment variable

## When This Skill Activates

Any time the user asks to:
- Draft an email or reply
- Send an email
- Compose a message for someone
- Respond to an email thread
- Forward an email

## Writing Style Rules

### Absolute Prohibitions

These are dead giveaways that AI drafted the email. Never use them in email body text:

1. **Em dashes** (`—`) and **en dashes** (`–`). Rewrite using commas, periods, semicolons, or parentheses instead.
   - BAD: "We've talked it through — and have some questions"
   - GOOD: "We've talked it through and have some questions"

2. **Hyphen-style bullet lists in the email body**. Use numbered lists, line breaks, or prose paragraphs instead. If a list is truly needed, use plain numbers or letters.

3. **Filler pleasantries**: "I hope this email finds you well", "Please don't hesitate to reach out", "I wanted to touch base", "I'd be happy to assist"

4. **Overly formal constructions**: "Per our previous discussion", "As per your request", "Pursuant to", "In regard to"

5. **AI hedging patterns**: "It's worth noting that", "It's important to mention", "I should point out that"

### Voice and Tone

Write in the user's voice:
- **Direct and conversational**. Write like you'd talk to a coworker.
- **Concise**. Get to the point quickly. Short paragraphs, short sentences.
- **Warm but not fluffy**. Friendly opener, clear ask, done.
- **Use contractions naturally** (we've, don't, I'll, that's).
- **Lowercase "i" in casual internal emails is fine** if it matches prior thread tone.

### Scheduling a Meeting or Call

**Scheduling link:** Use the `scheduling_link` value from `user_profiles` whenever the user wants to include a link for the recipient to book a time.

When the email involves setting up a time to talk, close with a simple ask for availability. Keep it natural and conversational, e.g. "Let me know if any day this week works for you."

If specific times are being offered, list them and add a fallback like "If none of those work, let me know what's better."

### Calendar "Hold" Blocks

Events titled just "Hold" (or similar generic holds without a specific name) are personal time blocks the user uses to prevent external bookings. They are NOT real commitments.

- **"Hold"** or **"Hold - [time block reason]"** with no person/company name → treat as **available/free time**
- **"Hold for McArthy's"**, **"Hold for Jordan"**, etc. with a specific name → treat as a **real commitment**, do NOT offer this time

When checking availability, read the full event list (not just freebusy) to distinguish between generic holds and named holds.

### Structural Guidelines

- Lead with context or the ask, not preamble
- One topic per paragraph
- End with a clear next step or question
- Keep emails under 150 words when possible (exceptions: complex multi-point replies)

## Signature Handling

The `draft_gmail_message` and `send_gmail_message` tools auto-append the Gmail signature via `include_signature: true` (the default). Do NOT manually fetch or embed the signature in the body -- this causes double signatures.

Just write the email body content and let the tool handle the signature.

### Body Format

Use `body_format: "html"` for all emails so the signature renders correctly. Wrap paragraphs in `<p>` tags:

```html
<div dir="ltr">
  <p>[paragraph 1]</p>
  <p>[paragraph 2]</p>
  <p>[sign-off name]</p>
</div>
```

### For Drafts

**Full mode:** Use the Google Workspace MCP `draft_gmail_message` tool with `body_format: "html"`. The user will review and send from Gmail.

**Quick mode:** Use the built-in `gmail_create_draft` tool (discovered via `ToolSearch: "+gmail draft"`). Use `contentType: "text/html"`. This tool does not auto-append a Gmail signature — append the user's sign-off name at the end of the body. The user adds their full signature when sending from Gmail.

### For Programmatic Sends

**Full mode only.** Use the Google Workspace MCP `send_gmail_message` tool with `body_format: "html"`. Only use programmatic send when the user explicitly says "send it" (not "draft it" or "save it").

**Quick mode:** Programmatic send is not available. Always create a draft and tell the user: "Draft created — open Gmail to review and send." If the user says "send it", explain that quick mode only supports drafts and suggest switching to `mode: "full"` in `outworkos.config.yaml`.

## Threading

Always thread replies correctly. This requires three fields:

| Field | Value | Purpose |
|-------|-------|---------|
| `thread_id` | Gmail thread ID from the original message search | Groups messages in the same conversation |
| `in_reply_to` | `Message-ID` header from the message being replied to | Links reply to specific parent |
| `references` | Space-separated chain of all `Message-ID` headers in the thread | Full thread ancestry |

**How to get these values:**
1. `search_gmail_messages` to find the thread
2. `get_gmail_message_content` or `get_gmail_thread_content` to read messages and extract `Message-ID` headers
3. Use the thread ID from the search result, and the `Message-ID` from the most recent message as `in_reply_to`

If `Message-ID` headers are not available from the MCP tool response, use `in_reply_to` and `references` from the last message in the thread (they're usually echoed in the raw headers).

## Default Configuration

| Setting | Value |
|---------|-------|
| Sender email | Retrieved from `user_profiles.email` via Supabase MCP |
| Body format | `html` (required for signature rendering) |
| Signature | Auto-appended by tool (`include_signature: true` default). Do NOT embed manually. |

## Workflow

1. **Retrieve user profile**: Query `user_profiles` for email, display_name, scheduling_link, and domain (see Runtime Context above)
2. **Gather context**: Read the relevant thread (if replying) to understand tone and history
3. **Compose**: Write the email following style rules above
4. **Self-check**: Before calling the tool, scan the draft for em dashes, en dashes, AI tells, and filler phrases. Fix any violations.
5. **Present to user**: Show the full email text for approval before creating the draft/send
6. **Create draft or send**: Use the appropriate MCP tool based on user intent
7. **Confirm**: Report the draft ID or sent message ID back to the user

## Pre-Send Checklist

Run this mental checklist before every email tool call:

- [ ] No em dashes (—) or en dashes (–) anywhere in the body
- [ ] No hyphen-bullet lists
- [ ] No AI filler phrases
- [ ] Threading fields set (for replies)
- [ ] Correct recipients (to, cc, bcc)
- [ ] Subject line matches thread (for replies: "Re: [original subject]")
- [ ] Body format is HTML (required for signature)
- [ ] Signature NOT manually embedded (tool auto-appends it)
- [ ] Email reads like the user wrote it, not an AI

## Step 8: Reply Tracking

**Database:** Use Supabase MCP `execute_sql` with the project ID from `$SUPABASE_PROJECT_ID`. All reply tracking reads and writes use this project. Never use other databases for reply tracking.

After confirming the draft or send (Step 7), ask:

> **Are you expecting a reply to this?**

If the user says **yes**:

1. **Store a tracking record** in `reply_tracking`:
   ```sql
   INSERT INTO reply_tracking (
     user_id, gmail_thread_id, recipient_name, recipient_emails,
     subject, summary, sent_at, status, project_slug
   ) VALUES (
     auth.uid(),
     '{thread_id}',
     '{recipient_name}',
     ARRAY['{email1}', '{email2}'],
     '{subject}',
     '{brief summary of what was asked or requested}',
     now(),
     'waiting',
     '{project_slug or NULL}'
   );
   ```

2. **Create a Todoist task** with the `waiting-reply` label:
   - **Content:** `Waiting for reply: {Recipient Name} — {brief what was asked}`
   - **Description:**
     ```
     **Tracking reply from:** {Recipient Name} ({email})
     **Sent:** {date}
     **What was asked:** {1-2 sentence summary}

     **Sources:**
     - Gmail: https://mail.google.com/mail/u/0/#all/{thread_id}
     ```
   - **Label:** `waiting-reply` (create if it doesn't exist, color: charcoal)
   - **Project:** Match to the relevant Todoist project from the manifest (if known)
   - **Section:** Place in whatever section is natural (Do, Triage, etc.) — do NOT force into Waiting
   - **Priority:** Normal (p4)
   - **No due date** (the tracking age handles urgency)

3. **Store the Todoist task ID** back into `reply_tracking`:
   ```sql
   UPDATE reply_tracking SET todoist_task_id = '{task_id}'
   WHERE gmail_thread_id = '{thread_id}' AND user_id = auth.uid() AND status = 'waiting';
   ```

If the user says **no**, skip tracking entirely.

### When NOT to Ask

Skip the reply tracking question for:
- Internal team emails to the user's own domain (from `user_profiles.domain`) unless the user explicitly asks
- Simple confirmations ("Got it", "Thanks", "Sounds good")
- FYI/announcement emails with no ask

### AI Suggestion Mode

If the email clearly contains a question or request (e.g., "Can you send me...?", "What do you think about...?", "Let me know if...", "When can we...?", scheduling a meeting link), suggest tracking proactively:

> This looks like you're expecting a reply (you asked about X). Want me to track it?

This keeps the flow manual but prevents forgetting. Over time, the patterns from `reply_tracking` records will inform automation.
