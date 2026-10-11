---
name: monarch-fresh-account-reset
description: "Reset the Monarch Android app (D:\\Monarch) to a fresh local account on the S25 Ultra and verify it — what pm clear destroys vs what reseeds, the pre-wipe recoverability check, and the epoch-baseline trap that pays a brand-new account ~497,000 idle essence. Use when asked for a fresh account/clean DB, or when a new install shows absurd idle numbers."
---

# Monarch fresh-account reset

`D:\Monarch`, package `com.monarch.app`. ADB at
`$LOCALAPPDATA/Android/Sdk/platform-tools/adb.exe`.

## 1. Before wiping — the recoverability check

`pm clear` is irreversible and there is no root. Do this FIRST, because "reset
my local DB" and "keep my routine" can arrive in either order:

```bash
"$ADB" shell "find /sdcard -iname '*monarch*' -o -iname '*export*.json'"   # in-app export?
"$ADB" shell run-as com.monarch.app ls -la /data/data/com.monarch.app/databases
```

What survives a wipe, and what does not:

| Data | After `pm clear` |
|---|---|
| Presets / routine | **Reseeded** from `data/Seed.kt` |
| Sessions, XP, level, titles, streak | Gone |
| Relics, crests, idle essence | Gone |
| Supabase profile row (cloud) | **Survives** — see §4 |
| User edits to a preset | Gone, unrecoverable |

`Seed.kt` is commented *"the user's real four-day split"* and seeds
**Heavy Pull MON, Legs TUE, Volume Pull THU, Push FRI**. So an unedited routine
restores verbatim. Verify set counts against pre-wipe screenshots rather than
assuming: Heavy Pull = 22 sets (5+4+4+3+3+3), Legs = 17 (3+4+3+4+3).

## 2. The wipe

```bash
"$ADB" shell am force-stop com.monarch.app
"$ADB" shell pm clear com.monarch.app
"$ADB" shell am start -W -n com.monarch.app/.MainActivity
```

Install the current build *before* clearing if a fix must be present on first
launch — otherwise first launch writes state through the old code.

## 3. The epoch-baseline trap

A fresh `idle_state` row carries `lastCollectedAtMs = 0`
(`MIGRATION_..._: INSERT OR IGNORE INTO idle_state ... VALUES (1,0,0,1.0,0)`).
The accrual curve deliberately **never stops paying** (full rate 24h, taper 48h,
then a permanent 10% floor), so there is no cap to save you: the epoch reads as
a ~56-year absence and banks

```
490,000 h  ×  10/h (floor rate)  ×  0.10 (MIN_EFFICIENCY)  ≈  497,000 essence
```

Fix belongs in `Idle.accruedExact`, not the UI: `lastCollectedAtMs <= 0` means
*no baseline*, return 0. `collect()` stamps the baseline, so it self-heals.

Gotcha when adding that guard: existing curve tests in `IdleTest` used
`lastCollectedAtMs = 0` as a convenient origin and will fail. Rebase them onto a
real `base` timestamp (`1_700_000_000_000L`) and offset every `nowMs` — do not
weaken the guard.

## 4. Verification (what "fresh" must look like)

Drive by uiautomator text bounds, not coordinates:

```python
sh("shell","uiautomator","dump","/sdcard/ui.xml")
xml = sh("shell","cat","/sdcard/ui.xml")   # then regex text="..." bounds="[x,y][x,y]"
```

Expect on the Court screen: `HUNTER`, `LV 1`, `0 / 100 XP`, `0/95` titles,
streak `—`, `PROGRAMS 4`, today's quest populated.
On Shadow: `ESSENCE 0.00`, `RATE 10.0 PER HOUR`, `SHADOWS 0`, `RELIC ×1.00`,
and the factor bars near-empty (they measure each factor against its own
ceiling via `Idle.MAX_TRAINING_FACTOR` / `MAX_SKILL_FACTOR`).

Confirm all four programs really came back — scroll the presets screen and
collect names plus day chips across several dumps; a single dump only shows the
first two.

Cloud caveat worth stating to the user: the Supabase `profiles` row is NOT
wiped. Signing in again pushes the fresh local aggregates over it, dropping the
cloud level/XP to the new values.
