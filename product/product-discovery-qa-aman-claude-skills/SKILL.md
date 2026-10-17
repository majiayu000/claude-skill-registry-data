---
name: product-discovery
description: >
  Run product discovery to identify what to build. Use when the user says "product discovery",
  "how do I know what to build", "validate this idea", "talk to customers",
  "are we building the right thing", "discovery process", or wants to reduce the risk
  of building something users don't want - even if they don't say "discovery".
---

## Overview

Based on **Inspired** by Marty Cagan (Silicon Valley Product Group). Cagan's central argument: the biggest risk in product is not execution risk - it's value risk (will users buy it?), usability risk (can users figure it out?), feasibility risk (can we build it?), and business viability risk (does it work for the business?). Discovery is how you tackle all four before writing a line of code.

The best product teams run discovery and delivery in parallel. Discovery is not a phase - it's a continuous habit.

## Workflow

### Step 1: Identify the four risks
For the idea or problem at hand, assess:
- **Value risk** - Do users actually want this? Will they use it?
- **Usability risk** - Will users understand how to use it?
- **Feasibility risk** - Can the team build it with current skills and tech?
- **Viability risk** - Does it work legally, financially, and ethically for the business?

Rate each: High / Medium / Low. Focus discovery on High risks.

### Step 2: Frame the opportunity (not the solution)
State the problem as an opportunity: "Users struggle to [X], which causes [Y impact]."
Avoid framing as a solution at this stage. Mocking up a solution before validating the problem is the most common discovery failure.

### Step 3: Run customer interviews (Value risk)
Goal: understand the problem deeply, not validate your solution.
- Talk to 5-8 users in the target segment
- Ask about their current behavior, not hypothetical preferences
- "What do you do today when [problem occurs]?" not "Would you use a feature that does X?"
- Look for patterns across interviews, not individual quotes

### Step 4: Run usability tests (Usability risk)
With a prototype (even paper):
- Give users a task, watch silently
- Don't explain how it works - if they can't figure it out, that's the data
- 5 users reveal ~85% of usability issues (Nielsen's law)

### Step 5: Validate feasibility with engineering (Feasibility risk)
Before committing: one-hour spike with the tech lead.
- "Is this technically possible in our appetite?"
- "What's the hardest part?"
- Surface blockers early, not after the PRD is written.

### Step 6: Check viability (Business risk)
- Legal: any compliance, privacy, or IP issues?
- Finance: does the unit economics work?
- Marketing: can we explain this clearly?
- Sales: does this help or hurt existing deals?

### Step 7: Decide: persevere, pivot, or kill
Based on discovery findings:
- **Persevere** - risks are manageable, move to shaping
- **Pivot** - problem is real but solution needs rethinking
- **Kill** - problem is smaller than assumed or solution isn't viable

## Anti-Patterns

**1. Validating solutions instead of discovering problems**
Bad: "We showed users our mockup and they said they liked it."
Good: Users are polite. Test behavior, not opinion. "5 out of 5 users completed the task without prompting" is evidence. "They said it looked great" is not.

**2. Discovery as a one-time phase**
Bad: "We did discovery in Q1, now we're in delivery mode."
Good: Discovery never stops. Run continuous weekly interviews even during delivery.

**3. PMs doing discovery alone**
Bad: PM interviews customers, reports findings to the team.
Good: Cagan's "product trio" - PM, designer, and tech lead attend discovery together. Shared understanding beats written summaries.

**4. Skipping feasibility until spec is written**
Bad: Beautiful PRD handed to engineering that has a fundamental technical blocker.
Good: 1-hour feasibility spike before any spec writing.

## Quality Checklist

- [ ] All four risks assessed (value, usability, feasibility, viability)
- [ ] Problem framed as opportunity, not solution
- [ ] Customer interviews focused on behavior, not opinion
- [ ] Usability tested with prototype (not described, tested)
- [ ] Feasibility checked with tech lead before spec
- [ ] Clear decision: persevere, pivot, or kill
