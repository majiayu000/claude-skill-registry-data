---
name: to-spec
description: Turn the current conversation context into a spec. Use when user wants to create a spec (or PRD) from the current context.
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a spec (you may know this document as a PRD). Do NOT interview the user, just synthesize what you already know.

## Process

0. If the task folder has an `intent.md`, read it first. The spec answers it in the originator's terms. Where the intent conflicts with an ADR, the glossary, or the codebase, raise it with the user and record what stays unresolved under Open Concerns. Don't edit the intent.

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect any ADRs in the area you're touching. If the spec has to contradict an ADR, say so explicitly rather than silently overriding it: _Contradicts ADR-0007 (event-sourced orders), but worth reopening because…_

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Check with the user that these seams match their expectations.

3. Audit the technical decisions the feature depends on: what handles each solved problem (auth, validation, jobs, …), where the code lives, what schema/API contracts change. Decisions already settled in the conversation go into the spec as-is. For any that were never settled, check the project's existing dependencies and stack conventions — usually those already cover it and no new dependency is needed; record what will be used. Only when nothing in the project covers a genuinely solved problem, pick the idiomatic candidate for the stack and confirm it with the user alongside the seams. Either way, don't leave the choice implicit in the spec.

4. Write the spec using the template below, then save it per the `aiwork-protocol` skill.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A LONG, numbered list of user stories. Each user story should be in the format of:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

This list of user stories should be extremely extensive and cover all aspects of the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Libraries and dependencies chosen (and why, when an alternative was considered)
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts — not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Open Concerns

Decisions the spec had to leave open. Typically the intent contradicts an ADR, the glossary, or the codebase, or the choice belongs to someone outside this session, such as a policy or budget decision. One line per concern, including who needs to decide.

Writing them down instead of quietly picking a side keeps the spec honest. Omit when empty. `/implement-spec` stops on it otherwise.

## Further Notes

Any further notes about the feature.

</spec-template>
