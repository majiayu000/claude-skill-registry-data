---
name: devils-advocate
description: Challenge and stress-test ideas through adversarial thinking. Use when user wants to "poke holes", "challenge this", "what could go wrong", "devil's advocate", "stress test", "red team", "pre-mortem", "review this", "validate", "audit", or needs to find weaknesses before they become problems. (project)
allowed-tools: Read
---

# Devil's Advocate - Idea Stress-Tester

Challenge ideas rigorously to find weaknesses before reality does. Better to break it in the lab than in production.

## Critical Quality Gate

This skill is **essential for reviewing completed work**—not just plans. Use it to:
- **Review implementations** before they ship
- **Validate architectures** after design, before and after build
- **Challenge deliverables** before handoff
- **Audit decisions** that have already been made

**Core skill for:** [[Architect]] (validates technical decisions) and [[Analyst]] (challenges market assumptions). Both personas rely on devil's advocate as their primary quality mechanism.

## Core Principle

**Break it in the lab, not in production.** Challenge completed work before shipping—surviving ideas emerge stronger.

## Quick Start

1. Identify the idea, plan, or decision to stress-test
2. Select technique based on what you're testing
3. Attack ruthlessly, then use insights to strengthen

## Technique Selection

| Need | Use | Why |
|------|-----|-----|
| Find vulnerabilities in a plan | Red Team / Blue Team | Adversarial attack-and-defend cycle |
| Prevent project failure | Pre-mortem Analysis | Work backward from imagined failure |

**Default**: Start with Pre-mortem for plans, Red Team for designs/systems.

## Techniques

### Red Team / Blue Team
Adversarial analysis where one side attacks and the other defends. Find vulnerabilities through simulated opposition.

Read [cookbook/red-team-blue-team.md](./cookbook/red-team-blue-team.md)

### Pre-mortem Analysis
Imagine the project has failed, then work backward to identify what went wrong. Prevent failure by predicting it.

Read [cookbook/pre-mortem.md](./cookbook/pre-mortem.md)

## Guidelines

1. **Attack genuinely** - Half-hearted challenges don't find real weaknesses
2. **Separate creation from critique** - Don't devil's advocate while brainstorming
3. **Critique the idea, not the person** - This is about improving outcomes
4. **Document vulnerabilities** - Findings are valuable even if uncomfortable
5. **End with action** - Every weakness found should lead to mitigation

## When Devil's Advocate Works Best

**Before implementation:**
- Plans feel "too certain" or "obviously right"
- High-stakes decisions with limited reversibility
- Technical designs before implementation
- Strategies before major investment

**After implementation (reviewing completed work):**
- Code reviews for critical systems
- Architecture validation before release
- Post-implementation audits
- Deliverable review before stakeholder handoff
- "Is this actually ready?" gut-check moments

**Always applicable:**
- When you keep avoiding hard questions
- When everyone agrees too quickly

## Warning Signs You Need This

- "What could possibly go wrong?"
- "Everyone agrees this is perfect"
- "We don't need to think about failure"
- "Let's not be negative"
- Team avoids raising concerns

## The Right Mindset

Devil's advocate is an act of care, not negativity. You're protecting the team from future pain by finding problems now when they're cheap to fix.

The goal is never to kill ideas - it's to make surviving ideas stronger.
