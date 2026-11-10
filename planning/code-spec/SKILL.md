---
name: code-spec
description: "Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed."
disable-model-invocation: true
---

This skill takes the current conversation context and codebase understanding and produces a spec. Do NOT interview the user; just synthesize what you already know.

The issue tracker and triage label vocabulary should have been provided to you. If not, read `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`.

## Process

1. Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the spec, and respect ADRs in the area you're touching, and the design.md principles that apply.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better - the ideal number is one.

Name any planned test that would break a [test speed rule](../../../config/docs/code-style/tests.md#test-speed) and warn about it clearly, saying which rule it breaks. The spec's Testing Decisions repeat the warning, so it reaches the ticket implemented from it. The warning needs no approval of its own.

Check with the user that these seams match their expectations.

3. Decide whether the spec has **Phases**, yourself, without asking: **split a spec into Phases only at a boundary where real use could change or cancel what follows** ([`planning.md`](../../../docs/agents/planning.md#phases)). When it applies, write the proposed `## Phases` section of the template, naming Phase 1's stand-ins; the developer reviews it with the rest of the spec. With no boundary, leave the section out.

4. Write the spec using the template below, then publish it to the project issue tracker. Apply the `ready-for-agent` triage label - no need for additional triage.

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

## Phases

1. Phase 1, <name>: stories <n–m>. Stand-ins: <what it runs on until a later Phase replaces it>. Status: planned
2. Phase 2, <name> (provisional): stories <n–m>. Status: planned

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

- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules will be tested
- Prior art for the tests (i.e. similar types of tests in the codebase)
- A warning for each planned test that would break a test speed rule, naming the test and the rule, repeated from the seam step

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

## Model fit

<Model> <effort>
<one-line reason>

</spec-template>

`## Model fit` is the last section of a spec meant for one session: a pair line naming one of the pairs in [`planning.md`](../../../docs/agents/planning.md#model-fit), then a one-line reason. A spec that won't fit one session is still published, without the section, and a chat line recommends `/code-tickets` for sub-issues; say nothing if the developer has explicitly agreed in the conversation that it becomes tickets.
