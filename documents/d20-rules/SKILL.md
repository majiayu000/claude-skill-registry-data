---
name: d20-rules
description: This skill should be used when the GM needs to look up rules, reference what the SRD says, find official rules, get exact wording, check RAW (rules as written), verify rules references, or understand how mechanics work in d20 5E. Provides authoritative rule clarification from the System Reference Document 5.2.
version: 1.0.0
---

# SRD Rule Lookup Skill

Provide authoritative rule lookups from the System Reference Document 5.2 (SRD 5.2). Use the complete SRD markdown files in this skill's references directory to answer questions about official d20 5E rules.

## When to Use This Skill

This skill applies when the user:
- Asks "what does the SRD say about..."
- Requests "official rules for..."
- Wants "exact wording of..."
- Asks for "RAW" (rules as written)
- Needs to verify a rule during gameplay
- Questions how a mechanic works

## SRD File Organization

The SRD files are located at `${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/`:

| File | Contents | Size |
|------|----------|------|
| `00_Legal.md` | CC-BY-4.0 attribution (required for any derivative work) | 1KB |
| `01_PlayingTheGame.md` | Core mechanics: abilities, D20 tests, actions, combat, damage | 62KB |
| `02_CharacterCreation.md` | Character creation rules and process | 47KB |
| `03_Classes/` | Class descriptions (12 files, one per class) | 264KB |
| `04_CharacterOrigins.md` | Backgrounds, species, and origin features | 17KB |
| `05_Feats.md` | Feat descriptions and requirements | 8KB |
| `06_Equipment.md` | Weapons, armor, adventuring gear, trade goods | 65KB |
| `07_Spells.md` | All spell descriptions (A-Z) | 325KB |
| `08_RulesGlossary.md` | Alphabetical rules definitions | 70KB |
| `09_GameplayToolbox.md` | Optional rules and DM tools | 48KB |
| `10_MagicItems.md` | Magic item descriptions | 218KB |
| `11_Monsters.md` | Monster creation and CR rules | 17KB |
| `12_MonstersA-Z.md` | All monster stat blocks (A-Z) | 333KB |
| `13_Animals.md` | Animal stat blocks and mounts | 70KB |

## Search Patterns for Large Files

For efficient searching of large SRD files, use grep with the following patterns.

### Searching Spells (07_Spells.md)

Spells are organized under `#### Spell Name` headings. Use case-insensitive search:

```bash
# Find a specific spell (show 40 lines for full description)
grep -i -A 40 "^#### Fireball" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/07_Spells.md"

# Find a specific spell by partial name
grep -i -A 40 "^#### .*Lightning" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/07_Spells.md"

# List all spells starting with a letter
grep "^#### " "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/07_Spells.md" | grep -i "^#### A"

# Search spell descriptions for keywords (e.g., concentration spells)
grep -i -B 2 "Concentration" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/07_Spells.md" | grep -i "^####"
```

### Searching Monsters (12_MonstersA-Z.md)

Monsters are organized under `## Monster Name` headings:

```bash
# Find a specific monster (show 60 lines for full stat block)
grep -i -A 60 "^## Adult Red Dragon" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/12_MonstersA-Z.md"

# Find monsters by partial name
grep -i -A 60 "^## .*Zombie" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/12_MonstersA-Z.md"

# List all monsters
grep "^## " "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/12_MonstersA-Z.md"

# Find monsters by CR (search for "CR X" pattern in stat blocks)
grep -B 10 "CR 5" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/12_MonstersA-Z.md" | grep "^##"
```

### Searching Magic Items (10_MagicItems.md)

Magic items use `#### Item Name` headings:

```bash
# Find a specific magic item
grep -i -A 30 "^#### Bag of Holding" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/10_MagicItems.md"

# Find all items of a rarity
grep -i -B 2 "Rare" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/10_MagicItems.md" | grep "^####"
```

### Searching Rules Glossary (08_RulesGlossary.md)

Rules definitions use `#### Term` headings:

```bash
# Find a specific rule definition
grep -i -A 15 "^#### Advantage" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/08_RulesGlossary.md"

# Find rules mentioning a condition
grep -i -A 15 "^#### Frightened" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/08_RulesGlossary.md"

# List all rule definitions
grep "^#### " "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/08_RulesGlossary.md"
```

### Searching Classes (03_Classes/)

Each class has its own file:

```bash
# Find class features
grep -i -A 20 "^## " "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/03_Classes/05_Fighter.md"

# Search all classes for a feature name
grep -ri "Extra Attack" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/03_Classes/"
```

### Searching Equipment (06_Equipment.md)

```bash
# Find weapon properties
grep -i -A 5 "^#### Heavy" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/06_Equipment.md"

# Find armor stats
grep -i -A 10 "^#### Chain Mail" "${CLAUDE_PLUGIN_ROOT}/skills/d20-rules/references/srd/06_Equipment.md"
```

## Response Format

When answering rule questions:

1. Quote the exact SRD text first (use blockquotes)
2. Cite the source file
3. Explain or clarify if needed
4. Note any related rules

Example response:

> From `08_RulesGlossary.md`:
>
> **Advantage**
> If you have Advantage on a D20 Test, roll two d20s, and use the higher roll. A roll can't be affected by more than one Advantage, and Advantage and Disadvantage on the same roll cancel each other.

This means having multiple sources of Advantage doesn't stack - you still only roll two dice.

## Attribution Requirement

When quoting substantial portions of the SRD in any output, include the CC-BY-4.0 attribution from `00_Legal.md`:

> This work includes material from the System Reference Document 5.2 ("SRD 5.2") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.

## Common Rule Categories

Quick reference for which file to search:

| Question About | Search File |
|----------------|-------------|
| How combat works | `01_PlayingTheGame.md` (## Combat) |
| Ability checks, saves | `01_PlayingTheGame.md` (## D20 Tests) |
| Conditions (blinded, prone, etc.) | `08_RulesGlossary.md` |
| Spell effect/description | `07_Spells.md` |
| Monster stat block | `12_MonstersA-Z.md` |
| Weapon/armor stats | `06_Equipment.md` |
| Class feature | `03_Classes/[class].md` |
| Magic item effect | `10_MagicItems.md` |
| Rest rules | `08_RulesGlossary.md` (#### Long Rest, #### Short Rest) |
| Death and dying | `01_PlayingTheGame.md` (## Damage and Healing) |
| Cover, visibility | `01_PlayingTheGame.md` |
| Encounter building | `09_GameplayToolbox.md` |

## Notes

- The SRD contains only rules released under CC-BY-4.0; some PHB content is excluded
- Spell lists are in `07_Spells.md` under `### Class Spell Lists`
- Creature types and their traits are in `11_Monsters.md`
- For animal companions and mounts, check `13_Animals.md`
