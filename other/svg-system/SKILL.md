---
name: svg-system
description: 'Provides implementation guidance for Angular SVG systems for icons and general SVG images using adaptive and sprite patterns. Use when adding SVG entries to a registry, choosing between adaptive and sprite rendering, applying semantic color roles, fixing dark mode SVG color issues, using CSS mask-image with --icon-url, or wiring reusable directive-based SVG bindings. Keywords: icon, icons, svg image, svg images, adaptive svg, sprite svg, registry, currentColor, color role, dark mode, theme, mask-image, --icon-url, svg, directive, adaptSvg, getAdaptiveSvgColorVar.'
---

# SVG System - Adaptive and Sprite

> Scope note: this skill is for any SVG images (icons, logos, glyphs, decorative marks), not only icon-only workflows.

## Folder/File Structure (Recommended)

```
src/app/shared/
  constants/
    icons.ts
  models/
    icon.model.ts
    index.ts
  directives/
    adapt-svg.directive.ts
  utils/
    adaptive-svg-color.util.ts
public/icons/
```

### Responsibility Split

- `constants/icons.ts`: icon registry entries only (actual icons used by the app).
- `models/icon.model.ts`: icon domain types and type guards.
- `models/index.ts`: model barrel exports.
- `directives/adapt-svg.directive.ts`: DOM style bindings for adaptive SVG rendering.
- `utils/adaptive-svg-color.util.ts`: semantic role to CSS variable mapping.
- `public/icons/`: raw SVG asset files.

---

## When to Use This Skill

- Adding a new SVG entry to a registry (icons or other SVG images)
- Choosing `adaptive` versus `sprite`
- Applying SVG color from semantic tokens
- Fixing SVG color in dark mode
- Standardizing SVG render patterns in Angular templates

---

## Icon Types

### Adaptive Icon

Use `adaptive` for icons that must follow theme tokens at runtime.

```ts
export type AdaptiveIcon = {
  kind: 'adaptive';
  src: string;
  colorRole?: AdaptiveIconColorRole;
};

export type AdaptiveIconColorRole =
  | 'on-primary'
  | 'primary-on-container'
  | 'on-secondary'
  | 'secondary-on-container'
  | 'on-tertiary'
  | 'tertiary-on-container'
  | 'text'
  | 'text-muted'
  | 'success'
  | 'warning'
  | 'error';
```

### Sprite Icon

Use `sprite` for icons rendered from an SVG sprite sheet.

```ts
export type SpriteIcon = {
  kind: 'sprite';
  spritePath: string;
  symbolId: string;
};
```

---

## Best Practice Rules

- Use semantic tokens, not raw colors:
  - `var(--color-on-primary)`
  - `var(--color-primary-on-container)`
- Keep color-role logic adaptive-only.
- Do not use `<img src="...svg">` when you need runtime recoloring.
- For adaptive monochrome icons, use CSS mask with `background-color: currentColor`.
- Keep icon source in `public/icons/` for stable URL-based delivery.

---

## Recommended Adaptive Render Pattern

### 1. Icon definition

```ts
export const APP_ICONS = {
  menu: {
    kind: 'adaptive',
    src: '/icons/menu.svg',
    colorRole: 'primary-on-container',
  },
} as const;
```

### 2. Color var resolver

```ts
export function getAdaptiveIconColorVar(icon: AdaptiveIcon): string {
  switch (icon.colorRole) {
    case 'on-primary':
      return 'var(--color-on-primary)';
    case 'primary-on-container':
      return 'var(--color-primary-on-container)';
    case 'on-secondary':
      return 'var(--color-on-secondary)';
    case 'secondary-on-container':
      return 'var(--color-secondary-on-container)';
    case 'on-tertiary':
      return 'var(--color-on-tertiary)';
    case 'tertiary-on-container':
      return 'var(--color-tertiary-on-container)';
    case 'text':
      return 'var(--color-text)';
    case 'text-muted':
      return 'var(--color-text-muted)';
    case 'success':
      return 'var(--color-success)';
    case 'warning':
      return 'var(--color-warning)';
    case 'error':
      return 'var(--color-error)';
    default:
      return 'currentColor';
  }
}
```

### 3. Angular template binding (cleaner)

Prefer binding one directive input instead of multiple inline style bindings.

```html
<span class="icon" [adaptSvg]="iconVm" aria-hidden="true"></span>
```

```ts
export type AdaptiveSvgIconVm = {
  src: string;
  colorVar: string;
};
```

```ts
import { Directive, input } from '@angular/core';

@Directive({
  selector: '[adaptSvg]',
  host: {
    '[style.color]': 'adaptSvg().colorVar',
    '[style.--icon-url]': 'iconUrl()',
  },
})
export class AdaptiveSvgIconDirective {
  adaptSvg = input.required<AdaptiveSvgIconVm>();

  protected iconUrl(): string {
    return `url(${this.adaptSvg().src})`;
  }
}
```

Why this is cleaner:
- Template stays minimal and readable.
- Icon style contract is centralized in one directive.
- Reuse across headers, buttons, list items, menus, and cards.

### 4. CSS mask style

```scss
.menu-icon {
  width: 1.25rem;
  height: 1.25rem;
  display: block;
  background-color: currentColor;
  mask-image: var(--icon-url);
  mask-repeat: no-repeat;
  mask-position: center;
  mask-size: contain;
  -webkit-mask-image: var(--icon-url);
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-position: center;
  -webkit-mask-size: contain;
}
```

You can rename `.menu-icon` to any semantic class (for example `.icon` or `.action-icon`) based on component context.

---

## Example: Add a New Adaptive SVG

### 1. Add the SVG asset

```text
public/icons/notification.svg
```

### 2. Add it to the registry

```ts
export const APP_ICONS = {
  menu: {
    kind: 'adaptive',
    src: '/icons/menu.svg',
    colorRole: 'primary-on-container',
  },
  notification: {
    kind: 'adaptive',
    src: '/icons/notification.svg',
    colorRole: 'text',
  },
} as const;
```

### 3. Build a view model in a component

```ts
import { APP_ICONS } from '@app/shared/constants/icons';
import { getAdaptiveSvgColorVar } from '@app/shared/utils/adaptive-svg-color.util';
import type { AdaptiveSvgIconVm } from '@app/shared/directives/adapt-svg.directive';

const notificationDef = APP_ICONS.notification;

protected readonly notificationVm: AdaptiveSvgIconVm = {
  src: notificationDef.src,
  colorVar: getAdaptiveSvgColorVar(notificationDef),
};
```

### 4. Render with the directive

```html
<span class="icon" [adaptSvg]="notificationVm" aria-hidden="true"></span>
```

### 5. Optional a11y note

- Decorative SVG: keep `aria-hidden="true"`.
- Informational/action SVG: provide a label on the clickable host element.

---

## Sprite Render Pattern

Use sprite icons where runtime recolor is not tied to adaptive role mapping.

```html
<svg class="icon" aria-hidden="true">
  <use [attr.href]="spritePath + '#' + symbolId"></use>
</svg>
```

Use `currentColor` on the host element if sprite paths are authored to inherit stroke/fill.

---

## Common Pitfalls

- `img` SVG staying dark in dark mode:
  - Cause: external SVG image is not styled by page `color` cascade.
  - Fix: use mask pattern or inline/sprite SVG.
- Hardcoded hex colors in icon styles:
  - Cause: theme mismatch across light and dark modes.
  - Fix: always map through semantic tokens.
- Mixing adaptive role fields into sprite type:
  - Cause: blurred responsibilities and inconsistent API.
  - Fix: keep role fields in `AdaptiveIcon` only.

---

## Quick Checklist

- Icon added to your registry with correct `kind`
- Adaptive icon has optional `colorRole`
- Component binds icon source and color separately
- CSS uses `currentColor` + mask for adaptive URL icons
- No raw color literals for icon tone in component styles
- Dark mode verified
