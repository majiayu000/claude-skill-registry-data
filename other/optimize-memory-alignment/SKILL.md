---
name: optimize-memory-alignment
description: "Use when optimizing ECS component memory layouts for CPU cache alignment. Triggers: 'cache alignment', 'memory layout'."
---

# optimize-memory-alignment

## 1. Overview

Rearranges ECS component struct fields for optimal CPU cache alignment. Analyzes access patterns (Hot/Warm/Cold), applies data-oriented layout principles, and calculates precise byte offsets for cache-line efficiency. Output: `memory_layout.md` with optimized struct layouts and alignment recommendations per platform.

## 2. When to Use

- **Scenarios**: Optimizing ECS component memory layouts for cache efficiency, reducing cache misses in performance-critical systems, restructuring data-oriented designs for SoA (Structure of Arrays) layouts.
- **Triggers**: `cache alignment`, `struct padding`, `memory layout`, `data-oriented design`, `SoA`, `cache miss`, `memory optimization`, `ECS layout`.

## 3. Core Pattern

1. **Access Pattern Analysis**: For each component, identify field access frequency: **Hot** (every frame), **Warm** (periodic), or **Cold** (rare/on-demand).
2. **Cache Line Boundary Definition**: Define target platform cache line size (e.g., 64 bytes for x86_64/ARM64) to guide alignment rules.
3. **Layout Rule Application**: Apply data-oriented principles: Group high-frequency fields in the first block (**Hot-First**), isolate cold fields (**Frequency Separation**), pad blocks to match cache lines (**Alignment & Padding**), and group same-type fields (**Type Packing**).
4. **Layout Calculation**: Calculate precise byte offsets for every field across all defined memory blocks.
5. **Specification Export**: Write the finalized, validated layout into `{TARGET_FOLDER}/docs/memory_layout.md`. Requires input from `{TARGET_FOLDER}/docs/ecs_spec.md` to understand archetype structures.

## 4. Interaction Protocol

### Error Handling & Intercepts

- **[High-Frequency Violation]**: If hot fields are spread across multiple cache lines: *"I notice your 'Hot' fields span more than one cache line. This will cause unnecessary cache misses. Should we rearrange the layout to consolidate them?"*
- **[Cache Waste]**: If a block has excessive padding (e.g., >50% empty): *"The current layout for [Component] results in significant cache waste. Should we attempt to pack more 'Warm' fields into this block?"*

## 5. Red Flags

- **Consolidated Hot Fields**: Keep high-frequency ("Hot") fields within single cache lines.
- **Efficient Packing**: Minimize empty space in memory blocks (e.g., <50% waste).
- **Pure Data Components**: Include only POD (Plain Old Data) types within component structures.
- **Frequency-Based Layout**: Group hot and cold data in separate memory blocks to avoid cache pollution.
- **Platform-Aligned Offsets**: Match field offsets to target platform alignment requirements (x86_64, ARM64).
