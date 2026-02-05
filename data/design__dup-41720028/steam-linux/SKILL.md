---
name: steam-linux
description: This skill should be used when working with Steam on Linux - managing non-Steam game shortcuts, configuring Proton/Wine compatibility, parsing VDF files, or finding Steam paths and prefixes.
---

# Steam Linux Management

Use this skill when modifying Steam shortcuts, configuring Proton, or working with Steam's configuration files on Linux.

## Steam Paths

```
STEAM_ROOT = ~/.local/share/Steam
├── config/
│   ├── config.vdf          # Text VDF - Proton mappings, settings
│   └── libraryfolders.vdf  # Text VDF - Steam library locations
├── steamapps/
│   ├── common/             # Installed games and Proton versions
│   ├── compatdata/         # Proton prefixes (Wine bottles)
│   └── libraryfolders.vdf  # Library paths
└── userdata/{USER_ID}/
    └── config/
        └── shortcuts.vdf   # Binary VDF - Non-Steam game shortcuts
```

### Finding Steam User ID

```python
from pathlib import Path
STEAM_ROOT = Path.home() / ".local/share/Steam"
userdata = STEAM_ROOT / "userdata"
user_id = next((d.name for d in userdata.iterdir() if d.is_dir() and d.name.isdigit()), None)
```

### Finding Steam Library Folders

Parse `libraryfolders.vdf` (text VDF):
```python
libs = [STEAM_ROOT]
with open(STEAM_ROOT / "steamapps/libraryfolders.vdf") as f:
    for line in f:
        if '"path"' in line:
            path = line.split('"')[3]
            libs.append(Path(path))
```

## Binary VDF Format (shortcuts.vdf)

Non-Steam shortcuts use binary VDF format.

### Type Bytes
- `0x00` - Nested object start
- `0x01` - String value
- `0x02` - Int32 value (little-endian)
- `0x08` - Object end

### Structure
```
0x00 "shortcuts" 0x00
  0x00 "0" 0x00           # First shortcut (index)
    0x02 "appid" 0x00 [4 bytes LE int]
    0x01 "AppName" 0x00 "Game Name" 0x00
    0x01 "Exe" 0x00 "\"path/to/exe\"" 0x00
    0x01 "StartDir" 0x00 "\"path/to/dir\"" 0x00
    0x01 "LaunchOptions" 0x00 "options" 0x00
    ...
  0x08                     # End of shortcut
0x08 0x08                  # End of shortcuts, end of root
```

### Parsing Example

See `references/vdf-parser.py` for complete implementation.

### Shortcut App ID Generation

Steam generates app IDs for non-Steam games using CRC32:
```python
import zlib
def generate_app_id(exe_path, app_name):
    key = f'"{exe_path}"{app_name}'
    crc = zlib.crc32(key.encode('utf-8')) & 0xFFFFFFFF
    return crc | 0x80000000
```

### Shortcut Fields

Required fields for a shortcut entry:
```python
{
    'appid': int,           # Generated app ID
    'AppName': str,         # Display name
    'Exe': str,             # Path in quotes: '"path/to/exe"'
    'StartDir': str,        # Working dir in quotes
    'icon': str,            # Icon path (optional)
    'ShortcutPath': str,    # Usually empty
    'LaunchOptions': str,   # Command line args
    'IsHidden': int,        # 0 or 1
    'AllowDesktopConfig': int,
    'AllowOverlay': int,
    'OpenVR': int,
    'Devkit': int,
    'DevkitGameID': str,
    'DevkitOverrideAppID': int,
    'LastPlayTime': int,    # Unix timestamp
    'FlatpakAppID': str,
    'tags': {}              # Nested object for categories
}
```

## Text VDF Format (config.vdf)

Steam's main config uses text VDF format - key-value pairs with tabs.

### Proton Compatibility Tool Mapping

Located in `config.vdf` under `CompatToolMapping`:
```
"CompatToolMapping"
{
    "APP_ID"
    {
        "name"      "proton_experimental"
        "config"    ""
        "priority"  "250"
    }
}
```

### Adding Proton Mapping

```python
def add_compat_tool_mapping(app_id, tool="proton_experimental"):
    config_path = STEAM_ROOT / "config/config.vdf"
    with open(config_path, 'r') as f:
        content = f.read()

    # Check if already exists in CompatToolMapping section
    compat_start = content.find('"CompatToolMapping"')
    if compat_start != -1:
        compat_section = content[compat_start:compat_start+5000]
        if f'"{app_id}"' in compat_section:
            return  # Already configured

    # Find insertion point after CompatToolMapping {
    pos = content.find('"CompatToolMapping"')
    brace_pos = content.find('{', pos)

    # Build entry (use chr(9) for tabs to avoid template issues)
    TAB = chr(9)
    NL = chr(10)
    entry = NL + TAB*5 + f'"{app_id}"' + NL
    entry += TAB*5 + '{' + NL
    entry += TAB*6 + '"name"' + TAB*2 + f'"{tool}"' + NL
    entry += TAB*6 + '"config"' + TAB*2 + '""' + NL
    entry += TAB*6 + '"priority"' + TAB*2 + '"250"' + NL
    entry += TAB*5 + '}'

    new_content = content[:brace_pos+1] + entry + content[brace_pos+1:]
    with open(config_path, 'w') as f:
        f.write(new_content)
```

## Proton/Compatdata

Each game/shortcut has a Wine prefix in compatdata:

```
~/.local/share/Steam/steamapps/compatdata/{APP_ID}/
├── pfx/                    # Wine prefix root
│   └── drive_c/           # C: drive
│       ├── Program Files/
│       ├── Program Files (x86)/
│       └── users/steamuser/
├── version                 # Proton version used
└── config_info            # Configuration metadata
```

### Finding a Game's Prefix

```python
def find_game_prefix(game_name_pattern):
    """Find compatdata prefix containing a specific game/app."""
    for lib in get_steam_libraries():
        compatdata = lib / "steamapps/compatdata"
        if not compatdata.exists():
            continue
        for prefix in compatdata.iterdir():
            # Check for the game in common Windows install locations
            for check_path in [
                prefix / "pfx/drive_c/Program Files" / game_name_pattern,
                prefix / "pfx/drive_c/Program Files (x86)" / game_name_pattern,
            ]:
                if check_path.exists():
                    return prefix
    return None
```

### Sharing Prefixes Between Shortcuts

To make a shortcut use an existing prefix (e.g., for Battle.net games):
```
LaunchOptions: STEAM_COMPAT_DATA_PATH="/path/to/compatdata/APP_ID" %command% [args]
```

## Proton Versions

Common Proton tool IDs:
- `proton_experimental` - Proton Experimental
- `proton_10` - Proton 10.0
- `proton_9` - Proton 9.0

Proton locations:
```
{LIBRARY}/steamapps/common/Proton - Experimental/proton
{LIBRARY}/steamapps/common/Proton 10.0/proton
```

## Launching Games

### Via Steam Protocol
```bash
steam steam://rungameid/{APP_ID}
xdg-open steam://rungameid/{APP_ID}
```

### Via Command Line
```bash
steam -applaunch {APP_ID}
```

**Note**: These require Steam to be running and may not work reliably for non-Steam shortcuts.

## Important Notes

1. **Close Steam before modifying config files** - Steam may overwrite changes
2. **Restart Steam after changes** - New shortcuts won't appear until restart
3. **App IDs for shortcuts** - Must use the CRC32-based generation algorithm
4. **Quote paths in Exe/StartDir** - Always wrap paths in double quotes
5. **Template escaping** - When using in chezmoi templates, avoid `\n`, `\t`, use `chr()` instead
