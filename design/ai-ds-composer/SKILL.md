---
name: ai-ds-composer
version: 1.0.0
description: Strategic guide for consuming design system metadata to compose components intelligently. Use when generating or modifying UI components and layouts to ensure component reuse, proper variant selection, and adherence to design system patterns. Helps Claude understand project structure, read hierarchical metadata indexes, apply anti-pattern rules, and flag when existing components don't fit a requirement.
---

# Design System Component Reasoning

Your role is to help generate UI using existing design system components—not to invent new code. This skill teaches you to reason through design system metadata hierarchically and make component decisions that prioritize reuse.

## Core Principle

**Consume metadata → Understand intent → Select components → Compose patterns → Flag gaps**

Success means high component reuse with intentional, justified decisions.

## Getting Started: Understanding the Project

When you encounter a design system request, your first step is understanding the project structure. Read the available documentation:

1. **Top-level system metadata** - Usually in `src/` or project root, shows framework decisions, philosophies, and metadata hierarchy
2. **Package.json** - Reveals framework (Astro, Next.js, etc.), dependencies (React, Vue), styling approach, icon library
3. **CSS metadata** (if exists) - How the project structures styling: tokens, utilities, layout patterns

If none of these exist, infer from folder structure and ask the user for clarity. The project stack directly influences which components to suggest (Astro components ≠ React patterns).

### Example Metadata Hierarchy

```
project-root/
├── src/
│   ├── design-system.metadata.ts (top-level: project philosophy)
│   ├── styles/
│   │   └── index.metadata.ts (CSS architecture, token structure)
│   └── components/
│       ├── atoms/
│       │   ├── index.metadata.ts (all atoms, selection guide, priorities)
│       │   ├── Button/
│       │   │   ├── Button.astro (actual component)
│       │   │   └── Button.metadata.ts (variants, props, use cases)
│       │   ├── Heading/
│       │   │   ├── Heading.astro
│       │   │   └── Heading.metadata.ts
│       │   └── ... (other atoms)
│       ├── molecules/
│       │   ├── index.metadata.ts (compositions, common patterns)
│       │   └── ... (cards, form elements, etc.)
│       └── organisms/
│           ├── index.metadata.ts
│           └── ... (hero, sections, etc.)
```

When working with a project, you'll read metadata at multiple levels—start broad, narrow down to specific.

## The Component Selection Algorithm

When you need to suggest a component, follow this flow:

### 1. Parse the User's Intent

Convert vague requests into clear requirements:

**Vague:** "Add a button like the one on the homepage"
**Clear:** "Need a primary call-to-action button matching the hero section style, size=lg, with an arrow icon"

Tools for clarity: Ask follow-up questions, reference existing usage, look for patterns in the codebase.

### 2. Consult the Metadata Hierarchy (Hybrid Approach)

**First pass (cache once per conversation):**
- Read `design-system.metadata.ts` (or infer from structure)
- Understand project philosophies: "Prefer native HTML" vs "Use components"
- Note the metadata organization

**Subsequent passes (per component decision):**
- Read the appropriate layer index (`atoms/index.metadata.ts` etc.)
- Scan the `SelectionGuide` for your use case
- Pull the specific component metadata

**Example workflow for "I need a button":**
```
1. Cache: Read design-system.metadata → learn "prefer CSS over Spacer, components for interactivity"
2. Lookup: Check atoms/index.metadata → Button is high priority, use cases include "primary-call-to-action"
3. Read: Pull Button.metadata.ts → find variant options (primary/secondary/ghost/danger)
4. Decide: Based on intent, suggest variant + props
5. Verify: Check antiPatterns in Button.metadata → "Never use Button for plain navigation"
```

### 3. Apply Selection Criteria

Component metadata contains `selectionCriteria` or `SelectionGuide`. Use these to justify your choice:

```typescript
// From Button.metadata.ts - these are decision rules
selectionCriteria: {
  usePrimary: "Main action user should take on the page/section",
  useSecondary: "Alternative actions, cancel buttons",
  useGhost: "Tertiary actions, minimal visual weight",
  useDanger: "Delete, remove, destructive actions"
}
```

Match user intent to these criteria, not your intuition.

### 4. Check Anti-Patterns (Hard Rules)

Anti-patterns are violations of design system philosophy. They exist in metadata as warnings.

**From Button metadata:**
```
antiPattern: "Using button for plain navigation"
reason: "Buttons indicate actions, not navigation"
alternative: "Use Link component for navigation"
```

**Core rule:** Never suggest an anti-pattern without explicit user override and human acknowledgment. If the user says "I know, but I need it anyway," that's a decision they own—but flag it clearly.

### 5. Suggest Composition & Variants

Once you've selected the component, determine:

- **Which component?** (e.g., `Button`)
- **Which variant?** (e.g., `variant="primary"`)
- **What props?** (e.g., `size="lg"`, `disabled={false}`)
- **How composed?** (e.g., Button with Icon inside, following composition rules from metadata)
- **Why this choice?** (cite the metadata criterion that led here)

### 6. Explain Your Reasoning

Always show your thinking by referencing metadata:

**Good:**
> "You need a primary call-to-action. Button metadata shows `variant="primary"` is used for 'main call-to-action, high visual prominence.' Size should be `lg` for hero sections, following the composition pattern shown in `selectionGuide.actions`."

**Avoid:**
> "You need a button. I'll use primary variant because it looks good."

## When Components Don't Fit

If the user's request doesn't map to existing components, **flag it explicitly**:

1. **Identify the gap:** "You need X, but the design system has Y. These don't align because..."
2. **Explain why:** Reference what exists and why it doesn't work
3. **Don't auto-generate:** Don't invent a new component. Instead:
   - Suggest a workaround (compose existing components differently)
   - Explain the implication (e.g., "This would require custom CSS")
   - Let the human decide if it warrants a new component

**Example:**
> "Your use case needs a collapsible accordion with nested groups. The design system has no Accordion component. You could:
> - Compose with existing Button + disclosure patterns (simpler, limits nesting)
> - Create a new Accordion component (more work, but more flexible)
> 
> Which approach works for your requirement?"

## Handling Vague Metadata Hints

Metadata includes AI-specific fields like `aiHints` and `keywords`. Use these as starting points, but rely on structured fields (`props`, `variants`, `selectionCriteria`, `antiPatterns`) for real decisions.

```typescript
// Structured - use this for decisions
variants: { 
  variant: { options: ["primary", "secondary"], default: "primary" }
}

// Helpful but secondary - use for exploration
aiHints: { 
  keywords: ["button", "cta", "submit"]
}
```

## CSS vs Components Decision

Your project likely emphasizes "use native HTML + CSS utilities" when possible, reserving components for complex interactive patterns.

**Pattern from atoms/index.metadata.ts:**
```
preferNativeHTML: "Use native <h1>-<h6> instead of Heading when possible"
preferCSS: "Use CSS gap in flex/grid instead of Spacer"
```

Apply this philosophy:
- **Layout problem?** Suggest CSS utilities (grid, flexbox, gap)
- **Spacing issue?** Suggest margin/padding utilities, not Spacer component
- **Simple text?** Suggest native `<p>`, not Text component
- **Complex interaction?** That's when components shine

## Output Format

When suggesting components, structure your response as:

```
**Component:** Button
**Variant:** primary
**Size:** lg
**Props:** { href: "/features", target: "_blank", rel: "noopener noreferrer" }

**Composition:**
<Button variant="primary" size="lg" href="/features">
  Get Started
  <Icon name="ArrowRight" size={16} />
</Button>

**Why this choice:**
- Selection criteria (from Button.metadata): "Use primary for main call-to-action"
- Pattern reference: Similar to homepage hero button in ThoughtsSection
- Variant logic: lg size for hero context (from size guide)

**Notes:**
- Icon added following Button composition pattern
- External link uses rel="noopener noreferrer" (security best practice)
```

## Working with Reference Files

When the SKILL.md body isn't enough, see the bundled references:

- **COMPONENT_SELECTION.md** - Detailed component selection examples across different project types
- **METADATA_STRUCTURE.md** - How to read and interpret different metadata formats
- **COMPOSITION_PATTERNS.md** - Common component compositions and pattern rules
- **ANTI_PATTERNS.md** - Full anti-pattern reference with explanations

Load these when you encounter complexity or need validation.

## Key Reminders

1. **Metadata is authority** - Your suggestions should always map back to documented metadata, not assumptions
2. **Prefer reuse** - Composing existing components > generating new code (every time)
3. **Make trade-offs explicit** - If you're choosing component A over B, explain why
4. **Flag gaps early** - The human decides if a gap warrants a new component; you identify it
5. **Respect anti-patterns** - They exist for reasons in the metadata; violations need explicit override
6. **Cite your sources** - Reference which metadata file informed your decision

---

## Next Steps

When ready to apply this skill:

1. Understand the project structure (folder layout, package.json, top-level metadata)
2. Parse the user's intent clearly
3. Navigate the metadata hierarchy
4. Apply selection criteria and check anti-patterns
5. Suggest components with reasoning
6. Flag gaps without auto-generating
7. Iterate based on feedback

The goal isn't perfect UI from the first prompt—it's intelligent component reuse with clear, justifiable decisions.
