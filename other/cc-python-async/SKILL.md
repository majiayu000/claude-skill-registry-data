---
name: cc-python-async
description: "Use when Python event-loop blocking, task cancellation, async resource cleanup, bounded concurrency or thread offloading need implementation or diagnosis."
---

# Python async lifecycle

Apply to libraries, CLI tools, desktop cores and services. Determine the application role from the actual project; a frontend/backend product name does not constrain the language.

Map event-loop work, blocking clients, task ownership and resource acquisition. Confirm interpreter/runtime features before choosing task-group APIs.

## Apply the workflow

1. Locate the actual project, task boundary and existing contracts; load only the language and domain material needed now.
2. Apply the [specialist checks](references/practice.md), establishing the input evidence before selecting the smallest change.
3. Verify affected behavior with existing repository tools. Explicitly report missing tools, environments or execution; a plan is not a passing result.
4. Deliver scope, specialist decisions, actual verification and remaining risk. A review-only task stays read-only.

## Task boundary

General Python package/typing conventions use the project standard; do not create an event loop per request as a generic fix.

## Engineering practices

Read the [local engineering decisions](references/engineering-practices.md) for this task and follow their links to relevant shared principles. Apply levels and exceptions against actual project contracts; product frontend/backend labels do not constrain language or role.
