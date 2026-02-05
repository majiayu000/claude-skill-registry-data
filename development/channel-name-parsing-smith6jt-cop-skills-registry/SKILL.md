---
name: channel-name-parsing
description: "Multi-format channel name parsing for KINTSUGI CHANNELNAMES.txt files"
author: KINTSUGI Team
date: 2024-12-15
---

# Channel Name Parsing - Research Notes

## Experiment Overview
| Item | Details |
|------|---------|
| **Date** | 2024-12-15 |
| **Goal** | Parse channel names from various CHANNELNAMES.txt formats |
| **Environment** | KINTSUGI pipeline, Python 3.10+ |
| **Status** | Success |

## Context
Different microscopy systems and users produce CHANNELNAMES.txt files in various formats. KINTSUGI needs to parse channel/marker names to label output files correctly. The parsing must auto-detect the format and handle multiple conventions.

## Supported Formats

### Format 1: Simple List (One Channel Per Line)
Most common format from CODEX systems. Each line is a channel name, 4 channels per cycle. Cycle number extracted from DAPI marker name (DAPI-01, DAPI-02, etc.).

```
DAPI-01
Blank
Blank
Blank
DAPI-02
CD31
CD8
CD45
DAPI-03
CD20
Ki67
CD3e
```

### Format 2: Cycle-Prefixed with Colon
```
1: DAPI, Blank, Blank, Blank
2: DAPI, CD31, CD8, CD45
3: DAPI, CD20, Ki67, CD3e
```

### Format 3: Tab-Separated
```
1	DAPI	Blank	Blank	Blank
2	DAPI	CD31	CD8	CD45
3	DAPI	CD20	Ki67	CD3e
```

### Format 4: CSV (Comma-Separated)
```
1,DAPI,Blank,Blank,Blank
2,DAPI,CD31,CD8,CD45
3,DAPI,CD20,Ki67,CD3e
```

## Verified Workflow

### Complete Parsing Function
```python
import re
from pathlib import Path

def load_channel_names(meta_dir, filename="CHANNELNAMES.txt", channels_per_cycle=4):
    """
    Load channel names from various formats.

    Returns: dict {cycle_number: [channel_names]} or None
    """
    channel_file = Path(meta_dir) / filename

    # Try alternative filenames
    if not channel_file.exists():
        alt_names = ["CHANNELNAMES.txt", "channelnames.txt", "channel_names.txt",
                     "channel_names.csv", "channels.txt", "markers.txt"]
        for alt_name in alt_names:
            alt_file = Path(meta_dir) / alt_name
            if alt_file.exists():
                channel_file = alt_file
                break
        else:
            return None

    # Read non-empty, non-comment lines
    lines = []
    with open(channel_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                lines.append(line)

    if not lines:
        return None

    channel_dict = {}
    first_line = lines[0]

    # Detect format from first line
    if ':' in first_line or '\t' in first_line or \
       (first_line.split(',')[0].strip().isdigit() and len(first_line.split(',')) > 2):
        # Cycle-prefixed format
        for line in lines:
            try:
                if ':' in line:
                    cycle_str, names_str = line.split(':', 1)
                    cycle = int(cycle_str.strip())
                    names = [n.strip() for n in names_str.split(',')]
                elif '\t' in line:
                    parts = line.split('\t')
                    cycle = int(parts[0].strip())
                    names = [n.strip() for n in parts[1:]]
                else:
                    parts = line.split(',')
                    cycle = int(parts[0].strip())
                    names = [n.strip() for n in parts[1:]]
                channel_dict[cycle] = names
            except (ValueError, IndexError):
                continue
    else:
        # Simple list format - detect cycles from DAPI-XX pattern
        current_cycle = 0
        cycle_channels = []

        for line in lines:
            dapi_match = re.match(r'DAPI[-_]?(\d+)', line, re.IGNORECASE)

            if dapi_match:
                # Save previous cycle
                if cycle_channels and current_cycle > 0:
                    channel_dict[current_cycle] = cycle_channels
                # Start new cycle
                current_cycle = int(dapi_match.group(1))
                cycle_channels = [line]
            elif current_cycle > 0:
                cycle_channels.append(line)
                if len(cycle_channels) == channels_per_cycle:
                    channel_dict[current_cycle] = cycle_channels
                    cycle_channels = []

        # Save final cycle
        if cycle_channels and current_cycle > 0:
            channel_dict[current_cycle] = cycle_channels

    return channel_dict
```

### Usage
```python
meta_dir = project.paths.meta  # or Path("/path/to/meta")
channel_name_dict = load_channel_names(meta_dir)

if channel_name_dict is None:
    # Fallback to manual definition
    channel_name_dict = {
        1: ["DAPI", "Blank1a", "Blank1b", "Blank1c"],
        2: ["DAPI", "CD31", "CD8", "CD45"],
        3: ["DAPI", "CD20", "Ki67", "CD3e"],
    }

# Access channel name for cycle 2, channel 3
marker = channel_name_dict.get(2, [''] * 4)[2]  # "CD8"
```

## Failed Attempts (Critical)

| Attempt | Why it Failed | Lesson Learned |
|---------|---------------|----------------|
| Only supporting cycle-prefixed format | Simple list format common in CODEX systems | Must auto-detect format from first line |
| Hardcoding 4 channels per cycle | Some systems have different channel counts | Make channels_per_cycle a parameter |
| Requiring exact "DAPI" match | Some files use "DAPI-01", "DAPI-02" with cycle number | Use regex to extract cycle from DAPI marker |
| Case-sensitive matching | "dapi-01" and "DAPI-01" both valid | Use re.IGNORECASE flag |

## Final Parameters

### Format Detection Heuristic
```python
# Check first line for format indicators
first_line = lines[0]

is_cycle_prefixed = (
    ':' in first_line or           # "1: DAPI, Blank..."
    '\t' in first_line or          # "1\tDAPI\tBlank..."
    (first_line.split(',')[0].strip().isdigit() and
     len(first_line.split(',')) > 2)  # "1,DAPI,Blank..."
)
```

### DAPI Cycle Extraction Regex
```python
dapi_match = re.match(r'DAPI[-_]?(\d+)', line, re.IGNORECASE)
# Matches: DAPI-01, DAPI_01, DAPI01, dapi-1, etc.
```

## Key Insights
- Auto-detect format rather than requiring user specification
- Simple list format uses DAPI marker to determine cycle boundaries
- Always provide fallback when file not found or parsing fails
- Support multiple filename conventions (CHANNELNAMES.txt, channelnames.txt, etc.)
- Comments (lines starting with #) should be ignored
- Empty lines should be skipped

## References
- CODEX channel naming conventions
- KINTSUGI Notebook 2 cell-7 (Processing Parameters)
