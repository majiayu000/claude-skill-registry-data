---
name: idea-calibrate
description: Turn a raw idea into a calibrated, testable v1 plan before any code. Use when you have only an idea, a rough brief, or a feature request, and need the problem, user, success criteria, assumptions, and non-goals confirmed. Only invoke via the orcinus router.
license: MIT
user-invocable: false
---

# IDEA-CALIBRATE — from raw idea to a plan you can build

Turn a vague idea into a brief that is sharp enough to code from, and no sharper than the evidence allows. Do not write code here. Do not choose a stack. Do not start building until the gate at the end is confirmed by the user.

## Rules

- The problem comes before the solution. No feature, no architecture, no stack until the problem and the user are written down.
- Decisions are the user's. Ask, recommend, wait. Never decide for them.
- Assumptions are assumptions. Write them as such, with the cheapest test that would prove or kill them. Never present a guess as a fact.
- If you do not know, ask. Guessing a user, a need, or a number is a failure, not a shortcut.
- One round at a time. Ask the frontier — every question whose prerequisites are already settled — in one round, with a recommended answer for each. Wait for the answers before the next round.

## Steps, in order

### 1. Capture the raw idea

Write it down verbatim, with the date and who said it. Do not edit, improve, or interpret it yet. A fleeting idea that is not captured is lost. If the idea arrived outside this session, it should already be in the store — pull it from there with `idea-capture` instead of re-typing it.

### 2. Clarify the problem

Ask until these are written in one sentence each:

- **Problem:** what hurts, for whom, how often, and what happens if nothing changes?
- **User:** one specific person, not "everyone" and not "users".
- **Current workaround:** what do they do today instead?

If the problem and the user are the same sentence, they are not clear enough yet. Keep asking.

### 3. Nurture: problem → opportunities → solutions

Build a small tree, in that order:

- One problem.
- Two or three opportunities under it (different ways the problem could be eased).
- One or two solutions under each opportunity.

Do not add a solution that does not hang off an opportunity, and do not add an opportunity that does not hang off the problem. Cut any branch the user does not care about.

### 4. Validate: assumptions and cheapest tests

List every assumption the plan depends on. Rank them by risk (importance × uncertainty). For the top two or three, name the cheapest test that would prove or kill each one, and what evidence would change the decision. If no test is possible, say so — that assumption stays a risk, not a fact.

### 5. Pre-mortem

Imagine it is six months later and the project failed. List the three most likely causes. For each, name one thing to do now that would prevent it or make it visible early.

### 6. Scope v1

Write down:

- **Must-have:** the smallest set that proves the idea works.
- **Nice-to-have:** explicitly out of v1.
- **Non-goals:** what this project will not do, even if asked.
- **Success criteria:** measurable, with a number and a date. "Better" is not a criterion.
- **First slice:** one behaviour, with one test, that can be built first.

## Gate: Idea → Code

Stop here. Present the calibrated brief (below) and ask the user to confirm it in writing. Do not start coding, scaffolding, or choosing a stack until they confirm the problem, the user, the success criteria, the non-goals, and the first slice. If they change anything, update the brief and confirm again.

## Output: the calibrated brief

Return the brief in this form, no more, no less:

- Raw idea (verbatim, with date)
- Problem (one sentence)
- User (one specific person)
- Current workaround
- Opportunity tree (problem → opportunities → solutions)
- Assumptions, ranked, with cheapest tests
- Pre-mortem (three causes, three preventions)
- v1 scope (must-have / nice-to-have / non-goals)
- Success criteria (measurable)
- First slice

## Sources

Method, in our own words, inspired by: grilling (mattpocock/skills, MIT) for the frontier interview; egm-brainstorm / egm-draft for sharpening; phuryn/pm-skills (MIT) for the opportunity-solution tree, assumption mapping, pre-mortem, and prioritization frameworks. No text was copied from those projects.
