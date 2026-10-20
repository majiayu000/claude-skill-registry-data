---
name: write-build-plan
description: >-
  Load this skill when deciding how to build an app or feature before writing code: one committed
  plan file with scope, design decisions, and phases that each end in a runnable check. Trigger on
  "plan this app", "plan the next feature", "how should we build this".
argument-hint: "[what to build]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Write a Build Plan

Turn a request into one plan file that an agent can build from without asking again, in the format
in `${CLAUDE_PLUGIN_ROOT}/references/plan-format.md`. Done means the plan is saved, audited, and
summarized under Output.

## Procedure

1. **Triage, and announce the label in one line.**

   | Label             | The work                                                         | Path                                                  |
   | ----------------- | ---------------------------------------------------------------- | ----------------------------------------------------- |
   | **Spike**         | Throwaway code to answer one question ("can this library do X?") | No plan. Name the question and stop                   |
   | **Bounded**       | One change inside the existing design: no new component or model | A plan of one to three phases                         |
   | **Architectural** | A new app, component, data model, or major version               | A full plan. A new app gets an MVP boundary in step 3 |

   The label may move up mid-session, never down: a spike that turns into a keeper gets a plan, and
   architectural work keeps its plan when it shrinks.

2. **Read what exists before asking.** Read the format file, the repo, every plan in the plans
   folder that is not `built`, and only the frontmatter of each `built` one (read its full text
   only when the new work touches what it built), the README, and any issue or spec the user
   named. When `product/BUSINESS_PLAN.md` exists, set `business_plan` and take the goal and target
   user from it rather than restating them. Put whatever is still unclear into **one round** of
   questions, each with a recommended answer. With no human to answer, take each recommended
   answer and list it under Open.

3. **Draw the scope.** Write In and Out. For each candidate item ask: _is this needed to build
   what was asked, now?_ If not, it goes under Out with its reason. For a new app, In is the MVP:
   the smallest set that makes the app usable for its core purpose. If an item can be removed and
   the app still delivers that, it is Out.

4. **Decide how far to plan in detail.** Plan every phase in full when the build is foreseeable.
   Uncertainty, not size, cuts the detail short: a novel or unproven core mechanic, a decision
   that needs building and seeing first, or an MVP that keeps growing as you discuss it. Then plan
   in full up to the phase that settles the uncertainty, and list the rest as `unplanned`
   one-liners. Detailed phases past an open question are fiction, and building against them
   wastes more than replanning later.

5. **Write the Design.** Only the decisions the phases need, each with its reason. Settle or
   explicitly defer each of these that applies, because each one stops a builder mid-phase when
   it is left open:
   - Auth, and who owns each resource. A resource that exists but belongs to someone else returns
     the same status as a missing one, so the response does not leak that it exists.
   - Pagination on list endpoints, environment variable names, and the migration strategy.
   - Cross-origin requests: allowed origins, and the cookie policy when auth uses cookies.
   - Resources created by an explicit action, never implicitly by the first dependent action,
     which races with a second request arriving before the resource exists.
   - Loading, error, and empty states for every screen that fetches.
   - For an LLM feature: model and provider, how the message list is built from stored messages,
     and what happens when a conversation outgrows the context window.

6. **Sequence the phases.** Foundations first (data model, auth) before the features that use
   them. No phase relies on anything a later phase introduces. Prefer thin vertical slices that
   leave the app demonstrable, but when a foundation and a slice pull against each other, the
   foundation wins. Give each phase a Check a builder can run. More than six phases is a sign to
   re-run step 4.

7. **Audit, then save.**
   - Every In item is built by some phase, and nothing a phase builds is missing from In.
   - Every phase has a runnable Check, or names its manual check and why.
   - No placeholder (`TODO`, `...`, "adjust as needed"), no reference to a file, route, type, or
     field the plan does not define, and no field named differently in two places.

   Save to the plans folder with `status: ready`, or `status: draft` when an Open question blocks
   building. Add the Planned line to the plan's `## Record`, in the format the plan format file
   gives.

## Rules

- One plan per request. Leave a `built` plan as written: new work gets a new plan file.
- Write only the plan file.
- Leave every decision that is not needed now under Out or Open, not in Design.

## Output

Close the reply with:

- The label from step 1 and the plan's path.
- The In list, and the phases one line each with their Check.
- Open: every assumption taken without an answer.

## Hands off to

- For an architectural plan, `ceh-build-planning:review-build-plan` reviews it from a fresh context
  before anyone builds.
- When `ceh-build-from-plan` is installed, `ceh-build-from-plan:implement-from-plan` builds the
  plan phase by phase.
