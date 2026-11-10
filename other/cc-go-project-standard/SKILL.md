---
name: cc-go-project-standard
description: "Use when Go module/workspace organization, package ownership, error and context conventions, dependency boundaries or engineering validation need design or review."
---

# Go project engineering

Apply to libraries, CLI tools, desktop cores and services. Determine the application role from the actual project; a frontend/backend product name does not constrain the language.

Locate go.work and the nearest go.mod; preserve module import paths and dependency versions. Do not run a root-level go get simply because the task is in a submodule.

## Apply the workflow

1. Locate the actual project, task boundary and existing contracts; load only the language and domain material needed now.
2. Apply the [specialist checks](references/practice.md), establishing the input evidence before selecting the smallest change.
3. Verify affected behavior with existing repository tools. Explicitly report missing tools, environments or execution; a plan is not a passing result.
4. Deliver scope, specialist decisions, actual verification and remaining risk. A review-only task stays read-only.

## Task boundary

A focused goroutine/channel lifecycle defect belongs to the concurrency specialty.

## Engineering practices

Read the [local engineering decisions](references/engineering-practices.md) for this task and follow their links to relevant shared principles. Apply levels and exceptions against actual project contracts; product frontend/backend labels do not constrain language or role.
