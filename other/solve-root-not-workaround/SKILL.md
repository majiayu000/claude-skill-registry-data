---
name: solve-root-not-workaround
description: When tooling is broken, fix or find the canonical path rather than routing around it ad hoc; extend the module that owns the concern.
---

# Solve the root, not a workaround

An ad hoc bypass of broken tooling leaves the breakage in place for the next person and scatters the fix across call sites. The frustration of a broken tool is not time pressure; there is room to do it properly.

**Why:** workarounds accumulate into a second, undocumented system that no one owns.

**How to apply:** locate the component that owns the concern and fix it there, or ask for the canonical fixed tool. Prefer extending an existing owner over adding a parallel mechanism beside it.
