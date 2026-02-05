---
name: validation-trigger
description: Natural language wrapper for validation commands - automatically triggers /validate-and-fix when users request quality checks, linting, or auto-fixes
schema_version: 1.0
---

# validation-trigger

**Type:** WRITE-CAPABLE
**DAIC Modes:** IMPLEMENT only
**Priority:** Medium

## Trigger Reference

This skill activates on:
- **Keywords:** "fix linting", "validate code", "quality check", "auto-fix", "run quality checks", "fix issues", "lint", "format code", "fix formatting"
- **Intent Patterns:** `(fix|validate|check).*(lint|quality|code|issues)`, `auto.*?fix`, `quality.*?(check|validate)`, `run.*?checks`, `(format|lint).*?code`

From: `skill-rules.json` - validation-trigger configuration

## Purpose

Automatically trigger validation and auto-fix commands (`/validate-and-fix`) when users request code quality checks or automatic fixes using natural language.

## Core Behavior

When activated in IMPLEMENT mode:

1. **Validation Intent Detection**
   - Detect quality check and auto-fix requests
   - Route to validation command

2. **Command Invocation**
   - "fix linting" → `/validate-and-fix`
   - Command runs linting, type checks, tests, and auto-fixes issues

## Natural Language Examples

**Triggers this skill:**
- ✓ "Fix linting errors"
- ✓ "Validate code quality"
- ✓ "Auto-fix issues"
- ✓ "Run quality checks"
- ✓ "Format code"

## Safety Guardrails

**WRITE-CAPABLE RULES:**
- ✓ Only execute in IMPLEMENT mode
- ✓ Verify active task before auto-fixing
- ✓ Command modifies files to fix issues
