---
name: comp-scout-notify
description: Send beautifully formatted HTML digest emails summarizing open competitions, their status, and strategy. Supports dark mode, closing soon highlights, and multiple recipients.
---

# Competition Digest Notifier

Send beautifully formatted HTML email digests summarizing open competitions.

## What This Skill Does

1. Queries GitHub issues for open competitions
2. Extracts competition details, strategy, and draft entries
3. Formats as HTML email with dark mode support
4. Highlights competitions closing soon
5. Sends via SMTP to configured recipients

## Prerequisites

- `gh` CLI authenticated
- Target repository with competition issues
- SMTP credentials configured (for sending)

## Configuration

Set environment variables or add to `.env`:

```bash
# SMTP Settings
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your@email.com
SMTP_PASSWORD=app-specific-password

# Recipients (comma-separated)
EMAIL_TO=recipient1@email.com,recipient2@email.com
EMAIL_FROM=Competition Scout <your@email.com>

# Target repository (optional, uses config or default)
TARGET_REPO=discreteds/competition-data
```

### Gmail Setup

For Gmail, create an App Password:
1. Go to Google Account → Security → 2-Step Verification
2. At bottom, click "App passwords"
3. Generate password for "Mail"
4. Use this as `SMTP_PASSWORD`

## Workflow

### Step 1: Build Digest

Query GitHub issues and build digest data:

```bash
python skills/comp-scout-notify/notifier.py json
```

This queries:
- All open issues with `competition` label
- Comments on each issue (for strategy/entries)

### Step 2: Send Email

Send the digest to configured recipients:

```bash
python skills/comp-scout-notify/notifier.py send
```

### Step 3: Preview (Optional)

Save HTML/TXT/JSON to `/tmp` for preview:

```bash
python skills/comp-scout-notify/notifier.py preview
# Then open /tmp/competition-digest.html in browser
```

## Email Features

### Dark Mode Support
Email automatically adapts to recipient's dark/light mode preference.

### Quick Summary Table
| Competition | Prize | Closes | Status |
|-------------|-------|--------|--------|
| Win $500 Gift Card | $500 | 15 Dec | Drafted |
| Win Trip to Bali | $5,000 | 20 Dec | Analyzed |

Status shows: New → Analyzed → Drafted → Submitted

### Closing Soon Section
Competitions closing within 3 days are highlighted in red with special section.

### Competition Cards
Each competition shows:
- Title with closing date badge
- Prize summary
- Prompt with word limit
- Strategy (if analyzed): recommended tone, themes, angles
- Draft entries (if composed)
- "Enter Competition" button

### Plain Text Fallback
For email clients that don't support HTML, a plain text version is included.

## CLI Commands

```bash
# Send digest email
python skills/comp-scout-notify/notifier.py send

# Preview (save to /tmp)
python skills/comp-scout-notify/notifier.py preview

# Output JSON digest
python skills/comp-scout-notify/notifier.py json
```

## Example Session

```
User: Send me a competition digest

Claude: I'll build and send the competition digest.

[Runs: python skills/comp-scout-notify/notifier.py send]

Building digest from discreteds/competition-data...
Found 12 competitions (3 closing soon)
Connecting to smtp.gmail.com:587...
Email sent to 2 recipient(s)

✅ Digest sent!

**Summary:**
- 12 total competitions
- 3 closing soon (highlighted)
- 8 with strategy
- 5 with draft entries

Recipients: user@email.com, other@email.com
```

## Integration

### With comp-scout-daily (End-to-End Workflow)

The notify skill is called automatically at the end of the daily workflow:

```
1. Scrape competitions
2. Analyze new ones
3. Compose entries
4. Send digest email ← comp-scout-notify
```

### Standalone Usage

Can also be invoked directly:
- "Send me a competition digest"
- "Email me the competition summary"
- "Send digest to user@email.com"

## Data Extraction

### From Issue Body
- Title, URL, Brand
- Prize summary
- Closing date, Draw date
- Winners notification
- Prompt (from blockquote)

### From Issue Comments
- Strategy Analysis:
  - Sponsor category
  - Recommended tone
  - Themes, Words, Angles
  - Things to avoid
- Entry Drafts:
  - Option text
  - Word count

### From Issue Labels
- `entry-drafted` → Has draft entries
- `entry-submitted` → Already submitted
- `closing-soon` → Closing within 3 days

## Email Template Structure

```
┌─────────────────────────────────────┐
│  Competition Scout                  │
│  Monday, 9 December 2024            │
├─────────────────────────────────────┤
│  ┌────────┐ ┌────────┐              │
│  │   12   │ │   3    │              │
│  │ Total  │ │  New   │              │
│  └────────┘ └────────┘              │
├─────────────────────────────────────┤
│  Quick Summary Table                │
│  ┌───────────────────────────────┐  │
│  │ Competition │ Prize │ Closes │  │
│  ├───────────────────────────────┤  │
│  │ Win $500... │ $500  │ 15 Dec │  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│  ⚡ Closing Soon (red section)      │
│  ┌───────────────────────────────┐  │
│  │ Competition Card              │  │
│  │ - Title + badges              │  │
│  │ - Prize                       │  │
│  │ - Prompt                      │  │
│  │ - Strategy                    │  │
│  │ - [Enter Competition]         │  │
│  └───────────────────────────────┘  │
├─────────────────────────────────────┤
│  All Competitions                   │
│  [Competition cards...]             │
├─────────────────────────────────────┤
│  Generated by Competition Scout     │
└─────────────────────────────────────┘
```

## Troubleshooting

### "SMTP credentials not configured"
Set `SMTP_USERNAME` and `SMTP_PASSWORD` environment variables.

### "No recipients configured"
Set `EMAIL_TO` environment variable (comma-separated for multiple).

### "Authentication failed" (Gmail)
- Enable 2-Step Verification
- Generate App Password (not your regular password)
- Ensure "Less secure apps" is not the issue (use App Password instead)

### Empty digest
- Check `TARGET_REPO` points to correct repository
- Verify issues have `competition` label
- Run `gh issue list -R REPO --label competition` to verify
