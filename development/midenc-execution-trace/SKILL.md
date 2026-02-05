---
name: midenc-execution-trace
description: |
  Use when working on the Miden compiler (`midenc` / `cargo miden`), debugging failing tests or implementing compiler changes, and you need a Miden VM MASM execution trace to understand the stack state after each instruction. Covers `MIDENC_TRACE=executor=trace` (typically with `cargo make test -- --no-capture ...`).
---

# MIDENC Trace (MASM execution trace)

## Quick start

- Run a single Rust test with MASM execution tracing enabled:
  - `MIDENC_TRACE=executor=trace cargo make test --no-capture <test_name_or_filter>`
- If you only care about traces on failures (and want faster parallel execution), omit `--no-capture`:
  - `MIDENC_TRACE=executor=trace cargo make test <test_name_or_filter>`
- If you want parallel execution but still want output on passing tests, prefer `--success-output`:
  - `MIDENC_TRACE=executor=trace cargo make test --success-output immediate <test_name_or_filter>`

## What `MIDENC_TRACE=executor=trace` gives you

- A step-by-step trace of MASM execution from the VM executor.
- For each executed instruction/op, it prints the current stack state (practically: the quickest way to answer “what was on the stack right after this instruction?”).

## Recommended workflow for debugging compiler changes

1. Reproduce the issue on the smallest possible test (or add a focused test).
2. Run with live output so you can see the trace stream as the test executes:
   - `MIDENC_TRACE=executor=trace cargo make test --no-capture <test_name_or_filter>`
3. Compare the trace against the expected stack discipline for the procedure(s) you’re debugging:
   - When you see a mismatch, jump to the corresponding emitted MASM (pair with the `emit` skill if you also need `MIDENC_EMIT=masm=...`).

## Practical tips

- Prefer a single test when tracing: `executor=trace` is extremely verbose and slows runs down.
- If you’re running via `cargo nextest` directly, the equivalent “live output” flag is `--no-capture`:
  - `MIDENC_TRACE=executor=trace cargo nextest run --no-capture <filter>`
