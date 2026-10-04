---
name: remember
description: Harmonia remember - capture a single learning into the right memory tier. Use ONLY when explicitly invoked as /harmonia:remember.
disable-model-invocation: true
---

Capture ONE learning through the memory script with an explicit tier. Never a bare or defaulted global write.

1. Elicit the tier from the developer - do not guess it:
   - `project` - specific to this repo (the usual choice);
   - `global` - a cross-project pattern, carrying NO client content.
   Ask which tier, and pass `--client` for a client-work learning.

2. Capture it, body on stdin:

```bash
echo "<the learning body>" | bash ${CLAUDE_PLUGIN_ROOT}/bin/memory/capture.sh --tier <project|global> [--client] --title "<short title>" --tags "<lang,topic>"
```

Client content never reaches the global tier: `capture.sh` refuses a `--client` write to `--tier global` with a non-zero exit, and refuses a global entry with no recognized language tag (it would be unreachable by recall). That deterministic guard is the backstop behind the tier you elicit - not a licence to default the tier. Surface the script's output.
