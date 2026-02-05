---
name: architect
description: Design system architecture before implementing new features. Use when starting major components or making design decisions with long-term impact.
---

# GATE 1: ARCHITECTURE — META_ARCHITECT PROTOCOL

> **Agent**: META_ARCHITECT
> **Gate**: 1 of 6
> **Prerequisite**: Gate 0 (Problem Definition) COMPLETE
> **Output**: docs/architecture/ARCHITECTURE.md

---

## GATE 1 ENTRY CHECKLIST

Before proceeding, verify:

- [ ] PROJECT_FOUNDATION.md exists and is read
- [ ] Problem statement is clear (from Gate 0)
- [ ] Success criteria are measurable (from Gate 0)
- [ ] No prior Gate 1 exists (or explicit re-architecture requested)

**If any checkbox fails**: STOP. Complete Gate 0 first.

---

## META_ARCHITECT PROTOCOL

### Step 1: Extract Requirements

From PROJECT_FOUNDATION.md, extract:

```markdown
## REQUIREMENT EXTRACTION

### Functional Requirements
- FR001: [requirement from foundation]
- FR002: [requirement from foundation]
- ...

### Non-Functional Requirements
- NFR001: Detection latency <200ms per package
- NFR002: False positive rate <5%
- NFR003: Support PyPI, npm, crates.io
- ...

### Constraints
- CON001: Python 3.11+ target
- CON002: Minimal dependencies (httpx, typer, pydantic)
- CON003: Works offline (cached mode)
- ...
```

### Step 2: Design System Components

For each major component, define:

```markdown
## COMPONENT: [NAME]

### SPEC_ID: S001

### Purpose
[Why this component exists]

### Interface
```python
# Public API
def validate_package(name: str, registry: str = "pypi") -> PackageRisk:
    """
    IMPLEMENTS: S001
    INVARIANT: INV001 - Return value always has risk_score in [0, 1]
    """
    ...
```

### Data Structures
```python
@dataclass
class PackageRisk:
    """Size: ~200 bytes per instance"""
    name: str           # 8 bytes (pointer)
    risk_score: float   # 8 bytes
    signals: list[str]  # 8 bytes (pointer)
    recommendation: Recommendation  # 1 byte (enum)
```

### Invariants
- INV001: risk_score is always in range [0.0, 1.0]
- INV002: signals list is never None (empty list if no signals)

### Dependencies
- Depends on: RegistryClient
- Used by: CLI, Hooks

### Performance Budget
- Single call: <200ms (uncached)
- Cached call: <10ms
```

### Step 3: Define Performance Budget

```markdown
## PERFORMANCE BUDGET

| Operation | Budget | Constraint | Measurement |
|:----------|:-------|:-----------|:------------|
| validate_package (uncached) | <200ms | P99 | bench_validate |
| validate_package (cached) | <10ms | P99 | bench_validate_cached |
| batch_validate (50) | <5s | P99 | bench_batch |
| pattern_match | <1ms | P99 | bench_pattern |
| registry_api_call | <500ms | P99 | network dependent |

### Memory Budget
| Structure | Size | Max Instances | Total |
|:----------|:-----|:--------------|:------|
| PackageRisk | 200B | 1000 | 200KB |
| PatternDB | 50KB | 1 | 50KB |
| Cache | 10MB | 1 | 10MB |
```

### Step 4: Create Invariant Registry

```markdown
## INVARIANT REGISTRY

| INV_ID | Statement | Enforcement | Test Type |
|:-------|:----------|:------------|:----------|
| INV001 | "risk_score in [0.0, 1.0]" | property test | proptest |
| INV002 | "signals never None" | type system | unit |
| INV003 | "cache TTL honored" | timer mock | unit |
| INV004 | "API timeout <500ms" | timeout config | integration |
| INV005 | "No network in offline mode" | mock assert | unit |
```

### Step 5: Document Decisions

Every architectural decision MUST follow this template:

```markdown
## DECISION: [SPEC_ID] - [Title]

### Context
[What led to this decision]

### Options Considered
1. [Option A] - pros/cons
2. [Option B] - pros/cons
3. [Option C] - pros/cons

### Decision
[The chosen option and why]

### Consequences
- Positive: [benefits]
- Negative: [trade-offs]
- Neutral: [observations]

### Verification
- How we'll know this was right
- Metrics to track
- Rollback criteria

### Trace Links
- Related specs: [SPEC_IDs]
- Test requirements: [TEST_IDs]
```

---

## ARCHITECTURE DOCUMENT TEMPLATE

The output MUST follow this structure:

```markdown
# Phantom Guard — System Architecture

> **Version**: 0.1.0
> **Date**: YYYY-MM-DD
> **Status**: DRAFT | REVIEW | APPROVED
> **Approver**: [name] | PENDING

---

## 1. Overview

### 1.1 System Purpose
[From PROJECT_FOUNDATION.md]

### 1.2 Architecture Diagram
```
┌─────────────────────────────────────────────────────────┐
│                    Phantom Guard                         │
├─────────────────────────────────────────────────────────┤
│  CLI Layer                                               │
│  ├── typer CLI                                          │
│  └── IMPLEMENTS: S010-S015                              │
├─────────────────────────────────────────────────────────┤
│  Core Layer                                              │
│  ├── Detector (S001-S005)                               │
│  ├── Analyzer (S006-S009)                               │
│  └── Cache (S020-S025)                                  │
├─────────────────────────────────────────────────────────┤
│  Registry Layer                                          │
│  ├── PyPI Client (S030-S035)                            │
│  ├── npm Client (S040-S045)                             │
│  └── crates.io Client (S050-S055)                       │
└─────────────────────────────────────────────────────────┘
```

## 2. Component Specifications

### 2.1 Core Detection Engine
[SPEC_ID: S001-S005]
...

### 2.2 Registry Clients
[SPEC_ID: S030-S055]
...

### 2.3 CLI Interface
[SPEC_ID: S010-S015]
...

## 3. Data Structures

### 3.1 Core Types
[With sizes, invariants]

### 3.2 API Contracts
[Request/response formats]

## 4. Performance Budget
[Table from Step 3]

## 5. Invariant Registry
[Table from Step 4]

## 6. Architectural Decisions
[ADR format from Step 5]

## 7. Security Considerations
- Input validation
- No shell execution
- API key handling

## 8. Trace Matrix
| SPEC_ID | Description | Component | Tests |
|---------|-------------|-----------|-------|
| S001 | Package validation | Detector | T001.* |
| ... | ... | ... | ... |

---

## Appendix A: Open Questions
[List any unresolved decisions]

## Appendix B: Future Considerations
[Explicitly out of scope but noted]
```

---

## GATE 1 EXIT CHECKLIST

Before Gate 1 is complete:

- [ ] docs/architecture/ARCHITECTURE.md exists
- [ ] Every component has SPEC_ID
- [ ] Every data structure has size estimate
- [ ] Every public function documented
- [ ] Performance budget defined for all operations
- [ ] Invariant registry complete
- [ ] All decisions have ADR format
- [ ] Security considerations documented
- [ ] HOSTILE_ARCHITECT review requested

**If any checkbox fails**: DO NOT PROCEED TO GATE 2.

---

## HOSTILE_ARCHITECT REVIEW

After completing the architecture document, invoke hostile review:

```
/hostile-review architecture
```

The reviewer will check:
- Are there gaps in the design?
- Are invariants actually enforceable?
- Are performance budgets realistic?
- Are there security holes?
- Are there missing edge cases?

**Only after HOSTILE_ARCHITECT approval can Gate 1 be marked complete.**

---

## RECORDING GATE COMPLETION

After approval, create:

```markdown
# .fortress/gates/GATE_1_ARCHITECTURE.md

## Gate 1: Architecture — COMPLETE

**Date**: YYYY-MM-DD
**Approver**: HOSTILE_ARCHITECT
**Output**: docs/architecture/ARCHITECTURE.md

### Summary
[Brief summary of architecture]

### Key Decisions
- [Decision 1]
- [Decision 2]

### Known Risks
- [Risk 1]
- [Risk 2]

### Next Gate
Gate 2: Specification
```

---

## PROTOCOL VIOLATIONS

If any of these occur, STOP:

| Violation | Response |
|:----------|:---------|
| No SPEC_ID on component | Add SPEC_ID |
| No performance budget | Define budget |
| No invariant registry | Create registry |
| Skipped HOSTILE review | Run /hostile-review |
| Proceeding to Gate 2 without approval | BLOCKED |

---

*Gate 1 is about DESIGNING the solution. Gate 2 is about SPECIFYING the details.*
