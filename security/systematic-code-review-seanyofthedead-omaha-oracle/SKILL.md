---
name: systematic-code-review
description: |
  4-phase code review methodology: UNDERSTAND changes, VERIFY claims against
  code, ASSESS security/performance/architecture risks, DOCUMENT findings with
  severity classification. Use when reviewing pull requests, auditing code
  before release, evaluating external contributions, or pre-merge verification.
  Use for "review PR", "code review", "audit code", "check this PR", or
  "review my changes". Do NOT use for writing new code or implementing features.
version: 2.0.0
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
routing:
  triggers:
    - "review code"
    - "code review methodology"
  category: code-review
---

# Systematic Code Review Skill

Systematic 4-phase code review: UNDERSTAND changes, VERIFY claims against actual behavior, ASSESS security/performance/architecture risks, DOCUMENT findings with severity classification. Each phase has an explicit gate that must pass before proceeding because skipping phases causes missed context, incorrect conclusions, and incomplete risk assessment.

## Instructions

### Phase 1: UNDERSTAND

**Goal**: Map all changes and their relationships before forming any opinions.

**Step 1: Read CLAUDE.md**
- Read and follow repository CLAUDE.md files first because project conventions override default review criteria and may define custom severity rules, approved patterns, or scope constraints.

**Step 2: Read every changed file**
- Use Read tool on EVERY changed file completely because reviewing summaries or reading partial files misses dependencies between changes and leads to incorrect conclusions.
- Map what each file does and how changes affect it.
- Check affected dependencies and identify ripple effects because changes in one file can break consumers that aren't in the diff.

**Step 3: Identify dependencies**
- Use Grep to find all callers/consumers of changed code.
- Note any comments that make claims about behavior (these are claims to verify in Phase 2, not facts to trust).

**Step 3a: Caller Tracing** (mandatory when diff modifies function signatures, parameter semantics, or introduces sentinel/special values)

When the change modifies how a function/method is called or what parameters mean:

1. **Find ALL callers** -- Grep for the function name with receiver syntax across the entire repo.
2. **Trace the VALUE SPACE** -- For each parameter source, classify what values can flow through:
   - Query parameters: user-controlled -- ANY string including sentinel values
   - Auth token fields: server-controlled (UUIDs, structured IDs)
   - Constants/enums: fixed set
3. **Verify each caller** -- For each call site, check that parameters are validated before being passed.
4. **Report unvalidated paths** -- Any caller that passes user input to a security-sensitive parameter without validation is a BLOCKING finding.
5. **Do NOT trust PR descriptions** about who calls the function -- verify independently.

**Step 4: Document scope**

```
PHASE 1: UNDERSTAND

Changed Files:
  - [file1.ext]: [+N/-M lines] [brief description of change]

Change Type: [feature | bugfix | refactor | config | docs]

Scope Assessment:
  - Primary: [what's directly changed]
  - Secondary: [what's affected by the change]
  - Dependencies: [external systems/files impacted]

Caller Tracing (if signature/parameter semantics changed):
  - [function/method]: [N] callers found
    - [caller1:line] -- parameter validated: [yes/no]
  - Unvalidated paths: [list or "none"]
```

**Gate**: All changed files read, scope fully mapped, callers traced (if applicable). Proceed only when gate passes.

### Phase 2: VERIFY

**Goal**: Validate all assertions in code, comments, and PR description against actual behavior.

**Step 1: Run tests**
- Execute existing tests for changed files because review cannot approve without test execution.
- Capture complete test output. Show the output rather than describing it.
- Verify test coverage: confirm tests exist for the changed code paths.

**Step 2: Verify claims**
- Check every comment claim against code behavior because comments frequently become outdated.
- Verify edge cases mentioned are actually handled.
- Trace through critical code paths manually.

**Step 3: Document verification**

```
PHASE 2: VERIFY

Claims Verification:
  Claim: "[Quote from comment or PR description]"
  Verification: [How verified]
  Result: VALID | INVALID | NEEDS-DISCUSSION

Test Execution:
  $ [test command]
  Result: [PASS/FAIL with summary]
```

**Gate**: All assertions verified against actual behavior. Tests executed with output captured.

### Phase 3: ASSESS

**Goal**: Evaluate security, performance, and architectural risks specific to these changes.

**Step 1: Security assessment**
- Evaluate OWASP top 10 against changes.
- Explain HOW each vulnerability was ruled out.

**Step 2: Performance assessment**
- Check for N+1 queries, unbounded loops, unnecessary allocations.

**Step 3: Architectural assessment**
- Compare patterns to existing codebase conventions.
- Assess breaking change potential.

**Step 4: Extraction severity escalation**
- If the diff extracts inline code into named helper functions, re-evaluate all defensive guards.
- A missing check rated LOW as inline code becomes MEDIUM as a reusable function.

**Step 5: Document assessment**

```
PHASE 3: ASSESS

Security Assessment:
  SQL Injection: [N/A | CHECKED | ISSUE]
  XSS: [N/A | CHECKED | ISSUE]
  Input Validation: [N/A | CHECKED | ISSUE]
  Auth: [N/A | CHECKED | ISSUE]

Performance Assessment:
  Findings: [specific issues or "No performance issues found"]

Risk Level: LOW | MEDIUM | HIGH | CRITICAL
```

**Gate**: Security, performance, and architectural risks explicitly evaluated.

### Phase 4: DOCUMENT

**Goal**: Produce structured review output with clear verdict and rationale.

Report facts without self-congratulation. When classifying severity, use the Severity Classification Rules and classify UP when in doubt.

```
PHASE 4: DOCUMENT

Review Summary:
  Files Reviewed: [N]
  Lines Changed: [+X/-Y]
  Test Status: [PASS/FAIL/SKIPPED]
  Risk Level: [LOW/MEDIUM/HIGH/CRITICAL]

Findings:

BLOCKING (cannot merge):
  1. [Issue with file:line reference]

SHOULD FIX (fix unless urgent):
  1. [Issue with file:line reference]

SUGGESTIONS (author's choice):
  1. [Suggestion with benefit]

Verdict: APPROVE | REQUEST-CHANGES | NEEDS-DISCUSSION
Rationale: [1-2 sentences]
```

**Gate**: Structured review output with clear verdict. Review is complete.

---

## References

- [Severity Classification](references/severity-classification.md) -- Full classification tables and decision tree
- [Go Review Patterns](references/go-review-patterns.md) -- Go-specific patterns that linters miss
- [Receiving Feedback](references/receiving-feedback.md) -- How to handle review feedback
