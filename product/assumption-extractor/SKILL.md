---
name: Assumption Extractor
description: Identifies unstated assumptions in early-phase artifacts that could invalidate the design
version: 1.0.0
author: Mattermost Design Team
tags: [requirements-analysis, risk-mitigation, problem-discovery, defense-ux]
allowed-tools: Read, Grep, Glob
---

# Assumption Extractor

## Purpose

The Assumption Extractor surfaces hidden dependencies, implicit user knowledge requirements, and environmental assumptions embedded in problem statements, brain dumps, and early-phase design artifacts. By making assumptions explicit and testable, this skill reduces the risk of building features that fail in production due to invalid preconditions.

This is particularly critical for DoD/defense platforms where unstated assumptions about security boundaries, clearance levels, network topology, or mission context can have operational consequences.

> **Shared vocabularies:** `mission_tier` uses the canonical classification enum in [`${CLAUDE_PLUGIN_ROOT}/templates/conventions.md`](../../templates/conventions.md) §2 (IL2/IL4/IL5/IL6/UNCLASSIFIED/MIXED; default IL5). The `risk_level` column (HIGH/MEDIUM/LOW) rates *how damaging it is if an assumption is wrong* — it is an input to design risk, distinct from the P1/P2/P3 finding-severity scale in conventions §1, which the downstream `edge-case-hunter`/`threat-modeler` apply.

## When to Use

- **Early Problem Definition**: Before a problem statement is finalized; after initial brain dump but before user research
- **Feature Kickoff**: When a feature brief or PRD is handed off to the design team
- **Design Review**: When a design solution seems elegant but its dependencies aren't documented
- **Risk Assessment**: Before proposing a solution to stakeholders; to identify what must be validated
- **Cross-Team Alignment**: When communicating assumptions with engineering, product, and security teams
- **Legacy Feature Analysis**: When reverse-engineering the unstated assumptions in an existing feature

## When NOT to Use

- To replace user research or requirements validation (use after gathering evidence, not instead of it)
- As a tool for vetting final designs (use earlier in the discovery phase)
- To generate exhaustive lists of every conceivable assumption (focus on assumptions that, if wrong, materially affect the design)

## Input Requirements

### Input Schema

```json
{
  "artifact_text": {
    "type": "string",
    "description": "The artifact to analyze: brain dump, problem statement, feature brief, design proposal, or research notes",
    "minLength": 100,
    "maxLength": 5000
  },
  "feature_domain": {
    "type": "string",
    "enum": ["authentication", "messaging", "permissions", "audit", "integration", "mobile", "workflow", "search", "analytics", "admin", "compliance"],
    "description": "The functional area the artifact addresses"
  },
  "mission_tier": {
    "type": "string",
    "enum": ["IL2", "IL4", "IL5", "IL6", "UNCLASSIFIED", "MIXED"],
    "description": "Classification / impact level of the system; affects which assumptions are relevant. Canonical enum per ${CLAUDE_PLUGIN_ROOT}/templates/conventions.md §2; default IL5.",
    "default": "IL5"
  },
  "context": {
    "type": "object",
    "properties": {
      "user_roles": {
        "type": "array",
        "items": {"type": "string"},
        "description": "Roles mentioned or implied in the artifact (e.g., 'admin', 'end-user', 'security-officer')"
      },
      "related_systems": {
        "type": "array",
        "items": {"type": "string"},
        "description": "External systems, APIs, or integrations mentioned or implied"
      }
    }
  }
}
```

### Example Input

```json
{
  "artifact_text": "Admins need a way to control classified-channel access with attribute-based rules instead of hand-managed ACLs. They should define a policy (e.g., clearance >= SECRET AND program = OVERWATCH AND device is compliant), see a live preview of who matches, and apply it. Access should be re-evaluated continuously so a user who loses an attribute is removed automatically.",
  "feature_domain": "permissions",
  "mission_tier": "IL5",
  "context": {
    "user_roles": ["admin", "security-officer"],
    "related_systems": ["IdP / ICAM attribute provider", "device-posture service", "Mattermost channels"]
  }
}
```

## System Prompt

You are a principal UX designer and systems thinker specializing in DoD/defense collaboration platforms. Your role is to systematically uncover unstated assumptions in design artifacts that could lead to misaligned requirements, failed deployments, or security vulnerabilities.

When analyzing the provided artifact, extract all unstated assumptions and categorize each as:

### 1. USER ASSUMPTIONS
What the author assumes about user behavior, knowledge, mental models, or operational environment.
- Examples: "Assumes admins understand LDAP schema syntax", "Assumes users have reliable network connectivity", "Assumes all team leads have been trained on the feature"
- These are often the most design-critical because they determine information architecture, interaction complexity, and error handling

### 2. SYSTEM ASSUMPTIONS
What the author assumes about Mattermost capabilities, integrations, state management, or persistence.
- Examples: "Assumes LDAP sync is bi-directional", "Assumes real-time database replication", "Assumes mobile app supports this interaction pattern"
- These affect technical feasibility and downstream design decisions

### 3. SECURITY ASSUMPTIONS
What the author assumes about trust boundaries, classification levels, access controls, audit trails, or identity verification.
- Examples: "Assumes all channel members have the same clearance level", "Assumes only authorized admins can access bulk-invite features", "Assumes audit logging captures all user additions"
- These are high-risk; violations can create compliance gaps or unauthorized access

### 4. ENVIRONMENTAL ASSUMPTIONS
What the author assumes about the deployment context, network topology, device constraints, or external service availability.
- Examples: "Assumes internet connectivity for external API calls", "Assumes screen width ≥ 1024px", "Assumes admin uses desktop, not mobile", "Assumes LDAP server is always available"
- These affect rollout scope, feature graceful degradation, and offline-first design

### ANALYSIS PROCESS
1. Read the artifact carefully, highlighting any statement that depends on an unstated condition
2. For each assumption, ask: "What would break if this assumption were false?"
3. Only surface assumptions where the answer is meaningful (design fails or experience degrades materially)
4. Avoid listing obvious, universally-held assumptions (e.g., "assumes the internet exists")
5. Rate risk: HIGH (design fails), MEDIUM (degraded experience but feature remains usable), LOW (minor issue or edge case)
6. Always frame the clarifying question as something that can be answered through user research, audit, or technical investigation

### OUTPUT FORMAT
Generate a markdown table with these columns:
- **Category** — USER / SYSTEM / SECURITY / ENVIRONMENT
- **Assumption** — The assumption stated explicitly
- **Risk if Wrong** — HIGH / MEDIUM / LOW
- **Clarifying Question** — A testable question to validate this assumption
- **Research Method** — How to answer the question (user interview, audit, technical spike, etc.)

Follow the table with a brief narrative summary (2–3 paragraphs) of the highest-risk assumptions and their design implications. Highlight any assumptions that conflict with each other or with known constraints.

---

## Output Format

### Primary Output: Assumption Table

| Category | Assumption | Risk if Wrong | Clarifying Question | Research Method |
|----------|-----------|---------------|--------------------|-----------------|
| SECURITY | The attribute provider (IdP/ICAM) is the authoritative, current source for clearance and program attributes | HIGH | Where do clearance/program attributes originate, and what is the lag between a real-world change and the attribute updating? | Audit attribute provider; interview security officer |
| SYSTEM | Access is re-evaluated continuously, so losing an attribute removes a user automatically | HIGH | Is enforcement point-in-time (only at join) or continuous? What happens to an active session when an attribute changes? | Technical requirements review; ABAC engine audit |
| USER | Admins can express their intended access set as an attribute rule without help | MEDIUM | Can admins translate "the OVERWATCH planners" into clearance/program/device predicates? Do they need a live match preview? | Admin interviews; usability test of the policy builder |
| ENVIRONMENT | The attribute provider and device-posture service are available and responsive during a policy evaluation | MEDIUM | What is the availability SLA? What is the fail-safe when an attribute can't be read — deny, or last-known-good? | Infrastructure audit; failure-mode design review |

### Summary Narrative

**Highest-Risk Assumptions:**

1. **Attribute Freshness & Continuous Enforcement** — The artifact implies attributes always reflect reality and access updates automatically. In IL5/Zero Trust environments (NIST SP 800-207), stale attributes are a spillage vector. Critical question: is enforcement continuous or point-in-time, and what is the attribute-update lag? Design must show attribute freshness and define fail-safe behavior when an attribute can't be read.

2. **Attribute Authority & Homogeneity** — The policy assumes the attribute provider is authoritative and that everyone matching a rule is genuinely cleared for the channel's content. In practice attribute sources lag and overlap. Design must account for: (a) validating attributes before grant, (b) handling users whose attributes are unknown/expired, (c) logging every allow/deny with the deciding attributes (AC-16, AU-2).

3. **Admin Expertise** — Authoring an attribute rule assumes admins can translate intent ("the OVERWATCH planners on compliant devices") into predicates. Research must determine whether a live match-preview and attribute picker are needed to prevent over- or under-grant.

**Design Implications:**
- Show a live preview of who matches a rule before it is applied (catch over/under-grant)
- Render the per-attribute trace behind every allow/deny (AC-3/AC-16 visibility)
- Define explicit fail-safe behavior (default-deny) when an attribute source is unavailable
- Surface attribute freshness per user-session so admins know the decision basis is current

---

## Usage Example

### Scenario
A product manager provides this brain dump for a new feature:

**Input Artifact:**
> "We want operators to be able to mark an individual message as SECRET even in a lower-classification channel, and have the system warn them before it reaches anyone without the clearance to see it."

### Invocation
```
Skill: Assumption Extractor
Input:
  artifact_text: "We want operators to be able to mark an individual message as SECRET even in a lower-classification channel, and have the system warn them before it reaches anyone without the clearance to see it."
  feature_domain: "messaging"
  mission_tier: "IL5"
  context:
    user_roles: ["operator", "security-officer"]
    related_systems: ["IdP / ICAM attribute provider", "Mattermost channels"]
```

### Output
| Category | Assumption | Risk if Wrong | Clarifying Question | Research Method |
|----------|-----------|---------------|--------------------|-----------------|
| USER | Operators correctly judge the classification of their own message before marking it | MEDIUM | How do operators decide a message is SECRET vs CONFIDENTIAL today? Is there guidance or a default? | Operator interviews; observe current marking behavior |
| SECURITY | The system can read every recipient's clearance attribute at send time to warn on a mismatch | HIGH | Where do recipient clearance attributes come from, and what happens if one is unknown — block or warn? | Security requirements review; attribute-provider audit |
| SYSTEM | Channel-level classification and message-level classification are enforced independently | HIGH | Can a SECRET message live in a CONFIDENTIAL channel without exposing it to under-cleared members already in that channel? | Technical requirements review; ABAC enforcement audit |
| ENVIRONMENT | Mobile (TOC) surfaces the same classification marker and pre-send warning as desktop | MEDIUM | Does the mobile composer show the marker and warning at the same prominence? | Mobile usability test with operators |
| SECURITY | Every classification action (mark, downgrade, override-send) is logged and attributed | HIGH | Does the audit log capture each marking and each warning-override individually, with who/when/why? | Audit logging review; compliance requirements check |

**Narrative Summary:**

The artifact glosses over a critical security assumption: message-level classification can leak if the channel already contains under-cleared members. The highest risk is SECURITY — the system must read recipient clearance at send time and define a fail-safe (default-deny on unknown clearance) per NIST SP 800-207. In IL5 environments this likely requires a pre-send warning that names the under-cleared recipients (AC-3/AC-16 visibility) and logs any override (AU-2).

Secondary concern: mobile parity. If the TOC mobile composer renders the classification marker or warning less prominently than desktop, the guardrail fails for the primary field interface.

---

## Output Schema

```json
{
  "assumptions_table": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "category": {
          "type": "string",
          "enum": ["USER", "SYSTEM", "SECURITY", "ENVIRONMENT"]
        },
        "assumption": {
          "type": "string",
          "description": "The unstated assumption, stated explicitly"
        },
        "risk_level": {
          "type": "string",
          "enum": ["HIGH", "MEDIUM", "LOW"]
        },
        "clarifying_question": {
          "type": "string"
        },
        "research_method": {
          "type": "string",
          "enum": ["user-interview", "admin-interview", "security-audit", "technical-spike", "compliance-review", "infrastructure-audit", "design-review"]
        }
      },
      "required": ["category", "assumption", "risk_level", "clarifying_question", "research_method"]
    }
  },
  "narrative_summary": {
    "type": "string",
    "description": "2–3 paragraph narrative highlighting highest-risk assumptions and design implications"
  },
  "highest_risk_categories": {
    "type": "array",
    "items": {"type": "string"},
    "description": "Categories with the most HIGH-risk assumptions"
  }
}
```

---

## Validation Rules

A high-quality Assumption Extractor output must meet these criteria:

1. **Scope**: Surfaces 5–12 distinct assumptions. Fewer than 5 suggests incomplete analysis; more than 12 suggests over-specification.

2. **Assumption Quality**:
   - Each assumption is stated in a single, clear sentence
   - The assumption can be tested or verified (not vague)
   - If the assumption is wrong, the design materially fails or experiences significant degradation
   - Avoids "universal" assumptions (e.g., "assumes electricity exists")

3. **Risk Rating Accuracy**:
   - HIGH-risk assumptions directly threaten security, compliance, or core functionality
   - MEDIUM-risk assumptions degrade UX or introduce edge cases
   - LOW-risk assumptions are optional optimizations or minor edge cases

4. **Clarifying Questions**:
   - Each question is answerable through research, audit, or technical investigation
   - Questions are specific enough to guide the next step (avoid vague questions like "Is this true?")
   - Questions surface testable hypotheses, not opinions

5. **Narrative Summary**:
   - Identifies the top 2–3 assumptions with the highest design impact
   - Explains why each assumption matters for this feature
   - Proposes a concrete design implication or research direction

6. **Context-Appropriate**:
   - Assumptions reflect the mission tier (IL4 designs surface clearance/classification concerns; IL2 designs may not)
   - SECURITY category assumptions are prominent in IL4+ systems
   - Questions reference appropriate stakeholders (security officer, compliance, infrastructure team)

---

## Related Skills

- **Problem Sharpener** — Use after Assumption Extractor to refine the problem statement by addressing top assumptions
- **Interview Synthesizer** — Use to gather data answering the clarifying questions surfaced by Assumption Extractor
- **Standards Mapper** — Use to identify compliance implications of SECURITY assumptions
- **traceability-checker** — Use to verify that the final design addresses each assumption

---

## Notes for Teams

**Common Pitfalls:**

1. **Confusing Assumptions with Requirements** — An assumption is something the author takes for granted without stating it. A requirement is an explicit demand. If the artifact says "users must have ≥ IL4 clearance," that's a requirement, not an assumption.

2. **Ignoring SECURITY Assumptions in Lower-Tier Systems** — Even IL2 systems have security assumptions (e.g., "only team members can see channel content"). Don't skip SECURITY category analysis.

3. **Missing Environmental Assumptions** — The most fragile assumptions are often about the deployment context (network, device, availability). Ask: "What if this assumption is false in a real deployment?"

4. **Assumptions vs. Design Decisions** — "The UI will have a confirm dialog" is a design decision. "The admin will not accidentally bulk-invite the wrong users" is an assumption. Focus on assumptions, not decisions.

**For Product Managers:**
Use this skill to de-risk requirements kickoff. Before handing off a feature to design, run it through Assumption Extractor. The output becomes your research roadmap.

**For Designers:**
Use this skill during design review to document the preconditions your design depends on. Share the output with engineers and QA so they understand what to validate.

**For Security/Compliance:**
Use this skill to identify authorization, audit, and clearance assumptions that must be validated before ATO submission.
