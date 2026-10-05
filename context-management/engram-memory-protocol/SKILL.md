---
name: engram-memory-protocol
description: "Trigger: memory, decision, bug fix, discovery, session summary, Engram. Preserve NutrIA continuity with curated project memory."
license: MIT
metadata:
  author: "NutrIA"
  version: "0.1.0"
---

# Activation Contract
Use at session start, after important work and before session end.

# Hard Rules
- Call `mem_context` at session start for ongoing work; search before relying on a past decision.
- Save decisions, bugs, discoveries, conventions and confirmed preferences immediately with `mem_save`.
- Use stable `topic_key` values for evolving topics; do not overwrite unrelated memories.
- Save a session summary before declaring work done.
- Never store secrets, tokens, connection strings or sensitive user data.

# Execution Steps
1. Feed the user prompt through `mem_save_prompt` when available.
2. Retrieve recent context and full observations as needed.
3. Save curated structured observations with What, Why, Where and Learned.
4. Resolve returned conflicts explicitly; do not silently ignore them.

# Output Contract
Leave searchable, minimal memory and a session handoff.
