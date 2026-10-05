---
name: relay-sync
description: Synchronize state between multiple Claude Code instances via airlock-coordination
---

# Relay Sync

Coordinate state and task handoffs between concurrent Claude Code instances using the airlock-coordination layer. Prevents conflicting edits, surfaces in-progress work across tabs, and enables structured handoffs when one instance completes a phase that another must continue.

## Integration

This skill integrates with the `airlock-coordination` repo. It reads and writes coordination state through `otto-hooks.py` and the coordination bus — never via direct file edits. Session state that spans instances is persisted through `airlock-persona`'s `session-manager.py`.

## Standalone Behavior

- Before starting a file-modifying task, check the coordination bus for any in-progress locks on the same files
- Register a lock with task scope and estimated completion before beginning destructive or multi-file operations
- On completion or interruption, release locks and write a handoff summary to the coordination bus so other instances can resume cleanly
- Surface active instances and their current tasks when the user asks about multi-instance state
- If a conflict is detected (two instances attempting to modify the same file), pause and surface both task contexts to the user for resolution rather than proceeding unilaterally
