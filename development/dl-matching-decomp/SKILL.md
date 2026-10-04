---
name: dl-matching-decomp
description: Reconstruct source-equivalent code from an authorized compiled binary through matching decompilation, reproducible builds, disassembly/decompiler analysis, function/section diffing, and final hash verification. Use when asked to reproduce an executable/ROM/library byte-for-byte, diagnose why a rebuilt binary does not match, infer compiler/ABI/codegen settings, or organize a decompilation project. Do not use to bypass DRM/access controls, defeat license checks, extract credentials/secrets, or enable malware.
---

# Matching Decompilation / Binary-Matching Reconstruction

Use this skill for **authorized reverse engineering** where the goal is to reconstruct maintainable source whose compiled output matches a reference binary as closely as possible, ideally byte-for-byte.

The target is a **source-equivalent reconstruction**, not a claim that the original source text has been recovered. Comments, original identifier names, macros, formatting, and some high-level constructs are usually not uniquely recoverable from a stripped optimized binary.

## Core principle

Treat the full-file hash as the **final acceptance test**, not the primary debugging signal.

Work from coarse to fine:

1. Establish exact reference artifacts and provenance.
2. Fingerprint the binary and determine format, architecture, ABI, endianness, and likely toolchain.
3. Make the build deterministic/reproducible.
4. Partition differences by section/object/function.
5. Reconstruct one small unit at a time from disassembly/decompiler output and observed data flow.
6. Recompile with pinned compiler/linker versions and flags.
7. Compare generated machine code, relocations, data layout, and section metadata.
8. Iterate on source shape/toolchain settings until local units match.
9. Only after local matching, require the whole-file hash to match.

## Authorization and boundaries

Before substantial work, establish that the user owns the binary/source, has permission to analyze it, or is working on a legitimately obtained artifact for interoperability, preservation, research, debugging, or migration.

Stay within the reconstruction task. Do not provide workflows whose purpose is to bypass DRM, authentication, license enforcement, anti-cheat, access controls, credential storage, or defensive security controls. Do not add persistence, stealth, exploitation, or malicious payload behavior.

## Initial triage

Inspect before editing or guessing.

Collect:

- reference binary path and expected hash, if known;
- candidate source/build tree, if any;
- binary/container type: ELF, PE/COFF, Mach-O, ROM/firmware image, static/shared library, object file;
- architecture and endianness;
- debug symbols, map files, export/import tables, string tables, relocation information, embedded compiler strings, build IDs, timestamps;
- build scripts, lockfiles, linker scripts, response files, SDK/toolchain versions;
- whether the binary contains nondeterministic fields.

Prefer standard tools already available in the environment. Typical examples: `file`, `strings`, `readelf`, `objdump`, `nm`, `llvm-objdump`, `otool`, `dumpbin`, `sha256sum`, `shasum`, `cmp`, `xxd`, Ghidra, IDA, Binary Ninja, radare2/rizin, or platform-specific ROM tools.

Never assume a compiler or optimization level from coding style alone. Gather evidence.

## Reproducible-build gate

Before changing reconstructed logic, verify that rebuilding the **same candidate source twice** yields identical binaries. If it does not, fix nondeterminism first.

Common nondeterministic inputs include:

- timestamps and archive member dates;
- absolute paths embedded in debug data;
- randomized build IDs or UUIDs;
- filesystem iteration order;
- locale/timezone differences;
- compiler/linker version drift;
- unpinned SDKs or generated assets;
- link-order differences;
- LTO/PGO state;
- environment-dependent macros.

Record the exact compiler, assembler, linker, SDK, flags, environment variables, and linker script. If containers/Nix/lockfiles already exist, prefer using them over inventing a new build environment.

## Matching workflow

### 1. Fingerprint the target

Run `scripts/fingerprint.py` on the reference and candidate binaries when useful. Record at least size and SHA-256. MD5/SHA-1 may be included only when matching historical project metadata; do not treat them as stronger integrity checks than SHA-256.

### 2. Localize differences

If hashes differ, do not repeatedly rewrite source blind. Use `scripts/compare_binary.py` and native binary tools to answer:

- Is file size identical?
- What is the first differing offset?
- Are differences sparse or pervasive?
- Do differences cluster in code, data, relocation, symbol, debug, or metadata regions?
- Is the mismatch a link/layout problem rather than source semantics?

For structured formats, prefer section/function-level comparison over raw whole-file diff.

### 3. Build a function/section map

Create or update a progress table with units such as:

`unit | reference range/symbol | candidate symbol/file | match status | confidence | next hypothesis`

When symbols are absent, use stable synthetic names based on address (for example `sub_0012A430`) until semantics justify a better name. Do not invent original names as facts.

### 4. Reconstruct semantics

For each unit:

- inspect disassembly and decompiler output;
- identify calling convention, parameter widths, signedness, return type, stack frame, globals, constants, switch tables, and control flow;
- reconstruct the simplest high-level code consistent with the machine code and surrounding callers/callees;
- preserve observable integer widths, overflow behavior, aliasing constraints, struct packing, alignment, and volatile access where relevant;
- treat undefined behavior as a red flag rather than a matching technique of first resort.

Decompiler output is evidence, not ground truth.

### 5. Match code generation

When semantics look correct but machine code differs, test one hypothesis at a time. Common causes include:

- compiler version/patch level;
- optimization level or per-function pragmas;
- inlining decisions;
- `static`/`inline`/visibility differences;
- signed vs unsigned types and integer promotion;
- enum/bitfield/struct layout;
- stack alignment and ABI switches;
- exception/RTTI settings;
- floating-point mode;
- PIC/PIE/code model;
- register-pressure changes caused by expression shape;
- source expression ordering;
- linker ordering, relaxation, garbage collection, or identical-code folding;
- generated tables/assets rather than source logic.

Prefer a semantically clear reconstruction. Only use awkward source shaping when exact matching requires it and document why.

### 6. Compare at the right layer

Use this order of evidence:

1. function-level assembly/instruction diff;
2. object/section bytes and relocations;
3. linked image layout;
4. whole-file bytes;
5. whole-file hash.

Normalize addresses/relocations only for diagnosis. The final exact-match gate must compare the real produced artifact without normalization.

### 7. Validate behavior separately

Binary equality strongly indicates identical machine representation for that build, but maintain separate behavioral tests when possible. If exact matching is impossible because the historical toolchain is unavailable, report the nearest achieved level precisely: semantic match, instruction match modulo addresses, section match, or byte-for-byte match.

## Diagnostic heuristics

Read `references/mismatch-patterns.md` when a candidate is close but not exact.

Quick interpretation:

- **Same size, a few short differing ranges:** constants, relocation values, timestamps/build IDs, or one/few functions.
- **Same functions but shifted addresses:** link order, section alignment, padding, or different function sizes earlier in the image.
- **Large code-region divergence:** wrong compiler/version/flags, inlining/LTO, ABI, or reconstruction shape.
- **Code matches but file hash differs:** headers, debug info, signatures, build IDs, checksums, resource sections, timestamps, or padding.
- **Data-only divergence:** struct layout, generated assets/tables, endianness, packing, locale, or initialization order.

## Output format

When reporting progress, be concrete and compact. Include:

- current matching level;
- exact evidence collected;
- most likely mismatch class;
- next smallest experiment that can falsify the hypothesis;
- commands/files changed;
- before/after hash and byte-match metrics when available.

Do not say “source recovered” unless source artifacts were actually recovered from symbols/debug/source archives. Prefer “reconstructed source” or “source-equivalent reconstruction.”

## Supporting resources

- `references/methodology.md` — deeper end-to-end method.
- `references/mismatch-patterns.md` — mismatch signatures and likely causes.
- `references/tooling.md` — tool selection by platform/format.
- `examples/progress-template.md` — suggested tracking format.
- `scripts/fingerprint.py` — deterministic hashes and basic file signature.
- `scripts/compare_binary.py` — raw byte-diff summary suitable for iterative matching.
