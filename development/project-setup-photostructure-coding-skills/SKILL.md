---
name: project-setup
description: Setup and hardening review for cross-platform modern-C++ (C++17) native projects, especially Node.js addons built with node-gyp / node-addon-api. Use when asked to "set up a native addon", "harden a C/C++ build", "review my binding.gyp", "add compiler hardening flags", "wire up AddressSanitizer/UBSan/TSan/clang-tidy", "set up cross-platform CI / prebuilds for a native module", or "make this native code maintainable". Produces an applicability-aware baseline gap analysis (Met / Gap / Not applicable / Needs verification) across build config, per-OS/per-arch compiler hardening, sanitizer & static-analysis wiring, CI/prebuilds/supply-chain, and modern-C++ conventions — not exploit findings.
metadata:
  website: "https://photostructure.com/coding/"
---

# Native C/C++ Project Setup & Hardening

Assess a cross-platform modern-C++ (C++17) project — especially a Node.js native addon
built with node-gyp and node-addon-api — against a practical, evidence-based baseline for
build hardening, analysis tooling, portability, and maintainable code. Report applicable
preventive-control gaps even when no defect is currently proven, while clearly
distinguishing hardening advice from actual bugs.

Use the **OpenSSF Compiler Options Hardening Guide** as the compiler/linker backbone, the
**C++ Core Guidelines** for code conventions, **CERT C/C++** and the sanitizer/tool docs
for analysis, and official node-gyp / Node-API documentation for the addon toolchain. See
[ATTRIBUTION.md](./ATTRIBUTION.md).

## Boundary with resource review

Keep this skill separate from `resource-review`:

| This skill (`project-setup`)                          | The `resource-review` skill                   |
| ----------------------------------------------------- | --------------------------------------------- |
| Asks whether applicable controls meet a baseline      | Asks whether a memory/resource defect exists  |
| Reports evidence-backed best-practice gaps            | Reports only proven defects                   |
| Uses Met / Gap / Not applicable / Needs verification  | Uses Critical / High / Medium / Low           |
| Prioritizes Essential / Recommended / Optional        | Prioritizes impact and trigger reachability   |

A missing stack protector or an unset sanitizer job is a hardening Gap, not a
vulnerability. If the assessment uncovers an actual defect (a real leak, use-after-free,
or race), list it separately under **Escalate to resource review** and recommend
the `resource-review` skill; do not mix it into hardening counts or assign it a CVSS-style
severity.

## Core rules

- **Applicability before compliance.** Profile the project and select only controls that
  match its real build systems, target OSes/arches, threading, prebuild strategy, and
  vendored dependencies.
- **Effective behavior over presence.** A flag in one `conditions` branch, a sanitizer
  script that never runs in CI, or a `.clang-tidy` with `WarningsAsErrors: ''` is not
  proof the control is effective on the shipped build.
- **Research globally, report locally.** Read the whole `binding.gyp`/CMake, CI workflows,
  scripts, and `common.gypi` defaults to resolve what the compiler actually receives;
  report only on the requested scope.
- **Credit toolchain defaults.** Mark a control Met when the toolchain or node-gyp
  `common.gypi` already provides it (MSVC `/GS`, `/DYNAMICBASE`, `/NXCOMPAT` are on by
  default; Release builds optimize). Do not flag a default-on protection as missing.
- **Arch-gate the dangerous flags.** Some hardening flags **hard-error** on the wrong
  architecture (`-fcf-protection=full` is x86-only; `-mbranch-protection` is arm64-only).
  Recommending them ungated breaks the build — always require a `target_arch` condition.
- **No cargo-cult controls.** Record Not applicable when a control has no relevant surface
  (TSan on a strictly single-threaded synchronous addon; `-Wl,-z,*` on a macOS-only
  build), with one-line reasoning.
- **Sanitizer-aware.** `_FORTIFY_SOURCE` must be **off** in AddressSanitizer builds.
  Standard-library hardening assertions are independent and may remain enabled unless the
  project's exact toolchain demonstrates a conflict; a hardening recommendation that breaks
  the sanitizer build is a Gap, not an improvement.
- **No auto-apply.** Propose changes; edit only when the user explicitly asks.

## Control states and priorities

Every assessed control has exactly one state:

| State                 | Meaning                                                                        |
| --------------------- | ------------------------------------------------------------------------------ |
| **Met**               | Effective implementation is evidenced in build config, CI, or toolchain default |
| **Gap**               | Control applies and evidence shows it is absent, disabled, or materially incomplete |
| **Not applicable**    | The project lacks the surface (no Windows target, no threads, no prebuilds, …)   |
| **Needs verification**| The control applies, but a required fact (toolchain version, CI behavior) cannot be established statically |

Prioritize gaps by risk reduction, not by fear:

| Priority        | Use when                                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------- |
| **Essential**   | A broadly expected boundary is missing on a security-sensitive surface: no stack protector/FORTIFY on code doing raw buffer/`memcpy` work; C++ exceptions able to cross the C ABI; mutable global state in a worker-capable addon; over-broad sanitizer suppressions masking first-party leaks |
| **Recommended** | Meaningful hardening with clear applicability: full RELRO (`-Wl,-z,relro -Wl,-z,now`), UBSan+TSan in CI, `-fvisibility=hidden` on C++ TUs, an oldest-glibc prebuild, arch-gated CFI |
| **Optional**    | Context-dependent defense-in-depth or maturity: `-fstrict-flex-arrays=3`, `-ftrivial-auto-var-init=zero`, `-D_GLIBCXX_ASSERTIONS` in release, extra CI telemetry |

Do not use priority as a disguised severity. Consider exposure (does untrusted input
reach the native code?), what the code actually does, existing compensating controls, and
implementation/toolchain cost.

## Review workflow

Run these steps in order. Load reference files only when their domains apply.

### 1. Resolve scope

- If the user names paths or a diff, report only on those while researching the rest of
  the build. Otherwise review working changes, including untracked files:
  ```bash
  if git rev-parse --verify --quiet origin/HEAD >/dev/null; then
    git diff --merge-base origin/HEAD
  else
    git diff HEAD
  fi
  git ls-files --others --exclude-standard
  ```

### 2. Build the project profile

Establish from config rather than assumptions (read
[`references/build-and-toolchain.md`](./references/build-and-toolchain.md)):

- build system(s): node-gyp/`binding.gyp`, CMake, or both; node-addon-api and
  `NAPI_VERSION`; `NAPI_CPP_EXCEPTIONS`;
- language standard and how it is set per platform;
- target OSes (Linux glibc/musl, macOS, Windows) and arches (x64, arm64);
- prebuild strategy (prebuildify/node-gyp-build, prebuild) and shipped binaries;
- concurrency: worker threads, `AsyncWorker`, threadsafe functions, shared state;
- vendored C/C++ sources (amalgamations) and how they are pinned/updated;
- CI matrix, sanitizer/analysis jobs, and release/publish flow.

State unresolved assumptions in the report.

### 3. Select the baseline

Read [`references/baseline-and-reporting.md`](./references/baseline-and-reporting.md). Pin
the compiler/linker baseline to the **OpenSSF Compiler Options Hardening Guide** and the
code baseline to the **C++ Core Guidelines**; verify version-sensitive flag availability
against the project's actual toolchain floor (for example the oldest glibc/GCC used by its
prebuild container). Never assert a flag exists without confirming it for that toolchain.

### 4. Select applicable domains

| Detected surface                                             | Load                                                     |
| ------------------------------------------------------------ | -------------------------------------------------------- |
| Always                                                       | `baseline-and-reporting.md`, `build-and-toolchain.md`    |
| Any compiled C/C++ (all real projects)                       | `compiler-hardening.md`                                  |
| Any project that can build under a sanitizer / static analyzer | `sanitizers-and-analysis.md`                           |
| Ships prebuilt binaries, multi-OS/arch, vendors C sources    | `ci-and-release.md`                                      |
| Hand-written C++ (RAII, ownership, threading, C-ABI boundary) | `modern-cpp-conventions.md`                             |

### 5. Gather evidence

For each applicable control:

- read the *effective* flags the compiler/linker receive for the Release build on each
  OS/arch, not just one `conditions` branch;
- confirm CI actually runs and *gates* on the control (a sanitizer job whose zero exit is
  never checked, or `clang-tidy` with `WarningsAsErrors: ''`, is advisory, not enforced);
- credit toolchain and `common.gypi` defaults; account for arch/OS applicability;
- record `file:line` evidence for Met and Gap; use Needs verification for a concrete
  missing fact (a toolchain version, whether a CI job blocks merge), phrased as a question.

Presence of a flag in the file is a lead; effectiveness on the shipped build is the
finding.

### 6. Consolidate

Group repeated misses under the narrowest common remediation (one missing POSIX hardening
block covering every non-Windows TU is one Gap, not one per file). Separate controls when
OS/arch applicability or remediation differs.

### 7. Report

Use the structure in `baseline-and-reporting.md`:

```markdown
## Native Setup & Hardening Review: <scope>

**Project profile:** <build systems, targets/arches, prebuilds, threading, vendored deps>
**Baseline:** OpenSSF Compiler Hardening Guide + C++ Core Guidelines
**Assumptions:** <unresolved toolchain/CI facts>

### Coverage Summary
| Domain | Met | Gap | Needs verification | Not applicable |
|--------|----:|----:|-------------------:|---------------:|

### Essential Gaps
#### [HARDEN-001] <control> — Gap
- **Applicability:** Why this control applies to this project.
- **Evidence:** `file:line` and the effective build behavior observed.
- **Recommendation:** Minimal concrete change (arch-gated where required).
- **Tradeoffs:** Toolchain floor, startup cost, sanitizer-build interaction.
- **Source:** OpenSSF/Core Guidelines/vendor reference.

### Recommended Gaps
...
### Optional Improvements
...
### Needs Verification
...
### Controls Already Met
### Not Applicable
### Remediation Roadmap
1. Now — Essential, low-risk, arch-gated fixes.
2. Next — Recommended controls and CI gating.
3. Later — Optional defense-in-depth.

### Escalate to Resource Review
Only concrete defects, excluded from hardening counts — recommend the `resource-review` skill.
```

If no gaps remain, say which profile/baseline was assessed and that all applicable
controls examined were Met; still list unresolved verification questions.

## Source freshness

Prefer primary sources in this order:

1. OpenSSF Compiler Options Hardening Guide for the flag baseline.
2. Compiler/linker vendor docs (GCC, Clang/LLVM, Microsoft Learn) for exact flag behavior,
   arch applicability, and minimum toolchain version.
3. C++ Core Guidelines and cppreference for code conventions.
4. Sanitizer/tool docs (AddressSanitizer, clang-tidy, Valgrind) and node-gyp/Node-API
   docs for tooling and addon specifics.

When internet access is available, verify version-sensitive flags against the project's
toolchain floor. Never use listicles as normative sources. When offline, use the pinned
references and state that current toolchain behavior was not re-verified.

## References

| File                                                                                 | Covers                                                                                                   |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| [`references/baseline-and-reporting.md`](./references/baseline-and-reporting.md)     | Standards backbone, profile-driven applicability, evidence rules, state/priority calibration, report format |
| [`references/build-and-toolchain.md`](./references/build-and-toolchain.md)           | `binding.gyp` anatomy, node-addon-api/`NAPI_VERSION`, standard selection, symbol visibility/prefixing, vendoring, Windows arch traps |
| [`references/compiler-hardening.md`](./references/compiler-hardening.md)             | Per-OS/per-arch compiler & linker hardening flag matrix (GCC/Clang + MSVC), arch-gating, FORTIFY-vs-sanitizer, the `.node`-is-a-shared-library reality |
| [`references/sanitizers-and-analysis.md`](./references/sanitizers-and-analysis.md)   | Wiring ASan/UBSan/TSan/LSan/Valgrind and clang-tidy/cppcheck; running them against a Node addon; suppression discipline; CI gating |
| [`references/ci-and-release.md`](./references/ci-and-release.md)                     | Cross-platform CI matrix, prebuilds (glibc/musl/arch), coverage, npm provenance, vendored-source supply chain |
| [`references/modern-cpp-conventions.md`](./references/modern-cpp-conventions.md)     | RAII/ownership, rule of five, exception safety across the C ABI, concurrency correctness, header hygiene, maintainable structure |

## Project adaptation

Treat the repository's build policy, documented toolchain floors, and platform constraints
as input — not automatic exemptions. Record accepted tradeoffs (a `_FORTIFY_SOURCE=3`
deferral because the prebuild container ships an older GCC, a deliberately single-writer
threading model) and their compensating controls explicitly, so future reviews do not
reopen the same decision without new facts.
