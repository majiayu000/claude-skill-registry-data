---
name: screenshot
description: Capture PNG screenshots of dex TUI commands for debugging UI layout issues. Use when iterating on CLI interface code or debugging rendering problems.
---

# Screenshot Tool

Capture screenshots of dex TUI commands using vhs.

## Instructions

1. Run the screenshot tool with a dex command:
   ```bash
   ./tools/screenshot.sh "<command>" [options]
   ```

2. Read the output file to view the captured TUI:
   ```bash
   # Default output is /tmp/dex-screenshot.png
   ```

3. Use the Read tool on the PNG file to see the rendered UI.

## Options

- `-o, --output <path>` - Output PNG path (default: /tmp/dex-screenshot.png)
- `-k, --keys <keys>` - Key sequence to send after initial load (comma-separated)
- `-w, --wait <seconds>` - Initial wait time in seconds (default: 10)
- `--no-open` - Don't open the screenshot after capture

## Key Sequence

Use `-k` to navigate through screens. Supported keys:
- `enter` - Press Enter (navigate into views)
- `esc` - Press Escape (go back)
- `j`, `k` - Navigate up/down
- `g`, `G` - Go to top/bottom
- Any single character

## Examples

```bash
# Screenshot list view (search results)
./tools/screenshot.sh "search api"

# Screenshot matches view (press Enter to expand first result)
./tools/screenshot.sh "search api" -k enter

# Screenshot conversation view (Enter twice)
./tools/screenshot.sh "search api" -k enter,enter

# Screenshot with navigation (go to matches, scroll down twice)
./tools/screenshot.sh "search api" -k enter,j,j

# Custom output path
./tools/screenshot.sh "search api" -o /tmp/api-search.png -k enter

# Don't auto-open (useful for automation)
./tools/screenshot.sh "list" --no-open
```

## View Navigation

The search command has 4 views:
1. **List view** - Initial search results (no keys needed)
2. **Matches view** - All matches in a conversation (`-k enter`)
3. **Conversation view** - Full conversation with messages (`-k enter,enter`)
4. **Message view** - Full message content (`-k enter,enter,enter`)

## Workflow

1. Make changes to TUI code in `src/cli/commands/`
2. Run screenshot tool to capture the result
3. Read the PNG to view the rendered UI
4. Iterate based on what you see

## Requirements

Requires vhs: `brew install vhs`
