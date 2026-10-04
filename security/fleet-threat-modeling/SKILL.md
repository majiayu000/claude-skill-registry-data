---
name: fleet-threat-modeling
description: How DevSecOps thinks about threats — STRIDE categories, attack surface mapping, trust boundaries, and producing actionable security requirements (not "be secure")
user-invocable: false
---

# Threat Modeling

## The Problem This Solves

A security contribution that says "ensure proper authentication" is
useless. The engineer already knows that. Threat modeling produces
SPECIFIC, ACTIONABLE requirements:

- "The /api/tasks endpoint accepts task_id as a path parameter.
  Validate that the requesting agent owns the task before returning
  data. Without this, any agent can read any task."

That's a security requirement. "Be secure" is not.

## Framework: STRIDE per Component

For each component or feature being reviewed:

### S — Spoofing (Identity)
- Can an attacker pretend to be someone else?
- Are authentication tokens validated on every request?
- Can agent identities be forged in IRC/gateway messages?

### T — Tampering (Data Integrity)
- Can data be modified in transit or at rest?
- Are task fields validated before state changes?
- Can board memory events be injected?

### R — Repudiation (Audit)
- Can an agent deny performing an action?
- Are all state-modifying operations logged?
- Is the trail tamper-resistant?

### I — Information Disclosure
- Can an agent see data they shouldn't?
- Are errors leaking internal state?
- Are secrets (tokens, keys) properly scoped?

### D — Denial of Service
- Can an agent flood the system?
- Are there rate limits on tool calls?
- Can a single task block the orchestrator?

### E — Elevation of Privilege
- Can an agent perform actions beyond their role?
- Are role boundaries enforced at the tool level?
- Can contribution tasks be self-approved?

## Process

### Step 1: Map the Attack Surface

For the feature or component under review:
1. What are the entry points? (APIs, tool calls, IRC messages, file reads)
2. What data flows through? (task data, credentials, user content)
3. What are the trust boundaries? (agent → MCP → MC, agent → gateway)
4. What assets are at risk? (task data, credentials, fleet state)

### Step 2: Apply STRIDE

For each entry point, walk through STRIDE. Not everything applies
to everything — focus on what's realistic:

| Component Type | Focus On |
|---------------|----------|
| API endpoint | Spoofing, Tampering, Info Disclosure |
| State machine | Tampering, Elevation |
| File operations | Tampering, Info Disclosure |
| Inter-agent communication | Spoofing, Repudiation |
| Configuration | Tampering, Elevation |

### Step 3: Produce Specific Requirements

For each threat identified:
1. **What:** the specific vulnerability
2. **Where:** the specific code/component
3. **Impact:** what happens if exploited
4. **Control:** the specific mitigation
5. **Verification:** how to test the control works

### Step 4: Classify Severity

| Severity | Criteria |
|----------|----------|
| Critical | Remote exploitation, data breach, privilege escalation |
| High | Auth bypass, significant data exposure |
| Medium | Limited info disclosure, DoS potential |
| Low | Minor issues, defense in depth |

## Output: Security Contribution

When contributing to a task via `fleet_contribute`:

```
## Security Requirements for: {task_title}

### Threat Summary
{1-2 sentences: what's the risk profile}

### Requirements
1. [CRITICAL] {specific control}
   - Threat: {STRIDE category}: {specific threat}
   - Where: {file/endpoint/component}
   - Verify: {how to test}

2. [HIGH] {specific control}
   ...

### Trust Boundaries
- {boundary}: {what crosses it, how to protect}

### Out of Scope
- {what was assessed and found acceptable, so the engineer doesn't waste time}
```

## Common Mistakes

1. **Generic requirements** — "validate all inputs" tells the engineer nothing
2. **Missing the real threat** — spending time on XSS in an internal CLI tool
3. **Over-classifying** — not everything is Critical
4. **Ignoring the fleet context** — agents are NOT external attackers, but
   behavioral drift IS a real threat (see fleet-elevation/20 anti-corruption)
5. **Blocking instead of guiding** — security_hold is for confirmed risks,
   not theoretical concerns
