---
name: gtm-decision-lab
description: Market and demand reality-check workflow for AI builders, founders, indie hackers, B2B SaaS, developer tools, PMM, growth, incubator, and advisory work. Use when the user needs to test whether a project has real demand, choose a beachhead segment, audit target customers, separate evidence from founder assumptions, check AI hype risk, select a GTM motion, pressure-test positioning, design first validation experiments, or turn messy product/customer notes into a defensible market reality and GTM decision brief. Do not use for product feature design, technical architecture, mature enterprise launch operations, campaign calendars, or generic marketing copy unless the user first needs market/demand decisioning.
---

# GTM Decision Lab

Turn partial early-stage product evidence into a market reality and GTM decision brief. Prioritize decision quality over polish: expose evidence, assumptions, risks, confidence, validation gates, and whether the user should build, validate first, or hold.

## Operating Principle

This skill does not validate the user's ego. It validates market reality.

Never present a market or GTM guess as a fact. If evidence is weak, produce a validation plan or hold decision instead of a full strategy. Treat customer evidence as stronger than public market commentary.

Only serve market and demand decisions. Do not decide what the product should become. Do not design product features, UX, technical architecture, or roadmap unless a feature is strictly needed to test demand, adoption, trust, or willingness to pay.

## Workflow

### 1. Intake and Evidence Audit

Collect enough context to decide what the user is actually asking:

- Product and core use case
- Current stage: idea, prototype, first users, first revenue, repeatable motion, or scaling
- Candidate customers, users, buyers, or segments
- Current evidence: interviews, sales calls, demos, waitlist reasons, usage data, revenue, support tickets, community signals, competitor observations
- Delivery object: what result the user will actually receive, not what the product is called
- Constraints: time, team, budget, geography, audience access, regulatory or trust requirements
- Desired outcome: first users, first revenue, validation, fundraising story, pipeline, launch plan, or segment choice

If evidence is thin, state that clearly and continue with assumption labels. Do not block unless the user is asking for a high-confidence recommendation without enough information.

Read `references/evidence-standards.md` when judging evidence quality, confidence level, or red flags.

Read `references/source-map.md` when the user asks for market research, competitor research, buyer research, channel research, or when the brief needs external evidence beyond user-provided notes.

Use `assets/intake-template.md` when the user's input is too short, scattered, or missing stage/evidence/constraint details. Ask the user to fill only the fields needed for the current decision; do not force the full template for small requests.

### 2. Run Market Reality Check

Before GTM motion or channel work, test whether the market need is real enough to continue:

- Demand type: pain, convenience, curiosity, compliance, revenue, risk reduction, status, or AI hype
- Target customer precision: who has the problem, in what situation, and why now
- Use case clarity: what job or workflow changes for the user
- Current alternative: what they use now, including manual work, spreadsheets, agencies, existing tools, or doing nothing
- Delivery object: the concrete result the customer receives
- Switching reason: why they would change behavior
- Trust/adoption requirement: what must be true before they rely on the product
- Willingness signal: payment, pilot, data sharing, demo commitment, referral, waitlist, compliment, or vague interest

Read `references/ai-project-market-risks.md` for AI-specific market risks, especially when the project uses AI as a core capability or selling point.

Required output:

- Market reality verdict: Build / Validate / Hold
- What can be believed now
- What cannot be believed yet
- Most dangerous assumption
- Smallest next validation action

### 3. Diagnose GTM Stage

Classify the user's stage and adapt the output:

| Stage | Default output |
|---|---|
| Idea only | Problem and buyer validation plan |
| Prototype | Segment and pain validation plan |
| First users | Beachhead and positioning hypothesis |
| First revenue | Motion and repeatability assessment |
| Repeatable motion | Channel and scaling decision brief |
| Scaling | Use this skill only for a focused GTM decision audit |

When the user is pre-revenue or pre-repeatability, avoid polished 90-day growth plans. Give the smallest testable GTM decision.

### 4. Choose or Audit Beachhead Segment

Compare at least two segments when possible. If the user offers only one, frame the output as an assumption audit and ask for alternatives only if comparison is necessary.

Read `references/scoring-rubric.md` for scoring dimensions, gates, and confidence rules.

Required output:

- Recommended beachhead or "hold pending validation"
- Scorecard with assumption flags
- Rejected or deferred segments with specific reasons
- What must be true for the recommendation to hold

### 5. Run Builder Reality Check

Calibrate whether the builder is positioned to learn from and deliver to the market:

- Access: Can the builder reach target users directly?
- Credibility: Why would this market trust the builder?
- Feedback: Can the builder get real user evidence quickly?
- Domain understanding: Is judgment grounded in customer contact or self-reference?
- Distribution: Is there any unfair access, community, audience, or partner path?
- AI-backward reasoning: Is the builder starting from "AI can do this" rather than "customers already struggle with this"?

This section should not judge personal worth. Judge market fit between builder, audience, evidence, and delivery path.

### 6. Select GTM Motion

Recommend one primary motion and, when useful, one supporting motion. Do not recommend a channel just because it is common.

Read `references/gtm-motions.md` for motion criteria and contraindications.

Required output:

- Primary motion
- Why it fits the buyer, price, product complexity, proof burden, urgency, and team constraints
- When the motion would be wrong
- First practical action for the motion

### 7. Build Positioning Hypothesis

Create a testable hypothesis, not final brand copy:

- For whom
- In what trigger situation
- Current alternative
- Main pain
- Why now
- Why this product
- Proof needed

Flag claims the user should not make until proven.

### 8. Design Validation Experiments

Read `references/validation-experiments.md` when building the experiment plan.

Design 14-day or 30-day experiments with:

- Hypothesis
- Target segment
- Channel or source
- Action
- Success signal
- Failure threshold
- Evidence to collect
- Decision rule after the experiment

Experiments must be small enough for a founder or small team to run.

### 9. Produce the Decision Brief

Use `assets/gtm-decision-brief-template.md` for the final structure. If the user asks only for a narrow audit, use the relevant sections and keep it concise.

Always include an evidence ledger:

- Evidence
- Assumption
- Risk if wrong
- Validation action

Use `examples/sample-output-ai-sales-risk.md` or `examples/sample-output-devtool-analytics.md` only as shape references when the user asks what a good result looks like. Do not copy their conclusions into a new user's brief.

## Maintenance Check

Use `evals/golden-cases.md` after changing the skill to check whether the workflow still handles sparse input, pre-revenue GTM, AI-builder demand illusions, and evidence-heavy GTM audits. These cases are not user-facing templates.

## Quality Gates

Before finalizing, check:

- The recommendation names a specific buyer, user, or segment, not a broad market.
- The market reality verdict is Build, Validate, or Hold, with a reason.
- The brief states what should not be built, scaled, or claimed yet.
- Each recommended channel has a reachability reason.
- Each positioning claim has proof or is marked as a hypothesis.
- Each major assumption has a validation action.
- The output states confidence: high, medium, or low.
- The brief includes clear next actions that can be executed within 14 or 30 days.

## Do Not Do

- Do not use TAM/SAM/SOM as proof of a beachhead.
- Do not polish an idea to make it sound investable when market evidence is weak.
- Do not assume the idea, target user, pain, willingness to pay, or adoption path exists.
- Do not discuss product features unless they directly test demand, adoption, trust, or willingness to pay.
- Do not write a campaign calendar before the GTM motion is justified.
- Do not imply PLG is suitable when the product requires high trust, integration, procurement, or executive approval.
- Do not imply outbound is suitable when pain is weak or the buyer cannot be identified.
- Do not generate generic marketing copy unless it is tied to a positioning hypothesis and validation plan.
- Do not copy playbooks from famous companies as if they fit the user's context.
- Do not be afraid to say: "Hold. Do not build yet."
