---
name: brand-guidelines
description: Use when applying, auditing, or documenting user-provided project brand assets, voice, tokens, typography, imagery, or visual rules for an artifact. Do not use for inventing a brand identity, copying another organization's brand, implementation, or publishing.
---

# Brand Guidelines

Apply the project's own approved identity consistently. Treat brand material as
project-local context, not a default style system or a prompt to invent one.

## Boundaries

- Use only brand rules, assets, and examples supplied by the user or already
  approved in the active project. Do not copy, infer, or recreate another
  organization’s identity, including Anthropic's colors, typography, or voice.
- Do not invent logos, palettes, type pairings, taglines, voice traits, customer
  claims, or identity rules when source material is absent. Report the gap and
  offer neutral, clearly labelled options only if requested.
- Do not access external brand portals, private drives, personal accounts, or
  external directories without explicit approval and applicable permissions.
- Do not edit source files, generate assets, install fonts, start renderers,
  perform visual QA, or publish without explicit approval.
- Preserve legal notices, licensing constraints, accessibility requirements, and
  supplied usage restrictions. Flag conflicting rules rather than resolving them
  by preference.

## Workflow

### 1. Inventory the approved source material

Identify the artifact, audience, channel, and available project-local inputs:
logos, color tokens, typography, spacing, imagery, icons, voice, terminology,
examples, accessibility requirements, and legal or co-branding constraints.

Record the source path or user-provided origin, scope, status, and uncertainty
for each rule. Separate a documented rule from an inference based on a sample.

### 2. Reconcile and scope the rules

Resolve only rules that are explicitly compatible. When sources conflict, state
the conflict, affected artifact, and decision owner. When a needed rule is
missing, explain the effect and ask the smallest question that can unblock the
artifact.

Choose the minimum applicable rules for the requested artifact. Do not turn a
single campaign example into a global brand rule or use visual consistency to
override usability, readable contrast, semantic structure, or platform policy.

### 3. Produce a brand application brief

Describe how the approved system applies to the artifact:

- Required and prohibited logo, color, typography, imagery, and tone use.
- Exact project token or asset references where they exist; never guess values.
- Content terminology, required disclosures, and approved claims.
- Accessibility constraints: contrast, text sizing, non-color cues, alt text,
  and motion as relevant.
- Channel-specific constraints and a list of decisions requiring approval.

For visual or content work, hand the brief to `frontend-design`,
`ui-design-system`, or `social-content` as appropriate. `frontend-design` owns
page-specific UI planning and `ui-design-system` owns reusable system rules;
neither may override the supplied brand system.

### 4. Request approval before persistence or production

If the user wants a durable brand document, generated assets, or implementation,
propose the exact project-local path, artifact type, inputs, and validation
method. Wait for approval before creating or changing files, rendering, or
running checks.

## Brand application brief

```markdown
## Artifact and Audience

## Approved Sources and Scope

## Required Rules

## Prohibited or Restricted Use

## Accessibility and Channel Constraints

## Conflicts, Gaps, and Assumptions

## Handoff and Required Approval
```

Stop at the brief unless the user explicitly approves a project-local artifact
or implementation workflow.
