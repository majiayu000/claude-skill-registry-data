---
name: motion-vue
description: Motion for Vue animation library guidance. Use when building Vue animations with motion-v package, implementing gesture animations (hover, press, drag), scroll-linked animations, layout animations, exit animations with AnimatePresence, variants, spring physics, or using hooks like useAnimate, useScroll, useSpring, useMotionValue, useTransform. Triggers on keywords like motion.div, motion-v, whileHover, whilePress, whileDrag, whileInView, AnimatePresence, layout animations, scroll animations, MotionConfig, LayoutGroup.
---

# Motion for Vue

Motion for Vue (`motion-v`) is a production-ready animation library with a hybrid engine capable of hardware-accelerated 120fps animations. This skill provides patterns and best practices for building performant, accessible Vue animations.

## Installation

```bash
npm install motion-v
```

### Nuxt Integration

```ts
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['motion-v/nuxt'],
})
```

### unplugin-vue-components

```ts
import Components from 'unplugin-vue-components/vite'
import MotionResolver from 'motion-v/resolver'

export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [MotionResolver()],
    }),
  ],
})
```

**Note:** Auto-import doesn't support `<motion />` component—import manually.

## Core Concepts

### The motion Component

Every HTML/SVG element has a motion equivalent: `motion.div`, `motion.button`, `motion.circle`, etc.

```vue
<script setup>
import { motion } from 'motion-v'
</script>

<template>
  <motion.div
    :initial="{ opacity: 0, y: 20 }"
    :animate="{ opacity: 1, y: 0 }"
    :transition="{ duration: 0.5 }"
  />
</template>
```

### Animation Props

| Prop | Purpose |
|------|---------|
| `initial` | Starting state (or `false` to skip enter animation) |
| `animate` | Target state to animate to |
| `exit` | State when removed (requires AnimatePresence) |
| `transition` | Animation configuration |
| `variants` | Named animation states |
| `whileHover` | State during hover |
| `whilePress` | State during press/tap |
| `whileDrag` | State during drag |
| `whileInView` | State when in viewport |
| `whileFocus` | State when focused |
| `layout` | Enable layout animations |
| `layoutId` | Shared element transitions |

## Animation Patterns

### Basic Animation

```vue
<motion.div
  :initial="{ opacity: 0, scale: 0.8 }"
  :animate="{ opacity: 1, scale: 1 }"
  :transition="{ type: 'spring', stiffness: 300, damping: 20 }"
/>
```

### Gesture Animations

```vue
<motion.button
  :whileHover="{ scale: 1.05, backgroundColor: '#3b82f6' }"
  :whilePress="{ scale: 0.95 }"
  :transition="{ type: 'spring', stiffness: 400, damping: 17 }"
  @hoverStart="() => console.log('hover started')"
  @hoverEnd="() => console.log('hover ended')"
  @pressStart="(e) => console.log('press started', e)"
  @press="(e) => console.log('press complete', e)"
/>
```

### Drag Gestures

```vue
<script setup>
import { motion, useDomRef } from 'motion-v'

const constraintsRef = useDomRef()
</script>

<template>
  <motion.div ref="constraintsRef" class="container">
    <motion.div
      drag
      :dragConstraints="constraintsRef"
      :dragElastic="0.2"
      :dragMomentum="true"
      :whileDrag="{ scale: 1.1, cursor: 'grabbing' }"
    />
  </motion.div>
</template>
```

### Variants (Orchestration)

```vue
<script setup>
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      when: 'beforeChildren',
      staggerChildren: 0.1
    }
  }
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
}
</script>

<template>
  <motion.ul
    :variants="containerVariants"
    initial="hidden"
    animate="visible"
  >
    <motion.li
      v-for="item in items"
      :key="item.id"
      :variants="itemVariants"
    >
      {{ item.name }}
    </motion.li>
  </motion.ul>
</template>
```

### Exit Animations (AnimatePresence)

```vue
<script setup>
import { motion, AnimatePresence } from 'motion-v'
import { ref } from 'vue'

const isVisible = ref(true)
</script>

<template>
  <AnimatePresence>
    <motion.div
      v-if="isVisible"
      key="modal"
      :initial="{ opacity: 0, scale: 0.9 }"
      :animate="{ opacity: 1, scale: 1 }"
      :exit="{ opacity: 0, scale: 0.9 }"
    />
  </AnimatePresence>
</template>
```

**Critical:** Direct children of AnimatePresence must have unique `key` props.

#### AnimatePresence Modes

```vue
<!-- sync (default): Enter/exit simultaneously -->
<AnimatePresence mode="sync">

<!-- wait: New child waits for exiting child -->
<AnimatePresence mode="wait">

<!-- popLayout: Exiting children pop out of layout flow -->
<AnimatePresence mode="popLayout">
```

#### Dynamic Exit with custom Prop

```vue
<script setup>
const variants = {
  enter: (direction) => ({
    x: direction > 0 ? 300 : -300,
    opacity: 0
  }),
  center: { x: 0, opacity: 1 },
  exit: (direction) => ({
    x: direction < 0 ? 300 : -300,
    opacity: 0
  })
}
</script>

<template>
  <AnimatePresence :custom="direction">
    <motion.div
      :key="currentPage"
      :custom="direction"
      :variants="variants"
      initial="enter"
      animate="center"
      exit="exit"
    />
  </AnimatePresence>
</template>
```

### Layout Animations

```vue
<!-- Animate layout changes -->
<motion.div layout :style="{ width: isExpanded ? '200px' : '100px' }" />

<!-- Shared element transitions -->
<motion.div v-if="isSelected" layoutId="highlight" />
```

**Important:** CSS changes should happen via `:style`, not `:animate`—layout handles the animation.

#### LayoutGroup for Coordination

```vue
<script setup>
import { motion, LayoutGroup, AnimatePresence } from 'motion-v'
</script>

<template>
  <LayoutGroup>
    <motion.ul layout>
      <AnimatePresence>
        <motion.li
          v-for="item in items"
          :key="item.id"
          layout
          :exit="{ opacity: 0, scale: 0.8 }"
        />
      </AnimatePresence>
    </motion.ul>
  </LayoutGroup>
</template>
```

## Scroll Animations

### Scroll-Triggered (whileInView)

```vue
<motion.div
  :initial="{ opacity: 0, y: 50 }"
  :whileInView="{ opacity: 1, y: 0 }"
  :inViewOptions="{ once: true, margin: '-100px' }"
/>
```

### Scroll-Linked (useScroll)

```vue
<script setup>
import { motion, useScroll, useSpring, useTransform } from 'motion-v'

const { scrollYProgress } = useScroll()
const scaleX = useSpring(scrollYProgress, {
  stiffness: 100,
  damping: 30,
  restDelta: 0.001
})
</script>

<template>
  <motion.div class="progress-bar" :style="{ scaleX }" />
</template>
```

### Element Progress Tracking

```vue
<script setup>
import { ref } from 'vue'
import { motion, useScroll, useTransform } from 'motion-v'

const targetRef = ref(null)
const { scrollYProgress } = useScroll({
  target: targetRef,
  offset: ['start end', 'end start']  // When element enters/leaves viewport
})

const opacity = useTransform(scrollYProgress, [0, 0.5, 1], [0, 1, 0])
const y = useTransform(scrollYProgress, [0, 1], [100, -100])
</script>

<template>
  <motion.div ref="targetRef" :style="{ opacity, y }" />
</template>
```

## Motion Values & Hooks

See [HOOKS_REFERENCE.md](references/HOOKS_REFERENCE.md) for complete API documentation.

### Quick Reference

| Hook | Purpose |
|------|---------|
| `useMotionValue(initial)` | Reactive animated value (no re-renders) |
| `useSpring(source, config)` | Spring-based motion value |
| `useTransform(value, input, output)` | Map values to new values |
| `useVelocity(value)` | Track velocity of motion value |
| `useScroll(options)` | Track scroll position/progress |
| `useAnimate()` | Imperative animation control |
| `useInView(ref, options)` | Viewport intersection detection |
| `useReducedMotion()` | User motion preference |
| `useAnimationFrame(callback)` | Per-frame callbacks |
| `useTime()` | Elapsed time as motion value |
| `useDragControls()` | Programmatic drag control |
| `useMotionTemplate` | Template string with motion values |
| `useDomRef()` | DOM ref for constraints |

## Transition Options

```vue
<!-- Tween (default) -->
<motion.div :animate="{ x: 100 }" :transition="{ duration: 0.5, ease: 'easeInOut' }" />

<!-- Spring (physics-based) -->
<motion.div :animate="{ scale: 1.2 }" :transition="{ type: 'spring', stiffness: 300, damping: 20 }" />

<!-- Spring (duration-based) -->
<motion.div :animate="{ rotate: 180 }" :transition="{ type: 'spring', duration: 0.8, bounce: 0.25 }" />

<!-- Per-value transitions -->
<motion.div
  :animate="{ x: 100, opacity: 1 }"
  :transition="{ default: { type: 'spring' }, opacity: { ease: 'linear', duration: 0.2 } }"
/>

<!-- Keyframes with timing -->
<motion.div
  :animate="{ x: [0, 100, 50, 100], transition: { duration: 2, times: [0, 0.3, 0.6, 1] } }"
/>

<!-- Repeat/loop -->
<motion.div :animate="{ rotate: 360 }" :transition="{ repeat: Infinity, repeatType: 'loop', duration: 2 }" />
```

**Spring options:** `stiffness`, `damping`, `mass`, `bounce`, `duration`, `restDelta`, `restSpeed`
**Tween options:** `duration`, `ease`, `delay`
**Repeat options:** `repeat` (count or Infinity), `repeatType` ('loop'|'reverse'|'mirror'), `repeatDelay`

## Global Configuration

### MotionConfig

```vue
<script setup>
import { motion, MotionConfig } from 'motion-v'
</script>

<template>
  <MotionConfig
    :transition="{ duration: 0.3, ease: 'easeOut' }"
    reducedMotion="user"
  >
    <App />
  </MotionConfig>
</template>
```

**reducedMotion options:**
- `"user"` (default): Respect device settings
- `"always"`: Force reduced motion
- `"never"`: Ignore preference

## Custom Components

Wrap any Vue component with motion capabilities:

```vue
<script setup>
import { motion } from 'motion-v'
import MyButton from './MyButton.vue'

// IMPORTANT: Define outside template to prevent recreation each render
const MotionButton = motion.create(() => MyButton)
</script>

<template>
  <MotionButton
    :whileHover="{ scale: 1.05 }"
    :whilePress="{ scale: 0.95 }"
  />
</template>
```

## Performance Best Practices

1. **Use motion values** instead of Vue state for frequently-updated styles:
   ```vue
   <script setup>
   const x = useMotionValue(0)  // No re-renders on change
   </script>
   ```

2. **Add `willChange`** for transform-heavy animations:
   ```vue
   <motion.div :style="{ willChange: 'transform' }" />
   ```

3. **Use `layout` sparingly**—it triggers measurements

4. **Prefer independent transforms** (`x`, `y`, `scale`, `rotate`) over `transform` string

5. **Use `initial={false}`** to skip enter animations when not needed

## Accessibility

Always respect user preferences:

```vue
<script setup>
import { useReducedMotion } from 'motion-v'

const prefersReducedMotion = useReducedMotion()
</script>

<template>
  <motion.div
    :animate="prefersReducedMotion ? {} : { x: 100 }"
    :transition="prefersReducedMotion ? { duration: 0 } : { duration: 0.5 }"
  />
</template>
```

## Common Patterns

See [PATTERNS.md](references/PATTERNS.md) for complete examples including:
- Modal dialogs with backdrop
- Accordion/collapsible content
- Tab indicators with shared layout
- Staggered list reveals
- Page transitions
- Draggable reorder lists
- Scroll progress indicators
- Parallax effects

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Exit animations not working | Ensure direct child of AnimatePresence has `key` prop |
| Layout animation jittery | Add `layoutScroll` to scrollable ancestors |
| Animation not smooth | Check for re-renders; use motion values |
| Gesture not working on SVG filter | Add gesture props to parent, use variants |
| Touch hover issues | Motion handles this automatically; don't use CSS :hover |
