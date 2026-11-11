---
name: audience-research
category: pm
description: Use when the stakeholder wants to know whether people would buy, pay for or want the product, what price works, what is missing, or wants to talk to potential customers - build an audience of synthetic personas from the project, run a study on it, report the findings with their limits, and offer one-to-one follow-ups
---
# Audience research

## Overview

TaskTrooper can invent an audience of fictional people from a project's brief, ask every one of them the same questions in separate interviews, and write a research report from the answers. Everything runs on the stakeholder's own agent runtime and is kept in their database; the Audience screen shows the same audiences, people, studies and reports. The people are synthetic. The result is a fast, cheap read on objections, missing pieces and price sensitivity, never evidence from real customers.

**Core principle:** ground it in what exists today, spend only on a yes, and report the findings with their limits.

## When to use

Trigger on: "would people pay for this", "who is this for", "test the idea / the price", "what's missing for people to buy", "talk to our customers", "build me an audience". Do not use it to decide what to build next on its own, and do not use it to invent user quotes for a deck.

## The flow

1. **Ground it.** Read the project first: `get_project_brief`, the README and the board (`list_board_tasks`, `get_board_summary`) through your read tools. Write down what the product is, what works today, what is only planned, its price if any and who the owner thinks it is for. People judge what exists, so describe the current state honestly, planned features marked as planned.
2. **Reuse.** `audience_list` first. An audience of the same product that is `ready` is reused; build a new one only when the product, market or question changed (`audience_update` then a rebuild is for small changes).
3. **Write the brief.** `audience_create` with the project's repository, an honest `product` text, three to five `segments` that include sceptics and non-buyers (counts add up to `persona_count`, default 12), `locations`, `current_solutions` (what people use today), `pricing`, `topic` and `language` (the stakeholder's own). Show the stakeholder the brief in a few lines and the number of calls building costs (`build_calls`).
4. **Ask before building.** The build spends model calls on the stakeholder's own runtime. Ask plainly: "This writes 12 people with 2 model calls. Build it?" Only after a yes call `audience_build` with `user_approved: true`. Then say it is building (a few minutes) and move on; check `audience_get` later, never poll in a loop.
5. **Plan the study.** For "would you pay" use the built-in core and add what the stakeholder needs: `price_points` around the stated price (half, the price, double) and at most a few extra `questions` ("What would make you switch from X?"). `study_plan` returns the call count (one per person plus the report). Show the plan and the count and ask. After a yes call `study_start` with `user_approved: true`; tell them it started and check `study_status` later.
6. **Read the report.** When `study_status` says done, call `study_report`. Present it in this order: the verdict and purchase-intent index and what it rests on; the willingness to pay (median, range, how many would pay nothing, the share who buy at each tested price); how segments differ; the top objections and what is missing, with how many people said each; two or three verbatim quotes with the person; the recommendations. Say in one sentence that these are synthetic personas and the numbers are hypotheses to validate with real people. Do not soften a weak result.
7. **Offer to go deeper.** Offer a one-to-one (`audience_talk`, or `study_follow_up` to tie it to the study) with a person who objected, and a question for everyone (`study_ask_everyone`, which costs one call per person and needs a yes). `study_ask_research` answers a question about the findings from the data.
8. **Turn findings into work only on request.** If the stakeholder wants the recommendations built, create the tasks through the normal board flow.

## Rules

- Never start `audience_build`, `study_start` or `study_ask_everyone` without the stakeholder's yes in this conversation, and always state the number of calls first. A yes to one step is not a yes to the next.
- Never report numbers you did not read from `study_report` or `study_status`, and never act as the audience yourself. If a call fails, say so and offer to retry; a missing result is not a "no".
- Never imply the people are real. Name them as synthetic personas whenever you quote them.
- Keep the brief true. Do not describe a feature that is not built as if it existed to get a friendlier answer; a flattering audience wastes the stakeholder's money.
- No agent runtime connected means nothing can run: tell the stakeholder to connect an agent CLI or API provider in Settings and stop.
- Use the stakeholder's language for the brief's `language` so the people and the report speak it.

## Cost reference

12 people: 2 calls to build, 13 to run a study (12 interviews and 1 report), 12 to ask everyone one more question, 1 per one-to-one message.
