---
name: minecraft-plugin-dev
description: Guide for building, scaffolding, editing, and debugging Minecraft server plugins for Paper, Spigot, and Folia, in Java or Kotlin. Use this whenever the user wants to create a Minecraft plugin, write or edit a plugin.yml or paper-plugin.yml, register Bukkit/Paper events or Brigadier commands, work with the Paper API (items, inventories, PDC, scheduling), set up a Gradle or Maven plugin project, add Folia (regionized threading) support, or asks anything about PaperMC/Spigot/Bukkit plugin development generally — even if they don't say the word "plugin" explicitly (e.g. "add a heal command to my server", "make an admin GUI in Minecraft", "why does my listener not fire"). Covers the 2026 Paper hard-fork changes and current API versions, plus Kotlin-specific setup (coroutines, Folia-safe dispatchers, JSpecify null-safety interop).
---

# Minecraft Plugin Development (Paper / Spigot / Folia)

## Current Version Snapshot — check this first, update this first

This is the one block in the skill that goes stale on its own schedule, independent of everything else here. When a new Minecraft/Paper drop ships, this is the only section that necessarily needs an edit — the rest of the skill is written to stay correct across version bumps.

| Fact | Value | Last verified |
|---|---|---|
| Latest Minecraft release | `26.3` ("Wilderness Bound", Java Edition) | 2026-09-17 |
| Latest Paper channel for `26.3` | **Experimental only** — not yet promoted to Paper's stable channel as of last verification | 2026-09-17 |
| Latest stable Paper line | `26.2` | 2026-09-17 |
| Java requirement to run the server | **25** | 2026-08-16 |

**What this means for any task right now:** for a plugin someone is actually going to run in production, target `26.2` (stable) and mention that `26.3` support exists in Paper's experimental channel if they want to test ahead of stable. For someone explicitly testing against the newest drop or reporting an issue specific to it, `26.3` experimental is the right target — but say plainly that it's experimental (Paper's own guidance: "you should always serve & use stable builds — experimental builds are prone to error and do not receive support"). Don't silently upgrade every `26.2` reference in a conversation to `26.3` without checking which one the situation actually calls for.

Check `https://papermc.io/downloads/paper` for the current channel status before treating this table as gospel — it can change within days of a Minecraft release, faster than this skill will be updated in turn.

## Orientation

This skill targets the **post-hard-fork Paper ecosystem** as of the 2026 `YEAR.DROP` versioning era. Two facts change how you should approach almost every task here:

1. **Paper is the default target.** Unless the user explicitly needs Spigot compatibility, generate Paper API code — it's a superset of Bukkit/Spigot and is where all active development happens. Only fall back to plain Bukkit/Spigot API calls if the user says they need Spigot compatibility.
2. **Versions look different now.** Minecraft/Paper versions are `YEAR.DROP[.PATCH]` (e.g. `26.2`, `26.3`), not `1.21.x`. Paper server jars are Mojang-mapped (unobfuscated) as of `26.1`+, and Paper requires **Java 25** to run. If you see or write code assuming `1.2x` version strings or obfuscated internal names, stop and flag it — that's now-outdated. See the version snapshot above for which specific drop is current and which channel (stable/experimental) it's in.

## Deciding Java vs Kotlin

Ask (or infer from existing project files — `build.gradle.kts` with a `kotlin("jvm")` plugin, `.kt` sources, etc.) which language the user wants:

- **Java** → follow `references/paper-api-guide.md` directly.
- **Kotlin** → read `references/kotlin-plugin-guide.md` **in addition to** the Java guide. Kotlin plugins use the exact same Paper API surface; the Kotlin reference only covers what's *different* (project setup, stdlib shading, coroutines/Folia interaction, null-safety interop, idiom conversions). Don't duplicate the Java guide's content when writing Kotlin — translate idiomatically instead (data classes where sensible, no unnecessary `!!`, trailing lambdas for listeners/schedulers, etc.).

If unclear and no existing project gives a signal, ask the user once rather than guessing — the project scaffold (Gradle plugin blocks, package layout, whether `kotlin-stdlib` needs shading) differs enough that guessing wrong wastes a full setup pass.

## Core workflow for "build me a plugin" style requests

1. **Clarify scope minimally**: target platform (Paper vs Spigot vs Folia-compatible), language (Java/Kotlin), and roughly what the plugin should do. Don't over-ask — one round of questions, then proceed with sensible defaults (Paper + `paper-plugin.yml` unless they need Spigot compat).
2. **Scaffold the project**: build file (Gradle Kotlin DSL by default), `plugin.yml` or `paper-plugin.yml`, main class extending `JavaPlugin`. See references for exact templates.
3. **Implement the feature** using the relevant Paper API area — events, commands (Brigadier via `LifecycleEvents.COMMANDS`), scheduling, PDC, items/data components, inventories, config. Use the **region-aware schedulers** (`GlobalRegionScheduler`/`RegionScheduler`/`EntityScheduler`/`AsyncScheduler`) instead of the legacy `BukkitScheduler` by default — it costs nothing on plain Paper and means the plugin isn't broken on Folia if the user later needs that.
4. **Wire it together** in `onEnable()`/`onDisable()` (or a `PluginBootstrap` for early command registration).
5. **Sanity-check before handing back code**: does it compile against Paper API concepts you're confident about? Flag anywhere you used an experimental/newer API (Brigadier arguments, data components, registries) so the user knows to double-check against current Javadocs (`jd.papermc.io`) if the exact method signature matters for a real build — API surface in these newer areas shifts faster than in the stable Bukkit-inherited API.

## Critical gotchas (don't skip these)

- **Folia is opt-in and separate.** It is *not* merged into Paper and isn't planned to be. Only reach for Folia-specific patterns (region/entity schedulers as a *requirement*, `folia-supported: true`, thread-ownership checks) if the user is actually targeting Folia or explicitly wants forward-compatible code. Otherwise mention it's an option rather than building for it unasked.
- **Don't use obfuscated/Spigot-mapped internal names** (`EntityHuman`, `PacketPlayIn...`, raw NMS reflection against old mappings) in any code targeting `26.1`+ — it will fail to load. If a task needs internals access, point to `paperweight-userdev` rather than hand-rolled reflection.
- **Never block the main or region thread.** File I/O, HTTP, JDBC — always async-schedule these, whichever scheduler family you're using.
- **`plugin.yml` vs `paper-plugin.yml`**: default to `paper-plugin.yml` for new Paper-only plugins (unlocks Brigadier command registration, `folia-supported`, the `libraries:` dependency loader). Use classic `plugin.yml` if the user needs the plugin to also load on Spigot.
- **Treat experimental API confidently but not blindly.** Paper's own docs mark `paper-plugin.yml`, bootstrappers/loaders, and parts of the Command API as experimental. Generate code using them freely (they're the current best practice) but say so when handing off, so the user knows to re-check signatures if something doesn't compile.

## Reference files

- `references/paper-api-guide.md` — the full Java/Paper API reference: project setup, plugin.yml/paper-plugin.yml, lifecycle, events, commands, permissions, scheduling, config, PDC, items/data components, inventories, Adventure/MiniMessage, entities/worlds, registries, plugin messaging, library loading, Folia support, databases, logging, testing, performance, building/shading, publishing, and a full worked example. Read this for any task that touches the Paper API itself.
- `references/kotlin-plugin-guide.md` — Kotlin-specific delta: Gradle setup with the Kotlin plugin, shading `kotlin-stdlib`, JSpecify null-safety interop with the Paper API, coroutine patterns that stay Folia-safe (manual dispatchers and the MCCoroutine library), idiom notes, and the same worked example translated to Kotlin. Read this whenever the user is working in Kotlin, in addition to the Java guide above.
- `references/ecosystem-integrations.md` — Vault/VaultUnlocked (economy), PlaceholderAPI (exposing and consuming placeholders), bStats metrics, update-checking against Modrinth/Hangar/SpigotMC, and packet-level control (PacketEvents vs. ProtocolLib, with a 2026 recommendation toward PacketEvents for new work). Read this whenever the task involves hooking into another plugin/service, adding analytics, checking for updates, or needs packet-level access beyond what events expose.
- `references/reliability-and-troubleshooting.md` — thread-safety pitfalls, error-handling patterns, config/data migration across plugin versions, cyclic dependency loading, and a symptom → cause → fix table for the most common plugin load failures. Read this whenever debugging a load/runtime error, designing a data migration, or when the user asks for the code to be more robust/correct rather than just functional.
- `references/paper-features-and-process.md` — custom recipes, the Dialog API, particle spawning, scoreboards/boss bars/tab list, CI/CD (GitHub Actions publishing to Hangar via `hangar-publish-plugin` and Modrinth via Minotaur), and multi-version support strategies. Read this for these specific feature areas or when setting up a build/release pipeline.

All reference files were compiled from official documentation and cross-checked in mid-August 2026, with the version snapshot above refreshed 2026-09-17 following the `26.3` release. Server-internals-facing APIs (raw NMS, obfuscated mappings, very new Brigadier/data-component/registry/Dialog additions) move fastest — the Dialog API in particular had a method deprecated within a couple of point releases of its own introduction. If a task depends on exact correctness there and the stakes are high (a real production build, not a quick prototype), verify against `https://docs.papermc.io/paper/dev/` and `https://jd.papermc.io/` directly rather than relying solely on these references. Third-party library versions (bStats, PacketEvents, Minotaur, hangar-publish-plugin, etc.) are also worth a quick check against their own repos before pinning in a real build — this skill gives correct-as-of-mid-2026 coordinates, not a guarantee against future releases.

**Keeping this skill current:** when a new Minecraft/Paper drop ships, update the Current Version Snapshot table above first — that alone keeps the skill's guidance correct for 90% of version-sensitive questions. Only touch the reference files themselves if the new drop changed something structural (a new hard-fork-style event, a new required Java version, an API removal) rather than just adding content (new blocks/items/biomes rarely require any edit here at all).
