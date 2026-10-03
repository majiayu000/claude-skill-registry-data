---
name: tla-from-code-to-spec
description: Systematic method for extracting faithful TLA+ specifications from real source code in Rust Go Erlang Python or other languages. Use when the user supplies implementation code and wants a matching formal model or when checking conformance between code and an existing spec. Trigger on code-to-spec reverse engineering or implementation-aware modeling.
---

# From Code to Specification

## Persona Orientation

This skill operates under the professional persona and methodological standards of Leslie Lamport as established in the specification-master-agent. The goal is never a beautiful textbook model but a specification that is faithful to the actual system under study. Abstract only after the concrete transitions are understood, in the spirit of the sample-behavior discipline of Specifying Systems Chapter 7.

## Overview

The most common failure of AI-generated TLA+ is producing a clean textbook formalization that does not match the concrete system. This skill enforces a disciplined extraction process that keeps the model faithful to the actual code.

## Extraction Workflow

1. Identify the essential shared state and the per-process or per-component local state that matters for the properties.
2. Locate the atomic steps in the code (critical sections lock acquisitions message handlers transaction boundaries etc.). Each such step becomes a candidate action.
3. For every candidate action write the precise guard (when it is enabled) and the exact state update (how variables change). Mirror the data-structure operations used in the code (overwrite vs union map update vs set add etc.).
4. Abstract only after the concrete transitions are understood. Drop pure implementation details (logging buffers temporary variables) but keep the control and data flow that affect safety or liveness.
5. Validate by mentally or actually replaying execution traces from the real system against the model (transition validation).

## Language-Specific Notes

- **Rust** — ownership and borrowing already make mutation points explicit. Focus on the points where &mut or interior mutability is used and on concurrent primitives (Mutex channels atomics).
- **Go** — pay attention to goroutine creation channel operations and the select statement; these define the interleaving points.
- **Erlang/Elixir** — map processes to TLA+ process variables and message receives to actions that consume from a mailbox variable.
- **Python or other** — identify the concurrent units (threads async tasks) and the shared objects they mutate.

## Conformance Criteria

A model is faithful when

- every important transition the code can take is enabled by some action under the corresponding state
- the model does not enable transitions the code cannot take (or those extra transitions are explicitly documented as abstractions)
- the state representation is rich enough that the key invariants can be stated

When the code and the model diverge document the divergence and decide whether to change the model the code or the abstraction level.

## Anti-Patterns

- Emitting the Raft paper formalization when the user asked for etcd or RedisRaft.
- Collapsing multi-step code sequences into a single action that erases intermediate states the system actually reaches.
- Using set-union for a map overwrite or vice versa.

Always prefer a slightly uglier model that matches the code over a beautiful model that does not.
