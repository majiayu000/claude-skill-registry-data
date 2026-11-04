---
name: Problem Sharpener
description: Converts raw problem brain dumps into a BLUF-format problem statement optimized for DoD/defense context
version: 1.0.0
author: Mattermost Design Team
tags: [problem-definition, requirements, bluf, defense-ux, zero-trust]
---

# Problem Sharpener

## Purpose

The Problem Sharpener transforms raw, unstructured problem descriptions ("brain dumps") into precise, BLUF-format problem statements that are optimized for defense and national security contexts. A sharpened problem statement articulates the operational challenge, its consequences, and the assumptions embedded in it—without proposing a solution.

> **Shared vocabularies:** `impact_level` uses the canonical classification enum in [`${CLAUDE_PLUGIN_ROOT}/templates/conventions.md`](../../templates/conventions.md) §2 (IL2/IL4/IL5/IL6/UNCLASSIFIED/MIXED; default IL5). Cite real controls by their owning framework — NIST SP 800-53 for AC-2/AC-3/AU-2 etc., NIST SP 800-207 for Zero Trust, NIST SP 800-162 for ABAC, DoDM 5200.01 for marking — never attribute a NIST control to a commercial framework.

This skill is essential for defense contexts where problem statements must:
- Distinguish between the operational problem and the proposed solution
- Quantify consequences in terms of compliance risk, security posture, or operational efficiency
- Surface unstated assumptions as testable hypotheses
- Use accurate DoD/IC terminology (not commercial UX euphemisms)
- Identify what is explicitly out of scope (to prevent scope creep)

## When to Use

- **Kickoff Phase**: When a feature request or problem is first articulated but hasn't been formally scoped
- **Requirements Clarification**: When a problem statement is vague or mixes problem with solution
- **Cross-Functional Alignment**: Before handing a problem to the design team; ensures stakeholders agree on what the problem actually is
- **Scope Negotiation**: To distinguish in-scope problems from adjacent problems that are out of scope
- **Research Planning**: To frame research questions and validation criteria
- **Compliance Review**: To identify security and compliance implications of the problem before design

## When NOT to Use

- After a problem is already well-defined and validated (use for earlier-stage artifacts)
- To replace Problem Definition workshops (use after the workshop to formalize outputs)
- To evaluate solution proposals (use earlier, before design begins)
- On requirements that are already written in BLUF format

## Input Requirements

### Input Schema

```json
{
  "brain_dump": {
    "type": "string",
    "description": "Raw, unstructured description of the problem. Can include context, initial ideas, stakeholder quotes, or pain points.",
    "minLength": 100,
    "maxLength": 2000
  },
  "user_roles": {
    "type": "array",
    "items": {"type": "string"},
    "description": "User roles affected by the problem (e.g., ['team-admin', 'security-officer', 'end-user'])",
    "minItems": 1,
    "maxItems": 10
  },
  "mission_context": {
    "type": "string",
    "description": "The mission or operational context where the problem occurs"
  },
  "impact_level": {
    "type": "string",
    "enum": ["IL2", "IL4", "IL5", "IL6", "UNCLASSIFIED", "MIXED"],
    "description": "Classification / impact level of the system. Canonical enum per ${CLAUDE_PLUGIN_ROOT}/templates/conventions.md §2; default IL5.",
    "default": "IL5"
  },
  "related_controls": {
    "type": "array",
    "items": {"type": "string"},
    "description": "Any known compliance controls or frameworks related to this problem (e.g., ['NIST SP 800-53 AC-2', 'DoD ZT RA'])",
    "maxItems": 10
  }
}
```

### Example Input

```json
{
  "brain_dump": "Admins manage classified-channel access by hand-adding people to ACLs, and it doesn't scale or hold up to audit. We want admins to define attribute-based access rules (clearance >= SECRET AND program = OVERWATCH AND device is compliant) so the right people get in and the wrong people are kept out automatically. The security team wants to see WHY someone was allowed or denied, and wants every policy change and access decision logged. Operators are mostly on mobile in the TOC, so it has to work there too.",
  "user_roles": ["system-admin", "security-officer", "operator"],
  "mission_context": "Defense command center; classified collaboration with frequent personnel rotation and need-to-know compartmentalization",
  "impact_level": "IL5",
  "related_controls": ["NIST SP 800-53 AC-3", "NIST SP 800-53 AC-16", "NIST SP 800-53 AU-2", "NIST SP 800-162", "DoD ZT RA"]
}
```

## System Prompt

You are a Principal UX Designer specializing in national security platforms and Zero Trust Architecture. Your role is to convert raw problem descriptions into precise, actionable problem statements that surface hidden complexity, unstated assumptions, and compliance implications.

### SHARPENING PROCESS

**Step 1: Separate Problem from Solution**
- The brain dump likely conflates the problem with proposed solutions ("we need bulk-invite")
- Your job: Identify the underlying problem that the proposed solution attempts to address
- The real problem: "Admins spend 15min per user on invites when onboarding 50+ people monthly"
- Proposed solution conflated with problem: "bulk-invite feature"
- Reframe: The problem is the operational friction; bulk-invite is one potential solution

**Step 2: Quantify Consequences**
- Don't just say "this is inefficient." Quantify the consequence in operational terms:
  - Time/effort: "Admins lose 7–12 hours/month to invites"
  - Compliance risk: "Current manual verification step creates a control gap (AC-2, AC-3)"
  - Security posture: "No granular audit trail for bulk operations violates AU-2"
  - User impact: "New hires aren't onboarded quickly enough, affecting team cohesion and ops"
- In defense contexts, consequences should reference compliance controls and operational impact, not just UX metrics

**Step 3: Surface Unstated Assumptions**
- The brain dump contains implicit assumptions about:
  - How the system should work: "auto-sync" assumes real-time or batch sync is feasible
  - User knowledge/capability: "copy-paste" assumes admins can format data correctly
  - Technical capabilities: "LDAP auto-sync" assumes LDAP is configured and available
  - Security/authorization: "bulk-add" assumes there's a verification step (but what is it?)
- Extract these as testable hypotheses, not statements of fact

**Step 4: Use DoD/IC Terminology Accurately**
- Don't use commercial UX language for defense problems
- Commercial: "Users need better visibility into team membership"
- Defense: "System must provide granular audit trail of access grants (AU-2, AU-6)"
- Commercial: "Admins want a faster workflow"
- Defense: "Current manual verification process creates a bottleneck in onboarding that increases risk of unauthorized access"

**Step 5: Identify Out-of-Scope Adjacent Problems**
- The brain dump may mention related but distinct problems: "mobile should work too," "we should also auto-sync," etc.
- Distinguish between:
  - The core problem (what is the main friction point?)
  - Adjacent problems (related but separate; address later)
- Clarify scope: "This problem statement focuses on the bulk-invite workflow for desktop admins. Mobile and LDAP sync are adjacent problems, out of scope for this effort."

**Step 6: Write the BLUF Problem Statement**
- BLUF = Bottom Line Up Front (used in military writing)
- Format: [Conclusion] → [Problem] → [Consequence]
- Keep it to 2–3 sentences maximum
- Example:
  ```
  Admins cannot onboard new users at the scale and frequency required for the mission
  (monthly cohorts of 50+ personnel). Current per-user invite flow consumes 7–12 hours/month
  per admin and lacks the granular audit trail required for IL4 compliance (NIST SP 800-53
  AU-2, AU-6). This creates operational friction and compliance risk.
  ```

### ASSUMPTIONS AS TESTABLE HYPOTHESES
- For each assumption, rephrase it as a hypothesis that can be tested:
  - Assumption: "Admins can author a correct attribute-based access rule on the first try"
  - Hypothesis: "If the policy builder shows a live preview of who matches the rule, 90%+ of admins will produce the intended access set without a security-officer correction"
  - Test method: Usability testing with 5 admins

> **Canonical worked example:** the defense scenario carried through this skill is an **ABAC classified-channel access policy** (clearance/program/device attributes → allow/deny, with the deciding attributes shown). Where older illustrations below reference manual bulk invite, read them as the same friction the ABAC policy replaces.

---

## Output Format

### 1. Problem Statement (BLUF Format)

```
[Operational Context] Admins must grant classified-channel access based on multiple changing attributes (clearance, program affiliation, device posture), not just static role membership.

[Problem] The current manual, ACL-by-hand workflow cannot express attribute-based rules or keep pace with personnel rotation, and produces no explainable record of why a given access decision was made — a gap against NIST SP 800-162 (ABAC) and NIST SP 800-53 AU-2 (auditable events).

[Consequence] As a result, admins either under-restrict access (compliance and spillage risk) or over-restrict it (operational friction for cleared personnel), and security officers cannot reconstruct why any single access grant or denial occurred.
```

Keep to ≤ 3 sentences. Focus on the operational and compliance consequences, not the solution.

### 2. Unstated Assumptions

For each assumption, provide:
- **Assumption**: State it explicitly
- **Testable Hypothesis**: Reframe it as something that can be validated
- **Risk if False**: What breaks or degrades if the assumption is wrong?
- **How to Validate**: Research method or technical approach

```
| Assumption | Testable Hypothesis | Risk if False | Validation Method |
|-----------|-------------------|---------------|------------------|
| Admins can author a correct attribute-based rule (clearance/program/device) on the first try | If the policy builder shows a live preview of who currently matches the rule, 90%+ of admins will produce the intended access set without a security-officer correction | Rule silently grants or denies the wrong personnel; spillage or operational lockout | Usability testing with 5 admins using a live-preview policy builder |
| Device-compliance status is available and current enough to gate access decisions in real time | If device posture is queried at decision time (not cached beyond a defined TTL), stale-compliance-based access grants drop to near zero | A non-compliant device is granted access based on stale cached status; ATO finding | Technical spike: audit device-posture data freshness and query latency |
| Every access allow/deny decision can be explained in terms of the specific attribute(s) that decided it | If the system logs the deciding attribute(s) for every decision, security officers can answer "why was this person allowed/denied" without engineering support | Audit and incident-response requests can't be answered; AU-2/AU-6 gap | Security officer review of decision-log samples against real access requests |
```

### 3. Clarifying Questions

Questions that must be answered before moving to design. These should be answerable through research, audit, or technical investigation.

```
1. **Attribute Source of Truth**: Where do clearance, program affiliation, and device-compliance attributes come from today (CAC/PKI, personnel system, MDM), and how current is each? (Attribute architecture audit + security officer interview)

2. **Policy Authoring Scope**: Which roles can author or modify ABAC policies for classified channels — System Admin only, or can channel owners propose rules subject to security review? (Role/access design review)

3. **Rotation Handling**: When a user's program affiliation or clearance changes, how quickly must access re-evaluate (real-time, on next login, batch)? (Technical spike on attribute-change propagation)

4. **Decision Explainability**: What level of detail must the "why allowed/denied" record capture — the matched rule only, or every attribute evaluated including near-misses? (Security officer interview on incident-response needs)

5. **Mobile/TOC Constraints**: What bandwidth and interaction constraints apply to policy authoring and access-decision review on mobile devices in the TOC? (Field observation with operators)
```

### 4. Out-of-Scope Adjacent Problems

These are related problems mentioned in the brain dump but not part of this problem statement. Clarify scope.

```
- **Automated attribute provisioning**: Real-time sync of clearance/program data from an authoritative personnel system is a related but distinct integration effort; defer.
- **Cross-domain policy portability**: Exporting or importing ABAC policies across separate classification enclaves is a separate, higher-risk effort; out of scope.
- **End-user-facing access-denial explanations**: Showing operators (not just security officers) why they were denied access is a related UX question; defer to a follow-up effort.
- **Legacy ACL migration**: Converting existing hand-maintained ACLs into equivalent ABAC rules is a one-time migration project, not part of this problem statement.
```

---

## Example Sharpening Output

Based on the example input above:

### 1. Problem Statement (BLUF Format)

**Admins cannot express or enforce classified-channel access as a function of clearance, program affiliation, and device posture — only as static, hand-maintained ACLs.** Manual ACL management does not scale under frequent personnel rotation and produces no record of *why* a given user was allowed or denied access, a gap against NIST SP 800-162 (ABAC) and NIST SP 800-53 AU-2/AC-3. **As a result, admins either over-grant access (spillage risk to uncleared or off-program personnel) or under-grant it (operational friction for correctly cleared operators), and security officers cannot reconstruct access decisions during an audit or incident review.**

---

### 2. Unstated Assumptions

| Assumption | Testable Hypothesis | Risk if False | Validation Method |
|-----------|-------------------|---------------|------------------|
| Admins can correctly author a compound attribute rule (clearance >= SECRET AND program = OVERWATCH AND device compliant) without a security-officer correction | If the policy builder shows a live preview of exactly who currently matches the rule before it's saved, 90%+ of admins will produce the intended access set on first try | Rule silently grants access to uncleared/off-program personnel, or locks out correctly cleared operators | Usability testing with 5 system admins using a live-preview policy builder |
| Device-compliance status is available at decision time and current enough to gate access | If compliance is queried fresh (not cached beyond a defined TTL) at each access decision, stale-compliance-based grants drop to near zero | A non-compliant device is granted access based on stale cached status; ATO finding | Technical spike: audit MDM/compliance-attribute query latency and staleness window |
| Every allow/deny decision can be explained in terms of the specific attribute(s) that decided it | If the system logs the deciding attribute(s) — not just "allowed"/"denied" — security officers can answer "why was this person allowed/denied" without escalating to engineering | Audit and incident-response requests go unanswered; AU-2/AU-6 gap | Security officer review of sample decision logs against real access requests |
| Operators authoring or reviewing policy on mobile in the TOC have sufficient screen space and connectivity to do so correctly | If the mobile policy-review flow is usable at TOC bandwidth and screen size, admins won't revert to a desktop-only workaround that delays access changes | Policy changes queue until an admin reaches a desktop, delaying time-sensitive access grants during operations | Field observation + prototype testing with operators on mobile in a simulated TOC environment |
| Personnel-rotation-driven attribute changes (clearance/program) propagate to the access decision fast enough to avoid stale grants | If attribute changes take effect within [X minutes] of the source system update, access reflects a person's current status during high-rotation periods | A rotated-out user retains access after their program affiliation changes; compliance gap | Technical spike: measure attribute-change-to-enforcement latency end-to-end |

---

### 3. Clarifying Questions

1. **Attribute Source of Truth**: Where do clearance, program affiliation, and device-compliance attributes come from today (CAC/PKI, personnel system, MDM), and how current is each? (Approach: Attribute architecture audit + security officer interview)

2. **Policy Authoring Scope**: Which roles can author or modify ABAC policies for classified channels — System Admin only, or can channel owners propose rules subject to security review? (Approach: Role/access design review)

3. **Rotation Handling**: When a user's program affiliation or clearance changes, how quickly must access re-evaluate — real-time, on next login, or batch? (Approach: Technical spike on attribute-change propagation)

4. **Decision Explainability**: What level of detail must the "why allowed/denied" record capture — the matched rule only, or every attribute evaluated including near-misses? (Approach: Security officer interview on incident-response needs)

5. **Mobile/TOC Constraints**: What bandwidth and interaction constraints apply to policy authoring and access-decision review on mobile devices in the TOC? (Approach: Field observation with operators)

---

### 4. Out-of-Scope Adjacent Problems

Clearly mark these as "defer to future effort" to manage expectations and prevent scope creep:

- **Automated attribute provisioning**: Real-time sync of clearance/program data from an authoritative personnel system is a related but distinct integration effort; defer.

- **Cross-domain policy portability**: Exporting or importing ABAC policies across separate classification enclaves is a separate, higher-risk effort; out of scope.

- **End-user-facing access-denial explanations**: Showing operators (not just security officers) why they were denied access is a related UX question; defer to a follow-up effort.

- **Legacy ACL migration**: Converting existing hand-maintained ACLs into equivalent ABAC rules is a one-time migration project, not part of this problem statement.

- **Contractor/temporary-personnel attribute lifecycle**: Automatically expiring or downgrading a contractor's clearance/program attributes when their engagement ends is a related security concern but requires distinct design and compliance work. Defer.

- **Bulk policy import/export**: Authoring one policy at a time via the live-preview builder is in scope; bulk import of many policies via file upload is a separate workflow. Defer.

---

## Output Schema

```json
{
  "problem_statement_bluf": {
    "type": "string",
    "description": "2–3 sentence BLUF-format problem statement focusing on operational and compliance consequences"
  },
  "assumptions": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "assumption": {
          "type": "string",
          "description": "The unstated assumption from the brain dump"
        },
        "testable_hypothesis": {
          "type": "string",
          "description": "How to reframe the assumption as a testable hypothesis"
        },
        "risk_if_false": {
          "type": "string",
          "description": "What breaks if the assumption is wrong?"
        },
        "validation_method": {
          "type": "string",
          "enum": ["user-research", "technical-spike", "audit", "security-review", "data-analysis"],
          "description": "How to validate this assumption"
        }
      },
      "required": ["assumption", "testable_hypothesis", "risk_if_false", "validation_method"]
    }
  },
  "clarifying_questions": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "question": {
          "type": "string",
          "description": "A specific, answerable question"
        },
        "why_it_matters": {
          "type": "string",
          "description": "How does the answer affect design or scope?"
        },
        "validation_approach": {
          "type": "string",
          "description": "How to answer the question (interview, audit, technical spike, etc.)"
        }
      },
      "required": ["question", "why_it_matters", "validation_approach"]
    }
  },
  "out_of_scope_adjacent_problems": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "problem": {
          "type": "string",
          "description": "The adjacent problem"
        },
        "why_out_of_scope": {
          "type": "string",
          "description": "Why it's deferred"
        },
        "suggested_phase": {
          "type": "string",
          "description": "When to address it (Phase 2, parallel effort, etc.)"
        }
      },
      "required": ["problem", "why_out_of_scope"]
    }
  }
}
```

---

## Validation Rules

A high-quality Problem Sharpener output must meet these criteria:

1. **Problem vs. Solution Clarity**:
   - The problem statement describes an operational friction or consequence, not a proposed solution
   - The statement does not assume a solution (e.g., "admins need bulk-invite" is a solution; "admins spend 15min per user on invites" is a problem)
   - If your statement includes a feature name (bulk-invite, auto-sync, etc.), reframe it

2. **BLUF Format**:
   - Starts with the operational context or conclusion
   - Proceeds to the problem and its consequence
   - 2–3 sentences maximum
   - Quantifies consequences (time, compliance risk, security posture) where possible

3. **Quantified Consequences**:
   - Time/effort: "X hours/month," "X minutes per task"
   - Compliance: "Violates [control ID]," "Creates a gap in [framework]"
   - Security: "Insufficient audit trail," "No access control enforcement"
   - User impact: "Delays onboarding by X days," "Creates operational friction"

4. **DoD/IC Terminology**:
   - Uses compliance control names (AC-2, AU-2, etc.) accurately
   - References appropriate frameworks (NIST SP 800-53, DoD ZT RA, DoDM 5200.01)
   - Avoids commercial UX language (e.g., "users want visibility" → "system must provide granular audit trail")

5. **Assumption Count**:
   - Surfaces 4–8 distinct assumptions (fewer than 4 suggests incomplete analysis; more than 8 suggests over-specification)
   - Each assumption is independently testable
   - Assumptions are ranked by risk (highest-risk assumptions first)

6. **Clarifying Questions Quality**:
   - Questions are specific and answerable (not vague)
   - Each question maps to a concrete validation approach (interview, audit, technical spike)
   - Questions address assumptions and unknowns that affect design scope and direction

7. **Out-of-Scope Definition**:
   - Clearly distinguishes between the core problem and adjacent problems
   - Provides reasoning for why each adjacent problem is deferred
   - Suggests a future phase or parallel effort for each deferred problem

---

## Related Skills

- **Assumption Extractor** — Use before or alongside Problem Sharpener to surface additional hidden assumptions
- **Interview Synthesizer** — Use to gather evidence for the problem statement (findings should directly support the BLUF)
- **Standards Mapper** — Use after Problem Sharpener to identify all compliance implications and design constraints
- **traceability-checker** — Use after design to verify the design addresses the problem statement (not scope creep)

---

## Notes for Teams

**Common Pitfalls:**

1. **Confusing the Problem with the Solution** — The most common mistake. A brain dump says "we need bulk-invite" but the actual problem is "admins spend too much time on invites." Separate them ruthlessly.

2. **Skipping Quantification** — "This is a pain point" is not useful. "Admins spend 7–12 hours/month" is actionable. Always quantify consequences in terms of time, compliance, or security.

3. **Ignoring Compliance Context** — In defense systems, every problem should reference compliance implications. "Admins want faster workflows" is commercial language. "Current manual workflow lacks the granular audit trail required for AU-2 compliance" is defense language. Use the latter.

4. **Too Many Clarifying Questions** — Focus on 5–7 questions that directly affect design scope and direction. If you have 15+ questions, you haven't done enough discovery; revisit the research.

5. **Scope Creep in Problem Definition** — A brain dump often includes multiple problems. Identify the core problem; defer others clearly. If your problem statement is long or addresses multiple areas, it's likely too broad.

6. **Assumptions Without Testing Methods** — Every assumption should have a clear validation method. If you can't articulate how to test an assumption, it's not an assumption yet; it's just speculation.

**For Product Managers:**
Use Problem Sharpener to formalize feature requests. It's the bridge between "someone asked for this" and "we understand the problem deeply enough to design a solution." Run every feature request through this skill before kickoff.

**For Designers:**
Use the output to anchor your design decisions. The problem statement is your north star; the assumptions are your design constraints; the clarifying questions are your research roadmap. If your design doesn't address the problem statement, it's off track.

**For Security/Compliance:**
Review the problem statement for compliance implications. The clarifying questions often reveal security architecture work that needs to happen in parallel with design.

**For Leadership:**
Use the out-of-scope adjacent problems to manage stakeholder expectations. Make it clear what is and isn't being addressed in this effort.
