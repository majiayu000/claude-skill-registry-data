---
name: lifecycle/garbage-collection
description: Remove the ephemeral model, flush VRAM, drop temp memory shards, and verify cleanup. Use immediately after transient execution.
---

# Garbage Collection (Ghost Cleanup)

Capabilities
- nuke_model_artifact: `ollama rm {model_name}`.
- flush_vram_cache: trigger GPU memory release (best-effort).
- drop_memory_shard: delete transient memory collection.
- verify_cleanup: confirm removal via `ollama list` or similar check.

Inputs
- model_name, memory_shard id.

Outputs
- cleanup report (success/fail), leftover checks.
