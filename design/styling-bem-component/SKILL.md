---
name: styling-bem-component
kind: pattern
rule: styling-bem
description: Pattern of rule styling-bem. Load when editing the styles of a kit component — the ready-made :host, modifiers, styling tokens, the styling language of the public site, overriding kit defaults. Not for screen layout — that is pattern styling-bem-layout.
---
<!-- rt-kit v0.34.0 · patterns/styling-bem-component.md · 06d54bbd57cd · правится надстройкой, не здесь -->

# Component styles

Pattern of the rule `styling-bem`. What must be true — the law
`docs/constitution/frontend-application.md`.

## When to use

- A kit component is edited — it lives in the package `@rt-tools/ui-kit-v2`, not in this tree.
- The styling of the public site is edited.
- A kit default has to be overridden in a component of your own.

## `:host` — the block itself

The host carries the block class, the layout sits on `:host`, the elements are nested inside:

```scss
:host {
    display: inline-flex;

    .<prefix > -tag {
        display: inline-flex;
        gap: var(--<prefix>-space-1);
        align-items: center;

        &--shape--pill {
            border-radius: var(--<prefix>-radius-full);
        }
    }
}
```

Indent — four spaces. A modifier — `&--<name>` or a class binding on the host
(`[class.<prefix>-component-name--active]="isActive()"`).

A screen outside the kit has no such section: `display: flex` with `gap` and `padding` on
`:host` is layout, and it lives in the application's shared layer.

## Values — only as tokens

```scss
✗ color: #fff;
✗ box-shadow: 0 1px 2px rgb(0 0 0 / 12%);
✓ color: var(--<prefix>-color-surface);
✓ box-shadow: var(--<prefix>-shadow-sm);
```

A composite value is taken as a ready-made token whole, not assembled from parts. SCSS variables
(`$primaryColor`) are not used for styling values at all.

## The styling language of the public site

Tropical premium, photo first:

- a light warm palette — sand, terracotta, palm green, only through `--<prefix>-color-*`;
- an accent serif in headings (`--<prefix>-font-serif`), a humanist sans in the text
  (`--<prefix>-font-sans`);
- large full-screen photos, generous spacing, restrained animations;
- dark overlays over photos — by variables with transparency.

## Overriding a kit default

Styles of a component with `ViewEncapsulation.None` weigh the same as the kit defaults:
`.<prefix>-block__item` and `.<prefix>-kit-item` have one class each, and the outcome is decided
by the order of inclusion. The override is written as a descendant of the block:

```scss
& &__item {
    color: var(--<prefix>-color-text-muted);
}
```

## Common misses

- A stylelint switch-off comment: selectors are joined by nesting, not by disabling the rule.
- `!important`: forbidden, and an inline `width: 100%` on the panel box cannot be overridden
  with it.
- New declarations while moving styles: what exists is moved, new appears only when the task is
  a feature.
- A linter remark that lay in the file before is left alone: all are fixed, new and old alike.
- A `font-family: inherit` of your own in a component: inheritance is switched on globally in
  the `styles.scss` of both applications.
