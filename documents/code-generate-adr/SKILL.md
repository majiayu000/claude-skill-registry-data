---
name: code-generate-adr
description: Create an Architecture Decision Record. Use when asked to write or draft an ADR for an architectural or technical decision.
---

Create ADRs that match existing project conventions.

## Process

### Step 1 - Identify Context

- If code changes are involved, run `jj diff -s` for changed files and `jj diff -- path` to restrict scope.
- Focus on user-specified decisions, alternatives, constraints, or consequences.
- Ask for missing Context, Decision, or Consequences if necessary.

### Step 2 - Research and Plan

#### Standard Analysis

Apply a scout lens to identify existing ADR style, naming, structure, status values, and relevant architectural context for {files or requirements}:

- Map relevant files, conventions, and call paths.
- Cite file paths and line numbers.
- Distinguish confirmed patterns from one-offs.
- Stay read-only.
- Keep it concise and task-relevant.

Apply a planner lens to draft the minimal ADR structure for decision, alternatives, consequences, and tradeoffs:

- Prefer simple, boring solutions.
- Preserve existing project patterns.
- Make tradeoffs and assumptions explicit.
- Scope the plan to the current problem.

Apply a reviewer lens to review the proposed ADR for clarity, convention fit, decision focus, and unnecessary detail:

- Ground findings in file paths and line numbers.
- Prioritize the requested lens.
- Distinguish confirmed findings from speculative risks.
- Explain why each issue matters.

#### Advanced Analysis

- For ADRs with structural or cross-module implications:
  - Apply an architect lens to analyze module boundaries, ownership, and structural implications of the decision in {task}, identifying invariants and compatibility risks:
    - Map current module boundaries, ownership, and dependency direction first.
    - Recommend the smallest architecture that preserves invariants.
    - Avoid speculative generality.
  - Apply an auditor lens to audit the decision for production risks: data loss, migration hazards, rollback safety, and contract compatibility:
    - Flag only material risk — correctness bugs, security holes, data loss, migration hazards, rollback safety, contract compatibility.
    - This is a final gate, not iterative style review.

### Step 3 - Inspect Conventions

- Locate any existing ADR directory and naming conventions; inspect neighboring ADRs for title format, status values, headings, and detail level.
- Check `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `GEMINI.md`, or `CODEX.md`.

### Step 4 - Create ADR

- Use the project's ADR directory and naming conventions if present; otherwise propose `doc/adr/` or `docs/adr/` before creating a new structure.
- Include Title, Status, Context, Decision, Consequences, and Alternatives where appropriate.
- Keep a factual, decision-oriented record; avoid implementation logs or changelog-style text.
- Capture tradeoffs and rejected alternatives to clarify rationale.

### Step 5 - Verify

- Run configured formatting, markdown linting, doc builds, or link checks if available.
- Otherwise, review generated docs for accuracy against current code.

### Step 6 - Report

Report to the user:

1. **Decision Captured**
2. **Conventions Detected**
3. **ADR Added / Files Changed**
4. **Verification Results**
5. **Remaining Follow-up**
