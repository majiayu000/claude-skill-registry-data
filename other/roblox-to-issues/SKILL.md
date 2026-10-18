---
name: roblox-to-issues
description: Break a Roblox game PRD, roadmap, or plan into small independently-playtestable vertical slices instead of building the whole game at once. Use when the user wants to turn a concept or PRD into buildable tickets, split work into slices, plan what to build next, or stop Claude from trying to build an entire game in one pass. Each slice cuts through client, server, remotes, data, and UI for one small player-facing capability, verified with a Studio playtest.
---

# Roblox → Issues (Vertical Slices)

Break a plan into small issues that are each **buildable and playtestable on their own**. This is the antidote to "build the whole game in one go, everything half-broken."

The tracker location and label vocabulary should have been provided to you in `CLAUDE.md` / `docs/agents/`. If not, run `setup-roblox-skills`. Slices publish either as GitHub issues (`gh`) or as markdown files under `roadmap/<feature-slug>/slices/` — whichever the setup configured. In all cases, keep `ROADMAP.md` as the human-readable index.

## What a Roblox vertical slice is

A **tracer bullet**: the thinnest end-to-end path that a player can actually feel, cutting through **every layer it touches** — client input, server authority, remotes, DataStore, and UI — not one horizontal layer.

- **Right (vertical):** "Player taps the ore, server grants 1 coin, HUD shows the new balance, balance survives rejoin." Touches input + remote + server + data + UI. Playable.
- **Wrong (horizontal):** "Build the entire economy module." / "Build all the UI." Nothing is playable until everything is done — exactly the failure we are avoiding.

### Slice rules

- Each slice delivers one narrow but **complete** player-facing capability.
- Each slice is **verifiable in a Studio playtest** on its own (this is the acceptance signal).
- Prefer many thin slices over a few thick ones. If a slice can't be playtested in isolation, split it.
- Valuable state (currency, inventory, purchases, rewards, progression) is **server-authoritative from the first slice** — never a client-trust shortcut you plan to fix later.
- The **first slice is the tracer bullet**: the smallest thing that proves the core loop end-to-end (one action → one reward → one visible next goal). Build it before anything else.

### Slice types

- **AFK** — can be built and verified without a human decision. Prefer these.
- **HITL** — needs a human: a design approval, a balance judgment call, a Studio action only the user can take. UI slices are **HITL until an approved UI design artifact exists** (see `roblox-game-ux`); if UI design is missing, create a design-approval slice first and block the UI slice on it.

## Process

### 1. Gather context

Work from the PRD / conversation. If the user passes a reference (issue number, `ROADMAP.md` line, or file path), read it fully. Connect via `roblox-studio-workflow` if you need to see current place state. Use the game's own vocabulary.

### 2. Draft the slices

Order them so the **core loop tracer bullet is slice 1**, then layer capability outward (persistence → progression → social → monetization → polish). Each later slice should build on a slice that is already playable.

### 3. Quiz the user

Present the breakdown as a numbered list. For each slice show:

- **Title** — short, player-facing.
- **Type** — AFK / HITL.
- **Blocked by** — which slices must ship first.
- **Playtest check** — the exact in-Studio action that proves it works.
- **Server-authoritative?** — yes/no and which state it protects.

Ask: is the granularity right (too coarse / too fine)? Are dependencies correct? Should any slice split further? Are HITL/AFK correct? Iterate until approved.

### 4. Publish

Publish each approved slice to the configured tracker with the `needs-triage` label/status, blockers first so you can reference real IDs. Mirror each slice as a checkbox in `ROADMAP.md` using the pack's convention: `[ ]` not started, `[~]` built and tested but awaiting approval, `[x]` only after build + playtest + explicit human approval.

<slice-template>
## What to build

The end-to-end player-facing behavior for this slice. Describe what the player does and what the server does — not a layer-by-layer implementation.

## Layers touched

- Client: ...
- Server (authoritative): ...
- Remotes: ...
- Data / persistence: ...
- UI: ...

## Playtest check (acceptance)

- [ ] In a Studio playtest, <exact action> produces <exact result>.
- [ ] Valuable state is server-validated and survives rejoin (if applicable).
- [ ] No new console errors.
- [ ] Mobile: readable and tappable on a phone-sized viewport (if UI).

## UI design artifact

For UI slices: link the approved artifact (see `roblox-game-ux`) or "blocked on UI design approval".

## Blocked by

Reference the blocking slice, or "None — can start immediately".
</slice-template>

Do NOT close or modify a parent PRD/issue.

## Next

Run **`roblox-triage`** to sort the slices and mark which are ready to build, then build each slice with its phase specialist (e.g. `roblox-luau-architecture`, `roblox-combat-systems`, `roblox-ui-implementation`, `roblox-datastore-persistence`) and verify with `roblox-playtest-qa`. Keep `roblox-game-development-lifecycle` as the umbrella that decides slice order.
