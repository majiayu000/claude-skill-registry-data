---
name: build
description: Implementation surge mode — TDD-first, coverage-verified, deslop-checked. For feature builds that must be test-complete before handoff.
version: 1.0.0
execution-mode: remedial
argument-hint: "<feature, module, or spec to implement>"
authority: operator
category: dev-tools
status: candidate
---
# Build Mode Activation

## Chain Admission

When `/build` is part of an explicit multi-skill route, follow
`rules/skill-chain-admission.md` and obtain `ADMIT` from
`scripts/skill-chain-gate.py check` before editing files. `DENY` or `ERROR` is
a hard stop. The admission request must include the operator authorization
required by this skill's frontmatter.

You are operating in **BUILD MODE** — maximum implementation velocity, TDD-first, no speculative abstraction.

## Active Configuration
- **Tempo**: SPRINT (build fast, verify as you go)
- **Autonomy**: Maximum — implement, test, verify, deslop in one pass
- **Pipeline**: Spec → Red → Green → Refactor → Deslop

## Task
$ARGUMENTS

## Build Pipeline

1. **Spec** — confirm what you're building (read existing interfaces, don't invent)
2. **Red** — write failing tests first (`[tdd]`)
3. **Green** — implement the minimum to pass
4. **Refactor** — `[coverage]` to find gaps; fill them
5. **Deslop** — `[deslop]` to eliminate over-engineering; `[type-check]` if Python
6. **Verify** — `[regression-check]` to confirm nothing broken; `[ship-check]` before handoff

## Quick-Access Skills
- **TDD**: `[tdd]`, `[test-run]`, `[coverage]`, `[debug-test]`, `[flake-hunter]`
- **Quality**: `[deslop]`, `[type-check]`, `[complexity-score]`, `[dead-code]`, `[try-except-audit]`
- **Check**: `[regression-check]`, `[ship-check]`, `[dep-check]`, `[mtsmu-review]`
- **Docs**: `[api-docs]`, `[docstring-audit]`, `[readme-gen]`
- **Meta**: `[scope-decompose]`, `[story-write]`

## Rules
- **Tests first** — no implementation without at least one failing test
- **Green before moving** — never leave a red test to "fix later"
- **Stdlib-only** in services/ and integrations/ (no third-party runtime deps)
- **No speculative abstraction** — three similar lines > premature abstraction
- **No security vulnerabilities** — no command injection, no XSS, no SQL injection
- **Minimal surface** — don't add error handling for scenarios that can't happen
- No Ollama on MBP

## Output Contract
End every session with:
1. Files changed (count + paths)
2. Test delta (added / total / passing)
3. Coverage % (if changed)
4. `[deslop]` findings (addressed / deferred)
5. Ready for `[ship]`? (yes/no + blockers)

Begin building now.
