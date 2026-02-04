---
name: comp-scout-persist
description: "[DEPRECATED] Persistence logic has been merged into comp-scout-scrape. This skill remains for reference only."
---

# Competition Persistence (DEPRECATED)

> **⚠️ This skill is deprecated.** Its functionality has been merged into `comp-scout-scrape`.
>
> The scrape skill now handles:
> - Issue creation
> - Duplicate detection and comments
> - Milestone assignment
> - Auto-filter labeling and closing
>
> This file is retained for reference only. Do not invoke this skill directly.

---

## Original Documentation (Reference Only)

Store competitions as GitHub issues with project board integration.

## Prerequisites

- `gh` CLI installed and authenticated
- `yq` installed for YAML parsing
- hiivmind-pulse-gh workspace initialized (for project integration)
- Target repository created (separate from this skills repo)

## Key Concepts

### Issue as Dumping Ground

Each competition gets ONE issue. All related information is added as comments:
- Additional sources (from other aggregator sites)
- Strategy analysis
- Draft entries
- Submission confirmation
- Winner notification

### Simplified Deduplication

No complex parent-child relationships. When a duplicate is found:
1. Add a comment to the existing issue noting the additional source
2. Don't create a new issue

## Workflow

### Step 1: Determine Target Repository

The target repo should be specified or configured. This is NOT the skills repo.

```bash
# From workspace config
TARGET_REPO=$(yq '.repositories[0].full_name' .hiivmind/github/config.yaml)

# Or specify directly
TARGET_REPO="discreteds/competition-data"
```

### Step 2: Normalize Title for Matching

Strip common prefixes and normalize for comparison:

```
Original: "Win a $500 Coles Gift Card"
Normalized: "500 coles gift card"

Original: "Win 1 of 10 Travel Vouchers"
Normalized: "1 of 10 travel vouchers"
```

**Normalization rules:**
1. Lowercase
2. Strip prefixes: "Win ", "Win a ", "Win an ", "Win the ", "Win 1 of "
3. Remove punctuation
4. Collapse whitespace

### Step 3: Search for Existing Issues

```bash
gh issue list -R "$TARGET_REPO" \
  --label "competition" \
  --state open \
  --json number,title,url,body \
  --limit 100
```

### Step 4: Check for Duplicates

Compare normalized titles with fuzzy matching (80% similarity threshold).

**Also check:** If the competition URL appears in any issue body, it's definitely a duplicate.

```bash
# Search by URL in body
gh issue list -R "$TARGET_REPO" \
  --search "in:body $COMPETITION_URL" \
  --json number,title,url
```

### Step 5a: If Duplicate Found

Add a comment to the existing issue:

```bash
gh issue comment $ISSUE_NUMBER -R "$TARGET_REPO" --body "$(cat <<'EOF'
### Also found on netrewards.com.au

**URL:** https://netrewards.com.au/win-example/
**Title on this site:** Win Example Prize
*Discovered: 2024-12-09*
EOF
)"
```

### Step 5b: If New Competition

Create the issue:

```bash
gh issue create -R "$TARGET_REPO" \
  --title "$TITLE" \
  --label "competition" \
  --label "25wol" \
  --body "$(cat <<'EOF'
## Competition Details

**URL:** https://competitions.com.au/win-example/
**Brand:** Example Brand
**Prize:** $500 gift card
**Word Limit:** 25 words
**Closes:** 2024-12-31
**Draw Date:** 2025-01-07
**Winners Notified:** 2025-01-14

## Prompt

> Tell us in 25 words or less why you love Example Brand

---
*Scraped from competitions.com.au on 2024-12-09*
EOF
)"
```

### Step 6: Add to Project (Optional)

If using GitHub Projects:

```bash
# Get issue URL from creation output
ISSUE_URL="https://github.com/discreteds/competition-data/issues/1"

# Add to project
gh project item-add 5 --owner discreteds --url "$ISSUE_URL"
```

### Step 7: Set Milestone

Create or find milestone for the closing date month:

```bash
# Check if milestone exists
MILESTONE_TITLE="December 2024"
MILESTONE=$(gh api repos/$TARGET_REPO/milestones --jq ".[] | select(.title==\"$MILESTONE_TITLE\") | .number")

# Create if needed
if [ -z "$MILESTONE" ]; then
  gh api repos/$TARGET_REPO/milestones \
    --method POST \
    --field title="$MILESTONE_TITLE" \
    --field due_on="2024-12-31T23:59:59Z"
fi

# Set on issue
gh issue edit $ISSUE_NUMBER -R "$TARGET_REPO" --milestone "$MILESTONE_TITLE"
```

## Issue Templates

### New Competition Issue

```markdown
## Competition Details

**URL:** {url}
**Brand:** {brand}
**Prize:** {prize_summary}
**Word Limit:** {word_limit} words
**Closes:** {closing_date}
**Draw Date:** {draw_date}
**Winners Notified:** {winners_notified_date}

## Prompt

> {prompt}

---
*Scraped from {site} on {scraped_date}*
```

### Additional Source Comment

```markdown
### Also found on {site}

**URL:** {url}
**Title on this site:** {title}
*Discovered: {date}*
```

### Strategy Comment

```markdown
## Strategy Analysis

**Sponsor Category:** {sponsor_category}
**Brand Voice:** {brand_voice}
**Recommended Tone:** {recommended_tone}

### Approach
{approach}

### Themes to Use
{themes_list}

### Angle Ideas
{angle_ideas_list}

### Avoid
{avoid_list}

---
*Generated: {date}*
```

### Entry Draft Comment

```markdown
## Entry Drafts

### Option 1 ({word_count} words) ⭐⭐⭐⭐⭐
> {entry_text}

Arc: {arc_type}
Notes: {notes}

### Option 2 ({word_count} words) ⭐⭐⭐⭐
> {entry_text}

Arc: {arc_type}
Notes: {notes}

**Recommendation:** Option {n} - {reason}

---
*Generated: {date}*
```

### Submission Confirmation Comment

```markdown
## Entry Submitted ✅

**Submitted:** {date}
**Entry used:** Option {n}

> {final_entry_text}

---
Now waiting for results. Draw date: {draw_date}
```

### Winner Notification Comment

```markdown
## Result: {WON|DID NOT WIN}

**Notified:** {date}
**Result:** {description}

{additional_notes}
```

## Labels

Create these labels in the target repository:

| Label | Color | Description |
|-------|-------|-------------|
| `competition` | `#0366d6` | All competition issues |
| `25wol` | `#6f42c1` | 25 words or less type |
| `closing-soon` | `#d73a49` | Closes within 3 days |
| `entry-drafted` | `#28a745` | Entry has been composed |
| `entry-submitted` | `#0075ca` | Entry has been submitted |
| `won` | `#ffd700` | Won the competition! |

### Label Management

```bash
# Create labels
gh label create "competition" --color "0366d6" -R "$TARGET_REPO"
gh label create "25wol" --color "6f42c1" -R "$TARGET_REPO"
gh label create "closing-soon" --color "d73a49" -R "$TARGET_REPO"
gh label create "entry-drafted" --color "28a745" -R "$TARGET_REPO"
gh label create "entry-submitted" --color "0075ca" -R "$TARGET_REPO"
gh label create "won" --color "ffd700" -R "$TARGET_REPO"

# Add label to issue
gh issue edit $ISSUE_NUMBER -R "$TARGET_REPO" --add-label "entry-drafted"

# Remove label
gh issue edit $ISSUE_NUMBER -R "$TARGET_REPO" --remove-label "closing-soon"
```

## Milestone Strategy

Use milestones to track competitions by closing month:

- "December 2024"
- "January 2025"
- "February 2025"

This allows filtering by timeframe in the project board.

## Example Session

```
User: Save these competitions to GitHub

Competitions:
1. Win $500 Coles Gift Card (closes Dec 31)
2. Win a Trip to Bali (closes Jan 15)
3. Win Year's Supply of Coffee (closes Dec 20)

Claude: I'll persist these to the competition-data repository.

Checking for existing issues...
- "Win $500 Coles Gift Card" - Not found, creating new issue
- "Win a Trip to Bali" - Not found, creating new issue
- "Win Year's Supply of Coffee" - Found existing issue #12 (from competitions.com.au)

Creating issues...

✅ Created issue #15: Win $500 Coles Gift Card
   - Added to project
   - Milestone: December 2024

✅ Created issue #16: Win a Trip to Bali
   - Added to project
   - Milestone: January 2025

✅ Added comment to issue #12: Win Year's Supply of Coffee
   - Noted additional source from netrewards.com.au

Summary:
- 2 new issues created
- 1 duplicate found (added as comment)
- All added to project board
```

## Updating Issues

### Add Strategy Analysis

```
User: Add the strategy analysis to issue #15

Claude: Adding strategy as comment to issue #15...

[Runs: gh issue comment 15 -R "$TARGET_REPO" --body "..."]

✅ Strategy added to issue #15
```

### Add Entry Drafts

```
User: Add these entries to issue #15

Claude: Adding entry drafts as comment to issue #15...

[Runs: gh issue comment 15 -R "$TARGET_REPO" --body "..."]
[Runs: gh issue edit 15 -R "$TARGET_REPO" --add-label "entry-drafted"]

✅ Entries added to issue #15
✅ Added "entry-drafted" label
```

### Mark as Submitted

```
User: I submitted entry option 2 for issue #15

Claude: Recording submission on issue #15...

[Runs: gh issue comment 15 -R "$TARGET_REPO" --body "..."]
[Runs: gh issue edit 15 -R "$TARGET_REPO" --add-label "entry-submitted"]

✅ Submission recorded on issue #15
✅ Added "entry-submitted" label
```

## Integration with hiivmind-pulse-gh

This skill can leverage hiivmind-pulse-gh for advanced project operations:

- `hiivmind-pulse-gh-projects` - Update project item fields
- `hiivmind-pulse-gh-milestones` - Manage milestones
- `hiivmind-pulse-gh-workspace-refresh` - Refresh cached IDs if needed

The workspace config at `.hiivmind/github/config.yaml` contains cached project and field IDs.
