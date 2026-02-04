---
name: intelligence
description: Information gathering utilities (analytics, research, content analysis) (general)
---

# Intelligence Skill

## Overview

This skill provides **comprehensive information gathering utilities** for project planning and content analysis. It consolidates analytics queries, external research, and content intelligence operations into a single skill.

**Key principle:** This is a **utility skill** - it wraps Kurt CLI commands and provides low-level operations. It can be used directly by users OR called by higher-level skills (like project-management, workflows).

**Primary use case:** During project planning (Step 4 of create-project) to identify what content needs work.

---

## When to Use This Skill

✅ **Use intelligence-skill when:**
- Analyzing traffic patterns to find content issues (audit-traffic)
- Finding content about specific topics with traffic data (identify-affected)
- Researching topics with AI (search)
- Monitoring community discussions (reddit, hackernews, feeds)
- Comparing content coverage vs competitors (compare-gaps, compare-coverage)
- Quick analytics spot-checks (top, bottom, trending)

❌ **Don't use intelligence-skill when:**
- Creating or editing content → Use `content-writing-skill`
- Managing CMS content → Use `cms-interaction-skill`
- Managing projects → Use `project-management-skill`

**Rule of thumb:** If it's gathering information or analyzing data, use this skill. If it's creating/managing content, use other skills.

---

## Operations (18 total, 3 categories)

### Analytics Operations (6)
Low-level traffic queries for spot-checking and analysis.

- `top <N>` - Top pages by traffic
- `bottom <N>` - Lowest traffic pages
- `trending` - Pages with increasing traffic
- `declining` - Pages losing traffic
- `summary <domain>` - Analytics overview
- `check <url>` - Traffic for specific page

### External Research Operations (6)
Research from external sources (AI, Reddit, Hacker News, RSS).

- `search "<query>"` - AI-powered research (Perplexity)
- `list` - Browse past research results
- `get <filename>` - Get specific research result
- `reddit -s <subreddit>` - Monitor Reddit discussions
- `hackernews` - Monitor Hacker News
- `feeds <url>` - Monitor RSS/Atom feeds

### Content Intelligence Operations (6)
Complex analysis combining content + analytics for project planning.

- `identify-affected --search-term <term>` - Find content with traffic prioritization
- `audit-traffic --domain <domain>` - Traffic audit report
- `impact-estimate --topic <topic>` - Estimate content opportunity value
- `compare-gaps --own <domain> --competitor <domain>` - Find missing content
- `compare-coverage --own <domain> --competitor <domain>` - Compare content types/topics
- `compare-quality --own <domain> --competitor <domain>` - Compare depth/quality metrics

---

## Operation Details

### Analytics Operations

**top <N>** - Top pages by traffic
- **Use:** Quick check for most popular content
- **Example:** `intelligence top 10`

**bottom <N>** - Lowest traffic pages
- **Use:** Find zero-traffic/orphaned pages
- **Example:** `intelligence bottom 10`

**trending** - Pages with increasing traffic
- **Use:** Find momentum topics to expand on
- **Example:** `intelligence trending`

**declining** - Pages losing traffic
- **Use:** Urgent attention needed (high traffic + declining = critical)
- **Example:** `intelligence declining`

**summary <domain>** - Analytics overview
- **Use:** Understand traffic distribution and health
- **Example:** `intelligence summary docs.company.com`

**check <url-pattern>** - Traffic for specific URL(s)
- **Use:** Spot-check traffic during planning
- **Example:** `intelligence check "bigquery"`

### Research Operations

**search "<query>"** - AI-powered research (Perplexity)
- **Use:** Gather reference sources for projects
- **Flags:** `--recency hour|day|week|month`, `--save`
- **Example:** `intelligence search "AI tools trends" --recency week --save`

**list** - Browse past research
**get <filename>** - Retrieve specific research

**reddit -s <subreddit>** - Monitor Reddit discussions
- **Use:** Find what audience is discussing
- **Example:** `intelligence reddit -s dataengineering --min-score 10`

**hackernews** - Monitor HN discussions
**feeds <url>** - Monitor RSS/Atom feeds

### Content Intelligence Operations

**identify-affected --search-term <term>** - Find content with traffic prioritization
- **Use:** Update content about specific topic
- **Priority matrix:** CRITICAL (high traffic + declining) → ZERO (no traffic)
- **Example:** `intelligence identify-affected --search-term "bigquery" --content-type tutorial`

**audit-traffic --domain <domain>** - Comprehensive traffic audit
- **Use:** Domain-wide health check
- **Finds:** High-traffic stale, declining traffic, zero-traffic pages
- **Example:** `intelligence audit-traffic --domain docs.company.com`

**impact-estimate --topic <topic>** - Estimate new content opportunity
- **Use:** Prioritize new content creation
- **Returns:** HIGH/MEDIUM/LOW impact estimate
- **Example:** `intelligence impact-estimate --topic "security" --domain docs.company.com`

**compare-gaps --own <domain> --competitor <domain>** - Find missing content
- **Use:** Identify content you don't have vs competitor
- **Prerequisite:** Competitor content must be indexed
- **Example:** `intelligence compare-gaps --own docs.yourco.com --competitor docs.competitor.com`

**compare-coverage --own <domain> --competitor <domain>** - Compare content types
- **Use:** Understand content mix gaps (tutorials, guides, examples)
- **Example:** `intelligence compare-coverage --own docs.yourco.com --competitor docs.competitor.com`

**compare-quality --own <domain> --competitor <domain>** - Compare content depth
- **Use:** Set quality bar for content
- **Compares:** word count, code examples, images, update frequency
- **Example:** `intelligence compare-quality --own docs.yourco.com --competitor docs.competitor.com`

---

## Common Workflows

**For updating docs:** `audit-traffic` → select high-priority items
**For new content:** `compare-gaps` + `impact-estimate` → prioritize topics
**For competitive analysis:** `compare-gaps` + `compare-coverage` + `compare-quality`
**For research:** `search` + `reddit`/`hackernews` → gather sources

---

## Routing Logic

```bash
# Parse first argument to determine operation type
OPERATION=$1

case "$OPERATION" in
  # Analytics operations → analytics subskill
  top|bottom|trending|declining|summary|check)
    invoke: subskills/analytics.md
    ;;

  # Research operations → research subskill
  search|list|get|reddit|hackernews|feeds)
    invoke: subskills/research.md
    ;;

  # Content intelligence operations → content-intelligence subskill
  identify-affected|audit-traffic|impact-estimate|compare-gaps|compare-coverage|compare-quality)
    invoke: subskills/content-intelligence.md
    ;;

  *)
    echo "Unknown operation: $OPERATION"
    echo ""
    echo "Available operations:"
    echo "  Analytics: top, bottom, trending, declining, summary, check"
    echo "  Research: search, list, get, reddit, hackernews, feeds"
    echo "  Content Intelligence: identify-affected, audit-traffic, impact-estimate,"
    echo "                        compare-gaps, compare-coverage, compare-quality"
    echo ""
    echo "See 'Operation Details' section in intelligence-skill/SKILL.md for usage examples"
    exit 1
    ;;
esac
```

---

## Integration with Other Skills

**Called by:**
- `project-management-skill` (Step 4 - identify targets during project planning)
- `workflow-skill` (default workflows use intelligence operations)
- Direct user invocation for ad-hoc analysis

**Uses:**
- `kurt content list` - Query indexed content
- `kurt content stats` - Content statistics
- `kurt research` - External research commands
- `kurt cluster-urls` - Topic clustering

**Works with:**
- `content-writing-skill` - Intelligence identifies targets, writing creates content
- `cms-interaction-skill` - Intelligence analyzes, CMS manages
- `workflow-skill` - Workflows compose intelligence operations

---

## Key Principles

1. **Utility skill** - Low-level, composable operations
2. **Modular subskills** - Load only needed operations (context efficiency)
3. **Used during planning** - Primarily for project planning (Step 4)
4. **Data-driven** - Combines content metadata + analytics + external research
5. **Delegates to CLI** - Wraps kurt commands, doesn't reimplement logic

---

## See Also

- **project-management-skill** - Uses intelligence in Step 4 (identify targets)
- **content-intelligence subskill** - Detailed implementation of complex operations
- **analytics subskill** - Traffic analysis implementation
- **research subskill** - External research implementation
