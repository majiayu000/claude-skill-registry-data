---
name: thrunt-ui-phase
description: Generate UI design contract (UI-SPEC.md) for frontend phases
argument-hint: "[phase]"
allowed-tools: Read, Write, Bash, Glob, Grep, Task, WebFetch, AskUserQuestion, mcp__context7__*
---

<objective>
Create a UI design contract (UI-SPEC.md) for a frontend phase.
Orchestrates thrunt-ui-researcher and thrunt-ui-checker.
Flow: Validate → Research UI → Verify UI-SPEC → Done
</objective>

<execution_context>
@.github/thrunt-god/workflows/ui-phase.md
@.github/thrunt-god/references/ui-brand.md
</execution_context>

<context>
Phase number: $ARGUMENTS — optional, auto-detects next unplanned phase if omitted.
</context>

<process>
Execute @.github/thrunt-god/workflows/ui-phase.md end-to-end.
Preserve all workflow gates.
</process>
