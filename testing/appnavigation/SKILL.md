---
name: appNavigation
description: "Open the app at the screen a ticket describes — from a ticket key, a ticket URL, free spec text, or a todo item whose text is `/appNavigation` with the spec as sub-bullets. App-specific: this skill is a placeholder until you implement it for your app; until then it says so and stops. Use when the user wants the app opened where a ticket points — phrases like '/appNavigation PROJ-321', 'open the app at this screen', 'reproduce PROJ-321 on my device'."
argument-hint: "<KEY | url | spec text>"
---

# /appNavigation

**Not implemented for this app yet.** When invoked, say so in one line and stop. This file
describes what the skill is meant to do; the steps are yours to write, because every one of
them depends on your app.

## What it should do

Take a locator and end with the app open at that place, ready for the check a todo item asks
for:

- **Input** — a ticket key or URL (read through the tracker configured in
  `.claude/prompt-todo/config.json`), free spec text, or a todo item whose text is
  `/appNavigation` with the spec as sub-bullets. `/todoFromTicket` writes such an item from
  the context block at the end of a bug report: `Server:`, `App version:`, then the lines that
  name where in the app the bug lives (for a pizza-ordering app: `Restaurant:`, `Pizza:`,
  `Topping:`). Every line is optional.
- **Environment** — map `Server:` to a build of the app (flavour, bundle, URL) and make sure
  that build, at the requested version when one is given, is installed on the device,
  simulator or browser. Refuse production.
- **Login** — sign in with the credentials for that environment, kept in a file that is not
  committed.
- **Navigation** — walk from the app's start screen to the place the spec names, one level at
  a time, stopping at the deepest level the spec gives. When a level matches several things,
  ask with `AskUserQuestion` instead of guessing.
- **Report** — one line naming the screen reached (and what could not be reached, if
  anything). Nothing is edited in the todo file; the item is ticked by the user's confirm word
  like any other.

## Why there is no implementation here

Build system, environments, login screen, screen names, test ids and the automation tool
(Maestro, XCUITest, Playwright, adb, …) are all specific to your app. Write the steps above for
it in this file, add any scripts next to it, then connect the skill with
`/todoSetup appNavigation`; from then on `/todoFromTicket` writes the `/appNavigation` item
and the ticket's `QA:` items say "on the #N screen".
