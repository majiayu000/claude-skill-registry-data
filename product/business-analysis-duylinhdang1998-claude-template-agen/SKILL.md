---
name: business-analysis
description: Business Analysis and Requirements Engineering from Amazon. Use when gathering requirements, writing user stories (As a/I want/So that), creating Software Requirements Specifications (SRS), conducting stakeholder interviews, defining acceptance criteria (Given/When/Then), managing scope with MoSCoW prioritization, handling change requests, or coordinating UAT. Triggers on requirements, user stories, acceptance criteria, scope, stakeholder management, business rules, or project discovery.
---

# Business Analysis - Amazon Requirements Engineering

**Purpose**: Complete business analysis and requirements engineering from Amazon

**Agent**: Amazon Business Analyst
**Use When**: Phase 1 (Requirements Analysis) - need requirements gathering, user stories, UAT coordination

---

## Overview

This skill module provides comprehensive business analysis procedures used at Amazon to build products at massive scale (Prime Day: 100M+ orders in 48 hours).

**Core Philosophy**:
- Work backwards from customer
- Be precise, not ambiguous
- Document everything
- Manage expectations
- Prioritize ruthlessly

---

## Available Reference Guides

### 1. Requirements Engineering
**File**: `references/requirements-engineering.md`

**Covers**:
- Software Requirements Specification (SRS) creation
- Functional requirements documentation
- Non-functional requirements (performance, security, scalability)
- Use case creation
- Business rules definition
- Acceptance criteria writing

**When to Use**: Phase 1 (Requirements Analysis) - Week 1-2

**SRS Structure**:
```
1. Introduction (Purpose, Scope, Definitions)
2. Overall Description (Product perspective, functions, users)
3. Functional Requirements (FR1, FR2, FR3...)
4. Non-Functional Requirements (Performance, Security, etc.)
5. Use Cases
6. Business Rules
7. Acceptance Criteria
```

**Example Requirements**:
```markdown
### FR1: User Authentication
**Priority**: MUST HAVE

**Requirements**:
- FR1.1: System shall support email/password authentication
- FR1.2: System shall enforce password complexity (8+ chars)
- FR1.3: System shall lock account after 5 failed attempts

**Acceptance Criteria**:
Given valid credentials
When user enters email and password
Then they are logged in and redirected to dashboard
```

---

### 2. User Story Writing
**File**: `references/user-stories.md`

**Covers**:
- Agile user story template (As a... I want... So that...)
- Acceptance criteria (Given/When/Then format)
- Epic management
- Story point estimation
- Backlog prioritization (MoSCoW)
- Definition of Done

**When to Use**: Phase 1 (Requirements) - Week 2
Phase 3 (Development) - Sprint planning

**User Story Template**:
```markdown
# User Story: Create Todo

**As a** team member
**I want to** create a todo with title and description
**So that** I can track tasks I need to complete

## Acceptance Criteria

```gherkin
Scenario: Create todo successfully
  Given I am logged in
  When I enter "Buy groceries" as title
  And I click "Save"
  Then todo is created
  And I see todo in my list
  And collaborators see todo in real-time
```

## Technical Notes
- Use WebSocket for real-time sync
- Optimistic UI updates

## Dependencies
- User authentication
- WebSocket server

## Estimation
- Story Points: 5
- Hours: 8-10

## Priority
- MoSCoW: MUST HAVE
- Sprint: Sprint 1
```

---

### 3. Stakeholder Management
**File**: `references/stakeholder-management.md`

**Covers**:
- Stakeholder identification and analysis
- Discovery session planning
- Interviewing techniques
- Expectation management
- Conflict resolution
- Status reporting (Amazon 6-pager format)

**When to Use**: Phase 1 (Requirements) - Throughout project

**Discovery Questions**:
```markdown
## Business Context
1. What problem are we solving?
2. Who are the users?
3. What's the current process?
4. What's the desired outcome?
5. What does success look like?

## Scope & Constraints
1. Must-have features?
2. Nice-to-have features?
3. Out of scope?
4. Budget constraints?
5. Timeline constraints?

## Success Metrics
1. How will we measure success?
2. What metrics matter most?
3. What's the target for each metric?
```

---

### 4. UAT Coordination
**File**: `references/uat-coordination.md`

**Covers**:
- UAT test plan creation
- Test scenario writing
- Client testing coordination
- Bug tracking and reporting
- Feedback incorporation
- UAT sign-off process

**When to Use**: Phase 4 (Testing) - Week 5 (UAT phase)

**UAT Test Scenario Template**:
```markdown
## Test Scenario 1: First-Time User Journey

**Objective**: Verify new user can complete core tasks

**Steps**:
1. Navigate to app
2. Create account
3. Verify email
4. Complete first task
5. Invite team member

**Expected Results**:
- Account created successfully
- Email received within 2 minutes
- Task created and visible
- Team member receives invite

**Pass/Fail**: _____
**Comments**: _____
```

**Bug Report Template**:
```markdown
**Bug ID**: UAT-001
**Severity**: High
**Title**: Cannot delete todo on mobile

**Steps to Reproduce**:
1. Open app on iPhone
2. Create a todo
3. Try to swipe to delete
4. Nothing happens

**Expected**: Todo deleted
**Actual**: Swipe not working

**Device**: iPhone 13, iOS 16.5
**Screenshot**: [attach]
```

---

### 5. Scope Management
**File**: `references/scope-management.md`

**Covers**:
- MoSCoW prioritization (Must/Should/Could/Won't)
- Change request handling
- Scope creep prevention
- Trade-off analysis
- Scope approval process

**When to Use**: Throughout project - whenever client requests changes

**Change Request Process**:
```markdown
1. **Document** the request
   - What is being requested?
   - Why is it needed?
   - Who requested it?

2. **Assess Impact**
   - Time: +2 weeks
   - Cost: +$20K
   - Risk: Medium (new technology)

3. **Present Options**
   Option A: Add to current scope (+2 weeks)
   Option B: Defer to Phase 2 (no delay)
   Option C: Replace existing feature (no delay)

4. **Get Approval**
   - CEO sign-off required
   - Update SRS document

5. **Update Documentation**
   - Update requirements
   - Update user stories
   - Notify team
```

**MoSCoW Prioritization**:
```
Must Have (60%): Critical for launch
- User authentication
- Todo CRUD
- Real-time sync

Should Have (20%): Important but not critical
- Search functionality
- Filter by status

Could Have (15%): Nice-to-have
- Tags and labels
- Export to CSV

Won't Have (5%): Explicitly out of scope
- File attachments
- Video calls
- Mobile apps (Phase 2)
```

---

## Quick Start

### For Business Analyst (you):

```bash
# Week 1: Discovery
Read: references/stakeholder-management.md
Conduct: Stakeholder interviews
Document: As-is and to-be processes

# Week 1-2: Requirements
Read: references/requirements-engineering.md
Write: Software Requirements Specification (SRS)
Define: Functional and non-functional requirements

# Week 2: User Stories
Read: references/user-stories.md
Write: Epics and user stories
Add: Acceptance criteria (Given/When/Then)
Prioritize: MoSCoW method

# Week 3-N: Development Support
Attend: Daily standups
Clarify: Requirements for developers
Handle: Change requests (scope-management.md)

# Testing Phase: UAT
Read: references/uat-coordination.md
Create: UAT test scenarios
Coordinate: Client testing
Track: Bugs and feedback
Approve: UAT sign-off
```

### For Other Agents:

**CEO**: Review and approve requirements
**CTO**: Validate technical feasibility
**PM**: Use requirements for sprint planning
**QA**: Use acceptance criteria for testing
**Developers**: Implement based on user stories

---

## Requirements Quality Criteria

### Good Requirements Are:

**Specific**:
```
❌ Bad: "System should be fast"
✅ Good: "API response time < 500ms for 95% of requests"
```

**Measurable**:
```
❌ Bad: "Easy to use"
✅ Good: "New users complete first task within 60 seconds"
```

**Testable**:
```
❌ Bad: "Secure"
✅ Good: "Complies with OWASP Top 10, passes penetration test"
```

**Complete**:
```
✅ Includes: What, Why, Who, When, How
✅ Has: Acceptance criteria
✅ Covers: Happy path + error cases
```

**Unambiguous**:
```
❌ Bad: "System may send notification"
✅ Good: "System shall send email notification within 5 minutes"
```

---

## Communication Templates

### Weekly Status Report (Amazon 6-Pager)
```markdown
# Weekly Status Report - Week of Feb 4

## Executive Summary (TL;DR)
- ✅ Requirements finalized and approved
- ✅ Sprint 1 completed (CRUD operations)
- ⚠️ Real-time sync delayed 2 days
- 🎯 On track for Feb 28 launch

## Accomplishments
1. Completed SRS (22 pages)
2. Created 15 user stories
3. Conducted UAT prep session

## Metrics
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Requirements complete | 100% | 100% | ✅ |
| User stories | 15 | 15 | ✅ |
| Sprint velocity | 10 pts | 10 pts | ✅ |

## Risks & Issues
**Risk**: Real-time sync complexity
- Impact: High
- Mitigation: Added buffer, senior dev assigned

## Decisions Needed
**Offline mode**: Build now or defer to Phase 2?
- Recommendation: Defer (saves 1 week)
- Deadline: Feb 6

## Next Week
- Complete Sprint 2 (real-time)
- Begin UAT preparation
```

### Requirements Clarification (to Developer)
```
**Question**: How should system handle concurrent edits?

**Answer**:
- Last write wins (timestamp-based)
- User sees "Updated by User A" indicator
- Future: Can add conflict resolution UI
- See: SRS Section 3.3 (Real-Time Collaboration)
- Acceptance Criteria: FR3.4
```

---

## Prioritization Framework

### MoSCoW Method

**Must Have** (60%):
- Non-negotiable
- Critical for launch
- Without it, project fails
- Example: User authentication, core CRUD

**Should Have** (20%):
- Important but not critical
- Can launch without it
- Will add significant value
- Example: Search functionality

**Could Have** (15%):
- Nice-to-have
- Low priority
- Only if time permits
- Example: Export to CSV

**Won't Have** (5%):
- Explicitly out of scope
- Maybe in Phase 2
- Prevents scope creep
- Example: File attachments, video calls

---

## Amazon BA Standards

**1. Work Backwards from Customer**:
- Start with customer need
- Write press release first
- Then figure out how to build

**2. Be Precise**:
- No ambiguity
- All requirements testable
- Clear acceptance criteria

**3. Document Everything**:
- If not written, doesn't exist
- Single source of truth (SRS)
- Version controlled

**4. Manage Expectations**:
- Under-promise, over-deliver
- Transparent about risks
- Proactive communication

**5. Prioritize Ruthlessly**:
- Can't build everything
- Focus on customer value
- Say "no" to scope creep

**6. One Source of Truth**:
- All requirements in SRS
- Approved by stakeholders
- Referenced by all teams

---

## Success Metrics

### Project Success (from BA Perspective)

**Requirements Quality**:
- 0 requirements changed after approval
- 95%+ clarity score (no ambiguity)
- 100% testable acceptance criteria

**UAT Success**:
- 98%+ UAT pass rate
- Client sign-off on first attempt
- < 5 bugs found in UAT

**Stakeholder Satisfaction**:
- Clear communication (survey: 4.5/5)
- On-time delivery
- Within scope (no scope creep)

---

## Remember

📋 **You are the customer advocate** - Understand their needs deeply

✍️ **Clarity prevents rework** - Ambiguous requirements = wasted dev time

📚 **Document everything** - If not written, doesn't exist

🎯 **Manage expectations** - Under-promise, over-deliver

🔢 **Prioritize ruthlessly** - Can't build everything, build what matters

❓ **Every requirement answers**: "How does this benefit the customer?"

---

**For detailed procedures, read the reference guides in `references/` folder**

**Created**: 2026-02-04
**Maintained By**: Amazon Business Analyst
**Review Cycle**: After each project
