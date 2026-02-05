---
name: mmd-cli
description: Use the MIDI Markdown Compiler (mmdc) CLI for compiling MMD to MIDI, validating syntax, real-time playback with TUI, exporting to different formats (JSON, CSV, table), and managing device libraries. Use when the user wants to compile, validate, play, inspect MMD files, or work with device libraries.
---

# MMDC CLI Usage Skill

## Overview

This skill helps you effectively use the MIDI Markdown Compiler (`mmdc`) command-line interface for compiling, validating, playing, inspecting MMD files, and managing device libraries.

## Core Commands

### Compile MMD to MIDI

```bash
# Basic compilation
mmdc compile input.mmd -o output.mid

# With custom resolution
mmdc compile song.mmd -o song.mid --ppq 960

# Export to different formats
mmdc compile song.mmd --format json -o events.json
mmdc compile song.mmd --format csv -o events.csv
mmdc compile song.mmd --format table  # Display in terminal
```

### Validate Without Compiling

```bash
# Full validation (recommended before compilation)
mmdc validate song.mmd

# Verbose output with details
mmdc validate song.mmd --verbose

# Just syntax check (no semantic validation)
mmdc check song.mmd
```

### Real-Time Playback

```bash
# Play with TUI (interactive terminal UI)
mmdc play song.mmd --port 0

# List available MIDI ports
mmdc play --list-ports

# Play with specific port by name
mmdc play song.mmd --port "IAC Driver Bus 1"
```

**TUI Controls**:
- **Spacebar** - Pause/Resume
- **Q** - Quit
- **R** - Restart from beginning

### Inspect Events

```bash
# Display event timeline as table
mmdc inspect song.mmd

# With more detail
mmdc inspect song.mmd --verbose

# Filter by event type
mmdc inspect song.mmd --type note_on
mmdc inspect song.mmd --type cc
```

### Device Library Management

```bash
# List all installed device libraries
mmdc library list

# Show info about a specific library
mmdc library info quad_cortex
mmdc library info eventide_h90

# Validate a device library file
mmdc library validate devices/my_device.mmd
mmdc library validate custom_library.mmd

# Search for libraries
mmdc library search "eventide"
mmdc library search "helix"
mmdc library search "neural"

# Create a new device library template
mmdc library create my_device
mmdc library create my_synth --manufacturer "Acme" --device "Acme Synth Pro"
mmdc library create my_fx --output my_library.mmd --channel 5

# Install library from repository (planned feature)
# mmdc library install eventide-h90
```

**Library Commands**:
- `library list` - Shows all available device libraries with alias counts
- `library info <name>` - Displays library metadata and all available aliases
- `library validate <file>` - Checks library syntax and structure
- `library search <query>` - Searches libraries by name, manufacturer, or description
- `library create <name>` - Creates a new device library template
- `library install <source>` - (Planned) Install from repository or URL

## Common Options

### Output Formats

- `--format midi` (default) - Standard MIDI file
- `--format json` - JSON representation
- `--format csv` - CSV export (midicsv-compatible)
- `--format table` - Terminal table display

### Resolution/PPQ

- `--ppq 480` (default) - High resolution
- `--ppq 960` - Very high resolution
- `--ppq 192` - Standard resolution

### Verbosity

- `--verbose` - Detailed output
- `--quiet` - Minimal output
- `--debug` - Debug information

## Workflow Examples

### Development Workflow

```bash
# 1. Check syntax while writing
mmdc check song.mmd

# 2. Full validation before compilation
mmdc validate song.mmd

# 3. Inspect events to verify
mmdc inspect song.mmd

# 4. Compile to MIDI
mmdc compile song.mmd -o output.mid

# 5. Test playback
mmdc play song.mmd --port 0
```

### Quick Test Loop

```bash
# Edit, validate, play cycle
mmdc validate song.mmd && mmdc play song.mmd --port 0
```

### Batch Processing

```bash
# Compile all MMD files in directory
for file in *.mmd; do
  mmdc compile "$file" -o "output/$(basename "$file" .mmd).mid"
done

# Validate all examples
mmdc validate examples/**/*.mmd
```

## Troubleshooting

### Validation Errors

```bash
# Get detailed error information
mmdc validate song.mmd --verbose

# Check just syntax first
mmdc check song.mmd

# Inspect specific section
mmdc inspect song.mmd
```

**Common Errors**:

1. **Timing going backwards**
   - Error: "Time X is before previous event at time Y"
   - Fix: Ensure timing markers increase monotonically

2. **Values out of range**
   - Error: "Value X exceeds maximum allowed (127)"
   - Fix: Check MIDI value ranges (0-127, channels 1-16)

3. **Missing timing marker**
   - Error: "No timing marker before first event"
   - Fix: Always start with `[00:00.000]` or `[1.1.0]`

4. **Invalid syntax**
   - Error: "Unexpected token at line X"
   - Fix: Check syntax against REFERENCE.md in mmd-writing skill

### Playback Issues

```bash
# List all available MIDI ports
mmdc play --list-ports

# Test with different port
mmdc play song.mmd --port 1

# Check events are correct
mmdc inspect song.mmd
```

**Common Issues**:
- No MIDI output: Check port number with `--list-ports`
- Wrong timing: Verify events with `inspect` command
- Missing events: Check validation output

### Compilation Failures

```bash
# Validate first to see errors
mmdc validate song.mmd

# Check for import issues
mmdc check song.mmd --verbose

# Export to JSON for debugging
mmdc compile song.mmd --format json -o debug.json
```

## Tips and Best Practices

### Always Validate First

Before compiling, always validate to catch errors early:

```bash
mmdc validate song.mmd && mmdc compile song.mmd -o output.mid
```

### Use Inspect for Debugging

When timing or values seem wrong, inspect the events:

```bash
mmdc inspect song.mmd | grep "note_on"
mmdc inspect song.mmd --type cc
```

### Test with Playback

Real-time playback helps verify timing and automation:

```bash
mmdc play song.mmd --port 0
# Use spacebar to pause, Q to quit, R to restart
```

### Export for Analysis

JSON and CSV formats are great for analysis:

```bash
# JSON for programmatic access
mmdc compile song.mmd --format json -o events.json

# CSV for spreadsheet analysis
mmdc compile song.mmd --format csv -o events.csv
```

## Integration with Other Tools

### Using with UV (Python Package Manager)

```bash
# Run from project directory
uv run mmdc compile song.mmd -o output.mid

# Or after installation
mmdc compile song.mmd -o output.mid
```

### Using with Just (Task Runner)

```bash
# If project has justfile
just compile input.mmd output.mid
just validate song.mmd
just run play song.mmd
```

### Piping Output

```bash
# Validate and capture output
mmdc validate song.mmd 2>&1 | tee validation.log

# Inspect and filter
mmdc inspect song.mmd | grep "00:10"
```

## Error Codes

Common exit codes:
- `0` - Success
- `1` - Validation error
- `2` - File not found
- `3` - Compilation error
- `4` - Runtime error (playback)

## Getting Help

```bash
# General help
mmdc --help

# Command-specific help
mmdc compile --help
mmdc validate --help
mmdc play --help
mmdc inspect --help

# Version information
mmdc --version
```

## Quick Reference

| Task | Command |
|------|---------|
| Compile to MIDI | `mmdc compile input.mmd -o output.mid` |
| Validate | `mmdc validate song.mmd` |
| Syntax check | `mmdc check song.mmd` |
| Play with TUI | `mmdc play song.mmd --port 0` |
| List MIDI ports | `mmdc play --list-ports` |
| Inspect events | `mmdc inspect song.mmd` |
| Export JSON | `mmdc compile song.mmd --format json -o out.json` |
| Export CSV | `mmdc compile song.mmd --format csv -o out.csv` |
| Table display | `mmdc compile song.mmd --format table` |
| List libraries | `mmdc library list` |
| Library info | `mmdc library info quad_cortex` |
| Validate library | `mmdc library validate devices/my_device.mmd` |
| Search libraries | `mmdc library search "eventide"` |
| Create library | `mmdc library create my_device` |

## Complete Examples

### Example 1: Basic Compile and Play

```bash
# Create a simple MMD file
cat > test.mmd << 'EOF'
---
title: "Test Song"
ppq: 480
tempo: 120
---

[00:00.000]
- tempo 120
- note_on 1.C4 100 1b
- note_on 1.E4 100 1b
- note_on 1.G4 100 1b
EOF

# Validate
mmdc validate test.mmd

# Compile
mmdc compile test.mmd -o test.mid

# Play
mmdc play test.mmd --port 0
```

### Example 2: Debugging Workflow

```bash
# Check syntax
mmdc check problematic.mmd

# Full validation with verbose output
mmdc validate problematic.mmd --verbose

# Inspect events to find issues
mmdc inspect problematic.mmd

# Export to JSON for detailed analysis
mmdc compile problematic.mmd --format json -o debug.json

# View specific event types
mmdc inspect problematic.mmd --type cc | less
```

### Example 3: Batch Validation

```bash
# Validate all MMD files
find . -name "*.mmd" -exec mmdc validate {} \;

# Or with better output
for file in examples/**/*.mmd; do
  echo "Validating $file..."
  mmdc validate "$file" || echo "FAILED: $file"
done
```

### Example 4: Export and Analyze

```bash
# Export to CSV
mmdc compile song.mmd --format csv -o events.csv

# Analyze in spreadsheet or with command-line tools
cut -d',' -f1,3,4 events.csv | grep "note_on"

# Export to JSON for scripting
mmdc compile song.mmd --format json -o events.json
jq '.events[] | select(.type == "note_on")' events.json
```

## Performance Tips

### Large Files

For large MMD files (>1000 events):

```bash
# Use higher PPQ for better precision
mmdc compile large.mmd -o large.mid --ppq 960

# Validate in chunks by inspecting sections
mmdc inspect large.mmd --from 0 --to 100
```

### Rapid Iteration

```bash
# Watch mode (requires entr or similar)
ls *.mmd | entr -c mmdc validate song.mmd

# Quick compile and play
alias mmdp='mmdc validate $1 && mmdc play $1 --port 0'
mmdp song.mmd
```

## Related Skills

- **mmd-writing** - For help writing MMD files with correct syntax

## Additional Resources

- **Project Examples**: `examples/` directory contains 49 working example files
- **User Documentation**: `docs/user-guide/` in project root
- **Specification**: `spec.md` - Complete MMD language specification
- **Developer Guides**: `docs/dev-guides/` for implementation details

## Common Use Cases

### Live Performance

```bash
# List MIDI ports to find your device
mmdc play --list-ports

# Play live set automation
mmdc play live-set.mmd --port "Your Device Name"
```

### Studio Production

```bash
# Compile automation for DAW
mmdc compile automation.mmd -o automation.mid --ppq 960

# Validate before session
mmdc validate *.mmd
```

### Testing and Development

```bash
# Quick validation loop during development
while true; do
  clear
  mmdc validate song.mmd
  sleep 2
done

# Generate test data
mmdc compile test.mmd --format json -o test-data.json
```

---

For help writing MMD files, see the **mmd-writing** skill.
For project documentation, see `docs/` in project root.
