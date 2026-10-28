---
name: fabric-loop
description: >-
  Fabric mode for a repeat-until-done cycle (CI green, review rounds). Arrives
  in 5.4.1; until then routes to loop-templates and its flow-loop template.
category: bdb-core
---

# `/fabric-loop` — arrives in 5.4.1

This mode is documented, not implemented yet. It will run one cycle repeatedly until an exit condition holds, with a bounded iteration count.

**Until 5.4.1:** use the `loop-templates` skill and its `flow-loop` template, or `ci-until-green` / `review-rounds` for those two cases. Say in one line that `fabric-loop` is not available yet and which template you used instead.

Do not improvise an unbounded loop. A loop always has a maximum iteration count and an exit condition.
