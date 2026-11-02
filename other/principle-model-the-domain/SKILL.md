---
name: principle-model-the-domain
description: Apply when writing stateful logic, a growing if/else chain, or a shape assumption repeated across files.
disable-model-invocation: true
---

# Model the domain

Choose the structure before the logic; the right structure removes logic.

- Settle the core types and data structures, traced against every access
  pattern, before writing the logic that uses them.
- Encode domain rules in a data structure that fits them (a state machine, a
  typed model, a lookup table, a union, a reducer) rather than in
  conditionals scattered through the code.
- Organise a module around one body of domain knowledge, not around an
  execution phase such as load, validate, transform or save.
- Each increment lands in or deepens one coherent abstraction; do not spread
  a new capability across callers as special-case coordination.
- Deduplicate structure (types, data models), but tolerate a few similar
  statements rather than a premature abstraction.
- Leave boring code boring when it is clear, local and unlikely to grow. Add
  indirection only when it removes branches, duplicated rules, invalid states
  or lifecycle risk; its reader-load cost is `principle-minimize-reader-load`'s
  test.
