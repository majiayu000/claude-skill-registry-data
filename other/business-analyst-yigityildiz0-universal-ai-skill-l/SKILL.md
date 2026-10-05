---
name: business-analyst
description: Business analysis expertise for translating business needs into technical requirements. Use when eliciting requirements from stakeholders, modeling business.
---

# Business Analyst

Structured business analysis frameworks for bridging the gap between stakeholders and engineering teams. This skill provides templates, modeling techniques, and communication tools that translate business needs into actionable technical requirements.

## When to Use This Skill

Use this skill for:

- Eliciting and documenting requirements from stakeholders
- Modeling business processes to identify inefficiencies and automation opportunities
- Writing functional specifications that engineers can implement without ambiguity
- Analyzing data structures and defining data dictionaries for new systems
- Performing gap analysis between current capabilities and desired future state
- Creating acceptance criteria and test scenarios from business rules
- Managing stakeholder communication throughout the requirements lifecycle

**Trigger phrases**: "requirements gathering", "business process", "functional spec", "gap analysis", "data dictionary", "acceptance criteria", "stakeholder interview", "use case", "BPMN", "as-is to-be", "swimlane diagram", "traceability matrix", "UAT plan", "requirements sign-off", "change request"

## What This Skill Does

Provides a seven-step business analysis workflow that moves from stakeholder discovery through requirements documentation, process modeling, data analysis, gap identification, acceptance testing, and structured communication.

### Overview

1. **Requirements Elicitation** - Discover and capture stakeholder needs using structured techniques
2. **Business Process Modeling** - Map current and target processes with standard notation
3. **Functional Specification Writing** - Document testable requirements with traceability
4. **Data Analysis and Modeling** - Define entities, relationships, and data quality rules
5. **Gap Analysis** - Assess current state, define target state, and identify gaps
6. **Acceptance Criteria and Testing** - Extract business rules into verifiable test scenarios
7. **Stakeholder Communication** - Report status, manage changes, and secure sign-off

## Instructions

### Step 1: Requirements Elicitation

Requirements elicitation is the foundation of every successful project. Use multiple techniques to triangulate the true need, because stakeholders often describe solutions rather than problems.

**Stakeholder Map**:

```
STAKEHOLDER MAP
───────────────
ID    Name/Role          Interest   Influence   Engagement Strategy
────  ─────────────────  ─────────  ──────────  ──────────────────────────────
S-01  [Name, Title]      High       High        Manage closely (1:1 sessions)
S-02  [Name, Title]      High       Low         Keep informed (weekly updates)
S-03  [Name, Title]      Low        High        Keep satisfied (approval gates)
S-04  [Name, Title]      Low        Low         Monitor (include in broadcasts)
```

**Interview Guide**:

```
INTERVIEW GUIDE
───────────────
Stakeholder:    [Name, Role]
Objective:      [What you need to learn]

CONTEXT (10 min)
- Describe your role in this process from start to finish.
- What are the biggest pain points you face today?
- Walk me through a typical day involving [process/system].

SPECIFICS (20 min)
- What information do you need to complete [task]?
- What decisions do you make, and what data drives them?
- What happens when [exception/error scenario] occurs?

VALIDATION (10 min)
- If we solved [stated problem], what would change for you?
- What would success look like in 6 months?
- Is there anything I have not asked that you expected me to?
```

**Workshop Facilitation**: For cross-functional requirements, run a 2-4 hour session (max 8-10 participants) with this agenda: context setting (15 min), current state walkthrough (30 min), pain point identification via silent brainstorm and dot voting (40 min), future state visioning (30 min), requirements extraction (30 min), wrap-up with action items (15 min). Assign a dedicated facilitator and scribe.

**Observation**: Watch users perform tasks and log each step with the tool used, time taken, and pain points observed. This reveals requirements stakeholders cannot articulate because the behavior is habitual.

**Survey Design**: Use surveys to validate requirements across a large user population after interviews identify themes. Include Likert scales for satisfaction, multiple choice for preferences, and limit open text to 2-3 questions.

**Elicitation Output**:

```
ELICITATION SUMMARY
───────────────────
Session type:   [Interview / Workshop / Observation / Survey]
Date:           [YYYY-MM-DD]
Participants:   [Names]

REQUIREMENTS IDENTIFIED
ID       Type          Description                              Priority   Source
───────  ────────────  ───────────────────────────────────────  ─────────  ──────
REQ-001  Functional    [System shall do X when Y occurs]        High       S-01
REQ-002  Non-functional[Response time under 3 seconds]          High       S-02

OPEN QUESTIONS: [Items needing follow-up]
CONFLICTS: [Disagreements requiring resolution by DATE]
```

### Step 2: Business Process Modeling

Process models make invisible workflows visible, exposing bottlenecks, redundant steps, and handoff failures.

**BPMN Quick Reference**: Events (circles: start, end, intermediate), Activities (rounded rectangles: tasks, subprocesses), Gateways (diamonds: XOR for exclusive, AND for parallel, OR for inclusive), Flows (solid arrows for sequence, dashed for messages), Swimlanes (pools for organizations, lanes for roles).

**As-Is Process Map**:

```
AS-IS PROCESS: [Process Name]
─────────────────────────────
Process owner: [Name]     Scope: [Start trigger] to [End state]

SWIMLANE DIAGRAM
Lane: [Role A]  | [Task 1] ──> [Task 2] ──> <Decision?> ──> [Task 3]
                |                              │ No
Lane: [Role B]  |                              ▼
                |                         [Task 4] ──> [Task 5]

METRICS: Cycle time [X days], Handoffs [N], Manual steps [N/total], Error rate [X%]
```

**To-Be Process and Improvement Log**:

```
IMPROVEMENT LOG: [Process Name]
───────────────────────────────
#   Current Step           Change                  Rationale                Expected Impact
──  ─────────────────────  ──────────────────────  ───────────────────────  ──────────────
1   Manual data entry      Automate via API        Eliminates errors        -80% error rate
2   Email approval loop    In-app approval queue   Reduces wait time        -2 days cycle time
3   Separate reporting     Real-time dashboard     Single source of truth   -4 hrs/week manual
```

**Decision Table**:

```
DECISION TABLE: [Business Rule Name]
────────────────────────────────────
Conditions                     | Rule 1  Rule 2  Rule 3  Rule 4
───────────────────────────────|────────────────────────────────
Order value > $10,000          | Y       Y       N       N
Customer tier = Premium        | Y       N       Y       N
───────────────────────────────|────────────────────────────────
Apply 15% discount             | X       -       -       -
Apply 10% discount             | -       X       X       -
Apply standard pricing         | -       -       -       X
```

**Process Improvement Checklist**: For each step ask: Can it be eliminated? Automated? Combined with adjacent steps? Does the handoff add value? Is the approval a legacy control? Does the step exist only because of a system limitation? Does it introduce delay longer than the work itself?

### Step 3: Functional Specification Writing

Ambiguous specifications are the single largest source of defects. Write requirements that an engineer can implement and a tester can verify without asking follow-up questions.

**Use Case Format**:

```
USE CASE: [UC-001] [Name]
─────────────────────────
Actor: [Role]    Goal: [What the actor accomplishes]    Trigger: [Initiating event]
Preconditions:  [What must be true before]
Postconditions: [What is true after success]

MAIN SCENARIO
1. [Actor does X]  2. [System responds Y]  3. [Actor provides Z]  4. [System confirms]

EXTENSIONS
3a. Validation fails → System displays error → Actor corrects, return to 3
4a. External service unavailable → System queues for retry → Notifies actor

BUSINESS RULES: BR-01 [rule], BR-02 [rule]
FREQUENCY: [X times per day/week]
```

**User Story Decomposition**: Split epics using these strategies: by workflow step (each step becomes a story), by data variation (simple type vs complex type), by business rule (standard rule vs exception). Ensure each resulting story can be completed in a single sprint.

**Functional Requirements Template**:

```
FUNCTIONAL REQUIREMENTS: [Feature Name]
───────────────────────────────────────
ID       Requirement Statement                                         Priority  Source
───────  ─────────────────────────────────────────────────────────────  ────────  ──────
FR-001   The system shall accept [data] in [format] via [channel]      Must      REQ-001
FR-002   The system shall calculate [result] using [formula]           Must      REQ-003
FR-003   The system shall reject [input] when [condition]              Should    Workshop

Rules: Use "shall" (mandatory), "should" (desirable), "may" (optional).
One behavior per requirement. Include measurable criteria. Avoid "user-friendly" or "fast".
```

**Non-Functional Requirements**: Categorize into Performance (response time, throughput), Scalability (concurrent users), Availability (uptime SLA), Security (encryption, access control), Compliance (GDPR, retention), Usability (task completion time), Accessibility (WCAG level), and Maintainability (coverage target). Each must have a measurement method.

**Traceability Matrix**:

```
TRACEABILITY MATRIX: [Project Name]
───────────────────────────────────
Business Need    Requirement    Design Element     Test Case      Status
───────────────  ─────────────  ─────────────────  ─────────────  ──────
BN-001           FR-001         API endpoint /foo   TC-001, TC-002 Implemented
BN-002           FR-003         Dashboard widget    TC-004, TC-005 Not started

Check for: business needs without requirements, requirements without tests, orphan requirements.
```

### Step 4: Data Analysis and Modeling

Poorly defined data structures lead to integration failures, reporting errors, and costly migrations. Define data models early and validate them with stakeholders who understand the business meaning of each field.

**Entity-Relationship Model**:

```
ER MODEL: [Domain Name]
───────────────────────
Entity: Customer
  Attributes: customer_id (PK), name, email (unique), tier, created_date, status

Entity: Order
  Attributes: order_id (PK), customer_id (FK), order_date, total_amount, status

RELATIONSHIPS
Customer  1──────M  Order       (A customer places zero or more orders)
Order     1──────M  OrderLine   (An order contains one or more order lines)
```

**Data Dictionary**:

```
DATA DICTIONARY: [Entity Name]
──────────────────────────────
Field           Type        Required  Default    Business Definition                  Constraints
──────────────  ──────────  ────────  ─────────  ───────────────────────────────────  ─────────────────
customer_id     UUID        Yes       Auto-gen   Unique identifier at registration    Immutable
email           VARCHAR(255)Yes       None       Primary contact email                Valid format, unique
tier            ENUM        Yes       Standard   Classification for pricing rules     Standard/Premium/Enterprise
status          ENUM        Yes       Active     Current lifecycle state               Active/Suspended/Closed
```

**Data Flow Description**: Document external entities (who sends/receives data), processes (what transforms data), data stores (where data persists), and data flows (what moves between them, in which direction, carrying what content).

**Data Quality Rules**:

```
DATA QUALITY RULES: [Entity/Domain]
───────────────────────────────────
ID      Rule Type      Field(s)     Rule Description                       Action on Violation
──────  ─────────────  ───────────  ─────────────────────────────────────  ────────────────────
DQ-001  Completeness   email        Must not be null or empty              Reject record
DQ-002  Format         email        Must match standard email regex        Reject with message
DQ-003  Uniqueness     email        No two active records share email      Reject duplicate
DQ-004  Referential    customer_id  Must exist in Customer table           Reject transaction
DQ-005  Consistency    line_total   Must equal quantity x unit_price       Recalculate and log
```

**Migration Requirements**: For each source field, define: target field, transformation rule, and validation notes. Include a migration plan: extract, transform, validate against quality rules, load to staging, reconcile (counts, checksums, samples), stakeholder review, production cutover with rollback window.

### Step 5: Gap Analysis

Gap analysis identifies the distance between current capabilities and the desired future state, providing a structured basis for investment decisions and prioritization.

**Current State Assessment**:

```
CURRENT STATE: [Capability Area]
────────────────────────────────
ID    Capability              Current Tool/Process    Maturity     Pain Points
────  ──────────────────────  ──────────────────────  ───────────  ─────────────────
C-01  Order processing        Manual spreadsheet      Ad hoc       Error-prone, slow
C-02  Customer communication  Individual emails       Repeatable   No templates

Maturity: Ad hoc → Repeatable → Defined → Managed → Optimized
```

**Gap Identification Matrix**:

```
GAP MATRIX: [Initiative Name]
─────────────────────────────
ID    Capability        Current State        Target State          Gap Description              Severity
────  ────────────────  ───────────────────  ────────────────────  ───────────────────────────  ────────
G-01  Order processing  Manual spreadsheet   Automated system      No system support; manual    Critical
G-02  Customer comms    Ad hoc emails        Event-driven templates No automation or templates  High
```

**Impact Analysis**: For each gap, assess two dimensions. Impact of leaving the gap open (operational, financial, strategic, customer effects). Impact of closing the gap (process improvement, cost savings, competitive positioning). Include effort to close: duration, cost, resources, and dependencies on other gaps.

**Cost-Benefit Framework**: Compare costs (implementation, labor, training, ongoing maintenance) against benefits (labor savings, error reduction, revenue enabled, penalties avoided) over a 1-3 year horizon. Calculate NPV, payback period, and ROI.

**Recommendation Prioritization**:

```
PRIORITY MATRIX
───────────────
Gap ID  Recommendation              Business Value  Effort  Risk  Priority Score  Sequence
──────  ──────────────────────────  ──────────────  ──────  ────  ──────────────  ────────
G-01    Implement order automation  High (9/10)     High    Med   7.5             Phase 1
G-02    Deploy comms templates      Med (7/10)      Low     Low   8.0             Phase 1

Score = (Value x 0.5) + (Inverse Effort x 0.3) + (Inverse Risk x 0.2)
```

### Step 6: Acceptance Criteria and Testing

Acceptance criteria translate business rules into testable conditions. They serve as the contract between business stakeholders and the engineering team.

**Business Rule Extraction**:

```
BUSINESS RULES: [Feature Name]
──────────────────────────────
ID      Rule Name              Rule Statement                                         Source       Type
──────  ─────────────────────  ─────────────────────────────────────────────────────  ───────────  ─────────
BR-001  Discount eligibility   Premium customers get 10% off on orders > $500         Policy doc   Calculation
BR-002  Approval threshold     Orders > $10,000 require manager approval              Finance      Authorization
BR-003  Account lockout        Lock after 5 consecutive failed login attempts          Security     Security
```

**Given/When/Then Scenarios**:

```
SCENARIO 1: Premium customer receives discount (happy path)
  Given a customer with tier "Premium" and an order totaling $600
  When  the customer submits the order
  Then  the system applies a 10% discount and the total becomes $540

SCENARIO 2: Standard customer does not receive discount
  Given a customer with tier "Standard" and an order totaling $600
  When  the customer submits the order
  Then  no discount is applied and the total remains $600

SCENARIO 3: Order below discount threshold
  Given a customer with tier "Premium" and an order totaling $400
  When  the customer submits the order
  Then  no discount is applied and the total remains $400
```

Write one scenario per business rule per path: happy path, error path, and boundary.

**Acceptance Test Matrix**:

```
TEST MATRIX: [Feature Name]
───────────────────────────
Business Rule   Happy Path  Error Path  Boundary   Edge Case  Status
──────────────  ──────────  ──────────  ─────────  ─────────  ──────
BR-001          SC-01       SC-02       SC-03      -          Ready
BR-002          SC-04       SC-08       SC-09      SC-10      Ready
BR-003          SC-05       SC-06       SC-07      SC-11      Draft
```

**UAT Planning**:

```
UAT PLAN: [Release Name]
────────────────────────
Coordinator: [Name]    Environment: [URL]    Period: [Start] to [End]

ENTRY CRITERIA: Scenarios scripted, environment deployed, critical defects resolved, participants briefed
EXIT CRITERIA: 100% must-have scenarios executed, zero critical defects, business sign-off obtained

PARTICIPANTS
Name            Role              Scenarios Assigned   Training Date
──────────────  ────────────────  ───────────────────  ─────────────
[Name]          [Business role]   SC-01 through SC-06  [Date]
```

**Defect Classification**:

| Severity | Business Definition | Response SLA |
|----------|-------------------|--------------|
| Critical | Process blocked, no workaround | Fix within 4 hours |
| High | Major function impaired, costly workaround | Fix within 1 day |
| Medium | Minor impairment, acceptable workaround | Fix within 1 week |
| Low | Cosmetic, no business impact | Fix in next release |

### Step 7: Stakeholder Communication

Effective communication prevents misalignment and builds trust. Use structured templates so status, changes, and decisions are unambiguous.

**Status Report**:

```
STATUS REPORT: [Project Name] - Week of [YYYY-MM-DD]
─────────────────────────────────────────────────────
Overall: [GREEN / AMBER / RED]

COMPLETED: [Item 1], [Item 2], [Milestone reached]
PLANNED:   [Item 1], [Item 2]

RISKS/ISSUES
ID    Type   Description                      Impact    Mitigation              Owner    Due
────  ─────  ───────────────────────────────  ────────  ──────────────────────  ───────  ──────
R-01  Risk   API dependency may slip 1 week   Timeline  Parallel dev path       [Name]   [Date]

DECISIONS NEEDED: [Description, options, recommendation, needed by DATE]
```

**Requirements Sign-Off**: Distribute document with review deadline. Reviewers submit comments. BA consolidates and resolves conflicts. Updated document sent for final review (3 business days). Approvers sign to confirm completeness. "Approved with comments" requires all comments resolved before implementation. Sign-off establishes the agreed baseline but does not prevent future change requests.

**Change Request**:

```
CHANGE REQUEST: [CR-001]
────────────────────────
Requested by: [Name]    Date: [YYYY-MM-DD]    Priority: [Critical/High/Medium/Low]

DESCRIPTION: [What is requested and why]

IMPACT ASSESSMENT
Area           Impact Description                              Severity
─────────────  ─────────────────────────────────────────────   ────────
Requirements   [Requirements added/modified/removed]           [H/M/L]
Timeline       [Schedule impact in days/weeks]                 [H/M/L]
Budget         [Cost impact]                                   [H/M/L]
Testing        [Test cases to add/modify]                      [H/M/L]

RECOMMENDATION: [Approve, reject, or defer with rationale]
```

**Impact Notification**: When a change affects stakeholders, communicate: what happened (factual summary), who is affected, what it means (consequences), what is being done (actions and dates), and what you need from them (specific asks with deadlines).

**Decision Record**:

```
DECISION: [DEC-001]
───────────────────
Date: [YYYY-MM-DD]    Decided by: [Name]    Status: [Proposed/Accepted/Superseded]

CONTEXT: [Why this decision was needed]
OPTIONS: A) [description, pros, cons]  B) [description, pros, cons]  C) [description, pros, cons]
CHOSEN: [Option and primary reason]
CONSEQUENCES: [What this enables, what it rules out]
REVIEW TRIGGER: [Condition to revisit: date, metric threshold, or event]
```

## Quick Reference: Technique Selection Guide

| Situation | Recommended Technique | Step |
|-----------|----------------------|------|
| "What do stakeholders need?" | Interviews + stakeholder map | Step 1 |
| "How does the current process work?" | As-is process map + observation | Step 2 |
| "What should the system do?" | Use cases + functional requirements | Step 3 |
| "What data do we need?" | ER model + data dictionary | Step 4 |
| "Where are we vs where we need to be?" | Gap matrix + impact analysis | Step 5 |
| "How do we know it works?" | Given/When/Then + UAT plan | Step 6 |
| "How do we keep everyone aligned?" | Status reports + change requests | Step 7 |

## Common Mistakes to Avoid

### Mistake 1: Capturing Solutions Instead of Requirements
```
Bad:  "The system shall use a dropdown menu for country selection"
Good: "The system shall allow the user to select their country from a list of 195 recognized countries"
```

### Mistake 2: Skipping the Current State
```
Bad:  Jump straight to designing the future system
Good: Map the as-is process first, then identify which steps to automate, eliminate, or improve
```

### Mistake 3: Writing Untestable Requirements
```
Bad:  "The system shall be easy to use"
Good: "A new user shall complete the registration process in under 3 minutes without assistance"
```

### Mistake 4: Ignoring Data Migration
```
Bad:  Assume data from the old system will "just work" in the new one
Good: Define field-by-field mapping, transformation rules, and a validation plan before development begins
```

### Mistake 5: Informal Change Management
```
Bad:  Stakeholder emails a new requirement; developer implements it immediately
Good: Change request submitted, impact assessed, approved by designated authority, then scheduled
```

## Quality Checklist

- [ ] Stakeholder map is complete with engagement strategy per stakeholder
- [ ] At least two elicitation techniques were used (triangulation)
- [ ] As-is process is documented with measurable metrics
- [ ] To-be process addresses specific identified pain points
- [ ] Every functional requirement uses "shall" and is independently testable
- [ ] Data dictionary defines every field with type, constraints, and business meaning
- [ ] Gap analysis includes cost-benefit for each recommendation
- [ ] Acceptance criteria are written in Given/When/Then format for every business rule
- [ ] UAT plan has defined entry and exit criteria
- [ ] Change request process is documented and stakeholders are aware of it
- [ ] Traceability matrix links business needs to requirements to test cases with no orphans

## Related Skills

- `product-manager` - Product strategy, prioritization, and roadmap planning
- `technical-writer` - Documentation standards and user-facing content
- `plan-before-code` - Engineering planning and exploration before implementation
- `test-driven-development` - Writing automated tests from acceptance criteria

---

**Version**: 1.0.0
**Last Updated**: March 2026


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets are not met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
