---
name: feedback-integration
description: >
  Use when receiving feedback from reviews, testing, QA, or HITL processes. This skill
  provides a structured process for incorporating feedback into deliverables, ensuring
  no feedback item is lost, misunderstood, or inadequately addressed.
---

# Feedback Integration

## Overview
This skill defines how to process, understand, and integrate feedback into deliverables. Whether from code review, QA testing, quality gates, or human approval, proper feedback integration ensures work meets required standards before final delivery.

## When to Use
- After receiving code review comments
- After QA testing identifies issues
- After quality gate validation returns findings
- After human review and approval feedback
- After any validation or testing cycle
- **Don't use when:** Feedback is purely informational with no action required

## Core Procedures

### Step 1: Collect and Catalog
Gather ALL feedback in one place and categorize:
- [ ] **BLOCKING:** Must be fixed before delivery can proceed
- [ ] **RECOMMENDED:** Should be fixed for quality but not blocking
- [ ] **OPTIONAL:** Improvement suggestion, nice-to-have
- [ ] **CLARIFICATION:** Request for explanation, may or may not need change

### Step 2: Understand Each Item
For each feedback item:
1. **Paraphrase** the feedback in your own words to confirm understanding
2. **Identify** what specific change or action is needed
3. **Check** if multiple feedback items relate to the same root issue
4. **Flag** any feedback that's unclear or seems incorrect

### Step 3: Plan Integration
1. Group related feedback items together
2. Determine the most efficient order to address them
3. Estimate effort for each fix or change
4. Identify any feedback that requires clarification before acting

### Step 4: Execute Changes
1. Address BLOCKING items first
2. Address RECOMMENDED items next
3. Address OPTIONAL items as time permits
4. For each change made, document what was done and which feedback item it addresses

### Step 5: Verify and Respond
For each feedback item:
```
Feedback #[number]: [original feedback text]
Category: [BLOCKING/RECOMMENDED/OPTIONAL/CLARIFICATION]
Action taken: [what was done to address it]
Status: [RESOLVED / CLARIFIED / DISPUTED]
Disputed reason: [if status is DISPUTED, explain why]
```

### Step 6: Request Re-review
- Submit updated deliverable for re-review
- Include summary of all changes made
- Highlight areas needing particular attention
- Set expectation on what's ready for approval

## Quality Checklist
- [ ] ALL feedback items cataloged and categorized
- [ ] BLOCKING items all resolved before re-submission
- [ ] Each feedback item has corresponding action documented
- [ ] Disputed items have clear reasoning documented
- [ ] Updated deliverable addresses all applicable feedback
- [ ] Re-review request includes summary of changes

## Error Handling
- **Error:** Feedback is unclear or ambiguous
  **Response:** Ask clarifying question before making changes, don't guess
- **Error:** Feedback seems incorrect or conflicts with requirements
  **Response:** Dispute with specific reasoning and evidence, request clarification
- **Error:** Feedback volume exceeds capacity to address
  **Response:** Address BLOCKING items first, communicate capacity issue with timeline
- **Error:** Making changes introduces new issues
  **Response:** Run output-validation-checklist, fix new issues, document in re-review

## Cross-Team Integration
**Related Skills:** output-validation-checklist, handoff-protocol, systematic-debugging, conflict-resolution
**Used By:** ALL agents when receiving review or QA feedback, especially developers, documenters, refactors