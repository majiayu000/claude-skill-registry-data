---
name: self-service-design
description: "Use this skill when designing the UX and content strategy for a Salesforce-powered self-service portal or help center — covering pre-deflection article surfacing, Help Center search UX, friction-calibrated case submission forms, community peer support layers, and deflection measurement. Trigger keywords: design self-service portal, case deflection strategy, help center UX design, reduce support volume with self-service, knowledge base search experience. NOT for Experience Cloud technical setup or component configuration. NOT for knowledge article authoring or article lifecycle management."
category: admin
salesforce-version: "Spring '25+"
well-architected-pillars:
  - User Experience
  - Operational Excellence
  - Reliability
triggers:
  - "design self-service portal for case deflection"
  - "reduce support volume with self-service help center"
  - "help center UX design and knowledge base search experience"
  - "case deflection strategy using knowledge article surfacing"
  - "friction-calibrated case submission form design"
tags:
  - self-service-design
  - case-deflection
  - help-center
  - knowledge
  - experience-cloud
  - customer-service
inputs:
  - "Current inbound case volume by contact reason (from Case reports or Einstein Conversation Mining)"
  - "Existing knowledge article inventory: count, category coverage, average age"
  - "Portal audience: authenticated customers vs. unauthenticated public visitors"
  - "Deflection goal: target reduction percentage or absolute case volume target"
  - "Available channels: Help Center, Community (peer support), Einstein Bot, email-to-case"
outputs:
  - "Self-service portal design brief covering UX structure, deflection mechanisms, and measurement plan"
  - "Pre-deflection article surfacing specification for case submission form"
  - "Friction calibration recommendation for the case submission flow"
  - "Deflection rate measurement setup using Case Deflection component"
  - "Community peer support readiness assessment"
dependencies: []
version: 1.0.0
author: Pranav Nagrecha
updated: 2026-04-06
---

# Self-Service Design

Use this skill when designing how customers or partners will find answers and optionally submit cases on a Salesforce-powered self-service portal. It activates when the goal is to reduce inbound case volume through deliberate UX design: article surfacing placement, search experience quality, case form friction calibration, and peer community engagement — not through technical Experience Cloud configuration.

---

## Before Starting

Gather this context before working on anything in this domain:

- **Contact reason breakdown:** Pull current case volume by contact reason from Case reports or Einstein Conversation Mining. Without topic-level volume you cannot prioritize which knowledge gaps to close first or measure deflection meaningfully.
- **Article inventory baseline:** Count existing knowledge articles, their category coverage, and average last-modified date. Self-service only deflects if findable, accurate articles exist for the top contact reasons. Designing UX before fixing content gaps produces cosmetic improvements with no deflection impact.
- **Portal audience type:** Authenticated community members have persistent identity; unauthenticated visitors cannot. This determines whether you can personalize article suggestions, track case submission history, or measure per-user deflection patterns.
- **Existing deflection mechanisms already in place:** Check whether the org already uses Einstein Search for Experts, Einstein Bot, or a pre-submission search prompt. Design should layer on existing mechanisms, not duplicate them.

---

## Core Concepts

### Pre-Deflection Article Surfacing

Pre-deflection is the primary lever for reducing case volume. It works by surfacing relevant knowledge articles to the customer before they submit a case — specifically during or immediately before the case submission form. The Salesforce implementation uses Knowledge search embedded in the Case Creation component on Experience Cloud sites. When a customer types a subject or description, the component queries published Knowledge articles and displays up to five suggested results inline. If the customer finds an answer, they abandon the form without submitting a case.

The effectiveness of pre-deflection depends entirely on article quality and findability:
- Articles must be published to the channel used by the portal (Customer Community or Public Knowledge Base).
- Article titles must use natural-language, customer-facing terminology — not internal support agent terminology.
- Search relevance is driven by the Knowledge search index, which weights title matches more heavily than body content.

Pre-deflection is measured by the Case Deflection component, a standard Experience Cloud component that displays a "Did this article help?" prompt and tracks whether the customer proceeded to submit a case after viewing a suggested article.

### Help Center Search UX

The Help Center template on Experience Cloud provides a search-first landing experience. The primary UX pattern is a prominent full-page search bar that queries both Knowledge articles and, optionally, community questions and answers. Design decisions for search UX:

- **Search bar placement:** Above the fold, without competing UI elements. Every additional nav item or promotional banner above the search bar reduces search usage.
- **Zero-results handling:** When search returns no results, the portal should immediately offer a case submission link — not a dead end. Unhandled zero-result states are a primary driver of customer frustration and channel escalation.
- **Faceted filtering:** Article category or product filters help customers narrow results when initial queries are broad, but should not be the primary navigation pattern. Most customers search rather than browse.
- **Article previews in search results:** Displaying the first 150–200 characters of article body in search results allows customers to assess relevance before clicking, reducing pogo-sticking and improving time-to-answer.

### Friction-Calibrated Case Submission

Case form friction is a design lever, not an accident. The goal is to require just enough steps to confirm the customer has attempted self-service before submitting a case — without causing abandonment by customers who have a legitimate transactional or complex need.

Calibration model:
1. **Mandatory search prompt (low friction):** Display a search step before showing the case form fields. Requires one interaction but does not block submission. Appropriate for most orgs as a baseline.
2. **Required article acknowledgment (medium friction):** Customer must click through a suggested article before the Submit button activates. Increases deflection rate but also increases abandonment. Use only when article coverage for the top contact reason is high (>80% of cases have a matching article).
3. **Progressive disclosure (medium friction):** Show only subject and description fields first. Surface article suggestions. Only reveal category, priority, and attachment fields after the customer dismisses the suggestions. Balances deflection opportunity with form completion.
4. **No friction (baseline):** Direct case form with no pre-deflection. Appropriate only when the org has no published Knowledge base or when the portal audience is exclusively authenticated partners with time-sensitive transactional requests.

High friction designs — multi-step wizards requiring customers to confirm they searched, rate articles, and explain why no article helped — consistently produce abandonment rather than deflection. Abandoned sessions are not deflected cases; they are unresolved customer needs that resurface through phone or email channels.

### Community Peer Support Layer

A community forum layer (Chatter Q&A or Experience Cloud Questions component) enables customers to answer each other's questions, extending the effective knowledge base without requiring internal article authoring for every topic. Design requirements for a functional community peer support layer:

- **Active seeding is required at launch:** A community with zero answered questions produces zero deflection. Before launch, seed the community with 20–50 realistic Q&A pairs using internal content (converted from existing support macros, email templates, or FAQ documents). Unseeeded communities generate a "ghost town" perception that suppresses customer engagement.
- **Expert recognition:** Visible reputation indicators (badges, answer counts, top contributor labels) drive ongoing community participation. Without recognition, high-quality contributors stop answering after initial engagement.
- **Moderation queue:** Community content requires moderation to prevent misinformation from deflecting customers to incorrect answers. Plan for a moderation workflow before enabling community Q&A for public deflection.
- **Answer promotion:** Promoting community answers to Knowledge articles for high-traffic topics creates a compounding deflection effect. This requires a workflow connecting Community question resolution to the Knowledge authoring process.

### Deflection Rate Measurement

The Case Deflection component on Experience Cloud sites tracks article views during case creation and records whether the customer submitted a case after viewing an article. The standard metric is:

**Case Deflection Rate = (Article Views During Case Creation that Did Not Result in a Case Submission) / (Total Article Views During Case Creation)**

Measurement design requirements:
- Deflection rate is a lagging metric. It does not improve until article quality and findability improve. Design for article findability first; measure deflection rate as a validation signal, not a primary leading indicator.
- Baseline contact volume must be established before portal launch. Without a pre-launch baseline, you cannot demonstrate deflection impact to stakeholders.
- Track deflection by contact reason, not just aggregate. Aggregate deflection rate masks which topic areas are working and which need article investment.
- Distinguish between deflection (customer found answer) and abandonment (customer gave up). The Case Deflection component's "Did this article help?" prompt captures intent, but low response rates to that prompt mean the metric is an approximation.

---

## Common Patterns

### Pattern: Search-First Help Center with Pre-Submission Article Surfacing

**When to use:** The org has a published Knowledge base covering the top 5–10 contact reasons, and the goal is to reduce inbound email-to-case or web-to-case volume.

**How it works:**
1. Build the portal on the Help Center Experience Cloud template (or a custom template with equivalent search prominence).
2. Place the search bar as the primary above-the-fold element with no competing UI.
3. Add the Case Creation component to the Contact Support page and enable Knowledge article suggestions in the component settings. Configure the component to display suggestions after the customer enters a subject.
4. Add the Case Deflection component to track whether customers who viewed a suggestion submitted a case.
5. Configure zero-results search behavior to show a "Contact Support" call-to-action immediately below the empty results message.
6. Set article view targets: any article with fewer than 50 views per month in a portal with 500+ monthly case submissions is likely not surfaced effectively — investigate search index positioning and title terminology.

**Why not the alternative:** Relying on article browsing (category navigation) instead of search-first design produces lower deflection rates because customers with urgent questions do not browse — they search. Category navigation serves customers exploring a product; search serves customers with a specific problem.

### Pattern: Friction Gate with Mandatory Search Before Case Submission

**When to use:** Article coverage for the top three contact reasons is high, but customers are bypassing the Help Center and submitting cases directly through bookmarked URLs or email.

**How it works:**
1. Remove direct links to the case submission form from portal navigation and email footers.
2. Route all case submission entry points through a search landing page that requires one search query before the case form link appears.
3. Use Experience Cloud page visibility rules or a custom LWC component to conditionally show the case form link only after a search interaction event fires.
4. Monitor the abandonment rate at the search gate separately from the deflection rate. If abandonment spikes, the gate friction is too high for the audience.

**Why not the alternative:** Embedding the case form directly on the search results page (low-friction pattern) is appropriate when article coverage is incomplete. The mandatory search gate is only appropriate when coverage is high; applying it prematurely frustrates customers who correctly know no article exists for their issue.

---

## Decision Guidance

| Situation | Recommended Approach | Reason |
|---|---|---|
| Article base covers fewer than 50% of top contact reasons | Invest in article authoring before portal redesign | UX improvements cannot compensate for missing content |
| Portal is primarily authenticated community members | Enable Case Deflection component + community Q&A with seeded content | Authenticated users produce better deflection measurement and can participate in peer support |
| Portal audience is unauthenticated public visitors | Search-first Help Center with pre-submission article surfacing only; no community Q&A | Unauthenticated visitors cannot participate in community; focus on Knowledge search quality |
| Org has Einstein Bot already handling first-contact deflection | Layer Help Center design to handle post-bot escalation path | Avoid duplicating deflection logic; portal is the fallback for cases the bot does not resolve |
| Stakeholder requires deflection metrics before launch | Establish baseline contact volume and contact reason distribution first | No baseline = no provable deflection impact post-launch |
| High-volume topic with no matching article | Prioritize article creation for that topic before adding friction | Adding friction when no article exists drives abandonment, not deflection |

---

## Recommended Workflow

Step-by-step instructions for an AI agent or practitioner working on this task:

1. **Establish baseline metrics.** Pull current case volume by contact reason (last 90 days minimum). Identify the top 5–10 contact reasons. Count existing published Knowledge articles per contact reason. Record total monthly case volume as the pre-launch baseline. No design work proceeds until this data is available.
2. **Assess article coverage gaps.** For each top contact reason, verify at least one published Knowledge article exists, uses customer-facing terminology in the title, and is assigned to the correct channel for the portal audience. Flag gaps. If coverage is below 50% for any of the top three contact reasons, block portal redesign work and redirect to article authoring.
3. **Design the search UX.** Specify the Help Center template layout: search bar prominence, zero-results behavior, article preview format in search results, facet availability. Validate against the principle that search must be the primary entry point, not category browsing.
4. **Specify pre-deflection article surfacing.** Define the case submission flow: where the search prompt appears, how many articles are surfaced, whether article acknowledgment is required before submission, and what happens at zero results. Calibrate friction level against article coverage completeness.
5. **Design the deflection measurement setup.** Specify Case Deflection component placement and configuration. Define the deflection rate calculation and the reporting cadence. Identify who owns the monthly review and what threshold triggers an article quality intervention.
6. **Assess community peer support readiness.** If peer community Q&A is in scope: confirm seeded content plan (minimum 20 Q&A pairs before launch), define the moderation workflow, specify the expert recognition mechanism, and document the promoted-answer-to-Knowledge workflow. If these cannot be resourced, recommend deferring community Q&A rather than launching an unseeded forum.

---

## Review Checklist

Run through these before marking work in this area complete:

- [ ] Baseline case volume by contact reason documented with pre-launch figures
- [ ] Knowledge article coverage confirmed for top 5 contact reasons (titles use customer-facing terminology, correct channel assignment)
- [ ] Search bar is the primary above-the-fold element with no competing navigation
- [ ] Zero-results search behavior routes to case submission, not a dead end
- [ ] Case submission flow includes pre-deflection article surfacing with calibrated friction level documented and justified
- [ ] Case Deflection component is configured and deflection rate measurement plan is defined
- [ ] Community Q&A either deferred (with documented reason) or launched with seeded content, moderation workflow, and expert recognition

---

## Salesforce-Specific Gotchas

Non-obvious platform behaviors that cause real production problems:

1. **Deflection rate is a lagging metric — design for findability first.** The Case Deflection component reports on outcomes, not inputs. A portal can have well-designed UX and still show 0% deflection if articles are not published to the correct channel, use internal jargon in titles, or are not indexed by the Knowledge search engine. Practitioners who optimize UX before auditing article quality waste implementation effort on a metric that will not move.

2. **Article channel assignment must match the portal audience.** Knowledge articles must be explicitly assigned to the Customer Community, Partner Community, or Public Knowledge Base channel — whichever the portal uses. An article published to the wrong channel will not appear in portal search results even if it exists in the org and is visible to internal users. This is a common post-launch surprise when knowledge articles were authored for internal use and not re-assigned before portal go-live.

3. **Friction in the case form must be calibrated — too much friction drives abandonment, not deflection.** Multi-step pre-submission wizards that require customers to rate articles, confirm they searched, and explain why no article helped consistently produce form abandonment rates above 30% in customer service research. Abandoned sessions represent unresolved customer needs that migrate to higher-cost channels (phone, email escalation), not genuinely deflected cases. Measure abandonment separately from deflection and treat high abandonment as a friction miscalibration signal.

4. **Community peer support requires active seeding — an empty forum produces no deflection.** Experience Cloud Q&A launches with zero content. Portals that launch community forums without seeded Q&A content produce a "ghost town" perception that suppresses customer posting behavior. The deflection contribution from peer community is zero until answered questions accumulate. Plan for internal seeding (20–50 realistic Q&A pairs from existing support content) before launch.

5. **Case Deflection component only measures deflection during case creation — it does not capture self-service sessions that never reached the case form.** A customer who searches, finds an answer, and leaves without opening the case form at all is not counted by the Case Deflection component. Total deflection impact is higher than what the component reports. Supplement with contact rate trend analysis (total cases per 1,000 portal sessions month-over-month) for a more complete deflection picture.

---

## Output Artifacts

| Artifact | Description |
|---|---|
| Self-service design brief | UX structure, deflection mechanism specification, friction calibration decision, and measurement plan for the portal |
| Article coverage gap report | List of top contact reasons with no matching published Knowledge article, formatted as a backlog for the knowledge team |
| Deflection measurement plan | Case Deflection component configuration, reporting cadence, deflection rate baseline, and threshold for intervention |
| Community readiness assessment | Go/defer recommendation for peer community Q&A with seeding plan if proceeding |

---

## Related Skills

- `architect/case-deflection-strategy` — Use for org-wide deflection program design across all channels (bot, portal, email, chat). This skill focuses on portal UX design specifically; the architect skill covers cross-channel strategy, Einstein Bot integration, and Einstein Conversation Mining analysis.
