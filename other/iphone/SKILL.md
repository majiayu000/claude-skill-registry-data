---
name: iphone
description: Use to build the app for iPhone or the iPhone simulator, publish it to TestFlight, or put a development build on the owner's phone, from Linux over ssh to the Mac, without the owner doing anything.
---

Everything iPhone happens on the Mac: `ssh mac 'zsh -lc "nice -n 19 taskpolicy -d throttle <command>"'` (a login shell, so Homebrew, Rust
and Xcode's tools are on its PATH). The Mac is the owner's own laptop, in use, and shared by every agent, so what you
run there runs under `nice -n 19 taskpolicy -d throttle` (lowest CPU priority, throttled disk),
which its children inherit, and with `CARGO_BUILD_JOBS=4`, half its cores. That is how the owner's own apps come
first: on 18 Nov, with six busy programs of his standing in, a cargo build at normal priority took 62% of their work,
one under `nice -n 19` and a throttled disk 52%, and one under `taskpolicy -b` 37%, which is far slower for you (an
incremental `one` build took 12 minutes instead of 1 or 2), so don't use `taskpolicy -b`. Its load average isn't a reason to wait: the owner's
simulators and Chrome had it above 200 with CPU to spare, so don't add to what uses its memory: shut down and delete a
simulator you booted, and remove your `~/scratch/` checkout, when you're done.

Work in a checkout of your own there under `~/scratch/`, at your commit. Clone it whole, not `--depth 1`: the app's
version and build number are `tooling/version`'s count of commits, so a shallow clone builds an app numbered 1.

What's built is the One App, plain, and a network's app is that build finished for it (`clients/app/README.md`):
its settings, in its repo's `app/` as its main has it on the remote (`git -C <the network's repo> fetch origin main &&
git -C <it> archive origin/main app`), never go in this repo, its GitHub runs or a checkout's files, which may be
behind. `tooling/testflight` is how a build is finished; this is what it and the README don't say.

## What exists

- No Apple account is signed in to Xcode, so its automatic signing fails: `cargo tauri ios build`'s own signing and
  export (`errSecInternalComponent`), and an export with `signingStyle` `automatic` even with the API key, which signs
  only with Apple's cloud-managed certificates, which App Store Connect refuses this key (403). An export with
  `signingStyle` `manual`, the certificate and each target's profile by name, works (`tooling/testflight`).
- The team is X96JC3HCV7, the owner's own (Individual), which signs the One App (`app.theone.client`) and The PTC
  App. Its Apple Development identity, for a development build on the owner's phone, is in a keychain of its own on
  the Mac, `ptc-build`, not the login keychain, whose password is the 1Password item "Mac build keychain (ptc-build)"
  in the `ptc-nosudo` vault, and on the Mac in `~/.config/ptc/build-keychain-pw`. Its Apple Distribution identity,
  for TestFlight, and its Developer ID Application identity, which `tooling/release` signs a Mac's server and app
  with, are each a .p12 in 1Password ("Apple Distribution identity", "Developer ID Application identity", each with
  its "... password" item, in `ptc-nosudo`), the Developer ID one in the repo's GitHub secrets too
  (`DEVELOPER_ID_P12`, `DEVELOPER_ID_P12_PASSWORD`), and on no Mac. The public repo's runs sign nothing for the App
  Store: `tooling/testflight` signs on Linux.
- The team's App Store Connect API key (Admin, `R49QVKSHMK`; its item is in Agent Memory) makes App IDs
  (`/v1/bundleIds`, `/v1/bundleIdCapabilities`) and profiles (`POST /v1/profiles` with the App ID and the team's
  certificate: `IOS_APP_DEVELOPMENT`, its `DEVELOPMENT` certificate and the phone from `/v1/devices`, or
  `IOS_APP_STORE` and its `DISTRIBUTION` one), whose `profileContent` is the profile. Profiles are kept on the Mac in
  `~/Library/Developer/Xcode/UserData/Provisioning Profiles/`, named by UUID (`security cms -D -i <file>` shows each
  one's `Name`, App ID and entitlements): "The One App Development", "The One App App Store" and "The One App
  Notifications App Store". A profile is made again when its App ID changes, which leaves it invalid. The wildcard
  profile ("iOS Team Provisioning Profile: *") carries no push, so a build signed with it isn't woken by
  notifications.
- That key can't make an App Store Connect app, an App Group, or put a group on an App ID: the API has nothing for
  them, and Xcode's own developer services, which `xcodebuild -allowProvisioningUpdates -authenticationKeyPath ...`
  uses, refuse it (401). The owner does them on the website. The One App's group (`group.app.theone.client`) is on
  both its App IDs and in all four of their profiles, so its client is kept in the group and its notification
  extension reads its key there. A profile made before a group is ticked has none, and is made again once it is. Its
  widget extension has an App ID of its own, `<identifier>.widgets`, which needs the same group and an App Store
  profile made after, or `tooling/testflight` leaves the widgets out.
- A development profile's `aps-environment` is `development` and an App Store one's `production`. The network's edge
  sends to one of APNs's two, the sandbox with `APNS_SANDBOX=1` (`apps/notifications/edge/README.md`), so a phone is
  woken only where its build matches it.
- The phone is paired with the Mac: `xcrun devicectl list devices` names it.

## Building and signing

1. Turn signing off in your checkout: `CODE_SIGNING_ALLOWED: NO` in `gen/apple/project.yml`'s settings for both
   targets, `app_iOS` and `Notifications`, then `gen/apple/generate`.
   An `.xcconfig` doesn't do it: `cargo tauri ios build` takes none. Then `cargo tauri ios build --archive-only
   --no-sign`, and the app is `gen/apple/build/app_iOS.xcarchive/Products/Applications/<name>.app`. Or build for the
   simulator with `--target aarch64-sim --debug`, which needs no signing. Finish it for the network as
   `tooling/testflight` does: its identifier and link schemes in each target's `Info.plist` (`AppGroup` too), and its
   address in the app's `network` file.
2. Put each target's profile in it as `embedded.mobileprovision`, and sign it with that profile's own entitlements
   less `keychain-access-groups` (a wildcard, which a signature can't hold), which keeps its
   `com.apple.security.application-groups`, `group.app.theone.client`: `security cms -D -i <profile> > p.plist`,
   `plutil -extract Entitlements xml1 -o e.plist p.plist`, then `/usr/libexec/PlistBuddy -c "Delete :<key>" e.plist`
   (`plutil` reads the dots in `com.apple...` as a path). A profile's `com.apple.developer.associated-domains` is `*`,
   which a signature can't hold either: set it to the network's own (`webcredentials:` and `applinks:` its domain), or
   its web view offers no passkeys. Sign
   `PlugIns/Notifications.appex` first, then the app; with no profile for the extension, remove `PlugIns/` instead.
3. Unlock the keychain and `codesign` in the same ssh connection: `security -i` reads `unlock-keychain -p ...` on
   stdin, then `codesign --force --keychain <it> --sign "Apple Development" --entitlements <file> <app>`. The
   password goes on stdin, never in a command line, where `ps` and logs see it. The key's partition list must
   already allow `codesign` (`security set-key-partition-list -S apple-tool:,apple:`); if it doesn't, a dialog
   appears on the owner's screen. `security lock-keychain <it>` at the end of that same connection.

For the simulator, or to try a change on the phone before it's released, sign with the development profile and
`xcrun devicectl device install app --device <id> <app>`, which installs over the app there, keeping its data, locked
phone or not. It replaces TestFlight's build, so the phone takes no more updates until it's installed from TestFlight
again. `xcrun devicectl device process launch --device <id> <the app's identifier>` opens it, which a locked phone
refuses (`Locked`). `one builds` shows the phone's new build only once the app has opened.

## TestFlight

The owner's phone takes the One App from TestFlight, which updates it by itself; its Update Required's Update opens
TestFlight. `tooling/testflight <the network's repo>` publishes main, as `tooling/release client` does whenever the
phone's native code changed: GitHub's macOS runner builds it plain (`.github/workflows/iphone.yml`), and the script
finishes it on Linux, signs it with rcodesign, the App Store profiles and Apple Distribution, and uploads it with the
API key (App Store Connect's `buildUploads`), with no Mac. Apple processes it by itself in a few minutes, which
nothing waits for: then the internal group "The One App" has the build (`hasAccessToAllBuilds`) and its testers take
it automatically. App Store Connect's `processingState` says where it is, and Apple emails if it rejects it.

A network's own people (the PTC team, in its external group "PTC staff") get a build only at a milestone, through the
group's public link, which the network's download page offers: `tooling/testflight --milestone <the network's repo>`
(Andre, 23 Nov). It takes the newest build there, adds it to the external group, submits it to Apple's beta review,
which takes a day or so, turns on the group's public link and sets it as the download page's. A release never does it:
each build's review is its own.

## Memory

An iPhone counts the app's GPU memory as its own (footprint's "IOAccelerator (graphics)" and "IOSurface"); the
simulator doesn't. There the GPU's work runs in the Mac's `SimMetalHost` and `SimRenderServer`, shared with every
other app on it, and the app's footprint (`footprint <pid>` on the Mac) is only its CPU side: about 105 MB with apps
open on 20 Nov, flat over many opens. So a phone's memory over budget that's GPU memory doesn't show on the simulator,
and Metal's `currentAllocatedSize` and the graphics ledger both read 0 there. Its CPU side (heap, JS, code) is the
same as a phone's, so the simulator is where to find a CPU-side leak. What a phone holds, part by part, is in its
Telemetry (`one.client.memory.*`, `clients/app/src/memory.rs`).

On the simulator, `simctl launch --console` shows nothing the app says (`eprintln!`): read what it reports from the
Telemetry of the network it's in. Its client's home is its App Group's container, as Xcode signs a simulator build
with the group (`xcrun simctl` lists none: find the folder under the device's `data/Containers/Shared/AppGroup/` whose
metadata names `group.app.theone.client`), so that's where its `network` file goes. A network on Linux reaches it
through `ssh -R <port>:localhost:<port>` to the runner, and `axe` drives it (the App Library's search opens an app).

## Mistakes already made

- Signing through anything running in the owner's logged-in session (Xcode, a GUI `osascript`, a Terminal tab):
  each signature put a password dialog on his screen. Only ssh, and only a keychain unlocked in that connection.
- Leaving signing to `cargo tauri ios build` or Xcode's automatic signing, which fail with no account signed in.
  `cargo tauri ios build` with the API key (`APPLE_API_KEY`) signs only the app's entitlements before its export, so
  the notification extension would lose its App Group.
- Signing with the wildcard profile: the phone got no APNs token and said it isn't woken by notifications.
- Signing a simulator build ad hoc with entitlements that name the team, such as associated domains
  (`codesign -s - --entitlements`): the simulator killed it as it opened (`Code Signature Invalid`). Built for the
  simulator with signing left on in `project.yml`, Xcode signs it locally, with no account, and puts its
  entitlements in the binary (`__entitlements`), where the simulator reads them.
