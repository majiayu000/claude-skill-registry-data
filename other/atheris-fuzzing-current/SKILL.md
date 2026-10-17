---
name: atheris-fuzzing-current
description: Build and qualify bounded coverage-guided Python fuzzing harnesses with Atheris. Use for parser or API fuzzing, structured inputs, crash replay and native extension campaign setup; preserve byte domains, target instrumentation and explicit sanitizer scope.
license: CC-BY-SA-4.0
metadata:
  status: experimental-unbenchmarked
---

# Atheris fuzzing

Define the target contract first: accepted bytes/text/typed inputs, documented
rejections, invariants and independently specified wrong outcomes. Keep crash
replay, coverage, semantic correctness and native memory-safety results separate.

Verify the latest stable release and platform artifacts before installation.
As qualified on 2026-10-02, Atheris 3.1.0 has Linux x86-64 wheels for Python
3.12–3.14; its README also advertises source support for 3.11. Only Linux/Python
3.14.8 pure-Python execution was qualified here. Pin dependency digests and the
execution image; verify `importlib.metadata.version("atheris")`. A newer source
HEAD or supported-version statement is not proof of a matching release wheel.

Instrument the actual Python target before importing it; instrument the wrapper
when needed for initial coverage. Verify that executions reach target branches.
Catch only its documented input-rejection exceptions. Preserve unexpected
exceptions. Include empty and malformed inputs when the contract requires them.
Keep harness state deterministic and reset mutable state between inputs.

Pass bytes directly when the API accepts bytes. For text APIs, decode according
to the specified encoding/error policy; do not silently drop invalid bytes unless
that normalization is explicitly the target. An HTTPResponse supplied with body
bytes tests body reading, not HTTP message parsing. Choose the actual wire parser
when status, headers, framing or request syntax is in scope.

For typed targets, use `FuzzedDataProvider` with bounded fields in a fixed order.
Treat its schema as part of corpus provenance. Exhausted input yields defaults;
measure meaningful target coverage, valid-domain reach and input diversity.
Require a minimum length only when the independently specified target requires it.

Run in an owned disposable environment with explicit wall-clock, per-input,
memory, process, output, input-size and corpus/artifact bounds. Keep the target
offline unless networking is explicitly required and isolated. Start with a
qualified small corpus and a bounded run; `-atheris_runs=N` permits graceful
Python coverage export, whereas libFuzzer's `-runs=N` does not guarantee it.
Record exact versions, flags, source/corpus hashes, instrumentation, seed,
resources, raw outputs and cleanup. Reproduce and minimize failures before
classifying them; known-seed replay does not establish new bug discovery.

Native extensions need a separate qualification: a compatible Clang/libFuzzer/
sanitizer build, target instrumentation symbols, successful runtime startup and
an observed known instrumented defect. Locate installed preload libraries with
`atheris.path()` and verify the selected file, rather than hard-coding an
interpreter path or using the package's subdirectory. Do not preload globally.
Document interpreter accommodations and excluded leak/exception classes;
allocation denial of service is not universally low impact. Preserve independent
semantic/error tests alongside a narrowly scoped native campaign.

See [qualification boundaries](references/qualification.md). Original provenance
and attribution accompany this overlay. No coding-agent improvement is established.
