---
name: macos-app-releases
description:
  Ship native SwiftPM macOS apps outside the Mac App Store, with Developer ID signing, notarization, GitHub Releases and
  Sparkle 2 updates. Covers DMG, zip and SHA256SUMS assets, an EdDSA-signed appcast, a tag-driven GitHub Actions release
  workflow with protected secrets, and a local fallback from the Mac. Use when setting up, running or debugging a Mac
  app's release pipeline, signing identity, notarization, update feed, release secrets or version bumps.
---

# Releasing macOS apps outside the App Store

This pipeline has shipped several SwiftPM apps, sandboxed and not, some with app extensions. `make bump V=patch PUSH=1`
tags a version; a GitHub Actions run tests, signs with Developer ID, notarizes and staples, and publishes a GitHub
Release with the DMG, zip, `SHA256SUMS` and a signed Sparkle `appcast.xml` that installed copies read through
`releases/latest`. Without CI secrets, the same scripts publish from the Mac. Project skeleton, variants and
entitlements basics are in the `macos-app-development` skill.

## Rules for agents

- Never read, print, copy, export or upload secrets: the .p12 and its password, the app-specific password, the Sparkle
  private key, secret values. The user runs `gh secret set`, `generate_keys -x` and Keychain exports; you give them the
  exact commands.
- Run `generate_keys` (it creates or reads a Keychain key) only when the user asks for the key.
- Notarization uploads the build to Apple: run `make build-notarized` or a credentialed `make release` only when the
  user asks for a release or a notarized build.
- Tag, push a tag or create a GitHub release only when the user asks. `make bump` without `PUSH=1` tags locally.
- Never install over, launch or update the user's installed copy to test; check builds in `build/`.

## Placeholders and templates

| Placeholder      | Example            | Meaning                                                           |
| ---------------- | ------------------ | ----------------------------------------------------------------- |
| `<App>`          | `Acme`             | SwiftPM product, executable and `.app` name; `<App>-X.Y.Z.dmg`    |
| `<app>`          | `acme`             | Sparkle Keychain account (lowercase)                              |
| `<bundle id>`    | `com.example.acme` | Release bundle id; Dev and Test builds append `.dev` and `.test`  |
| `<owner>/<repo>` | `example/acme`     | Public GitHub repository                                          |
| `<profile>`      | `example-notary`   | notarytool Keychain profile, shared by the team's apps            |
| `<TEAMID>`       | `ABCDE12345`       | Apple team id, in parentheses in the Developer ID identity's name |

| Template                                                           | Copy to              | Does                                                                           |
| ------------------------------------------------------------------ | -------------------- | ------------------------------------------------------------------------------ |
| [build-app.sh](references/build-app.sh)                            | `scripts/`           | Assembles the `.app`, embeds and thins Sparkle, signs nested code              |
| [release.sh](references/release.sh)                                | `scripts/`           | App, zip, DMG, `SHA256SUMS`; notarizes and staples, or ad-hoc + what's missing |
| [appcast.sh](references/appcast.sh)                                | `scripts/`           | Downloads the live feed, adds and signs the new item with its release notes    |
| [bump-version.sh](references/bump-version.sh)                      | `scripts/`           | `VERSION`, `CHANGELOG.md` section, commit, `vX.Y.Z` tag, optional atomic push  |
| [changelog.sh](references/changelog.sh)                            | `scripts/`           | `CHANGELOG.md` sections from Conventional Commits; prints a version's notes    |
| [ci-select-xcode.sh](references/ci-select-xcode.sh)                | `scripts/`           | Picks the newest Xcode 26+ on the runner                                       |
| [release.yml](references/release.yml), [ci.yml](references/ci.yml) | `.github/workflows/` | Tag-driven release; tests and a release build on PRs and main                  |
| [release.mk](references/release.mk)                                | `Makefile`           | `app`, `release`, `build-notarized`, `install-notarized`, `appcast`, `bump`    |
| [AppUpdater.swift](references/AppUpdater.swift)                    | app sources          | Sparkle controller and Check for Updates… (SwiftUI or AppKit)                  |
| [releasing.md](references/releasing.md)                            | `docs/`              | Maintainer doc: both routes, feed, key, secrets                                |

## 1. Decide first

| Choice        | Recommendation                                                                                              | Why                                                                                                |
| ------------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Store         | Developer ID (this skill). App Store needs an Xcode project, the sandbox and Apple's updates                | Sparkle isn't allowed in the store; Developer ID keeps features the sandbox blocks                 |
| Hosting       | Public repo: GitHub Releases, feed `https://github.com/<owner>/<repo>/releases/latest/download/appcast.xml` | No bucket or extra credentials; `latest` never points at a pre-release                             |
| Private repo  | Its assets need auth: host files and feed on a bucket behind your domain, uploaded by CI                    | Sparkle and browsers can't authenticate (R2's `r2.dev` URLs are rate-limited: use a custom domain) |
| Feed URL      | Final before the first shipped build                                                                        | It's baked into every installed copy                                                               |
| Architectures | Apple silicon only (`ARCH=arm64`, Sparkle thinned to match)                                                 | Smaller and simpler; Intel needs a universal build                                                 |
| Versions      | `./VERSION` is `CFBundleShortVersionString`; the build number is the commit count                           | Only grows; Sparkle compares `CFBundleVersion`                                                     |
| Pre-releases  | `vX.Y.Z-beta.N` tags publish a GitHub pre-release without a feed                                            | Testers download it; installed copies never update to it                                           |
| Sandbox       | Optional with Developer ID; if sandboxed, Sparkle needs its installer service (§3)                          | Decide before features (see `macos-app-development`)                                               |

Record these in a decision record (context, decision, consequences).

## 2. Once per developer (the user)

1. **Developer ID Application certificate** (paid Apple Developer Program; Apple limits who on the team can create it):
   Xcode ▸ Settings ▸ Accounts ▸ Manage Certificates ▸ + ▸ Developer ID Application. Check it and read the team id:
   `security find-identity -v -p codesigning` → `"Developer ID Application: Name (TEAMID)"`.
2. **App-specific password** for the notarizing Apple Account: account.apple.com ▸ Sign-In and Security ▸ App-Specific
   Passwords.
3. **notarytool profile** in the login Keychain, one for all the team's apps:
   `xcrun notarytool store-credentials <profile> --apple-id <apple id> --team-id <TEAMID>` (prompts for the password).
   Check: `xcrun notarytool history --keychain-profile <profile>`.

## 3. Once per app

**Sparkle 2 through SwiftPM.** In `Package.swift`,
`.package(url: "https://github.com/sparkle-project/Sparkle", from: "2.10.0")`; the app target gets
`.product(name: "Sparkle", package: "Sparkle")` and
`linkerSettings: [.unsafeFlags(["-Xlinker", "-rpath", "-Xlinker", "@executable_path/../Frameworks"])]`.
[build-app.sh](references/build-app.sh) copies the framework with `ditto`, thins it to `ARCH`, strips the absolute
rpaths SwiftPM adds, and signs innermost first with `--force --options runtime --timestamp` (ad-hoc without either when
there's no identity):

1. `Sparkle.framework/Versions/B/XPCServices/Installer.xpc`, then `Downloader.xpc` with
   `--preserve-metadata=entitlements`
2. `Versions/B/Autoupdate`, `Versions/B/Updater.app`, then `Sparkle.framework`
3. App extensions (sandboxed, each with its own entitlements) and helpers
4. The app, with its entitlements: hardened runtime, only proven needs, each with an XML comment saying why

**Info.plist**: `SUFeedURL` (above) and `SUEnableAutomaticChecks` `true` (skips Sparkle's "check automatically?"
question). `build-app.sh` adds `SUPublicEDKey` from `Resources/SparklePublicKey.txt` to release builds and deletes the
feed keys from Dev and Test builds, so they never update over the installed release. A **sandboxed** app also needs
`SUEnableInstallerLauncherService` `true`, `com.apple.security.network.client` (or `SUEnableDownloaderService`) and a
`com.apple.security.temporary-exception.mach-lookup.global-name` array with `$(PRODUCT_BUNDLE_IDENTIFIER)-spks` and
`$(PRODUCT_BUNDLE_IDENTIFIER)-spki`; `build-app.sh` fills in each variant's bundle id.

**EdDSA keys** (the user runs these):

```bash
swift package resolve
.build/artifacts/sparkle/Sparkle/bin/generate_keys --account <app>      # creates or reuses; prints the public key
.build/artifacts/sparkle/Sparkle/bin/generate_keys --account <app> -p   # prints it again
```

Commit the public key as `Resources/SparklePublicKey.txt`. Back up the private key outside the repo (export with `-x`,
store it in a password manager): installed copies only accept updates signed with it. One account per app keeps keys
apart; Sparkle also allows one key for all apps.

**Updater UI**: [AppUpdater.swift](references/AppUpdater.swift). `SPUStandardUpdaterController(startingUpdater: false…)`
is `nil` without a feed and key, starts a second after launch, and backs Check for Updates… right after About in the app
menu (and in a menu bar panel, if the app has one), disabled when `nil`.

## 4. Add the release tooling

Copy the templates, replace the placeholders, `chmod +x scripts/*.sh`, put `0.1.0` in `VERSION`, and confirm nothing is
left: `grep -rnE '<(App|app|bundle id|owner|repo|profile)>' scripts .github Makefile docs` (drop the templates'
"Template from…" notes, which name them too). Then `make release` builds ad-hoc and lists what's missing, which proves
the pipeline before any credential is involved. Adjust the Test steps in both workflows to the app's packages.

**Release notes come from the commits.** `make bump` adds the release's `CHANGELOG.md` section (`changelog.sh`): the
Conventional Commits since the previous release (a stable one counts from the previous stable tag, so it includes its
betas), as breaking changes (`feat!:`, `BREAKING CHANGE:`), features, fixes and performance; other types stay out. That
section is the GitHub release's body (`release.yml`) and, written next to the zip as `<App>-X.Y.Z.md`, the update's
notes in `appcast.xml`, which Sparkle's update window renders (`sparkle:format="markdown"`). So the project's commit
subjects must be Conventional Commits that read well in a list. Backfill releases made before this with
`scripts/changelog.sh section X.Y.Z <previous tag> <tag>`. To reword notes, bump without `PUSH`, edit, amend,
`git tag -fa`.

## 5. GitHub setup (the user runs these)

1. Restrict the `release` environment to `v*` tags:

   ```bash
   REPO=<owner>/<repo>
   gh api -X PUT "repos/$REPO/environments/release" --input - <<'JSON'
   {"deployment_branch_policy": {"protected_branches": false, "custom_branch_policies": true}}
   JSON
   gh api -X POST "repos/$REPO/environments/release/deployment-branch-policies" -f name='v*' -f type=tag
   gh api "repos/$REPO/environments/release/deployment-branch-policies" --jq '.branch_policies[] | "\(.type) \(.name)"'
   ```

2. Export the identity: Keychain Access ▸ login ▸ My Certificates ▸ "Developer ID Application: …" (its disclosure
   triangle shows the private key; without it, the .p12 can't sign) ▸ File ▸ Export Items… ▸ `.p12` with a strong
   password.
3. Set the six secrets. Without `--body`, `gh` prompts for the value or reads stdin:

   ```bash
   base64 -i developer-id.p12 | gh secret set DEVELOPER_ID_P12 --env release -R "$REPO"
   gh secret set DEVELOPER_ID_P12_PASSWORD --env release -R "$REPO"
   gh secret set APPLE_ID --env release -R "$REPO"
   gh secret set APPLE_APP_PASSWORD --env release -R "$REPO"
   gh secret set APPLE_TEAM_ID --env release -R "$REPO"
   .build/artifacts/sparkle/Sparkle/bin/generate_keys --account <app> -x sparkle.key
   gh secret set SPARKLE_PRIVATE_KEY --env release -R "$REPO" < sparkle.key
   rm sparkle.key developer-id.p12   # once both are backed up outside the repo
   gh secret list --env release -R "$REPO"   # the six names; values are never shown
   ```

GitHub personal accounts have no account-wide Actions secrets: each repository needs its own copy (the same values work
for every app of the team). One app-specific password can serve every app; one per repository (named after it) lets the
user revoke one without breaking the others. `APPLE_TEAM_ID` isn't secret (it's in every signature): `--body <TEAMID>`.
Every secret is optional: without them the workflow publishes an ad-hoc release without a feed and says so in the notes.

## 6. First release and verification

```bash
make bump V=0.1.0 PUSH=1   # first release: tags the current VERSION; later: make bump V=patch PUSH=1
gh run watch -R <owner>/<repo>
gh release view v0.1.0 -R <owner>/<repo> --json assets --jq '.assets[].name'   # dmg, zip, SHA256SUMS, appcast.xml
```

On the downloaded assets (or `build/release` for a local build):

```bash
shasum -a 256 -c SHA256SUMS
spctl -a -vv <App>.app                           # accepted, source=Notarized Developer ID
codesign --verify --deep --strict --verbose=2 <App>.app
xcrun stapler validate <App>.app && xcrun stapler validate <App>-X.Y.Z.dmg
curl -sL https://github.com/<owner>/<repo>/releases/latest/download/appcast.xml | grep -E 'shortVersionString|edSignature'
```

The feed's new item needs the version, an `sparkle:edSignature` and a `url` into `releases/download/vX.Y.Z/`. The real
proof needs two stable releases: the user installs the older one in `/Applications`, chooses Check for Updates…, gets
offered the newer one, and it installs and relaunches in place. Record that check; it covers feed, signature, framework
signing and (sandboxed) installer services at once. Pre-release tags publish without a feed, so test updates with stable
versions.

## 7. Publishing from the Mac (no CI secrets)

```bash
make bump V=X.Y.Z          # commit and tag locally; nothing is pushed
make build-notarized       # Keychain identity + <profile>; stops without an identity
make appcast               # Keychain Sparkle key, account <app>
git push --atomic origin main vX.Y.Z
gh release create vX.Y.Z build/release/<App>-X.Y.Z.dmg build/release/<App>-X.Y.Z.zip \
  build/release/SHA256SUMS build/appcast/appcast.xml --title vX.Y.Z --verify-tag \
  --notes-file <(scripts/changelog.sh notes X.Y.Z)
```

The tag push still starts the workflow, which tests and builds for minutes, then finds the release and leaves its files
alone. Create the release right after pushing; if the workflow wins the race, it publishes its own (ad-hoc, without a
feed) and the user deletes that release (`gh release delete vX.Y.Z` keeps the tag) and creates theirs.

## 8. Pitfalls

- **Runners aren't your Mac.** A debug-build timing bound failed one first tag run; a UI test failed on another because
  runners show legacy scroll bars. Keep timing asserts loose and UI tests independent of system settings. If a run
  wedges at start with no test output, wrap `swift test` in a watchdog that samples, kills and retries.
- **Release builds compile differently.** A Swift 6 concurrency error appeared only with `-c release` on the runner's
  newer Xcode: `ci.yml` builds the release configuration too.
- **A failed tag run publishes nothing.** Fix on main and release the next patch; moving a pushed tag is the user's
  call.
- **Never overwrite a published release.** `gh release upload --clobber` once replaced notarized files from the Mac with
  an ad-hoc CI build, which also breaks the feed's signatures. The workflow leaves existing releases alone.
- **Every stable release needs `appcast.xml`.** The feed follows `releases/latest`, so a stable release without it
  breaks update checks for everyone until the next one. Without the Sparkle key in CI, publish from the Mac.
- **Feed history comes from the previous release.** `appcast.sh` downloads it with `curl -L` (GitHub redirects `latest`;
  without `-L` you sign a redirect page). It reuses an existing `build/appcast/appcast.xml`: delete that folder when CI
  published the last release.
- **A wrong key fails silently.** `generate_appcast` only warns and writes the item unsigned when the key doesn't match
  `SUPublicEDKey`; `appcast.sh` fails instead.
- **`--generate-notes` is nearly empty** for a project that commits straight to main: GitHub lists merged pull requests,
  so the body is just a compare link. The `CHANGELOG.md` section is the notes; `--generate-notes` is only the workflow's
  fallback when a version has none.
- **Shallow clones break updates.** Without `fetch-depth: 0` the build number is 1 and Sparkle sees an older build.
- **The tag must equal `VERSION`**: tag with `make bump` only.
- **CI keychain**: a temporary keychain with `set-key-partition-list` (or codesign waits on an invisible prompt), added
  to the search list, notary credentials stored in it with `--keychain`, deleted at the end.
- **Notarize the zip, ship the stapled app.** notarytool takes a zip or DMG; staple the app, zip it again, and sign,
  notarize and staple the DMG on its own.
- **Signing**: never `codesign --deep` to sign (one set of entitlements for everything); sign each nested piece. An
  ad-hoc build with the hardened runtime can't load Sparkle under library validation (no team id): leave the runtime to
  real identities, as `build-app.sh` does, or add `com.apple.security.cs.disable-library-validation` to that build.
- **Sparkle at launch**: its first-run prompt during launch kept a window from opening; start it a second later.
- **Absolute rpaths** from SwiftPM point at the checkout's `.build`: strip them so the bundle is self-contained.
- **Runner labels**: use a real image (`macos-26`) plus `ci-select-xcode.sh`; a label that matches no runner never
  starts.

## Checklist

- [ ] Decisions recorded: Developer ID, hosting, feed URL, architectures, sandbox.
- [ ] `security find-identity` shows the identity; `notarytool history` works with the profile.
- [ ] Sparkle embedded and signed nested-first; `codesign --verify --deep --strict` passes; Dev/Test have no feed.
- [ ] `Resources/SparklePublicKey.txt` committed; the private key backed up outside the repo.
- [ ] Templates copied, no placeholders left, ad-hoc `make release` lists what's missing.
- [ ] Commits follow Conventional Commits; `CHANGELOG.md` starts with the first release (or is backfilled).
- [ ] `release` environment limited to `v*` tags with six secrets, or the Mac route documented.
- [ ] First release: four assets, `spctl` and `stapler` pass, signed appcast item.
- [ ] Second release: an installed older build updates in place through Check for Updates….
