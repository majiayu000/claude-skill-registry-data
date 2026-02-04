---
name: skyrim-archive
description: Read, extract, and create BSA/BA2 archives. Use when the user wants to package mod assets, extract files from existing mods, or inspect archive contents.
---

# Skyrim Archive Module

Read, extract, and create BSA/BA2 archives using Spooky's AutoMod Toolkit.

## Prerequisites

Run all commands from the toolkit directory:
```bash
cd "<TOOLKIT_PATH>"
# Example: cd "C:\Tools\spookys-automod-toolkit"
```

## External Tools

| Tool | Purpose | Auto-Download |
|------|---------|---------------|
| BSArch | Create/extract archives | No - manual install |

### Installing BSArch
1. Download xEdit from [GitHub releases](https://github.com/TES5Edit/TES5Edit/releases)
2. Extract the archive
3. Copy `BSArch.exe` to `tools/bsarch/` in the toolkit directory

Check tool status:
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive status
```

## Command Reference

### Check Tool Status
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive status
```

### Get Archive Info
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive info "<archive>"
```
Output includes: Archive type, version, file count, total size.

### List Archive Contents
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive list "<archive>" [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--filter`, `-f` | - | Filter pattern (e.g., `*.nif`, `textures/*`) |
| `--limit` | 100 | Max files to list (0 = all) |

### Extract Archive
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive extract "<archive>" --output "<dir>" [options]
```
| Option | Description |
|--------|-------------|
| `--output`, `-o` | Output directory |
| `--filter`, `-f` | Filter pattern for files to extract |

**Requires:** BSArch tool installed

### Create Archive
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive create "<directory>" --output "<file>" [options]
```
| Option | Default | Description |
|--------|---------|-------------|
| `--output`, `-o` | Required | Output archive path |
| `--compress` | true | Compress archive contents |
| `--game` | `sse` | Game type: `sse`, `le`, `fo4`, `fo76` |

**Requires:** BSArch tool installed

## Common Workflows

### Inspect Existing Mod Archive
```bash
# Get archive info
dotnet run --project src/SpookysAutomod.Cli -- archive info "SomeMod.bsa"

# List first 100 files
dotnet run --project src/SpookysAutomod.Cli -- archive list "SomeMod.bsa"

# List all NIF meshes
dotnet run --project src/SpookysAutomod.Cli -- archive list "SomeMod.bsa" --filter "*.nif"

# List all textures
dotnet run --project src/SpookysAutomod.Cli -- archive list "SomeMod.bsa" --filter "textures/*"

# List all scripts
dotnet run --project src/SpookysAutomod.Cli -- archive list "SomeMod.bsa" --filter "*.pex"
```

### Extract Mod for Analysis/Editing
```bash
# Extract entire archive
dotnet run --project src/SpookysAutomod.Cli -- archive extract "SomeMod.bsa" --output "./Extracted"

# Extract only textures
dotnet run --project src/SpookysAutomod.Cli -- archive extract "SomeMod.bsa" --output "./Extracted" --filter "textures/*"

# Extract only meshes
dotnet run --project src/SpookysAutomod.Cli -- archive extract "SomeMod.bsa" --output "./Extracted" --filter "*.nif"

# Extract only scripts for decompilation
dotnet run --project src/SpookysAutomod.Cli -- archive extract "SomeMod.bsa" --output "./Extracted" --filter "scripts/*"
```

### Package Mod as BSA
```bash
# 1. Organize files in Data structure
# MyModData/
#   meshes/mymod/weapon.nif
#   textures/mymod/weapon.dds
#   scripts/MyMod_Script.pex

# 2. Create compressed SSE archive
dotnet run --project src/SpookysAutomod.Cli -- archive create "./MyModData" --output "MyMod.bsa"

# 3. Create uncompressed archive (faster loading)
dotnet run --project src/SpookysAutomod.Cli -- archive create "./MyModData" --output "MyMod.bsa" --compress false

# 4. Create LE-compatible archive
dotnet run --project src/SpookysAutomod.Cli -- archive create "./MyModData" --output "MyMod.bsa" --game le
```

### Troubleshooting Workflow
```bash
# 1. Check what's in a broken mod's BSA
dotnet run --project src/SpookysAutomod.Cli -- archive list "BrokenMod.bsa" --limit 0

# 2. Extract everything for analysis
dotnet run --project src/SpookysAutomod.Cli -- archive extract "BrokenMod.bsa" --output "./Debug"

# 3. Check mesh textures
dotnet run --project src/SpookysAutomod.Cli -- nif textures "./Debug/meshes/SomeMesh.nif"

# 4. Decompile scripts
dotnet run --project src/SpookysAutomod.Cli -- papyrus decompile "./Debug/scripts" --output "./Debug/Source"
```

## Directory Structure for Packaging

The source directory should mirror Skyrim's Data folder:
```
MyModData/
  meshes/
    mymod/
      weapon.nif
      armor.nif
  textures/
    mymod/
      weapon.dds
      weapon_n.dds
      armor.dds
  scripts/
    MyMod_MainScript.pex
    MyMod_EffectScript.pex
  sound/
    fx/
      mymod/
        sound.wav
```

## Archive Types

### BSA (Bethesda Softworks Archive)
- Used by: Skyrim LE, Skyrim SE
- Magic: `BSA\0`
- Supports compression
- Best for general mod assets

### BA2 (Bethesda Archive 2)
- Used by: Fallout 4, Fallout 76
- Magic: `BTDX`
- Two storage types: General, Textures
- Better compression for textures

### Game Type Selection

| Game | Flag | Notes |
|------|------|-------|
| `sse` | Skyrim SE/AE | Default, most common |
| `le` | Skyrim LE | Older format |
| `fo4` | Fallout 4 | BA2 format |
| `fo76` | Fallout 76 | BA2 format |

## Common Issues

### BSArch Not Found
```bash
# Check status
dotnet run --project src/SpookysAutomod.Cli -- archive status

# Follow installation instructions if missing
```

### Wrong Archive Format
- SSE mods need SSE archives (`--game sse`)
- LE mods need LE archives (`--game le`)
- Using wrong format causes purple textures or crashes

### Missing Files After Packaging
- Ensure correct directory structure
- Files must be in proper subfolders (meshes/, textures/, etc.)
- Case sensitivity may matter

## Important Notes

1. **BSArch required** for create/extract - info/list work without it
2. **Match archive to game** - SSE and LE use different formats
3. **Directory structure matters** - Must mirror Data folder
4. **Compression trade-off** - Smaller files but slower loading
5. **Use `--json` flag** for machine-readable output when scripting

## JSON Output

All commands support `--json` for structured output:
```bash
dotnet run --project src/SpookysAutomod.Cli -- archive info "MyMod.bsa" --json
```

Example response:
```json
{
  "success": true,
  "result": {
    "fileName": "MyMod.bsa",
    "type": "BSA",
    "version": "105",
    "fileCount": 150,
    "fileSize": 52428800
  }
}
```
