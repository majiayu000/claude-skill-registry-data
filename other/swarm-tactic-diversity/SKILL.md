---
name: llm-swarm-tactic-diversity
description: Assign each new agent a different directional rotation pattern from a set of permutations to ensure swarm coverage diversity across the map
---

# Swarm Tactic Diversity

## Overview

When spawning multiple agents with the same patrol/exploration pattern, they all cover the same area. By maintaining a pool of movement pattern permutations (e.g., 8 rotations of NESW) and assigning each new agent the next pattern in round-robin order, the swarm naturally distributes across the map. This avoids clustering without explicit coordination or communication between agents.

## Quick Start

```python
TACTICS = [
    ['NORTH', 'EAST', 'SOUTH', 'WEST'],
    ['SOUTH', 'EAST', 'NORTH', 'WEST'],
    ['NORTH', 'WEST', 'SOUTH', 'EAST'],
    ['SOUTH', 'WEST', 'NORTH', 'EAST'],
    ['EAST', 'NORTH', 'WEST', 'SOUTH'],
    ['WEST', 'SOUTH', 'EAST', 'NORTH'],
    ['EAST', 'SOUTH', 'WEST', 'NORTH'],
    ['WEST', 'NORTH', 'EAST', 'SOUTH'],
]

class SwarmManager:
    def __init__(self):
        self.tactic_index = 0
        self.agents = {}

    def register(self, agent_id):
        self.agents[agent_id] = {
            'directions': TACTICS[self.tactic_index],
            'step': 0,
        }
        self.tactic_index = (self.tactic_index + 1) % len(TACTICS)

    def get_direction(self, agent_id):
        agent = self.agents[agent_id]
        d = agent['directions'][agent['step'] % len(agent['directions'])]
        agent['step'] += 1
        return d

swarm = SwarmManager()
for ship_id in new_ships:
    swarm.register(ship_id)
```

## Workflow

1. Define N direction permutations (rotations/reflections of base pattern)
2. Maintain a global round-robin index
3. On each new agent spawn, assign the next permutation
4. Agent follows its assigned pattern for patrol/exploration
5. Swarm naturally covers different quadrants without coordination

## Key Decisions

- **Number of permutations**: 4 (rotations) or 8 (rotations + reflections) cover a square grid
- **Round-robin vs random**: round-robin guarantees even distribution; random may cluster
- **Pattern type**: works with spirals, zigzags, or any directional sequence
- **Scaling**: with more agents than permutations, patterns repeat — acceptable since agents start at different positions

## References

- [Halite Swarm Intelligence](https://www.kaggle.com/code/yegorbiryukov/halite-swarm-intelligence)
