---
description: Define team vision, values, and the culture you want to build
---

# Vision

Define the vision for "$ARGUMENTS". Establish the team's purpose, values, and the culture you want to cultivate.

## Prerequisites

Read `.metapowers/leadership/$ARGUMENTS/01-assess.md`. If this file does not exist, tell the user:

> Phase 1 (Assess) has not been completed for "$ARGUMENTS". Run `/leadership:assess $ARGUMENTS` first, or use `--skip-checks` to bypass.

If `--skip-checks` is present in $ARGUMENTS, skip this check and log to `.metapowers/leadership/$ARGUMENTS/skip-log.md`.

## Process

1. **Read context:**
   - Read `.metapowers/leadership/$ARGUMENTS/01-assess.md` for team assessment and challenges

2. **Define team purpose:**
   - Why does this team exist? What unique value does it deliver?
   - How does the team's work connect to the broader organization's mission?

3. **Establish team values:**
   - Ask the user: What behaviors do you want to see every day?
   - Define 3-5 team values with concrete behavioral examples
   - For each value: "We value X, which means we do Y and never do Z"

4. **Define target culture:**
   - What does a great day on this team look like?
   - How should decisions be made? (see decision-frameworks.md)
   - How should conflicts be handled?
   - What's the communication style? (async-first, meetings, docs)

5. **Write the artifact** to `.metapowers/leadership/$ARGUMENTS/02-vision.md` with sections:
   - **Team Purpose** — why the team exists
   - **Values** — 3-5 values with behavioral examples
   - **Culture Blueprint** — decision-making, communication, conflict norms
   - **Success Vision** — what "great" looks like in 6 months

## Output

The vision written to `.metapowers/leadership/$ARGUMENTS/02-vision.md`. Present a summary highlighting:
- Team purpose statement
- Core values
- Key cultural norms
