---
name: s32debugger-resolve-gdb-variant
description: >
  Resolve the correct S32Debugger GDB variant from a target core or core
  instance. Use this whenever a flow needs to choose between `arm32` and
  `arm64` before starting GTA/GDB, generating or validating a config,
  checking a single-core or multicore startup path, adapting an existing
  debugger flow, or normalizing an explicit core instance such as `M7_0` or
  `A53_0_0` without losing the original instance identity.
license: LA_OPT_Online Code Hosting NXP_Software_License
metadata:
  author: NXP
  version: "1.0.0"
  product: s32debugger
  tags: '[s32debugger, gdb-variant, resolution]'
---

# S32Debugger Resolve GDB Variant

Resolve the correct S32Debugger GDB variant from the target core family while
preserving any explicit core instance. This skill determines `arm32` versus
`arm64` only; it does not choose init scripts, startup order, config policy,
or flash behavior.

## When to use

Use this skill when:
- A flow needs the correct GDB variant before startup, config generation, or
  validation.
- The user provides an explicit core instance such as `M7_0`, `M7_0_LS`,
  `A53_0_0`, or `R52_0` and the variant must be chosen without losing that
  instance identity.
- The request needs core normalization but not broader startup orchestration.

Do **not** use this skill for:
- Guessing the variant from the SoC name when the target core is still unknown.
- Expanding into init-sequence, startup, config-generation, or flash logic.

## Quickstart

### 1. Mandatory reference read

Before using this skill, read:
- `references/authoring-procedure.md`
- `references/examples.md`

Do not continue until those files have been reviewed.
### 2. Read the target core string

```
Examples: M7, M7_0, M7_0_LS, A53_0_0, R52_0, A78_0_0
Rule: if the core family is clear from the core string, resolve it directly
```

### 3. Normalize only for family matching

```
Strip for matching: _0, _1, _0_0, _LS
Preserve separately: the original explicit instance for downstream use
```

### 4. Map family to variant

```
ARM32: M7, M33, M0, M4, R52
ARM64: A53, A78
Return: normalized family, preserved instance, selected variant, justification
```

## Guardrails

**Mandatory reference rule**
- Read the listed reference files before selecting a branch, generating output,
  or producing the final answer.
- Treat the references as part of the skill, not as optional supplemental
  notes.
**Scope**
- Resolve GDB variant only.
- Preserve the distinction between normalized core family and explicit core
  instance.
- Select the variant from the target core family, not from the SoC family.

**Destructive actions**
- Default to direct resolution when the family is clear.
- Do not discard a usable explicit instance such as `M7_0` or `A53_0_0`.
- Do not rewrite the request into a broader startup or init decision here.

**Refuse-and-escalate**
- If the core name is missing, ask for the target core explicitly.
- If the core string is ambiguous or unsupported, request clarification instead
  of guessing.
- If only a generic SoC name is available and the target core is unknown, stop
  and ask for the exact core rather than inferring the variant.
- If downstream logic needs more than the variant, hand off to the relevant
  startup or family-context skills.

**Do**
- Normalize for matching while preserving the explicit instance separately.
- Return the relative executable path when it is useful.
- Keep the justification short and grounded in the mapping.

**Do not**
- Select the GDB variant from the SoC family instead of the target core family.
- Throw away the explicit instance too early.
- Guess when the family is unknown or unclear.

## Validation loop
0. Confirm the required reference files were reviewed before executing the
   workflow or finalizing the answer.
1. Confirm the request contains a core string or else ask for one.
2. Verify normalization preserves the original instance while extracting the
   family correctly.
3. Verify the family maps to the supported `arm32` or `arm64` set.
4. Verify the response distinguishes normalized family from explicit instance.
5. Verify no broader init/startup/flash policy is being introduced.
6. Return normalized family, explicit instance if present, selected variant,
   executable path when useful, and short justification.

## Out of scope

- Guessing the variant from a vague SoC reference alone.
- Choosing init scripts, startup order, config policy, or flash behavior.
- Replacing family-context lookup when authoritative context values are needed.
- Discarding explicit core-instance information that later skills may need.

## See Also

- `references/authoring-procedure.md` - normalization rules, family mapping,
  and response structure.
- `references/examples.md` - example mappings and anti-patterns.
- Related skills: `s32debugger-start-standalone-live-session`,
  `s32debugger-start-singlecore-standalone-live-debug-session`,
  `s32debugger-start-multicore-standalone-live-debug-session`,
  `s32debugger-connect-gdb-to-s32-debug-probe`,
  `s32debugger-resolve-core-name-from-context`
