---
name: marketing-report
description: "Producing the weekly/monthly marketing report — pulling GA4, Search Console, Listmonk, and Postiz numbers via the sibling skills, writing it to the shared REPORTS/ directory from a template, and sending the highlights."
metadata: { "marketingclaw": { "emoji": "📊" } }
---

# Marketing Report Skill

A reporting playbook, not a new API integration: it composes the `ga4`, `gsc`, `listmonk`, and
`postiz` skills (whichever are configured — skip sections cleanly for ones that aren't), writes
the result to the shared marketing directory, and sends a short highlights summary.

This skill has no environment variables of its own. It inherits whatever subset of
`GOOGLE_APPLICATION_CREDENTIALS`/`GA4_PROPERTY_ID`/`GSC_SITE_URL`/`LISTMONK_*`/`POSTIZ_*` is set —
if a sibling skill's env is missing, report that section as "not connected" rather than failing
the whole report.

## Workflow

1. **Pick the period.** Weekly report = last 7 full days; monthly = last full calendar month.
   Compute the date range explicitly (don't rely on a model's sense of "today" — use the
   actual current date).
2. **Pull each data source that's configured:**
   - `ga4` skill → sessions/users/conversions by channel, top landing pages, week-over-week
     or month-over-month deltas.
   - `gsc` skill → top queries and pages by clicks/impressions, average position movement,
     any new/lost top-10 rankings.
   - `listmonk` skill → subscriber growth/churn, campaigns sent in the period and their
     open/click/bounce rates.
   - `postiz` skill → posts published in the period per network, and engagement if the
     connected network's integration surfaces it (not all do — note when it's unavailable).
   - `seo-audit` skill → only for the monthly report's SEO section (see below).
3. **Fill `references/report-template.md`** with the pulled numbers. Keep prose minimal — this
   is a numbers-first report. Call out anomalies (a metric that moved >20% in either direction)
   explicitly rather than burying them in a table.
4. **Write the file** to:
   ```bash
   STATE_DIR="${MARKETINGCLAW_STATE_DIR:-$HOME/.marketingclaw}"
   OUT_DIR="$STATE_DIR/marketing/REPORTS"
   mkdir -p "$OUT_DIR"
   # Weekly: weekly-YYYY-WW.md (ISO week number). Monthly: monthly-YYYY-MM.md.
   ```
   Use the Write tool to create `$OUT_DIR/weekly-<year>-<ISO-week>.md` (or
   `monthly-<year>-<month>.md`), resolving `$STATE_DIR` to its actual value first — do not leave
   the literal `$STATE_DIR` string in the path you pass to the tool.
5. **Send highlights**, not the whole report, via the available message tool: 3-5 bullet points
   (biggest win, biggest concern, one number that moved a lot) plus a pointer to the full file
   path. Only escalate/flag loudly for real anomalies; a normal, uneventful week gets a short,
   calm summary.

## Monthly SEO section

For the monthly report only, run the `seo-audit` skill against 2-3 key pages (homepage plus
whatever the `gsc` data shows as top-traffic or most-changed) and fold a "top 3 SEO actions"
list into the report, sourced from that audit plus any notable `gsc` query/position movement.

## Notes

- Never invent numbers for a data source that isn't configured — write "not connected (no
  `LISTMONK_URL` set)" or similar instead of a placeholder.
- Keep the report file itself append-only across the archive (one file per period); don't
  overwrite a prior period's file when generating a new one.
- If `$STATE_DIR/marketing/` doesn't exist yet (team not provisioned via `setup-marketing`),
  create the `REPORTS/` subdirectory but flag to the human that `BRAND.md` and the rest of the
  shared directory look unset up.
