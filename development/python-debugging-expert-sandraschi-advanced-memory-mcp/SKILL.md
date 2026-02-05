---
name: python-debugging-expert
description: Master debugger for Python code with expertise in common errors, performance issues, and debugging tools
license: Proprietary
---

# Python Debugging Expert
> **Status**: ✅ Research complete
> **Last validated**: 2025-11-08
> **Confidence**: 🟡 Medium — Research-backed debugging playbook – review semi-annually

## How to use this skill
1. Begin with [modules/core-guidance.md](modules/core-guidance.md) to triage the issue and plan reproduction.
2. Use [modules/diagnostics-and-tooling.md](modules/diagnostics-and-tooling.md) to select appropriate debuggers and tracing tools.
3. Resolve concurrency issues via [modules/async-and-concurrency.md](modules/async-and-concurrency.md).
4. Address hotspots and leaks with [modules/performance-and-memory.md](modules/performance-and-memory.md).
5. Stabilize reproduction pipelines through [modules/testing-and-reproduction.md](modules/testing-and-reproduction.md).
6. Track follow-ups in [modules/known-gaps.md](modules/known-gaps.md) and revisit [modules/research-checklist.md](modules/research-checklist.md) every six months.

## Module overview
- [Core guidance](modules/core-guidance.md) — intake template, triage, communication.
- [Diagnostics & tooling](modules/diagnostics-and-tooling.md) — pdb, debugpy, logging, tracing, IDE features.
- [Async & concurrency](modules/async-and-concurrency.md) — asyncio debugging, race detection, multiprocessing.
- [Performance & memory](modules/performance-and-memory.md) — profiling CPU/memory, GC, leak detection.
- [Testing & reproduction](modules/testing-and-reproduction.md) — fixtures, property-based tests, CI automation.
- [Known gaps](modules/known-gaps.md) — future research.
- [Research checklist](modules/research-checklist.md) — validation cadence.

## Research status
- Updated for Python 3.13 debugging improvements, async task diagnostics, and modern tooling.
- Next review due 2026-05-01 or sooner if CPython introduces major debugging changes.
- Known gaps capture C extension debugging and distributed tracing coverage pending further work.
