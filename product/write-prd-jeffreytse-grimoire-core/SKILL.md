---
name: write-prd
description: Use when a new feature, product, or significant change needs to be defined before engineering begins — including greenfield features, major redesigns, API changes, or cross-team initiatives. Trigger when a problem or opportunity is validated and stakeholders need alignment before scoping work.
source: Google PM spec format, Lenny Rachitsky PRD template (Lenny's Newsletter), productboard best practices, Shreyas Doshi product frameworks
tags: [product, requirements, prd, alignment, user-stories, success-metrics, planning, stakeholders]
verified: true
---

# Write PRD

Write a Product Requirements Document that aligns stakeholders on what to build, why to build it, and how to know when it succeeded — before a line of code is written.

## Why This Is Best Practice

**Adopted by:** Google, Meta, Airbnb, Stripe, Linear, and virtually every product-led company with more than one team. Google's internal "PRD" format is taught in every PM onboarding. Lenny Rachitsky's PRD template (used by 100k+ PMs per his newsletter) synthesizes practices from Meta, Figma, Duolingo, and Notion.

**Impact:** A McKinsey study found that misaligned requirements are the #1 cause of project failure (39% of failed projects). IBM research found that fixing a requirements defect after deployment costs 100× more than fixing it during design. Teams that write PRDs before engineering reduce rework by 30–50% (Productboard 2022 survey of 1,400 PMs).

**Why best:** A PRD externalizes assumptions. Without it, engineers build to their mental model of the feature, designers build to theirs, and the PM means something different entirely. The act of writing forces the PM to answer hard questions — especially around edge cases, success metrics, and out-of-scope decisions — before those questions cost sprint time.

Sources: McKinsey "The business value of design" 2018; IBM Systems Sciences Institute; Lenny Rachitsky, "How to write a good PRD" (Lenny's Newsletter, 2021); Productboard Product Excellence Report 2022.

## Steps

1. **Write the problem statement** (1 paragraph): what user problem are you solving? Who has this problem? What is the cost of not solving it? Do not mention the solution yet.

2. **State the goal and non-goals**: one sentence per goal ("Users can complete checkout without a credit card"). Non-goals are equally important — they define scope boundaries and prevent feature creep. ("This release does not include mobile payment methods.")

3. **Define success metrics** before writing requirements. Use the HEART framework (Happiness, Engagement, Adoption, Retention, Task success) or North Star + guardrail metrics. Make metrics measurable: not "improve checkout conversion" but "increase checkout completion rate from 62% to 70% within 60 days of launch."

4. **Write user stories** in the format: "As a [persona], I want to [action] so that [outcome]." Each story should be independently testable. Group by persona if you have multiple user types.

5. **Define functional requirements** — what the system must do. Use "must" for non-negotiable, "should" for strong preference, "may" for optional. Number each requirement (FR-01, FR-02) for traceability.

6. **Define non-functional requirements**: performance (p99 latency < 300ms), availability (99.9% uptime), security (PII must be encrypted at rest), accessibility (WCAG 2.1 AA compliance).

7. **List open questions** with owners and resolution dates. Unanswered questions do not block publishing — they must be visible so they get resolved before engineering starts.

8. **Write the out-of-scope section** explicitly. If stakeholders ask "what about X?" and the answer is "not in this release," X belongs here with a rationale.

9. **Add a launch plan sketch**: phased rollout, feature flags, rollback plan, customer communication. Even a 3-bullet sketch prevents surprises at launch.

10. **Get sign-off** from engineering lead, design lead, and relevant stakeholders before handing to the team. A PRD without sign-off is a draft.

## Rules

- The problem statement must be written before the solution. If you find yourself describing the solution in sentence one, rewrite.
- Every requirement must trace to a user story or goal. Requirements that don't trace to anything are scope creep.
- Success metrics must be baseline + target + timeframe. "Improve retention" fails all three.
- The PRD is a living document during discovery; it freezes at engineering kickoff. After kickoff, changes require explicit sign-off and version history.
- Length should match complexity. A two-day feature warrants 1 page. A cross-team initiative warrants 5–8 pages. Never pad; never over-compress.

## Examples

**Problem statement (bad):** "We need to build a new onboarding flow with tooltips and a welcome email."

**Problem statement (good):** "42% of new users who sign up never complete their first task (source: Mixpanel, Q3 2023). Exit surveys indicate they don't understand what to do after creating an account. This costs us an estimated $180k/month in lost expansion revenue from users who churn before reaching activation."

**Success metric (bad):** "Users will have a better onboarding experience."

**Success metric (good):** "Increase 7-day activation rate (users who complete ≥1 task) from 58% to 72% within 30 days of launch. Guardrail: do not increase support ticket volume by more than 5%."

**Non-goal (bad):** "Out of scope: mobile."

**Non-goal (good):** "Out of scope: native mobile onboarding (iOS/Android). Web mobile is in scope. Native mobile will be addressed in Q2 after web results are measured."

## Common Mistakes

- **Solution-first writing:** Describing the feature before establishing the problem makes the PRD unfalsifiable — you can't tell if the feature succeeded if you never defined what success looks like.
- **Vanity metrics:** Page views, button clicks, and "engagement" without context are not success metrics. Tie metrics to business outcomes.
- **Skipping non-goals:** Teams will build the things you didn't say were out of scope. Every non-goal you write saves a sprint.
- **No open questions section:** Unresolved questions buried in Slack threads become hidden requirements that surface at launch.
- **Never updated:** PRDs that diverge from what was actually built are worse than useless — they cause confusion during post-launch reviews and incident investigations.
