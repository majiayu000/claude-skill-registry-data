---
name: motion
description: Motion animation library for JavaScript, React and Vue. Use when creating animations, gestures, layout transitions, scroll-linked effects, or working with motion values and animation controls.
metadata:
  author: Hairyf
  version: "2026.2.1"
  source: Generated from https://github.com/motiondivision/motion, scripts located at https://github.com/antfu/skills
---

Motion is an open-source animation library for JavaScript, React, and Vue. It provides a simple API with first-class support for multiple platforms, a hybrid animation engine combining JavaScript with native browser APIs for 120fps GPU-accelerated animations, and production-ready features including TypeScript support, extensive test suite, tree-shakable builds, and a tiny footprint. Batteries included: gestures, springs, layout transitions, scroll-linked effects, and timelines.

> The skill is based on Motion v12.29.2, generated at 2026-02-01.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Motion Components | Basic motion components (motion.div, motion.svg, etc.) | [core-components](references/core-components.md) |
| Basic Animation | animate prop, initial, while states | [core-animation](references/core-animation.md) |
| JavaScript animate() | Vanilla animate(), sequences, createScopedAnimate | [core-javascript-animate](references/core-javascript-animate.md) |
| Vanilla scroll() | Imperative scroll() and scrollInfo() for non-React | [core-vanilla-scroll](references/core-vanilla-scroll.md) |
| motionValue | Create MotionValues without React | [core-vanilla-motion-value](references/core-vanilla-motion-value.md) |
| stagger | Orchestrate child delays in variants | [core-stagger](references/core-stagger.md) |
| frame / cancelFrame | Motion's animation loop | [core-frameloop](references/core-frameloop.md) |
| motion/mini | Minimal bundle entry | [core-motion-mini](references/core-motion-mini.md) |
| Variants | Declarative animation variants and orchestration | [core-variants](references/core-variants.md) |
| Transitions | Animation timing, easing, spring physics | [core-transitions](references/core-transitions.md) |

## Motion Values

| Topic | Description | Reference |
|-------|-------------|-----------|
| useMotionValue | Create and use motion values for reactive animations | [values-motion-value](references/values-motion-value.md) |
| useSpring | Spring-based motion values with physics | [values-spring](references/values-spring.md) |
| useTransform | Transform motion values with functions | [values-transform](references/values-transform.md) |
| useMotionTemplate | Combine motion values into a string (e.g. filter, boxShadow) | [values-motion-template](references/values-motion-template.md) |
| useFollowValue | Motion value that follows a source with any transition | [values-follow](references/values-follow.md) |
| useScroll | Scroll-linked motion values and animations | [values-scroll](references/values-scroll.md) |
| useVelocity | Access velocity of motion values | [values-velocity](references/values-velocity.md) |
| useTime | Time-based motion values | [values-time](references/values-time.md) |
| useWillChange | GPU layer hint for animating elements | [values-will-change](references/values-will-change.md) |

## Gestures

| Topic | Description | Reference |
|-------|-------------|-----------|
| Drag | Drag gestures with constraints and controls | [gestures-drag](references/gestures-drag.md) |
| Pan | Pan gestures for touch and pointer events | [gestures-pan](references/gestures-pan.md) |
| Tap & Press | Tap and press gesture handlers | [gestures-tap-press](references/gestures-tap-press.md) |
| Hover & Focus | Hover and focus state animations | [gestures-hover-focus](references/gestures-hover-focus.md) |

## Layout Animations

| Topic | Description | Reference |
|-------|-------------|-----------|
| AnimatePresence | Animate components entering and exiting | [layout-animate-presence](references/layout-animate-presence.md) |
| usePresence / useIsPresent | Access presence state in AnimatePresence children | [layout-use-presence](references/layout-use-presence.md) |
| usePresenceData | Read AnimatePresence custom prop in descendants | [layout-presence-data](references/layout-presence-data.md) |
| LayoutGroup | Coordinate layout animations across components | [layout-group](references/layout-group.md) |
| Layout Animations | Automatic layout animations with layoutId | [layout-animations](references/layout-animations.md) |
| Reorder | Drag-to-reorder with layout animations | [layout-reorder](references/layout-reorder.md) |
| useInstantLayoutTransition | Block layout update for one frame | [layout-instant-transition](references/layout-instant-transition.md) |
| useResetProjection | Reset layout projection tree after structural change | [layout-reset-projection](references/layout-reset-projection.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| In View | useInView, inView(), usePageInView for viewport/visibility | [features-in-view](references/features-in-view.md) |
| Resize | resize() observer for window or element size | [features-resize](references/features-resize.md) |
| Optimized Appear | SSR-friendly appear animations with handoff | [features-optimized-appear](references/features-optimized-appear.md) |
| SVG Path | pathLength, pathOffset, pathSpacing for path animations | [features-svg-path](references/features-svg-path.md) |
| motion/client | Next.js "use client" and tree-shakable components | [features-react-client](references/features-react-client.md) |

## Utils

| Topic | Description | Reference |
|-------|-------------|-----------|
| useReducedMotion | Hooks for reduced motion preference | [utils-reduced-motion](references/utils-reduced-motion.md) |
| useAnimationFrame | Frame-synced callback with Motion's loop | [utils-animation-frame](references/utils-animation-frame.md) |
| useCycle | Cycle through a list of states | [utils-cycle](references/utils-cycle.md) |
| useMotionValueEvent | Subscribe to motion value events | [utils-motion-value-event](references/utils-motion-value-event.md) |
| delay | Frame-synced delayed execution | [utils-delay](references/utils-delay.md) |
| interpolate | Map input range to output | [utils-interpolate](references/utils-interpolate.md) |
| useDomEvent | Attach DOM event listeners | [utils-dom-event](references/utils-dom-event.md) |
| useInstantTransition | Block layout animations during update | [utils-instant-transition](references/utils-instant-transition.md) |
| calcLength / createBox / distance | Projection geometry and distance | [utils-path-geometry](references/utils-path-geometry.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Animation Controls | Programmatic animation control with useAnimation | [advanced-animation-controls](references/advanced-animation-controls.md) |
| useAnimate | Imperative animation API | [advanced-use-animate](references/advanced-use-animate.md) |
| LazyMotion | Code-split animations for better performance | [advanced-lazy-motion](references/advanced-lazy-motion.md) |
| MotionConfig | Global configuration and reduced motion | [advanced-motion-config](references/advanced-motion-config.md) |
| Scroll Animations | Scroll-linked animations and parallax effects | [advanced-scroll-animations](references/advanced-scroll-animations.md) |
| transformTemplate | Custom transform output | [advanced-transform-template](references/advanced-transform-template.md) |
| addScaleCorrector | Layout projection scale correctors | [advanced-scale-corrector](references/advanced-scale-corrector.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Bundle Size | Entry points and optimization strategies | [best-practices-bundle](references/best-practices-bundle.md) |
