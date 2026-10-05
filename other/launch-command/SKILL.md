---
name: launch-command
description: 'Launch orchestration and readiness assessment engine with cross-functional workstream tracking and go/no-go gates. Use when: launch readiness, launch checklist, launch orchestration, go no go, launch plan, are we ready to launch.'
---

# Launch Command (IGNITE Protocol)

A comprehensive launch orchestration engine that coordinates eight cross-functional workstreams through four progressive gates, producing a quantified readiness dashboard and executable launch day runbook. IGNITE ensures nothing ships without verified readiness across every dimension that determines launch success.

## When to Use
- Preparing for a product launch and need structured readiness tracking
- Running a go/no-go decision meeting and need objective scoring
- Coordinating multiple teams toward a shared launch date
- Building a launch day runbook with hour-by-hour execution plan
- Assessing whether a launch is ready to proceed or needs to slip
- Post-gate review to identify workstreams that are falling behind
- Transitioning from build phase to market-facing execution

## What You'll Need

**Critical inputs (ask if not provided):**
- Product name, target launch date, and launch type (GA, beta, feature, major release)
- Target audience and market segment definitions
- Positioning and messaging framework (from position-lock)
- Sales enablement status and materials inventory
- Marketing campaign plan and channel strategy (from demand-engine)
- Analytics and measurement framework (from launch-pulse)

**Nice-to-have:**
- Competitive landscape analysis (from battle-scanner)
- Partner readiness status (from partner-blueprint)
- Community/PLG strategy (from community-catalyst)
- Budget allocation plan (from budget-allocator)
- Customer journey maps (from journey-architect)
- Previous launch debriefs and lessons learned

## Process

### Step 1: Define the Eight Launch Workstreams

Each workstream represents a critical dimension of launch readiness. Assign an owner and define 5-10 criteria per workstream.

| # | Workstream | Owner Role | Weight | Description |
|---|-----------|------------|--------|-------------|
| 1 | Product | Product/Engineering | 20% | Feature completeness, stability, performance, documentation |
| 2 | Positioning | Product Marketing | 15% | Messaging locked, value props validated, differentiation clear |
| 3 | Sales Enablement | Sales/Revenue | 15% | Battle cards, talk tracks, demo environments, pricing approved |
| 4 | Marketing | Marketing/Demand Gen | 15% | Campaigns built, content ready, channels activated, PR queued |
| 5 | Partners | Partnerships | 10% | Partner communications, co-marketing assets, integration tested |
| 6 | Community/PLG | Growth/Community | 10% | Self-serve flow tested, community seeded, PLG hooks live |
| 7 | Operations | Ops/Support | 10% | Support trained, SLAs defined, escalation paths, billing ready |
| 8 | Analytics | Data/Analytics | 5% | Dashboards live, tracking verified, baselines captured, alerts set |

### Step 2: Score Each Workstream

For each workstream, define 5-10 specific criteria and score each on the IGNITE readiness scale.

**IGNITE Readiness Scale:**

| Score | Status | Definition | Visual |
|-------|--------|------------|--------|
| 0 | Not Started | No work begun, no owner assigned | Red |
| 1 | In Progress | Work underway but not complete, gaps remain | Orange |
| 2 | Complete | Work finished, awaiting verification or sign-off | Yellow |
| 3 | Verified | Complete, tested, reviewed, and approved by stakeholder | Green |

**Example: Product Workstream Criteria**

| # | Criterion | Score (0-3) | Evidence | Owner | Notes |
|---|-----------|-------------|----------|-------|-------|
| 1 | All launch features code-complete | | | | |
| 2 | QA sign-off with zero P0/P1 bugs | | | | |
| 3 | Performance benchmarks met (latency, uptime) | | | | |
| 4 | Security review completed | | | | |
| 5 | API documentation published | | | | |
| 6 | Migration/upgrade path tested | | | | |
| 7 | Feature flags configured for staged rollout | | | | |
| 8 | Rollback plan documented and tested | | | | |

**Workstream Readiness Score** = (Sum of criteria scores) / (Number of criteria x 3) x 100%

### Step 3: Four Progressive Gates

Each gate must be passed sequentially. A gate passes when its threshold conditions are met.

| Gate | Timing | Name | Threshold | Key Decisions |
|------|--------|------|-----------|---------------|
| G1 | T-60 days | Foundation | All workstreams >= 25% | Confirm launch date, lock scope, assign all owners |
| G2 | T-30 days | Readiness | All workstreams >= 50%, overall >= 60% | Lock messaging, approve budget, begin pre-launch |
| G3 | T-7 days | Confidence | All workstreams >= 75%, overall >= 80% | Final go/no-go signal, activate campaigns |
| G4 | T-1 day | Go/No-Go | All workstreams >= 75%, overall >= 90% | Ship or slip decision, launch day authorization |

**Gate Review Protocol:**
1. Each workstream owner presents 5-minute status update
2. Score each criterion live with evidence
3. Calculate workstream and overall scores
4. Identify blockers and assign resolution owners with deadlines
5. Gate decision: PASS (proceed) / CONDITIONAL (proceed with mitigations) / FAIL (remediate and re-review)

### Step 4: Calculate Overall Launch Readiness

**Overall Launch Readiness Index (LRI):**

```
LRI = SUM(Workstream_Score_i x Weight_i) for i = 1..8
```

**Decision Matrix:**

| LRI Score | Lowest Workstream | Decision | Action |
|-----------|-------------------|----------|--------|
| >= 90% | All >= 75% | GREEN: Launch | Execute launch day runbook |
| 80-89% | All >= 75% | YELLOW: Conditional | Launch with documented mitigations |
| 80-89% | Any < 75% | ORANGE: Remediate | Fix lowest workstream, re-gate in 48h |
| 70-79% | Any score | RED: Delay | Slip launch 1-2 weeks, full re-plan |
| < 70% | Any score | BLACK: Reset | Major replanning required, new date TBD |

### Step 5: Build Launch Day Runbook

Create a day-by-day execution plan from T-7 through T+30.

**Pre-Launch (T-7 to T-1):**

| Day | Activities | Owner | Verification |
|-----|-----------|-------|-------------|
| T-7 | Final gate review, campaign activation approval | PMM | Gate G3 pass |
| T-6 | Press embargo briefings begin, analyst outreach | Comms | Briefing tracker |
| T-5 | Sales team final enablement session | Sales | Quiz/cert scores |
| T-4 | Support team launch briefing, escalation drill | Support | Drill completion |
| T-3 | Social media content queued, email campaigns staged | Marketing | Campaign QA |
| T-2 | Feature flags verified, monitoring dashboards checked | Engineering | Dashboard green |
| T-1 | Go/No-Go gate G4, war room setup, all-hands brief | Leadership | G4 pass |

**Launch Day (T-0):**

| Time | Activity | Owner | Fallback |
|------|----------|-------|----------|
| 06:00 | Feature flags flipped, staged rollout begins | Engineering | Rollback within 15 min |
| 07:00 | Monitoring check: error rates, latency, uptime | SRE | Alert if >1% error rate |
| 08:00 | Press embargo lifts, PR distribution | Comms | Hold if product issues |
| 09:00 | Blog post published, social media activated | Marketing | Pause if negative signal |
| 10:00 | Email campaign sends begin (wave 1) | Demand Gen | Pause if deliverability <95% |
| 12:00 | Midday status check, war room sync | All leads | Escalation if any RED |
| 14:00 | Sales outreach begins to priority accounts | Sales | Delay if demo env unstable |
| 16:00 | Community announcement, forum post | Community | Moderate for issues |
| 18:00 | End-of-day status, overnight monitoring plan | All leads | On-call rotation confirmed |

**Post-Launch (T+1 to T+30):**

| Window | Focus | Key Metrics | Actions |
|--------|-------|-------------|---------|
| T+1 to T+3 | Stabilization | Error rates, support tickets, adoption | Hotfix if needed, respond to feedback |
| T+4 to T+7 | Early signal | Traffic, signups, activation rate | Amplify winning channels, pause underperformers |
| T+8 to T+14 | Optimization | Pipeline, conversion rates, engagement | A/B test messaging, optimize landing pages |
| T+15 to T+30 | Acceleration | Revenue, retention, NPS | Scale winning plays, plan phase 2 |

### Step 6: Risk Register and Contingency Plans

For each identified risk, document severity, probability, and mitigation.

| Risk | Severity (1-5) | Probability (1-5) | Risk Score | Mitigation | Trigger | Contingency |
|------|----------------|-------------------|------------|------------|---------|-------------|
| Product instability at scale | 5 | 2 | 10 | Load testing, staged rollout | >1% error rate | Rollback, hotfix |
| Competitive counter-launch | 3 | 3 | 9 | Embargo timing, rapid response | Competitor announcement | Battle card activation |
| Low initial adoption | 4 | 3 | 12 | PLG optimization, outreach | <50% of day-1 target | Increase paid spend, sales push |
| Negative press coverage | 4 | 2 | 8 | Analyst prebriefs, messaging QA | Negative article | Rapid response protocol |
| Support overwhelm | 3 | 3 | 9 | Pre-launch training, KB articles | >2x ticket volume | Surge staffing, chatbot deflection |

## Output

Save to `outputs/launch-command/`

### Deliverables:
1. **Launch Readiness Dashboard** -- Overall LRI score, per-workstream scores, gate status, trend over time, RED/YELLOW/GREEN indicators per criterion
2. **Gate Checklists** -- G1 through G4 detailed checklists with criteria, scores, evidence, and pass/fail determination for each gate review
3. **Launch Day Runbook** -- Hour-by-hour T-7 through T+30 execution plan with owners, verification steps, fallback procedures, and escalation paths
4. **Post-Launch Protocol** -- T+1 through T+30 monitoring plan, optimization triggers, debrief schedule, and handoff to growth-loop for ongoing retention

## Chain Connections
- **Receives from:** position-lock (messaging), demand-engine (channel strategy), enablement-forge (sales materials), journey-architect (touchpoints), partner-blueprint (partner readiness), community-catalyst (PLG strategy), budget-allocator (spend plan), launch-pulse (measurement framework), battle-scanner (competitive intel)
- **Feeds into:** launch-pulse (activates measurement), growth-loop (handoff post-launch), launch-debrief (retrospective input)
- **Enhanced by:** signal-radar (market timing signals), flywheel-sync (system health check pre-launch)
