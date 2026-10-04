---
name: note-taker
description: Capture short notes into project files.
license: MIT
compatibility:
  agentskills: ">=0.1"
  allbert: ">=0.4"
metadata:
  tags: [notes, writing]
intents: [task, memory_query]
allowed-tools: [write_file, request_input, read_reference]
scripts:
  - name: slugify
    path: scripts/slugify.py
    interpreter: python
---

# Note Taker

When the user wants a durable note captured, ask for any missing destination details
with `request_input`.

If you want the canonical note shape, use `read_reference` on
`references/note-template.md`.

If you need a stable slug from a short title, use `run_skill_script` with the
`slugify` script.

Then write a concise markdown note with `write_file`.
