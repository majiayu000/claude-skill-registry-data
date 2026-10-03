---
name: dead-code-audit-frontend
description: "Audit dead code in frontend/src for Svelte frontend code. Triggers on: requests like 'find dead code', 'remove unused code', 'cleanup unused', 'what can be refactored', deeper inspection after a large refactor (bind:event, helper extraction, feature removal), before a big feature update, or after a long merge. Checklist: unused imports, props with no call sites, $state values never read, $derived values never read, functions never called, exports never imported, types/interfaces never used, the $derived(() => expr) anti-pattern, and inline handlers that could be refactored. Produce a report first, then execute."
---

# Skill: Dead code audit for frontend

## When to run

- User asks for "code cleanup", "dead code", "unused", "tidy up"
- After a large refactor (e.g., extracting helpers, removing a feature) — leaves orphans
- Before merging a long-running branch
- Periodically to surface debt

## Audit catalyst list

For each, run matching greps:

### Imports
```
grep for `^import .* from` per file, list imports, then grep each named import's symbol usage within that file (must appear ≥ 1 time outside the import line).
```

### Props in components
For each `$props()` destructure, confirm each prop is read in the markup or script. Unused prop = dead because consumers can stop passing it.
Recently removed feature can leave props behind — Common example: a `variant` prop whose default branch was removed, leaving an unconditional template.

### `$state`
`let x = $state(...)` — must appear in `{x}` or `{... x ...}` or be read inside another `$derived` / function used by template.

### `$derived`
`const x = $derived(...)` — must appear as `{x}` in template (or be read by another `$derived` / function used in template).

### Functions declared in `<script>`
For each `function foo()` code path that's not exported: trace call graph from template. If unreachable: dead.

### Exports from `.ts` files
For each `export const foo`, `export function bar`, `export type X`: grep the entire `frontend/src` for usage. If zero uses: dead export.

### Types / interfaces
For each `export type X` in `types/`: confirm at least one `.svelte` or `.ts` file imports it. If only the declaration file references it, it's dead.

### Anti-pattern: `$derived(() => expr)` returning a function
This is the function form of derived in Svelte 5 — it evaluates to the arrow function, not the value. Most of the time the user wanted `$derived(expr)` (eager). Verify each `$derived(...)` body that returns a value; if the body is `() => { ... return value; }` and the call site does `title()` as if it were a value, that's a bug masquerading as dead-code-shaped behavior. Convert to `$derived.by(() => { return value; })` or inline the expression.

### Inline event handlers that could be `bind:` (subject to AGENTS.md)
Grep `oninput=\{(e) =>` and `onchange=\{(e) =>`. Each handler should either (a) be a named function with side effects, (b) trigger state mutation that requires a callback pattern (per AGENTS.md bug #4, when parent state is `string | undefined`), or (c) be a candidate to become `bind:value`. Beware: in this repo, `bind:value` is forbidden for form components (see `.opencode/AGENTS.md`). Don't suggest `bind:` on form components.

## Output format

Always deliver report before executing. Use this format:

```
## Dead code report

### File: <path>

| Lines | What | Why dead | Suggested fix |
|---|---|---|---|
| X-Y | `<code>` | No call site outside itself | Delete lines X-Y |
```

Group by:
1. Safe to delete (no behavior change, no API impact)
2. Refactor suggestion (e.g., `$derived` anti-pattern)
3. Risky (state used internally for caching, load guards) — recommend asking user before removing

## Verification before execution

For every dead code candidate, before deleting:
1. Grep the entire `frontend/src` for any reference (functions, props, exports)
2. Read related files to confirm call graph
3. Skip "internal but functional" code — e.g., `loaded` flag in `settings.svelte.ts` that guards `load(force)` dedupe. Not dead.
4. Skip "redundant duplicate" code — e.g., `galleryCategoriesApi` duplicates `galleryApi.categories()`. Mention but don't delete (replacing it changes call sites, refactor by preference).

## Execution protocol

After report:
1. Ask the user which categories to apply (safe / anti-pattern / risky)
2. Execute edits in batch
3. Run `svelte-check` (see verify-svelte-check skill) after each batch
4. Report final state

## Pitfalls

- Don't delete "internal state that sets only itself" without checking that internal state isn't read indirectly (e.g., the `loaded` guard reads `this.loaded` later).
- Don't rely on `svelte-check` alone. It surfaces unused locals and imports, but doesn't catch unused exports, props, or `$derived`.
- Inline handlers are not dead code just because they "could be `bind:`". They may exist for AGENTS.md compliance. Cross-check `.opencode/AGENTS.md` before suggesting bind.
- Custom exports in `.svelte.js` files (`toastStore.info()` etc) may be intentional public API for future. If unsure, ask user before removing.