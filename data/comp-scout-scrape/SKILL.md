---
name: comp-scout-scrape
description: Scrape competition websites, extract structured data, and auto-persist to GitHub issues. Creates issues for new competitions, adds comments for duplicates.
---

# Competition Scraper

Scrape creative writing competitions from Australian aggregator sites and **automatically persist to GitHub**.

## What This Skill Does

1. Scrapes competitions.com.au and netrewards.com.au
2. Extracts structured data (dates, prompts, prizes)
3. **Checks for duplicates** against existing GitHub issues (by URL and title similarity)
4. Creates issues for **NEW** competitions only
5. Adds comments to existing issues when same competition found on another site
6. Skips competitions that are already tracked

**The scraper already filters out sponsored/lottery ads. Your job is to check for duplicates, then persist only new competitions.**

## What Counts as "New"

A competition is NEW if:
- Its URL is not found in any existing issue body (check the full body text, not just the primary URL field)
- AND its normalized title is <80% similar to all existing issue titles

A competition is a DUPLICATE if:
- Its URL appears anywhere in an existing issue (body text, comments) → already tracked, skip
- Its normalized title is >80% similar to an existing issue title → likely same competition, skip
- Same competition found on a different aggregator site → add comment to existing issue noting the alternate URL

**Note:** An issue body may contain multiple URLs (one per aggregator site). When checking for duplicates, search the entire issue body for the scraped URL, not just a specific field.

## Word Limit Clarification

**"25WOL" is a category name, NOT a filter.** Competitions with 25, 50, or 100 word limits are all valid creative writing competitions - persist them all (if new).

## Prerequisites

```bash
pip install playwright
playwright install chromium
```

Also requires:
- `gh` CLI authenticated
- Target repository for competition data (not this skills repo)

## Workflow

### Step 1: Determine Target Repository

The target repo stores competition issues. Specify or get from config:

```bash
# From workspace config (if hiivmind-pulse-gh initialized)
TARGET_REPO=$(yq '.repositories[0].full_name' .hiivmind/github/config.yaml 2>/dev/null)

# Or use default/specified
TARGET_REPO="${TARGET_REPO:-discreteds/competition-data}"
```

### Step 2: Scrape Listings

Run the scraper to get structured competition data:

```bash
python skills/comp-scout-scrape/scraper.py listings
```

**Output:**
```json
{
  "competitions": [
    {
      "url": "https://competitions.com.au/win-example/",
      "site": "competitions.com.au",
      "title": "Win a $500 Gift Card",
      "normalized_title": "500 gift card",
      "brand": "Example Brand",
      "prize_summary": "$500",
      "prize_value": 500,
      "closing_date": "2024-12-31"
    }
  ],
  "scrape_date": "2024-12-09",
  "errors": []
}
```

### Step 3: Check for Existing Issues

For each scraped competition, check if it already exists:

```bash
# Get all open competition issues
gh issue list -R "$TARGET_REPO" \
  --label "competition" \
  --state open \
  --json number,title,body \
  --limit 200
```

**Match by:**
1. URL in issue body (exact match = definite duplicate)
2. Normalized title similarity (>80% = likely duplicate)

### Step 4: Fetch Details for New Competitions

For competitions not already tracked, get full details:

```bash
python skills/comp-scout-scrape/scraper.py detail "https://competitions.com.au/win-example/"
```

For multiple new competitions, use batch mode:

```bash
echo '{"urls": ["url1", "url2", ...]}' | python skills/comp-scout-scrape/scraper.py details-batch
```

### Step 4.5: Apply Auto-Tagging Rules (NOT Filtering)

**IMPORTANT: Auto-tagging is for LABELING issues, not for skipping/excluding competitions.**

Check competitions against user preferences from the data repo's CLAUDE.md to determine which labels to apply.

1. Fetch preferences:
```bash
gh api repos/$TARGET_REPO/contents/CLAUDE.md -H "Accept: application/vnd.github.raw" 2>/dev/null
```

2. Parse the Detection Keywords section for tagging rules

3. For each competition, check if title/prize matches any keywords:
```
For each tag_rule in [for-kids, cruise]:
  For each keyword in tag_rule.keywords:
    If keyword.lower() in (competition.title + competition.prize_summary).lower():
      Add tag_rule.label to issue labels
```

4. **ALL competitions are ALWAYS persisted as issues.** Tagged competitions:
   - Get the relevant label applied (e.g., `for-kids`, `cruise`)
   - Are closed immediately with explanation comment
   - But they ARE STILL CREATED as issues (for record-keeping and potential review)

### Step 5: Auto-Persist Results

#### For New Competitions → Create Issue

```bash
gh issue create -R "$TARGET_REPO" \
  --title "$TITLE" \
  --label "competition" \
  --label "25wol" \
  --body "$(cat <<'EOF'
## Competition Details

**URL:** {url}
**Brand:** {brand}
**Prize:** {prize_summary}
**Word Limit:** {word_limit} words
**Closes:** {closing_date}
**Draw Date:** {draw_date}
**Winners Notified:** {notification_info}

## Prompt

> {prompt}

---
*Scraped from {site} on {scrape_date}*
EOF
)"
```

Then set milestone by closing month:
```bash
gh issue edit $ISSUE_NUMBER -R "$TARGET_REPO" --milestone "December 2024"
```

#### For Duplicates → Add Comment

If competition URL found on another site:

```bash
gh issue comment $EXISTING_ISSUE -R "$TARGET_REPO" --body "$(cat <<'EOF'
### Also found on {other_site}

**URL:** {url}
**Title on this site:** {title}
*Discovered: {date}*
EOF
)"
```

#### For Filtered Competitions → Create Issue + Close

If competition matched auto-filter keywords:

```bash
# Create the issue first (for record-keeping)
ISSUE_URL=$(gh issue create -R "$TARGET_REPO" \
  --title "$TITLE" \
  --label "competition" \
  --label "25wol" \
  --label "$FILTER_LABEL" \
  --body "...")

# Extract issue number
ISSUE_NUMBER=$(echo "$ISSUE_URL" | grep -oE '[0-9]+$')

# Close with explanation
gh issue close $ISSUE_NUMBER -R "$TARGET_REPO" --comment "$(cat <<'EOF'
Auto-filtered: matches '$KEYWORD' in $FILTER_RULE preferences.

See CLAUDE.md in this repository for filter settings.
EOF
)"
```

### Step 6: Report Results

Present confirmation to user:

```
✅ Scrape complete!

**Created 3 new issues:**
- #42: Win a $500 Coles Gift Card (closes Dec 31)
- #43: Win a Trip to Bali (closes Jan 15)
- #44: Win a Year's Supply of Coffee (closes Dec 20)

**Auto-filtered 2 (created + closed):**
- #45: Win Lego Set (for-kids: matched "Lego")
- #46: Win P&O Cruise (cruise: matched "P&O")

**Found 2 duplicates (added as comments):**
- #38: Win Woolworths Gift Cards (also on netrewards.com.au)
- #39: Win Dreamworld Experience (also on netrewards.com.au)

**Skipped 7 already tracked**
```

**IMPORTANT:** Do NOT ask "Would you like me to analyze these?" at the end. When invoked by `comp-scout-daily`, the workflow will automatically invoke analyze/compose skills next. Report results and stop.

## Output Fields

### Listing Output

| Field | Type | Description |
|-------|------|-------------|
| url | string | Full URL to competition detail page |
| site | string | Source site (competitions.com.au or netrewards.com.au) |
| title | string | Competition title as displayed |
| normalized_title | string | Lowercase, prefixes stripped, for matching |
| brand | string | Sponsor/brand name (if available) |
| prize_summary | string | Prize description or value badge |
| prize_value | int/null | Numeric value in dollars |
| closing_date | string/null | YYYY-MM-DD format |

### Detail Output

All listing fields plus:

| Field | Type | Description |
|-------|------|-------------|
| prompt | string | The actual competition question/prompt |
| word_limit | int | Maximum words (default 25) |
| entry_method | string | How to submit entry |
| winner_notification | object/null | Notification details from JSON-LD |
| scraped_at | string | ISO timestamp of scrape |

### Winner Notification Object

| Field | Type | Description |
|-------|------|-------------|
| notification_text | string | Raw notification text |
| notification_date | string/null | Specific date if mentioned |
| notification_days | int/null | Days after close/draw |
| selection_text | string | How winners are selected |
| selection_date | string/null | When judging occurs |

## Title Normalization

Titles are normalized for deduplication:

1. Lowercase
2. Strip prefixes: "Win ", "Win a ", "Win an ", "Win the ", "Win 1 of "
3. Remove punctuation
4. Collapse whitespace

**Example:**
```
Original: "Win a $500 Coles Gift Card"
Normalized: "500 coles gift card"
```

## Example Session

```
User: Scrape competitions

Claude: I'll scrape competitions and persist new ones to GitHub.

[Runs: python skills/comp-scout-scrape/scraper.py listings]

Found 12 competitions from both sites.

[Runs: gh issue list -R discreteds/competition-data --label competition --json number,title,body]

Checking against 45 existing issues...
- 3 are new
- 2 are duplicates (same competition, different source)
- 7 already tracked

Fetching details for 3 new competitions...

[Creates issues and adds comments]

✅ Scrape complete!

**Created 3 new issues:**
- #46: Win a $500 Coles Gift Card (closes Dec 31)
  - Milestone: December 2024
- #47: Win a Trip to Bali (closes Jan 15)
  - Milestone: January 2025
- #48: Win a Year's Supply of Coffee (closes Dec 20)
  - Milestone: December 2024

**Added 2 duplicate comments:**
- #38: Also found on netrewards.com.au
- #39: Also found on netrewards.com.au

```

## CLI Commands Reference

```bash
# Scrape all listing pages
python skills/comp-scout-scrape/scraper.py listings

# Get full details for one competition
python skills/comp-scout-scrape/scraper.py detail "URL"

# Get full details for multiple competitions (batch mode)
echo '{"urls": ["url1", "url2"]}' | python skills/comp-scout-scrape/scraper.py details-batch

# Debug: just get URLs
python skills/comp-scout-scrape/scraper.py urls
```

### Batch Details Output

```json
{
  "details": [
    {
      "url": "...",
      "title": "...",
      "prompt": "Tell us in 25 words...",
      "word_limit": 25,
      ...
    }
  ],
  "scrape_date": "2024-12-09",
  "errors": []
}
```

## Persistence Details

This skill handles all GitHub persistence. The separate `comp-scout-persist` skill is **deprecated** - its functionality is merged here.

### Issue Creation Template

```markdown
## Competition Details

**URL:** {url}
**Brand:** {brand}
**Prize:** {prize_summary}
**Word Limit:** {word_limit} words
**Closes:** {closing_date}
**Draw Date:** {draw_date}
**Winners Notified:** {notification_info}

## Prompt

> {prompt}

---
*Scraped from {site} on {scrape_date}*
```

### Labels

| Label | Description | Auto-applied |
|-------|-------------|--------------|
| `competition` | All competition issues | Always |
| `25wol` | 25 words or less type | Always |
| `for-kids` | Auto-filtered (kids competitions) | When keyword matches |
| `cruise` | Auto-filtered (cruise competitions) | When keyword matches |
| `closing-soon` | Closes within 3 days | By separate check |
| `entry-drafted` | Entry has been composed | By comp-scout-compose |
| `entry-submitted` | Entry has been submitted | Manually |

### Milestones

Issues are assigned to milestones by closing date month:
- "December 2024"
- "January 2025"
- etc.

```bash
# Create milestone if needed
gh api repos/$TARGET_REPO/milestones \
  --method POST \
  --field title="$MONTH_YEAR" \
  --field due_on="$LAST_DAY_OF_MONTH"

# Assign to issue
gh issue edit $ISSUE_NUMBER -R "$TARGET_REPO" --milestone "$MONTH_YEAR"
```

### Duplicate Comment Template

```markdown
### Also found on {other_site}

**URL:** {url}
**Title on this site:** {title}
*Discovered: {date}*
```

### Filtered Issue Handling

When a competition matches filter keywords:
1. Issue is created (for record-keeping)
2. Filter label is applied (e.g., `for-kids`)
3. Issue is immediately closed with explanation

```bash
gh issue close $ISSUE_NUMBER -R "$TARGET_REPO" \
  --comment "Auto-filtered: matches '$KEYWORD' in $FILTER_RULE preferences."
```

## Integration

This skill is invoked by `comp-scout-daily` as the first step in the workflow.

After scraping, you can:
- Use **comp-scout-analyze** to generate entry strategies
- Use **comp-scout-compose** to write actual entries
- Both will auto-persist their results as comments on the issue
