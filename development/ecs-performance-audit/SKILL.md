---
name: ecs-performance-audit
description: Analyze Entity Component System implementations for performance bottlenecks including entity iteration efficiency, system priority ordering, memory allocation patterns in hot paths (OnUpdate, rendering loops), cache coherency, LINQ allocations, and boxing issues. Use when reviewing ECS code for optimization, debugging slow entity updates, or investigating frame rate drops.
---

# ECS Performance Audit

## Overview
This skill performs comprehensive performance analysis of Entity Component System implementations in the C#/.NET 10.0 game engine. It identifies bottlenecks, memory allocation issues, and cache coherency problems that impact frame time.

## When to Use
Invoke this skill when encountering:
- Frame rate drops related to entity processing
- Slow iteration over large entity collections
- Questions about system execution order optimization
- Memory allocation concerns in hot paths (OnUpdate, rendering)
- Cache coherency issues with component layouts
- Performance regressions after ECS changes
- System initialization or update performance issues

## Analysis Process

### 1. System Iteration Patterns
- Identify systems iterating without proper component filtering
- Check for O(n²) algorithms in entity loops
- Verify LINQ usage doesn't cause unnecessary allocations - always prefer zlinq library
- Look for `GetEntitiesWith<T>()` calls in hot paths
- Check for unnecessary component lookups (cache component references when possible)

### 2. Priority & Ordering
- Validate system execution order via `SceneSystemRegistry` and `SystemManager`
- Check for implicit update order dependencies
- Verify priority values align with execution requirements:
  - ScriptUpdateSystem: Priority 100
  - AnimationSystem: Priority 198
  - TileMapRenderSystem: Priority 200
  - SpriteRenderingSystem, ModelRenderingSystem: Default
- Suggest priority adjustments for better parallelization potential

### 3. Memory Allocation
- Flag allocations in `OnUpdate()`, `Render()`, `OnEvent()` loops
- Identify boxing, LINQ materializations (`.ToList()`, `.ToArray()`)
- Check for closure captures creating heap allocations
- Look for string concatenation in hot paths
- Identify lambda allocations in frequent operations
- Recommend object pooling strategies for frequently created objects
- Suggest `Span<T>` and `stackalloc` and Memory<T> where appropriate

### 4. Data Locality & Cache Coherency
- Evaluate component data layout (prefer value types when small)
- Check for Structure of Arrays vs Array of Structures opportunities
- Suggest cache-friendly component packing

### 5. Reflection & Dynamic Dispatch
- Flag reflection usage in hot paths (use static caching like `ScriptableEntity`)
- Check for virtual method calls that could be devirtualized
- Identify dictionary lookups that could use faster alternatives
- Verify factory pattern usage for appropriate caching

### 6. Profiling Recommendations
- Suggest specific `dotnet-trace` or profiler commands
- Recommend benchmark scenarios for validation
- Provide before/after measurement guidance
- Reference `Benchmark` project and `docs/specifications/physics-benchmark-design.md`

## Output Format
Provide findings in this structure:

**Issue**: [Clear description of the problem]
**Impact**: [Performance cost - frame budget impact, allocation rate, cache misses]
**Location**: [File path with line numbers, e.g., `Engine/Scene/Systems/MySystem.cs:42`]
**Recommendation**: [Specific optimization with code example]
**Priority**: [Critical/High/Medium/Low based on frame time impact]

### Example Output
```text
**Issue**: LINQ materialization in OnUpdate() loop
**Impact**: ~5,000 allocations per frame (60fps = 300k/sec), causing GC pressure
**Location**: Engine/Scene/Systems/RenderingSystem.cs:156
**Recommendation**: Replace `.ToList()` with direct iteration:
// Before
foreach (var entity in scene.GetEntitiesWith<SpriteRendererComponent>().ToList())

// After
foreach (var entity in scene.GetEntitiesWith<SpriteRendererComponent>())

**Priority**: High
```
