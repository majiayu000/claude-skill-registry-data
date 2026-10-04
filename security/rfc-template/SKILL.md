---
name: rfc-template
enabled: true
description: |
  Use when performing rfc template — structures a Request for Comments (RFC)
  document for proposing significant technical changes that require cross-team
  input and approval. This template guides authors through problem definition,
  proposed solution, alternatives analysis, and rollout planning, ensuring
  proposals are comprehensive enough for informed review.
required_connections:
  - prefix: wiki
    label: "Documentation Platform"
config_fields:
  - key: rfc_number
    label: "RFC Number"
    required: true
    placeholder: "e.g., RFC-2026-015"
  - key: title
    label: "RFC Title"
    required: true
    placeholder: "e.g., Migrate to event-driven architecture"
  - key: author
    label: "Author"
    required: true
    placeholder: "e.g., Jane Smith"
features:
  - RFC
  - DOCUMENTATION
  - ARCHITECTURE
---

# Request for Comments (RFC)

## Phase 1: Problem Statement

Define the problem clearly and concisely.

1. - [ ] What is the current state?
2. - [ ] What is the problem or opportunity?
3. - [ ] Who is affected?
4. - [ ] What is the cost of inaction?
5. - [ ] What are the success criteria for a solution?

**Metadata:**

| Field | Value |
|-------|-------|
| RFC Number | |
| Title | |
| Author | |
| Status | Draft / Open for Comment / Final Comment Period / Accepted / Rejected |
| Created | |
| Comment Deadline | |
| Reviewers | |

## Phase 2: Proposed Solution

Describe the proposed approach in detail.

1. - [ ] High-level overview (1-2 paragraphs)
2. - [ ] Detailed technical design
3. - [ ] Architecture diagrams
4. - [ ] API changes or new APIs
5. - [ ] Data model changes
6. - [ ] User experience changes

**Scope:**

- [ ] What is in scope for this RFC
- [ ] What is explicitly out of scope
- [ ] What are the dependencies

## Phase 3: Alternatives Considered

| Alternative | Description | Why Not Chosen |
|------------|------------|----------------|
|            |            |                |

For each alternative:
- [ ] Describe the approach
- [ ] List advantages over the proposed solution
- [ ] List disadvantages compared to the proposed solution

## Phase 4: Impact Analysis

**Compatibility:**
- [ ] Backward compatible: Y/N
- [ ] Migration required: Y/N
- [ ] Breaking changes: list

**Performance:**
- [ ] Expected performance impact
- [ ] Benchmarks or estimates

**Security:**
- [ ] Security implications
- [ ] New attack surfaces

**Cost:**
- [ ] Infrastructure cost changes
- [ ] Engineering effort estimate
- [ ] Ongoing maintenance cost

**Risk Assessment:**

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
|      |           |        |            |

## Phase 5: Rollout Plan

1. - [ ] Phase 1: ___ (description, timeline, success criteria)
2. - [ ] Phase 2: ___ (description, timeline, success criteria)
3. - [ ] Phase 3: ___ (description, timeline, success criteria)

- [ ] Rollback plan
- [ ] Feature flag strategy
- [ ] Monitoring and validation approach

## Phase 6: Open Questions

| Question | Raised By | Status | Resolution |
|----------|-----------|--------|------------|
|          |           |        |            |

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "We can skip some steps for this case" | Adapt the workflow steps, don't skip them | Skipped steps are where incidents and oversights originate |
| "The user seems to already know what to do" | Complete all workflow phases with the user | The workflow catches blind spots that experience alone misses |
| "This is a minor case, full process is overkill" | Scale the process down, don't turn it off | Minor cases become major when unstructured; the process scales, not disappears |
| "I'll fill in the details later" | Complete each section before moving on | Deferred details are forgotten; real-time capture is more accurate |
| "The template output isn't necessary" | Always produce the structured output format | Structured output enables comparison, audit trails, and handoff to other teams |

## Output Format

### RFC Summary

- **RFC:** ___
- **Title:** ___
- **Status:** ___
- **Decision:** Accepted / Rejected / Deferred
- **Decision Date:** ___
- **Decision Rationale:** ___

### Action Items

- [ ] Address all open questions
- [ ] Incorporate reviewer feedback
- [ ] Create implementation plan and tickets
- [ ] Schedule kickoff for implementation
- [ ] Archive RFC in decision log
