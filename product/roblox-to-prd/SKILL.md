---
name: roblox-to-prd
description: Turn a Roblox game concept or the current conversation into a short, buildable PRD (game design brief) and publish it to the project tracker. Use when the user wants to lock a chosen concept into a spec before building, write a design brief, or create a PRD for a Roblox game or feature. Pairs with roblox-to-issues, which slices the PRD into vertical slices so the game is built one playable piece at a time instead of all at once.
---

# Roblox → PRD

Turn what is already decided into a concise, buildable **game design brief (PRD)**. Do NOT interview the user from scratch — synthesize the concept, conversation, and place state you already have. If the concept has not been pressure-tested yet, run `roblox-game-ideas` (grilling mode) first.

The tracker location and label vocabulary should have been provided to you in `CLAUDE.md` / `docs/agents/`. If not, run `setup-roblox-skills`.

## Why this exists

The single biggest failure mode in AI-built Roblox games is trying to build the whole game in one pass, which leaves everything half-working. A PRD is the contract that a later step (`roblox-to-issues`) slices into small, independently playtestable pieces. Keep it tight: enough to slice, not a novel.

## Process

1. **Read the current state.** Connect through `roblox-studio-workflow` if a place exists. Read `ROADMAP.md` if present. Use the game's own vocabulary consistently (currency names, entity names, zone names).

2. **Sketch the systems, not the whole game.** List the major server-authoritative systems and client controllers this concept needs (core loop, economy, save/load, progression, social, UI surfaces). Flag which hold **valuable state** (currency, inventory, purchases, rewards, progression) — those must be server-authoritative. Confirm the system list matches the user's expectation before writing.

3. **Handle UI up front.** If the concept has meaningful UI, note whether a Roblox UI design artifact exists yet (see `roblox-game-ux`). If not, record an explicit **design step** rather than treating UI as ready to build.

4. **Write the PRD** using the template, then publish it to the tracker with the `needs-triage` label/status so it enters the normal flow.

<prd-template>

## Player Promise

What the player gets, in their words. One or two sentences.

## Core Loop

The single repeating loop, start to reward to next goal. Name the first fun action and how fast it happens (target: 10–30 seconds).

## First Session

What the first 30–60 seconds look like: spawn, first action, first reward, first visible goal.

## Systems To Build

A list of the server-authoritative systems and client controllers. For each: one line on what it does and whether it holds valuable state (server-authoritative) or is client-side presentation.

## Player Stories

A numbered list, format: "As a player, I want <capability>, so that <benefit>." Cover the core loop, progression, social, monetization, and mobile paths. Extensive but plain.

## Economy & Monetization

Currency sources and sinks, what is sold (passes, developer products, cosmetics), and the anti-pay-to-win rule for this game. Write "None yet" if pre-monetization.

## Persistence

What must survive rejoin/shutdown (currency, inventory, progression, settings) and what is session-only.

## UI & Design

Which surfaces need a UI design artifact (HUD, shop, reward, menus) and whether that artifact exists and is approved. For non-UI PRDs, write "No UI design step required."

## Mobile & Performance Targets

Mobile-first expectations (touch targets, readability, safe areas) and any frame-rate/instance budgets.

## Out Of Scope

What this PRD deliberately does not cover, so slicing stays focused.

## Risks

The top 1–3 risks and how each is checked (usually a Studio playtest).

</prd-template>

## Next

Hand the published PRD to **`roblox-to-issues`** to break it into small, playtestable vertical slices. If the PRD flagged UI work, run **`roblox-game-ux`** to produce and approve the UI design artifact before UI slices become buildable.
