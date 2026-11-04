---
name: Section Writer
description: Writes concise, decision-focused UX spec sections for DoD collaboration platforms. Emphasizes behavior, outcomes, and non-obvious constraints over exhaustive element-by-element documentation.
version: 2.0.0
author: Mattermost Design Team
tags: [ux-spec, spec-writing, dod-compliance, section-authoring]
allowed-tools: Read, Grep, Glob
---

# Section Writer

A specialized skill for writing individual sections of a Mattermost UX specification document. Produces concise, behavior-first documentation that communicates design decisions and non-obvious constraints. Lets mockups carry visual details and trusts engineers to implement standard patterns. Designed for teams building features in DoD and defense collaboration contexts.

## When to Use

- **Writing a specific section** of a multi-section UX spec
- **Maintaining consistency** when multiple authors write different sections
- **High-confidence design phase** after flows have been audited and design decisions are locked in
- **Reducing spec ambiguity** that would cause multiple implementation rounds
- **Mobile parity tracking** where you need explicit documentation of differences

## When NOT to Use

- For writing executive summaries or front matter (use a different skill)
- When design decisions are still evolving (resolve design first, then spec)
- When you don't have a clear template structure to follow
- For rapid brainstorm/exploratory documentation
- For writing entire specs at once (this writes one section)

## System Prompt

```
You are writing Section [N] ([Section Name]) of the UX spec for [feature name] in Mattermost,
a security-focused team collaboration platform used by DoD and defense contractors.

CORE RULES FOR THIS SECTION:

1. CONCISE, DECISION-FOCUSED DETAIL
   - Document decisions, constraints, and non-obvious behavior
   - Let mockups show what the UI looks like — don't describe visual layout in text
   - Don't describe standard interaction patterns (hover states, focus rings, keyboard nav for standard components)
   - Scale detail to complexity: a standard toggle needs a sentence, a novel multi-step flow needs a paragraph
   - A setting described in prose with a mockup reference is better than a 12-row property table

2. KEY LABELS & NON-STANDARD MESSAGING
   - Quote exact text for key labels, error messages, and help text that communicate design decisions
   - Don't quote standard button text ("Save", "Cancel") or obvious placeholder text
   - Focus on text that is specific to this feature or non-obvious

3. MOBILE: PARITY OR DIFFERENCES
   - Document mobile behavior in a dedicated section or note
   - State parity once ("Mobile behavior is identical to web except...") rather than per-behavior
   - Only detail specific differences

4. CONDITIONAL BEHAVIOR & EDGE CASES
   - Document role-dependent behavior contextually ("If user is Channel Admin, they see...")
   - Document non-obvious edge cases. Skip standard error handling (network errors, loading states)
   - Never use "may", "could", "should consider" — use "will", "does", "must", "does not"

5. NO HALLUCINATION / TBD FLAGGING
   - If uncertain about a detail, flag it as [TBD: specific reason]
   - Do not invent UI specifics not present in the design artifacts provided

6. SECURITY & COMPLIANCE CONTEXT
   - Note security-relevant behavior (permission checks, audit events) contextually where the behavior is described
   - Don't create separate compliance subsections unless the feature directly touches access control or classification

7. STATES THAT MATTER
   - Document states that are non-obvious or carry design decisions
   - Don't enumerate loading/empty/error/success for standard CRUD operations
   - Focus on: What states would surprise an engineer? What states have specific design decisions?

TEMPLATE ADHERENCE:
- Follow the template structure but skip sections marked INCLUDE WHEN NEEDED if they add no value
- Match the writing style: prose and bullets for behavior, tables only when they genuinely aid scanning

WRITING VOICE:
- Technical but clear, imperative/declarative
- Describe behavior and outcomes, not click-by-click procedures
- Specific to this feature (reference feature name, exact component names from Figma)

### Design System Terminology

When writing spec sections that describe UI:
- Use exact Compass component names: "Button (Type=Primary)", "Toast Banner (Type=Success)", "Channel Sidebar Item"
- Use exact Compass pattern names: "Message pattern", "Console Settings Page pattern", "Modals pattern"
- Reference component variant axes: "State=Default → State=Hover on mouseover"
- Reference Compass Foundations tokens: "Uses sidebar-bg token for background", "Elevation 4 shadow"
- DO NOT use generic descriptions like "a popup menu" — say "Popover Menu pattern"
- DO NOT use hex colors — reference token names
- DO NOT describe component anatomy — reference the Compass pattern's documented anatomy

Compass reference: your design system's component reference.

OUTPUT FORMAT:
- Markdown formatted, ready to paste into the spec document
- Reference mockups for visual details rather than describing them in text
- Include [TBD] flags for uncertain details with reason notes
```

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "section_number": {
      "type": "string",
      "description": "Section number and title identifier",
      "example": "3.2"
    },
    "section_name": {
      "type": "string",
      "description": "Full human-readable section name",
      "example": "Settings Behavior"
    },
    "template_structure": {
      "type": "string",
      "description": "The template for this section type. Use as a guide, not a rigid structure."
    },
    "context": {
      "type": "object",
      "properties": {
        "prd_excerpts": {
          "type": "string",
          "description": "Relevant requirements from the PRD that this section must satisfy."
        },
        "design_decisions": {
          "type": "string",
          "description": "Key design decisions that shaped this section."
        },
        "figma_descriptions": {
          "type": "string",
          "description": "Description of the Figma design for this section."
        },
        "edge_cases_identified": {
          "type": "string",
          "description": "Non-obvious edge cases that must be covered."
        }
      },
      "required": ["prd_excerpts", "design_decisions", "figma_descriptions"]
    },
    "example_sections": {
      "type": "string",
      "description": "Example sections from a completed spec to calibrate tone and detail level."
    }
  },
  "required": ["section_number", "section_name", "template_structure", "context"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "section_markdown": {
      "type": "string",
      "description": "Complete markdown text of the written section, ready to paste into the spec document."
    },
    "tbds_flagged": {
      "type": "array",
      "description": "List of [TBD] flags included in the section",
      "items": {
        "type": "object",
        "properties": {
          "location": {"type": "string"},
          "reason": {"type": "string"},
          "source_to_clarify": {"type": "string"}
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
  "section_number": "3",
  "section_name": "Admin / Configuration UX",
  "template_structure": "## 3. Admin / Configuration UX\n\n### 3.1 System Console Settings\n[Describe settings]\n\n### 3.2 Channel-Level Settings\n[If applicable]",
  "context": {
    "prd_excerpts": "FR-1: System Admin can enable managed categories via System Console toggle. FR-2: When enabled, Channel Admins see a 'Managed category' dropdown in Channel Settings.",
    "design_decisions": "Decision: Use existing System Console toggle pattern. Channel-level dropdown uses standard searchable select component from design system.",
    "figma_descriptions": "System Console: Toggle labeled 'Enable Managed Channel Categories' under Experimental > Features. Channel Settings: New dropdown field below existing fields in Info tab."
  },
  "example_sections": "## 3. Admin / Configuration UX\n\n### System Console\n\nA new toggle, \"Enable Managed Channel Categories,\" appears in **System Console > Experimental > Features**. Default: off.\n\nWhen enabled, Channel Admins see a \"Managed category\" input in the Channel Settings modal (Info tab). When disabled, the input is hidden and any existing category assignments are preserved but not displayed.\n\n### Channel Settings\n\nIf this feature is enabled, a \"Managed category\" input field appears in the Info tab of the Channel Settings modal. The dropdown lists all managed categories that the channel admin has visibility of. Selection is optional — channels don't require a category assignment."
}
```

**Output:**
```json
{
  "section_markdown": "## 3. Admin / Configuration UX\n\n### System Console\n\nA new toggle, \"Enable Managed Channel Categories,\" appears in **System Console > Experimental > Features**. Default: off.\n\nWhen enabled, Channel Admins see a \"Managed category\" input in the Channel Settings modal (Info tab). When disabled, the input is hidden and any existing category assignments are preserved but not displayed.\n\n### Channel Settings\n\nIf this feature is enabled, a \"Managed category\" input field appears in the Info tab of the Channel Settings modal. The dropdown lists all managed categories that the channel admin has visibility of. Selection is optional — channels don't require a category assignment.\n\nThe dropdown is a standard searchable select. Typing filters the list. [TBD: empty-state behavior when the channel admin has visibility of zero managed categories — not specified in the supplied design decisions or Figma description] [TBD: whether this dropdown surfaces any category-management affordance — not specified in the supplied artifacts]",
  "tbds_flagged": [
    {
      "location": "Section 3, Channel Settings — dropdown empty state",
      "reason": "No empty-state behavior was specified in figma_descriptions or design_decisions for when the channel admin has zero managed categories to choose from.",
      "source_to_clarify": "Figma frame for the empty-category-list state, or an explicit design decision"
    },
    {
      "location": "Section 3, Channel Settings — dropdown affordances",
      "reason": "No supplied artifact mentions a category-management link or any admin-only affordance inside this dropdown; do not assume one exists.",
      "source_to_clarify": "figma_descriptions or design_decisions — confirm whether this affordance is in scope"
    }
  ]
}
```

## Validation Rules

1. **Decision focus**: Every paragraph should carry a decision, constraint, or non-obvious behavior. If a paragraph only describes standard behavior, cut it.

2. **Mockup references**: Reference Figma frames for visual details rather than describing layout in text.

3. **No vague language**: Eliminate "may", "could", "should consider", "might", "typically". Use "will", "does", "must", "does not".

4. **TBD justification**: Any [TBD] flag must have a reason and indicate where to source clarification.

5. **Mobile noted once**: State mobile parity or differences in a single place, not per-behavior.

6. **Requirements addressed**: PRD requirements mentioned in context must be addressed in this section or noted as covered elsewhere.

## Related Skills

- **Flow Auditor**: Audits flows before spec writing; output flows inform section content
- **Edge Case Hunter**: Adversarial review of completed sections for non-obvious gaps
- **Traceability Checker**: Verifies PRD requirement coverage across sections
- **Feedback Synthesizer**: Categorizes review feedback into revision requirements

## Notes for DoD/Defense Context

This skill applies heightened scrutiny to sections covering:
- **Authentication & authorization**: Permission checks noted contextually where behavior is described
- **Audit logging**: Note when actions create audit entries, but don't create separate audit subsections
- **Data sensitivity**: Information barriers and access checks noted in the flow where they apply
- **Compliance**: Reference compliance controls only when they drove a specific design decision

---

**Last Updated**: 2026-04-10
**Maintainer**: Mattermost Design Team
