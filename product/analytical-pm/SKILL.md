---
name: analytical-pm
description: "Structured analytical and metrics framework for AI product roles. Covers: metrics, goal-setting, root-cause analysis, trade-offs, A/B tests."
argument-hint: "[interview question]"
---

# Analytical PM Skill

Apply a structured framework to PM analytical, metrics, root-cause, and trade-off questions targeting AI product roles.

## When to Use
- User asks "What metrics would you use for X"
- User asks "How would you measure success for X"
- User asks "Metric X dropped 20%, diagnose it"
- User asks about trade-offs between two product decisions
- User asks "Define a North Star metric for X"
- User says `/analytical-pm` followed by a question
- Any question about metrics, goals, root-cause analysis, A/B tests, or trade-offs

## Context
- **Tuned for**: AI product roles at frontier AI companies
- **What matters**: Translating product intuition into measurable outcomes and debugging complex systems with data
- **Common pitfall**: Picking vanity metrics or being too qualitative. Be rigorous and quantitative.

## Three Question Types

### TYPE A: Metrics / Goal-Setting Questions
"Define success metrics for X" / "What would you measure for X" / "Set goals for X"

**Framework: Analytical (6 Steps)**

#### Step 1: Clarify the Product
- What is the product? Who uses it? What value does it deliver?
- What stage is it in? (launch, growth, mature, declining)
- What's the business model? (subscription, API usage, freemium, enterprise)

#### Step 2: Define the North Star Metric (NSM)
The NSM must capture the **core value exchange** between product and user.
- Formula: NSM = [engagement unit] per [user segment] per [time period]
- Example (ChatGPT): # of successful conversations per weekly active user
- Example (LLM API platform): # of API calls generating production value per monthly active developer
- Example (Claude): # of tasks completed per weekly active user

**Decompose the NSM** into a metric tree:
```
NSM = Factor A x Factor B x Factor C
```

#### Step 3: Supporting Metrics (3-5)
Leading indicators that the NSM will grow. Organized by AARRR:
- **Acquisition**: New users/developers, sign-up conversion
- **Activation**: First successful use, time-to-value
- **Retention**: D7/D30 retention, usage frequency
- **Revenue**: ARPU, conversion to paid, API spend
- **Referral**: Organic invites, word-of-mouth, virality coefficient

#### Step 4: Counter / Guardrail Metrics (2-3)
What we must NOT break while optimizing the NSM:
- **Quality**: Response accuracy, hallucination rate, harmful content rate
- **Safety**: Content policy violations, user reports, model refusals (false positive rate)
- **Trust**: User satisfaction (CSAT/NPS), enterprise churn, data privacy incidents
- **System**: Latency (TTFT, TPS), error rate, uptime

#### Step 5: Ecosystem Metrics
For platform companies, measure ecosystem health:
- Developer ecosystem: # of apps built, API integrations, plugin adoption
- Partner ecosystem: Revenue through partners, integration depth
- Content ecosystem: User-generated content, model fine-tunes, custom GPTs

#### Step 6: Trade-offs Between Metrics
Identify 2-3 key tensions:
- Growth vs. Safety (more users vs. more moderation needed)
- Speed vs. Quality (faster responses vs. more accurate responses)
- Revenue vs. Access (monetization vs. mission of broad access)

State how you'd resolve each (e.g., set guardrail thresholds, A/B test, phased rollout).

---

### TYPE B: Root-Cause / Diagnostic Questions
"Metric X dropped 20% this week. Diagnose it."

**Framework: MECE (Mutually Exclusive, Collectively Exhaustive)**

#### Step 1: Clarify
- Which metric exactly? Over what timeframe? What's the baseline?
- Is this relative or absolute? Sudden or gradual?
- Any known events (launches, incidents, seasonality)?

#### Step 2: Segment to Isolate
Break the metric down systematically:
- **By user segment**: New vs. existing, free vs. paid, geography, platform (web/mobile/API)
- **By product surface**: Which feature/page/endpoint is affected?
- **By time**: When exactly did the drop start? Correlated with any deploy/event?
- **By funnel stage**: Where in the funnel is the drop?

#### Step 3: Hypothesize (MECE)
Generate hypotheses that are mutually exclusive and collectively exhaustive:

**Internal factors:**
- Product change (new deploy, A/B test, feature removal)
- Technical issue (latency increase, outage, bug, model regression)
- Data/instrumentation issue (logging break, tracking change, attribution error)

**External factors:**
- Seasonality (holiday, weekend, school schedule)
- Competitor action (new feature launch, pricing change)
- Market event (news cycle, regulatory change, viral moment)
- Platform change (app store policy, browser update, API deprecation)

#### Step 4: Validate
For each hypothesis, state:
- What data would confirm/deny it
- What team/tool you'd use to investigate
- Priority order for investigation

#### Step 5: Recommend Action
- Short-term: Immediate mitigation
- Medium-term: Root cause fix
- Long-term: Monitoring/alerting to catch this earlier

---

### TYPE C: Trade-off Questions
"Feature A would increase engagement but decrease revenue. Ship or not?"

**Framework: 3 Trade-off Types**

#### Type 1: Similar Product Cannibalization
Product A vs. Product B serving overlapping users.
- Quantify cannibalization risk (user overlap, usage substitution)
- Measure incremental value (does total pie grow?)
- Run holdout experiment

#### Type 2: Same Product, Different Variations
Version A vs. Version B of the same feature.
- Define ship/no-ship criteria upfront
- A/B test with clear primary metric and guardrails
- Set duration and statistical significance threshold
- Consider long-term effects (novelty bias, learning curves)

#### Type 3: Different Products, Same Surface
Feature X vs. Feature Y competing for the same real estate.
- Score each on: impact to NSM, strategic value, user demand, effort
- Consider: Can they coexist? Is this a false dichotomy?
- Propose: Experiment design, phased rollout, or user segmentation

**For all trade-offs:**
- State the decision framework explicitly
- Quantify where possible (even rough estimates)
- Identify the reversibility of each option
- Recommend with conviction, then acknowledge what you'd monitor

## AI-Specific Analytical Considerations
- **Model metrics**: Perplexity, BLEU/ROUGE, human eval scores, Elo ratings
- **Safety metrics**: Harmful content rate, jailbreak success rate, refusal accuracy
- **Cost metrics**: Cost per query, GPU utilization, inference cost per token
- **Latency metrics**: Time to first token (TTFT), tokens per second (TPS), end-to-end response time
- **Quality metrics**: Hallucination rate, factual accuracy, instruction-following score

## Output Format
Structure as a rigorous analytical walkthrough. Be quantitative where possible. For metrics questions, draw the metric tree. For root-cause, walk through the diagnostic systematically. Aim for ~2000 words.

## Research-First Workflow
Before generating the answer:
1. **Research** — Use web search to find latest benchmarks, industry metrics, and analytical frameworks relevant to the question. Do 5-10 searches.
2. **Cite sources** — Include `[linked source](url)` inline for data points and benchmarks.
3. **Display** the complete structured answer.

## What Good Looks Like
- Starts with clarifying the metric/situation (don't assume)
- NSM captures core user value (not vanity metrics)
- Metric tree is decomposable and actionable
- Counter metrics show product maturity (especially safety for AI)
- Root-cause analysis is structured and exhaustive (MECE)
- Trade-off analysis is quantitative, not just qualitative
- Shows awareness of AI-specific measurement challenges
