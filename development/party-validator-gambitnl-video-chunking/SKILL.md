---
name: party-validator
description: Validate and manage D&D party configuration files including player names, character mappings, and DM information. Use when creating new party configs, troubleshooting speaker mapping issues, or verifying configuration before session processing.
---

# Party Validator Skill

Validate, create, and manage D&D party configuration files for accurate speaker mapping.

## What This Skill Does

This skill helps manage party configurations to ensure accurate speaker-to-character mapping during session processing:

1. **Validate Configurations**: Check party config files for correct structure and data
2. **Create New Configs**: Generate party configuration files from templates
3. **Update Configs**: Modify existing configurations with new players or characters
4. **Compare Configs**: Diff multiple party configurations
5. **Speaker Mapping**: Preview how speakers will be mapped to characters
6. **Troubleshoot Issues**: Diagnose and fix common configuration problems

## Why Party Configs Matter

Party configurations enable:
- **Accurate Speaker Mapping**: Map SPEAKER_00, SPEAKER_01, etc. to actual players
- **Character Attribution**: Link dialogue to D&D characters for IC content
- **Knowledge Extraction**: Properly attribute actions and dialogue to characters
- **Consistent Naming**: Maintain consistent player/character names across sessions

## Configuration File Structure

### Location
Party configs are stored in: `data/party_<name>.json`

### Schema
```json
{
  "party_name": "Main Campaign Party",
  "campaign": "Dragon Heist",
  "dm": {
    "name": "Alice",
    "voice_characteristics": "Female, low pitch, authoritative"
  },
  "players": [
    {
      "name": "Bob",
      "voice_characteristics": "Male, mid pitch, energetic",
      "characters": [
        {
          "name": "Thorin Ironfist",
          "class": "Fighter",
          "race": "Dwarf"
        }
      ]
    },
    {
      "name": "Charlie",
      "voice_characteristics": "Male, high pitch, dramatic",
      "characters": [
        {
          "name": "Elara Moonwhisper",
          "class": "Wizard",
          "race": "Elf"
        }
      ]
    }
  ]
}
```

### Required Fields

**Root Level:**
- `party_name` (string): Descriptive name for the party
- `dm` (object): Dungeon Master information
- `players` (array): List of player objects

**DM Object:**
- `name` (string): DM's real name

**Player Object:**
- `name` (string): Player's real name
- `characters` (array): List of character objects (can be empty for new players)

**Character Object:**
- `name` (string): Character's name in the game
- `class` (string): D&D class (optional but recommended)
- `race` (string): D&D race (optional but recommended)

### Optional Fields

- `campaign` (string): Campaign name or setting
- `voice_characteristics` (string): Voice description to aid speaker mapping
- `session_range` (array): e.g., [1, 50] - sessions this config applies to
- `notes` (string): Additional information about the party
- `created_date` (string): When configuration was created
- `last_updated` (string): Last modification date

## Usage

### Validate Existing Config
User: "Validate the default party configuration"
User: "Check if party_main.json is correct"
User: "Is the party config valid?"

### Validate All Configs
User: "Validate all party configurations"
User: "Check all party config files"

### Create New Config
User: "Create a new party config called 'oneshot' with 3 players"
User: "Set up a party configuration for my new campaign"

### Update Existing Config
User: "Add a new player named David to the main party config"
User: "Update Bob's character to level 5 Paladin"

### Troubleshoot Issues
User: "Why is speaker mapping wrong for session 12?"
User: "The DM is being identified as a player. Help me fix the config."

## Command Reference

```bash
# Validate specific config
python cli.py validate-config --party default

# Validate all configs
python cli.py validate-config --all

# Create new config
python cli.py create-party-config --name oneshot --players Alice Bob Charlie

# Update config
python cli.py update-party-config --name default --add-player David

# Show config
python cli.py show-party-config --name default

# List all configs
python cli.py list-party-configs
```

## MCP Tool Integration

Use `mcp__videochunking-dev__validate_party_config` to validate configurations.

### Validate Specific Config
```python
# Via MCP tool
validate_party_config(config_name="default")
```

Returns:
```json
{
  "file": "party_default.json",
  "valid": true,
  "player_count": 4,
  "character_count": 4,
  "errors": [],
  "warnings": []
}
```

### Validate All Configs
```python
# Via MCP tool
validate_party_config()  # No config_name = validate all
```

Returns:
```json
{
  "configs": [
    {
      "file": "party_default.json",
      "valid": true,
      "player_count": 4,
      "character_count": 4,
      "errors": [],
      "warnings": []
    },
    {
      "file": "party_oneshot.json",
      "valid": false,
      "errors": ["Missing 'dm' field"],
      "warnings": ["Player 0 has no characters"]
    }
  ],
  "total_validated": 2
}
```

## Validation Rules

### Critical Errors (Must Fix)
- ❌ Missing `party_name` field
- ❌ Missing `dm` object
- ❌ Missing `players` array
- ❌ Invalid JSON syntax
- ❌ DM missing `name` field
- ❌ Player missing `name` field
- ❌ Characters array is not a list
- ❌ Duplicate player names
- ❌ Character missing `name` field

### Warnings (Should Review)
- ⚠️ Player has no characters (might be observer or new)
- ⚠️ Character missing `class` or `race` (less detailed extraction)
- ⚠️ No `voice_characteristics` (harder to map speakers)
- ⚠️ Very few players (<2) or many players (>8)
- ⚠️ No `campaign` specified
- ⚠️ Empty or very short character names

### Recommendations
- ℹ️ Add voice_characteristics for better speaker mapping
- ℹ️ Include character class and race for richer knowledge extraction
- ℹ️ Specify campaign name for organization
- ℹ️ Add notes about campaign setting or party dynamics

## Common Issues and Solutions

### Issue: Missing Required Field
```
Error: Missing 'dm' field in party_custom.json

Solution:
Add DM information:
{
  "dm": {
    "name": "Your DM Name"
  }
}
```

### Issue: Invalid JSON Syntax
```
Error: Invalid JSON in party_default.json - Unexpected token at line 15

Solution:
- Check for missing commas between fields
- Ensure all quotes are matched
- Verify no trailing commas
- Use JSON validator: jsonlint.com
```

### Issue: Duplicate Player Names
```
Error: Duplicate player name 'Bob' found in party_main.json

Solution:
- Use unique player names
- If same person plays different characters across sessions,
  use disambiguating names: "Bob_Character1", "Bob_Character2"
- Or create separate configs per session range
```

### Issue: Player Has No Characters
```
Warning: Player 'Charlie' has no characters defined

Solutions:
1. Add character to players array:
   "characters": [{"name": "CharName", "class": "Rogue", "race": "Human"}]
2. If player is observer/DM assistant, this is okay (can ignore warning)
3. If new campaign, add character after character creation session
```

### Issue: Wrong Speaker Mapping
```
Problem: SPEAKER_00 is mapped to wrong player in output

Solutions:
1. Check if voice_characteristics are accurate and distinct
2. Verify player order matches typical speaking order
3. Review diarization settings (may need adjustment)
4. Consider manual speaker label correction post-processing
5. Ensure no players are missing from config
```

### Issue: Character Name Mismatched
```
Problem: Character name in transcript doesn't match config

Solutions:
1. Update config with actual name used in game
2. Add name variations/aliases to character object
3. Use consistent character names during play
4. Manually correct extracted knowledge if needed
```

## Creating New Party Configs

### Template-Based Creation

Use provided template:
```bash
cp data/party_template.json data/party_newcampaign.json
# Edit party_newcampaign.json with actual information
python cli.py validate-config --party newcampaign
```

### Interactive Creation

Follow prompts:
```bash
python cli.py create-party-config --interactive

Party name: Summer Oneshot
Campaign name (optional): Lost Mine of Phandelver
DM name: Alice

How many players? 4

Player 1 name: Bob
Player 1 voice: Male, deep voice
Player 1 character name: Thorin
Player 1 character class: Fighter
Player 1 character race: Dwarf

... (repeat for all players)

Config saved to: data/party_summer_oneshot.json
Validation: ✅ VALID
```

### Programmatic Creation

```python
from src.party_config import PartyConfig

config = PartyConfig.create(
    party_name="Test Party",
    campaign="Test Campaign",
    dm_name="Alice",
    players=[
        {
            "name": "Bob",
            "voice": "Male, mid pitch",
            "characters": [
                {"name": "Thorin", "class": "Fighter", "race": "Dwarf"}
            ]
        },
        {
            "name": "Charlie",
            "characters": [
                {"name": "Elara", "class": "Wizard", "race": "Elf"}
            ]
        }
    ]
)

config.save("data/party_test.json")
config.validate()  # Returns errors and warnings
```

## Speaker Mapping Preview

Before processing, preview how speakers will be mapped:

```bash
python cli.py preview-speaker-mapping --party default --session session_012

Expected Mapping (based on typical speaking order):
  SPEAKER_00 → Alice (DM)
  SPEAKER_01 → Bob (Thorin Ironfist)
  SPEAKER_02 → Charlie (Elara Moonwhisper)
  SPEAKER_03 → David (Grim Stonefist)
  SPEAKER_04 → Eve (Lyra Brightwood)

Notes:
  - Mapping is based on voice_characteristics and typical patterns
  - Actual mapping may vary based on who speaks first
  - Review output after processing for accuracy
  - Adjust voice_characteristics if mapping is incorrect
```

## Configuration Management

### Version Control

Commit party configs to git:
```bash
git add data/party_*.json
git commit -m "Add main campaign party config"
git push
```

### Backup Configs

Before making changes:
```bash
cp data/party_default.json data/party_default.json.backup
```

### Multiple Configs for Same Campaign

Use session ranges or naming:
```
party_main_sessions_1-10.json   # Original party
party_main_sessions_11-20.json  # New player joined
party_main_sessions_21-30.json  # Player left, character replaced
```

Or simply:
```
party_main_early.json
party_main_current.json
```

Specify during processing:
```bash
python cli.py process video.mp4 --party main_current
```

## Advanced Validation

### Schema Validation

Use JSON Schema for strict validation:
```bash
python cli.py validate-config --party default --strict

# Uses schema file: schemas/party_config_schema.json
```

### Cross-Session Validation

Ensure config matches actual session data:
```bash
python cli.py validate-config --party default --check-session session_012

Validation Results:
  ✅ All speakers in session_012 mapped to config players
  ⚠️ SPEAKER_04 in session but only 4 players in config (expected 5 speakers)

Recommendation:
  Check if new player joined for session_012
  Update config or verify diarization didn't over-segment
```

### Historical Validation

Check if configs match historical usage:
```bash
python cli.py validate-config --history

Party Config Usage:
  party_default.json:
    Used in: 25 sessions (session_001 to session_025)
    Speaker counts: 5 (consistent)
    Issues: None

  party_oneshot.json:
    Used in: 3 sessions (session_026, session_027, session_028)
    Speaker counts: 4, 4, 5 (inconsistent)
    Issues: Session_028 had extra speaker not in config

Recommendations:
  ⚠️ Review session_028 - possible new player or guest
  ℹ️ Consider creating party_oneshot_v2.json for future sessions
```

## Integration with Other Skills

- **session-processor**: Use validated configs for session processing
- **diagnostics-runner**: Includes party config validation in health checks
- **campaign-analyzer**: Use character names from configs for knowledge extraction
- **video-chunk**: Validates party config before starting pipeline

## Best Practices

1. **Create Config Before First Session**: Set up party config before processing
2. **Include Voice Characteristics**: Helps with speaker diarization accuracy
3. **Keep Configs Updated**: Add new players/characters as they join
4. **Version Configs**: Track changes in git for history
5. **Validate After Changes**: Always validate after editing configs
6. **Use Descriptive Names**: Name configs clearly (party_main, party_oneshot_winter)
7. **Document Special Cases**: Add notes for temporary players or guests
8. **Backup Before Major Changes**: Save backups before restructuring
9. **Test with Sample Session**: Process one session to verify mapping
10. **Review First Output**: Manually check speaker mapping is correct

## Example Workflows

### New Campaign Setup
```
User: "I'm starting a new campaign. Help me set up the party config."

Assistant uses party-validator:
1. Asks for party details (DM, players, characters)
2. Creates new config file: data/party_newcampaign.json
3. Validates structure
4. Previews speaker mapping
5. Confirms ready for session processing
```

### Troubleshooting Bad Mapping
```
User: "Session 12 has wrong speaker assignments. The DM is labeled as a player."

Assistant uses party-validator:
1. Validates party config: check config is correct
2. Reviews session 12 output: check actual speaker assignments
3. Compares expected vs actual mapping
4. Identifies issue: Speaker order different than expected
5. Suggests: Update voice_characteristics or manually correct session
```

### Config Migration
```
User: "We had a player change characters. Update the config."

Assistant uses party-validator:
1. Reads current config
2. Updates player's character information
3. Validates updated config
4. Creates backup of old config
5. Recommends: Specify session range for old vs new character
```

## Future Enhancements

Potential features:
- Automatic speaker-to-player mapping based on voice analysis
- Config templates for common party sizes
- Visual config editor (web UI)
- Character progression tracking (levels, abilities)
- Session attendance tracking
- Voice sample collection for better diarization
- Integration with D&D Beyond for character import
- Multi-language support for international campaigns
