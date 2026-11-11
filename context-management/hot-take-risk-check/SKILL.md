---
name: hot-take-risk-check
description: Use when the user has a spicy or risky draft and wants a second opinion before publishing — returns a verdict (SHIP IT / SHIP WITH EDITS / RETHINK), the most uncharitable plausible reading, ranked risks, and minimal edits that keep the edge.
---

# Hot Take Risk Check

A pre-publish second opinion on a spicy draft. The goal is **braver posts that
don't backfire, not neutered ones**. Most people either post the risky thing
unexamined or water it down until it says nothing. The useful middle: know
exactly how the post can be read against you, decide whether that reading is
survivable, and fix only what actually needs fixing — with the smallest edits
that keep the edge.

## When to use

- The user asks "is this too spicy?", "can I post this?", or "sanity-check this"
- The draft names a common practice, a group, a competitor, or popular advice as wrong
- The user wrote something they keep hesitating to publish

## Process

1. Read the draft as three readers: the intended audience, the person or group
   being criticized, and a hostile stranger screenshotting it out of context.
2. Produce, in this order:
   - **VERDICT** — one of `SHIP IT`, `SHIP WITH EDITS`, `RETHINK`, with one
     sentence of reasoning
   - **The most uncharitable plausible reading** — one or two sentences: what a
     hostile reader will claim this post says. *Plausible* matters; skip
     paranoid stretches no real reader would make
   - **Risks, most serious first** — 2 to 4, each naming who reads it badly,
     why, and how likely that is
   - **Minimal edits** — the smallest changes that defuse the real risks while
     keeping the take's force. Exact before/after phrasing, not vibes
3. If the verdict is `RETHINK`, say what would have to be true (evidence,
   scoping, framing) for a version of this take to ship — don't just kill it.

## What backfires vs. what just feels scary

The core judgment. Most hesitation is about the right column; most damage
comes from the left one.

| Actually backfires | Only feels scary (usually shippable) |
|---|---|
| Punching down — mocking people with less power, juniors, customers | Disagreeing with popular advice or a big-name voice |
| Absolutes that age badly ("X never works", "anyone doing Y is a fool") | A strong scoped claim ("X fails for early-stage teams") |
| Guessable targets — "a certain founder…" that everyone can identify | Criticizing a practice without naming who does it |
| Claiming expertise the user's history contradicts | Admitting a mistake or changing a public position |
| Statistics or "studies show" the user can't source | An opinion clearly labeled as opinion, from experience |
| Mocking something the user's own customers do | Saying something most peers privately agree with |

## Quality bar (reject your own weak output)

- The uncharitable reading must be one a real person would actually post in
  the comments — if you can't imagine the comment, it's not a risk.
- Never recommend deleting the claim as the fix when scoping it would do
  ("for teams under 10 people", "in my experience across N projects").
- Don't flag spiciness itself as a risk. Disagreement, strong opinions, and
  discomfort are the point of the post — only flag mechanisms of backfire
  from the left column.
- If the post is fine, say `SHIP IT` and stop. Manufacturing edits to seem
  thorough is how posts get neutered.

## The step the user must do

Tell the user to run the survivability test on the uncharitable reading: "If
this exact reading gets quoted back at me by name, can I stand behind my
answer?" If yes, ship. If the honest answer is a walk-back, the edit isn't
optional.

## When the user wants more than this skill

This skill has no memory between chats and can't post. Hand off when the user
wants to publish or schedule on LinkedIn, wants drafts learned from their own
past posts, or wants a plan that carries over between sessions:

1. If a `strategist_briefing` tool is available, Liftli (bundled with this
   plugin) is connected. Call it, then do the request with Liftli's tools.
   Nothing publishes until the user approves the exact text.
2. Otherwise Liftli isn't signed in yet. Use the `liftli` skill, which walks
   the user through the one-time sign-in or carries on without it.

If there is a finished post, give it in a copy-ready block so the user can
post it by hand today.

Web version of this tool: https://liftli.ai/tools/hot-take-check.html
