---
name: repo-analysis
description: Techniques for deep-diving into unknown codebases. Focuses on dependency graphs, data flow, and architectural patterns. Use when starting a task in an unfamiliar project.
version: "1.0.0"
verified_date: 2026-04-29
category: core
---

# Repository Analysis

## Purpose
Rapidly gain a comprehensive understanding of a project's architecture, dependencies, and internal logic.

## When to Use This Skill
Use during the first 15 minutes of any task in a project that has not been previously analyzed.

## Phase 1: Structural Audit
1. **Map the directory structure**: Use the `list_dir` or `mcp_filesystem_directory_tree` tools. Do not use `ls` via bash.
2. **Identify core technologies**: Read `package.json`, `requirements.txt`, etc., using `mcp_filesystem_read_text_file`.

## Phase 2: Logic Flow Analysis
1. **Trace entry points**: Use `grep_search` to map `import` trees and function calls. Never use `grep` inside a bash command.
2. **Monorepo Scale Analysis**: For massive monolithic repositories, avoid raw exhaustive grep. Use AST (Abstract Syntax Tree) parsing or vector-based codebase search if available to prevent context limit exhaustion.
2. **Data Model Discovery**: Identify the main data models and state management strategy.
- [ ] Did I identify the true root cause, or just a symptom?
- [ ] Is the proposed change isolated, or will it break upstream logic?

## Output Format / Delivery
- A concise context mapping report.
- A targeted execution plan for fixes.

## Behavior Rules
1. **Trust but Verify**. Do not rely on outdated READMEs; check the actual code.
2. **Document Findings**. Save a summary of the project's "mental model" in artifacts.

## Maintenance Notes
- Initial global core skill.
