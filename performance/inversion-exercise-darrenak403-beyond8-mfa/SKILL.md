---
name: Inversion Exercise
description: Flip core assumptions to reveal hidden constraints and alternative approaches - "what if the opposite were true?"
when_to_use: when stuck on unquestioned assumptions or feeling forced into "the only way" to do something
version: 1.1.0
---

# Inversion Exercise

## Overview

Flip every assumption and see what still works. Sometimes the opposite reveals the truth.

**Core principle:** Inversion exposes hidden assumptions and alternative approaches.

## Quick Reference

| Normal Assumption | Inverted | What It Reveals |
|-------------------|----------|-----------------|
| Cache to reduce latency | Add latency to enable caching | Debouncing patterns |
| Pull data when needed | Push data before needed | Prefetching, eager loading |
| Handle errors when they occur | Make errors impossible | Type systems, contracts |
| Build features users want | Remove features users don't need | Simplicity > addition |
| Optimize for common case | Optimize for worst case | Resilience patterns |
| Centralize configuration | Distribute configuration | Feature flags, per-tenant config |
| Synchronous request → response | Async command → event | Event-driven architecture |

## Process

1. **List core assumptions** — What "must" be true?
2. **Invert each systematically** — "What if the opposite were true?"
3. **Explore implications** — What would we do differently?
4. **Find valid inversions** — Which actually work somewhere?

## Example

**Problem:** Users complain the app is slow

**Normal approach:** Make everything faster (caching, optimization, CDN)

**Inverted:** Make things intentionally slower in some places
- Debounce search input (add latency → enable better results, fewer DB hits)
- Rate limit requests (add friction → prevent abuse, smooth load)
- Lazy load content (delay → reduce initial load time)

**Insight:** Strategic slowness can improve UX and system health

## Red Flags You Need This

- "There's only one way to do this"
- Forcing a solution that feels wrong
- Can't articulate why the approach is necessary
- "This is just how it's done"
- Every solution feels like fighting the problem

## Remember

- Not all inversions work — test boundaries
- Valid inversions reveal context-dependence
- Sometimes the opposite is the answer
- Question every "must be" or "always" statement
