---
name: create-a-prd
description: Create a Product Requirements Document through user interview, codebase exploration, and module sketching, then file it as local Markdown. Use when user wants a PRD, product requirements, feature spec, or to formalize a feature idea into a shareable document.
license: MIT
effort: high
allowed-tools: Read Write Edit Bash Glob Grep Skill
---

# /create-a-prd

Create a PRD by interviewing the user, exploring the codebase, sketching deep modules, then filing the PRD as a local Markdown file.

## Workflow

You may skip steps when the conversation already covered them — capture, don't re-interview.

### 1. Get a long, detailed description

Ask the user for a long, detailed description of the problem they want to solve and any potential solutions they've considered. Encourage rambling — you'll structure it later.

### 2. Verify in the codebase

Explore the repo to confirm the user's assertions and understand current state. If the user says "we don't have X yet", check. If they say "this currently does Y", trace it.

### 3. Grill the user

Interview relentlessly about every aspect of the plan. For every question, **provide your recommended answer** — lead with "I'd recommend X because Y. Want to go with that, or something different?"

Walk down each branch of the design tree, resolving dependencies between decisions one at a time. Sub-decisions before siblings.

If a question can be answered by the codebase, **explore the codebase instead of asking**.

Park anything the user can't answer yet in an **Open Questions** list — don't let unresolved decisions stall the interview or get silently dropped. They go into the PRD's Open Questions section.

If grilling gets long, hand off to `/grill-me` for a tighter loop.

### 4. Sketch modules

Sketch the major modules you'll need to build or modify. Actively look for opportunities to extract **deep modules** that can be tested in isolation.

A deep module = small interface + lots of implementation. The interface rarely changes; the implementation hides complexity. Shallow modules = wide interface + thin implementation, and should be avoided.

Ask the user: do these modules match expectations? Which need tests? What's the test surface — unit, integration, end-to-end?

### 5. Confirm the outline

Before writing the file, present a short outline — the title, the problem statement, the user-story list, and the module sketch — and **wait for the user's approval**. A PRD is a durable artifact; don't file it as a surprise. Incorporate their corrections, then proceed.

### 6. Write the PRD

Once the outline is approved, write the PRD in Markdown using the template below. The PRD should be **self-contained** — understandable without reading the codebase — and **durable** — it should not break when the code moves or changes.

Pick a short, descriptive **feature name** for the title (the `#` heading). Derive the filename from it, lowercased and hyphenated: a PRD titled "Add a new payment method" is filed at `prds/prd-add-a-new-payment-method.md`.

**Before writing, check whether the target file already exists.** If it does, ask the user whether to overwrite it, file under a new name, or stop — never clobber an existing PRD silently.

**Durability rule**: do NOT include specific file paths, line numbers, or current code snippets. Code moves; the PRD shouldn't break the moment it's read three weeks from now. Describe modules, behaviors, and contracts — not implementation.

<prd-template>

# <Feature Name>

**Status:** Draft · **Created:** <YYYY-MM-DD>

## Problem Statement

The problem the user is facing, from the user's perspective. Not "the system has bug X" but "users can't accomplish Y because of X".

## Solution

The solution to the problem, from the user's perspective. What changes for them when this ships?

## Success Metrics

How we'll know the problem is actually solved — observable, measurable outcomes. Not "the feature exists" but "X is now possible / Y dropped / Z is measurable". A handful of concrete signals.

## User Stories

A LONG, numbered list of user stories. Each follows the format:

`As an <actor>, I want <feature>, so that <benefit>`

Example:
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending

For each non-trivial story, add a short **Acceptance criteria** sub-list — the conditions that make it "done." These become the basis for issues and tests downstream.

This list should be extensive — cover all aspects of the feature, including edge cases, error states, and admin paths. Aim for ≥ 8 stories on a non-trivial feature.

## Implementation Decisions

Decisions made during the interview. Include:

- Modules to build/modify (by name and responsibility, not file path)
- Interfaces to be modified (signature shape, not source location)
- Technical clarifications from the developer
- Architectural decisions
- Schema or data-model changes
- API contracts
- Specific interactions or flows

Do NOT include file paths, line numbers, or code snippets — they go stale.

## Testing Decisions

- A description of what makes a good test for this feature (test behavior through public interfaces, not implementation)
- Which modules will be tested
- Prior art in the codebase — similar test patterns already established

## Out of Scope

What is NOT being built in this PRD. Be explicit. This prevents gold-plating during implementation.

## Open Questions

Decisions raised during the interview but deferred — anything unresolved that implementation depends on. Omit if everything was settled.

## Further Notes

Optional. Anything else worth recording.

</prd-template>

After filing, share the file path with the user. Suggest `prd-to-issues` as the next step.