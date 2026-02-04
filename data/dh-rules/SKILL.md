---
name: dh-rules
description: This skill should be used when the GM needs to look up Daggerheart rules, reference what the SRD says, find official rules, get exact wording, check RAW (rules as written), verify rules references, or understand how mechanics work in Daggerheart. Provides authoritative rule clarification from the Daggerheart System Reference Document 1.0.
version: 1.0.0
---

# Daggerheart SRD Rule Lookup Skill

Provide authoritative rule lookups from the Daggerheart System Reference Document 1.0 (SRD 1.0). Use the SRD markdown files in this skill's references directory to answer questions about official Daggerheart rules.

## When to Use This Skill

This skill applies when the user:
- Asks "what does the SRD say about..."
- Requests "official Daggerheart rules for..."
- Wants "exact wording of..."
- Asks for "RAW" (rules as written)
- Needs to verify a rule during gameplay
- Questions how a Daggerheart mechanic works
- Needs to look up adversary stat blocks
- Needs class feature or ability details
- Needs domain card descriptions

## SRD Directory Organization

The SRD files are located at `${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/`:

| Directory | Contents |
|-----------|----------|
| `abilities/` | Domain cards and abilities (Arcana, Blade, Bone, etc.) |
| `adversaries/` | Adversary stat blocks by name |
| `ancestries/` | Ancestry features and options |
| `armor/` | Armor definitions and stats |
| `classes/` | Class definitions (9 classes: Bard, Druid, Guardian, Ranger, Rogue, Seraph, Sorcerer, Warrior, Wizard) |
| `communities/` | Community features and options |
| `consumables/` | Consumable item definitions |
| `contents/` | Core rules (Combat, Character Creation, etc.) |
| `domains/` | Domain descriptions (9 domains: Arcana, Blade, Bone, Codex, Grace, Midnight, Sage, Splendor, Valor) |
| `environments/` | Environmental rules and hazards |
| `frames/` | Campaign frame content |
| `items/` | General item definitions |
| `subclasses/` | Subclass definitions |
| `weapons/` | Weapon definitions and stats |
| `.build/md/` | Compiled reference files |

## Search Patterns for SRD Files

For efficient searching of SRD content, use grep with the following patterns.

### Searching Adversaries

Each adversary has its own file in `adversaries/`. Use case-insensitive search:

```bash
# Find a specific adversary by name (exact match)
cat "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/adversaries/Bear.md"

# Find adversaries by partial name (list matching files)
ls "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/adversaries/" | grep -i "zombie"

# Search across all adversaries for a keyword (e.g., tier, type)
grep -ri "Tier 2" "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/adversaries/"

# Find all Bruiser type adversaries
grep -ri "Bruiser" "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/adversaries/" | head -20

# Find adversaries with Fear Features
grep -ri "Fear Feature" "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/adversaries/"
```

### Searching Classes

Each class has its own file in `classes/`:

```bash
# Read a specific class
cat "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/classes/Guardian.md"

# Search for a class feature across all classes
grep -ri "Evasion" "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/classes/"

# List all class files
ls "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/classes/"
```

### Searching Domain Cards (Abilities)

Domain cards are in `abilities/`, one file per card:

```bash
# Find a specific domain card by name
cat "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/abilities/Fireball.md" 2>/dev/null

# Search for domain cards by partial name
ls "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/abilities/" | grep -i "bolt"

# Find all cards in a specific domain
grep -ri "Arcana" "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/abilities/" | head -30

# Search for cards by effect keyword
grep -ri "damage" "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/abilities/" | head -20

# Find cards by recall cost
grep -ri "Recall Cost" "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/abilities/"
```

### Searching Core Rules (Contents)

Core rules are in `contents/`:

```bash
# List available core rule documents
ls "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/contents/"

# Search for a specific rule across all core content
grep -ri "Critical Success" "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/contents/"

# Search for Hope/Fear mechanics
grep -ri "Hope" "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/contents/" | head -20
grep -ri "Fear" "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/contents/" | head -20

# Search for combat rules
grep -ri "Action Roll" "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/contents/"
```

### Searching Domains

Domain descriptions are in `domains/`:

```bash
# Read a specific domain
cat "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/domains/Arcana.md"

# List all domains
ls "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/domains/"
```

### Searching Ancestries and Communities

```bash
# List available ancestries
ls "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/ancestries/"

# List available communities
ls "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/communities/"

# Search for a specific ancestry feature
grep -ri "Feature" "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/ancestries/"
```

### Searching Equipment

```bash
# List weapons
ls "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/weapons/"

# List armor
ls "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/armor/"

# Search for a weapon by name
cat "${CLAUDE_PLUGIN_ROOT}/skills/dh-rules/references/srd/weapons/Longsword.md" 2>/dev/null
```

## Response Format

When answering rule questions:

1. Quote the exact SRD text first (use blockquotes)
2. Cite the source file
3. Explain or clarify if needed
4. Note any related rules

Example response:

> From `contents/Combat.md`:
>
> **Critical Success**
> When you roll doubles on your Duality Dice (both dice show the same value), you achieve a Critical Success. This counts as a success with Hope, plus you gain an additional Hope token.

This means rolling 4-4, 7-7, or any matching pair triggers a Critical Success.

## Attribution Requirement

When quoting substantial portions of the SRD in any output, include the DPCGL attribution:

> This work includes material from the Daggerheart System Reference Document 1.0, published by Darrington Press. Daggerheart and all related marks are trademarks of Critical Role, LLC and used under the Darrington Press Community Gaming License (DPCGL). See https://www.daggerheart.com/ for full license terms.

## Common Rule Categories

Quick reference for which directory to search:

| Question About | Search Location |
|----------------|-----------------|
| How combat works | `contents/` (Combat.md) |
| Action rolls, Hope/Fear | `contents/` |
| Class features | `classes/[class].md` |
| Subclass features | `subclasses/` |
| Domain cards | `abilities/` |
| Domain descriptions | `domains/` |
| Adversary stat block | `adversaries/[name].md` |
| Ancestry features | `ancestries/` |
| Community features | `communities/` |
| Weapon stats | `weapons/` |
| Armor stats | `armor/` |
| Consumables | `consumables/` |
| Environmental hazards | `environments/` |

## Notes

- The SRD contains only content released under the DPCGL; some published content may be excluded
- Adversary files use individual markdown files per adversary (unlike d20's single large file)
- Domain cards are individual files in `abilities/` with domain indicated in content
- File names may contain spaces; use quotes in paths when necessary
- For quick lookups, `cat` the specific file; for broad searches, use `grep -ri`
