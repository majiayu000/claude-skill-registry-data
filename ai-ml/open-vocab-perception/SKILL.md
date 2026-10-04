---
name: open-vocab-perception
description: Use when the robot must find/segment/grasp an object named in language ("pick up the blue mug") without a trained detector — run a Grounding DINO → SAM 2 → depth-lift pipeline driven by a text prompt.
stacks: [python]
domains: [hardware]
phases: [dev]
tags: [perception, foundation-models, sam2, grounding-dino, open-vocabulary, grasping]
scope: kit
---
**When to use.** Language-specified targets, or avoiding per-object training. *Why:* open-vocab
foundation models remove the label→train→deploy loop; you swap the noun in the prompt.

**Procedure.**
1. Text prompt → Grounding DINO boxes (tune box/text thresholds).
2. Boxes → SAM 2 masks (and track across frames if moving).
3. Lift the chosen mask to 3D via the depth image + camera intrinsics; cluster to a grasp target.
4. **Done when:** the named object is localized in 3D within tolerance on a test scene; run heavy models off-board.

**Knowledge:** KNOWLEDGE-LIBRARY.md §B1. **Example:** the Grounded-SAM-2 snippet there.
