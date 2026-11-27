---
name: roblox
description: "Build, test, publish and earn with a Roblox game: Rojo and Lune setup, Robux receipts, Open Cloud publish, Creator Hub hands steps. Use for any Roblox or Luau work."
---

# Roblox

The one home for how a Roblox game is built here. Proven on Kleingarten
(`yverse-studio/kleingarten`, three slices merged at 5/5, 2026-10-07). How Claude runs and sees
the game (Lune, Open Cloud Luau Execution, Studio MCP screenshots): `toolbox/catalog/roblox.md`.
Studio work on the PC: the `studio` skill.

## Split

- Cloud thread: Luau in git, Lune tests, CI publish. No Roblox client runs in the cloud.
- PC (Remote Control, Studio open): play, walk, `screen_capture`, feel and design checks.
- yskills' hands: anything in Creator Hub that needs the account owner (below).

## Project setup

- **Rojo** keeps every script in the repo; `rokit` pins the tools (`rojo`, `lune`, `selene`).
- **Lune** tests first: `lune run tests/run.luau`. Selene can't fetch its API dump in cloud
  threads, so it runs in CI only.
- **Bake the world** into the built place: after `rojo build`, a Lune script runs the real map
  builder into Workspace (the server replaces that copy at start). A world built only by a server
  script leaves the place empty, so Studio and thumbnails show sky. Set `Lighting.Technology` in
  the project file, or Studio asks to migrate lighting on every open. Check what a built `.rbxl`
  holds with Lune before calling a slice done.
- **Strings**: all player text in one tested `Strings` module (en, de).
- **HUD twin**: an HTML copy of the HUD with the same offsets, so the cloud can screenshot it
  and `design-critic` can review it.

## Money (Robux)

- Earn with game passes (one-time perks), developer products (repeatable buys) and Premium
  payouts; cash out through DevEx (yskills' account).
- Find products by their Creator Hub name, never hard-coded ids.
- `ProcessReceipt`: store the purchase id together with the grant, return `PurchaseGranted`
  only after that save went through, re-save on a known id (never grant twice, never lose a buy).

## Publish

- A game is an "experience" holding places. A new place is made in Studio (File, Publish to
  Roblox As, hover the experience, "Add as a new place"); Creator Hub "Add a Place" only
  attaches a place that belongs to no experience.
- Place ids are public: `develop.roblox.com/v1/universes/<id>/places`.
- CI publishes with Open Cloud: PR to the test place, `main` to the live place
  (`/universes/v1/<u>/places/<p>/versions`). `serverSize`:
  `PATCH apis.roblox.com/cloud/v2/universes/<u>/places/<p>?updateMask=serverSize`.
- Only the account owner can create the API key (Universe Places write, Luau Execution); it goes
  in the game repo's Actions secret, never in chat.

## Only yskills (one numbered list, exact names)

API key, icon, thumbnails, maturity questions, public listing and DevEx. Ship the files and the
texts in `docs/LISTING.md` first, so yskills only uploads and clicks.
