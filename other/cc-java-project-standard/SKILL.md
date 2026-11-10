---
name: cc-java-project-standard
description: "Use when Java package/module structure, build-tool conventions, application boundaries, exceptions, persistence ownership or repository-wide Java engineering needs design or review."
---

# Java project engineering

Apply to libraries, CLI tools, desktop cores and services. Determine the application role from the actual project; a frontend/backend product name does not constrain the language.

Read the declared JDK, build descriptor, wrapper and existing package layering. Preserve the current language level and dependency platform.

## Apply the workflow

1. Locate the actual project, task boundary and existing contracts; load only the language and domain material needed now.
2. Apply the [specialist checks](references/practice.md), establishing the input evidence before selecting the smallest change.
3. Verify affected behavior with existing repository tools. Explicitly report missing tools, environments or execution; a plan is not a passing result.
4. Deliver scope, specialist decisions, actual verification and remaining risk. A review-only task stays read-only.

## Task boundary

JVM profiling and pool/GC incidents belong to the runtime specialty; do not impose a particular web framework.

## Engineering practices

Read the [local engineering decisions](references/engineering-practices.md) for this task and follow their links to relevant shared principles. Apply levels and exceptions against actual project contracts; product frontend/backend labels do not constrain language or role.
