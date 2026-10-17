---
name: lottiefiles-motion-design-skill
description: Universal motion design principles for AI agents — timing, easing, choreography, and Disney animation principles adapted for UI
triggers:
  - "add animation to this component"
  - "create a loading state animation"
  - "animate this button interaction"
  - "make this transition feel more natural"
  - "choreograph these elements entering"
  - "review my animation for motion design principles"
  - "what easing should I use for this"
  - "help me with micro-interactions"
---

# LottieFiles Motion Design Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

This skill teaches AI agents to think like motion directors — choosing the right timing, easing, choreography, and emotional intent before writing animation code. Philosophy-first, implementation-agnostic approach that works with any animation system (CSS, Framer Motion, GSAP, Lottie, React Spring, etc.).

## Installation

```bash
npx skills add LottieFiles/motion-design-skill
```

The skill integrates with 40+ AI coding agents including Claude Code, Cursor, Codex, and GitHub Copilot.

## Core Philosophy

### The Three Pillars

Every animation decision flows from three questions:

1. **WHY** — What's the purpose? (feedback, guidance, delight, hierarchy)
2. **WHAT** — Which properties communicate that? (position, scale, opacity, color)
3. **HOW** — What personality matches the brand? (snappy, smooth, bouncy, minimal)

### The 8-Step Motion Checklist

Before writing any animation code:

1. **Purpose** — Why does this need to animate?
2. **Emotion** — What should the user feel?
3. **Personality** — Which motion archetype fits the brand?
4. **Properties** — Which CSS/transform properties to animate?
5. **Duration** — How long should it take?
6. **Easing** — What curve shape matches the intent?
7. **Choreography** — If multiple elements, what's the sequence?
8. **Quality** — Does it pass the motion design checklist?

## Motion Personality Archetypes

Choose one archetype per brand/project:

### 1. Snappy (Productivity, Tools)
```javascript
// Framer Motion example
const snappy = {
  duration: 0.2,
  ease: [0.4, 0, 0.2, 1] // easeInOutCubic
};

// CSS example
.snappy-button {
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

### 2. Smooth (Finance, Professional)
```javascript
// Framer Motion
const smooth = {
  duration: 0.4,
  ease: [0.25, 0.1, 0.25, 1] // easeInOutQuart
};

// CSS
.smooth-card {
  transition: all 400ms cubic-bezier(0.25, 0.1, 0.25, 1);
}
```

### 3. Bouncy (Social, Playful)
```javascript
// Framer Motion
const bouncy = {
  type: "spring",
  damping: 15,
  stiffness: 300
};

// CSS (approximated)
.bouncy-modal {
  transition: all 500ms cubic-bezier(0.68, -0.55, 0.265, 1.55);
}
```

### 4. Minimal (Editorial, Luxury)
```javascript
// Framer Motion
const minimal = {
  duration: 0.6,
  ease: [0.25, 0, 0.1, 1] // easeOutQuart
};

// CSS
.minimal-fade {
  transition: opacity 600ms cubic-bezier(0.25, 0, 0.1, 1);
}
```

## Duration & Easing Reference

### Duration by Element Size

| Element Type | Duration | Use Case |
|-------------|----------|----------|
| Icon/Badge | 150-200ms | Small UI feedback |
| Button/Input | 200-300ms | Interactive elements |
| Card/Panel | 300-400ms | Medium containers |
| Modal/Drawer | 400-500ms | Large overlays |
| Page Transition | 500-700ms | Full screen changes |

### Easing by Intent

| Intent | Easing Function | Cubic Bezier | Use Case |
|--------|----------------|--------------|----------|
| **Enter** | easeOut | `(0, 0, 0.2, 1)` | Elements appearing |
| **Exit** | easeIn | `(0.4, 0, 1, 1)` | Elements disappearing |
| **Move** | easeInOut | `(0.4, 0, 0.2, 1)` | Position/size changes |
| **Attention** | easeOutBack | `(0.34, 1.56, 0.64, 1)` | Success feedback |
| **Smooth** | easeInOutQuart | `(0.25, 0.1, 0.25, 1)` | Professional feel |

## Property Selection Guide

**What each property communicates:**

- **Opacity** — Existence (appearing/disappearing)
- **Scale** — Importance (growing/shrinking attention)
- **Position (x/y)** — Origin/direction (where it came from)
- **Rotation** — Playfulness/dynamism
- **Color** — State change (success/error/focus)

**Recommended combinations:**

```javascript
// Entrance (appearing)
opacity: 0 → 1 + translateY(20px → 0)

// Exit (disappearing)
opacity: 1 → 0 + scale(1 → 0.95)

// Success feedback
scale(1 → 1.1 → 1) + color(blue → green)

// Error shake
translateX(0 → -10 → 10 → 0) with easeOutBounce
```

## Common Patterns

### Pattern 1: Button Hover/Press

```javascript
// Framer Motion
const buttonVariants = {
  idle: { scale: 1 },
  hover: { scale: 1.05, transition: { duration: 0.2 } },
  press: { scale: 0.95, transition: { duration: 0.1 } }
};

<motion.button
  variants={buttonVariants}
  initial="idle"
  whileHover="hover"
  whileTap="press"
>
  Click me
</motion.button>
```

```css
/* CSS version */
.button {
  transition: transform 200ms cubic-bezier(0.4, 0, 0.2, 1);
}
.button:hover {
  transform: scale(1.05);
}
.button:active {
  transform: scale(0.95);
  transition-duration: 100ms;
}
```

### Pattern 2: Card Entrance

```javascript
// Framer Motion
const cardVariants = {
  hidden: { 
    opacity: 0, 
    y: 20 
  },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: {
      duration: 0.4,
      ease: [0, 0, 0.2, 1] // easeOut
    }
  }
};

<motion.div
  variants={cardVariants}
  initial="hidden"
  animate="visible"
>
  Card content
</motion.div>
```

```css
/* CSS version with Intersection Observer */
.card {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 400ms ease-out, 
              transform 400ms ease-out;
}
.card.visible {
  opacity: 1;
  transform: translateY(0);
}
```

### Pattern 3: Loading → Success → Error States

```javascript
// Framer Motion
const buttonStates = {
  idle: {
    scale: 1,
    backgroundColor: "#3b82f6"
  },
  loading: {
    scale: 0.95,
    backgroundColor: "#6366f1",
    transition: { duration: 0.2 }
  },
  success: {
    scale: [1, 1.1, 1],
    backgroundColor: "#10b981",
    transition: { 
      scale: { duration: 0.4, times: [0, 0.5, 1] },
      backgroundColor: { duration: 0.3 }
    }
  },
  error: {
    x: [0, -10, 10, -10, 10, 0],
    backgroundColor: "#ef4444",
    transition: {
      x: { duration: 0.5 },
      backgroundColor: { duration: 0.3 }
    }
  }
};

function SubmitButton() {
  const [state, setState] = useState('idle');
  
  return (
    <motion.button
      variants={buttonStates}
      animate={state}
    >
      {state === 'loading' && 'Submitting...'}
      {state === 'success' && '✓ Success'}
      {state === 'error' && '✗ Error'}
      {state === 'idle' && 'Submit'}
    </motion.button>
  );
}
```

### Pattern 4: Staggered List Entrance

```javascript
// Framer Motion
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1 // 100ms delay between children
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.3 }
  }
};

<motion.ul
  variants={containerVariants}
  initial="hidden"
  animate="visible"
>
  {items.map(item => (
    <motion.li key={item.id} variants={itemVariants}>
      {item.content}
    </motion.li>
  ))}
</motion.ul>
```

### Pattern 5: Modal Enter/Exit

```javascript
// Framer Motion with AnimatePresence
const backdropVariants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 }
};

const modalVariants = {
  hidden: { 
    opacity: 0, 
    scale: 0.95,
    y: 20 
  },
  visible: { 
    opacity: 1, 
    scale: 1,
    y: 0,
    transition: {
      duration: 0.3,
      ease: [0, 0, 0.2, 1]
    }
  },
  exit: {
    opacity: 0,
    scale: 0.95,
    transition: {
      duration: 0.2,
      ease: [0.4, 0, 1, 1]
    }
  }
};

<AnimatePresence>
  {isOpen && (
    <>
      <motion.div 
        className="backdrop"
        variants={backdropVariants}
        initial="hidden"
        animate="visible"
        exit="hidden"
      />
      <motion.div
        className="modal"
        variants={modalVariants}
        initial="hidden"
        animate="visible"
        exit="exit"
      >
        Modal content
      </motion.div>
    </>
  )}
</AnimatePresence>
```

## Multi-Element Choreography

When animating multiple elements, follow the **hierarchy → stagger → overlap** principle:

### Hierarchy Rules

1. **Most important first** — Hero content enters before supporting elements
2. **Follow reading order** — Respect natural eye flow (top→bottom, left→right)
3. **Group by relationship** — Related elements move together

### Stagger Timing

```javascript
// Small gaps (snappy)
staggerChildren: 0.05 // 50ms

// Medium gaps (balanced)
staggerChildren: 0.1 // 100ms

// Large gaps (dramatic)
staggerChildren: 0.15 // 150ms
```

### Choreography Example: Dashboard Entry

```javascript
// 1. Hero chart enters first
// 2. Stats cards stagger in
// 3. Sidebar fades in last

const dashboardVariants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2 // Wait for hero
    }
  }
};

<motion.div variants={dashboardVariants} initial="hidden" animate="visible">
  {/* Hero enters immediately */}
  <motion.div variants={heroVariants}>
    <Chart />
  </motion.div>
  
  {/* Cards stagger after hero */}
  <motion.div variants={containerVariants}>
    {cards.map(card => (
      <motion.div key={card.id} variants={cardVariants}>
        {card.content}
      </motion.div>
    ))}
  </motion.div>
  
  {/* Sidebar fades in last */}
  <motion.aside variants={sidebarVariants}>
    <Sidebar />
  </motion.aside>
</motion.div>
```

## Disney's 12 Principles (UI-Adapted)

### 1. Squash & Stretch
**UI Application:** Scale feedback on interactive elements
```javascript
// Button press
whileTap={{ scale: 0.95 }}
```

### 2. Anticipation
**UI Application:** Subtle motion before main action
```javascript
// Button hover primes for click
hover: { scale: 1.05, y: -2 }
```

### 3. Staging
**UI Application:** Focus attention through contrast
```javascript
// Dim background, highlight modal
backdrop: { opacity: 0.8 }
```

### 4. Straight Ahead vs. Pose-to-Pose
**UI Application:** Keyframe complex sequences
```javascript
scale: [1, 1.2, 1.1, 1] // Bounce through keyframes
```

### 5. Follow Through & Overlapping Action
**UI Application:** Stagger related elements
```javascript
staggerChildren: 0.1
```

### 6. Slow In/Slow Out
**UI Application:** Use easing curves (not linear)
```javascript
ease: [0.4, 0, 0.2, 1] // Always ease, never linear
```

### 7. Arcs
**UI Application:** Natural curved motion paths
```javascript
// Dropdown arcs down and slightly inward
x: [0, -10, 0], y: [0, 0, 20]
```

### 8. Secondary Action
**UI Application:** Subtle supporting animations
```javascript
// Icon rotates while button scales
rotate: 360, scale: 1.1
```

### 9. Timing
**UI Application:** Duration conveys weight/importance
```javascript
// Small: 200ms, Large: 400ms
```

### 10. Exaggeration
**UI Application:** Emphasize success/error states
```javascript
success: { scale: [1, 1.2, 1] } // Bounce bigger
```

### 11. Solid Drawing
**UI Application:** Maintain visual hierarchy during motion
```javascript
// Keep z-index/stacking order clear
```

### 12. Appeal
**UI Application:** Polish until it feels right
```javascript
// Iterate on easing/timing until satisfying
```

## Accessibility & Performance

### Respect User Preferences

```javascript
// Framer Motion
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

<motion.div
  animate={reducedMotion.matches ? { opacity: 1 } : { opacity: 1, y: 0 }}
  initial={reducedMotion.matches ? { opacity: 0 } : { opacity: 0, y: 20 }}
/>
```

```css
/* CSS */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Performance Guidelines

1. **Animate transform/opacity only** — GPU-accelerated
2. **Avoid animating:** width, height, top, left (causes layout thrashing)
3. **Use `will-change` sparingly** — Only during animation
4. **Debounce scroll listeners** — Use Intersection Observer instead

```javascript
// ✅ Good (GPU-accelerated)
transform: translateY(20px)
opacity: 0

// ❌ Avoid (forces reflow)
top: 20px
height: auto
```

## Quality Checklist

Before shipping any animation, verify:

- [ ] **Purpose is clear** — Why does this animate?
- [ ] **Timing feels natural** — Not too fast/slow
- [ ] **Easing matches intent** — Curves feel appropriate
- [ ] **No janky performance** — 60fps on target devices
- [ ] **Respects reduced motion** — Fallback for a11y
- [ ] **Enhances, doesn't distract** — User can still focus on task
- [ ] **Consistent with brand** — Matches motion personality
- [ ] **Tested on real devices** — Not just desktop/simulator

## Troubleshooting

### Animation feels too fast
**Fix:** Increase duration by 50-100ms, use gentler easing curve

### Animation feels too slow
**Fix:** Decrease duration, use sharper easing (higher acceleration)

### Animation feels robotic
**Fix:** Never use `linear` easing — always use curves with acceleration

### Animation causes jank/stuttering
**Fix:** 
- Animate only `transform` and `opacity`
- Check for forced reflows (width/height/top/left)
- Use `will-change: transform` during animation
- Reduce complexity (fewer elements, simpler paths)

### Animation feels disconnected from brand
**Fix:** Re-check motion personality archetype — adjust duration/easing to match

### Multiple animations feel chaotic
**Fix:** Apply choreography rules — stagger timing, establish hierarchy, group related elements

### Animation works on desktop but not mobile
**Fix:**
- Reduce duration by 20-30% for mobile
- Simplify motion paths
- Test on real devices, not simulators
- Consider disabling parallax/complex effects on low-end devices

## Implementation Examples (Multiple Frameworks)

### CSS Animations

```css
/* Entrance animation */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.card-enter {
  animation: fadeInUp 400ms cubic-bezier(0, 0, 0.2, 1);
}

/* Loading pulse */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.loading {
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
```

### React + Framer Motion

```javascript
import { motion } from 'framer-motion';

function AnimatedCard({ children }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ 
        duration: 0.4,
        ease: [0, 0, 0.2, 1]
      }}
    >
      {children}
    </motion.div>
  );
}
```

### Vue + GSAP

```vue
<template>
  <div ref="card" class="card">
    {{ content }}
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { gsap } from 'gsap';

const card = ref(null);

onMounted(() => {
  gsap.from(card.value, {
    opacity: 0,
    y: 20,
    duration: 0.4,
    ease: 'power2.out'
  });
});
</script>
```

### Svelte

```svelte
<script>
  import { fade, fly } from 'svelte/transition';
  import { cubicOut } from 'svelte/easing';
</script>

<div 
  in:fly={{ y: 20, duration: 400, easing: cubicOut }}
  out:fade={{ duration: 200 }}
>
  Card content
</div>
```

### Angular

```typescript
import { trigger, state, style, transition, animate } from '@angular/animations';

export const cardAnimation = trigger('cardEnter', [
  transition(':enter', [
    style({ opacity: 0, transform: 'translateY(20px)' }),
    animate('400ms cubic-bezier(0, 0, 0.2, 1)', 
      style({ opacity: 1, transform: 'translateY(0)' })
    )
  ])
]);

// In component
@Component({
  animations: [cardAnimation]
})
```

## Additional Resources

The full skill includes deep-dive documentation in these directories:

- **`director/`** — Philosophy, decision frameworks, emotion mapping, choreography
- **`patterns/`** — Ready-to-use recipes for common UI animations
- **`reference/`** — Timing tables, property guides, troubleshooting

These files provide extended context but the principles above cover 90% of practical motion design decisions.

## When to Use This Skill

Activate motion design thinking when:

- Building interactive UI components (buttons, cards, forms)
- Implementing state transitions (loading, success, error)
- Orchestrating multi-element sequences (lists, dashboards)
- Establishing brand motion identity
- Reviewing animation code for improvements
- Debugging janky or unnatural-feeling animations
- Adapting motion for accessibility or performance

Remember: **Always think WHY → WHAT → HOW before writing animation code.**
