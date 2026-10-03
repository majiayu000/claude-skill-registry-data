---
name: minecraft-plugin-dev
description: "Develop Minecraft server plugins using the Paper/Bukkit/Spigot API for Minecraft 26.x (and the 1.21.x line). Handles creating Paper plugins with JavaPlugin, event listeners with @EventHandler, commands, schedulers (sync/async/Folia-safe), Persistent Data Container (PDC), Adventure text components, Vault economy integration, BungeeCord/Velocity messaging, plugin.yml and paper-plugin.yml configuration, YAML config management, and Paper-specific enhancement APIs. Targets Paper API 26.2 (Java 25; 1.21.x servers use Java 21) with Gradle (Kotlin DSL). Plugins run server-side only and do not require client installation. Use when creating or modifying Minecraft server plugins, working with Paper/Bukkit/Spigot APIs, or developing server-side features involving event handlers, commands, or plugin.yml configuration."
---

# Minecraft Plugin Development Skill

## Platform Overview

| Platform | Base API | Notes |
|----------|----------|-------|
| **Paper** | Bukkit/Spigot + Paper extensions | Recommended; async chunk loading, Adventure native |
| **Spigot** | Bukkit + Spigot extensions | Legacy; fewer APIs, slower |
| **Bukkit** | Base API only | Avoid for new plugins |
| **Folia** | Paper fork | Region-threaded; requires special scheduler APIs |

> Paper is the recommended target. Paper includes all Bukkit and Spigot APIs plus
> significant performance improvements and additional APIs.

### Routing Boundaries
- `Use when`: the target is server-side Paper/Bukkit/Spigot plugin behavior with JavaPlugin APIs.
- `Do not use when`: the task requires client-side installable mods or loader APIs (`minecraft-modding` / `minecraft-multiloader`).
- `Do not use when`: the task is pure vanilla datapack/command content (`minecraft-datapack` / `minecraft-commands-scripting`).
- `Do not use when`: the task is a Bedrock add-on or Script API pack (`minecraft-bedrock-addon-dev`).
- `Do not use when`: the task is installing, configuring or operating an existing plugin (`minecraft-server-admin`, `minecraft-permissions-admin`, `minecraft-essentials-ops`).
- `Do not use when`: the task is writing automated tests (`minecraft-testing`) or release pipelines (`minecraft-ci-release`).

## Bundled References

- Read `references/runtime-patterns.md` when the task touches scheduling, Folia support, PDC, Adventure/MiniMessage, YAML config, Vault, or Paper-specific APIs.

---

## Project Setup

### `settings.gradle.kts`
```kotlin
rootProject.name = "my-plugin"
```

### `build.gradle.kts`
```kotlin
plugins {
    java
    id("com.gradleup.shadow") version "8.3.0"
}

group = "com.example"
version = "1.0.0-SNAPSHOT"

repositories {
    mavenCentral()
    maven("https://repo.papermc.io/repository/maven-public/")
    // For Vault (economy API)
    maven("https://jitpack.io")
}

dependencies {
    compileOnly("io.papermc.paper:paper-api:26.2.build.+")
    // Optional: Vault economy/permission integration
    compileOnly("com.github.MilkBowl:VaultAPI:1.7")
}

java {
    toolchain.languageVersion.set(JavaLanguageVersion.of(25))
}

tasks {
    processResources {
        // Substitutes ${version} in plugin.yml with the Gradle project version
        filesMatching(listOf("plugin.yml", "paper-plugin.yml")) {
            expand("version" to project.version)
        }
    }
    shadowJar {
        archiveClassifier.set("")
    }
    build {
        dependsOn(shadowJar)
    }
}
```

### `gradle/wrapper/gradle-wrapper.properties`
```properties
distributionUrl=https\://services.gradle.org/distributions/gradle-8.8-bin.zip
```

---

## Project Layout
```
my-plugin/
├── build.gradle.kts
├── settings.gradle.kts
├── gradle/
│   └── wrapper/
│       └── gradle-wrapper.properties
└── src/main/
    ├── java/com/example/myplugin/
    │   ├── MyPlugin.java          ← main class (extends JavaPlugin)
    │   ├── listeners/
    │   │   └── PlayerListener.java
    │   ├── commands/
    │   │   └── MyCommand.java
    │   └── managers/
    │       └── DataManager.java
    └── resources/
        ├── plugin.yml
        ├── paper-plugin.yml      ← optional, Paper-only metadata
        └── config.yml
```

---

## Core Files

### `plugin.yml` (Bukkit-compatible default)
```yaml
name: MyPlugin
version: "${version}"
main: com.example.myplugin.MyPlugin
description: An example Paper plugin
author: YourName
website: https://github.com/example/my-plugin
api-version: '26.2'

commands:
  myplugin:
    description: Main plugin command
    usage: /myplugin <subcommand>
    permission: myplugin.use
    aliases: [mp]

permissions:
  myplugin.use:
    description: Allows use of /myplugin
    default: true
  myplugin.admin:
    description: Admin access
    default: op
```

> Minecraft Java now uses year-based versions (26.1, 26.2, 26.3). Use `api-version: '26.2'`
> to target Paper 26.2. Older servers on the 1.21 line still use `api-version: '1.21'`
> or `'1.21.<patch>'`.
> In this repo, the validator accepts `1.21`, positive `1.21.<patch>` values, and `26.<minor>` or
> `26.<minor>.<hotfix>` values. A 26.x minor newer than the documented example (`26.2`) is allowed
> but warned, so new Paper releases do not force an immediate validator edit.
> Values such as `1.21.0`, `1.21.01`, `1.22` or `26.0` are rejected.
> Paper 26.x needs Java 25. Paper 26.3 is still beta; confirm the build on https://papermc.io/downloads/paper before you pin it.

### `paper-plugin.yml` (Paper-only metadata)

Use `paper-plugin.yml` when you need Paper-specific metadata such as `folia-supported`
or server/bootstrap dependency ordering. Keep `plugin.yml` if you must stay portable
to Bukkit-derived servers that do not understand the Paper-specific file.

```yaml
name: MyPlugin
version: "${version}"
main: com.example.myplugin.MyPlugin
api-version: '26.2'
folia-supported: true

dependencies:
    server:
        Vault:
            load: BEFORE
            required: false
```

### Main Plugin Class
```java
package com.example.myplugin;

import com.example.myplugin.commands.MyCommand;
import com.example.myplugin.listeners.PlayerListener;
import org.bukkit.plugin.java.JavaPlugin;

public final class MyPlugin extends JavaPlugin {

    private static MyPlugin instance;

    @Override
    public void onEnable() {
        instance = this;
        saveDefaultConfig();

        // Register listeners
        getServer().getPluginManager().registerEvents(new PlayerListener(this), this);

        // Register commands
        var cmd = getCommand("myplugin");
        if (cmd != null) {
            cmd.setExecutor(new MyCommand(this));
            cmd.setTabCompleter(new MyCommand(this));
        }

        getLogger().info("MyPlugin enabled!");
    }

    @Override
    public void onDisable() {
        getLogger().info("MyPlugin disabled.");
    }

    public static MyPlugin getInstance() {
        return instance;
    }
}
```

---

## Event Listeners

```java
package com.example.myplugin.listeners;

import com.example.myplugin.MyPlugin;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import org.bukkit.event.EventHandler;
import org.bukkit.event.EventPriority;
import org.bukkit.event.Listener;
import org.bukkit.event.entity.PlayerDeathEvent;
import org.bukkit.event.player.PlayerJoinEvent;
import org.bukkit.event.player.PlayerQuitEvent;

public class PlayerListener implements Listener {

    private final MyPlugin plugin;

    public PlayerListener(MyPlugin plugin) {
        this.plugin = plugin;
    }

    @EventHandler(priority = EventPriority.NORMAL, ignoreCancelled = true)
    public void onPlayerJoin(PlayerJoinEvent event) {
        event.joinMessage(
            Component.text(event.getPlayer().getName() + " joined!", NamedTextColor.GREEN)
        );
    }

    @EventHandler
    public void onPlayerQuit(PlayerQuitEvent event) {
        event.quitMessage(
            Component.text(event.getPlayer().getName() + " left.", NamedTextColor.YELLOW)
        );
    }

    @EventHandler(ignoreCancelled = true)
    public void onPlayerDeath(PlayerDeathEvent event) {
        // Modify death message using Adventure components
        event.deathMessage(
            Component.text("☠ ", NamedTextColor.RED)
                .append(Component.text(event.getPlayer().getName(), NamedTextColor.WHITE))
                .append(Component.text(" died!", NamedTextColor.RED))
        );
    }
}
```

### EventPriority order
`LOWEST → LOW → NORMAL → HIGH → HIGHEST → MONITOR`  
Use `MONITOR` for logging only (never modify outcome). Use `ignoreCancelled = true` unless
you have a specific reason to handle cancelled events.

### Cancellable events
```java
@EventHandler
public void onBlockBreak(BlockBreakEvent event) {
    if (event.getPlayer().hasPermission("myplugin.break.deny")) {
        event.setCancelled(true);
        event.getPlayer().sendMessage(Component.text("You cannot break blocks!", NamedTextColor.RED));
    }
}
```

---

## Commands

```java
package com.example.myplugin.commands;

import com.example.myplugin.MyPlugin;
import net.kyori.adventure.text.Component;
import net.kyori.adventure.text.format.NamedTextColor;
import org.bukkit.command.Command;
import org.bukkit.command.CommandExecutor;
import org.bukkit.command.CommandSender;
import org.bukkit.command.TabCompleter;
import org.bukkit.entity.Player;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

import java.util.List;

public class MyCommand implements CommandExecutor, TabCompleter {

    private final MyPlugin plugin;

    public MyCommand(MyPlugin plugin) {
        this.plugin = plugin;
    }

    @Override
    public boolean onCommand(@NotNull CommandSender sender, @NotNull Command command,
                             @NotNull String label, @NotNull String[] args) {
        if (!(sender instanceof Player player)) {
            sender.sendMessage(Component.text("Only players can use this command.", NamedTextColor.RED));
            return true;
        }

        if (!player.hasPermission("myplugin.use")) {
            player.sendMessage(Component.text("No permission.", NamedTextColor.RED));
            return true;
        }

        if (args.length == 0) {
            player.sendMessage(Component.text("Usage: /myplugin <reload|info>", NamedTextColor.YELLOW));
            return true;
        }

        return switch (args[0].toLowerCase()) {
            case "reload" -> {
                plugin.reloadConfig();
                player.sendMessage(Component.text("Config reloaded.", NamedTextColor.GREEN));
                yield true;
            }
            case "info" -> {
                player.sendMessage(Component.text("Version: " + plugin.getDescription().getVersion(), NamedTextColor.AQUA));
                yield true;
            }
            default -> {
                player.sendMessage(Component.text("Unknown subcommand.", NamedTextColor.RED));
                yield false;
            }
        };
    }

    @Override
    public @Nullable List<String> onTabComplete(@NotNull CommandSender sender, @NotNull Command command,
                                                @NotNull String label, @NotNull String[] args) {
        if (args.length == 1) {
            return List.of("reload", "info").stream()
                .filter(s -> s.startsWith(args[0].toLowerCase()))
                .toList();
        }
        return List.of();
    }
}
```

---

## Schedulers

For classic Paper plugins, `BukkitScheduler` is still fine. If you claim Folia support,
route player, entity, region, global, and async work through the matching Folia-aware
scheduler. Keep scheduling behind a small project-local interface when one plugin must
support both Paper and Folia.

See `references/runtime-patterns.md` for copy-ready sync, async, cancelable, and
Folia-safe scheduler examples.

---

## Persistent Data Container (PDC)

PDC stores arbitrary data on any `PersistentDataHolder` (players, entities, items, chunks).
Data is saved with the world and persists across restarts.

Create `NamespacedKey` instances once, keep data types stable after release, and use
PDC for small metadata rather than large datasets. Prefer config files or a database
for large or query-heavy plugin state.

See `references/runtime-patterns.md` for player, item, chunk, and world PDC examples.

---

## Adventure Text Components

Paper uses [Adventure](https://docs.advntr.dev/) natively for all text. No legacy chat colors.
Use `Component` builders for code-owned messages and MiniMessage for config-driven
messages. Avoid legacy `ChatColor` unless the target project already depends on it
for compatibility.

See `references/runtime-patterns.md` for simple messages, hover/click events,
MiniMessage parsing, titles, and action bars.

---

## Configuration (YAML)

### `src/main/resources/config.yml`
```yaml
# Default config
settings:
  max-players: 20
  welcome-message: "<green>Welcome to the server!"
  cooldown-seconds: 30

database:
  host: localhost
  port: 3306
  name: myplugin_db
```

### Accessing config values
Call `saveDefaultConfig()` in `onEnable()`, provide explicit defaults when reading
values, and validate config shape before starting long-running tasks.

### Custom config file
Use custom YAML files only when separating user config from mutable plugin data is
worth the extra file handling. Keep blocking disk writes off hot event paths.

See `references/runtime-patterns.md` for config read/write and custom YAML examples.

---

## Vault Integration (Economy / Permissions)

Declare Vault as `compileOnly`, soft-depend on it in plugin metadata, and disable
economy features cleanly when the service provider is unavailable. Never assume a
Vault-compatible economy plugin is installed just because Vault itself is present.

See `references/runtime-patterns.md` for a minimal economy setup and charge example.

---

## Paper-Specific APIs

Use Paper APIs when they remove main-thread blocking or simplify Adventure-native
behavior. Keep optional plugin integrations behind presence checks and metadata
soft-dependencies.

See `references/runtime-patterns.md` for async chunk loading, custom item meta,
profile lookup, and protection-plugin integration examples.

---

## Common Tasks Checklist

### Creating a new event listener
- [ ] Create class implementing `Listener`
- [ ] Annotate methods with `@EventHandler`
- [ ] Call `getServer().getPluginManager().registerEvents(listener, plugin)` in `onEnable()`
- [ ] Add `ignoreCancelled = true` unless you need cancelled events

### Adding a new command
- [ ] Define command in `plugin.yml` under `commands:`
- [ ] Create executor class implementing `CommandExecutor`
- [ ] (Optional) implement `TabCompleter` for autocomplete
- [ ] Register with `getCommand("name").setExecutor(new MyExecutor())`

### Saving plugin data
- [ ] For simple values: use `config.yml` via `getConfig()` / `saveConfig()`
- [ ] For per-entity data: use PDC with a `NamespacedKey`
- [ ] For large datasets: use async scheduler + file I/O or a database

### Scheduling a repeating task
- [ ] Determine if task needs main thread (use `runTaskTimer`) or is I/O (use `runTaskTimerAsynchronously`)
- [ ] Store the `BukkitTask` reference so you can cancel in `onDisable()`
- [ ] Cancel all tasks in `onDisable()` or use `getServer().getScheduler().cancelTasks(plugin)`

---

## Build, Validate, and Run

1. Build the plugin JAR:
   ```bash
   ./gradlew shadowJar
   # Output: build/libs/my-plugin-1.0.0-SNAPSHOT.jar
   ```
2. Run the bundled validator to catch config and layout errors:
   ```bash
   ./scripts/validate-plugin-layout.sh --root /path/to/plugin-project
   # Strict mode treats warnings as failures:
   ./scripts/validate-plugin-layout.sh --root /path/to/plugin-project --strict
   ```
3. Fix any reported errors and re-run until clean.
4. Deploy: copy JAR to `server/plugins/` and restart, or use the dev server:
   ```bash
   ./gradlew runServer
   ```

The validator checks:
- `plugin.yml` required keys (`name`, `version`, `main`, `api-version`) and repo-supported `1.21`, positive `1.21.<patch>` and `26.<minor>[.<hotfix>]` `api-version` values, with warnings for versions newer than the repo's current example
- Main class path exists and extends `JavaPlugin`
- `/reload` anti-pattern detection in source snippets

---

## References

- Paper API Javadoc: https://jd.papermc.io/paper/
- Paper Dev Docs: https://docs.papermc.io/paper/dev/getting-started/
- Adventure (text API): https://docs.advntr.dev/
- MiniMessage format: https://docs.advntr.dev/minimessage/format.html
- Vault API: https://github.com/MilkBowl/VaultAPI
- Bukkit API Javadoc: https://javadoc.io/doc/org.bukkit/bukkit/
- run-task Gradle plugin: https://github.com/jpenilla/run-task
