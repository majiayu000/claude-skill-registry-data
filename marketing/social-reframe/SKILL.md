---
name: social-reframe
description: Create aspect-specific social derivatives using approved focus points or fit rules for 16:9, 9:16, 1:1, 4:5, or custom dimensions without arbitrarily cropping required story information.
disable-model-invocation: true
author: Alan Guice (Badgids)
license: Apache-2.0
---

# Social Reframe

## Workflow

1. Read `../../references/SOCIAL_CAMPAIGN.md`, the destination deliverable, source media QC, and any focus-region metadata.
2. Prefer destination-native source media when available.
3. Otherwise choose `cover` only when a safe focus point keeps required faces, action, props, and text visible.
4. Choose `contain` with padding when a fill crop would destroy required information.
5. Run `scripts/social_reframe.py` for deterministic derivatives.
6. Register the derivative as new media and run QC if it is a final campaign asset.

## Done

The destination aspect is correct and the crop decision is explicit and reproducible.
