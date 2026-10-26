---
name: new-component
description: Scaffold a new shared UI primitive in src/shared/ui — tokenized, accessible, dark-mode-ready, with a testID and a test. Use when the user wants to add a reusable UI element (button, card, sheet, badge, etc.) to the shared kit.
argument-hint: [ComponentName]
allowed-tools: Read, Write, Glob, Grep
---

## Task

Add `$ARGUMENTS` to the shared UI kit (`src/shared/ui`), matching the existing primitives EXACTLY.
This is the "lean core + generate on demand" model — only add what a feature actually needs.

1. **Read the contract first:** `docs/design/quality-bar.md`, `docs/conventions/design-system.md`,
   and an existing primitive (`src/shared/ui/button.tsx`, `text.tsx`) to copy the shape.
2. **Confirm the need.** If it's unclear which feature needs this or what variants/props it must
   support, ask before generating — don't pre-build unused surface.
3. **Create `src/shared/ui/<kebab-name>.tsx`:**
   - A function component; props typed and exported as `export type <Name>Props`.
   - Styling via NativeWind `className` + `cn()` — **role tokens only, never raw hex**.
   - Light/dark aware via the role tokens (no inverted hardcoded colors).
   - A `testID` passthrough; if interactive, ≥44pt touch target + accessibility role/label.
   - If animated, use Reanimated and respect reduced motion.
4. **Export** it from `src/shared/ui/index.ts` (keep the list alphabetical).
5. **Test:** add `src/shared/ui/__tests__/<kebab-name>.test.tsx` (renders; key prop/state behaviour;
   testID present).
6. **Self-check** against the boundaries + `no-restricted-imports` rules and the quality-bar checklist.

Return the files created + a one-line usage example.
