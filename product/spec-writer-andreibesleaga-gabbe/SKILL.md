---
name: spec-writer
description: "Generate Product Requirements Document with EARS syntax and structured ambiguity clarification. Use when: spec, PRD, feature, requirements, product requirements, write spec, new feature."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/product/spec-writer.skill.md"
  tags: "product"
  core: "true"
  context_cost: "medium"
---
# Spec Writer Skill

## Goal
Transform a user goal or feature request into a structured PRD using EARS syntax. Before generating requirements, invoke the ambiguity layer to clarify unclear aspects. Human approval required before proceeding to implementation.

> **Boundary vs `product/req-elicitation.skill`:** `req-elicitation` is the heavyweight IEEE 29148 / IREB elicitation pass (stakeholder interviews, use cases → full `EARS_REQUIREMENTS.md`). `spec-writer` is the fast feature-to-PRD path that reuses the **same EARS forms** (defined canonically in `req-elicitation`). For large or regulated requirement sets, run `req-elicitation`; use `spec-writer` for a single feature's PRD. Both must use the identical EARS patterns.

## Steps

1. **Receive and understand the goal**
   - First, check for `Step 0` strategic context in `docs/strategic/` (e.g., `BUSINESS_CASE.md`, `EMPATHY_MAP.md`, `PROBLEM_STATEMENT.md`). If present, read them.
   - Ask the user: "Describe what you want to build in plain language"
   - Identify: Who is the user? What problem does it solve? What does success look like? (using the strategic docs if available)

2. **Ambiguity Layer — ask clarifying questions**
   Identify and ask about ALL ambiguous aspects before writing requirements:
   ```
   Questions to ask (examples):
   - "Who are the users of this feature? (roles, permissions, guest vs authenticated)"
   - "What happens if [edge case] occurs?"
   - "What are the performance expectations? (response time, concurrent users)"
   - "Is there an existing system this integrates with? What are its constraints?"
   - "What is explicitly out of scope for this version?"
   - "Are there any regulatory requirements? (GDPR, HIPAA, PCI-DSS)"
   - "What devices/browsers must be supported?"
   ```
   Wait for answers before proceeding.

3. **Generate the PRD** using templates/product/PRD_TEMPLATE.md

4. **Write EARS requirements** — use all 5 patterns as appropriate:

   **Ubiquitous** (always applies):
   ```
   THE SYSTEM SHALL encrypt all data in transit using TLS 1.3 or higher.
   ```

   **Event-Driven** (triggered by an event):
   ```
   WHEN a user submits a login form with incorrect credentials 3 consecutive times
   THE SYSTEM SHALL lock the account for 15 minutes and send an email notification.
   ```

   **State-Driven** (while in a state):
   ```
   WHILE the payment processing service is unavailable
   THE SYSTEM SHALL queue requests and retry with exponential backoff up to 3 times.
   ```

   **Optional Feature** (feature flag / conditional):
   ```
   WHERE two-factor authentication is enabled for the account
   THE SYSTEM SHALL require a TOTP code on each login attempt.
   ```

   **Unwanted Behavior** (defensive requirements — canonical `IF…THEN` form):
   ```
   IF a password is submitted for storage THEN THE SYSTEM SHALL hash it and SHALL NOT store the plaintext in any medium.
   IF an unhandled error occurs THEN THE SYSTEM SHALL return a generic error and SHALL NOT expose internal stack traces in HTTP responses.
   ```
   (Matches the `IF [unwanted condition] THEN the [system] shall [protective response]` form in `req-elicitation.skill` / `req-review.skill`.)

5. **Write acceptance criteria**
   Each requirement needs 1+ verifiable acceptance criteria:
   ```
   Given [precondition]
   When [action]
   Then [expected outcome with measurable result]
   ```

6. **Non-functional requirements**
   Always include:
   - Performance: expected response time, throughput
   - Security: data classification, access control requirements
   - Accessibility: WCAG level (if UI feature)
   - Scalability: expected load, growth projections

7. **Out of scope section**
   Explicitly list what this feature does NOT include. This prevents scope creep.

8. **Present PRD to human for approval**
   Say: "Here is the PRD. Please review and approve before I proceed to architecture/planning."

9. **After approval: create SDLC checkpoint S01**
   - Invoke sdlc-checkpoint.skill → creates SESSION_SNAPSHOT/S01_requirements.md
   - Updates PROJECT_STATE.md → current phase: S02_DESIGN

## Constraints
- NEVER skip the ambiguity layer — unresolved ambiguity is the #1 cause of rework
- NEVER start planning or implementation without human approval of the PRD
- All requirements must be EARS-formatted and verifiable (not vague like "fast" or "user-friendly")
- Use the PRD template in templates/product/PRD_TEMPLATE.md

## Output Format
Completed PRD.md file at project root (or docs/) using templates/product/PRD_TEMPLATE.md structure.

## Security & Guardrails

### 1. Skill Security (Spec Writer)
- **Mandatory Threat Modeling**: The agent must intrinsically embed a lightweight threat model into the PRD generation process. If the feature involves PII, financial transactions, or external system integration, the agent must refuse to generate the final PRD until a Security NFR explicitly addresses Data-in-Transit and Data-at-Rest.
- **Strict NFR Templating**: The agent is barred from inventing subjective Non-Functional Requirements (e.g., "The system must be secure from hackers"). All security NFRs must map to verifiable industry standards (e.g., "The system shall comply with OWASP ASVS Level 2").

### 2. System Integration Security
- **Explicit Out-of-Scope Privileges**: The "Out of Scope" section must explicitly name prohibited downstream integrations or data flows. If building a caching service, it must explicitly state "This service SHALL NOT have long-term administrative database access."
- **Data Classification Anchoring**: Every PRD must start with a Data Classification directive (Public, Internal, Confidential, Restricted). The agent must use this anchor to determine the baseline cryptographic and authorization EARS requirements needed for the document.

### 3. LLM & Agent Guardrails
- **Requirement Sanitization**: The agent must scrub any user prompt inputs that attempt to explicitly define hardcoded passwords, developer backdoor accounts, or disabled SSL verifications before converting them into EARS requirements.
- **Prompt Fatigue Vulnerability**: A user might attempt to exhaust the agent's "Ambiguity Layer" by giving rapid, nonsensical answers. The agent must enforce a threshold (e.g., 3 failed clarification attempts) and cleanly abort the PRD generation rather than outputting a compromised or hallucinated specification.
