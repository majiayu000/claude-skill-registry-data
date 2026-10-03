---
name: xbox-studio
description: Build, run, scaffold, troubleshoot, or product-shape a controller-first macOS Xbox helper for Bluetooth readiness, controller pairing, cloud gaming, Remote Play, captures, and account support using official Xbox, Microsoft, Apple, and browser-supported surfaces. Use when Codex needs to turn "control my Xbox stuff from my Mac" into a realistic menu bar app, launcher, or support workflow without inventing unsupported Xbox APIs.
---

# Xbox Studio

Use this skill when the user wants a Mac app, menu bar utility, launcher, or troubleshooting flow for Xbox tasks.

Default product shape: the existing `apps/xbox-studio` menu bar app, with controller and Bluetooth readiness as the primary lane and cloud gaming, Remote Play, and captures as secondary flows.

## Quick Start

1. Run `python3 scripts/xbox_brief.py --goal "<user request>"` to normalize the request.
2. If the user is asking for a broad Mac control hub or a controller and Bluetooth check, default to the existing Xbox Studio app in `apps/xbox-studio`.
3. To build and open the app fast, run `bash scripts/run_xbox_studio.sh` from the repo workspace. Use `bash scripts/run_xbox_studio.sh --build-only` for a smoke build.
4. Choose the lane only after the brief:
   - `menu-bar-app`
   - `browser-helper`
   - `controller-setup`
   - `capture-helper`
   - `support-only`
5. Be explicit about capability boundaries:
   - keep Microsoft sign-in inside Microsoft-owned browser or account surfaces
   - do not promise a public Xbox console control API unless current official docs prove one exists
   - on Mac, prefer the local Xbox Studio app, browser launchers, and controller-setup flows; Xbox pages that describe the Xbox mobile app target iOS or Android
6. If a real app scaffold is requested, prefer the existing SwiftUI menu bar app first and extend it rather than inventing a new Xbox shell.

## Workflow

### Choose The Lane

- `menu-bar-app`: extend or run the existing Xbox Studio launcher so controller checks, cloud gaming, Remote Play, and account surfaces stay one click away.
- `browser-helper`: use the user's signed-in browser session to launch cloud gaming, Remote Play, account pages, or support flows.
- `controller-setup`: focus on Bluetooth pairing, firmware guidance, and input troubleshooting on macOS.
- `capture-helper`: organize user-exported or downloaded captures locally and deep link into the official share or account surfaces when needed.
- `support-only`: explain the fastest supported path without building a local helper.

### Build The Brief

Run the brief script first. Useful commands:

```bash
python3 scripts/xbox_brief.py --goal "control my xbox stuff from my mac"
python3 scripts/xbox_brief.py --goal "make a Mac menu bar app to open Xbox cloud gaming and remote play fast"
python3 scripts/xbox_brief.py --goal "help me pair my Xbox controller to my Mac" --lane controller-setup --focus controller
python3 scripts/xbox_brief.py --goal "organize Xbox captures on my Mac and open the official share surface" --lane capture-helper --focus captures
bash scripts/run_xbox_studio.sh
bash scripts/run_xbox_studio.sh --repo-root /path/to/codex-goated-skills --build-only
```

The brief should capture:

- primary focus: `cloud-gaming`, `remote-play`, `controller`, `captures`, `account`, or `console-help`
- requested lane and default Mac shell
- required supported surfaces
- trust boundary for sign-in and automation
- fallback path if the preferred action is not directly scriptable
- whether the current request should route into the existing Xbox Studio app

### Capability Boundaries

- Treat Xbox or Microsoft web surfaces, the Xbox console UI, and Apple Bluetooth settings as the source of truth.
- Prefer `xbox.com/play` for cloud gaming and browser-first Remote Play entry.
- When the official Xbox pages describe app-only features such as installs, library management, or chat, remember that those descriptions target the Xbox mobile app on iOS or Android.
- On Mac, build helpers around browser launch, account handoff, local file handling, and controller setup rather than reverse-engineering unsupported endpoints.
- Do not invent direct APIs for console power, install queues, captures, or messages.
- If an action requires a signed-in Microsoft session or console confirmation, say so and optimize time-to-action instead of pretending it is fully automatable.

### Menu Bar App Guidance

- Prefer `MenuBarExtra` or an accessory app with an `NSStatusItem`.
- For broad "control my Xbox stuff from my Mac" requests, default to the existing `apps/xbox-studio` app and improve that experience first.
- Keep the main surface action-oriented:
  - show controller and Bluetooth readiness first
  - open Bluetooth settings or the Apple pairing guide
  - open Xbox controller help or firmware guidance
  - open cloud gaming and Remote Play
  - open Xbox account or subscriptions
  - open captures folder or official share surface
- Prefer a small popover for status and a settings window for console nicknames, saved links, and capture-folder preferences.
- Treat launch-at-login as optional.
- Always include a clear quit path in the UI.

### Controller Setup Guidance

- Use Apple's Bluetooth pairing flow for supported Xbox controllers on Mac.
- Keep controller firmware updates in Microsoft's documented surfaces.
- Treat controller troubleshooting as the primary app journey:
  - Bluetooth off
  - Bluetooth permission needed
  - Bluetooth resetting or unknown
  - no controller detected
  - non-Xbox controller detected
  - Xbox controller connected
- If the user asks for remapping, verify the exact supported tool path first rather than inventing a general-purpose Xbox remapping API on macOS.
- Load `references/controller-symptom-matrix.md` when shaping UI copy, troubleshooting states, or support actions.

### Cloud Gaming And Remote Play

- Cloud gaming is a browser-first lane. Use `xbox.com/play`.
- Remote Play can begin from `xbox.com/play` when the user switches to Remote Play and their console has remote features enabled.
- Check subscription, region, and browser constraints before promising availability.
- If browser automation is needed, pair this skill with [$playwright](/Users/arnav/.codex/skills/playwright/SKILL.md).

### Captures And Sharing

- Prefer user-owned local folders or exported media once files are on disk.
- Build helpers that watch, rename, sort, transcode, or surface capture files after export or download.
- For browsing or sharing flows that stay inside Microsoft-owned surfaces, launch or guide the user there instead of simulating a private API.

### Security And Privacy

- Keep Microsoft credentials out of custom storage unless the user explicitly requests that risk and understands the tradeoff.
- Prefer signed-in browser sessions and Microsoft-owned surfaces.
- Never frame account access, device control, or console management as appropriate for systems the user does not own or administer.

### Implementation Preferences

- Start with the smallest reliable flow that meets the request.
- Prefer:
  - existing Xbox Studio app
  - browser launcher or deep link
  - menu bar wrapper only when extending the existing app is not enough
  - automation last
- If the user wants a real macOS app scaffold in the local workspace, extend `apps/xbox-studio` rather than creating a second Xbox app by default.

## Required Deliverables

- A short implementation brief with the chosen lane.
- A clear statement of what is directly automatable versus what hands off into official Xbox or Microsoft surfaces.
- A concrete Mac surface:
  - menu bar app
  - browser helper
  - controller setup flow
  - capture helper
  - support steps
- The fastest user path to the actions they actually asked for.

## Resources

- `scripts/xbox_brief.py`: normalizes the user's request into a build brief.
- `scripts/run_xbox_studio.sh`: builds and opens the existing Xbox Studio app from a repo workspace, or does a smoke build with `--build-only`.
- `references/official-supported-paths.md`: concise guardrails for what Xbox officially documents for browser, mobile, and controller flows, plus what to avoid claiming on macOS.
- `references/controller-symptom-matrix.md`: controller-first symptom map for Bluetooth state, controller detection, and Remote Play readiness copy.
