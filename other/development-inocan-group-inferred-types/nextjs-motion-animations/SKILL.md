---
name: nextjs-motion-animations
description: Motion-based animation system for Next.js with performance-optimized patterns
license: MIT
compatibility: nextjs
metadata:
  library: motion
  version: "12.23.26"
  framework: nextjs
  css: tailwindcss
---

# Next.js Motion Animation System

A comprehensive animation system using Motion (formerly Framer Motion) v12.23.26 with performance-optimized patterns for Next.js applications.

## When to Use This Skill

Use this skill when you need to:
- Add scroll-triggered animations to sections
- Create interactive hover/tap animations
- Implement staggered animations for lists
- Add SVG path animations
- Set up a centralized animation system
- Optimize animation performance in Next.js

## Core Animation Architecture

### Library Setup
- **Primary**: Motion v12.23.26 (modern, lightweight alternative to framer-motion)
- **CSS Framework**: TailwindCSS with custom animation utilities
- **Compatibility**: React 19+ and Next.js 16+

### Installation
```bash
npm install motion@12.23.26
# Optional for CSS animations
npm install tw-animate-css@1.4.0
```

## 1. Centralized Animation Variants

Create `src/lib/animations.ts` with reusable variants:

```typescript
// Basic fade animations with directional movement
export const fadeInUp = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }
};

export const fadeInDown = {
  hidden: { opacity: 0, y: -30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.6 } }
};

export const fadeInLeft = {
  hidden: { opacity: 0, x: -30 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.6 } }
};

export const fadeInRight = {
  hidden: { opacity: 0, x: 30 },
  visible: { opacity: 1, x: 0, transition: { duration: 0.6 } }
};

export const fadeInScale = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.6 } }
};

// Container for staggered child animations
export const staggerContainer = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.2 }
  }
};

// Individual items within staggered containers
export const staggerItem = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } }
};
```

## 2. Implementation Patterns

### A. Scroll-triggered Animations
Standard pattern for content reveals:

```tsx
import { motion } from 'motion';
import { fadeInUp } from '@/lib/animations';

<motion.div
  variants={fadeInUp}
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true }}
>
  Content here
</motion.div>
```

### B. Staggered Animations
For sequential reveals of multiple elements:

```tsx
import { motion } from 'motion';
import { staggerContainer, staggerItem } from '@/lib/animations';

<motion.div
  variants={staggerContainer}
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true }}
>
  <motion.h1 variants={staggerItem}>Title</motion.h1>
  <motion.p variants={staggerItem}>Subtitle</motion.p>
  <motion.div variants={staggerItem}>CTA Buttons</motion.div>
</motion.div>
```

### C. Interactive Animations
For buttons and interactive elements:

```tsx
import { motion } from 'motion';

<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  animate={{ y: [0, -8, 0] }}
  transition={{
    y: { duration: 2, repeat: Infinity, ease: "easeInOut" }
  }}
>
  Call to Action
</motion.button>
```

## 3. Advanced Animation Features

### A. SVG Path Animation
For connecting lines and decorative elements:

```tsx
import { motion } from 'motion';

<motion.svg>
  <motion.path
    d="M 200 100 Q 400 50 600 100 T 1000 100"
    stroke="rgb(var(--primary) / 0.3)"
    strokeDasharray="8 8"
    initial={{ pathLength: 0 }}
    whileInView={{ pathLength: 1 }}
    viewport={{ once: true }}
    transition={{ duration: 2, delay: 0.5 }}
  />
</motion.svg>
```

### B. Hover Interactions with Dynamic Properties

```tsx
import { motion } from 'motion';

<motion.span
  whileHover={{
    scale: 1.2,
    backgroundColor: "rgb(var(--primary) / 0.2)"
  }}
  transition={{ duration: 0.2 }}
>
  Icon
</motion.span>
```

## 4. CSS Animations for Continuous Effects

Complement Motion animations with CSS for always-running effects:

```css
/* Add to globals.css */
@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

@keyframes slide-up {
  0% { opacity: 0; transform: translateY(10px); }
  100% { opacity: 1; transform: translateY(0); }
}

.animate-float { 
  animation: float 4s ease-in-out infinite; 
}

.animate-slide-up { 
  animation: slide-up 0.4s ease-out forwards; 
  opacity: 0; 
}
```

## 5. Animation Timing Strategy

### Performance Optimizations
- Use `viewport={{ once: true }}` to prevent re-triggers
- Consistent 0.6s duration for main elements
- 0.1s stagger delays for sequential reveals
- 0.2s delay before children start animating

### Layered Animation Approach
1. **Immediate**: CSS animations for persistent effects
2. **On Scroll**: Motion variants for content reveals
3. **On Interaction**: Hover/tap states for interactivity
4. **Background**: Subtle floating animations for visual interest

## 6. Component Integration Examples

### Hero Section
Two-column layout with opposing slide animations:

```tsx
<motion.section className="grid md:grid-cols-2 gap-8">
  <motion.div
    variants={fadeInLeft}
    initial="hidden"
    whileInView="visible"
    viewport={{ once: true }}
  >
    <h1>Hero Title</h1>
    <p>Hero Description</p>
  </motion.div>
  
  <motion.div
    variants={fadeInRight}
    initial="hidden"
    whileInView="visible"
    viewport={{ once: true }}
  >
    <img src="/hero-image.jpg" alt="Hero" />
  </motion.div>
</motion.section>
```

### Features Grid
Staggered item reveals with hover interactions:

```tsx
<motion.div 
  variants={staggerContainer}
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true }}
  className="grid md:grid-cols-3 gap-6"
>
  {features.map((feature, index) => (
    <motion.div
      key={index}
      variants={staggerItem}
      whileHover={{ y: -5 }}
      className="p-6 bg-white rounded-lg shadow"
    >
      <h3>{feature.title}</h3>
      <p>{feature.description}</p>
    </motion.div>
  ))}
</motion.div>
```

### Process Steps
Sequential reveals with connecting line animations:

```tsx
<motion.div className="relative">
  {/* Connecting line */}
  <motion.div
    className="absolute left-4 top-8 h-full w-0.5 bg-primary/20"
    initial={{ scaleY: 0 }}
    whileInView={{ scaleY: 1 }}
    viewport={{ once: true }}
    transition={{ duration: 1, delay: 0.5 }}
  />
  
  {/* Steps */}
  <motion.div
    variants={staggerContainer}
    initial="hidden"
    whileInView="visible"
    viewport={{ once: true }}
  >
    {steps.map((step, index) => (
      <motion.div
        key={index}
        variants={staggerItem}
        className="relative pl-12 pb-8"
      >
        <div className="absolute left-0 w-8 h-8 bg-primary rounded-full" />
        <h3>{step.title}</h3>
        <p>{step.description}</p>
      </motion.div>
    ))}
  </motion.div>
</motion.div>
```

### CTA Sections
Pulsing buttons with bounce effects:

```tsx
<motion.section
  variants={fadeInScale}
  initial="hidden"
  whileInView="visible"
  viewport={{ once: true }}
  className="text-center py-16"
>
  <motion.button
    whileHover={{ scale: 1.05 }}
    whileTap={{ scale: 0.95 }}
    animate={{ 
      boxShadow: [
        "0 0 0 0 rgba(59, 130, 246, 0.7)",
        "0 0 0 10px rgba(59, 130, 246, 0)",
      ]
    }}
    transition={{
      boxShadow: { duration: 1.5, repeat: Infinity }
    }}
    className="px-8 py-4 bg-blue-500 text-white rounded-lg"
  >
    Get Started Now
  </motion.button>
</motion.section>
```

## 7. Best Practices

### Performance Guidelines
- Always use `viewport={{ once: true }}` for scroll animations
- Prefer `transform` and `opacity` changes over layout properties
- Use `will-change: transform` sparingly and remove after animation
- Batch animations that occur simultaneously

### Accessibility Considerations
- Respect `prefers-reduced-motion` media query
- Provide fallbacks for users with motion sensitivity
- Keep animation durations reasonable (< 1s for most interactions)

### Implementation Example with Reduced Motion Support

```tsx
import { motion } from 'motion';

const AnimatedComponent = ({ children }) => {
  const prefersReducedMotion = typeof window !== 'undefined' && 
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  return (
    <motion.div
      variants={prefersReducedMotion ? {} : fadeInUp}
      initial={prefersReducedMotion ? false : "hidden"}
      whileInView={prefersReducedMotion ? false : "visible"}
      viewport={{ once: true }}
    >
      {children}
    </motion.div>
  );
};
```

## 8. Package.json Dependencies

```json
{
  "dependencies": {
    "motion": "^12.23.26"
  },
  "devDependencies": {
    "tw-animate-css": "^1.4.0"
  }
}
```

## Summary

This animation system provides:
- **Smooth, performant animations** that enhance UX without overwhelming
- **Clear separation** between scroll-triggered reveals, interactive feedback, and ambient effects
- **Centralized management** for consistency across the application
- **Performance optimization** through proper timing and viewport controls
- **Accessibility support** with reduced motion preferences

The system scales from simple fade-ins to complex orchestrated sequences while maintaining optimal performance in Next.js applications.