---
name: ai-audit
description: |
  SOP for auditing AI-generated code.
  Trigger when:
  - Reviewing, refactoring, or cleaning up AI-generated code to prevent regressions or hallucinated APIs.
  - Prompt contains: /ai-audit, code audit, AI cleanup, common flaws.
---

# AI-Generated Code Audit Workflow

**Verification Dual — adversarial path.** This skill is the applied methodology for the adversarial half of the [Verification Dual](../../rules.md#2-prime-invariants): when no deterministic evaluator can be built for a condition in LLM-generated code, it is closed by decorrelated, context-free agents running this audit protocol from independent attractor basins. Load it whenever the symbolic path is unavailable and an adversarial review of AI-generated code is required.

A 4-layer framework for auditing LLM-generated code. Traditional SAST is insufficient—AI code is syntactically flawless but often logically "hollow."

> **Principle of Zero Trust:** Treat every AI-generated line as a high-risk external contribution.

---

## Layer 1: Inefficiency Taxonomy (ODC Framework)

LLMs prioritize token sequence probability over algorithmic optimization, creating systematic inefficiencies.

> Research shows 0.74 correlation between General Logic failures and Readability/Maintainability issues.

### Orthogonal Defect Classification (ODC)

| Category            | Technical Trigger                                         | The AI-ism                                                     | Remediation                                             |
| :------------------ | :-------------------------------------------------------- | :------------------------------------------------------------- | :------------------------------------------------------ |
| **Algorithm**       | Prime divisibility iterates to `n` instead of `√n`        | Inefficient iterative blocks; overly broad loop conditions     | Narrow loop constraints; implement early stopping       |
| **Algorithm**       | O(n²) logic where O(n log n) is standard                  | Sub-optimal complexity; prioritizes "plausible" over optimal   | Replace with standard library or optimized algorithms   |
| **Assignment**      | Used-before-assignment; shadowing built-ins (`dict = {}`) | Shadowing & bloat; misuse of variable binding                  | Rename shadowed variables; ensure proper initialization |
| **Interface**       | Accessing `_internal` members outside class scope         | Structural incoherence; poor class hierarchy integration       | Enforce encapsulation; refactor to public APIs          |
| **Checking**        | Passes happy path but lacks `try/except` or null checks   | Partially wrong logic; failure to address edge cases (CWE-754) | Mandate input validation and exception traceability     |
| **Maintainability** | Unnecessary `else` after `return` or `break`              | Defensive bloat; complex control flow without value            | Flatten conditional logic; reduce cyclomatic complexity |

### Architectural Impact

AI code is logically simpler and more repetitive than human code. Any deviation into complexity without clear performance gain is a diagnostic marker of model failure.

---

## Layer 2: Slopsquatting & Dependency Verification

"Slopsquatting" is a supply chain attack where adversaries register hallucinated package names.

> **Risk Statistics:**
>
> - GPT-4 hallucinates packages ~20% of the time
> - Gemini reaches 64.5%
> - The "huggingface-cli" phantom received 30,000 downloads despite being empty

### Verification Checklist

- [ ] **Registry Cross-Reference:** Verify every import against official registries (npm, PyPI)
- [ ] **Version Hallucination Audit:** Flag non-existent versions (e.g., `pandas==2.5.0`, `tensorflow==3.2.1`)
- [ ] **Ecosystem Integrity:** Reject cross-ecosystem borrowing (e.g., `@utils/helper` in Python)

### Remediation

> **If a phantom dependency is detected:** Nuke and rebuild. Do not attempt to fix the import. Re-generate using only organization-approved, security-vetted libraries.

---

## Layer 3: Stylistic Signature ("Transformer Cadence")

AI code exhibits "Verbosity Drift" and a specific rhythm. These stylistic markers often correlate with logic gaps.

### Diagnostic Markers

- [ ] **Marker A — Robotic Documentation:** Comments explain _what_ (`# increment x by 1`) rather than _why_
- [ ] **Marker B — Defensive Bloat:** Redundant null checks or wrappers masking shallow logical depth
- [ ] **Marker C — Context Collapse:** Complexity increases across iterations without resolving root bug

### Context Collapse Remediation

> **Stop and Restart Threshold:** If code complexity (NLOC/CCN) increases over 3 iterations without resolving the primary defect, discard the session. The model has entered a hallucination loop—start fresh.

---

## Layer 4: Instruction Adherence & Reasoning Failure

The "Curse of Instructions": failure rates increase exponentially with multiple constraints. Chain-of-Thought (CoT) reasoning can divert focus from simple constraints.

### Constraint Attention Audit

1. **Constraint Mapping:** Identify all negative constraints from the original prompt
   - "Do not use the `requests` library"
   - "Must be Python 3.9 compatible"
   - Format requirements

2. **Attention Analysis:** Audit the reasoning trace
   - Flag where model _acknowledges_ constraint in thinking but _violates_ in code

### Remediation

> **High Adherence Failure:** If significant violations occur under high-constraint prompts, bypass LLM's internal CoT. Use an external constraint-validation classifier.

---

## Audit Report Template

### Critical Risk Scorecard

| Layer   | ODC Mapping          | Focus Area              | High-Risk Indicator                                    |
| :------ | :------------------- | :---------------------- | :----------------------------------------------------- |
| Layer 1 | Algorithm/Assignment | Logic & Performance     | O(n²) complexity; benchmark failures                   |
| Layer 2 | Interface            | Security & Dependencies | Hallucinated packages (20%+ risk); phantom versions    |
| Layer 3 | Function/Class       | Stylistic Signature     | Robotic comments; defensive bloat hiding shallow logic |
| Layer 4 | Checking             | Instruction Adherence   | Negative constraint violations; CoT-driven neglect     |

### Report Format

```
AUDIT REPORT: [Component Name]
Date: YYYY-MM-DD
Auditor: [Name]

LAYER 1: Logic & Performance
  Status: [PASS/FAIL]
  Findings: ...
  Remediation: ...

LAYER 2: Dependencies
  Status: [PASS/FAIL]
  Findings: ...
  Remediation: ...

LAYER 3: Stylistic Signature
  Status: [PASS/FAIL]
  Findings: ...
  Remediation: ...

LAYER 4: Instruction Adherence
  Status: [PASS/FAIL]
  Findings: ...
  Remediation: ...

OVERALL: [PASS/FAIL/CONDITIONAL]
Priority Remediations:
1. ...
2. ...
```

### Final Directive

Present report to Software Architect prioritizing remediability. High-risk artifacts must be rejected immediately. Highlight where code lacks "lexical diversity" or "structural depth" and provide ODC-mapped remediation steps.