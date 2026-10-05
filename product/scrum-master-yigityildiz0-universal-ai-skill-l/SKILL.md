---
name: scrum-master
description: Scrum and agile facilitation expertise for engineering teams. Use when planning sprints, facilitating retrospectives, removing blockers, tracking velocity.
---

# Scrum Master

Structured scrum and agile facilitation frameworks for engineering teams. This skill provides sprint planning tools, retrospective formats, metrics dashboards, and coaching patterns that connect agile principles to daily engineering execution.

## When to Use This Skill

Use this skill for:

- Planning sprints with realistic capacity and clear goals
- Facilitating daily standups (synchronous or async) and managing flow
- Running sprint reviews and demos for stakeholders
- Leading retrospectives that produce actionable improvements
- Tracking velocity, burndown, cycle time, and other delivery metrics
- Identifying and removing impediments that block the team
- Coaching teams toward higher agile maturity and self-organization

**Trigger phrases**: "sprint planning", "daily standup", "retrospective", "retro", "velocity", "burndown", "cycle time", "WIP limit", "impediment", "blocker", "scrum", "agile", "sprint goal", "definition of done", "definition of ready", "backlog refinement", "sprint review", "demo", "team health", "continuous improvement"

## What This Skill Does

Provides a seven-step scrum facilitation workflow that covers the complete sprint lifecycle, from planning through delivery, with metrics and coaching patterns for continuous improvement.

### Overview

1. **Sprint Planning** - Capacity calculation, estimation, goal setting, and backlog refinement
2. **Daily Standups and Flow Management** - Standup formats, async options, Kanban board design, and WIP limits
3. **Sprint Review and Demo** - Demo preparation, stakeholder feedback, and release readiness
4. **Retrospective Facilitation** - Five formats with action item tracking and psychological safety
5. **Velocity and Metrics** - Tracking, interpretation, and anti-patterns in delivery metrics
6. **Impediment Removal** - Impediment logs, escalation paths, dependency management, and risk tracking
7. **Team Health and Continuous Improvement** - Health checks, maturity assessment, coaching, and scaling

## Instructions

### Step 1: Sprint Planning

Sprint planning translates backlog items into a realistic commitment organized around a clear sprint goal. Never plan at 100% utilization; leave room for unplanned work, meetings, and support duties.

**Capacity Calculation Template**:

```
SPRINT CAPACITY: Sprint [Number]
─────────────────────────────────
Sprint duration: [N] days | Team size: [N] members

Team Member  | Available Days | Capacity Factor | Effective Days
─────────────|────────────────|─────────────────|───────────────
[Name]       | 10             | 0.7             | 7.0
[Name]       | 8 (PTO 2d)    | 0.7             | 5.6
─────────────|────────────────|─────────────────|───────────────
Team total effective days:   [sum]
Unplanned buffer (20%):      [sum * 0.2]
Committable capacity:        [sum * 0.8]

Capacity factor 0.7 accounts for meetings, code review, and context switching.
Adjust per role: seniors 0.6 (more review); juniors 0.75.
```

**Story Point Estimation Techniques**:

| Technique | Best For | How It Works |
|-----------|----------|--------------|
| Planning Poker | Teams of 3-9, well-defined stories | Fibonacci cards (1,2,3,5,8,13,21). Reveal simultaneously. Discuss outliers. Re-vote. |
| T-Shirt Sizing | Large backlogs, rough sizing | XS/S/M/L/XL mapped to point ranges (XS=1, S=2, M=3, L=5, XL=8+). |
| Affinity Mapping | New teams, bulk estimation | Sort stories into relative groups on a wall. Assign points to groups. |
| Reference Stories | Teams with history | Pick 3-5 completed stories as calibration anchors. Compare new stories against them. |

Rules: Estimate complexity and risk, not hours. If a story exceeds 13 points, split it. The team estimates, not the scrum master.

**Sprint Goal Definition**:

```
SPRINT GOAL: Sprint [Number]
────────────────────────────
Goal:         [One sentence: the outcome, not a feature list]
Success test: [How will we know the goal is met at sprint review?]
Key stories:  [3-5 stories that directly serve this goal]
Anti-goal:    [What this sprint is NOT trying to achieve]
```

Good: "Users can complete onboarding end-to-end without manual intervention". Bad: "Complete stories ABC-123, ABC-124, ABC-125" (task list, not a goal).

**Backlog Refinement Checklist** (run mid-sprint for the upcoming sprint):

- [ ] Each story follows "As a / I want to / So that" format
- [ ] Acceptance criteria written in Given/When/Then format
- [ ] Story is estimated or ready to estimate
- [ ] Dependencies identified and documented
- [ ] Story fits within a single sprint (if not, split it)
- [ ] Edge cases and error scenarios listed

**Definition of Ready** (entry gate for sprint planning):

- [ ] User problem is clearly stated
- [ ] Acceptance criteria reviewed by the team
- [ ] Story estimated by the team
- [ ] Dependencies resolved or dependent items complete
- [ ] Design assets available (if applicable)
- [ ] Small enough to complete in one sprint
- [ ] Test scenarios outlined (happy path + error path)

### Step 2: Daily Standups and Flow Management

The daily standup is a coordination event where the team synchronizes on progress, surfaces blockers, and adjusts the plan. It is not a status report to the scrum master.

**Standup Format Options**:

| Format | Structure | Best For |
|--------|-----------|----------|
| Classic Three Questions | Did / Will do / Blockers | Small co-located teams (3-5) |
| Walk the Board | Right-to-left across the board, discuss each in-progress item | Teams focused on finishing over starting |
| Round Robin with Focus | One priority + one risk per person | Larger teams (6-9) |
| Exception-Based | Speak only if blocked, need help, or changed plans | Mature self-organizing teams |

**Walk the Board Protocol**: Start at "In Review" (can we get these to Done?), move to "In Progress" (anything stuck > 2 days?), then "To Do" (who pulls next? WIP limits respected?). Park detailed discussions for after standup. 15 minutes max.

**Async Standup Template** (for distributed teams):

```
ASYNC STANDUP: [Name] - [Date]
───────────────────────────────
DONE:       [Completed items with ticket refs]
WORKING ON: [Current focus with ticket ref]
BLOCKED BY: [Blocker + who can unblock] or "No blockers"
NEEDS SYNC: [Topic requiring a live conversation] or "None"
```

Post by a consistent deadline daily. Scrum master reviews within 1 hour and flags blockers.

**Kanban Board Design**:

```
Column        | WIP Limit | Entry Criteria             | Exit Criteria
──────────────|───────────|────────────────────────────|─────────────────────
Backlog       | None      | Meets Definition of Ready  | Pulled into sprint
To Do         | None      | In current sprint backlog  | Developer picks it up
In Progress   | 2/dev     | Developer assigned         | Code complete, tests pass
In Review     | 3 total   | PR opened, CI green        | Approved by reviewer
Done          | None      | Merged and deployed/staged | N/A
```

**WIP Limits**: Team WIP for "In Progress" = team size * 1.5 (rounded down). When limits are hit: stop starting, help finish, investigate why items are stuck. Signs limits are too high: items sit "In Progress" 3+ days, people juggle 3+ items. Signs too low: developers idle waiting for reviews.

**Blocker Identification Checklist** (check daily):

- [ ] Any item "In Progress" > 2 days without a PR?
- [ ] Any PR open > 24 hours without review?
- [ ] Any external dependency with no status update this week?
- [ ] Any story where the developer has unasked questions?

**Flow Metrics** (track weekly):

| Metric | Definition | Target |
|--------|-----------|--------|
| Cycle Time | "In Progress" to "Done" | < 3 days |
| Lead Time | Backlog entry to "Done" | < 10 days |
| Throughput | Items completed per week | [team baseline] |
| Blocker Count | Active blockers | 0 |

### Step 3: Sprint Review and Demo

The sprint review demonstrates working software and collects stakeholder feedback. It is not a slideshow.

**Demo Preparation Checklist** (complete 1 day before review):

- [ ] 3-5 items selected for demo (prioritize stakeholder-visible work)
- [ ] Presenter assigned for each item
- [ ] Demo environment prepared with test data (never demo on production)
- [ ] Each demo scripted: setup, action, expected result
- [ ] Backup screenshots/recordings in case of environment failure
- [ ] Summary of completed, incomplete, and carry-over items drafted

**Sprint Review Agenda** (60 min for a 2-week sprint):

1. Sprint goal recap: met, partially met, or not met (5 min)
2. Live demos with Q&A after each item (30 min)
3. Items not completed and carry-over plan (5 min)
4. Stakeholder feedback capture (15 min)
5. Next sprint preview (5 min)

**Stakeholder Feedback Log**:

```
ID  | Feedback        | Source      | Type    | Priority | Action
────|─────────────────|─────────────|─────────|──────────|───────────
F-1 | [text]          | [Name/Role] | Feature | [H/M/L]  | Add to backlog
F-2 | [text]          | [Name/Role] | Bug     | [H/M/L]  | Fix next sprint
```

Types: Feature, Bug, Enhancement, Question, Praise, Concern. Priority: H = next sprint, M = 2-3 sprints, L = backlog.

**Release Readiness Assessment**:

- [ ] All acceptance criteria verified
- [ ] No open P0/P1 defects
- [ ] Performance tested at expected scale
- [ ] Monitoring and alerting configured
- [ ] Rollback procedure documented and tested
- [ ] Release notes drafted
- [ ] Product Owner approves release

### Step 4: Retrospective Facilitation

The retrospective is the team's most important continuous improvement tool. Vary the format to prevent staleness and always end with concrete action items.

**Psychological Safety Ground Rules** (read aloud at the start of every retro):

1. What is said in the retro stays in the retro (unless the team agrees otherwise)
2. We assume everyone did their best with what they knew at the time
3. We focus on systems and processes, not individuals
4. Silence is okay; not everyone processes ideas at the same speed
5. Action items need a volunteer owner, not an assigned one
6. The scrum master participates but does not dominate

Check-in question (rotate): "In one word, how did this sprint feel?" or "On a scale of 1-5, how confident are you that we can improve next sprint?"

**Format 1: Start / Stop / Continue** (45 min, best for new teams)

Brainstorm (5 min): sticky notes for Start, Stop, Continue. Group themes (10 min). Dot vote with 3 votes each (5 min). Discuss top 3 themes with root cause analysis (20 min). Select 1-3 actions with owners (5 min).

**Format 2: 4Ls - Liked / Learned / Lacked / Longed For** (45 min, balances positives with gaps)

Same process as Start/Stop/Continue. "Learned" and "Longed For" reveal training needs and tooling gaps that other formats miss.

**Format 3: Sailboat** (60 min, visual metaphor for abstract concepts)

Draw: Island (destination/goal), Wind/Sails (what propelled us), Anchor (what slowed us), Rocks (risks ahead), Sun (recognition). Silent brainstorm (7 min), cluster (10 min), discuss anchors and rocks (25 min), actions (8 min).

**Format 4: Timeline** (60 min, best after significant events or incidents)

Build a chronological timeline of sprint events with color coding (green/red/yellow). Walk through events, identify patterns and turning points. Use "5 Whys" on the most impactful negative pattern. Actions target root causes.

**Format 5: Mad / Sad / Glad** (45 min, when morale needs attention)

Three columns for emotions. Validate feelings before problem-solving. If "Mad" items target individuals, redirect to the process. If the board is mostly "Mad" and "Sad", team morale needs attention beyond the retro.

**Action Item Tracking**:

```
RETRO ACTION TRACKER
─────────────────────
Sprint | Action                        | Owner   | Due Date   | Status
───────|───────────────────────────────|─────────|────────────|──────────
S-14   | Set up automated deploy       | [Alice] | 2026-04-01 | Done
S-15   | Reduce PR review to <24h      | [Team]  | 2026-04-15 | Not Started
```

Rules: Review last sprint's actions at the START of every retro. Max 3 new actions. Actions must be specific and measurable. If not done after 2 sprints, re-commit or drop honestly.

### Step 5: Velocity and Metrics

Metrics are tools for the team's self-improvement, not management surveillance. Use them to spot trends, not to judge individuals.

**Velocity Tracking**: Track story points completed per sprint. Use the rolling average over the last 3 sprints for planning (not the peak). Never compare velocity between teams.

**Burndown vs Burnup**: Burndown tracks remaining work (flat sections = stuck items; staircase = stories too large). Burnup tracks completed work plus scope changes (makes mid-sprint scope additions visible). Use burnup when scope creep is recurring.

**Cycle Time vs Lead Time**: Lead Time = backlog entry to Done. Cycle Time = "In Progress" to Done. A large gap means items sit in the backlog too long. Track weekly averages over 4-6 sprints.

**Throughput**: Items completed per week. Often more stable than velocity because it is unaffected by estimation inconsistencies. Use for forecasting: "At 5.5 items/week, 20 items takes approximately 3.6 weeks".

**Escaped Defects**: Escape Rate = Production Defects / (Sprint Defects + Production Defects) * 100. Target < 15%. Track which defect categories escape most to focus testing improvements.

**Metric Interpretation Guide**:

| Metric | Healthy | Warning |
|--------|---------|---------|
| Velocity | Stable within +/- 15% over 4+ sprints | Swings of 30%+ or declining |
| Cycle Time | Consistent or decreasing | Increasing over 3+ sprints |
| Throughput | Stable or increasing | Decreasing with same team size |
| Escaped Defects | < 15% escape rate | > 25% or rising trend |
| Sprint Goal | Met 80%+ of sprints | Missed 3+ consecutive |
| Carry-over | < 10% of committed points | > 25% carried over regularly |

**Anti-Patterns in Metrics**:

| Anti-Pattern | Harm | Alternative |
|-------------|------|-------------|
| Comparing velocity across teams | Teams estimate differently; comparison is meaningless | Compare each team to its own trend |
| Velocity as a KPI | Teams inflate estimates to look productive | Use velocity for planning only |
| Demanding velocity increase | Encourages cutting corners | Focus on removing impediments |
| Tracking individual velocity | Discourages collaboration | Track team-level metrics only |
| Ignoring metrics entirely | Problems invisible until crisis | Review 2-3 metrics weekly |
| Cherry-picking good sprints | Hides systemic issues | Use rolling averages over 4+ sprints |

### Step 6: Impediment Removal

The scrum master's core responsibility is removing obstacles that prevent the team from delivering. Track impediments systematically and escalate promptly.

**Impediment Log Template**:

```
IMPEDIMENT LOG
───────────────
ID     | Raised     | Description              | Impact    | Owner   | Status
───────|────────────|──────────────────────────|───────────|─────────|───────────
IMP-01 | 2026-03-15 | CI pipeline takes 45 min | SLOWING   | [SM]    | In Progress
IMP-02 | 2026-03-16 | No staging env access    | BLOCKING  | [DevOps]| Escalated

Impact levels: BLOCKING (resolve in hours), SLOWING (resolve in 2 days), ANNOYING (resolve within sprint).
```

**Escalation Paths**:

| Level | Who | Resolve In | Triggers |
|-------|-----|-----------|----------|
| 1: Team | Scrum Master | 4 hours | Tooling, access, unclear requirements |
| 2: Cross-team | SM + Eng Manager | 2 days | Dependencies, resource conflicts, process disagreements |
| 3: Management | Eng Manager + Director | 1 week | Budget, policy blocks, staffing gaps |
| 4: Executive | VP/CTO | 2 weeks | Strategic misalignment, cross-department conflicts |

Rule: Never escalate without documenting the problem, impact, options considered, and a recommended path forward.

**Dependency Tracker**:

```
ID     | Our Team Needs        | From Team    | Needed By  | Status   | Risk
───────|───────────────────────|──────────────|────────────|──────────|─────────
DEP-01 | Auth API v2 endpoint  | Platform     | Sprint 16  | On Track | Low
DEP-02 | Updated design system | Design       | Sprint 15  | At Risk  | High
```

Review weekly. For "At Risk" or "Blocked" dependencies, maintain a mitigation plan. Communicate missed deadlines immediately.

**Cross-Team Coordination**: Weekly 30-min sync with scrum masters from dependent teams. Agenda: dependency status review (10 min), upcoming needs (10 min), blocker resolution (10 min).

**Risk Register**:

```
ID     | Risk                    | Likelihood | Impact | Score | Mitigation              | Owner
───────|─────────────────────────|────────────|────────|───────|─────────────────────────|──────
RSK-01 | Key developer leaves    | Low        | High   | 6     | Cross-train on crit path| [SM]
RSK-02 | Scope creep             | High       | Medium | 9     | Enforce change process  | [PO]

Scoring: Likelihood (1-3) x Impact (1-3). Review weekly; daily when score >= 6.
```

**Decision Log**:

```
DECISION LOG
─────────────
ID     | Date       | Decision                    | Context                    | Decided By | Reversible
───────|────────────|─────────────────────────────|────────────────────────────|────────────|───────────
DEC-01 | 2026-03-15 | Use PostgreSQL over MongoDB  | Need strong consistency    | Tech Lead  | No
DEC-02 | 2026-03-18 | Adopt trunk-based dev        | Reduce merge conflicts     | Team       | Yes
```

Record every decision affecting architecture, process, or scope. Include context so future team members understand the reasoning. Mark reversibility so the team knows which decisions can be revisited cheaply.

### Step 7: Team Health and Continuous Improvement

A high-performing team is not just fast; it is healthy, engaged, and continuously improving.

**Team Health Check** (quarterly, based on the Spotify model):

Rate GREEN/YELLOW/RED with trend arrows (UP/FLAT/DOWN) for: Delivering Value, Speed, Code Quality, Fun, Learning, Mission Clarity, Teamwork, Psychological Safety, Management Support, Sustainable Pace. Aggregate anonymously. Discuss RED items and declining trends. Select 1-2 dimensions to improve next quarter with specific actions.

**Agile Maturity Assessment**:

| Level | Name | Characteristics |
|-------|------|----------------|
| 1 | Adopting | Follows Scrum events, roles defined, basic metrics tracked |
| 2 | Practicing | Self-organizes within sprint, retro actions completed, DoD enforced, realistic planning |
| 3 | Optimizing | Proactive impediment removal, metrics drive decisions, CI/CD and TDD embedded |
| 4 | Mastering | Adapts processes to context, coaches other teams, high predictability |

Rate each area 1-4. Focus growth plans on the lowest-scoring areas.

**Coaching Patterns**:

| Pattern | When to Use | How to Apply |
|---------|-------------|--------------|
| Ask, Don't Tell | Team asks SM to decide | "What options do you see?" |
| Silent Observer | Team looks to SM for permission | Attend standup but do not speak unless asked |
| Pair Facilitation | Developing future scrum masters | Co-facilitate a retro, then debrief |
| Teaching Moment | Team makes a process mistake | Wait for retro; ask "what did we learn?" |
| Mirror | Unaware dysfunctional pattern | "I noticed standups run 25 min. What causes that?" |
| Shield | External pressure threatens sprint | Absorb management requests; protect team focus |
| Connector | Team lacks skills or information | Connect with experts, training, or outside resources |

**Scaling Frameworks Overview**:

| Framework | Teams | Key Concepts | Best For |
|-----------|-------|-------------|----------|
| SAFe | 5-125+ | Agile Release Trains, Program Increments | Large enterprises with compliance needs |
| LeSS | 2-8 | One Product Backlog, one PO, Sprint Review Bazaar | Single-product companies |
| Nexus | 3-9 | Nexus Integration Team, Cross-Team Refinement | Scrum-mature teams needing lightweight coordination |
| Scrum@Scale | 2-1000+ | Scrum of Scrums, MetaScrum | Scaling organic scrum practices |

Start with the simplest framework that fits your context. No framework replaces the need for strong scrum masters on individual teams.

**Definition of Done Evolution**:

| Stage | When | Criteria Added |
|-------|------|---------------|
| Foundation | New teams | Code compiles, unit tests pass, peer-reviewed, merged, acceptance criteria verified |
| Quality | After 3-5 sprints | Integration tests pass, coverage meets standard, no new static analysis warnings, tested on staging |
| Production-Ready | After 8-10 sprints | Feature flagged, monitoring configured, docs updated, performance tested, security reviewed |
| Excellence | Mature teams | Accessibility audited, runbook updated, release notes written, knowledge sharing scheduled |

Review the DoD every quarter. Add criteria when the team consistently meets current items. Never remove criteria to make a story "Done" that would otherwise fail; adjust in the retrospective for future sprints.

## Quick Reference: Ceremony Selection Guide

| Situation | Recommended Tool | Step |
|-----------|-----------------|------|
| "How much can we commit?" | Capacity Calculation | Step 1 |
| "How big is this story?" | Estimation Techniques | Step 1 |
| "Is this story ready?" | Definition of Ready | Step 1 |
| "What should standup focus on?" | Walk the Board | Step 2 |
| "How do we coordinate across time zones?" | Async Standup | Step 2 |
| "Are we finishing or just starting?" | WIP Limits + Flow Metrics | Step 2 |
| "What do we demo?" | Demo Preparation Checklist | Step 3 |
| "Can we release this?" | Release Readiness Assessment | Step 3 |
| "How do we improve?" | Retrospective Formats | Step 4 |
| "Are we getting faster or slower?" | Velocity + Cycle Time | Step 5 |
| "What is blocking us?" | Impediment Log + Escalation | Step 6 |
| "How healthy is our team?" | Team Health Check | Step 7 |
| "When is a story truly done?" | Definition of Done | Step 7 |

## Quality Checklist

- [ ] Sprint goal is a measurable outcome, not a list of stories
- [ ] Capacity is calculated with a buffer for unplanned work
- [ ] All stories in the sprint meet the Definition of Ready
- [ ] Standup is timeboxed to 15 minutes and focuses on flow
- [ ] WIP limits are set and respected
- [ ] Sprint review includes a live demo of working software
- [ ] Stakeholder feedback is captured in a structured log
- [ ] Retrospective uses a varied format and produces 1-3 concrete actions
- [ ] Previous retro actions are reviewed before brainstorming new ones
- [ ] Velocity is tracked as a rolling average, not a target
- [ ] Impediments are logged with owners and resolution dates
- [ ] Dependencies are tracked and reviewed weekly
- [ ] Team health check is conducted at least quarterly
- [ ] Definition of Done evolves as the team matures

## Related Skills

- `product-manager` - Product management analysis for feature prioritization and scope control
- `plan-before-code` - Engineering planning and exploration before implementation
- `test-driven-development` - Writing tests from acceptance criteria
- `code-quality` - Ensuring implementation meets non-functional requirements

---

**Version**: 1.0.0
**Last Updated**: March 2026


### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets are not met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
