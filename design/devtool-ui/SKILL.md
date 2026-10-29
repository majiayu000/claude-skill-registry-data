---
name: devtool-ui
description: |
  Build dense developer-tool frontends with Svelte 5, semantic CSS custom
  properties, and focused dependencies. Use for session or log viewers,
  analytics dashboards, search interfaces, virtualized lists, keyboard
  navigation, dual-theme design, real-time updates, or a frontend embedded in a
  Go or Rust binary. Patterns cover Svelte 5 runes, SSE, accessible responsive
  layouts, and lists with 20K+ items; they are drawn from production work on
  agentsview (761 stars).
---

# Developer Tool UI

Use this skill to build a fast, keyboard-native interface for structured,
high-volume data. The patterns come from production code handling 20,000+
item lists with sub-16ms frame budgets, dual themes, and zero component-library
overhead. Adapt the sample thresholds to the app's measured workload; keep the
principles below unless the user has a concrete reason to depart from them.

## Build sequence

1. **Set the visual system.** Define semantic CSS properties for surfaces,
   text, role-based backgrounds, and accents in both light and dark themes.
   Read [visual design](references/visual-design.md) for color, typography,
   and interaction details.
2. **Choose the app structure.** Group components by feature, decide whether a
   History API router is enough, and define typed content blocks where users
   need independent rendering or filtering. Read [architecture](references/architecture.md)
   for those choices and for Go embedding.
3. **Define data ownership.** Split reactive state by domain, add a typed API
   boundary, and decide which state belongs in local storage. Read
   [state management](references/state-management.md) for stores, SSE, routing,
   and persistence.
4. **Protect responsiveness.** Virtualize long lists, cancel stale requests,
   and cache expensive rendering where profiling supports it. Read
   [performance](references/performance.md) for adapter, pagination, cache,
   and debounce patterns.
5. **Make interaction accessible.** Centralize global shortcuts, keep list
   navigation based on data indices, and verify focus, ARIA, and narrow-screen
   behavior. Read [keyboard and accessibility](references/keyboard-a11y.md)
   for implementation patterns.
6. **Integrate and check.** Connect the layers, then verify theme switching,
   keyboard use, loading and cancellation, and representative large lists in
   the running app.

## Core principles

1. **Semantic over descriptive.** Name CSS variables by meaning (`--tool-bg`),
   not appearance (`--amber-50`). Names survive theme changes.
2. **Minimal dependencies.** Three runtime deps (`@tanstack/virtual-core`,
   `marked`, `dompurify`) and hand-written everything else. Each dependency is
   bundle size, upgrade churn, and security surface.
3. **Performance through architecture.** Virtual scrolling, LRU caching,
   AbortController on every async operation, progressive loading. Performance
   is a structural decision, not a late-stage optimization.
4. **Keyboard-first, mouse-supported.** One centralized `keydown` handler with
   three tiers (modifier combos, Escape cascade, single-key shortcuts gated on
   input focus and modal state), vim-style j/k navigation on data indices, a
   Cmd+K command palette.
5. **Two complete themes.** Design light and dark simultaneously, not "light
   first, then invert." Tint the neutrals (blue-shifted dark backgrounds);
   pure grays such as `#1a1a1a` read as sterile.
6. **No component library.** Scoped Svelte `<style>` blocks plus CSS custom
   properties give full control over micro-interactions with no dead code or
   specificity battles. Tailwind fits forms and marketing pages, not dense
   information displays with `color-mix()`-driven state styling.
7. **Embedded SPA.** Plain Vite + Svelte 5, no SvelteKit. Build to static files
   and embed them in a Go or Rust binary (`//go:embed`) for single-binary
   deployment.

## Choosing a reference

Each reference is independent. Load the one matching the current decision:

- [Visual design](references/visual-design.md): semantic color tiers, tinted
  dark palettes, typography, polish, and stable entity colors.
- [Performance](references/performance.md): virtualizer integration, LRU
  caching, request cancellation, progressive pages, debounce, and dependency
  trade-offs.
- [State management](references/state-management.md): Svelte 5 stores, effect
  roots, SSE, a custom router, persistence, and a typed fetch client.
- [Keyboard and accessibility](references/keyboard-a11y.md): shortcut
  handling, vim-style navigation, command palette, ARIA, and responsive layout.
- [Architecture](references/architecture.md): feature-based components,
  SPA choice, backend embedding, typed content blocks, resizable panes, and
  page rendering.

## Anti-patterns

- **One giant store.** Every `$effect` reruns on any field change. Split by
  data-ownership domain, but not per component; that scatters related state
  and forces prop drilling or event buses.
- **Scatter-registered keyboard handlers.** Per-component listeners cause
  duplicate responses, orphaned listeners, and ordering ambiguity. One
  centralized handler is the single source of truth.
- **Forgetting AbortController.** Without cancellation, stale responses
  overwrite current data and stale closures write to outdated state. Every
  async store method gets one.
- **Skipping virtual scrolling.** "A few hundred items" becomes 20,000 faster
  than you think. Virtualize from the start; the adapter pattern makes it no
  harder than a plain list. Fixed row heights are simpler; measured variable
  heights need the adapter plus cache invalidation on context switch.
- **Pure gray dark themes and Tailwind for dense displays.** See principles 5
  and 6.
- **Unchecked hand-written styling.** Owning the CSS means owning keyboard
  focus (`:focus-visible`), contrast, `aria-label` on icon buttons, and touch
  targets. Check those explicitly.
