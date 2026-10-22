---
name: release-mac-app
description: >-
  Releases Sparkle-updated macOS apps end to end: build, notarization, appcast, GitHub Release,
  Homebrew cask, and closeout checks. Use when shipping a new version of a Mac menu-bar app or
  utility.
source: "https://github.com/steipete/agent-scripts"
attribution: "steipete/agent-scripts by Peter Steinberger"
version: "1.0.0"
platform: macos
license: MIT
---

# Mac App Release

> **Attribution:** Sourced from [steipete/agent-scripts](https://github.com/steipete/agent-scripts) by [Peter Steinberger](https://github.com/steipete).

Use for Sparkle-updated macOS apps (menu bar apps, utilities, etc.).

## Rules

- Work from the app repo.
- Read `.mac-release.env`; it is the repo-owned release manifest.
- Never print private key material.
- Prefer Keychain Sparkle signing. `SPARKLE_PRIVATE_KEY_FILE` is an explicit override only.

## Release Manifest (`.mac-release.env`)

Required fields:
- `MAC_RELEASE_APP_NAME` - app name
- `MAC_RELEASE_REPO` - `owner/repo`
- `MAC_RELEASE_BUNDLE_ID` - bundle identifier
- `MAC_RELEASE_VERSION_FILE` - path to version file
- `MAC_RELEASE_APPCAST` - path to appcast XML
- `MAC_RELEASE_FEED_URL` - public appcast feed URL
- `MAC_RELEASE_DOWNLOAD_URL_PREFIX` - download base URL
- `MAC_RELEASE_APP_ZIP` - app zip artifact name
- `MAC_RELEASE_PACKAGE_CMD` - build/package command

## Release Checklist

- [ ] appcast entry has URL, length, Sparkle signature
- [ ] downloaded enclosure verifies with Sparkle
- [ ] extracted app passes `codesign`, `spctl`, and `stapler validate`
- [ ] GitHub release has app zip + dSYM zip
- [ ] release notes match the changelog section
- [ ] after verified release, bump changelog to next patch `Unreleased`

## Key Commands

```bash
# Check app code signing
codesign -dv --verbose=4 /path/to/App.app

# Verify notarization
spctl -a -vv /path/to/App.app

# Verify stapling
xcrun stapler validate /path/to/App.app

# Check zip contents
unzip -l App.zip

# Sign appcast entry (Sparkle)
sign_update App.zip private_key.pem
```

## 1Password Integration

If the release requires secrets via 1Password:
- Set `MAC_RELEASE_OP_ITEM` + `MAC_RELEASE_OP_FIELDS` in `.mac-release.env`
- Secrets are read once via `op` inside one persistent tmux session
- Never expose or echo secret values
- Prefer secrets already exported in the environment; call `op` only for fields that are missing
- Read all missing fields in one command inside that tmux session, so 1Password prompts once per release
