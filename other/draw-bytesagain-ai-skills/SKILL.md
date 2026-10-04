---
name: draw
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [draw, tool, utility]
description: "Create SVG diagrams with shapes, layers, and multi-format export. Use when generating graphics, building diagrams, arranging layouts."
---
# Draw

Design toolkit for managing color palettes, generating swatches, mixing colors, creating gradients, previewing designs, and exporting results. A command-line companion for designers and front-end developers.

## Commands

| Command | Description |
|---------|-------------|
| `draw palette <input>` | Create or log a color palette entry |
| `draw preview <input>` | Record a design preview note |
| `draw generate <input>` | Generate and log a design asset or concept |
| `draw convert <input>` | Log a color or format conversion |
| `draw harmonize <input>` | Record a color harmony analysis |
| `draw contrast <input>` | Log a contrast check result |
| `draw export <input>` | Log an export operation |
| `draw random <input>` | Record a random color or design generation |
| `draw browse <input>` | Log a browsing/discovery session |
| `draw mix <input>` | Record a color mixing result |
| `draw gradient <input>` | Log a gradient definition |
| `draw swatch <input>` | Record a color swatch entry |
| `draw stats` | Show summary statistics across all logs |
| `draw export <fmt>` | Export all data (json, csv, or txt) |
| `draw search <term>` | Search across all log files for a term |
| `draw recent` | Show the 20 most recent activity entries |
| `draw status` | Health check — version, disk usage, last activity |
| `draw help` | Show all available commands |
| `draw version` | Show current version |

Each command without arguments displays the most recent 20 entries from its log file.

## Data Storage

All data is stored in `~/.local/share/draw/`:

- **Per-command logs** — `palette.log`, `preview.log`, `generate.log`, `convert.log`, `harmonize.log`, `contrast.log`, `export.log`, `random.log`, `browse.log`, `mix.log`, `gradient.log`, `swatch.log`
- **Activity history** — `history.log` (unified timeline of all actions)
- **Exports** — `export.json`, `export.csv`, or `export.txt` (generated on demand)

Data format: each entry is stored as `YYYY-MM-DD HH:MM|<value>`, pipe-delimited for easy parsing.

## Requirements

- Bash 4+ with `set -euo pipefail`
- Standard POSIX utilities (`date`, `wc`, `du`, `head`, `tail`, `grep`, `cut`, `basename`)
- No external dependencies or API keys required

## When to Use

1. **Building a color system** — log palettes, harmonies, and contrast checks while designing a brand or UI theme
2. **Prototyping design assets** — generate swatches, gradients, and random color explorations for rapid iteration
3. **Auditing accessibility** — record contrast ratios and color harmony data for WCAG compliance reviews
4. **Maintaining a design journal** — track every color decision, mix experiment, and conversion over time
5. **Exporting design data** — export your full color and design history as JSON, CSV, or plain text for handoff to other tools

## Examples

```bash
# Log a new palette
draw palette "#FF5733 #33FF57 #3357FF warm-sunset"

# Record a contrast check
draw contrast "bg:#FFFFFF fg:#333333 ratio:12.6:1 PASS"

# Mix two colors and log the result
draw mix "#FF0000 + #0000FF = #800080 purple"

# Generate a gradient definition
draw gradient "linear 90deg #000000 → #FFFFFF"

# Create a swatch entry
draw swatch "Coral #FF7F50 used in header CTA"

# Export all design data as JSON
draw export json

# Search all logs for a specific hex color
draw search "FF5733"

# View recent activity
draw recent

# Check overall status
draw status
```

## Output

All command output goes to stdout. Redirect to a file if needed:

```bash
draw stats > design-report.txt
draw export csv
```

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
