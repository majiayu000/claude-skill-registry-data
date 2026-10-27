---
name: kmi-cli
description: >
  Query Belgian weather via KMI/IRM meteo.be API. Use when user wants
  forecasts, current weather, radar, warnings, or UV index for Belgian locations.
  Triggered by mentions of Belgian weather, KMI, IRM, meteo.be, or Belgian forecast.
license: MIT
homepage: https://github.com/dedene/kmi-irm-cli
metadata:
  author: dedene
  version: "1.0.0"
  openclaw:
    requires:
      bins:
        - kmi
    install:
      - kind: brew
        tap: dedene/tap
        formula: kmi
        bins: [kmi]
      - kind: go
        package: github.com/dedene/kmi-irm-cli/cmd/kmi
        bins: [kmi]
      - kind: binary
        url: https://github.com/dedene/kmi-irm-cli/releases/latest
        bins: [kmi]
---

# kmi-cli

CLI for [KMI/IRM](https://www.meteo.be/) - Belgian weather data from the Royal Meteorological Institute.

## Quick Start

```bash
# Current weather
kmi current Brussels

# 7-day forecast
kmi forecast Leuven

# Weather warnings
kmi warnings Belgium

# UV index
kmi uv Antwerp
```

## No Authentication Required

This CLI uses the public meteo.be API. No API key or registration needed.

## Core Rules

1. **Always use `--json`** when parsing output programmatically
2. **Location formats**: city name (`Brussels`), coordinates (`50.85,4.35`), or favorite (`@home`)
3. **Use favorites with @prefix** - e.g., `kmi forecast @home`
4. **Rate limiting is automatic** - CLI handles this transparently

## Output Formats

| Flag | Format | Use case |
|------|--------|----------|
| (default) | Table | User-facing display |
| `--json` | JSON | Agent parsing, scripting |
| `--plain` | TSV | Pipe to awk/cut |

## Workflows

### Current Weather

```bash
# By city name
kmi current Brussels

# By coordinates
kmi current 50.85,4.35

# By saved favorite
kmi current @home

# JSON output for parsing
kmi current Brussels --json
```

### Forecast

```bash
# 7-day forecast
kmi forecast Leuven

# Daily breakdown
kmi daily Leuven

# Hourly for next 12 hours
kmi hourly Leuven

# JSON output
kmi forecast Leuven --json
```

### Radar

```bash
# Download radar animation frames
kmi radar Brussels

# Specify output directory
kmi radar Brussels --output-dir ~/tmp
```

Note: Radar downloads image files to the current or specified directory.

### Warnings

```bash
# Get active weather warnings
kmi warnings Belgium

# JSON for scripting
kmi warnings Belgium --json
```

### UV Index

```bash
# UV index for location
kmi uv Antwerp

# JSON output
kmi uv Antwerp --json
```

### Favorites

```bash
# Save a favorite location
kmi favorites add home 50.85,4.35
kmi favorites add work Brussels

# List all favorites
kmi favorites list

# Use favorites with @ prefix
kmi forecast @home
kmi current @work

# Remove a favorite
kmi favorites remove work
```

## Scripting Examples

```bash
# Get current temperature
kmi current Brussels --json | jq -r '.temperature'

# Check if rain is expected today
kmi forecast Brussels --json | jq -r '.[0].precipitation'

# Get warning count
kmi warnings Belgium --json | jq 'length'

# List all forecasted conditions
kmi forecast Brussels --json | jq -r '.[] | "\(.day): \(.condition)"'
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `KMI_LANG` | Language (en, nl, fr, de) |
| `NO_COLOR` | Disable colored output |

## Guidelines

- No API key needed - works out of the box
- Favorites require user setup - do not create favorites without user consent
- Rate limiting is handled automatically - no special handling needed
- Radar command downloads files - inform user about file output

## Installation

```bash
# macOS/Linux
brew install dedene/tap/kmi

# Windows - download from GitHub Releases
# https://github.com/dedene/kmi-irm-cli/releases
```
