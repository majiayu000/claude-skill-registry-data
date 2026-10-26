---
name: add-feature
description: Install a ready-made feature pack from packs/ into the app (chat, scan-barcode, payments, feed-reels, nav, profile-settings, auth-screens, tabbars). Use when the user says "add <feature>", "install the <x> pack", "drop in chat/payments/scanner", or wants a prebuilt feature wired up.
argument-hint: [pack-name]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(cp *), Bash(mkdir *), AskUserQuestion
---

## Context

- Available packs: !`ls -1 packs 2>/dev/null | grep -v '^_' | grep -v README`

## Task

Install the feature pack **`$ARGUMENTS`** from `packs/<name>/` into the app. Packs are logic-first:
they ship working background (data + state + services + migrations + hooks) and a **minimal,
swappable UI** that the Claude Design pass replaces later. Catalog + philosophy: `packs/README.md`.

1. **Pick the pack.** If `$ARGUMENTS` is empty or ambiguous, list `packs/` and ask which one
   (AskUserQuestion). Read its `packs/<name>/pack.json` and `README.md`.
2. **Copy the code** from `packs/<name>/src/` into the `installTo` path (default
   `src/features/<name>/`). Preserve structure (`model/`, `data/`, `ui/`, services, `index.ts`).
3. **Migrations.** If `pack.json.migrations` exist, copy them into `supabase/migrations/` with the
   next free number, then tell the user to run `supabase db reset && supabase test db`.
4. **Routes/tabs.** If `pack.json.routes` exist, create the thin route file(s) under `src/app/` and
   (if relevant) add a tab entry. Keep routes THIN (wire to the feature's screen).
5. **Dependencies.** Print the exact install command from `pack.json.deps` / `expoInstall`
   (e.g. `npx expo install expo-camera`). Do NOT assume they're installed.
6. **Config / env.** Print every `pack.json.env` entry and whether it's needed for dev vs ship.
   Reassure: dev works key-free unless `devKeysNeeded` is true.
7. **Verify boundaries.** The copied feature must only import `@/shared/*` and its own folder. Fix
   any stray imports. Run nothing heavy — just confirm it slots into the `app → features → shared` rule.
8. **Report**: what was copied, the deps to install, the migration to run, and a one-line
   reminder that the UI is a placeholder to replace after the design pass.

Never wire a pack the user didn't ask for, and never paste real API keys.
