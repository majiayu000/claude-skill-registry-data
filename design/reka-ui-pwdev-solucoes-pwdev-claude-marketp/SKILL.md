---
name: reka-ui
description: >
  Skill for direct usage of Reka UI v2 headless primitives (the foundation of shadcn-vue).
  Use when you need to compose custom components beyond those available in shadcn-vue,
  understand asChild/as, controlled state, portals, or migrate from Radix Vue.
---

# Skill: Reka UI v2

> Reka UI is the successor to Radix Vue. Foundation of all shadcn-vue@latest components.
> Current version: v2.7.0 (March 2026)

## Installation

```bash
# Via shadcn-vue (recommended — includes styles)
npx shadcn-vue@latest add [component]

# Direct (for unstyled primitives)
npm install reka-ui

# Nuxt — auto-imports
# nuxt.config.ts
export default defineNuxtConfig({
  modules: ['reka-ui/nuxt']
})

# Vite — auto-import resolver
# vite.config.ts
import { RekaResolver } from 'reka-ui/resolver'
import Components from 'unplugin-vue-components/vite'
export default defineConfig({
  plugins: [
    vue(),
    Components({ resolvers: [RekaResolver()] })
  ]
})
```

---

## Fundamental pattern: Root + Parts

Every Reka UI component follows the Root + sub-parts pattern:

```vue
<script setup lang="ts">
import {
  AccordionRoot,
  AccordionItem,
  AccordionHeader,
  AccordionTrigger,
  AccordionContent,
} from 'reka-ui'

const value = ref(['item-1'])
</script>

<template>
  <!-- Root: manages state -->
  <AccordionRoot v-model="value" type="multiple">
    <!-- Item: context for each entry -->
    <AccordionItem value="item-1">
      <!-- Header + Trigger: accessible clickable element -->
      <AccordionHeader>
        <AccordionTrigger>Title</AccordionTrigger>
      </AccordionHeader>
      <!-- Content: expandable panel -->
      <AccordionContent>Item content</AccordionContent>
    </AccordionItem>
  </AccordionRoot>
</template>
```

---

## Controlled vs Uncontrolled state

```vue
<!-- Controlled: you control the state -->
<DialogRoot v-model:open="isOpen">
  <DialogTrigger>Open</DialogTrigger>
  <DialogPortal>
    <DialogContent>...</DialogContent>
  </DialogPortal>
</DialogRoot>

<!-- Uncontrolled: Reka UI manages internally -->
<DialogRoot :default-open="false">
  <DialogTrigger>Open</DialogTrigger>
  <DialogPortal>
    <DialogContent>...</DialogContent>
  </DialogPortal>
</DialogRoot>
```

**Convention**: `default*` prefix for initial values (uncontrolled).
`v-model:open`, `v-model:value`, `v-model:checked` for controlled.

---

## asChild — element composition

`asChild` allows the Reka UI component to apply its behavior to the child element:

```vue
<!-- WITHOUT asChild: Reka renders an extra <button> -->
<DialogTrigger>
  <Button>Open</Button>  <!-- Button inside button = invalid HTML -->
</DialogTrigger>

<!-- WITH asChild: Reka applies handlers to Button directly -->
<DialogTrigger as-child>
  <Button>Open</Button>  <!-- Correct: only one interactive element -->
</DialogTrigger>

<!-- Navigation with RouterLink -->
<NavigationMenuLink as-child>
  <RouterLink to="/dashboard">Dashboard</RouterLink>
</NavigationMenuLink>
```

---

## as — swap the rendered element

```vue
<!-- Primitive: swap div for section -->
<Primitive as="section" class="container">
  <slot />
</Primitive>

<!-- Create reusable base component -->
<script setup lang="ts">
import type { PrimitiveProps } from 'reka-ui'
import { Primitive } from 'reka-ui'

const props = withDefaults(defineProps<PrimitiveProps>(), {
  as: 'div'
})
</script>
<template>
  <Primitive v-bind="props">
    <slot />
  </Primitive>
</template>
```

---

## Portal — render outside the current DOM

```vue
<!-- Dialogs, Tooltips, Popovers need Portal -->
<DialogRoot v-model:open="open">
  <DialogTrigger>Open</DialogTrigger>
  <DialogPortal>
    <!-- Rendered in <body> — avoids z-index and overflow issues -->
    <DialogOverlay class="fixed inset-0 bg-black/50" />
    <DialogContent class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
      <DialogTitle>Title</DialogTitle>
      <DialogClose>Close</DialogClose>
    </DialogContent>
  </DialogPortal>
</DialogRoot>
```

---

## forceMount — keep in DOM for animations

```vue
<!-- Keep content in DOM even when closed (for CSS transitions) -->
<DialogContent force-mount v-show="open" class="data-[state=open]:animate-in">
  <!-- Content always mounted, visibility controlled by data-state -->
</DialogContent>
```

---

## Components by category

### Form inputs
`CheckboxRoot`, `RadioGroupRoot + RadioGroupItem`, `SwitchRoot`,
`SliderRoot`, `NumberFieldRoot`, `PinInputRoot`, `TagsInputRoot`

### Overlay
`DialogRoot`, `AlertDialogRoot`, `PopoverRoot`, `TooltipRoot`,
`HoverCardRoot`, `SheetRoot` (via DrawerRoot)

### Navigation
`NavigationMenuRoot`, `MenubarRoot`, `ContextMenuRoot`,
`DropdownMenuRoot`, `TabsRoot`

### Selection / Search
`SelectRoot`, `ComboboxRoot`, `ListboxRoot`

### Disclosure
`AccordionRoot`, `CollapsibleRoot`

### Data display
`ScrollAreaRoot`, `SeparatorRoot`, `AvatarRoot`, `AspectRatioRoot`

### Date / Time
`CalendarRoot`, `RangeCalendarRoot` (uses `@internationalized/date`)

---

## Virtualization — large lists

```vue
<script setup lang="ts">
import { ComboboxRoot, ComboboxVirtualizer, ComboboxItem } from 'reka-ui'

const items = ref(Array.from({ length: 10000 }, (_, i) => `Item ${i}`))
</script>

<template>
  <ComboboxRoot>
    <ComboboxContent>
      <!-- Automatic virtualization for performance -->
      <ComboboxVirtualizer
        :options="items"
        :estimate-size="32"
        v-slot="{ option }"
      >
        <ComboboxItem :value="option">{{ option }}</ComboboxItem>
      </ComboboxVirtualizer>
    </ComboboxContent>
  </ComboboxRoot>
</template>
```

Supported in: `ComboboxRoot`, `ListboxRoot`, `TreeRoot`

---

## useLocale and useDirection (v2.6+)

```vue
<script setup lang="ts">
import { useLocale, useDirection } from 'reka-ui'

// Global locale for date components
const { locale } = useLocale()
locale.value = 'pt-BR'

// RTL support
const { dir } = useDirection()
dir.value = 'ltr' // or 'rtl'
</script>
```

---

## Date/Calendar with @internationalized/date

```vue
<script setup lang="ts">
import { CalendarRoot, CalendarGrid, CalendarCell } from 'reka-ui'
import { CalendarDate, today, getLocalTimeZone } from '@internationalized/date'
import { ref } from 'vue'

const value = ref(today(getLocalTimeZone()))
</script>

<template>
  <CalendarRoot v-model="value" locale="pt-BR">
    <CalendarGrid>
      <CalendarCell v-for="date in dates" :date="date" />
    </CalendarGrid>
  </CalendarRoot>
</template>
```

---

## Radix Vue → Reka UI Migration

```bash
# Via shadcn-vue CLI (reinstalls all components with Reka)
npx shadcn-vue@latest add --all

# Manual: swap imports
# Before: import { Dialog } from 'radix-vue'
# After: import { DialogRoot } from 'reka-ui'
# or: import { Dialog } from '@/components/ui/dialog'  ← preferred
```

Main name changes:
| Radix Vue | Reka UI |
|---|---|
| `RadixDialog` | `DialogRoot` |
| `import from 'radix-vue'` | `import from 'reka-ui'` |
| Same API pattern | Same API pattern |

---

## Reka UI v2 Gotchas

- `asChild` + slot: do not add elements between the Reka component and the direct child
- `v-model:open` is reactive by reference — do not destroy and recreate the component
- `forceMount` + `v-show` works; `forceMount` + `v-if` does not (defeats the purpose)
- Portal teleports to `<body>` — `scoped` CSS may not reach the content
- `ComboboxVirtualizer`: `estimateSize` can be a function for variable heights (v2.7+)
- Calendar: `@internationalized/date` is a peer dependency — install separately: `npm i @internationalized/date`
