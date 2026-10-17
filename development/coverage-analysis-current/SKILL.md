---
name: coverage-analysis-current
description: Collect, validate and compare source coverage for native fuzz targets and regression corpora. Use for corpus replay, LLVM profile merging and JSON or lcov export, identifying untested branches, or checking whether a coverage comparison is complete and reproducible.
license: CC-BY-SA-4.0
metadata:
  status: experimental-unbenchmarked
---

# Complete, comparable coverage

Define the program/harness revision, relevant modules, instrumentation, build
flags, target reset rules, corpus and comparison question first. Use external
behavioral contracts to define correctness; executing a region is not proof that
its assertions are strong or its behavior is correct. Keep bug discovery,
throughput and coding-agent efficacy distinct from coverage.

Verify stable toolchain artifacts and matching compiler/profile/coverage tools.
Linux x64 LLVM 23.1.3 known-input/profile controls were qualified on 2026-10-07.
GCC needs the matching gcov tool and supported gcovr; `llvm-cov gcov` is not a
universal replacement. Qualify project policy ranges and actual CMake versions.
Do not apply LLVM development documentation as a stable-format guarantee.

For LLVM source-based coverage, compile target and driver with
`-fprofile-instr-generate -fcoverage-mapping`, retaining their actual optimization
and sanitizer settings. Source mappings precede optimization, so O3 alone does
not invalidate them. Source or scope changes can alter denominators; freeze them
or identify those changes explicitly before comparing percentages.

Enumerate an explicit bounded corpus manifest with hashes, including empty,
invalid and crash inputs when relevant. Sort it deterministically. Distinguish
selected, attempted, completed, rejected, crashed, timed-out and excluded cases.
Report every exclusion and collection failure. Do not declare completeness if
missing files, permissions, input bounds, allocation, target state or profile
collection prevented a selected case from being measured.

Replay each selected file in a bounded child process when crash isolation or
state reset requires it. Check exit status and capture bounded diagnostics.
Use an owned, stable, read-only staged corpus to avoid changing inputs during
collection. [The supplied driver](scripts/replay.cc) handles one regular file,
including empty data, with a fixed 1 MiB qualification bound and fail-closed read
errors. It requires C++17, the existing target entrypoint and external per-input
process/time/resource limits. Set a domain-appropriate bound before another
experiment and record the compiled driver hash. It is not a sandbox.

Give every process a qualified unique raw profile path, for example
`LLVM_PROFILE_FILE=/owned/profiles/case-%p.profraw`; preserve process/case mapping.
Crash exits may not flush profiles. Qualify platform-specific crash collection
instead of silently dropping crashes or inferring coverage from an exit code.
Confirm raw profiles are present, nonempty and compatible with the exact binary.

Merge the explicitly enumerated matching inputs with
`llvm-profdata merge -sparse <profiles...> -o coverage.profdata`. Treat any missing,
invalid or incompatible profile as incomplete. Export with both binary and
profile: `llvm-cov export ./target -instr-profile=coverage.profdata -format=text`
produces JSON; `-format=lcov` produces lcov. Verify the format and parser, and
retain exact inputs. HTML reports likewise need the binary/profile and a bounded
owned output directory. Do not hide collector errors to produce a report.

Export each comparison condition separately, then align file, region or branch
identities and denominators. Repeating `-instr-profile` does not produce a diff.
Report reached counts, total counts and added/lost relevant regions. Explain
scope exclusions rather than relying on broad substring filters. Preserve raw
reports and independent known-input checks that distinguish plausible wrong
results, including a truncated or missing collection.

Iterate on target reach, seeds, dictionaries and reset behavior using development
tasks. Keep holdouts and their expectations sealed until the frozen final
evaluation. Coverage plateaus need diagnosis; longer runtime alone is not a
guarantee. Show measured outcomes, cost and uncertainty before recommending a
skill or claiming improvement.

See [qualification limits](references/qualification.md); the original source and
license are included. This overlay remains unbenchmarked for coding-agent efficacy.
