---
name: atomic-design
description: >
  Atomic Design methodology for structuring React/Next.js component libraries.
  Defines five levels (atoms, molecules, organisms, templates, pages) with hard
  import rules, classification tests, and anti-patterns. Use when creating,
  reviewing, or restructuring frontend components.
tier: core
version: 0.1.0
kind: reference
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Atomic Design -- Frontend Component Architecture

Reference: Brad Frost, *Atomic Design* (https://atomicdesign.bradfrost.com/)

## Core Principle

Atomic Design is a mental model, not a linear process. You do not build atoms first, then molecules, then organisms. You think about the interface simultaneously as a cohesive whole and a collection of parts. Every component decision considers both its isolated purpose and its role in the larger system.

---

## The Five Levels

### 1. Atoms (`components/atoms/`)

The smallest, indivisible UI elements. They cannot be broken down further without losing their meaning.

**Examples:** Button, Input, Label, Badge, Avatar, Icon, Toggle, Divider, Skeleton, Spinner

**Rules:**
- Accept only generic, presentational props (size, variant, color, disabled)
- Never import other atoms -- they are leaf nodes
- Must work in complete isolation -- render one on a blank page and it must make visual sense
- Define variants via props, not separate components (`<Button variant="primary">` not `<PrimaryButton>`)
- No business logic, no domain knowledge, no data fetching

### 2. Molecules (`components/molecules/`)

Simple groups of atoms functioning together as a single unit with one clear purpose.

**Examples:** SearchField (Label + Input + Button), FormField (Label + Input + Error), ConfirmButton (Button + confirm state), RevealableSecret (EyeIcon + redacted text), Section (title + children container)

**Rules:**
- Import from `atoms/` only (rare exceptions for small utility molecules)
- Single responsibility: describe in one sentence without "and"
- Context-agnostic -- a SearchField works identically in header, sidebar, or modal
- Own simple interaction state (hover, focus, open/closed) but not application state
- If you cannot describe it without "and," it is an organism

### 3. Organisms (`components/organisms/`)

Complex, distinct sections of the interface composed of molecules, atoms, and potentially other organisms. They form recognizable, standalone regions of a page.

**Examples:** SiteHeader, DataTable, AuthProfileManager, JsonViewer, ConfigActions, ChatPanel, CommentThread, Sidebar

**Rules:**
- Can import atoms, molecules, and other organisms
- Represent a distinct section you can point at on the screen
- May accept data props but should not fetch data themselves
- Can have meaningful internal state (tabs, sort, accordion)
- Still reusable -- a DataTable can appear on multiple pages

**Molecule vs. organism test:** Groups items serving different purposes (navigation AND search AND user account) = organism. Groups items serving one purpose (search input + submit button) = molecule.

### 4. Templates (`components/templates/`)

Page-level layout components that arrange organisms into a structure. Define WHERE things go, not WHAT they contain.

**Examples:** DashboardLayout (Sidebar + Main + TopBar slots), SettingsLayout, AuthLayout

**Rules:**
- Use slots/children patterns -- accept organisms as props or children, not raw data
- Define responsive grid behavior
- Testable with skeleton content
- In Next.js: map to `layout.tsx` files or shared layout components
- Never hardcode specific organisms -- use composition

### 5. Pages (`app/` routes)

Specific instances of templates populated with real content and real data.

**Rules:**
- The ONLY level that fetches data
- Compose templates with organisms, passing real data down
- If real content breaks the layout, fix at the component level, not the page level
- Test edge cases: empty states, max-length content, errors, loading, role differences

---

## Directory Structure

```
src/
  components/
    atoms/           # Button, Input, Badge, Toggle, Spinner, EmptyState
    molecules/       # SearchField, FormField, ConfirmButton, Section, Row
    organisms/       # SiteHeader, DataTable, JsonViewer, ChatPanel
      agent/         # Agent-specific organisms
      instance/      # Instance-specific organisms
      settings/      # Settings organisms
    templates/       # DashboardLayout, AuthLayout
  app/               # Next.js pages (data fetching + composition)
  lib/
    hooks/           # Shared hooks (useClickOutside, useDebounce)
```

---

## Import Rules (Hard Constraints)

| From / To      | atoms | molecules | organisms | templates | pages |
|----------------|-------|-----------|-----------|-----------|-------|
| **atoms**      | NO    | NO        | NO        | NO        | NO    |
| **molecules**  | YES   | rare      | NO        | NO        | NO    |
| **organisms**  | YES   | YES       | YES       | NO        | NO    |
| **templates**  | NO    | NO        | YES       | NO        | NO    |
| **pages**      | rare  | rare      | YES       | YES       | NO    |

Dependencies flow downward only. Violations indicate misclassification.

---

## Anti-Patterns

### 1. Premature Abstraction
Do not create atoms/molecules for one-off components. Start concrete, extract when you see repetition. Three inline usages before extracting.

### 2. God Organisms
An organism containing half the page is misclassified. If it defines layout for the whole page, it is a template. Split if it does too many things.

### 3. Atoms with Business Logic
An atom that knows about user roles, pricing tiers, or feature flags is broken. Domain knowledge enters at the organism or page level via props.

### 4. Page-Level CSS Hacks
If a component needs custom styling on one page, add a variant prop to the component. Do not override from page-level CSS.

### 5. Skipping Templates
Jumping from organisms to pages leaks layout logic into page components. Always define page skeleton as a template.

### 6. Happy Path Only
Every component must handle: empty, error, loading, max-length, min-length, missing data, different roles, and disabled states.

### 7. Naming Drift
One pattern, one name, everywhere. If it is `SearchField` in the library, call it `SearchField` in code, design, conversation, and tickets. Never `SearchBar` / `SearchBox` / `SearchInput`.

---

## Component Creation Checklist

Before creating a new component:

1. **Level:** Which level? Apply the definitions strictly.
2. **Single responsibility:** One sentence without "and"?
3. **Existing patterns:** Similar component exists that could get a variant?
4. **Reusability:** Used in more than one place? If not, start inline and extract later.
5. **Import direction:** Only imports from lower levels?
6. **Edge cases:** Empty, loading, error, extreme content states handled?
7. **Naming:** Consistent with existing vocabulary?

---

## Maintenance

- The design system is a product with ongoing maintenance, not a one-time project.
- When modifying an atom, verify every molecule and organism that uses it.
- Deprecate gracefully with recommended alternatives before removing.
- Test with real content, not Lorem ipsum -- placeholder content hides layout bugs.
- The pattern library and production app use the same component code. One source of truth.

---

## Self-Check

Before applying this skill, verify:
- [ ] Project uses React or Next.js with a `components/` directory
- [ ] Project has enough components (10+) to benefit from structured classification
- [ ] Team has agreed to adopt component classification (do not impose unilaterally)
