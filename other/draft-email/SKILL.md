---
name: draft-email
created_by: Aman Parmar
last_modified: 20-04-2026
description: |
  Draft professional emails (MoM, status updates, decisions, stakeholder communication) and save as a
  draft in your email provider. Use this skill after a meeting, decision, spec update, or any event
  that needs email communication.
  Trigger phrases: "send MoM email", "draft meeting minutes email", "MoM email for [meeting]",
  "create MoM draft", "email the meeting notes", "draft MoM", "draft email", "send update email",
  "draft email for [topic]".
  Reads context from meetings, specs, tickets, and conversation. Looks up attendee emails from a
  local team directory, formats as HTML email, and pushes to the email provider as a draft (never sends).
---

# Draft Email

## Writing Framework

Based on Smart Brevity (Axios), Minto Pyramid Principle (McKinsey), Writing That Works (Ogilvy), HBR Guide to Better Business Writing (Garner), On Writing Well (Zinsser), and Made to Stick (Heath Brothers).

### Core Principle: Respect the reader's time

The reader is busy. They will scan, not read. Every line must earn its space. If a line doesn't help the reader understand or act, cut it.

### Email Structure — Adapt by Type

Headers like "What's new" and "Why it matters" are tools, not mandatory labels. Use them when they help the scanner — drop them when they feel forced. The rule: every email leads with the answer and ends with impact. How you get there depends on the email type.

#### Type 1: MoM / Decision Announcement
Use "What's new" + "Why it matters" headers ONLY when there is a genuine decision or announcement. For MoMs that summarize observations, discussions, or session findings (no single decision to announce), skip these headers and open with a direct context line.
```
# When there IS a key decision/announcement:
1. WHAT'S NEW (1 strong sentence - the key decision or outcome)
2. WHY IT MATTERS (1 sentence - impact on project/timeline)
3. GO DEEPER (numbered sections with SCQA for decisions)
4. WHAT'S NEXT (action items with named owners)
5. REFERENCE (attendees, links)

# When summarizing observations/discussions:
1. OPENING LINE (direct context: who met, what was discussed, key takeaway)
2. FINDINGS (numbered sections grouped by theme)
3. WHAT'S NEXT (action items with named owners)
4. REFERENCE (attendees, links)
```

#### Type 2: Data/Status Snapshot
NO "What's new" — there is no news, it's a report. The data IS the message.
```
1. OPENING LINE (direct: "Here is the team-wise breakdown of X as of DD-MM-YYYY.")
2. CONTEXT LINE (why the reader should care)
3. DATA TABLE (the primary content - sortable, with filter links)
4. KEY OBSERVATIONS (numbered, bold labels - highlight blockers, risks, outliers)
5. WHAT'S NEXT (action items with named owners)
6. CLOSING LINE (impact - what this means for the project)
7. REFERENCE (master filter, label, links)
```

#### Type 3: Reply in Existing Thread
NO headers at all — context already exists. Jump straight into the response.
```
1. DIRECT RESPONSE (answer the question or share the update)
2. DETAILS if needed (numbered points)
3. WHAT'S NEXT if actions are needed
```

#### Type 4: Update Email (not a reply, not data-driven)
Use "What's new" only if there is genuinely something new. Otherwise open with a direct line.
```
1. WHAT'S NEW or OPENING LINE
2. WHY IT MATTERS (1 sentence)
3. DETAILS (numbered sections)
4. WHAT'S NEXT (action items)
5. REFERENCE (links)
```

#### Type 5: Process / Instructions Email
NO "What's new" — you're telling people what to do, not announcing news.
```
1. OPENING LINE (what this email covers + why it matters in 1-2 sentences)
2. ROLE-BASED SECTIONS (numbered, one per role/team)
3. SUMMARY (1-line per role as a quick reference)
```

**When in doubt:** "What's new" is ONLY for emails where there is a single piece of news to announce. For everything else - meeting summaries, observations, data reports, process notes, instructions - skip the header and open with a direct context line.

### Minto Pyramid - Logic Order

1. **Answer first** - don't build up to the conclusion. State it, then support it.
2. **Group by theme** - not by chronology of the meeting.
3. **SCQA for decisions** - Situation, Complication, Question (implicit), Answer.
4. **Mutually exclusive points** - don't repeat the same idea in different words.

### Writing That Works - Tone

1. **Write for the scanner** - bold key terms, short paragraphs, white space
2. **Active voice** - "We finalized the approach" not "The approach was finalized"
3. **Specific, not vague** - "56 items" not "several items"
4. **No filler** - no "I hope this email finds you well", "As discussed"
5. **End with impact** - what this means for the project
6. **Future tense for upcoming work** - use "will" not present tense. Stakeholders should never read an email and think a feature is live when it's still in planning.

### HBR Guide - Sentence Craft (Garner)

1. **20 words per sentence average** - if a sentence exceeds 25 words, split it or cut words
2. **One goal per sentence**
3. **Contractions for tone** - use "I've", "we'll", "don't"
4. **Architect, Carpenter, Judge** - plan, draft, edit ruthlessly (cut 20-30%)
5. **Specifics over generalities** - numbers and names are credible

### On Writing Well - Decluttering (Zinsser)

1. **Strip every sentence**. "In order to" → "to". "At this point in time" → "now".
2. **Show the result, not the process**
3. **Kill jargon** - "Leverage" → "use". "Utilize" → "use". "Facilitate" → "help".
4. **No passive voice in emails**
5. **Simplicity is confidence**

### Made to Stick - Memorability (Heath Brothers)

1. **SUCCESs framework** - Simple, Unexpected, Concrete, Credible, Emotional, Story
2. **Lead with the unexpected**
3. **Concrete over abstract** - specific examples stick
4. **One core message per email**

## Formatting Rules

1. **Numbered lists ONLY** - NEVER use `<ul>`. Always `<ol>`. People need to say "point 3" in meetings, not count bullets.
2. **Lettered sub-items** - `a. b. c.` as plain text with `<br/>` for sub-points
3. **NEVER use em-dash** - always use regular dash (-)
4. **Bold for labels** - `<b>Section Name</b>` for every section header
5. **Every ticket hyperlinked** - `<a href="url">[PROJECT-XXXXX]</a>`
6. **Every wiki/doc page hyperlinked** - `<a href="url">Page Title</a>`
7. **Plain English for technical terms** - explain in parentheses
8. **Tables** - `<table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse; font-size:14px;">`. Use tables when data has 3+ rows and 3+ columns. Header row: `background-color:#f2f2f2`; totals row: bold + same background.
9. **No markdown in HTML body** - all formatting via HTML tags
10. **Under 400 words, 20 words/sentence average**
11. **@mention people in action items** - use the email provider's mention format (e.g., for Zoho: `<a target="_blank" class="ze_mention" href="mailto:email@[your-domain]">Full Name</a>`). Look up email from your team directory.
12. **NEVER fabricate email addresses or account IDs** - always look up from the team directory. If not found, use plain text and flag to user.

## Email Templates (by Type)

### Template: MoM / Decision Announcement

```html
<p>Hi all,</p>

<p><b>What's new:</b> [One sentence - the key decision or outcome]</p>

<p><b>Why it matters:</b> [One sentence - impact on project/timeline]</p>

<p><b>1. [Section title]</b></p>
<p>[1-2 sentences of context using SCQA]</p>

<p><b>2. [Section title]</b></p>
<p>a. [Point with why]<br/>
b. [Point with why]</p>

<p><b>3. What's next</b></p>
<p>a. [Owner @mention] - [specific action]<br/>
b. [Owner @mention] - [specific action]</p>

<p>[One line positioning - what this means for the project]</p>

<p><b>Reference:</b><br/>
Meeting ([purpose]): [attendee names]<br/>
Wiki: <a href="url">Page Title</a><br/>
Ticket: <a href="url">[PROJECT-XXXXX]</a></p>

<p>Regards,<br/>[your name]</p>
```

### Template: Data/Status Snapshot

```html
<p>Hi all,</p>

<p>Here is the [topic] breakdown as of [DD-MM-YYYY].</p>

<p>[One sentence - why the reader should care]</p>

<p><b>1. [Data section title]</b></p>
<table>
[Table with data, status columns, filter links, @mention leads]
[Total row with bold + background]
</table>

<p>[Callout for items outside filters, if any]</p>

<p><b>2. Key observations</b></p>
<p>a. [Observation with bold label and specific numbers]<br/>
b. [Observation]</p>

<p><b>3. What's next</b></p>
<p>a. [Owner @mention] - [specific action]</p>

<p>[One line - what this means for the project]</p>

<p><b>Reference:</b><br/>
Master filter: <a href="url">#XXXXX</a></p>

<p>Regards,<br/>[your name]</p>
```

### Template: Reply in Existing Thread

```html
<p>[Direct response - answer the question or share the update]</p>

<p>a. [Detail point]<br/>
b. [Detail point]</p>

<p>[Action items if needed]</p>

<p>Regards,<br/>[your name]</p>
```

### Template: Update Email

```html
<p>Hi all,</p>

<p>[Opening line - "What's new:" if genuine news, or direct context line]</p>

<p><b>Why it matters:</b> [One sentence - impact]</p>

<p><b>1. [Section title]</b></p>
<p>[Details]</p>

<p><b>2. What's next</b></p>
<p>a. [Owner @mention] - [specific action]</p>

<p>[One line positioning]</p>

<p><b>Reference:</b><br/>
[Links]</p>

<p>Regards,<br/>[your name]</p>
```

## Stakeholder Email Etiquette

1. **Don't attribute suggestions back to the person who made them** - just frame the suggestion cleanly. Never write "as you mentioned".
2. **Don't @mention people in the email body unless the user explicitly asks** - the CC list already provides visibility.
3. **Don't add editorial commentary on suggestions** - no priority judgments, no feasibility assessments. Frame clearly, let the reader draw conclusions.
4. **Don't decide who receives kudos or credit** - only include the names the user provides.
5. **Don't position the sender as directing someone above them in the reporting chain** - frame as organizing/capturing information.
6. **Don't assume technical details should be added or removed** - follow the user's lead.

## Self-Review Rubric (Run Before Saving Draft)

Score the draft on each point. Fix anything below 8 before saving.

| # | Criteria | Test |
|---|----------|------|
| 1 | Can the reader understand the key message in 10 seconds? | Read only the first 3 lines |
| 2 | Is the answer before the context? (Minto) | First sentence = conclusion |
| 3 | Does every section earn its space? | Remove it - does the email still work? |
| 4 | Are all lists numbered (no bullets)? | Grep for `<ul>` - should be zero |
| 5 | Are all links clickable? | No plain-text URLs or ticket IDs |
| 6 | Is every action item named with an owner? | No "Engineering - estimation needed" without a person |
| 7 | Are em-dashes absent? | Grep - should be zero |
| 8 | Is it under 400 words? | wc -w |
| 9 | Does it end with impact/positioning? | Last line before sign-off = "so what?" |
| 10 | Are attendees at the bottom, not the top? | Reference section, not metadata block |
| 11 | Average sentence length under 20 words? | Count words in 3 longest sentences - none should exceed 30 |
| 12 | Is there one concrete example or specific number? | At least one "e.g." or specific figure |

## Email Types — Detection and Routing

Determine the email type FIRST, then follow the matching structure and template.

### Type 1: MoM / Decision Announcement
- **Detect:** Source is a meeting file, user says "MoM", "meeting notes", "send minutes"
- **Structure:** "What's new" + "Why it matters" only if there is a single key decision to announce
- **Subject:** `MoM - <Short Title> (<DD Mon>)`
- **Audience:** meeting attendees + relevant stakeholders

### Type 2: Data/Status Snapshot
- **Detect:** Source is ticket data, filter results, dashboards. User says "pending issues", "status", "breakdown"
- **Structure:** Direct opening line (NO "What's new"), data table as primary content
- **Subject:** `[Project] | <Topic> - <Key Number> (<Summary>)`
- **Audience:** To = people who need to act. CC = their reporting managers.
- **Table rules:** Include status columns. Use @mentions for lead names. Include clickable filter links. NEVER link to dashboards - always use filter URLs.

### Type 3: Reply in Existing Thread
- **Detect:** User says "reply to", "respond to"
- **Structure:** No headers, direct response
- **Subject:** `Re: <existing thread>`
- Must include `inReplyTo` message ID for threading. Preserve To/CC from original thread.

### Type 4: Update Email
- **Detect:** Not a meeting, not data-driven, not a reply
- **Structure:** "What's new" only if genuine news; otherwise direct opening line
- **Subject:** `Re: <existing thread>` or `[Project] | Updates | <topic>`
- **Audience:** broader stakeholder chain

### Type 5: Process / Instructions Email
- **Detect:** User wants to communicate a workflow, process, or role assignment
- **Structure:** NO "What's new". Direct opening line. Role-based numbered sections. Summary at the end.
- **Subject:** `Process - <Short Title>`
- **Audience:** everyone who needs to follow the process

## Inputs

- **Source**: processed meeting file, conversation context, or user-provided content
  - Meeting file: `.local/meetings/processed/<monthname-yyyy>/<date>-<slug>.md`
  - If not specified, ask the user which meeting/topic to draft for
- **User directory**: `.local/team/users.md` - canonical name-to-email mapping (set up as a user convention)
- **Thread context**: if replying, search the email provider for the thread first

## Step 1 - Gather context

For MoM: Read the processed meeting file. Extract title, date, attendees, summary, decisions, action items.
For Updates: Gather from conversation - what was decided, by whom, with what rationale.
For Replies: Search the email provider for the thread, get the latest message ID, To/CC addresses.
For Data-Driven: Fetch live data first (ticket filters, API queries). Gather all numbers before drafting.

## Step 2 - Resolve attendee emails

Look up each attendee name in `.local/team/users.md` (match against Short Name or Full Name column).
If any name has no match, flag it and ask the user for the correct email before proceeding.

## Step 3 - Build the email

1. Determine email type using the detection rules above
2. Draft following the matching type-specific template
3. Run self-review rubric silently - fix any issues below score 8
4. Build the JSON and push to the email provider immediately
5. Report rubric scores to user after saving

## Step 4 - Compose email metadata

- **Subject**: context-dependent (MoM, Update, Reply)
- **To/CC**: from thread or attendee list
- **From**: `[your-email@your-domain]` (from env var)

## Step 5 - Push to email provider as draft

Pipe the JSON directly to a provider-specific script via stdin — no intermediate files needed:

```bash
echo '<json_string>' | python3 scripts/save-draft.py -
```

Do NOT write to `.local/scratch/` or any local file. The provider's draft is the only copy needed.
Always saves as draft - never sends.

The bundled `scripts/save-draft.py` is a Zoho Mail implementation. Adapt it to your provider (Gmail, Outlook, Fastmail, etc.) by replacing the API calls and auth flow. All provider credentials must come from env vars — no hardcoded URLs or account IDs.

## Step 6 - Confirm to user

Report: draft saved to [provider], any unresolved emails flagged.

## Anti-Patterns

1. **Hardcoding sender email or account ID** — always read from env vars.
2. **Saving to local files instead of provider drafts** — the draft lives in the mail client.
3. **Using bullet lists (`<ul>`)** — violates the numbered-lists rule.
4. **Inventing email addresses** when a name isn't in the team directory — flag instead.
5. **Adding @mentions in the body without user approval** — CC list is visibility; body mentions are the user's call.

## Quality Checklist

- [ ] All sender and account details come from env vars (no hardcoded emails/IDs)
- [ ] All list items are `<ol>`, never `<ul>`
- [ ] No em-dashes anywhere in the body
- [ ] Every attendee name is resolved via the team directory (or flagged)
- [ ] Self-review rubric scores all ≥ 8
- [ ] Saved as draft, never sent
- [ ] Under 400 words
