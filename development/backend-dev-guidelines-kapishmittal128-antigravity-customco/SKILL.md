---
name: backend-dev-guidelines
description: Core standards for backend engineering. Focuses on performance, security, and maintainable service architecture. Use when building APIs, background workers, or data services.
version: "1.0.0"
verified_date: 2026-04-29
category: backend
---

# Backend Development Guidelines

## Purpose
Ensure all backend code follows Antigravity production standards: highly performant, securely isolated, and easy to audit.

## When to Use This Skill
Use when implementing server-side logic, database handlers, or integration services.

## Phase 1: Architecture & Data Modeling
1. Define the service contract (API spec).
2. Design the database schema for scalability and query efficiency.
3. Identify external dependencies and security requirements.

## Phase 2: Core Implementation
1. Implement logic with strict input validation.
2. Use asynchronous patterns for all I/O operations.
3. Ensure proper error handling and logging.
4. **Security Enforcement**: 
   - **Sanitization**: Use `DOMPurify.sanitize()` (if outputting to frontend) or strict ORM bindings for all dynamic content.
   - **Secrets**: Scan for `API_KEY`, `TOKEN`, `SECRET` in all staged files. Never log PII or credentials.

## Phase 3: Verification
- [ ] Are all inputs sanitized?
- [ ] Is there a retry logic for external services?
- [ ] Are logs informative and free of PII?

## Output Format / Delivery
- Implementation plan or code changes.
- Audit report for existing logic.

## Behavior Rules
1. **Never skip validation**. Even for internal services.
2. **Prefer statelessness**. Minimize server-side session state.
3. **Auditability first**. All major state changes must be logged.

## Hard Usage Rules (Tier 2: Conditional)
- **ALLOWED**: Writing standard CRUD or middleware.
- **FORBIDDEN**: Implementing distributed state management without explicit architectural approval.
- **CONSTRAINT**: Must verify ORM methods against actual schema definition before generation.

## Safety Guardrails & Patched Prevention
1. **ORM Hallucination Patch**: Before writing DB queries, strictly cross-reference the exact ORM syntax documented in the workspace. Do not invent arguments (e.g., `includeAll`).
2. **Missing Indexes Patch**: If generating a `WHERE` or `JOIN` clause on a non-primary key, append a mandatory comment flagging the need for a database index.
3. **Sync I/O Patch**: All file system operations must use `fs.promises`. Synchronous methods (`readFileSync`) are strictly forbidden.
4. **Self-Rejection Clause**: If the output cannot be proven to satisfy its patches (e.g., missing schema context to guarantee ORM safety), **ABORT OUTPUT** and emit: *"REJECTED: Missing schema context to guarantee ORM safety."*

## Maintenance Notes
- Initial global core skill.
