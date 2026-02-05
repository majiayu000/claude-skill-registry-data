---
name: Sprint Planning Assistant
description: Assist with sprint planning, backlog grooming, story point estimation, and sprint capacity management. Use when planning sprints, estimating work, organizing backlog, or when user mentions sprint planning, velocity, capacity, or story points.
allowed-tools: Bash
---

# Sprint Planning Assistant

Expert assistance for planning sprints, estimating work, and managing team capacity.

## When to Use This Skill

- Planning a new sprint
- Grooming/refining the backlog
- Estimating story points
- Calculating team capacity
- Analyzing sprint velocity
- Organizing work priorities
- User mentions: sprint, velocity, capacity, estimation, story points

## Sprint Planning Process

### 1. Pre-Planning Preparation

#### Review Previous Sprint
```jql
sprint = "Sprint 42" ORDER BY updated DESC
```

**Analyze**:
- What was completed?
- What carried over?
- What was the velocity?
- Any blockers or issues?

#### Check Backlog Health
```jql
project = PROJ AND sprint IS EMPTY AND status = "To Do" ORDER BY priority DESC
```

**Verify**:
- Stories have descriptions
- Acceptance criteria defined
- Dependencies identified
- Estimates added

### 2. Sprint Planning Meeting

#### Step 1: Set Sprint Goal
- What is the primary objective?
- What value will we deliver?
- How does it align with roadmap?

**Example Goals**:
- "Complete user authentication system"
- "Improve page load performance by 50%"
- "Launch payment integration MVP"

#### Step 2: Calculate Capacity

**Formula**:
```
Capacity = (Team Size × Work Days × Hours per Day) - (Meetings + PTO + Buffer)
```

**Example**:
```
Team: 5 developers
Sprint: 10 work days
Work: 6 hours/day (accounting for meetings)
PTO: 2 days (one person out)
Buffer: 20% (for unexpected work)

Capacity = (5 × 10 × 6) - (2 × 6) - (20% of 288)
        = 300 - 12 - 58
        = 230 hours

Or in story points (if velocity is 40):
Capacity ≈ 40 story points
```

#### Step 3: Select Stories

**Criteria**:
1. Aligns with sprint goal
2. Has clear acceptance criteria
3. Team has necessary skills
4. No blocking dependencies
5. Fits within capacity

**Query for candidates**:
```jql
project = PROJ
AND status = "To Do"
AND sprint IS EMPTY
AND "Story Points" IS NOT EMPTY
ORDER BY priority DESC, rank ASC
```

#### Step 4: Review and Commit
- Total points within capacity?
- Dependencies manageable?
- Risks identified?
- Team agreement on scope?

## Story Point Estimation

### What Are Story Points?

Story points measure **relative effort/complexity**, not time:
- **Effort**: How much work?
- **Complexity**: How hard is it?
- **Uncertainty**: How much is unknown?

### Estimation Scales

#### Fibonacci Scale (Recommended)
```
1  - Trivial: Simple change, < 1 hour
2  - Easy: Small feature, well understood
3  - Moderate: Standard feature, clear path
5  - Average: Typical feature, some complexity
8  - Complex: Significant feature, multiple components
13 - Very Complex: Large feature, high uncertainty
21 - Epic: Too large, should be split
```

#### T-Shirt Sizes (Alternative)
```
XS = 1 point
S  = 2 points
M  = 3 points
L  = 5 points
XL = 8 points
```

### Estimation Techniques

#### Planning Poker
1. Product owner explains story
2. Team asks clarifying questions
3. Each person picks estimate (secretly)
4. Everyone reveals simultaneously
5. Discuss differences
6. Re-estimate until consensus

#### Reference Stories
Compare to previously completed work:
- "This is about the same as the login feature (5 points)"
- "This is simpler than the payment integration (8 points)"
- "This is more complex than adding a button (2 points)"

#### Three-Point Estimation
```
Estimate = (Optimistic + (4 × Most Likely) + Pessimistic) / 6

Example:
Best case: 3 points
Most likely: 5 points
Worst case: 13 points

Estimate = (3 + (4 × 5) + 13) / 6 = 36 / 6 = 6 points
```

### Factors Affecting Estimates

#### Increase Estimate For:
- New technology/unfamiliar domain
- External dependencies
- Unclear requirements
- Complex business logic
- Integration with many systems
- High risk/uncertainty

#### Keep Estimate Lower For:
- Familiar technology
- Clear requirements
- Similar to past work
- Self-contained changes
- Good test coverage exists

## Backlog Grooming

### When to Groom
- Regular sessions (e.g., mid-sprint)
- Before sprint planning
- When new priorities emerge

### Grooming Activities

#### 1. Refinement
- Clarify requirements
- Add acceptance criteria
- Identify dependencies
- Break down epics
- Add technical notes

#### 2. Estimation
- Add story points
- Validate existing estimates
- Re-estimate if scope changed

#### 3. Prioritization
- Order by business value
- Consider dependencies
- Balance quick wins vs. strategic work

#### 4. Cleanup
- Close duplicates
- Archive obsolete issues
- Update stale information

### Grooming Checklist

For each story:
- [ ] Clear title and description
- [ ] User story format (if applicable)
- [ ] Acceptance criteria defined
- [ ] Story points estimated
- [ ] Priority set
- [ ] Labels added
- [ ] Dependencies identified
- [ ] Assignee (if known)
- [ ] Sprint ready

## Capacity Management

### Team Capacity Factors

#### Available Hours
```
Base Hours = Team Size × Sprint Days × Hours/Day
Actual Hours = Base - (PTO + Meetings + Support + Buffer)
```

#### Focus Factor
Percentage of time spent on sprint work:
```
Typical: 60-70%
High performing: 70-80%
New team: 50-60%
```

#### Velocity
Average story points completed per sprint:
```
Velocity = Average(Last 3-5 Sprints)
```

### Capacity Planning Example

**Team Details**:
- 6 developers
- 2-week sprint (10 work days)
- Historical velocity: 45 points

**Commitments**:
- 1 developer on PTO for 3 days
- 2 developers in training for 2 days
- On-call rotation (1 person, 20% capacity)

**Calculation**:
```
Base capacity: 45 points (historical velocity)

Adjustments:
- PTO: -3 days of 1 person = -3 points
- Training: -2 days of 2 people = -4 points
- On-call: -20% of 1 person = -2 points
- Buffer (10%): -4 points

Sprint capacity: 45 - 3 - 4 - 2 - 4 = 32 points
```

## Sprint Anti-Patterns to Avoid

### ❌ Overcommitment
Loading 60 points when velocity is 40.

**Fix**: Use historical velocity as guide, add buffer

### ❌ Under-commitment
Loading 20 points when velocity is 40, to "guarantee" completion.

**Fix**: Commit to realistic amount, have stretch goals ready

### ❌ No Sprint Goal
Just a collection of random stories.

**Fix**: Define clear, valuable objective for the sprint

### ❌ Splitting Mid-Sprint
Constantly splitting stories after sprint starts.

**Fix**: Better grooming and estimation up front

### ❌ Ignoring Dependencies
Starting work that's blocked by external factors.

**Fix**: Identify dependencies during planning

### ❌ Gold Plating
Adding unplanned features during implementation.

**Fix**: Stick to acceptance criteria, capture new ideas as separate stories

## Sprint Queries

### Stories Ready for Sprint
```jql
project = PROJ
AND type = Story
AND status = "To Do"
AND sprint IS EMPTY
AND "Story Points" IS NOT EMPTY
AND description IS NOT EMPTY
ORDER BY priority DESC
```

### Current Sprint Progress
```jql
sprint in openSprints()
ORDER BY status ASC, priority DESC
```

### Unestimated Stories
```jql
project = PROJ
AND type IN (Story, Task)
AND "Story Points" IS EMPTY
AND status != Done
ORDER BY priority DESC
```

### Sprint Burndown Data
```jql
sprint = "Sprint 42"
AND status IN ("In Progress", "To Do")
```

### Carry-Over from Previous Sprint
```jql
sprint = "Sprint 42"
AND sprint = "Sprint 43"
AND resolution IS EMPTY
```

## Velocity Tracking

### Calculate Velocity

**Method 1: Average of Last 3 Sprints**
```
Sprint 40: 38 points
Sprint 41: 42 points
Sprint 42: 44 points

Velocity = (38 + 42 + 44) / 3 = 41 points
```

**Method 2: Weighted Average**
```
Recent sprints count more:
Velocity = (Sprint N × 3 + Sprint N-1 × 2 + Sprint N-2 × 1) / 6
```

### Velocity Trends

#### Increasing Velocity
- Team is maturing
- Processes improving
- Technical debt decreasing

#### Stable Velocity
- Team is consistent
- Good predictability
- Sustainable pace

#### Decreasing Velocity
- Investigate: technical debt? team changes? distractions?
- Address root causes
- May need to reduce commitments

### Velocity vs. Capacity

**Velocity**: Historical output (story points completed)
**Capacity**: Theoretical input (available hours/points)

Use **velocity** for sprint planning, not capacity.

## Sprint Planning Template

### 1. Sprint Details
```
Sprint Number: 43
Duration: Jan 15 - Jan 28 (10 work days)
Sprint Goal: Complete user profile functionality
Team Velocity: 41 points (average last 3 sprints)
```

### 2. Team Capacity
```
Team Members: 6 developers
Availability:
- Alice: 10 days (full)
- Bob: 7 days (3 days PTO)
- Carol: 10 days (full)
- Dave: 10 days (full)
- Eve: 9 days (1 day training)
- Frank: 10 days (full, but on-call)

Adjusted Capacity: 36 points
```

### 3. Sprint Backlog
```
Committed Stories (36 points):
- PROJ-101: User profile page (8 pts)
- PROJ-102: Avatar upload (5 pts)
- PROJ-103: Profile editing (8 pts)
- PROJ-104: Privacy settings (5 pts)
- PROJ-105: Profile completion badge (3 pts)
- PROJ-106: Update navigation (2 pts)
- PROJ-107: Profile tests (5 pts)

Stretch Goals (13 points):
- PROJ-108: Social media links (5 pts)
- PROJ-109: Custom themes (8 pts)
```

### 4. Dependencies & Risks
```
Dependencies:
- PROJ-102 blocked until design review (due Jan 16)
- PROJ-104 requires security review

Risks:
- Avatar upload may need third-party service
- Privacy settings have regulatory requirements

Mitigation:
- Start PROJ-101, 103, 106 first
- Spike for avatar service options
- Consult legal team early on privacy
```

### 5. Sprint Success Criteria
```
Must Have:
- Users can view and edit their profiles
- Avatar upload working
- Privacy controls functional

Nice to Have:
- Profile completion indicators
- Social media integration

Definition of Done:
- Code reviewed
- Tests passing (>80% coverage)
- Deployed to staging
- Acceptance criteria met
- Documentation updated
```

## How I'll Help

When you need sprint planning assistance, I will:

1. **Analyze backlog**: Review stories and readiness
2. **Calculate capacity**: Based on team size, availability, velocity
3. **Suggest stories**: Prioritized candidates for the sprint
4. **Estimate work**: Help with story point estimation
5. **Identify risks**: Dependencies, blockers, unknowns
6. **Track progress**: Monitor sprint health
7. **Provide queries**: JQL for sprint management

## Example Interaction

**You**: "Help me plan Sprint 45. Team of 5, one person out for 2 days, velocity is usually around 35 points"

**Me**: "I'll help plan Sprint 45.

**Capacity Calculation**:
- Base velocity: 35 points
- Adjustment for PTO: -1.5 points (2 days of 1 person ≈ 10%)
- Buffer (10%): -3.5 points
- **Sprint capacity: 30 points**

Let me search for ready stories:

[Uses `/jira-search` with refinement query]

**Recommended Sprint Backlog** (30 points):
1. PROJ-501: Payment gateway integration (13 pts) - HIGH PRIORITY
2. PROJ-502: Transaction history UI (8 pts)
3. PROJ-503: Receipt email templates (5 pts)
4. PROJ-504: Payment error handling (4 pts)

**Sprint Goal**: Complete basic payment processing flow

**Stretch Goals** (if time allows):
- PROJ-505: Refund functionality (8 pts)

Should I create these issues or adjust the selection?"
