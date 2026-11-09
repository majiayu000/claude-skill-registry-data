---
name: problem-to-product
description: Use when someone wants to turn a problem they personally keep running into into a product they would use every week, write a product brief from their own problem, plan requirements and a roadmap before any code, or keep a first-user log while using their own tool. Triggers include "turn this problem into a product", "write a product brief", "I keep failing at X, should I build something?", "plan this before I code", "log today's use of my tool", "is my tool ready to be a product?". Not for scoring ideas you don't personally have (use evaluate-side-project) or for portfolio demos (use proof-project).
---

# Problem to Product

Take one problem the user keeps failing at and walk it toward a product, with the user as the first user. The path has five stages, and each one ends with a question:

1. **Name the problem.** Can you say when it hurts, without naming a tool?
2. **Plan before code.** Does the plan fit in phases small enough to ship on evenings?
3. **Smallest loop.** Did the pain stop for you, at least on the days you used it?
4. **Use it on your own work.** Would you be annoyed if the tool disappeared tomorrow?
5. **Decide what makes it a product.** Can you explain the price with what the product costs you to run?

This skill covers stage 1 (BRIEF mode), stage 2 (PLAN mode), and stages 4-5 (LOG mode). Stage 3 is building, which the user does with their normal tools.

Pick the mode from context:

- **BRIEF**: the user describes a problem, an annoyance, or a product idea, and there is no `BRIEF.md` yet.
- **PLAN**: a `BRIEF.md` exists and the user wants requirements, non-goals, or a roadmap.
- **LOG**: the user has a working tool and just used it, or wants to know whether it is ready to become a product.

If unclear, ask: "Do you want to write the brief for a problem, plan from an existing brief, or log a session with a tool you already use?"

---

## BRIEF mode

### Step 1: Interview, one question at a time

Your goal is a one-page product brief, not a solution.

Rules:
- Ask one question at a time. Wait for the answer before the next one.
- If the user answers with a solution ("I need an app that..."), ask what happens on the day the problem hits instead.
- Never suggest a product, tool, or feature until the brief is written.

Cover these in order:
1. The moment: when exactly does the problem hurt? Ask for the last time it happened.
2. The cost: what does the user lose when it happens (time, money, missed work)?
3. What they tried: tools, habits, workarounds, and why each one stopped working.
4. Fixed: what would a normal week look like if the problem were gone?
5. Smallest loop: the least they could build that removes the pain for them alone.
6. Manual on purpose: what must stay in their hands, even if it could be automated.
7. Before pricing: what they should measure while they use their own tool.

Follow up on vague answers ("it depends", "usually", "people like me"). Ask for the last real time it happened. The useful details live in those follow-ups.

If the user can't name a single moment when the problem hurt in the last month, say so plainly: this may not be their problem yet, and a product built on it has no first user.

### Step 2: Write the brief

Copy `assets/brief-template.md` to `BRIEF.md` in the current folder and fill it in, one heading per area, under one page. Use the user's own words where you can.

End with the "I guessed these" list: every statement in the brief the user didn't actually say. Ask the user to confirm or correct each item, then update the brief.

### Step 3: Close the stage

Write the problem as one sentence that includes the moment it hurts and names no tool. Ask the user: "Can you say when it hurts, without naming a tool?" If the sentence still names a solution, rewrite it with them before moving on.

---

## PLAN mode

Read `BRIEF.md`. Produce two documents, one at a time, and stop for the user's approval after each.

### Step 1: Requirements with non-goals

Write `REQUIREMENTS.md`:
- **Requirements**: what the smallest loop must do for the user, each one testable.
- **Non-goals**: features the user agrees not to build, each with the reason. Take every item from the brief's "Manual on purpose" section and add it here.

Stop and ask the user to approve or edit it.

### Step 2: Roadmap in small phases

Write `ROADMAP.md`: phases small enough to finish in a few evenings each. Phase 1 is the smallest loop from the brief and nothing else. Every phase must leave something that works if the user stops there. Pricing, billing, and onboarding for other people come after the user has run their own tool for a few weeks, never in phase 1.

Stop and ask: "Does the plan fit in phases small enough to ship on evenings?"

---

## LOG mode

### Step 1: Record one session

If there is no `FIRST-USER-LOG.md`, copy `assets/first-user-log.md` to the project folder. Then add one entry for the session the user just had, asking only what they haven't told you:

- What the tool got wrong.
- What they fixed by hand.
- What they refused to let it do.
- Whether the pain came back on a day they didn't use it.

Keep each entry short and dated. Use their words.

### Step 2: Review when asked, or after every fourth entry

Read the whole log and report:
- **Still a first user?** Count the weeks with at least one entry. If the log went quiet for two weeks or more, say so: the user stopped using their own tool, and that is the answer to stage 4.
- **Guardrails**: things they refused to let the tool do more than once. Propose each as a written product rule.
- **What to measure before pricing**: things they always fix by hand, and the cost of each run if they recorded it.
- **Stage 4 question**: "Would you be annoyed if the tool disappeared tomorrow?" Answer with entries from the log, not with a feeling.

Only when the stage 4 answer is yes, move to stage 5: ask the user to write down what the product will and won't do for strangers, and to explain the price with what one real run costs them.

---

## Principles

- The user is the first user. If they won't use it every week, nobody else will either.
- Problem before solution, in every mode. Push back on answers that jump to a tool.
- Never invent facts about the user's problem, usage, or costs. Unknowns go in "I guessed these" or stay as open questions.
- One document at a time, each approved before the next.
