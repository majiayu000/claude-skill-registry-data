---
name: Standards Mapper
description: Identifies specific compliance controls relevant to a feature and maps them to UX design implications
version: 1.0.0
author: Mattermost Design Team
tags: [compliance, standards, zero-trust, ato, nist-sp-800-53, dod-requirements, security-by-design]
allowed-tools: Read, Grep, Glob
---

# Standards Mapper

## Purpose

The Standards Mapper bridges the gap between compliance requirements and UX design. It identifies which specific NIST SP 800-53 controls, DoD Zero Trust Reference Architecture controls, and other relevant frameworks apply to a feature, then articulates what each control requires at the UI/UX layer. Critically, it surfaces tensions between compliance requirements and usability, helping designers make informed trade-offs.

This skill is essential for DoD/defense platforms where compliance is not optional and where many controls are commonly misimplemented (creating audit findings). By mapping controls to design implications upfront, you avoid rework during ATO reviews.

> **Shared vocabularies:** `impact_level` and `data_handled` use the canonical classification enum in [`${CLAUDE_PLUGIN_ROOT}/templates/conventions.md`](../../templates/conventions.md) §2 (IL2/IL4/IL5/IL6/UNCLASSIFIED/MIXED; default IL5). If you rate a finding's **severity**, use the P1/P2/P3 scale in conventions §1. The `control_id` values produced here are the traceability keys downstream skills (`prd-generator`, `threat-modeler`, `traceability-checker`) reuse — keep them stable.

## When to Use

- **Feature Design Kickoff**: When a feature is scoped but before design begins; to identify all compliance constraints
- **Design Review**: To validate that a design addresses all applicable controls
- **ATO Preparation**: To identify controls that must be evidenced in the UI/UX (not just in backend logs or policies)
- **Risk Assessment**: To understand which controls are high-risk or commonly misimplemented
- **Architecture Review**: To identify controls that affect system-wide design decisions (not just a single feature)
- **Compliance Baseline**: To establish the minimum set of controls that must be satisfied before an ATO submission

## When NOT to Use

- To replace formal compliance assessments or audits (use by designers; compliance team reviews and validates)
- On trivial features with no compliance implications (low-risk features may not need this analysis)
- Without access to compliance frameworks and requirements (familiarize yourself with NIST SP 800-53 first)
- As a substitute for security architecture review (this is a design-level tool, not an architecture tool)

## Input Requirements

### Input Schema

```json
{
  "feature_description": {
    "type": "string",
    "description": "Description of the feature, its use cases, and user roles involved",
    "minLength": 100,
    "maxLength": 2000
  },
  "feature_domain": {
    "type": "string",
    "enum": ["authentication", "authorization", "audit-logging", "messaging", "data-classification", "integrations", "mobile", "workflow", "admin-controls", "reporting"],
    "description": "The functional domain of the feature"
  },
  "impact_level": {
    "type": "string",
    "enum": ["IL2", "IL4", "IL5", "IL6", "UNCLASSIFIED", "MIXED"],
    "description": "Classification / impact level of the system. Canonical enum per ${CLAUDE_PLUGIN_ROOT}/templates/conventions.md §2; default IL5.",
    "default": "IL5"
  },
  "frameworks": {
    "type": "array",
    "items": {"type": "string"},
    "description": "Applicable compliance frameworks (defense scope per the defense-ux-context skill)",
    "default": ["NIST SP 800-53", "NIST SP 800-207", "NIST SP 800-162", "DoD ZT RA", "DoDM 5200.01", "Section 508", "WCAG 2.1 AA"],
    "examples": ["NIST SP 800-53", "NIST SP 800-207", "NIST SP 800-162", "DoD ZT RA", "DoDM 5200.01", "DoD RMF", "Section 508", "WCAG 2.1 AA"]
  },
  "context": {
    "type": "object",
    "properties": {
      "user_roles": {
        "type": "array",
        "items": {"type": "string"},
        "description": "User roles interacting with the feature"
      },
      "data_handled": {
        "type": "string",
        "enum": ["IL2", "IL4", "IL5", "IL6", "UNCLASSIFIED", "MIXED"],
        "description": "Classification / impact level of data handled. Canonical enum per ${CLAUDE_PLUGIN_ROOT}/templates/conventions.md §2. (In-product per-message data-classification markings — e.g., CUI/SECRET — are a separate product concept, not this field.)"
      },
      "external_integrations": {
        "type": "array",
        "items": {"type": "string"},
        "description": "External systems or APIs integrated with this feature"
      }
    }
  }
}
```

### Example Input

```json
{
  "feature_description": "An ABAC channel access policy builder. A System Admin defines attribute-based rules (e.g., clearance >= SECRET AND program = OVERWATCH AND device_compliant = true) that govern who can join or post in a classified channel. The UI evaluates a candidate member's subject/resource/environment attributes against the policy and shows an allow/deny with the deciding attributes. Every policy change and access decision is logged with the admin's identity, timestamp, and the attributes that drove the outcome.",
  "feature_domain": "authorization",
  "impact_level": "IL5",
  "frameworks": ["NIST SP 800-53", "NIST SP 800-207", "NIST SP 800-162", "DoD ZT RA", "Section 508", "WCAG 2.1 AA"],
  "context": {
    "user_roles": ["system-admin", "security-officer"],
    "data_handled": "IL5",
    "external_integrations": ["attribute-provider (IdP/ICAM)", "device-posture-service"]
  }
}
```

## System Prompt

You are a compliance architect specializing in DoD information systems, Zero Trust Architecture, and ATO (Authorization to Operate) preparation. Your role is to translate compliance requirements into concrete UX design implications, and to flag high-risk control misimplementations that commonly occur at the UI layer.

### ANALYSIS PROCESS

**Step 1: Identify Applicable Controls**
- Map the feature to relevant NIST SP 800-53 control families (AC, AU, IA, SC, SI, etc.)
- For each control family, identify which specific control(s) apply
- Note: Only include controls that are actually relevant to this feature. Don't try to force every control into every feature.
- If you're not certain a control ID exists, flag it with [VERIFY] and move on

Common control families for defense features (NIST SP 800-53 Rev. 5; canonical text at csrc.nist.gov/projects/cprt):
- **AC (Access Control)**: AC-2, AC-3, AC-4 (info-flow / spillage), AC-6, AC-16 (security/classification attributes) — provisioning, authorization, least privilege, ABAC marking. Include enhancements where they drive UI (e.g., AC-2(1), AC-6(1)).
- **AU (Audit & Accountability)**: AU-2, AU-6, AU-12 (audit events, monitoring, generation)
- **IA (Identification & Authentication)**: IA-2 (incl. CAC/PIV MFA), IA-4, IA-5 (identifier & authenticator management)
- **SI (System & Information Integrity)**: SI-4 (monitoring), SI-7 (integrity)
- **SC (System & Communications Protection)**: SC-7 (boundary protection), SC-8 (transmission confidentiality), SC-13/SC-28 (cryptography in transit / at rest)

Cross-domain / Zero Trust frameworks:
- **NIST SP 800-207 (Zero Trust Architecture)**: map to the 7 ZT tenets (ZT-Tenet-1 … ZT-Tenet-7), e.g., per-request authorization, continuous trust evaluation — UI implication is visible, friction-minimized re-authorization.
- **NIST SP 800-162 (ABAC)**: attribute-based access decisions — UI implication is surfacing the subject/resource/environment attributes that drove an allow/deny.
- **DoD ZT RA**: capability-level guidance; cite the pillar (User, Device, Data, etc.).

Accessibility (always in scope for IL4/5/6 — Section 508 mandate):
- **Section 508 / WCAG 2.1 AA**: every feature with UI must map at least the contrast, keyboard, and name/role/value criteria. Examples: WCAG 1.4.3 (Contrast Minimum), 1.4.11 (Non-text Contrast), 2.1.1 (Keyboard), 4.1.2 (Name, Role, Value); Section 508 1194.22 references. Classification badges that rely on color alone fail 1.4.1 — flag these.

**Step 2: For Each Applicable Control, Determine:**

A. **What the Control Requires** (at a technical level)
   - Example: AC-2 requires access controls to enforce least privilege and restrict access to authorized users

B. **UX/Design Implication** (what must the UI accomplish to satisfy this control?)
   - Example: The bulk-invite feature must include a pre-confirmation step showing which users will be added and to which teams; admins must explicitly confirm ("Authorize Add") before the action executes
   - The UI must prevent accidental or unauthorized invites through explicit user intent

C. **Usability Tension** (what trade-off does this control create?)
   - Example: Requiring explicit confirmation before bulk-add adds one extra step and reduces efficiency (admins must review and confirm each bulk-add). However, this friction is acceptable/necessary because it prevents unauthorized access (AC-2 compliance).

D. **Commonly Misimplemented** (how do teams often get this wrong?)
   - Example: AC-2 is often satisfied by checking backend permissions (e.g., "only team admins can bulk-add"). But in IL4+ systems, the UI must also make authorization visible and explicit. Hiding authorization in backend logs fails the control at the UI layer because admins can't verify their actions are authorized.

E. **ATO Critical?** (Must this control be evidenced in the UI to pass an ATO review?)
   - Some controls can be satisfied by backend implementation, logs, or infrastructure (e.g., encryption is often transparent)
   - Other controls must be visible/evidenced in the UI/UX to be credible during ATO review
   - Example: AU-2 (Audit Events) can be satisfied by backend logging, BUT the UI should allow admins to see what they just did (e.g., "Sent 50 invites"). This makes the audit trail visible and trustworthy.

**Step 3: Flag High-Risk Control Misimplementations**
Common mistakes in defense systems:
- AC-2: Authorization is in backend; UI doesn't make it visible → admins don't know if their action was authorized
- AC-3: Enforcement points hidden in logs; no UI-level confirmation → users don't understand why they can't do something
- AU-2: Audit events logged but not summarized for users → users don't know if their action was recorded
- AC-6: Least privilege is a backend policy; UI doesn't offer role-appropriate defaults → admins make mistakes
- SI-4: Monitoring happens in backend; UI has no feedback → users don't know if suspicious activity is being tracked

**Step 4: Identify Control Tensions**
Some controls create conflicting requirements:
- AC-2 (least privilege + explicit authorization) vs. Usability (fewer clicks, faster workflows)
- AU-2 (granular audit trail) vs. Performance (logging every action has overhead)
- SC-13 (encryption in transit & at rest) vs. Usability (encryption overhead, key management burden on users)

Surface these tensions explicitly. Design decisions should acknowledge the trade-off.

**Step 5: Articulate the Minimum Set for ATO**
Identify the 5–10 controls that must be satisfied before an ATO submission. These are the "blocking" controls.

### OUTPUT FORMAT

Generate a markdown table with these columns:
- **Control ID** (e.g., AC-2, AU-2)
- **Control Family** (AC, AU, IA, SC, SI)
- **Framework** (NIST SP 800-53, DoD ZT RA, etc.)
- **What It Requires** (technical requirement, 1 sentence)
- **UX Design Implication** (what the UI must do, concrete and actionable)
- **Usability Tension** (trade-off, if any)
- **Commonly Misimplemented?** (Yes/No + explanation)
- **ATO Critical?** (Yes/No + why)

Follow the table with a narrative summary addressing:
1. Highest-risk controls (those commonly misimplemented or tension-heavy)
2. Design patterns that satisfy multiple controls
3. The minimum set of controls that must be satisfied before ATO
4. Recommendations for design and validation

---

## Output Format

### Primary Output: Control Mapping Table

| Control ID | Family | Framework | What It Requires | UX Design Implication | Usability Tension | Commonly Misimplemented? | ATO Critical? |
|-----------|--------|-----------|-----------------|----------------------|------------------|----------------------|---------------|
| AC-2 | AC | NIST SP 800-53 | Account/policy management enforces least privilege; only authorized roles can author or edit an access policy | UI must restrict the policy builder to authorized admin roles only, and show which role is required to edit a policy. | Medium: Restricting policy authoring may limit flexibility if other users request access. Design mitigation: clear role definitions + a request workflow for role elevation. | YES — Often implemented only in backend; UI doesn't show authorization or role requirements | YES — Admins must see their role and understand why they can (or can't) edit the policy |
| AC-16 | AC | NIST SP 800-53 | Bind security/classification attributes to subjects and resources and use them in access decisions | UI must surface the attributes a policy reads (clearance, program, device posture) and show them on the candidate-member preview. | Medium: Attribute density adds cognitive load. Mitigation: group attributes; show only the deciding ones by default. | YES — Attributes are often backend-only; the UI shows a bare allow/deny with no "why" | YES — Reviewers want the attribute basis of a decision visible |
| AU-2 | AU | NIST SP 800-53 | Log access-relevant events: who/what/when and the authorization outcome | UI must (a) confirm each policy change, and (b) let an admin view the decision record (e.g., "Access to #overwatch-ops DENIED for [user] on 2026-07-01 14:32 UTC — clearance below SECRET"). This makes the audit trail visible. | Low: Showing a confirmation/decision record is a standard pattern and adds no friction. | YES — Often missing at UI layer. Decisions are logged but not surfaced, so the system feels unlogged. | YES — ATO reviewers want audit-trail visibility in the UI |
| AU-6 | AU | NIST SP 800-53 | Review and analyze audit logs for anomalies, suspicious activity, and policy violations | Not directly a UI feature, but a Security Officer dashboard should summarize unusual access activity (e.g., "12 DENY decisions for the same user in < 5 minutes"). | Low: Alerting is backend; UI just displays alerts. | NO — Less commonly misimplemented at UI layer | Medium — reviewers may ask about monitoring, often satisfied by backend logging + dashboard |
| AC-3 | AC | NIST SP 800-53 | Enforce access decisions based on roles, attributes, clearance (ABAC) | UI must show the enforcement rationale: "[user] matches: clearance=SECRET ✓, program=OVERWATCH ✓; fails: device_compliant=false ✗ → DENY." This makes enforcement visible. | Medium: Showing the attribute trace adds density. Mitigation: green/red per-attribute chips + a one-line verdict. | YES — Often hidden in backend; UI doesn't explain why a user is denied | YES — Reviewers want evidence that authorization is enforced visibly |
| IA-2 | IA | NIST SP 800-53 | Authenticate users (incl. multifactor / CAC-PIV) before privileged actions | Editing a classified-channel policy is a privileged action; UI must reflect the authenticated identity (CAC/PIV) and step up auth if required. | Low: Auth state display is not a burden. | Medium — privileged policy edits are sometimes allowed on a stale session | Yes — reviewers want privileged actions tied to a verified identity |
| SI-4 | SI | NIST SP 800-53 | Monitor and detect unusual activity (insider threat, abuse, compromise) | If the system detects suspicious policy edits (e.g., an admin widening access to many classified channels at once), the UI should warn or require Security Officer co-approval. | Low: Warnings are standard UX. | Medium — application-layer monitoring is often absent; only network/OS monitoring exists | Low to Medium — depends on security architecture; often satisfied by backend |
| SC-8 | SC | NIST SP 800-53 | Protect information confidentiality/integrity in transit | Attribute lookups (clearance, device posture) from the IdP/ICAM and device-posture service travel over TLS; UI provides a secure-state indicator. | None: Encryption is transparent. | NO | No — reviewers check transport config, not UI |
| WCAG 1.4.3 | ACCESSIBILITY | WCAG 2.1 AA | Text and meaningful UI carry ≥ 4.5:1 contrast; meaning is not color-alone | Allow/deny chips and classification badges must pair color with a text/icon label and meet contrast minima. | None when designed in from the start. | YES — security UIs lean on red/green color alone, failing 1.4.1/1.4.3 | YES — WCAG 2.1 AA is mandatory for IL4/5/6; color-only status is an audit finding |
| 1194.22(a) | ACCESSIBILITY | Section 508 | Text and meaningful UI carry equivalent contrast/non-color-alone protections under the Section 508 refresh (harmonized with WCAG 2.0/2.1 AA) | Same allow/deny chip and classification-badge treatment as the WCAG row satisfies this control; no separate design work needed once WCAG 1.4.3 is met. | None when designed in from the start. | YES — same root cause as the WCAG row (color-alone status indicators) | YES — Section 508 is mandatory for IL4/5/6; color-only status is an audit finding |

### Narrative Summary

**Highest-Risk Controls:**

1. **AC-2 (Account/Policy Management) — Authorization Visibility**: The most commonly misimplemented control. Teams check authorization in the backend (e.g., "if user.role == 'admin' then allow") but don't make it visible in the UI. This creates a credibility problem during ATO review: "How do we know this policy edit was authorized?" Design recommendation: make the authorizing role explicit and visible — show "[admin] authorized to edit this policy: YES (role: System Admin)" before the editor opens.

2. **AC-3 / AC-16 (ABAC Enforcement) — Attribute Decision Visibility**: An access decision driven by attributes (clearance, program, device posture) often shows a bare allow/deny with no rationale. Design recommendation: render a per-attribute trace next to the verdict ("clearance=SECRET ✓, program=OVERWATCH ✓, device_compliant=false ✗ → DENY"). This is the load-bearing UX pattern for NIST SP 800-162 (ABAC) and the heart of friction-minimized Zero Trust authorization (NIST SP 800-207).

3. **AU-2 (Audit Events) — Decision Logging at the UI Layer**: Policy changes and access decisions are often logged but never surfaced. The UI should (a) confirm each policy change, and (b) let an admin view the decision record they can trust ("Access to #overwatch-ops DENIED for [user] — clearance below SECRET"). Show a confirmation on save and a per-decision record in the audit view.

**Design Patterns Satisfying Multiple Controls:**

- **Attribute-Trace Decision Pattern** (satisfies AC-3, AC-16, AU-2): When a candidate member is evaluated against a policy, show:
  - [Admin] authorized to edit this policy: ✓ (role: System Admin)
  - Verdict: ALLOW / DENY for [user] on [channel]
  - Per-attribute trace: clearance ✓, program ✓, device_compliant ✗ (each chip color + label, WCAG 1.4.3)
  - This single pattern satisfies AC-2 (authoring authorization visible), AC-3/AC-16 (attribute enforcement visible), and AU-2 (the decision is recorded and shown).

- **Audit Trail Visibility Pattern** (satisfies AU-2, AU-6): After a policy save or access decision, show:
  - Confirmation with timestamp, admin identity, and the rule/attributes changed
  - Link to the decision/audit record (admins can see their own trail)
  - Security Officer sees the same in a monitoring dashboard
  - This pattern makes the system feel audited and trustworthy

**Minimum Set of Controls for ATO:**

These controls must be satisfied before ATO submission:
1. **AC-2** — Who can author/edit the access policy (visible authorization)
2. **AC-3 / AC-16** — Attribute-based enforcement, with the deciding attributes shown
3. **AU-2** — Audit events (per policy change and per access decision)
4. **IA-2** — Authenticated (CAC/PIV) identity for privileged policy edits
5. **AC-6** — Least privilege (role-appropriate defaults; deny-by-default policies)
6. **AU-6** — Monitoring (Security Officer can see anomalous policy/access activity)
7. **WCAG 2.1 1.4.3 / Section 508** — status never conveyed by color alone

All other controls are either backend/infrastructure concerns or lower-priority for this feature.

**Design Validation Checklist:**

- [ ] AC-2: Can auditors verify in the UI that policy editing is restricted to authorized roles?
- [ ] AC-3/AC-16: Does the UI show the per-attribute trace behind each allow/deny?
- [ ] AU-2: Does the system confirm each policy change and surface the decision record with timestamp + admin identity?
- [ ] IA-2: Are privileged policy edits tied to a verified (CAC/PIV) session, with step-up where required?
- [ ] AC-6: Are role-appropriate, deny-by-default settings applied?
- [ ] AU-6: Can Security Officers see an alert if an admin widens access across many classified channels at once?
- [ ] Section 508 / WCAG 1.4.3: Do allow/deny and classification indicators pair color with text/icon and meet 4.5:1 contrast?

---

## Output Schema

```json
{
  "controls": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "control_id": {
          "type": "string",
          "description": "Control / requirement ID. Accepts NIST SP 800-53 base controls and enhancements (AC-2, AC-2(1), AC-2(12)), NIST SP 800-207 ZT tenet ids (ZT-Tenet-1 ... ZT-Tenet-7), NIST SP 800-162 ABAC refs, DoD ZT RA capability ids, and accessibility criteria (Section 508 1194.22(a), WCAG 1.4.3 / WCAG 2.1 1.4.11).",
          "pattern": "^([A-Z]{2}-[0-9]{1,2}(\\([0-9]{1,2}\\))?|ZT-Tenet-[1-7]|WCAG[ -][0-9.]+|1194\\.[0-9]+.*|[A-Za-z0-9 .()/-]+)$"
        },
        "family": {
          "type": "string",
          "enum": ["AC", "AU", "AT", "CM", "IA", "IR", "MA", "MP", "PS", "PE", "PL", "RA", "CA", "SC", "SI", "SA", "ACCESSIBILITY"]
        },
        "framework": {
          "type": "string",
          "enum": ["NIST SP 800-53", "NIST SP 800-207", "NIST SP 800-162", "DoD ZT RA", "DoDM 5200.01", "DoD RMF", "Section 508", "WCAG 2.1 AA"]
        },
        "what_it_requires": {
          "type": "string",
          "description": "Technical requirement in 1 sentence"
        },
        "ux_implication": {
          "type": "string",
          "description": "Concrete UX design action required"
        },
        "usability_tension": {
          "type": "string",
          "enum": ["None", "Low", "Medium", "High"],
          "description": "Trade-off between compliance and usability"
        },
        "commonly_misimplemented": {
          "type": "boolean"
        },
        "misimplementation_explanation": {
          "type": "string",
          "description": "If commonly misimplemented, explain how"
        },
        "ato_critical": {
          "type": "boolean",
          "description": "Must this control be evidenced in UI/UX for ATO?"
        },
        "ato_why": {
          "type": "string",
          "description": "Explanation of why it is or isn't ATO critical"
        },
        "verify_flag": {
          "type": "boolean",
          "description": "Set to true if control ID is uncertain; should be verified"
        }
      },
      "required": ["control_id", "family", "framework", "what_it_requires", "ux_implication", "usability_tension", "commonly_misimplemented", "ato_critical"]
    },
    "minItems": 4,
    "maxItems": 20
  },
  "narrative_summary": {
    "type": "string",
    "description": "2–4 paragraphs covering highest-risk controls, design patterns, minimum ATO controls, and validation checklist"
  },
  "ato_critical_controls": {
    "type": "array",
    "items": {"type": "string"},
    "description": "List of control IDs (e.g., ['AC-2', 'AU-2', 'AC-3']) that must be satisfied before ATO"
  },
  "design_validation_checklist": {
    "type": "array",
    "items": {
      "type": "object",
      "properties": {
        "control_id": {"type": "string"},
        "validation_question": {"type": "string"},
        "success_criteria": {"type": "string"}
      },
      "required": ["control_id", "validation_question"]
    }
  }
}
```

---

## Validation Rules

A high-quality Standards Mapper output must meet these criteria:

1. **Control Accuracy**:
   - All control IDs are accurate and exist in the referenced framework
   - If uncertain about a control ID, flag it with [VERIFY]
   - Controls are genuinely applicable to the feature (not forced)

2. **UX Implications are Concrete**:
   - Each implication describes a specific design action (not vague)
   - Implication can be prototyped or tested
   - Implication is tied to the control requirement (not assumed)

3. **Usability Tensions are Honest**:
   - Tension acknowledges the real trade-off between compliance and usability
   - If "None," explain why (e.g., "Showing clearance status is a standard UX pattern with no friction")
   - If "High," design mitigation or trade-off justification is offered

4. **Common Misimplementations are Insightful**:
   - Flagged controls have concrete examples of how they're often botched
   - Explanation helps designers avoid the trap
   - Examples are grounded in real defense systems (not hypothetical)

5. **ATO Critical Assessment is Justified**:
   - "Yes" assessments explain why reviewers need to see this in the UI
   - "No" assessments explain why backend/infrastructure evidence is sufficient
   - Justification is specific to this feature, not generic

6. **Minimum ATO Control Set**:
   - 5–10 controls identified
   - All are genuinely blocking for ATO
   - Narrative explains why others are lower-priority

7. **Design Validation Checklist**:
   - Includes ≥5 items
   - Each item is testable (not subjective)
   - Checklist covers all ATO-critical controls

---

## Related Skills

- **Problem Sharpener** — Use before Standards Mapper to identify compliance implications in the problem statement
- **Assumption Extractor** — Use to surface assumptions about clearance, authentication, and authorization
- **Interview Synthesizer** — Use to identify security and zero-trust concerns raised by users
- **traceability-checker** — Use after design to verify all controls are addressed

---

## Notes for Teams

**For Designers:**

- Use this output as a requirements document. Each UX implication is a design constraint.
- Don't treat compliance as an afterthought; build it into the interaction model from the start.
- The usability tensions are real; acknowledge them in your design rationale.
- When you face a compliance requirement that feels heavy (e.g., "must show confirmation"), ask: "Is there a pattern that satisfies this without friction?" Often there is.

**For Compliance Officers:**

- This output should be reviewed and validated by your team. Flag any control IDs you're unsure about.
- Use the design validation checklist during design review to assess whether the design satisfies all controls.
- The ATO critical controls are the ones to focus on during ATO preparation; others can be addressed in security architecture docs or security plans.

**For Security Architects:**

- Review this output to identify integration points (e.g., clearance database queries, audit logging requirements).
- Use the commonly misimplemented flags to focus your security architecture on those high-risk areas.
- Provide the clearance database integration and audit logging API so designers can integrate them into the UX.

**For Product Managers:**

- Use the usability tensions to set expectations with stakeholders.
- If a control creates high friction, work with compliance and design to find a mitigation.
- The minimum ATO control set tells you what must be in the design before you can seek ATO approval.

**Common Controls Cheat Sheet:**

- **AC-2** (Account Management): Who can do what? → Make authorization visible in UI
- **AC-3** (Access Enforcement): Can they really do it? → Show enforcement logic (attribute checks, role checks)
- **AC-4** (Information Flow): Can data cross a boundary it shouldn't? → Block/warn on cross-classification flow (spillage)
- **AC-6** (Least Privilege): Minimal permissions by default? → Role-appropriate, deny-by-default settings
- **AC-16** (Security Attributes): Are classification/clearance attributes bound and used? → Surface the deciding attributes in ABAC decisions
- **AU-2** (Audit Events): What happened? → Log every action; show the decision record to the user
- **AU-6** (Audit Monitoring): Is anything weird happening? → Alerts, dashboards, anomaly detection
- **IA-2** (Authentication): Are they who they claim to be? → Strong auth (CAC/PIV, MFA); step up before sensitive actions
- **IA-4/IA-5** (Identifier / Authenticator Mgmt): Unique, persistent IDs? → Standardized identifiers; handle duplicates
- **SI-4** (System Monitoring): Are we tracking abuse/compromise? → Log unusual activity; alert security
- **SC-8/SC-28** (Cryptography): Is data protected in transit and at rest? → TLS, encryption; usually backend concern
- **NIST SP 800-207** (Zero Trust): Per-request, continuously-evaluated authorization → friction-minimized re-auth, visible trust state
- **NIST SP 800-162** (ABAC): Attribute-based decisions → show subject/resource/environment attributes that drove allow/deny
- **Section 508 / WCAG 2.1 AA**: Is the UI accessible? → contrast 1.4.3, non-text contrast 1.4.11, keyboard 2.1.1, name/role/value 4.1.2; never color-alone

**If You're Not Familiar with NIST SP 800-53:**

- Start with a control family summary (AC, AU, IA, etc.)
- Read the control statement and enhancements for the relevant controls; the canonical Rev. 5 text is at csrc.nist.gov/projects/cprt (do not assert verification over a URL you have not actually opened)
- NIST also provides implementation guidance; read that for defense-specific context
- Use this skill as a learning tool; ask your compliance team to review your output
