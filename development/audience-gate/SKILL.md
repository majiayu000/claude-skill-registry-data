---
name: audience-gate
category: pm
description: Use when a delivery request is about to become board tasks and its success depends on how people react to it (new paid or user-facing feature, pricing, onboarding, landing or product copy, positioning) - offer an audience test before opening the work, run it on yes, let the stakeholder revise the plan and re-run to compare, then open the tasks; open them at once whenever the stakeholder says so
---
# Audience gate

## Overview

Some requests are cheap to build and expensive to get wrong with people: a price change, a new paid tier, a reworded landing page, an onboarding step. For those, a synthetic audience study before the first task costs a few model calls and can catch a plan people would reject. The stakeholder decides; you only offer.

**Core principle:** offer the test once, before any task exists. The stakeholder can test, revise and re-test as often as they like, or skip it and open the work at any moment.

## Offer the test when ALL of

- It is a DELIVERY request (build or change something), and
- Whether it works depends on how users, buyers or visitors react, not on whether the code works. Typical: a new user-facing or paid feature whose demand is unproven, a price or plan change, landing page, onboarding or product copy, positioning or naming, removing or limiting something people use, and
- An agent runtime is connected (`audience_list` answers; if audience research reports no runtime, skip the offer silently and go on with the board flow).

## Do NOT offer it for

- Bugs, `technical` work, refactors, infra, CI, internal tools, small UI fixes, anything the stakeholder already decided after research.
- A request the stakeholder framed as "just build it", "skip the test", "open the tasks", or an urgent fix.
- A plan already tested in this conversation and not changed since.
- A request whose open question is technical (that is `analiz-gate`, not this).

When in doubt, do not offer. An offer on every request becomes noise the stakeholder learns to click away.

## Flow

1. **Offer, before creating anything.** One `ask_user` single-choice question (`allow_multiple: false`), in the stakeholder's language, with one sentence of why ("this changes what people pay, so a quick synthetic audience test could catch a price they reject"). Options:
   - Test it with an audience first (state the rough cost: reuse of an existing audience vs a new build, about N model calls)
   - Open the tasks now
   Create no task, no analiz and no design task until they answer.
2. **"Open the tasks now"** → go straight to the normal board flow (`analiz-gate`, `implementation-task-spec`). Do not offer again for this request.
3. **"Test it first"** → run `audience-research` with the request as its subject. Write the brief honestly: the planned change is a plan, not a shipped feature ("we are considering adding X at Y per month"), put the plan in the study goal and questions, and pick the kind from what is being decided: `user_interviews` for a feature or price, `landing_page_test` or `message_testing` for copy, `ab_test` for the current page against the proposed one. Every approval step of `audience-research` still applies (build, script, start each need a yes with the call count).
4. **Report against the request.** When the study is done, present the report as `audience-research` says, then add three things about the plan itself: what in the plan the people supported, what they rejected or missed, and your recommendation in one line (go as planned, change these points first, or do not build). Then ask what they want: revise the plan, open the tasks as they are, or drop it.
5. **Revise and re-run.** When the stakeholder changes the plan (a price, a step, the copy, a feature cut), restate the revised plan in a few lines, then call `study_rerun` on the finished study with `changes` = the revisions in plain sentences, still framed as a plan. It reuses the same people and script; never rebuild the audience in between. Show the script and the call count and wait for the yes as for any study, then run it.
6. **Show what moved.** When the re-run is done call `study_compare` and present it: the verdict score before and after, how many people scored higher, lower or the same, the objections that went away and the new ones. Then say plainly whether the change did what the stakeholder wanted it to do (the objection they targeted is gone or not, the score moved or not). The loop repeats from step 5 as often as they want; compare the latest run with the one before it.
7. **Open the work on their OK.** When the stakeholder is satisfied, open the tasks through the normal board flow for the final plan, not the original one. Carry the evidence in the task's `description` context: the study title (and the re-run's), the verdict before and after, the one or two findings that shaped the plan, labelled as synthetic research. Never write "audience tested" or similar as an acceptance criterion.

## Override, at any point

The stakeholder can stop the gate whenever they want: "open it anyway", "skip the rest", "build what I asked". Then open the tasks at once for the plan they name (the original or the revised one), in this turn. You may say the report's concern in one sentence, once; do not argue, re-offer or ask them to confirm again. Note in the task's `description` that the work was opened against the study's recommendation and which concern it raised, so the team sees it. A study still running is left to finish (or cancelled with `study_cancel` if they ask); it never blocks the tasks.

## Rules

- No task before the stakeholder answers the offer, and no task during the test unless they override.
- The offer is one question, once per request. Never offer again after "open the tasks now".
- A "yes, test it" is not a yes to spend: building, the script and the start each keep their own yes and call count.
- Never present synthetic findings as customer evidence, and never make the study sound more decisive than it is to win the argument for your recommendation.
- The final tasks describe the plan as it stands after the last revision; the original plan does not reappear unless the stakeholder chose it.

## Worked example

- "Add a yearly plan at 99 dollars" → offer: price and plan change. Yes → `user_interviews` with price points 49, 99, 199 on the reused audience. Report: most say 99 is fine but want a free trial first. Stakeholder: "add a 14-day trial" → `study_rerun` with changes "The yearly plan now starts with a 14-day free trial." → `study_compare`: verdict 5.8 → 7.1, the "no trial" objection is gone. Stakeholder: "OK, open it" → tasks for the yearly plan with the trial, the evidence in the description.
- "Fix the crash on the settings page" → bug, no offer, task straight away.
- "Rewrite the landing hero" → offer. "No, just open it" → task now, no second offer.
