---
name: incident
description: Gather incident context and write a blameless postmortem with timeline, root cause, and action items.
disable-model-invocation: true
argument-hint: "/incident | /incident --gather | /incident --draft <title>"
allowed-tools: "Read, Grep, Glob, Bash, Write, AskUserQuestion, Skill"
sensitive: true
---

## Overview

Gather incident data from multiple sources, like recent deploys, error spikes, affected services, and recent changes, and produce a structured blameless postmortem following the template in [`standards/observability.md`](../../standards/observability.md). Can also help during active incidents by collecting diagnostic information.

## When to use

- After resolving a production incident to write the postmortem.
- During an active incident to quickly gather context and diagnostic data.
- When preparing for an incident review meeting.

## When NOT to use

- For non-production issues or local development bugs. Use standard debugging instead.
- For planned maintenance or expected downtime.

## Arguments

This skill accepts optional arguments after `/incident`:

- No arguments: interactive mode. Ask for incident details and build the postmortem.
- `--gather`: collect diagnostic data from available sources without writing a postmortem yet. Useful during an active incident.
- `--draft <title>`: start a postmortem draft with the given title, pre-filling what can be automated.

## Steps

### Gather mode (`--gather`)

1. **Collect deployment history.** Run these **in parallel**:
   - `git log --oneline --since="24 hours ago" --all` to find recent commits.
   - `GH_TOKEN=$(gh auth token --user <account>) gh release list --limit 5` to find recent releases, if `gh` is available.
   - `GH_TOKEN=$(gh auth token --user <account>) gh pr list --state merged --limit 10 --json number,title,mergedAt` to find recently merged PRs.

2. **Check service health.** Run these **in parallel**:
   - If the project has health check endpoints documented in the codebase, suggest curling them.
   - `docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"` to check container health, if applicable.
   - Check for error monitoring: suggest checking Sentry, Datadog, or CloudWatch based on project dependencies.

3. **Identify recent changes.** Run these **in parallel**:
   - `git diff --stat HEAD~10..HEAD` to show what changed recently.
   - `git log --oneline --since="48 hours ago" --format="%h %s (%an, %ar)"` for attributed change history.
   - Check for recent infrastructure changes: look for `.tf` or `pulumi` file modifications.

4. **Present findings.** Format as a diagnostic summary:

   ```
   ## Incident Diagnostic Summary

   **Gathered:** <timestamp GMT>
   **Repo:** <owner/repo>
   **Branch:** <current branch>

   ### Recent deployments
   <list of recent releases, merged PRs, and deploys>

   ### Recent code changes
   <summary of changes in the last 48 hours, grouped by area>

   ### Service status
   <container health, endpoint status if checked>

   ### Suggested next steps
   - Check <monitoring tool> for error rate spikes
   - Review <specific recent change> as potential cause
   - Check <dependency> health
   ```

### Postmortem mode (default or `--draft`)

1. **Ask for incident details** if not provided:
   - What happened? One sentence summary.
   - When was it detected? Timestamp or approximate time.
   - When was it resolved? Timestamp or approximate time.
   - What was the user impact? Who was affected and how.
   - What was the severity? SEV1 through SEV4.

2. **Gather automated context.** Run the same data collection as gather mode, steps 1-3 above.

3. **Build the timeline.** Combine user-provided timestamps with automated data:
   - Match deploy times against the incident window.
   - Identify the most likely triggering change.
   - Structure events chronologically with GMT timestamps per [`standards/observability.md`](../../standards/observability.md).

4. **Generate the postmortem draft.** Follow this structure from [`standards/observability.md`](../../standards/observability.md):

   ```markdown
   # Postmortem: <title>

   **Date:** <incident date>
   **Severity:** <SEV1-SEV4>
   **Duration:** <start to resolution>
   **Author:** <user>

   ## Summary

   <One paragraph: what happened, who was affected, what was the business impact>

   ## Impact

   - **Duration:** <total downtime or degradation window>
   - **Affected users:** <scope: all users, specific region, specific feature>
   - **Error budget consumed:** <if SLOs are defined>

   ## Timeline (GMT)

   | Time | Event |
   |------|-------|
   | HH:MM | <detection, first alert, or user report> |
   | HH:MM | <investigation started> |
   | HH:MM | <root cause identified> |
   | HH:MM | <mitigation applied> |
   | HH:MM | <service restored> |
   | HH:MM | <confirmed resolution> |

   ## Root Cause

   <The actual cause, not the trigger. Explain why the system behaved this way.>

   ## Contributing Factors

   <What made detection or recovery slower? Missing monitoring, unclear runbooks,
   lack of feature flags, insufficient testing?>

   ## What Went Well

   - <Things that worked: fast detection, effective communication, quick rollback>

   ## What Didn't Go Well

   - <Things that failed: slow detection, unclear ownership, manual recovery steps>

   ## Action Items

   | Action | Owner | Due Date | Status |
   |--------|-------|----------|--------|
   | <concrete task> | <person> | <date> | Open |

   ## Lessons Learned

   <Key takeaways that should inform future design and process decisions>
   ```

5. **Present the draft** to the user for review and refinement.
   - Ask if any sections need more detail.
   - Ask if the root cause analysis is accurate.
   - Ask if the action items are concrete enough, with real owners and due dates.

6. **File what generalizes.** When `SECOND_BRAIN_VAULT` resolves to a directory, offer to file an incident note before closing out.

   The postmortem belongs to the outage and stays where the team keeps postmortems. The vault note is the part that outlives it: the failure mode, the system property that allowed it, and what would catch it next time. Separate the two deliberately, because a vault note that restates the timeline is a duplicate that will drift.

   Delegate the write by calling the Skill tool with `brain` and the argument `capture`; that skill owns the note grammar. The note is a dated snapshot, so the incident date is the note date and its claims stay true without stamps. Link it to systems and people already in the vault, never to notes that do not exist yet.

## Rules

- All timestamps in GMT per [`standards/observability.md`](../../standards/observability.md). Never use local timezones.
- Blameless tone throughout. No individual blame, no "should have known better." Focus on systems and processes.
- Action items must be concrete tasks with owners, not vague improvements like "be more careful" or "improve monitoring."
- Never fabricate incident details. If information is missing, leave a placeholder and note what needs to be filled in.
- The root cause section must explain WHY, not just WHAT. "The deploy broke the API" is a trigger, not a root cause. "The deploy introduced a query without an index on a table with 10M rows, causing timeouts under normal load" is a root cause.
- Contributing factors are not excuses. They are system-level observations that inform action items.
- If `gh` or `glab` is not installed, skip the deployment history steps that require them and note the limitation.
- Never access production systems, databases, or monitoring dashboards directly. Suggest the user check them and provide the data.

## Common Rationalizations

- "The deploy inside the incident window is the root cause": that deploy is the trigger. The Root Cause section explains why the system failed under it, such as the missing index behind the timeouts.
- "A best-guess timestamp is close enough": an invented time corrupts the timeline. Leave a placeholder and name who can supply the real value.
- "`Improve monitoring` covers it": an action item names a concrete task, an owner, and a due date, or it is a placeholder the user still has to fill.
- "Naming the engineer who merged the change makes the timeline clearer": the postmortem is blameless. Describe the change and the process gap that let it through.
- "A quick query against production would confirm the theory": hand the query to the user and work from the data they return.

## Red Flags

- Stop and ask the user when a timestamp, severity, or impact figure has no source in user input or command output.
- Stop and rewrite when the Root Cause section names only the triggering change.
- Stop and convert when a timestamp is in local time or carries no zone.
- Stop and hand the step to the user when it needs a production system, database, or monitoring dashboard.
- Stop and reword when a sentence attributes the outage to a person.

## Verification

- Every timeline row carries a GMT timestamp sourced from the user or from a gathered command output.
- The Root Cause section explains why the system behaved as it did, beyond naming the trigger.
- Every action item has an owner and a due date, or is marked as a placeholder for the user to fill.
- Every missing detail appears as a placeholder that names what is needed.
- The user answered the three review questions from postmortem step 5 on the draft.
- In gather mode, the summary carries the gathering time in GMT and names every step skipped because `gh` or `glab` was missing.

## Related skills

- `/ship checks` - Check CI/CD pipeline status during incident investigation.
- `/ship commit` - Commit the postmortem document.
- `/review` - Review changes related to incident fixes.
