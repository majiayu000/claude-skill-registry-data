---
name: ztx-responsive-rtl
description: Responsive Persian RTL and LTR. Invoke for precise implementation, responsive states, tests and integration into existing code; part of the Perfect_AI OMEGA no-MCP Codex skill collection.
---
# Responsive Persian RTL and LTR

## When to invoke
Use for tasks involving **responsive persian rtl and ltr**, especially when user requests production-grade Persian/English UI, complex motion, 3D, mobile design, color selection or code review. This skill is authored locally, not third-party code.

## Mandatory implementation procedure
1. Inspect current routes/HTML/CSS/TS, component ownership, dependencies and existing tests. Preserve working behavior; write an inventory of affected files.
2. Read `../perfect-ai-master/references/45-i18n-rtl-localization-architecture.md` in this installed pack. For complex projects also read `22-responsive-engineering-foundations.md`, `36-advanced-color-science.md` and `50-skill-composition-knowledge-routing.md` **as relevant**, not all 50 modules blindly.
3. Translate requirements into explicit semantic DOM, state machine, responsive layout, animation stages, or GPU scene data. Identify *what works without JavaScript or WebGL*.
4. Implement real working code, minimal dependencies, error handling and cleanup. Choose exactly one motion owner for each CSS/Three property; ensure RTL direction and accessible actions.
5. Open `../perfect-ai-master/patterns/responsive/page-shell.md` if available; otherwise `skills/perfect-ai-master/patterns/responsive/page-shell.md` from pack root. Apply the component CSS only where appropriate.
6. Define motion/input/readability fallback for 320px narrow, 400% zoom, no hover, reduced motion, failed network/GPU and short landscape viewport. Test scenarios that materially apply.
7. Run syntax/typecheck/build and real browser tests if available. Distinguish passing tests from things only specified. Do not claim proprietary reference website source was extracted.

## Concrete engineering rules
- Layout: intrinsic CSS Grid/Flex, `minmax(0,1fr)`, `min-width:0`, logical properties; named container queries when child allocated size controls layout.
- Type and color: semantic tokens; `clamp()` without fixed-zoom lock; choose OKLCH scientifically and audit WCAG contrast; user-requested monochrome outranks auto colors.
- Motion: deterministic progress, reversibility, cleanup, reduced-motion static state and no accidental transform conflicts. Camera/geometry truly 3D if claimed.
- Interactive elements: visible focus, keyboard activation, touch target, loading/error/empty outcome; no placeholder CTA with no action.
- Performance: dynamic imports for heavy runtimes, image aspect ratios, no offscreen infinite rAF, GPU quality tier and resource disposal.

## Output contract
Produce implementation files with comments at non-obvious boundaries; tests for target capability; concise report of changed files, responsive matrix exercised, actual diagnostics and known limitations. Perfect_AI default is intentional monochrome.

## References
- Local master: `skills/perfect-ai-master/references/45-i18n-rtl-localization-architecture.md`.
- VibeFarsi local catalog (279 original specs retained): `skills/perfect-ai-master/registry/` (fetch upstream via CLI only with user's permission, no MCP).
- Reference APIs are linked in master guide; verify versions, avoid blind copying code from external sites.
