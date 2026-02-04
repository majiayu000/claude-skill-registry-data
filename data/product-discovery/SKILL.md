---
name: product-discovery
description: Conducts discovery sessions for features/products. Explores concept definition, business model, user journeys, competitive analysis, success metrics, and scoping decisions. Use when you need to explore "what is X", "let's understand", "discovery for", or the /discovery command.
---

# Discovery Skill

Conduct structured discovery sessions for features and products. This skill helps PMs explore and document a problem space before writing PRDs or creating user stories.

## Workflow Overview

The discovery process has **7 flexible phases**. All phases are optional—ask the user which aspects they want to explore at the start.

```
Phase 1: Concept Definition   → What is it? Is the problem validated?
Phase 2: Business Model       → Who manages it, for whom, how is it monetized?
Phase 3: Journey Mapping      → How do personas interact?
Phase 4: Competitive Analysis → How do competitors solve this? (OPTIONAL)
Phase 5: Success Metrics      → How do we know the solution worked? (OPTIONAL)
Phase 6: Scoping Decisions    → What goes into v1 vs. later?
Phase 7: Documentation        → Compile into a research document

```

---

## Phase 1: Concept Definition

**Objective:** Establish a shared understanding of what the concept/feature is.

**Approach:** Open-ended questions first, then structuring.

### Steps

```
1.1 Initial open-ended question
    └── "What do you understand by [X]?"
    └── "Tell me more about [X]"

1.2 Active listening + synthesis
    └── Rephrase what the user said
    └── "So [X] is [my interpretation]. Is that correct?"

1.3 Iterate until alignment
    └── As many questions as necessary
    └── Do not proceed with doubts

1.4 Concept checkpoint
    └── Summarize agreed definition
    └── "Before moving on, I confirm: [X] is [final definition]"

1.5 Problem validation
    └── "Why is this a pain point for the company?"
    └── "What evidence supports this problem?"
        ├── Quantitative: metrics, conversion, churn
        └── Qualitative: client reports, support tickets, interviews
    └── "Why solve this now?"
        ├── Urgency: revenue impact, competition, regulatory
        └── Opportunity cost of delay
    └── "What data do we have?"
        ├── Internal: analytics, NPS, support volume
        └── External: client feedback, market research

1.6 Problem validation checkpoint
    └── Summarize in table before proceeding

```

### Problem Validation Table Template

| Dimension         | Evidence                 | Source            |
| ----------------- | ------------------------ | ----------------- |
| Pain point        | [description]            | [who reported]    |
| Quantitative data | [metrics/numbers]        | [system/report]   |
| Qualitative data  | [client quotes/feedback] | [interviews/CS]   |
| Urgency driver    | [why now]                | [business reason] |

### Example 1: Hotlist (Public Safety)

```
Claude: "What do you know about hotlists in your context?"
→ Proposes hypothesis: "vehicle license plate watchlists"
User: "Let's discuss to enrich this context"
→ Series of questions about entity types, ownership, match actions
→ Result: "Hotlist = vehicle license plate watchlists that trigger
   real-time alerts when detected by LPR cameras"

```

### Example 2: Urgency Tag (Marketplace)

```
Claude: "What do you mean by 'urgency tag' feature?"
User: "A way for sellers to mark items they need to sell fast"
Claude: "So buyers could filter by urgency, and sellers pay premium
   for visibility. Is this about seller monetization or buyer UX?"
User: "Both - sellers pay, buyers find urgent deals faster"
→ Result: "Urgency tag = paid feature for sellers to highlight
   time-sensitive listings, improving discovery for buyers"

```

### Example 3: Customization Settings (SaaS)

```
User: "Users want more customization options"
Claude: "What specifically do they want to customize?"
User: "Dashboard layout, notification preferences, integrations"
Claude: "Analytics show that 80% never change defaults. Is the real
   problem that defaults don't match their workflow needs?"
→ Result: "The problem isn't lack of customization—it's that defaults
   don't serve the primary use cases. Focus on smarter defaults,
   not more options."

```

### Example 4: Problem Validation (E-commerce)

```
User: "We need a loyalty program"
Claude: "Why is this a pain point? What evidence do we have?"
User: "Repeat purchase rate is 15%, competitors have loyalty programs"
Claude: "What data supports this?"
→ Quantitative: 15% repeat rate vs 25% industry avg, 40% churn at 90 days
→ Qualitative: NPS comments mention "no reason to come back", CS tickets
   asking about rewards

| Dimension         | Evidence                     | Source             |
|-------------------|------------------------------|--------------------|
| Pain point        | Low repeat purchase rate     | Product analytics  |
| Quantitative data | 15% repeat vs 25% benchmark  | Mixpanel + industry|
| Qualitative data  | "No reason to come back"     | NPS survey Q4      |
| Urgency driver    | Competitor launched program  | Market research    |

→ Result: Problem validated. Evidence shows retention gap with clear
   quantitative + qualitative support. Competitive pressure adds urgency.

```

---

## Phase 2: Business Model

**Objective:** Understand who manages it, for whom, and business impact.

**Approach:** Questions emerge from context (not fixed). ALWAYS distinguish primary vs. future segments.

### Steps

```
2.1 Ownership
    └── "Who creates/manages [X]?"
    └── Typical options: company, client, end-user, hybrid

2.2 Segments (ALWAYS distinguish timing)
    └── "Who is the primary customer now?"
    └── "Is there potential expansion to other segments?"

2.3 Contextual questions (examples)
    ├── If data is involved: "Who owns the data?"
    ├── If payment is involved: "How is it monetized?"
    ├── If third parties are involved: "Who pays whom?"
    └── If compliance is involved: "What regulations apply?"

2.4 Checkpoint
    └── Summarize model in table: | Dimension | Primary | Future |

```

### Example 1: Hotlist (Public Safety)

```
| Dimension     | Primary             | Future                |
|--------------|---------------------|-----------------------|
| Ownership    | Admin Gabriel       | B2B Self-service      |
| Segment      | Police/City Guard   | Parking, Security     |
| Monetization | Included in product | New revenue stream    |

```

### Example 2: Seller Premium Features (Marketplace)

```
| Dimension     | Primary             | Future                 |
|--------------|---------------------|------------------------|
| Ownership    | Seller buys         | Subscription bundles   |
| Segment      | Power sellers       | All sellers            |
| Monetization | Fee per listing     | Monthly subscription   |

```

### Example 3: Notification System (SaaS)

```
| Dimension     | Primary             | Future                 |
|--------------|---------------------|------------------------|
| Ownership    | Company defines rules| Configurable rules     |
| Segment      | Enterprise clients  | SMB self-service       |
| Monetization | Included in plan    | Usage-based add-on     |

```

---

## Phase 3: User Journey Mapping

**Objective:** Map how personas interact with the feature.

**Approach:** Focus on 2-3 personas, flow in simple text.

### Steps

```
3.1 Identify personas (focus on 2-3, allow more)
    └── "Who are the primary users of [X]?"
    └── Suggest options based on context
    └── Allow user to add others

3.2 Choose journey stage
    ├── Setup/Onboarding - initial configuration
    ├── Main use - core flow
    └── Post-action - what happens after

3.3 Map flow (simple text)
    └── Numbered steps or bullets
    └── Distinguish actions by persona if relevant

3.4 Permissions (if applicable)
    └── "What can each persona do?"
    └── Table: Persona | Can create? | Can edit? | Can delete?

3.5 Checkpoint
    └── Validate flow with user before proceeding

```

### Example 1: Hotlist Setup Journey

```
Personas: Police Operator, Police Commander

Setup Journey:
1. Admin Gabriel creates hotlist types for client
2. Admin Gabriel configures webhooks per type
3. Operator/Commander views available hotlists
4. Operator/Commander adds plate + reason
5. System records audit trail (who added it)

Permissions:
| Persona    | Add plate | View list | Remove plate |
|------------|-----------|-----------|--------------|
| Operator   | Yes       | Yes       | Yes          |
| Commander  | Yes       | Yes       | Yes          |

```

### Example 2: Checkout Optimization Journey

```
Personas: Guest Buyer, Recurring Customer

Purchase Journey:
1. Buyer adds items to cart
2. Buyer goes to checkout
3. Guest: Enters shipping info OR Recurring: Uses saved address
4. Guest: Enters payment OR Recurring: Uses saved payment
5. System calculates taxes/shipping
6. Buyer reviews order summary
7. Buyer confirms purchase
8. System sends confirmation email

Drop-off points to investigate:
- Step 3: Guest abandonment (friction)
- Step 6: Price shock (unexpected fees)

```

### Example 3: Lead Management Journey in CRM

```
Personas: Sales Rep, Sales Manager

Lead Processing:
1. Marketing creates lead from form submission
2. System auto-assigns to Rep based on territory
3. Rep qualifies lead (BANT criteria)
4. Rep logs touchpoints on timeline
5. Manager reviews pipeline on dashboard
6. Rep converts to opportunity or archives

Permissions:
| Persona   | Create lead | Edit lead | Delete lead | View reports |
|-----------|-------------|-----------|-------------|--------------|
| Rep       | No (auto)   | Yes       | No          | Own only     |
| Manager   | Yes         | Yes       | Yes         | Entire team  |

```

---

## Phase 4: Competitive Analysis (OPTIONAL)

**Objective:** Understand how competitors solve the same problem.

**Approach:** 2-3 main competitors, table + qualitative highlights.

### Steps

```
4.1 Ask if user wants to include it
    └── "Do you want to include competitive analysis?"
    └── If no, skip to Phase 5

4.2 Identify competitors (2-3 main ones)
    └── "Do you know any competitors to analyze?"
    └── If no: perform web search for the domain

4.3 Research each competitor
    └── WebSearch: "[competitor] + [feature] + features"
    └── WebFetch: documentation if available
    └── G2/Capterra: feature comparison tables

4.4 Create comparison table
    └── Identified features vs. each competitor
    └── Column: Our decision + justification

4.5 Qualitative highlights
    └── Differentiators for each competitor
    └── Gaps/opportunities for us

4.6 Save references with links
    └── URLs of researched sources

```

### Example 1: Hotlist Competitive Analysis

```
Competitors analyzed: Flock Safety, Genetec AutoVu, Vigilant

| Feature       | Gabriel v1 | Flock           | Justification           |
|---------------|------------|-----------------|-------------------------|
| Metadata      | Minimal    | Rich (color,type)| Cloning invalidates data|
| Alert channel | Webhooks   | Mobile+RTCC     | v1 Simplicity           |
| TTL           | Per hotlist| Per plate       | Simple, extensible      |

Flock Differentiators:
- Shift mode (alerts only when on duty)
- Radius alerts (distance-based)
- Vehicle fingerprinting beyond plates

```

### Example 2: CRM Competitive Analysis

```
Competitors analyzed: Salesforce, HubSpot, Pipedrive

| Feature          | Our CRM   | Salesforce  | HubSpot   | Justification         |
|------------------|-----------|-------------|-----------|----------------------|
| Pricing model    | Per seat  | Per seat    | Freemium  | SMB needs + simple   |
| Customization    | Templates | Full custom | Limited   | Balance flexibility  |
| Mobile app       | Basic     | Full        | Full      | v2 Priority          |
| AI Features      | None      | Einstein    | Predictive| Roadmap item         |

HubSpot Differentiators:
- Free tier drives adoption
- Seamless marketing integration
- Better content management

Salesforce Differentiators:
- Enterprise-grade customization
- Massive app ecosystem
- Industry-specific clouds

```

### Example 3: Project Management Competitive Analysis

```
Competitors analyzed: Asana, Monday.com, Notion

| Feature       | Our Tool  | Asana      | Monday     | Notion     |
|---------------|-----------|------------|------------|------------|
| Views         | List only | List,Board | 8+ views   | Flexible   |
| Automations   | Basic     | Advanced   | Extensive  | Limited    |
| Docs          | Separate  | Minimal    | Minimal    | Native     |
| Price         | Simple    | Tiered     | Per seat   | Generous   |

Key Insight:
- Monday wins on visual appeal and templates
- Asana wins on workflow automation
- Notion wins on flexibility but loses on structure
- Our opportunity: Opinionated simplicity for small teams

```

---

## Phase 5: Success Metrics (OPTIONAL)

**Objective:** Define how we'll know the solution worked.

**Approach:** Use problem evidence (Phase 1), journey touchpoints (Phase 3), and competitive benchmarks (Phase 4) to define measurable success criteria.

### Steps

```
5.1 Ask if user wants to define metrics
    └── "Do you want to define success metrics now?"
    └── If no, skip to Phase 6

5.2 Primary success metric
    └── "What single metric proves the problem is solved?"
    └── Derived from problem evidence (Phase 1)

5.3 Leading indicators
    └── "What early signals show we're on track?"
    └── Derived from journey touchpoints (Phase 3)

5.4 Benchmarks
    └── "What are competitors achieving?" (if Phase 4 done)
    └── "What's a realistic target for v1?"

5.5 Guardrail metrics
    └── "What shouldn't get worse?"

5.6 Timeframe
    └── "When do we measure success?"
    └── v1 milestone vs long-term target

5.7 Success metrics checkpoint
    └── Summarize in table before proceeding

```

### Success Metrics Table Template

| Metric Type | Metric           | Baseline  | Target     | Timeframe |
| ----------- | ---------------- | --------- | ---------- | --------- |
| Primary     | [main KPI]       | [current] | [goal]     | [when]    |
| Leading     | [early signal]   | [current] | [goal]     | [when]    |
| Benchmark   | [competitor ref] | [theirs]  | [ours]     | [when]    |
| Guardrail   | [don't break]    | [current] | [maintain] | [always]  |

### Example 1: Loyalty Program (E-commerce)

```
| Metric Type | Metric | Baseline | Target | Timeframe |
|-------------|--------|----------|--------|-----------|
| Primary | Repeat purchase rate | 15% | 20% | 6 months |
| Leading | Loyalty signup rate | N/A | 30% | 1 month |
| Leading | Points redemption | N/A | 50% | 3 months |
| Benchmark | Industry avg repeat | 25% | 20% | 6 months |
| Guardrail | Avg order value | $85 | ≥$80 | Always |

```

### Example 2: Hotlist Alerts (Public Safety)

```
| Metric Type | Metric | Baseline | Target | Timeframe |
|-------------|--------|----------|--------|-----------|
| Primary | Alert response time | N/A | <2 min | 3 months |
| Leading | Hotlist adoption | 0 clients | 5 clients | 1 month |
| Leading | Plates added/client | N/A | >100 | 2 months |
| Benchmark | Flock response time | 90 sec | <120 sec | 3 months |
| Guardrail | False positive rate | N/A | <5% | Always |

```

### Example 3: Notification System (SaaS)

```
| Metric Type | Metric | Baseline | Target | Timeframe |
|-------------|--------|----------|--------|-----------|
| Primary | User engagement | 40% | 55% | 3 months |
| Leading | Email open rate | 18% | 25% | 1 month |
| Leading | Click-through rate | 3% | 6% | 2 months |
| Benchmark | Industry open rate | 22% | 25% | 3 months |
| Guardrail | Unsubscribe rate | 2% | <3% | Always |

```

---

## Phase 6: Scoping Decisions

**Objective:** Define what goes into v1 and what comes later.

**Approach:** List features from competition + journey, decide on each.

### Steps

```
6.1 Compile feature list
    └── Extract from competitive analysis (if done)
    └── Derive from user journey
    └── Consolidate into a single list

6.2 Ask for analysis level
    └── "Do you want to analyze line-by-line or general decision?"
    └── If line-by-line: discuss each feature individually
    └── If general: summarize decisions in a table

6.3 For each feature (if line-by-line)
    └── "Why [decision]? What is the justification?"
    └── Capture user's reasoning
    └── Document trade-off

6.4 Document in table
    └── | # | Feature | v1 Decision | Justification |
    └── Add "Future" column if relevant

6.5 Checkpoint
    └── Validate complete table before proceeding

```

### Example 1: Hotlist Feature Scope

```
| # | Feature          | Gabriel v1       | Competitor    | Justification          |
|---|------------------|------------------|---------------|------------------------|
| 1 | Hotlist creation | Admin only       | Self-service  | Flexible core API      |
| 2 | Plate metadata   | Minimal          | Rich          | Cloning invalidates    |
| 3 | Alert channel    | Webhooks only    | Multi-channel | v1 Simplicity          |
| 4 | Bulk import      | API only         | CSV + API     | CSV on roadmap         |
| 5 | Org sharing      | Not in v1        | Federation    | Low demand + GDPR      |

```

### Example 2: Notification System Scope

```
| # | Feature          | v1 Decision       | Justification                    |
|---|------------------|-------------------|----------------------------------|
| 1 | Delivery channels| Email only        | Lowest friction to start         |
| 2 | Freq. control    | Daily digest      | Prevent notification fatigue     |
| 3 | Custom triggers  | Pre-defined only  | User rules add complexity        |
| 4 | Prefs UI         | Simple toggles    | Advanced prefs in v2             |
| 5 | Analytics        | Open rates        | Deep analytics needs data        |

Future Roadmap:
- Push notifications (mobile)
- Slack/Teams integration
- User-defined trigger rules
- A/B testing for notification copy

```

### Example 3: Checkout Optimization Scope

```
| # | Feature           | v1 Decision      | Impact   | Justification          |
|---|-------------------|------------------|----------|------------------------|
| 1 | Guest checkout    | Yes              | +30% CR  | Reduces friction       |
| 2 | Saved payment     | Yes              | +15% CR  | Speed for recurring user|
| 3 | Progress indicator| Yes              | +5% CR   | Reduces uncertainty    |
| 4 | Buy now pay later | Not in v1        | Unkn.    | Needs vendor partner   |
| 5 | Social login      | Not in v1        | +10% CR  | Privacy concerns       |
| 6 | Address autocomp. | Yes              | +8% CR   | Google API available   |

Decision: Focus on #1, #2, #3, #6 for v1 (expected +58% CR improvement)

```

---

## Phase 7: Documentation

**Objective:** Compile everything into a research document.

**Approach:** Preview before saving, document saves in the squad's research folder.

### Steps

```
7.1 Compile document
    └── Standard structure based on completed phases
    └── Include only sections that were explored

7.2 Show preview to user
    └── Display formatted document
    └── Ask: "Anything to adjust before saving?"

7.3 Save document
    └── Location: {squad}/{product}/research/research-{feature}.md
    └── Confirm saving with full path

7.4 Wrap up
    └── "Discovery complete. Document saved at [path]."

```

### Document Structure

```markdown
# [Feature] - Research & Discovery

**Author:** [user]
**Date:** [today]
**Status:** Discovery complete

## 1. Context

(from Phase 1 + 2)

## 2. Product Decisions

(from Phase 6 - table)

## 3. User Journeys

(from Phase 3)

## 4. Success Metrics

(from Phase 5, if done)

## 5. Competitive Analysis

(from Phase 4, if done)

## 6. Next Steps

- [ ] Checklist of identified actions
```

---

## Integrations

**Slack:** Search for existing discussions on the topic before starting.
**Web Search:** For competitive analysis in Phase 4.
**Linear:** Check if related projects/issues already exist.

---

## Tips for PMs

### Before Starting Discovery

1. **Gather existing context** - Check Slack, docs, previous discussions.
2. **Know your stakeholders** - Who needs to be involved?
3. **Set time expectations** - Full discovery can take 30-60 min.

### During Discovery

1. **Be patient with iteration** - Good definitions take multiple passes.
2. **Challenge assumptions** - "Why do we think users need this?"
3. **Document trade-offs** - Future you will thank present you.
4. **Think in segments** - Primary vs. future helps prioritize.

### After Discovery

1. **Share the document** - Alignment requires visibility.
2. **Revisit as you learn** - Discovery is not a one-time event.
3. **Use for PRD** - The research doc is input for the PRD.

---

## References

### Product Discovery Frameworks

- [Teresa Torres' Opportunity Solution Tree](https://www.producttalk.org/)
- [Dual-Track Development](https://www.productboard.com/blog/step-by-step-framework-for-better-product-discovery/)
- [7 Product Discovery Examples - Zeda.io](https://zeda.io/blog/product-discovery-examples)

### Competitive Analysis Best Practices

- [B2B SaaS Competitive Analysis Guide](https://rampiq.agency/blog/saas-competitive-analysis/)
- [Competitor Research Template - Kalungi](https://www.kalungi.com/blog/b2b-saas-competitor-research)

### Statistics

- Microsoft: 70% of features are rarely or never used.
- Subito.it Premium Features: +3% CR, +5% revenue from discovery-led approach.

---

**Discovery complete. Would you like me to translate the next skill, or should we refine one of these further?**
