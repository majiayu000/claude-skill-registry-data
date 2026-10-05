---
name: granola
version: 1.0.0
description: "Pull meeting notes from Granola. Use when the user mentions 'Granola,' 'meeting notes,' 'pull notes from a meeting,' 'grab meeting notes,' or wants to import meeting context for content creation, brain file updates, or case study research."
---

# Granola Meeting Notes

Pull meeting notes from Granola's API via the CLI wrapper at `.claude/skills/granola/granola.sh`.

## Setup

The user needs a Granola API key (requires Business or Enterprise plan):

1. Open Granola desktop app > Settings > API > "Create new key"
2. Add it to the project `.env` file: `GRANOLA_API_KEY=grn_your_key_here`

If the key isn't configured, the script will tell the user what to do.

## Commands

```bash
SCRIPT=".claude/skills/granola/granola.sh"

# List recent notes (last 7 days)
$SCRIPT recent

# List notes from last N days
$SCRIPT recent 30

# List with date filters
$SCRIPT list --after 2026-04-01 --before 2026-04-07

# Get a specific note (summary only)
$SCRIPT get not_ABC123DEF456GH

# Get a note with full transcript
$SCRIPT get not_ABC123DEF456GH --transcript

# Pull a note into /incoming/ (includes transcript by default)
$SCRIPT pull not_ABC123DEF456GH

# Get raw JSON output (for any command)
$SCRIPT list --json
$SCRIPT get not_ABC123DEF456GH --json
```

## Workflow

When the user asks to pull meeting notes:

### 1. List available notes

Run `recent` or `list` with appropriate date filters to show what's available. Let the user pick which meeting(s) they want.

### 2. Fetch the note

Use `get` with `--transcript` to see the full content. Review the summary and transcript.

### 3. Decide where it goes

Based on the meeting content, route it appropriately:

| Content type | Destination |
|---|---|
| Customer call, demo, sales conversation | `pull` to `/incoming/`, then mine for brain file updates, case study material, or audience language |
| Product feedback, feature requests | Extract insights, suggest updates to `/brain/truth.md` or `/brain/positioning-and-messaging.md` |
| Internal strategy discussion | Summarize key decisions, suggest project memory updates |
| Partner or analyst meeting | Extract relevant intelligence for `/brain/market-signals.md` |
| Content planning meeting | Extract ideas for `/marketing/inspiration/content-ideas.md` |

### 4. Process the notes

Apply the same rigor used for Apollo transcript mining:
- Interpret through context (meeting notes may have transcription errors)
- Extract actual customer/prospect language for `/brain/audience-language.md`
- Identify conversion triggers and objections for `/brain/customer-journey.md`
- Flag any product claims that need verification against `/brain/truth.md`
- Never parrot raw transcript, always synthesize

## Important Notes

- The API is **read-only** and returns only notes with AI-generated summaries
- No search endpoint exists; use date filters to narrow results, then review locally
- Page size max is 30; use `--cursor` for pagination
- Rate limit: 5 requests/second (burst 25). Don't hammer it
- Transcript speakers are labeled "You" (microphone) and "Other" (speaker audio); actual names come from the attendees list
- The `/incoming/` folder is the user's drop zone; `pull` writes there by convention so the standard intake workflow applies
