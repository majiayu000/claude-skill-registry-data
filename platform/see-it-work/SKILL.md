---
name: see-it-work
description: Prove a change to an Expo app or a website works by seeing it, not by trusting a passing test. Picks which layer proves this change (component test, seeded simulator screenshot, smoke case, release build smoke run, browser preview, end to end journey), runs it, and shows the evidence. Use after any UI, navigation, layout, purchase or deep link change, before saying something is fixed or done, and when setting up testing in a new app.
---

# See it work

**The rule: a change is done when you have SEEN it work, not when a test passes.**
Tests prove behaviour. Only a screen proves layout. Never say "fixed" or "done" for
something a person will see until you have looked at it, and never claim more than
the layer you used can prove.

Read `references/layers.md` for how to run each layer. Read
`references/simulator-gotchas.md` before trusting any simulator result. Read
`references/paid-tier-testing.md` when the change touches a paywall, a usage limit
or anything that differs between free and paid.

## What you can and cannot use here

Check this first. It decides which layers are open to you.

| Where you are running | Layers available |
| --- | --- |
| A Mac with Xcode and a simulator (or an Android emulator) | All of them |
| Linux or Windows with an Android emulator | Component tests, Android screenshots, Android smoke and journeys |
| A cloud session (no simulator, no emulator) | Component tests and the browser preview only |

For a website (Platforms says web only), skip the simulator layers and use the
web section near the end of this file instead.

Simulators need a Mac. A cloud session cannot see a phone screen at all. If the
change needs a layer you do not have, do what you can, then say plainly which
check is still owed and add it to the release checklist for a person to do on a
device. Do not quietly downgrade the claim.

## 1. Decide which layer proves this change

Find the row that matches the change. Most changes need two layers: a test for the
behaviour and a screen for the look.

| The change | Prove it with |
| --- | --- |
| Logic, state, what renders in each case, what a tap does | Component test (layer 1) |
| Copy, colour, spacing, alignment, clipping, safe areas, anything you would describe by how it looks | Seeded screenshot (layer 2). Browser preview (layer 5) only for copy and colour, and only when there is no simulator |
| A new screen or route | Component test, plus a smoke case and its anchor (layer 3) |
| Navigation: "tapping X takes you to Y" | Component test that asserts the destination, plus a journey (layer 6) if the path crosses screens |
| Something that only breaks in a store build (native modules, minification, crash reporting) | Release build smoke run (layer 4) |
| A deep link, a share sheet, a paywall, onboarding | Journey from the real entry point (layer 6). A seeded jump cannot prove how you got there |
| A bug a user reported | Reproduce it first on the same OS version they have, then prove the fix the same way |

## 2. Write the test first and watch it fail

For any behaviour change, write or update the component test before the code.

1. Write the test. Assert what a person sees:
   - the **full string**, not a fragment (a full string match is what catches
     clipped or truncated text),
   - **every branch**: loading, empty, success and error,
   - that a press does what it should,
   - the **navigation destination**, not just that a navigation call happened.
2. Run it and watch it fail for the right reason.
3. Make the change. Run it until it passes.
4. **Undo the fix and confirm the test fails again.** Then put the fix back. A test
   that passes with and without the fix proves nothing. This has caught navigation
   "fixes" whose tests passed either way.

If the project has the test after edit hook (`templates/ui-test-hook.sh`), the
matching test runs after every UI edit and you will be told when a screen has no
test. Act on that message; do not work around it.

## 3. Look at it

For anything visual, get a screenshot of the real screen in the real state and
read the image yourself before saying anything about it.

- On a Mac: fire the test only seed deep link for the screen
  (`<your-scheme>://test-seed?screen=<id>`), let it settle, take a simulator
  screenshot, and open the PNG. See layer 2 in `references/layers.md`.
- Check the screenshot is of YOUR app and YOUR code. A shared simulator often has
  other apps installed, and one may be in front, or a system dialog may cover the
  screen. Then check the copy, build and worktree: a stale bundle or a Metro
  serving another checkout fakes a pass. See `references/simulator-gotchas.md`.
- If the bug is about layout near headers, modals or safe areas, use a simulator
  on the same major OS version as the person who reported it.
- In a cloud session: use the browser preview (layer 5). Say in the same message
  that it cannot prove geometry, gestures or anything native.

Compare against what was asked. If it is not right, fix and look again. Do not
describe a screen you have not seen.

## 4. Run the wider checks the change calls for

- **New or renamed screen:** add its `testID="screen-<id>"` anchor on every top
  level branch, add a smoke case, and run the coverage check
  (`templates/check-e2e-coverage.mjs`). Then run that one case.
- **Before a release:** run the whole smoke tier on both platforms against a
  release build made with the E2E flag (layer 4). Build the store binary again
  WITHOUT the flag afterwards. The test seam must never be in a store build.
- **A journey changed:** run the journey flow from the real entry point.

## 5. Show the evidence

Finish with what was proved and how, in a few lines:

- Which layer, which command, and the result (pass counts, or the screenshot
  itself shown to the user).
- That the test failed with the fix undone, for a bug fix.
- What is still unproved and why (no simulator, no real device, camera, purchase
  flow, other OS version). Add each item to the release checklist's **Pending**
  block with steps and the expected result, so a person checks it on a device.

A red result is information, not a verdict. Before calling a screen broken,
seed it and look at it: a red smoke run is often a slow cold start, not a broken
screen.

## Setting up a new project

Copy in only what the project needs, in this order. Each template says at the top
what it does and what to rename.

1. **Component tests** with React Native Testing Library, if not already there.
2. **The test after edit hook:** `templates/ui-test-hook.sh` into `scripts/`, and
   the hook block from `templates/hook-settings.jsonc` into
   `.claude/settings.json`. Edit the folder patterns at the top of the script.
3. **The test seam:** `templates/e2eEnabled.ts`, `templates/testSeed.ts` and the
   handler in `templates/native-intent.ts`. Replace `<your-scheme>` with the app's
   URL scheme and fill in the seeding for your own stores.
4. **The smoke tier:** `templates/smoke/_screen.yaml`,
   `templates/smoke/manifest.mjs`, and `templates/check-e2e-coverage.mjs`. Add the
   coverage check to the project's check command.
5. **Journeys:** start from `templates/journey.yaml` for the two or three paths
   that matter most (onboarding, the core action, the paywall).

Steps 4 and 5 use Maestro because that is what these templates were proven with.
Expo has its own route for the same layer: e2e by TesterArmy, run locally and then
on every pull request with EAS Workflows and Expo's hosted simulators
(https://docs.expo.dev/guides/using-e2e/, read 2026-10-20). If the project already
uses EAS Workflows, offer it as the option. The Last Mile has not run it on a real
app yet, so say that.

## A website instead of an app

The rule is the same; the tools are simpler, because the real screen is a browser
and every environment, cloud sessions included, can run one.

- **Behaviour:** component tests with the project's runner (Vitest or Jest with
  Testing Library), written first and watched failing, exactly as in step 2.
- **Look:** run the site (the dev server, or the branch's preview deploy if the
  host makes one), open the page with Playwright and screenshot it at 390 by 844
  and at 1280 by 800. Read both images. Most layout bugs on a website only show at
  one of the two widths.
- **Signed in pages:** sign in through the real form in the script, with a test
  account, never by pasting a session cookie into the code. Stub nothing you can
  run for real.
- **Journeys:** a Playwright test that starts at the URL a person actually arrives
  on (the home page, a shared link, a search result) and asserts the page it lands
  on and the words that matter there.
- **Before calling it shipped:** look at the live site once the deploy finishes.
  A preview that works can still break in production on environment values, caching
  or a different database.

Content capture for marketing video is a separate, experimental recipe:
`references/content-capture.md`. Skip it unless the user asks.

## Limits, stated plainly

- Component tests cannot see geometry. A test can pass while the text is hidden
  under a header.
- The smoke tier proves each screen mounts. It says nothing about layout.
- A seeded screen proves how the screen looks, not how a person reaches it.
- The browser preview is not a phone: no gestures, no native modules, no real
  safe areas or scroll geometry.
- Simulators need a Mac. Cameras, real purchases and push notifications need a
  real device.
