---
name: cockpit
description: Use only when the user explicitly asks to use Cockpit, invokes a Cockpit command or skill, or asks to install, configure, develop, debug, inspect, or verify Cockpit itself; do not activate for generic app, Flutter, UI, or E2E work.
---

# Cockpit

## Activation Boundary

Cockpit is opt-in. Activate this Skill only after an explicit user request to
use Cockpit or to work on Cockpit itself. A generic request about app
development, Flutter, UI, debugging, screenshots, mobile, desktop, browser, or
E2E does not activate it. Before activation, do not invoke Cockpit commands,
inspect sessions or targets, start or stop a daemon or app, load Cockpit MCP
resources, or suggest a Cockpit workflow. Do not carry Cockpit into an unrelated
later task unless the user explicitly activates it again.

`cockpit dev` owns Flutter discovery, processes, ports, and Supervisor state.
Development handles are short lowercase base-36 values (`1` through `9`, then
`a`, `b`, ...). Copy other generated IDs exactly; never replace them with paths.
Use the globally installed `cockpit` executable everywhere. Live capabilities
are authoritative.

## Flutter Preflight

Before running any `cockpit dev` command in a Flutter source checkout, first
confirm that its Cockpit bridge entrypoint is integrated. A normal Flutter app
does not expose a Cockpit bridge by itself, so `dev start` rejects it during
bridge-shell preflight before launching Flutter.

Cockpit accepts two layouts:

- **Direct entrypoint (recommended):** `cockpit/main.dart` and its bootstrap
  are ordinary Dart files in the application's existing Flutter package. Put
  `flutter_cockpit` in that package's `dev_dependencies`, run `flutter pub get`
  at the application root, and keep the production `lib/` entrypoint unchanged.
  This preserves the real Android/iOS/macOS host, identifiers, entitlements,
  permissions, flavors, and deep links.
- **Separate module:** `cockpit/pubspec.yaml` plus `cockpit/main.dart` form a
  non-published Flutter package that depends on the real application locally.
  Use this only when package and native-host isolation is intentional; it has a
  separate Dart package name and, with platform folders, a separate native app
  identity that must be configured deliberately.

In either layout, the entrypoint must resolve `flutter_cockpit`, wrap the real
application root in `FlutterCockpitApp`, and install the Cockpit navigator
observer for every Navigator the app owns. Run `flutter pub get` in the package
resolution root after changing dependencies. If any part is absent or does not
match the app's actual public bootstrap/router API, read and complete
[flutter.md](references/flutter.md) before `cockpit dev start`.

Only an already integrated checkout takes the fast path below. `cockpit/main.dart`
is the default development entrypoint; pass another entrypoint only when the
checkout intentionally uses one.

## Select The Device Explicitly

Device choice is a deliberate input, not a host heuristic. Never infer a device
from row order, the last Flutter target, a platform name, the host platform, or
a remembered session. A connected macOS host must not win over an iOS/Android
simulator or physical device. Before the first launch in a project, and whenever
the target is ambiguous, discover the current devices:

```bash
cockpit target discover
```

This returns a bounded `targets` list with the exact `id`, `name`, `platform`,
`emulator`, and `sdk`. Use the exact `id` in the next command. If the user did
not provide a device and more than one compatible target is listed, stop and
ask which exact row to use; never choose the first, last, host, or an emulator
implicitly. If exactly one compatible target exists, state its id, name, and
platform before using that exact id. Never silently switch between a simulator
and a physical device.

The copy-ready selection flow is always:

```bash
cockpit target discover
# choose one row by its exact id; do not guess from the name alone
cockpit dev start --device <chosenId>
cockpit session show <handle>
```

If `dev start` reports `deviceAmbiguous`, use the listed candidates and rerun
with one exact `--device`; if it reports `deviceNotFound`, reconnect or boot
that same intended device and rediscover it. Do not fall through to another
device or start a second app. For a fresh project with multiple active sessions,
inspect `cockpit session list` and select the intended handle before reusing it.

```bash
cockpit target discover
cockpit dev start --device <deviceId>
cockpit session list
cockpit session show <handle>
cockpit dev status --session <handle>
```

For a registered black-box target, select the exact target after discovery and
prove its live capabilities before any mutation:

```bash
cockpit target list
cockpit target get --target-id <targetId>
cockpit target inspect --target-id <targetId> --profile evidence
```

Physical-device work requires an online, unlocked, trusted device and its
native control path (Android ADB; iOS WDA/devicectl where native control is
needed). A connected row alone is not proof of E2E readiness: after the app is
registered, `target inspect --profile evidence` must advertise the required
tree, input, capture, lifecycle, and (for integration tests) VM capabilities.
Probe with a read-only inspect, a system-first screenshot, and `dev wait` before
running a real flow. Keep the same selected device id and session handle for
Flutter launches, tests, reloads, screenshots, network reads, and recovery.

For a wired physical iOS Flutter development session, Cockpit automatically
owns the Flutter SDK's `iproxy` forwarder for the selected device and remote
bridge port. Do not start `iproxy` manually, guess a host port, or launch a
second app. If forwarding is unavailable, repair the same Flutter SDK/device
connection (for example with `flutter precache --ios` and `devicectl`), then
rerun the same `dev start --device <id>`; Cockpit keeps the existing handle.
The app still needs a valid development signature, trusted computer,
Developer Mode, and an unlocked device. Wireless sessions use the device
network path instead and require local-network access.

These are external iOS prerequisites, not Cockpit settings. Before reporting a
launch or VM timeout, verify them once on the selected device:

- macOS must have the intended Xcode selected, first-launch components and iOS
  platform runtime installed. `flutter doctor -v`, `xcode-select -p`, and
  `xcodebuild -checkFirstLaunchStatus` are the read-only checks.
- A physical device must be paired and trusted, unlocked, and have Developer
  Mode enabled. The app's development team/signing profile must be valid; a
  successful Xcode build alone does not prove installation or VM reachability.
- The host app running Flutter (Terminal, IDE, or Codex) must be allowed to
  control Xcode in macOS **System Settings > Privacy & Security > Automation**.
  When this grant is missing, Xcode can finish building while install/launch
  waits and the Dart VM Service never appears. Grant only the requested Xcode
  automation access, then rerun the same command and device.
- For a wired device, keep the USB connection alive and use the Cockpit-owned
  `iproxy`; for a wireless device, allow the app's iOS Local Network prompt and
  publish the VM port with `flutter drive --publish-port`. Current Flutter
  `flutter test integration_test/...` cannot publish that port wirelessly, so
  use USB for it. Do not switch transport or device mid-run.
- ReplayKit consent is required only for native screen recording. Native WDA
  control additionally needs a reachable, signed WDA endpoint; neither is
  required for Flutter-tree-only integration actions.

Integration tests follow the same explicit selection; always pass the exact
discovered id even when Flutter currently reports a single default:

```bash
flutter test integration_test/<test>.dart -d <deviceId>
flutter drive --profile --no-dds --driver=integration_test/driver.dart \
  --target=integration_test/<test>.dart -d <deviceId>
```

Use `flutter test` for ordinary integration tests and `flutter drive --profile
--no-dds` for VM-backed performance evidence. iOS Simulator supports debug
integration only; Flutter rejects iOS Simulator profile/AOT builds because
profile is physical-device-only. Before a physical run, verify the
exact device again; after it starts, require a live status, a current
screen/anchor, and no disqualifying runtime or native-driver error. For a
source-owned test, `flutter_cockpit_test` still uses Flutter's official runner;
it does not select a device for you. If the device disappears, repair that
device and rediscover it; do not fall through to another target or create a
second session.

A wirelessly connected iOS device is a distinct case. Current Flutter
`flutter test integration_test/...` cannot publish its VM service port and may
fail with `Cannot start app on wirelessly tethered iOS device`. Use a USB
connection for that command, or run the same integration target through
`flutter drive --publish-port` (plus `--profile --no-dds` when profiling).
On Xcode 26+ physical profile runs, add `--ios-profile-debugger` to use
Flutter's direct LLDB path and avoid the Xcode fallback that can wait for
`CONFIGURATION_BUILD_DIR`.
Keep the chosen device unlocked, accept Xcode Automation and local-network
access when required, and treat a launch that stalls before the app process is
visible as blocked rather than switching devices.

## Choose The Command

### Choose One AI Control Surface

CLI and MCP are two transports over the same authenticated Supervisor API; they
do not provide separate runtime state or extra capabilities. Install the
Cockpit runtime once because it supplies both `cockpit` and `cockpit_mcp`, but
choose one surface as the primary interface for a task. CLI + Skill is the
default because it is portable, compact, scriptable, and does not inject a
large tool catalog into every turn:

- Use the CLI with this Skill for normal development, CI, batch actions, and
  hosts that can execute shell commands.
- Choose MCP only when the host cannot reliably run shell commands or when
  typed tool/resource discovery is materially useful. Keep its profile limited
  to the domains needed by the task (`core`, `flutter`, or `e2e`) and do not
  shell out to the CLI for the same operation.
- A native plugin may bundle Skill + MCP; that is one logical integration. Do
  not add a second standalone Skill copy or MCP server on top of it.

The Skill is guidance, not a third control plane. When both surfaces are
installed, one Supervisor, one selected session, and one request path remain
the source of truth. Never execute the same mutation through CLI and MCP, and
never load the full MCP catalog when a narrow profile or one CLI command proves
the next state.

Use the highest-level command that owns the task:

| Need | Command |
| --- | --- |
| Install or refresh the current AI host integration | `cockpit skill` |
| Check for a newer CLI release without changing anything | `cockpit update --check` |
| Update the installed CLI and running Supervisor | `cockpit update` |
| Start, inspect, control, debug, resize, capture, or reload Flutter | `cockpit dev` |
| Validate or run reusable Flutter/black-box tests | `cockpit case` / `cockpit suite` |
| Read a durable run, event stream, report, or artifact | `cockpit run` / `cockpit artifact` |
| Confirm session identity, checkout, entrypoint, or reachability | `cockpit session` |
| Discover one generic live capability | `cockpit op list --kind KIND` |
| Learn an operation schema and its safer task command | `cockpit explain KIND` |
| Execute an advertised operation without a task command | `cockpit op run KIND` |

Use `dev` for normal Flutter work; it resolves the required project resources.
`case` runs one journey, `suite` runs a durable campaign, and `op` executes an
advertised operation that has no task command.

## Flutter Fast Path

Start once anywhere inside the intended Flutter project, specifying only real
launch choices. Cockpit resolves the nearest enclosing Flutter package and its
actual Git checkout/worktree, so nested projects and nested worktree directories
remain isolated. From a common ancestor containing several Flutter projects,
enter the intended project directory or pass its entrypoint explicitly:

```bash
cockpit target discover
cockpit dev start --device <deviceId>
cockpit dev start --device <deviceId> --flavor staging --dart-define API_URL=https://example.test
```

Normal loop:

```bash
cockpit dev status
cockpit dev inspect "Documents"
cockpit dev tree
cockpit dev tap "Documents"
cockpit dev hover "More options"
cockpit dev hold "Documents" --duration 900ms
cockpit dev double "Card" --interval 120ms
cockpit dev drag "Canvas" --dx 120 --dy 0
cockpit dev drag "Reorder task Third" --to "Reorder task First" --place before
cockpit dev swipe "List" up
cockpit dev pinch "Map" 1.5
cockpit dev rotate "Canvas" 1.5708
cockpit dev type "hello" --into "Message"
cockpit dev focus "Message"
cockpit dev select "Message" 0 5
cockpit dev copy "Message"
cockpit dev paste "Message"
cockpit dev clear "Message"
cockpit dev press enter
cockpit dev scroll "Operations"
cockpit dev wheel "Operations" --dy 120
cockpit dev watch "Loading" --for 5s
cockpit dev open "myapp://tasks/42"
cockpit dev wait
cockpit dev viewport 800x600
cockpit dev screenshot
cockpit dev reload
cockpit dev restart
cockpit dev diagnose
cockpit dev stop
```

When the route and every action are already known, join the commands in one shell
call with `&&` to remove repeated Agent/tool round trips while keeping every default
LON result visible:

```bash
cockpit dev tap '@open-settings' &&
cockpit dev tap '@open-profile' &&
cockpit dev type "Iota" --into '@name' &&
cockpit dev tap '@save' &&
cockpit dev inspect "Saved"
```

`&&` preserves order and stops at the first failed command. Never use a single `&`:
it runs commands concurrently and can reorder UI mutations. End the chain with the
smallest read that proves the final state. If an intermediate result determines the
next route, locator, prompt action, or network-dependent branch, stop the chain at
that decision and observe before continuing. In a project with concurrent handles,
pass the same explicit `--session HANDLE` to every command in the chain.

After an edit, use the smallest proof loop: focused analyzer/test, `dev reload`,
the exact interaction, `dev wait`, a focused `dev inspect`, then a current screenshot
for visible claims. Use `restart` only when reload cannot apply the change. Do not
start a second app to recover a healthy session, and never restart or stop sessions
other than the selected handle.

`dev reload` starts a fresh runtime-diagnostic generation. Runtime errors from the
previous generation no longer fail current diagnosis or evidence, while any error
raised after the reload remains visible and disqualifying.

Use `dev open URI` for a custom-scheme deep link, Android app link, iOS
universal link, or ordinary HTTP(S) URL. It targets the selected session's
platform and does not print the URI. After opening, run `dev wait` and inspect
the expected route or anchor; command success proves platform dispatch, not
application routing.

On a human terminal, `dev start` reports its real launch stages on stderr while
Flutter builds and the bridge becomes ready. Structured stdout remains clean;
Agent/CI or redirected runs stay quiet, and `--format none` suppresses progress.
Do not add polling, sleeps, or verbose flags just to prove that launch is active.

Reads never relaunch stopped apps. Mutations may recover one owned crash. Use
`cockpit dev start` to explicitly relaunch a stopped or crashed app. Bridge and
port changes keep the existing handle.

## Copy-Ready Workflows

Start with the shortest command that proves the next state. Add `--session`,
`--view`, `--format`, or a custom timeout only when it changes the decision.

### Project, Flutter Shell, And Session

Run inside the intended app/worktree. Cockpit resolves the nearest Flutter
package and checkout; do not register roots, ports, targets, or apps manually.
The handle binds one project, checkout, target, app, bridge, port, and artifact
namespace:

```bash
cd /absolute/path/to/worktree/apps/mobile
cockpit dev start --device emulator-5554
cockpit session list
cockpit session show 2 --view more
cockpit dev status --session 2
```

Before blaming a Flutter launch hang, verify the bridge layout and then run
`flutter pub get` from the package-resolution root:

```bash
rg -n "flutter_cockpit|FlutterCockpitApp|NavigatorObserver" \
  pubspec.yaml cockpit/main.dart cockpit/cockpit_bootstrap.dart
flutter pub get
cockpit target discover
cockpit dev start --device <deviceId>
```

Human terminals show real launch stages on stderr. Do not add sleeps or polling.
On a real timeout, read `status` once; use `diagnose` only if it does not explain
the block, then follow `next` when the response provides it. Recover a
reconnecting bridge; explicitly start only a stopped or crashed app.

### Source-First Locate, Act, And Scroll

Read the containing build method/callback when source is available. Otherwise
inspect the smallest current surface and copy its `sel`:

```bash
rg -n "Save|onPressed|CompanyButton" lib
cockpit dev tap 'Dialog >> FilledButton["Save"]'
cockpit dev wait
cockpit dev inspect 'Saved'
```

Equal matches, missing targets, and expired `:` refs are failures to observe,
not guesses to repeat. Strengthen the selector with a real ancestor/type/state;
re-inspect after navigation, filtering, reorder, overlays, or keyboard changes.
Scroll the target directly; nested lazy containers are discovered automatically:

```bash
cockpit dev scroll 'Settings >> Text["Advanced"]'
cockpit dev scroll 'Settings >> Text["Advanced"]' --align center --offset 12
```

Use `--direction` only for the initial direction and alignment/offset only when
placement matters. Read [dev.md](references/dev.md) for structural edge cases.

### Observe, Recover, Prove

System-first capture on Android/iOS exposes OS dialogs and keyboards that are not
in the Flutter tree. Observe once, apply one evidence-matched recovery, then
prove the original anchor:

```bash
cockpit dev status --session 2
cockpit dev screenshot --session 2 --view more
cockpit dev recover --session 2 --dialog dismiss
cockpit dev wait --session 2
cockpit dev inspect --session 2 'EXPECTED_ANCHOR'
```

Use `--dialog accept` only when required by the scenario and `--keyboard` only
when the capture proves it blocks the target. Never speculate on permissions,
upgrades, sign-in, payments, deletion, installation, or external navigation.

### Bounded Network And Durable Tests

Read the newest-first network index before a body; bodies are separate artifacts:

```bash
cockpit dev network --failures
cockpit dev network 37 --body response
```

Sensitive values are masked by default. Add `--raw` only with `--body` for a
needed complete/binary payload. Page with `--before ID`; `receiving` means an
unfinished response is still being recorded. WebSocket activity is indexed;
raw socket interception is unavailable.

Validate documents first, infer LON/JSON/YAML from the file extension, and prove
a terminal run state rather than trusting process exit alone:

```bash
cockpit case validate --file /absolute/case.lon
cockpit case run --file /absolute/case.lon --idempotency-key task-20260828-1
cockpit run events --run-id RUN
cockpit run get --run-id RUN
cockpit suite report --run-id RUN --output-dir /absolute/report
```

Use `flutter_cockpit_test` for source-owned Flutter integration tests and
`case`/`suite` for black-box or cross-technology journeys.

### Batch Known Actions And Keep Output Small

Join only known ordered mutations with `&&`; never use a single `&`:

```bash
cockpit dev tap '@open-settings' --session 2 &&
cockpit dev tap '@open-profile' --session 2 &&
cockpit dev type 'Iota' --into '@name' --session 2 &&
cockpit dev tap '@save' --session 2 &&
cockpit dev inspect 'Saved' --session 2
```

Stop the chain at any route, locator, prompt, or network decision. Default output
is compact LON and input format is inferred. Use JSON output only for a JSON
consumer:

```bash
cockpit dev status --format json | jq '.lifecycle'
```

Use YAML or LON input files without spelling an input format:

```bash
cockpit op run viewport.set --input-file /absolute/viewport.yaml
```

Omit `--format lon`, `--view brief`, `--input-format`, default session, and
default timeout. Use `--output PATH` when the complete projection belongs in an
artifact file.

### Updates Are Explicit

```bash
cockpit update --check
```

Only after an explicit upgrade request run `cockpit update`, refresh with
`cockpit skill`, and align all three Flutter/Cockpit package constraints to the
same version. Never upgrade a user project or delete Cockpit state implicitly.

## Unexpected-State Recovery

Treat a missing target, failed postcondition, wait timeout, unexpected route or
overlay, changed screenshot, and disconnect as a state change. Do not repeat the
failed action blindly. Preserve the intended postcondition and the same session
handle, then observe the current state once:

```bash
cockpit dev status
cockpit dev screenshot --view more
cockpit dev inspect
```

Inspect the returned screenshot path with the host's local image tool when
available. On Android/iOS, a system-sourced capture may reveal an OS prompt that
cannot appear in the Flutter tree. Use `cockpit dev diagnose --view more`
only when status, screenshot, and bounded inspection do not explain the blocker.
If status returns `developmentTargetUnavailable`, do not poll status: run its
`next`, normally `cockpit target discover`, and restore or select the intended
device before reusing the same session handle.

If a timed-out mutation already produced the expected anchor, treat it as committed
and continue without repeating it. If the screen does not belong to the intended app,
project, or target, inspect the handle returned by status with `cockpit session show
HANDLE` and select the correct session before any mutation; never repair the wrong app.

When launch logs prove `app.debugPort`, `app.started`, and remote readiness but
the operation ends in `portHandoffFailed`, treat it as a loopback ownership-probe
failure. Simulators and port-forwarding proxies may expose one endpoint through
multiple listener PIDs; do not re-authorize, switch devices, guess ports, or start
another app. Read the session/daemon logs, clean up the failed app, and retry the
same device and handle once. See [dev.md](references/dev.md) for the exact flow.

Apply exactly one matching recovery:

- For a transient, non-interactive animation, toast, or loading state, run
  `cockpit dev wait` once and re-observe; do not tap or dismiss it speculatively.
- For an expected prompt, perform the scenario's explicit action with an exact
  locator.
- For an unexpected Flutter dialog, sheet, banner, or upgrade notice, prefer its
  explicit safe action such as Later, Not now, Skip, Cancel, or Close. For a menu,
  popup, or other dismissible Flutter overlay that has no state-changing action to
  select, run `cockpit dev dismiss`.
- For an unintended child route, run `cockpit dev back` once only when the current
  state proves that returning is correct.
- When a system-sourced capture proves that the keyboard, system UI, or an OS dialog
  blocks the app, use the selected development session's recovery command. It is a
  safe no-op when the app already has focus. Incidental blockers default to dismiss;
  accept only when the scenario explicitly requires it, and request keyboard
  dismissal only when the capture proves the keyboard is the blocker:

  ```bash
  cockpit dev recover
  cockpit dev recover --dialog dismiss
  cockpit dev recover --dialog accept
  cockpit dev recover --keyboard
  ```
  This task command owns the advertised `resolveBlockers` operation; do not
  build a generic `op run` payload for routine recovery. Omit `--dialog` for
  permission-free focus recovery; add it only when a native dialog is proven.
  On macOS, `macosSessionLocked` means the login window or screen saver owns
  the foreground. Unlock the desktop and retry the same session once; do not
  grant Accessibility permission, restart the app, or create another session.
  From a common ancestor with several active Flutter projects, append the exact
  `--session HANDLE`; never recover an implicitly selected neighboring app.
- For a runtime exception or failed request, diagnose and fix the cause, then use
  `cockpit dev reload`. For a stopped or crashed owned app, use `cockpit dev start`
  so Cockpit reconciles the existing handle; never launch a second app as recovery.

Do not generically accept an upgrade, installation, permission, sign-in, payment,
deletion, or external navigation. Do not loop taps, dismissals, Back, reload, or
restart. Do not clear app data, reinstall the app, reset a simulator/emulator, kill
unrelated processes, or create a second session as generic recovery. If the same
blocker survives one targeted recovery, collect standard diagnostics and fix the app
or environment cause instead of trying random actions. After any mutation timeout,
read status and inspect the expected anchor before retrying because it may have committed.

Prove recovery before resuming the original flow:

```bash
cockpit dev wait
cockpit dev inspect "EXPECTED_ANCHOR"
cockpit dev screenshot
```

Resume the original action once only after the expected anchor is present. Re-read
[dev.md](references/dev.md) when the blocker crosses Flutter/native boundaries or
the same state returns.

## Sessions And Isolation

The short handle is the only routine session selector. Cockpit stores one active
handle per canonical Flutter project, guarded by checkout identity. Commands run
inside that project reuse it automatically. One checkout may contain many Flutter
projects, and one project may keep concurrent platform or target handles. `cockpit
dev use HANDLE` changes the active selection for that handle's project. The selection persists.
An explicit `--session HANDLE` selects exactly one command and never changes the
saved active selection. A session-bound `next` command keeps that exact handle;
execute it as returned instead of dropping `--session`.

```bash
cockpit session list
cockpit session show 1
cockpit dev use 2
cockpit dev status --session 2
```

`session show` reports the Flutter project, entrypoint, platform/device,
lifecycle, and current live state. Add `--view more` when canonical workspace,
checkout, target, or runtime IDs are needed. Check it before a destructive
mutation when concurrent apps look similar. Omitting `--session` is safe
when running inside the intended project and its active handle is the intended
target. Read readiness as two independent signals: `appLive:true` with
`bridgeLive:false` means the application still runs but its control bridge is
blocked or reconnecting. Never run `dev start` for that state; follow `next`, normally
`cockpit dev recover --session HANDLE`, then read status once. Only an explicit stopped
or crashed state with `appLive:false` justifies `dev start`.
With concurrent targets for that project, select once with `dev use`, or
pass `--session HANDLE` on the exact command. Project selection always uses the
nearest enclosing Flutter package plus checkout/worktree identity; neighboring
projects and worktrees are never mixed. A true common-ancestor ambiguity still
requires entering the project directory or passing the exact handle.

`session list` is a fast, side-effect-free local index: it never starts a worker,
attaches Flutter, reconnects, or relaunches an app. Its `last` is the last saved
state, not a live probe. Use `session show HANDLE` or `dev status --session HANDLE`
only when current reachability is needed.
Stopped or crashed handles stay registered so `dev start` can recover them and
reuse the same short reference; Cockpit only removes duplicate target records
automatically. Remove a handle explicitly with `cockpit session remove --session
HANDLE` when the project is permanently gone.

Never register or delete roots, targets, apps, ports, or runtime sessions manually
for the fast path. Every `dev start` refreshes the selected entrypoint index,
reuses an identical development target, removes orphaned duplicate or stale target
registrations, and preserves the local handle. If a session is unreachable, inspect
`status` or `diagnose`; rerun `dev start` only when its state or `next` requires it.
Reads do not relaunch an intentionally stopped app. A timed-out request cancels that
request, not the owned app; check `dev status` before retrying. Cockpit does not read a
keychain or secret store. `--env` values are process-only and are not persisted.

For black-box platform targets, use only capabilities returned by `target inspect`.
Android uses ADB/UiAutomator, iOS uses simctl or target-scoped WDA, macOS uses
Accessibility, Windows uses UI Automation, and Linux probes AT-SPI. Flutter Web
keeps the in-app Flutter tree. A generic Chromium page needs an explicit target
`--cdp-url`; Cockpit never scans a default port or attaches to another browser
profile. Read [environments.md](references/environments.md) before registering a
browser page or repairing a blocked platform driver.

Use `cockpit update --check` for a side-effect-free release check. A newer
version is informational until the user explicitly asks to upgrade: never run
`cockpit update` or change project dependencies automatically. After explicit
upgrade approval, `cockpit update` updates the CLI and Supervisor while
preserving authorization and durable state; then run `cockpit skill` and give its
prompt to the current AI host so the complete Skill and selected integration
surface can be refreshed. Do not manually delete Cockpit home data, Pub
caches, sessions, executables, or ports.
When a Flutter project uses Cockpit packages, upgrade the active integration
(the root application's direct `dev_dependencies` or the optional development
shell) and `cockpit_protocol`, `flutter_cockpit`, and `flutter_cockpit_test`
constraints to the exact same Cockpit version only after the user explicitly
requests the upgrade, then run `flutter pub get`; read
[upgrade.md](references/upgrade.md) for the ordered project upgrade and
verification flow.

`cockpit daemon start` and an unflagged
`daemon restart` preserve the authorization of a healthy running daemon; with no
running daemon they start restricted. Add `--yolo` only to explicitly require yolo.
To return to restricted, stop the daemon and start it without `--yolo`. Lifecycle
lock waits consume the command's own timeout instead of blocking indefinitely.

## Timeout Defaults

Every executable command has `--timeout VALUE`; values accept `ms`, `s`, `m`, or `h`.
Use the default first and override only a measured slow operation. Common defaults:

| Command | Default |
| --- | ---: |
| `dev start` | `20m` |
| `dev status`, inspect, tree, direct UI actions, open, viewport, screenshot, diagnose | `1m` |
| `dev wait` | `30s` |
| `dev watch` | `30s` |
| `dev network`, recover, reload, stop | `2m` |
| `dev scroll` | `3m` |
| `dev restart` | `5m` |
| `target discover` | `2m` |
| case/suite validation | `1m` |
| `case run` | `30m` (maximum `6h`) |
| `suite run` | `2h` (maximum `24h`) |

Do not add sleeps around Cockpit. `dev wait` waits for UI quiet; add `--network` only
when the assertion depends on network completion. Its `--quiet` option changes the
settle window, not response view. After a mutation timeout, inspect state before
retrying because the mutation may already have committed.

## UI And Evidence

Execute exact text directly only when that text names the intended actionable
target, or use a stable locator. Do not add a pre-inspect round trip merely to
confirm an already-known action. If an action returns `unsupportedCapability`,
`ambiguousTarget`, `targetNotFound`, or `targetNotHittable`, do not guess that a
nearby control owns passive text. Run the exact `next` command once. A failed
stable selector performs a bounded inspect of the same query; an expired live
target ref refreshes the current control surface. Copy the returned actionable
`sel` and retry the original action once. If bounded inspect returns `count:0`,
use its current `route` and default bounded `mounted` targets to identify a wrong
route or visible blocker;
do not repeat the missing locator or load a full tree. Capture the current screen
only when those mounted targets do not explain the state.

For a first-party Flutter checkout, source is the default locator channel during
development, not an inspect fallback. The feature being edited and its build or
callback code are normally already known. Use that code directly; if it is not in
context, use `rg` with visible text, route names, Widget types, tooltips, or callback
names, then read only the containing build method and interaction callback. Construct
the exact structural selector and execute the action without a pre-inspect round trip.
Use `CompanyButton >> Text["Save"]` for a labeled custom control, or
`Toolbar >> [type="CompanyIconButton"]` when it has no text, key, or Semantics.
Cockpit traverses the mounted Element tree for explicit actions even when compact
inspect omitted that Element, requires one visible match, and performs a real
hit-tested `tap`, `hold`, or `double`. Equal matches fail as ambiguous; add a real
ancestor, route, key, or other source-proven condition instead of guessing or using
coordinates.

Use `dev inspect` before an action only for runtime facts source cannot determine:
which route or overlay is mounted, runtime-generated content or ordering, lazy
mounting, or a selector that failed or returned ambiguous. Source removes guesswork
but is not runtime proof: validate the source-defined live postcondition after the
action.

For runtime-only ambiguity or exploration, run the smallest `dev inspect QUERY`. It
searches mounted Flutter Element targets, independent of developer-authored
Semantics, and returns the shortest stable `sel` plus compact known `can` actions.
Copy `sel` exactly into `tap`, `type --into`, or `scroll`; every selector condition
intersects and equal matches fail instead of guessing. `inspect` prefers the shortest
unique stable selector: identity or exact text, then an ancestor scope, then path,
with `:nth()` reserved for truly ordered peers. Semantics remains one optional signal
and action fallback. Icon-only controls expose readable tooltips. Lazy lists expose
only mounted rows; pass an off-screen target directly to `dev scroll`, which owns
mounting and reveal.

With no query, `dev inspect` returns the mounted control surface as an
operation map: every addressable row in visual order, plus what sits beyond
the current viewport or under an overlay. Read each `targets` row as `sel`,
optional `label`, executable `can`, optional `state`, and optional `value`.
Text rows (titles, labels, content) carry no `can` and exist for context and
durable text selectors. State can report `disabled`, `selected|unselected`,
`on|off|mixed`, `focused`, `readonly`, or `obscured`; obscured inputs never
expose their value. Rows marked `offscreen` are mounted outside the viewport:
pass their `sel` directly to `dev scroll`, which owns reveal. Rows marked
`covered` sit behind an open dialog, sheet, or menu: they describe the page
that returns after the overlay is dismissed and stay non-actionable until
then, so act on the overlay's own rows or `dev dismiss` first. The response
reports `offscreen` and `covered` counts when those buckets are non-empty. A
`sel` beginning with `:` is an opaque live ref for this mounted UI; only
currently visible rows carry one. Copy it directly into the command named by
`can` without another inspect. Live refs are deliberately transient:
re-inspect after navigation, overlay, filtering, reorder, keyboard, or other
control-surface changes. Never store them in a case or suite. A disabled
target intentionally has no executable action. Use these rows directly
instead of querying every control or loading a tree merely to discover
actions. A targeted `dev inspect QUERY` still searches passive content and
returns a stable selector for durable reuse when text or structure, rather
than the whole control surface, is the question.

Interaction ownership stays explicit: merged ancestor `Semantics` never makes
passive descendants actionable, and descendants below `IgnorePointer(ignoring:
true)` or `AbsorbPointer(absorbing: true)` advertise no mutation actions. When
one actionable outer row
delegates selection to exactly one blocked control, the outer target carries
that control's state; multiple delegated controls leave state unresolved instead
of guessing. Execute only the `sel` whose own `can` advertises the command.

`can` maps directly to task commands:

| `can` | Command |
| --- | --- |
| `tap` | `dev tap [TARGET]` or `dev tap --at X,Y` |
| `hover` | `dev hover [TARGET]` or `dev hover --at X,Y` |
| `type` | `dev type VALUE --into TARGET` |
| `copy` | `dev copy [TARGET]` |
| `paste` | `dev paste TARGET` |
| `clear` | `dev clear TARGET` |
| `focus` | `dev focus TARGET` |
| `select` | `dev select TARGET START END` |
| `hold` | `dev hold [TARGET] [--duration TIME]` or `--at X,Y` |
| `double` | `dev double [TARGET] [--interval TIME]` or `--at X,Y` |
| `drag` | `dev drag TARGET --dx PX --dy PX` or `dev drag TARGET --to DEST [--place before|center|after]` |
| `fling` | `dev fling TARGET --dx PX --dy PX --velocity PX_PER_S` |
| `swipe` | `dev swipe TARGET up|down|left|right` |
| `pinch` | `dev pinch TARGET SCALE` |
| `rotate` | `dev rotate TARGET RADIANS` |
| `pan` | `dev pan TARGET --dx PX --dy PX` |
| `multi` | `dev multi [TARGET] --sequence-file FILE` |
| `inc` / `dec` | `dev inc TARGET` / `dev dec TARGET` |
| `dismiss` | `dev dismiss TARGET` |
| `scroll` | `dev scroll TARGET` |
| `wheel` | `dev wheel TARGET --dy PX [--steps N]` |

Do not substitute a gesture or coordinate action when a direct command is
advertised.

Selector quick reference:

| Need | Selector |
| --- | --- |
| Current mounted control | `:a7b9x2` |
| Exact text | `Save` |
| Cockpit ID | `#save` |
| Flutter Key | `@save-key` |
| Type + text | `FilledButton["Save"]` |
| Source-only custom type | `[type="CompanyIconButton"]` |
| Multiple conditions | `#save[type="FilledButton"][route="/edit"]` |
| Ancestor scope | `Dialog >> FilledButton["Continue"]` |
| Layered Stack scope | `Stack >> Positioned >> TextButton["Buy"]` |
| Nested branch scope | `Stack >> Stack >> TextButton["Buy"]` |
| Popup/overlay scope | `Overlay >> MenuItemButton["Delete"]` |
| Keyed row scope | `@task-row >> FilledButton["Open"]` |
| Contains / fuzzy text | `[*="Save"]` / `[~="Svae"]` |
| Contains / fuzzy tooltip | `[tip*="Save"]` / `[tip~="Svae"]` |
| Stable ordered item, last resort | `Button["Item"]:nth(2)` |

Selector string values use JSON quoting and `:nth()` is 1-based. Plain positional
text is exact. Prefer `#id`, exact text, `@key`, type/ancestor, route, then path;
use `:nth()` only for a real ordered list. Public branching scopes such as
`Stack`, `Positioned`, `IndexedStack`, `Overlay`, `OverlayPortal`,
`CompositedTransformTarget`, `CompositedTransformFollower`, `Flow`, and
`CustomMultiChildLayout` are retained in key-free paths so nested overlays and
custom layouts can be addressed without adding test-only keys. Equal actionable
matches use hit testing only when exactly one visible control wins; otherwise
Cockpit returns `ambiguousTarget`. Inactive `IndexedStack`/`Visibility` layers
are excluded even when their elements remain mounted. Do not invent selector
syntax: use the table or copy `sel` from `inspect`.

```bash
cockpit dev inspect
cockpit dev tap ':a7b9x2'
cockpit dev hover 'More options'
cockpit dev tap --at 320,640 --device mouse
cockpit dev hover --at 480,96
cockpit dev inspect "Save changes"
cockpit dev tap '#save-button'
cockpit dev hold ':k4m2p8'
cockpit dev drag 'Canvas' --dx 120 --dy 0
cockpit dev drag 'Reorder task Third' --to 'Reorder task First' --place before
cockpit dev swipe 'List' up
cockpit dev pinch 'Map' 1.5
cockpit dev inc ':v8c1r6'
cockpit dev tap 'Dialog >> FilledButton["Save"]'
cockpit dev tap 'Toolbar >> [type="CompanyIconButton"]'
cockpit dev type "hello" --into '@message'
cockpit dev focus '@message'
cockpit dev select '@message' 0 5
cockpit dev copy '@message'
cockpit dev paste '@message'
cockpit dev scroll "Operations"
cockpit dev wheel "Operations" --dy 120 --steps 3 --device trackpad
cockpit dev watch "Loading" --for 5s --every 200ms
```

`dev watch` is bounded and delta-only: it reports route, target, control-state,
and layout changes with `endedBy` set to `duration`, `timeout`, `quiet`,
`eventLimit`, or `error`.

Pointer actions `tap`, `hover`, `hold`, and `double` may omit a selector only
when they include the explicit `--at X,Y` point. Coordinates are logical Flutter
viewport pixels; they are a deliberate fallback for source-known custom surfaces
that expose no stable mounted target. Do not guess coordinates when a selector
can be derived from source or `inspect`.

For delivery-critical interactions, verify the complete time path rather than
only the final frame: a real hold/double interval, a multi-pointer sequence,
animation checkpoints, and a bounded watch for changing text/layout/state.
Finish with `dev wait` and one focused inspect or screenshot. Keep sequences
ordered, release every pointer, and stop watching on `quiet`, `eventLimit`, or
an operation error instead of retrying mutations.

Use `dev tree` only when bounded target inspection cannot explain the structure:

```bash
cockpit dev tree
cockpit dev tree --view more
cockpit dev tree --view full
cockpit dev tree --view more --under 'Settings >> List'
cockpit dev tree --view full --under '@task-list' --depth 2
```

Use `--under` to inspect only one mounted subtree and `--depth` to cap its
descendants relative to that root (`0` means the root only). The scope must
resolve to exactly one element; missing or ambiguous scopes fail explicitly and
never expand into a full-tree response. Both options require `--view more` or
`--view full`; `--max-nodes` remains the final artifact bound.

The default tree is a compact actionable target index with reusable `sel`, not a
partial raw tree. `more` writes the mounted public Widget structure to an artifact;
`full` writes every mounted Element, including private/offstage nodes, with
Widget/Element/State/Render types, geometry, scroll ancestry, and bounded diagnostic
properties. Both structural views print only the verified absolute artifact path.

`dev scroll TARGET` uses exact matching by default and automatically ranks visible
scroll containers. Lazy targets are searched with independent forward and reverse
budgets; once mounted, every scrollable ancestor is revealed from inner to outer and
the target must be fully visible through all ancestor viewports. `nearest` also verifies
the real hit test: when a fixed Flutter overlay covers an otherwise visible target and
scrolling can avoid it, Cockpit moves the target to the viewport center. Use
`[*="text"]` only when exact text is insufficient. `--direction up|down` selects only
the initial search direction; after reaching that boundary Cockpit automatically tries
the opposite direction. Use `--align start|center|end` only for deliberate placement;
`--offset PX` moves the target toward the viewport end for positive values and toward
the start for negative values. Omit `--align nearest`, zero offset, direction, and
default budgets.

`dev wheel TARGET --dy PX` dispatches real `PointerScrollEvent` signals to the
target. Use `--dx` for horizontal input, `--steps` for repeated wheel ticks,
`--interval` to space them, and `--device trackpad` when the app distinguishes
trackpad from mouse input. Cockpit advertises wheel on `Scrollable`, custom
`Listener(onPointerSignal: ...)`, and trackpad-aware `InteractiveViewer` targets;
it remains available without a Key or Semantics label when source structure is
the reliable locator. Use `--at X,Y` only for a signal owner that is not itself
discoverable as a mounted target.

Re-inspect after list reorder, filtering, navigation, dialogs, sheets, or keyboard
transitions. `type VALUE --into
TARGET` replaces the field value; use `press enter` for a separate IME/key action.

`dev wait` is UI-only by default; add `--network` only for request-dependent
assertions. `--timeout VALUE` accepts `ms`, `s`, `m`, or `h`; every command has a
generous operation-specific default, so override only when the app genuinely needs
more time. `--quiet` on `wait` changes its settle window, not output view.

Default screenshot routing follows what must be visible:

- Android/iOS capture the system screen first for OS dialogs, then Flutter.
- Desktop/Web capture Flutter first, then an available system fallback.
- `--view more` shows the source; brief still reports fallback.

```bash
cockpit dev screenshot
cockpit dev screenshot --format path
cockpit dev screenshot --save /absolute/current.png
cockpit dev screenshot --compare /absolute/baseline.png --diff /absolute/diff.png
```

Visible claims require a current screenshot. Return only paths, never bytes,
Base64, data URIs, image contents, or hashes. RGBA comparison is exact unless a
pixel tolerance is explicitly required. `--save` selects an exact output path;
`--compare` accepts a baseline and `--diff` writes the diff. Do not compare captures
from different sources or viewport sizes. Android/iOS system capture is essential for
permissions and OS dialogs; the response identifies Flutter fallback.

## Network And Diagnostics

The network command returns a bounded newest-first index, not unbounded bodies. The
default page is 12 rows. Each request has a numeric ID; request/response body retrieval
writes separate verified artifact files and prints their paths. Inspect the row first,
then retrieve only the needed side. `--before ID` pages backward without repeating the
current page.

Sensitive query, header, cookie, structured-body, and credential-like values are
masked with `*` by default, not removed. Use `--raw` only with `--body` when complete
values or binary bytes are required; raw data remains in the saved body file rather
than stdout. Metadata and bounded previews remain safe and small.

SSE and other unfinished HTTP responses remain `receiving`; repeated `dev network`
reads show their current state and body artifact until the response ends. WebSocket
connections and frame activity are indexed. Text frames may be previewed; binary and
unsafe payloads stay metadata or files. Raw socket interception is unsupported.

```bash
cockpit dev network
cockpit dev network 37
cockpit dev network --before 37
cockpit dev network --failures --method GET --uri /api
cockpit dev network 37 --body response
cockpit dev network 37 --body both --raw
```

Use `dev diagnose --view more` for bounded UI, error, log, and network
health. Use `full` only when the complete response is needed; large response
bodies should be read from their reported paths. Start with `--failures`, `--method`,
or `--uri` when the app generates heavy traffic.

## Output And Input

Brief canonical LON is the default. For routine human or Agent reads, omit
`--format`; never request JSON merely because it is structured. Use `--format json`
only on a pipeline that uses `jq`, when the next consumer/API explicitly requires
JSON, or when inspecting JSON-specific wire behavior. Omit
`--view brief`, `--format lon`, the current session, inferred input, and
default wait/screenshot settings. Add an option only when it changes the requested
behavior.
LON may table-encode repeated object arrays, for example
`mounted:[sel label can;@save Save tap;...]`. The first row declares columns; it is
not an empty target. Read later rows by those columns instead of switching to JSON
only to expand the same data.
Formats are `lon|json|yaml|jsonl|path|none`. `path` prints one verified artifact/output
path, `none` is silent, and `--output` writes an atomic projection whose stdout is
only its verified path.

```bash
cockpit dev diagnose --view more
cockpit dev diagnose --view full --output /absolute/diagnose.lon
cockpit dev status --format json | jq '.lifecycle'
cockpit op run viewport.set --input '{width:800 height:600}'
```

`--input` and `--input-file` accept LON, JSON, or YAML. File extensions are
preferred because input format is inferred; specify an input format only when a
source is ambiguous. Never invent fields: use `cockpit explain OPERATION` or the
advertised schema first.

Brief output contains only the next-decision fields. Use `--view more`
for diagnosis and `full` only for the complete response. Do not request or
print screenshots, file contents, Base64, data URIs, hashes, or unneeded
byte counts. Stdout reports verified paths; read an artifact file only when its
metadata proves it is the needed evidence.

`more:N` means N projected values were omitted; request `--view more` only when
those values affect the next decision. Copy operation input
names only from `explain` under `input.fields`.

## Flutter E2E And Black-Box E2E

### Integration-Test Development Loop

Use this loop while authoring a Flutter integration test or a black-box case;
it keeps failures diagnosable and avoids guessing:

1. **Prepare one target.** Confirm the Cockpit bridge layout, discover devices, and
   select one exact device id. Start or reuse one session and record its handle;
   never let a test silently switch targets.
2. **Author from source.** For `flutter_cockpit_test`, read the build method and
   callback first, then use the smallest structural selector (`#id`, `@key`,
   exact text, type/ancestor). Use `case`/`suite` for black-box flows and put
   native/system actions on the explicit native plane.
   For an internationalized flow, make the language switch a real step, then
   obtain every later translated label from the app's current translation
   getter at the moment of the action. Cockpit resolves every selector again
   for each command, so `cockpit.tap(cockpit.context.t.checkout.pay)` follows slang,
   intl, easy_localization, or a custom localization context after the switch.
   Do not cache translated strings or transient `:ref` values across a locale
   change; re-inspect after the language mutation. Prefer keys, Cockpit IDs,
   types, and structural scopes for language-independent controls.
3. **Prove the baseline.** Run the smallest focused test, then check
   `cockpit dev status`, `cockpit dev inspect`, and a current
   `cockpit dev screenshot`. Screenshots are evidence paths only; do not print
   image bytes. On Android/iOS, inspect the system capture first for dialogs or
   keyboards; on desktop/web, inspect the Flutter capture first.
4. **Add one step and one postcondition.** Run the exact interaction, settle
   with `dev wait`, and assert the route, target state, text, or screenshot that
   the step promises. Screenshots are opt-in: keep ordinary steps compact and
   capture only when the user requests a visual checkpoint or the step fails,
   is ambiguous, or reports a missing target. For `flutter_cockpit_test`, use
   `cockpit.screenshot(name: 'failure-<step>')`; for a live/black-box flow use
   `dev screenshot`, then retain only the artifact path. Use
   `snapshot`/assertions for cheap state facts and bounded logs,
   `dev diagnose --view more`, or run artifacts for runtime evidence. Do not
   screenshot every animation tick or print image/log bytes. For lazy or
   animated surfaces, use direct `dev scroll`, animation
   checkpoints, or bounded `dev watch`; do not add sleeps.
5. **Diagnose a failure once.** Preserve the same session and collect the
   failure screenshot, focused `inspect`/`tree`, `dev diagnose`, and the test
   artifact path. Read source locations and the smallest relevant artifact
   before changing a selector. If an OS overlay is proven, apply one matching
   `dev recover`/host action and re-prove the original anchor; never blindly
   repeat a tap or accept a prompt.
6. **Harden and promote.** Re-run the focused flow, then the complete case or
   suite with its terminal report and artifacts. Keep screenshots for visual
   checkpoints and failure evidence, keep large logs/network/timeline data in
   files, and verify the same test on every CI platform that advertises its
   capabilities. A passing process exit alone is not a passing E2E test.

For locale coverage, verify the actual UI path and read translation getters
again after the language mutation. `flutter_cockpit_test` exposes
`cockpit.context`, a freshly resolved visible application context below the
current `Localizations`; it needs no business Key, Semantics label, or cached
context. The selector is resolved when each command runs, so an old translated
string or `:ref` must never be reused:

```dart
await cockpit.tap(cockpit.context.t.settings.language);
await cockpit.tap(cockpit.context.t.language.chinese);
await cockpit.waitForUi();
await cockpit.tap(cockpit.context.t.settings.save);
```

Here `.t` is slang's application-owned translation extension, not a Cockpit
API. For `intl`, use `AppLocalizations.of(cockpit.context)!`; for
`easy_localization` or a custom delegate, call that app's existing getter with
`cockpit.context`. Cockpit does not import any localization package. Perform
the real language switch, wait for the rebuilt UI, then obtain the next label
from a freshly read context/getter. For language-independent controls, prefer
keys, Cockpit IDs, types, and structural scopes.

Typical focused loop:

```bash
cockpit target discover
cockpit dev start --device <deviceId>
flutter test integration_test/<test>.dart -d <deviceId>
cockpit dev screenshot --save /absolute/evidence/baseline.png
cockpit dev inspect "EXPECTED_ANCHOR"
cockpit dev wait
cockpit dev screenshot --save /absolute/evidence/after.png
```

For a durable black-box flow, validate before running and inspect its terminal
run rather than polling a process:

```bash
cockpit case validate --file /absolute/case.yaml
cockpit case run --file /absolute/case.yaml --idempotency-key <key>
cockpit run events --run-id <run>
cockpit run get --run-id <run>
```

For Dart-authored Flutter integration tests, use the development-only
`flutter_cockpit_test` package. It keeps Flutter's official
`integration_test` runner while reusing Cockpit's source-first Element
selectors, real hit-tested actions, nested/lazy scrolling, assertions,
native evidence, real wheel input, and explicit host actions. Add it with
`flutter pub add --dev flutter_cockpit_test`; never import it from production
application code. Start with `cockpitTestWidgets`, use source-known selectors
directly, and keep OS/system actions behind the explicit `hostCommand` bridge.
Do not use this package for a purely black-box target; use `cockpit case` or
`cockpit suite` there. Read [flutter-test.md](references/flutter-test.md) for
the complete API and platform workflow.

For native `flutter drive` performance runs, use `--profile --no-dds` so the
app runs in Flutter's profile build and integration_test connects to the device
VM Service directly. `flutter test integration_test/...` is debug-only. The
non-web Flutter Driver rejects `flutter drive --release`; do not keep retrying
that command. A release artifact can still be built for a native XCTest,
Android instrumentation, or device-lab runner, but VM-backed Cockpit timeline,
CPU, heap, GC, and DevTools data are unavailable there. The complete platform
commands and the release-harness boundary are in
[flutter-test.md](references/flutter-test.md).

Black-box `case` files can mark more than one performance segment in the same
journey. Keep segments sequential and give each a unique name:

```yaml
target:
  platform: flutter
  targetKind: flutterApp
  plane: semantic
  buildMode: profile
steps:
  - stepId: perf-start
    startPerformance: {name: open-list, mode: profile}
  - stepId: open-list
    action: {type: tap, locator: {text: Open list}}
  - stepId: perf-stop
    stopPerformance: {}
  - stepId: perf-start-checkout
    startPerformance: {name: checkout, mode: light}
  - stepId: checkout
    action: {type: tap, locator: {text: Checkout}}
  - stepId: perf-stop-checkout
    stopPerformance: {}
```

`target.buildMode` checks the selected session's actual `debug`, `profile`, or
`release` mode; it never substitutes a requested value. `startPerformance.mode`
is capture density (`light` or `profile`), not the app build mode. Only one
segment may be active, segments may not overlap, and each completed segment is
published as `performance/<name>.json`. Failure, cancellation, and timeout
attempt residual performance cleanup. A target without the advertised
performance capability is blocked before execution.

For Flutter performance work, use `cockpit.profile` around the smallest
meaningful interaction. It records the engine's original `FrameTiming` values,
including vsync and raster-finish wall-time timestamps, and, on native targets,
the official integration-test VM timeline/GC streams plus bounded process RSS
samples. The report includes build/raster/vsync/total phase percentiles,
cache peaks, jank, memory start/end/peak/delta, and explicit retention drops.
Tune collection only when it changes the decision: `sampleEvery` controls native
RSS frequency, `streams` and `timeline` select VM tracing, `memory` disables RSS,
and `maxEvents` bounds retained VM events. Keep the defaults for normal captures;
use a shorter interval or narrower streams only for a targeted investigation.
Normal in-memory retention is intentionally compact (20,000 timeline events,
20,000 CPU samples, 2,000 heap samples, and 2,000 rebuild frames); it does not
reduce the lossless JSONL archive when `archive` is supplied.
Short captures may keep the complete report in memory. For multi-hour flows,
open a `CockpitPerformanceArchive` and pass it as `archive` so records stream
to rotating JSONL chunks while the report remains a quick in-memory projection.
The explicit archive defaults to lossless. Set `maxPendingBytes` to tune the
in-memory back-pressure window: `lossless` spills excess records to a
recoverable JSONL sidecar, while `low` drops and counts records beyond the
bound. The manifest path is the entry point for the complete stream; its chunk
entries are relative to the manifest, so a downloaded CI artifact directory
can be moved without rewriting paths.
Combine manifests or individual JSONL chunks from multiple platform/CI runs
with `CockpitPerformanceArchive.merge([...])`; it validates and rewrites the
stream incrementally, preserves each source order, and namespaces duplicate
capture handles. It does not globally sort events from different devices
because their monotonic clocks are unrelated.
A standalone HTML opened with `file://` can read only its embedded payload; it
cannot silently read arbitrary project JSON/JSONL paths. Use an HTTP server or
a browser file picker for external JSONL files, and load chunks incrementally
instead of embedding a multi-gigabyte stream.
The bounded result is stored in
`IntegrationTestWidgetsFlutterBinding.reportData` under
`cockpit.performance.NAME`; normal Cockpit output stays compact. With a JSONL
archive, the result omits retained frame/event arrays and the manifest/chunks
are the lossless source of truth. `dropped` counts expose retention limits;
aggregates describe retained frames when a retention limit is reached. Empty phases omit duration aggregates, `fps` is
omitted when source timestamps cannot prove a strictly increasing cadence, and
Web reports VM timeline as `unavailable:web`. Treat missing metrics as
unavailable, never as zero. Reports include the Flutter build mode. Debug
timings are diagnostic only; profile timings are suitable for performance
decisions. Release timings are suitable only when collected by a native release
harness, not by `flutter drive`, which rejects release mode for non-web tests.
Use the report artifact path for
large timeline inspection instead of printing frame/event arrays. The standalone
HTML viewer uses relative capture time, hover details, frame-budget, jank,
cadence, raster-cache trend, VM category cost, operation hotspots, startup milestones,
memory, cache/GC, duration-based VM flame charts, CPU sampling stacks,
heap/allocation classes, and evidence-only GPU/shader signals, plus a code-evidence table
populated only from source locations explicitly provided by VM event arguments;
it never guesses a Dart file or CPU call stack from frame timing.
The complete report also includes the bounded VM heap trend, all-isolate
before/after health and lifecycle events, timeline recorder/stream metadata, VM
runtime identity, and VM process-memory trees. Compact results keep only counts;
`performanceJson()`/`exportPerformanceJson()` and HTML retain the complete
bounded projections. Selected-class allocation stacks and exact Perfetto CPU/
timeline payloads are opt-in (`allocationClassIds` and `perfetto: true`) because
they change profiling overhead.

For application-owned attribution, register `CockpitPerformancePlugin` in the
direct `cockpit/` entrypoint or optional development module, or pass
`plugins: [...]` to one `cockpit.profile()` call. A
plugin is inert outside an explicit capture. Its sink exposes `instant`,
`begin/end`, `trace`, `counter`, and `sample`; every event uses the same
monotonic clock as VM timeline events and carries `src` plus optional isolate
and source location. Keep AOP adapters on explicit development hooks rather
than weaving production code. Per-plugin and global event limits, category
filters, sampling, payload depth/size bounds, and invalid/truncated/drop counts
are enforced before events enter the report. A failed plugin is isolated and
reported in `report.plugins`; it never fails the measured action. Compact
results keep only plugin counts and drops, while complete JSON, HTML, and
`Download timeline` retain the bounded attributable events. Example:

```dart
final class CheckoutPlugin extends CockpitPerformancePlugin {
  CheckoutPlugin() : super(id: 'checkout-aop');

  @override
  CockpitPerformancePluginRun open(CockpitPerformancePluginContext context) =>
      _CheckoutRun(context.sink);
}

final class _CheckoutRun extends CockpitPerformancePluginRun {
  _CheckoutRun(this.sink);

  final CockpitPerformanceSink sink;

  @override
  void start() {
    CheckoutHooks.onSpan = (name, startUs, endUs) {
      sink.span(name, category: 'business', startUs: startUs, endUs: endUs);
    };
  }

  @override
  void stop(CockpitPerformancePluginStats stats) {
    CheckoutHooks.onSpan = null;
  }
}

final report = await cockpit.profile(
  () => runCheckoutFlow(),
  plugins: <CockpitPerformancePlugin>[
    CheckoutPlugin(),
  ],
);
```

`open` runs for each capture and must return a new Run. Keep mutable
subscriptions, timers, counters, and buffers on the Run. For a small stateless
hook, use `CockpitPerformancePlugin.callbacks(setup: ..., cleanup: ...)`.

Plugin setup and cleanup have a bounded lifecycle timeout (two seconds by
default). The profile closes frame, memory, VM, and plugin windows immediately
after the action, before teardown/report export, so instrumentation overhead is
not attributed to the measured interaction.

The same report records the Flutter engine display refresh rate and derived
frame budget as `devtools.display`. Set `trackRebuilds: true` only when you
need DevTools-compatible `Flutter.RebuiltWidgets` frame counts and source
mappings; `devtools.rebuild` contains bounded per-frame entries, aggregate
widget totals, unresolved locations, and drops, and restores the VM extension
state afterward. It is separate from Cockpit's in-process rebuild tracker and
is never enabled by default.
VM `Logging` and `Debug` streams are captured by default as bounded metadata
(`devtools.log` and `devtools.dbg`); they retain only values already present in
the notifications, never evaluate VM objects, and expose drop counts when a
limit is reached. Set `logs: false` or `debug: false` only for a deliberately
filtered capture. Isolate snapshots also retain new/old generation heap spaces
and breakpoint counts when available.
The HTML report also has a DevTools coverage panel. It marks FrameTiming, raster
cache, VM timeline, GC, process RSS, cold-start milestones, CPU sampling,
heap/allocation profile, display refresh, widget rebuilds, and matching GPU/shader timeline signals only when
verified data is retained; unsupported platform counters remain unavailable.
Use Cockpit network evidence for HTTP/SSE/WebSocket traffic. Its
`Download timeline` button exports retained VM events as Chrome trace-compatible `traceEvents` JSON. FrameTiming
and memory values remain in the canonical report and their dedicated charts.

Validate documents before running them. During local development, run the same
validated file directly; use the indexed identity when the document is a durable
shared workspace asset or CI source.
Run IDs are durable; observe bounded events and export the finalized report bundle
only after the run reaches a terminal state.

```bash
cockpit case validate --file /absolute/case.lon
cockpit suite validate --file /absolute/suite.yaml
cockpit case run --file /absolute/case.lon --idempotency-key KEY
cockpit suite run --file /absolute/suite.yaml --idempotency-key KEY
cockpit case list --id CASE
cockpit suite list --id SUITE
cockpit case run --case-id CASE --idempotency-key KEY
cockpit suite run --suite-id SUITE --idempotency-key KEY
cockpit run list
cockpit run get --run-id RUN
cockpit run events --run-id RUN
cockpit suite report --run-id RUN --output-dir /absolute/report
cockpit artifact list --run-id RUN
cockpit artifact read --run-id RUN --artifact-id ARTIFACT --output /absolute/artifact
```

`.lon`, `.json`, `.yaml`, and `.yml` documents infer their input format, so omit
`--input-format`. Run inputs accept LON, JSON, or YAML through `--inputs` or
`--inputs-file`. `--file` and the indexed `--case-id`/`--suite-id` form are
mutually exclusive. A submission idempotency key identifies one logical run: reuse it
after transport uncertainty and never invent a new key until `run get` proves the
first submission does not exist.

Case and suite runs reuse the current Flutter project's active development session
when one exists. Pass `--session HANDLE` only to select another exact development
session, or `--target-id TARGET` for an explicitly registered black-box target; the
two selectors are mutually exclusive. Use `list --id ID` for exact lookup and add
`--path SUBSTRING` only when mirrored templates or fixtures make an ID ambiguous.

`run events` reads a bounded resumable SSE sequence until terminal or disconnect.
Resume with the last sequence or event ID; sequence numbers are monotonic. Do not
export `suite report` before terminal completion. `artifact list` returns metadata;
`artifact read` verifies the artifact and writes only to the requested output path.
Use `run list` to recover or switch to a recent durable run in the current workspace;
add `--cursor` only when the first bounded page does not contain the needed run.

Use real live capabilities only. Report unsupported capabilities as `unavailable`
or `blocked`. Distinguish product failure, authoring failure,
environment block, and infrastructure failure in reports. A passing process exit is
not sufficient: require terminal run state, expected assertions, no disqualifying
runtime/network errors, and current evidence.

## Advanced And References

Use generic operations only when no task command covers a live capability. Query one
kind instead of loading the full catalog, inspect its schema, then execute it:

```bash
cockpit op list --kind viewport.set
cockpit explain viewport.set
cockpit op run viewport.set --input '{width:800 height:600}'
```

`--scope` belongs only to `op list`; use `op list --scope supervisor` when
discovering a Supervisor operation. `explain KIND` and `op run KIND` resolve the
advertised scope automatically and do not accept `--scope`. Workspace discovery
resolves the current checkout by default. From a common ancestor with several active
Flutter projects, pass the same `--session HANDLE` to `op list`, `explain`, and
`op run`. Pass `--root-id` only when the live
descriptor declares root scope. `--session` injects the canonical runtime session only
when the schema declares it; do not put `sessionId` into input manually. Cockpit
generates an idempotency key only where the descriptor allows it. `op run` adopts the
descriptor's default timeout; add `--timeout` only to override it within the advertised
maximum.

## Public Client Control

REST is the complete external command and resource control plane. A client reads
the live catalogs and operation schema, then executes the same advertised
operations used by CLI and MCP:

```text
GET  /api/v2/server
GET  /api/v2/capabilities
GET  /api/v2/operations
GET  /api/v2/workspaces/{workspaceId}/operations
GET  /api/v2/operations/schema
POST /api/v2/operations
POST /api/v2/workspaces/{workspaceId}/operations
GET  /api/v2/runs/{runId}/events
```

`/api/v2/capabilities` is the static Supervisor-wide catalog and never starts,
attaches, or reconnects workspace workers. Use the selected workspace's operations
route when exact workspace-live operation availability is required.

Use the bearer token and loopback endpoint from Supervisor discovery, send the
negotiated API/feature headers, and use `cockpit_protocol` for strict DTO,
OpenAPI, and JSON Schema contracts. Supervisor operations use the global POST;
workspace operations use the workspace POST. The operation invocation envelope
owns workspace/root identity, idempotency, and deadline; its `input` contains
only the selected operation's advertised request fields.

SSE is the durable, resumable stream for run events. Resume with
`afterSequence` or `Last-Event-ID`; do not replace it with terminal polling.
WebSocket is only an internal Flutter Web bridge transport and is not a public
client command protocol. App network WebSocket frames may still appear in
`dev network`; that capture feature is unrelated to client control.

Checkouts/worktrees isolate sessions, ports, mutations, network data, and artifacts;
never make another checkout's session implicit. Keep Cockpit wiring in a development
entrypoint; production Flutter code must not import the bridge package.

Read [flutter.md](references/flutter.md) for bridge shells,
[upgrade.md](references/upgrade.md) for CLI and project package upgrades,
[dev.md](references/dev.md) for recovery/native boundaries,
[e2e.md](references/e2e.md) for black-box E2E,
[reporting.md](references/reporting.md) for CI,
[environments.md](references/environments.md) for unavailable platforms, and
[protocol.md](references/protocol.md) for live operation contracts.

A pass requires terminal UI/state, no disqualifying runtime/network error, and
current evidence. An unavailable required capability prevents a pass.
