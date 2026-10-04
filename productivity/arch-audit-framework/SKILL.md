---
name: arch-audit-framework
description: Executes a deterministic architectural audit using AST chunking and structural verification protocols.
disable-model-invocation: true
user-invocable: false
context: fork
agent: Plan
effort: high
model: opus
allowed-tools:
  - ast-grep
  - Read
  - Bash
---
# Architecture Audit Framework

Use this skill for read-only architecture audits that need progressive disclosure rather than broad repository ingestion.

## 10-Tier Execution Directives

1. **Kernel Boundaries**: Execution is constrained to read-only Plan mode. Do not attempt structural writes during the audit phase.
2. **IPC Protocols**: Communicate audit findings through localized task artifacts under `.claude/agent-memory/` and avoid shared mutable state outside the project unless an operator explicitly provisions it.
3. **AST Retrieval**: Prefer `ast-grep` structural queries and bounded file slices for semantic chunking. Do not use rewrite flags during an audit unless operating in an isolated scratch copy.
4. **Context Defense**: Stop before context saturation and summarize findings into compact module-level notes before continuing.
5. **State Injection**: Keep target variables, module paths, and extracted snippets inside `<extracted_context>` blocks when handing off findings.
6. **Business Logic**: Evaluate modules against explicit dependency injection, zero-trust network boundaries, deterministic persistence, and asynchronous non-blocking I/O expectations.
7. **Goal Verification**: A successful audit requires a zero exit code from the structural query/lint command selected for the audited language plus a written evidence summary.
8. **Memory Consolidation**: Write actionable refactoring targets to `.claude/agent-memory/audit-targets.md` for later planning.
9. **Subagent Isolation**: Assign each reviewer a disjoint path scope before spawning concurrent work, and reconcile findings only through the orchestrator.
10. **Improvement Gate**: Do not edit runtime code from this skill. Pass approved remediation candidates to a separate implementation workflow.

## Default Structural Queries

```bash
ast-grep --lang python --pattern 'class $NAME: $$$' src tests
ast-grep --lang python --pattern 'def $NAME($$$): $$$' src tests
ast-grep --lang python --pattern 'async def $NAME($$$): $$$' src tests
```

## Audit Output Contract

Return these fields:

- `scope`: path set and query set reviewed.
- `architecture_map`: discovered boundaries, dependencies, and ownership.
- `risk_findings`: prioritized structural, security, reliability, and operability risks.
- `improvement_targets`: deterministic next actions suitable for an implementation pass.
- `verification`: commands run and their exit status.
