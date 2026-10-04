---
name: figma-ui-ux-consistency
description: |
  Orchestrates all 7 Figma MCP plugin skills into a unified, project-aware lifecycle for achieving
  and maintaining UI/UX consistency — from audit through design system creation, code
  implementation, and ongoing governance. Use when auditing visual consistency, establishing a new
  design system, reconciling Figma with an existing codebase, or building a component library from
  current screens. Works in 5 ordered phases: Audit (extract patterns), Foundations (define tokens),
  Library (build Figma components), Implement (translate to code), Governance (rules and review loops).
  Also for re-auditing after significant feature growth, onboarding new designers, or before major
  releases. Delegates canvas operations to plugin sub-skills; owns phase sequencing and checkpoints.
  Complements ui-ux-pro-max and frontend skills.
---

# Figma UI/UX Consistency — Orchestration Skill

A holistic orchestration skill that sequences the 7 Figma MCP plugin sub-skills into a
single, project-aware lifecycle for achieving and maintaining UI/UX consistency. This
skill owns the **what-to-do-when** logic. It delegates **how-to-do-it** to the
appropriate sub-skill.

**This skill does not call `use_figma` directly.** It composes the 7 plugin skills and
manages phase transitions, checkpoints, and project-specific adaptation.

**Companion skills (always load together):**
- `ui-ux-pro-max` — design system spec, token structure, component patterns
- `frontend` — implementation of design specs into code
- `superpowers-plan-design-review` — review design deliverables before implementation
- `superpowers-design-review` — visual audit of live implementations

---

## When Invoked

Use this skill when the user says or asks for:
- "audit the UI for consistency issues"
- "establish a design system for [project]"
- "fix the inconsistent styling across our app"
- "reconcile Figma with our codebase"
- "build a component library from our existing screens"
- "Figma-to-code governance workflow"
- Any request involving Figma + code consistency at a project or portfolio level

**Skill boundaries:**
- This skill orchestrates; it does not execute Figma canvas writes directly.
- For **creating** a design system in Figma: load `figma-generate-library`.
- For **writing** Figma screens from code: load `figma-generate-design`.
- For **reading** Figma and generating code: load `figma-implement-design`.
- For **connecting** Figma components to code: load `figma-code-connect-components`.
- For **authoring project rules**: load `figma-create-design-system-rules`.
- For **creating a new Figma file**: load `figma-create-new-file`.
- For any canvas write operation: load `figma-use` first (mandatory prerequisite).

---

## The 5-Phase Consistency Lifecycle

```
Phase 1: AUDIT       → Extract patterns, identify inconsistencies, document gaps
Phase 2: FOUNDATIONS → Define tokens, color semantics, typography scale, spacing
Phase 3: LIBRARY     → Build component library (via figma-generate-library)
Phase 4: IMPLEMENT   → Implement designs in code + connect components
Phase 5: GOVERNANCE  → Rules, review loops, change management
```

**Rule: Always execute phases in order.** Phase N+1 requires Phase N to be
complete and approved. Skipping phases creates cascading failures that are
expensive to undo.

---

## Phase 1 — UI Audit

**Goal:** Understand what exists, what is consistent, and what is broken.

### 1a. Determine Audit Scope

Ask the user:
1. Which Figma file(s) or URL(s) to audit?
2. Which codebase directory or repo to cross-reference?
3. Is this a new project (no existing design system) or an existing one?

If no Figma file exists yet, use `generate_figma_design` to capture the running
application into Figma first (web apps only), then audit the captured file.

### 1b. Extract Existing Patterns

Run `get_design_context` on key screens, then:
- Document the **component inventory**: list every distinct visual element by name
  (Button, Card, Modal, Badge, Input, NavItem, etc.)
- Document the **token inventory**: extract color values, spacing values, font sizes,
  border radii, shadow values as you encounter them
- Identify **duplicates**: same visual, different name or values
- Identify **variants**: same component family, inconsistent naming
- Identify **hardcoded values**: colors/spacing not using any token system

### 1c. Cross-Reference with Codebase

Read the project's existing design tokens or CSS variables. Document:
- Which Figma values match the code
- Which Figma values diverge from the code
- Which code values have no Figma equivalent (and vice versa)

### 1d. Produce the Audit Report

Present a structured report:

```markdown
## UI Audit Report — [Project Name]

### Consistent Patterns (Keep)
- [Component]: [what is working, e.g. "Buttons use --primary-500 consistently"]

### Inconsistencies to Fix (Priority Order)
1. **[Issue]**: [description, e.g. "5 different border-radius values used]
   - Seen in: [screens/components]
   - Proposed fix: [unified value]
2. ...

### Missing Design System Elements
- [ ] Token: no spacing scale defined
- [ ] Component: no shared Badge component, 3 ad-hoc versions exist
- ...

### Code ↔ Figma Divergences
| Element | Figma Value | Code Value | Recommended |
|---------|------------|------------|-------------|
| Button bg | #3B82F6 | #2563EB | [pick one] |

### Audit Summary
- Total components found: N
- Unique visual patterns: N
- Divergences code↔Figma: N
- Recommended: [new system / incremental fix / no DS needed]
```

**USER CHECKPOINT:** Present the audit report. Await explicit approval before
proceeding to Phase 2. If user says "skip audit" or "start from scratch," confirm
they understand the gaps that won't be caught, then proceed.

### Project-Specific Rules for Phase 1

**examplecrm** (brand: teal + amber, fonts: Playfair Display + Plus Jakarta Sans):
- Audit must document existing teal/amber usage as the brand anchor
- Any palette decisions must reference the teal + amber brand rule
- Typography audit must flag any non-brand font usage

---

## Phase 2 — Design System Foundations

**Goal:** Establish the token system that all components will consume.

### 2a. Confirm Brand / Style Anchor

Before creating any tokens, confirm:
- Brand colors (e.g., teal + amber for examplecrm)
- Brand typography (e.g., Playfair Display + Plus Jakarta Sans)
- Style direction (minimal, glass, editorial, data-dense — from ui-ux-pro-max)
- Motion tier (A/B/C from ui-ux-pro-max)

### 2b. Define Token Architecture

Produce a token spec covering all 4 foundations:

**Color:**
```
Primitive tokens:  blue/50 → blue/900, gray/50 → gray/900, white, black
Brand tokens:      teal/50 → teal/900, amber/50 → amber/900  [examplecrm]
Semantic tokens:   color/bg/primary, color/text/primary,
                    color/border/default, color/accent/primary
                    color/status/success, color/status/warning,
                    color/status/error, color/status/info
```

**Typography:**
```
Font families:     [heading: Playfair Display], [body: Plus Jakarta Sans]  [examplecrm]
Font sizes:        text/xs=12, text/sm=14, text/base=16, text/lg=18,
                    text/xl=20, text/2xl=24, text/3xl=30, text/4xl=36
Font weights:      font/regular=400, font/medium=500, font/semibold=600, font/bold=700
Line heights:      leading/tight=1.2, leading/normal=1.5, leading/relaxed=1.75
```

**Spacing:**
```
spacing/xs=4, spacing/sm=8, spacing/md=16, spacing/lg=24,
spacing/xl=32, spacing/2xl=48, spacing/3xl=64
```

**Radius / Shadow:**
```
radius/none=0, radius/sm=4, radius/md=8, radius/lg=12, radius/full=9999
shadow/sm, shadow/md, shadow/lg (effect style references)
```

### 2c. Write Foundations to Project Memory

Save the token spec to:
```
[project]/memory/design-system-foundations.md
```

This file becomes the anchor that both Figma and code reference. Update it before
touching Figma or code in later phases.

**USER CHECKPOINT:** Present the foundations spec. Await explicit approval before
creating anything in Figma.

### Phase 2 Anti-Patterns
- Creating tokens in Figma before writing the spec to project memory
- Defining semantic tokens that duplicate raw values instead of aliasing primitives
- Using `ALL_SCOPES` on any variable
- Skipping brand anchor confirmation (color, font, style)

---

## Phase 3 — Component Library Creation

**Goal:** Build the Figma component library from the foundations established in Phase 2.

**Load `figma-generate-library` and `figma-use` together for this phase.**
This skill provides the orchestration logic; those skills provide the Plugin API
execution logic.

### 3a. Run Discovery (figma-generate-library Phase 0)

- Analyze codebase — extract existing UI components and their prop API
- Inspect Figma file — existing pages, variables, components, styles
- Search subscribed libraries via `search_design_system`
- Lock v1 scope: agree on exact token set + component list

### 3b. Create Foundations in Figma (figma-generate-library Phase 1)

- Variable collections (Primitives → Semantic → Spacing)
- Effect styles and text styles
- **Always bind visual properties to variables** — no hardcoded fills/strokes

### 3c. Create File Structure (figma-generate-library Phase 2)

Standard page skeleton:
```
Cover → Getting Started → Foundations → --- → Components → --- → Utilities
```

### 3d. Build Components One at a Time (figma-generate-library Phase 3)

For each component (in dependency order — atoms before molecules):
1. Create dedicated page
2. Build base component with full variable bindings
3. Create variant combinations
4. Add component properties
5. Validate with `get_metadata` + `get_screenshot`
6. **USER CHECKPOINT per component**

**Component priority order for v1:**
```
1. Button        6. Badge          11. Modal/Dialog
2. Input         7. Avatar         12. Table
3. Select        8. Card           13. Pagination
4. Checkbox      9. Tag/Chip       14. Toast/Snackbar
5. Toggle        10. Dropdown      15. Tabs
```

### Phase 3 Anti-Patterns
- Building components before foundations (tokens) exist in Figma
- Hardcoding any fill/stroke/spacing/radius value
- Creating a variant per icon (use INSTANCE_SWAP instead)
- Batch-creating all components without user checkpoints
- Parallelizing `use_figma` calls (always sequential)

---

## Phase 4 — Implementation & Code Connection

**Goal:** Translate the Figma library into production code, and connect Figma
components to code components for bidirectional handoff.

### 4a. Implement Figma Designs in Code

**Load `figma-implement-design` for this step.**

For each screen/section:
1. Fetch `get_design_context` + `get_screenshot` from Figma
2. Download required assets from the Figma MCP assets endpoint
3. Map Figma design tokens → project design tokens
4. Reuse existing components where they match
5. Implement new components using project conventions
6. Validate visual parity against the Figma screenshot

**Translation rules:**
- Treat Figma output as design intent, not final code style
- Replace Tailwind utilities with project tokens
- Prefer project design system components over raw Figma translation
- Document deviations for accessibility or technical reasons

### 4b. Connect Figma to Code Components

**Load `figma-code-connect-components` for this step.**

After implementing a component in code:
1. Locate the corresponding Figma component node
2. Run `figma-code-connect-components` to create a Code Connect mapping file
3. Verify the mapping links the correct Figma component to the correct code component
4. Map all variant properties and states

### 4c. Create Project Figma-to-Code Rules

**Load `figma-create-design-system-rules` for this step.**

Generate project-specific rules that encode:
- Which design system conventions apply to this project
- Naming conventions for components, tokens, and variants
- When to prefer Figma vs. code as the source of truth
- How to handle conflicts between Figma and code

Output: `[project]/figma-design-system-rules.md`

### Phase 4 Anti-Patterns
- Implementing without fetching `get_design_context` first
- Hardcoding hex values instead of design tokens
- Creating duplicate components that already exist in the codebase
- Skipping Code Connect mappings (breaks bidirectional handoff)

---

## Phase 5 — Governance

**Goal:** Ensure consistency is maintained after the initial build.

### 5a. Establish Design Review Gate

Add a `superpowers-design-review` checkpoint to the team's definition of done:
- Any new screen or major UI change must be reviewed against the Figma source
- The review must validate: colors match tokens, spacing matches scale, typography
  matches the type ramp, no ad-hoc components created without design review

### 5b. Write Project-Specific Figma Rules

Generate `[project]/figma-design-system-rules.md` using `figma-create-design-system-rules`.

The rules file must capture:
- Project brand tokens (e.g., examplecrm teal + amber)
- Project font stack
- Allowed component inventory
- Naming conventions
- Forbidden patterns (ad-hoc components, hardcoded values)
- Conflict resolution: Figma wins for visual; code wins for behavior

### 5c. Set Up Ongoing Audit Triggers

Teach the team to re-run Phase 1 audit when:
- A new designer joins the project
- The product has undergone significant feature growth (>30% new screens)
- A user or stakeholder flags visual inconsistency
- Before a major release

### 5d. Track the State Ledger

For long-running or recurring consistency work:
- Maintain `[project]/memory/figma-consistency-state.json` tracking:
  - Last audit date
  - Components created in Figma (with IDs)
  - Token coverage (% of components using tokens vs. hardcoded)
  - Code↔Figma divergence log
- Re-read this file at the start of every session

### Phase 5 Anti-Patterns
- Changing design tokens in Figma without updating the project rules file
- Allowing "one-off" components without design review
- Skipping Code Connect on new components (starts the divergence cycle again)

---

## Project-Specific Adaptation

### examplecrm (Next.js 14 + FastAPI + Supabase, teal + amber, Playfair Display + Plus Jakarta Sans)

**Brand anchor — never override without explicit user approval:**
- Primary teal: `#0D9488` (Tailwind: `teal-600`) — brand anchor
- Accent amber: `#F59E0B` (Tailwind: `amber-500`) — brand accent
- Font heading: `Playfair Display` (Google Fonts)
- Font body: `Plus Jakarta Sans` (Google Fonts)

**Token naming convention for examplecrm:**
```
color/teal/[shade]    e.g., color/teal/600
color/amber/[shade]   e.g., color/amber/500
color/bg/primary      → teal-50 (light) / teal-900 (dark)
color/text/primary    → gray-900 (light) / gray-50 (dark)
color/accent          → amber-500
typography/font/heading → Playfair Display
typography/font/body    → Plus Jakarta Sans
```

**Forbidden for examplecrm:**
- Using blue/purple brand colors in primary UI
- Mixing Playfair Display into body text or Plus Jakarta Sans into headings
- Using teal-700+ for backgrounds (creates accessibility issues)
- Hardcoded teal/amber hex values (must use CSS variables from the brand token system)

### Other Projects

For ExampleApp:
- Detect brand colors, fonts, and style direction from the project's existing
  CLAUDE.md or PROJECT.md before Phase 2
- Apply the same 5-phase lifecycle with project-specific tokens

---

## Skill Orchestration Map

| If the user wants to... | Load this skill |
|---|---|
| Run the full consistency lifecycle | `figma-ui-ux-consistency` |
| Execute Phase 1 (audit) | `figma-ui-ux-consistency` + `figma-implement-design` (for get_design_context) |
| Execute Phase 2 (foundations spec) | `figma-ui-ux-consistency` + `ui-ux-pro-max` |
| Execute Phase 3 (build library in Figma) | `figma-ui-ux-consistency` + `figma-generate-library` + `figma-use` |
| Execute Phase 4 (implement in code) | `figma-implement-design` + `figma-code-connect-components` |
| Execute Phase 4 (write project rules) | `figma-create-design-system-rules` |
| Create a new Figma file | `figma-create-new-file` |
| Perform design review | `superpowers-design-review` |

---

## Key Rules

1. **Never call `use_figma` without loading `figma-use` first.**
2. **Never skip Phase 1 (audit).** Starting from scratch without knowing what's broken
   means fixing symptoms instead of root causes.
3. **Never skip user checkpoints.** Consistency work requires human judgment on visual
   priorities. Never build Phase N+1 without Phase N approval.
4. **Variables before components.** Tokens must exist in Figma before components bind to them.
5. **Code↔Figma conflicts: ask the user.** Never silently pick one. Document both options
   and their implications.
6. **Never parallelize `use_figma` calls.** Figma state mutations are sequential.
7. **Always validate after every Figma write.** Use `get_metadata` for structure,
   `get_screenshot` for visuals.
8. **Persist the state ledger.** For workflows spanning multiple sessions, write to disk
   (`/tmp/figma-consistency-{project}-{date}.json`) and re-read at session start.
9. **For examplecrm: never override the teal+amber brand anchor** without explicit user approval.
