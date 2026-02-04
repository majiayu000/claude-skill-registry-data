---
name: batch-report-generator
description: Generate GenuVerity fact-check reports from structured input (Gemini research output). Use /batch-report to process research into HTML reports. Optimized for token efficiency - expects pre-researched sources.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebFetch
---

# Batch Report Generator

Generate fact-check reports from pre-researched input (e.g., Gemini Deep Research output).

## Quick Start

```
/batch-report
```

Then paste your structured input (see format below).

## Structured Input Format

Paste this JSON format with your Gemini research:

```json
{
  "reports": [
    {
      "slug": "claim-name-2025",
      "title": "The Full Claim Title",
      "verdict": "FALSE",
      "claim": "One sentence: what was claimed",
      "claimant": "Who made the claim",
      "date": "Jan 2025",
      "category": "Health & Medical",
      "sources": [
        {
          "title": "Primary Source Name",
          "url": "https://example.com/article",
          "quote": "Key quote that supports/refutes the claim..."
        }
      ],
      "context": "2-3 sentences explaining why this verdict was reached. From Gemini research."
    }
  ]
}
```

## Gemini Prompt Template

Copy this to Gemini for Deep Research:

```
Research these fact-check topics. For EACH topic, provide:

1. VERDICT: FALSE / MISLEADING / MIXED / CONTEXT NEEDED
2. CLAIM: One sentence summary of what was claimed
3. CLAIMANT: Who made the claim (person/organization)
4. DATE: When the claim was made
5. SOURCES: 10-15 primary sources (NO Wikipedia), each with:
   - Title
   - URL
   - Key quote (verbatim)
6. CONTEXT: 3 sentences explaining the verdict

TOPICS:
1. [Topic 1]
2. [Topic 2]
3. [Topic 3]
...

Format your response as JSON matching this structure:
{
  "reports": [
    {
      "slug": "topic-name-2025",
      "title": "Full Title",
      "verdict": "FALSE",
      "claim": "...",
      "claimant": "...",
      "date": "...",
      "category": "...",
      "sources": [{"title": "...", "url": "...", "quote": "..."}],
      "context": "..."
    }
  ]
}
```

## Categories

Use one of these category values:
- `U.S. Politics & Policy`
- `Health & Medical`
- `AI & Deepfakes`
- `Immigration & Border`
- `International Affairs`
- `Economic Claims`
- `Conspiracy & Hoaxes`
- `Platform & Tech`
- `Media & Journalism`

## Verdicts

| Verdict | When to Use |
|---------|-------------|
| `FALSE` | Claim is demonstrably untrue |
| `MISLEADING` | Contains truth but distorts context |
| `MIXED` | Partially true, partially false |
| `CONTEXT` | Needs additional context to evaluate |

## What This Skill Does

1. **Parses** your structured JSON input
2. **Validates** all source URLs exist (via WebFetch)
3. **Generates** HTML from `docs/report-template-2025.html`
4. **Creates** Chart.js visualization based on data
5. **Adds** entry to `js/reports-data.js`
6. **REQUIRES MANUAL RUN**: `node tools/sync-chart-configs.js` (see warning below)
7. **Runs** `./validate-report.sh` to verify
8. **Commits** to feature branch

> **WARNING: CHART SYNC IS NOT AUTOMATIC**
>
> After generating reports, you MUST manually run:
> ```bash
> node tools/sync-chart-configs.js
> ```
> Without this, carousel thumbnails will show wrong/placeholder data.
> This step extracts chart data from HTML and updates reports-data.js.

## CRITICAL: Chart Height Constraint

**ALWAYS** wrap canvas in height-constrained div. NEVER use height attribute on canvas:

```html
<!-- ❌ WRONG - Chart expands to 20,000+ pixels -->
<canvas id="myChart" height="220"></canvas>

<!-- ✅ CORRECT - Height constrained by wrapper -->
<div style="height: 280px; position: relative;">
    <canvas id="myChart"></canvas>
</div>
```

## CRITICAL: Float-Figure Placement (Text Wrap)

**ALWAYS** place float-figures BEFORE the text that should wrap around them:

```html
<!-- ✅ CORRECT - Text wraps beside chart -->
<section>
    <h2>Section Title</h2>
    <figure class="float-figure">...chart...</figure>
    <p>This paragraph wraps beside the chart.</p>
    <p>More text continues wrapping.</p>
</section>

<!-- ❌ WRONG - Chart at end, no text to wrap -->
<section>
    <h2>Section Title</h2>
    <p>This text appears ABOVE the chart.</p>
    <figure class="float-figure">...chart...</figure>
</section>  <!-- Nothing after figure! -->
```

**Key rules:**
1. Place figure IMMEDIATELY AFTER `<h2>` or BEFORE paragraphs
2. Ensure 2-3 paragraphs of text FOLLOW the figure
3. NEVER place a figure as the last element in a section

## Token Optimization

This skill is designed for **minimal token usage**:
- Expects pre-researched sources (no web search needed)
- Uses template-based generation (no creative writing)
- Batch processes multiple reports
- Caches verified URLs

## Output

For each report:
- `localreports/{slug}.html` - The report HTML
- Entry in `js/reports-data.js` with chart config
- Updated sitemaps via `node tools/generate-sitemaps.js`
- Synced chart thumbnails via `node tools/sync-chart-configs.js`

## CRITICAL: Chart Thumbnail Sync (MANDATORY)

After creating ANY new reports, **ALWAYS** run:

```bash
node tools/sync-chart-configs.js
```

This syncs the chart configs in `js/reports-data.js` to match the actual charts in each HTML report. Without this step, carousel cards show wrong/blank chart previews.

**Post-generation checklist:**
1. ✅ Create HTML reports in `localreports/`
2. ✅ Add entries to `js/reports-data.js`
3. ✅ Run: `node tools/generate-sitemaps.js`
4. ✅ Run: `node tools/sync-chart-configs.js` ← **MANDATORY**
5. ✅ Run: `./validate-report.sh` on each report
6. ✅ Commit and push

## Example Workflow

1. **You**: Ask Gemini to research 5 topics (20 min)
2. **You**: Paste Gemini's JSON output here
3. **Claude**: Generates 5 HTML reports (~5 min)
4. **Claude**: Commits to feature branch
5. **You**: Review on Vercel preview

## References

- [REPORTS.md](/.claude/docs/REPORTS.md) - Full report guidelines
- [VISUAL_STANDARDS.md](/.claude/docs/VISUAL_STANDARDS.md) - Colors & charts
- [report-template-2025.html](/docs/report-template-2025.html) - HTML template

## REMINDER: Option B Automation

After testing this workflow, build full automation:
- Agent SDK batch processor script
- Playwright MCP for source verification
- Research cache system
- Queue-based processing
