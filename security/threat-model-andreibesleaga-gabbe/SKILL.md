---
name: threat-model
description: "STRIDE threat modeling before implementing security-sensitive features. Use when: threat, STRIDE, attack surface, security design, new API, new feature security, threat model."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/security/threat-model.skill.md"
  tags: "security"
  core: "true"
  context_cost: "medium"
---
# Threat Model Skill

## Goal
Create a STRIDE threat model BEFORE implementing any security-sensitive feature. Prevents security issues at design time (cheapest point to fix) rather than after implementation (expensive) or in production (catastrophic).

## When to Invoke
- Before implementing: authentication, authorization, user registration, file upload
- Before implementing: payment processing, data storage, API endpoints, admin features
- Before any feature that handles: PII, financial data, health data, secrets, files

## Steps

1. **Identify system components and trust boundaries**
   - Reference the C4 Component diagram if it exists (`docs/architecture/`)
   - Draw the data flow: user → entry point → processing → storage → response
   - Mark trust boundaries (where permissions or privilege changes)
   - Identify actors: authenticated user, anonymous user, admin, external service, attacker

2. **Apply STRIDE to each component**

   For each component (API endpoint, service, data store), systematically ask:

   **S — Spoofing (impersonation)**
   - Can an attacker pretend to be another user or service?
   - Example threats: stolen JWT tokens, forged API keys, session hijacking

   **T — Tampering (data modification)**
   - Can an attacker modify data in transit or at rest?
   - Example threats: MITM attacks, SQL injection, parameter tampering, mass assignment

   **R — Repudiation (deny actions)**
   - Can an attacker deny performing an action?
   - Example threats: no audit log, no digital signature for financial transactions

   **I — Information Disclosure (data leaks)**
   - Can an attacker access data they shouldn't see?
   - Example threats: IDOR, verbose error messages, log injection, SSRF

   **D — Denial of Service**
   - Can an attacker degrade or block service availability?
   - Example threats: no rate limiting, resource exhaustion, large file uploads

   **E — Elevation of Privilege**
   - Can an attacker gain more permissions than they should have?
   - Example threats: JWT algorithm confusion, IDOR to admin endpoints, business logic bypass

3. **Score each threat**

   | Factor | Low | Medium | High |
   |---|---|---|---|
   | **Likelihood** | Attacker needs special access/skills | Known exploit pattern exists | Trivial to exploit |
   | **Impact** | Minor data exposure | User data compromised | All data, system compromise |

   Priority = Likelihood × Impact (High×High = Critical)

4. **Propose mitigations for High and Critical threats**

   ```markdown
   | Threat | STRIDE | L | I | Priority | Mitigation |
   |---|---|---|---|---|---|
   | Stolen JWT allows impersonation | S | H | H | Critical | Short expiry (15min), refresh token rotation, token revocation list |
   | IDOR on /users/{id} endpoint | I | M | H | High | Verify ownership: user.id === session.userId before returning |
   | No rate limit on /auth/login | D | H | M | High | Max 5 attempts/min per IP, 3 per account, exponential backoff |
   ```

5. **Fill THREAT_MODEL_TEMPLATE.md**
   - Save to: `docs/security/threat-models/[feature-name]-threat-model.md`

6. **Update CONSTITUTION.md** if new security invariants emerge
   - Example: "WHEN a user accesses /api/users/{id}, THE SYSTEM SHALL verify the requesting user owns that resource"

7. **Create tasks for mitigations**
   - Add each High/Critical mitigation to project/TASKS.md
   - These are blocking tasks — must be implemented before the feature is complete

8. **Human review required**
   - Present threat model to human before implementing the feature
   - Confirm all Critical and High mitigations will be implemented

## STRIDE Quick Reference

| Letter | Category | Question to ask |
|---|---|---|
| S | Spoofing | Who is claiming to be who, and how do we verify it? |
| T | Tampering | What data can be modified by unauthorized parties? |
| R | Repudiation | Can actions be denied? Are they logged immutably? |
| I | Information Disclosure | What can be leaked, and to whom? |
| D | Denial of Service | What can be exhausted, flooded, or blocked? |
| E | Elevation of Privilege | How can someone gain more access than intended? |

## Constraints
- Threat modeling is MANDATORY before implementing: auth, payment, file storage, admin features
- All Critical threats must have implemented mitigations before feature ships
- High threats must have mitigations or documented risk acceptance by human
- Never implement a security control without documenting why it addresses a specific threat

## Output Format
Completed threat model file at `docs/security/threat-models/[name]-threat-model.md` + tasks added for mitigations.

## Security & Guardrails

### 1. Skill Security (Threat Modeling)
- **Model Tampering Defense**: The threat models generated by this skill (`[name]-threat-model.md`) act as foundational security contracts. The agent must treat these files as protected artifacts; modification requests post-approval must trigger a formal re-review cycle. A developer cannot simply delete a row in the threat model markdown to bypass a mitigation requirement.
- **Mitigation Task Tracking**: The agent must atomically ensure that when a High/Critical mitigation is added to the Threat Model (Step 4), a corresponding, explicitly linked task is created in `project/TASKS.md` (Step 7). The agent must fail the operation if the task creation fails, preventing silent mitigation drops.

### 2. System Integration Security
- **Threat Model to Architecture Drift**: The agent must periodically cross-reference the approved Threat Model against the actual implemented Infrastructure as Code (IaC) or architecture diagrams. If the Threat Model assumes a firewall blocking internal traffic, but the IaC opens all internal ports, the agent must flag this critical drift.
- **Lateral Trust Boundary Identification**: When mapping trust boundaries (Step 1), the agent must actively look for "implicit" lateral trust. For example, if two microservices reside in the same Kubernetes namespace, the agent must highlight this as a shared trust boundary and apply STRIDE to intra-namespace communication.

### 3. LLM & Agent Guardrails
- **Threat Omission Hallucination**: The LLM might selectively ignore complex or nuanced threats to produce a simpler, "cleaner" threat model. The agent must utilize a strict, deterministic checklist encompassing the entire STRIDE methodology to force the generation of edge-case scenarios, refusing to output the model until all categories are populated.
- **Mitigation Downplay Bias**: An overly helpful agent might suggest inadequate, low-effort mitigations for critical threats to appease a user prioritizing speed (e.g., suggesting "adding a comment" instead of implementing proper RBAC for Privilege Escalation). The agent must anchor its mitigation recommendations to strict industry standards (OWASP ASVS).
