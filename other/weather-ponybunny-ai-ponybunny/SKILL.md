---
name: weather
description: Get current weather using wttr.in (no API key needed)
---

# Weather Skill

To get the weather for a location, use `execute_command` with `curl`.

## Usage

```bash
curl -s "wttr.in/Location?format=3"
```

## Examples

**User:** "What's the weather in London?"
**Action:** `execute_command("curl -s 'wttr.in/London?format=3'")`

**User:** "Weather in San Francisco"
**Action:** `execute_command("curl -s 'wttr.in/San+Francisco?format=3'")`
