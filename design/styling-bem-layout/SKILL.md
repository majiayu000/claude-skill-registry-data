---
name: styling-bem-layout
kind: pattern
rule: styling-bem
description: Pattern of rule styling-bem. Load when assembling a section screen, a form, a panel or a dialog. Blocks of the shared layer, markup through rtBlock and rtElem, your own element in a foreign subtree, the sign that an edit goes to the wrong place. Kit component styles — pattern styling-bem-component.
---
<!-- rt-kit v0.34.0 · patterns/styling-bem-layout.md · 9ca221e21688 · правится надстройкой, не здесь -->

# A screen on the shared layout layer

Pattern of the rule `styling-bem`. What must be true — the law
`docs/constitution/frontend-application.md`.

## When to use

- A section screen, a form, the content of a panel or of a modal window is being assembled.
- Layout appears in the styles file of a screen.

## The styles file of a screen is empty by default

The layout is declared once in the application's shared layer (`apps/<app>/src/styles/`), and
the screen only applies it. The admin has four blocks, the site has one:

| Block                 | What it lays out                                                |
| --------------------- | --------------------------------------------------------------- |
| `<prefix>-page`       | a section screen: title, toolbar, scrolling, table, pagination  |
| `<prefix>-form`       | a form with card sections and rows of fields                    |
| `<prefix>-panel`      | the content of the edit panel                                   |
| `<prefix>-window`     | the content of a modal window                                   |
| `<prefix>-site-page`  | the site's content column: section title and the intro paragraph |

The block goes on the host, the elements get their classes from `rtBlock` at the root of the
template:

```typescript
host: { class: '<prefix>-page' },
```

```html
<ng-container rtBlock="<prefix>-page">
    <header rtElem="header">
        <div rtElem="header-main">
            <h1 rtElem="title">{{ 'bookingsTitle' | transloco }}</h1>
            <p rtElem="hint">{{ 'bookingsHint' | transloco }}</p>
        </div>
    </header>
</ng-container>
```

`rtBlock` on `<ng-container>` sets no class — the node is a comment. A second carrier of the
block class is not needed, nor a `<section>` wrapper of your own.

## Your own element in a foreign subtree

Both directives on one element; the block class is not set then, only the element class:

```html
<div rtBlock="<prefix>-bookings-page" rtElem="confirm"></div>
```

The class comes out as `<prefix>-bookings-page__confirm`, and the descendants inside count from
the same block.

## What stays in the screen file

Only what belongs to this one screen and does not ask for the shared layer — the calendar grid,
the map on the property page, the conversation feed. Next to it, write why it is not shared.

## Common misses

- `display: flex` with `gap` and `padding` on `:host` in the screen file — that is layout.
  Screens that look alike drift apart from it: the page title was declared in eleven components
  in three different font sizes.
- `rtElem` without an ancestor with `rtBlock`: rendering fails at runtime, the build and the
  lint are silent.
- A class whose rule was removed while `rtElem` stayed in the template: caught by
  `npm run check:styles`.
- An element of a foreign block in a foreign subtree: the block name arrives by injection, and
  there is nothing to mix it in with.
