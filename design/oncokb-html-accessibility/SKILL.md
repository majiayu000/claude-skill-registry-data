---
name: oncokb-html-accessibility-reference
description: Audit designs, prototypes, or built interfaces for accessibility risks using WCAG-aligned principles adapted for healthcare, clinical, and enterprise environments. Use to identify barriers, assess severity, and determine when expert review is required.
license: Proprietary
metadata:
  author: ux-design-team
  domain: healthcare-ux
  standards: wcag-2.2, section-508, nhs-accessibility
  version: "1.0"
---
# Accessibility Audit (Healthcare UX)
## Purpose
This skill enables a **structured accessibility audit** of digital interfaces used in healthcare, clinical, operational, or patient-facing contexts.
It translates established accessibility standards into **practical audit steps** that can be applied early, repeatedly, and consistently—especially in AI-assisted or rapid development workflows.
Use this skill to:
- Identify accessibility barriers
- Reduce clinical, legal, and ethical risk
- Improve usability for all users, not only those with disabilities
- Evaluate AI-generated or prototype interfaces before release
This skill is evaluative, not certifying.
---
## When to Use This Skill
Apply this skill when:
- Reviewing wireframes, designs, prototypes, or production UI
- Evaluating AI-generated interfaces or workflows
- Auditing internal tools used by clinicians or staff
- Assessing patient-facing experiences
- Accessibility requirements are unclear, assumed, or undocumented
This skill complements—but does not replace—formal compliance testing or assistive technology testing.
---
## How to Use This Skill
1. Define the **scope**
   - Page, screen, component, or workflow
2. Identify **primary user roles**
   - Clinician, coordinator, patient, caregiver, admin
3. Walk through realistic tasks end-to-end
4. Evaluate findings across each audit domain
5. Document **specific, observable issues**
6. Assign severity and remediation guidance
7. Escalate when risk exceeds self-service thresholds
Focus on real interaction flows, not static screenshots alone.
---
## Audit Framework
This audit is organized around **eight accessibility domains**, aligned with the intent of WCAG 2.2, Section 508, and healthcare service guidance.
Evaluate each domain independently.
---
### 1. Perceivable Content
Users must be able to perceive information regardless of sensory ability.
**Evaluate whether:**
- Text alternatives exist for non-text content
- Text and UI elements meet contrast requirements
- Information is not conveyed by color alone
- Visual hierarchy supports fast comprehension
**Healthcare emphasis**
- Low contrast and color-only indicators increase error risk
- Status, priority, and alerts must be perceivable by all users
---
### 2. Operable Interaction (Keyboard & Input)
Users must be able to operate the interface with different input methods.
**Evaluate whether:**
- All functionality is keyboard accessible
- Focus order follows a logical task flow
- Focus indicators are always visible
- No interaction traps users unintentionally
**Healthcare emphasis**
- Keyboard access is critical for assistive technologies
- Lost focus during clinical workflows creates failure points
---
### 3. Understandable Language & Behavior
Content and interactions must be predictable and easy to understand.
**Evaluate whether:**
- Language is plain, clear, and audience-appropriate
- Labels and instructions are unambiguous
- Similar actions behave consistently
- Errors are explained clearly and respectfully
**Healthcare emphasis**
- Ambiguity increases cognitive load
- Error messages must support recovery, not blame
---
### 4. Robust Structure & Semantics
Content must be correctly interpreted by assistive technologies.
**Evaluate whether:**
- Headings follow a meaningful hierarchy
- Landmarks and roles are used appropriately
- Forms and controls use proper semantics
- Tables expose headers and relationships clearly
**Healthcare emphasis**
- Poor semantics can completely block screen reader use
- Data tables require explicit structure to be usable
---
### 5. Forms & Data Entry
Data entry must be accessible, accurate, and forgiving.
**Evaluate whether:**
- Inputs have clear labels and instructions
- Required fields are communicated accessibly
- Errors are identified and explained inline
- Validation does not block assistive technologies
**Healthcare emphasis**
- Data entry errors can affect care and operations
- Recovery must be fast and obvious
---
### 6. Status, Feedback, and System Messages
Users must always understand what the system is doing.
**Evaluate whether:**
- Loading, success, and error states are visible
- Status changes are announced to assistive technologies
- Feedback is timely and meaningful
**Healthcare emphasis**
- Silent failures erode trust
- Clear feedback reduces hesitation and repeat actions
---
### 7. Motion, Timing, and Sensory Safety
Interfaces must not cause discomfort or harm.
**Evaluate whether:**
- Motion can be reduced or disabled
- No flashing or rapid animations are present
- Time limits can be extended or avoided
- Transitions are predictable and calm
**Healthcare emphasis**
- Motion sensitivity and fatigue are common
- Calm interfaces reduce stress in high-stakes contexts
---
### 8. Cognitive Load & Task Complexity
Accessibility includes cognitive accessibility.
**Evaluate whether:**
- Tasks are broken into manageable steps
- Information is chunked and prioritized
- The interface supports recognition over recall
- Users are not overwhelmed with simultaneous demands
**Healthcare emphasis**
- Cognitive overload increases error rates
- Simplicity supports safety, not oversimplification
---
## Severity Classification
Each identified issue should be assigned a severity level:
- **Critical** — Blocks access or introduces safety risk
- **High** — Major barrier with no reasonable workaround
- **Medium** — Partial barrier or significant usability degradation
- **Low** — Minor issue or improvement opportunity
Severity should reflect **real user impact**, not theoretical compliance.
---
## Output Expectations
A completed accessibility audit should result in:
- A list of concrete accessibility issues
- The affected users and interaction contexts
- Severity level for each issue
- Clear remediation guidance
- Explicit escalation flags where needed
Avoid vague findings such as “improve accessibility” or “not compliant.”
---
## Common Pitfalls to Avoid
- Treating accessibility as visual contrast only
- Relying solely on automated tools
- Confusing compliance with usability
- Ignoring cognitive and clinical context
- Auditing without task-based walkthroughs
---
## When to Escalate
Escalate for expert accessibility or UX review when:
- The issue affects patient-facing experiences
- Clinical decision-making is involved
- Assistive technology compatibility is uncertain
- Legal or regulatory exposure is possible
- Remediation is complex or systemic
- Multiple high-severity issues cluster together
Escalation is a strength, not a failure.
---
## References

`references/audit_reference_guide.md`

This skill is informed by established accessibility standards and healthcare service guidance, including:
- WCAG 2.2 principles and success criteria
- U.S. Section 508 accessibility requirements
- NHS digital service accessibility practices
These sources are intentionally abstracted into actionable audit guidance suitable for rapid and AI-assisted workflows.
