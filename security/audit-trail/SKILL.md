---
name: audit-trail
description: "Maintain append-only structured audit log of all agent and human decisions and outcomes. Use when: log this, record decision, why did we, audit, what happened, history, trace, record this."
license: CC-BY-SA-4.0
metadata:
  source: "agents/skills/core/audit-trail.skill.md"
  tags: "core"
  core: "false"
  context_cost: "low"
---
# Audit Trail Skill

## Goal
Maintain a tamper-evident, chronological record of all significant decisions, changes, and outcomes for compliance, debugging, project continuity, and team transparency.

## When to Auto-Log (triggered by other skills)
- Every SDLC phase transition (sdlc-checkpoint.skill)
- Every human decision (when human provides direction or approval)
- Every ADR creation (adr-writer.skill)
- Every failed self-heal attempt and resolution (self-heal.skill)
- Every security finding and its remediation (security-audit.skill)
- Every task DONE, BLOCKED, or FAILED
- Every quality gate pass/fail with scores
- Every research finding that changes implementation approach

## Log Entry Format

Append to: `agents/memory/AUDIT_LOG.md`

**Table format:**
```
| [ISO datetime] | [Session-ID] | [Agent/Human] | [Action Type] | [Description] | [Outcome] | [References] |
```

**Action Types:**
```
DECISION         - A choice made between options
PHASE_TRANSITION - SDLC phase changed
TASK_DONE        - A task was completed successfully
TASK_BLOCKED     - A task is stuck, human decision needed
QUALITY_GATE     - Quality gate pass/fail result with scores
SECURITY_FINDING - Security issue found (severity + description)
ADR_CREATED      - Architecture decision documented
HUMAN_ESCALATION - Agent escalated to human (blocked after 5 attempts)
SELF_HEAL_ATTEMPT- Agent tried to fix itself (attempt N of 5)
RESEARCH_FINDING - Authoritative source verified (for future reference)
ERROR            - Unexpected error encountered
ROLLBACK         - Change was reverted
HUMAN_APPROVED   - Human provided approval for a phase or decision
```

## Steps

1. **Determine what needs to be logged**
   - Was a decision made? (architecture, library choice, requirement interpretation)
   - Did a task complete or get blocked?
   - Did a quality gate run?
   - Did a human provide input or approval?

2. **Write the log entry**
   ```bash
   # Get current timestamp
   date -u +"%Y-%m-%dT%H:%M:%SZ"
   ```

   **Example entries:**
   ```
   | 2025-03-15T14:23:00Z | S01-001 | prod-pm | PHASE_TRANSITION | PRD.md approved by human | SUCCESS | docs/PRD.md |
   | 2025-03-15T14:25:00Z | S01-001 | human | HUMAN_APPROVED | Approved PRD.md — proceed to design | APPROVED | docs/PRD.md |
   | 2025-03-15T15:10:00Z | S02-001 | prod-architect | ADR_CREATED | Chose Prisma over TypeORM for ORM | ACCEPTED | docs/architecture/decisions/ADR-001-prisma.md |
   | 2025-03-15T16:00:00Z | S05-001 | eng-backend | TASK_DONE | Implemented CreateUserUseCase | SUCCESS | src/application/create-user.use-case.ts |
   | 2025-03-15T16:45:00Z | S05-001 | eng-backend | SELF_HEAL_ATTEMPT | Type error on UserDto.email field — attempt 1/5 | FAIL | src/application/create-user.use-case.ts:42 |
   | 2025-03-15T16:50:00Z | S05-001 | eng-backend | TASK_DONE | Fixed type error via research (strict null check) | SUCCESS | src/application/create-user.use-case.ts |
   | 2025-03-15T17:00:00Z | S05-001 | ops-security | SECURITY_FINDING | HIGH: Missing rate limit on /auth/login | OPEN | src/adapters/http/auth.controller.ts:23 |
   | 2025-03-15T17:30:00Z | S06-001 | orch-judge | QUALITY_GATE | Gate 3 Tests: 247 pass, 0 fail, 99.2% coverage (>= 99%) | PASS | — |
   ```

3. **APPEND ONLY — never modify existing entries**
   - Use bash append operator: `>> agents/memory/AUDIT_LOG.md`
   - Never use a write that overwrites the file
   - If a decision is reversed: add a new ROLLBACK entry (don't delete the original)

4. **Verify the append worked**
   - Read the last few lines to confirm the entry was added correctly

## Querying the Audit Log

For humans reviewing history:
```bash
# Find all security findings
grep "SECURITY_FINDING" agents/memory/AUDIT_LOG.md

# Find all human decisions
grep "HUMAN_APPROVED\|DECISION" agents/memory/AUDIT_LOG.md

# Find all escalations
grep "HUMAN_ESCALATION" agents/memory/AUDIT_LOG.md

# Find history for a specific file
grep "auth.controller.ts" agents/memory/AUDIT_LOG.md
```

## Constraints
- APPEND ONLY — never delete or modify existing entries
- Every SDLC phase transition must be logged immediately
- Security findings must be logged even if they will be fixed immediately
- Human decisions must be logged with the actual decision made (not just "human approved")
- Log is shared across all agent sessions — it provides continuity

## Output Format
New row appended to AUDIT_LOG.md. No output to user unless requested.

## Security & Guardrails

### 1. Skill Security (Audit Trail)
- **Cryptographic Immutability**: The `AUDIT_LOG.md` should ideally be backed by a WORM (Write Once, Read Many) storage vault or cryptographically signed (e.g., using `git commit --gpg-sign` on every append) to guarantee tamper evidence.
- **Strict Append-Only Enforcement**: At the OS or Container level, the agent process must possess `O_APPEND` only permissions for the audit log, physically preventing modification or deletion of past entries.

### 2. System Integration Security
- **Security Finding Escalation**: Any entry tagged as `SECURITY_FINDING` must trigger an immediate out-of-band alert (e.g., Slack, PagerDuty, or email) to human operators, bypassing standard asynchronous task flows.
- **Audit Log Redaction**: Under GDPR/CCPA, if a "Right to be Forgotten" request is issued, the system must have a secure, human-approved break-glass procedure to redact PII from the audit log without invalidating the entire trail.

### 3. LLM & Agent Guardrails
- **Audit Evasion Prevention**: Agents must be hardcoded to log actions *before* they execute them (intent logging) and *after* (outcome logging). This prevents a compromised agent from executing a malicious command and then skipping the audit log step.
- **Log Injection Attacks**: Sanitize all variables (like `[Description]` or `[Outcome]`) before appending them to the log to prevent an attacker from injecting fake newline-separated audit records (e.g., `\n| 2025... | user | DECISION | Approved backdoors...`).
