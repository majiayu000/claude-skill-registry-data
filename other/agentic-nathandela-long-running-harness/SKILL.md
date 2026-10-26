---
name: Agentic Codebase
description: Audit and set up a codebase for agentic AI development using the 15-principle manifesto
---

# Agentic Codebase Skill

## Overview

Assess and improve a codebase's readiness for AI agent collaboration. Based on the 15-principle Agentic Codebase Manifesto organized across 3 pillars.

This skill operates in two modes:
- **Mode: audit** -- Score the codebase against all 15 principles, produce a report with evidence and prioritized actions
- **Mode: setup** -- Run audit first, then incrementally fill gaps with real content generated from codebase analysis

Mode is set by the calling command (\`/compound:agentic-audit\` or \`/compound:agentic-setup\`). The command wrapper tells you which mode to run -- do not parse \`$ARGUMENTS\` for mode detection.

## Stack Detection

Before auditing, detect the project stack to adapt checks:
1. Look for package.json (Node/TS), pyproject.toml or setup.py (Python), Cargo.toml (Rust), go.mod (Go), Makefile, CMakeLists.txt (C/C++)
2. Check for framework markers: next.config, django, fastapi, express, etc.
3. Identify build/test/lint commands from config files
4. Store detected stack for use in principle checks and AGENTS.md generation

## Audit Methodology

### Scoring Rubric
Each principle is scored:
- **0 (Absent)**: No evidence of this principle in the codebase
- **1 (Partial)**: Some evidence but incomplete or inconsistent
- **2 (Present)**: Clear, consistent implementation

Adapt criteria to the detected stack. For example: "strict mode" means TypeScript strict, Python mypy --strict, or Rust default safety. "Linter" means ESLint, pylint/ruff, clippy, golangci-lint, etc. Score based on the ecosystem's equivalent tooling.

### The 15 Principles

#### Pillar I: Codebase Memory (Traceability) -- max 8 points

**P1. Repository is the only truth**
Check: All context an agent needs lives in version control
Evidence: Look for docs/ directory, inline documentation, config files
Score 0: No docs directory, no README beyond boilerplate
Score 1: README exists but key context lives elsewhere
Score 2: Comprehensive docs/, config, and context all in-repo

**P2. Trace decisions, not just outcomes**
Check: Architectural decisions have recorded rationale
Evidence: Look for docs/adr/, docs/decisions/, ADR files
Score 0: No decision records
Score 1: Some decisions documented but inconsistent format
Score 2: ADR directory with structured records

**P3. Never answer the same question twice**
Check: Solutions/fixes are documented to prevent rediscovery
Evidence: Solutions docs, post-mortems, troubleshooting guides, or a memory system
Score 0: No solutions documentation
Score 1: Scattered notes but no systematic approach
Score 2: Structured solutions docs or integrated memory system

**P4. Knowledge is infrastructure**
Check: Documentation is versioned alongside code
Evidence: Specs, research, standards co-located in repo
Score 0: Documentation lives outside version control
Score 1: Some docs in repo but key knowledge is external
Score 2: All project knowledge versioned in docs/

#### Pillar II: Implementation Feedbacks (Mechanical Verification) -- max 8 points

**P5. Test is specification**
Check: Tests define behavior before or alongside implementation
Evidence: Test files, coverage tooling, test-first patterns
Score 0: No tests or minimal coverage
Score 1: Tests exist but post-hoc or inconsistent
Score 2: Comprehensive test suite with test-driven patterns

**P6. Constraints are multipliers**
Check: Linters, type checkers, architectural rules configured and enforced
Evidence: ESLint/pylint/clippy config, TypeScript strict mode, CI enforcement
Score 0: No linting or type checking
Score 1: Linter exists but not enforced in CI
Score 2: Strict linting + type checking enforced in CI

**P7. Write feedback for machines**
Check: Error messages, logs, and output are structured for agent consumption
Evidence: Structured logging, clear error messages with context
Score 0: Unstructured logs, generic error messages
Score 1: Some structured logging but inconsistent
Score 2: Structured logging throughout, remediation hints in errors

**P8. Fight entropy continuously**
Check: Active maintenance processes prevent drift
Evidence: Automated formatting, dependency updates, quality monitoring
Score 0: No automated maintenance
Score 1: Basic formatting but no proactive monitoring
Score 2: Automated formatting + dependency updates + quality tracking

#### Pillar III: Mapping the Context (Navigable Structure) -- max 8 points

**P9. Map, not manual**
Check: Entry point document provides a navigable map, not an encyclopedia
Evidence: AGENTS.md, CLAUDE.md, or similar
Score 0: No agent-facing entry point document
Score 1: README exists but not optimized for agents
Score 2: Dedicated AGENTS.md or CLAUDE.md with commands, structure, conventions

**P10. Explicit over implicit, always**
Check: Types, naming, patterns are explicit
Evidence: Type annotations, consistent naming, documented conventions
Score 0: No type annotations, inconsistent naming
Score 1: Some types but gaps, or undocumented conventions
Score 2: Full type coverage, documented naming conventions

**P11. Modularity is non-negotiable**
Check: Single responsibility per file, clear boundaries
Evidence: File sizes, module organization, dependency structure
Score 0: Monolithic files (>500 LOC common), unclear boundaries
Score 1: Some modular structure but large files remain
Score 2: Consistent small files, clear APIs, enforced boundaries

**P12. Structure in layers, govern by inheritance**
Check: Layered architecture with explicit dependency rules
Evidence: Layer separation, import rules, dependency graph
Score 0: No discernible layering
Score 1: Informal layers but no enforcement
Score 2: Explicit layers with enforced dependency directions

#### Cross-Cutting -- max 6 points

**P13. Simplicity compounds**
Check: Prefer boring technologies, minimal abstractions
Evidence: Dependency count, abstraction depth
Score 0: Over-engineered with many abstractions
Score 1: Moderate complexity, some unnecessary abstractions
Score 2: Minimal dependencies, straightforward patterns

**P14. Human designs the system, not the output**
Check: Human effort in system design (tests, docs, constraints)
Evidence: Quality of test harnesses, documentation, CI/CD
Score 0: No investment in development infrastructure
Score 1: Some tooling but gaps in key areas
Score 2: Strong CI, testing framework, documentation system

**P15. Parallelize by decomposition**
Check: Work can be split into independent units
Evidence: Module independence, clear interfaces, minimal coupling
Score 0: Tightly coupled, hard to work on independently
Score 1: Some independent modules but shared state
Score 2: Well-decomposed with clear interfaces

### Audit Execution Steps

1. Run \`ca search "agentic codebase"\` for relevant lessons
2. Detect project stack (see Stack Detection above)
3. Use Glob and Grep to check for evidence of each principle:
   - Glob for: docs/**, *.test.*, *_test.go, test_*.py, *_test.rs, .eslintrc*, AGENTS.md, CLAUDE.md
   - Grep for: type annotations, structured logging, ADR format
   - Read key files: README, config files, sample source files
4. Score each principle (0-2) with specific evidence
5. Aggregate scores by pillar and compute total out of 30
6. Generate prioritized actions (score-0 first, then score-1)
7. Present report to user

### Report Format

Present as markdown tables per pillar:

Pillar I: Codebase Memory -- X/8
| # | Principle | Score | Evidence |
|---|-----------|-------|----------|
| P1 | Repository is the only truth | 0/1/2 | finding |
...repeat for all pillars with separator rows...

**Overall Score: X/30**

### Priority Actions
1. [Score-0 items first, most impactful]
2. ...

After presenting, use \`AskUserQuestion\`: "Create a beads epic with issues for improvements?"
If yes, create epic via bd create and individual issues.

## Setup Methodology

### Prerequisites
Run the full audit first. Setup only addresses gaps found by the audit.

### Setup Execution Steps

1. Present audit findings summary
2. For each principle scored 0 or 1, propose a concrete action:

**P1/P4 gaps**: Create docs/ skeleton (INDEX.md, adr/, standards/) with real content from analysis
**P2 gaps**: Create ADR template and first ADR from actual architecture analysis
**P3 gaps**: Suggest solutions documentation structure
**P5 gaps**: Suggest test framework setup based on detected stack
**P6 gaps**: Suggest linter/type checker configuration for detected stack
**P7 gaps**: Suggest structured logging patterns for detected stack
**P9 gaps**: Generate AGENTS.md by analyzing actual codebase (build commands, structure, conventions)
**P10 gaps**: Suggest type annotation and strict mode settings
**P11 gaps**: Identify files >500 LOC, suggest refactoring targets
**P12 gaps**: Document layer structure and suggest import lint rules (e.g., eslint-plugin-import boundaries, Rust mod visibility)
**P13 gaps**: Flag over-abstraction (deep inheritance, excessive wrappers), suggest simplification targets
**P14 gaps**: Suggest CI pipeline improvements, test harness setup, or pre-commit hooks for detected stack
**P15 gaps**: Identify tightly coupled modules, suggest interface extraction for parallel workability
**P8 gaps**: Suggest automated formatting (prettier/black/rustfmt), dependency update tooling (renovate/dependabot), and quality monitoring

3. Before each action, use \`AskUserQuestion\`: "Create [file]? Preview: [content]"
4. Only create/modify files the user approves
5. Never overwrite existing files without explicit approval

### Setup Completion Gate
After all approved actions are applied, verify:
- List all files created/modified during setup
- Run quality gates if available (\`pnpm test\`, \`pnpm lint\`)
- Confirm no existing files were overwritten without approval
- Present summary: principles addressed, files created, remaining gaps

## Memory Integration

- Before analysis: \`ca search "agentic codebase"\` for relevant lessons
- After completing: offer \`ca learn\` to capture insights

## Common Pitfalls

- Scoring too generously without specific evidence for score 2
- Generating template content instead of analyzing the actual codebase
- Overwriting existing files without asking
- Not detecting the project stack before generating content
- Creating too many files at once instead of prioritizing
- Forgetting to offer beads epic creation after audit

## Quality Criteria

- All 15 principles assessed with specific evidence
- Scores justified with findings
- Pillar totals and overall score calculated correctly
- Actions prioritized (score-0 before score-1)
- Stack detected and checks adapted accordingly
- User consulted via AskUserQuestion at key decisions
- Memory searched before analysis
- Setup mode ran audit first
- No files overwritten without approval
- Generated content based on actual codebase analysis
