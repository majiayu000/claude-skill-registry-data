---
title: Best practices
skill: true
name: svelte-core-bestpractices
description: Svelte best practices for writing, editing, or reviewing Svelte/SvelteKit components and modules. Use when touching Svelte reactivity, props, events, snippets, each blocks, styling, context, actions/attachments, stores, or Svelte 5 runes.
---

## Process

1. Identify the Svelte mode before changing code.
   - Check `package.json` and existing components.
   - If the project already uses Svelte 5 runes, write new code in runes mode.
   - If the touched area is legacy Svelte and a runes migration is not requested, keep the local style consistent.
   - Done when the edit has one clear syntax mode for the touched files.

2. Put reactivity in the narrowest primitive that fits.
   - Local reactive state: `$state`.
   - Computed value: `$derived` or `$derived.by`.
   - Side effect or external subscription: `$effect`, `{@attach ...}`, `createSubscriber`, or an event handler, depending on the trigger.
   - Done when no `$effect` is being used just to compute state.

3. Keep state scoped.
   - Component-only values stay local.
   - Shared state that must be scoped to a subtree uses context.
   - Shared module state is acceptable only when cross-user leakage is impossible or irrelevant.
   - Done when SSR state cannot leak between users.

4. Review DOM boundaries.
   - Lists use keyed each blocks with stable object identity.
   - Global listeners use `<svelte:window>` or `<svelte:document>` when possible.
   - Parent-to-child styling uses CSS custom properties before `:global`.
   - Done when the DOM update and cleanup paths are explicit.

## `$state`

Use `$state` only for values that should update a template expression, `$derived`, or `$effect`. Normal variables are fine for everything else.

Objects and arrays created with `$state({ ... })` or `$state([ ... ])` are deeply reactive. Mutation triggers updates, but proxying has overhead. For large values that are only reassigned, such as API responses, use `$state.raw`. Use `$state.snapshot` before passing proxy state to an external API or storing a moment-in-time copy.

Rune-enabled `.svelte.js`/`.svelte.ts` modules should export factories or objects with getters and named mutation methods. Do not export a rune variable that is reassigned internally, and avoid module-global mutable state when instances or SSR requests need isolation.

## `$derived`

Use `$derived` for computed values.

```js
let square = $derived(num * num);
```

Use `$derived.by` when the computation needs a function body.

```js
let total = $derived.by(() => {
  return items.reduce((sum, item) => sum + item.price, 0);
});
```

Do not use `$effect` to assign ordinary computed state.

```js
// avoid
let square;

$effect(() => {
  square = num * num;
});
```

Derived values are writable, but they re-evaluate when their dependencies change. If a derived expression returns an object or array, Svelte returns it as-is; it is not made deeply reactive.

## `$effect`

Use `$effect` as an escape hatch for real side effects. Avoid writing Svelte state inside effects.

Choose the tighter tool when one exists:

- External library sync, such as D3: `{@attach ...}`.
- User-triggered work: the event handler or a function binding.
- Debug logging: `$inspect`.
- External reactive source: `createSubscriber` from `svelte/reactivity`.

Effects do not run on the server, so `if (browser) { ... }` inside an effect is unnecessary.

## `$props`

Treat props as changing values. Values that depend on props should usually be derived.

```js
let { type } = $props();

let color = $derived(type === 'danger' ? 'red' : 'green');
```

This stale version should be avoided:

```js
let { type } = $props();
let color = type === 'danger' ? 'red' : 'green';
```

## `$bindable`

Use `$bindable` only when a child is intentionally an input-like controller for a parent-owned value. Keep domain operations such as add, save, or delete as callback props so mutation ownership stays visible.

## `$inspect.trace`

Use `$inspect.trace(label)` to debug reactivity. Put it as the first line of an `$effect`, `$derived.by`, or a function called by them. It shows which dependency triggered the update.

## Events

In modern Svelte, event listeners are element attributes that start with `on`.

```svelte
<button onclick={() => save()}>save</button>
<button {onclick}>save</button>
<button {...props}>save</button>
```

For global targets, prefer Svelte elements over manual lifecycle wiring.

```svelte
<svelte:window onkeydown={handleKeydown} />
<svelte:document onvisibilitychange={handleVisibilityChange} />
```

## Snippets

Use snippets for reusable markup that can be rendered with `{@render ...}` or passed as props.

```svelte
{#snippet greeting(name)}
  <p>hello {name}!</p>
{/snippet}

{@render greeting('world')}
```

Declare snippets in the template. Top-level snippets can be referenced from `<script>`. A snippet that does not read component state can also be exported from `<script module>`.

## Each blocks

Use keyed each blocks for lists with stable item identity.

```svelte
{#each todos as todo (todo.id)}
  <TodoItem {todo} />
{/each}
```

The key must uniquely identify the object. Use IDs, not array indexes.

If an item will be mutated with a binding such as `bind:value={item.count}`, avoid destructuring the item in the each block.

## CSS from JavaScript values

Use CSS custom properties through the `style:` directive.

```svelte
<div style:--columns={columns}>...</div>
```

```css
.grid {
  grid-template-columns: repeat(var(--columns), 1fr);
}
```

## Styling child components

Use CSS custom properties as the parent-to-child styling hook.

```svelte
<!-- Parent.svelte -->
<Child --color="red" />
```

```svelte
<!-- Child.svelte -->
<h1>Hello</h1>

<style>
  h1 {
    color: var(--color);
  }
</style>
```

Use `:global` only when the child cannot expose a styling hook, such as with some library components.

```svelte
<div>
  <Child />
</div>

<style>
  div :global {
    h1 {
      color: red;
    }
  }
</style>
```

## Attachments

Prefer `{@attach ...}` for new reusable DOM behavior. Return cleanup for every global listener or external resource. Existing `use:` actions remain valid for interoperability, but do not omit their `destroy()` path.

## Error boundaries

Use `<svelte:boundary>` for local descendant rendering/effect failures and clear the failure condition before calling its `reset` function. Do not expect it to catch errors thrown directly by event handlers. In SvelteKit, keep route failures distinct: `error(...)` from `load` is handled by the nearest `+error.svelte`.

## Context

Use context instead of shared-module state when state should be scoped to a component subtree. This is especially important during server-side rendering, where module state can leak between users.

Prefer `createContext` over `setContext` and `getContext` when possible because it provides type safety.

## TypeScript and tests

Type component props, callbacks, snippets, and state collections when a project uses TypeScript, but continue runtime validation at server/API boundaries. Keep verification layers distinct: pure tests for logic, component-browser tests for isolated component contracts, end-to-end tests for complete running-app flows, and builds for bundling evidence.

## Async Svelte

Svelte 5.36 and higher can use await expressions and hydratable promises directly inside components. These require `experimental.async` in `svelte.config.js` and are not fully stable.

Use async Svelte only when the project has already opted into that experimental mode.

## Modern replacements

For new runes-mode code, prefer these replacements:

- `$state` for reactive state instead of implicit `let` reactivity.
- `$derived` for computed values instead of `$:` assignments.
- `$effect` for side effects instead of `$:` statements.
- `$props` instead of `export let`, `$$props`, and `$$restProps`.
- `onclick={...}` instead of `on:click={...}`.
- `{#snippet ...}` and `{@render ...}` instead of `<slot>`, `$$slots`, and `<svelte:fragment>`.
- `<DynamicComponent>` instead of `<svelte:component this={DynamicComponent}>`.
- `import Self from './ThisComponent.svelte'` and `<Self>` instead of `<svelte:self>`.
- Classes with `$state` fields for shared reactivity instead of stores when that state is part of a domain object.
- `{@attach ...}` for new DOM behavior; retain `use:action` where interoperability requires it.
- Arrays and objects in `class` attributes instead of `class:` directives.

## Completion check

Before finishing a Svelte edit or review, verify every touched component/module against this list:

- State uses the narrowest reactive primitive.
- Computed values are derived, not effect-assigned.
- Effects are limited to real side effects or external subscriptions.
- Prop-dependent values update when props change.
- Lists with identity are keyed by stable IDs.
- Global listeners have a clear cleanup path or use Svelte global elements.
- Parent-to-child styling has an explicit CSS custom property hook when needed.
- Context is used where SSR-scoped shared state matters.
- Rune modules do not export reassigned state or leak accidental globals.
- Bindings are limited to deliberate input-like shared values.
- Route errors and component error boundaries are not conflated.
- TypeScript checks are paired with runtime validation at untrusted boundaries.
- Tests target the narrowest appropriate layer.
- New code follows the project's Svelte mode.
