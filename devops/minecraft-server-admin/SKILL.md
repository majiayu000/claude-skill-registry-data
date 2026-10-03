---
name: minecraft-server-admin
description: "Set up, configure, build, analyze, and operate Minecraft Java Edition servers for 26.x (and 1.21.x) across Paper, Purpur, Folia, Velocity networks, and modded (Fabric/NeoForge) deployments. Use this for Paper/Purpur/Folia/Velocity server building, plugin discovery/download/install planning from Hangar, Modrinth, GitHub, SpigotMC, or BukkitDev, plugin marketplace/source review, server zip/folder analysis, server archetype design (lobby, SMP, creative, minigames, proxy network), plugin compatibility/configuration planning, performance tuning, backups, incidents, Docker/Pterodactyl patterns, and security hardening. Use for Java server infrastructure and plugin operations, not for writing plugin or mod code."
---

# Minecraft Server Administration Skill

## Scope and Routing Boundaries

### Routing Boundaries
- `Use when`: the task is infrastructure or live operations for Java Minecraft servers (deployment choice, server buildout, plugin sourcing, plugin installation planning, plugin compatibility, tuning, backups, proxying, security, incident response, or existing server folder/zip analysis).
- `Do not use when`: the task is writing plugin code (`minecraft-plugin-dev`) or writing mods/loaders (`minecraft-modding`, `minecraft-multiloader`).
- `Do not use when`: the task is WorldEdit command workflows (`minecraft-worldedit-ops`) or EssentialsX workflow/policy design (`minecraft-essentials-ops`).
- `Do not use when`: the task is datapack/resource-pack authoring (`minecraft-datapack`, `minecraft-resource-pack`).
- `Do not use when`: the task is Bedrock Dedicated Server operations (`minecraft-bedrock-server-admin`) or Geyser/Floodgate crossplay setup (`minecraft-crossplay-ops`).
- `Do not use when`: the task is a bot playthrough of a live server (`minecraft-bot-qa`).

## Support Assets

- Read `references/deployment-checklists.md` when the task is an incident, rollout window, proxy change, or recovery drill and you need a compact checklist before acting.
- Read `references/plugin-marketplaces.md` when choosing, downloading, auditing, or updating plugins from Hangar, Modrinth, GitHub Releases, SpigotMC, BukkitDev, or project websites.
- Read `references/server-archetypes.md` when designing a lobby, survival/SMP, creative/build, minigame, proxy network, or staging/test server.
- Use `scripts/analyze-java-server.py` when the user provides an existing Java server folder or zip and needs a plugin/configuration report.

---

## Java Server Orchestration and Delegation

Treat this skill as the Java server/plugin operations orchestrator. Keep these tasks here:

- server jar selection, Java runtime checks, startup commands, Docker/Pterodactyl setup, file layout, and backups
- plugin marketplace discovery, source trust review, direct-download/manual-download decisions, and install/update rollout planning
- server archetype design for lobby, survival/SMP, creative/build, minigame, proxy network, and staging servers
- server folder or zip inspection, plugin inventory, dependency warnings, duplicate jar detection, and configuration gap reports

Delegate specialized work when the prompt narrows to a tool or implementation surface:

- `minecraft-permissions-admin`: LuckPerms groups, tracks, contexts, inheritance, temporary grants, audits, or rollback policy.
- `minecraft-essentials-ops`: EssentialsX homes, warps, kits, moderation, economy, and command policy.
- `minecraft-worldedit-ops`: WorldEdit selections, schematics, brushes, masks, paste safety, or in-world edit operations.
- `minecraft-crossplay-ops`: Geyser/Floodgate placement, authentication mode, Bedrock client joining, and Java-to-Bedrock resource-pack delivery.
- `minecraft-plugin-dev`: writing or modifying custom Java plugin code, Paper API usage, scheduler logic, commands, listeners, or plugin tests.

For large prompts, decompose the work explicitly. Example: analyze the server folder here, route LuckPerms policy to `minecraft-permissions-admin`, route EssentialsX kit/economy setup to `minecraft-essentials-ops`, then return here for staged rollout, backups, and startup-log verification.

How to delegate depends on where this skill is running:

- In the main agent on a host with subagents, send each delegated part to the `minecraft-java-ops` subagent as a separate brief (use `minecraft-task-router` for the brief format and for work that also needs Bedrock, code or QA skills).
- Inside a subagent, do not delegate. Finish what this skill covers and return `needs-other-skill` with a handoff note for the rest.
- On a host without subagents, load the specialist skill yourself, one at a time, and keep this skill's order: analysis, backup, staging, verification, rollout.

---

## Workflow: Analyze Existing Server Folder or Zip

When the user provides a Java server directory or zip, inspect before recommending plugin changes:

```bash
python3 ./scripts/analyze-java-server.py \
  --input /path/to/server-or-archive.zip \
  --output server-report.json \
  --format json \
  --target-version 26.2 \
  --server-type auto
```

Use Markdown output for handoff reports:

```bash
python3 ./scripts/analyze-java-server.py \
  --input /path/to/server \
  --output server-report.md \
  --format md \
  --target-version 26.2
```

Review the report for:

- detected server type and important config files
- installed plugin metadata from `plugin.yml`, `paper-plugin.yml`, and `velocity-plugin.json`
- missing hard dependencies, duplicate plugin names, missing config folders, suspicious jars, and Folia compatibility warnings
- world, datapack, log, backup, and proxy hints
- recommended next actions before downloading or changing plugins

The analyzer is intentionally read-only. It never executes jars, never downloads plugins, and never modifies the inspected server.

---

## Deployment Decision Matrix

Use this table first. Pick a deployment type before changing configs.

| Deployment profile | Recommended stack | Pick this when | Watch-outs |
|---|---|---|---|
| Small SMP on Paper | Paper only | Up to ~30 concurrent players, broad plugin compatibility, low ops overhead | Do not over-tune early; profile before changing many defaults |
| Larger public Paper server | Paper + Spark + stricter plugin/change control | Public server with frequent joins, moderate plugin set, uptime matters | Plugin sprawl is the top TPS risk |
| Velocity-backed network | Velocity + multiple Paper backends | Hub/minigame/factions split across servers, need shared entrypoint | Forwarding/auth mismatches can block joins |
| Purpur gameplay-heavy server | Purpur (optionally behind Velocity) | You want gameplay knobs exposed in config without custom plugin code | Extra toggles increase misconfiguration risk |
| Folia high-concurrency server | Folia + Folia-compatible plugins only | Very high concurrency with region-threading goals | Many plugins are not Folia-safe |
| Fabric/NeoForge mod server | Fabric or NeoForge server build | You require loader mods, custom content, modpack behavior | Bukkit/Paper plugins do not apply |

### Deployment Type Routing

- Small SMP and most public plugin servers: use Paper baseline first.
- Use Purpur only when you explicitly need Purpur gameplay controls.
- Use Folia only when plugin compatibility has been validated for region-threading.
- Use Velocity when one process is not enough or you need separate backend roles.
- Use Fabric/NeoForge when the requirement is mod-driven, not plugin-driven.

---

## Playbook: Performance Tuning

### Step 1: Establish baseline

Collect a baseline before edits:

```bash
free -h
top -b -n 1 | head -n 25
```

In server console:

```bash
tps
mspt
spark healthreport
```

Record:
- peak player count
- MSPT at idle and at peak activity
- top plugins by CPU from Spark report

### Step 2: Profile the real bottleneck

Use Spark instead of guesswork:

```bash
spark profiler --timeout 180
spark tps
spark tickmonitor --interval 10
```

Then identify whether the issue is:
- plugin task load
- entity count / mob farm pressure
- chunk generation / disk I/O
- garbage-collection pauses

### Step 3: Apply targeted fixes

Do not tune everything at once. Apply one group at a time.

1. Chunk and simulation pressure:
- lower `view-distance` and `simulation-distance` first
- pre-generate worlds for survival-heavy maps

1. Entity pressure:
- adjust despawn ranges and mob-spawn behavior in Paper world config
- cap problematic entities where appropriate

1. Plugin pressure:
- disable or replace top offenders from Spark traces
- reduce async task frequency where plugin settings allow

### Step 4: Use stable startup flags

For Java 25 on Paper/Purpur 26.x (use Java 21 for servers still on 1.21.x):

```bash
java -Xms10G -Xmx10G \
  -XX:+UseG1GC \
  -XX:+ParallelRefProcEnabled \
  -XX:MaxGCPauseMillis=200 \
  -XX:+UnlockExperimentalVMOptions \
  -XX:+DisableExplicitGC \
  -XX:+AlwaysPreTouch \
  -XX:G1NewSizePercent=30 \
  -XX:G1MaxNewSizePercent=40 \
  -XX:G1HeapRegionSize=8M \
  -XX:G1ReservePercent=20 \
  -XX:G1HeapWastePercent=5 \
  -XX:G1MixedGCCountTarget=4 \
  -XX:InitiatingHeapOccupancyPercent=15 \
  -XX:G1MixedGCLiveThresholdPercent=90 \
  -XX:G1RSetUpdatingPauseTimePercent=5 \
  -XX:SurvivorRatio=32 \
  -XX:+PerfDisableSharedMem \
  -XX:MaxTenuringThreshold=1 \
  -Dfile.encoding=UTF-8 \
  -jar server.jar --nogui
```

For under 12 GB memory budgets, reduce heap and use smaller region size.

### Step 5: Verify improvements

After each change set:

```bash
spark tps
spark healthreport
```

Keep the change only if MSPT/tick stability improves under representative load.

---

## Playbook: Plugin Operations

Use `references/plugin-marketplaces.md` before adding or updating plugins. Prefer trusted public sources that expose clear version, platform, dependency, license, and release provenance. Do not assume paid, authenticated, or license-restricted resources can be downloaded automatically; provide manual steps instead.

### Safe plugin change workflow

1. Build a plugin inventory:
- plugin name and version
- required dependencies
- minimum server version

1. Stage updates:
- apply plugin updates in staging first
- run smoke checks: joins, teleports, economy, permissions, saves

1. Production rollout window:
- announce maintenance window
- stop server cleanly
- snapshot plugin jars and config
- deploy update batch

1. Post-rollout verification:
- watch startup logs for API warnings
- run command and permission sanity checks
- track TPS/MSPT for 15-30 minutes

### Rollback checklist

- Keep previous plugin directory snapshot.
- If severe regression occurs:
  - stop server
  - restore prior plugin jars/configs
  - start and confirm login/world integrity
- Document failing plugin/version pair for future blocks.

---

## Playbook: Server Archetype Planning

Use `references/server-archetypes.md` for practical starting stacks. Pick the server role before choosing plugins; a lobby, SMP, creative/build server, minigame backend, proxy network, and staging environment have different plugin risk profiles.

For every archetype:

1. Define player journey and administrative controls.
2. Choose the minimal plugin stack that supports that journey.
3. Check Minecraft version, server type, Java version, hard dependencies, soft dependencies, Folia safety, and release recency.
4. Stage the exact plugin set, generate configs, and review logs before production rollout.
5. Keep rollback snapshots of `plugins/`, `config/`, and server properties.

---

## Playbook: Proxy and Forwarding (Velocity)

### Velocity baseline

`velocity.toml` essentials:

```toml
bind = "0.0.0.0:25565"
online-mode = true
player-info-forwarding-mode = "modern"
forwarding-secret-file = "forwarding.secret"
```

### Backend server requirements

`server.properties` on backend:

```properties
online-mode=false
enforce-secure-profile=false
```

Paper backend forwarding support (`config/paper-global.yml`):

```yaml
proxies:
  velocity:
    enabled: true
    online-mode: true
    secret: "paste-the-shared-forwarding-secret-here"
```

Use the same secret value stored in Velocity's `forwarding.secret` file; the backend
config takes the secret string itself, not a file path.

### Validation runbook

1. Confirm proxy port is reachable from clients.
2. Confirm backend is firewalled from direct internet access.
3. Join through proxy and verify:
- UUID consistency
- skin/profile forwarding
- plugin permission behavior

### Common proxy incidents

- "Invalid player info forwarding":
  - mismatch in forwarding mode or shared secret between Velocity and backend.
- Random auth/session failures:
  - mixed `online-mode` expectations or direct backend exposure.

---

## Playbook: Backup and Recovery

### Backup policy template

| Asset | Frequency | Retention | Notes |
|---|---|---|---|
| World folders (`world*`) | Hourly incremental + daily full | 7 daily, 4 weekly | Highest priority |
| `plugins/` and `config/` | Daily | 14 daily | Required for quick rollback |
| Proxy config/secrets | Daily | 30 daily | Store encrypted off-host |
| Container/orchestration files | On change + weekly | 8 weeks | Git-tracked where possible |

### Example backup script

```bash
#!/usr/bin/env bash
set -euo pipefail

DATE="$(date +%Y-%m-%d_%H-%M-%S)"
BACKUP_ROOT="/backups/minecraft"
SERVER_ROOT="/srv/minecraft"
DEST="${BACKUP_ROOT}/${DATE}"

mkdir -p "$DEST"
tar -czf "${DEST}/worlds.tar.gz" -C "$SERVER_ROOT" world world_nether world_the_end
tar -czf "${DEST}/plugins-config.tar.gz" -C "$SERVER_ROOT" plugins config
cp "$SERVER_ROOT/server.properties" "$DEST/server.properties"
```

### Recovery drill (must be tested)

1. Stop server.
2. Restore selected backup to staging directory.
3. Validate ownership/permissions.
4. Start server in maintenance mode.
5. Verify:
- world spawn loads
- player data is readable
- key plugins initialize
1. Reopen to players.

Define targets:
- `RPO` (acceptable data loss window)
- `RTO` (acceptable restore duration)

---

## Playbook: Live Troubleshooting

### Incident triage flow

1. Classify incident:
- crash on startup
- severe lag / TPS collapse
- join/auth failures
- memory/disk pressure

1. Capture evidence first:

```bash
df -h
free -h
```

From server/proxy console:

```bash
spark tps
spark healthreport
```

1. Stabilize:
- stop risky rollout changes
- disable newest suspect plugin first
- reduce player impact (maintenance mode, temporary queue, restricted worlds)

1. Recover and document:
- apply rollback or hotfix
- document root cause and permanent preventive action

### Fast symptom map

| Symptom | First checks | Typical root cause |
|---|---|---|
| Startup crash after plugin update | latest logs, plugin dependency chain | incompatible plugin/API mismatch |
| High MSPT only at peak hours | Spark profiler, entity/chunk stats | mob farms, heavy scheduled tasks, chunk I/O |
| Players cannot join via proxy | forwarding mode + secret + backend exposure | Velocity/backend config mismatch |
| Periodic hard lag spikes | GC pauses + autosave + backup overlap | memory pressure, backup I/O contention |

---

## Operational Config Reference

### `server.properties` high-impact keys

```properties
max-players=100
view-distance=10
simulation-distance=8
sync-chunk-writes=true
max-tick-time=60000
enable-rcon=false
```

### `bukkit.yml` and `spigot.yml`

Use Spigot/Bukkit docs as authoritative for version-specific defaults and side effects.
Tune conservatively and re-measure after every change set.

### Paper config files

- `config/paper-global.yml`
- `config/paper-world-defaults.yml`

Adjust these only after profiling identifies an actionable bottleneck.

---

## Deployment Patterns

### Docker Compose (Paper)

```yaml
services:
  paper:
    image: itzg/minecraft-server:java25
    container_name: mc-paper
    environment:
      EULA: "TRUE"
      TYPE: "PAPER"
      VERSION: "26.2"
      MEMORY: "10G"
    ports:
      - "25565:25565"
    volumes:
      - ./data:/data
    restart: unless-stopped
```

### Pterodactyl/Wings notes

- Keep startup command and memory allocations consistent with tested JVM flags.
- Pin panel and Wings versions to supported combinations.
- Validate backup mount and restore workflow before production.

---

## Security Hardening Checklist

- Keep `online-mode=true` unless proxy forwarding requires backend `online-mode=false`.
- Never expose backend Paper ports directly when using Velocity.
- Restrict RCON and panel/admin surfaces by firewall/IP allowlist.
- Rotate secrets (`forwarding.secret`, panel credentials, backup credentials).
- Keep plugin sources trusted; verify checksum/release source before install.
- Maintain off-host encrypted backups.
- Keep Java runtime and host OS patched.

---

## References

### Paper (primary)

- https://docs.papermc.io/paper/
- https://docs.papermc.io/paper/admin
- https://docs.papermc.io/paper/profiling/

### Spigot/Bukkit (primary config reference)

- https://www.spigotmc.org/wiki/spigot-configuration/
- https://www.spigotmc.org/wiki/bukkit-configuration/
- https://www.spigotmc.org/wiki/start-up-parameters/

### Proxy and ecosystem docs

- https://docs.papermc.io/velocity/
- https://docs.papermc.io/paper/adding-plugins/
- https://hangar.papermc.io/
- https://docs.modrinth.com/api/
- https://spark.lucko.me/docs
- https://geysermc.org/wiki/geyser/
- https://pterodactyl.io/project/introduction.html
