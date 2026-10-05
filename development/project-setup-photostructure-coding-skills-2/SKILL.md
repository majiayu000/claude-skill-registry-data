---
name: project-setup
description: Set up, assess, or improve stable Rust projects for idiomatic safe code, maintainability, strict but usable rustc/Clippy/rustfmt policy, Cargo workspace and feature design, MSRV/edition/toolchain management, testing and CI, unsafe/FFI boundaries, documentation, crates.io packaging, and release hygiene. Use when asked to create or review a Rust project or Cargo.toml, make a Rust codebase easier to maintain, configure strict lints, reduce or govern unsafe code, add Miri/fuzz/sanitizer checks, structure a workspace, prepare or dry-run a crate publish, or establish Rust release and dependency policy. In assessment mode, produces an applicability-aware Met / Gap / Not applicable / Needs verification baseline rather than claiming bugs or unsoundness.
metadata:
  website: "https://photostructure.com/coding/"
---

# Rust Project Setup

Set up, assess, and improve Rust projects using current official Rust, Cargo, Clippy,
rustfmt, rustdoc, crates.io, and RustSec guidance. Optimize for code that is easy to
understand, difficult to misuse, explicit about unsafe proof obligations, and practical
to test and publish.

See [ATTRIBUTION.md](./ATTRIBUTION.md). Keep detailed recipes in the references and load
only the domains that apply.

## Choose the operating mode

State the mode before acting:

| User intent | Mode | Default behavior |
| --- | --- | --- |
| “Create/set up/configure this Rust project” | **Implement** | Edit the requested project, then run proportionate checks |
| “Assess/review our Rust setup or maintainability” | **Assess** | Report evidence-backed baseline states; do not edit |
| “Advise/design/give me a checklist” | **Advice** | Explain an adapted setup or workflow; do not edit or perform external mutations |
| “Make this code more idiomatic/maintainable” | **Refactor** | Preserve behavior, public API, MSRV, features, and target support unless the user authorizes a change |
| “Prepare this crate for publishing/release” | **Release preparation** | Inspect and dry-run packaging; never perform an external publish, tag, push, owner change, or release without explicit authorization |

When the request combines modes, apply each boundary separately. Read-only assessment
does not authorize cleanup edits merely because they are easy.

## Boundary with defect and security review

This skill assesses preventive controls and maintainability, not whether code is sound or
exploitable.

| This skill | A future proof-gated safety review |
| --- | --- |
| Asks whether applicable project controls meet a baseline | Proves a concrete soundness, concurrency, or security defect |
| Reports Met / Gap / Not applicable / Needs verification | Requires a reproducer, dynamic trace, or complete invariant/data-flow proof |
| Prioritizes Essential / Recommended / Optional | Prioritizes demonstrated impact and reachability |
| May recommend Miri, fuzzing, sanitizers, and narrower unsafe | Uses their results as evidence for a specific defect |

`unsafe` is not automatically a defect. Conversely, safe Rust can panic, deadlock, leak,
exhaust resources, mishandle data, or violate application invariants. Keep those facts
separate from compiler-enforced memory and thread safety.

## Core rules

- **Profile before prescribing.** Library, binary, proc macro, build script, FFI layer,
  `no_std`, embedded, WASM, async service, and unpublished workspace helper have different
  baselines.
- **Effective policy over file presence.** A root `[workspace.lints]` is ineffective for
  a member that does not opt in. A CI command without the relevant packages, targets, or
  features does not cover them.
- **MSRV is a contract.** Check `rust-version`, edition, resolver, dependency selection,
  lint availability, and CI against the declared floor. A contributor toolchain file is
  not proof that the MSRV works. Resolver 3 prefers compatible dependencies but does not
  enforce MSRV, and mixed-MSRV members can affect the shared resolution.
- **Strict does not mean every lint.** Use Clippy's default groups, consider `pedantic`
  with narrow exceptions, and cherry-pick `restriction` lints. Never enable the whole
  `restriction` or `nursery` groups as a generic best practice.
- **Prefer scoped, explained exceptions.** Do not weaken the whole workspace to silence
  one intentional pattern. Do not scatter unexplained `allow` attributes either.
- **Treat unsafe as a proof boundary.** Forbid it in safe-only crates. Where required,
  isolate it behind private safe abstractions, document caller/implementor contracts, and
  explain why each block or impl discharges its obligations.
- **Preserve compatibility deliberately.** Public items, fields, traits, error variants,
  feature names/defaults, MSRV, platforms, and public dependency types can be SemVer
  commitments.
- **Do not cargo-cult ownership.** A `clone`, `Arc`, mutex, generic, lifetime, trait,
  newtype, builder, or async function is neither good nor bad without the actual ownership,
  concurrency, and API need.
- **Never publish by implication.** `cargo package`, `cargo publish --dry-run`, and archive
  inspection are preparation. `cargo publish` and registry ownership changes are external,
  durable actions requiring explicit user intent.
- **Verify current behavior.** Editions, resolver defaults, lints, Cargo packaging,
  docs.rs, crates.io limits, and trusted-publishing providers evolve. Resolve them against
  official live sources and the project's toolchain when internet access is available.

## Assessment states and priorities

Use these only in **Assess** mode.

| State | Meaning |
| --- | --- |
| **Met** | Effective implementation is evidenced in manifests, source, CI, or observed local behavior |
| **Gap** | The control applies and evidence shows it is absent, disabled, or materially incomplete |
| **Not applicable** | The project lacks the surface, with a concrete reason |
| **Needs verification** | The control applies, but a required fact cannot be established safely |

| Priority | Use when |
| --- | --- |
| **Essential** | A foundational contract or release boundary is missing: undeclared/testless MSRV promise, publishable private crate, unaudited broad unsafe surface, package contents exposing secrets, or CI that does not build the supported product |
| **Recommended** | Clear maintainability or reliability value: workspace lint inheritance, feature matrix, doctests, Miri for exercised unsafe code, package dry runs, or structured public errors |
| **Optional** | Context-dependent maturity: broader fuzzing, extra target checks, stricter curated lints, deeper supply-chain policy, or automated release ergonomics |

Priority is not defect severity.

## Workflow

### 1. Resolve scope and instructions

- Read applicable `AGENTS.md`, `CLAUDE.md`, contribution, release, and security policy.
- If paths or a diff are named, report only on that scope while reading shared manifests,
  workspace configuration, CI, and public callers needed to understand it.
- Otherwise inspect the working tree, including untracked files. Preserve unrelated
  changes.
- Establish whether commands may fetch dependencies, update a lockfile, modify generated
  files, or touch a registry before running them.

### 2. Build the project profile

Read [`references/project-and-workspace.md`](./references/project-and-workspace.md) and
establish:

- package roles: library, binary, proc macro, build script, `*-sys`/FFI, examples,
  benchmarks, fuzz/xtask/internal helpers;
- workspace topology, publishable members, resolver, edition, `rust-version`, contributor
  toolchain, effective `.cargo/config.toml` and invocation directory, lockfile policy,
  supported targets, `std`/`no_std`, and async runtime;
- public API and SemVer commitments, features/default features, target-specific code,
  native dependencies, generated code, and build-time execution;
- rustc/Clippy/rustfmt/rustdoc policy, CI matrix, Miri/fuzz/sanitizer use, dependency
  audit policy, documentation, packaging, registry, and release ownership.

State unresolved assumptions.

### 3. Select the baseline and domains

Read [`references/baseline-and-reporting.md`](./references/baseline-and-reporting.md).

| Detected surface or task | Load |
| --- | --- |
| Always | `baseline-and-reporting.md`, `project-and-workspace.md` |
| Lints, formatting, tests, CI, MSRV verification, Miri/fuzz/sanitizers | `linting-testing-and-ci.md` |
| Code/API maintainability, errors, ownership, unsafe/FFI, docs | `idiomatic-safe-rust.md` |
| Publishable crate, package contents, SemVer, docs.rs, release/auth/ownership | `publishing-and-release.md` |

Use the current stable Rust/Cargo documentation as the default baseline, adapted to the
declared MSRV and supported targets. Use the Rust API Guidelines as recommendations, not
mandates; current Cargo/rustdoc behavior wins where older guidance conflicts.

### 4. Gather evidence

Prefer static evidence first:

- manifests, lockfiles, `rust-toolchain.toml`, rustfmt/Clippy config, workspace inheritance;
- crate roots, module visibility, public signatures/docs, unsafe blocks/impls and their
  safety contracts;
- CI/release workflows, feature/target matrices, build scripts, proc macros, package
  include/exclude rules, and docs.rs metadata.

Then run safe local checks proportionate to the mode and project. Do not blindly paste a
universal command block: adapt package, target, feature, platform, MSRV, and network
flags. Treat grep hits and clean tool runs as evidence for executed coverage, not proof of
absence.

For Met and Gap, record `file:line` and effective behavior. Phrase Needs verification as
one concrete question with a safe verification method.

### 5. Execute the selected mode

- **Implement:** make the smallest coherent setup, config, documentation, or CI changes;
  preserve existing policy unless the request changes it; validate the result.
- **Assess:** consolidate repeated misses under their root cause and report with the
  template below. Do not edit.
- **Advice:** give an applicability-aware design, checklist, or command sequence; state
  assumptions and stop before edits, uploads, tags, pushes, or registry changes.
- **Refactor:** characterize public/API/MSRV/feature behavior first; use tests and SemVer
  analysis to prevent an “idiomatic” rewrite from silently breaking users.
- **Release preparation:** follow the dry-run gate in
  `publishing-and-release.md`; stop before external mutation unless explicitly requested.

### 6. Report or hand off

For implementation/refactoring, lead with the resulting behavior, files changed, checks
run, and any remaining compatibility or release decision.

For assessment, use:

```markdown
## Rust Project Baseline Review: <scope>

**Profile:** <roles, workspace, targets, MSRV/edition, features, unsafe/FFI, publishing>
**Baseline:** Current official Rust/Cargo guidance adapted to <MSRV/targets>
**Assumptions:** <unresolved facts>

### Coverage Summary
| Domain | Met | Gap | Needs verification | Not applicable |
| --- | ---: | ---: | ---: | ---: |

### Essential Gaps
#### [RUST-001] <control> — Gap
- **Applicability:** Why it applies.
- **Evidence:** `file:line` and effective behavior.
- **Recommendation:** Minimal concrete change.
- **Tradeoffs:** MSRV, compatibility, compile time, contributor or release impact.
- **Source:** Primary official guidance.

### Recommended Gaps
### Optional Improvements
### Needs Verification
### Controls Already Met
### Not Applicable
### Remediation Roadmap
```

If all examined controls are Met, name the profile and coverage; do not imply that tools
proved soundness or that unexamined feature/target combinations passed.

## Source freshness

Prefer primary sources in this order:

1. Rust Reference, standard-library docs, Rust Book, Edition Guide, rustc/rustdoc books.
2. Cargo Book/reference and official Clippy/rustfmt documentation.
3. crates.io and docs.rs official documentation; Rust project announcements for current
   registry/toolchain changes.
4. Rust API Guidelines for idiomatic public API considerations.
5. RustSec and the official upstream documentation for optional tools such as Miri,
   cargo-audit, cargo-deny, or cargo-fuzz.

When offline, use these pinned references and explicitly mark version-sensitive facts as
not re-verified. Do not use popularity lists or blog folklore as normative guidance.

## References

| File | Covers |
| --- | --- |
| [`references/baseline-and-reporting.md`](./references/baseline-and-reporting.md) | Applicability, evidence, states/priorities, false positives, reporting |
| [`references/project-and-workspace.md`](./references/project-and-workspace.md) | Cargo/project structure, workspaces, toolchains, MSRV/edition/resolver, features, lockfiles, build-time code |
| [`references/linting-testing-and-ci.md`](./references/linting-testing-and-ci.md) | Strict usable rustc/Clippy/rustfmt policy, testing matrix, CI, Miri, fuzzing, sanitizers |
| [`references/idiomatic-safe-rust.md`](./references/idiomatic-safe-rust.md) | Ownership/API design, types/invariants, errors/panics, unsafe/FFI, concurrency, docs, maintainability gotchas |
| [`references/publishing-and-release.md`](./references/publishing-and-release.md) | crates.io metadata/package contents, SemVer, docs.rs, dry runs, trusted publishing, ownership, dependencies |

## Project adaptation

Treat documented MSRV, target, feature, unsafe, dependency, and release policies as input,
not automatic exemptions. Record intentional tradeoffs and narrow lint exceptions with
their rationale so future work does not reopen them without new evidence.
