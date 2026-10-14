---
name: to-initiative
description: Turn the current conversation into a Kairos initiative with an attached PRD — no interview, just synthesis of what's already been discussed.
disable-model-invocation: true
---

Everything this skill needs is already in the conversation — stress-testing a half-formed plan is `/kairos:grill-me`, run before this skill, not during it.

## Process

1. Explore the repo, if you haven't already, until you can name the modules this feature touches and the candidate seams. Use the project's domain glossary vocabulary throughout the PRD, and respect ADRs in the area you're touching — `search` Kairos for both if they aren't already in context.

2. Sketch out the seams at which you're going to test the feature. Existing seams should be preferred to new ones. Use the highest seam possible. If new seams are needed, propose them at the highest point you can. The fewer seams across the codebase, the better — the ideal number is one.

   Check with the user that these seams match their expectations. The confirmed seams become the backbone of the PRD's Testing Decisions.

3. Publish to Kairos:

   - Find the coordination board with `my_boards`. If more than one could hold this work — or none exists — ask the user.
   - `create_item(item_type: initiative, board: <coordination board>, title: ...)` — a title in the domain glossary's words, content stating the problem and intended outcome in a few sentences.
   - `create_item(item_type: document, template: prd, board: <team board>, parent: <initiative short code>, title: ..., content: <the PRD>)` using the template below. `board` is the owner board of the PRD (required); the `parent` edge attaches the PRD to the initiative — no other wiring needed. The PRD is done when every decision made in the conversation lands in a template section — implementation, testing, or Out of Scope; nothing decided in-chat is left implicit.

   Name the initiative and the PRD only by the short codes in the results of `create_item`. Work for later is a quoted title, not "phase 2" (the `kairos-vocabulary` skill).

   Finish by telling the user both short codes. Breaking the initiative into tasks is `/kairos:decompose`, when the user is ready.

<prd-template>

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

A description of the things that are out of scope for this PRD.

## Further Notes

Any further notes about the feature.

</prd-template>
