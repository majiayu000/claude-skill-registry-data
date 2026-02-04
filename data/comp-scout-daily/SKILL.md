---
name: comp-scout-daily
description: End-to-end automated daily competition workflow. Orchestrates scrape, analyze, compose, and notify skills - all unattended for cron execution.
---

# Daily Competition Scout

Automated end-to-end workflow for cron/scheduled execution. **Orchestrates other skills** rather than duplicating their logic.

## CRITICAL: Fully Unattended Operation

**This skill MUST run completely unattended with NO user prompts.**

When this skill is invoked:
1. **DO NOT** ask "Would you like me to..." at any point
2. **DO NOT** wait for user confirmation before persisting
3. **DO NOT** ask permission to analyze or compose entries
4. **JUST DO IT** - scrape, persist, analyze, compose, notify - all automatically

If you find yourself about to ask a question, STOP and use the default behavior instead.

## CRITICAL: Check for Duplicates Before Persisting

**Each competition should only be stored ONCE, even if it appears on multiple sites.**

Before creating any issue, you MUST:
1. Get all existing issues: `gh issue list -R $TARGET_REPO --label competition --state all --json number,title,body --limit 500`
2. For each scraped competition, check if it already exists by:
   - URL appears anywhere in any issue body (search full text - issues may have multiple URLs from different sites)
   - OR normalized title similarity >80% to any existing issue title
3. If URL found in existing issue → SKIP (already tracked)
4. If title >80% similar but different URL → add comment to existing issue with the alternate URL
5. If truly new (URL not found AND title <80% similar) → create issue

**Word limit clarification:** "25WOL" is a category name. Competitions with 25, 50, or 100 word limits are all valid - persist them (if new).

**Auto-tagging (for-kids, cruise) is for LABELING, not skipping:**
- Tagged competitions ARE STILL CREATED as issues (if new)
- They just get a label and are closed automatically

## What This Skill Does

This skill is a **workflow orchestrator** that invokes other skills in sequence:

```
┌─────────────────┐
│ comp-scout-daily│
└────────┬────────┘
         │
         ▼
┌─────────────────┐     Scrapes listings, fetches details,
│ comp-scout-scrape│────▶ checks duplicates, persists issues
└────────┬────────┘
         │
         ▼ (for each new, non-filtered issue)
┌─────────────────┐
│comp-scout-analyze│────▶ Generates strategy (--unattended)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│comp-scout-compose│────▶ Drafts entries (--unattended)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│comp-scout-notify │────▶ Sends email digest
└─────────────────┘
```

**Runs completely unattended - no user prompts during execution.**

## Prerequisites

- `gh` CLI authenticated
- Playwright installed: `pip install playwright && playwright install chromium`
- Target repository with CLAUDE.md containing user preferences
- SMTP credentials for email notifications (optional)

## Invocation

### Via Claude Code
```
"Perform daily competition scout"
"Run the daily comp scout workflow"
"Do the morning competition scrape and analysis"
```

### Via Cron
```bash
# Daily at 7am
0 7 * * * claude -p "Perform daily competition scout" >> /var/log/comp-scout.log 2>&1
```

## Workflow

### Phase 1: Configuration

Determine target repository and load user preferences:

```bash
TARGET_REPO="${TARGET_REPO:-discreteds/competition-scout-25WOL}"

# Fetch user preferences from data repo
gh api repos/$TARGET_REPO/contents/CLAUDE.md -H "Accept: application/vnd.github.raw" 2>/dev/null
```

Parse from CLAUDE.md:
- Auto-filter keywords (for-kids, cruise, etc.)
- Saved stories for entry composition
- Personal context (partner name, location)

### Phase 2: Scrape, Dedupe, and Persist (Automatic)

**Execute the scrape workflow directly** - no questions asked.

YOU MUST:
1. Run the scraper to get listings from both sites
2. **BEFORE creating any issues**, fetch ALL existing issues (open AND closed, limit 500)
3. For each scraped competition:
   - Search all issue bodies for the scraped URL (full text search, not field match)
   - If URL found → SKIP (already tracked)
   - If URL not found, check title similarity against all existing titles
   - If title >80% similar → add comment to existing issue with alternate URL, don't create new
   - If URL not found AND title <80% similar → this is NEW
4. Fetch details for NEW competitions only
5. Create issues for NEW competitions (no asking)
6. Apply auto-filter rules (create + close filtered issues)

**Key point: Most scraped competitions will already be tracked. Only create issues for truly new ones.**

```
Output: List of new issue numbers created (usually 0-3 per day)
```

### Phase 3: Analyze Each New Issue (Automatic)

**For each new, non-filtered issue: analyze strategy immediately.**

YOU MUST:
1. Read the issue details
2. Determine sponsor category and brand voice
3. Generate 5 angle ideas using default tone mapping
4. **ADD STRATEGY COMMENT IMMEDIATELY** (no asking)

**DO NOT ask "Would you like me to analyze?" - JUST DO IT.**

### Phase 4: Compose Entries for Each New Issue (Automatic)

**For each new, non-filtered issue: compose entries immediately.**

YOU MUST:
1. Read the issue + strategy comment
2. Load saved stories from target repo CLAUDE.md
3. Match story keywords to competition (or use generic)
4. Generate 3-5 entry variations with ratings
5. **ADD ENTRIES COMMENT IMMEDIATELY** (no asking)
6. **ADD entry-drafted LABEL** (no asking)

**DO NOT ask "Would you like me to compose entries?" - JUST DO IT.**

### Phase 5: Check Closing Soon

Query for competitions closing within 3 days:

```bash
gh issue list -R "$TARGET_REPO" \
  --label "competition" \
  --state open \
  --json number,title,body,labels
```

Parse closing dates and flag urgent items.

### Phase 6: Invoke comp-scout-notify

**Delegate to the notify skill** for email digest.

```
Invoke: comp-scout-notify send
Output: Email sent to configured recipients
```

### Phase 7: Output Summary Report

```markdown
## Daily Competition Scout Report - 2025-12-09

### Summary
- **New competitions:** 5
- **Auto-filtered:** 2 (1 for-kids, 1 cruise)
- **Analyzed and drafted:** 3
- **Duplicates added:** 1

### New Competitions (Ready for Entry)

| Issue | Competition | Closes | Story Used | Recommended |
|-------|-------------|--------|------------|-------------|
| #15 | Win $500 Coles Gift Card | Dec 31 | Generic | Option 2 |
| #16 | Win a Spa Day | Jan 5 | Margot Deserves Pampering | Option 1 |
| #17 | Win Kitchen Appliance | Dec 20 | Generic | Option 3 |

### Auto-Filtered (Created + Closed)

| Issue | Competition | Reason |
|-------|-------------|--------|
| #18 | Win Lego Set | for-kids (keyword: Lego) |
| #19 | Win P&O Cruise | cruise (keyword: P&O) |

### Closing Soon - Action Needed

| Issue | Competition | Days Left | Status |
|-------|-------------|-----------|--------|
| #12 | Woolworths Gift Cards | 1 | entry-drafted |
| #14 | TVSN Prize Pack | 2 | entry-drafted |

### Recommendations

1. **Priority:** #12 closes tomorrow - entry drafted, recommend Option 2
2. **High value:** #16 Spa Day ($500) - entry uses saved story, strong fit
3. **Review:** #17 Kitchen Appliance - closes in 11 days, time to refine
```

## Unattended Operation

The skill makes NO interactive prompts during execution:

| Decision | Automatic Behavior |
|----------|-------------------|
| Story selection | Use best keyword-matching saved story, or generic approach |
| Entry generation | All entries drafted with star ratings; recommendation noted |
| Filter decisions | Based on keywords in CLAUDE.md preferences |
| Duplicates | Add comment to existing issue automatically |
| Tone selection | Based on sponsor category (see comp-scout-analyze) |

All choices are logged in the report for user review.

## Error Handling

| Error | Behavior |
|-------|----------|
| Scrape fails for one site | Log error, continue with other site |
| Issue creation fails | Log error, skip to next competition |
| Analyze fails for one issue | Log error, skip compose for that issue |
| Compose fails for one issue | Log error, continue to next issue |
| Notify fails | Log error, report still generated |
| No new competitions | Report "No new competitions found" |

Errors are included in the final report.

## Configuration

### Environment Variables

```bash
TARGET_REPO=discreteds/competition-scout-25WOL
```

### Data Repo CLAUDE.md

Must contain:
- **User Preferences**: Auto-filter rules with keywords
- **Saved Stories**: Personal stories for automatic matching (optional)
- **Personal Context**: Partner name, location, interests

## Skill Invocation Pattern

This skill **orchestrates** - it does not duplicate logic:

| Skill | Invoked By Daily | Mode |
|-------|------------------|------|
| comp-scout-scrape | Yes | Automatic (handles own persistence) |
| comp-scout-analyze | Yes | `--unattended` flag |
| comp-scout-compose | Yes | `--unattended` flag |
| comp-scout-notify | Yes | Automatic |
| comp-scout-persist | No | Logic merged into scrape |

Individual skills remain available for interactive use when you want manual control.

## Example Cron Log Output

```
$ claude -p "Perform daily competition scout"

Starting daily competition scout...

Phase 1: Loading configuration
  Target repo: discreteds/competition-scout-25WOL
  Filter rules: for-kids (9 keywords), cruise (6 keywords)
  Saved stories: 2 available

Phase 2: Invoking comp-scout-scrape
  competitions.com.au: 8 competitions
  netrewards.com.au: 5 competitions
  New issues created: #43, #44, #45
  Filtered issues (closed): #46, #47
  Duplicate comments: #38

Phase 3: Invoking comp-scout-analyze (--unattended)
  #43: Strategy added (Food/beverage → Relatable, sensory)
  #44: Strategy added (Travel → Discovery, bucket-list)
  #45: Strategy added (Tech → Knowledgeable, self-aware humor)

Phase 4: Invoking comp-scout-compose (--unattended)
  #43: 3 entries drafted (using saved story: Sunday BBQ)
  #44: 4 entries drafted (generic approach)
  #45: 3 entries drafted (generic approach)

Phase 5: Checking closing soon
  3 competitions closing within 3 days

Phase 6: Invoking comp-scout-notify
  Email sent to 2 recipients

## Daily Competition Scout Report - 2025-12-09
[Full report as shown above]
```

## Key Design Principle

**DRY (Don't Repeat Yourself)**: This skill invokes other skills rather than reimplementing their logic. This means:

1. Bug fixes in individual skills automatically apply to daily workflow
2. Interactive and unattended modes share the same core logic
3. Each skill has a single source of truth for its behavior
4. Testing individual skills also tests the daily workflow

If you need to change how analysis works, change `comp-scout-analyze` - the daily workflow will automatically use the updated logic.
