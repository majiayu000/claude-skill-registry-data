---
name: claude-design-playbook
description: "Use when the user wants Claude Design or `DESIGN.md` workflow help: pick an aesthetic family, derive a `DESIGN.md` from a live brand or screenshots, audit a site against a target `DESIGN.md`, or remix two design systems into one coherent third system."
metadata:
  short-description: Claude Design and DESIGN.md workflows
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/claude-design-playbook/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/claude-design-playbook/SKILL.md`
> Source of truth: `registry/skills/claude-design-playbook/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Claude Design Playbook

Use this skill when the user is working in the **Claude Design** workflow and needs help choosing, authoring, auditing, or remixing a `DESIGN.md`.

This is not a general frontend design skill.
If the user mainly wants implementation, styling, or broad UI critique without a `DESIGN.md` workflow, hand off to `frontend-design`.

## Use this skill for

- Pick one Claude Design family before generating a system
- Turn a live site or screenshot set into a structured `DESIGN.md`
- Audit a site against an existing or proposed `DESIGN.md`
- Remix two design systems into one coherent third system

## Do not use this skill for

- Generic "make this page prettier" requests
- Building production UI code
- Broad anti-slop frontend advice with no Claude Design tie-in
- General visual critique not grounded in a target system

## Workflow

### 1. Pick the route

Choose exactly one route first:

- `family-picker`
- `brand-to-design-md`
- `audit-live-site-against-design-md`
- `remix-two-brands`

Do not mix routes unless the user explicitly asks for a chained workflow.

### 2. Load the minimal references

- Read [references/families.md](references/families.md) for family selection and examples.
- Read [references/prompt-packs.md](references/prompt-packs.md) for route-specific prompt structure.
- Read [references/design-md-structure.md](references/design-md-structure.md) whenever a `DESIGN.md` must be produced or evaluated.
- Read [references/workflow-notes.md](references/workflow-notes.md) for chaining and handoff notes.

### 3. Route instructions

#### `family-picker`

- Ask the minimum questions needed to classify the product surface, audience, and desired level of courage versus familiarity.
- Force one recommendation.
- Provide one alternative and one family to avoid.
- Finish by pointing to a concrete family reference and the next Claude Design step.

#### `brand-to-design-md`

- Work from a live URL, screenshots, or a supplied design system artifact.
- Only claim tokens and behaviors that can be verified from rendered output.
- Produce a nine-section `DESIGN.md` using the canonical structure in [references/design-md-structure.md](references/design-md-structure.md).
- Mark unknown font identities or unverified motion rules as `unknown`.

#### `audit-live-site-against-design-md`

- Compare the rendered site against the target system, not against your preferences.
- Score hierarchy, spacing, color, accessibility, motion, and copy only when evidence is visible.
- End with an ordered punch list that can be fed back into Claude Design.

#### `remix-two-brands`

- Pick one system for typography and one accent family.
- Prefer the stricter spacing scale and the more restrained depth model.
- State which parent contributes each major token family and why.
- The result must read like a third system, not a stitched blend.

### 4. Keep `DESIGN.md` outputs compact and verified

- Use the canonical nine sections only.
- Prefer role-based token names over poetic brand labels.
- Keep guidance operational for coding agents.
- Reject vague adjectives that do not change implementation.

### 5. Handoff when the user wants implementation

If the user now wants HTML, React, CSS, or a full frontend artifact:

- keep the chosen family or generated `DESIGN.md`
- summarize the system in a few implementation-ready constraints
- hand off to `frontend-design`

Do not try to replace `frontend-design` with this skill.

## Anti-slop bridge

When the user asks how to avoid generic AI UI during the Claude Design workflow:

- keep the answer tied to the selected family or target `DESIGN.md`
- point to Anthropic's frontend aesthetics cookbook for broader prompting patterns
- point to `frontend-design` for implementation-phase aesthetic direction

This skill should not become a duplicate anti-slop doctrine.

## Reference loading guide

- Start with [references/prompt-packs.md](references/prompt-packs.md) for route behavior.
- Load [references/families.md](references/families.md) when a family decision or example is needed.
- Load [references/design-md-structure.md](references/design-md-structure.md) whenever emitting or auditing a `DESIGN.md`.
- Load [references/workflow-notes.md](references/workflow-notes.md) only when chaining Claude Design outputs into audits, remixes, or implementation handoff.
- Use [references/provenance-manifest.json](references/provenance-manifest.json) when you need to verify where curated material came from.
