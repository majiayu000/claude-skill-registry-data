---
name: auto-learner
description: Use when autonomous learning from execution data. Skills improve themselves
  by identifying patterns in successful vs failed executions without human intervention.
  Use when working with auto learner.
domain: meta
author: oyi77
license: Apache-2.0
subdomain: meta-skills
tags:
- auto
- learner
- meta-learning
- self-improvement
- skill-evolution
persona:
  name: Autonomous Learner
  expertise: Machine learning, pattern recognition, self-supervision
  philosophy: Learn by doing, improve by reflecting
version: 1.0.0
category: meta
---


# Auto Learner

## When to Use

**Trigger phrases:**
- "auto learner"
- "Help me with auto learner"

**Use cases:**
- When the task matches this skill's domain expertise

**When NOT to use:**
- For tasks outside this skill's scope

/auto-learner enable --skill seo-optimizer

# Trigger learning cycle
/auto-learner learn --skill seo-optimizer --min-samples 100

# View learned improvements
/auto-learner status --skill seo-optimizer
```

### Learning Triggers

- After 100 executions
- When success rate drops below threshold
- When new error patterns emerge
- On user request
- Scheduled daily/weekly

### Safety

- Changes are staged, not immediate
- Human approval required for major changes
- Rollback always available
- Tests must pass before deployment


## When NOT to Use

- When the skill is stable and not changing
- For skills with fewer than 10 invocations (not enough data)
- When manual curation produces better results


## Overview

Auto Learner is a foundational meta-skills skill that provides skill management capabilities for the agent ecosystem.

## Architecture

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for skill management
- **Output layer** — Formats and delivers results
- **State management** — Maintains context across invocations

## Configuration

- Set up required environment variables and paths
- Configure logging level and output format
- Define resource limits (memory, time, API calls)
- Enable/disable features via configuration flags

## Integration

- Exposes standard interfaces for other skills to consume
- Supports event-driven and request-response patterns
- Compatible with the 1ai-skills hook system
- Logs metrics for the skill performance monitor

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Skills do not need to evolve" | Static skills become outdated. Self-evolving skills improve continuously. |
| "Manual skill management is fine" | With 1000+ skills, manual management is impossible. Automate. |
| "Performance does not matter" | Skill performance directly impacts agent effectiveness. Track it. |


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run auto learner workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings
## Verification Checklist

- [ ] Learning cycle completes without errors
- [ ] Pattern detection accuracy > 80%
- [ ] Generated improvements are specific and actionable
- [ ] No regression in skill performance after updates
- [ ] Audit trail maintained for all auto-generated changes
