---
name: kpa-find-design-inconsistencies
description: Find 5 component design inconsistencies - divergent UI patterns, APIs, or conventions
context: fork
agent: Sonnet
metadata:
  author: kpa
  updated-date: "2026-03-19"
---

Find 5 component design inconsistencies across the codebase — places where similar UI patterns, component APIs, or design conventions diverge without good reason.

## Steps

1. Systematically scan components for inconsistencies in the categories below.
2. For each item found, report:
   - **Category**: Which category from the list below
   - **Location**: File paths and line numbers of the inconsistent examples
   - **Description**: What the inconsistency is, showing the divergent approaches
   - **Recommendation**: Which pattern to standardize on and why

## Categories to Check

### Component API Patterns
- Props that mean the same thing but are named differently across components (e.g., `isLoading` vs `loading` vs `isDisabled` vs `disabled`)
- Inconsistent use of boolean prop conventions (e.g., `show` vs `isVisible` vs `visible` vs `open`)
- Similar components that accept children vs render props vs specific content props for the same purpose
- Callback props with inconsistent naming (e.g., `onClick` vs `onPress` vs `handleClick` vs `onSelect`)
- Inconsistent patterns for optional vs required props across similar components

### Layout & Spacing
- Components that solve the same layout problem with different approaches (e.g., flexbox vs grid vs absolute positioning)
- Inconsistent spacing values — similar UI elements using different margin/padding values where they should match
- Mixed use of Tailwind spacing scale (e.g., `p-3` in one place, `p-4` in an equivalent context)
- Container width or max-width patterns that vary without reason

### State Management Patterns
- Similar components that manage loading/error/empty states differently
- Inconsistent patterns for where state lives (parent vs child, context vs prop drilling)
- Mixed approaches to form state (controlled vs uncontrolled) within similar components
- Different error handling or fallback UI patterns for equivalent situations

### Visual Design Tokens
- Inconsistent color usage for similar semantic purposes (e.g., different grays for borders, different blues for links)
- Typography inconsistencies — similar text elements using different sizes, weights, or font classes
- Border radius values that vary across components that should look consistent
- Shadow, opacity, or transition values that differ for no clear reason

### Component Structure
- Similar features built as single monolithic components in one place but properly decomposed in another
- Inconsistent file organization — some components colocate helpers/types/hooks while others split them out
- Mixed patterns for client vs server component boundaries in equivalent situations
- Wrapper/container components that duplicate logic instead of sharing a common abstraction

### Interaction Patterns
- Inconsistent hover, focus, or active states across interactive elements
- Different approaches to showing tooltips, popovers, or contextual information
- Mixed patterns for confirmation dialogs or destructive action handling
- Inconsistent keyboard navigation or accessibility patterns across similar components

## Notes

- Focus on genuine inconsistencies — places where the same intent is expressed differently without justification.
- Do NOT flag intentional variation (e.g., a modal being different from a dropdown is expected).
- Prioritize inconsistencies that affect user experience or developer ergonomics.
- When recommending which pattern to standardize on, prefer the approach that is more prevalent, more idiomatic for the framework, or simpler.
- Do NOT fix the issues, only report them.
