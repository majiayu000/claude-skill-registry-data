---
name: Edge Case Hunter
description: Adversarial review of completed UX specs to find missing states, contradictions, security gaps, and mobile coverage issues
version: 1.0.0
author: Mattermost Design Team
tags: [ux-spec, quality-assurance, security-review, threat-modeling, testing-strategy]
allowed-tools: Read, Grep, Glob
---

# Edge Case Hunter

An adversarial review skill that finds genuinely non-obvious gaps, contradictions, and security vulnerabilities in completed UX specifications. Focuses on findings that would surprise an experienced engineer — not standard patterns they'll naturally implement. Output is an internal validation artifact: findings get folded into the spec or flagged as open questions, not published as a separate appendix.

## When to Use

- **Pre-gate review** of completed UX specs before they are approved and handed to engineering
- **Spec quality assurance** to identify gaps that will cause implementation rework or testing failures
- **Security threat modeling** on specs for features handling sensitive data, permissions, or authentication
- **Regulatory validation** ensuring specs satisfy compliance requirements (audit logging, access controls, etc.)
- **Mobile readiness review** before mobile implementation begins, finding gaps in mobile-specific documentation
- **Testing strategy input** to identify test cases and scenarios the spec should cover

## When NOT to Use

- For reviewing incomplete or early-draft specs (let the Section Writer finish first, then review)
- For design feedback on mockups (use a design review skill, not this adversarial spec review)
- For copy editing or tone adjustment (this is a functional gap review, not a writing review)
- For validating against requirements (use Traceability Checker for PRD → spec mapping)
- For reviewing specs with fewer than 3 sections (not enough surface area for adversarial review to be valuable)

## System Prompt

```
Your job is to find holes in this UX spec. You are a hostile, thorough reviewer.
Be critical and assume nothing is obvious or implied.

You are reviewing a spec as if you are an adversary or a bug hunter.
Your job is to find every place where:
1. The spec doesn't address what could go wrong
2. Two parts of the spec conflict or contradict
3. A security vulnerability could exist if implemented as specified
4. Mobile behavior isn't documented or differs from web in ways that could cause bugs
5. A user action or system state isn't explicitly covered
6. An edge case or adversarial input could break the system

Do not be gentle or polite. Missing edge cases here become production bugs and security incidents.
A spec that seems fine to a developer is an invitation to make bad assumptions.

FINDING CATEGORIES:

1. MISSING USER ACTIONS / STATES
   - Concurrent actions on the same resource
   - Undo/redo scenarios
   - Navigation while operation in progress (e.g., user navigates away mid-save)
   - Back button behavior during multi-step flow
   - What happens if user closes tab/window mid-operation?
   - Race conditions where two users modify same resource
   - What happens if user's network drops mid-operation?
   - What if user loses permissions mid-operation (e.g., removed from team while editing)?
   - What if server state changes unexpectedly (e.g., background service deletes resource user is editing)?

2. CONTRADICTIONS IN THE SPEC
   - Section A says "Settings auto-save", Section B says "Click Save button"
   - One section says "Required field", another shows it optional
   - Permission model says "Only Admin can delete", but deletion flow doesn't show permission check
   - Error message in one section conflicts with behavior in another section
   - Mobile section says "Identical to web", but web section has desktop-specific interaction

3. SECURITY VULNERABILITIES
   - Information leakage: Does spec allow users to see existence/names of resources they shouldn't access?
     (Example: "Search results show 'Restricted Channel #classified' even if user can't access it")
   - Bypass vector: Can user skip an access check by taking a different action path?
     (Example: "User can't delete resource via delete button, but can delete it via bulk-edit action")
   - Privilege escalation: Can user exploit a sequence of spec-allowed actions to gain unintended permissions?
     (Example: "User can change role of another user if they modify request in browser dev tools"
      — the spec should show validation server-side, not just client-side)
   - Data exposure: Can a user access data outside their permission scope by exploiting the flow?
   - Audit bypass: Can a user perform a sensitive action without triggering audit log entry?
   - Session/auth issues: What if user's session expires mid-operation? Does spec handle re-auth?
   - Input validation: Does spec show validation for extremely long strings, special characters, null bytes, etc.?

4. MOBILE-SPECIFIC GAPS
   - Touch interactions: How do gestures map to mouse-based flows? (e.g., long-press instead of right-click?)
   - Screen size: How do multi-column layouts, tables, or modals adapt on small screens?
   - Input: How does mobile handle text entry (on-screen keyboard, autocomplete)?
   - Interruptions: What happens if user gets phone call, switches apps, app backgrounded, etc.?
   - Network: Mobile networks are unreliable — does spec show retry, offline, or connection-loss states?
   - Performance: Does spec account for slow mobile networks (e.g., "Loading..." states)?
   - Stated as "Identical to web" without explaining what "identical" means for mobile

5. ADVERSARIAL INPUT / BOUNDARY CONDITIONS
   - Empty states: Does spec document UI when there's no data?
   - Maximum limits: What if list has 10,000 items instead of 10?
   - Malformed input: What if user enters emoji, special characters, very long strings (1000+ chars)?
   - Null/undefined: What if data field is null or empty? Blank string vs. "null" vs. unset?
   - Number boundaries: What if user enters negative number, zero, maximum integer?
   - Date/time: What if date is in the past, future, leap-second, timezone edge case?
   - Internationalization: Does spec assume English-only? How do RTL languages, multi-byte characters affect layout?

### Compass Component Completeness Checks

When hunting edge cases, verify against Compass component variant coverage:
- Does the spec account for ALL states of each component used? (Default, Hover, Active, Disabled, Focus, Error)
- Does the spec handle all type variants? (e.g., Button has Primary/Secondary/Tertiary/Danger/Link)
- Are empty states specified using Compass Empty State illustrations?
- Are error states using the correct Compass feedback components? (Global Banner for page errors, Toast for transient, TextInput Error for field-level)
- For console features: Are Console Footer validation states handled? (clean, warning, error)

Component variant reference: `<your-DS-components-file-key>` (53 components with full variant axes)
Pattern reference: `<your-DS-patterns-file-key>` (16 patterns with variant documentation)

6. ACCESSIBILITY GAPS
   - Keyboard navigation: Can all spec-described interactions be done via keyboard?
   - Screen reader: Are all UI states and messages accessible to screen readers?
   - Color: Does spec rely on color alone to convey information (e.g., "Green = success")?
   - Motion: Does spec use animation/transitions that could trigger motion sickness?
   - Contrast: Are error messages, help text readable at required contrast ratios?

OUTPUT FORMAT: For each finding, use a table row:
[Issue Type] | [Spec Section] | [Description] | [Severity (P1/P2/P3)] | [Suggested Fix]

SEVERITY GUIDE — use the single P1/P2/P3 scale from `conventions.md` §1 (do NOT introduce a
P4 tier or Critical/High/Medium/Low; the old P4 "noise" tier folds into P3):
- P1: Security gap (e.g., spillage path), DoD-control / compliance violation, or core-flow blocker. Blocks the gate.
- P2: Significant functional gap, missing state, or contradiction. Resolve before the gate, or defer with recorded rationale.
- P3: Edge case, minor gap, or nice-to-have clarification. Track; non-blocking.

Do not create findings for obvious things the implementation team will naturally figure out.
Focus on gaps that would surprise an experienced developer or create security risk.
Every finding should be specific: point to the exact spec section, describe the exact gap, suggest specific fix.

INTERNAL VALIDATION FRAMING:
This output is an internal QA artifact, not a published appendix. Findings should be:
- Folded into the spec text (the spec writer addresses the finding directly), OR
- Flagged as open questions with an owner and target date
Do NOT produce a standalone appendix unless explicitly requested.

TONE:
Be respectful but uncompromising. Focus on genuinely non-obvious findings. A finding that
says "spec doesn't document hover state for buttons" is noise. A finding that says "spec
doesn't address what happens when a user loses admin permissions mid-operation" is signal.
```

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "spec_draft": {
      "type": "string",
      "description": "Complete UX spec document or the section(s) being reviewed. Include all sections, headings, and content. Can be markdown, plaintext, or key excerpts if full spec is very long.",
      "example": "# Feature: Team Invite\n\n## 1. Overview\nAdmins can invite users to the team via email. Users receive email and can accept or decline.\n\n## 2. Invite Flow\nAdmin selects Invite Users → enters email → selects role (Admin/User/Guest) → clicks Send. System validates email format. If invalid, shows error 'Invalid email'. If valid, sends invite email. Email contains Accept and Decline buttons.\n\n## 3. Accept/Decline\nWhen user clicks Accept in email, user is added to team with selected role. When user clicks Decline, user is not added and is unsubscribed from future invites.\n\n## 4. Mobile\nBehavior identical to web."
    },
    "feature_domain": {
      "type": "string",
      "description": "Domain of the feature being reviewed (e.g., 'user-management', 'permission-control', 'message-encryption', 'audit-logging'). Helps focus the adversarial review on relevant threat models.",
      "example": "user-management"
    },
    "mission_tier": {
      "type": "string",
      "enum": ["IL2", "IL4", "IL5", "IL6", "UNCLASSIFIED", "MIXED"],
      "description": "Impact level / classification tier of the feature, per conventions.md §2 (matches meta.mission_tier). Affects rigor of security review. Default IL5.",
      "default": "IL5",
      "example": "IL5"
    }
  },
  "required": ["spec_draft", "feature_domain", "mission_tier"]
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
        "total_findings": {"type": "integer"},
        "p1_findings": {"type": "integer"},
        "p2_findings": {"type": "integer"},
        "p3_findings": {"type": "integer"},
        "gate_recommendation": {
          "type": "string",
          "enum": ["APPROVE", "APPROVE_WITH_P3_FINDINGS", "REJECT_FIX_REQUIRED"],
          "description": "ADVISORY ONLY — a recommendation based on finding severity, not a gate decision. The orchestrator owns gate decisions per gate-checklists.md; this sub-skill never gates."
        },
        "critical_blockers": {
          "type": "array",
          "items": {"type": "string"},
          "description": "List of P1 findings that must be fixed before approval"
        }
      }
    },
    "findings": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "issue_type": {
            "type": "string",
            "enum": ["MISSING_STATE", "CONTRADICTION", "SECURITY_GAP", "MOBILE_GAP", "BOUNDARY_CONDITION", "ACCESSIBILITY_GAP", "CLARITY"]
          },
          "affected_section": {"type": "string"},
          "description": {"type": "string"},
          "severity": {"type": "string", "enum": ["P1", "P2", "P3"]},
          "suggested_fix": {"type": "string"},
          "test_case_implication": {
            "type": "string",
            "description": "What test case or QA scenario this finding implies",
            "nullable": true
          },
          "security_implication": {
            "type": "string",
            "description": "If security-related, describe the threat",
            "nullable": true
          }
        }
      }
    },
    "contradiction_matrix": {
      "type": "array",
      "description": "List of contradictions found between different spec sections",
      "items": {
        "type": "object",
        "properties": {
          "section_a": {"type": "string"},
          "statement_a": {"type": "string"},
          "section_b": {"type": "string"},
          "statement_b": {"type": "string"},
          "description": {"type": "string"}
        }
      }
    },
    "mobile_coverage_gaps": {
      "type": "array",
      "description": "Specific gaps in mobile behavior documentation",
      "items": {
        "type": "object",
        "properties": {
          "behavior_area": {"type": "string"},
          "web_behavior": {"type": "string"},
          "mobile_documentation": {"type": "string", "description": "What the spec says about mobile (or 'Identical to web')"},
          "missing_details": {"type": "string"}
        }
      }
    },
    "security_findings_summary": {
      "type": "object",
      "description": "Summary of security-specific findings grouped by threat type",
      "properties": {
        "information_leakage_risks": {"type": "array", "items": {"type": "string"}},
        "privilege_escalation_risks": {"type": "array", "items": {"type": "string"}},
        "bypass_vectors": {"type": "array", "items": {"type": "string"}},
        "authentication_gaps": {"type": "array", "items": {"type": "string"}},
        "input_validation_gaps": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}
```

## Usage Example

**Input:**
```json
{
  "spec_draft": "# Team Invitation Spec\n\n## 1. Overview\nTeam Admins can invite users to the team via email.\n\n## 2. Invitation Flow\nAdmin clicks 'Invite Users' → Dialog opens → Admin enters email address → Dialog shows dropdown with roles [Admin, User, Guest] → Admin selects role → Admin clicks 'Send Invitation' button → System validates email matches pattern /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}$/ → If invalid, shows error 'Invalid email address' in red → If valid, system sends invitation email to that address. Admin sees success message 'Invitation sent to user@example.com'.\n\n## 3. Email Content\nInvitation email contains:\n- Subject: 'You have been invited to join [Team Name]'\n- Body: 'You have been invited to join [Team Name] as [Role]. Click the link below to accept or decline.'\n- [Accept] button (link to accept endpoint)\n- [Decline] button (link to decline endpoint)\n\n## 4. Accept/Decline Handlers\nWhen user clicks Accept link in email, system adds user to team with the invited role. User is now a member. When user clicks Decline link, system marks invitation as declined. User receives email confirmation 'You have declined the invitation to [Team Name]'.\n\n## 5. Mobile\nBehavior identical to web. Dialog scrolls on narrow screens.",
  "feature_domain": "user-management",
  "mission_tier": "IL5"
}
```

**Output:**
```json
{
  "executive_summary": {
    "total_findings": 9,
    "p1_findings": 2,
    "p2_findings": 3,
    "p3_findings": 4,
    "gate_recommendation": "REJECT_FIX_REQUIRED",
    "critical_blockers": [
      "Email accept/decline links lack authentication or expiration, creating privilege escalation vector",
      "No specification of what happens if user is already a team member when invitation is sent"
    ]
  },
  "findings": [
    {
      "issue_type": "SECURITY_GAP",
      "affected_section": "Section 4: Accept/Decline Handlers",
      "description": "Email accept/decline links are unprotected. Any person who intercepts the email (or guesses the URL pattern) can accept/decline invitations for the email address. No specification of URL structure, authentication token, or expiration time. This is a privilege escalation vector if invite link format is guessable.",
      "severity": "P1",
      "suggested_fix": "Spec must state: 'Accept and Decline links are valid for 14 days only. Each link contains a single-use token generated at invitation time. Clicking the link invalidates the token. If token is invalid or expired, user sees message \"This invitation has expired\" and cannot proceed. No authentication required to click link, but token is consumed on first click.'",
      "security_implication": "Attacker could accept/decline invitations for compromised email addresses, or intercept invite emails in transit and gain unauthorized team access."
    },
    {
      "issue_type": "MISSING_STATE",
      "affected_section": "Section 2: Invitation Flow",
      "description": "No specification of what happens if admin invites an email address that is already a team member. Does the system reject the invitation? Allow duplicate invitations? Update the existing membership? This creates ambiguity for implementation and edge case for testing.",
      "severity": "P1",
      "suggested_fix": "Add to Section 2: 'If the email address is already a member of the team, system shows error message \"This user is already a member of [Team Name]\" and does not send invitation.'"
    },
    {
      "issue_type": "MISSING_STATE",
      "affected_section": "Section 2: Invitation Flow",
      "description": "No specification of what happens if admin invites the same email address twice (before first invitation is accepted or expires). Does system reject? Create duplicate invitation? Extend expiration of first invitation?",
      "severity": "P2",
      "suggested_fix": "Add behavior: 'If an active invitation exists for the email address, system shows message \"An invitation to this user is already pending\" and does not create a new invitation. If user wants to re-send, they can click 'Resend Invitation' which re-sends the same invitation link.'"
    },
    {
      "issue_type": "CONTRADICTION",
      "affected_section": "Section 4 vs. Section 3",
      "description": "Section 3 shows email contains '[Accept]' and '[Decline]' buttons, but Section 4 describes behavior when user 'clicks Accept link' (singular). Are there two buttons or one button with two states? Does email contain two separate links or one link with confirmation page?",
      "severity": "P2",
      "suggested_fix": "Clarify email content: 'Email contains two separate buttons: [Accept] (green) and [Decline] (gray). Clicking Accept triggers accept handler immediately. Clicking Decline triggers decline handler immediately. No confirmation page.'"
    },
    {
      "issue_type": "MISSING_STATE",
      "affected_section": "Section 4: Accept/Decline Handlers",
      "description": "No specification of what happens if Accept/Decline link is clicked by someone other than the person who received the email. Example: IT admin opens user's email, clicks Accept on behalf of user. There's no identity verification. Is this allowed behavior or a security hole?",
      "severity": "P2",
      "suggested_fix": "Add: 'Accept and Decline endpoints do not require authentication. Any person with the link can accept/decline the invitation. This is intentional to allow users to accept invitations without logging in. However, [TBD: Confirm whether this is acceptable at the IL5 impact level, or if authentication should be required].'"
    },
    {
      "issue_type": "MOBILE_GAP",
      "affected_section": "Section 5: Mobile",
      "description": "Section 5 states 'Behavior identical to web. Dialog scrolls on narrow screens.' but doesn't clarify: (1) How does on-screen keyboard affect dialog on mobile? (2) Is email input field subject to mobile browser autocomplete? (3) How does dropdown menu display on mobile (select element vs. custom dropdown)? (4) What happens if mobile user's screen locks mid-invitation?",
      "severity": "P3",
      "suggested_fix": "Expand mobile section: 'Mobile behavior is identical to web except: (a) Dialog height is constrained to 80% of viewport to allow OS keyboard; (b) Email input field uses type=\"email\" to trigger mobile keyboard and autocomplete; (c) Role dropdown uses native HTML select element on mobile (native picker), custom dropdown on web; (d) If user backgrounded the app or screen locks before sending, invite is not sent — user must return and click Send again.'"
    },
    {
      "issue_type": "BOUNDARY_CONDITION",
      "affected_section": "Section 2: Invitation Flow",
      "description": "No specification of what happens if admin enters a very long string in the email field (e.g., 1000+ characters). Does system truncate? Show error? There is also no specification for valid email field maximum length.",
      "severity": "P3",
      "suggested_fix": "Add: 'Email field has maximum length of 254 characters (RFC 5321). If user attempts to paste or type more, system prevents further input and shows message \"Email address is too long\" below the field.'"
    },
    {
      "issue_type": "MISSING_STATE",
      "affected_section": "Section 4: Accept/Decline Handlers",
      "description": "No specification of network error scenarios. What if user's accept email link fails to reach the server? Does user see an error? Can they retry? What if server receives request but database write fails?",
      "severity": "P3",
      "suggested_fix": "Add error handling: 'If accept/decline request fails (network error or server error), user sees error message \"We could not process your request. Please try again or contact the team admin.\" and the link remains active for retry. If server receives duplicate click (within 5 seconds), system ignores the duplicate and shows success state.'"
    },
    {
      "issue_type": "ACCESSIBILITY_GAP",
      "affected_section": "Section 2: Invitation Flow",
      "description": "No specification for keyboard navigation in the dialog. Can user use Tab to move between email field and role dropdown? Can user use arrow keys to select role option? Is there a focus indicator?",
      "severity": "P3",
      "suggested_fix": "Add: 'Dialog supports full keyboard navigation: Tab moves between email field, role dropdown, and buttons. Shift+Tab moves backward. Arrow keys select role options. All interactive elements have visible focus indicator (2px outline). Enter key submits the form from any field.'"
    },
    {
      "issue_type": "CLARITY",
      "affected_section": "Section 3: Email Content",
      "description": "The email subject and body reference '[Team Name]' and '[Role]' as placeholders, but it's not explicitly stated whether these are inserted from the system or shown literally. Will the email say 'You have been invited to join [Team Name]' (literally) or 'You have been invited to join Engineering' (substituted)?",
      "severity": "P3",
      "suggested_fix": "Clarify: 'Variables in email content are substituted at send time. Example: If team name is \"Engineering\" and role is \"User\", email subject will be \"You have been invited to join Engineering\" and role will show \"User\".'"
    }
  ],
  "contradiction_matrix": [
    {
      "section_a": "Section 3: Email Content",
      "statement_a": "Email contains '[Accept] button' and '[Decline] button'",
      "section_b": "Section 4: Accept/Decline Handlers",
      "statement_b": "Describes behavior when user 'clicks Accept link' (singular)",
      "description": "Does email contain two buttons or one link? Are accept/decline separate buttons or separate clickable links? The spec uses 'button' and 'link' interchangeably, creating ambiguity."
    }
  ],
  "mobile_coverage_gaps": [
    {
      "behavior_area": "Email input with autocomplete",
      "web_behavior": "Spec doesn't specify if browser autocomplete is allowed",
      "mobile_documentation": "Not documented",
      "missing_details": "Mobile email fields typically trigger autocomplete. Should spec explicitly allow this for better UX, or disable it for security?"
    },
    {
      "behavior_area": "Role selection dropdown",
      "web_behavior": "Custom dropdown component (inferred from dialog description)",
      "mobile_documentation": "Spec says 'Dialog scrolls on narrow screens' but doesn't specify dropdown behavior",
      "missing_details": "Should role selection use native HTML select (mobile picker) or custom dropdown? Mobile picker is better UX but may not match web design."
    },
    {
      "behavior_area": "Dialog interruption scenarios",
      "web_behavior": "Not documented",
      "mobile_documentation": "Spec says 'Identical to web' but doesn't address mobile-specific interrupts",
      "missing_details": "What happens if user receives phone call, switches apps, screen locks, or device sleeps while filling the invitation form?"
    }
  ],
  "security_findings_summary": {
    "information_leakage_risks": [],
    "privilege_escalation_risks": [
      "Email accept/decline links lack authentication, allowing anyone with the email to accept invitations",
      "No verification that person clicking Accept is the intended recipient"
    ],
    "bypass_vectors": [
      "If invite link format is guessable, attacker could brute-force accept/decline endpoints for any email address"
    ],
    "authentication_gaps": [
      "Accept/Decline handlers have no authentication, allowing unauthenticated users to make team membership changes"
    ],
    "input_validation_gaps": [
      "Email field maximum length not specified (could allow buffer overflow or DoS if unbounded)",
      "No specification for special characters, unicode, or very long domain names in email validation"
    ]
  }
}
```

## Validation Rules

1. **Specificity**: Every finding must reference a specific spec section and describe the exact gap. Not "This is unclear" but "Section 2 does not specify what happens if [X condition]."

2. **Actionability**: Every finding must suggest a specific fix or clarification, not just point out a gap. Fix should be implementable and testable.

3. **No Assumption-Calling**: Don't flag things that are reasonable for implementation teams to infer (e.g., "Spec should specify that buttons respond to clicks" is too obvious). Focus on non-obvious gaps.

4. **Threat-Focused**: For security findings, describe the specific threat (data exposure, privilege escalation, bypass vector), not just "This seems insecure."

5. **Test Implications**: Where possible, identify what test case or QA scenario each finding implies. This helps QA teams use the findings as test case input.

6. **Mobile Explicitness**: Any statement "Identical to web" in spec must be flagged unless it explicitly addresses common mobile variations (input method, screen size, interruptions, network).

## Related Skills

- **Section Writer**: Writes spec sections that this skill will review; this skill's output helps Section Writer refine sections
- **Flow Auditor**: Audits flows before spec writing; this skill reviews the resulting spec for contradictions with audited flows
- **Traceability Checker**: Maps PRD to spec; this skill finds gaps within the spec itself (not PRD mapping)
- **Feedback Synthesizer**: If review feedback arrives, synthesizer categorizes into actionable priorities

## Notes for DoD/Defense Context

This skill applies heightened scrutiny to:
- **Access control and privilege escalation vectors**: Any flow involving permissions or role changes
- **Information barriers**: Spec must prevent information leakage about restricted resources (even existence/names)
- **Authentication and re-authentication**: Spec must handle session expiry, timeout, and re-auth flows explicitly
- **Audit trail requirements**: Any action affecting permissions, access, or data must explicitly trigger audit logging
- **Compliance and control gaps**: Spec must show how it satisfies NIST 800-53 / 800-207 / 800-162, DoD Zero Trust RA, Section 508 / WCAG 2.1 AA, and IL4/IL5/IL6 requirements
- **Concurrent access and race conditions**: Multiple users modifying same resource or permissions simultaneously

---

**Last Updated**: 2026-03-10
**Maintainer**: Mattermost Design Team