---
name: postmortem
description: >
  Write a blameless postmortem after an incident. Use when the user says "postmortem",
  "post-incident review", "PIR", "what happened in that incident", "incident review",
  "blameless postmortem", "5 whys", "how do we prevent this again",
  or needs to document learnings from a production incident
  - even if they don't explicitly say "postmortem".
---

## Overview

Based on **"The Field Guide to Understanding Human Error"** by Sidney Dekker and the **Google SRE Book**. Dekker's fundamental insight: human error is never the cause of an incident - it is a symptom of a system that put people in a position where mistakes were likely. A blameless postmortem asks not "who made the mistake?" but "what conditions made this mistake likely, and how do we change those conditions?"

Google SRE's postmortem culture: incidents are opportunities to improve systems, not to assign blame. Engineers who feel safe reporting mistakes surface problems before they become incidents.

## Workflow

### Step 1: Schedule within 48 hours (SEV1) or 1 week (SEV2)

Postmortems decay in value quickly. Memories fade, context is lost. Set the meeting within 48 hours of a SEV1 resolution.

Attendees: IC, Operations Lead, on-call engineer(s), and anyone who can contribute to understanding what happened. No executives in the room - their presence changes behavior.

### Step 2: Build the timeline

Reconstruct what happened in chronological order. Be precise about times.

```
Timeline:
[HH:MM] - [what happened - system event, human action, or observation]
[HH:MM] - [alert fired: name]
[HH:MM] - [on-call engineer paged]
[HH:MM] - [first action taken]
[HH:MM] - [mitigation applied]
[HH:MM] - [service restored]
```

Include: system events, alerts, human decisions, and the reasoning people had at the time.

### Step 3: Identify contributing factors (not root cause)

Dekker's principle: complex systems rarely have a single root cause. They have contributing factors that aligned to create conditions for failure.

For each contributing factor, ask: "If this had been different, would the incident have been less likely or less severe?"

Common contributing factor categories:
- Technical: insufficient alerting, missing circuit breakers, inadequate testing
- Process: no deployment checklist, unclear escalation path, missing runbook
- Knowledge: alert with no runbook, undocumented dependency, new team member
- Capacity: system at limits, team understaffed, alert fatigue

### Step 4: Apply the 5 Whys

For the primary contributing factor, drill down:
- Why did X happen? - Because Y
- Why did Y happen? - Because Z
- Why did Z happen? - Because...

Stop when you reach a level where an action item can change the system. "Because the engineer made a mistake" is never the stopping point - that's where the analysis begins.

### Step 5: Write action items

Every postmortem must produce action items. Without them, it's just storytelling.

Each action item:

```
Action: [specific thing to do]
Owner: [named person, not "the team"]
Due: [specific date]
Priority: [P1 - fix before next deploy / P2 - this sprint / P3 - this quarter]
Type: [Prevention / Detection / Mitigation / Process]
```

Action types:
- **Prevention** - stops this failure mode from occurring
- **Detection** - makes the problem visible sooner
- **Mitigation** - reduces impact when it does occur
- **Process** - changes how the team responds

### Step 6: Write the postmortem document

```
Postmortem: [Incident title]
Date: [incident date]
Authors: [IC + contributors]
Severity: [SEV1/SEV2]
Duration: [start to resolution]
Impact: [users affected, features degraded]

Summary
[2-3 sentences: what happened, why it mattered, how it was resolved]

Timeline
[full timeline from Step 2]

Contributing Factors
[bullet list from Step 3 - no blame language]

5 Whys Analysis
[drill-down from Step 4]

What Went Well
[what helped contain or resolve the incident faster]

Action Items
[table from Step 5]

Lessons Learned
[2-3 insights that are generalizably useful beyond this specific incident]
```

### Step 7: Share broadly

Postmortems are most valuable when shared. Publish to an internal wiki, engineering all-hands, or team newsletter. Other teams often have the same latent failure modes.

## Anti-Patterns

**1. Blame language**
Bad: "The engineer deployed without testing."
Good: "The deployment process did not have a required staging environment check, making it possible to deploy untested code."
Dekker: blame stops investigation. "Human error" as a cause explains nothing and changes nothing.

**2. No action items**
Bad: Postmortem documents what happened but ends without concrete next steps.
Good: Every postmortem produces at least 2 action items with owners and dates. Track them to completion.

**3. Postmortem after the deadline**
Bad: "We'll get to it when things calm down." (more than 1 week for SEV1)
Good: Timebox it. A 60-minute postmortem within 48 hours is worth more than a 2-hour postmortem 3 weeks later.

**4. Only focusing on what went wrong**
Bad: Pure failure analysis, nothing about what was done right.
Good: Include "What went well." The practices that helped contain the incident should be reinforced, not just the failures fixed.

## Quality Checklist

- [ ] Scheduled within 48h (SEV1) or 1 week (SEV2)
- [ ] Timeline is precise (specific times, not "around noon")
- [ ] Contributing factors identified with no blame language
- [ ] 5 Whys drilled to a system-level cause, not a person
- [ ] Every action item has: owner (named), due date, priority, type
- [ ] "What went well" section included
- [ ] Document shared with broader engineering team
- [ ] Action items tracked to completion in next retrospective
