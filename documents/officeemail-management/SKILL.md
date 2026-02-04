---
name: office:email-management
description: Handle email tasks (checking inbox, drafting replies, managing threads, adding events to calendar). Use when working with emails to prevent common mistakes like broken threading or missing recipients.
---

# Email Management with Office Admin

Use this skill when handling:
- Checking inbox or finding specific emails
- Drafting email replies
- Adding events from emails to calendar
- Managing email workflows
- Bulk email triage

## Core Principles

1. **Always draft, never send** - Save emails as drafts for user review before sending
2. **Threading is critical** - Replies must appear in the correct conversation thread
3. **Match user's voice** - Reference their office-admin config for tone and style
4. **Extract structured data** - Pull event details, action items, contact info from emails
5. **Proactive calendar integration** - Auto-check conflicts and add events

## User Style Configuration

Before drafting emails, load the user's style from `~/.claude/office-admin-config.json`:

```json
{
  "email": {
    "tone": "ultra-terse" | "conversational" | "professional" | "warm",
    "signature": "none" | "minimal" | "full",
    "formality": "casual" | "standard" | "formal",
    "responseLength": "minimal" | "balanced" | "detailed",
    "patterns": ["common phrases they use"],
    "customGuidelines": "Additional freeform style notes"
  }
}
```

If config doesn't exist, prompt user to run `/setup-office-admin` first.

## Email Drafting Workflow

### Step 1: Find the Thread

When drafting a reply, ALWAYS search for the original email first:

```
Search for: [subject] from [sender name]
Get: Full email content, thread ID, message ID, recipient email
```

**Why:** You need context AND threading information. Skipping this = standalone draft instead of threaded reply.

### Step 2: Get Threading Details

Extract from search results:
- `thread_id` - Links all messages in the conversation
- `message_id` - The specific message you're replying to (usually most recent)
- `recipient_email` - The To: address (CRITICAL - tool doesn't auto-extract!)

**Critical:** All three are required for proper threading. Missing any = broken draft.

### Step 3: Draft Using User's Voice

Reference their config for:

**Tone Guidelines:**
- **Ultra-terse**: 1-2 lines, no fluff, direct
- **Conversational**: Casual but complete, friendly
- **Professional**: Formal, structured, proper grammar
- **Warm**: Friendly, personal, include pleasantries

**Signature Guidelines:**
- **None**: No sign-off, message ends immediately
- **Minimal**: Simple "Best," or "Thanks,"
- **Full**: Complete signature block from config

**Response Length:**
- **Minimal**: One-liners when possible
- **Balanced**: 2-3 sentences typical
- **Detailed**: Thorough explanations

**User Patterns:**
Use their common phrases from config `patterns` array when appropriate.

### Step 4: Create Threaded Draft

When creating the draft, specify:
- **To:** Recipient's email address (CRITICAL - always explicit!)
- **Thread ID** (to keep it in conversation)
- **In-Reply-To message ID** (the message you're replying to)
- **Subject** (maintain thread subject, usually "Re: [original]")
- **Body** (match user's voice from config)
- **Signature** (based on user's preference)

**CRITICAL:** Always explicitly provide the `To:` email address. The MCP tool does NOT automatically extract the recipient from the thread - if you omit it, it will create a broken draft with invalid addresses.

**Example tool call structure:**
```
To: sender@example.com
Thread ID: 19a5fc252ad4dd3a
In-Reply-To message ID: 19a711957d96874d
Subject: Re: Project Discussion
Body: [message in user's style]
[Signature if configured]
```

### Step 5: Verify Threading

After creating draft, confirm:
- Draft appears in the correct conversation thread
- Subject line maintains thread format
- Draft is saved (not sent)

If threading failed:
1. Get correct thread ID and message ID again
2. Recreate draft with proper IDs
3. Don't create a new standalone email

### Step 6: Iterate on Feedback

User will refine wording:
- Update the draft with changes
- Maintain proper threading
- Keep user's voice consistent

## Calendar Integration

**IMPORTANT:** When emails contain event information, PROACTIVELY add them to the calendar and check for conflicts. Don't wait for user to ask.

### Step 1: Extract Event Details

Look for:
- Date and time
- Location
- Event title/description
- Attendees/who's invited
- Any special notes

### Step 2: Check Calendar for Conflicts

BEFORE creating the event:
1. Check user's calendar for the event date
2. Look for conflicts around the event time
3. Note any existing commitments
4. Reference their working hours from config

**Why:** User needs to know if there's a conflict before committing.

### Step 3: Report Conflicts or Availability

Tell the user:
- "You're free at [time] on [date]" ✅
- "That conflicts with [existing event] at [time]" ⚠️
- Show the relevant portion of the day's schedule

### Step 4: Add Event to Calendar (if appropriate)

If user confirms or if there's no conflict, create the event with:
- Clear title (include location if helpful)
- Correct date/time with timezone awareness (from config)
- Location field
- Description noting who invited/context
- Attendees (if it's a meeting with others)

**Example:**
```
Title: "Lunch with Mike Evans at Soho House"
Date: December 3, 2025
Time: 12:00 PM to 1:30 PM ([User's Timezone from config])
Location: Soho House
Description: "Lunch invitation from Mike Evans to discuss Q1 planning"
Attendees: mike@example.com
```

### Step 5: Confirm Addition

Let user know the event was added and provide:
- Calendar link for verification
- Note any conflicts that were identified
- Confirm if adjustments are needed

### Step 6: Handle Tentative Events

For events pending confirmation:
- Create calendar event with "HOLD:" prefix in title
- Example: "HOLD: Call with Jean (pending confirmation)"
- Add "(pending confirmation)" in description
- Update to remove "HOLD" once confirmed
- Delete if falls through

### Step 7: Timezone Handling

When scheduling with people in other timezones:
- Use user's timezone from config as primary
- Specify BOTH timezones in the email
- Example: "9am [your timezone] (4pm their timezone)"
- Double-check timezone conversion before sending

## Inbox Triage

When checking inbox:

### Step 1: Search for Unread

Get recent unread emails with:
- Sender
- Subject
- Date
- Preview snippet

### Step 2: Categorize

Group mentally by type:
- **Urgent/Today**: Meetings, time-sensitive requests
- **Action needed**: Need response or calendar add
- **FYI**: Updates, newsletters
- **Archive**: No action needed, informational only

**NEVER categorize as "DELETE"** - Users should archive instead of deleting.

**For spam/unwanted emails:**
- Mark as spam using Gmail's spam function (if truly spam)
- Unsubscribe from newsletters (if there's an unsubscribe link)
- Archive everything else (don't delete - email storage is cheap, deletion is permanent)

### Step 3: Summarize Clearly

Present in order of priority:
- Recent/urgent first
- Group related emails (threads)
- Highlight action items
- Note any follow-ups needed

### Step 4: Use Subagents for Bulk Processing

For large triage operations (10+ emails):
- Use Task tool with general-purpose subagent
- Have subagent categorize all emails
- Subagent can draft multiple replies in one go
- More efficient than processing one-by-one

## Bulk Email Processing with Subagents

When user asks to triage many emails or handle multiple replies:

1. **Use subagent for triage**:
   - Pass clear categorization criteria
   - Have subagent check calendars for scheduling
   - Pass user's email style config to subagent
   - Get comprehensive report back

2. **Use subagent for bulk drafting**:
   - Provide list of emails needing replies
   - Give subagent user's voice guidelines from config
   - Subagent creates all drafts with proper threading
   - Review and user sends

**Example prompt structure for subagent:**
```
Triage all unread emails in inbox. Categorize as:
- ACTION NEEDED (with specific next steps)
- CALENDAR (extract event details, check conflicts)
- ARCHIVE (no action needed)

For ACTION NEEDED, draft replies using this style:
[Include user's email config]

Return comprehensive report.
```

## Common Mistakes to Avoid

### ❌ Creating Standalone Drafts Instead of Threaded Replies
**Problem:** Draft appears as new email, not in conversation thread
**Solution:** Always get thread ID and message ID before creating draft

### ❌ Not Matching User's Voice
**Problem:** Email doesn't sound like the user
**Solution:** Reference their office-admin config for tone, formality, patterns

### ❌ Adding Wrong Signature
**Problem:** Adding "Best," when user configured "none"
**Solution:** Check config `email.signature` setting

### ❌ Sending Instead of Drafting
**Problem:** User can't review before it goes out
**Solution:** ALWAYS save as draft, let user send

### ❌ Forgetting to Extract Calendar Events
**Problem:** User has to manually add events later
**Solution:** Proactively offer to add events when you see them in emails

### ❌ Missing the `To:` Field
**Problem:** Draft created with invalid `@example.com` address that bounces
**Solution:** ALWAYS explicitly provide recipient email address from thread search

### ❌ Wrong Timezone
**Problem:** Event added in wrong timezone
**Solution:** Use timezone from user's config (default: their local timezone)

## Integration Checklist

Before completing an email task, verify:

- [ ] Loaded user's office-admin config for style preferences
- [ ] Found original email/thread for context
- [ ] Got thread ID, message ID, AND recipient email if replying
- [ ] Drafted in user's voice (matched config settings)
- [ ] Created as DRAFT (not sent)
- [ ] Verified proper threading if reply
- [ ] Extracted and added calendar events if present
- [ ] Checked for scheduling conflicts
- [ ] Summarized what was done for user

## CRM Integration

When processing emails with new contacts:
- Check if contact exists in CRM
- Add to CRM if significant contact
- Log interaction in CRM
- Associate with company if applicable

See `office:crm-management` skill for details.

## Success Criteria

You've successfully handled email tasks when:
- Drafts appear in correct conversation threads
- User says "looks good" without needing changes
- Calendar events are added proactively
- Inbox summaries surface what matters
- Process feels efficient and natural
- Voice matches user's configured style

## Remember

Email is personal communication using the user's voice. The goal is to save time while maintaining authentic, effective communication that sounds like THEM.

When in doubt: Check their config, follow their patterns, and always draft first.
