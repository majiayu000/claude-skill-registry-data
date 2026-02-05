---
name: atomic-design-planning
description: Use this skill when discussing UI components, design systems, frontend implementation, or component architecture. Guides thinking about Atomic Design methodology - atoms, molecules, organisms - and promotes component reuse over creation. Triggers on UI/frontend discussions, "what components do we need?", "should I create a new component?", or design system questions.
---

# Atomic Design Planning Skill

This skill guides UI component architecture using Atomic Design methodology, emphasizing reuse of existing components and proper categorization of new ones.

## When to Use

Apply this skill when:
- Planning UI features or components
- Deciding whether to create new components
- Discussing frontend architecture
- Users ask "what components do we need?"
- Reviewing UI implementation plans

## Atomic Design Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│  PAGES         - Complete screens with real content     │
├─────────────────────────────────────────────────────────┤
│  TEMPLATES     - Page-level layout structures           │
├─────────────────────────────────────────────────────────┤
│  ORGANISMS     - Complex UI sections (Header, LoginForm)│
├─────────────────────────────────────────────────────────┤
│  MOLECULES     - Simple groups (SearchInput, NavItem)   │
├─────────────────────────────────────────────────────────┤
│  ATOMS         - Basic blocks (Button, Input, Icon)     │
└─────────────────────────────────────────────────────────┘
```

## Component Categories

### Atoms
Smallest, indivisible UI elements: Buttons, Inputs, Labels, Icons.
- No dependencies, highly reusable, controlled by props only

### Molecules
Simple combinations of 2-4 atoms: SearchInput, FormField, NavItem.
- Single responsibility, reusable in multiple organisms

### Organisms
Complex, distinct UI sections: Header, ProductCard, LoginForm.
- May connect to data/state, often feature-specific

## The Reuse-First Principle

Before creating ANY component:
1. **Search existing atoms** - Is there a Button/Input that works?
2. **Search existing molecules** - Can a FormField be adapted?
3. **Search existing organisms** - Does a similar Card exist?
4. **Only then create new** - Is this truly unique?

## Decision Table

| Question | If Yes | If No |
|----------|--------|-------|
| Does something similar exist? | Reuse/extend it | Continue evaluation |
| Will this be used in 2+ places? | Consider extracting | Inline it instead |
| Is it truly indivisible? | Make it an atom | Make it a molecule+ |

## Integration with Jira Workflow

When planning UI features, create Subtasks for:
1. **Atom Subtasks** - New basic components needed
2. **Molecule Subtasks** - New component combinations
3. **Organism Subtasks** - New feature-level components

Investigation phase should identify existing components to reuse.

Remember: **Reuse existing components. Only create what's truly missing.**
