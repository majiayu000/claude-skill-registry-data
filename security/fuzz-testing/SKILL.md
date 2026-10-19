---
name: fuzz-testing
description: >
  Design coverage-guided fuzzing campaigns: choose a fuzz target, write a deterministic harness
  (libFuzzer/cargo-fuzz, Atheris for Python, AFL++), seed and minimize a corpus, add dictionaries
  and sanitizers, triage and minimize crashes, and run short fuzz regressions in CI. Use when code
  parses untrusted or complex bytes (file formats, protocols, decompressors, deserializers,
  regex/URL/JSON/XML handling), or native extensions that must not crash or corrupt memory. Use
  only on code and systems you own or are authorized to test. Do NOT use for input-space
  property checks with typed values (property-based-testing), for judging test strength
  (mutation-testing), or for black-box attacks on live services.
compatibility: >
  Agent Skills-compatible coding agents. Rust cargo-fuzz (needs a nightly toolchain), C/C++
  libFuzzer/AFL++ (Clang), Python Atheris (README lists CPython 3.11 to 3.14, Linux/macOS).
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "fuzzing, libfuzzer, cargo-fuzz, afl, atheris, corpus, sanitizers, crash-triage"
  topics: "software-development, testing, security"
---

# Fuzz Testing

Coverage-guided fuzzing mutates inputs, keeps the ones that reach new code, and watches for crashes, sanitizer reports, hangs, and failed assertions. Quality depends on three things you control: the harness (what is called, with what, how deterministically), the corpus (where the search starts), and the oracle (what counts as a bug).

Boundaries: sanitizer selection, combinations and report interpretation are [memory-sanitizers](../memory-sanitizers/SKILL.md); typed-value properties with shrinking are [property-based-testing](../property-based-testing/SKILL.md); to prove tests catch seeded faults see [mutation-testing](../mutation-testing/SKILL.md); reviewing code for vulnerability classes is `security-code-review`; profiling slow inputs is `performance-profiling`.

## Non-negotiable rules

1. Authorization first. Fuzz only your own code or targets the owner has authorized. Run harnesses locally or in CI against in-process functions; never fuzz someone else's production service.
2. Fuzz in-process, offline, in a scratch directory. The harness must not touch the network, real credentials, user files, or production databases; it must not spawn shells with fuzz-controlled strings. Seeds must not contain secrets or real customer data (corpora get committed and shared).
3. Crashing inputs are potentially sensitive (they can encode exploit conditions). Store them under controlled access, report through the project's security process if the target is a library others use, and do not publish exploit write-ups from this skill's workflow.
4. Do not "fix" a finding by catching and swallowing the crash in the harness. Fix the code or document an explicit, narrow expected-error contract.
5. A fuzz run with no findings is not a proof; report coverage reached, run time, and corpus size, not "secure".
6. Never commit multi-GB corpora or `artifacts/` blindly; commit a small minimized seed corpus and the regression inputs.

## Workflow

### 1. Choose the target (decision points)

Good targets: pure-ish functions from bytes (or structured input) to result, with complex branching: parsers, decoders, deserializers, state machines fed event streams, normalizers. Poor targets: functions dominated by IO, global state, or threads. Wrap such code behind a function that takes an in-memory buffer. If the entry point takes a struct, derive structure from bytes (see step 3).

Pick the engine:

| Situation | Engine |
|---|---|
| Rust crate | cargo-fuzz (libFuzzer) |
| C/C++ library already building with Clang | libFuzzer (`-fsanitize=fuzzer`), or AFL++ with `afl-clang-fast` |
| Need many cores/long campaigns, file or stdin targets | AFL++ (`-M`/`-S` parallel instances) |
| Pure Python | Atheris |
| Python with native extensions | Atheris plus instrumented/sanitized extension (read Atheris native-extension guide) |
| Go | built-in `go test -fuzz` (not covered here; see Go docs) |

### 2. Write the harness

Rules for a good harness: deterministic (same bytes, same behavior), fast (aim for thousands of execs/s; thin out setup per call), no leaking state between calls, bounded memory, no randomness or clock dependence, no `exit()` on bad input.

Rust (cargo-fuzz):

```rust
// fuzz/fuzz_targets/parse_header.rs
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    if let Ok(s) = std::str::from_utf8(data) {
        let _ = mycrate::parse_header(s);   // oracle: must not panic
    }
});
```

Commands (from the rust-fuzz book): `cargo fuzz init`, `cargo fuzz list`, `cargo fuzz run <target>`. Crashes are written under `fuzz/artifacts/<target>/`. Extra libFuzzer flags go after `--`, e.g. `cargo fuzz run parse_header -- -max_total_time=60`.

Python (Atheris):

```python
import sys, atheris

with atheris.instrument_imports():
    import mylib

def test_one_input(data: bytes):
    fdp = atheris.FuzzedDataProvider(data)
    text = fdp.ConsumeUnicodeNoSurrogates(256)
    try:
        mylib.parse(text)
    except mylib.ParseError:      # documented, expected error only
        pass

atheris.Setup(sys.argv, test_one_input)
atheris.Fuzz()
```

Only catch exceptions the API documents. Any other exception is a finding.

C/C++ libFuzzer: define `extern "C" int LLVMFuzzerTestOneInput(const uint8_t *data, size_t size)`; build with `-fsanitize=fuzzer,address` (add `undefined` for UBSan); run `./fuzzer corpus/ -max_len=4096 -timeout=5`. Common libFuzzer flags: `-max_len`, `-runs`, `-max_total_time`, `-timeout`, `-rss_limit_mb`, `-dict`, `-artifact_prefix`, `-merge=1`.

AFL++ (from the fuzzing-in-depth guide): build with `afl-clang-fast`/`afl-cc` (or `CC=afl-clang-fast CXX=afl-clang-fast++ ./configure --disable-shared`), optionally `AFL_USE_ASAN=1`, then `afl-fuzz -i seeds -o out -- ./target @@` (`@@` becomes the input path; omit it for stdin targets). Run `afl-system-config` as root once after boot if you can, else `AFL_SKIP_CPUFREQ=1`. Parallel: one `-M main` and several `-S name` sharing the same `-o`.

### 3. Structure-aware input (when raw bytes die early)

If a checksum, length field, or magic header rejects 99% of mutations, fuzz *after* that layer: call the inner parser, or generate a struct. In cargo-fuzz derive `Arbitrary` (the `arbitrary` crate with the `derive` feature) and accept the type in the target: `fuzz_target!(|input: MyInput| { ... })`. In Atheris use `FuzzedDataProvider` to carve typed fields. Alternative for checksums: recompute the checksum inside the harness before calling the parser (only in the harness, never in production code).

### 4. Seed corpus and dictionary

- Start with 10 to 100 small valid inputs covering each feature (real format samples you are allowed to use, or hand-made). Prefer small files; mutators work better on small seeds.
- Add a dictionary of tokens (keywords, magic bytes, delimiters) via libFuzzer `-dict=file` or AFL++ `-x file` when the grammar is token-rich.
- Minimize periodically: libFuzzer `-merge=1 new_corpus/ old_corpus/` merges and keeps only coverage-contributing inputs; `cargo fuzz cmin <target>` and `cargo fuzz tmin <target> <crash>` exist for corpus and input minimization (check `cargo fuzz --help` on your version); AFL++ has `afl-cmin` and `afl-tmin`.
- Commit the minimized seed corpus under version control; keep the working (growing) corpus in CI cache or artifact storage.

### 5. Sanitizers and oracles

Decide the bug oracle explicitly:
- Memory safety (C/C++): AddressSanitizer, UBSan, optionally MSan (needs fully instrumented deps). Which sanitizers can be combined and how to read their reports is in [memory-sanitizers](../memory-sanitizers/SKILL.md); this skill only needs them switched on in the fuzz build.
- Rust: panics, arithmetic overflow in debug-style builds, and `unsafe` code under ASan; `assert!` for logic invariants.
- Differential: compare two implementations (`parse_a(x)` vs `parse_b(x)`); mismatch is the finding.
- Round trip: `parse(print(parse(x))) == parse(x)`. This is where fuzzing overlaps property-based testing, with coverage guidance replacing random generation.
- Resource: timeouts (`-timeout`) and RSS limit expose algorithmic complexity bugs; treat them as findings, not noise.

### 6. Run, then triage

1. Smoke: run 30 to 60 s locally. If `exec/s` is under a few hundred or coverage stalls instantly, fix the harness (see anti-patterns) before burning CPU.
2. Campaign: longer (hours) on a dedicated machine or scheduled CI job; use multiple instances for AFL++.
3. For each crash: reproduce by running the target on the single artifact file; minimize it; classify (memory error, panic, assert, OOM, timeout); find root cause; dedupe by stack trace; write a regression test.
4. Fix, then copy the minimized crashing input into a regression directory that CI always replays.

### 7. CI strategy

- On every PR: replay the committed corpus and regression inputs only, with `-runs=0` (libFuzzer: executes corpus files and exits) or a short time-boxed run. Fails fast on regressions, costs seconds.
- Nightly/weekly: time-boxed discovery run (e.g. `-max_total_time=1800`), upload `artifacts/` and the grown corpus; open an issue for new crashes.
- For open-source projects with a build that suits it, continuous fuzzing services exist (e.g. OSS-Fuzz); check their current eligibility and onboarding requirements before depending on one.

## Worked example: Rust header parser

1. `cargo fuzz init`; edit the generated target as above to call `parse_header`.
2. Put 20 small valid headers in `fuzz/corpus/parse_header/`.
3. `cargo fuzz run parse_header -- -max_total_time=60`: finds a panic on index `data[len]` when the declared length equals the buffer length.
4. Minimize: `cargo fuzz tmin parse_header fuzz/artifacts/parse_header/crash-...`.
5. Fix off-by-one, add the minimized bytes as a unit test fixture, keep the corpus. Add CI step replaying the corpus.

(Illustrative workflow; the numbers are an example, not a recorded run.)

## Anti-patterns

- Harness reads files/env or uses `rand`/time; coverage and reproducibility die.
- Huge `-max_len` with slow targets; keep inputs as small as the format allows.
- Swallowing all exceptions or all `Result`s so nothing is ever a "bug".
- One giant seed file; no dictionary for a token-heavy grammar.
- Fuzzing the whole application via CLI when an in-process function exists.
- Ignoring sanitizer "leak" or "timeout" reports as noise without checking.
- Treating equal exec counts as progress; look at coverage growth (`cov:` and `ft:` in libFuzzer output, or `cargo fuzz coverage`).
- Running fuzzers as root on shared machines, or with network access.

## Verification checklist

- [ ] Target authorized and harness fully in-process, offline, deterministic
- [ ] Oracle stated (what counts as a bug) and expected errors narrowly caught
- [ ] Seed corpus small, free of secrets, minimized; dictionary added if grammar is token-based
- [ ] Sanitizers on for native code; exec/s and coverage growth recorded
- [ ] Each crash reproduced, minimized, root-caused, covered by a regression input
- [ ] CI replays corpus on PRs; long runs scheduled separately

## References

- [Troubleshooting: low coverage, slow, flaky crashes](references/troubleshooting.md)
- [Scenarios for evaluating this skill](references/scenarios.md)
- [Sources and provenance](references/sources.md)
