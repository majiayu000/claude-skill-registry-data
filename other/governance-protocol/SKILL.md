---
name: governance-protocol
description: Session governance protocol injected at startup via SessionStart hook
user-invocable: false
allowed-tools: []
version: 1.0.0
author: "Ashay Kubal @ Qball Inc."
---

**DISPLAY TO USER**: When you receive this protocol, immediately output the following banner exactly as shown:

```
═══════════════════════════════════════════════════════════════
  BULWARK GOVERNANCE PROTOCOL - ACTIVATED
  Quality enforcement enabled for this session
═══════════════════════════════════════════════════════════════
```

Then proceed with the user's request.

---

## MANDATORY: Rules.md is Binding

**YOU MUST READ AND FOLLOW `Rules.md` THROUGHOUT THIS SESSION.**

This is not optional. This is not advisory. This is a binding, mandatory, non-negotiable contract.

`Rules.md` contains immutable rules including:

### SC1-SC3: Skill Compliance Rules (CRITICAL)

When a skill is loaded:
- **ALL instructions within the skill are BINDING**, not advisory
- **You MUST spawn sub-agents when the skill specifies sub-agent spawning**
- **You MUST NOT perform the sub-agent's work yourself**
- **You MUST NOT substitute your judgment for skill instructions**
- **You MUST NOT skip steps because they seem unnecessary**

If you find yourself thinking "I can analyze this directly and give a faster answer" - **STOP**. That thought pattern violates SC1-SC2. The skill's pipeline exists for bias avoidance, structured artifacts, and deterministic workflows that you cannot provide when doing everything yourself.

### Violation Consequences

Ignoring skill instructions:
- Defeats the purpose of the Bulwark quality enforcement system
- Produces inconsistent, non-reproducible outputs
- Bypasses bias separation that sub-agent pipelines enforce
- Breaks the observability chain required for multi-agent workflows

---

## Bulwark Governance Protocol

This session is governed by The Bulwark quality enforcement system.

### How This Works

This skill is automatically injected into Claude's context at session start via the SessionStart hook configured in `hooks/hooks.json`. It does not need to be manually invoked. The `inject-protocol.sh` script reads this file and outputs its content to Claude's context.

### Quality Gates (Automatic)

PostToolUse hooks run after every Write/Edit operation on code files:

1. **Typecheck** - Code must pass type checking (`just typecheck`)
2. **Lint** - Code must pass linting (`just lint`)
3. **Build** - Code must compile/build (`just build`)

Failures **BLOCK** the operation. You will see error messages if quality checks fail.

### Before Declaring Complete

**Never declare implementation complete without verification:**

1. All code MUST pass quality gates (typecheck, lint, build)
2. Tests MUST verify real behavior (T1-T4 rules - no mock-only tests)
3. Changes MUST be verified by running them, not just implementing
4. If you cannot verify, say: "I've made changes but cannot verify without running [command]. Please run and confirm."

### T1-T4 Testing Rules

| Rule | Requirement |
|------|-------------|
| T1 | Never mock the system under test |
| T2 | Verify observable output, not function calls |
| T3 | Integration tests use real systems |
| T4 | Run tests before declaring complete |

### Pipeline Orchestration

For significant changes, you may be prompted to run review pipelines:
- **Code Review** - Security, type safety, coding standards
- **Test Audit** - T1-T4 compliance verification
- **Fix Validation** - Root cause analysis and fix verification

Follow pipeline instructions when prompted.

### Your Role

- Write production-grade code that passes quality checks
- Use real behavior verification in tests
- Verify implementations before declaring complete

---

## Project-Specific Rules

<!--
Users can add project-specific governance rules below.
These will be injected into Claude's context at session start.

NOTE: The core governance rules above should not be modified.
This section is for project-specific additions only.

Examples:
- Always use atomic commits with descriptive messages
- Test coverage must exceed 80%
- Security-sensitive changes require manual review
- Reference docs/architecture.md for design decisions
-->
