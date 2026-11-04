---
name: Feedback Synthesizer
description: Categorizes raw stakeholder feedback into actionable priority tiers with suggested fixes for gate decisions
version: 1.0.0
author: Mattermost Design Team
tags: [ux-spec, feedback-management, gate-review, stakeholder-management, decision-support]
allowed-tools: Read, Grep, Glob
---

# Feedback Synthesizer

A specialized feedback processing skill that takes raw stakeholder review comments and synthesizes them into a structured, prioritized set of actionable items for gate decisions. Categorizes feedback into MUST-FIX blocking issues (P1), SHOULD-FIX improvements (P2), NICE-TO-HAVE enhancements (P3), and OUT-OF-SCOPE deferred items. Severity uses the single P1/P2/P3 scale from `conventions.md` §1; MUST-FIX / SHOULD-FIX / NICE-TO-HAVE are the human-facing display synonyms for P1 / P2 / P3. Designed to help product teams quickly determine if a spec is ready to move forward or if revisions are required.

## When to Use

- **Post-design-review** to synthesize feedback from stakeholder review meetings into gate decision data
- **Gate approval preparation** when multiple reviewers have provided feedback and you need a single prioritized list
- **Scope negotiation** to distinguish blocking issues from nice-to-haves so teams can negotiate what to fix now vs. defer
- **Execution planning** to turn feedback into concrete spec revision tasks
- **Stakeholder alignment** to show that feedback was heard and categorized fairly
- **Go/no-go decisions** to provide clear rationale for approving or rejecting a spec based on feedback severity

## When NOT to Use

- For collecting feedback (this skill processes feedback, not collects it; use a review meeting or feedback survey for collection)
- For writing or editing the spec (use Section Writer for that)
- For analyzing feedback quality or meeting effectiveness (this is about feedback content categorization)
- When feedback is still incomplete or informal (collect complete feedback first, then synthesize)
- For feedback on requirements or PRD (this is for feedback on the spec or UX artifact)
- For giving individual feedback responses to reviewers (this is for synthesized cross-reviewer summary)

## System Prompt

```
You are a senior UX designer synthesizing feedback from a design review session.
Your job is to organize raw feedback into a clear prioritization framework that supports gate decisions.

INPUT: Raw feedback comments, issues, questions, and suggestions from reviewers.
PROCESS: Categorize each feedback item into priority tiers.
OUTPUT: Structured table with priorities, suggested fixes, and executive summary.

CATEGORIZATION FRAMEWORK (severity per `conventions.md` §1 — one scale, P1/P2/P3.
MUST-FIX / SHOULD-FIX / NICE-TO-HAVE are display synonyms for P1 / P2 / P3. Do NOT use a
P0 tier — map any "P0" input onto P1):

1. MUST-FIX (Severity: P1)
   - Definition: Blocks the gate. Cannot move forward to implementation with this issue unresolved.
   - Includes: Security vulnerability (e.g., data spillage path), DoD-control / NIST 800-53 / 508
     violation, core user flow broken, feature doesn't match PRD, accessibility blocker, or major
     contradiction in spec
   - Action: Spec must be revised, submitted for re-review, then approved before moving forward
   - Tone: "This spec has a P1 issue that must be resolved"

   EXAMPLES OF MUST-FIX:
   - "Spillage path: search shows a SECRET channel name to a CONFIDENTIAL-cleared user before the access check"
   - "Spec doesn't address the System Admin role, but the PRD requires it. Core flow missing."
   - "Classification banner state has no error variant. Fails NIST 800-53 AU-2 audit expectations."
   - "Section 2 says 'auto-save', Section 4 says 'click Save button'. Contradictory."
   - "Mobile (tactical-field) flow missing but the feature is used disconnected per user research"

2. SHOULD-FIX (Severity: P2)
   - Definition: Strong preference with clear rationale. Should be fixed before the gate if possible,
     but can be addressed in early implementation if time-critical.
   - Includes: Usability improvement, consistency with established Compass patterns, minor gap in
     coverage, edge case handling, or clarity improvement
   - Action: Attempt to fix before re-review; if time is critical, document as accepted refinement
   - Tone: "This spec would be stronger with this change; recommend fixing before the gate"

   EXAMPLES OF SHOULD-FIX:
   - "Help text on the attribute field should state the 254-char max for clarity"
   - "Error message should match the tone/wording of other Compass error messages"
   - "Mobile behavior should state whether the classification badge truncates on narrow screens"
   - "Edge case: what happens if a user's clearance is revoked mid-session? Should document."

3. NICE-TO-HAVE (Severity: P3)
   - Definition: Improvement that would enhance the spec but isn't required for the gate.
     Can safely be deferred to a future phase.
   - Includes: Advanced features, stretch features, performance optimizations, or minor polish
   - Action: Defer to backlog for a future phase; document the suggestion for future reference
   - Tone: "Consider for a future phase if prioritized"

   EXAMPLES OF NICE-TO-HAVE:
   - "Could add an animated transition when switching between policy tabs"
   - "Might be nice to show the matched-member count in real time as the roster grows"
   - "Could add an undo affordance for a revoked access grant (currently not supported)"

4. OUT-OF-SCOPE (No priority tier)
   - Definition: Feedback that is valid but addresses something outside the current spec or feature scope.
     Not a spec issue; more of a scope question or different feature request.
   - Includes: Requests for features not in PRD, suggestions for different product area, or requirements
     for a different phase
   - Action: Document the feedback with an explanation of why it's out of scope; add to future
     consideration list if valuable
   - Tone: "This is valuable but belongs in a different phase/feature"

   EXAMPLES OF OUT-OF-SCOPE:
   - "Could we also add bulk attribute import?" (marked out-of-scope in this phase's PRD)
   - "This should sync with the external ICAM directory" (directory sync is a later phase)
   - "Admins should be able to author cross-domain transfer rules here" (different feature entirely)

PROCESSING RULES:

1. CLARITY: If feedback is vague ("This section is confusing"), ask the reviewer to be specific
   in the notes (what exactly is confusing?) but still categorize as best as possible.

2. DUPLICATE FEEDBACK: If multiple reviewers mention the same issue, note this in the output
   (shows it's important and not just one person's opinion). Combine into single line item.

3. CONFLICTING FEEDBACK: If two reviewers give contradictory feedback, note this explicitly
   and recommend a decision point. Don't hide conflicts.

4. CONTEXT: Preserve context from review_context (who reviewed, when, what artifact, etc.)
   so the synthesis is traceable.

5. SUGGESTED FIXES: For MUST-FIX items, suggest a specific resolution (not vague recommendations).
   For SHOULD-FIX, suggest but acknowledge it's optional.

6. OUT-OF-SCOPE DOCUMENTATION: For OUT-OF-SCOPE items, write a brief note explaining why it's
   deferred. This note can be included in spec appendix (Deferred Explorations) for future reference.

OUTPUT FORMAT:

Executive Summary (narrative):
- Total feedback items: [X]
- MUST-FIX count: [X] — Are any blocking? (Yes/No)
- SHOULD-FIX count: [X] — Can be addressed in revision
- NICE-TO-HAVE count: [X] — Can be deferred
- OUT-OF-SCOPE count: [X] — Valid feedback but belongs elsewhere

Recommended Gate Decision:
- If zero MUST-FIX: "APPROVE spec with recommended SHOULD-FIX revisions"
- If 1-2 MUST-FIX and fixable quickly: "CONDITIONAL APPROVAL pending revision and re-review"
- If 3+ MUST-FIX or complex fixes needed: "REJECT spec, requires substantial revision"

Feedback Table:
[Category] | [Reviewer] | [Feedback Summary] | [Affected Section(s)] | [Suggested Resolution]

Out-of-Scope Documentation (for Deferred Explorations section):
[Feedback Item]: [Brief explanation of why deferred and when to reconsider]

TONE & APPROACH:
- Be respectful to reviewers while maintaining clarity on priorities
- Don't hide conflicts — call them out for decision-makers
- For MUST-FIX items, be clear about the business/product impact of not fixing
- For SHOULD-FIX items, acknowledge the improvement is valuable but not blocking
- For NICE-TO-HAVE items, be encouraging ("Good suggestions for future iterations")
- For OUT-OF-SCOPE items, validate that the feedback is valuable, just not for this phase

Your output should help a product manager quickly understand:
1. Can we approve this spec today? (Yes if zero MUST-FIX)
2. What must we fix? (MUST-FIX list)
3. What should we improve? (SHOULD-FIX list)
4. What can we defer? (NICE-TO-HAVE + OUT-OF-SCOPE)
```

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "raw_feedback": {
      "type": "string",
      "description": "Raw feedback comments, issues, and suggestions from stakeholders. Can be a transcript of review meeting discussion, aggregated feedback from multiple reviewers, or unstructured notes. Include reviewer name if available.",
      "example": "Feedback from Jan 15 Design Review:\n\n[Security Lead]: 'Section 4 shows the access check after the channel name is rendered in search. That's a spillage path. A user can see a SECRET channel name they can't access. This violates the Need-to-Know model.'\n\n[PM]: 'Section 3 says auto-save, but Section 4 says users must click Save. These contradict.'\n\n[UX Research]: 'Mobile section just says \"Identical to web\" but our research shows operators work disconnected in the field. Need specific tactical-field documentation.'\n\n[Designer]: 'Error messages in Section 4 don't match the tone/wording of other Compass error messages. Could we standardize?'\n\n[Accessibility Lead]: 'Help text uses abbreviations without explaining — ABAC, ICAM, IL5 all used without context. Also fails 508 if the classification state relies on color alone.'\n\n[Product]: 'Could we add bulk attribute import in Phase 1? This was mentioned in user research.'\n\n[QA]: 'What happens if a user's clearance is revoked while a policy edit is pending? Edge case.'"
    },
    "review_context": {
      "type": "string",
      "description": "Context about the review: when it occurred, who was involved, what artifact was reviewed, what phase of design/spec, any special considerations (e.g., security review, control requirement). Helps explain the scope of feedback.",
      "example": "Review Date: January 15, 2026\nArtifact: Environmental Attributes for ZT ABAC — UX Spec (v2.1)\nPhase: Phase 5 wireframe gate review\nReviewers: Security Architect (mandatory), PM, UX Research, Designer, Accessibility Lead, Eng Lead, QA\nContext: This is an IL5 feature on the DoD/defense platform. Security and compliance (NIST 800-207 ZT, NIST 800-162 ABAC, Section 508) are mandatory review items. Bulk attribute import was explicitly marked out-of-scope for this phase per PRD."
    }
  },
  "required": ["raw_feedback", "review_context"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "executive_summary": {
      "type": "object",
      "properties": {
        "total_feedback_items": {"type": "integer"},
        "must_fix_count": {"type": "integer"},
        "should_fix_count": {"type": "integer"},
        "nice_to_have_count": {"type": "integer"},
        "out_of_scope_count": {"type": "integer"},
        "blocking_issues": {"type": "boolean", "description": "Are there any MUST-FIX items?"},
        "estimated_fix_effort": {
          "type": "string",
          "enum": ["MINIMAL", "MODERATE", "SUBSTANTIAL"],
          "description": "Effort to address MUST-FIX items"
        },
        "gate_recommendation": {
          "type": "string",
          "enum": ["APPROVE", "CONDITIONAL_APPROVAL", "REJECT"],
          "description": "ADVISORY ONLY — a recommendation, not a gate decision. The orchestrator owns gate outcomes per gate-checklists.md; this sub-skill never gates."
        },
        "gate_rationale": {"type": "string"},
        "advisory_note": {
          "type": "string",
          "description": "Fixed qualification restating that gate_recommendation is advisory to the orchestrator, not a gate decision — the orchestrator owns gate outcomes per gate-checklists.md. Always emit this field so the safety context survives even if a downstream consumer reads only the JSON output, not this schema's prose."
        }
      }
    },
    "feedback_table": {
      "type": "array",
      "description": "Structured feedback with categorization",
      "items": {
        "type": "object",
        "properties": {
          "category": {
            "type": "string",
            "enum": ["MUST_FIX", "SHOULD_FIX", "NICE_TO_HAVE", "OUT_OF_SCOPE"]
          },
          "reviewer": {"type": "string"},
          "feedback_summary": {"type": "string"},
          "affected_section": {"type": "string"},
          "detailed_description": {"type": "string"},
          "suggested_resolution": {"type": "string"},
          "duplicate_mentions": {
            "type": "array",
            "items": {"type": "string"},
            "nullable": true,
            "description": "If other reviewers mentioned this, list them here"
          },
          "impact_if_not_fixed": {
            "type": "string",
            "nullable": true,
            "description": "For MUST-FIX, what happens if not addressed?"
          }
        }
      }
    },
    "must_fix_summary": {
      "type": "array",
      "description": "Consolidated list of all MUST-FIX items requiring spec revision",
      "items": {
        "type": "object",
        "properties": {
          "issue_id": {"type": "string", "example": "MUST-FIX-001"},
          "summary": {"type": "string"},
          "severity": {"type": "string", "const": "P1", "description": "All MUST-FIX items are P1 per conventions.md §1 (this list is the P1 subset). Use blocking_reason for why."},
          "blocking_reason": {"type": "string", "description": "What this P1 blocks (e.g., spillage path, 508 failure, broken core flow)."},
          "resolution_steps": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Specific steps to fix this issue"
          },
          "re_review_required": {"type": "boolean"}
        }
      }
    },
    "should_fix_summary": {
      "type": "array",
      "description": "Consolidated list of SHOULD-FIX items for consideration in revision",
      "items": {
        "type": "object",
        "properties": {
          "issue_id": {"type": "string", "example": "SHOULD-FIX-001"},
          "summary": {"type": "string"},
          "rationale": {"type": "string"},
          "suggested_fix": {"type": "string"}
        }
      }
    },
    "out_of_scope_items": {
      "type": "array",
      "description": "Items to document in spec's Deferred Explorations section",
      "items": {
        "type": "object",
        "properties": {
          "feedback_item": {"type": "string"},
          "reason_out_of_scope": {"type": "string"},
          "deferred_to_phase": {"type": "string", "nullable": true},
          "documentation_note": {
            "type": "string",
            "description": "Brief note for spec appendix explaining deferral"
          }
        }
      }
    },
    "conflicts_and_decisions": {
      "type": "array",
      "description": "Any contradictory feedback requiring a decision",
      "items": {
        "type": "object",
        "properties": {
          "conflict_description": {"type": "string"},
          "reviewer_a": {"type": "string"},
          "reviewer_a_position": {"type": "string"},
          "reviewer_b": {"type": "string"},
          "reviewer_b_position": {"type": "string"},
          "recommended_decision": {"type": "string"},
          "decision_rationale": {"type": "string"}
        }
      }
    },
    "next_steps": {
      "type": "object",
      "properties": {
        "immediate_actions": {
          "type": "array",
          "items": {"type": "string"},
          "description": "What needs to happen before next gate decision"
        },
        "spec_revision_required": {"type": "boolean"},
        "re_review_scope": {
          "type": "string",
          "enum": ["FULL", "FOCUSED", "NONE"],
          "description": "After revisions, what scope of re-review is needed?"
        },
        "timeline_estimate": {
          "type": "string",
          "description": "Estimated time to address MUST-FIX items and re-review",
          "example": "1-2 days for fixes, 1 day for re-review"
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
  "raw_feedback": "[Security Architect]: 'Section 2 renders the channel name in search results BEFORE the access check. This is a spillage path — a user sees \"Restricted Channel #SCI-X\" even if they lack Need-to-Know. Filter results to accessible channels before display.'\n\n[Compliance Officer]: 'Section 5 doesn't show audit logging. All access-policy changes must be logged per NIST 800-53 AU-2. This is a requirement.'\n\n[PM]: 'Could we add bulk attribute import in this phase? User research showed admins want to load many attributes at once.'\n\n[UX Designer]: 'Help text on the attribute field uses \"ABAC\" without explaining it. Should expand.'\n\n[Accessibility Lead]: 'The classification state relies on color alone — no icon or text. Fails Section 508 / WCAG 2.1 AA.'\n\n[Mobile Researcher]: 'Mobile section just says \"Identical to web\" but on a tactical handset the policy panel covers the full screen and scrolls. Need to be explicit about field constraints.'\n\n[PM again]: 'Section 2 says auto-save, but Section 3 says click Save button. Which is it?'\n\n[QA]: 'What happens if a user's clearance is revoked while a policy edit is pending? Edge case.'",
  "review_context": "Design Review Date: 2026-01-15\nArtifact: Environmental Attributes for ZT ABAC — UX Spec (v2.1)\nPhase: Phase 5 wireframe gate review\nReviewers: Security Architect (mandatory), Compliance Officer, PM, UX Designer, Accessibility Lead, Mobile Researcher, QA\nContext: IL5 DoD/defense environment. Security and compliance are mandatory approval items. Bulk attribute import was explicitly deferred to a later phase per PRD. Accessibility required for Section 508 / WCAG 2.1 AA."
}
```

**Output:**
```json
{
  "executive_summary": {
    "total_feedback_items": 8,
    "must_fix_count": 4,
    "should_fix_count": 2,
    "nice_to_have_count": 0,
    "out_of_scope_count": 1,
    "blocking_issues": true,
    "estimated_fix_effort": "MODERATE",
    "gate_recommendation": "REJECT",
    "gate_rationale": "Spec has 4 MUST-FIX (P1) items: a spillage path (classified channel name shown pre-check), a compliance gap (NIST 800-53 AU-2 audit logging), a Section 508 / WCAG 2.1 AA violation (color-only classification state), and a contradiction (auto-save vs. manual save). These block the gate and must be resolved before implementation. Estimated effort: 1-2 days to fix, 1 day for re-review. Recommend scheduling follow-up review for end of week.",
    "advisory_note": "REJECT here is an advisory recommendation to the orchestrator, not a gate decision. The orchestrator owns gate outcomes per gate-checklists.md."
  },
  "feedback_table": [
    {
      "category": "MUST_FIX",
      "reviewer": "Security Architect",
      "feedback_summary": "Access check renders restricted resource names to users without Need-to-Know (spillage path)",
      "affected_section": "Section 2: Policy Search Workflow",
      "detailed_description": "Section 2 renders the channel name in search results before the access check. A user sees 'Restricted Channel #SCI-X' in the dropdown even without Need-to-Know. This reveals the existence of a restricted resource to an unauthorized user — a spillage path.",
      "suggested_resolution": "Move the access check BEFORE display. Spec should state: 'The system filters search results to channels the user has Need-to-Know for. Channels the user cannot access are not shown.'",
      "impact_if_not_fixed": "Users can discover restricted channels they shouldn't know exist. Violates the DoD Need-to-Know model and NIST 800-207 ZT enforcement.",
      "duplicate_mentions": null
    },
    {
      "category": "MUST_FIX",
      "reviewer": "Compliance Officer",
      "feedback_summary": "Audit logging requirement missing entirely from spec",
      "affected_section": "Section 5 (entire section)",
      "detailed_description": "The PRD requires all access-policy changes to be logged for audit. The spec does not document this. For DoD deployment, audit logging per NIST 800-53 AU-2 is mandatory.",
      "suggested_resolution": "Add a section documenting: what events trigger audit log entries (policy create, edit, apply, revoke), what data is captured (timestamp, actor, subject, attributes changed), where logs are stored (audit service), and retention policy. Include an example log entry.",
      "impact_if_not_fixed": "Spec cannot pass the Security Architect gate. Feature cannot deploy to an IL5 environment without audit logging.",
      "duplicate_mentions": null
    },
    {
      "category": "MUST_FIX",
      "reviewer": "Accessibility Lead",
      "feedback_summary": "Classification state uses color alone (Section 508 / WCAG 2.1 AA failure)",
      "affected_section": "Section 4: Classification States",
      "detailed_description": "Section 4 conveys the classification state with a colored band only — no icon or text label. Users who are colorblind cannot distinguish the state. Violates Section 508 / WCAG 2.1 AA (mandatory for DoD).",
      "suggested_resolution": "Add to Section 4: 'The classification marking pairs the color band with the level text (e.g., \"SECRET\") and a lock icon. State is conveyed by color, text, and icon together.'",
      "impact_if_not_fixed": "Spec fails Section 508 / WCAG 2.1 AA. Feature cannot pass the accessibility gate.",
      "duplicate_mentions": null
    },
    {
      "category": "MUST_FIX",
      "reviewer": "PM",
      "feedback_summary": "Contradiction between auto-save behavior in different sections",
      "affected_section": "Section 2 vs. Section 3",
      "detailed_description": "Section 2 states 'Settings auto-save after user stops typing', but Section 3 says 'User clicks Save button to save settings'. Spec contradicts itself on whether save is automatic or manual. Implementation will be ambiguous.",
      "suggested_resolution": "Choose one behavior and apply consistently: Either (a) auto-save after inactivity timer, or (b) manual save with explicit button. Update both sections to be consistent. If auto-save, explain what happens if user navigates away — is save in progress?",
      "impact_if_not_fixed": "Engineering will receive ambiguous spec and have to guess which behavior is correct. Likely causes implementation to not match design intent.",
      "duplicate_mentions": ["PM mentioned this again in later feedback"]
    }
  ],
  "must_fix_summary": [
    {
      "issue_id": "MUST-FIX-001",
      "summary": "Spillage path: access check happens after restricted resource names are rendered",
      "severity": "P1",
      "blocking_reason": "Reveals existence of a restricted channel to a user without Need-to-Know",
      "resolution_steps": [
        "Review Section 2 Policy Search Workflow",
        "Move the access check before search-result display",
        "Update spec to state: 'The system filters results to channels the user has Need-to-Know for'",
        "Add security note: 'Restricted channels are not revealed in search results to unauthorized users'"
      ],
      "re_review_required": true
    },
    {
      "issue_id": "MUST-FIX-002",
      "summary": "Missing compliance requirement: audit logging not documented",
      "severity": "P1",
      "blocking_reason": "NIST 800-53 AU-2 audit logging is mandatory for IL5 deployment",
      "resolution_steps": [
        "Create a section documenting audit logging requirements",
        "Specify events: policy create, edit, apply, revoke, and any access changes",
        "Document data captured: timestamp, actor, subject, attributes changed",
        "Include an example audit log entry and retention policy",
        "Reference NIST 800-53 AU-2 / DoD ZT RA"
      ],
      "re_review_required": true
    },
    {
      "issue_id": "MUST-FIX-003",
      "summary": "Accessibility violation: classification state uses color alone",
      "severity": "P1",
      "blocking_reason": "Section 508 / WCAG 2.1 AA failure; blocks the accessibility gate",
      "resolution_steps": [
        "Update Section 4 Classification States",
        "Pair the color band with the level text and a lock icon",
        "Ensure the level text clearly identifies the classification",
        "Verify color contrast meets WCAG 2.1 AA (4.5:1 for text)"
      ],
      "re_review_required": true
    },
    {
      "issue_id": "MUST-FIX-004",
      "summary": "Contradiction: auto-save vs. manual save behavior",
      "severity": "P1",
      "blocking_reason": "Ambiguous spec; engineering would have to guess the intended behavior",
      "resolution_steps": [
        "Determine intended behavior: auto-save or manual save",
        "Update Section 2 and Section 3 to be consistent",
        "If auto-save: specify delay timer, in-progress indicators, what happens on navigation",
        "If manual-save: specify Save button location and success/failure feedback"
      ],
      "re_review_required": true
    }
  ],
  "should_fix_summary": [
    {
      "issue_id": "SHOULD-FIX-001",
      "summary": "Help text uses unexplained acronyms (ABAC, etc.)",
      "rationale": "Help text mentions ABAC without explaining it. Not every admin will know the term. Makes the spec less accessible to non-specialist stakeholders.",
      "suggested_fix": "Change help text from 'Define ABAC rules' to 'Define attribute-based rules (which user attributes and values grant access) for this channel.'"
    },
    {
      "issue_id": "SHOULD-FIX-002",
      "summary": "Mobile behavior needs explicit documentation beyond 'Identical to web'",
      "rationale": "Mobile section vaguely states 'Identical to web' but a tactical handset has real constraints: the policy panel goes full-screen on narrow screens, the classification badge can truncate, etc. Mobile-specific documentation prevents implementation surprises.",
      "suggested_fix": "Expand mobile section: 'Mobile: the policy panel is full-width and scrollable on narrow screens. The classification badge keeps its icon and level text when space is tight (color band may compress). Touch interactions identical to web (no swipe gestures). Leave space for the on-screen keyboard (panel max height 60% of viewport).'"
    }
  ],
  "out_of_scope_items": [
    {
      "feedback_item": "Add bulk attribute import in this phase",
      "reason_out_of_scope": "Bulk attribute import was explicitly marked out-of-scope for this phase in the PRD. It is a valid request for a later phase.",
      "deferred_to_phase": "Later phase (TBD)",
      "documentation_note": "Bulk attribute import (CSV upload or API batch): deferred. The single-attribute flow in this phase is the foundation for a later bulk import."
    }
  ],
  "conflicts_and_decisions": [
    {
      "conflict_description": "Contradictory feedback on save behavior between two spec sections",
      "reviewer_a": "Section 2",
      "reviewer_a_position": "Settings auto-save after user stops typing",
      "reviewer_b": "Section 3",
      "reviewer_b_position": "User clicks Save button to save settings",
      "recommended_decision": "Implement auto-save behavior (Section 2 is correct). Manual save creates extra clicks and friction.",
      "decision_rationale": "Auto-save is modern UX pattern and reduces user friction. However, spec must clarify: (1) How long does inactivity timer wait? (2) What if user navigates away during save? (3) Is there a visible 'Saving...' indicator? Update Section 3 to match Section 2."
    }
  ],
  "next_steps": {
    "immediate_actions": [
      "Schedule 1-hour refinement session with PM, Security Lead, and Accessibility Lead to discuss MUST-FIX-001 and MUST-FIX-004 (the complex ones)",
      "Assign spec revision task: 2 hours to implement MUST-FIX fixes (audit logging section, error state icons, consistency on save behavior)",
      "Assign security review: 30 min for Security Lead to verify information leakage fix",
      "Schedule 30-min re-review with focused scope on the 4 MUST-FIX items"
    ],
    "spec_revision_required": true,
    "re_review_scope": "FOCUSED",
    "timeline_estimate": "Spec revision: 2 hours. Re-review: 1 hour. Recommended schedule: Revisions by end of Wednesday, re-review Thursday morning, approved by Thursday EOD."
  }
}
```

## Validation Rules

1. **Categorization Clarity**: Every feedback item must be assigned to exactly one category (MUST-FIX, SHOULD-FIX, NICE-TO-HAVE, or OUT-OF-SCOPE). No item should be ambiguous.

2. **Actionability**: Every MUST-FIX and SHOULD-FIX item must have a specific suggested resolution, not vague advice. Resolution should be implementable by the spec author.

3. **Duplicate Detection**: If multiple reviewers mention the same issue, it should be noted as such (increases importance signal).

4. **Context Preservation**: Review context (who reviewed, when, what phase, why) should be evident in the output so recommendations are traceable.

5. **Gate Clarity**: The gate recommendation must be unambiguous: APPROVE, CONDITIONAL_APPROVAL, or REJECT — and labeled advisory (the orchestrator decides the gate, not this skill). Rationale must clearly explain the recommendation.

6. **Out-of-Scope Documentation**: Every OUT-OF-SCOPE item must have a note suitable for inclusion in the spec's Deferred Explorations appendix.

7. **Conflict Resolution**: If feedback items contradict, explicitly call out the conflict and recommend a decision (don't hide conflicts).

## Related Skills

- **Section Writer**: Writes spec sections; this skill processes feedback about those sections
- **Edge Case Hunter**: Identifies gaps in specs; this skill categorizes feedback about those gaps
- **Traceability Checker**: Maps PRD to spec; this skill processes feedback from traceability reviews
- **Flow Auditor**: Audits flows; this skill processes feedback from flow reviews

## Notes for DoD/Defense Context

This skill applies heightened scrutiny to feedback related to:
- **Security findings**: Any security-related MUST-FIX (P1) items get escalated to security review before proceeding
- **Compliance violations**: Section 508 / WCAG 2.1 AA, audit logging (NIST 800-53 AU-2), and NIST 800-207 / 800-162 feedback gets marked MUST-FIX (P1)
- **Access control and permission model**: Feedback on role-based / ABAC behavior and access checks is treated as P1
- **Information barriers / spillage**: Feedback about revealing restricted resources or cross-domain data leakage is marked MUST-FIX (P1)
- **Conflict resolution**: When security and usability feedback conflict (e.g., "the access check is inconvenient"), security wins unless explicitly overridden by product leadership

---

**Last Updated**: 2026-03-10
**Maintainer**: Mattermost Design Team