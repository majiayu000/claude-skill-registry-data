---
name: content-performance-reporter
description: "Compile weekly analytics CSV exports from Instagram, YouTube, Google Analytics, LinkedIn, TikTok, Facebook, and Twitter into a narrative performance report: what worked, what didn't, the week's pattern, and concrete recommendations. No code, no dashboards, no API required. Triggers: 'content performance report', 'analyze my content performance', 'what worked this week', 'weekly content report', 'compile my analytics', 'отчёт по контенту', 'что сработало на этой неделе', 'анализ контент-аналитики', 'еженедельный отчёт по контенту', 'скомпилируй аналитику'."
version: 1.0.0
---

# Content Performance Reporter

This skill compiles CSV analytics exports from content platforms into a structured narrative weekly report — what worked, what didn't, the pattern behind top performers, and concrete recommendations for next week. Designed for marketers, SMM managers, and content creators who need readable editorial insight, not another dashboard.

**Input:**
- One or more CSV files from analytics platforms in the Cowork workspace (Instagram, YouTube, Google Analytics, LinkedIn, TikTok, Facebook, Twitter/X)

**Output:**
- Markdown report: per-platform metrics table, Top 3 / Bottom 3 posts, narrative What Worked / What Didn't, Pattern of the Week, and 1–2 actionable recommendations

---

## Language Detection

Detect the user's language from their message:
- If Russian (or contains Cyrillic): respond in Russian
- If English (or other Latin-script language): respond in English
- If ambiguous: respond in the language of the trigger phrase used

---

## Instructions

### Step 1: Locate Files

1. Identify CSV files from the user's message
   - If a filename or path is provided: use it directly
   - If no file specified: scan the Cowork workspace folder for CSV files with analytics-related names (metrics, analytics, insights, export, report, stats, instagram, youtube, ga4, linkedin, tiktok, facebook, twitter)
   - If no CSV files found: stop and report — "No analytics CSV files found. Upload your platform export and try again."

2. For each file: detect the platform by matching column headers against known patterns (see Platform Detection table below)
   - If platform cannot be identified: mark as "Unknown platform" and continue with generic mode

### Step 2: Extract Metrics

For each file, extract:
- Date / period (if present)
- Reach / impressions / views metrics
- Engagement metrics: Likes, Comments, Shares, Saves, Reactions, Engagement Rate
- Traffic metrics: Clicks, CTR, Link Clicks
- Platform-specific: Watch Time (YouTube), Follower Growth, Profile Visits

Normalize all numeric values before calculation:
- Strip thousand separators: `1,234` → `1234`
- Strip currency and % symbols
- Convert shorthand: `1.2K` → `1200`, `3.5M` → `3500000`

If a file has no numeric metric columns: skip the file; note it in Notes. If no readable files remain after skipping: stop with the "no files found" message.

### Step 3: Identify Top and Bottom Content

For each file, select the **primary metric** based on platform:
- Instagram: Reach (or Impressions if Reach not present)
- YouTube: Views
- LinkedIn: Impressions
- Google Analytics: Sessions (or Pageviews)
- TikTok: Video Views
- Twitter/X: Impressions
- Facebook: Reach
- Unknown: first numeric column

Sort by primary metric:
- **Top 3:** highest values
- **Bottom 3:** lowest values
- If the file has fewer than 6 rows: show all rows; skip Top/Bottom labels

If no content identifier column found (title, URL, ID, post name): use Row # as identifier; add note — "No content title column detected — rows used as identifiers."

**Edge case — Large file (>1000 rows):** analyze all rows for aggregate metrics; use top 100 rows by primary metric for Top/Bottom selection; note the sampling.

### Step 4: Calculate Aggregate Metrics

For each platform:
1. Sum the primary metric for the period (Total Reach / Views / Impressions)
2. Calculate Average Engagement Rate if ER column present
3. If a second file or comparison period exists in the data: calculate delta (Current − Previous); express as `+N%` or `−N%`
   - If no previous period data: show current values only; do not display delta

### Step 5: Write the Narrative

Based on the extracted data, write:

**What Worked** — 2–3 specific findings with numbers:
- Focus on the highest-performing content, format, topic, or posting pattern
- Each point must reference a concrete metric (e.g., "Video posts averaged 2× more reach than carousels: 3,200 vs 1,500")

**What Didn't Work** — 2–3 specific findings:
- Focus on the lowest performers or declining metrics
- Avoid generic statements; tie each point to data

**Pattern of the Week** — 1–2 sentences:
- Identify the common thread among the top 3 performers: format, topic, CTA type, length, timing
- If no clear pattern: write "No dominant pattern identified — performance was evenly distributed across content types."

**Recommendation for Next Week** — 1–2 concrete actions:
- Derived directly from the data (not generic advice like "post more often")
- Format: imperative, specific (e.g., "Produce 2+ short-form video posts similar to [top post title]")

### Step 6: Format and Output Report

Build the output using the Output Format structure below. If multiple platforms are present: one section per platform, followed by a combined Summary section.

---

## Platform Detection

| Platform | Key column headers (any match triggers detection) |
|----------|--------------------------------------------------|
| Instagram | `Reach`, `Impressions`, `Engagement`, `Profile Activity`, `Followers reached` |
| YouTube | `Video title`, `Views`, `Watch time`, `Average view duration`, `Subscribers gained` |
| Google Analytics | `Sessions`, `Pageviews`, `Bounce rate`, `Source / Medium`, `Landing page` |
| LinkedIn | `Update title`, `Impressions`, `Clicks`, `Engagement rate`, `Followers` |
| TikTok | `Video views`, `Play time`, `TikTok videos` |
| Twitter/X | `Impressions`, `Engagements`, `Retweets`, `Link clicks`, `Tweet text` |
| Facebook | `Post clicks`, `Reactions`, `Post reach`, `Shares`, `Facebook Insights` |

---

## Output Format

```markdown
## Content Performance Report — [Period]

### [Platform Name]

| Metric | This Week | vs. Last Week |
|--------|-----------|---------------|
| Total Reach / Views | 12,400 | +8% ↑ |
| Avg. Engagement Rate | 4.2% | −0.3pp ↓ |
| Best Post Reach | 3,200 | — |

**Top 3 Posts**
1. [Title / ID / Row #] — [Primary Metric]: 3,200 | ER: 6.1%
2. [Title / ID / Row #] — [Primary Metric]: 2,800 | ER: 5.4%
3. [Title / ID / Row #] — [Primary Metric]: 2,100 | ER: 4.8%

**Bottom 3 Posts**
1. [Title / ID / Row #] — [Primary Metric]: 340 | ER: 1.1%
2. …
3. …

---

### What Worked
- [Specific finding with number]
- [Specific finding with number]
- [Specific finding with number]

### What Didn't Work
- [Specific finding with number]
- [Specific finding with number]

### Pattern of the Week
[1–2 sentences about the common thread among top performers]

### Recommendation for Next Week
1. [Concrete, data-backed action]
2. [Concrete, data-backed action]

---
### Notes
- [Platform detection note, merge flag, data gap, or sampling note — omit section if empty]
```

---

## Negative Cases

- **No CSV files found:** Stop — "No analytics CSV files found. Upload your platform export and try again."
- **CSV has no numeric columns:** Skip file; add to Notes. If all files skipped: stop with the "no files found" message.
- **No content identifier column:** Use Row # as identifier; add note.
- **Request for charts / visual output:** Explain — "I can't generate charts here, but you can paste the table into Google Sheets or Excel to visualize it."
- **Request to compare with industry benchmarks:** Explain — "I can only compare against your own previous data — no external benchmark data is available in this mode."
- **Single row of data (no meaningful Top/Bottom):** Show the single item; skip Top 3 / Bottom 3 structure; note — "Only 1 content item found — Top/Bottom ranking skipped."
