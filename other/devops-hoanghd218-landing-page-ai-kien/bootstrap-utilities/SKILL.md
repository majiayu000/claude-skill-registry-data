---
name: bootstrap-utilities
description: This skill should be used when the user asks about Bootstrap utilities, Bootstrap spacing utilities, Bootstrap margin utilities, Bootstrap padding utilities, Bootstrap display utilities, Bootstrap flex utilities, Bootstrap text utilities, Bootstrap color utilities, Bootstrap background utilities, Bootstrap border utilities, Bootstrap shadow utilities, Bootstrap sizing utilities, Bootstrap position utilities, Bootstrap visibility utilities, Bootstrap overflow utilities, Bootstrap opacity utilities, Bootstrap float utilities, Bootstrap vertical align utilities, Bootstrap link utilities, or needs help with Bootstrap utility classes.
---

# Bootstrap 5.3 Utilities

Bootstrap provides extensive utility classes for rapid styling without custom CSS. These are generated via the Utilities API and can be customized.

## Spacing Utilities

### Margin (m-) and Padding (p-)

```html
<!-- All sides -->
<div class="m-3">Margin 1rem all sides</div>
<div class="p-3">Padding 1rem all sides</div>

<!-- Specific sides -->
<div class="mt-3">Margin top</div>
<div class="mb-3">Margin bottom</div>
<div class="ms-3">Margin start (left in LTR)</div>
<div class="me-3">Margin end (right in LTR)</div>
<div class="mx-3">Margin horizontal (left + right)</div>
<div class="my-3">Margin vertical (top + bottom)</div>

<!-- Same pattern for padding: pt-, pb-, ps-, pe-, px-, py- -->
<div class="px-3 py-2">Horizontal padding 1rem, vertical 0.5rem</div>
```

### Spacing Scale

| Class | Size |
|-------|------|
| `{m\|p}-0` | 0 |
| `{m\|p}-1` | 0.25rem (4px) |
| `{m\|p}-2` | 0.5rem (8px) |
| `{m\|p}-3` | 1rem (16px) |
| `{m\|p}-4` | 1.5rem (24px) |
| `{m\|p}-5` | 3rem (48px) |
| `{m\|p}-auto` | auto (margin only) |

### Responsive Spacing

```html
<div class="mt-0 mt-md-3 mt-lg-5">
  No margin, 1rem on md, 3rem on lg+
</div>
```

### Gap Utilities (Flexbox/Grid)

```html
<div class="d-flex gap-3">
  <div>Item 1</div>
  <div>Item 2</div>
</div>

<div class="d-grid gap-2">
  <button class="btn btn-primary">Button 1</button>
  <button class="btn btn-primary">Button 2</button>
</div>

<!-- Row and column gaps -->
<div class="d-grid gap-0 row-gap-3 column-gap-3">...</div>
```

## Display Utilities

```html
<div class="d-none">Hidden</div>
<div class="d-inline">Inline</div>
<div class="d-inline-block">Inline-block</div>
<div class="d-block">Block</div>
<div class="d-flex">Flexbox</div>
<div class="d-inline-flex">Inline flex</div>
<div class="d-grid">Grid</div>
<div class="d-table">Table</div>
<div class="d-table-row">Table row</div>
<div class="d-table-cell">Table cell</div>

<!-- Responsive display -->
<div class="d-none d-md-block">Hidden on xs/sm, block on md+</div>
<div class="d-block d-lg-none">Visible until lg</div>

<!-- Print display -->
<div class="d-print-none">Hidden in print</div>
<div class="d-none d-print-block">Only visible in print</div>
```

## Text Utilities

### Alignment

```html
<p class="text-start">Left aligned (start)</p>
<p class="text-center">Center aligned</p>
<p class="text-end">Right aligned (end)</p>

<!-- Responsive alignment -->
<p class="text-start text-md-center text-lg-end">
  Left on xs/sm, center on md, right on lg+
</p>
```

### Transform

```html
<p class="text-lowercase">lowercased text</p>
<p class="text-uppercase">UPPERCASED TEXT</p>
<p class="text-capitalize">Capitalized Text</p>
```

### Decoration

```html
<a href="#" class="text-decoration-none">No underline</a>
<p class="text-decoration-underline">Underlined text</p>
<p class="text-decoration-line-through">Strikethrough text</p>
```

### Wrapping and Overflow

```html
<div class="text-wrap">Text that wraps normally</div>
<div class="text-nowrap">Text that won't wrap</div>
<p class="text-break">Longwordthatwillbreaktopreventoverflow</p>
<p class="text-truncate" style="max-width: 150px;">
  This text is truncated with ellipsis...
</p>
```

### Font Weight and Style

```html
<p class="fw-bold">Bold text</p>
<p class="fw-bolder">Bolder text (relative)</p>
<p class="fw-semibold">Semibold text</p>
<p class="fw-medium">Medium text</p>
<p class="fw-normal">Normal weight</p>
<p class="fw-light">Light text</p>
<p class="fw-lighter">Lighter text (relative)</p>
<p class="fst-italic">Italic text</p>
<p class="fst-normal">Normal style</p>
```

### Line Height

```html
<p class="lh-1">Line height 1</p>
<p class="lh-sm">Small line height</p>
<p class="lh-base">Base line height</p>
<p class="lh-lg">Large line height</p>
```

## Flexbox Utilities

### Direction

```html
<div class="d-flex flex-row">Horizontal</div>
<div class="d-flex flex-row-reverse">Horizontal reversed</div>
<div class="d-flex flex-column">Vertical</div>
<div class="d-flex flex-column-reverse">Vertical reversed</div>
```

### Justify Content

```html
<div class="d-flex justify-content-start">Start</div>
<div class="d-flex justify-content-end">End</div>
<div class="d-flex justify-content-center">Center</div>
<div class="d-flex justify-content-between">Space between</div>
<div class="d-flex justify-content-around">Space around</div>
<div class="d-flex justify-content-evenly">Space evenly</div>
```

### Align Items

```html
<div class="d-flex align-items-start">Top</div>
<div class="d-flex align-items-end">Bottom</div>
<div class="d-flex align-items-center">Center</div>
<div class="d-flex align-items-baseline">Baseline</div>
<div class="d-flex align-items-stretch">Stretch</div>
```

### Align Self

```html
<div class="align-self-start">Top</div>
<div class="align-self-center">Center</div>
<div class="align-self-end">Bottom</div>
```

### Flex Wrap

```html
<div class="d-flex flex-wrap">Wrap</div>
<div class="d-flex flex-nowrap">No wrap</div>
<div class="d-flex flex-wrap-reverse">Wrap reverse</div>
```

### Flex Grow/Shrink

```html
<div class="flex-grow-0">Don't grow</div>
<div class="flex-grow-1">Grow to fill</div>
<div class="flex-shrink-0">Don't shrink</div>
<div class="flex-shrink-1">Can shrink</div>
<div class="flex-fill">Fill available space</div>
```

### Order

```html
<div class="order-0">First</div>
<div class="order-1">Second</div>
<div class="order-2">Third</div>
<div class="order-first">Very first (-1)</div>
<div class="order-last">Very last (6)</div>
```

## Background Utilities

```html
<div class="bg-primary">Primary</div>
<div class="bg-secondary">Secondary</div>
<div class="bg-success">Success</div>
<div class="bg-danger">Danger</div>
<div class="bg-warning">Warning</div>
<div class="bg-info">Info</div>
<div class="bg-light">Light</div>
<div class="bg-dark">Dark</div>
<div class="bg-body">Body</div>
<div class="bg-body-secondary">Body secondary</div>
<div class="bg-body-tertiary">Body tertiary</div>
<div class="bg-white">White</div>
<div class="bg-black">Black</div>
<div class="bg-transparent">Transparent</div>

<!-- Opacity -->
<div class="bg-primary bg-opacity-75">75%</div>
<div class="bg-primary bg-opacity-50">50%</div>
<div class="bg-primary bg-opacity-25">25%</div>
<div class="bg-primary bg-opacity-10">10%</div>

<!-- Gradient -->
<div class="bg-primary bg-gradient">Gradient</div>
```

## Text Color Utilities

```html
<p class="text-primary">Primary text</p>
<p class="text-secondary">Secondary text</p>
<p class="text-success">Success text</p>
<p class="text-danger">Danger text</p>
<p class="text-warning">Warning text</p>
<p class="text-info">Info text</p>
<p class="text-muted">Muted text</p>
<p class="text-body">Body text</p>
<p class="text-body-secondary">Body secondary</p>
<p class="text-body-tertiary">Body tertiary</p>
<p class="text-body-emphasis">Body emphasis</p>
<p class="text-black">Black text</p>
<p class="text-white bg-dark">White text</p>

<!-- Opacity -->
<p class="text-primary text-opacity-75">75% opacity</p>
<p class="text-primary text-opacity-50">50% opacity</p>
<p class="text-primary text-opacity-25">25% opacity</p>
```

## Border Utilities

```html
<!-- Add borders -->
<div class="border">All sides</div>
<div class="border-top">Top</div>
<div class="border-end">End</div>
<div class="border-bottom">Bottom</div>
<div class="border-start">Start</div>

<!-- Remove borders -->
<div class="border-0">No border</div>
<div class="border-top-0">No top border</div>

<!-- Border color -->
<div class="border border-primary">Primary</div>
<div class="border border-success">Success</div>
<div class="border border-danger">Danger</div>

<!-- Border width -->
<div class="border border-1">1px</div>
<div class="border border-2">2px</div>
<div class="border border-3">3px</div>
<div class="border border-4">4px</div>
<div class="border border-5">5px</div>

<!-- Border radius -->
<div class="rounded">Rounded</div>
<div class="rounded-0">No radius</div>
<div class="rounded-1">Small radius</div>
<div class="rounded-2">Default radius</div>
<div class="rounded-3">Large radius</div>
<div class="rounded-4">XL radius</div>
<div class="rounded-5">XXL radius</div>
<div class="rounded-circle">Circle</div>
<div class="rounded-pill">Pill</div>
<div class="rounded-top">Top only</div>
<div class="rounded-end">End only</div>
<div class="rounded-bottom">Bottom only</div>
<div class="rounded-start">Start only</div>
```

## Shadow Utilities

```html
<div class="shadow-none">No shadow</div>
<div class="shadow-sm">Small shadow</div>
<div class="shadow">Regular shadow</div>
<div class="shadow-lg">Large shadow</div>
```

## Sizing Utilities

### Width

```html
<div class="w-25">25% width</div>
<div class="w-50">50% width</div>
<div class="w-75">75% width</div>
<div class="w-100">100% width</div>
<div class="w-auto">Auto width</div>
<div class="mw-100">Max-width 100%</div>
<div class="vw-100">100vw</div>
<div class="min-vw-100">Min 100vw</div>
```

### Height

```html
<div class="h-25">25% height</div>
<div class="h-50">50% height</div>
<div class="h-75">75% height</div>
<div class="h-100">100% height</div>
<div class="h-auto">Auto height</div>
<div class="mh-100">Max-height 100%</div>
<div class="vh-100">100vh</div>
<div class="min-vh-100">Min 100vh</div>
```

## Position Utilities

### Position Values

```html
<div class="position-static">Static (default)</div>
<div class="position-relative">Relative</div>
<div class="position-absolute">Absolute</div>
<div class="position-fixed">Fixed</div>
<div class="position-sticky">Sticky</div>
```

### Placement

```html
<!-- Edge positioning (0%, 50%, 100%) -->
<div class="position-absolute top-0 start-0">Top left</div>
<div class="position-absolute top-0 end-0">Top right</div>
<div class="position-absolute bottom-0 start-0">Bottom left</div>
<div class="position-absolute bottom-0 end-0">Bottom right</div>
<div class="position-absolute top-50 start-50">Center (needs transform)</div>
```

### Centering with Translate

```html
<!-- Center an element -->
<div class="position-absolute top-50 start-50 translate-middle">
  Perfectly centered
</div>

<!-- Center horizontally only -->
<div class="position-absolute start-50 translate-middle-x">
  Horizontally centered
</div>

<!-- Center vertically only -->
<div class="position-absolute top-50 translate-middle-y">
  Vertically centered
</div>
```

### Common Pattern: Badge Positioning

```html
<button class="btn btn-primary position-relative">
  Notifications
  <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
    99+
  </span>
</button>
```

## Overflow Utilities

```html
<div class="overflow-auto">Auto</div>
<div class="overflow-hidden">Hidden</div>
<div class="overflow-visible">Visible</div>
<div class="overflow-scroll">Scroll</div>

<div class="overflow-x-auto">Horizontal auto</div>
<div class="overflow-x-hidden">Horizontal hidden</div>
<div class="overflow-y-auto">Vertical auto</div>
<div class="overflow-y-hidden">Vertical hidden</div>
```

## Opacity Utilities

```html
<div class="opacity-100">100%</div>
<div class="opacity-75">75%</div>
<div class="opacity-50">50%</div>
<div class="opacity-25">25%</div>
<div class="opacity-0">0%</div>
```

## Visibility Utilities

```html
<div class="visible">Visible</div>
<div class="invisible">Invisible (takes space)</div>
```

## Z-Index Utilities

```html
<div class="z-n1">-1</div>
<div class="z-0">0</div>
<div class="z-1">1</div>
<div class="z-2">2</div>
<div class="z-3">3</div>
```

## Object Fit Utilities

```html
<img class="object-fit-contain" src="...">
<img class="object-fit-cover" src="...">
<img class="object-fit-fill" src="...">
<img class="object-fit-scale" src="...">
<img class="object-fit-none" src="...">
```

## Interaction Utilities

```html
<div class="user-select-all">Select all on click</div>
<div class="user-select-auto">Default selection</div>
<div class="user-select-none">Cannot select</div>
<div class="pe-none">Pointer events none</div>
<div class="pe-auto">Pointer events auto</div>
```

## Float Utilities

Float utilities position elements to the left or right of their container, allowing text to wrap around them.

```html
<div class="float-start">Float start (left in LTR)</div>
<div class="float-end">Float end (right in LTR)</div>
<div class="float-none">No float</div>

<!-- Responsive floats -->
<div class="float-sm-start">Float start on sm+</div>
<div class="float-md-end">Float end on md+</div>
<div class="float-lg-none">No float on lg+</div>
```

| Class | Description |
|-------|-------------|
| `float-start` | Float left (LTR) |
| `float-end` | Float right (LTR) |
| `float-none` | Remove float |

Responsive: `float-{breakpoint}-{start|end|none}`

**Note**: Modern layouts typically use flexbox or grid instead of floats. Floats remain useful for wrapping text around images.

## Vertical Align Utilities

Control vertical alignment of inline, inline-block, inline-table, and table cell elements.

```html
<span class="align-baseline">baseline</span>
<span class="align-top">top</span>
<span class="align-middle">middle</span>
<span class="align-bottom">bottom</span>
<span class="align-text-top">text-top</span>
<span class="align-text-bottom">text-bottom</span>
```

| Class | Alignment |
|-------|-----------|
| `align-baseline` | Baseline (default) |
| `align-top` | Top of line |
| `align-middle` | Middle of line |
| `align-bottom` | Bottom of line |
| `align-text-top` | Top of parent's font |
| `align-text-bottom` | Bottom of parent's font |

**Note**: These work on inline/inline-block elements and table cells, not block elements. For block vertical alignment, use flexbox (`align-items-*`).

## Link Utilities

Style links with opacity, underline color, offset, and hover effects. Added in Bootstrap 5.3.

```html
<!-- Link opacity -->
<a href="#" class="link-opacity-10">10% opacity</a>
<a href="#" class="link-opacity-25">25% opacity</a>
<a href="#" class="link-opacity-50">50% opacity</a>
<a href="#" class="link-opacity-75">75% opacity</a>
<a href="#" class="link-opacity-100">100% opacity</a>

<!-- Hover opacity -->
<a href="#" class="link-opacity-50-hover">50% on hover</a>

<!-- Underline color -->
<a href="#" class="link-underline-primary">Primary underline</a>
<a href="#" class="link-underline-secondary">Secondary underline</a>
<a href="#" class="link-underline-success">Success underline</a>

<!-- Underline offset -->
<a href="#" class="link-offset-1">1 offset</a>
<a href="#" class="link-offset-2">2 offset</a>
<a href="#" class="link-offset-3">3 offset</a>

<!-- Underline opacity -->
<a href="#" class="link-underline-opacity-0">No underline</a>
<a href="#" class="link-underline-opacity-25">25% underline</a>
<a href="#" class="link-underline-opacity-50">50% underline</a>

<!-- Combined styling -->
<a href="#" class="link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover">
  Styled link
</a>
```

| Class | Description |
|-------|-------------|
| `link-opacity-{10\|25\|50\|75\|100}` | Link text opacity |
| `link-opacity-{value}-hover` | Opacity on hover |
| `link-underline-{color}` | Underline color |
| `link-offset-{1\|2\|3}` | Underline distance |
| `link-underline-opacity-{0\|10\|25\|50\|75\|100}` | Underline opacity |

## Utilities API

Bootstrap's utilities are generated via a Sass-based API, allowing full customization.

### API Structure

Each utility is defined as a map with these key options:

| Option | Description |
|--------|-------------|
| `property` | CSS property name (required) |
| `values` | List or map of values (required) |
| `class` | Custom class prefix (optional) |
| `responsive` | Generate responsive variants (default: false) |
| `print` | Generate print variants (default: false) |
| `state` | Generate state variants like `:hover` |
| `css-var` | Output as CSS variables instead of rules |
| `css-variable-name` | Custom CSS variable name (with css-var) |
| `local-vars` | Map of local CSS variables |
| `rfs` | Enable fluid rescaling (default: false) |
| `rtl` | Include in RTL output (default: true) |

**Note**: All utilities include `!important` by default. Disable globally with `$enable-important-utilities: false`.

### Adding Custom Utilities

```scss
@import "bootstrap/scss/functions";
@import "bootstrap/scss/variables";
@import "bootstrap/scss/variables-dark";
@import "bootstrap/scss/maps";
@import "bootstrap/scss/mixins";
@import "bootstrap/scss/utilities";

$utilities: map-merge(
  $utilities,
  (
    "cursor": (
      property: cursor,
      class: cursor,
      responsive: true,
      values: auto pointer grab grabbing not-allowed
    )
  )
);

@import "bootstrap/scss/utilities/api";
```

### Modifying Existing Utilities

```scss
// Add responsive variants to an existing utility
$utilities: map-merge(
  $utilities,
  (
    "overflow": map-merge(
      map-get($utilities, "overflow"),
      (responsive: true)
    )
  )
);
```

### Removing Utilities

```scss
// Remove entirely
$utilities: map-remove($utilities, "float");

// Or set to null
$utilities: map-merge($utilities, ("float": null));
```

## Common Patterns

Frequently-used utility combinations for real-world scenarios.

### Centered Container (Full Viewport)

```html
<div class="d-flex justify-content-center align-items-center min-vh-100">
  <div class="text-center">
    <h1>Perfectly Centered</h1>
    <p>Both horizontally and vertically</p>
  </div>
</div>
```

### Sticky Footer Layout

```html
<div class="d-flex flex-column min-vh-100">
  <header class="bg-dark text-white p-3">Header</header>
  <main class="flex-grow-1 p-3">Main content</main>
  <footer class="bg-body-secondary p-3">Footer stays at bottom</footer>
</div>
```

### Card with Spacing and Shadow

```html
<div class="card shadow-sm border-0 rounded-3">
  <div class="card-body p-4">
    <h5 class="card-title mb-3">Title</h5>
    <p class="card-text text-muted mb-0">Content</p>
  </div>
</div>
```

### Responsive Hide/Show

```html
<!-- Hidden on mobile, visible on desktop -->
<div class="d-none d-md-block">Desktop only</div>

<!-- Visible on mobile, hidden on desktop -->
<div class="d-block d-md-none">Mobile only</div>
```

### Icon + Text Alignment

```html
<div class="d-flex align-items-center gap-2">
  <svg>...</svg>
  <span>Text aligned with icon</span>
</div>
```

## When to Use Utilities vs Custom CSS

| Scenario | Recommended Approach |
|----------|---------------------|
| One-off spacing adjustment | Utility classes (`mt-3`, `p-4`) |
| Consistent component styling | Custom component class |
| Responsive show/hide | Display utilities (`d-none d-md-block`) |
| Complex hover/focus states | Custom CSS |
| Values not in Bootstrap scale | Extend via Utilities API or custom CSS |
| Repeated pattern (3+ times) | Extract to custom class |
| Quick prototype | Utilities for speed |
| Production component | Consider extracting repeated utilities |

**Rule of thumb**: If you're applying the same combination of 4+ utilities to multiple elements, consider creating a custom class.

## Additional Resources

### Reference Files

- `references/utilities-reference.md` - Complete utility class reference
- `references/api-customization.md` - Advanced Sass customization examples

### Example Files

- `examples/card-layout.html` - Card styling with spacing, shadows, and borders
- `examples/responsive-utilities.html` - Responsive display and spacing patterns
- `examples/flex-centering.html` - Flexbox centering techniques
