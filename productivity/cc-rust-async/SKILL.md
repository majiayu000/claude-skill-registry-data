---
name: cc-rust-async
description: "Use when Rust futures, Tokio tasks, cancellation safety, bounded async concurrency, blocking boundaries or shutdown behavior need implementation or diagnosis."
---

# Rust async lifecycle

Apply to libraries, CLI tools, desktop cores and services. Determine the application role from the actual project; a frontend/backend product name does not constrain the language.

Identify runtime/version and every suspension point, resource owner and cancellation boundary. Check the actual future documentation before assuming cancellation safety.

## Apply the workflow

1. Locate the actual project, task boundary and existing contracts; load only the language and domain material needed now.
2. Apply the [specialist checks](references/practice.md), establishing the input evidence before selecting the smallest change.
3. Verify affected behavior with existing repository tools. Explicitly report missing tools, environments or execution; a plan is not a passing result.
4. Deliver scope, specialist decisions, actual verification and remaining risk. A review-only task stays read-only.

## Task boundary

Use the project standard for crate layout; only apply Tokio-specific behavior when Tokio and its actual version are present.

## Engineering practices

Read the [local engineering decisions](references/engineering-practices.md) for this task and follow their links to relevant shared principles. Apply levels and exceptions against actual project contracts; product frontend/backend labels do not constrain language or role.
