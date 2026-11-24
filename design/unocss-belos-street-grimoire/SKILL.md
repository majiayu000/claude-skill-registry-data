---
name: unocss
title: UnoCSS
description: The instant on-demand atomic CSS engine
icon: ⚡
tags: [css, atomic-css, unocss, tailwind]
---

UnoCSS - The instant on-demand atomic CSS engine

### Configuration
- Installation and basic setup → See [configuration](reference/configuration.md)
- Custom rules and shortcuts → See [configuration](reference/configuration.md)
- Theme configuration (colors, breakpoints, fonts) → See [configuration](reference/configuration.md)
- Class writing order → See [configuration](reference/configuration.md)

### Presets
- preset-uno, preset-mini, preset-wind → See [presets](reference/presets.md)
- preset-icons for icon system → See [presets](reference/presets.md)
- preset-attributify for attribute syntax → See [presets](reference/presets.md)
- Custom presets → See [presets](reference/presets.md)

### Shortcuts & Transformers
- Creating reusable shortcuts → See [shortcuts-transformers](reference/shortcuts-transformers.md)
- Dynamic shortcuts → See [shortcuts-transformers](reference/shortcuts-transformers.md)
- transformer-directives for @apply → See [shortcuts-transformers](reference/shortcuts-transformers.md)
- transformer-variant-group → See [shortcuts-transformers](reference/shortcuts-transformers.md)

## Quick Start

```bash
pnpm install -D unocss
```

```ts
// uno.config.ts
import { defineConfig, presetUno, presetIcons, presetAttributify } from 'unocss'

export default defineConfig({
  presets: [
    presetUno(),
    presetAttributify(),
    presetIcons({
      scale: 1.2,
      cdn: 'https://esm.sh/'
    }),
  ],
})
```

```ts
// main.ts
import 'virtual:uno.css'
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
```

## Key Features

- **Instant**: No scanning, generate on-demand
- **Flexible**: Fully customizable
- **Powerful**: Built-in presets for common patterns
- **Lightweight**: Only generate what you use
- **Compatible**: Works with any framework

## Common Patterns

### Basic Classes

```html
<div class="flex items-center justify-between p-4 bg-white shadow-md rounded-lg">
  <h1 class="text-2xl font-bold text-gray-800">Hello UnoCSS</h1>
</div>
```

### Responsive Design

```html
<div class="flex flex-col md:flex-row gap-4">
  <div class="w-full md:w-1/2">Left</div>
  <div class="w-full md:w-1/2">Right</div>
</div>
```

### Dark Mode

```html
<div class="bg-white dark:bg-gray-800 text-gray-900 dark:text-white">
  Content
</div>
```

## Best Practices

1. **Use presets**: Start with preset-uno
2. **Use shortcuts**: Create reusable class combinations
3. **Use transformers**: For directives and variant groups
4. **Organize config**: Keep config modular for large projects

## Resources

- [Official Documentation](https://unocss.dev/)
- [Playground](https://unocss.dev/play)
- [Presets](https://unocss.dev/presets)
