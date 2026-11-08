---
name: to-spec
description: Synthesize a conversation into a scoped specification, with publication when requested.
disable-model-invocation: true
---

Synthesize the current conversation and relevant codebase understanding into a spec. Reuse settled requirements, contracts, and decisions without another interview.

When fetching tracker context or preparing publication, read [Tracker integration](../triage/TRACKER.md) for destination, role mapping, and authorization rules. Missing tracker setup does not block a draft.

## Process

1. Reuse existing context. Inspect relevant code only where it could change the spec's behavior or contracts. Use the project's domain glossary vocabulary and respect ADRs in the affected area.

2. Identify the agreed contracts and test interfaces. Ask only about unresolved choices that materially affect scope or those contracts. Do not reopen settled seams or invent decisions to fill gaps.

3. Write the requested spec using the applicable template sections below. Keep the problem, behavior, and scope explicit; scale the detail to the change. Return the draft, or publish it to the authorized destination when requested. Apply the configured `ready-for-agent` role only when the scope and contracts are settled enough for agent work.

Finish with the draft or published issue reference. If publication is blocked, return the completed draft and the specific remaining decision or access requirement.

<spec-template>

## Problem Statement

The problem that the user is facing, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

Number the distinct in-scope user behaviors. Use this format where it clarifies the actor and benefit:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Cover the requested behavior and meaningful edge cases without padding the list or expanding the feature.

## Implementation Decisions

A list of implementation decisions that were made. This can include:

- The modules that will be built/modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.

Exception: if a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Testing Decisions

A list of testing decisions that were made. Include:

- The contracts and risks the selected checks address
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
