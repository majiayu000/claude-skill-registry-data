---
name: secure-coding
description: "Implementing OWASP Proactive Controls (Input Validation, Output Encoding, AuthZ/AuthN). Use when: secure coding."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/coding/secure-coding.skill.md"
  tags: "coding"
  core: "true"
  context_cost: "low"
---
# secure-coding Skill

## Goal
This skill guides the implementation of security controls *during* development (Shift Left).

## Steps
## 1. Input Validation (Defense)
> "Never trust input."

- **Syntactic Validation**: Is it an email? Is it a number? (Use Zod/Pydantic).
- **Semantic Validation**: Is `start_date` before `end_date`? Is `transfer_amount` > 0?
- **Allow-list**: Only accept known good characters (e.g., `[a-zA-Z0-9]`). Block everything else.

## 2. Output Encoding (Defense)
> "Context matters."

- **HTML Context**: Escape `<` -> `&lt;`. (Prevent XSS).
- **SQL Context**: Use Parameterized Queries. (Prevent SQLi).
- **JSON Context**: Ensure valid JSON structure.

## 3. Authentication & Authorization
- **NIST Guidelines**:
  - Passwords: Min 12 chars, no complexity rules, check against pwned passwords.
  - MFA: Required for admin/privileged actions.
  - Sessions: Absolute timeout (e.g., 12 hours) + Idle timeout (e.g., 30 mins).
- **Authorization**:
  - **Broken**: `if (user.isAdmin)` (Client-side check).
  - **Fixed**: `if (ctx.user.hasPermission('delete:user'))` (Server-side check).

## 4. Cryptography
- **At Rest**: Use AES-256-GCM (Authenticated Encryption).
- **In Transit**: TLS 1.3 only.
- **Hashing**: Argon2id or bcrypt (work factor > 12).
- **Secrets**: Never hardcode. Use `process.env`.

## Security & Guardrails

### 1. Skill Security (Secure Coding)
- **Validation Bypass via Type Coercion**: In Step 1 (Input Validation), the agent might rely on loose checking (`==`) instead of strict type checking (`===`), or use a validation library improperly (e.g., forgetting to cast string digits to actual integers before enforcing a `>= 0` rule). An attacker can exploit this loose coercion to bypass semantic validation. The agent must enforce strict type bindings and immutable schemas (e.g., `z.strict()`) at all system boundaries.
- **Context-Confused Encoding (XSS Mutation)**: In Step 2 (Output Encoding), the agent might correctly encode data for an HTML body but mistakenly use that same encoded string inside an inline Javascript block (`<script> var name = "ENCODED_DATA"; </script>`), which requires entirely different escaping rules. The agent must rigidly track the *destination context* of the tainted data and apply the exact encoding algorithm mandated for that specific DOM or SQL context.

### 2. System Integration Security
- **Hardcoded Secret Regression**: Step 4 states "Never hardcode. Use `process.env`." If the agent is refactoring a legacy file that currently has a hardcoded secret, it might attempt to "fix" it by moving the secret into a standard constant variable at the top of the file, completely failing the objective. The agent must integrate with the environment's Secrets Management pipeline (e.g., AWS Secrets Manager, Doppler) and physically remove the secret string from the codebase.
- **Crypto Downgrade via Fallback**: When configuring TLS or hashing (Step 4), the LLM might include "fallback" mechanisms to support legacy clients (e.g., allowing TLS 1.2 or MD5 if the primary fails). This enables Man-in-the-Middle downgrade attacks. The agent must enforce strict, configuration-level prohibition of deprecated cryptographic protocols, crashing the application rather than defaulting to insecure algorithms.

### 3. LLM & Agent Guardrails
- **Hallucinated "Safe" Libraries**: An LLM might confidently suggest using a third-party library to handle input sanitization (e.g., `import sanitizeHtml from 'random-npm-package'`) that is actually abandoned or known to be vulnerable. The agent must strictly limit security-critical implementations (Crypto, Auth, Sanitization) to a globally approved, architecturally verified list of standard libraries (e.g., `DOMPurify`, `bcrypt`, `crypto`).
- **Authorization Drift**: Over long contexts, the LLM might forget the nuanced difference between Authentication (AuthN - "Who are you?") and Authorization (AuthZ - "What can you do?"). It might write code that says `if (user.isAuthenticated()) { deleteDatabase(); }`. The agent's internal prompt pipeline must forcibly inject the `AuthZ != AuthN` constraint immediately before generating any route-handling or controller logic.
