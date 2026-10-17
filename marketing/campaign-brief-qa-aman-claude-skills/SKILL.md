---
name: campaign-brief
description: Plan a marketing campaign end-to-end using Allan Dib's Before/During/After framework (The 1-Page Marketing Plan). Produces a phase-specific campaign brief with goal, audience, message, channels, assets, timeline, budget, and success metrics. Use when the user asks to plan a campaign, brief a campaign, "we need a campaign for X", launch plan, GTM plan, marketing plan for <product>, demand gen plan, or any multi-channel marketing initiative. Reads ICP, services, and KPIs from knowledge/. For a full quarterly strategy rather than one campaign, see marketing-plan scope in positioning-doc and kpi-review. For the content schedule inside the campaign, see social-calendar. For the post-campaign review, see retro.
metadata:
  grounded_in:
    - "1-Page Marketing Plan (Before/During/After) - Allan Dib"
  reads:
    - knowledge/icp/personas.md
    - knowledge/services/
    - knowledge/markets/positioning.md
    - knowledge/markets/competitors.md
    - knowledge/kpis.md
    - knowledge/learnings.md
    - knowledge/company.md
  writes:
    - output/campaign-brief/
---

# campaign-brief

Produces a campaign brief that an empowered team can execute without needing a follow-up meeting. Every brief is anchored to one phase of the customer journey (Before/During/After) using Allan Dib's 1-Page Marketing Plan. Phase determines channels, assets, and success metrics - not the other way around.

## When to use

- "Plan a campaign for our Q3 launch"
- "Build a GTM plan for <product>"
- "Brief a demand gen campaign targeting CMOs"
- "Write the launch plan for the integration with X"
- "We need a marketing plan for <event/feature/audience>"

## Framework: Before/During/After (Allan Dib, The 1-Page Marketing Plan)

Every campaign primarily serves one phase. Force the choice before building anything else.

**BEFORE** - Prospects who don't know you exist.
- Goal: get strangers to raise their hand
- Focus: reach, awareness, USP clarity
- Channels: paid social, SEO, PR, cold outreach, events, partner content
- Success metrics: reach, impressions, hand-raisers (leads generated), CPL

**DURING** - Leads who know you but haven't bought.
- Goal: convert interest into purchase
- Focus: lead capture, nurture, trust-building, sales conversion
- Channels: email sequences, retargeting, demos, webinars, case studies
- Success metrics: MQLs, SQLs, demo bookings, trial starts, conversion rate

**AFTER** - Customers who have already bought.
- Goal: create raving fans who expand and refer
- Focus: world-class experience, upsell, cross-sell, referrals
- Channels: customer comms, CSM touchpoints, loyalty programs, referral incentives
- Success metrics: NPS, expansion revenue, referrals generated, churn rate, LTV

A campaign cannot serve all 3 phases at once. If the user wants all 3, split it into 3 campaigns.

## Inputs needed

Walk the user through these one at a time. Do not skip.

1. **Campaign phase**: Before, During, or After? If the user isn't sure, ask: "Are you trying to reach new people, convert known leads, or grow existing customers?" Force a single answer.
2. **Campaign goal**: one sentence, tied to the phase.
3. **Primary KPI**: the one number that defines success. With a target.
4. **Audience**: which persona from `knowledge/icp/personas.md`. If multiple, force-rank.
5. **Window**: start date, end date (DD-MM-YYYY).
6. **Budget**: total, or "no paid budget".
7. **Constraints**: legal, brand, channel restrictions, dependencies on other teams.
8. **What's already decided**: any creative, channel, or partner choices the user has locked in.

## Process

1. **Load context.** Read all `reads:` files. If `knowledge/icp/personas.md` is missing, stop and run `/brand-context`.

2. **Identify the phase.** Before generating any brief content, confirm the Before/During/After phase with the user. State it explicitly: "This is a BEFORE campaign. The goal is to generate hand-raisers from people who don't yet know us."

3. **Check `knowledge/learnings.md`** for any relevant past campaign retros. Reference them in the brief.

4. **Generate the brief in this format**:

   ```
   # <Campaign name>

   **Phase**: BEFORE | DURING | AFTER (Allan Dib framework)
   **Phase goal**: <get hand-raisers | convert leads | grow customers>
   **Campaign goal**: <one sentence, single-objective>
   **Primary KPI**: <metric> -> target <number> by <DD-MM-YYYY>
   **Window**: DD-MM-YYYY to DD-MM-YYYY
   **Budget**: $<amount> or <none>
   **Owner**: <person, ask the user>
   **Status**: draft

   ## Audience
   - **Primary persona**: <from knowledge/icp/>
   - **Top 3 pains we are speaking to**:
     1. ...
     2. ...
     3. ...
   - **Where they are**: channels, communities, publications

   ## Message
   - **Core message** (one sentence the audience should remember):
   - **Proof points** (3 max). Each must be lifted from `knowledge/company.md` verified proof points
  with the source named inline. If fewer than three verified proof points exist, ship fewer: write
  `[NO VERIFIED PROOF POINT]` and move it to Open questions. **Never generate a proof point** -
  these flow straight into `/linkedin-post` and `/landing-page-writer` and become public claims:
     1. ...
     2. ...
     3. ...
   - **What we are NOT saying**: explicit anti-messages to avoid scope creep

   ## Strategy
   - **Why now** (timing rationale):
   - **Differentiation vs <competitor>** (how this plays where we win):
   - **What we learned from <past campaign>** (from knowledge/learnings.md):

   ## Channel mix
   Channels must match the campaign phase. BEFORE = reach channels. DURING = conversion channels. AFTER = retention channels.

   | Channel | Role | Asset count | Spend | Owner |
   |---|---|---|---|---|
   | LinkedIn organic | Awareness | 8 posts | $0 | <name> |
   | LinkedIn ads | Demand | 3 ad sets | $X | <name> |
   | Email nurture | Conversion | 5-email sequence | $0 | <name> |
   | ... | | | | |

   ## Assets needed
   Group by team. Be specific.
   - **Content**: 1 pillar article (1800w), 8 LinkedIn posts, 3 quote graphics
   - **Design**: 1 landing page hero image, 3 ad creatives, 1 email header
   - **Video**: 1 explainer (60s)
   - **Sales enablement**: 1 one-pager, 1 deck update
   - **Web**: 1 landing page

   ## Timeline
   Working backward from launch date.
   | Week | Milestone | Owner |
   |---|---|---|
   | -4 | Brief approved, assets briefed | |
   | -3 | First drafts in review | |
   | -2 | Final assets, landing page live | |
   | -1 | Soft launch, internal alignment | |
   | 0 | Launch | |
   | +1 | First metrics review | |
   | +4 | Campaign retro | |

   ## Success metrics
   Phase-specific. Do not mix metrics from other phases.

   **BEFORE campaigns**:
   - **Primary**: <reach | CPL | hand-raisers generated> = <target>
   - **Secondary**: impressions, CTR, email sign-ups
   - **Leading indicators** (visible by week 1): ad CTR, organic post reach
   - **Lagging indicators** (visible by week 4): total leads captured, CPL

   **DURING campaigns**:
   - **Primary**: <MQLs | SQLs | demo bookings | trials> = <target>
   - **Secondary**: email open rate, demo-to-close rate
   - **Leading indicators** (visible by week 1): email opens, landing page CVR
   - **Lagging indicators** (visible by week 4): total SQLs, pipeline generated

   **AFTER campaigns**:
   - **Primary**: <NPS | referrals | expansion revenue | churn rate> = <target>
   - **Secondary**: product usage, upsell conversion, CSAT
   - **Leading indicators** (visible by week 1): feature adoption, support tickets
   - **Lagging indicators** (visible by week 4): NPS score, referrals, expansion ARR

   ## Risks and mitigations
   - **Risk**: <what could go wrong>
     **Mitigation**: <what we do about it>

   ## Open questions
   - List anything you do not have an answer to. Do not invent.

   ## Approvals
   - [ ] Marketing lead
   - [ ] Product
   - [ ] Sales
   - [ ] Legal (if applicable)
   ```

5. **Self-check**:
   - Phase is declared and all elements serve that phase
   - Channels match the phase (no conversion channels in a BEFORE campaign, no awareness channels in an AFTER campaign)
   - Single primary KPI - not three
   - Specific persona, not "marketers"
   - Working-backward timeline, not aspirational
   - Concrete assets list with counts
   - References at least one prior learning if `knowledge/learnings.md` exists
   - Phase-specific success metrics only

6. **Save** to `output/campaign-brief/<DD-MM-YYYY>-<slug>.md` with frontmatter:
   ```yaml
   ---
   format: campaign-brief
   campaign: <name>
   phase: <before|during|after>
   goal: <awareness|demand|expansion|retention|recruitment>
   start: DD-MM-YYYY
   end: DD-MM-YYYY
   primary-kpi: <metric>
   target: <number>
   budget: <amount or none>
   created: DD-MM-YYYY
   ---
   ```

7. **Offer next actions**:
   - Generate the asset list as individual skill calls (`/linkedin-post` x 8, `/landing-page-writer` x 1, etc.)
   - Build the launch deck (`/ppt-maker`)
   - Remind the user: "Set a calendar reminder to run `/retro` on [launch date + 28 days] to capture learnings."

## Rules

- Declare the phase before writing a single line of the brief. Phase determines everything else.
- One primary KPI. If the user names three, force them to rank and pick one.
- Channel mix must match the phase. A BEFORE campaign with a demo CTA is a contradiction. Call it out.
- Never copy a previous campaign brief without reading `knowledge/learnings.md` first. Past failures should change current plans.
- If budget is zero, do not propose paid channels. Reallocate to organic.
- Timeline must be working backward from launch. If the user gives a launch date, derive milestones from it. If not, ask.
- If the user wants to run a BEFORE and DURING campaign simultaneously, produce two separate briefs. Mixed-phase campaigns are unfocused campaigns.

## Handling [UNVERIFIED] and [NEEDS INPUT] tags

`brand-context` tags any number the user was unsure of as `[UNVERIFIED]`, and several skills tag
gaps as `[NEEDS INPUT]`. Those tags are a contract, and it only works if this skill honours it.

1. **Carry the tag forward.** If a baseline, benchmark or proof point arrives tagged, every figure
   derived from it is tagged too. A target built on an unverified baseline is an unverified target.
2. **Never silently promote.** Do not drop the tag because the number looked confident in the
   source file.
3. **Say it in the output.** List every tagged input in its own line near the top, so a reader
   knows which numbers are measured and which are estimates before they act on them.
4. **A decision that would change if the tagged number were wrong must say so explicitly.**

## The Before / During / After model (Allan Dib)

Allan Dib's *The 1-Page Marketing Plan* splits a campaign into three phases with different jobs,
different audiences and different metrics. Most failed campaigns are a During-phase tactic aimed at
a Before-phase audience.

| Phase | Audience | Job | Primary metric | Typical channels |
|---|---|---|---|---|
| **Before** | They do not know you | Earn attention and permission | Reach, new subscribers | Content, paid awareness, PR, partnerships |
| **During** | They know you, have not bought | Convert interest into a decision | Conversion rate, pipeline | Email, retargeting, demos, sales enablement |
| **After** | They bought | Retain, expand, get referrals | Retention, expansion, referral rate | Onboarding, community, case studies |

**One campaign, one phase.** A brief covering all three is a strategy document, not a campaign, and
it produces channel plans nobody can execute. Pick the phase, then choose channels that serve it.

## Decision thresholds

| Signal | Threshold | What to do |
|---|---|---|
| Phases in scope | More than 1 | Split into separate briefs, sequenced |
| Primary KPIs | More than 1 | Pick one. The rest are supporting metrics |
| Verified proof points | Fewer than 3 | Ship fewer and move the gap to Open questions. Never generate one |
| Baseline for the target | Missing or `[UNVERIFIED]` | Tag the target, and state which decisions change if the baseline is wrong |
| Channels planned | More than 4 for one phase | Cut. Thin coverage across many channels beats nothing, but not by much |

## Related skills

- `/brand-context` owns `knowledge/company.md`, the source of verified proof points
- `/social-calendar` turns the content line of this brief into a dated schedule
- `/kpi-review` reads the results against the target set here
- `/retro` runs after the campaign and writes reusable learnings back
- `/growth-experiment` when a channel in the plan is unproven for this audience

## What this skill cannot know

- Whether the team has capacity to produce the assets this brief plans. Ask before finalising
- Whether the budget figure is approved or aspirational
- Whether a channel worked for this audience before, unless it is in `knowledge/learnings.md`
- Whether the target derived from an `[UNVERIFIED]` baseline is reachable
