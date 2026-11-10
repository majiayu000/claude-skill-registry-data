---
name: cc-cpp-project-standard
description: "Use when C++ module/header boundaries, resource lifetime, exception safety, ABI, build-standard conventions or project-wide C++ checks need design or review."
---

# C++ project engineering

Apply to libraries, CLI tools, desktop cores and services. Determine the application role from the actual project; a frontend/backend product name does not constrain the language.

Read the actual C++ standard, standard library, compiler matrix, build presets and exported ABI before choosing features.

## Apply the workflow

1. Locate the actual project, task boundary and existing contracts; load only the language and domain material needed now.
2. Apply the [specialist checks](references/practice.md), establishing the input evidence before selecting the smallest change.
3. Verify affected behavior with existing repository tools. Explicitly report missing tools, environments or execution; a plan is not a passing result.
4. Deliver scope, specialist decisions, actual verification and remaining risk. A review-only task stays read-only.

## Task boundary

Do not upgrade the C++ standard or replace the build system without a task need; pure C interfaces retain their own contract.

## Engineering practices

Read the [local engineering decisions](references/engineering-practices.md) for this task and follow their links to relevant shared principles. Apply levels and exceptions against actual project contracts; product frontend/backend labels do not constrain language or role.
