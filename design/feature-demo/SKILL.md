---
name: feature-demo
description: Build a tap-through demo of a feature so the person can see it before it ships, instead of reading a spec about it. Enumerates the feature's real states, draws them in the app's own colours and fonts, publishes a clickable walkthrough, and annotates each step with the decision behind it. Use when a feature has states nobody can reach by tapping around, when a spec conversation has stalled, when asking for a product decision, or when the person says they cannot picture it.
---

# Feature demo

**A spec gets skimmed. A demo gets opinions.**

The point of this skill is not presentation. It is that a tap-through surfaces the
product questions prose hides, and it surfaces them before the feature is finished
rather than after it ships. The feature this skill came from had its copy rewritten,
a missing screen discovered, and a whole class of user found unhandled, all in the
twenty minutes after the first demo went up, and none of it had come out of two
rounds of reading the spec.

Use it when:

- A feature has states nobody can reach by tapping around (day seven of a seven day
  flow, the empty state, the error, the second time somebody does it).
- You are about to ask for a product decision. A demo gets a real answer; a
  paragraph of options gets "sounds good".
- The person says they cannot picture it, or a spec conversation has stalled.
- You want feedback on copy. Copy read inside a phone frame gets judged like copy.
  Copy in a bulleted list gets skimmed.

Do NOT use it to claim something works. A demo shows intent. Seeing the real thing
on a real device is a different job, and `see-it-work` is the skill for it. Say which
one you did.

## The method

### 1. List the real states first, from the code

Not the happy path. Read the state machine, the card's state union, the hook, and
write down every state it can actually be in. The states that teach you something
are the awkward ones:

- the second time, and the tenth
- somebody who already has the thing the feature offers
- somebody the reward or the offer does not apply to
- the state after the person declines

If a state has no design yet, that is the finding. Put it in the demo as a gap
rather than quietly skipping it.

### 2. Get references before drawing anything

Run `reference-hunt`, or search Mobbin directly if it is connected. Design invented
from scratch reads as invented, and the person will say so. Note which parts came
from a real screen and which are yours, and say so when you hand it over.

### 3. Use the app's own palette and fonts

Read the real token file (`constants/colors.ts`, `constants/tokens.ts`, the theme,
whatever the project calls it) and use those exact values in the demo. A demo in
generic greys gets feedback about the greys. A demo in the app's actual sage and
cream gets feedback about the feature.

Pull the real font too. If the app uses a Google font, the demo can link it.

### 4. Draw a phone, make it tappable

Not a slideshow. The buttons inside the phone should move the flow the way the real
ones do, so the person discovers the sequence by pressing things. Add a numbered
step list beside it for jumping around.

Number the steps only if the feature genuinely IS a sequence. If the states are
alternatives rather than steps, label them instead.

### 5. Annotate the decisions, not the UI

Under the phone, one short note per step saying the thing a screenshot cannot: why
this card retires itself after six showings, why the permission ask sits here rather
than in onboarding, what is claimed at which moment. This is what turns a demo into
a design review. Without it the person can only react to how it looks.

### 6. Publish it and hand over the link

An artifact, or whatever the host offers. One link, and say in one line what you
want them to look at.

## Two ways to build it, and when each is right

**Hand written HTML.** Fastest, works anywhere, no build step. You redraw the
component in HTML and CSS using the app's tokens. The risk is drift: it is a
drawing of the component, not the component, so it can show something the code does
not do. Right for a flow across many screens, for states that do not exist yet, and
for anything you want to tap through.

**The real components, rendered.** If the project has a component preview harness
(react-native-web plus esbuild plus a headless browser), point it at the actual
components and screenshot them. Higher fidelity, and it cannot drift because it IS
the code. Right for reviewing a single card's states and its copy. See
`references/preview-harness.md`.

Doing both is normal: the real components for proof the card looks right, the hand
written tap-through for the flow between them.

## Traps

See `references/traps.md` for the full list with symptoms. The ones that cost the
most time:

- **A modal renders into a portal and your screenshot comes back blank.** The
  content is in the DOM and not in the capture. Give the component a preview-only
  prop that renders it inline.
- **Headless Chrome does not advance animation.** Fine for static cards. For a
  mid-animation frame you need a real browser driver with real waits.
- **Copy that reads fine in a spec reads robotic in a phone frame.** This is the
  demo doing its job. Expect to rewrite copy after the first look, and check your
  own house style has not been over-applied: a rule against dashes is not a rule
  against apostrophes.
- **A label that works on a button does not work in a sentence.** "Log breakfast"
  as a button, "Seven days of log breakfast" in a sentence. Give each item both
  forms.

## Finishing

Hand over the link and say three things:

1. What you want them to look at.
2. Which parts are referenced from real apps and which are your own.
3. That this is a demo, not proof it works, and what the real thing still needs
   before anyone can trust it.

Then expect changes. A demo that comes back with no feedback usually means it was
too polished to argue with, or it only showed the happy path.
