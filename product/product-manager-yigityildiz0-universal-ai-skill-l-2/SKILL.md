---
name: product-manager
description: "Product management analysis for engineering-informed decision framing. Use when a task needs product framing, feature prioritization based on user impact and engineering reality, scope control to prevent complexity creep, or structured now/next/later sequencing with explicit tradeoffs. Turkish triggers: ürün kararı, PRD ve önceliklendirme, kullanıcı ve iş hedeflerini dengele."
---

# Product Manager

Structured product management frameworks for engineering teams. This skill provides decision templates, prioritization models, and planning tools that connect user outcomes to engineering execution.

## When to Use This Skill

Use this skill for:

- Defining what to build and why before starting implementation
- Prioritizing features when resources are constrained
- Scoping MVPs to avoid complexity creep
- Writing clear requirements and acceptance criteria
- Aligning stakeholders on sequencing and tradeoffs
- Planning launches with measurable success criteria
- Framing engineering decisions in terms of user impact

**Trigger phrases**: "product framing", "prioritize features", "scope the MVP", "what should we build", "user story", "acceptance criteria", "roadmap", "now next later", "RICE score", "feature priority", "launch plan", "stakeholder alignment"

## What This Skill Does

Provides a seven-step product management workflow that translates user problems into engineering plans with clear scope, explicit tradeoffs, and measurable outcomes.

### Overview

1. **Problem Discovery** - Map user problems to measurable outcomes
2. **Scope Definition** - Draw boundaries and detect scope creep
3. **Prioritization** - Score and rank work using structured frameworks
4. **Requirements** - Write testable acceptance criteria
5. **Stakeholder Alignment** - Clarify ownership and communication
6. **Roadmap and Sequencing** - Order work with dependency awareness
7. **Launch and Validation** - Ship with confidence and measure results

## Instructions

### Step 1: Problem Discovery and User Outcome Mapping

Before building anything, establish a shared understanding of the user problem. Every feature should trace back to a user outcome, not a stakeholder request or a technical preference.

**User Problem Statement Template**:

```
PROBLEM STATEMENT
─────────────────
Who:        [Target user persona or segment]
Situation:  [Context in which the problem arises]
Problem:    [What the user cannot do, or what causes friction]
Impact:     [Consequence of the problem remaining unsolved]
Evidence:   [Data, quotes, support tickets, or observations]
```

**Jobs-to-Be-Done (JTBD) Framework**:

Frame every feature request as a job the user is trying to accomplish. This prevents solution-first thinking.

```
When [situation], I want to [motivation], so I can [expected outcome].
```

Examples:
- When I receive a failing CI notification, I want to see the exact error with file and line, so I can fix it without re-reading the entire log.
- When I onboard to a new codebase, I want a map of the architecture and key entry points, so I can start contributing within a day.

**Outcome vs Output Distinction**:

| Dimension | Output (avoid as goal) | Outcome (target this) |
|-----------|----------------------|---------------------|
| Definition | A deliverable or artifact | A change in user behavior or metric |
| Example | "Ship search feature" | "Users find relevant results in under 3 seconds" |
| Measurable by | Completion (done/not done) | Metric movement (before/after) |
| Risk | Shipping something nobody uses | Slower to define but validates real value |

**Success Metrics Definition**:

For each problem, define metrics before writing code:

```
SUCCESS METRICS
───────────────
Primary metric:    [The single number that proves the problem is solved]
Leading indicator: [Early signal that correlates with the primary metric]
Guardrail metric:  [What must NOT degrade as a side effect]
Measurement plan:  [How and when each metric will be collected]
Target:            [Specific threshold that defines success]
Timeline:          [When you expect to see movement]
```

**Discovery Checklist**:

- [ ] Problem is stated from the user's perspective, not the team's
- [ ] At least one JTBD statement is written
- [ ] Success metric is defined with a numeric target
- [ ] Guardrail metric is identified (what should not break)
- [ ] Evidence exists (not just intuition) to support the problem's importance
- [ ] The outcome is distinct from the output

### Step 2: Scope Definition and Boundary Setting

Scope creep is the primary reason engineering projects miss deadlines. Define explicit boundaries before implementation begins.

**MVP Scoping Framework**:

An MVP is not a bad version of the full product. It is the smallest thing that tests whether the core assumption is true.

```
MVP DEFINITION
──────────────
Core assumption:  [What belief must be validated?]
Minimum to test:  [Smallest feature set that validates the assumption]
Not included:     [Features explicitly deferred]
Success signal:   [What result proves the assumption correct?]
Failure signal:   [What result disproves it?]
Time box:         [Maximum calendar time for this MVP]
```

**In/Out Table**:

Use this table at the start of every project to create an explicit contract about scope.

```
SCOPE TABLE: [Feature Name]
────────────────────────────
IN SCOPE                          | OUT OF SCOPE (this release)
──────────────────────────────────|────────────────────────────
[Feature A]                       | [Feature X - deferred to v2]
[Feature B]                       | [Feature Y - nice to have]
[Feature C]                       | [Feature Z - separate initiative]
```

Rules for the In/Out table:
- Every item in "Out of Scope" must have a reason (deferred, separate initiative, not validated, too expensive)
- The table is a living document; changes require explicit stakeholder acknowledgment
- If an "Out" item moves "In", something else must move "Out" or the timeline extends

**Scope Creep Detection Signals**:

Watch for these patterns during implementation:

| Signal | Example | Response |
|--------|---------|----------|
| "While we're at it" | "While we're adding search, let's add filters too" | Add to backlog, evaluate separately |
| "It's just a small change" | "Can we also handle edge case X?" | Estimate cost, compare to deadline |
| "Users will expect" | "Users will expect dark mode" | Validate with data, not assumptions |
| "We should future-proof" | "Let's make it configurable for all cases" | Build for current need, refactor later |
| Expanding personas | "What about admin users too?" | Scope to primary persona first |

**Ship Now vs Later Decision Framework**:

When debating whether to include something in the current release:

```
SHIP-NOW-OR-LATER DECISION
───────────────────────────
Feature: [Name]

                          YES    NO
Blocks the core use case?  [ ]   [ ]
Affects >50% of users?     [ ]   [ ]
Costs <2 days to build?    [ ]   [ ]
Hard to add retroactively? [ ]   [ ]
Required for compliance?   [ ]   [ ]

Score: [count of YES answers]
- 4-5 YES: Ship now
- 2-3 YES: Discuss with team, lean toward now if time permits
- 0-1 YES: Ship later
```

### Step 3: Prioritization Frameworks

Use structured scoring to replace opinion-based prioritization. Choose the framework that fits your team's maturity and data availability.

**RICE Scoring**:

Best for teams with usage data and medium-to-large backlogs.

```
RICE SCORE = (Reach x Impact x Confidence) / Effort

Reach:      Number of users affected per quarter (use real data)
Impact:     0.25 (minimal), 0.5 (low), 1 (medium), 2 (high), 3 (massive)
Confidence: 100% (high), 80% (medium), 50% (low) - be honest
Effort:     Person-weeks (round up, include testing and review)
```

| Feature | Reach | Impact | Confidence | Effort | RICE Score |
|---------|-------|--------|------------|--------|------------|
| Example A | 5000 | 2 | 80% | 3 | 2667 |
| Example B | 1000 | 3 | 50% | 1 | 1500 |
| Example C | 8000 | 0.5 | 100% | 2 | 2000 |

**ICE Scoring**:

Simpler alternative when you lack precise reach data. Good for early-stage products.

```
ICE SCORE = Impact x Confidence x Ease

Impact:     1-10 (how much will this move the target metric?)
Confidence: 1-10 (how sure are we about impact and feasibility?)
Ease:       1-10 (how easy is this to implement? 10 = trivial)
```

**Impact/Effort Matrix**:

Visual tool for quick triage of a small number of items (under 20).

```
         HIGH IMPACT
              |
  Quick Wins  |  Strategic Bets
  (do first)  |  (plan carefully)
              |
─────────────+──────────────
              |
  Fill-ins    |  Avoid
  (do if idle)|  (deprioritize)
              |
         LOW IMPACT

X-axis: Effort (left = low, right = high)
Y-axis: Impact (bottom = low, top = high)
```

**MoSCoW Method**:

Best for fixed-deadline projects where scope is the variable.

```
MOSCOW CLASSIFICATION: [Release Name]
──────────────────────────────────────
MUST HAVE    (release fails without these)
- [Feature A]
- [Feature B]

SHOULD HAVE  (important but workarounds exist)
- [Feature C]
- [Feature D]

COULD HAVE   (nice-to-have, include if time permits)
- [Feature E]

WON'T HAVE   (explicitly excluded this release)
- [Feature F] - reason: [deferred to Q3]
```

**Weighted Scoring with Engineering Constraints**:

When engineering reality must factor into prioritization alongside business value:

```
WEIGHTED PRIORITY SCORE
───────────────────────
                        Weight    Feature A    Feature B    Feature C
User impact             30%       8            6            9
Revenue potential       20%       7            9            5
Engineering complexity  20%       3 (inverse)  7 (inverse)  4 (inverse)
Strategic alignment     15%       9            5            8
Technical debt payoff   15%       2            8            6
────────────────────────────────────────────────────────────────────
Weighted score                    5.75         6.90         6.35
```

Note: For engineering complexity, invert the score (10 = trivial, 1 = extremely complex) so that easier items score higher.

### Step 4: Requirements and Acceptance Criteria

Ambiguous requirements cause rework. Write requirements that an engineer can implement and a tester can verify without asking follow-up questions.

**User Story Format**:

```
As a [user persona],
I want to [action or capability],
so that [benefit or outcome].
```

Rules for good user stories:
- The persona is specific (not "a user" but "a developer on a team of 5+")
- The action is observable (the user does something, the system responds)
- The benefit maps to a real outcome, not a feature description
- If the story cannot fit on an index card, it needs splitting

**Acceptance Criteria Template**:

Write acceptance criteria using the Given/When/Then format. Each criterion must be independently testable.

```
ACCEPTANCE CRITERIA: [Story Title]
───────────────────────────────────

AC-1: [Short descriptive name]
  Given [precondition or initial state]
  When  [action performed by the user or system]
  Then  [expected observable result]

AC-2: [Short descriptive name]
  Given [precondition]
  When  [action]
  Then  [result]

AC-3: [Error case]
  Given [precondition]
  When  [invalid action or error trigger]
  Then  [system handles gracefully: error message, fallback, etc.]
```

**Testable Criteria Checklist**:

Every acceptance criterion must pass these checks:

- [ ] Binary: Can be verified as pass or fail with no ambiguity
- [ ] Independent: Does not depend on other criteria being tested first
- [ ] Specific: Includes concrete values, thresholds, or states (not "fast" but "under 200ms")
- [ ] Complete: Covers the happy path, at least one error path, and boundary conditions

**Edge Case Identification Template**:

Use this matrix to systematically find edge cases before implementation:

```
EDGE CASE MATRIX: [Feature Name]
─────────────────────────────────
Category          | Edge Case                    | Expected Behavior
──────────────────|─────────────────────────────|──────────────────
Empty input       | User submits blank form      | Validation error shown
Boundary values   | Input at max length          | Accepted; truncation warning
Concurrent access | Two users edit same record   | Last-write-wins with conflict notice
Permission denied | User lacks required role     | 403 with explanation
Network failure   | API timeout during save      | Retry with user notification
Data migration    | Legacy records missing field | Default value applied
Scale             | 10x expected volume          | Degrades gracefully, no crash
```

**Non-Functional Requirements (NFRs)**:

NFRs are often discovered during production incidents. Define them upfront.

```
NON-FUNCTIONAL REQUIREMENTS: [Feature Name]
────────────────────────────────────────────
Category        | Requirement                           | Measurement
────────────────|───────────────────────────────────────|────────────
Performance     | Page loads in <2s at P95               | Lighthouse, APM
Availability    | 99.9% uptime during business hours     | Uptime monitor
Security        | All inputs validated server-side        | Security audit
Accessibility   | WCAG 2.1 AA compliance                 | axe-core scan
Scalability     | Supports 10x current user count         | Load test
Data retention  | User data deletable within 30 days      | Compliance audit
Observability   | Errors logged with correlation ID        | Log search
```

### Steps 5–7: Stakeholder Alignment, Roadmap, Launch
Read [references/stakeholder-roadmap-launch.md](references/stakeholder-roadmap-launch.md) when the task reaches stakeholder alignment, roadmap sequencing, launch planning, or post-launch validation.

## Quick Reference: Framework Selection Guide

Not sure which framework to use? Start here.

| Situation | Recommended Framework | Step |
|-----------|----------------------|------|
| "What problem are we solving?" | JTBD + Problem Statement | Step 1 |
| "Is this in scope?" | In/Out Table | Step 2 |
| "What should we build first?" | RICE (data-rich) or ICE (early stage) | Step 3 |
| "When is this done?" | Acceptance Criteria (Given/When/Then) | Step 4 |
| "Who decides?" | RACI Matrix | Step 5 |
| "What order?" | Now/Next/Later + Dependency Map | Step 6 |
| "Are we ready to ship?" | Launch Checklist + Rollout Plan | Step 7 |

## Common Mistakes to Avoid

### Mistake 1: Solution-First Thinking
```
Bad:  "We need to add a Kafka queue for real-time updates"
Good: "Users need to see changes within 5 seconds. What's the simplest way?"
```

### Mistake 2: Scope as a Feature List
```
Bad:  In scope: search, filters, sorting, pagination, saved searches, export
Good: In scope: search + filters (validates core use case)
      Out of scope: sorting, pagination, saved searches, export (v2)
```

### Mistake 3: Vague Acceptance Criteria
```
Bad:  "The page should load quickly"
Good: "Given a user on a 4G connection, when the page loads, then first contentful paint is under 1.5 seconds"
```

### Mistake 4: No Guardrail Metrics
```
Bad:  "Success = 20% increase in signups"
Good: "Success = 20% increase in signups AND no decrease in 30-day retention"
```

### Mistake 5: Roadmap as a Promise
```
Bad:  "Q3: Feature X, Q4: Feature Y" (treated as deadline commitments)
Good: "Now: Feature X (committed). Next: Feature Y (high confidence). Later: Feature Z (directional)."
```

## Quality Checklist

- [ ] User problem is stated from the user's perspective with evidence
- [ ] Scope has an explicit In/Out table reviewed by the team
- [ ] Features are prioritized with a structured framework (not opinions)
- [ ] Acceptance criteria are written in Given/When/Then format
- [ ] Every criterion is independently testable and binary
- [ ] RACI matrix has exactly one accountable person per row
- [ ] Decision log captures key decisions with context and rationale
- [ ] Roadmap uses Now/Next/Later, not fixed quarterly dates
- [ ] Launch checklist is complete before rollout begins
- [ ] Post-launch review is scheduled before launch happens

## Related Skills

- `plan-before-code` - Engineering planning and exploration before implementation
- `test-driven-development` - Writing tests from acceptance criteria
- `code-quality` - Ensuring implementation meets non-functional requirements
- `context-analysis` - Deep analysis of existing systems before feature design

---

**Version**: 1.0.0
**Last Updated**: March 2026


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets are not met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
