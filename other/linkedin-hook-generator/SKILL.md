---
name: linkedin-hook-generator
description: Use when the user wants hooks, opening lines, or a stronger first line for a LinkedIn or X post — generates 8 pattern-labeled hooks (contrarian, number+outcome, confession, story) sized to survive the "see more" fold.
---

# LinkedIn Hook Generator

Generate scroll-stopping opening lines for LinkedIn (or X) posts. The hook is
the only part of a post most people ever see: LinkedIn shows roughly the first
210 characters before the "…see more" fold on desktop, and around 140 on
mobile. If the hook doesn't earn a pause, the post doesn't exist.

## Read the voice file first

Look for `.liftli/voice.md` in the project, then `~/.liftli/voice.md`. If one
exists, read it and follow it: the audience, the positions, the proof the user
is allowed to use, what is off limits, and how they sound. Use only stories and
numbers from the voice file, the chat, or material this skill gathers. If
there is no voice file, write anyway, and at the end suggest building one once
with the `linkedin-voice` skill (install:
`npx skills add liftli-ai/linkedin-agent-skills --skill linkedin-voice`).

## When to use

- The user asks for hooks, opening lines, or "a better first line"
- The user has a draft whose opening is weak (offer this before rewriting the whole post)
- The user has a topic but no post yet (hooks are the fastest way to find the angle)

## Process

1. Get the raw material: a topic, a draft, or a story. If the user gave a
   draft, mine it for its most specific details (numbers, moments, quotes) —
   hooks are built from specifics.
2. Generate **8 hooks, each using a different pattern** from the list below.
   Max ~200 characters each; the strongest versions fit under 140 (safe on
   mobile). Label each with its pattern.
3. Ask which direction resonates, then offer to tighten the winner.

## The patterns

| Pattern | Shape | Example skeleton |
|---|---|---|
| Number + unexpected outcome | specific figure, then the twist | "We spent $30k on ads. The best channel turned out to be free." |
| Confession / mistake | own the error, imply the lesson | "I ignored my biggest customer for three weeks. On purpose." |
| Contrarian claim | cut against advice the reader already heard | "Posting every day is bad advice for most people." |
| Tension between two facts | two true things that shouldn't coexist | "Our churn doubled. Revenue went up." |
| Mid-story drop | start inside the moment | "The client went quiet for nine days. Then the email arrived." |
| Question they'd Google at 1am | a question with real pull, not rhetorical | "Why do great products lose to average ones with better feeds?" |
| Before/after gap | the transformation, compressed | "18 months ago nobody replied to my posts. Last week a post hired me." |
| Receipts | a claim + immediate proof fragment | "Comments beat posts for reach. I have 90 days of data." |

## Quality bar (reject your own weak output)

- No throat-clearing ("I've been thinking a lot lately…"), no "I'm excited to
  share", no vague inspiration ("Success is a journey").
- Concrete beats abstract: a real-sounding number or named moment in most hooks.
- No AI tells: no "Not only… but also", no enumerator adverbs, 0–1 emoji.
- Read each hook amputated — alone, out of context. If it doesn't create an
  information gap the reader wants closed, cut it and generate a replacement.

## The step the user must do

Tell the user to swap approximate specifics for their real ones (the actual
dollar figure, the actual number of days, the sentence actually said). A hook
with a true detail in it can't sound like AI, because AI didn't know that detail.

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

Web version of this tool: https://liftli.ai/tools/hook-generator.html
