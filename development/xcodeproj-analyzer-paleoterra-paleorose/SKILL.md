---
name: xcodeproj-analyzer
description: Parse and analyze Xcode project files to identify configuration issues, missing files, and build settings
type: skill
language: python
---

# Xcodeproj Analyzer

Parse `.xcodeproj` files to analyze build configurations, find issues, and generate reports.

## Capabilities

- Parse project.pbxproj files
- List all targets and their configurations
- Find missing file references
- Identify duplicate file entries
- Analyze build settings
- Check code signing configuration
- List dependencies between targets
- Find unused build phases
- Validate schemes
- Generate project structure reports

## Tools Included

### `xcodeproj_reader.py`
Python script to parse and analyze Xcode project files

**Commands:**
```bash
# Show project summary
./xcodeproj_reader.py PaleoRose.xcodeproj summary

# List all targets
./xcodeproj_reader.py PaleoRose.xcodeproj targets

# Find missing files
./xcodeproj_reader.py PaleoRose.xcodeproj missing-files

# Check build settings
./xcodeproj_reader.py PaleoRose.xcodeproj build-settings <target>

# Export configuration
./xcodeproj_reader.py PaleoRose.xcodeproj export-json output.json
```

## Usage

Invoke when you need to:
- Debug project configuration issues
- Find missing or duplicate files
- Analyze build settings
- Generate project documentation
- Validate project structure
- Compare configurations across targets

## Integration

- Complements `file-organizer` skill
- Works with `build-time-optimizer`
- Supports `dependency-analyzer`
