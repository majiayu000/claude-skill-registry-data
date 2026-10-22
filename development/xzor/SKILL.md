---
name: xzor
description: Use when writing, changing or explaining .xzor components or an xzor app (Blazor-style components for TypeScript, packages @source-crafter/xzor and @source-crafter/xzor-runtime), including pages, routes, layouts, slots, cascading values, dependency injection, main.ts or the xzor build.
---

# xzor

## Overview

A `.xzor` file is one component: HTML with `@` expressions plus a `@code { }` block of TypeScript class members. `xzor build` compiles each file to a TypeScript class, type-checks the project with TypeScript 7, and bundles `main.ts` into `dist/main.js` with Bun.

**It looks like Blazor, but it is not Blazor.** Many Blazor names don't exist here (`<Router>`, `@foreach`, `@Body`, `LayoutComponentBase`, `@using`, `NavLinkMatch`, `StateHasChanged`, `createApp`). When unsure, use the forms below; never invent APIs.

## Turning a request into files

1. Pick components (one `.xzor` each, PascalCase file name = component name), pages (components with `@page`), layouts (components with `@slot`) and services (`.ts` classes).
2. Write `main.ts` (the entry: `@Mount`), `Routes.xzor` (only if there are pages), `index.html`, and check `tsconfig.json`.
3. Run `bun x xzor build` and fix every error it reports before answering. Errors point at `.xzor` lines.

## Project setup

```sh
bun add -d @source-crafter/xzor typescript@^7
bun add @source-crafter/xzor-runtime
bun x xzor init          # package.json scripts, tsconfig.json, .gitignore (adds only what is missing)
bun run dev              # xzor dev: build, serve (SPA fallback), print the URL; saving a .xzor patches the open page keeping state, other changes reload
bun x xzor build         # one-off production build into dist/
```

`xzor init` writes this `tsconfig.json` (or adds the missing parts to an existing one):

```json
{
  "compilerOptions": {
    "target": "ES2022", "module": "ESNext", "moduleResolution": "bundler",
    "lib": ["ES2022", "ESNext.Disposable", "DOM"],
    "strict": true, "noEmit": true, "skipLibCheck": true,
    "rootDirs": [".", ".xzor"]
  },
  "include": ["**/*.ts", ".xzor/**/*.ts"],
  "exclude": ["dist", "node_modules"]
}
```

No `experimentalDecorators`: xzor uses standard decorators.

`index.html` loads the bundle, not `main.ts`:

```html
<div id="app"></div>
<script type="module" src="./dist/main.js"></script>
```

Generated `.xzor/` and `dist/` are build output: never edit them. Don't create `routes.ts` at the root, and never import `./main` from a component.

## Component anatomy

```xzor
@import { type EventCallback } from "@source-crafter/xzor-runtime"
@import TodoItem from "./TodoItem.xzor"

@code {
  title = "Todos";                        // a field is a prop the parent can set
  todos: Todo[] = [];
  changed?: EventCallback<number>;        // callback prop; calling it re-renders the parent

  add(text: string) {                     // inside @code it is plain TypeScript: use this.
    this.todos.push({ text, done: false });
    this.changed?.(this.todos.length);
  }
}

<h2>@title (@todos.length)</h2>
```

- Imports go at the top as `@import ...` lines (any ES import), never inside `@code`. Directives (`@page`, `@import`, `@inject`, `@inherits`, ...) can come in any order.
- In the **template**, write member names bare (`@title`, `@add(x)`): xzor adds `this.` itself. Inside `@code`, write `this.`.
- `#private` members also work bare in the template: `@#secret`.

## Template syntax

| Need | Write |
|---|---|
| Print a value | `@name`, `@user.name`, `@items[0]`, `@(a + b)` for anything else; an array literal needs no parentheses: `@['a', 'b']` |
| Literal `@` | `@@` (emails like `a@b.com` are fine as is) |
| Condition | `@if (x) { ... } else if (y) { ... } else { ... }` |
| Loop | `@for (const item of items) { <li @key="item.id">@item.name</li> }` (any JS `for` head; there is no `@foreach`) |
| Switch | `@switch (v) { case "a": <p>A</p> break; default: <p>?</p> }` |
| Statements | `@{ const total = sum(items); }` then `@total` |
| No wrapper | `<text>...</text>` |
| Comment | `@* ... *@` |
| Attribute | `class="item @kind"`, `disabled="@(!ok)"` (`false`/`null` removes it) |
| Event | `@onclick="save"`, `@onclick="() => count++"`, `<form @onsubmit="add" @onsubmit:preventDefault>` (modifiers combine with the handler) |
| Two-way binding | `<input @bind="text" />`, `@bind:event="oninput"`, checkbox `@bind="todo.done"`, numbers stay numbers |
| Bind a component | `<Stepper @bind-value="n" />` (child has `value` and `valueChanged?: EventCallback<T>`) |
| DOM/instance ref | `@ref="input"` with a field `input?: HTMLInputElement;` |
| Spread attributes | `@attributes="attrs"` |
| Inline SVG | `<svg viewBox="0 0 24 24"><path d="@d" /></svg>` (keep the `<svg>` and its children in one place, not split across an `@if`/`@for`) |

Props on a child: `<Child title="text" count="n + 1" onSave="save" />`. A callback prop (`onSave?: EventCallback<T>`) can also be set like a DOM event: `@onsave="save"`. A prop typed `string`, a union of string literals, an imported alias of string literals (`type Size = "s" | "m"`), or given a string default (`name: Kind = "a"`) takes text; any other type takes a TypeScript expression. Misspelled or mistyped props are build errors.

An event re-renders **only the component that owns the handler**, and that render reads everything again (its fields, props and injected services). If shared state changes in *another* component's handler, call `this.stateHasChanged()` on the components that show it, or pass the value down as a prop.

## Styles and module code

```xzor
@module {
  export type Kind = "a" | "b";            // module scope: exportable, no `this`
  export const label = (k: Kind) => k.toUpperCase();
}
@code { kind: Kind = "a"; pct = 40; }
<div class="bar">@label(kind)</div>
<style>
  .bar { width: @pct%; }
  @if (kind === "b") { .bar { color: red; } }
</style>
```

- One top-level `<style>` per component, or a sibling `X.css.xzor` (not both). Rules are scoped to the component's markup and the content it passes to children; `<style global>` (or `@global` first in `X.css.xzor`) opts out.
- `@name` / `@(expr)` only in property values (one CSS custom property each); `@if (...) { rules } else { rules }` toggles rules; `@@` is a literal `@`; `@media`, `@keyframes`, ... stay CSS.
- `@module { }` (one per file) is module-level TypeScript: constants, types, helpers, markup values; other files import its exports from the `.xzor`. It can't read component members.

## Lifecycle

`protected override onInitialized()` / `onInitializedAsync()` once; `onParametersSet()` / `onParametersSetAsync()` on mount and when props change; then render; then `onAfterRender(first: boolean)`. `shouldRender()` can skip a render, `dispose()` runs on removal. A resolved `...Async` promise re-renders.

## Slots (layouts and wrappers)

```xzor
@* Card.xzor *@
<section class="card">
  @slot:header { <h3>Untitled</h3> }   @* named slot with fallback *@
  @slot                                @* default slot (this is Blazor's @Body / ChildContent) *@
</section>
```

```xzor
<Card>
  @slot header { <em>Today</em> }
  <p>Everything else fills the default slot.</p>
</Card>
```

Slots can pass data: `@slot:item(todo)` in the component, `@slot item(t) { <b>@t.text</b> }` in the parent.

## Cascading values

Provider: `@cascade:theme(currentTheme) { @slot }`. Consumer, at any depth: `@code { @Cascade theme!: string; }` (or `@Cascade("theme") mode!: string;`). Pass a new object to notify; in-place mutation is not detected.

## Pages and routing

```xzor
@* pages/TodoPage.xzor *@
@page "/todos/:id"
@code { id = 0; }                      @* ":id" fills the prop, converted to its type *@
<h2>Todo @id</h2>
```

One `Routes.xzor` (never itself a `@page`) holds the router and the layouts:

```xzor
@import MainLayout from "./layouts/MainLayout.xzor"

@ClientRoutes(route) {
  @notFound { <p>Nothing at @route.path</p> }
  @catch(error) { <p class="error">@(String(error))</p> }
  @default(page) { <MainLayout>@page</MainLayout> }
}
```

- `@page` works in any `.xzor` of the project (a `pages/` folder is only a convention). The component's class name is its file name.
- A layout is an ordinary component with `@slot` where the page goes.
- Typed links: `@import { href } from "./routes"` (relative path; the table is generated), then `<a href="@href.TodoPage({ id: 3 })">`. A page without parameters needs no argument: `href.About()`.
- `@import { NavLink } from "@source-crafter/xzor-runtime"`, then `<NavLink href="/" match="exact">Home</NavLink>`: it adds `class="active"` and `aria-current="page"` on its route; `match="prefix"` is the default.
- Animated page changes: call `viewTransitions(true)` (from `@source-crafter/xzor-runtime`) in `main.ts`; give an element the same `view-transition-name` on both pages to morph it.
- Plain `<a href="/about">` links navigate without reloading.
- Tag routes with `@page "/admin" as admin` and give them a layout with `@admin(page) { <AdminLayout>@page</AdminLayout> }`.
- Served under a sub-path (GitHub Pages): add `<base href="/repo/">` to `index.html`; routes and `href` follow it.

## Services (compile-time dependency injection)

```ts
// main.ts: the entry. @Mount says which component renders into which element.
import { type IApplication, Mount, Singleton, Scoped } from "@source-crafter/xzor-runtime";
import Routes from "./Routes.xzor";
import { TodoService } from "./services/todos";

@Mount(Routes, "app")                 // <div id="app">
@Singleton(TodoService)               // or @Singleton<ITodos>(TodoService), @Scoped(...), @Transient(...)
export class Application implements IApplication {}
```

```xzor
@import { type TodoService } from "./services/todos"   @* a type import is enough: main.ts creates it *@
@inject TodoService todos             @* "Type name"; then use @todos / this.todos *@
```

- Constructor parameters of services are resolved by type (or by key name for `@Singleton("key", factory)`). Classes are plain; no decorators on them.
- Group reusable registrations in a `@ServiceProvider()` class and add it with `@Import(Provider)` on `Application`.
- Never call `mount()` yourself and don't give an `@inject` component a `constructor`.
- Missing, ambiguous or cyclic services are build errors.

## Models (state that tracks its changes)

Use a model for data that is edited and then saved: a form, a row of a table, anything where you need "what changed", "undo" or "is it valid". For plain UI state, keep using `@code` fields.

```ts
// models/worker.ts
import { Model, Persist, Validate, minValue, required } from "@source-crafter/xzor-runtime/model";

export class Worker extends Model {
  @Validate(required) name = "";
  @Validate(minValue(0)) hours = 0;
  @Persist get payment() { return this.hours * 20; }   // sent with the fields
}
```

```xzor
@import { EntitySet } from "@source-crafter/xzor-runtime/model"
@import { Worker } from "../models/worker"
@code {
  team = EntitySet.track(Worker, [{ name: "Ada", hours: 8 }]);
}
@for (const w of team.view) {
  <input type="number" @bind="w.hours" @bind:event="oninput" /> @w.payment
  <small>@(w.errors.hours?.[0])</small>
  <button @onclick="() => team.delete(w)">Delete</button>
}
<button @onclick="() => team.revertChanges()" disabled="@(!team.hasChanges)">Revert</button>
<button @onclick="() => team.confirmChanges()" disabled="@(team.hasErrors)">Save</button>
```

- Write plain fields. The build turns them into tracked ones, and warns on stderr when a class is not tracked: fix every warning.
- Extend `Model`, or another model class (its fields continue after the base's). Build one with `new Worker(data)` (state Unchanged) or `new Worker()` (Detached; the first edit makes it Added). If you write a constructor, call `this.assign(data)` in it.
- A component that reads a model while it renders draws again when that value changes, even if the change comes from a service or a timer. Do not call `stateHasChanged()` for models.
- `hasState(State.Modified | ...)` (`State.Detached | Unchanged | Added | Deleted | Modified`, from `.../model`; there is no `state` property), `markAdded()`/`markModified()`/`markUnchanged()`/`markDeleted()`, `changes` (what to send to the server, `null` if nothing; the state is sent as `$$`, and `$$` in constructor data sets it), `revertChanges()`, `confirmChanges(serverValues?)`, `hasErrors`, `errors` (messages per field, filled after the first edit), `hasValidChanges`.
- Decorators: `@Validate(...)`, `@Persist` (a getter sent with the fields), `@Ignore` (kept out of `changes`), `@Untracked` (a plain field). Validators: `required`, `email`, `phone`, `maxLength`, `minLength`, `requiredIdValue`, `nonZero`, `minValue`, `maxValue`.
- `EntitySet.track(Type, items)` is a list of models: `delete(item)`, `view` (without deleted), `changes`, `hasChanges`, `hasErrors`, `revertChanges()`, `confirmChanges(serverItems?)`. Change it with `push`, `splice`, ...; `set[i] = x` is not noticed. Read it through `view` or `for...of` (not `length`, an index or `set.map`) so the reader follows pushes and deletes.
- Needs `"ESNext.Decorators"` in the tsconfig `lib`. Not supported: plain object graphs with cycles, one set held by two models.

## Fine components (the default)

Every component is compiled with no render pass: the DOM is built once and each dynamic part updates alone when a field it reads changes. Write `@render` on the first line only to get the virtual-DOM render pass instead.

- Its `@code` fields are tracked like a model's: `count++` in a handler updates the page. Never call `stateHasChanged()` for that; call it only after changing something untracked (a plain array's `push`, an object's property).
- Put list data in an `EntitySet` (or reassign a plain array) and loop with `@for (const x of list.view)`: rows are kept by identity.
- Totals and other derived values are plain expressions (`@team.view.reduce((s, w) => s + w.hours, 0)`); no extra fields or setters.
- The tsconfig `paths` (when used) must map `@source-crafter/xzor-runtime/model` as well as `@source-crafter/xzor-runtime`.

## Hot reload and PWA

- `xzor dev` hot reload: saving a `.xzor` patches the changed components in the open page and keeps their state; other changes reload. A `#private` member, a new import or a changed base class reload too, and arrow-function fields keep old code until a reload.
- To make the app installable and offline, add `manifest.webmanifest` next to `index.html` (`name`, `short_name`, `start_url: "./"`, `scope: "./"`, `display`, a 192x192 and a 512x512 icon, both files must exist) and `<link rel="manifest" href="manifest.webmanifest">` in `index.html`. No decorator or code is needed.
- `xzor build` then writes `sw.js` beside `index.html` and registers it (never in `xzor dev`). Don't edit it: it is generated and gitignored, but it must be deployed with the app. Offline loads fall back to the cached app; a new deploy shows up on the second load (the first fetches it in the background). Fix any `xzor: manifest.webmanifest: ...` warning.

## Common mistakes

| Wrong (Blazor or guess) | Right |
|---|---|
| `createApp(App).mount(...)`, `app.services.add...` | `@Mount(App, "app")` + `@Singleton(...)` on `Application` in `main.ts` |
| `<Router>`, `<RouteView>`, `<Found>` | `@ClientRoutes(route) { @default(page) { ... } }` in `Routes.xzor` |
| `@inherits LayoutComponentBase`, `@Body` | a plain component with `@slot` |
| `@foreach (var x in xs)` | `@for (const x of xs)` |
| imports inside `@code`, `@using` | `@import ...` at the top |
| `NavLinkMatch.All` | `match="exact"` |
| `<script src="main.ts">` | `<script type="module" src="./dist/main.js">` |
| `StateHasChanged()` | `this.stateHasChanged()` |
| TypeScript 5, `experimentalDecorators` | TypeScript 7, standard decorators |
| `@("<")` to print `<` | `&lt;` (HTML character references are decoded, like in Razor) |
