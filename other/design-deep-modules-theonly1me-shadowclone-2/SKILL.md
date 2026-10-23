---
name: design-deep-modules
description: 'Use when designing or reshaping a module, or when callers coordinate too many steps. Also use it when the user says "this is hard to test", "callers know too much", or "simplify this interface". Puts related state and decisions behind a small interface that states what the caller wants. Tests then use that interface instead of the internal steps. Not for typing values at a boundary (use `typescript-type-safety`).'
metadata:
  shadowclone-category: architecture
  shadowclone-section: engineering
  shadowclone-applies-when: when designing or reshaping a module or subsystem
---
# Design Deep Modules

## Use when

Callers repeat the same sequence of calls, a layer only forwards arguments, or tests must reach through layers to see behavior. A deep module gives callers a lot of behavior through a small interface.

## Gates

1. Can each caller state its intent in one call, without knowing the internal order of steps?
2. Does one owner hold each piece of related state and each decision about it?
3. Does each new layer serve a real variation or isolation need, not only forwarding?
4. Do the tests use the public interface, and replace dependencies only at outside boundaries?
5. Are the invariants and the error behavior part of the interface contract?

## Process

1. Read the callers. List the state, the order of steps, and the rules that they coordinate.
2. Put that state and those decisions under one owner. Name an operation for what the caller wants.
3. If the boundary is not clear, compare two placements by caller effort, error handling, and test effort.
4. Move the internal order of steps behind the interface.
5. Remove each layer that only forwards calls.
6. Write tests against the new interface, then remove the knowledge that callers no longer need.

## Example

**Situation:** Three commands each read a config file, merge it with defaults, check a policy, and take a lock before they write.
**Easy route:** Add a helper for each of the four steps, and keep the order in each command.
**Hidden cost:** Each command still owns the order. A new command can skip the policy check, and each test must repeat the four steps.
**Best route:** Add one operation that takes the intended change and does the four steps inside. The commands call that operation.
**Evidence:** Each command became one call. A test through the new operation failed without the policy check, and the step tests in each command were no longer needed.

## Guardrails

- Use an options object when callers would otherwise pass related values in a fixed order.
- Return the outcomes that callers need, and keep side effects inside their owner.
- Do not add an abstraction without a concrete variation or isolation need.
- A short interface still costs effort if callers must call it in a hidden order.

## Completion

- The new interface: its exported names and one call example.
- The caller steps that the module now owns.
- The test command for the new interface, with its result line.
