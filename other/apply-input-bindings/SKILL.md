---
name: apply-input-bindings
description: "Use when mapping actions to multi-platform hardware bindings (KBM, Xbox, PS, touch). Triggers: 'input mapping', 'cross-platform input'."
---

## 1. Overview

Maps abstract game actions to concrete hardware inputs across multiple platforms, producing a cross-platform binding matrix. Core principle: code against abstract Action IDs, not physical buttons.

## 2. When to Use

Use when:
- You have abstract action IDs and need concrete hardware bindings for multiple platforms (KBM, Xbox, PS, touch).
- You're updating bindings after adding new actions or supporting a new platform.
- You need a cross-platform binding matrix documented in `input_mapping.md`.

Do not use when:
- Abstract actions haven't been defined yet — run `define-player-controls` first.
- You only need bindings for one platform with no cross-platform goals.

## 3. Red Flags
- **Abstract Action IDs**: Reference abstract Action IDs exclusively in implementation code
- **Complete Platform Coverage**: Define bindings for every requested target platform
- **Analog Configuration**: Set dead zone thresholds and response curves (Linear, Exponential) for all analog inputs
- **Unique Input Bindings**: Assign non-conflicting physical inputs per device
- **Hardware-Appropriate Interactions**: Map interactions to supported hardware capabilities
- **Mobile Touch Support**: Include touch mappings for all mobile/handheld platforms

## 3. Workflow
1. **Action Abstraction**: Extract hardware-agnostic Action IDs (`move`, `jump`, `attack`) from game specs.
2. **Multi-Platform Mapping**: Determine optimal bindings for KBM, Xbox, PlayStation, Touch.
3. **Analog & Sensitivity**: Set dead zone thresholds and response curves for all analog inputs.
4. **Complexity Validation**: Verify complex interactions are supported by chosen platform capabilities.
5. **Export**: Write cross-platform mapping matrix to `{TARGET_FOLDER}/docs/16_input_mapping.md`.

## 4. Error Intercepts
- **[Platform Gap]**: "Action [ID] has no mapping for [Platform]. Unplayable on that device. Assign default or wait?"
- **[Control Complexity]**: "Action [ID] requires [Complexity Type] which may be difficult on [Platform]. Consider [Alternative]?"
