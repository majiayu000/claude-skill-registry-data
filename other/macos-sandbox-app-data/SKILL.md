---
name: macos-sandbox-app-data
description: >
  Locate, inspect, and safely edit config/data for sandboxed macOS apps that store
  state under ~/Library/Containers and ~/Library/Group Containers instead of an obvious
  config.yaml. Use when an App Store/Flutter/Electron app hides the active config behind
  bundle IDs, JSON controller files, runtime-generated profiles, or subscription-managed
  sources.
tags:
  - macos
  - app-sandbox
  - containers
  - config
  - troubleshooting
version: 1
---

Goal
- Find the real persistent config for a macOS app, not just the first YAML/JSON that looks plausible.
- Distinguish user-editable source files from generated runtime artifacts.
- Make edits in the durable layer that will survive app restart when possible.

Use when
- User says an app has custom rules/config but cannot find where it is stored.
- A macOS app from App Store/TestFlight/Flutter/Electron hides state behind a bundle ID.
- Searching for `config.yaml` in home directory returns nothing useful.
- The app appears to generate runtime YAML/JSON from a separate source profile.

Do not use when
- The app is clearly a plain CLI tool with config already in `~/.config`, `/etc`, or repo-local files.
- The target is an iOS device backup or mobile container, not local macOS app data.

Core model
Most sandboxed macOS apps split state across 3 layers:
1. App container
   - `~/Library/Containers/<bundle-id>/`
   - Often holds app-local caches, Documents, Preferences, and sandbox-private files.
2. Group container
   - `~/Library/Group Containers/group.<bundle-id>/`
   - Often holds shared app data, active profiles, logs, downloaded assets, or service state.
3. Generated runtime state
   - Files regenerated from a source profile or controller JSON.
   - Safe to inspect; often wrong place to edit.

Workflow
1. Identify the app bundle/process first.
   - `mdfind 'kMDItemFSName == "*Clash*"c'`
   - `ps aux | rg -i 'clash|mihomo|sing-box|bundle-id-fragment'`
2. Search likely container roots before broad home scans.
   - `find ~/Library/Containers -maxdepth 3 -iname '*bundle*'`
   - `find ~/Library/Group Containers -maxdepth 3 -iname '*bundle*'`
3. If the app is running, use open files as ground truth.
   - `lsof -p <pid> | rg -i 'yaml|yml|json|plist|profile|config|group containers|containers'`
4. Read controller files before editing anything.
   - Common names: `service.json`, `profiles.json`, `setting.json`, `storage.json`, `*.plist`
   - Look for keys like:
     - `core_path`
     - `current_id`
     - `runtime-profile-save-path`
     - `patch`
     - `url`
5. Classify candidate files.
   - Persistent source profile: user-editable, usually referenced by `core_path` or `current_id`
   - Runtime compiled profile: regenerated, often named like `runtime`, `final`, `patch_final`
   - Metadata/patch overlay: JSON controlling selection, subscriptions, or merge behavior
6. Edit the persistent source, not the generated runtime artifact.
7. Check overwrite risk before finalizing.
   - If profile metadata includes a remote `url` or auto-update flag, manual edits may be overwritten.
8. If the source profile is subscription-managed, look for a patch/overlay layer before telling the user to disable updates.
   - Check JSON/controller files for `profile_patchs.json`, `core_path_patch`, or `core_path_patch_final`.
   - If metadata is thin, inspect app strings for patch evidence:
     - `strings -a /Applications/<App>.app/... | rg 'profile_patch|overwrite-rules|overwrite-sub-rules|add_profile_patch|patch_board'`
   - If a YAML candidate only contains overlay keys such as `prepend`, `append`, or `delete` and lacks `proxies` / `proxy-providers`, do not import it as the main profile. Treat it as a patch layer and attach it to the real subscription/profile via the app's patch metadata.
   - In Clash Mi, `Invalid Clash Yaml file: proxies and proxy-providers not found` is the signature that a patch-only YAML was imported as if it were a full profile.
   - Prefer a no-overwrite patch layer for durable custom rules on top of the subscription when the app exposes one.
9. Verify after edit.
   - Re-read controller file and target profile path.
   - Confirm the app reloads or regenerates runtime config from the edited source.
   - If using a patch layer, confirm it attaches to the current subscription/profile instead of replacing the upstream source.
   - Check logs for permission or port-conflict errors if behavior does not change.

Fast commands
```bash
find "$HOME/Library/Containers" -maxdepth 4 \( -iname '*<app>*' -o -iname '*<bundle>*' \) 2>/dev/null
find "$HOME/Library/Group Containers" -maxdepth 4 \( -iname '*<app>*' -o -iname '*<bundle>*' \) 2>/dev/null
lsof -p <pid> 2>/dev/null | rg -i 'yaml|yml|json|plist|profile|config|group containers|containers'
rg -n 'core_path|current_id|runtime-profile-save-path|patch|url' "$HOME/Library/Group Containers/group.<bundle>"
```

Verification checklist
- Found the active bundle/container, not just a similarly named log file.
- Found the controller file that points to the live profile.
- Identified whether the target file is source or generated runtime.
- Checked whether subscription/update metadata can overwrite edits.
- Avoided reporting runtime artifacts as the primary edit target.

Pitfalls
- Broad `~/Library` searches on macOS trigger many `Operation not permitted` results; narrow scope early.
- Group container may hold the real config while app container only holds caches/preferences.
- A visible `runtime_profile.yaml` or `patch_final.json` is often generated output, not the durable source.
- Some apps store the active path only in JSON, so `config.yaml` searches miss the real target.
- App logs may reveal TCC issues like Full Disk Access requirements; this can block related service behavior.
- Subscription-managed profiles can revert manual edits on refresh.
- If the app has a patch board / overlay mechanism, advising `do not update` is usually second-best; prefer durable no-overwrite patches over hand-editing subscribed YAML.
- User-supplied rule lists may contain invalid Clash syntax like `DOMAIN,http://host:port/,DIRECT` or trailing `/` in `DOMAIN-SUFFIX`; normalize before recommending import.
- If the user gives only a rule overlay list (`prepend`/`append`/`delete`), do not tell them to import it as a standalone Clash config; wire it into the app's patch mechanism instead.

Support files
- `references/clash-mi.md` — concrete observed layout, patch hints, and edit targets for Clash Mi on macOS.
