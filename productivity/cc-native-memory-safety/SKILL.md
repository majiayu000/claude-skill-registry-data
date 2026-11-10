---
name: cc-native-memory-safety
description: "Use when C/C++ leaks, use-after-free, double release, bounds errors, allocator mismatch, FFI ownership or teardown races need diagnosis or repair."
---

# Native memory and FFI safety

Apply to libraries, CLI tools, desktop cores and services. Determine the application role from the actual project; a frontend/backend product name does not constrain the language.

Preserve a reproducible input, allocation/release stacks, platform/runtime identity and concurrent teardown sequence.

## Apply the workflow

1. Locate the actual project, task boundary and existing contracts; load only the language and domain material needed now.
2. Apply the [specialist checks](references/practice.md), establishing the input evidence before selecting the smallest change.
3. Verify affected behavior with existing repository tools. Explicitly report missing tools, environments or execution; a plan is not a passing result.
4. Deliver scope, specialist decisions, actual verification and remaining risk. A review-only task stays read-only.

## Task boundary

Apply language-appropriate ownership: C cleanup contracts and C++ RAII are different; sanitizer success is bounded evidence.

## Engineering practices

Read the [local engineering decisions](references/engineering-practices.md) for this task and follow their links to relevant shared principles. Apply levels and exceptions against actual project contracts; product frontend/backend labels do not constrain language or role.
