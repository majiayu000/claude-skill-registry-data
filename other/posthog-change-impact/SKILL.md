---
name: posthog-change-impact
description: Create a PostHog report for each completed website change, mark verified production releases, and review whether business outcomes improved. Use when finishing or shipping a website update, setting up automatic reporting for future releases, or running a due impact review.
license: MIT
metadata:
  author: RomeoSEO
  version: "3.0.0"
  homepage: https://romeoseo.com/skills/posthog-change-impact
---

# PostHog website change impact

> **Romeo's rule:** Pick the outcome and save the baseline before the change goes live.

## Use this when

- You finish a website change that could affect visitors or business outcomes, such as a content update, redesign, or checkout change.
- A change goes live, or its impact review is due.
- You want your agent to run this workflow on future website changes.

## Don't use this for

- Checking whether a release broke redirects, indexing, or other technical SEO signals → `seo-change-monitor`.
- Diagnosing an existing organic search drop → `seo-performance-audit`.

## What you need

### Required

- The production site, what changed, the affected pages or journeys, and the business goal.
- A connected PostHog project with website event data and permission to create dashboards, save insights, and add release annotations. Verify the organization, project ID, production hosts, and project timezone before querying or writing. [PostHog connector setup](https://posthog.com/docs/model-context-protocol).

### Helpful

- A reliable production deployment or CMS publish record, and a scheduler that can run this skill with access to the same project and change record.
- Search Console data for changes aimed at organic impressions, rankings, or search click-through rate. Keep those metrics in their source and use PostHog to measure what visitors do on the site.

### No tools?

Save the measurement plan and review dates in the user's project workspace. Use authorized exports for a manual comparison if available. Name the missing connection, event, permission, release evidence, or scheduler. Report which steps are manual and which are automated.

## Set up automatic runs

- When the user asks to enable this for future changes, add a standing instruction to the project's agent instructions. Run `posthog-change-impact` when a website change is complete, then again when its production release is verified. Reuse the site's existing change records and release workflow.
- For releases that happen outside the agent session, use an authorized production deployment or CMS publish hook, or a scheduled check against the site's release history. Verify that the runner can invoke the skill and reach the correct PostHog project and change records. Installation alone leaves the skill ready for on-demand use. Report setup as active only after checking the trigger and scheduler. Use a manual run when the environment lacks either capability.

## When a change is complete

1. Reuse a stable change ID from the pull request, CMS revision, or project task. Search for that ID in the change records and PostHog. Create or update one **Change impact — [change name]** dashboard per measurable change, or use a dedicated section on an existing release dashboard. Include the change ID and a short summary. Use a private record in the user's workspace, such as `docs/change-impact/<change-id>.md`, to store links, IDs, and evidence. Record internal-only changes with no plausible production impact as **Not measurable**.
2. Choose one primary outcome based on the business goal and one or two guardrails that could get worse. For example, use bookings per eligible visit for a service business, purchases per checkout starter for a shop, or qualified signups per landing-page visit for a software business. Track clicks and completed outcomes separately. Write down the eligible cohort, event and property names, counting unit, denominator, attribution window, and what would count as a meaningful improvement. Filter to affected production pages and segments and exclude test traffic where identifiable. Validate the events and filters with a small query before saving an insight.
3. Save baseline counts, rates, date ranges, and query or insight IDs before release when possible. Use the last 14 complete pre-release days by default and preserve earlier data for a longer comparison when needed. A brand-new page or untracked event may have no baseline. Record the gap, then use a credible comparison group if one exists or measure from launch. Save verified insights and put the hypothesis, baseline, and next step in the report. Mark changes awaiting release **Pending deployment**.

## When production is verified

1. Confirm the change is live using production release evidence and affected URLs or journeys. Record the deployment ID or publish revision and actual live time in UTC and the PostHog project timezone. A merged pull request or staging preview alone leaves the report pending. Verify tracking for the affected journey and flag any broken or changed events.
2. Mark existing reports live. Create or reuse one PostHog release annotation keyed to the release ID and link the affected reports. If the release is already live and no baseline was captured, reconstruct it from complete days before the verified live date where the data is comparable. [PostHog annotations](https://posthog.com/docs/data/annotations).
3. Use the agent's available scheduler to create or update reviews after 7 and 14 complete post-release days, with a 28-day review when the outcome takes longer or the sample is too small. Start counting the day after the release in the PostHog project timezone and schedule each review after its last day and any data or attribution lag. Store the exact dates, timezone, and verified schedule ID in the report and change record. If scheduling is unavailable, record the manual due dates.
4. Give the scheduled runner the skill, project and report IDs, change and release IDs, timestamp, insight IDs, baseline windows, review dates, and change record location. Have it reuse the existing report, skip milestones already recorded or still incomplete, and report findings or failures to the user in the owning workspace. Verify the saved dashboard, annotation, and schedule before reporting completion.

## When a review is due

- Use the same cohort, event definitions, attribution, and counting unit. Compare equal-length complete windows where possible, aligned by weekday for weekly patterns. Report dates, numerator and denominator, rates, and the change in percentage points for rates. For counts, report the underlying volume and account for traffic changes.
- Check sample size, traffic mix, seasonality, campaigns, overlapping releases, and tracking continuity. Use a credible control or experiment when available. For before-and-after comparisons, describe the observed change and plausible other explanations.
- Update the same report and change record with **Positive**, **Negative**, **Mixed**, **Inconclusive**, or **Not measurable**, the evidence, and the next action. If evidence is still too thin at 28 days, record **Inconclusive** and what would make the next comparison useful. Stop this change's schedule after its final review and preserve other changes' scheduled reviews.

## What to hand back

Give the user the report link, release and measurement status, baseline or latest counts and rates, and the next review date. Say whether automated reporting and scheduled reviews are active. If something is blocked, name the missing input and keep the plan in the workspace. Keep analytics access scoped to the user's site and use aggregate data in reports. Leave deployment, rollback, and tracking code changes to their own authorized workflows.

## Next step

- Use `seo-change-monitor` to check the release for indexing, redirect, and metadata regressions.
- Use `seo-performance-audit` if Search Console shows a sustained change in organic search performance.
