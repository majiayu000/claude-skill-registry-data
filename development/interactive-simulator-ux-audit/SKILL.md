---
name: interactive-simulator-ux-audit
description: Audit an iOS/iPadOS app's live behavior on a booted Simulator by driving it with `idb` (accessibility tree, taps, screenshots) to find bugs a fixed-frame snapshot cannot show — navigation and modal flows, back-stack, completion screens, safe-area / Dynamic Island clipping, offline and signed-out states, Dynamic Type at AX sizes. Use when asked to test the UI, find UX problems, drive the simulator to audit a UX flow, verify an interactive flow end-to-end, or size a parallel-simulator fleet. Not for scripted CI-run UI tests → host-driven-xcuitest-e2e; plain build / launch / screenshot → xcode-build-skill:xcode-build or apple-skills:simulator-utils; not for native macOS apps, which idb cannot target. Requires `udid` and `flow` arguments — the fork has no conversation history.
context: fork
agent: general-purpose
argument-hint: "[udid] [flow]"
allowed-tools: Bash(idb *) Bash(xcrun simctl *) Read
---

# Interactive Simulator UX Audit (idb-driven)

Snapshot tests render a view in a fixed-size `NSHostingView` — they model neither
navigation, taps, the device safe area, nor the Dynamic Island. A whole class of bugs
only shows when something actually drives the app: a screen that never appears after
a selection, a flow that's unplayable when the user is signed out of a cloud account,
completion content clipped by the Dynamic Island. This skill is the audit loop that
catches those, using `idb` (Facebook's iOS Simulator automation tool) to tap, read the
accessibility tree, and capture screenshots against a **booted** Simulator.

## When to invoke

- Asked to "test the UI", "find UX problems", or "drive the simulator".
- Verifying a navigation, modal, or completion flow actually renders end-to-end after a code change.
- Auditing safe-area / Dynamic-Island layout, or an offline / signed-out flow, that snapshot tests can't model.
- Debugging a report that only reproduces "in the app," not in any test.

## Scope

Owns: live Simulator driving via `idb`, the audit loop, and the coordinate/build gotchas
below. Does **not** own: scripted, CI-run UI tests that launch and assert without a human
watching → `host-driven-xcuitest-e2e`; static pixel-diff regression gates → `swift-testing-baseline`.
Use this skill first to *find* a bug interactively; write a host-driven XCUITest afterward
to *pin* the fix.

## Inputs

`context: fork` runs this skill in a subagent with **no access to the conversation
history** — it can't infer anything from earlier turns, only from the invocation
arguments and this file. When invoking (matches `argument-hint: "[udid] [flow]"`), supply:

Target simulator UDID: `$0`; flow to audit: `$1`.

- **`udid`** — the target **booted** simulator's identifier (`idb list-targets`). One
  fork drives exactly one simulator; never omit this and let the fork boot/pick one
  implicitly — see "One booted simulator serializes all driving" under Gotchas, and
  the fleet-sizing note under Preflight below for running several forks in parallel.
- **`flow`** — what to audit: the screen/feature and the specific behavior in
  question (e.g. "onboarding flow: verify the paywall's dismiss button returns to the
  correct tab, not the root").
- Anything else the fork can't discover on its own: which app/scheme is under test,
  whether the build is already installed (skip "Build + install the app under test"
  below if so), and any account/state precondition (e.g. "drive it signed out").
- **Expected build version / bundle identifier** — what the Review Checklist's
  "installed build version matches the intended commit/build" item is checked
  against; without it the fork can't tell a stale install from the current one.

Without these, the fork has no way to know which simulator to drive or what "done"
looks like — it starts from this file alone.

## Prereq: install `idb` (one-time, not via Homebrew)

If your project's policy forbids Homebrew, a direct GitHub release download is a distinct,
usually-allowed path — confirm against your own policy, then:

1. **`idb_companion`**: download `idb-companion.macos-arm64.tar.gz` from
   https://github.com/facebook/idb/releases → extract to e.g.
   `~/idb-tools/companion/idb-companion.macos-arm64/` (binary lives in `bin/`, with a sibling
   `Frameworks/` directory the binary loads via `@executable_path`). An objc
   duplicate-class warning for `FBProcess` at launch is non-fatal. The asset filename
   changes across releases — confirm the current one first with
   `gh release view --repo facebook/idb --json assets`.
2. **`idb` CLI**: `pip3 install --user fb-idb`.
3. Put both on `PATH`. Symlink `idb` directly. For the companion, use a **wrapper script**
   that `exec`s the real binary's *absolute path* — a bare symlink breaks the
   `@executable_path/../Frameworks` rpath and the companion fails to load its frameworks.
4. Verify: `idb list-targets`, then against a booted simulator's UDID,
   `idb ui describe-all --udid <udid>` returns the accessibility tree (element frames +
   labels) in **device-point** space (e.g. an iPhone 17 Pro reports 402×874 pt).

## Preflight: how many simulators fit on this Mac

Before running multiple agents or audit sessions in parallel, size the fleet with
arithmetic, not a tool — steps 1-2 need nothing beyond Activity Monitor or `xcrun simctl`
and already give a usable answer for most cases.

1. **Measure your own per-simulator footprint.** Boot one simulator running your actual
   app, let it settle, then read its `phys_footprint` — Activity Monitor's Memory column
   for the simulator's processes (or sum it yourself via `xcrun simctl spawn <udid> ...`
   if scripting). Runnable parallel count ≈ available RAM ÷ that measured number. Don't
   adopt a fixed GB figure from a blog post or any tool's README as your budget — real
   footprint shifts with iOS version, installed apps, and what the app under test does.
2. **Default answer: lower the parallel count, not the tooling.** If stock simulators
   already saturate the machine, that's the normal case — reduce how many agents/sessions
   run at once until it fits. As a dated, third-party reference point only (not a catalog
   default): on a 16 GB M1 Pro, stock simulators reportedly start thrashing around 5
   concurrent instances (`https://github.com/MobAI-App/simslim`, verified 2026-09-03). If
   step 1's math already gets you a workable number, stop here — an optional third step
   (a per-simulator daemon-disable) is in `references/simulator-fleet-sizing.md` and is
   unrelated to the rest of this skill.

## Build + install the app under test

- **Check the installed build version first**, in the app's own Settings/About screen if it
  has one. A stale install silently invalidates every finding in the session — confirm you're
  testing the build you think you are before reporting anything as a bug.
- Typical build: `xcodebuild -workspace <App>.xcworkspace -scheme <Scheme> -sdk iphonesimulator
  -configuration Debug -destination 'platform=iOS Simulator,name=<device>' -derivedDataPath
  build/sim build`, then `xcrun simctl install <udid> <App.app>`.
- **Build from a normal checkout, not an ephemeral agent worktree**, if your project keeps
  gitignored build secrets (API keys, provisioning config) outside version control. A worktree
  missing those files can make a Debug build crash at launch on a startup assertion — that's
  an environment artifact of the worktree, not a code bug; don't chase it as one.

## The drive loop

```
idb ui describe-all --udid <udid>            # element frames + accessibility labels
idb ui tap --udid <udid> <x> <y>              # tap at device-point coordinates
xcrun simctl io <udid> screenshot <path.png>  # capture, then read the PNG and look at it
xcrun simctl io <udid> recordVideo <path.mp4> # capture a flow as video
```

`recordVideo` fails outright if `<path.mp4>` already exists (`NSPOSIXErrorDomain` code 17,
"file exists") — pass `--force` to overwrite, or `rm -f <path.mp4>` first, especially when re-running
the same recording path across attempts.

- **Get tap coordinates from `describe-all`**, not from eyeballing a screenshot — a
  screenshot is rendered at the device's pixel scale (commonly 3×), not point space. Tap the
  center of an element's reported `frame`.
- **Look at every screenshot.** The accessibility tree tells you *what* elements exist; only
  the rendered image shows clipping, overlap, empty space, unreadable glyphs, or wrong z-order.
- After each tap, `describe-all` again before the next action — a tap can miss, dismiss an
  unrelated system alert, or navigate further than expected, and you need to know where you
  actually landed.

### When `describe-all` legitimately returns an empty tree

`idb`'s accessibility dump is not 100% reliable — observed in practice (and tracked upstream,
e.g. facebook/idb#767) to come back empty or missing elements on some view hierarchies, with no
element frame to tap from. When that happens, don't treat "no pixel-coordinate tapping" as
absolute: fall back to **screenshot pixels ÷ device scale = points** (e.g. a 1206×2622 px
screenshot at a 3× scale device → tap at pixel ÷ 3, so 402×874 pt for that iPhone 17 Pro) and
**screenshot after every tap** to confirm it landed correctly — this fallback is only safe
because you're verifying each step, not because the math is guaranteed accurate.

## Gotchas

- **Shells that don't word-split an unquoted variable** (zsh, by default) will pass
  `"$xy"` as one argument and fail with `invalid int value` if you built a coordinate string
  like `xy="201 488"`. Pass literal integers, or force splitting (`${=xy}` in zsh).
- **`idb` must be on `PATH`** for any MCP or wrapper tool that shells out to it — without it,
  taps fail with `spawn idb ENOENT` even though a plain screenshot still works (screenshot can
  go through `simctl` alone; tapping cannot).
- **One booted simulator serializes all driving.** Don't run two agents or two audit
  sessions against the same simulator concurrently — their taps collide. Running several
  agents each against their *own* booted simulator is fine and is a fleet-sizing question,
  not a driving one — see the Preflight section above.
- **Stress layout deliberately**: `xcrun simctl ui <udid> content_size
  accessibility-extra-extra-extra-large` then relaunch to test Dynamic Type; reset with
  `content_size large`. `appearance dark|light` for color scheme. System alerts (permission
  prompts, sign-in sheets) persist across an app relaunch — dismiss them before reading the
  app underneath.
- **Reaching a hard-to-blind-tap end state** (a puzzle win, a multi-step checkout): if the app
  has a debug-only launch argument or hook that seeds a near-terminal state, use it rather than
  trying to solve the app's own logic via taps — that's testing your tapping, not the UX.

## What to probe (this is what snapshots miss)

Core functionality should rarely hard-gate on an optional cloud/account state — verify it
doesn't, and drive all three states below separately; they exercise different code paths.

| State | How to induce | What diverges |
|---|---|---|
| Offline | Mid-flow, turn off the host Mac's network or use the host Mac's Network Link Conditioner (it applies to the whole Mac) — the Simulator uses the Mac's networking stack and has no separate airplane mode | Network calls fail fast — no connection to wait on |
| Online, signed out | Sign out of the cloud account with network reachable | The same calls can **hang** (a real round-trip stalls waiting on an unauthenticated container that never resolves) — a pass while offline can mask this |
| Online, signed in | Real signed-in test account in the simulator | Baseline correct behavior — account-gated features may by design show nothing when signed out; confirm the flow works signed in before flagging graceful degradation as a bug |

- **Navigation / modals**: does the destination screen actually appear after a selection; does
  a close/leave action show its confirmation; back-stack behavior after several pushes.
- **Safe area / Dynamic Island**: overlay or completion content clipped or overlapping system
  chrome on a notch/island device — invisible to a fixed-frame snapshot.
- **End-to-end completion**: a full success and a full failure path, including any step that
  submits to an external service that might be unavailable.

File each finding with its screenshot as evidence and a repro; label it environmental (stale
build, wrong account state) versus a genuine bug, and re-verify on a fresh, correctly-built
install before reporting it as real.

## Rationale

A snapshot test proves a view renders correctly *given* a state; it says nothing about
whether the app ever reaches that state through real interaction, or how it behaves at the
literal edges of a physical device (notch, Dynamic Island) that a fixed test harness frame
doesn't model. Driving the actual Simulator is the only check that covers the seam between
"the view is correct" and "the user can get there."

## Deviation considerations

- **No Simulator access (Linux CI, headless-only environment)**: this skill doesn't apply;
  rely on `host-driven-xcuitest-e2e` for automated coverage and snapshot tests for pixel
  regressions instead.
- **A pure macOS (AppKit/SwiftUI-Mac) app**: `idb`'s `ui` subcommand only works against
  simulators; drive a Mac app with `host-driven-xcuitest-e2e`'s window-frame-click pattern instead.

## Common Mistakes

1. **Tapping from screenshot pixel coordinates without first trying `describe-all`** — taps
   land at the wrong spot on any non-1× device unless converted (pixel ÷ scale); only fall back
   to pixel math when `describe-all` legitimately returns an empty tree (see above), and verify
   every such tap with a follow-up screenshot.
2. **Reporting a bug from a stale installed build** — always confirm the running version first.
3. **Treating "online + signed out" and "offline" as one case** — they exercise different code
   paths (fail-fast vs. hang) and must both be driven separately.
4. **Running two sim-driving sessions against one booted simulator** — taps interleave and
   corrupt both audits' results.
5. **Chasing a worktree-only launch crash as a code bug** when the project keeps build secrets
   outside version control — rule out the environment first.

## Review Checklist

- [ ] `idb list-targets` confirms the target simulator is booted before driving starts.
- [ ] Installed build version checked and matches the intended commit/build.
- [ ] Every tap coordinate came from a fresh `describe-all`, not a screenshot pixel estimate.
- [ ] Every screenshot was actually viewed, not just captured.
- [ ] Both offline and online-signed-out variants driven for any cloud-backed screen.
- [ ] Safe-area / Dynamic-Island framing checked on a notch/island-class device.
- [ ] Each reported finding has a screenshot + repro steps and is labeled bug vs. environmental.

## Related skills

- `host-driven-xcuitest-e2e` — turn a finding from this audit into an automated, CI-runnable regression test.
- `swift-testing-baseline` — the static snapshot-testing layer this skill complements, not replaces.
- `ios-accessibility-engineering` — Dynamic Type / VoiceOver checks that pair naturally with this audit loop.
- `mise-tool-management` — the general non-Homebrew tool-install pattern behind the `idb` install step above and the `simslim` step in `references/simulator-fleet-sizing.md`.
- `xcode-build-skill:xcode-build` / `apple-skills:simulator-utils` (aggregated externals) — plain build, launch, and screenshot commands; this skill is the fork-based audit loop on top of a build that already exists.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
