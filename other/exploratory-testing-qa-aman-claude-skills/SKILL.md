---
name: exploratory-testing
description: >
  Run structured exploratory testing sessions using test charters, timeboxing, and heuristics.
  Use when user says "exploratory testing", "charter-based testing", "explore the app", "unscripted
  testing", "session-based testing", "find unknown bugs", or needs to test an area without predefined
  scripts - even if they don't explicitly say "exploratory".
---

## Overview

Exploratory testing is simultaneous learning, test design, and execution. Based on "Exploratory
Software Testing" by Elisabeth Hendrickson and "Explore It!" (same author), this approach replaces
rigid test scripts with structured investigation using charters, timeboxes, and heuristics.

The core insight: scripted tests only find bugs you already imagined. Exploratory testing finds the
bugs you didn't anticipate - the ones that emerge from real usage patterns, unexpected interactions,
and system behaviors that scripted coverage can never reach.

## Workflow

### Step 1: Write a test charter

A charter defines the scope and mission of one exploratory session. Format:

```
Explore [area or feature]
Using [technique, tool, or approach]
To discover [information or risk type]
```

Examples:
- "Explore the checkout flow using rapid input variations to discover validation gaps."
- "Explore file upload using boundary conditions (0 bytes, max size, wrong MIME type) to discover error handling failures."
- "Explore user permissions using role-switching sequences to discover authorization gaps."

One charter = one session. Keep scope narrow enough to complete in 60-90 minutes.

### Step 2: Set a timebox

Sessions should be 60-90 minutes. Beyond 90 minutes, attention degrades and notes become inconsistent.

Structure your timebox:
- First 10 minutes: orient - understand the feature, review existing docs, set up test data
- Next 60-70 minutes: execute - follow the charter, take notes, log anomalies
- Last 10 minutes: debrief - summarize findings, classify bugs, identify follow-up charters

Use a timer. When time is up, stop even if you're mid-investigation. Log what you found and write a
follow-up charter for the remaining thread.

### Step 3: Apply heuristics to guide investigation

Heuristics are structured prompts that direct attention to known failure patterns. The HICCUPPS
heuristics (based on Hendrickson and Cem Kaner) are a reliable starting set:

- **H - History**: Has this feature broken before? Test the same paths.
- **I - Image**: Does behavior match the product's intended reputation (reliable, secure, etc.)?
- **C - Comparable products**: How do competitors handle this? Does this product match expectations?
- **C - Claims**: Does the product do what the docs, UI labels, and tooltips say it does?
- **U - User expectations**: What would a typical user assume? Does the product match that assumption?
- **P - Product**: Are there inconsistencies with how other parts of the product behave?
- **P - Purpose**: Does this serve the intended use case, or does it break under realistic usage?
- **S - Standards**: Does it conform to accessibility, security, or platform standards?

Apply at least 3 heuristics per session. Different heuristics reveal different bug classes.

### Step 4: Take structured notes during the session

Notes should capture three categories:

- **Observations**: What you saw (neutral, factual)
- **Anomalies**: What looked wrong or unexpected (potential bugs)
- **Questions**: What you don't know and need to follow up on

Example note format:
```
[Observation] Uploading a 4.9 MB file succeeds in 800ms on 3G emulation.
[Anomaly] Uploading a 5.1 MB file shows no error - just hangs indefinitely.
[Question] Is there a max file size limit enforced server-side? Not mentioned in UI.
```

Do not triage during the session. Log everything, evaluate afterward.

### Step 5: Debrief and classify findings

After the timebox ends, review your notes and classify each anomaly:

| Category | Description |
|----------|-------------|
| **Bug** | Confirmed unexpected behavior - file for the team |
- **Risk** | Potential issue, needs more investigation - write follow-up charter |
| **Question** | Unclear behavior - needs spec or product clarification |
| **Learning** | New understanding of how the system works - no action needed |

Write follow-up charters for every Risk item. These become inputs for future sessions.

### Step 6: Report the session

Share a session note with the team after each session:

```
Charter: [charter text]
Duration: [actual minutes]
Tester: [your role]
Coverage: [what was explored]
Bugs found: [count and severity]
Risks identified: [count]
Follow-up charters: [count]
```

Session notes build a coverage record that shows where exploratory effort has been invested.

## Anti-Patterns

**1. Exploring without a charter**
Bad: "I'll just click around and see what I find."
Good: Write a charter before starting. Aimless exploration wastes time and leaves inconsistent coverage.

**2. Ignoring the timebox**
Bad: Running an open-ended session for 3 hours.
Good: 60-90 minutes per session. Longer sessions produce diminishing returns and poor note quality.

**3. Triaging bugs during the session**
Bad: Stopping to file detailed bug reports mid-session.
Good: Log anomalies briefly during the session, classify and file after the timebox ends.

**4. Using only one heuristic**
Bad: Always testing with "what does the UI claim" and nothing else.
Good: Apply at least 3 different heuristics per session to surface different bug classes.

**5. No follow-up charters**
Bad: Session ends, risks are noted, nothing is scheduled to investigate them.
Good: Every Risk item from debrief becomes a charter for the next session.

**6. Treating exploratory testing as informal**
Bad: No notes, no debrief, no session report - "I tested it."
Good: Structured notes, timebox discipline, and a session report make exploratory testing auditable
and reproducible.

## Quality Checklist

- [ ] Charter written before starting (Explore / Using / To discover)
- [ ] Timebox set (60-90 minutes) and respected
- [ ] At least 3 HICCUPPS heuristics applied during session
- [ ] Notes taken in three categories: Observations, Anomalies, Questions
- [ ] Findings classified after timebox: Bug, Risk, Question, Learning
- [ ] Follow-up charters written for all Risk items
- [ ] Session note produced and shared with the team
- [ ] No personal names, project-specific paths, or internal tool references in output
