---
name: create-milestone
description: "Primary planning branch after /shape for major-tranche work that requires multiple independent PRDs. Use to create a GitHub milestone plus sequenced feature issues that will later mature from roadmap bet to research-ready to prd. Not for single-feature shaping, single-PRD big-batch work (which gets a container milestone from /write-a-prd), decomposition of a finished PRD, or implementation-ready work."
sources:
  primary:
    - "Shape Up — Ryan Singer"
  secondary:
    - "Thinking in Bets — Annie Duke"
    - "Thinking in Systems — Donella Meadows"
---

# Create Milestone

This skill bridges the gap between tranche-level shaping and feature-level delivery. Use it when `/shape` clarified work that requires multiple independent PRDs — the result is too large or too decomposable for one PRD. The goal is to create just enough GitHub-native structure to sequence feature bets, pick a tracer bullet, and let the selected feature re-enter the normal pipeline with a researchable brief.

> **One question per turn.** When confirming the branch, reviewing bets, or asking the user anything, ask one question at a time and wait for the answer before asking the next. Never batch questions into a list.
>
> **Prefer single-select.** Use single-select multiple choice when the user is choosing one direction, one priority, or one next step.
>
> **Use multi-select rarely.** Reserve it for compatible sets — goals, constraints, non-goals, success criteria — that can all coexist. If prioritization matters, follow up asking which selected item is primary.
>
> **Use the platform's question tool when available.** In Claude Code, use `AskUserQuestion`; in Codex, `request_user_input`; in Gemini, `ask_user`. Otherwise, present numbered options in chat and wait for the user's reply before proceeding.

## Invocation Position

This is a primary planning branch that follows `/shape` only when the shaped work is too large for a single PRD.

Use `/create-milestone` when:
- `/shape` already produced a closing summary with choices, assumptions, impositions, and structural signals
- the shaped work requires multiple independent PRDs rather than one bounded feature
- you need to sequence feature bets in GitHub before running feature-level `/research`

Do not use it when the work already fits inside one PRD, when a feature is already `research-ready`, or when the next need is decomposition or implementation.

## Why This Exists

`/shape` can clarify an entire app or product area, but `/research` needs a narrower question than "how should we build the whole thing?" `/create-milestone` turns tranche-level understanding into feature-level bets without creating a giant speculative PRD or introducing local roadmap files.

## Lifecycle States

Feature issues created by this skill move through three explicit states:

- `roadmap bet` — lightweight feature candidate attached to the milestone
- `research-ready` — same issue, expanded enough to support `/research`
- `prd` — same issue, expanded by `/write-a-prd` into the shaped pitch

Do not create a duplicate PRD issue by default. Preserve one canonical feature issue unless the bet fans out so materially that multiple PRDs are clearly required.

## Process

### 1. Confirm the branch

Before creating anything, confirm that the shaped work is too large for a single PRD.

Ask these questions one at a time — ask one, wait for the answer, then proceed to the next:
1. What is the milestone or tranche boundary?
2. What does success for this tranche look like?
3. What is explicitly out of scope for this tranche?
4. What is the smallest feature that would prove the architecture or product direction early?

If the answers suggest the work already fits one bounded pitch, do not continue. Return to the normal `/research` path.

### 2. Create the milestone frame

Create one GitHub milestone representing the tranche or v1 scope.

The milestone should make these items explicit:
- the tranche name
- the outcome it is trying to produce
- the rough boundary of what is included
- the clearest non-goals
- the milestone-level success criteria

Do not turn the milestone itself into a giant spec. The milestone is the container and progress tracker, not the planning artifact that carries all detail.

### 3. Derive feature bets

Create a small set of feature issues attached to the milestone.

Keep the set deliberately limited. Create only enough issues to define the tranche clearly and sequence the work. Avoid generating a giant backlog.

Each feature issue should include:
- `Current maturity: roadmap bet`
- Problem statement
- User or stakeholder
- Why now
- Appetite
- Dependency notes
- What this feature proves architecturally or product-wise
- Milestone role: tracer bullet, core capability, follow-on, or polish
- Out of scope for now

If labels are available, add a `bet` label alongside the written maturity field.

### 4. Sequence by dependency and risk

Order the feature bets using two rules:
- dependency order matters
- the first implemented feature should reveal architectural truth early

Choose one issue as the tracer bullet. It should be the smallest meaningful feature that tests the riskiest integration or core product assumption.

Avoid sequencing by convenience alone. The milestone should burn down uncertainty early, not merely produce visible progress.

### 5. Promote the next feature to research-ready

When a feature is selected to enter the delivery pipeline, expand that same issue from `roadmap bet` to `research-ready` before invoking `/research`.

The `research-ready` brief must include:
- Problem
- User or stakeholder
- Success signal
- Why now
- Appetite
- Constraints or impositions
- Assumptions to verify
- What this feature proves
- Out of scope for now

If labels are available, move the issue label from `bet` to `research-ready`.

Do not send a raw `roadmap bet` into `/research`.

### 6. Re-entry and backtracking

Once a feature is `research-ready`, it re-enters the default pipeline at `/research`, not `/shape`, because the tranche-level shaping already happened.

Normal progression for that feature becomes:
- `/research`
- `/write-a-prd`
- `/prd-to-issues`
- `/execute`
- `/pre-merge`
- merge
- `/compound`

If `/research` shows the milestone-level assumptions were materially wrong, backtrack to `/create-milestone` or all the way to `/shape` rather than forcing the work forward.

### 7. Milestone closeout

When the milestone's feature issues that define the tranche are complete, close the GitHub milestone.

If the tranche taught something reusable beyond a single feature, `/compound` may capture tranche-level lessons after closeout.

## Feature Issue Template

Use this structure for each new milestone feature issue:

<feature-bet-template>

## Current maturity

roadmap bet

## Problem

[What user or business problem this feature addresses]

## User / Stakeholder

[Who benefits, who uses it, or who is affected]

## Why now

[Why this belongs in this tranche rather than later]

## Appetite

[How much time this problem is worth at milestone-planning level]

## Dependency notes

[What this likely depends on, if anything]

## What this proves

[What architectural, product, or market truth this feature is meant to reveal]

## Milestone role

Tracer bullet / Core capability / Follow-on / Polish

## Out of scope for now

[Explicit exclusions while this remains a roadmap bet]

</feature-bet-template>

## Handoff

- **Expected input:** a closing summary from `/shape` with choices, assumptions, impositions, and structural signals for work that is too large for a single PRD
- **Produces:** a GitHub milestone, sequenced feature issues in `roadmap bet` state, and a selected feature promoted to `research-ready`
- **Re-enters the main pipeline at:** `/research` once a selected feature has been promoted to `research-ready`
- **May backtrack to:** `/shape` if milestone-level decomposition reveals the original shaping was wrong or too coarse
