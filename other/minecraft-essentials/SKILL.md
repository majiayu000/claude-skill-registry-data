---
name: minecraft-essentials
description: Install, upgrade, run, migrate, back up, and troubleshoot Minecraft Java servers. Use when Codex needs to work on a Minecraft-only setup such as Vanilla, Paper, Fabric, plugin compatibility, Java versioning, LAN join info, backups, Bedrock bridging, or moving a local server toward a more stable always-on setup.
---

# Minecraft Essentials

Use this skill for Minecraft Java server work only. This skill is not for general game launchers or unrelated hosting tasks.

## Quick Start

1. Identify the server type first: `vanilla`, `paper`, `fabric`, or an existing mixed setup.
2. Confirm the current world version, Java version, and whether the server is local-only or meant for outside players.
3. Back up the world and key config files before changing jars, plugin stacks, or major versions.
4. Prefer Paper for practical multiplayer servers unless the user explicitly needs pure Vanilla or a Fabric mod stack.
5. When the user wants broad Java client compatibility, treat ViaVersion, ViaBackwards, and ViaRewind as a compatibility layer on top of a modern Java server, not as a true old-version server.

## Workflow

### Audit First

- Inspect the server directory before changing anything.
- Confirm:
  - current jar or launcher
  - `server.properties`
  - world folders
  - plugin or mod folders
  - Java version in use
  - how the server is started today
- If the server already boots, preserve the current run path unless there is a clear reason to replace it.

### Choose The Right Stack

- Use Paper for:
  - stable local servers
  - plugin support
  - performance and admin tooling
  - compatibility plugins like ViaVersion
- Use Vanilla for:
  - minimal pure-Minecraft setups
  - users who do not want plugins
- Use Fabric for:
  - modded setups that depend on Fabric mods
  - cases where plugin ecosystems are not enough
- Do not mix Paper plugins and Fabric mods unless the user explicitly wants a hybrid approach and understands the tradeoffs.

### Versions And Compatibility

- Match the underlying world and server version carefully before upgrading.
- Explain clearly when a compatibility plugin lets older clients join a newer server.
- If the user wants Bedrock support, that is a separate bridge layer such as Geyser, not a Java-version compatibility plugin.
- Before major upgrades:
  - back up the world
  - back up launch scripts
  - call out any likely world format migration

### Required Deliverables

- A clear summary of the current Minecraft setup.
- The chosen server path and why it fits.
- Updated run scripts or launch instructions when needed.
- Join info for:
  - same machine
  - same LAN
  - hostname if available
- A backup path before risky changes.

### Plugin And Mod Guidance

- Keep plugin stacks focused. Add only what solves the actual player/admin need.
- Common Paper lanes:
  - compatibility: ViaVersion, ViaBackwards, ViaRewind
  - Bedrock bridge: Geyser, Floodgate
  - admin: permissions, moderation, backups
  - quality of life: homes, claims, anti-grief
- Verify plugin version compatibility with the target server version before adding them.

### Networking And Safety

- For LAN-only setups, surface `localhost`, the machine LAN IP, and the hostname.
- For internet exposure, explain the difference between local hosting, port forwarding, and VPS hosting.
- Call out that opening a Minecraft server to the public increases security and moderation needs.
- If the user wants 24/7 uptime, prefer moving toward a VPS or managed host instead of pretending a sleeping laptop is reliable infrastructure.

### Editing Guidance

- Keep launch scripts readable and easy to rerun.
- Prefer one obvious launcher per server mode.
- Do not delete world data, dimension folders, or plugin data unless the user explicitly asks.
- Explain migrations plainly, especially world layout changes and compatibility-layer limits.

## Resources

- `scripts/mc_lan_info.sh`: prints same-machine, LAN, and hostname join targets for a local Minecraft server.
- `references/server-modes.md`: when to choose Vanilla, Paper, or Fabric.
- `references/plugin-packs.md`: practical plugin bundles for compatibility, Bedrock, admin, and QoL.
- `references/operations-checklist.md`: backup, upgrade, migration, and exposure checklist.
