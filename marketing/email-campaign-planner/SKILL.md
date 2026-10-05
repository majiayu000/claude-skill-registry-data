---
name: email-campaign-planner
description: "Plan email campaigns and lifecycle sequences — segmentation, cadence, A/B testing."
version: 0.1.0
---

# Email Campaign Planner

Planner skill for designing email marketing campaigns *before* copywriting or implementation.

Use this skill to design campaigns that reach the right audience with the right message at the right time, with clear segmentation, flow logic, compliance, and measurement.

## JTBD (Jobs To Be Done)

### Primary Job
When I know I need an email campaign or lifecycle sequence but I haven't yet decided on audience segmentation, sequence logic, trigger timing, or success metrics,
I want a complete campaign design specification before drafting or building starts,
so I can hand copywriters, designers, and ESP admins a plan that answers their questions without back-and-forth.

### Secondary Jobs
- When I'm building a multi-email sequence and can't decide how many emails to send, what triggers each one, or how to branch on subscriber behavior, I want the flow logic decided upfront, so I can avoid rebuilding the automation mid-launch.
- When a past campaign underperformed and I need to redesign it, I want the segmentation, offer, and cadence rethought from the ground up, so I'm not just editing subject lines while leaving the structural problems in place.

### Job Layers
- Functional: Design a campaign strategy that defines audience segments, sequence flow and trigger logic, subject line approach, CTA specification, A/B test plan, compliance requirements, and measurement framework before any copy is written or automation is built.
- Emotional: Remove the uncertainty of launching a campaign that looks finished but breaks down because nobody agreed on who receives what, when, and why.
- Social: Helps the user give designers, copywriters, and ESP admins a brief specific enough that they can execute without asking clarifying questions.

### This Skill Is For
- A user about to launch a new promotional, nurture, onboarding, or reactivation campaign who needs the strategy locked before copywriting begins.
- A user whose campaign automation is getting complicated — multiple segments, branching flows, behavior-based triggers — and who needs the logic documented before building.
- A user whose previous campaign underperformed and who wants a redesign grounded in segmentation, offer, and measurement decisions rather than just surface edits.

### This Skill Is NOT For
- A user with an existing email campaign or lifecycle sequence who primarily needs a quality verdict; use `email-campaign-critic` instead.
- A user looking for quick ad hoc tips with no real planning or scope-setting problem.

### Paired With
- `email-campaign-critic`: After the email campaign or lifecycle sequence exists, use it to audit the result and surface real risks.
- `brand-voice-guide`: Use this when the unresolved problem is more about setting stable tone and vocabulary rules before campaign drafting.

### Resolution Paths
| User's Situation | What Happens | What They Leave With |
|-----------------|-------------|----------------------|
| Has a campaign goal but no structure | The skill defines audience segments, sequence, trigger logic, and measurement framework | A complete campaign brief the execution team can build from |
| Has a multi-email sequence with unclear branching | The skill maps flow logic, trigger conditions, and timing for each email | A campaign flow diagram with explicit branch conditions |
| Has a failing campaign that needs redesign | The skill rethinks segmentation, offer, and cadence from the ground up | A redesign specification with rationale for each structural change |

### When to Escalate
- If the user already has an implemented or drafted artifact and needs diagnosis first, escalate to `email-campaign-critic`.
- If the user's unresolved problem is primarily about setting stable tone and vocabulary rules before campaign drafting, escalate to `brand-voice-guide`.

## Purpose

Design email campaigns strategically, not reactively:

- **Define the scope**: What type of campaign? What's the business goal? Who's the audience? What's success?
- **Plan segmentation**: Who receives this email? Who's excluded? What content varies per segment?
- **Design the message**: What's the subject line strategy? What's the value proposition? What's the CTA?
- **Architecture the flow**: Single send or multi-email sequence? What triggers each email? What's the branching logic?
- **Plan for deliverability**: What compliance applies (CAN-SPAM, GDPR)? How do we authenticate? How do we measure?
- **Define measurement**: What metrics matter? What's the baseline? What's success?
- **Enable execution**: Produce a specification clear enough that designers, copywriters, and ESP admins can build without ambiguity

This skill produces a detailed campaign design specification that guides creative execution and implementation.

## Use_When

- Planning a new email marketing campaign (promotional, transactional, nurture, onboarding, reactivation)
- Designing multi-email drip sequences or workflows
- Planning segmented campaigns targeting different audience cohorts
- Establishing A/B test strategy before building emails
- Defining campaign flow and automation logic before implementation
- Planning email compliance (CAN-SPAM, GDPR, accessibility) into the design
- Designing measurement framework and success metrics
- Improving email performance by strategic redesign of an existing campaign

## Do_Not_Use_When

- You've already created email copy and want critique (use email-campaign-critic instead)
- You need help writing email copy (use copy-planner for copy-focused strategy)
- You want to design just the subject line (use copy-planner or copywriter)
- You're reviewing an already-sent campaign for performance analysis
- You need a quick, tactical email fix (planner is strategic, not tactical)

## Companion_Skills

- **email-campaign-critic**: Use AFTER designing campaign to review for subject line quality, CTA effectiveness, segmentation gaps, deliverability, and compliance before sending
- **copy-planner**: Use if you need deep body copy strategy (email-campaign-planner focuses on overall campaign architecture; copy-planner dives into message tonality, proof strategy, benefit framing)
- **copy-critic**: Use to review body copy quality after writing
- **content-model-critic**: Use when designing campaign with complex content/personalization requirements

## Steps

1. **Define the campaign scope and goals**: Provide context about:
   - What type of campaign? (Promotional, transactional, newsletter, nurture, onboarding, reactivation, etc.)
   - What's the business goal? (Lead gen, conversion, retention, brand awareness, engagement)
   - Who's the target audience/segment? (New users? Customers? Lapsed subscribers? Specific lifecycle stage?)
   - What success looks like (open rate target, CTR target, conversion rate, unsubscribe ceiling)
   - Any brand voice/tone guidelines?
   - Constraints? (Send platform limitations, frequency caps, timeline, compliance scope)
   - Share baseline metrics if available: last similar campaign open rate, CTR, conversion rate

2. **Share current state (if redesigning existing campaign)**:
   - How is this currently performed? (Baseline metrics: open rate, CTR, conversion)
   - What's working? What's not?
   - What prompted the redesign?
   - Any pain points in current flow or segmentation?

3. **Invoke the email-campaign-planner subagent**: Delegate to subagent with full planning protocol:
   - Segment definitions, exclusions, personalization strategy
   - Subject line and preview text strategy
   - Email layout and copy framework
   - CTA design specification
   - Campaign flow and trigger logic
   - A/B test plan
   - Compliance and deliverability planning
   - Measurement framework

4. **Return planning output**: Present the structured campaign design with:
   - Campaign Brief (goal, audience, metrics, constraints)
   - Audience Segmentation Plan (segments, exclusions, personalization matrix)
   - Subject Line & Preview Text Strategy (with A/B variants)
   - Email Layout Wireframe (section-by-section specification)
   - Body Copy Framework (value prop, proof strategy, reading level)
   - CTA Specification (primary action, copy, placement, visual design)
   - Campaign Flow Diagram (sequence, triggers, branching logic)
   - A/B Test Plan (variables, sample size, success criteria)
   - Compliance Checklist (CAN-SPAM, GDPR, accessibility standards)
   - Deliverability Plan (authentication, warm-up, list hygiene, sending cadence)
   - Measurement Framework (KPIs, baselines, reporting schedule)
   - Implementation Timeline

The plan guides creative execution and implementation. Use email-campaign-critic to review completed email before sending.

## Tool_Usage

When invoking email-campaign-planner:
- Use Read to examine existing campaign performance data, segmentation logic, historical baselines
- Use Grep to analyze subscriber segment sizes, engagement patterns, or campaign history
- Use Bash to calculate sample sizes for A/B tests, analyze historical metrics, extract baseline data
- Understand the business context, audience maturity, and competitive environment thoroughly before designing

## Related_Skills

- **email-campaign-critic**: Post-design review of subject line, copy quality, CTA, segmentation, deliverability, and compliance before sending
- **copy-planner**: When you need deep copy strategy (benefit framing, proof strategy, tone, readability level)
- **copy-critic**: Review body copy quality and voice consistency
- **content-model-critic**: When designing campaign with complex personalization or content requirements
- **marketing-strategy-planner**: If campaign is part of larger marketing funnel or strategy

## Output Checklist

The email-campaign-planner output should include:

- [ ] Campaign Brief (type, goal, audience, success metrics)
- [ ] Audience Segmentation Plan (segment definitions, exclusions, personalization matrix)
- [ ] Subject Line Strategy (hook type, length targets, A/B variants)
- [ ] Preview Text Strategy (complement approach, examples)
- [ ] Email Layout Wireframe (section order, mobile-first responsive, image strategy)
- [ ] Body Copy Framework (value prop, benefits, proof, reading level targets, copy length by section)
- [ ] CTA Specification (primary CTA copy, placement, visual design, secondary CTAs if any)
- [ ] Campaign Flow Diagram (for each email: trigger type (time-based/behavior-based/event-based), send condition, wait/timing, success metric; for branching: specify conditions and variant paths)
- [ ] A/B Test Plan (what's being tested, minimum sample size, success metric, decision rule)
- [ ] Compliance Checklist (filled-in checklist with ✓/✗ for CAN-SPAM items (subject line honesty, physical address, unsubscribe link), GDPR items (if EU audience: consent, opt-out, privacy policy), and Accessibility items (alt text, color contrast, font sizes, reading order, link text clarity))
- [ ] Deliverability Plan (must include: authentication status (SPF/DKIM/DMARC: configured/in-progress/not yet), warm-up strategy if new IP/domain, list hygiene summary, sending cadence)
- [ ] Landing Page Alignment (URL, headline, CTA button text, and verification that landing page delivers on email's promise)
- [ ] Measurement Framework (baseline metrics, KPIs, reporting schedule, analysis questions)
- [ ] Measurement Baseline (historical open rate, CTR, conversion rate for similar campaigns or segments, or explicit note that no baseline exists)
- [ ] Implementation Timeline (ordered phases with estimated duration and dependencies)
- [ ] Contract Appendix (what a designer/copywriter/ESP admin should be able to do with this plan)

## Key Domain Differentiators

Email-campaign-planner is **NOT** copy-planner. Distinctions:

| Element | Email Campaign Planner | Copy Planner |
|---------|------------------------|--------------|
| Subject line | Hook strategy, length, A/B approach | Wordsmithing specific copy |
| Body copy | Framework (value prop, benefits, proof structure), reading level, word count targets | Actual writing, tone refinement, persuasion techniques |
| Segmentation | Segment definitions, exclusions, content variations per segment | Not in scope |
| Campaign flow | Trigger logic, sequence design, branching rules, timing | Not in scope |
| CTA | Specification (copy approach, placement, visual design) | Exact button text wordsmithing |
| Compliance | Planning (what checklist applies) | Not in scope |
| Deliverability | Strategy (warm-up, authentication, cadence) | Not in scope |

Use email-campaign-planner first to design overall strategy. Use copy-planner next if you need deep copy strategy. Use copy-critic to review actual copy after writing.

## Success Criteria

A high-quality email campaign plan enables the execution team to:
1. Understand the goal and target audience without questions
2. Identify exactly which subscribers should receive the email(s) and why
3. Know what content varies per segment
4. Write subject line and copy using the provided framework
5. Design CTA with clarity on copy, placement, and visual treatment
6. Understand the sequence logic and trigger timing
7. Execute A/B tests with correct sample sizes and success metrics
8. Ensure compliance with relevant standards before send
9. Prepare infrastructure for proper authentication and deliverability
10. Measure success with clear baselines and KPIs

If the execution team has questions about any of these after reading the plan, the plan needs improvement.
