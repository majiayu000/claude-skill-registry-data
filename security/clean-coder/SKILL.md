---
name: clean-coder
description: "Enforces Clean Code standards, identifies code smells, and ensures SOLID principles. Use when: clean code, code smell, SOLID, refactor, quality check."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/coding/clean-coder.skill.md"
  tags: "coding"
  core: "true"
  context_cost: "medium"
---
# Clean Coder Skill

## Goal
To ensure code is readable, maintainable, and free of technical debt "smells" before it merges.

## Core Principles (2025 Standards)
1.  **SOLID**:
    -   **S**ingle Responsibility: One reason to change.
    -   **O**pen/Closed: Open for extension, closed for modification.
    -   **L**iskov Substitution: Subtypes must be substitutable.
    -   **I**nterface Segregation: Tiny, focused interfaces.
    -   **D**ependency Inversion: Depend on abstractions, not concretions.
2.  **DRY (Don't Repeat Yourself)**: Abstract logic, not just code.
3.  **KISS (Keep It Simple, Stupid)**: Simplest solution that works.
4.  **YAGNI (You Ain't Gonna Need It)**: Don't implement future features now.

## Common Code Smells
-   **Long Method**: > 20 lines (heuristic). Extract Method.
-   **Large Class**: Too many responsibilities. Extract Class.
-   **Primitive Obsession**: Using strings/ints instead of Value Objects.
-   **Feature Envy**: Using data from another object more than its own.
-   **Shotgun Surgery**: One change requires edits in many classes.

## Steps
When reviewing or writing code:
1.  **Scan for Smells**: Check against the `clean-code-principles.md` guide.
2.  **Suggest Refactoring**: "Split this huge function into 3 smaller ones: `validateInput`, `processData`, `saveResult`."
3.  **Verify Naming**: Variables should be descriptive (`userAssumingRole` vs `u`).
4.  **Check Comments**: Code should be self-documenting. Comments explain *why*, not *what*.

## Checklist
-   [ ] Descriptive naming?
-   [ ] Functions do one thing?
-   [ ] No duplicated logic?
-   [ ] No magic numbers/strings?
-   [ ] Dependencies injected?

## Security & Guardrails

### 1. Skill Security (Clean Coder)
- **Security-Blind Refactoring**: The agent might "clean up" authentication or encryption logic by simplifying it, inadvertently removing critical, non-obvious security mitigations (like constant-time string comparisons to prevent timing attacks, or explicit memory zeroing). The agent must flag any refactoring of cryptographic, authentication, or authorization modules as requiring immediate, mandatory human security review.
- **Over-Abstraction Vulnerabilities**: In pursuit of DRY and SOLID principles, the agent might extract logic into generic, highly abstract base classes or dynamic factory methods. This can obscure the control flow, making it exceptionally difficult for static analysis tools (SAST) to track tainted data from source to sink. "Clean" code must not sacrifice security auditability; the agent must prioritize explicit data flows over extreme abstraction.

### 2. System Integration Security
- **Log Forgetting via KISS**: While applying the KISS (Keep It Simple, Stupid) principle, the agent might identify verbose security logging or audit trailing as "unnecessary complication" and remove it to simplify the function. The agent must treat explicit Audit Logging and Security Telemetry components as mathematically untouchable by standard "Clean Code" heuristics.
- **Dependency Inversion Payload Injection**: When enforcing Dependency Inversion (Step 1.5), the agent might advocate for dynamic dependency injection config (e.g., loading concrete classes by string name at runtime). If an attacker can control those configuration strings, they achieve arbitrary code execution. The agent must verify that all Dependency Injection implementations rely on explicit, type-safe bindings, not untrusted runtime variables.

### 3. LLM & Agent Guardrails
- **Aesthetic Over Optimization**: The LLM might become obsessed with the *appearance* of clean code (e.g., converting all `if/else` chains into complex functional `reduce` operations) without considering the performance or readability impact for human maintainers. The checklist (Step 4) must enforce a "Readability First" constraint—if a refactored function requires more cognitive load to understand than the original, the refactor is rejected.
- **Hallucinated "Smells"**: Due to pattern misrecognition, the LLM might hallucinate a "Shotgun Surgery" smell where none exists, proposing massive, deeply invasive architectural changes for a minor feature PR. The agent must quantifiably prove the existence of a smell (e.g., citing exactly which 5 files will need changing) before suggesting sweeping architectural refactoring.
