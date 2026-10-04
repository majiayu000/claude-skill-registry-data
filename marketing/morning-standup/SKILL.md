---
name: morning-standup
description: >
  Full daily team standup across all 6 verticals: Sales, Social Media, Content,
  SEO, Creative, and Strategy. Spawns all vertical agents in parallel, collects
  reports, and presents a unified standup summary. Run at 9 AM daily.
tags: [daily, standup, orchestration, team, playbook]
---

# Morning Standup

The daily team standup. Run this at 9 AM every morning. It orchestrates all 6 verticals of Plasho's AI team, collects their reports, and presents a unified standup summary.

This playbook replaces the need for manually triggering each vertical separately.

## Prerequisites

- `agency.config.json` fully populated (run `/agency-setup` first)
- CRM initialized with all vertical tabs (run `/crm-setup` first)
- All 5 agent definitions installed: `sales-team-lead`, `social-media-lead`, `content-lead`, `seo-lead`, `creative-lead`
- Agent memory directories initialized for all verticals

## Composites & Capabilities Used

1. `signal-to-lead` composite -- find and score new leads (via sales vertical)
2. `lead-enrichment-pipeline` composite -- research, find contacts, validate (via sales vertical)
3. `outreach-draft-pipeline` composite -- generate personalized outreach (via sales vertical)
4. `social-content-writer` capability -- generate social posts (via social media vertical)
5. `social-engagement-responder` capability -- process engagement (via social media vertical)
6. `social-calendar` composite -- manage content calendar (via social media vertical)
7. `social-creative-brief` capability -- generate creative briefs (via creative vertical)
8. `blog-researcher` capability -- research content topics (via content vertical)
9. `content-brief` composite -- create content briefs (via content vertical)
10. `long-form-writer` capability -- draft content pieces (via content vertical)
11. `content-repurposer` composite -- repurpose content (via content vertical)
12. `programmatic-seo` composite -- scale content (via content vertical)
13. `seo-auditor` composite -- site SEO audits (via SEO vertical)
14. `technical-seo-audit` capability -- technical health checks (via SEO vertical)
15. `keyword-miner` composite -- keyword research (via SEO vertical)
16. `backlink-miner` capability -- backlink analysis (via SEO vertical)
17. `content-seo-optimizer` capability -- on-page optimization (via SEO vertical)
18. `schema-generator` capability -- structured data (via SEO vertical)
19. `video-production-brief` capability -- video briefs (via creative vertical)
20. `ad-creative-brief` capability -- ad creative briefs (via creative vertical)
21. `brand-voice` capability -- brand consistency (via creative vertical)

## Phase 0: Overnight Briefing

Before spawning any vertical agents, compile a quick executive summary by reading the CRM:

```
OVERNIGHT BRIEFING -- [Date]
---
- New inbound leads: [count]
- Email responses received: [count]
- Social mentions/signals: [count]
- Urgent items: [list or "none"]
- Tool credit status: Apollo [X%], ZeroBounce [X%]
```

Read CRM tabs for overnight changes:
- "Outreach CRM" for new responses
- "Inbound Leads" for new inbound
- "Social Media" for overnight engagement
- "Dashboard" for yesterday's summary

## Phase 1: Sales Standup

Spawn `sales-team-lead` agent. This internally coordinates:
- `inbound-lead-generator` -- find new qualified leads
- `plasho-lead-generator` -- research and enrich leads
- `plasho-sales-outreach` -- draft and queue outreach

Expected report format:
```
SALES STANDUP
  Yesterday: [leads generated], [demos booked], [follow-ups sent]
  Today: [lead target], [follow-ups due], [calls scheduled]
  Blockers: [any issues]
```

## Phase 2: Social Media Standup

Spawn `social-media-lead` agent. It executes:
- Generate today's posts (LinkedIn, Instagram, Twitter)
- Process overnight engagement and replies
- Detect and flag lead signals from social interactions
- Update the social content calendar

Expected report format:
```
SOCIAL MEDIA STANDUP
  Yesterday: [posts published], [engagement metrics], [lead signals]
  Today: [posts scheduled by platform]
  Blockers: [any issues]
```

## Phase 3: Content Standup

Spawn `content-lead` agent. It executes:
- Check content calendar and pipeline status
- Research trending topics in the Shopify/D2C space
- Draft the next content piece (blog post, case study, or pillar page)
- Update the editorial pipeline

Expected report format:
```
CONTENT STANDUP
  Yesterday: [published/drafted/researched]
  Today: [drafting target + keyword]
  Blockers: [any issues]
```

## Phase 4: SEO Standup

Spawn `seo-lead` agent. It executes:
- Monitor keyword rankings and flag changes
- Check indexation status and technical health
- Audit one prospect site (sales tool)
- Optimize one existing page for SEO

Expected report format:
```
SEO STANDUP
  Yesterday: [keywords tracked], [prospect audited], [pages optimized]
  Today: [audit target], [optimization target]
  Blockers: [any issues]
```

## Phase 5: Creative Standup

Spawn `creative-lead` agent. It executes:
- Generate creative briefs for today's social posts
- Plan upcoming video content
- Review brand consistency across recent outputs

Expected report format:
```
CREATIVE STANDUP
  Yesterday: [briefs completed], [assets delivered]
  Today: [briefs to generate by type]
  Blockers: [any issues]
```

## Phase 6: Strategy Check

Conditional execution based on day of week:
- **Monday**: Run `weekly-report` playbook (full pipeline review with metrics and forecast)
- **1st Monday of month**: Also run `strategic-review` playbook
- **Other days**: Skip, just note: "Next weekly report: [next Monday date]"

## Phase 7: Combined Standup Report

Compile all vertical reports into a unified standup:

```
MORNING STANDUP -- [Date]
================================

SALES (lead: sales-team-lead)
  Yesterday: [summary]
  Today: [plan]
  Blockers: [any]

SOCIAL MEDIA (lead: social-media-lead)
  Yesterday: [summary]
  Today: [plan]
  Blockers: [any]

CONTENT (lead: content-lead)
  Yesterday: [summary]
  Today: [plan]
  Blockers: [any]

SEO (lead: seo-lead)
  Yesterday: [summary]
  Today: [plan]
  Blockers: [any]

CREATIVE (lead: creative-lead)
  Yesterday: [summary]
  Today: [plan]
  Blockers: [any]

STRATEGY
  [Weekly/monthly status or next review date]
================================

Cross-vertical synergies:
- [Coordination needs between verticals]

Approve all? [Y] or adjust specific verticals?
```

## Phase 8: CRM Dashboard Logging

Log each vertical's summary to the "Dashboard" CRM tab via webhook:
- One row per vertical, all with today's date
- Include: Date, Vertical, Yesterday Summary, Today Plan, Blockers, Key Metrics

## Automation

This playbook is designed to be triggered daily at 9 AM. Options:
1. **Cron**: Automatic 9 AM trigger via standup-orchestrator agent
2. **Manual**: Run `/morning-standup` in Claude Code
3. **Interactive**: Say "Morning standup" to Claude Code

## Key Design Decisions

- **Parallel execution**: All 5 verticals spawn concurrently for speed
- **Fail-safe**: If any vertical fails, others continue; failures are reported
- **Approval gate**: Combined report is presented before any external actions execute
- **Strategy is conditional**: Weekly/monthly reviews only on relevant days
- **Cross-vertical coordination**: The orchestrator identifies synergy opportunities

## Example Usage

**Trigger phrases:**
- "Morning standup"
- "Run the standup"
- "Run /morning-standup"
- "Team standup"
- "9 AM standup"
- "Daily standup"
