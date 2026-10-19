---
name: axolotl-launcher
description: Discover and launch AXO / Axolotl Launcher Minecraft instances on Windows, including listing instances, resolving game directories, and entering an explicitly requested save. Use for launcher startup even when no Photon or VFX work is requested.
---

# AXO / Axolotl Launcher

Use the scripts in this skill directory. Instance IDs come from `axolotl_config.json`; profile folder names and display names are not launch IDs. Never print complete launcher configs, account databases, access tokens, or full Java command lines.

## Discover and select

Run `scripts/list-instances.ps1` first. It reads selected instance metadata, the registered Axolotl protocol executable, and bounded profile locations. The optional `references/local-paths.json` contains machine-local path hints; the checked-in copy is intentionally empty. Add only launcher and profile paths needed on the current machine, or pass `-ProfilesRoot`.

Choose the exact instance named by the user. Duplicate display names require the game directory to disambiguate. Do not search entire drives or read launcher databases when profile metadata is sufficient. An empty inventory means discovery failed, not that no instances exist; inspect the registered executable and ask for a bounded library directory if needed.

## Launch

`scripts/start-instance.ps1 -GameDir <inventory gameDir> -PlanOnly` validates the selection and reports whether that client is already running without starting it.

After the user requests opening the selected instance, omit `-PlanOnly`. The script uses the registered executable and the `axolotl://launch/instance/<escaped instance_id>` URI, then waits for a matching Java game directory. It preserves existing clients and reuses a matching running client. Process existence confirms client startup only; it does not prove title-screen readiness or world entry.

For an explicitly requested local save, add `-WorldName <save-folder-name>`. Check that `saves/<name>/level.dat` exists first; do not create a world implicitly. This delegates to `../minecraft-vfx-automation/scripts/launch-axolotl-quickplay.ps1`, which is Forge-specific, uses MCP-HELPER's default local endpoint on port 9876, and requires live world confirmation. Do not present it as generic Fabric/NeoForge quick-play. If a selected client is already running, preserve it and inspect its current world rather than restarting it.

A missing quick-play helper does not prevent ordinary instance launch. Use a matching Helper endpoint, client logs, or an allowed UI tool to verify readiness; do not infer successful world entry from a window title. Honor any user prohibition on GUI automation.

## Local configuration

The script reads `references/local-paths.json` for optional fallback paths. Keep this file local to the installation and do not commit personal paths. Registry discovery and `-ProfilesRoot` can be used without editing it.
