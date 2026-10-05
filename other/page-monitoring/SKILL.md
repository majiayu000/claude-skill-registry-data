---
name: page-monitoring
description: "Produces a monitoring plan for tracking changes to a target web page over time — covering change-detection tools, RSS-based monitoring, webhook alerts, and a structured process for logging and archiving each detected change."
status: stable
category: research
subcategory: preservation
version: 1.0
eval_score: 4.90
tags: [journalism, monitoring, change-detection, alerts, investigation, web-tracking]
---
# Page monitoring

## What this skill does
Produces a monitoring plan for tracking changes to a target web page over time — covering change-detection tools, RSS-based monitoring, webhook alerts, and a structured process for logging and archiving each detected change.

## When to use this skill
- You are watching a corporate or government web page for edits, deletions, or retractions that could affect your reporting
- You need to track when a policy document, data table, or public statement is updated
- You want to be alerted when a page changes rather than checking it manually every day
- You are monitoring for narrative drift — subtle rewording of official positions over time

## What you need to provide
**Required:** The URL(s) to monitor; what kind of change you are watching for (any change, text changes only, specific sections, new documents added, deletion of content)
**Optional:** How often you need to check (hourly, daily, weekly); how long the monitoring needs to run; whether you need historical diff records or just an alert when something changes; the number of pages you are monitoring (affects tool choice)

## How the Assistant Approaches This
1. **Selects the right monitoring method based on the page and the need.** Three main approaches, chosen by fit:

   - **Dedicated change-detection tools** (Visualping, ChangeTower, Distill.io): Best for monitoring specific sections of a page (a data table, a press-release list, a paragraph of text). These tools take periodic snapshots and compare them, alerting you by email or webhook when a difference is detected. Suitable when you need visual or text-level diff records.

   - **RSS-based monitoring:** Some government and institutional sites publish RSS feeds for press releases, document libraries, or news sections. If an RSS feed exists, it is the most reliable and least resource-intensive way to track new publications. The skill checks whether the target page has an associated RSS feed and guides the user to subscribe via a feed reader (Feedly, Inoreader, or a self-hosted reader like FreshRSS).

   - **Custom scripting with webhook alerts:** For advanced users or newsrooms with technical support. A lightweight script (using a tool like Huginn, changedetection.io, or a cron job with `curl` and `diff`) can poll a page at set intervals, compare the response to the previous version, and send an alert via email, Slack, or webhook. Best for monitoring multiple pages at scale or for pages that change-detection services cannot handle (dynamic content, API endpoints, authenticated pages).

2. **Configures the monitoring.** Walks through setup step by step for the chosen method: what to monitor (full page vs. specific CSS selector or section), how often to check, what threshold of change triggers an alert (any change, or only changes above a certain character count — to filter out ad rotation and timestamp updates), and where to send alerts.

3. **Sets up archiving for each detected change.** Every time a change is detected, the old version and the new version should both be preserved. Guides the user to configure automatic archiving (some tools support this natively) or to set up a manual workflow: receive alert, immediately archive the current page (see web-archiving skill), save the diff, and log the change in a monitoring log.

4. **Creates a monitoring log template.** A structured log the reporter maintains, recording: date of change, what changed (summary), archive URLs for before/after versions, and any editorial notes on the significance of the change.

## Output format
Three sections. First: a recommended monitoring method with setup instructions (200–400 words, step-by-step). Second: an archiving workflow for detected changes (100–200 words). Third: a monitoring log template. Total length: 400–700 words. Procedural register — instructions, not description.

## Quality criteria
- [ ] Monitoring method is chosen based on the user's specific situation, not presented as a generic list
- [ ] Setup instructions are specific enough for a reporter to follow without technical support (for tool-based methods)
- [ ] Alert configuration includes guidance on filtering noise (ad rotation, timestamps, irrelevant dynamic content)
- [ ] Archiving workflow ensures both old and new versions are preserved on each change
- [ ] Monitoring log template is included and usable
- [ ] RSS option is mentioned and checked when applicable
- [ ] Output is free of generic AI-template phrasing — no "delve into," "navigate the complexities of," Latinate filler verbs, restate-the-question intros, summary-of-the-summary closes, or em-dash overuse

## Example

### Input
URL: https://www.national-energy-authority.example.gov/data/emissions-quarterly-report
Context: This page publishes quarterly emissions data from the national energy authority. Last quarter, the authority quietly revised downward two figures in the Q1 report after publication without issuing a correction notice. We want to catch any future revisions to the Q2 data, which was published last week. Monitoring should run for at least three months. I am not technical — I need a tool I can set up without writing code.

### Output

**Recommended method: Visualping (change-detection tool)**

Visualping is a web-based service that takes periodic screenshots of a page and alerts you when the visual content changes. It requires no coding. Free tier allows monitoring up to 2 pages with daily checks; paid plans ($14/month) allow hourly checks and more pages.

Setup:

1. Go to visualping.io and create an account.
2. Paste the URL: `https://www.national-energy-authority.example.gov/data/emissions-quarterly-report`.
3. The tool will load a preview of the page. Select the area to monitor: draw a box around the emissions data table. This excludes the navigation bar, footer, and sidebar — those change for unrelated reasons (updated menus, new press releases) and would trigger false alerts.
4. Set the check frequency to **every 6 hours**. Daily checks risk missing a revision that is made and then revised again within the same day. Hourly checks are unnecessary for a government data page that updates infrequently and would consume your free-tier allowance quickly.
5. Set the change sensitivity to **medium**. "Low" sensitivity ignores minor formatting changes; "high" sensitivity triggers on single-character differences including whitespace. Medium catches meaningful text changes while filtering minor rendering differences.
6. Set the alert destination to your work email. Add a second alert to a shared newsroom inbox or Slack channel if available, so the alert is not dependent on one person checking their email.
7. Save the monitor. Visualping will take its first baseline snapshot immediately.

**Alternative check: RSS.** Before relying solely on Visualping, check whether the authority publishes an RSS feed for data updates. Look for an RSS icon on the page, or try appending `/feed` or `/rss` to the domain. Government data portals sometimes offer notification feeds for updated datasets. If an RSS feed exists, subscribe in a feed reader (Feedly is free) as a redundant alert channel.

**Archiving workflow for detected changes**

When Visualping sends an alert:

1. Open the URL immediately. Compare the current page to Visualping's "before" screenshot (included in the alert email).
2. Identify what changed: which figures, which text, which section.
3. Archive the current (changed) page using both Wayback Machine and Archive.today (see the web-archiving skill for the full procedure).
4. Save Visualping's "before" and "after" screenshots to your investigation folder.
5. Log the change in the monitoring log below.

If the authority deletes the page entirely, Visualping will report "page not found." In that case, your most recent archive becomes the last known version. Archive.today snapshots are more resilient than Wayback Machine for this purpose — prioritise checking that archive.

**Monitoring log**

| Date | Change detected | Summary of change | Before archive URL | After archive URL | Notes |
|------|-----------------|--------------------|--------------------|--------------------|-------|
| [date] | [yes/no alert] | [e.g., "Q2 SO₂ figure revised from 14,200 to 12,800 tonnes"] | [Wayback/Archive.today URL of previous version] | [Wayback/Archive.today URL of current version] | [editorial note: significance, whether correction notice was issued] |

## Known limitations
- Change-detection tools compare visual or textual snapshots. They miss changes inside downloadable files (PDFs, spreadsheets) unless the tool specifically supports those formats. If the emissions data is published as a downloadable file rather than on-page text, monitor the file's URL separately or use a tool like changedetection.io that supports file-hash monitoring.
- Free tiers of change-detection services limit the number of monitored pages and the check frequency. A newsroom monitoring many pages will need a paid plan or a self-hosted solution.
- Dynamic pages that render differently on each load (randomised ads, session-specific content, A/B testing) produce false positives. Section-specific monitoring and sensitivity tuning reduce this, but do not eliminate it.
- This skill sets up monitoring. It does not interpret what a change means. The reporter must assess whether a detected change is significant, accidental, or a routine update.

## Related skills
- [web-archiving](../web-archiving/SKILL.md)
- [content-access](../content-access/SKILL.md)
- [investigation-timeline-builder](../../../magazine-journalism/investigation/investigation-timeline-builder/SKILL.md)
