---
name: coverflow
description: Use when implementing coverflow carousels with 3D rotation. Applies Swiper configuration patterns with rotation limits to prevent flipping.
version: "2.0.0"
---

# Coverflow Effect (Swiper)

Swiper-based coverflow carousel with 3D rotation, click-to-center, and info overlays.

**References:**
- [Swiper Coverflow Demo](https://swiperjs.com/demos#effect-coverflow)
- [Swiper API Docs](https://swiperjs.com/swiper-api)

## Installation

```bash
npm install swiper
```

```typescript
import Swiper from 'swiper';
import { EffectCoverflow, FreeMode, Keyboard, Mousewheel } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/effect-coverflow';
```

## The Rotation Formula (CRITICAL)

Swiper calculates rotation as: `rotate × distance_from_center`

**Problem**: With `rotate: 50` and a slide 4 positions away, rotation = 200°, causing the slide to flip backwards.

**Solution**: Limit `slidesPerView` and calculate safe rotation:

```
max_rotation = rotate × (slidesPerView - 1) / 2
```

| slidesPerView | rotate | Max Rotation | Safe? |
|---------------|--------|--------------|-------|
| 5 | 20 | 40° | ✓ |
| 7 | 15 | 45° | ✓ |
| 5 | 45 | 90° | ⚠️ Edge |
| 'auto' | 50 | ∞ | ✗ FLIPS |

**Rule**: Keep `max_rotation < 90°` to prevent flipping.

## Configuration

### Core Options

```typescript
new Swiper('.coverflow-swiper', {
  modules: [EffectCoverflow, FreeMode, Keyboard, Mousewheel],
  effect: 'coverflow',
  grabCursor: true,
  centeredSlides: true,
  slidesPerView: 5,  // Limit to control rotation
  slideToClickedSlide: true,

  coverflowEffect: {
    rotate: 20,      // Keep low with slidesPerView limit
    stretch: 0,      // px offset between slides
    depth: 100,      // z-axis depth
    modifier: 1,     // effect multiplier
    slideShadows: false,
  },
});
```

### Official Swiper Defaults (Reference)

```javascript
coverflowEffect: {
  rotate: 50,      // degrees per slide position
  stretch: 0,      // px offset between slides
  depth: 100,      // z-axis depth
  modifier: 1,     // effect multiplier
  slideShadows: true,
}
```

## Scroll Handling

### Smooth Scrolling with Snapping

```typescript
freeMode: {
  enabled: true,
  sticky: true,  // Snap to slides after momentum
  momentumRatio: 0.5,
  momentumVelocityRatio: 0.5,
}
```

### Detect Horizontal vs Vertical Intent

```typescript
touchAngle: 30,  // Stricter than default 45
touchReleaseOnEdges: true,
passiveListeners: false,  // Allow preventDefault
mousewheel: {
  forceToAxis: true,
  releaseOnEdges: true,
}
```

### Prevent Page Scroll While in Coverflow

The mousewheel/trackpad can trigger both coverflow scroll AND page scroll simultaneously. Add a custom handler:

```typescript
let wheelHandler: ((e: WheelEvent) => void) | null = null;

function initCoverflow() {
  const container = document.querySelector<HTMLElement>('.coverflow-swiper');
  if (!container) return;

  const swiper = new Swiper('.coverflow-swiper', { /* config */ });

  // Prevent page scroll when scrolling within coverflow
  wheelHandler = (e: WheelEvent) => {
    const scrollingRight = e.deltaY > 0 || e.deltaX > 0;
    const scrollingLeft = e.deltaY < 0 || e.deltaX < 0;

    // Allow page scroll only at edges
    const allowPageScroll =
      (swiper.isBeginning && scrollingLeft) ||
      (swiper.isEnd && scrollingRight);

    if (!allowPageScroll) {
      e.preventDefault();
      e.stopPropagation();
    }
  };

  container.addEventListener('wheel', wheelHandler, { passive: false });
}

function destroyCoverflow() {
  if (wheelHandler) {
    const container = document.querySelector<HTMLElement>('.coverflow-swiper');
    container?.removeEventListener('wheel', wheelHandler);
    wheelHandler = null;
  }
  // ... destroy swiper
}
```

## Complete Example

```typescript
import Swiper from 'swiper';
import { EffectCoverflow, FreeMode, Keyboard, Mousewheel } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/effect-coverflow';

let swiperInstance: Swiper | null = null;
let wheelHandler: ((e: WheelEvent) => void) | null = null;

export function initCoverflow(): void {
  const container = document.querySelector<HTMLElement>('.coverflow-swiper');
  if (!container || swiperInstance) return;

  swiperInstance = new Swiper('.coverflow-swiper', {
    modules: [EffectCoverflow, FreeMode, Keyboard, Mousewheel],
    effect: 'coverflow',
    grabCursor: true,
    centeredSlides: true,
    slidesPerView: 5,
    slideToClickedSlide: true,
    touchAngle: 30,
    touchReleaseOnEdges: true,
    passiveListeners: false,
    keyboard: { enabled: true },
    mousewheel: {
      forceToAxis: true,
      releaseOnEdges: true,
    },
    freeMode: {
      enabled: true,
      sticky: true,
      momentumRatio: 0.5,
      momentumVelocityRatio: 0.5,
    },
    coverflowEffect: {
      rotate: 20,
      stretch: 0,
      depth: 100,
      modifier: 1,
      slideShadows: false,
    },
  });

  // Prevent page scroll
  wheelHandler = (e: WheelEvent) => {
    if (!swiperInstance) return;
    const scrollingRight = e.deltaY > 0 || e.deltaX > 0;
    const scrollingLeft = e.deltaY < 0 || e.deltaX < 0;
    const allowPageScroll =
      (swiperInstance.isBeginning && scrollingLeft) ||
      (swiperInstance.isEnd && scrollingRight);
    if (!allowPageScroll) {
      e.preventDefault();
      e.stopPropagation();
    }
  };
  container.addEventListener('wheel', wheelHandler, { passive: false });
}

export function destroyCoverflow(): void {
  if (wheelHandler) {
    const container = document.querySelector<HTMLElement>('.coverflow-swiper');
    container?.removeEventListener('wheel', wheelHandler);
    wheelHandler = null;
  }
  if (swiperInstance) {
    swiperInstance.destroy(true, true);
    swiperInstance = null;
  }
}
```

## CSS: Contain 3D Overflow

The coverflow effect rotates slides in 3D space, which extends them beyond their container bounds. Without overflow containment, this creates page-level horizontal scrollbars.

```css
.coverflow-wrapper {
  overflow-x: hidden;  /* Clip 3D rotated slides */
}

.coverflow-swiper {
  overflow: visible;   /* Allow slides to render outside for 3D effect */
}
```

**Key insight**: The inner `.coverflow-swiper` needs `overflow: visible` for the 3D transforms to render correctly, but the outer wrapper must clip them to prevent page scroll.

## CSS: Active Slide Styling

Use `.swiper-slide-active` to style only the centered slide:

```css
/* Info overlay - hidden by default */
.coverflow-item__info {
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
}

/* Only show on active/centered slide */
.swiper-slide-active .coverflow-item__info {
  opacity: 1;
  pointer-events: auto;
}
```

## CSS: Reflection Effect

```css
.coverflow-item img {
  -webkit-box-reflect: below 0.5em linear-gradient(
    transparent 60%,
    rgba(0, 0, 0, 0.3)
  );
}
```

## Accessibility

### Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  .swiper-slide {
    transition: none !important;
  }
}
```

### Keyboard Navigation

Enabled via `keyboard: { enabled: true }` - arrow keys navigate slides.

## Avoid

- **`slidesPerView: 'auto'` with high rotate** - causes flipping on edge slides
- **`rotate > 45` without limiting slidesPerView** - same flipping issue
- **Forgetting wheel handler cleanup** - causes memory leaks
- **Missing `passiveListeners: false`** - prevents `preventDefault()` from working
- **Using `scale` in coverflowEffect** - can cause weird sizing on distant slides
- **Missing `overflow-x: hidden` on wrapper** - 3D rotated slides create page-level horizontal scrollbars
