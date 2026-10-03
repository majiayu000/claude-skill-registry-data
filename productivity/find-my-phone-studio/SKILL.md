---
name: find-my-phone-studio
description: Build, run, troubleshoot, or refine a realistic Mac phone-recovery workflow, especially the bundled `apps/phone-spotter` menu bar app. Use when Codex needs a repo-native path for locate, ring, call, pairing, directions, or provider handoff on iPhone or Android without inventing unsupported tracking APIs.
---

# Find My Phone Studio

Use this skill when the user wants to work on a realistic phone-recovery workflow on macOS. If the current repo contains `apps/phone-spotter`, use that workspace by default.

Default product shape: an always-available macOS menu bar utility that helps the user jump into the best available Apple or Google action quickly, keeps local clues and pairing state on-device, and exposes a clear Quit path.

## Quick Start

1. If this repo contains `apps/phone-spotter`, use that workspace first.
2. Run `bash scripts/run_phone_spotter.sh doctor`.
3. Run `bash scripts/run_phone_spotter.sh inspect`.
4. Use `bash scripts/run_phone_spotter.sh generate` after changing `project.yml`.
5. Use `bash scripts/run_phone_spotter.sh typecheck` for a fast source-level sanity pass before a full build.
6. Use `bash scripts/run_phone_spotter.sh test` after model, pairing, or UI changes.
7. Use `bash scripts/run_phone_spotter.sh run` when you need the local menu bar build relaunched.
8. When the request is still exploratory, run `python3 scripts/find_my_phone_brief.py --goal "<user request>"` to normalize the product brief.
9. Default to a menu bar extra with these actions:
   - `Locate Phone`
   - `Ring Phone`
   - `Call Phone`
   - `Open Provider`
   - `Open Directions`
   - `Copy last known location`
   - `Quit`
10. Be explicit about capability boundaries:
   - do not promise a public Find My control API unless the current Apple docs prove one exists
   - do not claim "exact" coordinates beyond what Apple's own surface provides
   - keep Apple ID credentials in Apple-owned surfaces when possible
11. Only scaffold a new app when the bundled `Phone Spotter` workspace is missing or clearly not a fit.

## Workflow

### Choose The Lane

- `phone-spotter-workspace`: use and extend the bundled `apps/phone-spotter` menu bar app.
- `menu-bar-app`: build a persistent Mac menu bar app that opens supported Apple or Google surfaces, runs approved local helpers, and keeps "find" actions one click away.
- `shortcut-helper`: use Shortcuts or AppleScript glue when the user wants quick local automation and is comfortable with Apple-managed prompts or permissions.
- `browser-helper`: use browser automation only when the user explicitly wants the iCloud web flow and accepts sign-in in their own browser session.
- `support-only`: explain the most reliable user path without building a local app.

### Work The Bundled App First

- Read `references/project-map.md` before editing the app workspace.
- If the task changes project settings or app metadata, inspect `project.yml` and `PhoneSpotterApp/Info.plist` first.
- Keep `Phone Spotter` compact and menu-bar-first.
- Preserve local-first behavior:
  - pairing state and clues stay on-device
  - provider handoff remains explicit
  - no covert tracking or silent background surveillance flows
- Prefer the local runner script before typing `xcodegen` or `xcodebuild` manually.
- If `doctor` reports Xcode is not ready, stop and use the command it prints before trying `build`, `test`, or `run`.
- Use `typecheck` when you want the fastest local validation of the Swift sources without waiting for a full build.

### Build The Brief

Run the brief script first. Useful commands:

```bash
python3 scripts/find_my_phone_brief.py --goal "make a Mac menu bar app to find and ring my iPhone"
python3 scripts/find_my_phone_brief.py --goal "call my phone from the menu bar" --surface menu-bar-app --action call
python3 scripts/find_my_phone_brief.py --goal "open the provider flow for my phone" --surface menu-bar-app --action open-provider
```

The brief should capture:

- device type and likely Apple surface
- primary action: `locate`, `ring`, `call`, `open-provider`, `directions`, or `nearby`
- requested shell: menu bar app, popover, settings window, or no app shell
- trust boundary for sign-in and automation
- fallback path if the preferred action is not scriptable

### Capability Boundaries

- Treat Apple and Google apps, system services, and signed-in browser flows as the source of truth.
- Do not invent a general third-party Find My or Google Find API for arbitrary phone control.
- If the user says "exactly where it is," translate that into:
  - current or last known map location when available
  - directions handoff
  - nearby or precision-style guidance only if Apple's surface explicitly provides it on that device
- If ringing requires interaction in an Apple-owned UI, say so and build the helper around getting there faster.

### Menu Bar App Guidance

- Prefer `MenuBarExtra` or an accessory app with an `NSStatusItem`.
- Keep the main surface action-oriented:
  - latest device status
  - open location
  - ring device
  - call the phone when a number is stored
  - hand off to directions
  - open the provider surface
- Prefer a small popover for status and a settings window for account, automation, and fallback options.
- Treat launch-at-login as optional.
- Always include a clear quit path in the UI.
- Show the current integration mode clearly:
  - Apple app handoff
  - Google web handoff
  - Shortcuts helper
  - signed-in browser helper
- If you are editing the bundled repo app, preserve its current split:
  - status item plus popover
  - settings scene
  - QR pairing page on the same Wi-Fi
  - local clue timeline and summary copy actions

### Security And Privacy

- Keep Apple ID and Google credentials out of custom storage unless the user explicitly requests and accepts that risk.
- Prefer opening the Find My app, Google Find web flow, or the user's signed-in browser session instead of asking Codex to handle secrets.
- If automation touches browser state, use a profile the user controls and explain what is persisted.
- Never present stalking or covert-tracking behavior as acceptable. This skill is only for the user's own devices or devices they are authorized to manage.

### Implementation Preferences

- Start with the smallest reliable flow that meets the request.
- Prefer:
  - the bundled `apps/phone-spotter` workspace when it fits
  - deep links or app handoff
  - Shortcuts or AppleScript glue
  - browser automation last
- If browser control is needed, pair this skill with [$playwright](/Users/arnav/.codex/skills/playwright/SKILL.md).
- If the user wants a real macOS app scaffold in the local workspace, create a fresh menu bar target rather than overloading an unrelated existing app.

## Required Deliverables

- A short implementation brief with the chosen lane.
- Clear statement of what is and is not directly automatable.
- A concrete Mac surface:
  - menu bar app
  - shortcut
  - browser helper
  - support steps
- The fastest user path to:
  - see phone location
  - ring the phone
  - call the phone when allowed
  - hand off to directions when possible

## Resources

- `scripts/run_phone_spotter.sh`: local doctor, inspect, generate, open, build, test, and run helper for the Phone Spotter workspace.
- `scripts/find_my_phone_brief.py`: normalizes the user's request into an implementation brief.
- `references/project-map.md`: default workspace, main files, and guardrails for the bundled app.
- `references/apple-supported-paths.md`: guidance on supported surfaces, trust boundaries, and phrasing around location precision.
