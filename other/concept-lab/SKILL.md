---
name: concept-lab
description: "Build 3-5 real concepts side by side and let the user pick one. Use when the user says \"show me options\", \"explore some concepts\" or \"run a design round\"."
license: MIT
metadata:
  author: Tony Gorb
  source: https://github.com/tonygorb/skills
  category: design
  cover: "3-5 tabs"
---

# Concept lab

A design round with an agent: a few genuinely different concepts, built in the real page, shown
side by side. The human picks. The agent never decides. Then build only the pick and clean up.

```
question -> read -> references -> lab -> verify -> [PICK] -> write it down -> build the pick -> clean up
```

## When a round is worth it

Explore only when exploring changes the answer.

- Run a round when the structure or hierarchy is wrong, or something needs to move to another
  screen.
- If the fix is "smaller", "quieter" or "reword it", skip the round and make the edit.
- If the design system already decides it, or the notes say this was tried and rejected, don't
  reopen it. Point to the decision.

## Steps

1. **Settle the question.** Write it in one sentence: "Which layout makes the main action
   obvious?" If the request doesn't name one surface, or names a shared component used in many
   places, ask which in one line. Scope is the user's call.
2. **Read what's there.** Open the live screen and its source. Check the empty, error, long-text
   and many-items states. List what it already uses: components, spacing, type, colours, grid.
3. **Gather references.** Source options from real work: shipped products and well-known studios
   in the same field. Keep the link or name for each one. If an idea comes from the page's own
   grid rather than a reference, say so. Never present an invented pattern as a reference.
4. **Build the lab.** A dev-only page or route, never in the production build (check the build
   config). For each concept:
   - Render it inside the real page, with only the section under review swapped.
   - Use the real design tokens, components and icons. Put fake data in one file.
   - Put every element on the page's own columns. Make the block respond to its container, not
     only the viewport.
   - Give it its own folder and class prefix so two concepts can't collide.
5. **Make them different.** Three to five concepts, each a different hypothesis. If two differ
   only in padding or colour, they are one concept. Keep the count you agreed; don't silently drop
   one.
6. **Show them as tabs.** One round, one page:
   - The question as the heading, one tab per concept.
   - In each tab: a desktop frame (1440 wide) and a phone frame (390 wide) side by side, the same
     fixed height, each page scaled to fit (never above 100%) and scrolling inside its frame.
   - One line of notes per concept. People don't read long notes.
   - An "Open in the full page" link, so the concept can be judged in context.
   - A link per tab (`#c3`), so "look at 3" opens 3.
7. **Verify the lab as the human will see it.** Same URL, real viewports. Open every tab and
   take screenshots. Look for tiny scaled text, half-empty frames, things off the grid. Measure
   positions in the browser; don't eyeball. Only then say it's ready.
8. **Stop at the gate.** Hand over the URL and wait. See "The approval gate".
9. **Write it down.** Before anything is deleted, record the verdict in the project's notes
   file: what was approved, what was rejected and why, and how the pick works (sizes, behaviour,
   desktop and phone). Someone who never saw the lab must be able to build it from the notes.
10. **Build only the pick.** Carry its composition faithfully. Take the look, the layout and the
    behaviour from the concept; take data, routing and components from the real app. If part of
    it turns out wrong or impossible, say so and ask. Don't quietly redesign it.
11. **One sample before the rollout.** If the pick applies to many items or screens, build one,
    show it, get a reaction, then roll out. Show each new item before wiring it in.
12. **Clean up.** Remove the rejected concepts from the lab; remove the approved one once the human
    has seen the real build. Grep for its class prefix and file
    names, then run lint, typecheck and build to prove nothing still points at it. Delete only
    your own round.

A tiny sketch of a round, in no particular framework:

```
/dev/lab/<topic>                      # dev only, excluded from the production build
question: "Which layout makes the main action obvious?"
concepts:
  - { id: c1, name: "Single column", note: "One action, full width, everything else below." }
  - { id: c2, name: "Split",         note: "Action left, context right; stacks on phone." }
  - { id: c3, name: "Sticky bar",    note: "Action pinned to the bottom edge on scroll." }
section(id) -> the page with only the section under review, swapped to concept <id>
full(id)    -> the whole page with concept <id> in place
```

## The approval gate

- The human approves one concept, by name or number, in words.
- A concept is not approved because it exists, because it's the newest or because you like it.
- "I approved 3" is a claim. Check it against the lab's list and the notes before building.
  If they disagree, ask.
- "Proceed" after one sample approves that sample, not the ones the human hasn't seen.
- Picking which concept wins is never the agent's decision, however obvious it looks.

## When rounds keep missing

After two rejected rounds, stop making variants. Switch to the short loop:

1. Show real references and let the human pick by number.
2. Make one quick sample, in minutes.
3. Get the reaction, adjust, repeat.
4. Only then roll it out.

Long builds based on your own reading of someone's taste cost hours per rejection. A picked
reference and one sample cost minutes.

## Before it's done

- The verdict is in the notes file, approved and rejected.
- The pick is built and checked at desktop and phone in the real page.
- Superseded concepts are gone. Keep the approved one until the human has seen the real build,
  unless they ask for it sooner; it's the only comparison.
- Nothing in the codebase still references the lab round.

## Never

- Never build concepts as mockups or screenshots outside the real page.
- Never invent a new component or colour for a concept when the system has one.
- Never pick the winner yourself.
- Never delete the lab before the verdict is written down.
- Never roll a pick out to everything before one sample is approved.
- Never say the lab is ready without opening it at the URL the human will use.

## Red flags

- "These five are different enough." If two differ only in spacing, merge them.
- "The frames look fine scaled down." Text you can't read is a broken concept, whatever the idea.
- "They said proceed, so the rest are approved." Show each one first.
- "One more round of variants will land it." After two misses, go to references and one sample.

## What to hand back

At the gate: the lab URL, the question, and one line per concept. After the build: what was
approved, where the verdict is recorded, what changed, and what was removed.
