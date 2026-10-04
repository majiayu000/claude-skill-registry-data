---
name: demo-narrative
description: Use when preparing a sales demo, an investor demo, a partner walkthrough, or any scripted product flow with talking points. Use 48-72 hours before the live demo so there's time for dry-run, seed data verification, and fallback rehearsal.
---

# Demo Narrative

## Overview

Produce a scripted, scene-by-scene demo flow with talking points, wow moments, fallbacks, and a seed-data checklist — *before* the live demo. Output is `.forge/demo-narrative.md`: the audience and goal, the one key insight the demo must land, the scene script, the fallbacks, the Q&A anticipation, and the dry-run checklist. Pairs with `seed-data-and-fixtures` (the data backing each scene) and `gtm-strategy` (the wedge feature the demo is selling).

## When to Use

- A sales, investor, or partner demo is scheduled in the next 7 days
- A product walkthrough is being recorded
- A pitch deck is being built and the demo flow needs scripting
- The team has done "ad-hoc product walkthroughs" before and lost deals or stalled them

## When NOT to Use

- Pre-product, no working software yet — use `gtm-strategy` and `competitive-analysis` instead
- A demo for an internal audience that has full context — informal walk is fine
- The user-facing surface isn't ready and the demo would expose work-in-progress

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "Just show the features" | Feature parades don't sell. Stories sell. The audience remembers the moment, not the bullet list. |
| "We don't need a dry-run, we'll wing it" | The demo that crashes live is the one you didn't rehearse. The cost of one crashed demo > the cost of every dry-run you'll ever do. |
| "The data doesn't matter, they get the idea" | Dead-state UI with lorem ipsum kills credibility instantly. The audience pattern-matches "fake" and disengages. |
| "We can improvise the talking points" | Improvisation without preparation is rambling. The audience reads rambling as "they don't know their own product." |
| "Fallback is for cowards" | Fallback is for people who've ever lost a deal to a 502. Every live system breaks; preparation decides whether the audience notices. |
| "We don't need a wow moment, the product speaks for itself" | The audience has seen 12 demos this quarter. Without a wow moment, the demo is forgettable, which means the product is forgettable. |

## Red Flags

- A demo scheduled in <48h with no dry-run done
- Lorem ipsum, "Test User", or all-now() timestamps visible in any scene
- No fallback plan if a live API call fails
- No identified wow moment — the demo is "let me click through the menus"
- Feature parade structure ("here's the dashboard, here's the settings, here's the reports")
- Demo length unbudgeted, no buffer for questions
- Slack/email/notifications visible on the screen sharing surface
- Screen recording or live demo without testing the network the demo will use

## Core Process

### Step 1: Define audience + goal

Write at the top of `.forge/demo-narrative.md`:
- **Audience:** who (role, seniority, prior context). What they care about (cost / speed / risk / status quo).
- **Goal:** the *one* decision you want them to make after watching. Examples: "agree to a pilot", "introduce us to the security team", "wire transfer for Q3 commit".
- **Time budget:** 30 min total → 18 min demo + 12 min Q&A. With 20% buffer.

### Step 2: Identify the one key insight

The demo must land **one** insight — the audience-shaped reframe of the product. Examples:
- "Your team is spending 4 hours/week on this; we make it 4 minutes."
- "Every existing tool requires X to use; ours requires nothing."
- "The data you already have can answer Y in real time."

Write the insight as a single sentence. Every scene in the demo serves this insight.

### Step 3: Write the scene-by-scene script

5-7 scenes. Each follows: **setup → tension → wow → resolution.**

Per scene, document: scene goal, setup talking track, tension, wow moment, resolution talking track, required seed function, fallback (recorded GIF or screenshot), and time budget. Example:

```markdown
### Scene 3 — "The 4am page" (3.5 min)
Goal: show the runbook auto-resolving a paging incident.
Setup: "You've had a 3am page. The on-call gets out of bed, and..."
Tension: alert fires, walk through what an engineer normally does.
Wow: click "Auto-mitigate", service recovers in 8 seconds, show audit log.
Resolution: "A 6-hour incident compressed to one click."
Seed: seedDemoIncidentScene() — incident at 03:14:22 UTC, runbook-001 alert.
Fallback: if auto-mitigate fails live, switch to assets/demo-incident.gif.
```

Each scene ends with a transition that hands to the next. No "next, let me show you..." — every transition reinforces the insight.

### Step 4: Identify fallbacks for every scene

For every live action:
- What can fail (network, API, browser, third-party dependency)
- The fallback (recorded GIF, prebuilt screenshot, narrated story)
- The trigger ("if the spinner runs longer than 5 seconds, switch to the GIF")

Each fallback is rehearsed during the dry-run. The audience never sees the switch.

### Step 5: Write the seed data checklist

Cross-reference `seed-data-and-fixtures`. For every scene:
- The named seed function (`seedDemo<SceneName>()`)
- The state the scene assumes (logged in as @demo-user, dark mode off, no notifications)
- The reset script (between scenes if needed)

Verify the seed runs cleanly in the demo environment within 48h of the demo.

### Step 6: Prepare Q&A anticipation

List the top 10 questions the audience will ask, with prepared answers. Examples:
- "What about security/compliance?" → cross-reference `security-and-compliance` skill summary
- "How is this priced?" → cross-reference `gtm-strategy`
- "Who else uses this?" → 3 named reference customers if available; honest if not
- "What's your moat?" → cross-reference `competitive-analysis`

Mark questions that the demo-runner should *not* answer in the room and should redirect to a follow-up.

### Step 7: Run the dry-run checklist

Within 24h of the demo:

- [ ] Demo runs end-to-end on the exact machine + network that will be used
- [ ] Every scene's seed data is loaded and verified
- [ ] Every wow moment fires correctly
- [ ] Every fallback rehearsed (intentionally trigger each failure mode once)
- [ ] Notifications, badges, Slack, email — silenced and hidden
- [ ] Screen sharing tested with the actual conferencing tool
- [ ] Demo fits in time budget with 20% buffer
- [ ] Demo-runner can articulate the one key insight without notes

### Step 8: Header

Prepend a `forge:meta` header to `.forge/demo-narrative.md` (`generated_by: demo-narrative`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/seed-data.md]` if `.forge/seed-data.md` exists else `[]` — paths only, never hashes, `generated_from: {.forge/seed-data.md: <upstream content_hash AT generation time>}` if seed-data exists else `{}`, `content_hash: <sha256 first 8 of THIS file's body>`). See [forge-dependency-graph](../../references/forge-dependency-graph.md).

## Verification

- [ ] `.forge/demo-narrative.md` written
- [ ] Audience, goal, and one key insight stated in one sentence each
- [ ] 5-7 scenes scripted with setup/tension/wow/resolution
- [ ] Every scene has a named seed function in `.forge/seed-data.md`
- [ ] Every scene has a fallback plan
- [ ] Top 10 Q&A items prepared
- [ ] Dry-run completed within 24h of the demo
- [ ] Zero lorem ipsum or "Test User" in any scene
- [ ] Demo fits time budget with 20% buffer
