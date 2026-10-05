---
name: local-archive-export-upload
description: 'Use when a build must reach TestFlight without Xcode Cloud (quota, outage, CI not wired yet), or when a local `xcodebuild archive` / `-exportArchive -exportOptionsPlist` / `xcrun altool --upload-package` command fails — `ExportOptions.plist` keys (`method`, `destination`, `teamID`, `manageAppVersionAndBuildNumber`), `-authenticationKeyPath` vs `-allowProvisioningUpdates`, `CFBundleVersion` colliding with Xcode Cloud''s counter. Temporary fallback for xcode-cloud-single-track-ci; does NOT cover ASC operations after upload → asc-api-automation, nor `notarytool` notarization → apple-skills:guide-macos-spm-packaging.'
allowed-tools: Bash(xcodebuild archive *)
---

# Local Archive, Export, Upload

The manual escape hatch for getting a build to TestFlight when Xcode Cloud's
**Main CI** workflow (→ `xcode-cloud-single-track-ci`) can't run — quota
exhausted, an outage, or CI not wired up yet. Same three Apple CLIs Xcode
Cloud uses under the hood — `xcodebuild archive`, `-exportArchive`, upload —
driven by hand instead of Apple's managed runner.

## When to invoke

- Xcode Cloud can't run but a build must reach internal TestFlight today.
- Writing or debugging a local archive/export/upload script or one-off command.
- Diagnosing an `ExportOptions.plist` / signing / build-number failure.
- Asked "how do I ship a build without Xcode Cloud" or "what does
  `-exportOptionsPlist` need".

## Scope

Owns: the local three-step pipeline (archive → export → upload) and its
signing/export-key semantics. Does NOT own:

- ASC operations once the build exists (TestFlight groups, what's-new,
  submission) → `asc-api-automation`.
- What has to be true for the build to *pass* review →
  `app-store-review-rejections`.
- `.p8` / API-key storage → `build-time-secret-injection` +
  `apple-public-repo-security`.
- Restoring Xcode Cloud once quota returns — this is a **temporary
  substitute**, not a parallel permanent CI track.

## Pipeline

| Step | Command | Notes |
|---|---|---|
| 1. Archive | `xcodebuild archive -scheme <Scheme> -destination 'generic/platform=iOS' -archivePath build/App.xcarchive` | `-destination` picks the platform; a `generic/platform=...` destination (not a specific simulator/device) is what produces an archivable, distributable build. |
| 2. Export | `xcodebuild -exportArchive -archivePath build/App.xcarchive -exportPath build/export -exportOptionsPlist ExportOptions.plist` | Requires `-archivePath` + `-exportOptionsPlist`; `-exportPath` only needed when the plist's `destination` is `export` (see below). |
| 3. Upload | `xcrun altool --upload-package build/export/App.ipa --api-key <keyID> --api-issuer <issuerID> --wait` | `--api-key` / `--api-issuer` are the spelling `altool --help`'s own example uses; add `--wait` to block until Apple finishes processing instead of polling separately. Or fold into step 2 — see "One-step vs two-step" below. |

## Signing: two non-interactive paths

`xcodebuild -help` documents two credential sources for `-allowProvisioningUpdates`:
an account added in Xcode's Accounts settings, or an App Store Connect authentication
key passed via the `-authenticationKey*` trio. Both paths below therefore pass the flag
(needed on a script/cron path, not just CI):

| Path | Flags | Use when |
|---|---|---|
| Automatic signing via your Xcode account | `-allowProvisioningUpdates` (+ `-allowProvisioningDeviceRegistration` if a new device needs registering) | Run on your own dev Mac with an account added in Xcode's Accounts settings; xcodebuild creates/updates profiles and certs as needed. |
| API-key signing, no Apple ID session | `-allowProvisioningUpdates -authenticationKeyPath <p8> -authenticationKeyID <id> -authenticationKeyIssuerID <issuer>` | Unattended/scripted runs — reuse the same ASC API key from `asc-api-automation` / `build-time-secret-injection`, no Xcode account needed. |

## ExportOptions.plist: the common shape

The full key set is printed by `xcodebuild -help` under "Available keys for
-exportOptionsPlist" (18 keys on Xcode 26.5, covering thinning, manifests, on-demand
resources). For a plain "ship to TestFlight" export, six keys are load-bearing
(cross-checked against the key list in `xcodebuild -help`):

```xml
<key>destination</key>          <string>export</string>          <!-- or "upload" -->
<key>method</key>               <string>app-store-connect</string>
<key>manageAppVersionAndBuildNumber</key> <false/>
<key>signingStyle</key>         <string>automatic</string>
<key>teamID</key>               <string>ABCDE12345</string>
<key>uploadSymbols</key>        <true/>
```

- **`method: app-store-connect`** — the current name; `app-store` still works
  but Xcode 26.5's `xcodebuild -help` already marks it "deprecated: use
  app-store-connect" (the exact Xcode version the rename landed in is
  unconfirmed).
- **`manageAppVersionAndBuildNumber: false`** — defaults to `YES` (Xcode bumps
  the build number for you on export); set `false` when your own tooling
  controls `CFBundleVersion` — see build-number coordination below.
- **`teamID`** — omit to inherit the archive's signing team; set explicitly
  when a machine/CI identity could resolve ambiguously.

### One-step vs two-step upload — pick two-step on purpose

| `destination` | Artifact | Gate before upload | Use when |
|---|---|---|---|
| `export` | `.ipa`/`.pkg` written to `-exportPath` | Your own `--dry-run`/`--i-am-sure`-style flag on a separate upload command | Default |
| `upload` | None — xcodebuild uploads directly to Apple, no local artifact, no separate `altool` call | None — the network push happens the instant `-exportArchive` runs | Deliberate one-shot only |

Prefer `destination: export` + a separate, deliberately-gated upload command
so archive/export stay safe to run freely and only upload needs a human's
explicit go-ahead.

## Upload tool

`xcrun altool --help` (Xcode 26.5) lists `--upload-package <file>` first among
App-Upload commands and uses it in its own canonical example; the older
`--upload-app -f <file>` still works but isn't the tool's own example anymore.
altool searches fixed directories for `AuthKey_<keyID>.p8` (`./private_keys`,
`~/private_keys`, `~/.private_keys`, `~/.appstoreconnect/private_keys`, or
`$API_PRIVATE_KEYS_DIR`) — stage a per-run symlink into one of these if your
key lives in a gitignored `secrets/` dir, rather than moving the real file.

**`notarytool`** is not this path — it handles Developer-ID notarization
(outside-the-App-Store distribution), unrelated to TestFlight/App Store
uploads. The ASC API's Build Uploads path also works (see
`references/official-docs.md`), but this skill still defaults to `altool`.
For the other upload paths (Xcode Cloud, Xcode Organizer, Transporter), read
`references/official-docs.md`.

## Build-number coordination with Xcode Cloud

Per `xcode-cloud-single-track-ci`, Xcode Cloud assigns its own sequential
`CI_BUILD_NUMBER` per build, independent of whatever's in the repo. A local
build needs a `CFBundleVersion` that will never collide with — or fall below —
that counter:

- Use a high-resolution timestamp (`YYYYMMDDHHmm`) rather than a small
  hand-incremented integer — it can't collide with Xcode Cloud's small
  sequential counter, and TestFlight rejects a duplicate `CFBundleVersion` for
  the same `CFBundleShortVersionString`.
- macOS additionally requires build numbers to strictly increase *across*
  versions — if a local timestamp-based number ends up higher than Xcode
  Cloud's next assigned number, fix it once on the ASC side (Xcode Cloud →
  Settings → Build Number → Edit), the same fix `xcode-cloud-single-track-ci`
  documents for its "existing Mac app" exception.
- Set `manageAppVersionAndBuildNumber: false` (above) so Xcode's export-time
  bump doesn't fight your chosen number.

## Rationale

Every flag and key here is verifiable straight from Apple's own CLI (`man
xcodebuild`, `xcodebuild -help`, `xcrun altool --help`) — no fastlane, no
third-party packaging tool, consistent with this catalog's no-Homebrew /
Apple-native-first baseline (`asc-api-automation` makes the same call for ASC
REST automation). Provenance for each claim (doc-verified vs practice-observed)
is in `references/evidence.md`.

## Deviation considerations

- **Xcode Cloud is back / never was the bottleneck** — retire the local path;
  don't run it as a second permanent track (`xcode-cloud-single-track-ci`'s
  single-track rule).
- **Frequent local ships** — the "temporary substitute" framing breaks down;
  invest in restoring/expanding Xcode Cloud capacity instead of hardening
  this manual path further.

## Common Mistakes

1. Pre-`touch`ing `ExportOptions.plist` before writing it with `PlistBuddy`.
2. Using `destination: upload` as the default — loses the archive-only dry run.
3. Leaving `method: app-store` (deprecated form) in an old plist.
4. Hand-incrementing a small `CFBundleVersion` locally — collides with Xcode
   Cloud's own counter.
5. Reaching for `xcrun notarytool` for a TestFlight upload — it's for
   Developer-ID notarization, a different distribution path entirely.
6. Forgetting `ITSAppUsesNonExemptEncryption` on a new app — the build is
   marked Missing Compliance until the export-compliance questions are answered
   in ASC or via `PATCH /v1/builds/{id}` (`usesNonExemptEncryption`).

## Review Checklist

- [ ] Archive uses a `generic/platform=...` destination, not a specific
      simulator/device.
- [ ] Export uses `method: app-store-connect` (not the deprecated `app-store`).
- [ ] Signing passes `-allowProvisioningUpdates` on every path, with a
      deliberate credential source: the Xcode Accounts login (your dev Mac) or
      the `-authenticationKeyPath` trio (unattended).
- [ ] `destination: export` + a separate gated upload step, unless a one-step
      `upload` is a deliberate choice.
- [ ] `CFBundleVersion` source can't collide with Xcode Cloud's `CI_BUILD_NUMBER`.
- [ ] `ITSAppUsesNonExemptEncryption` set in Info.plist (or export-compliance
      is otherwise answered).
- [ ] `.p8` staged only via a per-run symlink into an altool-searched
      directory, never committed or left behind after the run.

## Related skills

- `xcode-cloud-single-track-ci` — the primary CI path this substitutes for;
  restore it once quota/outage clears.
- `asc-api-automation` — TestFlight/App Store operations once the build lands in ASC.
- `app-store-review-rejections` — its export-compliance row (an ASC upload
  step, not a Guideline number) and what has to be true for review to pass.
- `apple-skills:guide-macos-spm-packaging` (aggregated external) — Developer-ID
  signing / `notarytool` notarization for outside-the-App-Store distribution.
- `build-time-secret-injection` / `apple-public-repo-security` — where the
  `.p8` and its issuer/key IDs live and how leaks are prevented.
- `storekit2-iap-defaults` — this pipeline is how a build carrying that
  skill's IAP code reaches TestFlight.
- Official sources: when verifying or updating a factual or version-sensitive claim, read `references/official-docs.md`.
