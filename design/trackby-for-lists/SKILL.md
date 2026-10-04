---
id: angular.performance.trackby-for-lists
name: TrackBy for Lists
description: >
  Prevents unnecessary DOM recreation in Angular lists by using trackBy with *ngFor or track expressions with @for.
stack:
  - Angular
  - TypeScript
category: performance
status: stable
version: 0.10.0
owner: NgAutoPilot
triggers:
  - ngFor
  - "@for"
  - trackBy
  - track expression
  - large list
  - DOM recreation
---

# TrackBy for Lists

## Purpose

Use this skill to keep Angular list rendering stable by giving Angular a reliable identity for each item. The goal is to avoid unnecessary DOM destruction and recreation when arrays are refreshed, sorted, filtered, or replaced.
If the issue is broader list rendering cost, defer to `list-rendering-optimization`; this skill owns identity tracking specifically.

## When to Use

Use this skill when:

- A template renders a list with `*ngFor` or `@for`.
- List items come from an API, observable, signal, search result, or state update.
- A list can be reordered, filtered, paginated, or refreshed.
- Inputs, focus, animations, or expanded rows are reset unexpectedly.
- The task mentions slow lists or unnecessary DOM updates.
- The list contains child components, form controls, or locally managed UI state.

## Do

For `*ngFor`, use a stable `trackBy` function:

```html
<li *ngFor="let item of items; trackBy: trackByItemId">{{ item.name }}</li>
```

```ts
trackByItemId(_index: number, item: ItemViewModel): string {
  return item.id;
}
```

For Angular control flow with `@for`, use a stable `track` expression:

```html
@for (item of items(); track item.id) {
<li>{{ item.name }}</li>
}
```

Use a domain identifier when possible. If no stable ID exists, create one at the mapping boundary rather than relying on object identity.
When the project uses `@for`, prefer `track item.id` or an equivalent stable key instead of index-based tracking.

## Do Not

Avoid rendering lists without a stable identity:

```html
<li *ngFor="let item of items">{{ item.name }}</li>
```

Avoid unstable tracking values:

```html
@for (item of items; track buildRandomKey(item)) {
<li>{{ item.name }}</li>
}
```

Avoid using the index as identity for lists that can be reordered, inserted into, deleted from, or filtered:

```ts
trackByIndex(index: number): number {
  return index;
}
```

Avoid track keys that change between renders, such as random values, timestamps, or array positions in mutable lists.

## Review Checklist

- [ ] Every non-trivial Angular list has `trackBy` or `track`.
- [ ] The tracking value is stable across refreshes.
- [ ] The tracking value is unique within the rendered list.
- [ ] Index tracking is used only for static lists that never reorder or mutate in the middle.
- [ ] Tracking logic does not allocate random or time-based values.
- [ ] The change preserves focus, animation, and expanded-row behavior.
- [ ] List-local forms, child component state, and selection state are preserved after refresh.

## Expected Output

1. Find Angular lists that lack stable identity tracking.
2. Select the safest available item identifier.
3. Add `trackBy` for `*ngFor` or `track` for `@for`.
4. Avoid unrelated template refactors.
5. Add or update tests when list identity affects behavior.
