---
name: start-discussion
description: Use when the user says "/start-discussion", "let's discuss", "I have a problem", "I have an idea", "not sure what to do here", "want to think this through", or otherwise opens an exploratory conversation without yet knowing what shape the work will take. Drives an open discussion to extract context - what's the actual problem, what's the constraint, what would good look like. Once enough intent emerges, routes to /start-feature (or directly to /plan-change). No file outputs - this is talking, not writing. Companion to /start-feature for work where the intent is already clear.
allowed-tools: Bash(gh:*), Bash(git:*), Bash(rg:*), Bash(fd:*), Read, Grep, Glob, Skill
---

# start-discussion - explore before committing to a track

Not every conversation arrives with a known piece of work. Sometimes
the user has a problem they don't yet know how to frame, or an idea
they want to think out loud. `/start-discussion` holds that space.

It does not write files. It does not commit to a track. It draws out
context until the work itself becomes clear - at which point it hands
off to `/start-feature` (or directly to `/plan-change` if the next
move is obvious).

## What this skill does

1. Reflects what the user said back, so they know you heard them.
2. Asks open-ended questions that pull out context, constraints, and
   what "good" would look like.
3. As intent crystallises, names what's emerging and offers to route
   into the right next skill.

## Phase 0 - Open the space

The user has said "let's talk about X" or similar. Reflect what they
said back in one or two sentences, then ask one open-ended question.

Good opening questions:

- "What's the problem you're trying to solve - not the solution, the
  problem underneath it?"
- "What would good look like? Describe the state of the world after
  this is sorted."
- "What constraint is forcing this conversation now rather than two
  months ago?"
- "What have you already ruled out, and why?"

Pick one. Don't fire all four.

## Phase 1 - Pull on threads

Follow the substance of what the user says. Avoid:

- Jumping to a solution before the problem is clear.
- Drafting an ADR mid-conversation (that's `/plan-change`'s job).
- Padding with strawman options the user didn't raise.

Patterns worth listening for:

- **"We considered X but...":** there's already a decision shape.
- **"It would be nice if...":** they're describing the world after,
  which is what a spec captures.
- **"I don't know if this is even a problem":** explore whether it
  belongs in scope at all. Sometimes the answer is "not yet."
- **"Last time we tried this...":** prior art worth surfacing in an
  ADR's Context section later.

## Phase 2 - Name what's emerging

After 3-6 turns, you'll usually be able to say what this is: a feature,
a refactor, a bug investigation, or "still too vague, keep talking."
Surface that read to the user, in your own words. Two things to
include:

- The shape you think the work is taking ("this sounds like a
  refactor of the cancel-order path", "this sounds like a feature
  with a small adjacent bug").
- The substantive constraints you heard - not the whole conversation
  back, just the load-bearing facts.

Then ask whether to move into the planning track now or keep talking.

If the user wants to keep talking, keep going. No quota on discussion
turns. If they're ready, hand off via the Skill tool with the summary
pre-populated so they don't re-explain the problem.

## Phase 3 - Hand off

Invoke `/start-feature` with the summary. The user shouldn't have to
re-explain what was just discussed; the routing into `/plan-change`
or `/backfill-feature` can run with the context in hand.

If the discussion concluded with "nothing to build here" - that's a
valid outcome. Say so. Don't manufacture work to justify the skill.

## Operating rules

- **No file writes. Ever.** Discussion is the output.
- **Don't draft ADRs mid-conversation.** That's a `/plan-change`
  artefact. Tell the user "we'll capture this when we route into
  /plan-change" if they start asking for one.
- **Don't hurry.** Some conversations need ten turns to find the
  thread. Some need three. Trust the user's signal.
- **Surface the "no problem here" outcome.** If exploration reveals
  there's actually nothing to do, name it. Don't pad.

## Composing with other skills

- **Routes into:** `/start-feature` (then onward to `/plan-change` or
  `/backfill-feature`), or `/plan-change` directly when intent is
  clear by the end.
- **Companion entry:** `/start-feature` for work where intent is
  already known.
