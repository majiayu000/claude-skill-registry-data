---
name: core
description: ORBWEVA CORE Method skill — the strategic glue connecting founder skills to a structured business methodology. Use when user needs to run a CORE Assessment, convert skill outputs into ARC knowledge entries, map automations to AER pillars, or define Grow dashboard metrics. Triggers on "CORE method", "CORE assessment", "ARC entries", "AER mapping", "Grow metrics", or /core commands.
---

# CORE Method Skill

The strategic glue. Run the CORE Assessment, populate ARC, map AER automations, define Grow metrics — all from your existing skill outputs.

## Commands

| Command | Description |
|---------|-------------|
| `/core:assess` | Run a CORE Assessment using skills as building blocks |
| `/core:arc` | Convert any skill output into ARC-formatted knowledge entries |
| `/core:aer` | Map automation recipes to AER Acquire/Engage/Retain pillars |
| `/core:grow` | Define Grow dashboard metrics and KPIs from startup metrics output |
| `/core:help` | Command reference |

---

## Stage 1: CORE Assessment (`/core:assess`)

**Goal:** Run a structured CORE Assessment by orchestrating existing ORBWEVA skills in the right order.

```
CORE ASSESSMENT ORCHESTRATOR
==============================
The CORE Assessment produces a Calibration Document (10-15 pages).
Instead of starting from scratch, use existing skills as building blocks.

RING 1: CALIBRATE (Foundation — get this right or everything fails)
═══════════════════════════════════════════════════════════════════
What it defines: ICP, UVP, Messaging, Pricing

Step 1: Understand the customer
  Run: /discovery:interview → design interview script
  Run: /discovery:jobs → map Jobs-to-be-Done
  Run: /discovery:analyze → synthesize into personas + insights
  Output: Research-backed ICP definition + pain map

Step 2: Design the solution
  Run: /dt:empathize → empathy maps from discovery data
  Run: /dt:define → HMW problem statements
  Output: Solution framing grounded in real user needs

Step 3: Position in market
  Run: /gtm:positioning → ICP definition, value prop canvas, competitive positioning
  Run: /gtm:pricing → value-based pricing analysis
  Output: UVP statement + pricing rationale + messaging framework

RING 1 DELIVERABLE:
  [ ] ICP Definition (from /discovery:analyze persona)
  [ ] UVP Statement (from /gtm:positioning)
  [ ] Messaging Framework (from /gtm:positioning + /dt:define)
  [ ] Pricing Rationale (from /gtm:pricing)

RING 2: OPERATE (Sales, Marketing, Finance)
═══════════════════════════════════════════
What it defines: How you sell, market, and manage money

Step 4: Go to market
  Run: /gtm:channels → channel-market fit matrix
  Run: /gtm:outreach → cold outreach sequences
  Run: /gtm:landing → landing page CRO
  Run: /gtm:launch → pre-launch checklist
  Output: GTM playbook

Step 5: Know your numbers
  Run: /startup:unit → unit economics (CAC, LTV, payback)
  Run: /startup:funnel → funnel math + bottleneck ID
  Run: /solo:books → P&L + expense tracking setup
  Output: Financial operating framework

RING 2 DELIVERABLE:
  [ ] GTM Playbook (channels, outreach, landing page)
  [ ] Unit Economics (CAC, LTV, LTV:CAC, payback period)
  [ ] Funnel Map (stages, conversion rates, bottlenecks)
  [ ] Financial Framework (P&L structure, cash flow tracking)

RING 3: REINFORCE (Team, Ops, Product)
═══════════════════════════════════════
What it defines: How you build, hire, and retain

Step 6: Retention engine
  Run: /retain:emails → lifecycle email sequences
  Run: /retain:nps → NPS/CSAT survey design
  Run: /retain:playbook → full retention strategy
  Output: Customer retention system

Step 7: Operations
  Run: /solo:onboard → client onboarding automation
  Run: /solo:clients → client management system
  Run: /solo:time → time audit + priority matrix
  Run: /legal:terms → legal foundations
  Output: Operational playbook

Step 8: Team (if applicable)
  Run: /hire:jd → job descriptions for key roles
  Run: /hire:scorecard → interview scorecards
  Output: Hiring framework

RING 3 DELIVERABLE:
  [ ] Retention System (emails, NPS, playbook)
  [ ] Operational Playbook (onboarding, client management, time)
  [ ] Legal Foundations (ToS, privacy policy)
  [ ] Hiring Framework (if scaling beyond solo)

RING 4: EVOLVE (Environment, Competition, AI Visibility)
═══════════════════════════════════════════════════════════
What it defines: How you stay ahead

Step 9: Competitive intelligence
  Run: /startup:moat → competitive moat assessment (7 types, 0-35 score)
  Run: /startup:growth → growth curve analysis
  Run: /geo:score → AI citability score
  Run: /seo:page → SEO audit
  Output: Competitive position + AI visibility score

Step 10: Automation strategy
  Run: /agent:audit → workflow automation opportunities ranked by ROI
  Run: /agent:design → agent specs for top 3 opportunities
  Run: /solo:stack → tech stack evaluation
  Output: Automation roadmap

RING 4 DELIVERABLE:
  [ ] Moat Assessment (type, score, deepening strategy)
  [ ] AI Visibility Score (GEO + SEO)
  [ ] Automation Roadmap (top 3 agents, ROI ranking)
  [ ] Tech Stack Plan (tools, costs, integrations)
```

### CORE Assessment Scorecard

```
CORE ASSESSMENT SCORECARD
===========================
Rate completion and quality of each ring (0-25 points each):

Ring 1: CALIBRATE                    ___/25
  [ ] ICP backed by 10+ interviews       (0-5)
  [ ] UVP tested against competitors      (0-5)
  [ ] Messaging framework documented      (0-5)
  [ ] Pricing validated with data         (0-5)
  [ ] All outputs in writing              (0-5)

Ring 2: OPERATE                      ___/25
  [ ] GTM channels identified + tested    (0-5)
  [ ] Unit economics calculated           (0-5)
  [ ] Funnel mapped with benchmarks       (0-5)
  [ ] Financial tracking in place         (0-5)
  [ ] Launch checklist complete           (0-5)

Ring 3: REINFORCE                    ___/25
  [ ] Onboarding sequence live            (0-5)
  [ ] Retention metrics tracked           (0-5)
  [ ] Legal docs in place                 (0-5)
  [ ] Operations documented               (0-5)
  [ ] Support system functional           (0-5)

Ring 4: EVOLVE                       ___/25
  [ ] Moat identified and scored          (0-5)
  [ ] AI visibility measured              (0-5)
  [ ] Automation opportunities ranked     (0-5)
  [ ] Tech stack optimized                (0-5)
  [ ] Growth curve diagnosed              (0-5)

TOTAL: ___/100

INTERPRETATION:
  80-100: CORE-complete. Ready for scale.
  60-79:  Strong foundation. 1-2 rings need attention.
  40-59:  Gaps in multiple rings. Prioritize Ring 1 first.
  0-39:   Early stage. Start at Ring 1, work outward.

PRIORITY RULE: Never optimize Ring N+1 until Ring N scores >=15/25.
Ring 1 wrong → everything outward is optimized for the wrong goal.
```

---

## Stage 2: ARC Conversion (`/core:arc`)

**Goal:** Convert output from any ORBWEVA skill into ARC-formatted knowledge entries.

```
ARC ENTRY CONVERTER
=====================
ARC stores structured knowledge in categories.
This converter takes skill output and formats it for ARC.

ARC CATEGORIES:
  COM — Company info (who you are, who you serve)
  SVC — Services (what you offer)
  BEN — Benefits (outcomes customers get)
  VOI — Voice (brand voice, tone, key phrases)
  TMP — Templates (email templates, scripts, SOPs)
  PRC — Pricing & Process (pricing tiers, delivery workflow)

SKILL → ARC MAPPING:

/discovery:analyze → COM entries
  Persona name, role, goals, frustrations, trigger events
  Format: COM-001, COM-002, etc.

/gtm:positioning → COM + VOI entries
  ICP definition → COM
  Value prop → COM
  Competitive positioning → VOI (differentiation language)
  Key phrases → VOI

/gtm:pricing → PRC entries
  Pricing tiers, rationale, comparison → PRC-001, PRC-002
  Guarantees → PRC

/solo:offer → SVC + BEN entries
  Service packages → SVC-001, SVC-002
  Deliverables → SVC
  Outcomes/benefits → BEN-001, BEN-002

/retain:emails → TMP entries
  Email sequences → TMP-001, TMP-002
  Subject lines → TMP

/solo:copy → VOI + TMP entries
  Brand voice guidelines → VOI
  Landing page copy → TMP
  Ad copy → TMP

/legal:terms → TMP entries
  ToS template → TMP
  Privacy policy → TMP

ARC ENTRY FORMAT:
  ID:       [CATEGORY]-[3-digit number]  (e.g., COM-001)
  Title:    [Short descriptive title]
  Category: [COM/SVC/BEN/VOI/TMP/PRC]
  Content:  [The actual knowledge — 1-3 paragraphs]
  Source:   [Which skill/command produced this]
  Date:     [When created]
  Ring:     [Which CORE ring this belongs to: 1/2/3/4]
```

### ARC Population Checklist

```
ARC POPULATION CHECKLIST
==========================
Minimum viable ARC (before any automation runs):

Ring 1 → ARC (MANDATORY before AER deployment):
  [ ] COM-001: ICP definition (from /discovery:analyze)
  [ ] COM-002: Company description (manual)
  [ ] SVC-001: Primary service (from /solo:offer)
  [ ] BEN-001: Top 3 customer outcomes (from /gtm:positioning)
  [ ] VOI-001: Brand voice guidelines (from /solo:copy)
  [ ] VOI-002: Key phrases and messaging (from /gtm:positioning)
  [ ] PRC-001: Pricing tiers (from /gtm:pricing)

Ring 2 → ARC (before scaling):
  [ ] TMP-001: Email templates (from /retain:emails)
  [ ] TMP-002: Outreach sequences (from /gtm:outreach)
  [ ] SVC-002+: Additional services (from /solo:offer)
  [ ] PRC-002: Delivery process/SOP (from /solo:onboard)

Ring 3 → ARC (for retention):
  [ ] TMP-003: Support FAQ (from /solo:support)
  [ ] TMP-004: Onboarding sequence (from /solo:onboard)
  [ ] VOI-003+: Persona-specific voice variants

Ring 4 → ARC (for evolution):
  [ ] COM-003: Competitive landscape (from /startup:moat)
  [ ] COM-004: Market trends (from /agent:research)
```

---

## Stage 3: AER Mapping (`/core:aer`)

**Goal:** Map ORBWEVA skill outputs and agent recipes to AER's three pillars.

```
AER PILLAR MAPPER
==================
AER = Acquire + Engage + Retain
Each pillar is an automation system. Map your skill outputs to the right pillar.

ACQUIRE (Lead Generation & Nurturing)
═══════════════════════════════════════
"Find people who need your services and put them in your inbox."

Skills that feed Acquire:
  /gtm:outreach      → Cold email + LinkedIn sequences
  /gtm:landing       → Landing page optimization
  /solo:leads        → Lead magnet + funnel architecture
  /solo:sales        → Discovery call scripts + proposals
  /agent:leads       → Lead qualifier agent (n8n recipe)

Acquire Automation Stack:
  ┌─────────────────────────────────────────────┐
  │  1. Target    → ICP from /gtm:positioning    │
  │  2. Find      → /agent:leads (scraping)      │
  │  3. Verify    → Email verification            │
  │  4. Nurture   → /gtm:outreach sequences      │
  │  5. Qualify   → /agent:leads (scoring)        │
  │  6. Deliver   → Hot leads to inbox            │
  └─────────────────────────────────────────────┘

ARC entries needed: COM-001 (ICP), VOI-001 (voice), TMP-002 (outreach)
Agent recipe: /agent:leads
Grow metrics: leads/month, cost per lead, lead-to-customer rate


ENGAGE (SEO Content Engine)
═══════════════════════════
"Create and post content every day. Zero effort."

Skills that feed Engage:
  /solo:content      → Content batching + repurposing chain
  /solo:copy         → Sales copy frameworks
  /geo:score         → AI citability scoring
  /geo:optimize      → Content optimized for AI search
  /seo:page          → SEO audit per page
  /seo:schema        → Schema.org markup
  /agent:content     → Content repurposing agent (n8n recipe)
  /agent:social      → Social media scheduling agent

Engage Automation Stack:
  ┌─────────────────────────────────────────────┐
  │  1. Record    → Monthly content session       │
  │  2. Write     → /agent:content (AI repurpose) │
  │  3. Optimize  → /geo:optimize + /seo:page     │
  │  4. Publish   → /agent:social (multi-platform) │
  │  5. Report    → Grow dashboard                 │
  └─────────────────────────────────────────────┘

ARC entries needed: VOI-001 (voice), SVC-* (services), BEN-* (benefits)
Agent recipes: /agent:content, /agent:social
Grow metrics: content pieces/week, organic traffic, AI citations


RETAIN (24/7 AI Support)
═════════════════════════
"An AI assistant that answers customer questions instantly."

Skills that feed Retain:
  /retain:emails     → Lifecycle email sequences
  /retain:nps        → NPS/CSAT surveys
  /retain:cohort     → Cohort analysis
  /retain:playbook   → Full retention strategy
  /solo:support      → FAQ templates + escalation
  /solo:onboard      → Client onboarding
  /agent:support     → Customer support agent (n8n recipe)
  /agent:onboard     → Client onboarding agent

Retain Automation Stack:
  ┌─────────────────────────────────────────────┐
  │  1. Train     → ARC knowledge base            │
  │  2. Deploy    → /agent:support (AI chatbot)    │
  │  3. Handle    → Auto-respond to 80% of Qs     │
  │  4. Handoff   → Complex → human with context   │
  │  5. Learn     → Log interactions → improve ARC │
  └─────────────────────────────────────────────┘

ARC entries needed: SVC-* (services), TMP-003 (FAQ), PRC-* (pricing)
Agent recipes: /agent:support, /agent:onboard
Grow metrics: response time, resolution rate, NPS, churn rate
```

### AER Deployment Readiness

```
AER DEPLOYMENT READINESS
==========================
Before deploying any AER pillar, check:

ACQUIRE readiness:
  [ ] ICP defined and validated (/gtm:positioning)
  [ ] Outreach sequences written (/gtm:outreach)
  [ ] Landing page scoring >=50/70 (/gtm:landing)
  [ ] Lead scoring criteria defined (/agent:leads)
  [ ] ARC entries: COM-001, VOI-001, TMP-002
  Ready? [ ] Yes  [ ] No → Run Ring 1 skills first

ENGAGE readiness:
  [ ] Content strategy defined (/solo:content)
  [ ] Brand voice documented (/solo:copy)
  [ ] GEO score >=70/100 (/geo:score)
  [ ] SEO baseline established (/seo:page)
  [ ] ARC entries: VOI-001, SVC-*, BEN-*
  Ready? [ ] Yes  [ ] No → Run Ring 1-2 skills first

RETAIN readiness:
  [ ] Onboarding sequence designed (/retain:emails)
  [ ] FAQ documented (/solo:support)
  [ ] NPS/CSAT survey designed (/retain:nps)
  [ ] Escalation rules defined (/agent:support)
  [ ] ARC entries: SVC-*, TMP-003, PRC-*
  Ready? [ ] Yes  [ ] No → Run Ring 1-3 skills first
```

---

## Stage 4: Grow Metrics (`/core:grow`)

**Goal:** Define Grow dashboard KPIs from startup metrics skill output.

```
GROW DASHBOARD BUILDER
========================
Map your metrics to the Grow dashboard structure.

LAYER 1: HEADLINE METRICS (top of dashboard)
  North star metric: ___ (from /gtm:metrics)
  Monthly revenue:   $___ (from /solo:books)
  Active customers:  ___
  Growth rate:       ___% MoM (from /startup:growth)

LAYER 2: AER PILLAR METRICS

  ACQUIRE:
    Leads generated:          ___/month (from /startup:funnel)
    Cost per lead:            $___ (from /startup:unit)
    Lead-to-customer rate:    ___% (from /startup:funnel)
    Pipeline value:           $___

  ENGAGE:
    Content pieces published: ___/week (from /solo:content)
    Organic traffic:          ___/month (from /seo:page)
    AI citation score:        ___/100 (from /geo:score)
    Social engagement rate:   ___%

  RETAIN:
    Churn rate:               ___% (from /startup:churn)
    NPS score:                ___ (from /retain:nps)
    Avg response time:        ___ min
    Customer lifetime value:  $___ (from /startup:unit)

LAYER 3: FINANCIAL HEALTH
  Monthly burn:     $___ (from /startup:runway)
  Runway:           ___ months (from /startup:runway)
  LTV:CAC ratio:    ___:1 (from /startup:unit)
  Profit margin:    ___% (from /solo:books)

LAYER 4: AI OPERATIONS
  Active automations:     ___ (from /agent:audit)
  AI decisions/week:      ___
  AI health score:        ___/100
  Monthly AI spend:       $___ (from /agent:design cost estimates)

LAYER 5: COMPETITIVE POSITION
  Moat score:            ___/35 (from /startup:moat)
  Growth curve type:     ___ (from /startup:growth)
  Fundraise readiness:   ___/100 (from /startup:ready)
```

### Grow Alert Thresholds

```
GROW ALERT THRESHOLDS
=======================
Set these to get proactive alerts when metrics go off track.

CRITICAL (red — act immediately):
  Churn rate > 8%/month
  Runway < 3 months
  AI health score < 50/100
  Zero leads for 7+ days
  NPS < 0

WARNING (yellow — investigate this week):
  Churn rate > 5%/month
  LTV:CAC < 3:1
  Funnel conversion dropping >20% WoW
  Content cadence missed 2+ weeks
  AI spend > 15% of revenue

HEALTHY (green — keep going):
  Churn < 3%/month
  LTV:CAC > 3:1
  NPS > 30
  AI health > 80/100
  Runway > 12 months
```

---

## Integration Notes

```
THE ORBWEVA SKILLS ECOSYSTEM
==============================
                    ┌──────────────┐
                    │  /core:assess │ ← START HERE
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │ Ring 1   │ │ Ring 2   │ │ Ring 3-4 │
        │ Calibrate│ │ Operate  │ │ Reinforce│
        │          │ │          │ │ + Evolve │
        └────┬─────┘ └────┬─────┘ └────┬─────┘
             │            │            │
             ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌──────────┐
        │/core:arc │ │/core:aer │ │/core:grow│
        │ populate │ │ deploy   │ │ measure  │
        └──────────┘ └──────────┘ └──────────┘

Feeds from (all 8 ORBWEVA skill repos):
  - /discovery:* → Ring 1 (Calibrate)
  - /dt:* → Ring 1 (Calibrate)
  - /gtm:* → Ring 1-2 (Calibrate + Operate)
  - /startup:* → Ring 2-4 (Operate + Evolve)
  - /pitch:* → Ring 2 (Operate — fundraising)
  - /legal:*, /hire:*, /retain:* → Ring 3 (Reinforce)
  - /solo:* → Ring 2-3 (Operate + Reinforce)
  - /agent:* → Ring 4 (Evolve — automation)

This skill is the orchestrator. It doesn't replace any skill —
it sequences them and converts their outputs into the CORE framework.
```

## Principles

1. **Rings build outward in dependency order.** Get Ring 1 wrong -- everything outward is optimized for the wrong goal.
2. **Skills are the building blocks, CORE is the blueprint.** Each skill produces raw material; CORE assembles it into a business.
3. **ARC before AER.** Never automate what you haven't documented. Knowledge first, automation second.
4. **Measure what matters.** Grow shows what's working. Without metrics, you're guessing.
5. **The assessment never ends.** CORE is a quarterly cycle, not a one-time exercise.
