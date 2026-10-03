---
name: impact-timeline
description: Build a month-by-month career impact timeline across an entire tenure (or any multi-month window), sweeping every available source (GitHub, issue tracker, Slack, Notion, meeting notes like Granola, the company BI/data platform, Datadog, Sentry) one month at a time, then attaching real product/technical/business metrics to every entry in "accomplished X, measured by Y, by doing Z" form. Use this whenever the user wants a tenure retrospective, a departure/offboarding impact record, "everything I did at this company", a promotion or performance-review packet covering many months, a year-in-review, or asks to add metrics/evidence to an existing career document. For a single day/week/month recap, use `/flagrare:standup-report` or `/flagrare:brag-doc` instead; this skill is for the long arc.
---

# Impact Timeline

> **No em-dashes.** Nothing this skill writes may contain an em-dash; use a comma, colon, or parentheses instead. Enforced by a repo hook that flags em-dashes in generated `.md`. See `/flagrare:write-docs`.

Produce a durable, evidence-backed record of a person's impact over a long window (typically a full tenure), month by month, from every system that holds a trace of their work. The output is a single markdown file the person can carry into interviews, reviews, and their next job.

Two properties make this document worth building:

1. **Every month is swept in every source before moving on.** Ticket trackers show what was planned; git shows what shipped; Slack shows judgment, debugging, and unblocking that never became a ticket; meeting notes show praise, decisions, and assignments nobody wrote down elsewhere; the BI platform shows what the work meant to users and money. Any single source alone badly undercounts a year of work.
2. **Every claim carries a "measured by".** The difference between a changelog and an impact record is the Y in "accomplished X, measured by Y, by doing Z". Numbers where they exist, scale qualifiers where they don't, and honest caveats where the data is thin.

Read `references/playbook.md` before starting: it holds the per-source query recipes (exact gh/search syntax, Slack modifiers, meeting-notes questions, BI-platform access patterns) learned from real runs. The workflow below is the spine; the playbook is the muscle.

## Phase 0: Setup and identity

Establish before pulling anything:

- **Window**: start and end dates. Verify the claimed start date against the data (first PR, first Slack message); people misremember by days.
- **Identities**: GitHub login, tracker mention name, Slack user ID, work email, meeting-notes account. Watch for imposters: old commits by a similar name/personal email may be a different person entirely. Verify by email, not by first name.
- **Repos**: include archived/deprecated repos explicitly; early-tenure work often lives in a repo that was later retired. Ask, and also look for `_deprecated`/archive directories locally and archived repos in the org.
- **Output file**: create it immediately (e.g. `~/Dev/impact-timeline-export/impact-timeline.md`) and write each month as it completes. Never hold twelve months of findings in memory; a long run can be summarized mid-flight and progressive writes are what protect the work.
- **Reuse config** from the shared `~/.claude/skills/flagrare/config.json` if present (top-level `github_login`, `display_name`, org and tracker keys written by `/flagrare:brag-doc` and `/flagrare:standup-report`) rather than re-asking. Nest anything impact-timeline-specific under `skills["impact-timeline"]` and leave other skills' blocks untouched.

## Phase 1: Bulk enumeration (once, up front)

Pull the cheap complete datasets in one pass and bucket by month locally, instead of querying per month:

- All authored PRs (created date, merged date, repo, number, title) via search API, paginated. Save as TSV next to the output file.
- All reviewed PRs (same shape, `reviewed-by:` minus `author:`).
- Monthly counts (created, merged, reviews) to see the shape of the year before writing a word.

These TSVs are also part of the deliverable; keep them in the export folder.

## Phase 2: Month loop

For each month, in order, gather then write before advancing. Per month:

1. **PRs** from the TSVs: created that month, merged that month (including ones created earlier), reviews given.
2. **Tracker**: stories owned and completed in the month (completed-date range query). Harvest the related entities the API returns for free: epic names and states, iteration dates, objective names, requesters, severity/priority fields. Epics that closed "done" with the person's stories in them are headline material.
3. **Slack**: one search of the person's own messages for the month. Standup updates reconstruct narratives; #eng-team threads reveal debugging and unblocking; escalations reveal incident work. A second targeted search when something interesting surfaces (an incident, an initiative) is worth it; five searches per month is not.
4. **Meeting notes** (Granola or similar): defer to Phase 3's bulk queries unless a month's other sources hint at something meetings would confirm (an outage, a demo, a decision).
5. **Write the month's section** in the output file: story-of-the-month lead, "What I shipped" with outcome-first bullets, judgment/unblocking blocks, a Refs footnote with every PR/ticket/epic ID. Follow `/flagrare:brag-doc` voice rules (outcome first, own it, name the judgment, no bland enumeration).

Notion tends to be low-yield per month; search it once per initiative (specs, test plans, architecture docs the person authored) rather than per month.

Before the loop, read the contributions log once by running `python3 <plugin root>/lib/career/career_state.py contributions --home "$HOME"` (the plugin root is two directories above this skill's base directory); it returns the entries from both `~/.claude/skills/flagrare/career/contributions.log.md` and the older `~/.claude/skills/flagrare/senior-scan/contributions.log.md`, without duplicates. If it returns nothing, skip this step. `/flagrare:impact-scan` (formerly senior-scan) appends dated, already-vetted contributions there (design-review interventions, unblocking threads, RFC comments), which are exactly the amplification evidence a git/tracker sweep cannot see. Fold entries into their months as amplification, not IC work.

Also read `~/.claude/skills/flagrare/career/recognition.json` when it exists (peer recognition from a tool such as Bonusly, see `/flagrare:promotion`): fold each bonus into its month as recognition, using its cleaned `text`, giver, company value and link. It is evidence that someone saw the work, not work itself.

## Phase 3: Meeting-notes sweep

After the month loop, run 2-3 broad natural-language queries over the full window against the meeting-notes tool (see playbook for phrasings that worked). This reliably surfaces what code archaeology cannot:

- Explicit manager praise and its dates
- Leadership assignments (led a retro, led a design review, ran a demo)
- Incidents and postmortems the person authored or drove
- Recognition at all-hands, ship-it slides
- Product/business numbers quoted in meetings (member counts, dollar volumes, OKR grades)
- Org-context events that change how the timeline reads: layoffs, reorgs, leadership changes, contract wins/losses, the circumstances of the person's own departure. Query for these explicitly through the very last day covered; they cluster at the end of a tenure and a sweep run even a few days early misses them. If the person resigned, establish and record the sequence relative to any layoff (a resignation submitted before layoff news is a materially different story than one after).

Fold findings back into the relevant months, marked "(from meeting records)" so provenance stays visible.

## Phase 4: Metrics pass

Attach a "**Measured by:**" block to every month, and restructure the summary around three categories: **Product** (users, engagement, adoption), **Technical** (latency, errors, reliability), **Business** (money moved, cost/time saved, OKR outcomes). Sources in descending order of strength: Start with the user's **saved measurements** (`python3 <plugin root>/lib/career/measurements.py show --home "$HOME"`): results already measured with `/flagrare:measure-impact`, each with its query, date and confidence level. Use them first, and re-run their saved queries for the window when the data platform is reachable.

1. **The company data platform.** Find it (search Notion/wiki for "data wiki", "Mode", "Snowflake", "Amplitude", "Looker", "Metabase"). If it is browser-SSO gated, the user's own Google session in the automation browser often works; product dashboards frequently hold exactly the numbers needed (member growth, payment volumes, adoption rates). Pull raw query results via the platform's own API from the authenticated page rather than scraping rendered charts (playbook has the Mode recipe). Compute tenure-window slices (value at start date vs. now) for growth claims.
2. **Meeting/OKR records**: all-hands numbers, OKR grades, before/after states quoted by others (these carry independent credibility).
3. **Datadog/Sentry**: RUM percentiles for perf claims, Sentry event counts for killed errors. Respect retention windows: if the "before" period predates retention, pair the current measurement with a baseline recorded elsewhere (a checkpoint meeting, an incident doc) and cite both.
4. **The record itself**: counts of stories/PRs/epics, same-day-fix timings, CVE CVSS scores, "N of M items" audit results.

Honesty rules, non-negotiable because this document will be read by people who can check:
- Name the source and as-of date for every number.
- Flag small samples and clamped retention windows in the text, not in your head.
- Do not claim credit for adjacent metrics (a funnel improving near the person's change is context, not attribution, unless the record shows causation). When suggestive but unproven, say so or leave it out.
- Never fabricate a baseline. "The kills stopped" with a cited meeting record beats an invented percentage.

## Phase 5: Synthesis

End the document with a one-page summary: impact-in-numbers grouped Product/Technical/Business, scale stats, the tenure arc in 3-4 sentences, and five interview stories written explicitly as "accomplished X, measured by Y, by doing Z". Rewrite headline claims in that form; supporting detail can stay narrative.

Finish by:
- Saving/refreshing the export folder (timeline + TSVs).
- Updating memory with a pointer to the file so future sessions extend rather than rebuild.
- Reminding the user, if the document contains internal figures, to review before any public use.

## Single-month or short-window invocations

The same workflow collapses gracefully: Phase 1 scopes its searches to the window, Phase 2 runs once, Phase 3's bulk queries scope to the window, Phase 5's tenure synthesis is skipped (end with the month's "Measured by" block instead). Everything else, including the honesty rules and the org-context query, applies unchanged.

## Refreshing an existing timeline

When asked to update ("more work happened since"), re-pull the enumeration TSVs, diff against the saved ones for new/newly-merged PRs, run the tracker completed-range query for the gap window only, and edit the affected month sections and summary stats in place. Do not re-run the full year.
