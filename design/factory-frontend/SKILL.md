---
name: factory-frontend
description: Frontend conventions distilled across builds. CRUD shape (DataTable + drawer with mode union), RowActions primitive, format helpers, heading tiers, semantic color tokens, query-key naming, component-library decision criteria (Mantine vs shadcn). Read when scaffolding any UI surface that touches lists, forms, or entity editing.
---

# Factory frontend

Each section leads with **Principle** (one sentence, stack-agnostic), then **Why** (constraint → option → tradeoff), then **Recipe** (the Mantine or shadcn shape we use), and **Failure mode** when there's one to name. Sections that are pure style with no deeper truth are marked `Recipe only`.

## CRUD shape — DataTable + drawer with mode union

**Principle.** Model the drawer's state as a discriminated union; the drawer only edits the row it was opened from.

**Why.** A drawer is a small modal state machine: closed / creating / editing-row-X. Boolean `isOpen` + nullable `editingId` lets impossible states represent themselves (open + no id, closed + id). The discriminated union makes those states unrepresentable. The "edits only the row it was opened from" rule keeps each drawer single-shape; relations open their own drawers, so the state inside any one drawer never has to reason about more than one entity.

**Recipe.**

```tsx
type FooDrawerMode =
  | { kind: 'closed' }
  | { kind: 'create' }
  | { kind: 'edit'; foo: Foo };

const [drawerMode, setDrawerMode] = useState<FooDrawerMode>({ kind: 'closed' });

// Imperative form sync when mode changes
useEffect(() => {
  if (drawerMode.kind === 'edit') {
    form.setValues(toFormValues(drawerMode.foo));
    form.resetDirty();
  } else if (drawerMode.kind === 'create') {
    form.reset();
  }
}, [drawerMode.kind, drawerMode.kind === 'edit' ? drawerMode.foo.id : null]);
```

## DataTable columns — declarative factory

**Principle.** Columns are produced by a factory function that takes callbacks; the page wires the actions, not the column definitions.

**Why.** Inlining handlers in column definitions binds the columns to the page's state, which breaks reuse and complicates testing. A factory function that takes `onEdit` / `onDelete` / `onDuplicate` as parameters keeps the columns declarative and lets a different page wire different callbacks without forking the columns. Cost: one more layer of indirection. Benefit: columns are reusable, testable, and the wiring is grep-able.

**Recipe.**

```tsx
export function makeFooColumns({
  onEdit,
  onDelete,
}: {
  onEdit: (foo: Foo) => void;
  onDelete: (foo: Foo) => void;
}): ColumnDef<Foo>[] {
  return [
    { accessorKey: 'name', header: 'Name', sortable: true, filterable: true },
    { accessorKey: 'status', header: 'Status', cell: (row) => <StatusBadge status={row.status} /> },
    { id: 'actions', cell: (row) => <RowActions primary={{ ... }} overflow={[ ... ]} /> },
  ];
}
```

## RowActions primitive

**Principle.** Row actions follow one shape across the app: one primary action plus an overflow menu, tone-aware, with `hidden` for permission-gated items.

**Why.** Without a shared primitive, every table reinvents the same UI: a button here, a kebab menu there, two different "delete" affordances, three different danger styling decisions. A shared primitive collapses this into one component with one set of rules. New tables inherit the consistent affordance by default; tone and permission gating live where they belong (the primitive).

**Recipe.**

```tsx
<RowActions
  primary={{ label: 'Edit', onClick: () => onEdit(row) }}
  overflow={[
    { label: 'Duplicate', onClick: () => onDuplicate(row) },
    { label: 'Delete', tone: 'danger', onClick: () => onDelete(row), hidden: !canDelete },
  ]}
/>
```

## Format helpers — single source

**Principle.** All formatting (currency, integer, percent, date) lives in one file; never reimplement inline.

**Why.** Inline currency math drifts across views — one place shows `$1,200.00`, another shows `$1,200`, another shows `1.2K`. Each drift is a bug report; each fix is a search-and-replace that misses one. A single `src/lib/format.ts` makes "how do we display money" one answer in one file.

**Recipe.**

```ts
export const formatCurrency = (cents: number) => /* ... */;
export const formatCompactCurrency = (cents: number) => /* ... */;  // $1.2M
export const formatInteger = (n: number) => /* ... */;
export const formatPercent = (n: number) => /* ... */;              // expects 0..1
```

**Failure mode.** Currency formatting reimplemented inline across three pages — each page rounded differently, the dashboard totals didn't add up, the fix took a week to find.

## Heading hierarchy — tier components, not raw `<h1>`

**Principle.** Three named tiers (PageHeader / CardHeader / FormSection); consumers never set heading size or color.

**Why.** Freeform `<h1>` / `<h2>` / `<h3>` use is how typography drifts. One page has h2-32px section labels, another has h3-24px, the visual hierarchy collapses. Named tier components encode the rules in one place; the consumer picks the tier, not the size.

**Recipe.** Use `PageHeader` for the page title + primary actions + breadcrumbs; `CardHeader` for a section title within a card; `FormSection` for a form group label. Size and color contrast rules live in the components.

## Semantic colors — never raw palette names

**Recipe only** — the full design-system discipline lives in `factory-design.md` (token vocabulary, CSS-var + Tailwind bridge, dark/light as a variable swap, primitives as token consumers, vocabulary-sprawl failure mode). Read it before scaffolding a new UI surface.

For status-tone use specifically inside CRUD surfaces:

- Use semantic state tokens (`success` / `warning` / `danger` / `info` / `neutral`); never raw palette names (`red`, `blue`, `green`).
- Default badges to `neutral`; reserve one accent for the operationally-meaningful state per surface.
- Disambiguate via variant (filled / light / outline), not hue.

## Query keys — strict 2-segment prefix

**Principle.** Query keys follow `[entity, kind, ...params]`; invalidate at the 2-segment prefix after mutations.

**Why.** Same principle as `factory-api.md §TanStack Query hook` — a list query and a detail query for the same entity share invalidation triggers. The 2-segment prefix is the union; per-key invalidation drifts.

**Recipe.**

```ts
['entity', 'list', filters]    // list queries
['entity', 'detail', id]       // detail queries
```

Invalidate at `['entity']` after mutations.

## React Query Provider — per-SSR-request, stable per browser page

**Principle.** Construct the QueryClient inside `useState`; fresh per server render, stable per browser page.

**Why.** A module-scope QueryClient is shared across server renders, which means request A's data can leak into request B's response. A `useState`-wrapped factory makes the client construct once per server render (fresh data) and once per browser page (stable cache).

**Recipe.**

```tsx
export function Providers({ children }: { children: ReactNode }) {
  const [queryClient] = useState(() => new QueryClient({ defaultOptions: { /* ... */ } }));
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
}
```

## Conditional query enabling

**Recipe only** — the principle lives in `factory-api.md §conditional query enabling`.

```ts
const { data } = useQuery({
  queryKey: ['vehicle', 'list', { fleetId }],
  queryFn: () => listVehicles({ fleetId }),
  enabled: !!fleetId,
});
```

## Loading, empty, and error states — all three, every time

**Principle.** Every data view has a defined state for loading, empty, and error; never let a view fall back to "blank."

**Why.** A blank table is ambiguous to the user — is it loading, did the request fail, do they have no data? Three different conditions, one display state, every one a confusing user experience. Defining the three states explicitly turns ambiguity into information: skeleton means "wait," EmptyState means "you can act," error means "something is wrong, here's the retry."

**Recipe.**

- **Loading:** skeleton in tables, spinner in drawers. Don't block the page.
- **Empty:** explicit `EmptyState` component with primary CTA. Don't leave a blank table.
- **Error:** TanStack Query's `error` state surfaced inline, with retry button.

## Component library — Mantine vs shadcn

**Principle.** Mantine for CRUD-heavy / internal-tool surfaces; shadcn for design-flexible / marketing-adjacent surfaces. One library per project.

**Why.** Mantine ships dense, opinionated primitives — DataTable, DatePicker, Combobox — that save weeks on CRUD-heavy apps. shadcn ships unstyled primitives that maximize design control, which matters when the app shares styling with a marketing site. Mixing them in one project means two component systems, two theming setups, two ways to do the same thing — pick one.

**Recipe.**

**Mantine** — CRUD-heavy / form-table dense / internal-tool surfaces. Built-in primitives save weeks. Pair with `@mantine/form` + `schemaResolver` from `mantine-form-zod-resolver`.

**shadcn** — design flexibility / marketing-adjacent / unified Tailwind styling with a landing site. Pair with `react-hook-form` + `zodResolver`.

If the project has a marketing site and an app, default to shadcn for both. If app-only and CRUD-heavy, Mantine.

## Cross-feature import ban

**Principle.** Feature folders are peers, not a tree; cross-feature imports go through `lib/` or shared primitives.

**Why.** A direct import from `features/cases/` into `features/products/` creates a hidden coupling — refactoring cases now requires touching products. Routing shared logic through `lib/` makes the dependency explicit and the surface auditable. The cost is one extra file when extracting; the benefit is that feature folders stay independently refactorable.

**Recipe.** Enforce via ESLint `no-restricted-imports` if the project is large enough.

## Build local components last — extend shared primitives first

**Principle.** Extend shared primitives even for single-consumer needs; don't build local components first with the intent to "lift later."

**Why.** "Lift later" is the lie every local component tells. The local version diverges from the primitive — slightly different padding, slightly different focus ring — and by the time anyone reaches to lift it, the divergence is a refactor, not a move. Consistency only compounds if you pay it up front.

**Recipe.** When a primitive needs a new variant, add the variant to the primitive. When a screen needs a new layout, compose it from primitives, not from scratch.

## Don't edit relations inside an entity's drawer

**Principle.** A drawer edits only the row it was opened from; relations open their own drawers.

**Why.** A drawer that edits a customer and also lets you edit their related contacts inline accumulates state for two entities, two forms, two mutation chains. The composition gets exponentially harder to reason about. Each drawer for one entity is one state machine; relations get their own drawer, their own state.

**Recipe.** "Edit contacts" inside the customer drawer opens the contacts drawer, doesn't render an inline form.

## One direction of truth — no two-way state-DB sync

**Principle.** Pick one direction of truth per piece of state: server state via TanStack Query, or client reducer state for UI-only transient state. Never both.

**Why.** Two-way sync — a client reducer that mirrors a DB row and auto-persists on every change — looks elegant until the inevitable desync: the user edits while a background refresh comes in, the reducer applies the patch, the DB write loses the user's edit, the auto-persist hook then writes the stale reducer state back. The bug is invisible at first and impossible to reproduce. The fix is asymmetry: read from one source, write through one path. TanStack Query handles the read-write loop for server state; reducers handle UI-only state that doesn't touch the DB.

**Recipe.** Server data: `useQuery` for reads, `useMutation` with `invalidateQueries` for writes. UI-only state (drawer mode, filter selections, expanded rows): local reducer, never persisted.

**Failure mode.** Fleet-advisor's `RouteContext` + auto-persist hook — the client reducer and DB persistence desynced under concurrent edits, lost user changes silently.

## Source of truth — DOM-owned vs React-owned

**Principle.** Every mutable value has one authoritative home — the DOM node or React's render tree. Decide per *value*, not per form: a value that feeds a live-derived view (a running total, inline validation, a conditional field) belongs in React's tree; a write-mostly value that only matters at submit can stay DOM-owned.

**Why.** Model form state as a dependency graph: `quantity → lineTotal → subtotal`. React-owned state (controlled inputs) keeps the whole graph live — mutate a leaf and every derived node recomputes, paid for with a re-render per keystroke. DOM-owned state (uncontrolled inputs) cuts the graph at the leaf: the value lives in the input/ref, outside React's reach, so each derived node needs an explicit edge — a subscription — re-drawn by hand or it silently goes stale. "Controlled vs uncontrolled" is just the framework's name for which home you picked. The danger of uncontrolled is that a missing edge is *silent*: no error, the derived value just stops tracking, and unrelated re-renders make it look intermittently fine — which reads as a clamp or a cap and sends you debugging the wrong thing. The tell for ownership: if something on screen is a function of a value and must update as the user types, that value wants to be in React's tree.

**Recipe.** Hybrid is usually the right answer — keep write-mostly fields DOM-owned for snappy typing, make the derived subtree React-owned. In Mantine uncontrolled forms, don't read `form.getValues()` in render for display; route it through a subscribe-on-access hook so the read *is* the subscription and the edge can't be forgotten:

```ts
// reads the value AND subscribes the caller to its changes
export function useReactiveValues<T = unknown>(
  form: UseFormReturnType<any>,
  path: string,
): T {
  const [, bump] = useState(0);
  const onChange = useCallback(() => bump((n) => n + 1), []); // stable: no re-subscribe per render
  form.watch(path, onChange); // fires for nested edits + add/remove under `path`
  return (form.getValues() as Record<string, unknown>)[path] as T;
}
```

Rule: `getValues()` is for event handlers and submit only — never a render-for-display read. `form.watch` alone doesn't fix a stale total — its callback fires but doesn't re-render, so it must be paired with a state bump (which the hook hides). A *precise* lint rule ("`getValues()` in render scope") needs a custom AST rule; until then the hook is the enforcement — make the right path the only ergonomic one.

**Failure mode.** The severed edge — a derived value (line total, subtotal) computed from `getValues()` in render under an uncontrolled form. It updates only on incidental re-renders, so it looks intermittently correct and presents as a cap/clamp, which delays diagnosis. Kairos KAI-148: line totals froze at the last incidental render ("stuck at $2,700"); the fix was `useReactiveValues`, not a switch to controlled mode — the whole-form re-render and the controlled-`NumberInput` cursor quirks weren't worth buying a structural guarantee the user never sees.

## DataTable cell-edit vs drawer — different tools

**Principle.** Inline cell-edit is for fast bulk edits; drawer is for single-row, multi-field, validated edits.

**Why.** Cell-edit minimizes friction (one click, one field, one save) but provides no room for validation messages, related-field dependencies, or audit-log context. Drawer maximizes context (multi-field form, validation, related entities visible) but adds a click. Mismatching the tool to the task makes either workflow worse: cell-edit for a 12-field form is hostile; drawer for a single status flip is heavyweight.

**Recipe.** Bulk-flip status across 50 rows → cell-edit. Edit a customer's full record → drawer.

## Source patterns

Drawn from kairos (DataTable, RowActions, drawer mode unions, format helpers, heading tiers, semantic colors, query-key naming, Providers pattern, cross-feature import ban, `useReactiveValues` / DOM-vs-React state ownership — KAI-148), duezy (Mantine theme + semantic colors), fleet-advisor (shadcn + Mantine variants, conditional query enabling), ford-analysis (shadcn + Context-driven selection state).
