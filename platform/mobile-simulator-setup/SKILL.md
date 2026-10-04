---
name: mobile-simulator-setup
description: Install and verify the toolchain needed to boot a mobile simulator/emulator and control it programmatically — Xcode + Simulator + idb for iOS (macOS only), Android Studio SDK + platform-tools (adb) for Android (works on macOS/Linux/Windows). Use when setting up a new machine for mobile QA/testing, or when idb/adb commands fail because the toolchain isn't installed yet.
---

# Mobile Simulator/Emulator Environment Setup

One-time setup so a machine can run a mobile app in a simulator/emulator
and be driven by Claude. Two independent tracks — do whichever platform(s)
the team member needs. Android works on any OS (including Windows); iOS
requires a Mac.

## iOS — macOS only

Requires Xcode (from the App Store) and its command line tools:

```bash
xcode-select -p                    # sanity check — prints a path if installed
xcode-select --install             # if the above errored
sudo xcodebuild -license accept    # accept the Xcode license non-interactively
```

Install the iOS Simulator runtime (Xcode ships a default one; add others via
Xcode → Settings → Platforms, or):

```bash
xcodebuild -downloadPlatform iOS
```

Boot and verify a simulator:

```bash
open -a Simulator
xcrun simctl list devices          # confirm at least one device shows "Booted"
```

If nothing is booted:

```bash
DEVICE=$(xcrun simctl list devices available | grep -m1 'iPhone' | grep -oE '[A-F0-9-]{36}')
xcrun simctl boot "$DEVICE"
open -a Simulator
```

Install `idb` (Facebook's iOS Development Bridge — this is what gives
programmatic tap/swipe/type/screenshot control):

```bash
brew tap facebook/fb
brew install idb-companion
pip3 install fb-idb
```

Verify:

```bash
idb --version
idb list-targets       # should list the booted simulator's UDID, state "Booted"
```

If `idb list-targets` doesn't show the booted device, restart its daemon:
`killall idb_companion` (it auto-restarts on the next `idb` call).

### Getting the app under test onto the simulator

- Have a `.app` bundle already (e.g. a CI build artifact): `xcrun simctl
  install booted /path/to/YourApp.app`
- Only have source: build it first with whatever that project uses
  (`flutter build ios --simulator`, `xcodebuild -scheme ... -sdk
  iphonesimulator`, etc.) — this skill doesn't cover app builds, only the
  simulator + control tooling.
- Launch: `xcrun simctl launch booted <bundle-id>` (bundle id is in the
  app's `Info.plist`, or `unzip -p YourApp.app/Info.plist | plutil -p -`).

## Android — any OS (macOS / Linux / Windows)

Requires Android Studio (installs the SDK, `platform-tools`, and the
`emulator` binary by default) — or a standalone `cmdline-tools` install if
a full IDE isn't wanted.

Put `platform-tools`, `emulator`, and `cmdline-tools/latest/bin` (the last
one holds `avdmanager`/`sdkmanager`/`android` — see below) on `PATH`:

| OS | Typical SDK location |
|---|---|
| macOS | `~/Library/Android/sdk` |
| Linux | `~/Android/Sdk` |
| Windows | `%LOCALAPPDATA%\Android\Sdk` |

Verify:

```bash
adb version
emulator -version
```

### `avdmanager`/`sdkmanager` (cmdline-tools) — resolve the current version, never hardcode one

A machine may only have the **legacy, deprecated `tools` package**
(`Sdk\tools\bin\avdmanager`, from an old Android Studio install) or no
cmdline-tools at all. Two symptoms mean a current `cmdline-tools` package
is needed instead of the one on disk:

- `avdmanager`/`sdkmanager` isn't found anywhere under the SDK root.
- It exists but crashes with a `SAXParseException` / `cvc-type` XML error
  while "Loading local repository" — the legacy tool's schema can't parse
  a newer installed package (e.g. an extension-level platform like
  `android-33-ext4`). Don't work around this by touching the installed
  package that triggered it; install a current `cmdline-tools` instead.

**Never hardcode a specific cmdline-tools build number or download URL**
(e.g. a `commandlinetools-<os>-<build>_latest.zip` filename remembered
from training data or a past session) — Google rotates that build number
regularly, so a pinned filename silently installs an older version than
what's actually current, which is exactly the kind of stale-value-passed-
off-as-current thing `.claude/rules/no-fallbacks.md` warns about. Resolve
the current version at the time you need it:

1. **If any `sdkmanager` already runs** (even a legacy one — the crash
   above only hits *local* package parsing, so a fresh SDK with no
   extension-level platforms installed yet may run fine): just self-update
   via the officially supported path —
   ```bash
   sdkmanager "cmdline-tools;latest"
   ```
   This resolves and downloads the true current version from Google's own
   repository manifest; you never construct a URL by hand. **This download
   goes over the same network as everything else** — if it stalls or dies
   partway through, that's the identical sandboxed-network problem covered
   in "Downloading large SDK files" below, not a different failure. Don't
   burn retries on it specifically; fall through to option 2's manual
   download+handoff (it works as a recovery here too, not just for a true
   first-time bootstrap — a human-downloaded zip dropped into
   `cmdline-tools/latest` is indistinguishable from what self-update would
   have produced).
2. **If no `sdkmanager` runs at all yet (bootstrap case)**: ask the human
   to download the "Command line tools only" package for their OS
   themselves from
   https://developer.android.com/studio#command-line-tools-only (that page
   always serves the current build — don't guess/construct the
   `dl.google.com/.../commandlinetools-*.zip` URL yourself). Once you have
   the file, extract its inner `cmdline-tools/` folder to
   `Sdk\cmdline-tools\latest` (the folder name under `cmdline-tools\` must
   literally be `latest`, not a version number, for the `cmdline-tools;latest`
   package id to resolve), then immediately run step 1's self-update to
   jump from whatever build you just bootstrapped to the true current one.

**Java version**: current cmdline-tools builds require **Java 17+**
(`UnsupportedClassVersionError ... class file version 61.0` means the
active `java` is older than 17). Look for an existing JDK 17+ (Zulu,
Temurin, Android Studio's bundled `jbr`, etc.) before installing a new
one, and set `JAVA_HOME` to it for the `avdmanager`/`sdkmanager`
invocation rather than downgrading the cmdline-tools version to match an
old JDK.

**Recent cmdline-tools (~rev 23+) rebrands the CLI.** `sdkmanager`/
`avdmanager` still exist as thin wrapper scripts and still work, but print
a deprecation banner pointing at a new unified `android` binary (`android
sdk ...`, `android emulator create/start/stop/list/remove`). Prefer the
classic `avdmanager create avd -n <name> -k "system-images;..."` for AVD
creation (see below) over `android emulator create <profile>` — the new
`create <profile>` command auto-installs/updates dependencies it thinks it
needs (it tried to fetch a newer ~440MB `emulator` package on a fresh
create in testing) and will fail outright if that opportunistic download
hits the same unreliable-network problems described below. `avdmanager`
never does this — it only ever uses packages already on disk.

### Downloading large SDK files on an unreliable/sandboxed network

Sandboxed dev environments frequently have slow or flaky outbound
bandwidth. Observed failure modes when fetching SDK archives (cmdline-tools
zip, system-image zip — both 100MB-2GB+) directly via `Invoke-WebRequest`/
`curl` from inside the sandbox:

- A backgrounded download silently stops early but the file still exists
  on disk (looked "done" at 6MB when the real file is 150MB+).
- A long transfer dies mid-stream with "connection forcibly closed by the
  remote host" partway through (e.g. died at 87MB of 153MB).

**Always verify actual downloaded size against the expected size before
extracting/installing** — never assume a download that "finished running"
actually finished transferring:

```bash
curl -sI "$URL" | grep -i content-length   # or x-identity-content-length
```

If a download is large (rule of thumb: >50MB) or a first automated attempt
already failed/truncated, don't keep retrying the same automated path —
hand the human the exact resolved URL (see the next section for how to
resolve one without guessing) and ask them to download it themselves, then
continue once they give you the saved path. This is faster in practice
than repeated sandboxed retries and avoids installing a truncated/corrupt
archive.

### Resolving "the latest Android version" (system image) without guessing

Same no-hardcoded-version principle as cmdline-tools above, applied to
platform/system-image packages. Google's SDK repository is machine-
readable — read it instead of remembering a version:

```bash
curl -s https://dl.google.com/android/repository/repository2-3.xml -o repo.xml       # platforms, build-tools, cmdline-tools, emulator, ...
curl -s https://dl.google.com/android/repository/sys-img/google_apis/sys-img2-3.xml -o sysimg.xml   # system images for the google_apis tag (also try google_apis_playstore)
```

Each `<remotePackage>` has a `<channelRef ref="channel-N"/>` — the
manifest's own `<channel>` list maps these (`channel-0` = **stable**,
`channel-1` = beta, `channel-2` = dev, `channel-3` = canary). Filter to
`channel-0` for "the latest Android version" — the highest `api-level`
system image in the `google_apis` tag with a `channel-0` ref, matching
your host's CPU (`x86_64` on an Intel/AMD Windows/Linux/Intel-Mac host;
`arm64-v8a` on Apple Silicon — 32-bit `x86`/`armeabi` images have been
discontinued for recent API levels). A higher API level can exist only on
`channel-2`/`dev` (preview) — skip those unless a preview build was
specifically requested. Take the archive's `<url>` (relative to the
manifest's own base — `.../repository/` for `repository2-3.xml`,
`.../repository/sys-img/<tag>/` for a sys-img manifest) and its `<size>`
to verify the download per the section above.

### Installing a system image manually (when you already have the zip)

Needed either because you resolved+handed off a large download per above,
or because `sdkmanager`'s own install hit the same network issue.

1. **Extract with `unzip` (Info-ZIP), not `Expand-Archive`/
   `System.IO.Compression.ZipFile`.** A system image's `system.img` entry
   can be several GB, and .NET's `System.IO.Compression.ZipFile` (which
   `Expand-Archive` uses under the hood) throws `"A local file header is
   corrupt"` on such large individual entries even from a perfectly valid
   zip — it's a known limitation, not a sign the download is bad. Git
   Bash ships `unzip`; use it:
   ```bash
   mkdir -p "$SDK/system-images/android-<level>/<tag>/<abi>"
   cd "$SDK/system-images/android-<level>/<tag>" && unzip -q /path/to/downloaded.zip
   ```
   (the zip's own top-level folder is already named `<abi>`, e.g. `x86_64/`).
2. **Generate the missing `package.xml`.** Google's raw system-image
   archives ship a `source.properties` but *not* a `package.xml` — that
   file is normally synthesized locally by `sdkmanager` during a real
   install, describing the package to the legacy `LocalRepoLoader` that
   `avdmanager` still uses internally. Without it, `avdmanager create avd`
   fails with `Error: Package path is not valid` and won't even list the
   package as an option, **even though** `sdkmanager --list_installed`
   correctly shows it as installed (the two tools use different package
   indexes — don't take `list_installed` success as proof `avdmanager`
   will see it too).

   Build it from the sys-img manifest you already fetched to resolve the
   version (previous section) — this works even on a brand-new machine
   with zero pre-existing packages, so don't rely on finding an existing
   `package.xml` to copy from:

   a. In that manifest, re-locate the exact `<remotePackage
      path="system-images;...">...</remotePackage>` block for the package
      you downloaded, and note its `<uses-license ref="X"/>` (`X` is
      `android-sdk-license` for a stable/`channel-0` package,
      `android-sdk-preview-license` for a dev/preview one).
   b. Extract that same manifest's `<license id="X" type="text">...</license>`
      block whose `id` matches — verbatim, don't shorten it:
      ```bash
      awk '/<license id="X"/{f=1} f{print} f&&/<\/license>/{exit}' sysimg.xml
      ```
   c. Assemble `package.xml` as: the license block from (b), plus the
      `remotePackage` block from (a) renamed to `localPackage` with its
      `<archives>`, `<dependencies>`, and `<channelRef>` children removed
      (local packages don't carry those — everything else, including
      `<type-details>`, `<revision>`, and `<display-name>`, is copied
      verbatim), wrapped in a minimal repository root — **critically, the
      wrapper must declare the exact same namespace prefix the source
      manifest used for the sys-img schema, or the copied
      `xsi:type="<prefix>:sysImgDetailsType"` attribute won't resolve.**
      XML prefixes aren't portable across documents by themselves — check
      the very first line of the manifest you downloaded for its root
      element's own declaration (currently
      `<sys-img:sdk-sys-img xmlns:sys-img="http://schemas.android.com/sdk/android/repo/sys-img2/03" ...>`,
      i.e. prefix `sys-img`, schema version `03` — but don't hardcode
      either; reuse whatever this specific file's header actually says):
      ```xml
      <?xml version="1.0" encoding="UTF-8" standalone="yes"?><ns2:repository xmlns:ns2="http://schemas.android.com/repository/android/common/02" xmlns:sys-img="http://schemas.android.com/sdk/android/repo/sys-img2/03" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <license id="X" type="text">...text from (b)...</license>
      <localPackage path="system-images;android-<level>;<tag>;<abi>" obsolete="false">
        <type-details xsi:type="sys-img:sysImgDetailsType">...verbatim from (a)...</type-details>
        <revision>...verbatim from (a)...</revision>
        <display-name>...verbatim from (a)...</display-name>
        <uses-license ref="X"/>
      </localPackage>
      </ns2:repository>
      ```
      (the outer `<ns2:repository>` root/namespace itself is fixed —
      that's the generic local-package-descriptor schema every installed
      SDK package uses, unrelated to which remote manifest you sourced
      the system-image details from).
   d. Save it as
      `<sdk>/system-images/android-<level>/<tag>/<abi>/package.xml`.
3. Confirm it worked by just running `create avd` (next section) — if the
   package still isn't recognized, `avdmanager` fails with `Error: Package
   path is not valid. Valid system image paths are: ...` and lists what it
   *does* see (there is no separate "list system images" command —
   `avdmanager list target` only lists platforms, never system images, so
   don't use it to check this).

### Create and boot an emulator (AVD)

Or use Android Studio's Device Manager GUI, which does the same thing.
**On Windows, pipe the "no" (skip custom hardware profile) answer via
bash's `echo`, not PowerShell's** — `"no" | avdmanager.bat ...` in
PowerShell prepends a BOM byte that `avdmanager` rejects as `"no is not a
valid reply"`; Git Bash's `echo` doesn't have this problem:

```bash
echo no | avdmanager create avd -n test-device -k "system-images;android-34;google_apis;x86_64" --force
emulator -avd test-device
```

**Two log lines are benign, don't treat them as boot failure:**
- `ERROR | Unable to connect to adb daemon on port: 5037` right after
  launch — the emulator raced adb's own server start. Just run `adb
  start-server` (or any `adb` command, which auto-starts it) and continue
  polling `adb devices`; don't kill/relaunch the emulator over this.
- `WARNING | Please update the emulator to one that supports the
  feature(s): ...` (e.g. `AndroidVirtualizationFramework`,
  `SupportPixelFold`) — appears when the installed system image is newer
  than the bundled `emulator` binary. It still boots and runs fine; this
  only matters if you specifically need one of the named features, in
  which case update the `emulator` package too (`sdkmanager "emulator"` —
  another large download, so apply the same handling as above).

Verify the device is visible to adb:

```bash
adb devices     # should list e.g. "emulator-5554   device"
```

### Getting the app under test onto the emulator

- **Only have an APK, no source** (the common case for testing a
  teammate's build or a release candidate): this works fine —
  ```bash
  adb install -r /path/to/app.apk
  ```
  To find the package name and launch activity of an APK you didn't build
  (needs Android SDK build-tools' `aapt` on PATH):
  ```bash
  aapt dump badging /path/to/app.apk | grep -E "package:|launchable-activity:"
  ```
  Then launch it:
  ```bash
  adb shell am start -n <package>/<launchable-activity>
  ```
- **Have source** (e.g. Flutter): the project's own run command
  (`flutter run`) builds, installs, and launches in one step — no separate
  `adb install` needed unless you specifically want to test a pre-built APK
  instead of a fresh build.

## Common gotchas

- **iOS has no Windows/Linux path.** `idb-companion` wraps Apple's own
  Simulator/XCTest frameworks — there is no workaround on a non-Mac
  machine. Android is the cross-platform option.
- **Multiple booted devices/emulators** make target selection ambiguous —
  always pass `--udid <UDID>` (idb) or `-s <serial>` (adb) explicitly once
  more than one could be running.
- **`adb devices` shows nothing**: the emulator is still booting (first
  boot can take a minute+) — poll `adb devices` until the state changes
  from blank to `device`, not `offline`.
- **Don't hardcode a cmdline-tools/system-image build, version, or URL.**
  See the dedicated sections above — always resolve from Google's own
  repository manifest (or the official download page as a bootstrap
  fallback), never a remembered filename/build number.
- **Large downloads on a sandboxed network silently truncate or drop
  mid-transfer.** Verify byte size against the manifest/HTTP
  `Content-Length` before extracting; for anything over ~50MB, or after
  one failed automated attempt, just hand the human the resolved URL and
  ask them to download it instead of retrying automated fetches.
- **`Expand-Archive`/`System.IO.Compression.ZipFile` corrupts on multi-GB
  zip entries** (e.g. a system image's `system.img`) — use `unzip`
  (Info-ZIP, ships with Git Bash) instead.
- **A manually-placed system image needs a hand-written `package.xml`** —
  `avdmanager` won't recognize it as a valid `-k` target without one, even
  though `sdkmanager --list_installed` shows it fine. See the dedicated
  section above for the template approach.
- **PowerShell's `"no" | avdmanager...` inserts a BOM** that breaks the
  "custom hardware profile?" prompt — pipe from bash's `echo` instead.
- **Windows PATH**: `adb`/`emulator` not found usually means
  `platform-tools`/`tools`/`emulator` under the SDK root were never added
  to `PATH` — check `%LOCALAPPDATA%\Android\Sdk` exists and add its
  `platform-tools` and `emulator` subfolders.

## Load this skill when

- A machine doesn't yet have the iOS (Xcode + idb) or Android (SDK + adb)
  toolchain installed or verified for simulator/emulator control.
- `idb` or `adb` commands are failing and the cause looks like a missing
  install rather than a usage error.
- Getting a teammate's APK or `.app` build onto a simulator/emulator for
  the first time on a given machine.
