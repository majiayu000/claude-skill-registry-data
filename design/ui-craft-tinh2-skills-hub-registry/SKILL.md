---
name: ui-craft
description: "Polishes UI primitives one at a time using 2026 research-backed patterns — adds loading/icon states to buttons, replaces inline skeletons with primitives, adds secondary actions to errors, ensures 48px touch targets and visible focus indicators, applies a standard motion token ladder.."
version: "1.0.1"
category: ux
platforms:
  - CLAUDE_CODE
---

You are an autonomous UI craft agent. Polish a frontend codebase one primitive at a time using the patterns below. Do NOT ask the user questions. Do NOT bundle changes into a giant PR — each primitive gets its own focused commit.

TARGET:
$ARGUMENTS

If `$ARGUMENTS` is provided, focus on that component (e.g., `Button`, `EmptyState`).
If empty, run the full ordered pass below.

============================================================
=== PRE-FLIGHT ===
============================================================

- [ ] Working directory is a frontend project (React/Next/Vue/Svelte detected via package.json).
- [ ] Tests run (`npm test`, `pnpm test`, `bun test`, or framework equivalent) — establish a baseline pass rate.
- [ ] Lint/typecheck command available (`tsc --noEmit`, `eslint`, etc.).
- [ ] Git working tree is clean — refuse to start if dirty (offer to stash).

Recovery:

- If no test command exists: warn loudly. Continue but mark each phase "unverified."
- If tests already failing on main: stop and report the failing tests. Do not pile on.

============================================================
=== PRINCIPLES (from research, 2026) ===
============================================================

Apply these without re-deriving them:

**The three UI states (empty / loading / error)** are where polish lives.

- Empty: explain why empty, clear CTA, preview of populated state.
- Loading: skeleton screen matching final layout (not a generic spinner). Optimistic UI for likes/follows/CRUD.
- Error: plain-language what-went-wrong, what user can do, path back. Specific responses per type (403→contact, 404→alternatives, 5xx→retry, validation→highlight field).

**Motion ladder.** Only animate `transform` and `opacity` — these are GPU-composited. Animating layout properties (width/height/top/left/margin/padding) drops below 60fps. Wrap all animations in `prefers-reduced-motion`. Use three curves and four durations:

| Curve             | cubic-bezier          | Use                       |
| ----------------- | --------------------- | ------------------------- |
| `--ease-out-expo` | `0.16, 1, 0.3, 1`     | modals, large transitions |
| `--ease-snappy`   | `0.4, 0, 0.2, 1`      | loaders, toggles          |
| `--ease-spring`   | `0.34, 1.56, 0.64, 1` | hover, success bounces    |

| Duration            | Value | Use                             |
| ------------------- | ----- | ------------------------------- |
| `--duration-fast`   | 150ms | hover, focus micro-interactions |
| `--duration-base`   | 200ms | button press, toggles           |
| `--duration-medium` | 280ms | modals, drawers                 |
| `--duration-slow`   | 600ms | celebrations (rare)             |

**Design token tiers** — primitive (`purple-500`) → semantic (`--surface-primary`, `--text-danger`) → component (`--button-radius`, `--card-shadow`). Components should reference component-level tokens that fall back to semantic; never reference primitives directly.

**WCAG 2.2 polish gates** — every interactive element:

- Touch target ≥ 48 CSS px (project rule — exceeds 24px WCAG min).
- Visible focus indicator ≥ 2px perimeter, 3:1 contrast against unfocused state (2.4.13).
- Focus not entirely hidden by sticky content (2.4.11).
- Drag operations have single-pointer alternative (2.5.7).
- Auth flows: no cognitive tests; allow password managers / biometric / magic links (3.3.8).

**Reusable component checklist** — for each primitive:

- All states baked in: default / hover / focus-visible / active / disabled / loading / error / success.
- Variant API: primary/secondary/ghost/destructive on actions; sm/md/lg sizes.
- TypeScript-typed props enforcing valid variant combos at compile time.
- Accessibility as a primary requirement, not a checklist.
- Tests per state per variant.

============================================================
=== ORDERED PASS (one component per phase, one commit per phase) ===
============================================================

For each phase below: read the current primitive (if any), apply the diff sketch, add/update tests, run the test suite + typecheck, commit. Then move to the next phase.

### Phase 1 — Button

Audit `Button` (or the most-used button primitive). Add if missing:

- `loading?: boolean` + `loadingText?: string` — disables the button, sets `aria-busy`, renders an inline spinner.
- `leftIcon` / `rightIcon` slots — kills inline `<svg> + label` duplication.
- Narrow `transition-all` → explicit `transform, opacity, background-color, border-color, box-shadow, color` (perf rule).
- `focus-visible:ring-2` with `ring-offset-2` against current bg.
- Verify 48 px min-height on every size variant.

Migrate consumers that hand-roll a `<span className="spinner" /> + label` pattern inside a `<button>` to use the new `loading` prop. Stop after 5–10 high-impact migrations; bulk migration is its own task.

### Phase 2 — EmptyState

Audit `EmptyState`. Add if missing:

- `icon?: ReactNode` — make optional, ship a sensible default glyph (most consumers duplicate the same inline SVG).
- Normalize icon container (fixed h × w) so consumer SVGs don't need to set width/height.
- `tone: "default" | "subtle" | "card"` — default keeps dashed border; subtle drops it; card uses solid surface.
- `size: "default" | "compact"` — compact reduces vertical padding.
- `secondaryAction?: ReactNode` — for "Learn more" or "Watch demo" links beside the primary CTA.
- `data-empty-state` attribute for analytics/testing.

### Phase 3 — Skeleton

If no `Skeleton` primitive exists, create one. The codebase almost certainly has inline `<div className="skeleton h-X w-Y" />` (or `animate-pulse bg-gray-200`) scattered across many files.

```tsx
// skeleton.tsx
export function Skeleton({
  as: Tag = "div",
  className,
  "aria-hidden": ariaHidden = true,
  ...rest
}) {
  return (
    <Tag
      aria-hidden={ariaHidden}
      className={["skeleton", className].filter(Boolean).join(" ")}
      {...rest}
    />
  );
}

export function SkeletonStack({
  count,
  itemClassName = "h-4 w-full",
  gap = 3,
  label = "Loading",
}) {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-busy="true"
      aria-label={label}
      className={`flex flex-col gap-${gap}`}
    >
      {Array.from({ length: count }).map((_, i) => (
        <Skeleton key={i} className={itemClassName} />
      ))}
    </div>
  );
}
```

Migrate 5–10 loading-list patterns from inline `Array.from(...).map(<div className="skeleton ...">)` to `<SkeletonStack>`. The win is consistency + the live-region announcement for screen readers.

### Phase 4 — ErrorAlert (or equivalent)

Audit the error component. Add:

- `retryLabel?: string` — default "Try again" is brittle when the action isn't a retry (e.g., "Reconnect", "Refresh data").
- `secondaryAction?: ReactNode` — for "Contact support", "Go back", or "Get help" links.
- Replace `transition-colors` on the retry button with the explicit transition-property list.

### Phase 5 — Motion token ladder

Open the global stylesheet. Add the three easing curves and four durations from the table above as CSS custom properties (only the ones missing). Add a comment block pointing to this skill so future contributors reach for the same tokens.

Search the codebase for raw `cubic-bezier(...)` values and `transition: ... 0.3s ease`. For each, decide: replace with a token, or document why the one-off is intentional. Don't mass-migrate — leave a TODO comment with the recommended token.

### Phase 6 — Focus indicators (WCAG 2.2 2.4.13)

Grep for components that use only the browser default outline:

```bash
grep -rL "focus-visible:" --include="*.tsx" src/components
```

For each, add `focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[var(--primary)] focus-visible:ring-offset-2` (or the framework equivalent). Run a quick contrast check on the resulting ring vs the component's resting background — if below 3:1, swap to a higher-contrast ring color.

============================================================
=== PER-PHASE WORKFLOW ===
============================================================

1. Read the existing component (if any) and its test file.
2. Write the diff. Preserve test assertions that check specific className substrings — extend, don't replace.
3. Add tests for new features (each new prop gets at least one test).
4. Run the focused test file: `pnpm vitest run <path>` (or framework equivalent).
5. Run the full suite + typecheck before committing.
6. Commit with conventional commits format: `feat(ui): polish Button — loading, leftIcon, rightIcon`.
7. Keep each commit to ≤ 20 files (matches project CLAUDE.md if present).

============================================================
=== STRICT RULES ===
============================================================

- Never delete consumer code without checking it's actually unused.
- Never introduce a new variant or prop without a test.
- Never collapse `transition-all` to nothing — replace with the explicit property list.
- Never animate layout properties to "fix" a transition.
- Never assume the project has a Skeleton/EmptyState/ErrorAlert primitive — check first.
- Never skip the focus indicator audit, even if "everything looks fine."
- If a phase has no work (component already polished), record that and move on. Don't manufacture changes.

============================================================
=== FINAL REPORT ===
============================================================

After all phases (or after the requested phase finishes), print:

```
ui-craft pass complete

Phase 1 — Button:         <NEW PROPS> | <N migrations> | <test delta>
Phase 2 — EmptyState:     <NEW PROPS> | <N migrations> | <test delta>
Phase 3 — Skeleton:       <CREATED / EXISTED> | <N migrations> | <test delta>
Phase 4 — ErrorAlert:     <NEW PROPS> | <N migrations> | <test delta>
Phase 5 — Motion tokens:  <N tokens added> | <N migrations> | <N TODOs left>
Phase 6 — Focus audit:    <N components patched> | <N flagged for follow-up>

Total tests: <before> → <after>
Commits: <N>
```

If any phase failed verification, surface that — do not silently skip it.
