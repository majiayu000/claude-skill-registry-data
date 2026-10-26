---
name: execute-plan
description: Use when carrying out an implementation plan the person has already approved, whether starting it or resuming it in a later session, and the tracker in it has to stay true while the work happens. Not for producing the plan (write-plan) and not for reviewing the result.
---

# Execute a plan

**You are the plan's orchestrator; the `orchestrate-plan` skill holds those duties** (the mandate, dispatch, checking the run, verification, merges, pull requests). Load it with this one.

**The plan is a living document.** `write-plan` built it and its tracker; this skill keeps both true as the work teaches something. Amending a task, adding one, dropping one or moving a decision is normal work, written into the plan as it happens.

## Before starting

- **Open the plan in aiview every session** and give the person the URL.
- **Do not start** if the plan has no tracker, a phase has no goal, seats' roles and areas, or a check as a command (its tasks are written at its open). Say so and finish the plan first.
- **Reconcile a tracker the repository has moved past** before starting; say what you found.
- **Every phase runs on the swarm board**, however few seats it has, through the `orchestrate-plan` skill.

## Keeping the plan and its tracker

The tracker's protocol is the `write-plan` skill's `references/tracker.md`, read before the first edit.

- **Tick as you go, never in a batch.** ✅ only once this session has re-run the step's done-when.
- **Update before every handoff**: a question, an approval, the end of a turn.
- **Change the plan before acting on the change.** New work is a node, a dropped step is ✖ with the reason. A change that decides a module, interface, schema, contract or architecture is a row in the plan's decisions; one that becomes a slice gets its slice document first (`write-slice`).
- **A subagent's return is read, never pasted into a step**; each line of it has a home, listed in the tracker's protocol.

## When to pause

Stop for exactly three things:

- **A decision that is the person's.** A finding that breaks a decision the plan rests on, a repair with real options, work outside the plan's scope.
- **Verification only a person can do.** A browser flow, a real sign-in, another team's approval. Do everything mechanical first.
- **An action that leaves the machine and does not undo cheaply.** A production deploy, a migration on shared data. Approved once each. A merge the mandate's `pace` gives the orchestrator is approved by the mandate.

**A pause is a handoff**: the tracker current; what happened, the decision wanted, the options and a recommendation; then what the person does next, numbered, each with its exact command. A secret goes in a file the pause names, by path and keys.

**Do not pause for** per-step sign-off, verification you can do yourself, naming, structure, tool choice, or a failure you understand whose fix changes nothing decided. **Stop the line** when one step fails twice for unrelated reasons.

## The close

With a roadmap, say the plan finished and the roadmap may need redrawing; the person confirms the slot landed. When the plan delivered something a person looks at, recommend going over it with them through the `validate-delivery` skill.

List the decisions whose source is `agent default` that shipped, and ask whether any is to be revisited; when one of them is a `contract`, recommend the `validate-delivery` skill even if nothing was delivered for a person to look at.
