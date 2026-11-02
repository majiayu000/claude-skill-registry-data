---
name: principle-separate-before-serializing-shared-state
description: Apply when concurrent actors (processes, agents, workers) in code or tooling you are designing might write the same file, branch, key or object.
disable-model-invocation: true
---

# Separate before serializing shared state

Remove the shared write before coordinating it. This lens is for code and
tooling design; it does not change how agent work is divided.

- Before actors share state, ask what a concurrent modification would do;
  isolate the state unless the answer is nothing.
- By default, give each concurrent writer its own write target (a file, key,
  branch or directory) and merge only where the results are read.
- Where one shared target is a real invariant, serialize access by structure
  (a lock, a sequential phase, a single writer, compare-and-swap), never by
  an instruction to take turns.
