---
name: trace-codebase-provenance
description: Use when repo origin is unclear, dealing with leaks/sourcemaps/decompiled code, or needing to distinguish source of truth from derived, generated, or reconstructed layers
---

## Announce at start: "Using codebase-analyzer to trace codebase provenance."

## Overview

Distinguish source of truth from derived layers. Critical first step — if you misidentify generated code as source, every downstream analysis is poisoned.

**Prerequisite:** Reads `docs/analysis/target-classification.md` and `docs/analysis/tech-stack.md`.

## Deception Awareness

Assume the codebase may be trying to hide things. Look for: deliberately misleading variable names, code structured to look like one thing but do another, comments describing intent that doesn't match implementation, obfuscated strings, encoded URLs.

## Intent-Implementation Gap

Comments say "validates user input" but the function only trims whitespace. Function named `sanitize` that passes data through unchanged. The gap between stated purpose and actual behavior is where the truth lives. Always verify what code DOES, not what it SAYS it does.

## Process

1. Check for sourcemap files (*.map, .js.map) — if present without corresponding source, this is derived
2. Look for compilation markers: "DO NOT EDIT", "@generated", timestamps in headers
3. Identify hand-written vs machine-generated code patterns (see references/provenance-patterns.md)
4. Check git history: were files committed in batches (generated) or individually (hand-written)?
5. Scan for deception indicators: misleading names, intent-implementation gaps, obfuscated sections
6. Identify the source-of-truth layer: where did this code originate?
7. Map derivation chain: source -> intermediate -> shipped -> runtime
8. Produce provenance map with build dimension catalogue

## The Iron Law

```
Never confuse sourcemap with source, build output with source, decompiled code with original code.
```

## Build Dimension Catalogue

Every analysis output MUST include which config axes were examined:

```
## Build Dimensions Analyzed
- ENVIRONMENT: development (current)
- USER_TYPE: external (assumed from build)
- PROVIDER: not determined

## Dimensions NOT Analyzed
- USER_TYPE: internal, admin
- PROVIDER: all variants
```

## Trigger Signals

- **HIGH confidence**: Sourcemap without source -> decompiled/derived
- **HIGH confidence**: Build filters code based on config -> `analyze-build-pipeline`
- **HIGH confidence**: Decompiled signatures masquerading as original -> deception
- **MEDIUM confidence**: Partial source with generated files -> mixed provenance
- **MEDIUM confidence**: Intent-implementation gaps -> investigate further

## Rationalization Table

| Rationalization | Reality |
|---|---|
| "Looks like original source" | Check for sourcemap artifacts, decompiler signatures, auto-generated headers |
| "Build artifacts are documentation" | Build artifacts are EVIDENCE of the build process, not documentation of the source |
| "Comments explain what the code does" | Comments describe intent; only execution describes behavior. Verify both. |
| "Tests prove it works correctly" | Tests prove it works in tested scenarios. Untested paths are the danger zone. |

## Red Flags

- Assuming all .js files are source (could be compiled TS output)
- Not checking git history for batch-committed generated code
- Missing the build dimension catalogue (downstream skills depend on it)
- Trusting comments over implementation
- Accepting "clean" formatting as proof of original source

## SECURITY_SIGNAL

- Decompiled code masquerading as original
- Obfuscated sections that resist readability
- Hidden API endpoints in strings (base64, hex-encoded)
- Credentials in "test" files or "example" configs
- Functions that do more than their name implies

## Output Contract

Write `docs/analysis/provenance.md` using standard contract.
Include: provenance map, source-of-truth location, derivation chain, build dimensions, deception assessment.
