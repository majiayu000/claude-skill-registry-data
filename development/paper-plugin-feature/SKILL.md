---
name: paper-plugin-feature
description: End-to-end procedure for adding a player-facing feature (command, listener-driven behavior, or config option) to a Bukkit/Paper/Folia plugin so that registration, permissions, i18n, config validation, thread-safety, and tests all land consistently in one pass. Use whenever the user asks to add a command, feature, toggle, or config option to a Minecraft server plugin — including indirect requests like "players should be able to X" or "make Y configurable".
---

# Adding a feature to a Paper/Folia plugin

A feature is not done when the handler works. It is done when the permission is declared,
the messages are translatable, the config key validates, old configs keep their behavior,
Folia doesn't crash, and a test exercises it. Work through the checklists **in order** —
each step's output is an input to the next.

## Step 0 — Recon (always, before writing anything)

1. Read the plugin's main class, its message/i18n manager, and `plugin.yml`. Identify:
   - How commands are registered (plugin.yml + `onCommand` dispatch? Brigadier/Cloud?)
   - How messages are resolved (hardcoded? keyed file? MiniMessage or legacy `§`?)
   - Whether the plugin declares `folia-supported: true` (if yes, every step below has a
     Folia dimension; see the companion `folia-safety-audit` skill).
   - How config is read: at-use (`config.getX` everywhere) or cached-at-load into fields.
     Match the existing pattern; do not introduce a second one.
2. Grep for an existing feature of the same shape and mirror its structure. Consistency
   beats novelty in plugin codebases.

## Step 1 — Command & permission registration

- [ ] `plugin.yml`: add the command (description, usage, `permission:`, aliases).
- [ ] `plugin.yml`: declare the permission node under `permissions:` with an explicit
      `default:` (`true` for player-facing, `op` for admin). **Undeclared nodes behave
      inconsistently across permission plugins** — never rely on an implicit node.
- [ ] If a wildcard parent exists (e.g. `myplugin.*`), add the new node to its `children`.
- [ ] Register the executor wherever the plugin's other commands register (array/list in the
      main class, or per-command). Miss this and the command silently no-ops.
- [ ] Re-check the permission **in the handler** too (defense in depth; plugin.yml gating
      alone produces a generic Bukkit message instead of the plugin's own).

## Step 2 — Messages / i18n

- [ ] Every user-visible string goes in the messages file — zero hardcoded strings, including
      error paths and the "no permission" case.
- [ ] Follow the existing key naming scheme (`commands.<name>.<case>` or whatever the repo uses).
- [ ] Check whether the plugin merges bundled defaults into the server's messages file
      (look for `setDefaults` / `getResource` in the message manager):
      - **Merges** → new keys work on existing servers automatically; just add them.
      - **Doesn't merge** → new keys are missing on existing servers; either add merging
        (small, high-value fix) or code a fallback string.
- [ ] If the build template-expands resource files (Gradle `processResources` + `expand`),
      **no literal `$` may appear in the new strings** — it breaks the build.
- [ ] Pluralization/placeholders: match the existing convention (e.g. `{seconds}` + a
      code-computed `{plural}`); don't invent a new placeholder syntax.

## Step 3 — Config keys (only if the feature is configurable)

- [ ] Key + comment block in the bundled `config.yml`.
- [ ] Read it with an explicit code-side default: `config.getX("path", default)`. Most plugins
      do **not** auto-merge new config keys into existing server files — the code default is
      what makes the release migration-free.
- [ ] **Behavior-changing keys default to preserving old behavior.** A new "cancel teleport
      on damage" toggle defaults to `false`; a new limit defaults to "unlimited". Existing
      servers must upgrade without observable change.
- [ ] If the plugin has a config validator, add a rule (range/enum checks, warning vs error)
      in the same style. If it caches config into fields at load, add the field there —
      mark it `@Volatile`/`volatile` if any non-main thread reads it.
- [ ] Document reload behavior: does `/reload`-style command pick it up, or enable-only?
      Say so in the config comment.

## Step 4 — State & lifecycle (only if the feature holds per-player state)

- [ ] Concurrent structure (`ConcurrentHashMap` keyed by **UUID, never `Player`** — live
      references leak entity graphs and are illegal cross-region on Folia).
- [ ] Wire cleanup into the quit handler AND the plugin's disable-time clear.
- [ ] Decide persistence honestly: in-memory (dies with restart — usually right for
      session-scoped state) vs PDC/file (survives — only if the feature semantically needs it).

## Step 5 — Threading (mandatory when `folia-supported: true`, good hygiene otherwise)

Minimum bar (full audit → `folia-safety-audit` skill):
- [ ] Any entity access (`.location`, `.teleport*`, inventory, health) runs on that entity's
      scheduler on Folia — including entities *other than* the command sender.
- [ ] Scheduled work uses the right scheduler: entity-bound → `entity.getScheduler()`,
      global state → `GlobalRegionScheduler`, I/O → `AsyncScheduler`. Never block a
      command/event thread on network or disk.
- [ ] Adventure `sendMessage`/`showTitle` are thread-safe; sounds via the entity-emitter
      `playSound(player, sound, …)` overload (the `Location` overload reads a region-guarded
      accessor).

## Step 6 — Verification & shipping

- [ ] Build passes.
- [ ] Exercise the feature live (test server or bot harness): happy path, the permission-denied
      path, and each error message. If the repo has an e2e suite, add a scenario that asserts
      on the feature's **chat messages** (position checks are flaky when players cluster).
- [ ] Changelog entry + release-notes entry in the repo's established format.
- [ ] Update the project context doc (CLAUDE.md): new command/permission/config tables.

## Failure smells (stop and fix if you notice)

- A string literal with color codes in a `.kt`/`.java` file → belongs in the messages file.
- A permission string used in code but absent from `plugin.yml`.
- `config.get…` with no default, or a new key that changes behavior when absent.
- A new `HashMap` for player state, or a map that quit-cleanup doesn't know about.
- "Works for the sender" logic that touches a *second* player's entity state on the
  sender's thread — the classic Folia crash.
