---
name: archive
description: Archive and distribute forager to TestFlight. Auto-increments build number, archives for Release, uploads to App Store Connect, waits for processing, sets export compliance, and adds to beta test group. TRIGGER when the user says "archive", "deploy to TestFlight", "upload to TestFlight", "release a build", "ship a build", or any request to distribute the app.
allowed-tools: Read, Write, Bash(grep:*), Bash(awk:*), Bash(mv:*), Bash(git add:*), Bash(git commit:*), Bash(git push:*), Bash(git log:*), Bash(git status:*), Bash(git branch:*), Bash(xcodebuild:*), Bash(cat:*), Bash(swift:*), Bash(curl:*), Bash(jq:*), Bash(sleep:*), Bash(test:*), Bash(Tools/appstore-connect:*), Bash(chmod:*)
---

# Archive & Distribute to TestFlight

Full pipeline: version bump → archive → upload → distribute via script.

**CRITICAL: Permission-safe execution.** Run each operation as a SEPARATE Bash tool call. Never chain commands with `&&`, `||`, or pipes. Never combine multiple operations in one Bash call. One command per call. This ensures all commands match pre-approved permission patterns.

## Current State

- Marketing version: !`grep -m1 'MARKETING_VERSION' forager.xcodeproj/project.pbxproj`
- Build number: !`grep -m1 'CURRENT_PROJECT_VERSION' forager.xcodeproj/project.pbxproj`
- Branch: !`git branch --show-current`
- Uncommitted changes: !`git status --short`

**API key check** — Run this as your first step (do NOT use `!` backtick for this since it's outside the project dir):
```bash
test -f ~/.appstoreconnect/config && echo "API KEY CONFIGURED" || echo "NOT CONFIGURED"
```

## Prerequisites: App Store Connect API Key

The TestFlight automation requires an App Store Connect API key. Check if configured (run as a Bash call):

```bash
test -f ~/.appstoreconnect/config && cat ~/.appstoreconnect/config || echo "NOT CONFIGURED"
```

**If not configured**, guide the user through setup:

1. Go to **App Store Connect → Users and Access → Integrations → App Store Connect API**
2. Click **Generate API Key** (or use existing)
3. Role: **Developer** (minimum for TestFlight management)
4. Download the `.p8` file (can only download ONCE)
5. Note the **Key ID** and **Issuer ID** shown on the page

Then create the config:
```bash
mkdir -p ~/.appstoreconnect/private_keys

# User provides these values:
cat > ~/.appstoreconnect/config << 'EOF'
KEY_ID=XXXXXXXXXX
ISSUER_ID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
EOF

# User places their .p8 file:
# cp ~/Downloads/AuthKey_XXXXXXXXXX.p8 ~/.appstoreconnect/private_keys/
```

**If API key is not set up and user wants to skip TestFlight automation**, run steps 1-6 only and report that TestFlight distribution was skipped.

## Step 1: Pre-Flight Checks

Verify before archiving:
- [ ] On `main` branch (archives should be from main after PR merge)
- [ ] Working tree is clean (no uncommitted changes)
- [ ] Build succeeds in Release configuration

If not on main or there are uncommitted changes, warn the user and ask whether to proceed.

## Step 2: Auto-Increment Build Number

The build number (`CURRENT_PROJECT_VERSION`) auto-increments on every archive.

**Read current value** — run as separate calls:
```bash
grep -m1 'CURRENT_PROJECT_VERSION = ' forager.xcodeproj/project.pbxproj
```
Parse the number from output. Compute NEW_BUILD = CURRENT_BUILD + 1.

**Update both Debug and Release** — single script call:
```bash
Tools/bump-build.sh CURRENT_BUILD NEW_BUILD
```

**Show result** and confirm with user:
```
Version: 1.2 (build 24)
```

## Step 3: Optional — Bump Marketing Version

Only if the user explicitly requests a version bump (e.g., `/archive --version 1.3`):

```bash
# $ARGUMENTS may contain: --version X.Y
# If present, update MARKETING_VERSION in the first two occurrences (app target only)
```

Marketing version format: `MAJOR.MINOR` (e.g., 1.2, 1.3, 2.0). Validate format before applying.

## Step 4: Commit Version Bump

Use the current milestone from `docs/current-story.md` for the commit prefix. If no active milestone, use a generic prefix.

Run as three separate calls:
```bash
git add forager.xcodeproj/project.pbxproj
```
```bash
git commit -m "Bump build number to $NEW_BUILD for TestFlight"
```
```bash
git push
```

## Step 5: Archive

```bash
xcodebuild archive \
  -project forager.xcodeproj \
  -scheme forager \
  -archivePath ~/Desktop/forager-$MARKETING_VERSION-$NEW_BUILD.xcarchive \
  -destination 'generic/platform=iOS' \
  2>&1 | tail -5
```

This uses Release configuration by default (CloudKit enabled).

On success, report:
- Archive path
- Version and build number
- Archive size

On failure:
- Show full error output
- Check signing issues first (most common)

## Step 6: Export & Upload to App Store Connect

Use the Write tool to create `/tmp/ForagerExportOptions.plist` with this content:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store-connect</string>
    <key>teamID</key>
    <string>93FT2PT9NM</string>
    <key>destination</key>
    <string>upload</string>
    <key>signingStyle</key>
    <string>automatic</string>
</dict>
</plist>
```

Then run export as a separate call. **CRITICAL: Always include API key auth flags** — without them, `xcodebuild` cannot find App Store Connect credentials from CLI:
```bash
xcodebuild -exportArchive -archivePath ~/Desktop/forager-$MARKETING_VERSION-$NEW_BUILD.xcarchive -exportOptionsPlist /tmp/ForagerExportOptions.plist -exportPath ~/Desktop/forager-export -allowProvisioningUpdates -authenticationKeyPath /Users/rich/.appstoreconnect/private_keys/AuthKey_QBAG38ZPZR.p8 -authenticationKeyID QBAG38ZPZR -authenticationKeyIssuerID fbdd459e-6ae5-4dc5-82d0-c2bf095392e4
```

The `destination: upload` auto-uploads to App Store Connect.

## Step 7: TestFlight Distribution (Automated Script)

After upload succeeds, run the distribution script. This single command handles:
- JWT generation
- Build processing poll (up to 20 minutes)
- Export compliance verification
- "What to Test" notes (from latest commit or custom text)
- Beta review submission + approval wait
- Adding build to Public Beta Testers group

```bash
Tools/appstore-connect/testflight-distribute.sh $NEW_BUILD
```

Or with custom "What to Test" notes:
```bash
Tools/appstore-connect/testflight-distribute.sh $NEW_BUILD "Custom release notes here"
```

The script outputs progress and a final report. If it fails at any step, it exits with a non-zero code and an error message.

**If the script fails**, check:
- JWT issues → verify `~/.appstoreconnect/config` and `.p8` file
- Build not found → upload may still be propagating, wait 2 min and re-run
- Review stuck → check App Store Connect web UI

## Step 8: Final Report

After the script completes, report:

```
✅ Archive & TestFlight Distribution Complete

Version:       $MARKETING_VERSION (build $NEW_BUILD)
Archive:       ~/Desktop/forager-$MARKETING_VERSION-$NEW_BUILD.xcarchive
Status:        Available to testers (see script output for details)
```

## Arguments

- No arguments: full pipeline (archive → upload → distribute to **Public Beta Testers**)
- `--version X.Y`: also bump marketing version (e.g., `/archive --version 1.3`)
- `--no-upload`: archive and export only, skip TestFlight upload and distribution
- `--no-wait`: upload only, skip distribution script
- `--dry-run`: show what would happen without making changes
- `--testflight-only`: skip archive/upload, run only the distribution script (for builds already uploaded)

## Configuration

- **Team ID**: 93FT2PT9NM
- **Bundle ID**: com.richhayn.forager
- **Signing**: Automatic (Apple Development → Distribution managed by Xcode)
- **CloudKit**: Enabled in Release, disabled in Debug
- **API Key Config**: `~/.appstoreconnect/config` (KEY_ID, ISSUER_ID)
- **API Key File**: `~/.appstoreconnect/private_keys/AuthKey_{KEY_ID}.p8`
- **JWT Generator**: `Tools/appstore-connect/generate-jwt.swift`
- **Distribution Script**: `Tools/appstore-connect/testflight-distribute.sh`

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `No signing certificate` | Open Xcode → Signing & Capabilities → resolve. Or: `security find-identity -v -p codesigning` |
| `Provisioning profile` | Xcode auto-manages. Try: Xcode → Preferences → Accounts → Download Manual Profiles |
| `Export failed` | Try `xcodebuild -exportArchive` with `-allowProvisioningUpdates` flag |
| `Upload rejected` | Check build number isn't reused. App Store Connect rejects duplicate build numbers per version |
| `JWT generation failed` | Verify .p8 file path and format. Run: `swift Tools/appstore-connect/generate-jwt.swift <path> <key-id> <issuer-id>` manually |
| `API returns 401` | JWT may be expired (20 min). Script auto-refreshes after 15 poll cycles |
| `API returns 403` | API key role too restrictive. Needs at least "Developer" role |
| `Build not found after upload` | Wait 2-5 minutes for propagation, then re-run the distribution script |
| `Build stuck in PROCESSING` | Normal for up to 15 min. If >30 min, check App Store Connect web UI |
| `Export compliance already set` | Info.plist has `ITSAppUsesNonExemptEncryption`. Script handles this automatically |
