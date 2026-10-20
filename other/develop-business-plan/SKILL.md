---
name: develop-business-plan
description: >-
  Load this skill when anything about a business plan comes up: the single entry point that routes
  to the specialist skill for the moment. Trigger on "write a business plan", "validate my product
  idea", "do the numbers work", "run a premortem", "write a pitch deck".
argument-hint: "[plan-or-idea]"
disable-model-invocation: false
user-invocable: true
license: Apache-2.0
---

# Develop business plan

Route a business-plan request to the one specialist skill that owns its moment, and keep
`BUSINESS_PLAN.md` consistent between specialists. This skill owns only the routing and the rules
below. Every interview, test, and section edit belongs to a specialist. Done is the specialist for
this moment has run and the plan's frontmatter agrees with its content.

## Procedure

1. Find the plan. Glob `**/BUSINESS_PLAN.md` (schema in
   `${CLAUDE_PLUGIN_ROOT}/references/business-plan-schema.md`). When several exist, ask which one.
2. No plan exists → Invoke the Skill tool with skill="ceh-business-plan:find-product-market-fit",
   whatever was asked. It drafts from app plans or supplied material before asking anything. When
   the user asked for a different specialist, say in one line that it needs a plan first. The one
   exception: a request to review a plan, deck, or memo the user supplied goes straight to the
   review row.
3. A plan exists → match the request to a row of the routing table and invoke that skill, passing
   the plan's path. When the request names no moment ("continue", "work on my plan"), read the
   frontmatter: `status: draft` routes to the first row, `status: validated` to the review row.
4. When the specialist returns, re-read the plan's frontmatter. If `pmf_gate` is below `8/8`, set
   `status: draft`. Set `updated` to today.
5. Report in one or two lines what changed and which specialist the result points to next. Invoke
   it only when the user agrees.

## Routing

| The moment                                                                   | Call                                                                            |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| No plan yet, the gate is below 8/8, or the customer or problem is in doubt   | Invoke the Skill tool with skill="ceh-business-plan:find-product-market-fit"    |
| A verdict is wanted before time or money goes in                             | Invoke the Skill tool with skill="ceh-business-plan:review-business-plan"       |
| The plan cannot say why it wins, what it refuses, or what stops a copy       | Invoke the Skill tool with skill="ceh-business-plan:sharpen-strategy"           |
| The numbers must be believed: price, unit economics, runway, break-even      | Invoke the Skill tool with skill="ceh-business-plan:stress-test-unit-economics" |
| The first customers must be won: channel, launch, acquisition                | Invoke the Skill tool with skill="ceh-business-plan:plan-go-to-market"          |
| A hard-to-undo commitment is near, or the question is what could go wrong    | Invoke the Skill tool with skill="ceh-business-plan:run-premortem"              |
| The plan is agreed and work must start: objectives, owners, the next 90 days | Invoke the Skill tool with skill="ceh-business-plan:set-operating-plan"         |
| Money must be raised: a pitch deck, investor outreach, a fundraising email   | Invoke the Skill tool with skill="ceh-business-plan:write-investor-materials"   |

## Rules

- One specialist per request. Chaining them unasked runs interviews the user did not ask for.
- Do not do a specialist's work here. If this skill starts scoring, interviewing, or editing a
  section, the request was routed wrong.
- When a specialist stops on a missing input (no price, no ranked risks, no named customer), it
  names the skill that supplies it. Offer that skill as the next step.
- The status rule in step 4 runs after every specialist, because several of them re-score
  `pmf_gate` and only `find-product-market-fit` sets `status`, to `validated` when the gate
  passes.
- **No human to answer** (a headless run, or called by another agent): when several plans exist,
  take the most recently updated and say which. The specialist drafts and revises from what exists,
  asks nothing, and ends with the questions it would have asked, in order, each with the assumption
  it used instead. Report the next specialist without invoking it.

## Stop conditions

- The request is for the app's technical plan or architecture → say this plugin owns the business
  plan only and name `ceh-build-planning`.
