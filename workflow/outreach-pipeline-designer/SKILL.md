---
name: outreach-pipeline-designer
description: Design safe, human-reviewed prospecting, lead qualification, enrichment, scoring, outreach draft, and follow-up workflows. Use when the user asks to build an outreach pipeline, prospecting workflow, lead scoring system, sales ops dashboard, market research pipeline, cold email review queue, CRM handoff, or any AI-assisted outreach process that must avoid exposing credentials, private data, prospect lists, raw prompts, scraped exports, or unattended sending.
---

# Outreach Pipeline Designer

## Overview

Use this skill to design review-first outreach systems where AI helps search, enrich, score, draft, and prioritize, but a human approves every message, export, schedule, or system-of-record change.

## Workflow

1. Clarify the audience and offer: who the outreach is for, what problem is being solved, and what channels are allowed.
2. Read `references/pipeline-blueprint.md` and choose the minimum viable pipeline stages.
3. Read `references/scoring-rubric.md` before defining score ranges, qualification fields, and next actions.
4. Read `references/review-and-safety.md` before recommending sending, exporting, enrichment, scraping, or CRM updates.
5. Produce a pipeline design with source inputs, lead fields, enrichment fields, scoring thresholds, drafting rules, review states, handoff steps, and stop conditions.
6. Use fake sample leads and fake companies in examples. Never include real prospects, emails, phone numbers, API keys, prompt text, logs, CSV exports, or private CRM data.

## Default Pipeline

Use this sequence unless the user gives a stronger domain-specific process:

1. `source`: collect candidate accounts or contacts from approved inputs.
2. `normalize`: convert inputs into a consistent lead record.
3. `enrich`: add public business context and fit signals.
4. `score`: apply a transparent qualification rubric.
5. `draft`: create a first message or follow-up prompt for review.
6. `review`: approve, edit, reject, defer, or request more context.
7. `handoff`: export approved records, create tasks, or update a CRM.
8. `follow_up`: schedule reminders or next actions after human approval.

## Safety Rules

- Do not design unattended sending. Every email, DM, post, CRM mutation, or export needs human approval.
- Do not provide instructions for evading platform limits, harvesting private contact data, bypassing consent, or scraping behind login walls.
- Do not store or publish real prospect lists, raw exports, phone numbers, emails, credentials, prompt text, or enrichment logs.
- Prefer business-level account qualification before contact-level personalization.
- Include opt-out, suppression, duplicate detection, and disqualification states in any outbound workflow.
- Tell the user to check current laws, platform terms, and internal policies before launching outreach.

## Output Format

Return:

1. Pipeline summary.
2. Stage-by-stage workflow.
3. Lead record schema using fake fields only.
4. Scoring rubric with thresholds.
5. Review queue states and human approvals.
6. Drafting and personalization rules.
7. Safety, compliance, and publication boundaries.
8. Minimal build plan or implementation checklist if the user wants to build it.

If the user supplies real leads or private data, summarize the design pattern without copying those records into the output.
