---
name: network-studio
description: Install or update a macOS local-network monitor workspace and SwiftBar plugin. Use when Codex needs a repo-native path for LAN presence, device logging, local dashboards, or compact macOS network safety surfaces on networks the user owns or administers.
---

# Network Studio

Use this skill when the user wants the portable Network Studio workspace, not the native `wifi-watchtower` app. If the request is specifically about `apps/wifi-watchtower`, use `$wifi-watchtower` instead.

Default product shape: a portable local-network watcher installed into a user-chosen folder with an optional SwiftBar wrapper, a dashboard opener, and a continuous scan loop.

## Quick Start

1. Choose the lane first:
   - portable workspace install
   - SwiftBar plugin wiring
   - support-only guidance
2. Run `bash scripts/run_network_studio.sh doctor` to check prerequisites and the bundled template.
3. Install or refresh the workspace with `bash scripts/run_network_studio.sh install "<workspace-path>"`.
4. If the user wants a menu bar item and uses SwiftBar, add `--swiftbar-plugins-dir ~/SwiftBarPlugins` to the install command.
5. Use `bash scripts/run_network_studio.sh inspect` to review the template and installed layout.
6. After install, run `bash scripts/run_network_studio.sh open` to trigger a fresh scan and open the dashboard.
7. For a continuous watcher, run `bash scripts/run_network_studio.sh watch` or add flags such as `--interval 30 --resolve`.
8. Keep the workspace local-first and honest about uncertainty.

## Workflow

### Choose The Surface

- `network-studio-workspace`: install or refresh the portable workspace in a user-chosen folder
- `swiftbar-plugin`: wire or repair the compact SwiftBar surface that points at the installed workspace
- `support-only`: explain the most reliable network-check path without installing anything

### Install Or Update The Portable Workspace

- Use `scripts/run_network_studio.sh install` for the normal create-or-refresh path.
- Drop to `scripts/install_network_studio.py` only when you need the lower-level copy step.
- Preserve `device-labels.json` if it already exists.
- Preserve `logs/` contents. Do not delete history unless the user asks.
- Re-run the installer against the same workspace when the user asks to update an existing install.

### Wire SwiftBar

- Prefer pointing SwiftBar directly at `<workspace>/swiftbar` if the user is comfortable changing the plugin directory.
- If the user already uses `~/SwiftBarPlugins`, pass `--swiftbar-plugins-dir ~/SwiftBarPlugins`. The installer writes a thin wrapper there that calls the workspace plugin.

### Product Boundaries

- Use only on networks the user owns or administers.
- Explain that the portable workspace is LAN presence monitoring, not deep packet inspection.
- Recommend `brew install nmap` for more reliable portable-workspace discovery, but do not block on it.
- Note that dashboard links and label paths are generated from the installed workspace, so moving the workspace later requires a refresh or reinstall.
- Keep scans, labels, and trust explanations local by default. Do not add covert telemetry, network exfiltration, or surveillance framing.

## Resources

- `scripts/run_network_studio.sh`: repo-native doctor, inspect, install, refresh, open, and watch helper for the portable workspace.
- `scripts/install_network_studio.py`: copies the portable workspace, preserves user state, and optionally installs a SwiftBar wrapper.
- `references/project-map.md`: default workspace, main files, and validation notes for the portable workspace.
- `assets/workspace/`: bundled template for the watcher, dashboard builder, and SwiftBar plugin. Read or patch these files only when setup or behavior needs to change.
