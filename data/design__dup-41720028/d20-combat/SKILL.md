---
name: d20-combat
description: This skill should be used when the GM needs to handle combat situations, including starting combat, rolling initiative, resolving attack rolls, managing combat encounters, rolling damage, tracking hit points, applying conditions, or running d20-style tactical combat. Provides combat flow, turn structure, attack resolution, and condition references.
version: 1.0.0
---

# Combat Management Skill

Use this skill to guide d20-style combat encounters. Combat follows a structured turn order determined by initiative, with each participant taking actions to attack, defend, cast spells, or interact with the environment.

## Starting Combat

When combat begins, establish these elements in order:

1. **Establish positions** - Determine where combatants are located relative to each other
2. **Roll initiative** - All combatants roll to determine turn order
3. **Take turns** - Proceed through rounds until combat ends

### Rolling Initiative

Each combatant rolls initiative to determine turn order:

```
Initiative = d20 + Dexterity modifier
```

Use the corvran dice-roller skill for initiative rolls:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/../corvran/skills/dice-roller/scripts/roll.sh" "1d20+2"
```

Order combatants from highest to lowest initiative. Ties between players are resolved by player choice; ties between monsters use GM discretion.

**Surprise**: If a combatant is surprised (unaware combat is starting), they have Disadvantage on their initiative roll.

## Turn Structure

On each turn, a combatant can take the following in any order:

### Movement
Move up to your Speed (typically 30 feet). Movement can be split before and after your action.

### Action (pick one)
| Action | Effect |
|--------|--------|
| **Attack** | Make one attack with a weapon or Unarmed Strike |
| **Cast a Spell** | Cast a spell with a casting time of 1 action |
| **Dash** | Gain extra movement equal to your Speed |
| **Disengage** | Your movement doesn't provoke Opportunity Attacks this turn |
| **Dodge** | Attack rolls against you have Disadvantage; DEX saves have Advantage |
| **Help** | Give an ally Advantage on their next attack or ability check |
| **Hide** | Make a Stealth check to become hidden |
| **Ready** | Prepare an action to trigger on a specific condition |
| **Search** | Make a Perception, Insight, Medicine, or Survival check |
| **Study** | Make an Intelligence check to recall information |
| **Utilize** | Use a nonmagical object |

### Bonus Action
Only available if a feature, spell, or ability grants one. Examples include:
- Two-Weapon Fighting (attack with off-hand weapon)
- Cunning Action (Rogue)
- Certain spells (Healing Word, Misty Step)

### Reaction (once per round)
Triggered by specific events. Resets at the start of your next turn.
- **Opportunity Attack**: When a creature leaves your reach
- **Ready**: The trigger you defined occurs
- **Certain spells**: Shield, Counterspell

### Free Interaction
One free object interaction per turn (draw a weapon, open a door, pick up an item).

## Making Attack Rolls

To attack, roll d20 and add modifiers, then compare to target's Armor Class (AC):

```
Attack Roll = d20 + Ability Modifier + Proficiency Bonus (if proficient)
```

### Attack Types

| Attack Type | Ability Used |
|-------------|--------------|
| Melee weapon | Strength (or DEX with Finesse) |
| Ranged weapon | Dexterity |
| Unarmed Strike | Strength |
| Spell attack | Spellcasting ability |

### Attack Roll Outcomes

- **Roll >= AC**: Hit. Roll damage.
- **Roll < AC**: Miss. No damage.
- **Natural 20**: Critical Hit. Always hits. Double all damage dice.
- **Natural 1**: Automatic miss regardless of modifiers.

Use the dice-roller for attack rolls:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/../corvran/skills/dice-roller/scripts/roll.sh" "1d20+5"
```

### Advantage and Disadvantage

- **Advantage**: Roll 2d20, use the higher result
- **Disadvantage**: Roll 2d20, use the lower result
- Multiple sources don't stack
- Having both cancels to a normal roll

Common sources of Advantage:
- Attacking while hidden/invisible
- Target is prone (melee attacks)
- Target can't see you
- Help action from an ally

Common sources of Disadvantage:
- Target is prone (ranged attacks)
- You can't see the target
- Ranged attack while enemy is within 5 feet
- Certain conditions (Frightened, Poisoned, Restrained)

## Damage Rolls

On a hit, roll the weapon's damage dice plus your ability modifier:

```
Damage = Weapon Dice + Ability Modifier
```

Use the dice-roller for damage:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/../corvran/skills/dice-roller/scripts/roll.sh" "1d8+3"
```

### Common Weapon Damage

| Weapon | Damage | Type |
|--------|--------|------|
| Dagger | 1d4 + modifier | Piercing |
| Shortsword | 1d6 + modifier | Piercing |
| Longsword | 1d8 + modifier | Slashing |
| Greatsword | 2d6 + modifier | Slashing |
| Shortbow | 1d6 + modifier | Piercing |
| Longbow | 1d8 + modifier | Piercing |

### Critical Hit Damage

Roll all damage dice twice, then add modifiers once:

```
Critical Damage = (Weapon Dice x 2) + Ability Modifier
```

Example: Longsword critical = 2d8 + STR modifier

## Opportunity Attacks

When a creature you can see leaves your melee reach using its movement, action, or reaction, you may use your reaction to make one melee attack against it.

**Avoiding Opportunity Attacks**:
- Take the Disengage action
- Teleport
- Be moved by an external force (not your own movement)

## Special Combat Situations

### Cover
| Cover Type | Benefit |
|------------|---------|
| Half Cover | +2 AC and DEX saves |
| Three-Quarters Cover | +5 AC and DEX saves |
| Total Cover | Can't be targeted directly |

### Ranged Attacks in Melee
Making a ranged attack while within 5 feet of a hostile creature imposes Disadvantage.

### Two-Weapon Fighting
When you take the Attack action with a light melee weapon, you can use your bonus action to attack with a different light melee weapon in your other hand. Don't add your ability modifier to the damage of the bonus attack (unless negative).

### Grappling
Use an Unarmed Strike to grapple. Target makes STR or DEX save (their choice) vs DC 8 + your STR modifier + proficiency bonus. On failure, target has the Grappled condition.

### Shoving
Use an Unarmed Strike to shove. Same save as grappling. On failure, push target 5 feet or knock them Prone.

## Conditions Quick Reference

Combat frequently applies conditions. See `references/conditions.md` for full details.

| Condition | Key Effect |
|-----------|------------|
| **Blinded** | Auto-fail sight checks; attacks have Disadvantage |
| **Charmed** | Can't attack charmer; charmer has social Advantage |
| **Frightened** | Disadvantage on attacks/checks while source visible |
| **Grappled** | Speed 0; Disadvantage on attacks vs non-grappler |
| **Incapacitated** | Can't take actions, bonus actions, or reactions |
| **Invisible** | Advantage on attacks; attacks against have Disadvantage |
| **Paralyzed** | Incapacitated; auto-fail STR/DEX saves; auto-crit if hit |
| **Prone** | Disadvantage on attacks; melee attacks have Advantage against |
| **Restrained** | Speed 0; attacks have Disadvantage; Disadvantage on DEX saves |
| **Stunned** | Incapacitated; auto-fail STR/DEX saves |
| **Unconscious** | Incapacitated; Prone; auto-fail STR/DEX saves; auto-crit |

## Death and Dying

### Dropping to 0 HP
- **Monsters**: Die immediately (unless GM rules otherwise)
- **Player Characters**: Fall unconscious and begin making Death Saving Throws

### Death Saving Throws
At the start of each turn while at 0 HP, roll d20:
- **10 or higher**: Success
- **Below 10**: Failure
- **Three successes**: Become Stable (unconscious but not dying)
- **Three failures**: Die
- **Natural 1**: Two failures
- **Natural 20**: Regain 1 HP and consciousness

### Stabilizing
Use the Help action with a DC 10 Medicine check to stabilize a dying creature. A stable creature regains 1 HP after 1d4 hours.

## Encounter Templates

For encounter setup and tracking, see `references/encounter-template.md` and `references/encounter-example.md`.

## Dice Roller Fallback

If the corvran dice-roller skill is unavailable, describe the required roll and ask the player for the result:

> "Roll 1d20+5 for your attack against the goblin (AC 15). What did you get?"

---

*Combat rules derived from SRD 5.2.1, licensed under CC-BY-4.0.*
