---
name: anti-slop
description: Stops your agent from sounding like ChatGPT - no generic, padded, templated or invented output, and it tells you when something might read as AI-made. Before delivering anything (text, design, code, copy, video scripts, data), check it for anything that is or could look like generic AI output, and tell the user explicitly what you found. Use on every deliverable, and whenever the user asks to review something for "AI look", "slop", "sounds like ChatGPT", "generic" or "template-y".
author: sant1jmnz
tags:
  - writing
  - review
  - quality
---

# Anti-slop (rule #1)

**AI slop is forbidden.** Slop = output that looks mass-produced: generic, padded, templated, unverifiable, made without real judgment. Readers spot it in seconds and it destroys trust in everything around it.

Two obligations, always:

1. **Don't produce it.** Make specific, intentional, verifiable things.
2. **If something might be or look like slop, say so.** Never ship it silently. Tell the user what it is, why it reads as slop, and what you did or propose to fix it.

## How to apply (before every deliverable)

1. Re-read your own output as a skeptical stranger. Scan the checklist below.
2. Fix what you can without losing the user's intent.
3. Report. End the deliverable with one short block, only if there is something to report:

   > **Possible AI-slop:** `<what>` in `<where>` — looks generic because `<reason>`. Fixed: `<yes/how>` / Proposal: `<fix>`. Want me to redo it?

   If you checked and found nothing, say nothing (no ceremony). If you can't avoid placeholder or generic content (for example, a draft with sample copy), label it clearly as a placeholder.

## Checklist

**Text and copy**
- Stock openers/closers: "In today's fast-paced world", "Let's dive in", "In conclusion", "I hope this helps", "Unlock the power of", "game-changer", "seamless", "elevate", "delve", "tapestry", "landscape".
- Rhythm tells: everything in threes, staccato fragment stacks, reveal bridges ("Here's the thing:"), performed sincerity, rhetorical questions as filler, em dashes everywhere, emoji storms.
- Vague claims with no source, number or example. **Invented** stats, testimonials, reviews, client names, results: absolutely forbidden.
- Padding: restating the question, summarizing what was just said, hedging every sentence.
- Same structure and tone across several pieces (templated variety).

**Design and UI**
- Default look: purple/blue gradient hero, centered everything, three identical cards, emoji or generic icon sets as illustrations, glassmorphism/blur on everything, stock gradient blobs.
- Default fonts and spacing with no hierarchy; no real brand decisions; lorem-ipsum-grade copy.
- Layouts that could be any company's: swap the logo and nobody would notice.
- Fake social proof (logos, avatars, "10,000+ users") that doesn't exist.

**Code**
- Abstractions nobody asked for, comments that restate the code, boilerplate "for later", unused dependencies, over-defensive error handling around impossible cases, placeholder TODOs left in.
- Invented APIs/flags/options. Verify against docs (context7) instead of trusting memory.
- Claiming it works without running it.

**Media, video, audio**
- Generic stock-voice narration, filler b-roll, scripts that open with "Hey guys, today we're going to talk about".

**Data and claims**
- Any number, quote, source or result you didn't get from a real source or the user. If unverifiable: remove it, or flag it.

## When asked to review someone's content

List each suspected slop item with the exact quote/location, why it reads as slop, and a concrete rewrite. Be direct, not polite-vague.

## Related skills
`humanizer` (rewrite AI-sounding prose), `design-taste-frontend` (anti-generic UI), `verification-before-completion` (don't claim unverified results).
