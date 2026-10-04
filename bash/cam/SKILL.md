---
name: "CAM — Computer-Aided Manufacturing Toolpath Reference"
description: "Use when calculating CNC speeds and feeds, selecting cutting tools, referencing G-code commands, looking up material cutting data, or computing machining parameters."
version: "2.0.1"
author: "BytesAgain"
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: ["cam", "cnc", "machining", "gcode", "manufacturing", "toolpath", "engineering"]
---

# CAM — Computer-Aided Manufacturing Toolpath Reference

CNC machining reference — speeds & feeds calculator, toolpath strategies, G-code command reference, material cutting data, and machining parameter computation.

## Commands

### speeds-feeds
Calculate spindle speed (RPM) and feed rate.
```bash
bash scripts/script.sh speeds-feeds 10 80 0.05 3
```

### toolpath
Toolpath strategy reference (adaptive, pocket, contour, etc.).
```bash
bash scripts/script.sh toolpath
bash scripts/script.sh toolpath adaptive
```

### gcode
G-code and M-code command reference.
```bash
bash scripts/script.sh gcode
bash scripts/script.sh gcode G02
```

### materials
Material cutting data — recommended SFM, chipload, depth of cut.
```bash
bash scripts/script.sh materials
bash scripts/script.sh materials aluminum
```

### calculate
General machining calculations (MRR, power, time).
```bash
bash scripts/script.sh calculate mrr 10 2 0.5 800
bash scripts/script.sh calculate power 50 1500
```

### help
Show all commands.
```bash
bash scripts/script.sh help
```

## Output
- Calculated RPM, feed rates, and machining parameters
- G-code reference with syntax and examples
- Material-specific cutting recommendations

## Feedback
https://bytesagain.com/feedback/
Powered by BytesAgain | bytesagain.com
