---
name: discovery
description: "Use when the user proposes a feature or product idea with no plan yet, asks whether something is worth building, to challenge a feature, compare with existing products or competitors, run a market scan, or write an opportunity brief. Also use when the user mentions product discovery, build versus buy, PR-FAQ, or jobs to be done."
---
# Discovery

## When to use
- User proposes a feature or product idea and no workspace or plan exists
- User asks whether something is worth building, or to challenge a feature
- User asks what already exists: competitors, alternatives, build versus buy
- User asks for an opportunity brief, a PR-FAQ, or a market scan

## Overview

Discovery decides whether and what to build. Planning decides how. The job is
killing risk before engineering commits, so a day spent deciding not to build is a
win, never a failure. The output is a one-page opportunity brief ending in a
verdict: build, buy, test first, or drop. On build, the [`plan`](../plan/SKILL.md)
skill takes over.

Reference: [market-scan.md](market-scan.md). Read it at workflow step 3.

## Workflow

1. **Reframe as an outcome.** Rewrite the request as the user or business outcome
   it serves, measurable in one sentence. A feature with no stated outcome is the
   first red flag: ask one question, or in a delegated context derive the outcome
   from the brief and record it as an assumption.
2. **Challenge the four big risks** (Cagan, *Inspired*): **value** (will anyone
   use it), **usability** (can they figure it out), **feasibility** (can we build
   it in the time we have), **viability** (does it work for the business: cost,
   legal, support). One sentence per risk, each marked `low`, `open`, or
   `blocking`, with its evidence.
3. **Scan the market.** Browse what already solves the job: competitors, adjacent
   products, open source, internal tools, and doing nothing. Search the job in the
   end user's words before any solution-shaped query, or adjacent players stay
   invisible. Compare by how well each completes the user's job, never by feature
   checklist. Query shapes, table format, and sources live in
   [market-scan.md](market-scan.md).
4. **Map opportunities before solutions** (Torres, opportunity solution tree).
   One outcome per tree: outcome, then unmet needs, then candidate solutions, then
   assumption tests. Hold at least three candidates before choosing, and "integrate
   an existing product" from step 3 is always one of them.
5. **Test the riskiest assumption cheaply.** Name the single assumption that kills
   the idea fastest. Name the cheapest test: a query over existing data, a
   prototype, five user conversations. Never a build.
6. **Write the brief** to `docs/discovery/<name>.md` and stop for the verdict.
   In a delegated context, decide, record the reason, and continue.

## The opportunity brief

One page. Every claim cites a source: a user quote, a metric, a ticket, or a URL.

| Section | Holds |
|---|---|
| Outcome | The measurable user or business outcome, one sentence |
| Evidence | Demand signals, each with its source |
| Market | Full player list (rejected ones included), scan verdict, and the comparison table from step 3 |
| Risks | The four risks, each `low`, `open`, or `blocking`, with why |
| Verdict | Build, buy, test first, or drop, with the reason |
| Kill criteria | The evidence that would reverse the verdict |

Not: "Competitor X has dashboards, we need dashboards."
Yes: "Users export to Excel weekly to answer one question (tickets #312, #340); X answers it in-product."

## Boundaries

This skill decides whether and what, never how. On a build verdict it hands the
brief to the [`plan`](../plan/SKILL.md) triage; tasks, ADRs, and code start there.
Weighing conflicting reviews or field reports belongs to
[`bias-analysis`](../bias-analysis/SKILL.md). Claims about the existing codebase
follow [`evidence-based-analysis`](../evidence-based-analysis/SKILL.md).
