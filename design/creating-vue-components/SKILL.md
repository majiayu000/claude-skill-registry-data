---
name: creating-vue-components
description: Guides creating Vue 3 components with glass-morphism UI for the anime extension. Use when building UI components, styling with Tailwind, or implementing the design system.
---

# Creating Vue Components

Vue 3 component patterns with glass-morphism design for AnimeList.

## Component Template

```vue
<script setup lang="ts">
import { ref } from "vue";

interface Props {
    title: string;
    count?: number;
}

const props = withDefaults(defineProps<Props>(), {
    count: 0,
});

const emit = defineEmits<{
    (e: "update", value: number): void;
}>();
</script>

<template>
    <div
        data-testid="component-name"
        class="rounded-xl border border-white/20 bg-white/10 p-6 backdrop-blur-xs"
    >
        <!-- Content -->
    </div>
</template>
```

## Design System

### Background Gradients

```vue
<!-- Full-screen gradient -->
<div class="bg-gradient-to-br from-purple-600 via-purple-700 to-pink-600">

<!-- Animated particles (optional) -->
<div class="fixed inset-0 opacity-10">
    <div class="absolute left-8 top-12 h-3 w-3 animate-pulse rounded-full bg-white"></div>
    <div class="absolute right-16 top-20 h-2 w-2 animate-ping rounded-full bg-pink-300"></div>
</div>
```

### Glass Cards

```vue
<!-- Primary card -->
<div class="rounded-2xl border border-white/20 bg-white/10 p-8 backdrop-blur-xs">

<!-- Interactive card -->
<div class="rounded-xl border border-white/20 bg-white/10 p-6 backdrop-blur-xs
            transition-all duration-300 hover:border-white/30 hover:bg-white/15
            hover:shadow-lg hover:shadow-black/20">
```

### Typography

```vue
<!-- Headings -->
<h1 class="text-3xl font-bold text-white drop-shadow-md">Page Title</h1>
<h2 class="text-2xl font-bold text-white drop-shadow-md">Section</h2>
<h3 class="text-lg font-semibold text-white drop-shadow-xs">Card Title</h3>

<!-- Body text -->
<p class="leading-relaxed text-white/90 drop-shadow-xs">Description</p>
<p class="text-lg text-white/80 drop-shadow-xs">Subtitle</p>

<!-- Stats -->
<p class="text-2xl font-bold text-purple-200 drop-shadow-xs">12</p>
<p class="text-2xl font-bold text-green-200 drop-shadow-xs">87</p>
```

### Buttons

```vue
<!-- Primary -->
<button class="rounded-xl border border-white/30 bg-white/20 px-6 py-3
               font-medium text-white backdrop-blur-xs transition-all duration-200
               hover:border-white/40 hover:bg-white/30 hover:shadow-lg
               hover:shadow-black/20 active:scale-95">
    Button
</button>

<!-- Secondary -->
<button class="rounded-lg border border-white/20 bg-white/10 px-4 py-2
               text-sm font-medium text-white/90 backdrop-blur-xs
               transition-all duration-200 hover:bg-white/20 active:scale-95">
    Secondary
</button>
```

### Navigation

```vue
<RouterLink
    class="group flex items-center gap-3 rounded-xl border border-transparent
           px-4 py-3 text-sm font-medium text-white/90 transition-all duration-200
           hover:border-white/20 hover:bg-white/10 hover:text-white
           hover:shadow-md hover:shadow-black/20 active:scale-95"
    :class="{
        'border-white/30 bg-white/15 text-white shadow-md shadow-black/20': isActive,
    }"
>
    <span class="text-lg drop-shadow-xs">📺</span>
    <span>Watch Lists</span>
</RouterLink>
```

### Icons (Emoji System)

```vue
<span class="text-lg drop-shadow-xs">🏠</span>  <!-- Home -->
<span class="text-lg drop-shadow-xs">📺</span>  <!-- Watch Lists -->
<span class="text-lg drop-shadow-xs">⭐</span>  <!-- Favorites -->
<span class="text-lg drop-shadow-xs">⚙️</span>  <!-- Settings -->
<span class="text-2xl drop-shadow-xs">▶️</span> <!-- Currently Watching -->
<span class="text-2xl drop-shadow-xs">📝</span> <!-- Plan to Watch -->
```

### Brand Icon

```vue
<div class="flex h-8 w-8 items-center justify-center rounded-lg
            border border-white/30 bg-white/20 backdrop-blur-xs">
    <img src="/assets/images/darkness_32x32.png"
         alt="Darkness from KonoSuba"
         class="h-6 w-6 rounded-sm" />
</div>
```

## Layout Patterns

### Sidebar

```vue
<aside class="flex w-64 flex-col border-r border-white/20 bg-black/30
              text-white backdrop-blur-xs">
    <div class="flex h-16 items-center justify-center border-b border-white/20 bg-black/40">
        <!-- Brand -->
    </div>
    <nav class="flex-1 space-y-2 p-4">
        <!-- Nav items -->
    </nav>
</aside>
```

### Header

```vue
<header class="border-b border-white/20 bg-black/20 px-6 py-4 backdrop-blur-xs">
    <div class="flex items-center justify-between">
        <nav class="flex items-center space-x-2 text-sm text-white/80">
            <!-- Breadcrumbs -->
        </nav>
    </div>
</header>
```

### Grids

```vue
<div class="grid grid-cols-1 gap-6 md:grid-cols-3">  <!-- 3-col -->
<div class="grid grid-cols-1 gap-6 md:grid-cols-2">  <!-- 2-col -->
<div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">  <!-- 4-col -->
```

## Color Palette

| Purpose | Classes |
|---------|---------|
| Background | `from-purple-600 via-purple-700 to-pink-600` |
| Glass | `bg-white/10`, `bg-white/20` |
| Borders | `border-white/20`, `border-white/30` |
| Text | `text-white`, `text-white/90`, `text-white/80` |
| Purple accent | `text-purple-200`, `bg-purple-300` |
| Pink accent | `text-pink-200`, `bg-pink-300` |
| Success | `text-green-200` |
| Info | `text-blue-200` |

## Testing Requirements

Always include `data-testid` attributes:

```vue
<div data-testid="anime-card">
<button data-testid="submit-button">
<input data-testid="search-input" />
```

Test pattern:

```typescript
import { mount } from "@vue/test-utils";

it("should render", () => {
    const wrapper = mount(Component);
    expect(wrapper.find('[data-testid="anime-card"]').exists()).toBe(true);
});
```

## Popup Constraints

```vue
<!-- Fixed 320x240 dimensions -->
<div class="h-60 w-80 overflow-hidden">
```

## Checklist

- [ ] Use `<script setup lang="ts">`
- [ ] Apply glass-morphism (`bg-white/10 backdrop-blur-xs border-white/20`)
- [ ] Include `data-testid` attributes
- [ ] Use typography with `drop-shadow-xs/md`
- [ ] Add hover/active transitions
- [ ] Mobile-first responsive design
- [ ] Proper semantic HTML
