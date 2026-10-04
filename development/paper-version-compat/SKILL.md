---
name: paper-version-compat
description: Repeatable procedure for validating and honestly documenting a Bukkit/Paper/Folia plugin's compatibility when a new Minecraft/Paper version ships — research-first API checking, build strategy, runtime verification, and maintaining a tested-vs-assumed compatibility matrix. Use whenever a new Minecraft or Paper version is released, the user asks "does my plugin support version X", a paper-api dependency bump is considered, or release notes need a compatibility claim.
---

# Validating a Paper plugin against a new Minecraft/Paper version

The goal is an honest, documented compatibility claim — "tested" and "assumed" are different
statements and users deserve to know which one they're getting. Most version bumps need zero
code changes; the work is research, verification, and documentation discipline.

## Step 1 — Research first (never trust model memory)

New MC/Paper versions are usually past the model's training cutoff, and Minecraft's
versioning/cadence has changed over time. Before any code conclusion:

1. Web-search the Paper release announcement and docs.papermc.io update notes for the target
   version. Look specifically for: required Java version, plugin-affecting API removals,
   `api-version` policy changes, and remap/mappings changes.
2. Check the loaders-that-lag: **Folia releases behind Paper** — if no Folia build exists for
   the target version, the matrix entry is "N/A yet", not "supported".
3. If findings are thin (fresh release), mark every conclusion medium-confidence and say so
   in anything you write.

## Step 2 — Grep the plugin's real API surface

Don't audit the whole Bukkit API — audit what the plugin actually touches. Build the list once
and keep it in the project's context doc:

```
grep -roh --include=*.kt --include=*.java \
  -E 'org\.bukkit\.[A-Za-z.]+|io\.papermc\.[A-Za-z.]+|net\.kyori\.[A-Za-z.]+' src/ \
  | sort -u
```

Cross-check that list against the release's deprecations/removals. Typical hot spots:
registry access patterns (enum → `Registry` migrations), scheduler APIs (legacy
`scheduleSyncRepeatingTask`-style methods are perennial removal candidates), event signature
changes, `ItemStack`/component APIs, and anything `@Deprecated(forRemoval = true)` in the
current compile.

## Step 3 — Decide the build strategy (this is a policy, not a routine step)

- **Default: keep compiling against the *oldest* supported Paper API.** One JAR spanning
  versions comes from API stability plus conservative bytecode targeting — not from chasing
  the newest `paper-api`.
- Only bump `paper-api` / `api-version` when (a) you need a new API, or (b) you are
  deliberately dropping old-version support. Both are support-range decisions; changelog them.
- Java: servers may raise their required Java version across MC versions while old servers
  stay lower. Keep the **bytecode target at the floor** (e.g. Java 21 bytecode runs fine on a
  Java 25 server); use a newer toolchain freely. Verify Gradle itself can run on the JDK in
  use — Gradle's max-supported-JVM lags JDK releases, and the failure message is cryptic
  (run Gradle on an older JDK via `JAVA_HOME`; keep the toolchain block for compilation).

## Step 4 — Build & fix

Branch (e.g. `dev/<new-version>`), build, and treat new deprecation warnings as work items
now — they're the removals of the next cycle.

## Step 5 — Runtime verification ladder

Each rung upgrades the claim you're allowed to make:

1. **Boots clean** — plugin enables on the target version, no stack traces, info command works.
2. **Manual pass** — one full cycle of the plugin's core flow(s) by hand.
3. **Suite pass** — the project's e2e/bot suite green on the target version. Caveat for
   bot-based suites: bot libraries (mineflayer etc.) lag new protocol versions — options are
   ViaVersion on the *test* server (bots handshake old, server runs new) or deferring the
   "tested" claim, explicitly.
4. **Folia pass** — separate rung; Paper-tested says nothing about region-thread behavior.

Only rung 3+ justifies "Tested" in public docs. Rungs 1–2 justify "expected to work".

## Step 6 — Update the compatibility matrix (the durable artifact)

Maintain a table in the project context doc with **Status ∈ {Tested, Assumed, Partially
tested, N/A yet, Not supported}** and an *evidence* column (what ran, when). Rules:

- Never promote to "Tested" without the suite/manual pass on that exact platform+version.
- Downgrade honestly: a big internal change (threading, scheduler rework) drops previously
  "Tested" platforms back to "Partially tested" until re-run.
- Mirror the matrix everywhere users see claims: release notes, README badges, and the
  Modrinth/Hangar listing's game-version range — same commit.

## Step 7 — Release hygiene

- Changelog states the new supported range and whether code changed or only verification.
- If zero code changes were needed, say exactly that — "no code changes; verified on X" is a
  meaningful, reassuring release note.
- Update the local dev server pin (`runServer` version or equivalent) so the next contributor
  tests against the new default.

## Anti-patterns

- Claiming a version range from API stability alone while labeling it "tested".
- Bumping `paper-api` to the newest version reflexively — it silently narrows your floor.
- Skipping the Folia check because "it's just Paper with threads" (it is not).
- Letting the compatibility claim live only in a Modrinth dropdown, with no evidence trail
  in the repo.
