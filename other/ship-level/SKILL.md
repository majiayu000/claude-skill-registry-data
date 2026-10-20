---
name: ship-level
description: Audit how reliably a project gets from code to a running product against a 5-level release maturity scale (build, configuration, deploy, rollback, monitoring, backups), propose options, then split the chosen work into sub-plans delegated to Haiku or Sonnet while Opus plans and reviews. Use when the user runs /ship-level or asks to prepare, audit or harden a release or deployment.
summary: Prepare a safe, repeatable release
argument-hint: "[level 1-5] [audit|build] [scope path]"
model: inherit
---

# Ship level

Arguments: `$ARGUMENTS`

Parse the arguments:

- **LEVEL**: a number 1 to 5. Default 3.
- **MODE**: `audit` (score and propose only) or `build` (audit, then execution plan, then delegated build). Default `audit`.
- **SCOPE**: any path in the arguments limits the audit to that area. Default: the whole project.

State the parsed settings in one line before starting. If AskUserQuestion is unavailable, ask in plain text and wait for the answer.

You are the release lead on this project. Work to the LEVEL. The levels describe how safely and repeatably the product ships, not which platform it uses. Keep the project's host and tooling unless the user asks to change them.

This skill prepares and rehearses. It never deploys. Any action on a live system is written out for the user to run.

## Levels

Each level includes everything in the levels below it. The current level is the highest level whose requirements, and those of every level below it, are all met. Record a project that does not meet level 1 as level 0. List requirements already met above the current level as ahead.

1. **Runnable.** Build and start commands are documented. Every configuration value is listed with an example file. No secrets in the repository.
2. **Repeatable.** A clean checkout builds and starts by following the written steps, with nothing known only to one person. Dependency and runtime versions are pinned. Configuration is checked at start, and a missing or invalid value stops the process with a clear message. Deploy and stop procedures are written down.
3. **Releasable.** Deploy is a script, not a list of hand steps. A pre-launch checklist exists and has been walked. Health check in place. The process restarts after a crash. Logs are kept and can be found. Backups run on a schedule and a restore has been tried. Rollback is written and has been tried once. The running version can be seen.
4. **Operated.** One pipeline runs tests, build and deploy. Deploys cause little or no downtime. Monitoring and alerts reach a named person. A runbook covers the most likely failures. A rehearsal or staging environment matches the real one. Secrets are stored outside the code and can be rotated. Data changes can be applied and undone safely.
5. **Resilient.** More than one instance, with tested failover. Releases go out gradually and roll back automatically on failure. Disaster recovery has been rehearsed against a stated recovery time. Capacity and cost are tracked. Only choose this when downtime is costly or the product must stay up unattended.

## Models

Planning and audit run on Opus only. Execution runs on Haiku, or Sonnet when required.

- If this session runs Opus, continue. If it runs Fable, say that Fable costs more than Opus and ask the user once whether to continue on Fable or stop and run the skill again on Opus (`/model opus`). On Fable, read Opus in this skill as Fable, including in printed lines. On any other model, say which model is running and ask the user whether to continue on it or stop. Do not move these steps into a sub-agent: a sub-agent cannot ask the user questions.
- Executors are spawned with the Agent tool and an explicit `model` of `"haiku"` or `"sonnet"`. Never leave the model unset.
- Opus never makes the edits. Executors never change scope, choose a host or tool, or review their own work.

## Step 0: Release context

Before the audit, establish how this product ships and who runs it.

1. Look first. Read build and deploy scripts, container files, process manager and CI configuration, environment examples and the README. Read `LEVELS.md` if it exists: reuse a confirmed hosting profile and show it instead of asking again.
2. If there is no hosting profile, ask for it first: where it runs, who can reach it, expected and peak load, uptime need, machine limits, and limits set by the host.
3. Ask the user only what is still open, with AskUserQuestion, in at most two rounds.

   Round one:
   - **Release moment**: a fixed date or event / when ready / continuous.
   - **How it ships today**: by hand on one machine / copied to a server / pushed to a platform / not shipped yet.
   - **Downtime tolerance**: any time is fine / only outside use hours / never during an event / never.
   - **Who operates it**: the builder alone / a named person on the day / a team / nobody watching.

   Round two, only what still matters:
   - **Recovery need**: how much data loss is acceptable, and how fast it must be back.
   - **Access**: who holds the credentials, and what happens if that person is unavailable.
   - **Environments**: whether a rehearsal or staging copy exists or can exist.
   - **Data changes**: whether releases change stored data or its format.
   - **Past trouble**: what went wrong in earlier releases or rehearsals.
   - **Cost ceiling**: any limit on hosting or tooling spend.

4. If the user does not know an answer, record it as unknown, state the assumption you will use, and flag it as a risk.
5. Print a short release profile and wait for the user to confirm or correct it.

Remove from the audit any requirement the profile makes irrelevant, and say which ones and why. A localhost tool for one person does not need a pipeline or alerts. Never recommend a step the host cannot support.

## Step 1: Audit (Opus)

1. Clean-checkout rehearsal. Copy the repository to a throwaway folder with no installed dependencies and no local configuration. Follow the written steps exactly, using only example values. Record every point where the steps fail, are missing, or need knowledge that is not written down. Do not touch the user's working files.
2. Check configuration and secrets. List every value the product reads. Mark each as documented or not, validated at start or not, and secret or not. Search the repository and its history for committed secrets. Report any found secret as urgent, and tell the user it must be replaced, not only removed.
3. Check each release concern against the profile: build, start, stop, deploy, health, restart after crash, logs, backup and restore, rollback, version visibility, monitoring, data changes. For each record: in place and tried, in place but never tried, or missing. Cite the file or command.
4. State the level the project is at now, with one line of evidence per requirement. Say what is already sound and must be kept.
5. List every unmet requirement, ranked by risk: data loss first, then exposed secrets, then a release that cannot be undone, then outages, then the rest.
6. For each of the top gaps, give two or three distinct options. For each: what it changes, what it costs (effort, money, upkeep, new tools), when it is the wrong choice. Mark the one you recommend and why. Prefer what the host and existing tools provide over a new service.
7. Add a short list of optional ideas from one level above the target, labelled as stretch.
8. If the target LEVEL is wrong for this product or its release profile, say so and name the level you would pick.
9. Stop and wait for the user's choices. In `audit` MODE, write the record and the levels row (see Connections), then end here.

Challenge decisions that lower the result: say so plainly, give the reason and the alternative, then follow the user's final call. If a requirement does not fit this product, say so and skip it.

## Step 2: Execution plan (Opus)

After the user chooses, do not build directly.

1. Split the chosen work into sub-plans that can each be done and checked alone. One sub-plan covers one release concern. There is no fixed count: let the size of the project and of the chosen work set it. Do not pad a small job with trivial sub-plans, and do not merge unrelated concerns to keep the count low.
2. Each sub-plan states:
   - Goal, in one sentence.
   - Files to add or change, and files it must not touch.
   - Exact steps, with the names, values, commands and failure messages to use. Leave no choice of host or tool to the executor.
   - Done check: the local or rehearsal command that proves it works.
   - Live step: none, or the exact command the user must run on the real system, what it does, and how to undo it.
   - Dependencies: which sub-plans must finish first.
   - Model: Haiku or Sonnet, with a one-line reason.
3. Assign the model by this rule:
   - Haiku by default: documentation, checklists, environment example files, configuration files from a full specification, simple scripts.
   - Sonnet when needed: pipelines, deploy and rollback scripts, startup validation, health check and shutdown wiring, backup and restore scripts, data change safety.
   - If a sub-plan needs Sonnet, first try to split it until part of it fits Haiku.
4. Order the sub-plans. Mark which can run in parallel (no shared files) and which must run in sequence.

## Step 3: Delegation gate

Before spawning any executor:

1. Show a table of the sub-plans: number, goal, files, live step or none, model, parallel or sequential.
2. Print a warning line with the real counts from this plan, in the form: `Delegation: <n> sub-plans on Haiku, <n> on Sonnet. Review on Opus.` Each sub-plan starts a new agent with its own start-up cost. If the plan has three sub-plans or fewer, say that **No delegation** may cost less.
3. List every live step separately. State that the user runs these, in which order, and how each is undone. State any new cost.
4. Ask the user with AskUserQuestion:
   - **Delegate as planned (Recommended)**: run with the models shown.
   - **Haiku only**: downgrade every Sonnet sub-plan. Name which sub-plans are at risk.
   - **Sonnet for all**: upgrade every sub-plan.
   - **No delegation**: build in the main session. Warn that this runs every edit on the session's current model, which is Opus unless the skill said otherwise at the start.
5. Do not start until the user answers. If the user changes a model for one sub-plan in free text, apply it and show the table again.

## Step 4: Execute

- Immediately before each spawn, print one line: `Sub-plan 3 → Haiku: <goal>`.
- Each executor starts with no memory of this conversation. Pass it the whole sub-plan plus the relevant part of the release profile.
- Run parallel sub-plans in one message. Run sequential ones in order.
- Executors work on files and local rehearsals only. They never deploy, never connect to a live system, never read, print or write real secrets, never change addresses or domain settings, and never create paid resources.
- If an executor reports a sub-plan unclear or blocked, do not let it guess. Rewrite the sub-plan on Opus, or ask the user. A rewrite of a blocked sub-plan does not count as the corrective round.

## Step 5: Review (Opus)

After the sub-plans finish:

1. Repeat the clean-checkout rehearsal from Step 1 with the new steps and scripts.
2. Rehearse locally what can be rehearsed: start with missing configuration, stop during work, crash and restart, backup then restore into an empty copy, deploy then roll back.
3. Report the level reached, what moved, what is still open, and which concerns are in place but still never tried on the real system.
4. Hand the user the ordered list of live steps with their undo steps, and the pre-launch checklist.

For anything that failed, write a corrective sub-plan, assign a model the same way, print the warning line and run it. One corrective round, then report the remainder to the user. Report anything not verified.

## Connections

This skill is one of the connected level skills (`levels` runs them as one workflow, `levels-status` shows them all, `levels-next` picks the next one to run). Use the names as the skill listing shows them (a name may carry a prefix).

**Shared record.** At the start, read `LEVELS.md` in the project root if it exists and reuse what it already answers. At the end, create or update its ship section with: the release profile, target and reached level, concerns tried and never tried, pending live steps, and the date. Never write a secret into this file. Keep other skills' sections intact.

**Levels block.** Keep this block at the top of `LEVELS.md`, one row per layer, and update only this skill's row: current level, target level, count of open gaps. Keep the format exact.

```
<!-- levels
ship: 2/3 gaps=6
-->
```

**Handoffs from this skill.**

- A release concern needs product code that is missing, such as a health check, graceful shutdown, atomic writes or startup validation deep in the server: offer `backend-level`, scoped to that concern.
- Tests are missing or not automatic, so a pipeline has nothing to gate on: offer `test-level`.
- The interface has no state for maintenance, version mismatch or lost connection during a deploy: offer `design-level`, with the list of states.

**Handoffs into this skill.** When called by another skill, use the context passed in, skip questions the shared record answers, and return the result to the calling skill instead of offering a further handoff.

**Rules for every handoff.** Ask the user first with AskUserQuestion, and say which skill runs next, in which mode, and that it starts its own model spend. Never hand off silently. One hop only: a skill started by a handoff does not start another one, it reports back. If the target skill is missing, say so and stop.

## Quality bar

Nothing reported as working unless a rehearsal proved it. A backup counts only after a restore was tried. A rollback counts only after it was tried. No live action taken by this skill. No secret printed, stored or committed. No step that exists only in one person's memory.
