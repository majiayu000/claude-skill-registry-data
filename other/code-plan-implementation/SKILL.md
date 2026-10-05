---
name: code-plan-implementation
description: Generate implementation plans. Use when asked to plan how to implement a feature, fix, integration, or code change before modifying files.
---

Generate an actionable implementation plan based on task analysis and research.

## Process

### Step 1 - Identify Context

- Inspect changed files with `jj diff -s`; restrict with `jj diff -- path`.
- Focus on user-specified files or paths.
- Understand expected behavior, constraints, and verification requirements.

### Step 2 - Research and Scout

- When the task introduces new modules, interfaces, or abstractions, read the `john-ousterhout-software-design` reference and evaluate at least two design alternatives against its principles (deep modules, information hiding, pull complexity downward, design-it-twice).
- When structuring business logic, data access, or persistence layers, read the `martin-fowler-eaa-patterns` reference and choose appropriate domain-logic (Transaction Script / Domain Model / Table Module / Service Layer), data-source (Active Record vs Data Mapper), and O/R mapping patterns rather than inventing ad-hoc structure.

Apply a scout lens to analyze affected code areas, existing patterns, tests, architecture, integration points, and local conventions for {task}:

- Map relevant files, conventions, and call paths; cite file paths and line numbers.
- Distinguish confirmed patterns from one-offs; stay read-only and task-relevant.

Apply a researcher lens to research official documentation, best practices, constraints, migration considerations, and security guidance relevant to {task}:

- Prefer official documentation over blog posts; cite sources with URLs.
- Separate confirmed facts from plausible interpretations; note version requirements.
- Lead with the single most actionable recommendation.

- For large or cross-module tasks, apply an architect lens to analyze module boundaries, ownership, data flow, dependency direction, and structural invariants for {task}:
  - Map current boundaries, ownership, and dependency direction first.
  - Recommend the smallest architecture that preserves invariants.
  - Avoid speculative generality.

Apply a planner lens to design a minimal implementation plan for {task}, including alternatives and tradeoffs:

- Prefer simple, boring solutions; preserve existing project patterns.
- Make tradeoffs and assumptions explicit; scope to the current problem.

Apply a reviewer lens to review the proposed direction for security, correctness, simplicity, and project-convention risks for {task}:

- Ground findings in file paths and line numbers; prioritize the requested lens.
- Distinguish confirmed findings from speculative risks; explain why each issue matters.

### Step 3 - Adjudicate Decisions

- For high-impact or conflicting design choices, apply an oracle lens to adjudicate the conflicting recommendations for {task}:
  - Identify the decision; state assumptions and constraints.
  - Pick the smallest safe path that preserves future options.
  - Note what evidence would change the recommendation.

### Step 4 - Audit

- For production-bound changes, apply an auditor lens to audit the implementation plan for {task} for production risks:
  - Correctness, security, data loss, migration hazards, and rollback safety.
  - Flag only material risk; this is a final gate, not iterative style review.

### Step 5 - Validate Findings

- Read the relevant code directly to validate findings.

### Step 6 - Design Implementation

- Define a minimal approach, incorporating architecture and audit analysis when present.
- Identify target files and integration points; align verification with project-specific tooling.
- Prioritize simple, no-code, or boring solutions; avoid premature abstractions; favor fewer, deeper modules; avoid speculative generality.

### Step 7 - Report

1. **Context Analysis** — relevant code structure, patterns, existing architectural decisions, integration points.
2. **Security Considerations** — threats and secure patterns relevant to the plan.
3. **Documentation & Best Practices**:
   - Relevant docs or API constraints.
   - Common pitfalls.
   - Recommended libraries/tools with rationale, if any.
4. **Simplicity Constraint**:
   - No-code or simpler alternatives.
   - Over-engineering risks.
   - Minimal viable scope.
5. **Design / Architecture** — high-level approach, module boundaries and interfaces, tradeoffs.
6. **Implementation Plan** — numbered concrete steps, file targets, verification strategy.

Prioritize actionable, specific guidance over abstract advice.
