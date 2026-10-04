---
name: componentize
description: "Use to extract a page, section, or prototype into reusable components, to pull repeated UI into one component, or to split a large UI file into focused modules. Structure only. Not for visual changes."
---

# Componentize

Turn a draft or a big page into small components with sensible APIs, without changing how anything looks.

## Steps

1. Look at how the project already does components before making new ones.
2. Find repeated patterns, logical sections, and self-contained blocks.
3. Extract components. Spacing at the call site, a merged class prop on every one.
4. Reuse or extend existing project components wherever one fits.
5. Scan the extracted components for duplication and extract again.
6. Run the project's format, lint, typecheck, and tests, and confirm the UI and behavior didn't change.

## Rules

- Break the design into small, focused components. Repeated patterns, logical sections, and self-contained blocks each get their own. Never one giant component rendering everything.
- Never bake margins into a component. Margins go at the call site. Every component takes a `class` attribute and merges it into the classes on its top-level element.
- Use `clsx` or the project's equivalent to merge classes in client-side components.
- Form controls get reusable components organized by HTML element. One `Input` for every `<input>` type, one `Select`, one `Textarea`. Never `EmailInput` or `PasswordInput`. Check the project for existing ones first.
- Two or more elements with the same structure and styling that differ only in props, labels, placeholders, or types become one component parameterized by those props.
- After extracting, look for shared pieces across the new components and extract those too: section wrappers with the same max width and padding, heading groups with eyebrow plus heading plus subheading, card shells, button styles.
- Use existing project components whenever one exists, buttons and form elements especially. Extend rather than duplicate.
