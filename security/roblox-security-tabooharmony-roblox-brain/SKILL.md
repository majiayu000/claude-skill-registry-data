---
name: roblox-security
description: "Use when auditing or hardening Roblox code against exploits: authority, remotes, economy, purchases, and DataStore flows."
when_to_use: "Also for security reviews, cheaters or exploiters, duplicated items or currency, trusting client values, admin commands, and pre-release audits."
last_reviewed: 2026-10-14
sources:
  - https://create.roblox.com/docs/ui/text-filtering
  - https://create.roblox.com/docs/scripting/security/security-tactics
  - https://create.roblox.com/docs/scripting/security/client-server-boundary
  - https://create.roblox.com/docs/projects/server-authority
  - https://create.roblox.com/docs/projects/server-authority/techniques
  - https://create.roblox.com/docs/reference/engine/classes/Players
  - https://create.roblox.com/docs/scripting/capabilities
  - original
  - https://raw.githubusercontent.com/Roblox/creator-docs/main/content/en-us/reference/engine/classes/Player.yaml
  - https://raw.githubusercontent.com/Roblox/creator-docs/main/content/en-us/reference/engine/classes/SocialService.yaml
---

# Roblox Security

## When to Load

Load for authority, remote abuse, economy, saves, bans, or sandboxing audits. Remote validation/rate limits: `roblox-networking`.

## Quick Reference

**Core:** Client is always compromised. The server remains the source of truth, but the implementation depends on the authority model.

### Authority Models

- **Classic replication:** validate client requests against server state. Never trust client damage, currency, inventory, permissions, or positions.
- **Server Authority:** `Workspace.AuthorityMode = Server`: the server owns core simulation while clients predict and recover from misprediction. Use `BindToSimulation()` (needs `UseFixedSimulation`), not blanket `Heartbeat` correction. Cheap for stock characters, rewrite-scale for authored simulation (full.md).
- **Both:** validate attacks, purchases, teleports, permissions, and custom remotes at the server boundary.

### Audit Checklist

**CRITICAL:** Server-authoritative state · Documented authority model · Validate all arg types · Rate limit remotes · Session-lock DataStore · No client currency mutations · ProcessReceipt verification · No secrets in client code

**HIGH:** Validate custom movement and action transitions · BindToClose protection · Atomic trading · Never trust client values · Use InputActions for simulation input in Server Authority projects · Validate ProximityPrompt/ClickDetector/DragDetector like remotes

**MEDIUM:** Server cooldowns · server-computed leaderboards · anti-AFK reward checks · TextService filtering · Script sandboxing for third-party code

### Enforcement

Enforcement is a product decision with appeal implications. `Players:BanAsync`/`UnbanAsync` are server-only and need `Players.BanningEnabled`; `pcall` them. Duration, reason limits and device blocks: full.md.

### Anti-Patterns

Don't obfuscate client code, use `_G` for security, kick without logging, over-validate movement, or rely on client anti-cheat.

See `references/full.md` for detailed examples.
