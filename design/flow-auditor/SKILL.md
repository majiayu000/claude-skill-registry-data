---
name: Flow Auditor
description: Reviews user flows for missing paths, security bypasses, and navigation deviations in DoD collaboration specs
version: 1.0.0
author: Mattermost Design Team
tags: [ux-spec, security-review, user-flows, dod-compliance, threat-modeling]
allowed-tools: Read, Grep, Glob
---

# Flow Auditor

A specialized security and UX review skill that audits user journey flows against product requirements, security constraints, and established navigation patterns. Designed for DoD and defense collaboration platforms where missing flow paths can create security vulnerabilities.

## When to Use

- **Reviewing completed user flow diagrams** before they enter the UX spec writing phase
- **Validating flow coverage** against a defined PRD with specific user roles
- **Security threat modeling** on flows that handle sensitive or classified information
- **Identifying mobile-specific scenarios** that desktop flows don't address
- **Checking consistency** with existing Mattermost navigation patterns to prevent user confusion
- **Early phase gate review** before investing in detailed spec writing on incomplete flows

## When NOT to Use

- For reviewing flows that haven't been visualized or documented yet (collect basic flow data first)
- For reviewing design mockups or wireframes (use a visual/design review skill instead)
- For validating implementation against a completed spec (this reviews the spec creation inputs, not outputs)
- For accessibility review (that is a separate specialized review)
- When you have fewer than 2 distinct user roles in your product (this skill's value is in role-based threat modeling)

## System Prompt

```
You are a senior UX designer and security reviewer for a DoD collaboration platform.
Your role is to audit user flows for completeness, security, and consistency.

When reviewing flows, identify and report concise findings in these categories:

1. MISSING TASK FLOWS — Roles without flow coverage or missing role-specific paths
2. MISSING ERROR PATHS — Non-obvious error cases (skip standard network/loading errors)
3. SECURITY VULNERABILITIES — Bypass vectors, information leakage, privilege escalation
4. NAVIGATION DEVIATIONS — Inconsistencies with established Mattermost UI patterns
5. MOBILE GAPS — Mobile-specific scenarios not addressed

OUTPUT FORMAT: Concise findings list.
[Finding Type] | [Affected Flow(s)] | [Description] | [Severity: P1/P2/P3] | [Recommendation]

Focus on gaps that would surprise an experienced developer or create security risk.
Don't trace every step — describe the gap and its impact.

Severity: use the single P1/P2/P3 scale defined in `conventions.md` §1 (do not invent
Critical/High/Medium/Low or P0–P4). In flow-audit terms:
- P1: Blocks the gate (security risk, missing core flow, DoD-control / compliance violation)
- P2: Should be resolved before spec writing (usability, role coverage gap)
- P3: Track; defer to a later phase (mobile edge case, minor inconsistency)

Do not be polite about gaps. A missing flow here becomes a scope creep or security incident in spec writing.
```

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "flows_description": {
      "type": "string",
      "description": "Complete description or transcription of user flow diagrams. Include flow names, step sequences, decision points, and actors involved. Can include Figma link descriptions, Miro board exports, or narrative descriptions.",
      "example": "Flow: 'User Adds Team Member' - Admin selects Users menu → clicks 'Invite' → enters email → selects role (Admin/User/Guest) → clicks 'Send' → email sent confirmation → (alt path) Invalid email → error message. No flows defined yet for Guest role attempting to add members or for retry scenarios."
    },
    "user_roles": {
      "type": "array",
      "items": {"type": "string"},
      "description": "Complete list of distinct user roles in the system as defined in the PRD",
      "example": ["Admin", "Team Lead", "Standard User", "Guest", "Viewer", "Moderator"]
    },
    "prd_requirements": {
      "type": "string",
      "description": "Relevant excerpts from the PRD describing feature requirements, user stories, and acceptance criteria. Include security requirements, compliance constraints, and role-based access control rules.",
      "example": "Feature: Team Permissions. Req 2.1: Only Team Admin can modify team membership. Req 2.2: Guest users cannot create channels. Req 2.3: All permission changes must be logged for audit. User Story: As an Admin, I want to manage channel access so that I can enforce security boundaries."
    },
    "existing_navigation_patterns": {
      "type": "string",
      "description": "Description of established Mattermost navigation patterns that new flows should follow or explicitly deviate from. Include modal vs. inline edit patterns, breadcrumb conventions, back/cancel button behavior, etc.",
      "example": "Pattern 1: Settings pages use left sidebar navigation with immediate save. Pattern 2: Deletions always use confirmation modal with warning text. Pattern 3: Multi-step wizards include progress indicator and ability to go back to previous step."
    }
  },
  "required": ["flows_description", "user_roles", "prd_requirements"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "audit_summary": {
      "type": "object",
      "properties": {
        "total_flows_reviewed": {"type": "integer"},
        "user_roles_covered": {"type": "array", "items": {"type": "string"}},
        "user_roles_missing_flows": {"type": "array", "items": {"type": "string"}},
        "critical_findings_count": {"type": "integer", "description": "Count of P1-severity findings only — not the total finding count."},
        "gate_recommendation": {
          "type": "string",
          "enum": ["APPROVE", "APPROVE_WITH_FINDINGS", "REJECT"],
          "description": "ADVISORY ONLY — a recommendation based on finding severity, not a gate decision. The orchestrator owns gate decisions per gate-checklists.md; this sub-skill never gates."
        }
      }
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "finding_type": {
            "type": "string",
            "enum": ["MISSING_TASK_FLOW", "MISSING_ERROR_PATH", "MISSING_COMPLIANCE_FLOW", "SECURITY_VULNERABILITY", "NAVIGATION_DEVIATION", "MOBILE_GAP"]
          },
          "affected_flows": {"type": "array", "items": {"type": "string"}},
          "description": {"type": "string"},
          "severity": {"type": "string", "enum": ["P1", "P2", "P3"]},
          "recommendation": {"type": "string"},
          "security_impact": {
            "type": "string",
            "description": "If security-related, describe the specific threat or vulnerability",
            "nullable": true
          }
        }
      }
    },
    "role_coverage_matrix": {
      "type": "object",
      "description": "For each defined user role, list flows where that role is the actor",
      "additionalProperties": {
        "type": "array",
        "items": {"type": "string"}
      }
    }
  }
}
```

## Usage Example

**Input:**
```json
{
  "flows_description": "Flow 1: User Invites Team Member - Any Admin user selects team → Users menu → Invite button → modal opens → enters email → selects from dropdown (Admin/User/Guest) → clicks Send → email validation happens → if invalid shows error in modal → if valid shows confirmation and email is sent. Only one flow documented. No flows for what happens when Guest role tries this flow or when same email is invited twice.",
  "user_roles": ["Team Admin", "Team User", "Team Guest", "Workspace Admin"],
  "prd_requirements": "Req 1.1: Only Team Admin and Workspace Admin can invite users. Req 1.2: Inviting a user already in the team must show error. Req 1.3: All invitations logged for compliance audit. Req 1.4: Guest users should see 'Contact Admin' message instead of invite UI. User Story: As a Workspace Admin, I need to bulk invite users in one operation to support onboarding."
}
```

**Output:**
```json
{
  "audit_summary": {
    "total_flows_reviewed": 1,
    "user_roles_covered": ["Team Admin"],
    "user_roles_missing_flows": ["Team User", "Team Guest", "Workspace Admin"],
    "critical_findings_count": 4,
    "gate_recommendation": "REJECT"
  },
  "findings": [
    {
      "finding_type": "MISSING_TASK_FLOW",
      "affected_flows": ["Invite User"],
      "description": "Workspace Admin role not explicitly shown in flow. PRD Req 1.1 states both Team Admin AND Workspace Admin can invite. Need separate flow or explicit role branching.",
      "severity": "P1",
      "recommendation": "Add branch in 'User Invites' flow showing whether system is Team Admin or Workspace Admin context, with appropriate permission check."
    },
    {
      "finding_type": "MISSING_ERROR_PATH",
      "affected_flows": ["Invite User"],
      "description": "PRD Req 1.2 requires handling duplicate invites (same email invited twice), but flow shows no decision point or error path for this case.",
      "severity": "P1",
      "recommendation": "Add validation step after email entry that checks 'Email already invited to this team?' If yes, show specific error message and prevent send."
    },
    {
      "finding_type": "MISSING_COMPLIANCE_FLOW",
      "affected_flows": ["Invite User"],
      "description": "PRD Req 1.3 requires all invitations to be logged for compliance audit, but no flow shows an audit-log entry being written, or any confirmation that the invite action was recorded. This is a DoD compliance requirement (see 'Audit trails' in Notes for DoD/Defense Context) and cannot be silently omitted from the flow.",
      "severity": "P1",
      "recommendation": "Add an explicit step after 'email is sent' showing the system writing an audit-log entry (who invited whom, what role, when)."
    },
    {
      "finding_type": "MISSING_TASK_FLOW",
      "affected_flows": ["Invite User"],
      "description": "PRD Req 1.4 requires Guest users see 'Contact Admin' message instead of invite UI, but no flow shows Guest role attempting this action or the alternate UX path.",
      "severity": "P1",
      "recommendation": "Create separate flow: Guest selects Users menu → sees 'Contact your team admin to request member access' message → optional button to send request. Route this before Invite modal."
    },
    {
      "finding_type": "MISSING_TASK_FLOW",
      "affected_flows": ["Invite User"],
      "description": "PRD mentions 'bulk invite' user story but only single-email flow exists. No flow documented for inviting multiple users in one operation.",
      "severity": "P2",
      "recommendation": "Design flow for bulk invite: textarea with email list or CSV upload → validate emails → show summary → confirm → send all → show results per email (success/duplicate/invalid)."
    }
  ],
  "role_coverage_matrix": {
    "Team Admin": ["Invite User"],
    "Team User": [],
    "Team Guest": [],
    "Workspace Admin": []
  }
}
```

### Compass Pattern Flow Validation

Validate flows against Compass pattern relationships:
- Standard transitions: sidebar click → page navigation, button click → modal/popover, message action → RHS panel
- Console transitions: sidebar nav item → content area swap, Save → success toast, Cancel → discard confirmation modal
- Expected overlay hierarchy: Popover < Modal < Tour Point < Toast (elevation ordering)
- Back navigation: Console detail pages use Back Button, not browser back

Reference: Compass Patterns relationship map in `<your-DS-patterns-file-key>` (Agent Quick Reference, Section 2)
Console patterns: `<your-DS-console-file-key>` (Agent Quick Reference, Section 5)

## Validation Rules

1. **Completeness**: Every user role listed in `user_roles` MUST appear as an actor in at least one flow, OR have explicit justification for absence (e.g., "Viewer role has no flows by design")

2. **Security Rigor**: For any flow handling sensitive data (permissions, authentication, audit), every decision point must have both success and failure paths documented

3. **Consistency**: If multiple flows exist for related tasks, they must follow the same navigation pattern (e.g., all use modals or all use inline edit, not mixed)

4. **Mobile Coverage**: Flows with steps requiring text entry or dropdown selection must explicitly address mobile input method

5. **Traceability**: Every PRD requirement mentioned in `prd_requirements` must map to at least one flow, or be flagged as a gap

6. **Clarity**: Flow descriptions must use action verbs and define decision criteria precisely (not "check if valid" but "validate email format matches RFC 5322")

## Related Skills

- **Section Writer**: Uses approved flows as input to write detailed "User Flows" or "Task Flows" section of the spec
- **Edge Case Hunter**: Takes completed spec and finds security/state gaps the flows didn't anticipate
- **Traceability Checker**: Maps PRD requirements to spec sections; can accept this skill's output to track which flows cover which requirements
- **Feedback Synthesizer**: If review feedback identifies flow issues, synthesizer categorizes into MUST-FIX vs. NICE-TO-HAVE

## Notes for DoD/Defense Context

This skill applies heightened scrutiny to:
- **Bypass vectors**: Flows that could allow users to access classified/restricted information
- **Information leakage**: Flows that reveal existence of resources to unauthorized users (even if access is denied)
- **Audit trails**: Flows must explicitly show permission change logging for compliance
- **Session/authentication**: Flows for re-auth, timeout, and session termination in high-security contexts
- **Role elevation**: Any flow involving role changes or temporary permission grants must show explicit approval and logging

---

**Last Updated**: 2026-03-10
**Maintainer**: Mattermost Design Team