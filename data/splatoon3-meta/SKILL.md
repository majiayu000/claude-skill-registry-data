---
name: splatoon3-meta
description: "Domain expert for Splatoon 3 competitive gear abilities and weapon meta. Use when: (1) Labeling or classifying gear build features from SAE analysis, (2) Understanding why specific ability combinations appear in builds, (3) Identifying weapon archetypes and their associated ability patterns, (4) Semantic analysis of gear/ability relationships, (5) Interpreting competitive meta patterns in build data, (6) Any task requiring deep knowledge of Splatoon 3 ability synergies, anti-synergies, breakpoints, or playstyle associations."
---

# Splatoon 3 Meta Knowledge Expert

Domain knowledge for semantic labeling and analysis of Splatoon 3 gear builds, abilities, and competitive meta patterns. Designed for SAE feature labeling and build pattern classification.

## Quick Reference: Core Frameworks

### The AP System
- **Main slot**: 10 AP (also written as 1.0 in Japanese notation)
- **Sub slot**: 3 AP (also written as 0.1)
- **Max per build**: 57 AP (3 gear pieces × 19 AP)
- **Diminishing returns**: First sub = ~10% max effect (HIGHEST efficiency), First main = ~30%

### Japanese Meta Terminology
| Term | Meaning | Implication |
|------|---------|-------------|
| **お守り (Omamori)** | "Charm gear" | Small investments (0.1-0.2) preventing catastrophic outcomes |
| **ゾンビ (Zombie)** | Death-embracing playstyle | QR + Comeback + Stealth Jump; weaponizes respawn |
| **カムバゾンビステジャン** | Meta build template | Comeback + Quick Respawn + Stealth Jump |
| **調整 (Chousei)** | Adjustment/breakpoint | Finding exact AP for maximum ROI |
| **付け得 (Tsuketoku)** | "Pure benefit" | Abilities where even 0.1 is always worth it |

### The Four Omamori (Universal 0.1 Investments)
Always valuable at single-sub investment:
1. **Quick Super Jump** — Escape vector, gauge preservation
2. **Sub Resistance Up** — Combo breaking (30→28.4 dmg)
3. **Ink Resistance Up** — Mobility floor, DoT buffer
4. **Special Saver** — 50%→41% gauge loss on death

## Labeling Workflow

### Step 1: Identify Build Archetype
Determine primary playstyle from ability composition:

| Archetype | Key Indicators | Death Philosophy |
|-----------|----------------|------------------|
| **Zombie Slayer** | QR ≥1.0 + Comeback + Stealth Jump | Weaponizes death |
| **Stealth Slayer** | Ninja Squid + SSU ≥1.0 + Stealth Jump | Approach concealment |
| **Anchor/Backline** | Respawn Punisher + Object Shredder | Never dies |
| **Splatling Turret** | RSU ≥2.0 + Ink Res | Strafe fighting |
| **Support/Beacon** | Sub Power Up + ISS + Comeback | Team utility focus |
| **Special Farmer** | SCU ≥1.0 + Special Saver + Tenacity | Special as win condition |

### Step 2: Classify Ability Relationships
For each ability in the build, identify its functional role:

**Primary Categories**:
- `omamori` — Safety/insurance investment (typically 0.1-0.2)
- `zombie` — Death mitigation / aggression enabler
- `mobility` — Movement and positioning
- `efficiency` — Ink/special resource management
- `information` — Vision control (stealth or tracking)
- `punishment` — Making kills hurt more
- `team-utility` — Benefits teammates

**Secondary Tags**:
- `breakpoint-dependent` — Value hinges on specific AP threshold
- `weapon-specific` — Only valuable on certain weapon classes
- `mode-dependent` — Value changes by game mode
- `slot-exclusive` — Competes with other main-only abilities

### Step 3: Identify Synergies/Conflicts
Check for known relationships:

**Critical Synergies**:
- Ninja Squid → REQUIRES SSU ≥1.0 (offset 10% penalty)
- Comeback + QR + Stealth Jump → Complete Zombie package
- Respawn Punisher + Object Shredder → Anchor control package

**Critical Conflicts**:
- Respawn Punisher + Quick Respawn → RP reduces QR by 85%
- Respawn Punisher + frontline weapon → Self-penalty exceeds benefit
- Stealth Jump + Drop Roller → Same slot exclusion

## Reference Files

For detailed information, consult:

- **[`references/abilities.md`](references/abilities.md)** — Complete per-ability domain knowledge including:
  - Japanese terminology and shorthand
  - Standard AP adjustments and breakpoints
  - Weapon-specific context
  - Synergies and anti-synergies
  - Semantic tags for labeling

- **[`references/archetypes.md`](references/archetypes.md)** — Weapon archetype mappings:
  - Core abilities per weapon class
  - Playstyle associations
  - Template builds

- **[`references/synergies.md`](references/synergies.md)** — Relationship matrices:
  - Synergy chains with explanations
  - Anti-synergy conflicts with severity ratings
  - Slot competition mappings

- **[`references/weapons.md`](references/weapons.md)** — Complete weapon reference:
  - Weapon ID to name mappings (for mechinterp output)
  - Sub and special weapon for each kit
  - Weapon class groupings
  - Special-dependent weapon list (benefit heavily from SCU)

- **[`references/weapon-vibes.md`](references/weapon-vibes.md)** — Per-weapon "vibe" profiles ⚠️ *Community consensus*:
  - Ink/movement/aim feel per weapon
  - Typical ability investments (ISM, RSU, IA)
  - Range, approach style, Ninja Squid affinity
  - Role (lane/job) and death tolerance
  - Quick lookup tables by trait

## Death-Related Ability Nuances

Critical distinction for labeling death-mitigation features:

| Ability | Mechanism | Incentivizes Death? |
|---------|-----------|---------------------|
| **Quick Respawn** | Faster respawn on no-kill deaths | **YES** — activates only on consecutive deaths without kills |
| **Comeback** | 20s stat boost post-respawn | **NO** — rewards capitalizing on window, not dying |
| **Special Saver** | Reduce gauge loss | **NO** — passive insurance |
| **Stealth Jump** | Safe aggressive jumps | **INDIRECT** — enables riskier positioning |
| **Respawn Punisher** | Punish opponent deaths | **NO** — punishes YOUR deaths harder |
| **Haunt** | Track your killer | **INDIRECT** — provides value from being killed |

## Feature Label Examples

When labeling SAE features, use patterns like:

```
Feature: High QR + Comeback + Stealth Jump activation
Label: zombie_slayer_package, death_mitigation_hard, aggressive_reentry

Feature: Ninja Squid without SSU compensation
Label: incomplete_build, missing_synergy, suboptimal_mobility

Feature: Respawn Punisher + QR co-occurrence
Label: critical_conflict, anti_synergy, build_error

Feature: Exactly 0.1 of QSJ + SubRes + InkRes + SpecialSaver
Label: omamori_package, optimal_utility, japanese_meta_standard

Feature: RSU ≥2.0 without Splatling weapon
Label: potential_mismatch, weapon_context_required, investigate
```

## AP Threshold Flags

Flag these specific investment levels:

| Ability | Threshold | Significance |
|---------|-----------|--------------|
| SSU with Ninja Squid | ≥1.0 (10 AP) | Mandatory offset |
| Quick Respawn | ≥1.2 (12 AP) | Minimum effective Zombie |
| Intensify Action (Shooters) | 0.2 (6 AP) | "Golden ratio" for jump accuracy |
| Intensify Action (Blasters) | ≥1.0 (10 AP) | Ground accuracy while jumping |
| Run Speed Up (Splatlings) | ≥2.0 (20 AP) | Minimum for strafe viability |
| Special Saver | 0.1 (3 AP) | Highest efficiency single investment |

## MechInterp Integration

Use this skill when mechinterp analysis shows weapon-specific patterns.

### After weapon_sweep Analysis

If `weapon_sweep` shows a specific weapon dominates activation:

1. **Look up the weapon's kit** in `references/weapons.md`:
   - Find the weapon by name or ID
   - Note its sub weapon and special weapon

2. **Check if other high-activation weapons share kit components**:
   - Same sub weapon → Feature may encode sub weapon playstyle
   - Same special weapon → Feature may encode special farming/spam builds

3. **Cross-reference with weapon characteristics**:
   - Is this a "special-dependent" weapon? (See `references/weapons.md` special list)
   - What archetype does this weapon belong to? (See `references/archetypes.md`)

### Kit-Linked Feature Detection

When multiple weapons share a sub or special but feature activates for all of them:

| Pattern | Likely Interpretation |
|---------|----------------------|
| All high weapons have Squid Beakon | Beacon-focused playstyle feature |
| All high weapons have Ink Storm | Zoning/area denial special spam |
| All high weapons have Trizooka | Kill-focused special builds |
| All high weapons have Wave Breaker | Pressure special stacking |
| All high weapons have Crab Tank | Heavy special farming builds |

### Example: Feature 18712 Kit Analysis

```
weapon_sweep findings:
- Octobrush Nouveau: +0.22 delta (DOMINANT)
- Range Blaster: +0.09 delta
- Rapid Blaster: +0.08 delta

Kit lookup from weapons.md:
- Octobrush Nouveau: Squid Beakon + Ink Storm
- Range Blaster: Suction Bomb + Wave Breaker
- Rapid Blaster: Torpedo + Triple Inkstrike

Pattern check:
- No shared sub weapon
- But ALL are "special-dependent" weapons per meta

Conclusion: Feature encodes "Special Charge Up on special-dependent weapons"
           not just "Octobrush Nouveau builds"
```

### Quick Kit Lookup

For common weapon IDs in mechinterp output, see `references/weapons.md`.

Example high-frequency weapon IDs:
| ID | Weapon | Sub | Special |
|----|--------|-----|---------|
| 1111 | Octobrush Nouveau | Squid Beakon | Ink Storm |
| 220 | Range Blaster | Suction Bomb | Wave Breaker |
| 240 | Rapid Blaster | Torpedo | Triple Inkstrike |
| 2021 | Big Swig Roller | Splash Wall | Ink Vac |
| 2050 | Custom E-liter 4K | Squid Beakon | Kraken Royale |
