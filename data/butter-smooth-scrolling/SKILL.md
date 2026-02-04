---
name: butter-smooth-scrolling
description: Add cinematic lerp-based smooth scrolling for all scroll inputs (mouse wheel, trackpad, touch). Creates butter-smooth momentum scrolling like premium agency websites. Works alongside existing smooth-scroll anchor links.
---

# Butter Smooth Scrolling

Add cinematic, momentum-based smooth scrolling that interpolates scroll position using requestAnimationFrame. Creates the "butter smooth" feel seen on premium agency websites.

## Important: How This Differs from CSS Smooth Scroll

| Feature | CSS `scroll-behavior: smooth` | Butter Smooth Scrolling |
|---------|-------------------------------|------------------------|
| Anchor clicks | Yes | No (use existing smooth-scroll) |
| Mouse wheel | No | Yes |
| Trackpad | No | Yes |
| Touch | No | Yes |
| Momentum feel | No | Yes |
| Configurable smoothness | No | Yes |
| Performance impact | None | Minimal (RAF optimized) |

**This skill complements the existing `smooth-scroll` skill** - they work together, not as replacements.

## Prerequisites

- Next.js App Router
- React 19
- Existing `smooth-scroll` skill for anchor links (optional but recommended)

## Workflow

1. **Create ButterScroll Component** - Create `components/ui/butter-scroll.tsx`
2. **Add to Layout** - Include component in locale layout (alongside PageTransition)
3. **Configure Options** - Adjust lerp factor for desired smoothness
4. **Test** - Verify smooth scrolling on all inputs
5. **Accessibility** - Confirm reduced motion preference is respected

## Implementation

### Step 1: Create ButterScroll Component

Create `website/components/ui/butter-scroll.tsx`:

```tsx
"use client";

import { useEffect, useRef, useCallback } from "react";

interface ButterScrollOptions {
  /**
   * Lerp factor (0-1). Lower = smoother but slower.
   * 0.06 = very smooth (cinematic)
   * 0.12 = balanced (default)
   * 0.18 = snappy
   */
  lerp?: number;
  /**
   * Scroll sensitivity multiplier.
   * 1.0 = normal, 0.5 = slower, 1.5 = faster
   */
  sensitivity?: number;
  /**
   * Disable butter scroll for trackpad (use native)
   */
  disableTrackpad?: boolean;
  /**
   * Disable butter scroll for touch (use native)
   */
  disableTouch?: boolean;
  /**
   * Minimum velocity threshold to stop animation (performance)
   */
  threshold?: number;
}

const defaultOptions: Required<ButterScrollOptions> = {
  lerp: 0.12,
  sensitivity: 1.0,
  disableTrackpad: false,
  disableTouch: false,
  threshold: 0.5,
};

export function ButterScroll(props: ButterScrollOptions = {}) {
  const options = { ...defaultOptions, ...props };

  const targetScrollY = useRef(0);
  const currentScrollY = useRef(0);
  const rafId = useRef<number | null>(null);
  const isScrolling = useRef(false);
  const lastWheelTime = useRef(0);
  const touchStartY = useRef(0);
  const lastTouchY = useRef(0);

  // Linear interpolation function
  const lerp = useCallback((start: number, end: number, factor: number) => {
    return start + (end - start) * factor;
  }, []);

  // Get max scroll position
  const getMaxScroll = useCallback(() => {
    return document.documentElement.scrollHeight - window.innerHeight;
  }, []);

  // Clamp target scroll to valid range
  const clampScroll = useCallback(
    (value: number) => {
      return Math.max(0, Math.min(getMaxScroll(), value));
    },
    [getMaxScroll]
  );

  // Animation loop
  const animate = useCallback(() => {
    // Calculate new scroll position
    currentScrollY.current = lerp(
      currentScrollY.current,
      targetScrollY.current,
      options.lerp
    );

    // Apply scroll position
    window.scrollTo(0, currentScrollY.current);

    // Check if we should continue animating
    const diff = Math.abs(targetScrollY.current - currentScrollY.current);

    if (diff > options.threshold) {
      rafId.current = requestAnimationFrame(animate);
    } else {
      // Snap to final position
      window.scrollTo(0, targetScrollY.current);
      currentScrollY.current = targetScrollY.current;
      isScrolling.current = false;
      rafId.current = null;
    }
  }, [lerp, options.lerp, options.threshold]);

  // Start animation if not running
  const startAnimation = useCallback(() => {
    if (!isScrolling.current) {
      isScrolling.current = true;
      currentScrollY.current = window.scrollY;
      rafId.current = requestAnimationFrame(animate);
    }
  }, [animate]);

  // Detect if wheel event is from trackpad
  const isTrackpadEvent = useCallback((e: WheelEvent) => {
    const now = Date.now();
    const timeDelta = now - lastWheelTime.current;
    lastWheelTime.current = now;

    // Trackpad typically has smaller, more frequent deltas
    return Math.abs(e.deltaY) < 50 && timeDelta < 50;
  }, []);

  // Wheel event handler (mouse wheel + trackpad)
  const handleWheel = useCallback(
    (e: WheelEvent) => {
      // Check if trackpad and should be disabled
      if (options.disableTrackpad && isTrackpadEvent(e)) {
        return;
      }

      // Prevent default scroll
      e.preventDefault();

      // Normalize delta across browsers
      const normalizedDelta =
        e.deltaMode === 1
          ? e.deltaY * 20 // Line mode (Firefox)
          : e.deltaY; // Pixel mode (Chrome, Safari)

      // Update target scroll position
      targetScrollY.current = clampScroll(
        targetScrollY.current + normalizedDelta * options.sensitivity
      );

      // Start animation
      startAnimation();
    },
    [
      clampScroll,
      isTrackpadEvent,
      options.disableTrackpad,
      options.sensitivity,
      startAnimation,
    ]
  );

  // Touch start handler
  const handleTouchStart = useCallback(
    (e: TouchEvent) => {
      if (options.disableTouch) return;

      touchStartY.current = e.touches[0].clientY;
      lastTouchY.current = e.touches[0].clientY;

      // Sync current scroll position
      if (!isScrolling.current) {
        targetScrollY.current = window.scrollY;
        currentScrollY.current = window.scrollY;
      }
    },
    [options.disableTouch]
  );

  // Touch move handler
  const handleTouchMove = useCallback(
    (e: TouchEvent) => {
      if (options.disableTouch) return;

      const currentTouchY = e.touches[0].clientY;
      const deltaY = lastTouchY.current - currentTouchY;
      lastTouchY.current = currentTouchY;

      // Prevent default to take over scroll
      e.preventDefault();

      // Update target (inverted because dragging down = scroll up)
      targetScrollY.current = clampScroll(
        targetScrollY.current + deltaY * options.sensitivity
      );

      // Start animation
      startAnimation();
    },
    [clampScroll, options.disableTouch, options.sensitivity, startAnimation]
  );

  // Touch end handler - add momentum
  const handleTouchEnd = useCallback(() => {
    // Animation continues naturally due to lerp
  }, []);

  // Sync scroll position on resize or programmatic scroll
  const syncScroll = useCallback(() => {
    if (!isScrolling.current) {
      targetScrollY.current = window.scrollY;
      currentScrollY.current = window.scrollY;
    }
  }, []);

  useEffect(() => {
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    if (prefersReducedMotion) {
      // Skip all butter scroll behavior for accessibility
      return;
    }

    // Initialize scroll position
    targetScrollY.current = window.scrollY;
    currentScrollY.current = window.scrollY;

    // Add wheel listener with passive: false to allow preventDefault
    window.addEventListener("wheel", handleWheel, { passive: false });

    // Add touch listeners if not disabled
    if (!options.disableTouch) {
      window.addEventListener("touchstart", handleTouchStart, {
        passive: true,
      });
      window.addEventListener("touchmove", handleTouchMove, { passive: false });
      window.addEventListener("touchend", handleTouchEnd, { passive: true });
    }

    // Sync on scroll events (for anchor links, programmatic scrolls)
    window.addEventListener("scroll", syncScroll, { passive: true });

    // Sync on resize
    window.addEventListener("resize", syncScroll, { passive: true });

    return () => {
      window.removeEventListener("wheel", handleWheel);
      window.removeEventListener("touchstart", handleTouchStart);
      window.removeEventListener("touchmove", handleTouchMove);
      window.removeEventListener("touchend", handleTouchEnd);
      window.removeEventListener("scroll", syncScroll);
      window.removeEventListener("resize", syncScroll);

      if (rafId.current) {
        cancelAnimationFrame(rafId.current);
      }
    };
  }, [
    handleWheel,
    handleTouchStart,
    handleTouchMove,
    handleTouchEnd,
    syncScroll,
    options.disableTouch,
  ]);

  // This component renders nothing
  return null;
}
```

### Step 2: Add to Layout

Add ButterScroll to `app/[locale]/layout.tsx`:

```tsx
import { PageTransition } from "@/components/ui/page-transition";
import { ButterScroll } from "@/components/ui/butter-scroll";
import { Navbar2 } from "@/components/navbar2";
import { Footer2 } from "@/components/footer2";

export default async function LocaleLayout({
  children,
  params,
}: Props) {
  // ... existing code ...

  return (
    <NextIntlClientProvider messages={messages}>
      <PageTransition />
      <ButterScroll lerp={0.12} />
      <Navbar2 />
      <main>{children}</main>
      <Footer2 />
    </NextIntlClientProvider>
  );
}
```

**Important:**
- ButterScroll is a sibling component, not a wrapper
- Place it early in the component tree (after PageTransition)
- It renders nothing to the DOM

### Step 3: Configure Smoothness

Adjust the `lerp` prop based on desired feel:

```tsx
// Ultra smooth (cinematic, slow response)
<ButterScroll lerp={0.06} />

// Smooth (default, balanced)
<ButterScroll lerp={0.12} />

// Responsive (faster, less momentum)
<ButterScroll lerp={0.18} />

// Quick (minimal smoothing, snappy)
<ButterScroll lerp={0.25} />
```

### Step 4: Additional Options

```tsx
// Default: all inputs enabled
<ButterScroll lerp={0.12} />

// Disable for trackpad only (use native trackpad scroll)
<ButterScroll lerp={0.12} disableTrackpad />

// Disable for touch only (use native touch scroll)
<ButterScroll lerp={0.12} disableTouch />

// Custom configuration
<ButterScroll
  lerp={0.1}              // Smoothness factor
  sensitivity={1.2}       // Scroll speed multiplier
  disableTrackpad={false} // Enable for trackpad
  disableTouch={false}    // Enable for touch
  threshold={0.3}         // Animation stop threshold
/>
```

## How It Works

```
1. User scrolls (wheel/trackpad/touch)
   ↓
2. Event captured (preventDefault)
   ↓
3. Target scroll position updated (current + delta)
   ↓
4. requestAnimationFrame loop starts
   ↓
5. Each frame: currentScroll = lerp(currentScroll, targetScroll, 0.12)
   ↓
6. window.scrollTo(0, currentScroll)
   ↓
7. Loop continues until difference < threshold
   ↓
8. Snap to final position, stop animation
```

## Lerp (Linear Interpolation) Explained

```
lerp(start, end, factor) = start + (end - start) * factor

Example with factor 0.12:
- Frame 1: 0 + (100 - 0) * 0.12 = 12
- Frame 2: 12 + (100 - 12) * 0.12 = 22.56
- Frame 3: 22.56 + (100 - 22.56) * 0.12 = 31.85
- ... gradually approaches 100
```

Lower factor = more frames to reach target = smoother feel

## Performance Considerations

1. **GPU Acceleration:** `window.scrollTo` is optimized by browsers
2. **requestAnimationFrame:** Syncs with display refresh rate (60fps)
3. **Threshold cutoff:** Stops animation when movement imperceptible
4. **Reduced motion:** Completely disabled for accessibility
5. **No DOM manipulation:** Scroll position only, no transform hacks

## Accessibility

The component automatically respects `prefers-reduced-motion`:

```tsx
const prefersReducedMotion = window.matchMedia(
  "(prefers-reduced-motion: reduce)"
).matches;

if (prefersReducedMotion) {
  return; // Skip all butter scroll behavior
}
```

Users with reduced motion preference get native browser scrolling.

## Compatibility with Other Features

| Feature | Compatibility |
|---------|---------------|
| Smooth scroll anchor links | Works (sync on scroll event) |
| Page transitions | Works (component sibling) |
| Framer Motion animations | Works (no conflict) |
| Fixed navbar | Works (scroll position accurate) |
| Lazy loading images | Works (native scroll events fire) |
| Intersection Observer | Works (scroll position updates) |

## What This Skill Does NOT Do

- Handle keyboard scrolling (arrow keys, Page Up/Down stay native)
- Provide scroll-linked animations (use Framer Motion)
- Work when reduced motion is enabled (accessibility)

## Troubleshooting

### Scroll feels choppy
- Increase lerp factor: `lerp={0.15}`
- Check for heavy JavaScript blocking main thread

### Anchor links don't work
- Ensure smooth-scroll skill is active
- Check `syncScroll` is being called on scroll events

### Scroll is too slow
- Increase sensitivity: `sensitivity={1.5}`
- Increase lerp: `lerp={0.18}`

### Touch feels wrong on specific device
- Try `disableTouch={true}` to use native touch scroll

## Checklist

- [ ] `ButterScroll` component created at `components/ui/butter-scroll.tsx`
- [ ] Component added to `app/[locale]/layout.tsx`
- [ ] Lerp factor configured (default 0.12)
- [ ] Test: Mouse wheel scrolling feels smooth and momentum-like
- [ ] Test: Trackpad scrolling feels smooth
- [ ] Test: Touch scrolling feels smooth on mobile
- [ ] Test: Anchor links still work (smooth-scroll skill)
- [ ] Test: Page transitions work (page-transitions skill)
- [ ] Test: Reduced motion preference disables effect
- [ ] Test: 60fps maintained (Chrome DevTools Performance)

## Output

After running this skill:
- `components/ui/butter-scroll.tsx` - Lerp scroll component
- `app/[locale]/layout.tsx` - Updated with ButterScroll
- Cinematic butter-smooth scrolling on all inputs
