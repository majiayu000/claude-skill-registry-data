---
name: figma-desktop
description: Extract design data from Figma files using REST API scripts. Includes frame extraction, metadata retrieval, screenshots, design token extraction, annotations, and FigJam content for design-to-code workflows.
---

# Figma Desktop Skill

Extract and process Figma design data for design-to-code implementation in the IRIS project.

## Capabilities

### REST API Scripts
Node.js scripts that extract Figma data (requires `FIGMA_TOKEN`):

- **extract-frames.js** - Extract all frames from a Figma page
- **get-metadata.js** - Get node structure and hierarchy
- **get-screenshot.js** - Capture node screenshots
- **get-variable-defs.js** - Extract design tokens (colors, text styles, variables)
- **get-annotations.js** - Get dev mode annotations and handoff notes
- **get-code-connect-map.js** - Get Figma component metadata for code mapping
- **get-figjam.js** - Extract FigJam board content (sticky notes, shapes, text)
- **compare-frames.js** - Compare current vs documented frames

## Setup

### Figma Token

Generate your token at https://www.figma.com/settings → Personal Access Tokens

The scripts look for the token in this order:
1. CLI argument (passed directly to script)
2. `FIGMA_TOKEN` environment variable
3. `FIGMA_KEY` environment variable
4. Claude user settings (`~/.claude/settings.json`)

**Recommended: Claude Settings** (persists across sessions)

Add to `~/.claude/settings.json`:
```json
{
  "env": {
    "FIGMA_KEY": "your-figma-token"
  }
}
```

**Alternative: Environment Variable**
```bash
# Windows (PowerShell)
$env:FIGMA_TOKEN="your-token"

# Windows (CMD)
set FIGMA_TOKEN=your-token

# Mac/Linux
export FIGMA_TOKEN="your-token"
```

### IRIS Project File Key
```
xFC8eCJcSwB9EyicTmDJ7w
```

## Usage

### Extract Frames
```bash
node .claude/skills/figma-desktop/scripts/extract-frames.js xFC8eCJcSwB9EyicTmDJ7w 2501:2715
```

### Get Metadata
```bash
node .claude/skills/figma-desktop/scripts/get-metadata.js xFC8eCJcSwB9EyicTmDJ7w 6804:13742
```

### Get Screenshot
```bash
node .claude/skills/figma-desktop/scripts/get-screenshot.js xFC8eCJcSwB9EyicTmDJ7w 6804:13742
```

### Get Design Tokens
```bash
node .claude/skills/figma-desktop/scripts/get-variable-defs.js xFC8eCJcSwB9EyicTmDJ7w
```

### Get Annotations
```bash
node .claude/skills/figma-desktop/scripts/get-annotations.js xFC8eCJcSwB9EyicTmDJ7w 6804:13742
```

### Get Code Connect Mapping
```bash
node .claude/skills/figma-desktop/scripts/get-code-connect-map.js xFC8eCJcSwB9EyicTmDJ7w
```

### Get FigJam Content
```bash
node .claude/skills/figma-desktop/scripts/get-figjam.js xFC8eCJcSwB9EyicTmDJ7w 123:456
```

### Compare Frames
```bash
# First extract current frames
node .claude/skills/figma-desktop/scripts/extract-frames.js xFC8eCJcSwB9EyicTmDJ7w 2501:2715

# Then compare with documented frames
node .claude/skills/figma-desktop/scripts/compare-frames.js
```

## Output Files

Scripts create temporary files in project root:
- `temp-frames-list.json` - Frame list
- `temp-metadata-*.json` - Node metadata
- `temp-design-tokens-*.json` - Design tokens
- `temp-annotations-*.json` - Annotations data
- `temp-code-connect-*.json` - Component mappings
- `temp-figjam-*.json` - FigJam content
- `temp-comparison-report.json` - Frame comparison
- `screenshot-*.png` - Screenshots

Clean up with:
```bash
rm temp-*.json screenshot-*.png
```

## Integration

This skill integrates with IRIS documentation:
- Frame mapping: `docs/figma/frame-node-mapping.json`
- Screenshots: `docs/figma/screenshots/`
- Design tokens: `docs/figma/design-system-mapping.json`

## When to Use This Skill

Use this skill when:
- Implementing UI components from Figma designs
- Extracting design tokens for the design system
- Updating frame mappings after Figma changes
- Generating screenshots for documentation
- Extracting FigJam brainstorming content
- Getting dev handoff notes and annotations
- Automating batch operations on Figma data
- Running in CI/CD pipelines

## Node ID Format

Node IDs can be in either format:
- Colon format: `2501:2715` (API format)
- Dash format: `2501-2715` (URL format)

Scripts automatically convert between formats as needed.

## File Keys

Find the file key in any Figma URL:
```
https://figma.com/design/<FILE_KEY>/...
```

## Token Resolution

Scripts automatically resolve the Figma token from:
1. CLI argument
2. `FIGMA_TOKEN` env var
3. `FIGMA_KEY` env var
4. `~/.claude/settings.json` → `env.FIGMA_KEY`
