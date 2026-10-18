---
name: roblox-game-ideas
description: Generate or evaluate Roblox game ideas using retention, social, monetization, mobile-first, and first-session best practices. Use when pitching concepts, choosing a game direction, or improving a core loop.
---

# Roblox Game Ideas

## Goal

Create Roblox concepts that can win attention and keep players. Ideas must be playable quickly, social early, mobile-first, monetizable without breaking fairness, and suitable for frequent updates.

## Winner Checklist

Every strong concept should include:

- First fun action within 10-30 seconds.
- One clear core loop that repeats cleanly and rewards every cycle.
- Short-term goals for instant gratification.
- Long-term goals that can last for weeks.
- A Day-1 return hook and a visible Day-7 aspiration reward.
- Social mechanics in the first session, such as co-op objectives, friends, groups, gifting, trading, leaderboards, or shared progress.
- Mobile-first controls with large targets, forgiving input, and no keyboard dependency.
- Progression signals: XP, currency, collections, zones, meters, rank, or visible unlocks.
- Fair monetization woven into the loop through optional passes, boosts, cosmetics, VIP, private servers, or event items.
- Server-authoritative handling for valuable state such as currency, inventory, purchases, rewards, and progression.
- A click-worthy icon, thumbnail, and searchable name direction.

## Idea Format

For each idea, provide:

- Title and one-line promise.
- Player fantasy and target audience.
- First 30 seconds.
- Core loop.
- Social hook.
- Progression ladder.
- Retention hooks for Day 1, Day 3, and Day 7.
- Monetization that avoids pay-to-win.
- Mobile UX considerations.
- Update/event pipeline.
- Main risk and mitigation.

## Scoring

Score concepts from 1-5 on:

- First-session clarity.
- Core-loop repeatability.
- Social retention.
- Progression depth.
- Mobile fit.
- Fair monetization.
- Live-ops potential.
- Build feasibility.

Prefer fewer, sharper concepts over many vague ones. If a concept scores poorly on first-session clarity or mobile fit, revise it before recommending it.

## Grilling Mode (stress-test a chosen concept)

Once the user has picked a direction, switch from generating to **grilling** — interview them one question at a time to find the holes before any code is written. This is where a fuzzy concept becomes a buildable one.

- Ask **one question at a time** and wait for the answer before the next. For each, offer your recommended answer.
- Walk the design tree in dependency order: core loop → first 30 seconds → progression → economy → social → monetization → mobile controls → live-ops cadence. Resolve each before moving on.
- **Probe with concrete scenarios**, not abstractions: "A new mobile player spawns with 0 coins — what is the very first tap, and what does it give them?"
- **Sharpen fuzzy terms** into one canonical word the whole project will use ("is it a *coin*, a *gem*, or a *token*? pick one"). Consistent vocabulary now saves confusion in every later skill.
- **Pressure-test against the Winner Checklist and Anti-Patterns** above — if an answer implies a long tutorial, desktop-only control, or pay-to-win shortcut, call it out immediately.
- Capture resolved decisions as you go (in the concept notes or, if the project uses one, `CONTEXT.md`) so they aren't re-litigated later.

Stop when the core loop, first session, and monetization are concrete enough to write down without hand-waving.

## Anti-Patterns

Avoid concepts that depend on forced cutscenes, long tutorials, desktop-only controls, hidden progression, harsh early penalties, pay-to-win shortcuts, or content that exhausts before the 2-3 hour mark.

## Next

When the concept survives grilling, lock it into a spec with `roblox-to-prd`, then break it into playtestable slices with `roblox-to-issues`. To apply proven mechanics for the chosen genre, use `roblox-genre-patterns`; to shape the first-session flow, use `roblox-game-ux`.

