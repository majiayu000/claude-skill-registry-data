---
name: product-manager
description: Product management analysis for engineering-informed decision framing. Use when a task needs product framing, feature prioritization based on user impact.
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

### Step 5: Stakeholder Alignment

Misalignment between stakeholders causes more project delays than technical complexity. Use explicit frameworks to prevent ambiguity about who decides what.

**RACI Matrix**:

Define roles for every major decision and deliverable.

```
RACI MATRIX: [Project Name]
───────────────────────────
                    PM    Eng Lead   Designer   QA    Exec
Scope decisions     A     C          C          I     I
Technical approach  C     A          I          C     I
UX design           C     C          A          C     I
Release timing      A     R          I          C     I
Quality sign-off    C     C          I          A     I
Go/no-go decision   R     C          I          C     A

R = Responsible (does the work)
A = Accountable (makes the final call)
C = Consulted (provides input before decision)
I = Informed (notified after decision)
```

Rules:
- Every row has exactly one "A"
- "A" and "R" can be the same person but not always
- If a row has more than two "C" entries, the decision process will be slow; consider reducing

**Decision Log Template**:

Record every significant decision to prevent re-litigation.

```
DECISION LOG
────────────
ID:          DEC-001
Date:        [YYYY-MM-DD]
Decision:    [What was decided]
Context:     [Why this decision was needed]
Options:     [Options considered with brief pros/cons]
Chosen:      [Which option and why]
Decided by:  [Name and role]
Reversible:  [Yes/No - and what would trigger reversal]
```

**Cross-Functional Dependency Map**:

```
DEPENDENCY MAP: [Project Name]
──────────────────────────────
Deliverable          | Depends On              | Owner       | Status    | Risk
─────────────────────|─────────────────────────|─────────────|───────────|──────
API endpoint         | Schema design           | Backend     | Done      | Low
Frontend integration | API endpoint            | Frontend    | Blocked   | High
Load testing         | Staging environment      | DevOps      | In progress| Med
Documentation        | API endpoint + UX final  | Tech Writer | Not started| Low
```

**Communication Cadence**:

```
COMMUNICATION PLAN: [Project Name]
───────────────────────────────────
Audience        | Channel     | Frequency    | Content                    | Owner
────────────────|─────────────|──────────────|────────────────────────────|──────
Core team       | Standup     | Daily        | Blockers, progress         | Eng Lead
Stakeholders    | Status email| Weekly       | Milestones, risks, asks    | PM
Leadership      | Slide deck  | Biweekly     | KPIs, timeline, decisions  | PM
Customers       | Changelog   | At launch    | What's new, migration notes| PM
```

**Escalation Paths**:

```
ESCALATION FRAMEWORK
────────────────────
Level 1: Team-level (Eng Lead resolves within 1 business day)
  Triggers: Blocked tasks, minor scope questions, technical disagreements

Level 2: Cross-team (PM + Eng Lead + counterpart, resolve within 2 days)
  Triggers: Dependency delays, resource conflicts, scope changes >2 days

Level 3: Leadership (Director/VP, resolve within 3 days)
  Triggers: Timeline at risk, budget overrun, strategic pivot needed

Rule: Every escalation includes a written summary of the problem, options considered, and a recommended path forward. Never escalate without a recommendation.
```

### Step 6: Roadmap and Sequencing

A roadmap is a communication tool, not a commitment to exact dates. Use time horizons and dependency awareness to create realistic plans.

**Now/Next/Later Framework**:

```
ROADMAP: [Product Area]
───────────────────────

NOW (current sprint/iteration, committed)
  - [Feature A] - solves [problem], measured by [metric]
  - [Feature B] - prerequisite for [Feature D]

NEXT (1-2 sprints out, high confidence)
  - [Feature C] - depends on [Feature A] completion
  - [Feature D] - validated by [research/data]

LATER (3+ sprints, directional, subject to change)
  - [Feature E] - pending validation of [assumption]
  - [Feature F] - blocked by [external dependency]

WILL NOT DO (explicitly rejected)
  - [Feature G] - reason: [low impact, high cost]
```

Rules for the Now/Next/Later roadmap:
- "Now" items have acceptance criteria and an owner
- "Next" items have a problem statement and rough scope
- "Later" items have a hypothesis and a trigger condition for promotion
- Items move between columns only through explicit discussion, never silently

**Dependency-Aware Sequencing**:

```
SEQUENCING PLAN
───────────────
Phase 1 (Week 1-2): Foundation
  [Task A] ──→ [Task B] ──→ [Task C]
                  │
                  ▼
Phase 2 (Week 3-4): Core Features
  [Task D] ──→ [Task E]
  [Task F] (parallel, no dependencies)

Phase 3 (Week 5): Integration and Polish
  [Task G] (requires Task E + Task F)
  [Task H] (requires Task C)

Critical path: A → B → D → E → G
Float tasks (can slip without affecting deadline): F, H
```

**Milestone Definition**:

```
MILESTONE TEMPLATE
──────────────────
Name:           [M1: Core API Complete]
Target date:    [YYYY-MM-DD]
Definition:     [All CRUD endpoints deployed to staging with passing tests]
Deliverables:   [List of specific artifacts]
Exit criteria:  [What must be true to declare this milestone done]
Dependencies:   [What must be complete before this milestone starts]
Risk:           [Primary risk and mitigation]
```

**Risk-Adjusted Timeline**:

Add buffers based on uncertainty, not optimism.

```
TIMELINE ESTIMATION
───────────────────
Task              | Best Case | Likely | Worst Case | Risk-Adjusted
──────────────────|───────────|────────|────────────|──────────────
Task A            | 2d        | 3d     | 5d         | 3.5d
Task B            | 1d        | 2d     | 4d         | 2.5d
Task C            | 3d        | 5d     | 10d        | 6d
Integration       | 1d        | 2d     | 5d         | 3d
──────────────────|───────────|────────|────────────|──────────────
Total             | 7d        | 12d    | 24d        | 15d

Risk-Adjusted = (Best + 4*Likely + Worst) / 6  (PERT estimate)

Buffer policy: Add 20% to the risk-adjusted total for unknowns.
Communicate the risk-adjusted estimate externally, not the best case.
```

**Feature Flagging Strategy**:

Decouple deployment from release to reduce launch risk.

```
FEATURE FLAG PLAN: [Feature Name]
─────────────────────────────────
Flag name:          [feature-name-enabled]
Default state:      OFF
Rollout stages:
  1. Internal team only (dogfooding)          - 1 week
  2. 5% of users (canary)                     - 3 days
  3. 25% of users (early adopter ring)        - 1 week
  4. 100% of users (general availability)     - permanent
Rollback trigger:   [Error rate >1% or P95 latency >500ms]
Flag removal:       [Remove flag and dead code within 30 days of GA]
Owner:              [Name]
```

### Step 7: Launch and Validation

Launching is not the finish line. It is the start of validation. Plan for measurement, iteration, and (if needed) rollback.

**Launch Checklist**:

```
PRE-LAUNCH CHECKLIST: [Feature Name]
─────────────────────────────────────
Category          | Item                                    | Status
──────────────────|─────────────────────────────────────────|───────
Engineering       | All acceptance criteria passing          | [ ]
Engineering       | Load test completed at 2x expected load  | [ ]
Engineering       | Feature flag tested (on/off/rollback)    | [ ]
Engineering       | Monitoring and alerts configured          | [ ]
Engineering       | Runbook written for on-call team          | [ ]
Quality           | QA sign-off on staging                    | [ ]
Quality           | Accessibility audit passed                | [ ]
Quality           | Security review completed                 | [ ]
Documentation     | User-facing docs updated                  | [ ]
Documentation     | Internal knowledge base updated           | [ ]
Documentation     | API changelog entry written               | [ ]
Communication     | Release notes drafted                     | [ ]
Communication     | Support team briefed                      | [ ]
Communication     | Stakeholders notified of launch date      | [ ]
Rollback          | Rollback plan documented and tested       | [ ]
Rollback          | Data migration reversal verified          | [ ]
```

**Feature Flag Rollout Plan**:

```
ROLLOUT SCHEDULE: [Feature Name]
────────────────────────────────
Stage    | Audience         | Duration | Success Gate            | Rollback Gate
─────────|──────────────────|──────────|─────────────────────────|──────────────
Canary   | Internal team    | 3 days   | No P0/P1 bugs           | Any P0 bug
Ring 1   | 5% of users      | 5 days   | Error rate <0.5%         | Error rate >2%
Ring 2   | 25% of users     | 5 days   | P95 latency <300ms       | P95 >800ms
Ring 3   | 50% of users     | 3 days   | NPS/CSAT stable          | NPS drop >5pts
GA       | 100% of users    | Permanent| Metric targets met       | Exec decision
```

**A/B Test Design**:

When validating a feature with an experiment:

```
A/B TEST PLAN: [Experiment Name]
────────────────────────────────
Hypothesis:      [Changing X will improve Y by Z%]
Primary metric:  [Conversion rate, engagement, retention, etc.]
Guardrail metrics: [Metrics that must not degrade]
Control group:   [Current experience, 50% of traffic]
Treatment group: [New feature enabled, 50% of traffic]
Sample size:     [Minimum users needed for statistical significance]
Duration:        [Minimum runtime, typically 2-4 weeks]
Significance:    [p < 0.05 or 95% confidence interval]
Decision rule:   [Ship if primary metric improves >X% with significance]
Owner:           [Name]
```

**Success Metric Dashboard**:

Define what to monitor post-launch and where to find it.

```
POST-LAUNCH DASHBOARD: [Feature Name]
──────────────────────────────────────
Metric                | Source        | Baseline | Target  | Alert Threshold
──────────────────────|──────────────|──────────|─────────|────────────────
Adoption rate         | Analytics    | 0%       | 30%/30d | <10% at day 14
Error rate            | APM          | 0.1%     | <0.5%   | >1%
P95 response time     | APM          | 150ms    | <300ms  | >500ms
User satisfaction     | Survey/NPS   | N/A      | >4.0/5  | <3.0
Support ticket volume | Help desk    | 5/week   | <10/week| >20/week
```

**Post-Launch Review Template**:

Conduct a review 2-4 weeks after launch.

```
POST-LAUNCH REVIEW: [Feature Name]
───────────────────────────────────
Date:           [YYYY-MM-DD]
Participants:   [Names and roles]

1. RESULTS
   - Primary metric: [Target] vs [Actual]
   - Secondary metrics: [Summary]
   - Unexpected findings: [Any surprises]

2. WHAT WENT WELL
   - [Item 1]
   - [Item 2]

3. WHAT COULD IMPROVE
   - [Item 1 with specific action]
   - [Item 2 with specific action]

4. FOLLOW-UP ACTIONS
   | Action                    | Owner      | Due Date   |
   |---------------------------|------------|------------|
   | [Action 1]                | [Name]     | [Date]     |
   | [Action 2]                | [Name]     | [Date]     |

5. DECISION
   - [ ] Keep as-is (metrics met)
   - [ ] Iterate (metrics partially met, specific improvements identified)
   - [ ] Roll back (metrics not met, user impact negative)
   - [ ] Expand (metrics exceeded, roll out to additional segments)
```

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
