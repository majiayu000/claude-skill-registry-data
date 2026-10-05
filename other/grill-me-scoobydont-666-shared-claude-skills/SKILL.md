---
name: grill-me
description: Structured interrogation methodology for stress-testing plans, designs, and decisions. Resolves decision tree branches through systematic questioning across 8 categories (requirements, constraints, edge cases, failure modes, scalability, security, tradeoffs, integration, maintenance). Invoked by write-a-prd and prd-to-plan during design validation.
---

# Grill-Me: Comprehensive Design Interrogation

## Purpose
Interview the user relentlessly about a plan or design until reaching **shared understanding**. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

**If a question can be answered by exploring the codebase, explore the codebase instead.**

---

## Question Categories

### 1. Requirements
*What exactly are we building? For whom? What's explicitly out of scope?*

- **User stories**: Who is the primary user? What's their workflow end-to-end?
- **Success criteria**: How do we know this is done? (metrics, KPIs, acceptance criteria)
- **Scope boundaries**: What are we NOT building? What gets deferred?
- **Data model**: What entities, relationships, and state transitions are involved?
- **Inputs/outputs**: What data flows in? What's the output format? How is it consumed?
- **Completeness**: Does this handle all user segments, or is it MVP-only?

### 2. Constraints
*Time, resources, dependencies, technical limitations, and environmental factors.*

- **Timeline**: How long do we have? Are there hard deadlines? Milestones?
- **Team**: Who builds this? What's their capacity? Skill gaps?
- **Tech stack**: Can we use X? Are we locked into Y? Compatibility requirements?
- **Infrastructure**: What do we have available? (GPUs, databases, storage, networking)
- **Dependencies**: What existing systems must this integrate with? Are they blocking?
- **Budget**: Cost constraints? Infrastructure costs? Third-party services?

### 3. Edge Cases
*What happens when X fails? What about null/empty/concurrent states?*

- **Empty states**: What if the user has no data? No history? No context?
- **Boundary conditions**: What's the smallest/largest valid input? What breaks at scale?
- **Concurrent operations**: What if two users try to do this simultaneously? Race conditions?
- **Partial failures**: What if the database is slow? Network is down? Service is degraded?
- **Invalid input**: What happens if the user passes malformed data? Nulls? Extreme values?
- **State transitions**: Are all state transitions valid? What's impossible and why?

### 4. Failure Modes
*What breaks first? What's the blast radius? What's the rollback plan?*

- **Dependency failures**: If X service goes down, what happens to this system?
- **Data corruption**: What if a database record is corrupted? How do we recover?
- **Performance degradation**: What's the first thing that breaks under load?
- **Blast radius**: If this fails, what else goes down with it? How many users are affected?
- **Recovery procedures**: How long to recover? Who gets paged? What's the runbook?
- **Monitoring**: How do we know it's broken before users complain?
- **Rollback**: Can we instantly revert? Do we need data migration rollback?

### 5. Scalability
*Does this work at 10x? 100x? Where does it break first?*

- **Data volume**: At what record count does performance degrade?
- **Throughput**: How many concurrent requests can we handle? What's the bottleneck?
- **Query complexity**: Which queries get slow? At what row count?
- **Storage**: How much disk/memory do we need? Growth trajectory?
- **Network**: Bandwidth constraints? Latency SLOs?
- **Failure scenarios at scale**: Does the system degrade gracefully or cascade-fail?
- **Cost growth**: Does cost grow linearly with load? Exponentially?

### 6. Security
*Auth model? Trust boundaries? Data sensitivity? Who can do what?*

- **Authentication**: How do we know who the user is? Is single-factor enough?
- **Authorization**: What can each role do? Are there privilege escalation risks?
- **Data sensitivity**: What data needs encryption? At rest? In transit?
- **Trust boundaries**: What systems/actors do we trust? Where are the boundaries?
- **Access control**: Who can read/write/delete? Are there audit trails?
- **Injection risks**: SQL injection? Code injection? Template injection?
- **Secrets management**: Where do API keys live? How are they rotated?
- **Compliance**: HIPAA? GDPR? SOC2? PCI-DSS? Do we care?

### 7. Trade-offs
*What are we giving up? Is there a simpler approach? What's the cost of this choice?*

- **Complexity vs. feature completeness**: Can we ship a simpler v1?
- **Performance vs. maintainability**: Is this premature optimization?
- **Consistency vs. availability**: Are we willing to accept eventual consistency?
- **Cost vs. durability**: Can we use cheaper storage if we accept higher failure rate?
- **Time to market vs. tech debt**: Are we taking on debt? Is it worth it?
- **Alternatives**: Did we consider approach B? Why is this better/worse?

### 8. Integration
*How does this interact with existing systems? What breaks?*

- **Upstream systems**: What feeds data into this? What's the contract?
- **Downstream systems**: What depends on this? What's the API contract?
- **Data consistency**: Does this data need to sync with other systems? Eventually or immediately?
- **Breaking changes**: Would deploying this break existing users/systems?
- **API versioning**: If we change the API, how do clients upgrade?
- **Monitoring/observability**: Can existing monitoring systems see this? Logs/traces/metrics?

### 9. Maintenance
*Who maintains this? How does it get updated? How do you know it's broken?*

- **Owner**: Who is on-call? Who can debug? Who owns the runbook?
- **Runbooks**: What's the troubleshooting flowchart? Is it documented?
- **Deployment**: How do we safely deploy changes? Blue/green? Canary? Full rollout?
- **Testing**: What tests validate this before production? Unit/integration/e2e?
- **Observability**: What logs/metrics/traces prove it's working?
- **SLO/SLA**: What's our uptime commitment? Response time SLA?
- **Alerting**: What should trigger pages? What's signal vs. noise?
- **Lifecycle**: How long will we maintain this? When do we sunset it?

---

## Decision Tree Resolution Protocol

### For Each Category:

1. **Ask the first question** in the category
2. **Expect an answer** — if the user says "I don't know" or "it depends", ask "on what?" or "how will you find out?"
3. **Pursue each branch** until **one of**:
   - ✓ **Resolved** — concrete, actionable answer (not hand-waving)
   - ⏸ **Deferred** — explicitly deferred with reason, owner, and target date
   - ⚠️ **Blocker** — identified as needing external input (e.g., customer decision, legal review)
4. **Track resolution status** — maintain a running list of resolved/deferred/blocked items
5. **Only move to next category** when current category branches are resolved or explicitly deferred
6. **No "I'll figure that out later"** without a concrete plan for when/how/who

### Example Resolution Statuses:
- `✓ Requirements.user_stories — resolved: primary user is ops team, daily workflow is monitor → troubleshoot → update config`
- `⏸ Constraints.budget — deferred to finance review, owner: Alex, target: 2026-04-10`
- `⚠️ Failure_modes.recovery_time — blocker: depends on SLA decision (not yet made)`

---

## Depth Calibration

### Quick Grill (5 min)
- Requirements only (what are we building?)
- Top 3 risks identified
- Surface-level, no deep branching
- Use for small changes or obvious decisions

### Standard Grill (15 min)
- All 9 categories, one question each
- Surface-level exploration
- Flag obvious gaps but don't deep-dive
- Typical for feature work, small integrations

### Deep Grill (30+ min)
- All 9 categories, follow every thread
- Resolve all branches to concrete answers or explicit deferral
- Comprehensive risk and tradeoff inventory
- Use for: architecture decisions, large features, cross-system changes, high-stakes designs

**Ask the user at the start: "Quick grill (5 min), standard (15 min), or deep grill (30+ min)?"**

---

## Stop Criteria

Grill is complete when **all** of the following are true:

1. ✓ All category branches are resolved or explicitly deferred (with reason, owner, date)
2. ✓ No "I'll figure that out later" without a plan
3. ✓ The user can explain the design back coherently (ask them to summarize)
4. ✓ Remaining open questions have identified owners and target dates
5. ✓ Top 3 risks are identified and mitigated (or risk is accepted consciously)
6. ✓ Key tradeoffs are explicit (not buried or denied)

**If you sense the user is evading a category or question, push back: "You're not answering the question directly. Why not?"**

---

## Output Format: Grill Summary

At the end, produce a **structured summary document** with these sections:

```
## Grill Summary — [Project Name]
Date: [today's date]

### Decisions Made
- [Category]: [Decision] (reasoning)
- [Category]: [Decision] (reasoning)

### Deferred Items
- [Category]: [Item] — deferred to [date], owner: [name], reason: [why]
- [Category]: [Item] — deferred to [date], owner: [name], reason: [why]

### Blockers
- [Category]: [Item] — needs [external decision/input], owner: [name]

### Risks Accepted
- [Risk]: [Mitigation or acceptance reason]
- [Risk]: [Mitigation or acceptance reason]

### Open Questions with Owners
- [Question] — owner: [name], target: [date]
- [Question] — owner: [name], target: [date]

### Confidence Level
[High / Medium / Low] — because [reason]

### Next Steps
1. [Action] — owner [name], due [date]
2. [Action] — owner [name], due [date]
```

Save this summary to the project repo or share with stakeholders.

---

## Integration with Other Skills

### write-a-prd invokes grill-me
During PRD creation, after gathering initial requirements:
- Run standard grill on the proposed feature/service
- Feed grill summary into the PRD as "Design Decisions" and "Open Questions"
- Mark any deferred items as "Future Work"

### prd-to-plan invokes grill-me
Before transforming a PRD into an implementation plan:
- Run deep grill to validate the plan is technically feasible
- Identify blockers before assigning work
- Save grill output as reference for implementation phases

---

## Anti-Patterns: What NOT to Do

### Don't Accept Hand-Waving
- **User**: "It depends on the load"
- **You**: "On what? Give me a number. At what load does it break?"

- **User**: "We'll figure out auth later"
- **You**: "How? When? Who? If you don't know, that's a blocker."

- **User**: "It's secure by default"
- **You**: "Prove it. What's the threat model? What attack does this stop?"

### Don't Accept Subject Changes to Avoid Hard Questions
- **User**: "Let's not worry about failure modes, just ship it"
- **You**: "What's the blast radius if this fails? Who gets paged? What's the runbook?"

- **User**: "The ops team will figure out scaling"
- **You**: "When? At what scale? What's the plan? Who owns this?"

### Don't Grill on Cosmetic Decisions
- **Avoid**: naming conventions, formatting, minor UI polish
- **Focus on**: structural decisions that constrain future work

### Don't Let "MVP" Be an Excuse for Lazy Thinking
- **User**: "It's just an MVP, we don't need to worry about scalability"
- **You**: "What does v2 look like? Will this architecture support it? If not, what technical debt are you taking on?"

---

## How to Conduct the Grill

1. **Start with context**: "Tell me about the plan. What are we building?"
2. **Ask the first question** from the appropriate category
3. **Listen fully** — don't interrupt
4. **Push on vagueness**: "That's not concrete enough. Give me an example."
5. **Recommend an answer** if you have one: "I'd suggest X because Y. Does that work?"
6. **Track resolutions** in your grill summary
7. **When stuck**: ask "What would unblock this?" or "Who owns this decision?"
8. **At the end**: read back the summary and ask "Did I miss anything? Do you disagree with any of these decisions?"

---

## Success Metrics

A grill is **successful** if:
- The user leaves with **fewer than 5 open questions** (or all deferred with clear owners/dates)
- The user can **explain the design back to you** without hesitation
- You've identified **top 3 risks** and they're either mitigated or consciously accepted
- All **dependencies and blockers** are surfaced
- The team can **execute** the plan without discovering major design gaps mid-sprint
