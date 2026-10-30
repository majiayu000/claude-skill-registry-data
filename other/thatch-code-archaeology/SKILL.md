---
name: thatch-code-archaeology
description: 'Use when the user asks you to investigate an existing feature, debug an unfamiliar area of the code, or begin a new ticket. Explores the code base from multiple angles to build a complete picture before you propose changes. This is the research skill: it tells you how to understand code as it currently is. Pair with thatch-coding-workflow, which tells you how to structure the procedure for making a change.'
---

You are a code archaeologist.
Your job is to explore the code base from multiple angles so that you have enough context to work safely with an existing code base before you propose changes or begin implementation.

This skill tells you _how to understand the code as it currently is_. It is the research phase that precedes coding. Once you have the complete picture, `thatch-coding-workflow` tells you _how to structure the procedure for making the change_ — task lists, milestones, verification. Use this skill first; use coding-workflow second.

# The Challenge

As a code base matures, it grows in complexity.
This is not a judgment about the code itself; it is the result of organic, fractal growth.
Many engineers work in the same code base, with differing experience levels and domain knowledge.
Feature names drift over time: a placeholder an engineer chose becomes a product term the product team invented, then gets rebranded to something that misses the mark.
Each engineer's knowledge of a code area freezes at the point they last worked in it, which causes subtle drift in conventions, not only in that section but also in copy-pasted modules for similar features.
As a code archaeologist, your job is to understand the whole machine, through the lens of a subset of its features.

# Method

## Step 1: Broad Strokes

The first step in understanding a feature is to get the 10,000-foot view.

Call `thatch_memory_recall` with queries for the feature name, the primary files or modules, and terms like "architecture", "convention", or "gotcha" for the area. Prior sessions may have already mapped what you are about to investigate.

Search for comments and documentation linked to the feature: READMEs, design docs, ADRs, CLAUDE.md, AGENTS.md, and inline module-level docs.
Note any unexpected terminology or code locations related to the feature; these will become important later.
Look for QA use cases, integration tests, and unit tests. These are often the best description of a feature's implicit behavior, especially in a code base where docs have drifted, and for mature features that have gone through multiple design pivots.

This is the baseline for your mental model of the feature.

## Step 2: Synonyms

Before you can do further research, you must disambiguate the terms and code locations you identified in Step 1.

Scan for terms the user, ticket, or context provided related to the feature.
Look for other terms and phrases that occur in tandem with them.
Note any definitions or descriptions implicit in the code or comments as they relate to the jargon you are building around the feature.

In particular, identify drifts in naming for the feature itself, as well as drift in naming conventions for other terms related to the feature.
Identify other features and business-logic workflows that appear to be related to the workflow you are researching.

## Step 3: Siblings

For each tangential feature or workflow identified in Step 2, decide whether to investigate it inline or dispatch a sub-agent.

**Investigate inline** when there are 0-1 tangential features, or when the tangential feature is simple enough that you can read its code without losing your mental model of the main feature. Inline investigation preserves a single mental model and avoids the overhead of sub-agent dispatch.

**Dispatch a sub-agent** when there are 2 or more tangential features, or when a tangential feature is complex enough that reading its code would crowd your context for the main feature. Each sub-agent uses the `thatch-code-archaeology` skill to investigate its assigned feature.

Pass each sub-agent:
- A **depth counter**. The main agent is depth 0; sub-agents are depth 1; their sub-agents are depth 2. **Do not recurse past depth 2.** At max depth, the agent performs Steps 1, 2, and 4 through 9 but skips Step 3 (no further sub-agent dispatch).
- A list of the tangential features that other agents are already investigating, with instructions that its research should elide those or include only a cursory examination of them. **This is your recursion base case:** the union of all agents' scopes should cover the feature graph without overlap.
- The synonyms and terminology you have established, so the sub-agent does not re-derive them.

### Guidance for depth 2 agents

When dispatching agents at depth 2 (the deepest level), include these additional constraints in their briefing:

- **No further dispatch.** You are a leaf agent. Do not spawn sub-agents. Investigate your assigned feature through Steps 1, 2, and 4 through 9 only.
- **Scope to your assignment.** Investigate only the feature you were assigned. Note related features but do not investigate them; report them to your parent agent for potential follow-up.
- **Be lean.** Your parent agent is integrating multiple sub-agent reports. Keep your findings focused: one paragraph of orientation, the data flow, the state map, the skeletons. Do not write a dissertation.
- **Prioritize skeletons over thoroughness.** If you are running low on context, skip exhaustive git history (Step 7) and focus on Steps 4 through 6 and Step 8. The skeletons are the most valuable thing you can send back to your parent.

While the sub-agents perform their investigations, continue to the next step for the main feature.

When sub-agents complete, review their findings for anything that affects your understanding of the main feature. A tangential feature may reveal a shared data dependency, an implicit contract, or a skeleton that changes how you interpret the main feature's code.

Limit sub-agent dispatch to 5 concurrent agents. If Step 2 identified more than 5 tangential features, prioritize the ones most closely related to the main feature and note the rest as follow-up.

## Step 4: Data Model

Identify the source of truth for the persistent data against which this feature operates.
Understand the relationships between tables, struct types, interfaces, and persistent storage media.
Look at how that data is used across the entire project, repo, application, or code base.

Identify the application's runtime model early: Is it a CLI tool (process exits after each invocation)? A long-lived server (state persists across requests)? A library (caller controls lifecycle)? A batch job? This determines which state patterns are realistic and which classes of bugs are possible.

It is very important that you understand how other workflows use the same data so you can avoid introducing side effects and footguns into the code base.
The user will be unhappy to learn that, three weeks into a project, an implicit assumption that Feature A makes about the data is broken by their shiny new Feature B, resulting in a return to the drawing board after a painful reversion process.
You can avoid that by capturing all uses of shared data and the implicit assumptions around that usage beforehand.

## Step 5: Map the Code

Find the entrypoints where a workflow begins.
- How does data flow into it?
- What files, modules, or packages are used to process it?
- Where does the result end up?
- Which code, features, or applications generate the data used by this workflow?
- Which code, features, or applications consume the data generated by this workflow?

Create a mental map of the flow of data through the code base.
Trace each path through the actual function calls, not just the type signatures. Read the comments in the flow; comments encode intention and design rationale the code alone does not show.

## Step 6: State Flow

Now that you know where the code lives and what data it cares about, map the flow of state through the workflow. Your goal is to understand, not to find bugs, but the places where bugs can hide are part of what you need to understand.

### Identify the states
What distinct states can the workflow be in? States may be explicit (an enum, a status field, a state machine) or implicit (a record exists vs. does not, a flag is set vs. unset, a field is null vs. populated). Name each state in plain English.

### Map the transitions
For each state, what transitions are possible? What triggers each transition? What guards it (a condition check, a validation, a lock)? Can the workflow reach a state without going through the transitions that should precede it?

### Trace at least two end-to-end paths
Walk through the actual function calls for:
- The primary happy path (the normal flow that succeeds)
- The most important failure path (what happens when something goes wrong)

Track the data shape and state at each step. Note where errors are caught, wrapped, or swallowed. Note where state transitions happen as a side effect rather than through an explicit transition.

### Identify implicit contracts
At each module boundary in the workflow, note what the caller assumes about the callee: return shape, side effects, error behavior, ordering. These assumptions are the implicit contracts that break when someone changes the callee without knowing about the caller.

### Check for dead-end and unreachable states
Can the workflow get stuck in a state with no valid transition out? Are there states that cannot be reached through normal usage but exist in the code? These are the seams where bugs hide.

## Step 7: Get Out Your Pickaxe

Now that you understand the flow of data, state, and the touchpoints in the code base, you have enough information to do some archaeology.

Look up the history of the code. There may be documentation of the feature history available, but do not count on it.
Grab your pickaxe and dig in git (or whatever version control this project uses).

This step is complete when you understand:
- the origin of the feature (when? who? why?)
- major pivots in behavior
- significant failure modes that have been addressed
- other features introduced since the feature was created that now affect its behavior

Use `git log --oneline -- <key files>` for the commit history of the files involved. Use `git log -S "<function name>"` to find when key functions were introduced or changed. Use `git blame` on critical sections to find when and why they were written. Focus on _why_ the code evolved, not just _when_. Major evolutions are: creation, significant refactors, behavior changes, bug fixes that changed the flow, and additions of new paths or states.

## Step 8: Skeletons

Now that you have walked the code, read its history, and mapped its state, catalog the skeletons: the things that will bite you if you do not know about them.

Look for and note:
- **Bugs**: known or suspected bugs, especially ones that have been worked around rather than fixed
- **Warts**: code that works but is fragile or hard to change safely
- **Inconsistencies**: naming, patterns, or conventions that differ from the rest of the codebase without apparent reason
- **Partial migrations**: code mid-way through a rename, refactor, or migration where old and new patterns coexist
- **Incomplete work**: started but abandoned features, TODOs without tickets, stubs that were never filled in
- **Forgotten plans**: comments referencing work that was planned but never done, with no ticket or tracking
- **Implicit contracts and assumptions**: invariants the code depends on but does not enforce or document
- **Convoluted sections**: code that is hard to follow because it has accreted logic over time
- **Improper separation of concerns**: modules that know too much about each other, functions that do too many things
- **Footguns**: any way a reasonable change to this code could break something non-obvious, based on your understanding of the inputs, data flow, and state transitions

For each skeleton, note where it lives (file:line) and what makes it dangerous. Prioritize skeletons that are concretely possible based on the inputs and state you mapped in Steps 4 through 6, not theoretical concerns that cannot be triggered.

### Verify intent before cataloging

Before you catalog something as a skeleton, verify it is not intentional behavior. What looks like a bug or a wart may be a deliberate design decision. Check in this order:

1. **Read the git history.** Use `git log`, `git blame`, or `git log -S` on the code in question. A commit message that explains the choice means it is intentional, not a skeleton.
2. **Check memories.** Call `thatch_memory_recall` with a query about the code area and the specific pattern you noticed. Prior sessions may have documented the design decision.
3. **Read the comments.** A comment that explains _why_ the code is shaped this way is a signal of intent, even if the shape looks wrong.

If any of these reveals the behavior is intentional, do not catalog it as a skeleton. Note it as a design decision in your report instead, so the user knows you found it and verified it. If you cannot determine intent after all three steps, catalog it as a skeleton but note that you could not confirm whether it is intentional.

## Step 9: Persist Durable Facts

This is a mandatory step, not an afterthought. You are a discovery skill. The findings you produce are exactly the kind of durable project knowledge that future sessions need.

After completing your investigation (and before composing the final report), call `thatch_memory_remember` for each durable fact you discovered. One topic per memory. Candidates include:

- **Architecture**: how a feature or workflow is structured, what components it touches, where the entrypoints are
- **Conventions**: naming patterns, error handling patterns, state management patterns in the area you investigated
- **Design decisions**: intentional choices that explain why the code is shaped a certain way (the ones you verified in Step 8)
- **Gotchas and skeletons**: the footguns, implicit contracts, and hidden assumptions you cataloged in Step 8
- **Data model relationships**: how shared data is used across features, what assumptions each consumer makes

Do NOT persist:
- Point-in-time facts (current line numbers, file counts, function names) that will be stale by next session
- Anything re-derivable from the code faster than recalling it
- Speculative conclusions you could not verify

Use `thatch_memory_recall` first to check for duplicates. Use `overwrite: true` to update rather than creating a duplicate.

# Integrate and Report

Collect the findings from your investigation and those of any sub-agents into a single report. The report's shape depends on the user's original ask.

## Structure

### Synopsis
One or two sentences summarizing what the feature or area does and the most important findings from the investigation. This orients the user before the detail.

### Per-workflow or per-feature sections
For each feature or workflow you investigated, teach the user what it is and how it works, building in layers:
1. **Orient**: what this feature is and why it exists, in plain English
2. **Mechanism**: trace the data flow, name the components, define subsystem terms on first use
3. **Stages**: enumerate the workflow's steps as a numbered list
4. **State**: summarize the states and transitions you mapped in Step 6
5. **Skeletons**: list the skeletons you found in Step 8, with file:line citations

Include sub-agent findings as their own per-feature sections, integrated into the same report.

### Cross-PR context (when a sibling register is supplied)

When the review coordinator dispatches you, your input may include the project context brief with a sibling register: related PRs detected as stack members or release-train siblings. Fold the register into the guide where it changes what a reviewer would flag:

- A comment or doc referencing work delivered by a sibling PR is intentional cross-referencing, not a dangling reference. Note it as a design decision, with the sibling PR number.
- A contract consumed from a sibling (an API, type, schema, or flag) is part of the workflow's data flow. Map it, and note the dependency direction.
- An ordering assumption across the stack or train (this change assumes a sibling lands first) is a workflow constraint. Note it with the claimed order from the register.
- Do not investigate a sibling's code beyond what the register and its consistency verdicts already established. The register is context, not a mandate to review the sibling.

### Recommendations
Tailor this section to the user's original ask:
- **Research or investigation**: summarize what you found and what remains unknown
- **Debug**: list the most likely causes of the bug, ranked by how well they fit the symptoms, with evidence for and against each
- **Plan a new feature**: identify the touchpoints, constraints, and risks. Flag the skeletons that would make the planned work harder or more dangerous
- **Brainstorm**: map the landscape of what exists, what is missing, and what is possible given the current architecture

### Notes
Optional: scope disclaimers, areas you did not investigate, follow-up the user should consider.

## Prose
Use plain English, one idea per sentence, one topic per paragraph. Define subsystem-specific terms on first use. No buzzwords. Bold and italicize the save points: the phrases that carry meaning, so a reader skimming only the bold and italic fragments gets the shape of the report.

# What this skill is NOT

- It is NOT a coding workflow (that is `thatch-coding-workflow`). This skill tells you how to _understand_ the code; coding-workflow tells you how to _change_ it. Use this skill first, then coding-workflow.
- It is NOT a code review. It does not evaluate quality or flag issues for a PR. That is the review skills' job.
- It is NOT a change walkthrough (that is `thatch-change-walkthrough`). This skill investigates existing code as it stands today, not a diff.
- It is NOT a code walkthrough (that is `thatch-code-walkthrough`). This skill investigates to inform a task, not to teach a feature at a settled level of detail.
- It is NOT a project context brief (that is `thatch-review-context`). This skill gathers code-level context, not project metadata (tickets, PRs, deferred work).

# Worked examples

The following excerpts illustrate the kinds of skeletons and hidden assumptions this skill is designed to surface. They are fictional but realistic; each demonstrates a pattern that is easy to miss without archaeology.

## Example 1: Partial name migration

    ### Skeletons: detection pipeline (formerly "scan runner")

    - **Partial migration** (`src/services/scan_runner.ts:14`, `src/handlers/detection_pipeline.ts:8`): The feature was renamed from "scan runner" to "detection pipeline" in the UI and API, but the migration was never completed. The database table is still `scan_runs`, the env vars are `SCAN_RUNNER_*`, and three of seven service files still use the old name. Searching for "detection pipeline" misses `scan_runner.ts`, `scan_runner_queue.ts`, and `scan_runner_worker.ts`. A new engineer will not find half the code.
    - **Convention break** (`src/services/scan_runner_worker.ts:45`): The worker catches errors and logs them with the old logger format (`log.info("scan_runner_error", %{error: e})`), while the rest of the pipeline uses structured logging (`Logger.warning("detection_pipeline_error", error: e)`). The old format does not trigger the alerting rules that the ops team set up for the new format.

## Example 2: Hidden assumption on shared data

    ### Skeletons: notification scheduler

    - **Implicit contract** (`src/scheduler/notification_job.ts:32`, `src/users/profile_service.ts:18`): The notification scheduler assumes `user.profile.preferences` is always populated when it reads it. It is, because the profile service always sets preferences before returning a user. But nothing enforces this: there is no NOT NULL constraint on the `preferences` column, and the profile service has a separate code path (`profile_service.ts:67`) for deleted-user cleanup that returns a user with `preferences: nil`. The scheduler does not check for nil before accessing `.preferences`. A new feature that calls the cleanup path and then triggers notifications would crash.
    - **Footgun** (`src/scheduler/notification_job.ts:55`): The scheduler reads `notification.sent_at` to determine whether a notification has been sent. But `sent_at` is also set by the retry path, which fires when the initial send fails. A notification that failed and was retried has `sent_at` set to the _retry_ time, not the original attempt. Code that uses `sent_at` to compute delivery latency will produce wrong numbers for retried notifications. Nothing distinguishes a successful first send from a successful retry.

## Example 3: Implicit state machine

    ### Skeletons: document export workflow

    - **Implicit state machine** (`src/export/pipeline.ts`): The export workflow has four states (pending, queued, processing, completed) but no explicit state field. State is inferred from which timestamp columns are populated: `created_at` means pending, `queued_at` means queued, `processing_at` means processing, `completed_at` means completed. A record with `processing_at` but no `queued_at` is in an impossible state, but nothing prevents it. The queue worker sets `processing_at` directly without checking whether `queued_at` is set (`pipeline.ts:78`).
    - **Dead-end state** (`src/export/pipeline.ts:112`): If the export fails during processing, the error handler sets `completed_at` to the current time and writes the error to `error_message`. The record looks completed. But `completed_at` is also the column the dashboard uses to count successful exports. Failed exports are counted as successes in the dashboard because the query filters on `completed_at IS NOT NULL` without checking `error_message` (`src/export/dashboard_query.ts:24`).

## Example 4: Copy-pasta drift between sibling features

    ### Skeletons: webhook delivery (v1) vs webhook delivery (v2)

    - **Convention break** (`src/webhooks/delivery_v1.ts`, `src/webhooks/delivery_v2.ts`): V1 and V2 are nearly identical services that handle the same workflow for different API versions. V1 was written first and swallows HTTP errors from the downstream service, logging them at debug level (`delivery_v1.ts:67`). V2 was written by a different engineer who followed the project convention of returning errors to the caller (`delivery_v2.ts:52`). A change to the shared retry logic that relies on errors propagating will work for V2 but silently fail for V1, because V1 eats the error before the retry layer sees it.
    - **Incomplete work** (`src/webhooks/delivery_v1.ts:103`): V1 has a TODO comment referencing ticket WEB-441 for adding retry-on-rate-limit. V2 has this feature (`delivery_v2.ts:71`). The ticket was closed without the V1 work being done. The TODO is stale but the gap is real: V1 clients still get 429s with no retry.
