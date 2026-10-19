---
name: publish-macos
description: Bump version, commit, push, build a native macOS Xcode project, export a signed artifact, then publish to either GitHub Releases or the Mac App Store (remembered per project). Use /publish-macos [scheme] [--no-bump] [--github|--app-store|--target=<github|app-store>]. Auto-detects scheme if omitted.
purpose: Bumps version, builds a signed macOS app, and publishes it to GitHub or the App Store.
user_invocable: true
args: "[scheme] [--no-bump] [--github|--app-store|--target=<github|app-store>]"
stage: merge
---

# Build & Publish Native macOS Release

Bumps the version, commits, pushes, builds a native macOS Xcode project, exports a signed artifact, and publishes it to the configured target (GitHub Releases or Mac App Store). Tags the commit on success.

The publish target is remembered per-project in `./.claude/publish-macos-target`. First run asks. Later runs run silently unless the user overrides with `--github`, `--app-store`, or `--target=<…>`.

## Arguments

`/publish-macos [scheme] [--no-bump] [--github|--app-store|--target=<github|app-store>]`

- `scheme`: Xcode scheme to build. Auto-detected if omitted.
- `--no-bump`: Skip version bump, commit, push, and tagging. Build and publish only.
- `--github` / `--app-store` / `--target=<github|app-store>`: Publish target override. Persists to the per-project target file. If none is given and no file exists, the skill asks once.

## Workflow

### 1. Verify Xcode project

```bash
ls *.xcworkspace 2>/dev/null || ls *.xcodeproj 2>/dev/null
```

If neither found, stop:

> Not a native macOS project — no .xcworkspace or .xcodeproj found.

### 2. Detect scheme

If no scheme argument, list schemes:

```bash
xcodebuild -list 2>/dev/null
```

Pick the first non-test scheme (does not end in `Tests` or `UITests`). If multiple, use AskUserQuestion.

### 3. Resolve publish target

Priority:

1. **CLI arg** — `--github`, `--app-store`, or `--target=<value>`. Persist it:
   ```bash
   ~/.claude/hooks/publish-macos-target.sh set <github|app-store>
   ```
2. **Stored file** — otherwise read:
   ```bash
   ~/.claude/hooks/publish-macos-target.sh get
   ```
   If non-empty, use it silently. Do **not** mention the target until step 12 unless the user asks.
3. **First run** — if no arg and no stored value, use AskUserQuestion:

   ```
   question: "Where should this project publish to?"
   options:
     - label: "GitHub Releases"
       description: "Upload DMG / notarized .app to a new GitHub release"
     - label: "Mac App Store"
       description: "Upload .pkg to App Store Connect via altool"
   ```

   Save the choice:
   ```bash
   ~/.claude/hooks/publish-macos-target.sh set <github|app-store>
   ```

Hold the resolved target as `TARGET` for later steps.

### 4. Bump version (skip if `--no-bump`)

```bash
agvtool what-marketing-version -terse1 | tail -n 1 | tr -d ' '
```

If `agvtool` reports versioning isn't configured, stop:

> `agvtool` is not configured for this project. Enable Apple Generic Versioning, or re-run with `--no-bump`.

Ask which part to bump:

```
question: "Current version: CURRENT. Which part to bump?"
options:
  - label: "Patch"    description: "X.Y.Z → X.Y.(Z+1)"
  - label: "Minor"    description: "X.Y.Z → X.(Y+1).0"
  - label: "Major"    description: "X.Y.Z → (X+1).0.0"
```

Apply:

```bash
agvtool new-marketing-version NEW_VERSION
agvtool next-version -all
```

Confirm:

```
question: "Bumped to NEW_VERSION. Commit and push?"
options:
  - label: "Commit and push"  description: "git add -A && git commit && git push"
  - label: "Stop"             description: "Leave the working tree dirty and exit"
```

Stop if rejected.

**Stamp the changelog** (best-effort — skip silently if no `CHANGELOG.md` at repo root):

- Find the heading line for `NEW_VERSION` (matches `## [NEW_VERSION]` or `## NEW_VERSION`, with or without surrounding brackets).
- If that line contains an in-progress marker (case-insensitive: `in-progress`, `in progress`, `unreleased`, `wip`, `tbd`), replace the marker with today's date in `YYYY-MM-DD` format. Preserve the surrounding separator (`—`, `-`, `(`, etc.).
- If no matching heading exists, or the heading has no in-progress marker, leave the file alone.
- If multiple headings match the version, only stamp the first and report the others.

Then commit everything together:

```bash
git add -A
git commit -m "chore: bump version to NEW_VERSION"
git push
```

Remember `NEW_VERSION` for steps 11 and 12.

### 5. Confirm before building

```
question: "Build release archive for scheme: SCHEME?"
options:
  - label: "Build"
    description: "xcodebuild archive → export → publish"
```

Stop if rejected.

### 6. Prepare output directory

```bash
rm -rf build/publish
mkdir -p build/publish
```

### 6.5. Resolve Apple credentials

Needed by both targets (github needs them to sign/notarize; app-store needs them for `altool`). Resolve `APPLE_ID`, `APPLE_TEAM_ID`, `APPLE_APP_PASSWORD`. Always route through `~/.claude/hooks/secret.sh` per the CLAUDE.md secrets rule — never read tokens directly from memory or env. The helper checks Vaultwarden via `bw serve` first and falls back to env vars.

Canonical vault item: a single login named `apple-notarization` (lowercase slug, per the "Item names are lowercase service names" convention) with:
- `login.username` → Apple ID
- `login.password` → app-specific password (Apple rotates these on Apple-ID password changes — keep the live value in the vault, never hard-code in memory)

`APPLE_TEAM_ID` does not rotate, so it lives outside the vault (memory or Xcode project).

Resolution:

1. **Apple ID and app-specific password — via `secret.sh`** (Vaultwarden first, env-var fallback):
   ```bash
   APPLE_ID="$(~/.claude/hooks/secret.sh apple-notarization username)"
   APPLE_APP_PASSWORD="$(~/.claude/hooks/secret.sh apple-notarization password)"
   ```
   If either is empty: check whether a vault item exists under a different name with `curl -s "http://localhost:8087/list/object/items?search=apple"` (when `bw serve` is up) and report the mismatch — do not silently substitute.

2. **`APPLE_TEAM_ID` — memory, then env, then Xcode build settings**:
   ```bash
   APPLE_TEAM_ID="${APPLE_TEAM_ID:-}"   # env
   # …or read from saved memory if present
   # …or, as last resort, read DEVELOPMENT_TEAM from the project:
   xcodebuild -showBuildSettings -scheme SCHEME 2>/dev/null \
     | awk '/^[[:space:]]*DEVELOPMENT_TEAM = / {print $3; exit}'
   ```

If `bw` is installed but locked (`bw status` returns `locked`) and the env-var fallback is also empty:

> Vaultwarden is locked and no APPLE_APP_PASSWORD env var is set. Run `bw unlock` and set `BW_SESSION`, then re-run `bw serve --port 8087 &` so the helper can reach the vault.

If any of `APPLE_ID`, `APPLE_TEAM_ID`, `APPLE_APP_PASSWORD` is still missing:

> Publishing requires APPLE_ID, APPLE_TEAM_ID, and APPLE_APP_PASSWORD. Add a vault item named `apple-notarization` (login fields: Apple ID + app-specific password), or provide via env vars / memory / Xcode `DEVELOPMENT_TEAM`.

Hold the resolved values in env for the rest of the workflow.

### 7. Archive

Use `-workspace` if a `.xcworkspace` exists, else `-project`.

**If `TARGET == github`** (Developer ID signing — required so Gatekeeper accepts the DMG after download. Ad-hoc signing fails with "is damaged" once the quarantine bit is set):

```bash
xcodebuild archive \
  -workspace *.xcworkspace \
  -scheme SCHEME \
  -configuration Release \
  -archivePath build/publish/SCHEME.xcarchive \
  CODE_SIGN_STYLE=Manual \
  CODE_SIGN_IDENTITY="Developer ID Application" \
  DEVELOPMENT_TEAM="$APPLE_TEAM_ID" \
  | xcpretty || cat
```

**If `TARGET == app-store`** (let the project's own signing config handle it — Apple Distribution + provisioning profile are required):

```bash
xcodebuild archive \
  -workspace *.xcworkspace \
  -scheme SCHEME \
  -configuration Release \
  -archivePath build/publish/SCHEME.xcarchive \
  | xcpretty || cat
```

Swap `-workspace *.xcworkspace` for `-project *.xcodeproj` if only the project exists.

Stop on failure and show the last 30 lines.

### 8. Export

**If `TARGET == github`:**

```bash
cat > /tmp/ExportOptions.plist << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>developer-id</string>
    <key>teamID</key>
    <string>$APPLE_TEAM_ID</string>
    <key>signingStyle</key>
    <string>manual</string>
</dict>
</plist>
EOF

xcodebuild -exportArchive \
  -archivePath build/publish/SCHEME.xcarchive \
  -exportPath build/publish/export \
  -exportOptionsPlist /tmp/ExportOptions.plist
```

Then go to step 9.

**If `TARGET == app-store`:**

```bash
cat > /tmp/ExportOptions.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string>
</dict>
</plist>
EOF

xcodebuild -exportArchive \
  -archivePath build/publish/SCHEME.xcarchive \
  -exportPath build/publish/export \
  -exportOptionsPlist /tmp/ExportOptions.plist
```

The export dir will contain `SCHEME.pkg`. Skip to step 10.

Stop on failure.

### 9. Package for GitHub (only when `TARGET == github`)

Check for `create-dmg`:

```bash
which create-dmg
```

**If found:**

Stage the `.app` plus an `Applications` symlink in a clean directory first — `create-dmg` is brittle when handed an export dir that may carry sibling files (`DistributionSummary.plist`, `Packaging.log`, etc.):

```bash
mkdir -p build/publish/dmg-stage
cp -R build/publish/export/SCHEME.app build/publish/dmg-stage/
ln -sfn /Applications build/publish/dmg-stage/Applications

create-dmg \
  --volname "SCHEME" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --app-drop-link 450 185 \
  "build/publish/SCHEME.dmg" \
  "build/publish/dmg-stage/"
```

**TCC fallback** — if `create-dmg` (or any `hdiutil` mount path) errors with `Operation not permitted` referring to `/Volumes/SCHEME/...`, the running shell lacks the macOS Tahoe TCC grant for `/Volumes`. Do **not** ask the user to re-run from another terminal as the first move. The mount-free path works in any shell:

```bash
hdiutil makehybrid -hfs -hfs-volume-name "SCHEME" \
  -hfs-openfolder build/publish/dmg-stage \
  build/publish/dmg-stage \
  -o build/publish/SCHEME.tmp.dmg

hdiutil convert build/publish/SCHEME.tmp.dmg \
  -format UDZO \
  -imagekey zlib-level=9 \
  -o build/publish/SCHEME.dmg

rm -f build/publish/SCHEME.tmp.dmg
```

The fallback DMG is plainer (no backdrop, no positioned icons) but is a valid notarizable image and the Applications symlink keeps the install gesture intact. Mention the fallback was used in the final report so the user knows the chrome was skipped.

Then notarize and staple the DMG so Gatekeeper accepts it after download (Apple creds were resolved in step 6.5):

```bash
xcrun notarytool submit "build/publish/SCHEME.dmg" \
  --apple-id "$APPLE_ID" \
  --team-id "$APPLE_TEAM_ID" \
  --password "$APPLE_APP_PASSWORD" \
  --wait

xcrun stapler staple "build/publish/SCHEME.dmg"
```

Stop on notarization failure and show the submission log via `xcrun notarytool log <submission-id> --apple-id … --team-id … --password …`.

Set `ARTIFACT=build/publish/SCHEME.dmg`. Go to step 10.

**If not found:** ask:

```
question: "create-dmg not installed. How do you want to proceed?"
options:
  - label: "Notarize .app"
    description: "Notarize & staple the .app, zip it, attach to the release"
  - label: "Stop here"
    description: "Keep the exported .app and exit (no publish, no tag)"
```

If "Stop here": report location and exit.

If "Notarize .app" (Apple creds were resolved in step 6.5):

```bash
ditto -c -k --keepParent \
  "build/publish/export/SCHEME.app" \
  "build/publish/SCHEME.zip"

xcrun notarytool submit "build/publish/SCHEME.zip" \
  --apple-id "$APPLE_ID" \
  --team-id "$APPLE_TEAM_ID" \
  --password "$APPLE_APP_PASSWORD" \
  --wait

xcrun stapler staple "build/publish/export/SCHEME.app"

rm -f "build/publish/SCHEME.zip"
ditto -c -k --keepParent \
  "build/publish/export/SCHEME.app" \
  "build/publish/SCHEME.zip"
```

Set `ARTIFACT=build/publish/SCHEME.zip`.

### 10. Publish

Apple creds (`APPLE_ID`, `APPLE_TEAM_ID`, `APPLE_APP_PASSWORD`) were resolved in step 6.5 and are already in env.

#### If `TARGET == github`

Require `gh` authenticated (`gh auth status`). If not, stop with instructions.

```bash
gh release create "vNEW_VERSION" \
  "ARTIFACT" \
  --title "vNEW_VERSION" \
  --generate-notes
```

If `--no-bump` is in effect, ask the user for a release name (or default to the most recent tag incremented).

#### If `TARGET == app-store`

Upload the `.pkg`:

```bash
xcrun altool --upload-app \
  --type macos \
  --file "build/publish/export/SCHEME.pkg" \
  --username "$APPLE_ID" \
  --password "$APPLE_APP_PASSWORD"
```

Stop on failure. On success, the build is in App Store Connect awaiting processing — submission/review is manual from there.

### 11. Tag the commit (skip if `--no-bump`)

Only after publishing succeeds:

```bash
git tag "vNEW_VERSION"
git push origin "vNEW_VERSION"
```

If tagging fails (e.g. tag exists), report but don't roll back the published artifact.

Note: for `TARGET == github`, `gh release create` already creates the tag remotely. Check before re-tagging:

```bash
git fetch --tags
git tag -l "vNEW_VERSION"
```

If the tag already exists locally/remotely from the release, skip this step.

### 12. Report

```
Build complete:
  version  →  NEW_VERSION                         ← if bumped
  archive  →  build/publish/SCHEME.xcarchive
  artifact →  build/publish/SCHEME.dmg | .zip | .pkg
  target   →  github | app-store
  publish  →  https://github.com/.../releases/tag/vNEW_VERSION   ← github
           →  App Store Connect (awaiting processing)             ← app-store
  tag      →  vNEW_VERSION pushed                                 ← if bumped

All artifacts in build/publish/
```

## Rules

- Prefer `.xcworkspace` over `.xcodeproj` when both exist.
- Use `xcpretty` for archive output if available.
- Stop on first failure; show last 30 lines of build log.
- Version bump → build → publish → tag. Never tag before publish succeeds.
- `--no-bump` skips bump/commit/push and tagging. Build and publish still run.
- GitHub path always Developer-ID-signs the archive and notarizes + staples the DMG (or zipped .app). Ad-hoc signing is never used for downloads — Gatekeeper rejects it once quarantine is set.
- App Store path requires proper signing config in the Xcode project (Apple Distribution cert, provisioning profile). The skill does not override signing for this path.
- Target is persisted per-project in `./.claude/publish-macos-target`. Arg flags override and update the stored value. Silent otherwise.
- Never modify other project files beyond what `agvtool` touches.
