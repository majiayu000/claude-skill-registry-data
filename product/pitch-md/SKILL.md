---
name: pitch-md
description: Create or update a PITCH.md — a plain-text pitch for your project that tells the story, communicates the vision, and makes the case. Not a README (that's for users). Not a pitch deck (that's theater). This is the argument for why this thing should exist, written clearly enough that it speaks for itself.
license: Complete terms in LICENSE.txt
---

You help write PITCH.md files. A PITCH.md lives in the repo root alongside the README and the code. It's the human-readable case for why this project exists, who it's for, and where it's going.

The user provides context about their project — maybe rough notes, maybe a conversation dump, maybe just "write me a PITCH.md for this repo." You read the codebase, understand what's being built, and write a PITCH.md that tells the story clearly.

## What a PITCH.md Is

A PITCH.md is not a README. A README says "here's what this does and how to use it." A PITCH.md says "here's why this exists, who needs it, and why we're the ones building it."

It's not a pitch deck either. Pitch decks let weak ideas hide behind design. Markdown has nowhere to hide. Every sentence has to earn its place. That's the point.

A good PITCH.md can be forwarded to a collaborator, a funder, a journalist, or a friend — and they'll understand the project without a meeting.

## Structure

Use these sections. Adapt the headers to fit the project — these are the *ideas* that need to be present, not a rigid template.

### 1. The Opening (no header — just start)

Two to three sentences that say what this is and why it matters. No preamble. No "In today's rapidly evolving..." throat-clearing. Start with the thing.

### 2. The Problem

What's broken, missing, or wrong in the world right now? Be specific. Name the tools that exist and say plainly why they're not enough. Don't be mean about competitors — just be honest about the gap.

### 3. What We're Building

Describe the project in concrete terms. What does it actually do? What does it feel like to use? Paint the picture of the experience, not just the feature list. This is where a README would show code examples — a PITCH.md shows the *feeling* of the workflow.

### 4. How It Works

The key insight, the architectural bet, the technical approach — explained simply. Not a deep dive, but enough that a technical reader thinks "oh, that's clever" and a non-technical reader thinks "I follow." One or two paragraphs.

### 5. Who It's For

Be specific. "Musicians" is too broad. "Producers who work alone and want to release without a label or a distributor" — that's a person you can picture. Name the person. Describe their day.

### 6. Why Us

What do we know, have, or believe that makes us the right people to build this? For Manzanita, this is usually about living in the problem — being musicians ourselves, caring about the things we're building because we need them.

### 7. Where This Is Going

The honest roadmap. What works now, what's next, what's still a question mark. It's fine to say "we don't know yet" about some parts. Honesty about uncertainty is more compelling than a confident five-year plan.

### 8. The Ask (optional)

If there's a specific thing you want from the reader — try it, fund it, contribute, spread the word — say so directly. If there's no ask, skip this section entirely. Don't manufacture one.

## Voice

Write in a warm, grounded, direct voice. Short sentences. No corporate language. No hype. For Manzanita Research projects, follow the `brand-voice` skill. For other projects, match the project's existing tone — but the principles below are universal.

Specifically for PITCH.md:

- **Tell a story, don't make a sales pitch.** The reader should feel like they're hearing from someone who cares deeply about a real problem, not someone performing enthusiasm for investors.
- **Be specific over impressive.** "We tested this with 12 producers over three months" beats "our extensive beta program validated product-market fit."
- **Admit what you don't know.** Uncertainty handled honestly is more trustworthy than false confidence. "We think this approach works. Here's why, and here's what could go wrong."
- **No vanity metrics.** Don't lead with numbers unless they tell a real story. "4,000 people downloaded it" is less interesting than "a producer in São Paulo used it to finish an album she'd been stuck on for two years."
- **Write it to be forwarded.** The test: if someone sends this to a friend with "read this, tell me what you think" — does it stand on its own?

## Banned Patterns

These patterns weaken pitches regardless of brand:

- TAM/SAM/SOM calculations — this isn't a pitch deck
- "X for Y" comparisons ("it's like Spotify for producers") — reductive and usually wrong
- Bullet-point feature dumps — that's README territory
- Hockey-stick growth projections — we don't do hype
- "Disrupting the X industry" — we're building tools, not waging war
- Competitive matrices — if you have to put yourself in a grid to look good, the writing isn't doing its job

## Process

1. **Read the project.** Look at the README, the code, any existing docs. Understand what's actually built, not just what's planned.
2. **Ask if needed.** If the user's input is thin — no clear audience, no problem statement, no technical approach — ask before writing. A PITCH.md with gaps is worse than no PITCH.md.
3. **Write a draft** following the structure above. Adapt section headers to feel natural for this specific project.
4. **Review against the voice.** Read it back. Does every sentence earn its place? Does it sound like a person talking, or a document performing? Cut anything that performs.
5. **Present the draft.** Note any sections where you had to guess or infer — the user should validate those.

## Updating an Existing PITCH.md

When the user says "update" rather than "create":

1. Read the existing PITCH.md first.
2. Read recent commits, changelogs, or new code to understand what's changed.
3. Update the relevant sections. Don't rewrite sections that are still accurate — just evolve what's changed.
4. Call out what you updated and why, so the user can review the diff.
