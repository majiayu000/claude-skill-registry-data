---
name: check-design-system
description: Audit a Studio UI, prototype or system preview against its applicable design system.
---

1. Resolve the surface. Studio UI uses neutral Nuxt UI, [UI copy](../../context/ui-copy.md) and [Stack](../../context/stack.md). For a prototype run studio context and read its assigned system; explicit no-system work follows its supplied brief.
2. Inspect source and capture rendered evidence for relevant states and viewport sizes; the studio renders previews light only. Check component use, tokens, spacing, interaction, copy, accessibility and preview isolation.
3. Run `yarn check` and the applicable lint, typecheck, tests and build checks; consult [Verification](../../context/checks.md). Record findings with stable IDs, severity, file location, evidence and the governing rule.
4. Report findings for human review before applying fixes. Completion means every inspected surface and limitation is recorded; passing tools alone do not prove visual fidelity.
