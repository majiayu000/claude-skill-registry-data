---
name: firmware-differential-security-analysis
description: Compare vulnerable and fixed firmware images to isolate security-relevant validation and authorization changes. Use for patch diffs, CVE comparisons, and homologous embedded handlers.
---

# Firmware Differential Security Analysis

Use this skill when two firmware versions, builds, or related models must be
compared without assuming shared source lineage.

## Workflow

1. Preserve acquisition URLs, filenames, versions, hashes, extraction commands, architectures, and filesystem boundaries.
2. Identify corresponding binaries by names, hashes, strings, imports, section layout, and route/function relationships.
3. Align functions using call graphs, distinctive constants, strings, operation IDs, and normalized instruction patterns—not absolute addresses alone.
4. Diff candidate handlers and trace the smallest change affecting input validation, authorization, state gating, or sink reachability.
5. State old behavior, new behavior, checked parameter/state, branch outcome, and resulting security semantics.
6. Search the target firmware for architecture-independent signatures and classify each match as same vulnerable logic, same patched logic, related, absent, or unknown.

## Evidence discipline

Separate `VERIFIED BY PATCH DIFF` from target-firmware evidence. Do not claim
CVE applicability from operation-number similarity or strings alone. Preserve
unresolved indirect calls and runtime-registration conditions. Never execute
firmware binaries from acquired images.
