---
description: Get a one-time bypass so the next Write/Edit is not blocked by strict mode (for probing)
disable-model-invocation: true
---

The user wants to run a probe — make **one** minimal viable change by hand and verify it works,
then write the recipe into a task book afterward.

Create the one-time bypass flag:

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/pi-probe"
```

Then tell the user: **this flag is good for one use only** — it turns itself off automatically after
the next Write/Edit goes through. Once the probe is done, immediately write the verified recipe into
a task book, and dispatch everything else to pi as usual.
