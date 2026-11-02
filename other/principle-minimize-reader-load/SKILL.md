---
name: principle-minimize-reader-load
description: Apply when reviewing or shaping code that is hard to trace.
disable-model-invocation: true
---

# Minimize reader load

Code is as maintainable as it is cheap to follow.

- Judge maintainability by the layers a reader must trace and the state they
  must hold in mind, not by line counts, complexity scores or architecture
  labels.
- Before adding a layer or a piece of state, check that it removes at least
  as much reader load elsewhere as it adds.
- Inline layers that cost more than they save: a wrapper with one caller, an
  adapter with no second implementation, indirection for a need that has not
  arrived. An adapter that hides real complexity can pass this cost test.
- Give state the narrowest scope that works: a local over a field, a field
  over module state, module state over a global.
- Derive a value from its source when it is needed instead of storing a copy
  that must be kept in sync.
- Name each invariant once, at the boundary that owns it, not in every
  consumer.
