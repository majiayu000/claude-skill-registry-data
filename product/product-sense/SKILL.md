---
name: product-sense
description: "Structured product sense/design framework for AI product roles. Covers: design a product, improve X, productize a capability."
argument-hint: "[interview question]"
---

# Product Sense Skill

Apply a structured framework to PM product sense / product design questions targeting AI product roles.

## When to Use
- User asks a "Design a product for X" question
- User asks "How would you improve X"
- User asks "How would you productize X capability"
- User says `/product-sense` followed by a question
- Any product design, product sense, or "build a product" interview question

## Context
- **Tuned for**: AI product roles at frontier AI companies
- **What matters**: First-principles thinking, ambition, structured clarity, and taste
- **Common pitfall**: Rushing to solutions without clarifying the problem first. Always start with clarifying questions.

## Framework: Product Sense (6 Sections)

Generate the answer following this EXACT structure. Each section should be substantive - not just headers.

### Section 1: Clarifications (ASK FIRST, ALWAYS)
Ask 3-5 clarifying questions before proceeding. Categories:
- **Scope**: What company are we? What's the form factor? Platform constraints?
- **Users**: Who is the primary audience? B2C vs B2B vs B2B2C?
- **Business**: What stage is the company? Revenue model? Strategic priorities?
- **Technical**: What capabilities exist? What's feasible in the timeframe?
- **Constraints**: Budget, timeline, regulatory, geographic?

After listing questions, state reasonable assumptions for each and proceed.

### Section 2: Product Strategy & Rationale (WHY BUILD THIS)
- **Company Mission**: How does this align with the company's stated mission? Reference the specific company's mission statement and connect your product thinking to it.
- **Trends & Tailwinds**: What macro trends make this timely? (AI adoption curves, regulatory shifts, user behavior changes)
- **Competition**: Who else is doing this? What's the gap?
- **Strategic Moat**: What unique advantage does this company have here?
- **Product Goal**: One sentence on what we're building and why NOW

### Section 3: User Segmentation (WHO)
Segment users along 3 dimensions and pick a primary:
- **Reach**: How many potential users in each segment?
- **Frequency**: How often would they use this?
- **Underserved**: How poorly served are they today?

For each segment provide: persona name, description, why they'd use this, current alternatives.

**Pick primary segment** with clear rationale (usually: highest frequency + most underserved).

### Section 4: User Journey & Pain Points (WHAT HURTS)
Map the user journey for the primary segment:
1. Discovery/Awareness
2. Onboarding/First Use
3. Core Usage Loop
4. Retention/Return

For each stage, identify pain points scored on:
- **Severity** (1-3): How painful is this?
- **Frequency** (1-3): How often does it occur?
- **Alternatives** (1-3): How well do current solutions address this?

**Pick top 2-3 pain points** to solve. Justify the prioritization.

### Section 5: Solutions (HOW)
For each selected pain point:

**Brainstorm** (3-4 options per pain point, range from incremental to ambitious)

**Evaluate** each on:
- Impact on pain point (High/Med/Low)
- Engineering effort (High/Med/Low)
- Strategic alignment (High/Med/Low)
- Differentiation (High/Med/Low)

**Recommend** top solution with clear rationale. Describe:
- What the user sees/experiences (be concrete and specific)
- Key features for V1 vs V2
- Why this is better than alternatives

### Section 6: Success Metrics
- **North Star Metric**: One metric that captures the core value delivered
- **Supporting Metrics** (3-4): Leading indicators that the NSM will grow
- **Counter/Guardrail Metrics** (2-3): What we must NOT break (safety, quality, trust)
- **How to measure**: What instrumentation is needed?

## AI Company Flavor

When the question is about an AI company product, layer in:
- **Safety considerations**: How does this product avoid harm? What guardrails exist?
- **Model capabilities**: What model capabilities enable this? What's the technical frontier?
- **Scaling dynamics**: How does this get better with more users/data?
- **Mission alignment**: Tie back to the specific company's mission
- **Taste**: Match the company's culture — some labs value ambitious, creative, step-change thinking; others value careful, principled, safety-first thinking; others value scientific rigor. Research the specific company's values beforehand.

## Output Format
Structure the response as a conversational walkthrough — structured but natural. Use the section headers. Aim for ~2500 words total. Flag where you'd pause for discussion or input.

## Research-First Workflow
Before generating the answer:
1. **Research** — Use web search to find latest thinking from AI company blogs, PM thought leaders, market data, competitor intel. Do 5-10 searches.
2. **Cite sources** — Include `[linked source](url)` inline for major claims, data points, and trends.
3. **Display** the complete structured answer.

## What Good Looks Like
- Starts with clarifying questions (CRITICAL)
- Shows strategic thinking before jumping to solutions
- User empathy is specific and grounded (not generic)
- Solutions are creative AND feasible
- Metrics are specific and tied to user value
- Mentions trade-offs and what you'd NOT build
- Ties back to company mission
- Shows taste and opinion (not just framework execution)
