---
name: sop-builder
description: "Create Standard Operating Procedures with step-by-step workflows, RACI matrices, process maps, approval chains, and version control"
---

# SOP Builder

## Overview

Generate comprehensive Standard Operating Procedures (SOPs) that document processes, assign responsibilities, establish approval chains, and enable consistent execution across teams. This skill creates professional, compliance-ready SOPs with clear workflows and governance.

## Core Components

### 1. Process Definition
- **Process Title**: Clear, descriptive naming
- **Scope**: What's included and excluded
- **Objectives**: Desired outcomes
- **Frequency**: How often the process runs
- **Owner**: Primary responsible party

### 2. Step-by-Step Workflow
```
Step #: [Action]
- Input: [Required materials/data]
- Action: [Specific task]
- Output: [Deliverable]
- Owner: [Role responsible]
- Timeline: [Duration/deadline]
```

### 3. RACI Matrix
Create accountability structure:
- **R (Responsible)**: Does the work
- **A (Accountable)**: Makes final decision
- **C (Consulted)**: Provides input
- **I (Informed)**: Kept updated

```
Activity | Finance | Operations | Approval | Execution
---------|---------|-----------|----------|----------
Request  | R       | C         | I        | I
Review   | A       | R         | C        | I
Approval | C       | I         | A        | R
Execute  | I       | I         | I        | A
```

### 4. Approval Chains
- **Threshold Levels**: Define when escalation occurs
- **Approvers**: Named roles and escalation path
- **Timeline**: SLAs for approvals
- **Rejection Criteria**: When to bounce back

### 5. Process Map (ASCII)
```
START
  |
  v
[Step 1] --> [Step 2] --> [Step 3]
              |
              v (Error)
          [Correction]
              |
              v
         [Step 3]
              |
              v
            END
```

### 6. Decision Points
- **If X, then Y**: Clear branching logic
- **Exception Handling**: How to handle edge cases
- **Escalation Triggers**: When to involve management

## Template Structure

**SOP-XXX: [Process Name]**

Version: 1.0
Last Updated: [Date]
Next Review: [Date]
Owner: [Name/Role]

**Purpose**: [1-2 sentence summary]

**Scope**: [What's included; what's excluded]

**Responsible Parties**:
- Process Owner: [Role]
- Executor: [Role]
- Approver: [Role]
- Stakeholders: [List]

**Key Metrics**:
- Cycle time: [Target duration]
- Error rate: [Target %]
- Compliance: [Target %]

**RACI Matrix**: [See above]

**Process Steps**:
[Numbered steps 1-N with all details]

**Approval Chain**:
- Level 1 [Condition]: [Approver + Timeline]
- Level 2 [Condition]: [Approver + Timeline]
- Level 3 [Condition]: [Approver + Timeline]

**Exception Handling**:
- Exception 1: [Response]
- Exception 2: [Response]
- Escalation Protocol: [When/how to escalate]

## Best Practices

1. **Clarity**: Write for the most junior team member; avoid jargon
2. **Specificity**: Include URLs, templates, system names, field mappings
3. **Visual Aids**: Use flowcharts, screenshots, decision trees
4. **Version Control**: Track changes; date all revisions
5. **Testing**: Pilot with actual users before final release
6. **Accessibility**: Provide in multiple formats (PDF, online, video)
7. **Regular Reviews**: Schedule annual reviews; quarterly updates for new issues
8. **Training**: Link SOPs to training completion records
9. **Metrics**: Include KPIs to measure process health
10. **Feedback Loop**: Collect user feedback; iterate quarterly

## Common Pitfalls

- **Too Much Detail**: Balance completeness with readability
- **Outdated Information**: Assign ownership for keeping current
- **No Ownership**: Always assign a DRI (Directly Responsible Individual)
- **Lack of Examples**: Include real-world examples and sample outputs
- **No Exception Handling**: Anticipate what can go wrong
- **Missing Timelines**: Include both expected and max durations
- **Poor Formatting**: Use consistent structure across all SOPs

## Example: Approval Request SOP

**SOP-001: Expense Approval Workflow**

**Purpose**: Ensure all expenses are authorized, documented, and compliant with company policy.

**Scope**: All employee expenses; excludes routine operational costs over $50K (escalated to CFO).

**Key Metrics**:
- Average processing time: 5 business days
- First-pass approval rate: 95%+

**RACI Matrix**:
| Activity | Employee | Manager | Finance | CFO |
|----------|----------|---------|---------|-----|
| Submit | R | - | I | I |
| Initial Review | - | A | C | - |
| Compliance Check | - | - | R | - |
| Final Approval | - | - | A | - |
| Payment | - | - | R | I |

**Steps**:
1. Employee submits receipt + business justification in Expensify
2. Manager reviews within 2 business days (approve/reject/request info)
3. Finance compliance team verifies against policy ($50K threshold)
4. If under threshold: approved; if over: forwarded to CFO within 1 business day
5. Once approved, payment processed within 3 business days
6. Employee receives confirmation email with check/ACH date

**Approval Chain**:
- Manager (all amounts): 2 business days
- Finance ($5K-$50K): 1 business day
- CFO (>$50K): 2 business days

**Exceptions**:
- Missing receipt: Request within 48 hours or deny
- Policy violation: Hold for clarification; finance team notifies manager
- Duplicate expense: Flag and contact employee immediately

## Integration Points

- Link to policy documents (URL)
- Reference training materials
- Connect to system workflows (Salesforce, Workday, etc.)
- Reference related SOPs (e.g., SOP-002: Time Off Approval)
- Include templates and checklists as appendices

## Maintenance

- Assign process owner to monitor compliance monthly
- Quarterly review meetings with process stakeholders
- Annual comprehensive audit and revision
- Version control: date each update, summarize changes
- Notify affected teams of changes; provide training as needed

---

**Use this skill to**: Document any repeatable process, create compliance-ready workflows, establish clear accountability, and enable consistent execution at scale.
