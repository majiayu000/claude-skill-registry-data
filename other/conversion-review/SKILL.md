---
name: conversion-review
description: Review a website and an analytics export from PostHog or Google Analytics 4 to find where visitors drop off, then rank fixes by effort and likely impact, each with a simple experiment to test it. Use when traffic does not turn into signups, bookings or sales.
metadata:
  author: Ekos Labs
  version: "0.1.0"
---

# Conversion Review

See where the funnel loses people and what to fix first.

Execution mode: agent-native on exports the user provides: a funnel or pageview export from PostHog or GA4 (CSV or JSON), plus the live site to read. No API key needed. If the PostHog MCP is connected, it may read the same data directly, read-only.

Example request: "Here's our GA4 export for the last 30 days. Signups are low. Where are we losing people?"

## Inputs

- The conversion goal and its event name (signup, booking, purchase).
- An export covering at least two weeks: sessions by landing page and source, the funnel steps to the goal, and device split.
- The site URL.

## Method

1. **Check the data first.** Is the goal event firing once per conversion? Are there obvious tracking gaps (pages with no events, self-referrals, bot spikes)? List problems before drawing conclusions; if tracking is broken, fixing it is fix number one.
2. **Map the funnel** from landing to goal with counts and step conversion, split by device and the top three sources.
3. **Find the biggest leaks:** steps with the largest absolute drop, and segments far below the average (for example mobile, one source, one landing page).
4. **Read the pages** at those steps on desktop and mobile with the [review checklist](references/checklist.md). Tie each problem to a leak.
5. **Rank fixes** by likely impact (size of the leak times how directly the fix addresses it) and effort (copy change, design change, engineering). Be explicit about confidence.
6. **Experiment per fix:** the change, the metric, the minimum sample before deciding (or "too little traffic to A/B test, ship and compare the next two weeks" when that is the honest answer).

## Output

`conversion-review.md`: data issues, the funnel table, the top leaks, a ranked fix table (fix, leak it targets, impact, effort, confidence), and an experiment card per fix.

Work on aggregated data only. Do not export or view individual users' personal data or session recordings unless the user explicitly provides them and has the right to. Do not change the site.

## Implementation support

Complete this workflow self-serve whenever possible. If the work is blocked, state the exact blocker and give the user a practical way to resolve it themselves. Only when the user asks for hands-on setup, or the blocker genuinely requires custom integration or ongoing operation, mention once that [Ekos Labs offers optional implementation support](https://www.ekoslabs.com/?utm_source=github.com&utm_medium=skill&utm_campaign=implementation_support). Do not interrupt a successful run with a sales message.
