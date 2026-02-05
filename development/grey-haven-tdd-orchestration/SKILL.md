---
name: grey-haven-tdd-orchestration
description: "Master TDD orchestration with multi-agent coordination, strict red-green-refactor enforcement, automated test generation, coverage tracking, and >90% coverage quality gates. Coordinates tdd-python, tdd-typescript, and test-generator agents. Use when implementing features with TDD workflow, coordinating multiple TDD agents, enforcing test-first development, or when user mentions 'TDD workflow', 'test-first', 'TDD orchestration', 'multi-agent TDD', 'test coverage', or 'red-green-refactor'."
# v2.0.43: Skills to auto-load for subagents (TDD language specialists)
skills:
  - grey-haven-tdd-typescript
  - grey-haven-tdd-python
  - grey-haven-test-generation
  - grey-haven-code-quality-analysis
# v2.0.74: Orchestrator needs full tool access for coordination
allowed-tools:
  - Read
  - Write
  - MultiEdit
  - Bash
  - Grep
  - Glob
  - Task
  - TodoWrite
---

# TDD Orchestration Skill

Master TDD orchestrator ensuring strict red-green-refactor discipline with multi-agent coordination and comprehensive metrics.

## Description

Orchestrates Test-Driven Development workflows with automated test generation, implementation coordination, coverage tracking, and quality gates.

## What's Included

- **Examples**: Multi-agent TDD workflows, feature implementation with TDD
- **Reference**: TDD best practices, red-green-refactor patterns, coverage strategies
- **Templates**: TDD workflow templates, test planning structures
- **Checklists**: TDD verification, coverage validation

## Use This Skill When

- Implementing features with strict TDD methodology
- Coordinating multiple agents in TDD workflow
- Enforcing test-first development
- Achieving >90% test coverage

## Related Agents

- `tdd-orchestrator` - Multi-agent TDD coordinator
- `tdd-typescript-implementer` - TypeScript/JavaScript TDD
- `tdd-python-implementer` - Python TDD
- `test-generator` - Automated test creation

---

**Skill Version**: 1.0
