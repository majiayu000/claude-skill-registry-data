---
name: powershell-refactor
description: Refactor existing PowerShell scripts and modules while preserving observable behavior, interfaces, and safety controls.
---
# PowerShell Refactor

## Purpose
Modernize an existing PowerShell script or module with minimal, reviewable changes. Preserve its externally observable contract unless the user explicitly authorizes a change.

## Use when
A user asks to simplify, deduplicate, standardize, or improve maintainability of existing PowerShell code.

## Do not use when
The user requests a new script, an unrelated architecture redesign, or documentation only. Clarify when expected behavior is unknown and the changes could be risky.

## Inputs and baseline
Inspect the actual source, tests, manifest, CI configuration, PSScriptAnalyzer settings, supported PowerShell versions, platform constraints, and dependent callers when accessible. Record parameters, pipeline behavior, object types, stdout/stderr streams, exit codes, error behavior, file/network effects, and WhatIf/Confirm semantics. Distinguish verified facts from assumptions. Never claim tests ran without execution evidence.

## Scope presets
- **naming only:** change naming and casing without unrelated cleanup.
- **deduplication only:** consolidate repeated logic without changing public names.
- **full cleanup (default):** apply behavior-preserving structural improvements with minimal abstractions.
Respect the selected scope and report other findings separately.

## Workflow
1. Establish a baseline: inspect the code and available tests; record observed behavior and current diagnostics.
2. Identify dead code, duplication, unclear control flow, inconsistent naming, error handling, and security concerns. Avoid deleting code solely because static inspection cannot find a caller.
3. Plan the smallest safe patch. Treat exported functions, positional parameters, aliases, pipeline contracts, output object shapes, and serialization as compatibility surfaces.
4. Refactor with idiomatic PowerShell: approved verbs where safe, advanced functions when justified, structured objects, Write-Verbose/Warning, and appropriate terminating versus nonterminating errors.
5. Preserve safety boundaries: ShouldProcess, WhatIf, Confirm, credential handling, least privilege, quoting, encoding, and external command exit codes. Do not introduce Invoke-Expression or unsafe interpolation.
6. Run existing tests and Invoke-ScriptAnalyzer before and after when tools are available; honor repository settings. Prefer Pester and relevant PowerShell editions/platforms. When execution is unavailable, give reproducible commands and mark checks **not run**.
7. Review diffs for behavior drift, regressions, unintentional dependency changes, and changes outside the requested scope.
8. Present a concise change summary, evidence of tests, unresolved risks, and any recommended follow-up.

## Constraints
- Do not invent files, test results, APIs, or repository permissions.
- Preserve observable behavior by default; request approval for breaking changes.
- Never remove safeguards from destructive operations.
- Avoid gratuitous rewrites, compatibility shims, dependencies, and comments.
- Do not expose secrets in output or logs.

## Output contract
Report files changed, changes made, behavior preserved or exceptions, line counts when measured, analyzer findings, test commands and results (pass/fail/not run), and out-of-scope observations. State whether changes were committed or merely proposed.

## Examples
- Refactor a PowerShell reporting script without changing its parameters or output object properties.
- Deduplicate retry logic while preserving timeout and error behavior.
- Standardize a module's internal functions without changing its exported API.

## Validation checklist
- No unintended changes to exported functions, parameters, output types, or side effects.
- Existing tests pass or their unavailability is explicitly reported.
- Analyzer results are verified rather than inferred.
- Security controls and chosen scope are preserved.
