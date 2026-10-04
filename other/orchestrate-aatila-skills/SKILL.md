---
name: orchestrate
description: Shared coordination policy for codex-orchestrate and rp-orchestrate. Load when either skill requests it for role choice, assignment ownership, and whole-task verification.
---

# Orchestrate

Apply this policy through a harness-specific orchestration skill. The calling skill owns tool selection, context inheritance, and session lifecycle.

Stay available to the user while delegating substantive, bounded assignments. Delegate when an assignment can progress alongside useful work by you or another agent; handle small or tightly coupled work directly.

Preserve supplied plan identifiers, scope, dependencies, and explicit execution order. Fill missing dispatch details without decomposing an agreed plan again. A review request stays read-only; a chosen implementation workflow keeps its own completion requirements.

## Choose the role

Keep the coordinator on its current model and effort. Use these personal preferences for children unless the user specifies otherwise; the calling adapter resolves them to supported targets.

| Role | Model | Reasoning | Suitable assignment |
| --- | --- | --- | --- |
| Scout | `gpt-5.6-sol` | `low` | A narrow, read-only question: locate ownership, trace a path, find tests, or check an API fact. |
| Mechanical worker | `gpt-5.6-luna` | `max` | Bounded execution with the approach already decided: consistent call-site edits, fixture updates, or a specified transformation. |
| Worker | `gpt-5.6-sol` | `medium` | Scoped implementation that still needs local judgment. |
| Smart worker | `gpt-5.6-sol` | `high` | Difficult implementation, conflicting evidence, or ambiguity requiring deeper reasoning. |
| Advisor (optional) | `gpt-6-astra` | `high` | A bounded, read-only design or review question; retain useful decision context for related follow-ups. |

Luna's high effort does not make an ambiguous assignment mechanical. Resolve the behavior first. If a worker discovers an undecided contract or needs wider ownership, have it return the evidence and decision needed; clarify the brief or use a suitable role. Disclose necessary model fallbacks rather than silently changing the user's preferences.

## Assign and coordinate

Give each agent an outcome, workspace and relevant files, read-only scope or exclusive write ownership, dependencies, essential user constraints, applicable project instructions, and concrete completion criteria. Request a compact result with file evidence, checks actually run, and blockers. Fresh-context briefs must carry decisions the child cannot see.

Make children leaves by default: **Complete this assignment directly. Do not spawn other agents; the parent's delegation instructions apply only to the parent.** The calling adapter determines whether any nested delegation is permitted.

Dispatch independent assignments concurrently; verify prerequisites before dependent work. Track agent IDs, ownership, and outstanding results. Give each writable file one owner at a time, including shared tests and manifests; confirm a writer has stopped before transferring ownership. Coordinate commits separately because a shared checkout also shares its index.

Reuse agents when their context helps closely related work. An Astra advisor may remain available throughout the current task; send related questions and new evidence to the same advisor. Create one only for a concrete advisory question that can run alongside useful work, not as a mandatory team member.

Keep discoveries moving to the agents that need them, using the adapter's supported communication path. Resolve conflicting decisions and changes to scope, dependencies, or ownership centrally. While children run, advance distinct work without duplicating their investigation. Keep the user informed of meaningful findings; wait when no useful independent work remains.

Keep permissions within the user's existing authorization. Route requests for new approval to the user and continue unaffected work; another agent cannot grant it.

## Finish the whole request

Inspect actual changes and evidence, integrate the results, and verify the combined behavior against the user's request. Continue corrections until complete or concretely blocked. Account for every assignment before ending and stop unnecessary running work using the adapter's lifecycle rules. Report what was delivered, what was verified, and what remains untested or blocked.

## Basis

Adapted from Eric Provencher's [orchestrate skill](https://github.com/provencher/codex-skills/blob/main/orchestrate/SKILL.md) and the user's saved companion guide, with personal model preferences. Harness-specific contracts belong to the calling adapter.
