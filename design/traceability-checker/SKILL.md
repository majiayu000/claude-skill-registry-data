---
name: Traceability Checker
description: Generates PRD-to-spec traceability matrix, identifying requirements gaps and scope creep
version: 1.0.0
author: Mattermost Design Team
tags: [ux-spec, requirements-traceability, qa, scope-management, compliance-tracking]
allowed-tools: Read, Grep, Glob
---

# Traceability Checker

An internal validation skill that compares a completed UX specification against the PRD to verify requirement coverage. Identifies gaps, partial coverage, and scope creep. Output is an internal QA artifact — findings are folded into the spec as open questions or addressed in the spec text, not published as a separate appendix unless explicitly requested.

## When to Use

- **Internal validation** during Phase 7 to verify spec coverage of PRD requirements
- **Scope creep detection** to identify if spec is adding features not in the PRD
- **Change impact analysis** when PRD has been revised; identify what spec sections need updating
- **Gap identification** to surface requirements that need to be addressed before spec approval

## When NOT to Use

- For validating design decisions (use a design review skill, not requirements tracing)
- For evaluating PRD quality itself (this skill assumes PRD is the source of truth)
- For writing or editing the spec (use Section Writer for that)
- When PRD and spec have not been finalized yet (too much churn)
- For non-spec deliverables (this skill specifically compares spec to PRD)
- When there is no PRD (you need a requirements document as input)

## System Prompt

```
You are a QA architect performing a requirements traceability review.
Your job is to create a comprehensive traceability matrix that maps every requirement in the PRD
to the corresponding section(s) in the UX spec.

PROCESS:

1. PARSE PRD REQUIREMENTS
   - Extract every requirement, user story, acceptance criterion, and constraint from the PRD
   - Assign each a unique ID (e.g., REQ-1.1, REQ-2.3, USER-STORY-1, AC-3.2)
   - Understand the requirement: what behavior or capability must the system have?
   - Note if requirement is functional, security, compliance, performance, or accessibility

2. PARSE SPEC CONTENT
   - Identify every feature, behavior, interaction, and constraint documented in the spec
   - Note which spec section addresses which behavior
   - Understand what the spec claims to implement

3. MATCH REQUIREMENTS TO SPEC SECTIONS
   - For each PRD requirement, find the corresponding spec section(s) that address it
   - Match is successful if: spec explicitly documents the required behavior, user can accomplish the requirement using spec-described UI
   - Match is partial if: spec documents some but not all of the requirement, or requirement is only partially addressable via UI
   - Match is missing (gap) if: PRD requirement is not documented anywhere in the spec

4. IDENTIFY SCOPE CREEP
   - Find spec sections that are not tied to any PRD requirement
   - Assess if this is intentional (e.g., "nice to have" approved during design), or unintended scope expansion
   - Scope creep is only a finding if it conflicts with scope statement or adds significant effort

5. IDENTIFY USER STORY FULFILLMENT
   - For each PRD user story (As a [role], I want [capability], so that [value]),
     verify that the spec UI actually allows that user to accomplish the goal
   - Example: User story "As an Admin, I want to export data in CSV format so I can analyze offline"
     — does spec show how admin initiates export, what file is created, where file appears?

6. CREATE TRACEABILITY MATRIX
   - Row: One PRD requirement
   - Columns: Requirement ID, Requirement Text, Spec Section(s) that address it, Coverage Status
   - Coverage status: COVERED / PARTIAL / GAP / DEFERRED / OUT_OF_SCOPE

7. SUMMARIZE GAPS
   - For each GAP requirement: is it critical (blocks user story) or minor (nice to have)?
   - For each PARTIAL requirement: what part of the requirement is covered?
   - Note any DEFERRED requirements (intentionally out of this phase) with reason
   - Note any OUT_OF_SCOPE requirements with scope statement reference

8. SCOPE CREEP SUMMARY
   - List any spec sections that don't map to PRD requirements
   - For each, note if it's accepted scope expansion or unintended creep

OUTPUT FORMAT:

Traceability Matrix (table format):
[PRD Req ID] | [Requirement Text (brief)] | [Spec Section(s)] | [Status] | [Notes]

Summary of Gaps (narrative):
- List critical gaps (must be fixed)
- List minor gaps (should be fixed)
- List deferred items and reason

Summary of Scope Creep (narrative):
- List any spec sections not in PRD with assessment

SEVERITY OF GAPS (a coverage-gap taxonomy; maps onto the single P1/P2/P3 finding scale in
`conventions.md` §1 — CRITICAL GAP → P1, MAJOR GAP → P2, MINOR GAP → P3):

- CRITICAL GAP (P1): Requirement is core to the feature, a user story cannot be completed without it, or the requirement is compliance/security critical (e.g., audit logging, access enforcement)
- MAJOR GAP (P2): Requirement is important but could be deferred or worked around
- MINOR GAP (P3): Requirement is nice-to-have or an edge case

Be thorough. Missing requirements at this stage become scope disputes in implementation.
Never assume a requirement is covered if it's not explicitly stated in the spec.
Partial coverage is still a gap — note what part is covered and what part is missing.
```

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "prd": {
      "type": "string",
      "description": "Complete or summary text of the Product Requirements Document. Include all requirements, user stories, acceptance criteria, constraints, and scope boundaries. Can be document excerpts if PRD is very long.",
      "example": "# Product Requirements Document: Channel Membership Policies (ABAC)\n\n## Scope\nThis feature lets System Admins author attribute-based rules that govern channel membership on the IL5 platform.\n\n## Requirements\nREQ-1.1: System Admins can author attribute-based membership rules in System Console\nREQ-1.2: System prevents two policies from claiming the same channel\nREQ-1.3: Channel Admins can view (read-only) the policy applied to their channel\nREQ-1.4: All policy create/edit/apply/revoke actions are logged for audit (NIST 800-53 AU-2)\nREQ-2.1: Security Architects can override a policy on a per-channel basis with recorded justification\nREQ-2.2: A user who no longer matches a policy is flagged for review, not auto-removed\nREQ-3.1: The policy editor surfaces the count of currently-matching members\n\n## User Stories\nUS-1: As a System Admin, I want to author attribute-based membership rules so I can enforce Need-to-Know at scale\nUS-2: As a Channel Admin, I want to see which policy applies to my channel so I understand who can join\nUS-3: As a Security Architect, I want to override a policy on one channel with justification so I can handle exceptions without disabling the policy\n\n## Out of Scope\n- Bulk attribute import (CSV / API batch)\n- External ICAM directory sync\n- Scheduled / time-boxed policies"
    },
    "spec_draft": {
      "type": "string",
      "description": "Complete UX specification document being reviewed. Include all sections, headings, content, and appendices. This is compared against the PRD.",
      "example": "# UX Specification: Channel Membership Policies (ABAC)\n\n## 1. Overview\nSystem Admins author attribute-based rules that govern channel membership.\n\n## 2. Policy Authoring Workflow\n[Detailed description of the System Console policy editor]\n\n## 3. Channel-Admin View\n[Read-only view of the applied policy]\n\n## 4. Access Control\nOnly System Admins can author policies. [Note: Security Architect override not documented yet]\n\n## 5. Conflict Prevention\nSystem prevents two policies from claiming the same channel.\n\n## 6. Mobile Behavior\nIdentical to web.\n\n## 7. Error Handling\n[Error cases documented]"
    }
  },
  "required": ["prd", "spec_draft"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "traceability_matrix": {
      "type": "array",
      "description": "Complete traceability matrix mapping each PRD requirement to spec coverage",
      "items": {
        "type": "object",
        "properties": {
          "requirement_id": {
            "type": "string",
            "example": "REQ-1.1"
          },
          "requirement_text": {
            "type": "string",
            "description": "Brief statement of the requirement",
            "example": "System Admins can author attribute-based membership rules"
          },
          "requirement_type": {
            "type": "string",
            "enum": ["FUNCTIONAL", "SECURITY", "COMPLIANCE", "PERFORMANCE", "ACCESSIBILITY", "CONSTRAINT"]
          },
          "spec_sections": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Spec sections that address this requirement",
            "example": ["Section 2: Policy Authoring Workflow", "Section 4: Access Control"]
          },
          "coverage_status": {
            "type": "string",
            "enum": ["COVERED", "PARTIAL", "GAP", "DEFERRED", "OUT_OF_SCOPE"]
          },
          "coverage_percentage": {
            "type": "integer",
            "description": "Percentage of requirement covered by spec (0-100). 100 = full coverage, 0-99 = partial/gap",
            "example": 75
          },
          "notes": {
            "type": "string",
            "description": "Additional context, partial coverage details, or deferral reason",
            "example": "Spec covers policy authoring but does not document the Security Architect override (REQ-2.1)"
          },
          "severity_if_gap": {
            "type": "string",
            "enum": ["CRITICAL", "MAJOR", "MINOR"],
            "nullable": true,
            "description": "If gap, how severe is it?"
          }
        }
      }
    },
    "summary": {
      "type": "object",
      "properties": {
        "total_requirements": {"type": "integer"},
        "covered_count": {"type": "integer"},
        "partial_count": {"type": "integer"},
        "gap_count": {"type": "integer"},
        "deferred_count": {"type": "integer"},
        "out_of_scope_count": {"type": "integer"},
        "coverage_percentage": {
          "type": "number",
          "description": "Overall percentage of PRD requirements covered by spec"
        }
      }
    },
    "critical_gaps": {
      "type": "array",
      "description": "List of critical gaps that must be resolved before spec approval",
      "items": {
        "type": "object",
        "properties": {
          "requirement_id": {"type": "string"},
          "requirement_text": {"type": "string"},
          "gap_description": {"type": "string"},
          "user_story_impact": {"type": "string", "description": "Which user story is blocked by this gap?"},
          "recommendation": {"type": "string"}
        }
      }
    },
    "major_gaps": {
      "type": "array",
      "description": "List of major gaps that should be resolved before implementation",
      "items": {
        "type": "object",
        "properties": {
          "requirement_id": {"type": "string"},
          "requirement_text": {"type": "string"},
          "gap_description": {"type": "string"},
          "recommendation": {"type": "string"}
        }
      }
    },
    "scope_creep_findings": {
      "type": "array",
      "description": "Spec sections that don't map to PRD requirements",
      "items": {
        "type": "object",
        "properties": {
          "spec_section": {"type": "string"},
          "description": {"type": "string"},
          "assessment": {
            "type": "string",
            "enum": ["APPROVED_EXPANSION", "UNINTENDED_CREEP", "TBD"],
            "description": "Is this scope expansion intentional or unintended?"
          },
          "notes": {"type": "string"}
        }
      }
    },
    "user_story_fulfillment": {
      "type": "array",
      "description": "Assessment of whether each user story is fulfillable given the spec",
      "items": {
        "type": "object",
        "properties": {
          "user_story_id": {"type": "string"},
          "user_story_text": {"type": "string"},
          "fulfillable": {"type": "boolean"},
          "steps_to_accomplish_goal": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Can user accomplish story goal using spec-described UI?"
          },
          "missing_spec_details": {
            "type": "array",
            "items": {"type": "string"},
            "nullable": true,
            "description": "If not fully fulfillable, what spec details are missing?"
          }
        }
      }
    },
    "deferred_requirements": {
      "type": "array",
      "description": "Requirements intentionally deferred to future phases",
      "items": {
        "type": "object",
        "properties": {
          "requirement_id": {"type": "string"},
          "requirement_text": {"type": "string"},
          "deferral_reason": {"type": "string"},
          "planned_phase": {"type": "string", "description": "When will this be addressed?", "nullable": true}
        }
      }
    },
    "gate_recommendation": {
      "type": "object",
      "properties": {
        "decision": {
          "type": "string",
          "enum": ["APPROVE", "APPROVE_WITH_DEFERRED_ITEMS", "REJECT"],
          "description": "ADVISORY ONLY — a recommendation, not a gate decision. The orchestrator owns gate outcomes per gate-checklists.md; this internal-validation skill never gates."
        },
        "rationale": {"type": "string"},
        "blockers_to_resolve": {
          "type": "array",
          "items": {"type": "string"},
          "description": "If REJECT, list critical items that must be resolved"
        }
      }
    }
  }
}
```

## Usage Example

**Input:**
```json
{
  "prd": "# Channel Membership Policies (ABAC) PRD\n\n## Requirements\nREQ-1.1: System Admins can author attribute-based membership rules in System Console\nREQ-1.2: System prevents two policies from claiming the same channel\nREQ-1.3: Channel Admins can view (read-only) the policy applied to their channel\nREQ-1.4: All policy create/edit/apply/revoke actions are logged for audit (NIST 800-53 AU-2)\nREQ-2.1: Security Architects can override a policy on a per-channel basis with recorded justification\nREQ-2.2: A user who no longer matches a policy is flagged for review, not auto-removed\nREQ-3.1: The policy editor surfaces the count of currently-matching members\nREQ-3.2: Applying a policy grants matching users access immediately\n\n## User Stories\nUS-1: As a System Admin, I want to author attribute-based membership rules so I can enforce Need-to-Know at scale\nUS-2: As a Channel Admin, I want to see which policy applies to my channel so I understand who can join\nUS-3: As a Security Architect, I want to override a policy on one channel with justification\n\n## Out of Scope\n- Bulk attribute import (CSV / API batch)\n- External ICAM directory sync",
  "spec_draft": "# Channel Membership Policies (ABAC) Spec\n\n## 1. Overview\nSystem Admins author attribute-based rules that govern channel membership.\n\n## 2. Policy Authoring Interface\nAdmin opens the policy editor → defines attribute rules → assigns channels → clicks Apply. System validates the rule set. If valid, the policy applies. If invalid, shows an error.\n\n## 3. Conflict Prevention\nIf a channel is already claimed by another policy, the system shows a 'Channel already governed' error.\n\n## 4. Channel-Admin View\nChannel Admins see a read-only panel naming the policy applied to their channel and its match criteria.\n\n## 5. Mobile Behavior\nBehavior identical to web.\n\n## 6. Match Behavior\nWhen a policy is applied, matching users gain access. [Note: no behavior documented for a user who later stops matching the policy]"
}
```

**Output:**
```json
{
  "traceability_matrix": [
    {
      "requirement_id": "REQ-1.1",
      "requirement_text": "System Admins can author attribute-based membership rules",
      "requirement_type": "FUNCTIONAL",
      "spec_sections": ["Section 2: Policy Authoring Interface"],
      "coverage_status": "COVERED",
      "coverage_percentage": 100,
      "notes": "Spec documents the complete policy-authoring flow"
    },
    {
      "requirement_id": "REQ-1.2",
      "requirement_text": "System prevents two policies from claiming the same channel",
      "requirement_type": "FUNCTIONAL",
      "spec_sections": ["Section 3: Conflict Prevention"],
      "coverage_status": "COVERED",
      "coverage_percentage": 100,
      "notes": "Spec explicitly documents conflict prevention with an error message"
    },
    {
      "requirement_id": "REQ-1.3",
      "requirement_text": "Channel Admins can view (read-only) the policy applied to their channel",
      "requirement_type": "FUNCTIONAL",
      "spec_sections": ["Section 4: Channel-Admin View"],
      "coverage_status": "COVERED",
      "coverage_percentage": 100,
      "notes": "Spec documents the read-only policy panel"
    },
    {
      "requirement_id": "REQ-1.4",
      "requirement_text": "All policy create/edit/apply/revoke actions are logged for audit (NIST 800-53 AU-2)",
      "requirement_type": "COMPLIANCE",
      "spec_sections": [],
      "coverage_status": "GAP",
      "coverage_percentage": 0,
      "notes": "Spec does not document audit logging at all. This is a compliance requirement (NIST 800-53 AU-2) that must be documented.",
      "severity_if_gap": "CRITICAL"
    },
    {
      "requirement_id": "REQ-2.1",
      "requirement_text": "Security Architects can override a policy on a per-channel basis with recorded justification",
      "requirement_type": "FUNCTIONAL",
      "spec_sections": [],
      "coverage_status": "GAP",
      "coverage_percentage": 0,
      "notes": "Spec only documents the System Admin authoring flow. No Security Architect override is documented.",
      "severity_if_gap": "CRITICAL"
    },
    {
      "requirement_id": "REQ-2.2",
      "requirement_text": "A user who no longer matches a policy is flagged for review, not auto-removed",
      "requirement_type": "FUNCTIONAL",
      "spec_sections": ["Section 6: Match Behavior"],
      "coverage_status": "PARTIAL",
      "coverage_percentage": 50,
      "notes": "Spec covers initial match-and-grant but does not document the stop-matching path (flag-for-review vs. auto-remove).",
      "severity_if_gap": "MAJOR"
    },
    {
      "requirement_id": "REQ-3.1",
      "requirement_text": "The policy editor surfaces the count of currently-matching members",
      "requirement_type": "FUNCTIONAL",
      "spec_sections": [],
      "coverage_status": "GAP",
      "coverage_percentage": 0,
      "notes": "Spec does not document the matching-member count in the editor.",
      "severity_if_gap": "CRITICAL"
    },
    {
      "requirement_id": "REQ-3.2",
      "requirement_text": "Applying a policy grants matching users access immediately",
      "requirement_type": "FUNCTIONAL",
      "spec_sections": ["Section 6: Match Behavior"],
      "coverage_status": "COVERED",
      "coverage_percentage": 100,
      "notes": "Spec states 'matching users gain access' on apply"
    }
  ],
  "summary": {
    "total_requirements": 8,
    "covered_count": 3,
    "partial_count": 1,
    "gap_count": 4,
    "deferred_count": 0,
    "out_of_scope_count": 0,
    "coverage_percentage": 50
  },
  "critical_gaps": [
    {
      "requirement_id": "REQ-1.4",
      "requirement_text": "All policy actions are logged for audit (NIST 800-53 AU-2)",
      "gap_description": "Spec does not document audit logging. This is a compliance requirement that is completely missing from the spec.",
      "user_story_impact": "Affects all user stories — audit logging is required for IL5 deployment per NIST 800-53 AU-2",
      "recommendation": "Add a section documenting: what events are logged (policy create, edit, apply, revoke), what data is captured (timestamp, actor, subject, attributes changed), where logs are stored, and how they are accessed for audit."
    },
    {
      "requirement_id": "REQ-2.1",
      "requirement_text": "Security Architects can override a policy on a per-channel basis with recorded justification",
      "gap_description": "Spec only documents the System Admin authoring flow. The Security Architect override is completely absent.",
      "user_story_impact": "US-3 'As a Security Architect, I want to override a policy on one channel with justification' cannot be fulfilled",
      "recommendation": "Add a flow for the Security Architect to open a channel's applied policy, set a per-channel override, and record a justification. Specify how the Security Architect role is verified."
    },
    {
      "requirement_id": "REQ-3.1",
      "requirement_text": "The policy editor surfaces the count of currently-matching members",
      "gap_description": "Spec does not document the matching-member count in the editor. Admins cannot see the blast radius of a policy before applying it.",
      "user_story_impact": "Affects US-1 — the admin cannot gauge who a rule set will match before applying",
      "recommendation": "Add behavior: 'As the admin edits the rule set, the editor shows a live count of currently-matching members and a link to preview the matched roster.'"
    }
  ],
  "major_gaps": [
    {
      "requirement_id": "REQ-2.2",
      "requirement_text": "A user who no longer matches a policy is flagged for review, not auto-removed",
      "gap_description": "Spec documents the initial match-and-grant but does not document the stop-matching path. It is unclear whether a user who stops matching is auto-removed or flagged for review.",
      "recommendation": "Clarify: 'When a member stops matching the policy (e.g., a revoked attribute), they are NOT auto-removed. They are flagged for review in the policy editor, and a Channel Admin or Security Architect decides whether to remove them.'"
    }
  ],
  "scope_creep_findings": [
    {
      "spec_section": "Section 5: Mobile Behavior",
      "description": "Mobile section documents mobile-specific interaction details that go beyond PRD scope",
      "assessment": "APPROVED_EXPANSION",
      "notes": "Mobile behavior is appropriate expansion — not scope creep"
    }
  ],
  "user_story_fulfillment": [
    {
      "user_story_id": "US-1",
      "user_story_text": "As a System Admin, I want to author attribute-based membership rules so I can enforce Need-to-Know at scale",
      "fulfillable": true,
      "steps_to_accomplish_goal": [
        "System Admin opens the policy editor",
        "Admin defines attribute rules",
        "Admin assigns channels",
        "Admin clicks 'Apply'",
        "System applies the policy"
      ],
      "missing_spec_details": null
    },
    {
      "user_story_id": "US-2",
      "user_story_text": "As a Channel Admin, I want to see which policy applies to my channel so I understand who can join",
      "fulfillable": true,
      "steps_to_accomplish_goal": [
        "Channel Admin opens the channel's policy panel",
        "Admin reads the policy name and match criteria"
      ],
      "missing_spec_details": [
        "What the panel shows when no policy applies to the channel"
      ]
    },
    {
      "user_story_id": "US-3",
      "user_story_text": "As a Security Architect, I want to override a policy on one channel with justification",
      "fulfillable": false,
      "steps_to_accomplish_goal": [],
      "missing_spec_details": [
        "Spec does not document the Security Architect override flow at all",
        "No interface documented for setting a per-channel override or recording justification"
      ]
    }
  ],
  "deferred_requirements": [],
  "gate_recommendation": {
    "decision": "REJECT",
    "rationale": "Spec has critical gaps in compliance (NIST 800-53 AU-2 audit logging), role coverage (Security Architect override), and core functionality (matching-member count). These are fundamental PRD requirements that must be addressed before the spec is approved and handed to engineering. ADVISORY — the orchestrator owns the gate decision per gate-checklists.md.",
    "blockers_to_resolve": [
      "REQ-1.4: Add audit logging behavior (NIST 800-53 AU-2)",
      "REQ-2.1: Add Security Architect per-channel override flow",
      "REQ-3.1: Add matching-member count in the policy editor",
      "REQ-2.2: Clarify the stop-matching path (flag-for-review vs. auto-remove)"
    ]
  }
}
```

## Validation Rules

1. **Every PRD item covered**: Every requirement, user story, and acceptance criterion in the PRD must appear in the traceability matrix (even if marked as OUT_OF_SCOPE)

2. **Coverage percentage justified**: If coverage is marked as PARTIAL, the percentage must be explained in notes (e.g., "75% — spec covers happy path but not error path")

3. **User story completion**: For each user story, the output must explicitly state whether a user can accomplish the story goal using the spec's described UI. Not "spec mentions X" but "user can do Y by following steps Z"

4. **Gap severity justified**: Every GAP finding must have a severity (CRITICAL/MAJOR/MINOR) with rationale explaining why

5. **Scope creep assessment**: Any spec section not in PRD must be assessed as APPROVED_EXPANSION, UNINTENDED_CREEP, or TBD (not left ambiguous)

6. **Gate decision justified**: The final recommendation (APPROVE/REJECT) must be clearly justified based on gaps found

## Related Skills

- **Section Writer**: Writes spec sections that this skill will audit for PRD coverage
- **Edge Case Hunter**: Finds contradictions and gaps within the spec itself; this skill finds gaps between PRD and spec
- **Flow Auditor**: Audits flows against PRD; output flows should map to requirements this skill validates
- **Feedback Synthesizer**: If review feedback identifies missing requirements, synthesizer categorizes the feedback

## Notes for DoD/Defense Context

This skill applies heightened scrutiny to:
- **Compliance requirements**: Security, audit logging, access control, and regulatory requirements must be explicitly traced to spec sections
- **Role-based requirements**: Every role mentioned in PRD must have corresponding flows and behaviors documented in spec
- **Permission model**: Access control requirements must map to authentication/authorization sections in spec
- **Audit trail**: Compliance requirements for audit logging must be explicitly documented (not assumed to be implementation detail)
- **Information barriers**: Requirements preventing information leakage must map to specific spec sections describing access checks

---

**Last Updated**: 2026-03-10
**Maintainer**: Mattermost Design Team