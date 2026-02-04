---
name: ops
description: Operations engine for ID8Labs. Build systems that run without consuming you. Document, automate, delegate - in that order.
version: 1.0.0
mcps: [Supabase]
subagents: [operations-manager]
skills: []
---

# ID8OPS - Operations Engine

## Purpose

Build systems that run without you. Operations isn't about working harder—it's about working once and letting systems do the rest.

**Philosophy:** If you do it twice, document it. If you do it ten times, automate it. If it takes more than an hour, delegate it.

---

## When to Use

- Product is stable and needs operational rigor
- User is drowning in repetitive tasks
- User asks "how do I not be the bottleneck?"
- User needs to document processes
- User is thinking about hiring
- Project is in GROWING or OPERATING state

---

## Commands

### `/ops <project-slug>`

Run full operations audit and systematization.

**Process:**
1. AUDIT - Identify recurring work
2. SYSTEMATIZE - Document processes
3. AUTOMATE - Script what can be scripted
4. DELEGATE - Hand off what can't be automated
5. MEASURE - Track operational health
6. OPTIMIZE - Improve continuously

### `/ops audit`

Audit current operations for systematization opportunities.

### `/ops sop <process-name>`

Create a Standard Operating Procedure document.

### `/ops delegate <task>`

Create delegation framework for a specific task.

### `/ops playbook`

Generate comprehensive operations playbook.

---

## Operations Philosophy

### Solo Builder Reality

| Stage | Operations Focus |
|-------|------------------|
| Building | Minimal - focus on product |
| Launching | Essential checklists only |
| Growing | Document critical paths |
| Scaling | Systematize everything |

### The Operations Ladder

```
Level 1: Chaos
Everything in your head
You are the system

Level 2: Documentation
Processes written down
Others could follow them

Level 3: Automation
Scripts handle routine work
You review outputs

Level 4: Delegation
Others own processes
You set direction

Level 5: Organization
Systems run systems
You focus on strategy
```

**Goal:** Move up the ladder. Most solo builders stay at Level 1 too long.

---

## Process Detail

### Phase 1: AUDIT

**Identify all recurring work:**

| Task | Frequency | Time/Occurrence | Weekly Hours | Category |
|------|-----------|-----------------|--------------|----------|
| {task} | {daily/weekly} | {X min} | {X hrs} | {ops/support/dev} |

**Categories:**
- **Customer Support** - Answering questions, issues
- **Operations** - Billing, admin, maintenance
- **Marketing** - Content, social, outreach
- **Development** - Bug fixes, features
- **Strategy** - Planning, decisions

**Analysis:**
- Which tasks consume most time?
- Which are repetitive and predictable?
- Which require your unique skills?
- Which could someone else do?

### Phase 2: SYSTEMATIZE

**For each recurring task, create an SOP:**

```markdown
## SOP: {Task Name}

### Purpose
Why this task exists and what it achieves.

### Trigger
When to perform this task.

### Steps
1. Step one (be specific)
2. Step two
3. Step three

### Output
What the completed task produces.

### Quality Check
How to verify it was done correctly.

### Common Issues
What goes wrong and how to fix it.
```

**Systematization priority:**
1. Tasks you hate (you'll skip them otherwise)
2. Tasks that block others
3. Tasks that cause errors when done wrong
4. Tasks that take longest

### Phase 3: AUTOMATE

**Automation candidates:**

| Good for Automation | Bad for Automation |
|--------------------|-------------------|
| Repetitive, predictable | Requires judgment |
| Data entry/movement | Creative work |
| Notifications/alerts | Relationship building |
| Reporting | Complex decisions |
| Backups | Edge case handling |

**Automation tools for solo builders:**

| Category | Tools |
|----------|-------|
| Workflows | Zapier, Make, n8n |
| Scheduling | Cron, scheduled functions |
| Email | Sequences, auto-responders |
| Data | Scripts, database triggers |
| Monitoring | Uptime, error alerts |

**Automation ROI:**
```
Time saved per occurrence × Occurrences per month × 12
─────────────────────────────────────────────────────
Time to build automation + Time to maintain × 12

If ratio > 3, automate.
```

### Phase 4: DELEGATE

**Delegation framework:**

```
CAN delegate:
- Tasks with clear inputs/outputs
- Tasks with written SOPs
- Tasks that don't require context
- Tasks with measurable quality

CAN'T delegate:
- Tasks requiring your unique insight
- High-stakes decisions
- Relationship-dependent work
- Tasks you haven't systematized
```

**Delegation readiness checklist:**
- [ ] SOP exists and is complete
- [ ] Quality criteria defined
- [ ] Example outputs available
- [ ] Feedback loop established
- [ ] Access/tools documented

**Who to delegate to:**

| Option | Cost | Best For |
|--------|------|----------|
| VA (Virtual Assistant) | $5-25/hr | Admin, data entry |
| Freelancer | $25-100/hr | Specialized tasks |
| Contractor | $50-150/hr | Ongoing work |
| Part-time hire | Salary | Critical functions |
| AI tools | Varies | Repetitive analysis |

### Phase 5: MEASURE

**Operational health metrics:**

| Metric | What It Shows | Target |
|--------|---------------|--------|
| Response time | Support speed | < 24 hours |
| Resolution rate | Support quality | > 90% |
| Uptime | System reliability | > 99.5% |
| Error rate | Product quality | < 1% |
| Churn rate | Customer health | < 5%/mo |

**Weekly ops review:**
- What broke this week?
- What took longer than expected?
- What can be improved?
- What should be documented/automated?

### Phase 6: OPTIMIZE

**Continuous improvement cycle:**

```
Measure → Analyze → Improve → Measure
```

**Optimization targets:**
- Reduce time per task
- Reduce error rate
- Reduce response time
- Increase automation coverage
- Increase delegation effectiveness

---

## Framework References

### Systems Thinking
`frameworks/systems-thinking.md` - Building systems, not tasks

### SOPs
`frameworks/sops.md` - Standard operating procedure patterns

### Delegation
`frameworks/delegation.md` - Effective handoff frameworks

### Customer Success
`frameworks/customer-success.md` - Support and onboarding systems

### Team Building
`frameworks/team-building.md` - Hiring and culture (when ready)

---

## Output Templates

### SOP Template
`templates/sop-template.md` - Standard operating procedure

### Ops Playbook
`templates/ops-playbook.md` - Overall operations document

### Hiring Scorecard
`templates/hiring-scorecard.md` - Evaluation framework

---

## Tool Integration

### MCPs

**Supabase:**
- Operational data queries
- User support context
- System health metrics

### Subagents

**operations-manager:**
- Complex operations coordination
- System design assistance
- Process optimization

---

## Handoff

After completing operations setup:

1. **Save outputs:**
   - SOPs → `docs/sops/`
   - Playbook → `docs/OPS_PLAYBOOK.md`

2. **Log to tracker:**
   ```
   /tracker log {project-slug} "OPS: Systematized {N} processes. {N} automated. Ready for scale."
   ```

3. **Update state:**
   ```
   /tracker update {project-slug} OPERATING
   ```

4. **Next steps:**
   - Execute SOPs consistently
   - Review and improve weekly
   - When exit opportunity arises, transition to exit

---

## Quick Wins

### Day 1: Document Support
Write SOPs for:
- Answering common questions
- Bug report handling
- Refund process

### Week 1: Automate Notifications
Set up:
- New user alerts
- Error notifications
- Churn warnings

### Month 1: Build Playbook
Create comprehensive ops playbook covering:
- All recurring processes
- Emergency procedures
- Quality standards

---

## Anti-Patterns

| Anti-Pattern | Why Bad | Do Instead |
|--------------|---------|------------|
| "Just do it faster" | Doesn't scale | Systematize first |
| Automating first | Waste if wrong | Document, then automate |
| Delegating chaos | Sets up failure | Systematize, then delegate |
| No documentation | Knowledge silos | Write it down |
| Perfect systems | Never finished | Good enough, iterate |
| Ignoring ops | Drowning inevitable | Schedule ops time |

---

## Quality Checks

Before finalizing operations setup:

- [ ] Critical processes documented
- [ ] SOPs are followable by others
- [ ] Automation ROI is positive
- [ ] Delegation criteria defined
- [ ] Metrics dashboard exists
- [ ] Weekly review scheduled
- [ ] Emergency procedures documented
