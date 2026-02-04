---
name: product-prd
description: Generate comprehensive Product Requirements Documents (PRDs) for product managers. Use this skill when users ask to "create a PRD", "write product requirements", "document a feature", or need help structuring product specifications.
---

# PRD Generator

## Overview

Generate comprehensive and well-structured Product Requirements Documents (PRDs) that follow industry best practices. This skill helps product managers create clear and actionable requirements documents that align stakeholders and guide development teams.

## Main Workflow

When a user requests to create a PRD (e.g., "create a PRD for a user authentication feature"), follow this workflow:

### Step 1: Gather Context (Iterative)

Before generating the PRD, collect essential information through an **iterative discovery conversation**. Do not proceed with doubts—ensure full alignment before moving forward.

#### 1.1 Initial Open-Ended Question

Start with a broad question to understand the user's mental model:

```
"Tell me about [feature/product]. What problem does it solve?"
```

Let the user explain in their own words. Listen for implicit assumptions and gaps.

#### 1.2 Active Listening + Synthesis

After the user responds, **rephrase their answer** to confirm understanding:

```
"So [X] is [your interpretation]. Is that correct?"
```

This validates alignment and surfaces misunderstandings early.

#### 1.3 Iterate Until Alignment

Ask follow-up questions based on gaps identified. Continue until you have clarity on:

**Topics to Explore:**

- **Problem statement**: What pain exists today?
- **Target users**: Who experiences this problem?
- **Business goals**: Why does the company care?
- **Success metrics**: How will we know it worked?
- **Timeline/Constraints**: Deadlines or limitations?
- **Out of scope**: What are we explicitly NOT building?

**Do NOT proceed to Step 2 with unresolved questions.**

#### 1.4 Concept Checkpoint

Summarize the agreed definition before continuing:

```
"Before moving on: [feature] solves [problem] for [users] by [approach].
This aligns with [business goal] and success looks like [metric]. Correct?"
```

Wait for explicit confirmation.

#### 1.5 Problem Validation (Optional)

Ask: **"Do you want to validate the problem with evidence before proceeding?"**

- **If yes**: Gather quantitative + qualitative data (see table below)
- **If no**: Proceed to Step 2

### Problem Validation Table (Optional)

If the user opts for problem validation, collect evidence:

| Dimension         | Evidence                 | Source            |
| ----------------- | ------------------------ | ----------------- |
| Pain point        | [description]            | [who reported]    |
| Quantitative data | [metrics/numbers]        | [system/report]   |
| Qualitative data  | [client quotes/feedback] | [interviews/CS]   |
| Urgency driver    | [why now]                | [business reason] |

Use this table to document the problem's validity before investing in the PRD.

---

### Step 1 Examples

**Example A: Concept Refinement Through Iteration**

```
User: "I want a PRD for a notification system"

Claude: "Tell me about this notification system. What problem does it solve?"

User: "Users miss important updates"

Claude: "So users are missing updates that matter to them, and this causes
        [frustration/missed deadlines/lost opportunities]—is that right?"

User: "Yes, specifically they miss payment reminders and get charged late fees"

Claude: "Got it. So the core problem is: users miss payment reminders,
        leading to late fees. The notification system would prevent this.
        Who are these users—all customers or a specific segment?"

User: "Customers with recurring payments"

Claude: "Before moving on: A notification system for customers with recurring
        payments, solving missed payment reminders that cause late fees.
        Success = reduced late fee incidents. Correct?"

User: "Yes"
```

**Example B: Problem Validation Flow**

```
Claude: "Do you want to validate this problem with evidence before proceeding?"

User: "Yes, let's validate"

Claude: "Let's build the validation table:
        - Pain point: What specific complaints have you heard?
        - Quantitative: How many users are affected? What's the late fee rate?
        - Qualitative: Any user quotes or CS tickets about this?
        - Urgency: Why solve this now vs. later?"

User: "30% of recurring customers had at least one late fee last quarter.
       CS gets 50+ tickets/month about this. A customer said 'I'd pay more
       if you just reminded me.' We're losing customers to competitors
       who have this."

Claude: "Strong validation. Here's the evidence summary:

        | Dimension         | Evidence                        | Source       |
        | ----------------- | ------------------------------- | ------------ |
        | Pain point        | Customers missing payment dates | CS tickets   |
        | Quantitative data | 30% late fee rate, 50 tickets/mo| Analytics/CS |
        | Qualitative data  | 'I'd pay more for reminders'    | Customer     |
        | Urgency driver    | Competitor feature gap          | Churn data   |

        Ready to proceed to Step 2?"
```

---

**Note:** If the user provides a detailed brief upfront, you may accelerate through 1.1-1.3, but always confirm with 1.4 (Concept Checkpoint) before proceeding.

### Step 2: Gather Slack Context

Use the Slack MCP integration to search for relevant discussions about the feature or problem across all accessible channels. This enriches the PRD with the team's existing knowledge and decisions.

**Search Strategy:**

1. **Search by feature/product name**: Find discussions mentioning the feature.
2. **Search by problem keywords**: Identify conversations about pain points.
3. **Search by related terms**: Broaden context with related topics.

**What to Look For:**

- Previous discussions about the feature or problem.
- Decisions already made by the team.
- Technical considerations mentioned by engineers.
- User feedback shared in channels.
- Stakeholder concerns or requirements.
- Relevant links/documents shared.

**Slack Search Workflow:**

```
1. Use feature name and keywords from Step 1 to search all accessible channels.
2. Search for keywords related to the problem.
3. To resume your job, search only in these channels by its IDs and explicity to the user that you will search only in these channels:
    - #cancelamentos-e-vergonhas, ID C038XDZ6GLV
    - #problemas, ID C01GWAN9FHP
    - #feedbacks-gabriel, ID C03GV7MFMU5
    - #comitê-de-satisfação, ID C08F5FKD02H
4. Look for recent messages (last 30-90 days) for relevance.
5. Identify key participants in the discussions.
6. Extract insights and link to original messages when relevant.
7. For each possible relevant message to the context, ask the user to confirm its relevance

```

**PRD Integration:**

- Include relevant quotes or references in the PRD.
- Note decisions already made.
- Flag conflicting opinions for resolution.
- Reference key stakeholders identified in the discussions.

**Note:** If no relevant Slack discussions are found, or if Slack access is unavailable, proceed directly to Step 3. This step enriches context but is not mandatory.

### Step 3: Competitive Analysis (Optional)

Ask if user wants competitive analysis. If yes:

1. Identify 2-3 direct competitors in the market
2. WebSearch: "[competitor] + [feature] + features"
3. WebFetch: documentation if available
4. G2/Capterra for feature comparison
5. Create comparison table: Feature | Us | Competitor | Justification
6. Document differentiators + gaps
7. Save reference URLs

**Examples:**

**Public Safety (Hotlist Feature):**
```
Competitors: Mark43, Axon Records, Tyler Technologies
Search: "Mark43 hotlist vehicle alerts features"
Compare: Alert types, integration with CAD, mobile access
```

**SaaS CRM:**
```
Competitors: Salesforce, HubSpot, Pipedrive
Search: "HubSpot CRM pipeline management features"
Compare: Pipeline customization, automation, reporting
```

**Note:** If user declines competitive analysis or it's not relevant for the feature, proceed directly to Step 4.

### Step 4: Generate PRD Structure

Use the standard PRD template in `references/prd_template.md` to create a well-structured document. The PRD should include:

1. **Executive Summary** - High-level overview (2-3 paragraphs).
2. **Problem Statement** - Clear articulation of the problem.
3. **Goals & Objectives** - What we are trying to achieve.
4. **User Personas** - Who we are building for.
5. **User Stories & Requirements** - Detailed functional requirements.
6. **Success Metrics** - KPIs and measurement criteria.
7. **Scope** - What is in and out of scope.
8. **Technical Considerations** - Architecture, dependencies, constraints.
9. **Competitive Analysis** - How competitors solve this (optional).
10. **Design & UX Requirements** - UI/UX considerations.
11. **Timeline & Milestones** - Key dates and phases.
12. **Risks & Mitigation** - Potential issues and solutions.
13. **Dependencies & Assumptions** - What we are relying on.
14. **Open Questions** - Unresolved items.

### Step 5: Create User Stories

For each main requirement, generate user stories using the standard format found in `references/user_story_examples.md` for common patterns and best practices.
For each story, review whether you have the following details following the best practices below.

**DO:**

- Ask for details about the user story.
- Validate if you have enough context to create each one with well-written acceptance criteria.
- Ask the user to check each one before finalizing the story writing.

### Step 6: Define Success Metrics

Use appropriate metrics frameworks based on the product type:

- **AARRR (Pirate Metrics)**: Acquisition, Activation, Retention, Revenue, Referral.
- **HEART Framework**: Happiness, Engagement, Adoption, Retention, Task Success.
- **North Star Metric**: Single key metric representing core value.
- **OKRs**: Objectives and Key Results.

Consult `references/metrics_frameworks.md` for detailed guidance on each framework.

### Step 7: Validate & Review

Optionally run the validation script to ensure PRD completeness:

```bash
scripts/validate_prd.sh <prd_file.md>

```

This checks:

- All required sections are present.
- User stories follow the proper format.
- Success metrics are defined.
- Scope is clearly articulated.
- No placeholder text remains.

## Usage Patterns

### Pattern 1: New Feature PRD

**User Request:** "Create a PRD to add dark mode to our mobile app"

**Execution:**

1. Ask discovery questions about dark mode requirements.
2. Search Slack for existing discussions about dark mode or theming.
3. Generate PRD using the template.
4. Create user stories for:

- Theme switching.
- Preference persistence.
- Synchronization with system level.
- Design tokens updates.

5. Define success metrics (adoption rate, user satisfaction).
6. Identify technical dependencies (design system, platform APIs).

### Pattern 2: Product Improvement PRD

**User Request:** "Write requirements to improve our search functionality"

**Execution:**

1. Gather context on current search limitations.
2. Identify user pain points and desired improvements.
3. Search Slack for discussions about search issues and feedback.
4. Generate PRD focusing on:

- Current state analysis.
- Proposed improvements.
- Impact assessment.

5. Create prioritized user stories.
6. Define before/after metrics.

### Pattern 3: New Product PRD

**User Request:** "I need a PRD for a new analytics dashboard product"

**Execution:**

1. Comprehensive discovery (market analysis, user research).
2. Search Slack for discussions about analytics needs and dashboard requirements.
3. Generate a full PRD with:

- Market opportunity.
- Competitive analysis.
- Product vision.
- MVP scope.
- Go-to-market considerations.

4. Detailed user stories for core features.
5. Phased rollout plan.
6. Success metrics aligned with business goals.

### Pattern 4: Quick PRD / One-Pager

**User Request:** "Create a lightweight PRD for a small bug fix feature"

**Execution:**

1. Generate a simplified PRD focusing on:

- Problem statement.
- Solution approach.
- Acceptance criteria.
- Success metrics.

2. Optionally search Slack for bug reports or related discussions.
3. Skip sections not relevant to a small scope.
4. Keep the document concise (1-2 pages).

## PRD Best Practices

### Writing Quality Requirements

**Good Requirements Are:**

- **Specific**: Clear and unambiguous.
- **Measurable**: Can be verified/tested.
- **Achievable**: Technically feasible.
- **Relevant**: Tied to user/business value.
- **Time-bound**: Have a clear timeline.

**Avoid:**

- Vague language ("fast", "easy", "intuitive").
- Implementation details (let engineers decide how).
- Scope creep (keep core requirements).
- Assumptions without validation.

### User Story Best Practices

**DO:**

- Focus on value to the user, not features.
- Write from the user's perspective.
- Include clear acceptance criteria.
- Keep stories independent and small.
- Use a consistent format.

**DON'T:**

- Write technical implementation details.
- Create dependencies between stories.
- Create very large stories (epics).
- Use internal jargon.
- Skip acceptance criteria.

### Scope Management

**In-Scope Section:**

- List specific features/capabilities included.
- Be explicit and detailed.
- Link to user stories.

**Out-of-Scope Section:**

- Explicitly state what is NOT included.
- Prevents scope creep.
- Manages stakeholder expectations.
- May include "future considerations."

### Success Metrics Guidelines

**Choose Metrics That:**

- Align with business goals.
- Are measurable and trackable.
- Have clear targets/thresholds.
- Include leading and lagging indicators.
- Consider both user and business value.

**Typical Metric Categories:**

- **Adoption**: How many users use the feature?
- **Engagement**: How often do they use it?
- **Satisfaction**: Do users like it?
- **Performance**: Does it work well?
- **Business Impact**: Does it drive business goals?

## Advanced Features

### PRD Templates for Different Contexts

The skill supports different PRD formats:

**Standard PRD** - Full comprehensive document.
**Lean PRD** - Simplified for agile teams.
**One-Pager** - Executive summary format.
**Technical PRD** - Engineering-focused requirements.
**Design PRD** - UX/UI-focused requirements.

Specify the format when requesting: "Create a lean PRD for..." or "Generate a technical PRD for..."

### Design Integration

**Design Requirements Section Should Include:**

- Visual design requirements.
- Interaction patterns.
- Accessibility requirements (WCAG compliance).
- Responsive design considerations.
- Design system components to use.
- User flow diagrams.
- Wireframe/mockup references.

### Technical Considerations Section

**Should Address:**

- **Architecture**: High-level technical approach.
- **Dependencies**: External services, libraries, APIs.
- **Security**: Authentication, authorization, data protection.
- **Performance**: Load times, scalability requirements.
- **Compatibility**: Browser, device, platform support.
- **Data**: Storage, migration, privacy considerations.
- **Integration**: How it fits with existing systems.

### Stakeholder Alignment

**PRD Should Help To:**

- Align cross-functional teams.
- Set clear expectations.
- Enable parallel work streams.
- Facilitate decision making.
- Provide a single source of truth.

**Distribution Checklist:**

- [ ] Engineering reviewed technical feasibility.
- [ ] Design reviewed UX requirements.
- [ ] Product leadership approved scope.
- [ ] Stakeholders understand timeline.
- [ ] Success metrics agreed upon.

## Common PRD Scenarios

### Scenario 1: Customer Feature Request

When creating a PRD based on customer feedback:

1. Document the customer request verbatim.
2. Analyze the underlying problem.
3. Generalize the solution for all users.
4. Validate with product strategy.
5. Scope appropriately (may be smaller or larger than the request).

### Scenario 2: Strategic Initiative

When creating a PRD for a company strategic initiative:

1. Link with company OKRs/goals.
2. Include market analysis.
3. Consider the competitive landscape.
4. Think about multi-phase rollout.
5. Include success criteria aligned with strategy.

### Scenario 3: Technical Debt / Infrastructure

When creating a PRD for technical improvements:

1. Explain the user impact (even if indirect).
2. Document current limitations.
3. Articulate benefits (speed, reliability, maintainability).
4. Include heavy engineering input.
5. Define measurable improvements.

### Scenario 4: Compliance / Regulatory

When creating a PRD for compliance requirements:

1. Reference specific regulations (LGPD, GDPR, etc.).
2. Include legal/compliance review.
3. Deadlines are usually non-negotiable.
4. Focus on minimum viable compliance.
5. Document audit trail requirements.

## Validation & Quality Checks

### Self-Review Checklist

Before finalizing the PRD, check:

- [ ] **Problem is clear**: Anyone can understand what we are solving.
- [ ] **Users are identified**: We know who this is for.
- [ ] **Success is measurable**: We can determine if it worked.
- [ ] **Scope is bounded**: Clear what is in and out.
- [ ] **Requirements are testable**: QA can verify completeness.
- [ ] **Timeline is realistic**: Estimates validated with engineering.
- [ ] **Risks are identified**: We thought about what could go wrong.
- [ ] **Stakeholders aligned**: Key people reviewed and approved.

### Using the Validation Script

```bash
# Basic validation
scripts/validate_prd.sh my_prd.md

# Detailed output with suggestions
scripts/validate_prd.sh my_prd.md --verbose

# Check only specific sections
scripts/validate_prd.sh my_prd.md --sections "user-stories,metrics"

```

## Resources

This skill includes bundled resources:

### scripts/

- **generate_prd.sh** - Interactive PRD generation workflow.
- **validate_prd.sh** - Validates PRD completeness and quality.

### references/

- **prd_template.md** - Standard PRD template structure.
- **user_story_examples.md** - User story patterns and examples.
- **metrics_frameworks.md** - PM metrics guide (AARRR, HEART, OKRs).

## Tips for Product Managers

### Before Writing the PRD

1. **Do your research**: User interviews, data analysis, competitive analysis.
2. **Validate the problem**: Ensure it's worth solving.
3. **Check strategic alignment**: Does this fit our roadmap?
4. **Estimate effort**: Rough T-shirt size with engineering.
5. **Consider alternatives**: Is this the best solution?

### During PRD Creation

1. **Be clear, not clever**: Simple language wins.
2. **Show, don't tell**: Use examples, mockups, diagrams.
3. **Think about edge cases**: What can go wrong?
4. **Prioritize relentlessly**: What is MVP vs. nice-to-have?
5. **Collaborate early**: Don't work in isolation.

### After Completing the PRD

1. **Review with stakeholders**: Get feedback early.
2. **Iterate based on input**: PRDs are living documents.
3. **Present, don't just share**: Walk through the PRD.
4. **Get formal sign-off**: Ensure commitment.
5. **Keep updated**: Adjust as understanding evolves.

## Examples

### Example 1: Mobile Feature PRD

```bash
# User: "Create a PRD to add biometric authentication to our iOS app"

# Assistant will:
# 1. Ask discovery questions about security requirements, personas, existing auth.
# 2. Generate PRD covering:
#    - Problem: Password friction, security concerns.
#    - Solution: Face ID / Touch ID integration.
#    - User stories: Enable biometric, fallback to password, manage settings.
#    - Metrics: Adoption rate, login success rate, support tickets.
#    - Technical: iOS Keychain, LocalAuthentication framework.
#    - Risks: Device compatibility, privacy concerns.
# 3. Output PRD formatted in markdown.

```

### Example 2: Web Platform Improvement

```bash
# User: "Write requirements to improve our checkout flow conversion"

# Assistant will:
# 1. Collect data on current conversion rates and drop-off points.
# 2. Generate PRD including:
#    - Current state analysis with metrics.
#    - Proposed improvements (guest checkout, saved payment, progress indicator).
#    - A/B test plan.
#    - Success metrics: Conversion rate increase, time to checkout.
#    - User stories for each improvement.
# 3. Include phased rollout approach.

```

### Example 3: B2B Product PRD

```bash
# User: "I need a PRD for an admin dashboard for enterprise clients"

# Assistant will:
# 1. Identify B2B specific requirements (multi-tenancy, permissions, reporting).
# 2. Generate comprehensive PRD with:
#    - Enterprise user personas (admin, manager, analyst).
#    - Role-based access control requirements.
#    - Reporting and analytics needs.
#    - Integration requirements (SSO, SCIM).
#    - Success metrics: Client adoption, admin efficiency.
# 3. Include specific enterprise considerations (compliance, SLAs).

```

## Troubleshooting

**Problem: PRD is too long/detailed**

Solution: Create a "Lean PRD" focusing on problem, solution, acceptance criteria, and metrics. Reserve full PRD for larger initiatives.

**Problem: Requirements are too vague**

Solution: Add specific examples, use concrete numbers, include visual references. Replace "fast" with "loads in under 2 seconds."

**Problem: Stakeholders not aligned**

Solution: Share PRD early as a draft, incorporate feedback, present in person, get explicit sign-off before development begins.

**Problem: Scope keeps expanding**

Solution: Use "Out of Scope" section aggressively, create separate PRDs for future phases, tie scope to timeline constraints.

**Problem: Engineers say it's not feasible**

Solution: Involve engineering earlier in the process, be flexible in the solution approach, focus on the problem not the implementation.

## Best Practices Summary

1. **Start with the problem, not the solution.**
2. **Write for your audience** (execs need summary, engineers need details).
3. **Be specific and measurable** (avoid vague language).
4. **Include visuals** (mockups, diagrams, flows).
5. **Define success upfront** (metrics, not features).
6. **Scope aggressively** (MVP mindset).
7. **Collaborate, don't dictate** (get input from all functions).
8. **Keep updated** (PRD is a living document).
9. **Focus on "why" and "what", not "how"** (let engineers solve "how").
10. **Make it scannable** (headers, bullets, summaries).
