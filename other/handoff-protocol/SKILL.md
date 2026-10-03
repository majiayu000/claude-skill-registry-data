---
name: handoff-protocol
description: |
  Transport-neutral Interaction Records and risk-class evidence bundles for agent-to-agent
  communication. Replaces ad-hoc handoffs with a single canonical artifact that works
  identically in Agent Teams mode (via SendMessage) and fallback mode (via Task prompts).

  Triggers: handoff, hand off, pass to, route to, transfer, quality gate, QA review,
  escalate, sprint boundary, incident, phase gate, consultation, peer review, capability
  request, risk classification, scope expansion.
---

# Handoff Protocol — Interaction Records

The unified canonical artifact for all consequential agent exchanges. Every handoff,
consultation, escalation, review, or capability request produces an **Interaction Record**.

**Rule**: Peer messages that don't produce a record are ephemeral and cannot be relied
upon for decisions. If two agents agree on something that affects the system, it MUST
be written into an Interaction Record before the change is committed.

---

## The Interaction Record (canonical)

Use the same template regardless of transport (Agent Teams or orchestrator-mediated).

```markdown
## Interaction Record
| Task ID       | [DEPT-NNN, e.g., ENG-042] |
| Type          | [consultation \| handoff \| review \| escalation \| capability-request] |
| From          | [sender agent name] |
| To            | [receiver agent name or orchestrator] |
| Transport     | [agent-teams \| orchestrator-mediated] |
| Risk Class    | [low \| medium \| high] |
| Timestamp     | [ISO 8601] |

### Context
[What's been done, relevant files, current state. Be specific — the receiver cold-reads this.]

### Request
[Specific ask — what the sender needs from the receiver. One sentence if possible.]

### Constraints
[Timeline, technical limits, dependencies, files that must not be touched.]

### Evidence Bundle
[Risk-class-appropriate evidence — see Evidence Bundles section below.]

### Decision
[Filled by the receiver: what was decided, rationale, next steps. Left blank when sending.]
```

---

## Interaction Types

### 1. `handoff` — transfer of work between agents

Use when work is being passed forward. Include complete context, deliverable request, and
acceptance criteria in the `Context` and `Request` sections.

### 2. `consultation` — peer asking for input without transferring ownership

Use when an agent wants a peer's opinion on an approach, API contract, or design choice.
Ownership stays with the sender. Peer may propose, not commit.

```markdown
## Interaction Record
| Task ID | ENG-042 |
| Type | consultation |
| From | backend-engineer |
| To | security-engineer |
| Transport | agent-teams |

### Context
Implementing OAuth2 PKCE flow for the /auth endpoint. JWT session currently in place.

### Request
Is the code_verifier length of 43 chars sufficient, or should I use the 128-char max?

### My Proposal
43 chars (minimum per RFC 7636) — keeps URL shorter, still entropic.
```

### 3. `review` — formal review of completed work

Use when submitting work for QA or reality-check. Must include Evidence Bundle
matching the risk class.

### 4. `escalation` — agent stuck, needs reroute

Use when the agent has hit a wall. Must classify the **failure type**:

| Failure Type | Meaning | Orchestrator Action |
|---|---|---|
| `wrong-capability` | Agent needed different expertise | Reroute to matching capability |
| `task-too-large` | Scope expanded beyond assignment | Decompose into subtasks |
| `conflicting-requirements` | Spec contradicts code or other spec | Escalate to product/PM for clarity |
| `environment-issue` | Infra/tooling broken, not task logic | Route to devops/sre |
| `insufficient-context` | Agent needs info only another agent has | Route to knowledge holder |
| `unknown` | Can't classify — describe symptoms | Orchestrator investigates |

```markdown
## Interaction Record
| Task ID | ENG-042 |
| Type | escalation |
| From | backend-engineer |
| To | enterprise-orchestrator |

### Context
Attempted OAuth2 PKCE implementation. Blocked on Supabase JWT signing key rotation strategy.

### Request
Failure Type: wrong-capability
Need: security-engineer with auth+oauth2+supabase qualifiers

### Evidence Bundle
- Files attempted: src/auth/middleware.ts, src/auth/oauth.ts
- Error: "JWT signature verification failed after key rotation"
- What I tried: (1) single static key — works but rotates fail (2) kid-based lookup — key not found in JWKS
```

### 5. `capability-request` — agent needs a peer with specific expertise

Use when the agent doesn't need escalation but does need a specific capability. Lighter
weight than an escalation — typically same-priority routing.

```markdown
## Interaction Record
| Task ID | ENG-042 |
| Type | capability-request |
| From | backend-engineer |
| To | enterprise-orchestrator |

### Request
Capability needed: design-system + [tokens, dark-theme]
Reason: Need hex values for error state background in dark mode to render in email templates.
Urgency: non-blocking
```

---

## Evidence Bundles by Risk Class

Evidence requirements are **conjunctive** (AND, not OR). Each risk class lists the
minimum items that MUST be present. "Or" is not allowed — every listed item is required.

### Low Risk

**Triggers**: docs, comments, config tweaks, typo fixes, small internal refactors.
**No reviewer required** — orchestrator accepts on evidence completeness alone.

**Required evidence** (ALL of):
- File paths changed
- Brief description of change (≤3 sentences)

### Medium Risk

**Triggers**: new features, refactors, API changes, schema additions.
**Reviewer**: `qa-engineer` by default. If qa-engineer authored the work, use
`reality-checker`. If both unavailable, orchestrator reviews directly.

**Required evidence** (ALL of):
- File paths changed
- Test output mapped to acceptance criteria (which test verifies which criterion)
- Before/after behavior description
- Any migrations or breaking-change notes

### High Risk

**Triggers**: security changes, auth/session code, payments, data mutations at scale,
database migrations, RLS policy changes, external API credentials, env var changes.
**Reviewer**: `reality-checker` by default. Backup: `security-engineer` (if
reality-checker authored the work or is unavailable). **Cannot be auto-approved** —
if no reviewer available, task blocks and orchestrator reports to user. Waiver only
by explicit user instruction ("ship it without review").

**Required evidence** (ALL of):
- File paths changed
- Test output mapped to acceptance criteria
- Security implications analysis (what attack surface is affected)
- Rollback plan (exact commands or steps to revert)
- Reviewer sign-off (the reviewer's Interaction Record Decision section filled)
- Before/after behavior description

---

## Risk Reclassification

Risk is classified at dispatch AND re-evaluated on completion.

**Upgrade LOW → MEDIUM if**:
- More than 3 files changed
- Any test file modified
- Any API route modified

**Upgrade MEDIUM → HIGH if**:
- Any auth/security file touched (middleware, permissions, RLS)
- Any database migration created
- Any payment/billing code modified
- Any env var added or changed
- Any external credential reference added

If reclassified:
1. Apply the higher risk class's evidence requirements retroactively
2. If evidence is insufficient for new risk class → send back for additional evidence
3. Document the reclassification in the Interaction Record's `Decision` section

---

## File Scope Declaration (Task ID Gating)

Every task receives a **file scope** from the orchestrator at dispatch:

```markdown
## Task Assignment
| Task ID | ENG-042 |
| Assigned to | backend-engineer |
| Expected file scope | [src/auth/middleware.ts, src/auth/oauth.ts, tests/auth/*.test.ts] |
| Risk Class | medium |
```

**Rules**:
- The agent MAY modify files in the declared scope
- The agent MUST file a scope-expansion Interaction Record before touching any undeclared file
- On completion, orchestrator verifies every changed file was either declared OR had an approved scope-expansion record
- Undeclared changes → work rejected, agent must revert or file the expansion record

Scope expansion record:

```markdown
## Interaction Record
| Task ID | ENG-042 |
| Type | consultation |
| From | backend-engineer |
| To | enterprise-orchestrator |

### Request
Scope expansion: need to also modify src/middleware/cors.ts because OAuth redirect URI changed.
This is a 3-line config update, not logic.
```

---

## Agent Teams Authority Boundaries

When `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is enabled and peers can message each other
directly via SendMessage:

1. **Peers may propose, not commit**: "I think the API contract should be X" is valid.
   "I've decided the API contract is X" requires orchestrator confirmation.

2. **Consequential exchanges produce Interaction Records**: If two peers reach agreement
   on something that affects the system, the agreement MUST be written into an
   Interaction Record before any code changes.

3. **Orchestrator is the single source of authority**: Peers can debate, consult, and
   share evidence. Only the orchestrator (or a designated reviewer) can mark work as
   accepted.

4. **No side-channel decisions**: If a peer exchange changes the approach, files, or
   architecture, the orchestrator must be notified via an Interaction Record before
   the change is committed.

---

## Routing Decision Artifact

When the orchestrator routes a task to an agent, it produces an auditable **Routing Decision**:

```markdown
## Routing Decision
| Task ID | ENG-042 |
| Requested capability | auth: [oauth2, pkce] |
| Matched agents | security-engineer (auth: [oauth2, saml]), backend-engineer (auth: [jwt, session]) |
| Selected | security-engineer |
| Reason | Qualifier match: oauth2 is in security-engineer's qualifiers; backend-engineer only has jwt/session |
| Rejected | backend-engineer — qualifier mismatch |
| Tie-break rule applied | qualifier-match (highest priority) |
```

**Tie-breaking rules** (in priority order, all deterministic from current task context):
1. Qualifier match count — agent whose qualifiers cover the most requested qualifiers
2. Same-department affinity — agent in the same department as the requester (final tiebreaker, not default)
3. If still tied — orchestrator picks and documents exactly why in the Reason field

Load-balancing tie-breaks (e.g., "fewer current assignments") are intentionally excluded: there is no durable assignment ledger, so any such rule would be non-auditable across sessions.
