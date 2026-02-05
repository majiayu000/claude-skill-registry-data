---
name: cursor-reactivity
description: Use when implementing cursor-based interactions like proximity effects, hover zones, or elements that react to mouse/touch position. Applies patterns for throttling, falloff, and mobile alternatives.
version: "1.0.0"
---

# Cursor Reactivity Best Practices

Apply when elements react to cursor proximity or movement.

## Core Concept

Cursor reactivity = elements respond to cursor position without the cursor itself being styled. The cursor is invisible influence; elements are the responders.

## Setup

### Basic Proximity Detector
```typescript
interface ReactivityConfig {
  radius: number;           // influence zone in pixels
  falloff: 'linear' | 'exponential' | 'ease-out';
  intensity: number;        // 0-1 multiplier
  recovery: number;         // ms to return to rest
  enabled: boolean;
}

class ProximityEffect {
  private elements: HTMLElement[];
  private config: ReactivityConfig;
  private cursorX = 0;
  private cursorY = 0;

  constructor(selector: string, config: ReactivityConfig) {
    this.elements = [...document.querySelectorAll(selector)];
    this.config = config;
    this.bindEvents();
  }

  private bindEvents() {
    window.addEventListener('mousemove', this.handleMove, { passive: true });
  }

  private handleMove = (e: MouseEvent) => {
    this.cursorX = e.clientX;
    this.cursorY = e.clientY;
    this.update();
  };

  private update() {
    for (const el of this.elements) {
      const rect = el.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      const distance = Math.hypot(this.cursorX - centerX, this.cursorY - centerY);
      const influence = this.calculateInfluence(distance);

      this.applyEffect(el, influence);
    }
  }

  private calculateInfluence(distance: number): number {
    if (distance > this.config.radius) return 0;

    const normalized = 1 - distance / this.config.radius;

    switch (this.config.falloff) {
      case 'linear':
        return normalized * this.config.intensity;
      case 'exponential':
        return Math.pow(normalized, 2) * this.config.intensity;
      case 'ease-out':
        return (1 - Math.pow(1 - normalized, 3)) * this.config.intensity;
    }
  }

  private applyEffect(el: HTMLElement, influence: number) {
    // Override in subclass or pass callback
    el.style.setProperty('--influence', String(influence));
  }
}
```

## Falloff Functions

| Type | Feel | Use Case |
|------|------|----------|
| `linear` | Even, predictable | Subtle effects |
| `exponential` | Strong near, weak far | Magnetic feel |
| `ease-out` | Smooth, natural | Most UI interactions |

```typescript
// Visual comparison at 50% distance:
// linear:      0.5
// exponential: 0.25
// ease-out:    0.875
```

## Throttling (Critical for Performance)

### Throttle Mouse Events
```typescript
private lastUpdate = 0;
private throttleMs = 16; // ~60fps max

private handleMove = (e: MouseEvent) => {
  const now = performance.now();
  if (now - this.lastUpdate < this.throttleMs) return;

  this.lastUpdate = now;
  this.cursorX = e.clientX;
  this.cursorY = e.clientY;
  this.update();
};
```

### Use requestAnimationFrame for Visual Updates
```typescript
private rafId: number | null = null;
private needsUpdate = false;

private handleMove = (e: MouseEvent) => {
  this.cursorX = e.clientX;
  this.cursorY = e.clientY;
  this.needsUpdate = true;

  if (!this.rafId) {
    this.rafId = requestAnimationFrame(this.tick);
  }
};

private tick = () => {
  if (this.needsUpdate) {
    this.update();
    this.needsUpdate = false;
  }
  this.rafId = requestAnimationFrame(this.tick);
};
```

## Recovery Animation

### CSS Transition for Recovery
```css
.reactive-element {
  --influence: 0;
  transition: transform 0.4s ease-out, opacity 0.4s ease-out;
  transform: scale(calc(1 + var(--influence) * 0.1));
}
```

### JS-Controlled Recovery
```typescript
private isActive = false;
private recoveryTimeout: number | null = null;

private handleMove = (e: MouseEvent) => {
  this.isActive = true;
  clearTimeout(this.recoveryTimeout);
  // ... update logic

  this.recoveryTimeout = setTimeout(() => {
    this.recover();
  }, 100); // start recovery 100ms after last movement
};

private recover() {
  const decay = () => {
    this.influence *= 0.9; // decay factor
    if (this.influence > 0.01) {
      requestAnimationFrame(decay);
    } else {
      this.influence = 0;
      this.isActive = false;
    }
    this.applyEffect();
  };
  decay();
}
```

## Mobile Touch Alternatives

### Touch-Based Interaction
```typescript
private bindEvents() {
  if ('ontouchstart' in window) {
    this.bindTouchEvents();
  } else {
    this.bindMouseEvents();
  }
}

private bindTouchEvents() {
  // Option 1: Touch position = cursor position
  window.addEventListener('touchmove', (e) => {
    const touch = e.touches[0];
    this.cursorX = touch.clientX;
    this.cursorY = touch.clientY;
    this.update();
  }, { passive: true });

  // Option 2: Tap to activate
  this.elements.forEach(el => {
    el.addEventListener('touchstart', () => {
      this.activateElement(el);
    });
    el.addEventListener('touchend', () => {
      this.deactivateElement(el);
    });
  });
}
```

### Tap-to-Burst Pattern
```typescript
private handleTap(el: HTMLElement) {
  // Immediate burst
  el.style.setProperty('--influence', '1');

  // Animate decay
  el.animate([
    { '--influence': 1 },
    { '--influence': 0 }
  ], {
    duration: this.config.recovery,
    easing: 'ease-out',
    fill: 'forwards'
  });
}
```

### Gyroscope Alternative
```typescript
private bindGyroscope() {
  if (!('DeviceOrientationEvent' in window)) return;

  window.addEventListener('deviceorientation', (e) => {
    // Map device tilt to influence
    const tiltX = (e.gamma || 0) / 45; // -1 to 1
    const tiltY = (e.beta || 0) / 45;

    this.influence = Math.hypot(tiltX, tiltY);
    this.update();
  });
}
```

## CSS Custom Property Pattern

### Pass Influence to CSS
```typescript
private applyEffect(el: HTMLElement, influence: number) {
  el.style.setProperty('--cursor-influence', String(influence));
  el.style.setProperty('--cursor-x', `${this.cursorX}px`);
  el.style.setProperty('--cursor-y', `${this.cursorY}px`);
}
```

### Use in CSS
```css
.reactive-element {
  --cursor-influence: 0;

  /* Subtle scale */
  transform: scale(calc(1 + var(--cursor-influence) * 0.05));

  /* Glow intensity */
  filter: drop-shadow(0 0 calc(var(--cursor-influence) * 20px) var(--glow-color));

  /* Grain speed (used by JS) */
  --grain-speed: calc(0.5 + var(--cursor-influence) * 2);
}
```

## Reduced Motion

### Always Respect Preference
```typescript
private prefersReducedMotion =
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

constructor() {
  if (this.prefersReducedMotion) {
    this.config.enabled = false;
    return;
  }
  // ... normal setup
}
```

### Or Simplify Effect
```typescript
private applyEffect(el: HTMLElement, influence: number) {
  if (this.prefersReducedMotion) {
    // Simple opacity change only, no motion
    el.style.opacity = String(1 - influence * 0.2);
    return;
  }
  // Full effect...
}
```

## Cleanup

### Remove All Listeners
```typescript
destroy() {
  window.removeEventListener('mousemove', this.handleMove);
  window.removeEventListener('touchmove', this.handleTouchMove);
  window.removeEventListener('deviceorientation', this.handleOrientation);

  if (this.rafId) cancelAnimationFrame(this.rafId);
  if (this.recoveryTimeout) clearTimeout(this.recoveryTimeout);

  // Reset elements
  this.elements.forEach(el => {
    el.style.removeProperty('--cursor-influence');
  });
}
```

## Avoid

- Calculating distance for every pixel (use element centers or sampling)
- Updating on every mousemove without throttle
- Forgetting mobile/touch alternatives
- Hard-coded values (use config)
- Ignoring reduced motion preference
- Memory leaks from unremoved event listeners
- Using transform on elements that have layout-dependent children
