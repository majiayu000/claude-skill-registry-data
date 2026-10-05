---
name: principle-outcome-oriented-execution
description: "Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code."
disable-model-invocation: true
---

> **On this platform.** This is pstack's `principle-outcome-oriented-execution` skill (MIT, Lauren Tan; the unmodified source is in `vendor/pstack`). Read [the platform map](../../docs/pstack-platform.md) (installed: `~/.local/share/dev-platform/current/docs/pstack-platform.md`) once per session: it says what the Cursor tools named here are on this machine, and which steps the guard hook leaves to the owner.

# Outcome-Oriented Execution

Optimize for the intended, verifiable end state rather than preserving smooth intermediate states.

**Why:** Keeping every intermediate step fully stable often creates temporary compatibility code that becomes long-lived debt. Converge on the target architecture and prove correctness at explicit verification boundaries.

**Core rule:**
- Prioritize end-state integrity over transitional stability
- Intermediate breakage is acceptable when it is planned, scoped, and reversible

**Guardrails:**
- Use this for planned rewrites and migrations with explicit phase boundaries
- Declare where temporary breakage is acceptable
- Keep high-signal checks for actively touched areas while migrating
- Require full static and runtime verification at plan completion
