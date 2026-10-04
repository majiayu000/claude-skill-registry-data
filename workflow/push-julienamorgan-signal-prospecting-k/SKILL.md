---
name: push
description: >
  Exports approved outreach emails into the user's preferred format: sequencer
  CSV, plain text, or formatted for specific tools. Triggers: /push, "export
  emails", "push to instantly", "push to outreach". Reads: ./gtm/prospects.md,
  ./gtm/icp.md (for stack info). Writes: output files in ./gtm/export/.
  Standalone: yes.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---

# /push — Export to Sequencer or File

You take approved outreach emails and format them for the user's email
sequencer, or export them as plain text files ready to copy-paste.

---

## Process

### Step 1: Detect Format + Connected Tools

Check `./gtm/icp.md` for Connected Tools and Stack sections.

**If outreach/CRM tools are connected** (check Connected Tools in
icp.md for any MCP connections or API keys), offer direct push:

```
  I can push these directly to {connected tool}
  as a new campaign. Or export as files.
  Which do you prefer?
```

Use whatever tool is connected — follow its API conventions.
Do NOT hardcode preferences for any specific tool.

**If no direct push tools, offer file formats:**

**Adapt the menu to the user's stack.** Read icp.md Stack section.
If they use specific tools, name those tools in the options. If they
have no tools (just Gmail, manual sending), simplify the menu.

```
{If user has tools in their stack:}

  How do you want these exported?

  1. Plain text (copy-paste ready)
  2. CSV (for {their sequencer or "email sending tools"})
  3. {Their sequencer} format (if applicable)
  4. {Their CRM} format (if applicable)
  5. LinkedIn copy-paste (all messages with char counts)
  6. LinkedIn CSV (for {their LinkedIn tool or "automation tools"})
  7. Both email + LinkedIn files
  8. Just show me — I'll copy them manually

{If user has NO tools (Gmail, manual, etc.):}

  How do you want these exported?

  1. Plain text (copy-paste into Gmail)
  2. LinkedIn copy-paste (all messages, ready to send)
  3. Both email + LinkedIn text files
  4. Just show me — I'll copy them manually
```

### Step 2: Gather Approved Outreach

Read `./gtm/prospects.md` for all prospects with status "outreach-written".

Check what was written — email only, LinkedIn only, or both. Export
whatever exists.

If no outreach has been written, suggest: "Run /outreach first to write
outreach for your prospect list."

### Step 3: Export

#### Plain Text (.txt)

Simple, universal. One file with all emails separated by dividers.

Create `./gtm/export/outreach-{date}.txt`:

```
================================================================
TO: {prospect name} — {title} — {company}
EMAIL: {email if known, otherwise "[find email]"}
LINKEDIN: {url if known}
================================================================

Subject: {subject line}

{email body}

================================================================
{next email...}
```

#### CSV (Instantly, Apollo, Smartlead, etc.)

Create `./gtm/export/outreach-{date}.csv`:

```
first_name,last_name,email,company,title,subject,body,linkedin_url
{first},{last},{email or empty},{company},{title},{subject},{body with newlines as \n},{linkedin}
```

**CSV formatting rules:**
- Escape commas and quotes in body text
- Replace newlines with `\n` in the body column
- Include LinkedIn URL column even if empty
- Email column: use company domain email if found, otherwise leave blank
  with a note that they need to find it

#### Outreach / Salesloft Format

Create `./gtm/export/outreach-{date}-sequences.txt`:

```
SEQUENCE: Signal Outbound — {date}
STEP 1: Email (Day 0)

---

PROSPECT: {name} — {company}
Subject: {subject}
Body:
{email body}

---

{next prospect...}
```

#### HubSpot Sequences Format

Create `./gtm/export/outreach-{date}-hubspot.csv`:

```
Email,First Name,Last Name,Company,Job Title,Contact owner
{email},{first},{last},{company},{title},{user name from voice.md}
```

Plus a separate template file with the email body for the sequence step.

#### LinkedIn Copy-Paste (.txt)

Create `./gtm/export/linkedin-{date}.txt`:

```
================================================================
TO: {prospect name} — {title} — {company}
LINKEDIN: {linkedin URL}
CHARS: {character count}
================================================================

{linkedin connection request message}

================================================================
{next prospect...}
```

#### LinkedIn API (HeyReach, Dripify, etc.)

Create `./gtm/export/linkedin-{date}.csv`:

```
linkedin_url,first_name,last_name,company,title,message
{url},{first},{last},{company},{title},{message}
```

**CSV formatting for LinkedIn messages:**
- Escape commas and quotes in message text
- Replace newlines with spaces (LinkedIn messages are single-block)
- Verify every message is under 300 characters in the CSV

If the user has a LinkedIn automation tool in their stack (from icp.md),
format for that specific tool. If not, default to the generic CSV that
most tools can import.

#### Direct Push: Instantly API

If `$INSTANTLY_API_KEY` is set, push directly:

```bash
# Create campaign
curl -s "https://api.instantly.ai/api/v1/campaign/create" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'$INSTANTLY_API_KEY'",
    "name": "Signal Outbound — {date}",
    "schedule": {...}
  }'

# Add leads to campaign
curl -s "https://api.instantly.ai/api/v1/lead/add" \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "'$INSTANTLY_API_KEY'",
    "campaign_id": "{id from create}",
    "leads": [
      {
        "email": "{email}",
        "first_name": "{first}",
        "last_name": "{last}",
        "company_name": "{company}",
        "custom_variables": {
          "signal": "{signal}",
          "subject": "{subject}",
          "body": "{body}"
        }
      }
    ]
  }'
```

**NEVER hardcode the API key.** Always use $INSTANTLY_API_KEY.

After push, show:
```
  Pushed {N} leads to Instantly campaign
  "{campaign name}". Check your Instantly
  dashboard to review and activate.
```

#### Direct Push: Clay MCP

If Clay MCP is connected, offer to push contacts to a Clay table:

```
mcp__claude_ai_Clay__track-event:
  - event_name: "outreach_ready"
  - properties: {prospect data + outreach copy}
```

Or use Clay's account management:
```
mcp__claude_ai_Clay__add-contact-data-points:
  - Add signal, outreach copy, and status to existing contacts
```

### Step 4: Present Export

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  EXPORT COMPLETE
  {date}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Format: {format name}
  Prospects: {N}
  File: ./gtm/export/{filename}

  ──────────────────────────────────────────────

  {If any prospects are "LinkedIn only" or have pattern-guess emails:}

  EMAIL STATUS
  ─────────────────────────────────────────────
  {N} verified emails → ready to send
  {N} pattern-guess emails → verify before sending
  {N} LinkedIn only → connection requests ready

  {If pattern-guess emails exist:}
  Pattern-guess emails are based on the company's
  email format. Verify them before sending — a
  bounced email hurts your sender reputation.

  {If the user has an enrichment tool connected:}
  Want me to try verifying the pattern-guess emails
  with {connected tool}? Say "verify" and I'll check.

  {If no enrichment tools and user wants better emails:}
  If you have access to any email verification or
  enrichment tool, I can help you connect it and
  verify these. Otherwise, the LinkedIn outreach
  is ready to go as-is.

  ──────────────────────────────────────────────

  DELIVERABILITY CHECK
  ─────────────────────────────────────────────

  Before sending, make sure:

  ✓ Domain authentication (SPF, DKIM, DMARC)
    set up on your sending domain
  ✓ Sending domain is warmed up (if new, start
    with 5-10/day and ramp over 2-3 weeks)
  ✓ Daily send limit: stay under 50/day per
    mailbox for cold outreach
  ✓ Don't send all {N} emails at once — spread
    across 2-3 days minimum

  {If sequencer in stack:}
  Your sequencer handles warmup and send pacing
  automatically — just check it's configured.

  {If no sequencer (Gmail, manual sending):}
  Since you're sending manually, keep it to
  10-15 cold emails per day and space them out.
  Don't send them all at once.

  ──────────────────────────────────────────────

  NEXT STEPS

  {If pattern-guess emails exist:}
  1. Verify pattern-guess emails before sending.
     {If enrichment tool connected:} I can verify
     these now — say "verify" and I'll check them.
     {If no tools:} Send a test email to yourself
     at the guessed address, or search LinkedIn
     for the contact to confirm their email domain.

  {Adapt to their stack:}
  {If sequencer:} 2. Upload {filename} to {sequencer}
  {If Gmail/manual:} 2. Copy-paste from the .txt file
     into Gmail. Send 10-15 per day max.

  3. Send LinkedIn connection requests manually
     (copy from the LinkedIn .txt file)
  4. Come back after replies and tell me what
     worked — I'll log it and adjust next time

  ──────────────────────────────────────────────

  After you've sent these, tell me what got
  replies. I'll log it and adjust future outreach.
```

### Step 5: Update Status

Update prospects.md: change status from "outreach-written" to "sent"
for all exported prospects.

---

## Handling Replies (Post-Send)

When the user comes back to log results, make it structured and easy.

### Structured Result Logging

Show the sent prospect list and ask for results:

```
  RESULTS LOG — Batch {date}
  ─────────────────────────────────────────────

  {N} prospects sent. Mark each one:

  1. {Name} at {Company} ({channel})
  2. {Name} at {Company} ({channel})
  3. {Name} at {Company} ({channel})
  ...

  Tell me which ones replied. Examples:
  - "1 and 4 replied"
  - "got a reply from {name}"
  - "3 replies out of 10"
  - "nobody replied"

  Any details on what they said helps me
  write better next time.
```

The user can respond however they want — structured or casual:

- "1 and 4 replied" → mark those as replied, rest as no-reply
- "Got a reply from {name}" → update that one
- "3 replies, don't remember which" → ask who, or mark batch rate
- "Nobody replied" → mark all as no-reply, still valuable data
- "Got a LinkedIn accept from {name}" → update status + channel

**learnings.md format — DETAILED (this drives self-improvement):**

```markdown
## {date} — Batch: {N} sent, {N} replied

### Summary
- Emails sent: {N} | Replies: {N} | Reply rate: {X}%
- LinkedIn sent: {N} | Accepts: {N} | Accept rate: {X}%
- Best signal type this batch: {type}
- Best opener type this batch: {type}

### Replies
- {Name} at {Company}
  Channel: {email / linkedin}
  Signal type: {proven / high-intent / moderate / social}
  Signal used: {specific signal}
  Opener type: {observation / signal / question / buyer / social}
  Bridge angle: {methodology / scale / accuracy / api / price / workflow}
  CTA type: {send-address / quick-call / side-by-side / etc.}
  Notes: {what they said, if shared}

### No Reply
- {Name} at {Company}
  Channel: {email / linkedin}
  Signal type: {type}
  Opener type: {type}
  Bridge angle: {angle}
  CTA type: {type}

### Patterns
- Signal: {which signal types got replies vs didn't}
- Opener: {which opener types performed}
- Bridge: {which bridge angles worked}
- CTA: {which CTAs got responses}
- Channel: {email vs LinkedIn performance}
- Title: {which buyer titles responded — VP vs Director etc.}

### Cumulative Stats (update across all batches)
- Total sent: {N} | Total replies: {N} | Overall rate: {X}%
- Best performing combination: {opener} + {bridge} + {CTA}
- Worst performing combination: {what to avoid}
```

After logging, show the user:

```
  LEARNING UPDATE
  ─────────────────────────────────────────────

  Logged: {N} replies, {N} no-replies
  Reply rate this batch: {X}%
  Cumulative reply rate: {X}% across {N} batches

  {if patterns found:}
  WHAT'S WORKING
  • {signal type}: {X}% reply rate ({N} sends)
  • {opener type}: {X}% reply rate
  • {bridge angle}: {X}% reply rate
  • {channel}: {X}% reply rate

  {if anti-patterns found:}
  WHAT'S NOT
  • {signal/opener/bridge}: 0 replies across {N} sends
  • Deprioritizing for next batch.

  {Show progression:}
  BATCH PROGRESSION
  Batch 1: {N} sent → {N} replied ({X}%)
  Batch 2: {N} sent → {N} replied ({X}%)
  ...
  Trend: {improving / flat / declining}

  ──────────────────────────────────────────────

  Ready for the next batch. I'll find new
  companies showing fresh signals and apply
  what worked.

  Say "go" to start the next batch.
```

### Auto-Continue to Next Batch

**After logging results, offer to start the next batch immediately.**
If the user says "go", "next batch", "keep going", or similar:

1. Auto-continue to /prospect (which dedupes against existing)
2. /prospect will use updated learnings to inform signal prioritization
3. /outreach will use updated learnings to weight winning patterns

This is the core loop: send → log → learn → find → write → send.
Each cycle should be faster and more effective than the last.

---

## Handling Questions and Tangents

If the user asks about deliverability concepts ("what's SPF?", "how
do I set up DKIM?", "what's domain warmup?"), explain in plain
language with actionable steps. These are common questions at the
export stage — answer fully, don't just point them elsewhere.

If the user asks about tools ("should I get a sequencer?", "what's
the best sending tool?"), research current options via WebSearch and
give an honest recommendation based on their needs and budget.

If the user wants to go back ("can you rewrite email #3?", "I want
to add a prospect"), hand off to /outreach or /prospect as needed.
Don't try to do their job from within /push.

---

## Edge Cases

**No sequencer in stack:**
Default to plain text. If the user asks what tools they should use
for automated sending, research current options via WebSearch and
give an honest recommendation based on their budget and needs.
Do not hardcode preferences for any specific tool.

**User wants to send directly from here:**
This kit doesn't send emails. It writes and exports them. The user
sends from their own tool. This is by design — keeps the kit simple
and avoids needing email API credentials.

**User wants follow-up sequences:**
First-touch only for now. Suggest they come back in 3-5 days, check
replies, and run another batch for non-responders with a different
angle.
