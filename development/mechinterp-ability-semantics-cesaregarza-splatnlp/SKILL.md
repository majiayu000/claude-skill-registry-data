---
name: mechinterp-ability-semantics
description: Reference for ability family semantic groupings and gameplay meanings
---

# MechInterp Ability Semantics Reference

This skill provides domain knowledge about ability semantic groupings in Splatoon 3. Use this reference **AFTER** forming hypotheses to validate interpretations against gameplay semantics.

## When to Use This Skill

1. After observing patterns in enhancers/suppressors
2. When interpreting what a feature "means" strategically
3. To check if observed groupings match known semantic categories
4. To avoid missing obvious semantic interpretations

**IMPORTANT**: Form hypotheses from data FIRST, then check this reference. Don't use this to guide initial exploration.

## Semantic Groupings

### Death-Mitigation (Death-Accepting) Abilities

These abilities provide value **when the player dies**. Players using these implicitly accept that dying is part of their strategy.

| Ability | Effect | Strategic Implication |
|---------|--------|----------------------|
| `quick_respawn` | Faster respawn after death | Aggressive trading, accepts deaths |
| `special_saver` | Keep more special charge on death | Death is acceptable, special matters |
| `comeback` | Stat boost for 20s after respawn | Deliberately plays for respawn buff |
| `respawn_punisher` | Punish enemy deaths, accept own | Very aggressive, kill-or-be-killed |

**Interpretation**: If these are **suppressed**, the feature likely encodes "death-averse" or "survival-focused" builds.

### Mobility Abilities

Enhance movement speed and repositioning.

| Ability | Effect | Strategic Implication |
|---------|--------|----------------------|
| `swim_speed_up` | Faster movement in ink | Rotation, flanking, escaping |
| `run_speed_up` | Faster movement while shooting | Strafe fights, aggressive positioning |
| `quick_super_jump` | Faster super jump | Rotation, escaping danger |
| `stealth_jump` | Hidden super jump | Flanking, aggressive repositioning |

### Special-Focused Abilities

Center gameplay around special weapons.

| Ability | Effect | Strategic Implication |
|---------|--------|----------------------|
| `special_charge_up` | Build special faster | Special-centric playstyle |
| `special_power_up` | Stronger special effects | Special investment, timing-based |
| `special_saver` | Keep charge on death | Special preservation |

### Ink Efficiency Abilities

Sustain ink output over time.

| Ability | Effect | Strategic Implication |
|---------|--------|----------------------|
| `ink_saver_main` | Less main weapon ink usage | Sustained fire, painting |
| `ink_saver_sub` | Less sub weapon ink usage | Sub-focused builds |
| `ink_recovery_up` | Faster ink tank refill | Sustained pressure |

### Defensive Abilities

Protect against enemy effects.

| Ability | Effect | Strategic Implication |
|---------|--------|----------------------|
| `ink_resistance_up` | Reduced enemy ink damage | Frontline fighting |
| `sub_resistance_up` | Reduced sub weapon damage | Counter-sub, defensive |
| `intensify_action` | Squid surge, squid roll buffs | Evasive maneuvers |

### Aggressive/Slayer Abilities

Abilities that enhance kill potential.

| Ability | Effect | Strategic Implication |
|---------|--------|----------------------|
| `ninja_squid` | No ripples while swimming | Flanking, ambush |
| `stealth_jump` | Hidden landing marker | Aggressive rotation |
| `thermal_ink` | Track damaged enemies | Hunting, finishing kills |
| `respawn_punisher` | Punish enemy deaths | Commit to kills |

### Situational/Utility Abilities

Niche or situational effects.

| Ability | Effect | Strategic Implication |
|---------|--------|----------------------|
| `opening_gambit` | Strong start-of-game buff | Opening rushes, early aggression |
| `last_ditch_effort` | End-of-game buff | Clutch plays, overtime |
| `comeback` | Post-death buff | Death-accepting aggression |
| `tenacity` | Special charge when team disadvantaged | Team support |
| `object_shredder` | Damage to non-player objects | Objective control |
| `drop_roller` | Roll on super jump landing | Safe aggression, repositioning |
| `haunt` | Track killer after death | Information after death |

## Semantic Oppositions

Some ability groupings are conceptually opposed:

| Concept A | vs | Concept B |
|-----------|-----|-----------|
| Death-accepting (QR, SS, CB) | | Death-averse (survival builds) |
| Special-focused (SCU) | | Paint/efficiency-focused (ISM, ISS) |
| Aggressive (ninja_squid, SJ) | | Defensive (IR, SR) |
| Frontline (RSU, ninja_squid) | | Backline (SSU, QSJ) |

## Interpretation Patterns

### Pattern: Death-Mitigation Suppression

**If observed**: `quick_respawn`, `special_saver`, `comeback` appear as suppressors (low high_rate_ratio)

**Interpretation**: Feature encodes builds that **avoid dying**. Players with high activation prioritize survival over respawn efficiency.

**Example label**: "Death-Averse Special Build" or "Clean SCU Stacker (no death perks)"

### Pattern: SCU + Opening Gambit Enhancement

**If observed**: `special_charge_up` + `opening_gambit` both enhanced

**Interpretation**: Feature encodes aggressive opening special rushes. Get special fast, use it early.

**Example label**: "Opening Special Rush" or "First Special Aggression"

### Pattern: Mobility + Slayer Enhancement

**If observed**: `ninja_squid`, `stealth_jump`, `swim_speed_up` enhanced

**Interpretation**: Feature encodes flanking/slayer playstyle.

**Example label**: "Aggressive Flanker Kit"

### Pattern: Defensive Suppression

**If observed**: `ink_resistance_up`, `sub_resistance_up` suppressed

**Interpretation**: Feature prefers builds that don't need defensive abilities (perhaps ranged or support).

**Example label**: "Backline Support (no frontline abilities)"

## Common Misinterpretations

| What You See | Naive Interpretation | Better Interpretation |
|--------------|---------------------|----------------------|
| SCU dominant | "SCU detector" | Check for suppressed abilities to understand WHAT KIND of SCU |
| Death perks suppressed | "Anti-death feature" | "Death-AVERSE build" - players who don't plan to die |
| Mobility enhanced | "Mobility detector" | Check if specific mobility type (flanking vs rotation) |
| Single weapon class | "Weapon-specific" | Check ability patterns - might be playstyle, not weapon |

## Checklist for Semantic Validation

After forming a hypothesis, verify:

1. [ ] Does the enhancer pattern match a known semantic group?
2. [ ] Does the suppressor pattern match an opposing semantic group?
3. [ ] Is the interpretation consistent with gameplay strategy?
4. [ ] Could there be a simpler explanation (pure token detection)?
5. [ ] Does the weapon distribution support the semantic interpretation?

## See Also

- **mechinterp-investigator**: Overall investigation workflow
- **mechinterp-overview**: Now includes bottom tokens (suppressors)
- **token_influence_sweep**: Experiment type for detailed influence analysis
