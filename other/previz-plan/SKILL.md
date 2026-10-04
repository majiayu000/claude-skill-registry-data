---
name: previz-plan
description: Create tool-neutral scene previz plans with geometry, entrances, exits, actors, paths, props, eyelines, camera setups, screen direction, and cut order using stable project IDs.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Previz Plan

## Workflow

1. Read the standalone contract, core contract, previz schema, screenplay scene, director book, continuity, references, and planned shot scope.
2. Decide whether previz adds value. Use it for difficult geography, blocking, action, eyelines, moving cameras, vehicles, or coverage problems.
3. Separate verified geometry from planning assumptions.
4. Create `03_preproduction/previz/SCN-###.json` using the portable schema.
5. Record actor start and end states, important paths, entrances, exits, obstacles, important props, eyelines, camera setups, axis side, and screen direction.
6. Use metric coordinates only when known or intentionally chosen. Mark estimates as approximate.
7. Add a short `SCN-###.md` explanation of the scene geography and any unresolved staging problem.
8. If previz reveals a shot problem, update shot design and run `project-impact` for that scene scope.

## Done

The scene can be blocked or reconstructed in a generic 3D or diagramming tool without reading the chat, and no invented measurement is presented as known fact.
