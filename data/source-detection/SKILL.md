---
name: source-detection
description: Detect document source type (Zoom, Slack, JIRA, Confluence, email, meeting notes) from content patterns. Use when processing raw documents during intake or when identifying document types.
---

# Source Detection Patterns

Use these patterns to identify document source types from plain text content.

## Detection Priority

Check patterns in this order (first match wins with high confidence):
1. Zoom transcripts (most distinctive patterns)
2. Slack conversations
3. JIRA tickets
4. Confluence/wiki pages
5. Email threads
6. Meeting notes
7. General notes (default)

## Zoom Transcript

**High confidence indicators** (any 2+ = zoom):
- Timestamps in `HH:MM:SS` format (e.g., `00:15:32`, `01:23:45`)
- Speaker labels with colon: `John Smith:` followed by text
- `WEBVTT` header at start of file
- Multiple speakers with consistent formatting

**Medium confidence indicators** (supporting evidence):
- Phrases: "you're on mute", "can you hear me", "let me share my screen"
- "unmute", "muted", "screen share"
- Time-based speaker transitions

**Example patterns:**
```
WEBVTT

00:00:15.000 --> 00:00:20.000
John Smith: Good morning everyone, let's get started.

00:00:21.000 --> 00:00:25.000
Jane Doe: Hi John, can you hear me okay?
```

## Slack Conversation

**High confidence indicators** (any 2+ = slack):
- Channel references: `#channel-name`
- User mentions: `@username` or `@User Name`
- Timestamp formats: `10:30 AM`, `2:45 PM`, `14:30`
- Thread markers: "replied to a thread", "Thread", "in thread"

**Medium confidence indicators:**
- Emoji reactions: `:thumbsup:`, `:+1:`, `:smile:`
- Bot messages with structured formatting
- "Slack" mentioned in content
- Day/date groupings: "Monday, January 15th"

**Example patterns:**
```
#data-pipeline
Monday, January 15th

@john.smith 10:30 AM
Hey team, quick update on the migration

@jane.doe 10:32 AM
Thanks! :+1: Can you share the timeline?

  replied to a thread:
  @john.smith: Sure, here's the breakdown...
```

## JIRA Ticket

**High confidence indicators** (any 2+ = jira):
- Ticket ID pattern: `[A-Z]{2,10}-\d+` (e.g., `PROJ-1234`, `DATA-567`)
- Section headers: "Summary:", "Description:", "Acceptance Criteria:"
- Status fields: "Status:", "Priority:", "Assignee:", "Reporter:"

**Medium confidence indicators:**
- Status values: "To Do", "In Progress", "Done", "Blocked", "In Review"
- "Story Points:", "Sprint:", "Epic Link:"
- "Components:", "Labels:", "Fix Version:"
- Atlassian/JIRA mentioned

**Example patterns:**
```
PROJ-1234: Implement user authentication

Status: In Progress
Priority: High
Assignee: John Smith
Reporter: Jane Doe

Description:
As a user, I want to log in securely...

Acceptance Criteria:
- [ ] User can log in with email/password
- [ ] Session expires after 30 minutes
```

## Confluence/Wiki

**High confidence indicators** (any 2+ = confluence):
- Page/Space references: "Page:", "Space:", "Parent:"
- Wiki-style headers with `=` signs: `== Section ==`
- Confluence macros: `{code}`, `{info}`, `{note}`, `{panel}`
- Table of contents patterns

**Medium confidence indicators:**
- Breadcrumb paths: `Space > Parent Page > This Page`
- "Last modified by", "Created by" with timestamps
- Atlassian/Confluence mentioned
- Wiki-style links: `[[Page Name]]` or `[Link Text|Page Name]`

**Example patterns:**
```
Space: Engineering
Page: Architecture Overview

Created by: John Smith | Last modified: Jan 15, 2024

= Architecture Overview =

== Components ==

{info}
This document describes the high-level architecture.
{info}
```

## Email Thread

**High confidence indicators** (any 2+ = email):
- Headers: "From:", "To:", "Subject:", "Date:", "Sent:"
- Email addresses: `name@domain.com`
- Reply indicators: "Re:", "RE:", "Fwd:", "FW:"

**Medium confidence indicators:**
- CC/BCC fields
- Signature blocks (lines starting with `--` or common sign-offs)
- "Original Message" or "Forwarded message"
- Quote indicators: `>` at start of lines

**Example patterns:**
```
From: John Smith <john.smith@company.com>
To: Jane Doe <jane.doe@company.com>
Subject: Re: Quarterly Planning
Date: Mon, Jan 15, 2024 10:30 AM

Hi Jane,

Thanks for sending over the proposal...

--
John Smith
Senior Engineer
```

## Meeting Notes

**High confidence indicators** (any 2+ = meeting):
- Section headers: "Agenda", "Attendees", "Action Items", "Minutes"
- Structured bullet lists under sections
- Date header at document start
- "Meeting" in title or first lines

**Medium confidence indicators:**
- Time references for agenda items
- Names followed by task assignments
- "Next meeting:", "Follow-up:"
- Decision markers: "Decided:", "Agreed:", "TODO:"

**Example patterns:**
```
Meeting Notes - Sprint Planning
Date: January 15, 2024

Attendees:
- John Smith
- Jane Doe
- Bob Wilson

Agenda:
1. Review previous sprint
2. Plan upcoming work

Action Items:
- [ ] John: Update documentation
- [ ] Jane: Review PRs
```

## General Notes (Default)

If no specific pattern matches with confidence, classify as `notes`.

**Indicators that confirm "notes":**
- Unstructured text
- Personal notes style
- Mixed content without clear source indicators
- Bullet points without meeting structure

## Confidence Levels

- **High**: 2+ high-confidence indicators match
- **Medium**: 1 high-confidence indicator OR 3+ medium-confidence indicators
- **Low**: Only medium-confidence indicators OR uncertain match

## Output Format

When detecting source, return:
```yaml
source: zoom|slack|jira|confluence|email|meeting|notes
confidence: high|medium|low
indicators:
  - "indicator 1 found"
  - "indicator 2 found"
```
