---
name: shell-development
description: "Use when implementing a shell, command interpreter, or scripting runtime that parses and executes user commands to define the grammar and authority model before execution, keep parsing separate from effects, and test in a disposable environment with a minimal command set. Trigger for pipelines, redirection, expansion, job control, or shell compatibility work."
---

# Shell Development

## Overview

This skill applies when implementing a shell, command interpreter, or scripting runtime that parses and executes user commands. Its intended outcome is to define the grammar and authority model before execution, keep parsing separate from effects, and test in a disposable environment with a minimal command set.

## When to Use

### Preserved source section: When to Use

Use for an interactive or scripted command interpreter. State which shell syntax is supported and whether commands are simulated, built-in, or launched as host processes.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Safety and Acceptance

Do not run tests that execute arbitrary user-supplied commands on the host. Keep destructive operations and network access disabled by default in a prototype. Accept the declared grammar only when parse results, quoting, error behavior, and execution boundaries are covered by tests.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Grammar and compatibility target, including quoting, expansions, pipes, and redirection.
- Command registry, environment, working-directory semantics, and permission boundary.
- Disposable fixtures and tests for process lifecycle, signals, and output streams.

## Instructions

### Preserved source section: Procedure

1. **Specify syntax before execution.** Define tokens, quoting, comments, expansion order, operators, and parse errors. Build a parser that produces an inspectable command representation.
2. **Separate plan from effects.** Parse and validate a whole command before opening files or starting processes. Represent pipelines and redirections explicitly.
3. **Start with safe built-ins.** Implement a small allowlisted command set or a simulator before enabling arbitrary host process execution.
4. **Constrain expansion.** Make variable, glob, substitution, and path behavior explicit. Avoid evaluating text through a second shell or implicit `eval`.
5. **Manage processes correctly.** Specify exit status, signal forwarding, child cleanup, foreground/background behavior, and timeout limits.
6. **Test quoting and hazards.** Cover spaces, empty strings, metacharacters, redirection failures, pipeline errors, interrupted commands, and malicious-looking input in a sandbox.
7. **Document authority.** Clearly state which commands can access files, networks, and credentials and how users grant or revoke that capability.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Safety and Acceptance

Do not run tests that execute arbitrary user-supplied commands on the host. Keep destructive operations and network access disabled by default in a prototype. Accept the declared grammar only when parse results, quoting, error behavior, and execution boundaries are covered by tests.

## Output Format

Not specified in source skill.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

1. **Specify syntax before execution.** Define tokens, quoting, comments, expansion order, operators, and parse errors. Build a parser that produces an inspectable command representation.
5. **Manage processes correctly.** Specify exit status, signal forwarding, child cleanup, foreground/background behavior, and timeout limits.
6. **Test quoting and hazards.** Cover spaces, empty strings, metacharacters, redirection failures, pipeline errors, interrupted commands, and malicious-looking input in a sandbox.

### Source edge/failure guidance from: Safety and Acceptance

Do not run tests that execute arbitrary user-supplied commands on the host. Keep destructive operations and network access disabled by default in a prototype. Accept the declared grammar only when parse results, quoting, error behavior, and execution boundaries are covered by tests.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Preserved source section: Safety and Acceptance

Do not run tests that execute arbitrary user-supplied commands on the host. Keep destructive operations and network access disabled by default in a prototype. Accept the declared grammar only when parse results, quoting, error behavior, and execution boundaries are covered by tests.
