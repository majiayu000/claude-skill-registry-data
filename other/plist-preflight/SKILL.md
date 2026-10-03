---
name: plist-preflight
description: Audit macOS app Info.plist and entitlement files before build or release. Use when Codex needs to check bundle metadata, menu-bar app activation policy hints, permission usage strings, sandbox entitlements, or repo-wide plist hygiene without changing signing settings or project files.
---

# Plist Preflight

Use this skill when a macOS app build or release needs a quick metadata check before touching Xcode settings, signing, or source code. It is meant for local app workspaces with `Info.plist`, `.entitlements`, and generated XcodeGen projects.

## Core Workflow

1. Find the app workspace and inspect `project.yml` only for paths and target names.
2. Run the local helper against one app folder or the whole repo.
3. Review warnings before changing project files, signing settings, or app metadata.
4. Fix only the specific metadata problem the user asked about.
5. Re-run the helper and the app's repo-native doctor/build command when available.

## Local Helper

Use `scripts/plist_preflight.py` for deterministic checks:

```bash
python skills/plist-preflight/scripts/plist_preflight.py scan apps/telebar
python skills/plist-preflight/scripts/plist_preflight.py scan apps --format json
python skills/plist-preflight/scripts/plist_preflight.py scan apps/skillbar --expect-menu-bar --fail-on warning
python skills/plist-preflight/scripts/plist_preflight.py inspect apps/skillbar/SkillBarApp/Info.plist
python skills/plist-preflight/scripts/plist_preflight.py inspect apps/vibe-widget/VibeWidgetApp/VibeWidget.entitlements --format markdown
```

The helper uses Python standard-library `plistlib` only. It reads plist-style files and prints warnings; it does not modify files. Use `--format markdown` when the result should be pasted into a PR, issue, or release checklist. Use `--fail-on warning` for CI-style preflight runs that should stop on release-risk metadata, while the default only fails on blockers.

## What To Check

- `CFBundleIdentifier`, `CFBundleName`, `CFBundleDisplayName`, and executable metadata.
- `CFBundleShortVersionString` and `CFBundleVersion` before release or archive work.
- `LSUIElement` or `LSBackgroundOnly` for menu-bar-only utilities when relevant.
- Explicit `--expect-menu-bar` checks for app folders that should behave like accessory/menu-bar utilities.
- Privacy usage strings for requested capabilities such as Apple Events, camera, microphone, location, Bluetooth, contacts, or photo-library access.
- Sandbox and selected entitlement keys when an `.entitlements` file is present.
- Obvious placeholder bundle IDs, missing strings, malformed plists, or metadata that will confuse local app handoff.

## Guardrails

- Do not invent signing, provisioning, notarization, App Store, Microsoft 365, or Apple cloud behavior.
- Do not rewrite generated Xcode project files just to silence a metadata warning.
- Do not add usage strings for capabilities the app does not actually use.
- Treat entitlements as release-sensitive: explain the finding and make the smallest explicit edit only when requested.
- Keep output readable enough to paste into a PR or issue.

## Output Shape

When reporting results, group findings as:

- `Blockers`: malformed files, missing required bundle IDs, or unreadable plist data.
- `Warnings`: likely missing menu-bar metadata, placeholder values, or capability strings that need confirmation.
- `Notes`: healthy files, detected entitlement posture, and exact file paths checked.
