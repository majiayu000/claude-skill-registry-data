---
name: dh-domains
description: This skill should be used when handling domain cards and magical abilities in Daggerheart, including looking up domain card effects, understanding Recall costs, making Spellcast Rolls, selecting domain cards during character creation or advancement, or when players want to use domain-based abilities. Covers all 9 SRD domains (Arcana, Blade, Bone, Codex, Grace, Midnight, Sage, Splendor, Valor) and their associated cards.
version: 1.0.0
---

# Domain Cards Skill

Provides guidance for handling domain cards and magical abilities in Daggerheart adventures. Domain cards represent a character's magical or specialized abilities, organized into 9 thematic domains.

**Authoritative Source**: For exact rule wording, use the `dh-rules` skill to reference `srd/contents/Classes.md` and `srd/contents/Domain Card Reference.md`.

## The Nine Domains

Each domain represents a thematic school of power. Characters gain access to domains through their class, typically having access to 2 domains.

| Domain | Focus | Classes with Access |
|--------|-------|---------------------|
| **Arcana** | Innate magic, elements, raw power | Druid, Sorcerer |
| **Blade** | Weapon mastery, martial prowess | Guardian, Warrior |
| **Bone** | Tactics, body control, combat awareness | Ranger, Warrior |
| **Codex** | Magical study, books of power | Bard, Wizard |
| **Grace** | Charisma, charm, language mastery | Bard, Rogue |
| **Midnight** | Shadows, secrecy, stealth | Rogue, Sorcerer |
| **Sage** | Nature, beasts, natural world | Druid, Ranger |
| **Splendor** | Life, healing, light | Seraph, Wizard |
| **Valor** | Protection, shields, defensive power | Guardian, Seraph |

For detailed domain descriptions and class associations, see `references/domain-overview.md`.

## Domain Card Anatomy

Each domain card includes six elements:

| Element | Description |
|---------|-------------|
| **Level** | 1-10, determines when the card becomes available. You cannot acquire a card with a level higher than your PC's. |
| **Domain** | Symbol indicating which domain the card belongs to. You can only choose cards from your class's two domains. |
| **Recall Cost** | Stress spent to swap this card from your **vault** to your **loadout** (see Loadout & Vault below). |
| **Title** | The card's name. |
| **Type** | One of three types: **abilities** (typically non-magical), **spells** (magical), or **grimoires** (Codex domain only, grants collections of lesser spells). |
| **Feature** | The card's effect, including any special rules for using it. |

### Example Card

```
# CHAIN LIGHTNING

> **Level 5 Arcana Spell**
> **Recall Cost:** 1

Mark 2 Stress to make a Spellcast Roll, unleashing lightning on all
targets within Close range. Targets you succeed against must make a
reaction roll with a Difficulty equal to the result of your Spellcast
Roll. Targets who fail take 2d8+4 magic damage. Additional adversaries
not already targeted and within Close range of previous targets who
took damage must also make the reaction roll...
```

## Spellcast Rolls

Many domain cards require a Spellcast Roll. This is a standard Duality Dice action roll.

### Making a Spellcast Roll

```bash
bash "${CLAUDE_PLUGIN_ROOT}/../corvran/skills/dice-roller/scripts/roll.sh" "DdD+[trait]"
```

**Spellcast Trait**: Determined by your **subclass**, not class. Each subclass specifies which trait is used for all Spellcast Rolls. Guardian and Warrior subclasses have no Spellcast Trait (martial classes).

| Class | Subclass | Spellcast Trait |
|-------|----------|-----------------|
| Bard | Troubadour | Presence |
| Bard | Wordsmith | Presence |
| Druid | Warden of Renewal | Instinct |
| Druid | Warden of the Elements | Instinct |
| Ranger | Beastbound | Agility |
| Ranger | Wayfinder | Agility |
| Rogue | Nightwalker | Finesse |
| Rogue | Syndicate | Finesse |
| Seraph | Divine Wielder | Strength |
| Seraph | Winged Sentinel | Strength |
| Sorcerer | Elemental Origin | Instinct |
| Sorcerer | Primal Origin | Instinct |
| Wizard | School of Knowledge | Knowledge |
| Wizard | School of War | Knowledge |

### Spellcast Roll Targets

Some cards specify a target number in parentheses:

> "Make a Spellcast Roll (13)..."

The number in parentheses is the Difficulty. Compare your roll total to this number.

### Spellcast Outcomes

Spellcast Rolls follow standard action roll outcomes:

| Outcome | Condition | Effect |
|---------|-----------|--------|
| Critical Success | Both dice match | Automatic success, enhanced effect |
| Success with Hope | Total >= Difficulty, hope die higher | Success, player gains Hope |
| Success with Fear | Total >= Difficulty, fear die higher | Success, GM gains Fear |
| Failure with Hope | Total < Difficulty, hope die higher | Failure, player gains Hope |
| Failure with Fear | Total < Difficulty, fear die higher | Failure, GM gains Fear |

Some cards have different effects on success vs. failure (like Healing Hands).

## Loadout & Vault

Your **loadout** is the set of domain cards whose effects your PC can use during play. You can have up to **5 domain cards** in your loadout at one time.

Once you've acquired six or more domain cards, you must choose five to keep in your loadout; the rest are in your **vault**. Vault cards are inactive and do not influence play.

> **Note**: Subclass, ancestry, and community cards don't count toward your loadout or vault - they're always active.

### Managing Cards

**At the start of a rest** (before downtime moves): Freely swap cards between loadout and vault at no cost, as long as your loadout doesn't exceed 5 cards.

**At any other time**: To move a card from vault to loadout, mark Stress equal to the card's **Recall Cost**. If your loadout is full, you must also move a card to your vault (at no cost).

**When gaining a new card at level-up**: You can immediately add it to your loadout for free. If full, move another card to vault.

### Usage Limits

Some domain cards restrict how often they can be used (e.g., "once per rest"). Track these limits separately using whatever method you prefer - turning the card sideways, flipping it facedown, or using tokens.

> **Note**: If an effect gives you uses equal to a trait with modifier +0 or less, it grants 0 uses.

### Using a Domain Card

When a character uses a domain card:

1. **Verify Card is in Loadout**: Only loadout cards can be used
2. **Pay Any Activation Cost**: Some cards require marking Stress to activate
3. **Make Spellcast Roll** (if required): Roll DdD + Spellcast Trait vs. Difficulty
4. **Resolve Effect**: Apply the card's outcome
5. **Track Usage Limit** (if applicable): Mark if the card has limited uses

## Card Selection

### At Character Creation

PCs acquire **two 1st-level domain cards** at character creation. Each domain offers 3 options at Level 1. Choose from your class's two domains (you can take both from one domain or one from each).

### At Level-Up

Each time you level up, gain **one additional domain card** at or below your new level. Levels 2-10 typically offer 2 options per domain per level.

### Loadout Limit

Your loadout holds a maximum of **5 domain cards**. Once you have 6+ cards total, excess cards go to your vault.

## Looking Up Domain Cards

### Full Card Content

Domain card details are in the Daggerheart SRD. Use the dh-rules skill to search:

```bash
# Find a specific card
grep -ri "CARD_NAME" "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/abilities/"

# List all cards in a domain
cat "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/domains/[Domain].md"
```

### Domain Overview

For quick reference on all 9 domains and their thematic focus, see:
- `references/domain-overview.md`

### Full Domain Content

For complete domain card listings with all options by level, reference the SRD:
- `dh-rules/references/srd/domains/` - Domain descriptions and card tables
- `dh-rules/references/srd/abilities/` - Individual card details

## Quick Reference

### Spellcast Roll Formula
```
DdD + Spellcast Trait (from subclass) vs. Difficulty
```

### Loadout Rules
- Maximum **5 domain cards** in loadout
- Swap freely at start of rest (no cost)
- Swap mid-session by paying **Recall Cost** in Stress

### Domain-Class Access
| Class | Domains |
|-------|---------|
| Bard | Codex, Grace |
| Druid | Arcana, Sage |
| Guardian | Blade, Valor |
| Ranger | Bone, Sage |
| Rogue | Grace, Midnight |
| Seraph | Splendor, Valor |
| Sorcerer | Arcana, Midnight |
| Warrior | Blade, Bone |
| Wizard | Codex, Splendor |

## References

- `references/domain-overview.md` - Summary of all 9 domains with thematic descriptions
- `../dh-rules/references/srd/domains/` - Full SRD domain content (via symlink)
- `../dh-rules/references/srd/abilities/` - Full SRD domain card content (via symlink)
