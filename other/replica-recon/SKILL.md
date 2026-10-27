---
name: replica-recon
description: >-
  Reverse-engineers any app into a recon map: screen inventory, user flows,
  component list, inferred data model and a feature matrix, from public pages,
  screenshots, app store listings, help docs and the user's own account. The
  first step of the Replica pack. Use when the user says "clone this app",
  "reverse engineer X", "how does X work", "map out X", "what screens does X
  have", "I want to build my own version of X", "copy this app", or pastes an
  app's URL or App Store link and wants to rebuild it.
---

# replica-recon

Everything else in the pack builds from what this skill writes. A bad recon
map means a bad clone, so take the time here.

Output goes in the user's project:

```
replica/recon.md        the recon map (template: recon-map.md in this folder)
replica/features.csv    the feature matrix (template: features.csv in this folder)
replica/screens/        reference screenshots of the original. Never shipped.
```

## Authorized binary analysis (Claude Code and Codex)

For an APK, DEX, JAR, .NET assembly, IPA/Mach-O, Flutter AOT, Unity IL2CPP,
Electron ASAR, Go or native executable/library, read
[binary-analysis.md](binary-analysis.md) first and run
[bin_analyze.py](bin_analyze.py) to inventory hashes, detect the format and
pick the tool. When `replica/scope.md` records ownership or written
authorization and the requested analysis, that workflow permits static
decompilation and supersedes the clean-room source restriction below only for
the authorized target. Without that scope, continue public recon. Recovered
code never enters a product-mode clone.

## Working rules

This skill rebuilds functionality and UX patterns. It studies what the app
does and how a user moves through it, and it does not take what the app owns.

- Work from public sources and the user's own account or owned copy.
- Read pages at human speed; no bulk scraping or crawling.
- Do not copy the app's source, bundles or private APIs; public API docs are
  fine to read.
- Screenshots are reference only and stay in `replica/screens/`.
- For a binary the user owns, follow `binary-analysis.md` instead of the
  no-decompile line above; it applies to that target only.

## Step 1: scope

Ask three things, or propose answers and get a yes:

1. **Which app, which platform.** Web, iOS, Android, desktop.
2. **Which slice.** "All of Notion" is not a project. "Notion's pages, blocks
   and sharing" is. Default to the core loop: the one flow users pay for.
3. **Who it is for.** The user's own business, a niche, a product to sell.

## Step 2: list the sources

Build a sources table first, with a URL on every row. In order of value:

| source | what it gives you |
| --- | --- |
| help center / docs | the most complete feature list there is, and the settings |
| pricing page | which features matter (they gate them) |
| changelog | what was added recently, what the team thinks is important |
| app store listing | screenshots of every key screen, the pitch, ratings |
| public walkthrough videos | real flows, click by click |
| marketing site | positioning, the core loop in their words |
| the user's own account | the real thing, every state, driven by the user |
| public API docs | the data model, almost for free |

## Step 3: screen inventory

One row per screen. IDs are stable: S01, S02... Every other file refers to them.

`ID | screen | route or how you get there | purpose | key components | states seen`

States matter: empty, loading, filled, error, permission denied, mobile. An
empty state you did not record is an empty state you will not build.

## Step 4: user flows

F01, F02... Each one is a goal and the screens it passes through:

```
F01 Guest books a meeting
    S07 booking page -> S08 pick a time -> S09 details form -> S10 confirmed
    edge: no slots this week, time zone differs, slot taken while filling the form
```

Count the clicks on the happy path. It becomes the number to beat.

## Step 5: components

Every repeated UI part: buttons, inputs, date pickers, modals, tables, toasts,
nav. Name, variants, states, which screens use it. This becomes
replica-design's component list.

## Step 6: inferred data model

Entities, fields and relationships, each with its evidence and a confidence:

```
Booking  id, event_type_id, start_at, end_at, guest_name, guest_email,
         status (confirmed | cancelled | rescheduled), answers (json)
         evidence: S09 form fields, S10 confirmation, help article "Cancel a booking"
         confidence: high
```

Mark guesses as guesses. replica-architect turns this into a real schema.

## Step 7: feature matrix

Write `replica/features.csv` (columns: feature, area, priority, original,
clone, notes). Priority is must / should / could. `clone` starts at `no` for
every row and gets filled in during the build. replica-diff scores it.

## Step 8: what cannot be cloned

List it honestly, as `skip` rows with a reason: licensed content (a music
catalogue, a stock library), the network and its users, data the app owns,
partner deals, hardware, regulated licences (banking, health). "Clone any
app" means the features and the flow, not what the app owns.

## Step 9: size it

Screens, flows, entities, and the hard parts (realtime, sync, payments,
calendar or email integrations, offline). Give a size: S (a weekend), M (a
few weeks), L (a quarter), XL (rescope it). No promises of a perfect clone.

## Output

`replica/recon.md` and `replica/features.csv`, then a five-line summary: the
core loop, screen and flow counts, the three hardest parts, what is out of
scope, and the next step: `/replica-architect`.
