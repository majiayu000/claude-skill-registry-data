---
name: using-container-queries
description: Use container queries for component-based responsive design with @container syntax and named containers. Use when building portable, reusable components that adapt to parent size instead of viewport.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Using Container Queries

## Purpose

Container queries enable components to respond to their parent container's size instead of the viewport. This creates truly portable, reusable components that work anywhere.

## Basic Container Queries

**Step 1: Mark the container**

```html
<div class="@container">
  <div class="grid grid-cols-1 @sm:grid-cols-2 @lg:grid-cols-4 gap-4">
    <div>Card 1</div>
    <div>Card 2</div>
    <div>Card 3</div>
    <div>Card 4</div>
  </div>
</div>
```

The `@container` class makes an element a container query context.

**Step 2: Use container breakpoints**

Container breakpoint utilities use `@` prefix:

- `@sm:` - Container width ≥ 640px
- `@md:` - Container width ≥ 768px
- `@lg:` - Container width ≥ 1024px
- `@xl:` - Container width ≥ 1280px
- `@2xl:` - Container width ≥ 1536px

## Container vs Viewport Queries

**Viewport queries (viewport width):**

```html
<div class="grid-cols-1 md:grid-cols-2 lg:grid-cols-3"></div>
```

Responds to browser window width.

**Container queries (parent width):**

```html
<div class="@container">
  <div class="grid-cols-1 @md:grid-cols-2 @lg:grid-cols-3"></div>
</div>
```

Responds to parent container width.

## Named Containers

Use named containers for nested container queries:

```html
<div class="@container/main">
  <div class="@container/sidebar">
    <div class="flex flex-col @sm/main:flex-row">
      Main container responsive
    </div>

    <div class="text-sm @md/sidebar:text-base">
      Sidebar container responsive
    </div>
  </div>
</div>
```

**Syntax:** `@container/{name}` for the container, `@{breakpoint}/{name}:` for utilities.

## Portability Patterns

### Reusable Card Component

```html
<div class="@container">
  <article class="bg-white rounded-lg shadow-md p-4 @md:p-6">
    <div class="flex flex-col @md:flex-row @md:gap-6">
      <img class="w-full @md:w-48 rounded-lg" src="/image.jpg" />

      <div class="flex-1 mt-4 @md:mt-0">
        <h2 class="text-lg @md:text-xl @lg:text-2xl font-bold">Card Title</h2>

        <p class="mt-2 text-sm @md:text-base text-gray-600">
          Card description that adapts to container size.
        </p>

        <button class="mt-4 px-3 py-1.5 @md:px-4 @md:py-2 bg-blue-600 text-white rounded-md">
          Read More
        </button>
      </div>
    </div>
  </article>
</div>
```

This card works in:
- Full-width layouts
- Sidebar layouts
- Grid layouts
- Any container size

### Dashboard Widget

```html
<div class="@container">
  <div class="bg-white rounded-lg p-4">
    <div class="flex items-center justify-between">
      <h3 class="text-base @md:text-lg font-semibold">Widget Title</h3>
      <button class="text-xs @md:text-sm text-blue-600">View All</button>
    </div>

    <div class="mt-4 grid grid-cols-1 @sm:grid-cols-2 @lg:grid-cols-3 gap-3 @md:gap-4">
      <div class="p-3 bg-gray-50 rounded">Stat 1</div>
      <div class="p-3 bg-gray-50 rounded">Stat 2</div>
      <div class="p-3 bg-gray-50 rounded">Stat 3</div>
    </div>
  </div>
</div>
```

### Responsive Navigation

```html
<div class="@container/nav">
  <nav class="flex flex-col @md/nav:flex-row @md/nav:items-center gap-2 @md/nav:gap-6">
    <a href="#" class="text-sm @md/nav:text-base">Home</a>
    <a href="#" class="text-sm @md/nav:text-base">About</a>
    <a href="#" class="text-sm @md/nav:text-base">Services</a>
    <a href="#" class="text-sm @md/nav:text-base">Contact</a>
  </nav>
</div>
```

## Complex Layout Example

```html
<div class="@container">
  <div class="grid grid-cols-1 @sm:grid-cols-2 @lg:grid-cols-3 @xl:grid-cols-4 gap-4 @md:gap-6 @lg:gap-8">
    <div class="@container/card">
      <article class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="relative h-32 @md/card:h-48 bg-gradient-to-br from-blue-500 to-purple-600">
          <img class="w-full h-full object-cover" src="/image.jpg" />
        </div>

        <div class="p-3 @md/card:p-4 @lg/card:p-6">
          <h3 class="text-base @md/card:text-lg @lg/card:text-xl font-bold">
            Card Title
          </h3>

          <p class="mt-2 text-xs @md/card:text-sm @lg/card:text-base text-gray-600 line-clamp-2 @lg/card:line-clamp-3">
            Description that adapts based on available space in the card container.
          </p>

          <div class="mt-3 @md/card:mt-4 flex items-center justify-between">
            <span class="text-xs @md/card:text-sm text-gray-500">2 days ago</span>

            <button class="px-2 py-1 @md/card:px-3 @md/card:py-1.5 text-xs @md/card:text-sm bg-blue-600 text-white rounded">
              Read
            </button>
          </div>
        </div>
      </article>
    </div>
  </div>
</div>
```

## Mixing Container and Viewport Queries

You can combine both for maximum control:

```html
<div class="@container">
  <div class="
    grid
    grid-cols-1
    md:grid-cols-2
    lg:grid-cols-3
    @lg:grid-cols-2
    @xl:grid-cols-3
  ">
    Components adapt to both viewport and container
  </div>
</div>
```

**Order matters:** Viewport queries first, then container queries to override.

## Container Query Breakpoints

Default container breakpoints:

| Breakpoint | Min Width |
| ---------- | --------- |
| `@xs`      | 320px     |
| `@sm`      | 640px     |
| `@md`      | 768px     |
| `@lg`      | 1024px    |
| `@xl`      | 1280px    |
| `@2xl`     | 1536px    |

## Custom Container Breakpoints

Define custom container breakpoints in theme:

```css
@theme {
  --container-xs: 20rem;
  --container-sm: 40rem;
  --container-md: 48rem;
  --container-lg: 64rem;
  --container-xl: 80rem;
}
```

## Performance Considerations

Container queries are highly performant in modern browsers. They:

- Use native browser APIs
- Don't require JavaScript
- Trigger efficient reflows
- Work with CSS cascade layers

## Browser Support

Container queries require:
- Safari 16.4+
- Chrome 111+
- Firefox 128+

Same as Tailwind v4's minimum browser requirements.

## Best Practices

1. **Use for component portability** - Container queries excel at making components work anywhere
2. **Name containers when nested** - Use `/name` syntax for clarity
3. **Prefer container queries for components** - Use viewport queries for page-level layouts
4. **Combine with viewport queries** - Use both for maximum flexibility
5. **Test at various sizes** - Verify components work in narrow and wide containers

## Common Patterns

### Sidebar Layout

```html
<div class="flex gap-6">
  <aside class="w-64 @container/sidebar">
    <nav class="space-y-2">
      <a class="block p-2 text-sm @md/sidebar:text-base">Link 1</a>
      <a class="block p-2 text-sm @md/sidebar:text-base">Link 2</a>
    </nav>
  </aside>

  <main class="flex-1 @container/main">
    <div class="grid grid-cols-1 @lg/main:grid-cols-2 gap-4">
      <div>Content 1</div>
      <div>Content 2</div>
    </div>
  </main>
</div>
```

### Product Grid

```html
<div class="@container">
  <div class="grid grid-cols-2 @md:grid-cols-3 @lg:grid-cols-4 @xl:grid-cols-5 gap-4">
    <div class="@container/product">
      <div class="bg-white rounded-lg p-3 @md/product:p-4">
        <img class="w-full aspect-square rounded" src="/product.jpg" />
        <h3 class="mt-2 text-sm @md/product:text-base font-medium">Product</h3>
        <p class="mt-1 text-xs @md/product:text-sm text-gray-600">$99</p>
      </div>
    </div>
  </div>
</div>
```

### Form Layout

```html
<div class="@container">
  <form class="space-y-4 @md:space-y-6">
    <div class="grid grid-cols-1 @md:grid-cols-2 gap-4 @md:gap-6">
      <input class="px-3 py-2 @md:px-4 @md:py-3 border rounded" placeholder="First Name" />
      <input class="px-3 py-2 @md:px-4 @md:py-3 border rounded" placeholder="Last Name" />
    </div>

    <button class="w-full px-4 py-2 @md:px-6 @md:py-3 bg-blue-600 text-white rounded">
      Submit
    </button>
  </form>
</div>
```

## See Also

- RESEARCH.md sections: "Container Queries" and "Usage Patterns"
