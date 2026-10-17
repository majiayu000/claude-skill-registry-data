---
name: ruzzy-fuzzing-current
description: Prepare coverage-guided Ruby fuzzing with Ruzzy, define exception and sanitizer scope, and qualify tracing, crash replay and native builds. Use for Ruby parsers, API error contracts and C extensions; do not infer complete safety from a toy crash or suppressed exceptions.
license: CC-BY-SA-4.0
metadata:
  status: experimental-unbenchmarked
---

# Ruby fuzzing with Ruzzy

Define accepted input types, documented rejection exceptions and independent
semantic/memory-safety outcomes before building the harness. Select a fuzzer by
target and platform evidence; avoid unsupported ecosystem-superiority claims.

Verify current stable releases, supported platforms and the full native build
graph. Ruzzy 0.8.0 is the observed stable RubyGems release on 2026-10-02. Current
tool documentation includes Linux x86-64/ARM64 and Apple Silicon macOS; a platform
statement is not a successful installation. Pin the gem digest, Ruby/compiler/
sanitizer versions and environment. Keep tool AGPL licensing distinct from this
instruction overlay's CC-BY-SA licensing. Actual Ruzzy execution is unqualified
here; qualify the selected release rather than promising development-HEAD APIs.

For pure Ruby, use the release's tracer around the harness and verify target
branch coverage. For native extensions, build the target with compatible
instrumentation/sanitizers, inspect target symbols and verify runtime startup
with a known instrumented defect. Compiler flags and a toy crash alone do not
prove target coverage. Reset mutable state; keep the harness deterministic.

Catch the target's documented malformed-input exceptions only. `StandardError`
also catches many programming defects; `Exception` additionally catches control
exceptions such as `Interrupt` and `SystemExit`. A deliberately native-only
campaign may exclude language exceptions, but must report that scope and retain
independent semantic/error-contract tests. Do not turn unexpected failures into
successful inputs.

Set sanitizer injection for the single target command, not globally. Check the
actual release's `ASAN_PATH`/`UBSAN_PATH`. On macOS, qualify a non-system Ruby,
LLVM with libFuzzer, appropriate bundle linker flags and `DYLD_INSERT_LIBRARIES`;
SIP-protected shims can remove injection variables. Do not reuse Linux preload
instructions unchanged. Verify initialization and target detection explicitly.

Document interpreter leak accommodations and all excluded vulnerability classes.
Resource exhaustion can be a consequential denial of service; evaluate it under
the target's resource/service contract rather than dismissing allocation failure.
Run in an owned isolated disposable environment with bounded time, input size,
memory, processes, output and artifacts. Keep networking disabled unless required.

Use a versioned corpus appropriate to the target, preserving malformed cases
as well as valid structured inputs. Typed providers need fixed consumption order
and bounded fields; exhausted input can exercise repeated defaults. Qualify every
API against the selected stable gem. Record target/seed/corpus hashes, exact
commands, versions, resources, exclusions, raw outputs and cleanup. Replay and
minimize failures; known-seed replay is not evidence of independent discovery.

Report instrumented executions, meaningful target coverage, semantic findings
and native sanitizer findings separately. Preserve inconclusive and setup-failure
outcomes. Throughput, a clean bounded run or unavailable evidence does not imply
absence of vulnerabilities or superior coding-agent behavior.

Source contracts: [stable gem](https://rubygems.org/gems/ruzzy/versions/0.8.0),
[pinned tool README](https://github.com/trailofbits/ruzzy/blob/44bf09245e2612c8a97fee1be5573f8b2244784e/README.md).
Original provenance and license accompany this experimental overlay.
