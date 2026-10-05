---
name: gamestack-upgrade
description: Check whether the installed gamestack plugin is behind the marketplace's latest version and update it in place. Use when asked to "upgrade gamestack", "update gamestack", "check for gamestack updates", "is gamestack up to date", "auto update the plugin", "gamestack upgrade", or "what's new in gamestack". Pure plugin-maintenance utility — no design bible, no engine detection, nothing game-specific.
---

# Gamestack Upgrade

Claude Code's plugin auto-update is a **client-side opt-in**: each user (or org admin) toggles it per marketplace via `/plugin` → Marketplaces → Enable auto-update, and third-party marketplaces like `gamestack` default to **off**. This repo can't flip that switch for anyone. What it *can* ship is a skill that does the check on demand, using the same `claude plugin` CLI surface auto-update uses internally — invoking this skill is the manual equivalent of a successful auto-update pass.

## When to use this

- The user asks if gamestack is current, or asks to update it
- Before relying on a skill that might have changed recently (e.g. before a long headless run)
- Anytime — it's a read-then-maybe-write check, safe to run speculatively

## What it produces

A version report (current → latest, or "already current") plus, if it updated, the relevant `CHANGELOG.md` entries and a reminder to run `/reload-plugins`.

## The procedure

Read **`UPDATE.md`** for the full step-by-step: locate the install, refresh the marketplace, run the update, and report what changed.

## The one rule

> **Never hand-roll the version diff.** `claude plugin update` already computes "is there a newer version" using the same cache-key logic as auto-update — don't parse JSON or compare version strings yourself to decide whether to update; just run it and report what it says.

Start at `UPDATE.md`.
