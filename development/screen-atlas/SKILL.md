---
name: screen-atlas
description: Build a browsable catalogue of every screen in the app, captured from a running build and grouped into the journeys people actually walk, so you can see what each flow does without opening the app. Finds screens nothing navigates to as a side effect. Use when the user says they cannot picture how the app flows, wants a Mobbin for their own app, asks for screenshots of every screen, wants to review the whole app at once, or is about to redesign a flow and needs to see what is there now.
---

# Screen atlas

Someone who has built every screen themselves can still lose the shape of the
whole app. The fix is not a diagram, because a diagram is drawn from memory and
drifts. It is the real screens, in order, on one page.

**What this produces:** one self contained HTML file, grouped into flows, each
step captioned with what that screen is for. It lives in the repo and is
gitignored, because it is megabytes of screenshots that go stale the moment a
screen changes.

**The honesty rule, and it is the whole credibility of the thing.** The images
are real captures. The ORDER is written by hand from the navigation calls. Those
are different claims and the page must say so on its face. Never describe a hand
written sequence as a recorded journey.

## 1. Check the app has the seam, or stop here

This needs two things, and most apps have neither:

| Needs | What it is |
| --- | --- |
| A seed deep link | A development only URL that puts the app into a known state and lands on any named screen |
| A screen manifest | A list of every navigable screen, how to reach it, and what proves it rendered |

If the app has a smoke or end to end tier, it probably already has both, and
the manifest is the one in that tier. Reuse it. Do not write a second list of
screens: two lists disagree within a month, and the one nothing enforces is the
one that rots.

If the app has neither, say so and offer to build the seam first. The
`see-it-work` skill covers that, and it is a bigger job than the atlas.

## 2. Enumerate the screens

Read the manifest. Count what is reachable and what is deliberately skipped
(anything needing a camera, a real purchase, or hardware a simulator lacks).
Report both numbers. A catalogue that quietly omits the skipped ones is lying
by a smaller amount than one that fakes them, but it is still lying.

## 3. Capture them

Drive the manifest, one screen per case: stop the app, launch it, wait until it
is drawing, fire the seed, wait for the screen's anchor, screenshot.

**Read `references/capture-traps.md` before writing any of this.** Four traps
are in there and every one of them produces a run of failures that look like
broken screens and are not. The short version:

- A seed link fired before the router is listening is **lost silently**. Launch
  first, and wait long enough.
- A seed may be claimed **once per process**, so a run that does not restart
  between screens is refused with no error.
- An "optional" tap in a flow runner is **not failure proof**.
- **The duration tells you which failure you have.** Fast is the driver. The
  full timeout is the screen.

Two rules for the capture itself:

- **Shoot only after the screen is confirmed.** A screenshot taken before the
  anchor appears is a picture of a splash screen filed under a real screen's
  name, which is worse than a missing tile because nothing downstream can tell.
- **A retry belongs here and not in the release gate.** A gate that retries
  hides flake and stops being believed. A catalogue has the opposite priority:
  a missing tile for a healthy screen is the bad outcome.

## 4. Group them into flows

Trace the real navigation calls in the code. Do not invent the order from what
seems sensible: in a real run of this, two inferred sequences were wrong, and
tracing caught both.

For each flow write an id, a title, one line on what it is for, and the ordered
steps. For each step, one line on what that screen is for.

**Write it the way a person talks about the product.** The step note is for
someone thinking about the app, not reading the code. Say "the button in the
bottom right corner", not the component name.

**Record the screens that no flow reaches.** Give them their own section with
the reason, rather than dropping them. This is the most useful thing the atlas
produces and the easiest to lose: a screen can render perfectly, pass its test,
and be reachable by nothing. The first real run of this found three.

## 5. Build the page

One HTML file. Each flow is a block: title, summary, then a horizontally
scrolling strip of phone frames in order, numbered, each captioned.

- **Deduplicate the images.** A screen can appear in several flows. Inlining it
  per frame pays for its bytes every time: one build spent 1.4MB on a single
  captured screen before this was fixed. One CSS rule per screen, referenced by
  class, pays once.
- **Downscale.** Around 640px wide at JPEG quality 72 is plenty for review and
  is roughly 75KB a screen.
- **Numbering is earned here.** A flow IS a sequence, so numbered steps encode
  something true. Do not number things that are not ordered.
- **If it opens a larger view, give it three ways out:** a visible close button,
  Escape, and a click outside the image. A full screen overlay with no exit is
  the single worst thing this page can do, and a plain `display` rule on a
  `dialog` element will paint one over the page from the moment it loads.

## 6. Gate it so it cannot rot

The atlas is a second list that can disagree with the app, so wire two checks
into whatever the project runs before a commit:

- A flow naming a screen that no longer exists.
- A real screen that sits in no flow and is not recorded as having no entry
  point.

**Then break it both ways and watch it go red.** A check nobody has seen fail is
not a check.

Neither of these can catch a step ORDER that has gone stale, which is the
likelier rot. Say that in the file rather than implying the gate covers it.

## Finishing

Tell the user where the file is and how to rebuild it. Give the counts: flows,
screens, captured, skipped. Name anything the atlas found, especially screens
nothing reaches.

Do not publish it anywhere the user did not ask for. It is a picture of every
screen in an unreleased product, including developer tools and paywalls.
