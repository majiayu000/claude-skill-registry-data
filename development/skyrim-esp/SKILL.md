---
name: skyrim-esp
description: Create and modify Skyrim plugin files (.esp/.esl). Use when the user wants to create a mod, add weapons, armor, spells, perks, books, quests, NPCs, or globals to a plugin. Also use when inspecting existing plugins or merging mods.
---

# Skyrim ESP Module

Create, inspect, and modify Skyrim plugin files using the ESP module of Spooky's AutoMod Toolkit.

## Prerequisites

Run all commands from the toolkit directory:
```bash
cd "<TOOLKIT_PATH>"
# Example: cd "C:\Tools\spookys-automod-toolkit"
```

## Command Reference

### Create a Plugin
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp create "<name>.esp" [options]
```
| Option | Description |
|--------|-------------|
| `--light` | Create as ESL-flagged light plugin |
| `--author "Name"` | Set author in header |
| `--output "./path"` | Output directory |

### Inspect a Plugin
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp info "<plugin>"
dotnet run --project src/SpookysAutomod.Cli -- esp list-masters "<plugin>"
```

### Add Records

**Books** (work immediately, no model needed):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-book "<plugin>" "<editorId>" --name "Name" --text "Content..." --value 50
```

**Weapons** (require `--model` to be visible):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-weapon "<plugin>" "<editorId>" --name "Name" --type sword --damage 25 --model iron-sword
```
Model presets: `iron-sword`, `steel-sword`, `iron-dagger`, `hunting-bow`

**Armor** (require `--model` to be visible):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-armor "<plugin>" "<editorId>" --name "Name" --type heavy --slot body --rating 40 --model iron-cuirass
```
Model presets: `iron-cuirass`, `iron-helmet`, `iron-gauntlets`, `iron-boots`, `iron-shield`

**Spells** (require `--effect` to function):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-spell "<plugin>" "<editorId>" --name "Name" --effect damage-health --magnitude 50 --cost 45
```
Effect presets: `damage-health`, `restore-health`, `damage-magicka`, `restore-magicka`, `damage-stamina`, `restore-stamina`, `fortify-health`, `fortify-magicka`, `fortify-stamina`, `fortify-armor`, `fortify-attack`

**Perks** (require `--effect` to function):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-perk "<plugin>" "<editorId>" --name "Name" --description "Effect" --effect weapon-damage --bonus 25 --playable
```
Effect presets: `weapon-damage`, `damage-reduction`, `armor`, `spell-cost`, `spell-power`, `spell-duration`, `sneak-attack`, `pickpocket`, `prices`

**Quests**:
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-quest "<plugin>" "<editorId>" --name "Name" --start-enabled
```

**Globals** (configuration variables):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-global "<plugin>" "<editorId>" --type float --value 1.5
```

**NPCs** (record only - need race/face data for visibility):
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp add-npc "<plugin>" "<editorId>" --name "Name" --level 20 --essential
```

### Script Attachment
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp attach-script "<plugin>" --quest "<questId>" --script "<scriptName>"
```

### SEQ File Generation
Required for start-enabled quests:
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp generate-seq "<plugin>" --output "./SEQ"
```

### Merge Plugins
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp merge "<source>.esp" "<target>.esp" --output "Merged.esp"
```

## Common Workflows

### Create a Complete Weapon Mod
```bash
# 1. Create plugin
dotnet run --project src/SpookysAutomod.Cli -- esp create "MyWeaponMod.esp" --light --author "YourName"

# 2. Add weapon with model
dotnet run --project src/SpookysAutomod.Cli -- esp add-weapon "MyWeaponMod.esp" "MyWeapon_Sword" --name "Blade of Power" --type sword --damage 35 --value 500 --model iron-sword

# 3. Verify
dotnet run --project src/SpookysAutomod.Cli -- esp info "MyWeaponMod.esp"
```

### Create a Spell Pack
```bash
# Create plugin
dotnet run --project src/SpookysAutomod.Cli -- esp create "SpellPack.esp" --light

# Add damage spell
dotnet run --project src/SpookysAutomod.Cli -- esp add-spell "SpellPack.esp" "SP_Fireball" --name "Greater Fireball" --effect damage-health --magnitude 75 --cost 60

# Add healing spell
dotnet run --project src/SpookysAutomod.Cli -- esp add-spell "SpellPack.esp" "SP_Heal" --name "Major Healing" --effect restore-health --magnitude 100 --cost 50

# Add buff spell
dotnet run --project src/SpookysAutomod.Cli -- esp add-spell "SpellPack.esp" "SP_Fortify" --name "Warrior's Blessing" --effect fortify-health --magnitude 50 --duration 120 --cost 80
```

### Create a Perk Overhaul
```bash
# Create plugin
dotnet run --project src/SpookysAutomod.Cli -- esp create "PerkMod.esp" --light

# Combat perks
dotnet run --project src/SpookysAutomod.Cli -- esp add-perk "PerkMod.esp" "PM_WeaponMaster" --name "Weapon Master" --description "+20% weapon damage" --effect weapon-damage --bonus 20 --playable

# Magic perks
dotnet run --project src/SpookysAutomod.Cli -- esp add-perk "PerkMod.esp" "PM_Efficiency" --name "Magical Efficiency" --description "Spells cost 25% less" --effect spell-cost --bonus 25 --playable

# Stealth perks
dotnet run --project src/SpookysAutomod.Cli -- esp add-perk "PerkMod.esp" "PM_Assassin" --name "Assassin's Strike" --description "3x sneak attack damage" --effect sneak-attack --bonus 200 --playable
```

### Add Content to Existing Mod
```bash
# Check what's in the mod
dotnet run --project src/SpookysAutomod.Cli -- esp info "ExistingMod.esp"

# Add new content
dotnet run --project src/SpookysAutomod.Cli -- esp add-weapon "ExistingMod.esp" "NewWeapon" --name "Added Sword" --damage 30 --model steel-sword

# Verify addition
dotnet run --project src/SpookysAutomod.Cli -- esp info "ExistingMod.esp"
```

## Important Notes

1. **Always use `--model`** for weapons and armor - without it they'll be invisible
2. **Always use `--effect`** for spells and perks - without it they won't function
3. **EditorIDs must be unique** - use a prefix like `MyMod_` to avoid conflicts
4. **Light plugins (.esl)** have a 2048 record limit but don't use a load order slot
5. **Start-enabled quests require SEQ files** - generate with `generate-seq` command
6. **Use `--json` flag** for machine-readable output when scripting

## JSON Output

All commands support `--json` for structured output:
```bash
dotnet run --project src/SpookysAutomod.Cli -- esp info "MyMod.esp" --json
```
