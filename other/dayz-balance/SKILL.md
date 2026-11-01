---
name: dayz-balance
description: "Compares a DayZ mod's item stats with similar vanilla items and flags outliers with file:line and the vanilla median. Use it after writing item configs, or when the user asks whether an item is overpowered, too heavy or balanced."
argument-hint: "<ModName> [--json] [--ratio 1.5] [--min-peers 3] | --mod-dir <folder> [--vanilla-root P:\\]"
---

<!-- skill-dir-note -->
> **Path note:** `<skill-dir>` in commands below is the absolute path of this skill's folder. When the agent loads this skill the harness exposes the skill's base directory; substitute it before running. Sibling skills are reached via `<skill-dir>\..\dayz-X\`.

# /dayz-balance

A script reads the mod's `config.cpp` files, with the files they `#include` from the mod folder, and the unpacked vanilla configs on `P:\DZ\`, and measures each mod item against the vanilla items that share its parent class. It checks weight, health, damage, protection, cargo capacity and maximum quantity, and lists every stat far outside vanilla with file:line, the vanilla median and the closest vanilla items. It starts no process and needs no DayZ Tools. Reading all of `P:\DZ\` takes about five seconds. The script only measures. The AI reads the outliers and asks whether each one is intended; a mod may want a tougher vest on purpose.

Follow `skills/_shared/dayz-conventions.md`.

## Before you run

Run `/dayz-preflight` first in a new session or after a reboot. Balance only reads files, so it is exempt from the preflight gate (see `dayz-conventions.md`) and does not run it itself, but it needs `P:\` mounted and the vanilla data unpacked under `P:\DZ\`. Without them it stops with `ERROR` and `no vanilla data at P:\DZ`; preflight says which one is missing.

## How to run

```cmd
python "<skill-dir>\balance.py" <ModName> [--json]
python "<skill-dir>\balance.py" --mod-dir <folder> [--json]
```

| Argument | Notes |
|---|---|
| `<ModName>` | A mod under `workspace/<ModName>/` in the project cached by `/dayz-init`. |
| `--mod-dir` | Check any folder instead. Its name is the mod name unless `<ModName>` is given too. |
| `--vanilla-root` | The folder that holds the unpacked `DZ\` data. Default `P:\`. |
| `--ratio` | How many times above or below the vanilla median a value must be to count. Default `1.5`. |
| `--min-peers` | The fewest vanilla items needed to judge a stat. Default `3`. |
| `--json` | Print the full report as JSON after the verdict line. |

Run `/dayz-lint` first if the config has never been checked. A `config.cpp` that does not parse stops balance with an error.

## What it compares

Only stats the mod sets itself, on the item or on a mod base class above it. A stat the item inherits from vanilla is the vanilla value and is never flagged.

| Stat | Read from |
|---|---|
| `weight` | `weight` |
| `health` | `DamageSystem > GlobalHealth > Health > hitpoints` |
| `damage.health`, `damage.blood`, `damage.shock` | `DamageApplied > Health, Blood, Shock > damage` in `CfgAmmo`, the damage a bullet or melee hit deals |
| `protection.<kind>.<type>` | `DamageSystem > GlobalArmor > <kind> > <type> > damage`, for example `protection.projectile.health`. These are multipliers on damage taken, so a low value means more protection. |
| `protection.<name>` | `Protection > <name>`, for example `protection.biological` on masks. These are coverage, so a high value means more protection: masks that set it range from `0.25` (balaclavas) through `0.5` and `0.75` to `1` (GasMask), per `P:\DZ\characters\masks\config.cpp`. Items that set nothing, such as the bandanas and shemags in `P:\DZ\characters\headgear\config.cpp`, inherit `0` from the `Inventory_Base` `Protection` block in `P:\DZ\data\config.cpp`. |
| `capacity` | `itemsCargoSize[]`, as width times height in cells |
| `quantity` | `varQuantityMax` |

An item is a class with `scope = 2` in `CfgVehicles`, `CfgWeapons` or `CfgMagazines`. In `CfgAmmo` every class counts unless it sets `scope = 0` itself, because vanilla ammo is `scope = 1` and the melee damage classes inherit `scope = 0`.

## How peers are picked

1. Walk up from the mod item, past any mod base classes, to the nearest vanilla class. For a vest that inherits `PlateCarrierVest` that is `PlateCarrierVest`.
2. The peers are that class and every vanilla item below it, each with its own inherited stats. Classes the mod redefines are left out.
3. When fewer than `--min-peers` peers have the stat, go up one vanilla parent and try again, at most twice. If that is still too few, the stat is not judged.
   3a. A broad group mixes item kinds (`Clothing` holds masks, backpacks, boots and belts), so in every group, the first one included, only the peers that share an `inventorySlot[]` with the mod item are kept, and the report names the group as, for example, `Clothing in slot Mask`. This matters from the start because vanilla masks inherit `Clothing` directly (`class GasMask: Clothing` in `P:\DZ\characters\masks\config.cpp`), so a mod mask written the same way has `Clothing` as its nearest vanilla class. When that leaves fewer than `--min-peers`, or the item has no slot, the whole group is used.

4. `CfgAmmo` puts every kind of hit under `Bullet_Base`: melee hits (`class MeleeDamage: Bullet_Base` in `P:\DZ\weapons\melee\config.cpp:19`, with `FinisherHit` dealing `1000`), explosives and flares as well as bullets. So an ammo class is compared only with vanilla ammo of the same family, and the report names the group as, for example, `Bullet_Base (firearm rounds)`:
   - melee and environment hits: the class has `MeleeDamage` above it.
   - explosive rounds: `explosive` above `0`, as on `GrenadeM4`, `Rocket_RPG7_Base` and `Bullet_40mm_Explosive` in `P:\DZ\weapons\projectiles\config.cpp`.
   - flare and smoke rounds: `simulation = "shotIlluminating"`, as on `Bullet_Flare` and the `Bullet_40mm_Smoke_*` rounds.
   - 40mm launcher rounds: the other rounds with `Bullet_40mm_Base` above them, which are `Bullet_40mm_Base` itself (the inert grenade, `P:\DZ\weapons\projectiles\config.cpp:6875`) and `Bullet_40mm_ChemGas` (line 6949).
   - syringe darts: `Dart_Syringe` and classes below it (line 6445), the shock pistol dart fired from `Mag_ShockCartridge` (`P:\DZ\weapons\attachments\magazine\config.cpp:2208`).
   - firearm rounds: everything else. A round that deals health damage leaves out the non-lethal ones that deal `0` (`Bullet_12GaugeBeanbag`, `Bullet_12GaugeRubberSlug`); a round that deals none is compared with all of them.

   On the real `P:\DZ\` that leaves 18 lethal firearm rounds under `Bullet_Base`, the pistol, rifle and slug rounds from `Bullet_22` at `20` to `Bullet_308Win` and `Bullet_762x54` at `150` health damage, instead of 230 classes ranging from `0` to `1000`. A family with fewer than `--min-peers` vanilla rounds, such as the two 40mm launcher rounds or the one dart, is not judged.

A value is an outlier when it is outside the peers' whole range and at least `--ratio` times away from their median.

The text report gives a high outlier as `N x the median` and a low one as `N x below the median` (the median divided by the value), so weight 1 against a median of 12000 reads `12000x below the median 12000`.

## Output and exit codes

The first line is the verdict:

| Verdict | Exit | Meaning |
|---|---|---|
| `PASS` | 0 | At least one item was compared and none is an outlier. |
| `FLAG` | 1 | At least one outlier. |
| `ERROR` | 2 | Bad arguments, no cached project, no mod folder, no `config.cpp`, one that does not parse, or no vanilla data at `--vanilla-root`. |
| `UNCHECKED` | 3 | No outliers, but no item could be compared: the mod has no items, or every item has no vanilla parent (it inherits another mod's base classes, such as CF or Expansion bases not under `P:\DZ\`) or too few vanilla peers. Tell the user nothing was measured; it is not a pass. |

An item that sets none of the compared stats but has a vanilla parent counts as compared, because its stats are vanilla's own, and is printed as `compared (inherits vanilla stats)`. Then one entry per outlier, those items, and the items that were not compared, so the `not compared` lines are exactly the items missing from the `N compared` count:

```
FLAG
- workspace/MyVest/config.cpp:12  MyVest_Plate health = 5000: tougher than vanilla, 22.22x the median 225 of 6 vanilla items under PlateCarrierVest (range 225 to 225)
    closest: PlateCarrierVest 225, PlateCarrierVest_Black 225, PlateCarrierVest_Camo 225, PlateCarrierVest_Desert 225, PlateCarrierVest_Green 225
  compared (inherits vanilla stats): MyVest_Plain sets none of the compared stats
  not compared: MyVest_Gadget has no vanilla parent (parent MyVest_Unknown)
  WARN workspace/MyVest/config.cpp:20  #include "items\missing.hpp" not read: it was not found, so its classes were not compared
  WARN P:\DZ\somewhere\config.cpp  vanilla config not read (line 40: string starting with " is not closed on this line; add the closing "), so its classes are not peers
  1 outlier(s) in 3 item(s), 2 compared
```

With `--json` each finding has `item`, `section`, `stat`, `value`, `file`, `line`, `peer_base`, `peer_count`, `median`, `min`, `max`, `direction` (`high` or `low`), `meaning`, `ratio` (value divided by median, to four significant figures, so a tiny low value stays above 0) and the closest `peers`. Items not compared are under `skipped` with a `reason`; items compared only through inherited vanilla stats are under `inherits_vanilla`, in the same shape. Includes that were not followed are under `includes_skipped` with `file`, `line`, `include` and `reason`. `compared` counts the items measured against vanilla. Vanilla `config.cpp` files that do not tokenize are under `vanilla_unread` with `file` and `error`; their classes are missing from the peers, and the text report prints a `WARN` line for each.

## After the run

- On `UNCHECKED`, say that no item was compared and why (the `not compared` lines); do not report the mod as balanced.
- For each outlier, tell the user the item, the stat, the vanilla median and the closest vanilla items, and ask whether it is intended. Do not change a value on your own.
- When the user wants a value changed, hand the class to its owner: clothing and vests to `dayz-wearables-specialist`, firearms, magazines and ammo to `dayz-weapon-specialist`, vehicles (`CfgVehicles` classes under the `Car` or `Boat` bases, or a modded `Helicopter` base) to `dayz-vehicle-specialist`, everything else to `dayz-config-specialist`.

## Limits

- Stats that depend on script code (`OnStoreLoad`, custom damage handling) are not seen.
- Only the four item sections are read. Vehicles are compared like any `CfgVehicles` item, which says little about how they drive.
- `#include "file"` is followed when the file is inside the mod folder: a plain name is relative to the including file, and a name that starts with `\` is followed when its first folder is the mod folder's name (the `P:\<ModName>\` prefix). Findings point at the included file and line. An include outside the mod folder, missing, or including itself is not read and prints a `WARN` line, so a `PASS` never hides classes that were not compared. Vanilla `P:\DZ\` configs use no `#include`.
