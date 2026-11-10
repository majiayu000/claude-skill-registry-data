---
name: cc-rust-project-standard
description: "Use when Rust crate or workspace structure, module boundaries, ownership-facing APIs, Result conventions, Cargo dependencies or engineering checks need design or review."
---

# Rust project engineering

Apply to libraries, CLI tools, desktop cores and services. Determine the application role from the actual project; a frontend/backend product name does not constrain the language.

Read Cargo.toml, workspace membership, edition, MSRV and existing aliases before proposing modules or dependencies. Work in the owning crate rather than upgrading the entire workspace.

## Apply the workflow

1. Locate the actual project, task boundary and existing contracts; load only the language and domain material needed now.
2. Apply the [specialist checks](references/practice.md), establishing the input evidence before selecting the smallest change.
3. Verify affected behavior with existing repository tools. Explicitly report missing tools, environments or execution; a plan is not a passing result.
4. Deliver scope, specialist decisions, actual verification and remaining risk. A review-only task stays read-only.

## Task boundary

Existing Tokio cancellation or scheduling defects belong to the async specialty; unrelated frontend structure is outside this scope.

## Engineering practices

Read the [local engineering decisions](references/engineering-practices.md) for this task and follow their links to relevant shared principles. Apply levels and exceptions against actual project contracts; product frontend/backend labels do not constrain language or role.
