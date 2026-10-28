---
name: fabric-swarm
description: >-
  Fabric mode for many similar workers claiming items from one shared pool.
  Arrives in 5.4.1. Until then this skill routes to fabric-multigraph. Use when
  the user asks for a swarm or for many parallel workers on one list of items.
category: bdb-core
---

# `/fabric-swarm` — arrives in 5.4.1

This mode is documented, not implemented yet. It will run N similar workers that claim items from one shared list.

**Until 5.4.1:** use `fabric-multigraph` and split the list into 2-4 slices, one per worker. Say in one line that `fabric-swarm` is not available yet and that you routed to `fabric-multigraph`.

Do not improvise a swarm dispatcher, a shared claim file or a worker pool in the meantime. Agents never invoke each other; the dispatcher decides every next step.
