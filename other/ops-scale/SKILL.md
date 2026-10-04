---
name: ops-scale
description: Runtime scaling — adjust replicas, resources, autoscaling
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
effort: medium
---

# Operations — Scale

Adjust runtime capacity based on current load.

## Process

1. Assess current load (CPU, memory, request rate, queue depth)
2. Determine scaling action: scale up/down, add replicas, adjust limits
3. Execute scaling changes
4. Monitor for stability
5. Update autoscaling rules if applicable