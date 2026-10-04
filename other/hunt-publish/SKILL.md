---
name: hunt-publish
description: Publish a hunt as a case report, escalation, detection promotion, or leadership summary
argument-hint: "[target]"
allowed-tools: Read, Bash, Write, AskUserQuestion
---

<objective>
Publish the current hunt in the right format for action.

**Creates or updates:**
- `.planning/published/*.md`
- `.planning/STATE.md`

**After this command:** Route to follow-on hunting, escalation, or detection engineering based on the outcome.
</objective>

<execution_context>
@.github/thrunt-god/workflows/hunt-publish.md
</execution_context>

<process>
Execute the publishing workflow from @.github/thrunt-god/workflows/hunt-publish.md.
Choose the smallest publish format that drives action without overstating confidence.
</process>
