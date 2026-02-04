---
name: rpg-ruleset-cli
description: Manage and query tabletop RPG rulesets using the rpg-ruleset-cli tool with category theory-inspired categorical architecture. Use when users want to create, organize, search, or validate RPG rules, or work with theories, interpretations, worlds, entities, and transport functors.
---

# RPG Ruleset CLI

Use this skill when users want to work with tabletop RPG rulesets, including:
- Creating new systems with categorical architecture (theories → interpretations → worlds)
- Adding and managing rules with validation
- Querying rules with provenance tracking
- Transporting entities between worlds using functors
- Managing characters, objects, events, and locations

## CRITICAL: Always Use Absolute Paths

**IMPORTANT**: Always use absolute paths for all file and directory arguments. Relative paths may not work correctly with bazel run.

✓ **CORRECT**: `/home/xsaw/haskell-monorepo-dnd-rules/rpg/crossed-swords`
✗ **WRONG**: `rpg/crossed-swords` or `./rpg/crossed-swords`

This applies to:
- `init <PATH>` - Use absolute path for the directory to create
- `--data-dir <DIR>` - Use absolute path for the data directory
- `validate <FILE>` - Use absolute path for the file to validate

## Quick Command Reference

### Running the CLI
```bash
# All commands use this pattern:
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- [COMMAND] [OPTIONS]
```

### Available Commands

**init** - Initialize a new ruleset
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  init <PATH> --id <SYSTEM_ID> --name "System Name"
```

**add** - Add a new rule (auto-suggests ID)
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- add \
  -d <DATA_DIR> \
  --category <CATEGORY> \
  --title "Rule Title" \
  [--id RULE-ID] \
  [--visibility public|gm-only] \
  [--tag TAG1] [--tag TAG2]
```

**query** - Search for rules
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- query \
  -d <DATA_DIR> \
  [KEYWORDS...] \
  [--category CATEGORY] \
  [--system SYSTEM] \
  [--tag TAG] \
  [--limit N] \
  [--show-related]
```

**validate** - Validate rule files
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- validate \
  <FILE> \
  [--strict] \
  [--all]
```

**list** - List systems, categories, or rules
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- list \
  systems|categories|rules \
  [--system SYSTEM]
```

**info** - Show detailed rule information
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- info \
  <RULE_ID> \
  [--changelog]
```

## Categorical Commands (NEW)

The tool now supports a categorical architecture with three layers:

**Layer 1: Theories** - Abstract rule schemas
**Layer 2: Interpretations** - Concrete realizations of theories
**Layer 3: Worlds** - Playable game instances

### Theory Commands

**theory init** - Create a new base theory
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  theory init <THEORY_ID> --name "Theory Name"
```

**theory extend** - Extend an existing theory
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  theory extend <BASE_THEORY> <EXT_ID> --name "Extension Name"
```

**theory list** - List all theories
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  theory list [--show-extensions]
```

**theory info** - Show theory details
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  theory info <THEORY_ID>
```

### Interpretation Commands

**interp create** - Create a new interpretation
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  interp create <INTERP_ID> --name "Name" --theory <THEORY1> [--theory <THEORY2>...]
```

**interp realize** - Map abstract rule to concrete
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  interp realize <INTERP_ID> <ABSTRACT_ID> \
  --concrete <CONCRETE_ID> --title "Title" [--content <FILE>]
```

**interp list** - List all interpretations
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  interp list [--theory <THEORY>] [--show-completeness]
```

**interp validate** - Check interpretation completeness
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  interp validate <INTERP_ID> [--strict]
```

**interp info** - Show interpretation details
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  interp info <INTERP_ID>
```

### World Commands

**world create** - Create a new world
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  world create <WORLD_ID> --name "World Name" --interp <INTERP_ID>
```

**world list** - List all worlds
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  world list [--interp <INTERP_ID>]
```

**world info** - Show world details
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  world info <WORLD_ID> [--show-entities] [--show-transport]
```

### Entity Commands

**entity create** - Create a new entity
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  entity create <TYPE> <ENTITY_ID> \
  --world <WORLD_ID> --name "Name" [--file <YAML_FILE>]
```

Types: `character`, `object`, `event`, `location`

**entity list** - List entities in a world
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  entity list <TYPE> --world <WORLD_ID>
```

**entity show** - Show entity details
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  entity show <TYPE> <ENTITY_ID> --world <WORLD_ID>
```

### Transport Commands

**transport create-functor** - Create a transport functor
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  transport create-functor <FUNCTOR_ID> --name "Name" \
  --from <SOURCE_WORLD> --to <TARGET_WORLD> \
  --type <TYPE> [--map-file <FILE>]
```

Functor types: `FreeFunctor`, `ForgetfulFunctor`, `Projection`, `Embedding`

**transport entity** - Transport an entity between worlds
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  transport entity <TYPE> <ENTITY_ID> \
  --from <SOURCE_WORLD> --to <TARGET_WORLD> \
  --functor <FUNCTOR_ID> [--validate] [--dry-run]
```

**transport validate** - Validate a transport functor
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  transport validate <FUNCTOR_ID> [--check-adjunction]
```

**transport functor** - List transport functors
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  transport functor [--from <WORLD>] [--to <WORLD>]
```

### Global Options
- `--data-dir, -d DIR` - Root directory containing rulesets (default: ".")
- `--role, -r ROLE` - User role: player or gm (default: player)
- `--format, -f FORMAT` - Output format: text, json, markdown (default: text)
- `--verbose, -v` - Enable verbose output

## Common Workflows

### Workflow 0: Complete Categorical Workflow (NEW)

This demonstrates the full categorical architecture:

```bash
# Layer 1: Create Theory (Abstract Rules)
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  theory init fantasy-core --name "Fantasy Core Theory" -d /absolute/path

# Layer 2: Create Interpretation (Concrete Rules)
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  interp create crossed-swords --name "Crossed Swords" \
  --theory fantasy-core -d /absolute/path

# Realize abstract rules to concrete
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  interp realize crossed-swords THEORY-COMBAT-001 \
  --concrete CORE-001 --title "Attack Resolution" -d /absolute/path

# Validate interpretation completeness
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  interp validate crossed-swords -d /absolute/path

# Layer 3: Create World (Playable Instance)
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  world create my-campaign --name "Northern Realms" \
  --interp crossed-swords -d /absolute/path

# Add Entities
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  entity create character sir-aldric \
  --world my-campaign --name "Sir Aldric" -d /absolute/path

# Create second world
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  world create shadow-realm --name "Shadow Realm" \
  --interp shadow-interp -d /absolute/path

# Create transport functor
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  transport create-functor light-to-shadow \
  --name "Corruption Functor" \
  --from my-campaign --to shadow-realm \
  --type ForgetfulFunctor -d /absolute/path

# Transport entity (dry-run preview)
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  transport entity character sir-aldric \
  --from my-campaign --to shadow-realm \
  --functor light-to-shadow --dry-run -d /absolute/path
```

### Workflow 1: Create New Ruleset System

```bash
# 1. Initialize the system (MUST use absolute path)
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- \
  init /home/xsaw/haskell-monorepo-dnd-rules/rpg/my-fantasy-rpg \
  --id my-rpg --name "My Fantasy RPG"

# Creates:
# /home/xsaw/haskell-monorepo-dnd-rules/rpg/my-fantasy-rpg/
# ├── system.yaml
# ├── README.md
# ├── character-creation/
# ├── world-building/
# └── interactions/

# 2. Add first rule (ID auto-suggested) - use absolute path for --data-dir
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- add \
  -d /home/xsaw/haskell-monorepo-dnd-rules/rpg/my-fantasy-rpg \
  --category character-creation \
  --title "Ability Scores" \
  --tag core-mechanics

# 3. Edit the generated file to add content
# File created at: /home/xsaw/.../rpg/my-fantasy-rpg/character-creation/<rule-id>.md

# 4. Validate the rule (use absolute path)
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- validate \
  /home/xsaw/haskell-monorepo-dnd-rules/rpg/my-fantasy-rpg/character-creation/<rule-id>.md
```

### Workflow 2: Query Rules

```bash
# Search for combat rules (use absolute path)
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- query \
  -d /home/xsaw/haskell-monorepo-dnd-rules/rpg/my-fantasy-rpg combat

# Filter by category and tag
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- query \
  -d /home/xsaw/haskell-monorepo-dnd-rules/rpg/my-fantasy-rpg \
  --category character-creation \
  --tag combat \
  --limit 10

# Get JSON output for scripting
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- query \
  -d /home/xsaw/haskell-monorepo-dnd-rules/rpg/my-fantasy-rpg \
  magic --format json | jq

# GM-only rules
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- query \
  -d /home/xsaw/haskell-monorepo-dnd-rules/rpg/my-fantasy-rpg \
  secret --role gm
```

### Workflow 3: Add Rules with Specific IDs

```bash
# Add combat rule with explicit ID (use absolute path)
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- add \
  -d /home/xsaw/haskell-monorepo-dnd-rules/rpg/my-fantasy-rpg \
  --category character-creation \
  --id COMBAT-1.0 \
  --title "Melee Attacks" \
  --tag combat --tag melee \
  --visibility public

# Add GM-only secret
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- add \
  -d /home/xsaw/haskell-monorepo-dnd-rules/rpg/my-fantasy-rpg \
  --category world-building \
  --title "Campaign Secrets" \
  --visibility gm-only \
  --tag plot --tag secrets
```

## File Structure

### Directory Organization
```
my-ruleset/
├── system.yaml                 # System metadata
├── character-creation/         # Required category
│   ├── ability-scores.md
│   ├── classes.md
│   └── combat/                 # Subcategories allowed
│       └── melee-combat.md
├── world-building/             # Required category
│   ├── geography.md
│   └── magic-system.md
└── interactions/               # Required category
    └── social-rules.md
```

### Rule File Format

Every rule file uses Markdown with YAML frontmatter:

```markdown
---
category: character-creation
system: my-rpg
rules:
  - id: CHAR-001
    version: 1.0.0
    changelog:
      - version: 1.0.0
        date: 2025-11-16T10:00:00Z
        changes: "Initial version"
    tags: [core-mechanics, attributes]
    visibility: public
    title: "Ability Scores"
    # Optional fields:
    related: [CHAR-002, COMBAT-1.0]
    conditions: ["character.level >= 5"]
    formulas:
      attribute_modifier: "(score - 10) / 2"
    crossSystemRefs:
      - targetSystem: base-rpg
        targetRule: CORE-1.0
        refType: extends
---

## Character Creation

### [CHAR-001] Ability Scores

Every character has six core attributes:
- **Strength (STR)**: Physical power
- **Dexterity (DEX)**: Agility and reflexes
...
```

## Rule ID Conventions

### Format Rules
- **Pattern**: `PREFIX-X.Y` or `PREFIX-XYZ`
- **PREFIX**: Uppercase category abbreviation
- **Numbers**: Version or sequence

### Valid Examples
- ✓ `CHAR-001` - Character rule #1
- ✓ `COMBAT-1.0` - Combat rule v1.0
- ✓ `MAGIC-100` - Magic rule #100
- ✓ `STEALTH-2.5` - Stealth rule v2.5

### Invalid Examples
- ✗ `char-001` - Lowercase prefix
- ✗ `Combat_1` - Underscore separator
- ✗ `magic.100` - Dot separator without prefix

### Suggested Prefixes by Category
- `CHAR-` - character-creation
- `COMBAT-` - character-creation/combat
- `CLASS-` - character-creation/classes
- `MAGIC-` - world-building/magic
- `GEO-` - world-building/geography
- `SOCIAL-` - interactions/social
- `EXPLORE-` - interactions/exploration

## Validation

### Common Validation Errors

**Invalid Rule ID Format**
```
ERROR: Rule ID must match pattern: UPPERCASE-NUMBER
```
Fix: Use format like `CHAR-001` or `COMBAT-1.0`

**Duplicate Rule ID**
```
ERROR: Rule ID already exists in system
```
Fix: Use a different ID or let the tool auto-suggest one

**Missing Required Fields**
```
ERROR: Missing required field: tags
```
Fix: Add at least one tag to the rule

**Prefix Convention Warning**
```
WARNING: Expected prefix CHAR- for character-creation category
```
Fix: Use suggested prefix or ignore if intentional

### Validation Workflow

```bash
# Validate single file
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- validate \
  my-rpg/character-creation/abilities.md

# Strict mode (warnings = errors)
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- validate \
  my-rpg/character-creation/abilities.md --strict

# Validate all files in directory
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- validate \
  my-rpg/character-creation/abilities.md --all
```

## Best Practices

### 1. Let the Tool Suggest IDs
When adding rules, omit `--id` to get auto-suggested IDs:
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- add \
  -d my-rpg --category character-creation --title "New Rule"
# Output: Using suggested rule ID: CHAR-002
```

### 2. Use Consistent Tags
- Use lowercase-with-dashes: `core-mechanics`, `magic-system`
- Be specific: `melee-combat` not just `combat`
- Tag for searchability: `dice-rolls`, `character-advancement`

### 3. Organize with Subcategories
```
character-creation/
├── core-mechanics.md
├── classes/
│   ├── fighter.md
│   ├── wizard.md
│   └── rogue.md
└── combat/
    ├── melee.md
    └── ranged.md
```

### 4. Use Visibility Appropriately
- **public** (default): Visible to all players
- **gm-only**: Hidden from players, visible to GMs
```bash
# Query as GM to see all rules
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- query \
  -d my-rpg --role gm
```

### 5. Version Your Rules
Use semantic versioning in rule IDs for major changes:
- `COMBAT-1.0` - Original combat rules
- `COMBAT-2.0` - Major revision of combat rules

Reference old versions in changelog:
```yaml
changelog:
  - version: 2.0.0
    date: 2025-12-01T10:00:00Z
    changes: "Replaced COMBAT-1.0 with streamlined system"
```

### 6. Link Related Rules
```yaml
rules:
  - id: COMBAT-2.0
    related: [CHAR-001, MAGIC-3.0]
    # Use --show-related when querying
```

### 7. Validate Before Committing
```bash
# In git pre-commit hook:
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- validate \
  changed-file.md --strict
```

## Troubleshooting

### Issue: "Error loading system"
**Cause**: Not in a valid ruleset directory or missing system.yaml
**Solution**: Use `--data-dir` to specify the ruleset directory
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- query \
  --data-dir /path/to/my-rpg combat
```

### Issue: "Rule not found"
**Cause**: Rule ID doesn't exist or visibility mismatch
**Solution**:
1. List all rules: `list rules --system my-rpg`
2. Check with GM role: `--role gm`

### Issue: "File already exists"
**Cause**: `add` command won't overwrite existing files
**Solution**: Edit the existing file manually or use a different rule ID

### Issue: Validation fails with prefix warning
**Cause**: Rule ID prefix doesn't match category convention
**Solution**: Either:
1. Change ID to use suggested prefix
2. Accept the warning if prefix is intentional
3. Use `--strict` flag to treat as error if needed

## CRITICAL Format Requirements

### System.yaml Format

**WRONG:**
```yaml
system_id: my-rpg
name: My RPG
type: base                 # ✗ Wrong - must be "BaseSystem"
version: 1.0.0             # ✗ Wrong - must be object
```

**CORRECT:**
```yaml
system_id: my-rpg
name: My RPG
type: BaseSystem           # ✓ Correct
version:                   # ✓ Correct - object format
  vMajor: 1
  vMinor: 0
  vPatch: 0
categories:
  - character-creation
  - world-building
  - interactions
```

### Rule Frontmatter Format

**WRONG:**
```yaml
---
id: CORE-001              # ✗ Wrong - must be "rule_id"
system: my-rpg            # ✗ Wrong - must be "system_id"
category: interactions
title: "My Rule"
tags: [core]
related: []               # ✗ Wrong - must be "related_rules"
---
```

**CORRECT:**
```yaml
---
rule_id: CORE-001         # ✓ Correct
system_id: my-rpg         # ✓ Correct
category: interactions
title: "My Rule"
visibility: public
version: 1.0.0
tags: [core]
related_rules: []         # ✓ Correct
---
```

### Rule ID Format Restrictions

**Rule IDs MUST:**
- Use UPPERCASE prefix (2-6 letters)
- Use dash separator
- Use DIGITS ONLY after dash (no dots, no letters)

**Valid:**
- ✓ `CORE-001` - Simple number
- ✓ `COMBAT-100` - Three digits
- ✓ `CHAR-042` - Leading zeros OK
- ✓ `MAGIC-1` - Single digit OK

**Invalid:**
- ✗ `CORE-1.0` - Dots not allowed
- ✗ `core-001` - Lowercase not allowed
- ✗ `CORE_001` - Underscore not allowed
- ✗ `CORE-1A` - Letters after dash not allowed

### Common Init Command Bug

The `init` command may create system.yaml with incorrect format. After running `init`, you MUST fix:

```bash
# After: bazel run //...rpg-ruleset-cli -- init /path/to/system ...

# Fix system.yaml:
# 1. Change "type: base" → "type: BaseSystem"
# 2. Change "version: 1.0.0" → version object format
# 3. Delete README.md files (they conflict with rule parsing)
```

### README.md Files

**CRITICAL**: The `init` command creates README.md files, but the loader tries to parse ALL .md files as rules. This causes "MissingFrontmatter" errors.

**Solution**: Delete README.md files after init:
```bash
rm /path/to/system/README.md
rm /path/to/system/*/README.md
```

## Output Formats

### Text (default)
Human-readable output for terminal use

### JSON
For scripting and integration:
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- query \
  combat --format json | jq '.results[].rule.title'
```

### Markdown
For documentation generation:
```bash
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- query \
  --category character-creation --format markdown > rules.md
```

## When to Use This Skill

Use rpg-ruleset-cli when the user wants to:
- Create a new RPG system or ruleset
- Add rules to an existing system
- Search for specific rules by keyword, category, or tag
- Validate rule files for correct format
- List available systems, categories, or rules
- Get detailed information about a specific rule
- Organize game rules in a structured, queryable format
- Manage player vs GM visibility of rules
- Version and track changes to rules over time

## Integration with Git

The tool is designed to work with version control:
```bash
cd my-rpg
git init
git add .
git commit -m "Initial ruleset"

# After adding rules
bazel run //haskell/app/rpg-ruleset-cli:rpg-ruleset-cli -- add ...
git add character-creation/new-rule.md
git commit -m "Add new character rule"
```

## Quick Tips

1. **Start simple**: Use `init` → `add` → `validate` workflow
2. **Let tool suggest IDs**: Omit `--id` for automatic suggestions
3. **Use tags liberally**: Makes querying easier later
4. **Validate often**: Catch errors early with `validate --strict`
5. **Query with filters**: Narrow results with `--category`, `--tag`, `--system`
6. **JSON for scripts**: Use `--format json` for automation
7. **GM role for secrets**: Use `--role gm` to see hidden rules
8. **Related rules**: Use `--show-related` to see rule connections
