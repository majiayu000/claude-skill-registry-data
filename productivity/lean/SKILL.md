---
name: lean
description: Run a Lean waste audit on any process, workflow, or team. Identifies the 7 wastes, maps the value stream, suggests cuts, and tracks improvements. Use when asked to "audit this process", "find waste", "lean audit", "streamline this", or "what's slowing us down".
---

# Lean Process Audit

Analyze any process through the Lean Six Sigma lens. Identify waste, map the value stream, and suggest specific improvements.

## When to Use

- A process feels slow or bloated
- A team keeps missing deadlines
- The same problem keeps coming up at standups
- Before starting a new workflow (design it lean from the start)
- Monthly waste check on existing processes

## How It Works

### Step 1: Identify the Process

If the user says `/lean` with no args, ask:
> "What process do you want to audit? (e.g., standup format, sponsorship outreach, artist booking, content creation, or describe it)"

If args are provided, use them as the process to audit.

### Step 2: Map Current State (SIPOC)

For the identified process, build a SIPOC:

| Element | Question |
|---------|----------|
| **Suppliers** | Who/what provides inputs to this process? |
| **Inputs** | What goes in? (time, materials, information, decisions) |
| **Process** | What are the actual steps, in order? |
| **Outputs** | What comes out? What's the deliverable? |
| **Customers** | Who receives the output? Who cares if it's done well? |

### Step 3: Identify the 7 Wastes

Scan the process for each waste type:

| Waste | Question to Ask | Red Flag |
|-------|----------------|----------|
| **Transport** | Is information/work moving between too many people or tools? | More than 2 handoffs for a simple task |
| **Inventory** | Are there ideas, tasks, or plans piling up unacted on? | Backlog > 2x what gets done per week |
| **Motion** | Are people switching between too many tools/channels? | Same info in 3+ places |
| **Waiting** | Is work stalled waiting for someone's approval or response? | Any task blocked > 48 hours on a person |
| **Overproduction** | Are we making more than what's needed right now? | Planning 3 months out when next week isn't done |
| **Over-processing** | Are we polishing things that don't need to be polished yet? | V3 of a deck before sending V1 to anyone |
| **Defects** | Is work getting redone because of miscommunication? | "That's not what I meant" happening repeatedly |

### Step 4: Rate Severity

For each waste found, rate 1-3:
- **1 (Low):** Annoying but not blocking progress
- **2 (Medium):** Slowing the team down noticeably
- **3 (High):** Actively blocking critical path items

### Step 5: Prescribe Fixes

For each waste rated 2 or 3, propose a specific fix:
- Not "improve communication" - that's useless
- Specific: "Switch from verbal briefs to a 1-sentence written template in the dashboard"
- Actionable: someone can do it this week
- Measurable: you'll know if it worked

### Step 6: Output

Present as a clean audit report:

```
LEAN AUDIT: [Process Name]
Date: [Today]

SIPOC:
S: [Suppliers]
I: [Inputs]
P: [Steps]
O: [Outputs]
C: [Customers]

WASTE FOUND:
1. [Waste type] (severity N) - [description]
   FIX: [specific action]

2. [Waste type] (severity N) - [description]
   FIX: [specific action]

WASTE SCORE: [total severity points] / [max possible 21]
Lower is better. Under 7 = lean. 7-14 = needs work. 14+ = urgent.

RECOMMENDED FIRST ACTION: [the highest-severity fix that's easiest to implement]
```

Open this in the clipboard (use /clipboard pattern) so it can be copied and shared.

## Kaizen Sprint Mode

If the audit reveals a severity-3 waste on a critical path, suggest a Kaizen sprint:

> "This is blocking critical path. Want to run a Kaizen sprint on it? 5 focused sessions over the next week to fix this specific problem."

If yes, set up the 5-day format from doc 362:
- Day 1: Define problem + current state (2 hrs)
- Day 2: Root cause - 5 Whys (2 hrs)
- Day 3: Design future state (2 hrs)
- Day 4: Implement changes (execute)
- Day 5: Review - keep or revert (1 hr)

## Reference

Full framework details: `research/business/362-lean-six-sigma-festival-operations/README.md`
Lean team model: `research/business/263-obsidian-lean-team-model/README.md`

## Anti-patterns

- Don't audit everything at once. One process per audit.
- Don't suggest "more meetings" as a fix. Meetings are often the waste.
- Don't propose new tools. Work within existing tools (dashboard, Discord, docs).
- Don't over-complicate. If the fix takes longer to explain than the problem, it's wrong.
- Don't suggest fixes that require everyone to change behavior simultaneously. One change at a time.
