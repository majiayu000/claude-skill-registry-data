---
name: react-performance-optimizations
description: Techniques for Virtualization, Memoization, and RSC logic. Use when optimizing a sluggish React app or refactoring to server components.
version: "2.0.0"
verified_date: 2026-04-29
category: core
---

# React Performance Optimizations (Redesigned)

## Purpose
Enforce strict performance standards for React and Next.js applications through architectural state minimization rather than blind memoization.

## Hard Usage Rules (Tier 3: Unsafe without Diagnostics)
- **ALLOWED**: ONLY when the user explicitly provides a React Profiler trace or identifies a specific render loop.
- **FORBIDDEN**: General usage or preemptive "optimization" passes on working code.
- **CONSTRAINT**: **ABORT** execution if invoked without profiling data or explicit render loop identification.

## New Execution Strategy (Measure-First)
1. **Refuse Optimization**: Do not write `useMemo` or `useCallback` unless diagnostics are provided.
2. **Component Splitting First**: Push state down to the lowest possible leaf node. If a state update does not affect the parent, it must be moved out of the parent.
3. **Memoization as Last Resort**: If memoization is absolutely forced, run a strict static analysis pass over the dependency array before outputting.

## Safety Guardrails & Patched Prevention
- **Stale Closure Patch**: Never use `useCallback` without verifying that all referenced variables inside the closure are included in the dependency array. If tracing scope is impossible due to missing context, do not memoize.
- **Self-Rejection Clause**: If state can be pushed down to a child component, **DO NOT** use `useMemo`. If dependency correctness cannot be guaranteed, **ABORT OUTPUT**.

## When to Use This Skill
Use when optimizing a sluggish React app or refactoring to server components, specifically when you have diagnostics or profiling data.

## Phase 1: Optimization and State Splitting
1. Refuse optimization without diagnostics.
2. Push state down to the lowest possible leaf node. If a state update does not affect the parent, it must be moved out of the parent.
3. If memoization is forced, run static analysis on dependencies.

## Behavior Rules
1. **Measure First**: Always rely on profiling data before applying any optimization logic.
2. **Component Splitting First**: Prefer structural changes (component isolation) over hook-based caching (`useMemo`/`useCallback`).
3. **No Premature Optimization**: Do not memoize anything "just in case".

## Output Format / Delivery
- The output should be a targeted, structurally refactored component block.

## Maintenance Notes
- Complete redesign from v1 to v2. Abandoned blind memoization strategy in favor of Component Splitting and Measure-First execution.
