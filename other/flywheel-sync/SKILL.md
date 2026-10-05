---
name: flywheel-sync
description: 'Meta-skill that audits health of the entire product launch engine, identifies broken links between phases, and generates improvement roadmaps. Use when: system health, skill audit, launch engine health, are our skills working together, process audit, workflow health check.'
---

# Flywheel Sync (ORBIT System)

A meta-skill that operates above all other skills in the launch engine, auditing the health of skill-to-skill connections, identifying broken handoffs, redundant outputs, and bottlenecks, then generating a continuous improvement roadmap. ORBIT ensures the entire product launch system functions as an integrated flywheel rather than a collection of disconnected processes.

## When to Use
- Auditing whether the launch engine skills are working together effectively
- Diagnosing why a launch process feels slow, disconnected, or redundant
- Identifying gaps where important outputs are missing or not being consumed
- Checking if skill cadences are aligned with business rhythms
- Building a continuous improvement roadmap for the overall launch system
- Onboarding new team members to understand how skills interconnect
- Preparing for a major launch by verifying all system connections are healthy

## What You'll Need

**Critical inputs (ask if not provided):**
- List of active skills and their current usage status
- Recent outputs from each skill (or confirmation that skills have been run)
- Known pain points or friction in the current launch process
- Team structure and ownership map across skills
- Launch cadence (how often launches occur, what types)

**Nice-to-have:**
- Outputs from the most recent run of each skill
- Timestamps of last skill execution
- Team feedback on handoff quality and timing
- Historical launch debriefs (from launch-debrief)
- Current launch calendar and upcoming milestones

## Process

### Step 1: Map the Full Skill Connection Graph

Document every skill-to-skill connection in the launch engine with its expected data flow.

**Skill Connection Matrix:**

| From Skill | To Skill | Output Passed | Format | Timing | Status |
|-----------|---------|--------------|--------|--------|--------|
| signal-radar | battle-scanner | Market signals, trend data | Report | Weekly to Monthly | |
| signal-radar | position-lock | Emerging trends, whitespace | Report | Weekly to Quarterly | |
| battle-scanner | position-lock | Competitive landscape, gaps | Framework | Monthly to Quarterly | |
| battle-scanner | enablement-forge | Competitive battle cards | Cards | Monthly to Per-launch | |
| position-lock | demand-engine | Messaging framework, value props | Framework | Quarterly to Per-launch | |
| position-lock | enablement-forge | Messaging hierarchy, proof points | Framework | Quarterly to Per-launch | |
| demand-engine | budget-allocator | WAVE scores, channel strategy | Scored list | Per-launch | |
| demand-engine | launch-command | Channel activation plan | Plan | Per-launch | |
| journey-architect | demand-engine | Touchpoint map, stage definitions | Map | Per-launch | |
| journey-architect | growth-loop | Post-purchase journey stages | Map | Per-launch | |
| enablement-forge | launch-command | Sales materials inventory | Checklist | Per-launch | |
| budget-allocator | launch-command | Spend allocation plan | Model | Per-launch | |
| launch-command | launch-pulse | Launch plan, workstream status | Dashboard | Per-launch | |
| launch-pulse | growth-loop | Adoption and retention metrics | Metrics | Continuous | |
| launch-pulse | launch-debrief | Actuals vs targets | Scorecard | T+30, T+90 | |
| growth-loop | demand-engine | Referral pipeline, case studies | Assets | Continuous | |
| growth-loop | signal-radar | Customer signals, advocacy data | Signals | Continuous | |
| launch-debrief | All skills | Updated benchmarks, learnings | Playbook | Post-launch | |
| flywheel-sync | All skills | Health report, improvement roadmap | Dashboard | Quarterly | |

### Step 2: Score Each Connection (Orchestration Audit)

For every connection in the matrix, score its health on a 0-3 scale.

**Connection Health Scale:**

| Score | Status | Definition | Indicators |
|-------|--------|-----------|------------|
| 0 | Broken | No data flows between skills | Output exists but is never consumed, or skill is not run |
| 1 | Degraded | Data flows but with issues | Wrong format, stale data, manual transfer required, partial coverage |
| 2 | Functioning | Data flows reliably with minor gaps | Mostly automated, occasional format mismatch, acceptable lag |
| 3 | Optimized | Seamless, timely, complete data flow | Fully automated handoff, correct format, consumed within SLA |

**Connection Audit Table:**

| # | Connection | Score (0-3) | Issues Found | Impact | Remediation |
|---|-----------|-------------|-------------|--------|-------------|
| 1 | signal-radar to battle-scanner | | | | |
| 2 | signal-radar to position-lock | | | | |
| 3 | battle-scanner to position-lock | | | | |
| 4 | battle-scanner to enablement-forge | | | | |
| 5 | position-lock to demand-engine | | | | |
| 6 | position-lock to enablement-forge | | | | |
| 7 | demand-engine to budget-allocator | | | | |
| 8 | demand-engine to launch-command | | | | |
| 9 | journey-architect to demand-engine | | | | |
| 10 | journey-architect to growth-loop | | | | |
| 11 | enablement-forge to launch-command | | | | |
| 12 | budget-allocator to launch-command | | | | |
| 13 | launch-command to launch-pulse | | | | |
| 14 | launch-pulse to growth-loop | | | | |
| 15 | launch-pulse to launch-debrief | | | | |
| 16 | growth-loop to demand-engine | | | | |
| 17 | growth-loop to signal-radar | | | | |
| 18 | launch-debrief to All skills | | | | |

**Overall Orchestration Health** = (Sum of connection scores) / (Number of connections x 3) x 100%

### Step 3: Redundancy and Gap Analysis

Identify outputs that overlap, outputs that are missing, and outputs that are produced but never consumed.

**Output Inventory:**

| Skill | Output | Consumed By | Status | Action Needed |
|-------|--------|-----------|--------|--------------|
| signal-radar | Market Signal Report | battle-scanner, position-lock | Active / Stale / Missing | |
| battle-scanner | Competitive Landscape | position-lock, enablement-forge | | |
| position-lock | Messaging Framework | demand-engine, enablement-forge, launch-command | | |
| demand-engine | Channel Strategy | budget-allocator, launch-command | | |
| journey-architect | Journey Map | demand-engine, growth-loop | | |
| enablement-forge | Sales Materials | launch-command, sales team | | |
| budget-allocator | Budget Model | launch-command | | |
| launch-command | Readiness Dashboard | launch-pulse, all teams | | |
| launch-pulse | Metrics Framework | growth-loop, launch-debrief | | |
| growth-loop | Health Scores | signal-radar, demand-engine | | |
| launch-debrief | Improvement Playbook | All skills (next cycle) | | |

**Classification Key:**

| Category | Definition | Risk | Action |
|----------|-----------|------|--------|
| Redundant | Two+ skills produce overlapping outputs | Confusion, wasted effort | Consolidate into single source of truth |
| Gap | Expected output is missing, no skill produces it | Blind spot, broken handoff | Assign to existing skill or create new output |
| Waste | Output is produced but no skill consumes it | Wasted effort | Deprecate or find consumer |
| Orphan | Skill needs input but no skill provides it | Manual workaround, delays | Create upstream dependency |

**Redundancy and Gap Findings:**

| # | Finding | Category | Affected Skills | Severity | Recommended Action |
|---|---------|----------|----------------|----------|-------------------|
| 1 | | Redundant/Gap/Waste/Orphan | | High/Med/Low | |
| 2 | | | | | |
| 3 | | | | | |

### Step 4: Bottleneck Identification

Score each skill as a potential bottleneck based on three factors.

**Bottleneck Scoring Model:**

| Skill | Delay Impact (1-10) | Quality Impact (1-10) | Confusion (1-10) | Bottleneck Score |
|-------|---------------------|----------------------|------------------|-----------------|
| signal-radar | | | | |
| battle-scanner | | | | |
| position-lock | | | | |
| demand-engine | | | | |
| journey-architect | | | | |
| enablement-forge | | | | |
| budget-allocator | | | | |
| launch-command | | | | |
| launch-pulse | | | | |
| growth-loop | | | | |
| launch-debrief | | | | |
| flywheel-sync | | | | |

**Bottleneck Score Formula:**

```
Bottleneck_Score = (Delay_Impact x 0.40) + (Quality_Impact x 0.35) + (Confusion x 0.25)
```

**Factor Definitions:**

| Factor | Weight | 1 (Low) | 5 (Medium) | 10 (High) |
|--------|--------|---------|-----------|-----------|
| Delay Impact | 40% | Skill runs on time, outputs delivered within SLA | Occasional delays, 1-2 week lag | Chronic delays, blocks downstream skills for 3+ weeks |
| Quality Impact | 35% | Outputs are complete, accurate, actionable | Occasional gaps or inaccuracies | Outputs frequently incomplete, require rework |
| Confusion | 25% | Clear ownership, well-understood process | Some ambiguity on who owns what | Teams unsure of process, frequent miscommunication |

**Bottleneck Classification:**

| Score Range | Classification | Action |
|------------|---------------|--------|
| 7.0 - 10.0 | Critical Bottleneck | Immediate intervention, process redesign, additional resourcing |
| 5.0 - 6.9 | Moderate Bottleneck | Optimization needed, SLA tightening, template improvement |
| 3.0 - 4.9 | Minor Friction | Monitor, address in next quarterly review |
| < 3.0 | Healthy | No action needed |

### Step 5: Tempo Alignment Check

Verify that each skill runs at the appropriate cadence relative to the business rhythm.

**Skill Tempo Map:**

| Skill | Recommended Cadence | Actual Cadence | Aligned? | Adjustment Needed |
|-------|-------------------|---------------|----------|------------------|
| signal-radar | Weekly scan, monthly deep dive | | Yes/No | |
| battle-scanner | Monthly update, per-launch refresh | | | |
| position-lock | Quarterly refresh, per-launch validation | | | |
| demand-engine | Per-launch build, monthly optimization | | | |
| journey-architect | Per-launch, annual strategic refresh | | | |
| enablement-forge | Per-launch, monthly asset refresh | | | |
| budget-allocator | Per-launch, monthly rebalancing | | | |
| launch-command | Per-launch (T-60 through T+30) | | | |
| launch-pulse | Per-launch setup, continuous monitoring | | | |
| growth-loop | Continuous, quarterly program review | | | |
| launch-debrief | T+30 and T+90 per launch | | | |
| flywheel-sync | Quarterly health check | | | |

**Tempo Misalignment Patterns:**

| Pattern | Symptom | Fix |
|---------|---------|-----|
| Too slow upstream, fast downstream | Downstream skills work with stale inputs | Increase upstream cadence or add trigger-based updates |
| Too fast upstream, slow downstream | Outputs pile up unconsumed | Batch upstream outputs or increase downstream cadence |
| Event-driven gap | Launch skills idle between launches | Add continuous improvement tasks between launches |
| Missing trigger | Skill should run but nothing initiates it | Add calendar trigger or upstream completion trigger |

### Step 6: Generate the Integration Health Dashboard

Compile all analyses into a single health view.

**System Health Summary:**

| Dimension | Score | Status | Trend | Top Issue |
|-----------|-------|--------|-------|-----------|
| Orchestration Health | /100% | Green/Yellow/Red | Up/Down/Flat | |
| Redundancy/Gap Score | /10 findings | | | |
| Bottleneck Score (avg) | /10 | | | |
| Tempo Alignment | /12 aligned | | | |
| Overall System Health | /100% | | | |

**Overall System Health Calculation:**

```
System_Health = (Orchestration_Health x 0.35) + (Gap_Score_Inverse x 0.25)
             + (Bottleneck_Score_Inverse x 0.25) + (Tempo_Alignment x 0.15)
```

**Critical Path Identification:**
Map the longest dependency chain through the skill graph and identify which skills are on the critical path for each launch.

| Critical Path Step | Skill | Duration | Slack | On Critical Path? |
|-------------------|-------|----------|-------|------------------|
| 1 | signal-radar | Ongoing | N/A | Yes (foundation) |
| 2 | battle-scanner | 2 weeks | 1 week | Yes |
| 3 | position-lock | 3 weeks | 0 | Yes (bottleneck risk) |
| 4 | demand-engine | 2 weeks | 1 week | Yes |
| 5 | budget-allocator | 1 week | 2 weeks | No |
| 6 | launch-command | 8 weeks (T-60 to T-0) | 0 | Yes (controls timeline) |
| 7 | launch-pulse | 2 weeks setup | 1 week | Yes |
| 8 | growth-loop | Continuous post-launch | N/A | No (parallel) |
| 9 | launch-debrief | T+30 | 2 weeks | No (post-launch) |

### Step 7: Build the Continuous Improvement Roadmap

Prioritize all identified issues into a phased improvement plan.

**Improvement Roadmap:**

| Phase | Timeline | Focus | Key Actions | Success Metric |
|-------|---------|-------|-------------|---------------|
| Quick Wins | Next 2 weeks | Fix broken connections (score 0-1) | Repair data flows, create missing templates | All connections >= 1 |
| Optimize | Next 30 days | Reduce bottlenecks, align tempo | Process redesign for top 2 bottlenecks | Avg bottleneck score < 5.0 |
| Integrate | Next 60 days | Eliminate gaps and redundancies | Consolidate overlapping outputs, fill gaps | Zero critical gaps |
| Automate | Next 90 days | Systematize handoffs and triggers | Automated triggers between skills, SLA monitoring | Orchestration health >= 80% |
| Scale | Ongoing | Continuous improvement culture | Quarterly flywheel-sync reviews, feedback loops | System health >= 85% |

## Output

Save to `outputs/flywheel-sync/`

### Deliverables:
1. **System Health Dashboard** -- Overall system health percentage, orchestration health, gap/redundancy count, average bottleneck score, tempo alignment, and critical path identification with visual dependency map
2. **Gap and Redundancy Report** -- Every output classified as active, redundant, gap, waste, or orphan with recommended consolidation, creation, or deprecation actions
3. **Bottleneck Analysis** -- Every skill scored on delay impact, quality impact, and confusion with bottleneck classification (Critical/Moderate/Minor/Healthy) and specific remediation plans
4. **Continuous Improvement Roadmap** -- Phased plan (Quick Wins through Scale) with timeline, key actions, success metrics, and owners for each improvement initiative

## Chain Connections
- **Receives from:** All skills (outputs, timing data, quality feedback, connection health signals)
- **Feeds back into:** All skills (health assessments, improvement priorities, tempo recommendations, integration fixes)
- **Enhanced by:** launch-debrief (systemic patterns across launches), launch-command (critical path data), signal-radar (external timing pressures)
