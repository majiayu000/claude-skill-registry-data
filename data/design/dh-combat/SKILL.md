---
name: dh-combat
description: This skill should be used when the GM needs to handle Daggerheart combat, including action roll resolution, Hope/Fear token economy, spotlight flow, damage tracking, reaction rolls, and managing combat encounters. Provides action outcome tables, encounter tracking templates, and condition references.
version: 1.0.0
---

# Daggerheart Combat Management Skill

Use this skill to guide Daggerheart combat encounters. Unlike d20-style initiative, Daggerheart uses spotlight flow where the GM takes action when player rolls result in Fear or failure. The Hope/Fear token economy creates narrative tension between player momentum and GM opportunity.

**Authoritative Source**: For exact rule wording, use the `dh-rules` skill to reference `srd/contents/Combat.md`, `srd/contents/Making Moves and Taking Action.md`, and `srd/contents/Death.md`.

## Starting Combat

When combat begins:

1. **Establish the scene** - Describe positions, threats, and environmental features
2. **Initialize token tracking** - Set up Hope (per player, max 6) and Fear (GM, max 12)
3. **Players act first** - The player who initiated the conflict typically takes the first spotlight
4. **Flow continues** - Spotlight passes based on roll outcomes

### Initial Token State

At combat start:
- **Player Hope**: Carry over from session state (PCs start with 2 Hope at character creation, max 6)
- **GM Fear**: Carry over from session state (max 12)

Use the encounter template from `references/encounter-template.md` to track state.

## The Spotlight System

Daggerheart doesn't use initiative. Instead, the spotlight flows based on action outcomes:

### When Players Hold Spotlight
- A player takes an action and rolls
- If **Success with Hope**: Party keeps spotlight (players choose who acts next)
- If **Success with Fear**: GM takes spotlight (rolled with Fear)
- If **Failure** (Hope or Fear): GM takes spotlight
- If **Critical Success**: Player succeeds with bonus, gains Hope, clears Stress

### When GM Takes Spotlight
- Adversaries act, Fear Features activate, dangers escalate
- After GM action, spotlight returns to a player
- GM can spend Fear tokens for additional effects

### Spotlight Flow Diagram

```
Player Action
    |
    v
Roll Duality Dice
    |
    +---> Success + Hope higher ---> Party keeps spotlight
    |                                (choose who acts next)
    |
    +---> Success + Fear higher ---> GM takes spotlight
    |                                (rolled with Fear)
    |
    +---> Failure (any) -----------> GM takes spotlight
    |                                (GM makes a move)
    |
    +---> Critical ------------------> Auto success + bonus
                                       (gain Hope, clear Stress)
```

## Action Roll Resolution

When a player attempts an action with uncertain outcome:

1. **Determine the trait** - Which of the six traits applies?
2. **Check for Experiences** - Does a bounded Experience apply? (Review positive scope)
3. **Set the difficulty** - Use standard difficulties or adversary Evasion
4. **Roll Duality Dice** - `DdD + Trait + Experience (if applicable)`
5. **Determine outcome** - See the five outcomes below

### Difficulty Reference

| Difficulty | Target Number |
|------------|---------------|
| Easy | 10 |
| Moderate | 15 |
| Hard | 20 |
| Formidable | 25 |
| Legendary | 30 |

### The Five Action Outcomes

See `references/action-outcomes.md` for detailed resolution tables.

| Outcome | Condition | Token Effect | Spotlight |
|---------|-----------|--------------|-----------|
| **Critical Success** | Both dice match | Gain Hope, clear Stress | Auto success with bonus |
| **Success with Hope** | Total >= difficulty, hope > fear | Player gains Hope | Party keeps |
| **Success with Fear** | Total >= difficulty, fear > hope | GM gains Fear | GM takes |
| **Failure with Hope** | Total < difficulty, hope > fear | Player gains Hope | GM takes |
| **Failure with Fear** | Total < difficulty, fear > hope | GM gains Fear | GM takes |

> **Note**: A Critical Success counts as a roll "with Hope."

**Tie between dice values** (non-critical): Player chooses Hope or Fear.

### Using the Dice Roller

```bash
bash "${CLAUDE_PLUGIN_ROOT}/../corvran/skills/dice-roller/scripts/roll.sh" "DdD+3"
```

Output:
```json
{
  "expression": "DdD+3",
  "rolls": [7, 4],
  "modifier": 3,
  "total": 14,
  "hope": 7,
  "fear": 4,
  "higher": "hope"
}
```

## Advantage and Disadvantage

Daggerheart uses additional d6 dice for advantage/disadvantage:

### Advantage (+d6)
Roll an additional d6 and **add** it to your total.

**Common sources**:
- Target is Hidden (against you, until revealed)
- Target is Vulnerable
- Target is Restrained
- Tactical superiority (high ground, flanking)

### Disadvantage (-d6)
Roll a d6 and **subtract** it from your total.

**Common sources**:
- You are Frightened (against source of fear)
- Poor visibility or conditions
- Attempting something beyond your training
- Attacking a Hidden target

### Multiple Advantages/Disadvantages
- Multiple advantages stack (roll multiple d6s, add all)
- Multiple disadvantages stack (roll multiple d6s, subtract all)
- Advantages and disadvantages cancel one-to-one

**Example**: 2 advantages and 1 disadvantage = 1 advantage = +1d6

## Reaction Rolls

Some abilities allow reactions outside normal spotlight flow. **Reaction rolls do NOT generate Hope or Fear tokens**.

### When Reactions Occur
- Specific class features trigger
- Certain adversary abilities respond
- Environmental events require immediate response

### Resolving Reactions
1. Roll Duality Dice as normal
2. Apply success/failure based on total vs. difficulty
3. **Skip token generation** - ignore which die was higher for economy purposes
4. Spotlight does NOT shift based on reaction results

## Attack and Damage Flow

### Making Attacks

1. Roll Duality Dice + appropriate trait + modifiers
2. Compare total to target's **Evasion**
3. If total >= Evasion, the attack hits
4. Roll damage and apply to target

### Damage Resolution

1. Roll weapon damage dice (Proficiency × damage die + modifier)
2. Compare total damage to target's **Damage Thresholds**
3. Mark HP slots based on severity:

| Damage vs Thresholds | HP Marked |
|---------------------|-----------|
| Below Major threshold | 1 HP |
| At or above Major, below Severe | 2 HP |
| At or above Severe | 3 HP |

If damage is reduced to 0 or less, no HP is marked.

> **Optional Rule - Massive Damage**: If damage equals twice the Severe threshold, mark 4 HP instead of 3.

### Armor Slots

Your **Armor Score** determines how many Armor Slots you have. When you take damage:
- You can mark 1 Armor Slot to reduce HP marked by 1
- This choice is made when marking HP
- Armor Slots don't reduce the damage number, they reduce HP marked

### HP and Stress Tracking

Use visual notation for quick scanning:

```markdown
## Current Status
- **HP Marked**: ●●○○○○ (2/6)
- **Stress Marked**: ●○○○○○ (1/6)
- **Armor Slots Used**: ●○○
```

## Hope/Fear Token Economy

### Hope Tokens (Per Player)

| Aspect | Details |
|--------|---------|
| Maximum | 6 per character |
| Gained | When hope die is higher on action rolls |
| Not gained | On reaction rolls or critical success |
| Overflow | Excess tokens are lost |

**Spending Hope**:
- Reroll a die
- Boost damage
- Activate certain class features
- Assist another player's roll

### Fear Tokens (GM)

| Aspect | Details |
|--------|---------|
| Maximum | 12 total |
| Gained | When fear die is higher on player action rolls |
| Not gained | On reaction rolls or critical success |
| Overflow | Excess tokens are lost |

**Spending Fear**:
- Activate adversary Fear Features (costs vary)
- Introduce environmental complications
- Have reinforcements arrive
- Escalate a threat beyond normal action

### Token Tracking Format

Use visual notation (per TD-4):

```markdown
## Hope/Fear Economy

### Player Hope
| Player | Hope (max 6) |
|--------|--------------|
| Kira   | ●●●○○○       |
| Thorn  | ●●○○○○       |

### GM Fear
Fear: ●●●●●○○○○○○○ (5/12)
```

## Stress and Conditions

### Stress Accumulation

Characters gain Stress from:
- Narrative consequences
- Failed Fear rolls (GM discretion)
- Certain ability effects
- Witnessing trauma

### Maximum Stress

When all Stress slots are marked, the character gains the **Vulnerable** condition.

### Clearing Stress

- **Short Rest**: Clear a few Stress (GM discretion)
- **Long Rest**: Clear all Stress
- **Roleplay**: Recovery scenes can clear Stress
- **Specific abilities**: Some class features clear Stress

### Standard Conditions

See `references/conditions.md` for full condition effects. Daggerheart has **three standard conditions**:

| Condition | Effect |
|-----------|--------|
| **Hidden** | All rolls against you have disadvantage. Ends when seen, you move into line of sight, or you attack. |
| **Restrained** | You can't move, but can still take actions from your current position. |
| **Vulnerable** | All rolls targeting you have advantage. |

> **Note**: Some features apply special or unique conditions that work as described in the feature text.

## Death and Dying

### When a PC Marks Their Last HP

When a PC marks their last Hit Point, they must make a **death move** by choosing one of three options:

#### Blaze of Glory
Your character embraces death and goes out in a blaze of glory. Take one final action—it automatically critically succeeds (with GM approval)—then your character dies.

#### Avoid Death
Your character avoids death and faces consequences. They drop unconscious and can't move, act, or be targeted by attacks. Work with the GM to describe how the situation worsens.

They return to consciousness when an ally clears 1+ HP or after a long rest. After falling unconscious, roll your Hope Die—if the result ≤ your level, gain a **scar**: permanently cross out a Hope slot and determine its narrative impact with the GM. If you ever cross out your last Hope slot, your character's journey ends.

#### Risk It All
Roll your Duality Dice:
- **Hope Die higher**: Stay on your feet, clear HP or Stress equal to the Hope Die value (divide as you choose)
- **Fear Die higher**: Your character dies
- **Matching dice**: Stay up but clear nothing

### When Adversaries Fall

When an adversary marks their last HP, they typically die or are defeated (GM discretion based on narrative).

## Encounter Management

Use the encounter template from `references/encounter-template.md` to track:

- GM Fear tokens
- Current spotlight holder
- Party HP/Stress/Hope per player
- Adversary HP/Stress/Conditions
- Active effects

### Example Encounter State

```markdown
## GM Fear
Fear: ●●●●●○○○○○○○ (5/12)

## Spotlight
Currently: GM (after Kira's Fear roll)

## Combatants

### Party
| PC    | HP       | Stress   | Hope     | Conditions |
|-------|----------|----------|----------|------------|
| Kira  | ●●○○○○   | ●○○○○○   | ●●●○○○   | -          |
| Thorn | ○○○○○○   | ●●○○○○   | ●●○○○○   | Frightened |

### Adversaries
| Adversary      | HP       | Stress | Conditions |
|----------------|----------|--------|------------|
| Bone Wraith    | ●●●○○○   | ●○○    | -          |
| Skeleton (x2)  | ●●○○     | -      | -          |
```

## GM Guidance: Running Combat Narratively

### Describe, Don't Just Resolve

Each roll outcome should advance the fiction:
- **Success with Hope**: "You strike true, and as the blade bites, you feel a surge of confidence—take a Hope token."
- **Success with Fear**: "Your attack lands, but you've overextended. The wraith's hollow eyes lock onto you—I'll take a Fear token and the spotlight."

### Spend Fear Actively

Fear tokens are narrative fuel. Spend them to:
- Make adversaries more dangerous at dramatic moments
- Introduce complications when the party seems too comfortable
- Create memorable villain moments

Don't hoard Fear—a pile of unspent tokens means missed opportunities.

### Spotlight Flow as Pacing

The spotlight system naturally creates dramatic pacing:
- Tension builds as Fear accumulates
- Players feel momentum when Hope flows
- GM spotlight moments punctuate player actions

## Dice Roller Fallback

If the corvran dice-roller skill is unavailable, describe the required roll:

> "Roll 2d12 for your action roll, adding your Presence modifier (+2). Tell me both dice values and the total. The higher die determines whether you gain Hope or I gain Fear."

---

*Combat rules derived from the Daggerheart SRD by Darrington Press, used under the DPCGL.*
