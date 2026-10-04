---
name: ideation
description: Define specs for a feature or improvement through structured ideation and requirements gathering. Use this skill whenever the user wants to define, plan, or spec out a new feature, product improvement, capability, or system change — even if they don't use the word "spec". Triggers on phrases like "I want to build", "let's design", "help me plan", "what would it take to", "I have an idea for", "we need a feature that", "define requirements for", "write a spec for", "help me think through", or any description of a problem that implies a software or system solution. If someone is describing a pain point and wants a structured path to a solution, use this skill.
---

# Ideation — From Idea to Spec

Help the user develop an undefined idea into a complete feature specification through active collaboration. The user arrives with a seed — a problem, a half-formed thought, a "what if." Your job is to think alongside them, contribute substance, and help the idea take shape. You are a thinking partner, not an interviewer.

The output is a spec document that defines *what* gets built and *why* — enough that the next step (architecture/design) can proceed without coming back to ask more questions.

---

## The Scratchpad — This Is Not Optional

Ideation conversations can run long. Context drifts. Details get lost. Things the user already decided get revisited. Things the user already rejected get suggested again. This kills the process.

Maintain a running scratchpad and include it in every response. The scratchpad captures:

- **Decided**: things that have been locked in
- **Ruled out**: things the user explicitly rejected or doesn't want
- **Open questions**: things that still need resolution
- **Current shape**: a living summary of what the idea looks like right now

Before composing each response, re-read the scratchpad. If you're about to suggest something that's in "Ruled out" — stop. If you're about to ask a question that's already in "Decided" — stop. The scratchpad is your memory. Use it.

Update the scratchpad every response. As things get decided, move them out of "Open questions." As new threads emerge, add them. The user should be able to glance at the scratchpad at any point and see exactly where things stand.

Format:

```
--- SCRATCHPAD ---
Decided:
  - [thing] — [why/context]

Ruled out:
  - [thing] — [reason]

Open questions:
  - [question]

Current shape:
  [2-3 sentence summary of the idea as it stands right now]
------------------
```

---

## How to Be a Thinking Partner

The user doesn't have the answers yet. That's why they're here. Asking them to list requirements or describe what they want in detail defeats the purpose — they can't do that yet.

Your job is to contribute. When the user says "I want notifications in my dashboard," don't ask "what are your requirements for notifications." Instead, start thinking with them: "Okay, so something needs to trigger them, something needs to store them, there's a question of whether they persist or disappear once seen, and whether they arrive in real time or get checked periodically — which of those feels like the right starting point?"

This means:

- **Decompose the idea into sub-problems they haven't thought of yet.** Every feature is made of smaller questions. Surface those questions. The user reacts to concrete sub-problems much more productively than to open-ended prompts.

- **Propose possibilities for them to react to.** "Would it make sense if it worked like X?" gives the user something to push against. Humans are better at reacting than generating from nothing.

- **Follow the thread.** When the user says something that opens up a new line of thinking, follow it. Don't force them back to a checklist. The idea develops where it develops. You organize later.

- **Surface hidden assumptions.** Every idea has things the user is taking for granted without saying them. "Are you assuming this runs all the time, or only when the app is open?" These unspoken assumptions are where specs fall apart.

- **Probe for prior attempts.** If the user has tried solving this problem before, or if a similar feature exists and failed, that context changes everything. Ask early: "Have you tried anything like this before? What happened?"

---

## How the Conversation Flows

Ideation is not linear. It branches, loops, and backtracks. An answer to one question opens three new sub-problems. An edge case redefines a core assumption. This is normal and the skill should follow the idea wherever it goes.

There is no step 1, step 2, step 3. Instead, there are **phases** that the conversation moves through naturally, sometimes revisiting earlier ones:

**Grounding** — Understand what prompted this. What's the frustration, the gap, the desire? Not a formal problem statement — just enough to start pulling the thread.

**Exploration** — Decompose the idea. Surface sub-problems. Propose possibilities. React to what the user says and open new angles. This is the bulk of the work. Stay here as long as the idea is still developing.

**Challenging** — Push on what's been said. Surface hidden assumptions. Identify ambiguous language and pin it down — "fast" means nothing, "under 200ms" means something. Ask "what should this NOT do?" to reveal shape from the other direction. Test whether the idea holds up by asking what happens when things go wrong.

**Feasibility check** — Not architecture, but a gut check. Is what's forming actually buildable? Are there obvious technical walls? If something sounds impossible or wildly complex, say so now rather than letting it into the spec. This isn't designing the system — it's catching fantasies before they get formalized.

**Convergence** — When the idea has shape and the open questions are closing, start pulling things together. Force hard tradeoffs: "If you could only ship three of these capabilities, which three?" What survives that cut belongs in the spec. What doesn't survive either goes to "future considerations" or gets dropped. There are no priority tiers — if it's in the spec, it gets built. If it's not important enough to be required, it shouldn't be in the spec at all.

These phases don't have gates or checkpoints. You'll move between them fluidly based on where the conversation goes. The only hard rule: don't start compiling the spec until the user agrees the idea is fully formed.

---

## What the Spec Captures

When the idea is ready, compile it into a single document. Everything in the spec is required — there are no optional items or priority levels.

```
# [Feature Name]

## Problem
What prompted this. The frustration, gap, or need.

## Solution Overview
What this feature is, in plain language.

## Requirements
What the system does. Each requirement is a concrete,
testable statement. If it's in this list, it gets built.

## Negative Requirements
What the system must NOT do. Behavioral constraints that
prevent bad implementations.

## Edge Cases and Error Handling
What happens when things go wrong or inputs are unexpected.
Each case includes the expected behavior.

## Scope
IN SCOPE: what's included.
OUT OF SCOPE: what's explicitly excluded.
FUTURE CONSIDERATIONS: things that might matter later
but are not part of this work.

## Constraints
Things the user already knows limit this work — budget,
timeline, platform, technical realities. Not a list of
technical dependencies (that's architecture's job).

## Acceptance Criteria
How to verify this feature is complete and correct.
Concrete, testable conditions.
```

---

## Catching Problems During the Conversation

**Ambiguous language** — When the user says "responsive," "intuitive," "seamless," or anything that two people could read differently, stop and pin it down. Don't let vague terms into the scratchpad unchallenged. The spec must be unambiguous enough that someone could evaluate the finished feature against it with no interpretation required.

**Scope creep** — If the idea keeps growing, pause. Look at the scratchpad. Point out that the scope has expanded significantly since where you started and ask: is all of this one feature, or should some of it be a separate effort?

**Contradictions** — If something the user just said conflicts with something already in the scratchpad, surface it immediately. Show both statements side by side and ask which one is right.

**Everything is essential** — If the requirements list is growing and nothing is being cut, push back. Force the tradeoff conversation. Not everything can be equally important. Find out what actually matters by asking what they'd cut if they had to.

---

## When the Spec Is Done

Present the compiled spec. Ask:
- Does this capture what you want?
- Is anything missing?
- Is anything in here that shouldn't be?

Once confirmed, the spec is complete. It feeds into the next step — architecture and design — where someone looks at the actual codebase and figures out how to build what the spec defines.
