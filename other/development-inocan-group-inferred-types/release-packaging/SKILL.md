---
name: release-packaging
description: Package and release the .NET 8 WPF widget host app using MSIX or ClickOnce. Use when configuring installers, signing, update channels, and publishing release artifacts.
---

# Release Packaging

## Overview

Prepare secure, updateable installers for desktop distribution.

## Definition of done (DoD)

- MSIX or ClickOnce manifest configured with correct identity
- Release builds signed with valid certificate
- Auto-update URL configured and tested
- Version number incremented in publish profile
- Installer tested on clean machine (no dev tools)
- Uninstall leaves no orphan files/registry entries

## Workflow

1. Choose packaging method (MSIX or ClickOnce).
2. Configure signing certificate and pipeline secrets.
3. Set update channel and feed location.
4. Produce release artifacts and verify install.

## Guidance

- Prefer MSIX for modern deployment if available.
- Keep ClickOnce for legacy environments.
- Always sign release builds.

## References

- `references/msix.md` for MSIX packaging.
- `references/clickonce.md` for ClickOnce guidance.
- `references/signing.md` for certificate setup.
