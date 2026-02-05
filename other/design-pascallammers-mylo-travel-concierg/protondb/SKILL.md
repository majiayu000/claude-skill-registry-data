---
name: protondb
description: Analyze ProtonDB game compatibility and provide optimized Linux gaming configurations. Use when checking if games work on Linux, optimizing launch options, or troubleshooting gaming issues on AMD GPU + Wayland + Arch Linux.
---

# ProtonDB Gaming Advisor

Specialized assistance for analyzing ProtonDB data and providing optimized gaming configurations for Linux systems, with emphasis on AMD GPU/CPU + Wayland setups.

## Overview

This skill provides procedural knowledge for Linux gaming configuration. Use this skill when asked to:

- Check game compatibility with Proton/Linux
- Get ProtonDB ratings and community reports
- Generate optimized launch options for AMD hardware
- Troubleshoot gaming issues on Wayland
- Validate system requirements against hardware
- Recommend Proton versions for specific games

## Quick Start

### Check Game Compatibility

```bash
# Using helper script (recommended)
scripts/check_game.sh <app_id_or_name>

# Manual API call
curl -s 'https://www.protondb.com/api/v1/reports/summaries/<APP_ID>.json' | jq .
```

### Get Steam Game Info

```bash
# Using helper script
scripts/get_steam_info.sh <app_id>

# Manual API call
curl -s 'https://www.protondb.com/proxy/steam/api/appdetails/?appids=<APP_ID>' | jq .
```

### Generate Launch Options

```bash
# Generate launch options from actual ProtonDB user reports
scripts/generate_launch_options.sh <app_id>

# Filter for AMD GPU users
scripts/generate_launch_options.sh <app_id> --amd-only

# Filter for AMD + Wayland users
scripts/generate_launch_options.sh <app_id> --amd-only --wayland-only
```

### Manage Proton-GE Versions

```bash
# List installed Proton-GE versions
scripts/manage_proton_ge.sh list

# Install latest Proton-GE
scripts/manage_proton_ge.sh install

# Install specific version
scripts/manage_proton_ge.sh install GE-Proton9-1

# Get recommended version for specific game
scripts/manage_proton_ge.sh get-recommended <app_id>

# Check for updates
scripts/manage_proton_ge.sh check-updates

# Remove old version (with confirmation)
scripts/manage_proton_ge.sh remove GE-Proton8-32

# List available versions on GitHub
scripts/manage_proton_ge.sh list-available
```

## Analysis Workflow

### 1. Extract Game Information

Accept game identifier in multiple formats:
- Steam App ID: `1285190`
- Game name: `"Borderlands 4"`
- ProtonDB URL: `https://www.protondb.com/app/1285190`

Fetch Steam metadata:
```bash
curl -s 'https://www.protondb.com/proxy/steam/api/appdetails/?appids=<APP_ID>'
```

Extract: title, description, system requirements, DRM, Linux support status

### 2. Fetch ProtonDB Ratings

Get compatibility summary:
```bash
curl -s 'https://www.protondb.com/api/v1/reports/summaries/<APP_ID>.json'
```

Extract: tier rating, confidence level, total reports, trending tier

**Rating tiers:**
- **Native**: Official Linux support
- **Platinum**: Works perfectly out-of-box
- **Gold**: Works with minor tweaks
- **Silver**: Runs with workarounds
- **Bronze**: Runs poorly, significant issues
- **Borked**: Does not run

### 3. Gather Community Reports

Try community API endpoints (may be unavailable):
```bash
curl -s 'https://protondb-community-api.fly.dev/reports?appId=<APP_ID>&limit=50'
```

Alternative sources:
- GitHub Proton issues: `github.com/ValveSoftware/Proton/issues`
- Reddit: `/r/linux_gaming` and `/r/SteamPlay`
- Steam Community discussions

Prioritize reports with:
- Recent dates (< 3 months)
- Similar hardware (AMD GPU/CPU)
- Similar environment (Wayland, Arch-based)
- Detailed configuration info

### 4. Generate Configuration from User Reports

Extract launch options from actual ProtonDB user reports:
```bash
# All successful reports
scripts/generate_launch_options.sh <app_id>

# Filter for AMD GPU users
scripts/generate_launch_options.sh <app_id> --amd-only

# Filter for AMD + Wayland users
scripts/generate_launch_options.sh <app_id> --amd-only --wayland-only
```

### 4.5 Install Recommended Proton-GE Version

For Silver/Bronze-rated games or games with compatibility issues:

```bash
# Get game-specific Proton-GE recommendation
scripts/manage_proton_ge.sh get-recommended <app_id>

# Install the recommended version
scripts/manage_proton_ge.sh install <version>
```

The `check_game.sh` script automatically suggests Proton-GE installation when beneficial. Proton-GE includes:
- Additional game-specific patches not in official Proton
- Video codec support for cutscenes
- Faster updates for new game releases

The script analyzes Platinum/Gold reports and shows:
- Most common environment variables
- Proton versions used successfully
- GPU models in reports
- Detailed report excerpts

Base environment variables for AMD:
```bash
AMD_VULKAN_ICD=RADV              # Force RADV driver
RADV_PERFTEST=aco                # ACO shader compiler
VKD3D_CONFIG=dxr11               # DX Raytracing support
DXVK_ASYNC=1                     # Async shader compilation
SDL_VIDEODRIVER=wayland          # Native Wayland
```

Example launch options (from user reports):
```bash
AMD_VULKAN_ICD=RADV RADV_PERFTEST=aco DXVK_ASYNC=1 SDL_VIDEODRIVER=wayland %command%
```

Optional additions:
- `gamemoderun` - CPU governor optimization
- `mangohud` - Performance overlay

### 5. Validate System Requirements

Compare game requirements against hardware:
```bash
scripts/check_requirements.sh <app_id>
```

Consider:
- Add ~10-15% overhead for Proton translation
- DirectX 12 via VKD3D-Proton may need more VRAM
- Check VRAM, CPU cores, RAM, storage type
- Some games run better on Linux due to driver scheduling

### 6. Provide Configuration Report

Generate comprehensive analysis with:
- ProtonDB status and confidence level
- System requirements validation
- Recommended Proton version
- Optimized launch options
- Known issues and workarounds
- Performance expectations
- Additional resources

## Essential Dependencies

Arch Linux packages required:
```bash
# Core gaming
sudo pacman -S steam

# Performance and monitoring
sudo pacman -S gamemode lib32-gamemode
sudo pacman -S mangohud lib32-mangohud

# AMD GPU drivers (Mesa)
sudo pacman -S mesa lib32-mesa
sudo pacman -S vulkan-radeon lib32-vulkan-radeon
sudo pacman -S vulkan-icd-loader lib32-vulkan-icd-loader

# Wayland compositor for games
sudo pacman -S gamescope

# Enable gamemode
systemctl --user enable --now gamemoded.service
```

## Best Practices

1. **Prioritize data sources**: Official ProtonDB API → GitHub issues → Community APIs → Forums
2. **Match hardware**: Look for AMD GPU/CPU reports with similar specs
3. **Check recency**: Prefer reports from last 3 months
4. **Note confidence levels**: Strong confidence = reliable, weak = experimental
5. **Test incrementally**: Start with default config, add optimizations gradually
6. **Watch for anti-cheat**: Denuvo, EAC, BattleEye can cause issues
7. **Consider Proton version**: Experimental for new games, stable for established titles

## Common Issues

**Anti-cheat problems:**
- Check ProtonDB for EAC/BattleEye status
- Some games whitelisted, others blocked
- Denuvo may cause activation limits

**Wayland-specific:**
- Window focus issues: Use `gamescope` wrapper
- Resolution switching: Use gamescope with `-W -H -r` flags
- Input capture: May need XWayland fallback

**Performance issues:**
- Shader stutter: Enable `DXVK_ASYNC=1`
- CPU bottleneck: Ensure gamemode is active
- Memory issues: Try `VKD3D_CONFIG=upload_hvv`

## Reference Material

For detailed information, refer to:

- `references/api_endpoints.md` - Complete API documentation
- `references/amd_optimization.md` - AMD GPU + Wayland optimization guide
- `references/environment_variables.md` - Complete env var reference
- `references/proton_versions.md` - Version selection guide
- `references/known_issues.md` - Common problems and solutions

## Resources

### scripts/

- `check_game.sh` - Fetch ProtonDB rating and game info
- `get_steam_info.sh` - Get Steam metadata for game
- `generate_launch_options.sh` - Extract launch options from user reports
- `check_requirements.sh` - Validate system requirements

### references/

- `api_endpoints.md` - ProtonDB and Steam API documentation
- `amd_optimization.md` - AMD GPU + Wayland configuration guide
- `environment_variables.md` - Environment variable reference
- `proton_versions.md` - Proton version selection guide
- `known_issues.md` - Common issues and workarounds

### assets/

- `gamemode.ini` - GameMode configuration template
