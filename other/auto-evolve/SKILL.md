---
name: auto-evolve
description: Use when continuously monitors system performance identifies improvement
  opportunities and orchestrates find-skills and create-skills to autonomously evolve
  capabilities. The brain of the self-evolving system. Use when working with auto
  evolve.
domain: meta
author: oyi77
license: Apache-2.0
subdomain: meta-skills
tags:
- auto
- evolve
- meta-learning
- self-improvement
- skill-evolution
version: 1.0.0
category: meta
---

persona:
  name: "Charles Darwin"
  title: "The Evolution Architect - Master of Continuous Adaptation"
  expertise: ['System Evolution', 'Performance Optimization', 'Gap Analysis', 'Orchestration', 'Natural Selection of Skills']
  philosophy: "It is not the strongest of the species that survives nor the most intelligent but the one most responsive to change. My mission: ensure the system never stops improving."
  credentials: ['Theory of Evolution by Natural Selection', 'Systematic observation and analysis', 'Pioneer of adaptive systems thinking']
  principles: ['Monitor everything measure improvement', 'Find or create what is missing', 'Validate before deploying', 'Rollback on failure', 'Never break what works']

# Auto-Evolve - Continuous Self-Improvement Orchestrator

## Overview

The **brain** of the self-evolving system. Continuously monitors performance identifies gaps orchestrates skill discovery and creation and ensures quality. Like natural selection - the system adapts to survive and thrive.

**Single install then evolving** - the system gets smarter every day without human intervention!


## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I'll figure it out as I go" | A structured approach saves time and reduces errors. Follow the workflow in this skill rather than improvising. |
| "I already know this topic" | Familiarity breeds shortcuts. Use the checklist to verify you haven't missed critical steps. |
| "This doesn't apply to my situation" | The patterns here generalize across contexts. Adapt, don't skip — the underlying principles hold. |
| "One more tool will fix it" | Adding complexity rarely solves process gaps. Master the core workflow first. |

## When to Use
**Trigger phrases:**
- "auto evolve"
- "Continuously monitors system performance identifies improvement opportunities an"


**Automatic Activation** when:
- System performance degrades or gaps appear
- User requests cant be fulfilled by existing skills
- New domains or use cases emerge
- Scheduled evolution cycles (daily/weekly)
- User explicitly says "evolve" or "improve system"
- Meta-skills report improvement opportunities

## When NOT to Use

- System is stable and performing well (no issues detected)
- Less than 1 hour since last evolution cycle (cooldown)
- Critical operations in progress (avoid disruption)
- User explicitly disables auto-evolution

## The 7-Step Evolution Process
1. Validate input and check prerequisites
2. Initialize required connections and contexts
3. Execute core operation with monitoring
4. Validate output against expected format
5. Deliver results and log execution summary


### Step 1: Monitor System

Collect comprehensive system health data:

1. Get performance metrics from meta/performance-monitor
   - Response times success rates error rates
   - Token usage and cost efficiency
   - Skill utilization patterns
2. Get user feedback from meta/feedback-collector
   - Common pain points
   - Feature requests
   - Satisfaction scores
3. Get skill usage data from meta/auto-learner
   - Most/least used skills
   - Failed skill activations
   - Capability gaps (requests that matched no skill)
4. Get self-assessment from meta/self-assessment
   - Quality scores per skill
   - Known weaknesses
   - Improvement opportunities

### Step 2: Identify Opportunities

Analyze collected data to find improvement opportunities:

- **Performance gaps**: Skills that are slow or error-prone
- **Capability gaps**: User needs not covered by any skill
- **Quality gaps**: Skills with low satisfaction scores
- **Usage gaps**: Often-requested but rarely-successful skills
- **Integration gaps**: Skills that should work together but dont

Prioritize by impact:
1. High impact + easy fix = DO NOW
2. High impact + hard fix = PLAN
3. Low impact + easy fix = QUEUE
4. Low impact + hard fix = SKIP

### Step 3: Create Evolution Plan

Generate a structured plan for each opportunity:

For each opportunity:
1. Define the desired outcome
2. Identify which meta-skill should handle it
3. Determine dependencies and order
4. Set validation criteria
5. Estimate risk level
6. Create rollback plan

Maximum 5 changes per cycle to minimize risk.

### Step 4: Execute Find Phase

For each capability gap in the plan:

1. Delegate to meta/find-skills
2. Search for existing community solutions
3. If found and credible (score > 70):
   - Install existing skill
   - Skip generation
4. If not found:
   - Proceed to Create phase

### Step 5: Execute Create Phase

For gaps where no existing skill was found:

1. Delegate to meta/create-skills
2. Generate new skill based on requirements
3. Validate quality (must score > 85)
4. If quality too low: retry up to 3 times
5. If still failing: log and skip this cycle

### Step 6: Validate and Deploy

Before any changes go live:

1. Run all quality checks:
   - Structure validation (all sections present)
   - Content quality (no filler actionable clear)
   - Lint pass (no markdown errors)
   - Integration test (works with related skills)
   - Safety check (no breaking changes)
2. If ALL checks pass:
   - Deploy changes
   - Update activation rules
   - Notify system of new capabilities
3. If ANY check fails:
   - DO NOT deploy
   - Log failure details
   - Schedule for next cycle with fixes

### Step 7: Report and Learn

After each evolution cycle:

1. Generate evolution report:
   - Opportunities identified (count and types)
   - Actions taken (installed created improved)
   - Quality scores (per change)
   - Deployment status (success/failure)
   - Impact assessment (before/after metrics)
2. Feed back to meta/auto-learner:
   - What worked well
   - What failed and why
   - Patterns to remember
   - Strategies to avoid
3. Update meta/performance-monitor:
   - New baseline metrics
   - Improvement tracking
   - Trend analysis
4. Save report to auto-evolve/reports/
5. Log complete audit trail to auto-evolve/logs/

## Integration with All Meta-Skills
- Connects with existing toolchain via standard interfaces
- Supports webhook-based event notifications
- Compatible with CI/CD pipelines for automated workflows
- Provides structured output for downstream consumption


### Core Orchestration Flow

```
auto-evolve (orchestrator)
  |
  +-- meta/performance-monitor (data collection)
  +-- meta/feedback-collector (user signals)
  +-- meta/auto-learner (pattern memory)
  +-- meta/self-assessment (quality baseline)
  |
  +-- meta/find-skills (discover existing)
  +-- meta/create-skills (generate new)
  +-- meta/improvement-generator (enhance existing)
  |
  +-- meta/pattern-recognition (cross-domain insights)
  +-- meta/meta-orchestrator (coordinate all meta)
  +-- meta/data (structured storage)
```

### Integration Detail

| Meta-Skill | Role in Evolution | When Called |
|------------|------------------|------------|
| performance-monitor | Collect metrics | Every cycle Step 1 |
| feedback-collector | Gather user signals | Every cycle Step 1 |
| auto-learner | Remember patterns | Every cycle Step 7 |
| self-assessment | Quality baseline | Every cycle Step 1 |
| find-skills | Discover existing | Step 4 (find phase) |
| create-skills | Generate new | Step 5 (create phase) |
| improvement-generator | Enhance existing | When quality gaps found |
| pattern-recognition | Cross-domain insights | Step 2 (opportunity ID) |
| meta-orchestrator | Coordinate complex flows | Multi-skill operations |
| skill-evolution | Track skill versions | Step 6 (deploy) |
| data | Store structured results | All steps |

## Safety Configuration

```json
{
  "evolutionInterval": "daily",
  "maxChangesPerCycle": 5,
  "qualityThreshold": 90,
  "cooldownMinutes": 60,
  "autoDeploy": false,
  "safetyChecks": {
    "breakingChangeDetection": true,
    "rollbackOnFailure": true,
    "userReviewRequired": true,
    "malwareScan": true,
    "secretDetection": true
  },
  "rollback": {
    "enabled": true,
    "maxSnapshots": 10,
    "autoRollbackOnFailure": true
  },
  "notification": {
    "onCycleComplete": true,
    "onDeployment": true,
    "onFailure": true,
    "logLevel": "detailed"
  }
}
```

## Examples
```
# Basic usage
invoke <skill-name> with appropriate parameters

# Advanced usage with options
invoke <skill-name> --option value --verbose
```


### Example 1: Daily Evolution Cycle

auto-evolve daily cycle triggered:
1. Monitor: 3 skill gaps detected (podcast linkedin k8s)
2. Identify: podcast=high impact linkedin=medium k8s=high
3. Plan: 3 actions max 5 per cycle
4. Find: linkedin-outreach exists (score 82) - install it
5. Create: ai-podcast generated (score 88) k8s-deploy generated (score 91)
6. Validate: All pass quality threshold 90
7. Report: 3 gaps filled 2 created 1 installed 100% success

### Example 2: Performance-Driven Evolution

auto-evolve detects: email-marketing skill has 40% error rate
1. Monitor: email-marketing failing on template rendering
2. Identify: Performance gap in email-marketing
3. Plan: Improve email-marketing skill
4. Delegate to improvement-generator
5. Enhanced skill reduces error rate to 5%
6. Validate: Quality score improved from 65 to 89
7. Report: Error rate reduced 40% to 5%

### Example 3: User Feedback-Driven Evolution

auto-evolve collects: 8 users requested "YouTube shorts creation"
1. Monitor: Recurring feature request from feedback-collector
2. Identify: Capability gap for YouTube shorts
3. Plan: Find or create YouTube shorts skill
4. Find: No existing skill with score above 70
5. Create: youtube-shorts skill generated (score 86)
6. Validate: Passes all safety checks
7. Report: New capability added based on user demand

## Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| Operation times out | Network or service issue | Check connectivity and retry |
| Permission denied | Missing credentials | Verify API keys and access tokens |
| Invalid output | Input format mismatch | Validate input against expected schema |


### Evolution cycle too slow
- Reduce maxChangesPerCycle
- Use async operations for parallel actions
- Cache frequently accessed data
- Skip low-impact opportunities

### Too many failures in a cycle
- Lower qualityThreshold temporarily
- Check network connectivity for find-skills
- Review create-skills template selection
- Enable autoRollbackOnFailure

### Breaking changes detected
- DO NOT deploy - safety first
- Review change impact analysis
- Create compatible version instead
- Add deprecation path for old behavior

### System not improving
- Check monitoring data quality
- Verify feedback collection is working
- Ensure find-skills API endpoints are reachable
- Review auto-learner recommendations

### Evolution loop detected
- Check cooldownMinutes setting
- Verify change limits per cycle
- Review opportunity prioritization logic
- Add deduplication for repeated suggestions

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll do this later" | Explain why this excuse is wrong for this skill |
| "This is simple, skip steps" | Even simple tasks benefit from process |

## Red Flags

- Evolution targets are selected without measuring current performance baseline
- Agent does not validate that evolved skills maintain backward compatibility
- Watch for shortcuts and skipped steps

## Verification

After completing this skill, confirm:

- [ ] Performance baseline is measured before evolution
- [ ] Backward compatibility is verified for evolved skills
- [ ] All required outputs generated
- [ ] Success criteria met

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality
