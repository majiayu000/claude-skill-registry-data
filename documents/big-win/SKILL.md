---
name: big-win
description: Document a new Big Win for The ZAO — asks context questions, saves to quarterly docs, updates the master index. Use when something notable happens worth celebrating.
---

# Big Win — Document a ZAO Win

Record a notable achievement, milestone, or moment for The ZAO community. This skill collects context through questions, then saves the win to the appropriate quarterly doc.

## Step 1: Identify the Quarter

Determine which quarter the win belongs to based on when it happened:
- Q1: January - March
- Q2: April - June
- Q3: July - September
- Q4: October - December

Check if the quarterly doc exists:
```
Glob for research/*-q{quarter}-{year}-big-wins/README.md
```

If it doesn't exist, create it using the template from `research/241-q1-2026-big-wins/README.md` as reference.

## Step 2: Ask Context Questions

For EVERY win, ask these questions before documenting:

**Core (required):**
1. What happened? (one sentence)
2. When exactly? (date or date range)
3. Who was involved? (names, handles, partners)
4. What's the measurable result? (numbers: dollars, participants, items, views)

**Depth (ask at least 2):**
5. Why does this matter for The ZAO?
6. What led up to this? (backstory)
7. Any links? (articles, tweets, casts, videos, contracts, PRs)
8. Is this continuing into next quarter or was it a one-time thing?
9. What's the story you'd tell on stage about this win?
10. Any shout-outs to specific people?

**Content angle:**
11. Could this be a standalone post/thread? (for the daily deep-dive series)
12. What category does this fall into? (Token/DeFi, Events/IRL, Products, Community, WaveWarZ, Content, Partnerships)

Do NOT proceed to Step 3 until you have answers to at least questions 1-4.

## Step 3: Document the Win

Add the win to the quarterly README.md using this format:

```markdown
### {Number}. {Win Title}
- **Status:** DOCUMENTED | NEEDS MORE CONTEXT
- **What:** {one sentence}
- **When:** {date or range}
- **Details:** {2-5 sentences with full context}
- **Key people:** {names}
- **Numbers:** {measurable results}
- **Category:** {Token/DeFi | Events/IRL | Products | Community | WaveWarZ | Content | Partnerships}
- **Links:** {any URLs}
- **Q2+ continuation:** {yes/no + what's next}
- **NEEDS:** {any gaps still to fill}
```

## Step 4: Update the Comparison Table

Update the category comparison table in the quarterly doc to reflect the new win count and highlights.

## Step 5: Suggest Content

After documenting, suggest:
- A one-line teaser for the overarching quarterly recap post
- Whether this win deserves its own daily deep-dive post
- A potential hook/angle for the deep-dive

## Rules

- NEVER document a win without asking questions first — context is content
- ALWAYS include at least one number per win
- ALWAYS ask about links — they make the content real
- Keep Zaal's voice — this is build-in-public, not corporate PR
- Say "Farcaster" not "Warpcast"
- Empire Builder, WaveWarZ, Incented, Artizen — always capitalize properly
