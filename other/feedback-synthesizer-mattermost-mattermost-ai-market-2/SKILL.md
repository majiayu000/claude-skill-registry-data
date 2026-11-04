---
name: Feedback Synthesizer
description: Categorizes raw stakeholder feedback into actionable priority tiers with suggested fixes for gate decisions
version: 1.0.0
author: Mattermost Design Team
tags: [ux-spec, feedback-management, gate-review, stakeholder-management, decision-support]
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
  "required": ["review_context", "executive_summary", "feedback_table", "must_fix_summary"],
  "properties": {
    "review_context": {
      "type": "object",
      "description": "Preserved from the input for traceability (who/when/what phase).",
      "properties": {
        "review_date": {"type": "string"},
        "artifact": {"type": "string"},
        "phase": {"type": "string"},
        "reviewers": {"type": "array", "items": {"type": "string"}}
      },
      "required": ["review_date", "artifact", "phase"]
    },
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
        "advisory_note": {"type": "string", "description": "Restates that gate_recommendation is advisory — the orchestrator owns the gate decision."}
      },
      "required": ["total_feedback_items", "must_fix_count", "should_fix_count", "nice_to_have_count", "out_of_scope_count", "blocking_issues", "gate_recommendation", "gate_rationale"]
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
        },
        "required": ["category", "reviewer", "feedback_summary", "affected_section"]
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

A full worked example (raw feedback in → categorized output) lives in [`EXAMPLE.md`](./EXAMPLE.md),
kept out of this file to stay under the 500-line skill limit. Load it on demand for a concrete reference.

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