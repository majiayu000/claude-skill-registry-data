---
name: canvas-effects
description: Use when implementing Canvas-based visual effects like noise, grain, particles, or animated textures. Applies performance best practices for animation loops and pixel manipulation.
version: "1.0.0"
---

# Canvas Effects Best Practices

Apply when implementing animated visual effects with HTML Canvas.

## Setup

### Basic Canvas Component Pattern
```typescript
interface CanvasEffectConfig {
  density: number;      // 0-1
  speed: number;        // animation speed multiplier
  color: string;        // hex or rgb
  enabled: boolean;
}

class CanvasEffect {
  private canvas: HTMLCanvasElement;
  private ctx: CanvasRenderingContext2D;
  private animationId: number | null = null;
  private config: CanvasEffectConfig;

  constructor(canvas: HTMLCanvasElement, config: CanvasEffectConfig) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d')!;
    this.config = config;
    this.resize();
  }

  resize() {
    const dpr = window.devicePixelRatio || 1;
    const rect = this.canvas.getBoundingClientRect();
    this.canvas.width = rect.width * dpr;
    this.canvas.height = rect.height * dpr;
    this.ctx.scale(dpr, dpr);
  }

  start() {
    if (!this.config.enabled) return;
    const loop = () => {
      this.render();
      this.animationId = requestAnimationFrame(loop);
    };
    loop();
  }

  stop() {
    if (this.animationId) {
      cancelAnimationFrame(this.animationId);
      this.animationId = null;
    }
  }

  destroy() {
    this.stop();
    // cleanup resources
  }

  private render() {
    // implement in subclass
  }
}
```

## Noise/Grain Effect

### ImageData Manipulation (Fast)
```typescript
private render() {
  const imageData = this.ctx.createImageData(
    this.canvas.width,
    this.canvas.height
  );
  const data = imageData.data;
  const density = this.config.density;

  for (let i = 0; i < data.length; i += 4) {
    if (Math.random() > density) continue;

    const noise = Math.random() * 255;
    data[i] = noise;       // R
    data[i + 1] = noise;   // G
    data[i + 2] = noise;   // B
    data[i + 3] = 20;      // A (low opacity)
  }

  this.ctx.putImageData(imageData, 0, 0);
}
```

### Colored Grain
```typescript
private render() {
  const { r, g, b } = hexToRgb(this.config.color);
  // ... in loop:
  data[i] = r + (Math.random() - 0.5) * 50;
  data[i + 1] = g + (Math.random() - 0.5) * 50;
  data[i + 2] = b + (Math.random() - 0.5) * 50;
  data[i + 3] = Math.random() * 30;
}
```

## Performance

### Offscreen Canvas (Critical for Complex Effects)
```typescript
private offscreen: OffscreenCanvas;
private offscreenCtx: OffscreenCanvasRenderingContext2D;

constructor() {
  this.offscreen = new OffscreenCanvas(width, height);
  this.offscreenCtx = this.offscreen.getContext('2d')!;
}

private render() {
  // Draw to offscreen first
  this.renderToOffscreen();
  // Then copy to visible canvas
  this.ctx.drawImage(this.offscreen, 0, 0);
}
```

### Throttle Render Updates
```typescript
private lastRender = 0;
private targetFPS = 30; // grain doesn't need 60fps
private frameInterval = 1000 / this.targetFPS;

private loop = (timestamp: number) => {
  const delta = timestamp - this.lastRender;

  if (delta >= this.frameInterval) {
    this.render();
    this.lastRender = timestamp - (delta % this.frameInterval);
  }

  this.animationId = requestAnimationFrame(this.loop);
};
```

### Reduce Resolution for Performance
```typescript
resize() {
  const dpr = Math.min(window.devicePixelRatio, 1.5); // cap at 1.5x
  // or for grain effects, even lower:
  const dpr = 1; // grain doesn't need retina
}
```

### Visibility Check
```typescript
private observer: IntersectionObserver;

constructor() {
  this.observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        this.start();
      } else {
        this.stop();
      }
    },
    { threshold: 0 }
  );
  this.observer.observe(this.canvas);
}
```

## Text Masking

### Clip Grain to Text Shape
```typescript
private renderGrainInText(text: string) {
  // 1. Clear canvas
  this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

  // 2. Draw text as clip path
  this.ctx.save();
  this.ctx.font = 'bold 120px Unbounded';
  this.ctx.textAlign = 'center';
  this.ctx.textBaseline = 'middle';

  // Create clipping region from text
  this.ctx.beginPath();
  this.ctx.rect(0, 0, this.canvas.width, this.canvas.height);
  this.ctx.clip();

  // Use globalCompositeOperation for text mask
  this.ctx.globalCompositeOperation = 'source-over';
  this.ctx.fillStyle = 'white';
  this.ctx.fillText(text, this.canvas.width / 2, this.canvas.height / 2);

  // 3. Draw grain only where text exists
  this.ctx.globalCompositeOperation = 'source-atop';
  this.renderGrain();

  this.ctx.restore();
}
```

### Alternative: CSS Mask
```css
.grain-canvas {
  mask-image: url('text-mask.svg');
  mask-size: contain;
  -webkit-mask-image: url('text-mask.svg');
}
```

## Reactive Effects

### Cursor Influence Zone
```typescript
private cursorX = 0;
private cursorY = 0;
private influenceRadius = 150;

handleMouseMove = (e: MouseEvent) => {
  const rect = this.canvas.getBoundingClientRect();
  this.cursorX = e.clientX - rect.left;
  this.cursorY = e.clientY - rect.top;
};

private getInfluence(x: number, y: number): number {
  const distance = Math.hypot(x - this.cursorX, y - this.cursorY);
  if (distance > this.influenceRadius) return 0;
  // Exponential falloff
  return Math.pow(1 - distance / this.influenceRadius, 2);
}
```

## Reduced Motion

### Respect User Preference
```typescript
private prefersReducedMotion =
  window.matchMedia('(prefers-reduced-motion: reduce)').matches;

start() {
  if (this.prefersReducedMotion) {
    this.renderStatic(); // Single frame, no animation
    return;
  }
  // ... normal animation loop
}
```

## Cleanup (Critical)

### Always Clean Up
```typescript
destroy() {
  this.stop();
  this.observer?.disconnect();
  window.removeEventListener('resize', this.handleResize);
  window.removeEventListener('mousemove', this.handleMouseMove);
  this.canvas.width = 0;
  this.canvas.height = 0;
}
```

### Astro Integration
```astro
<script>
  import { CanvasGrain } from './CanvasGrain';

  const canvas = document.querySelector('canvas');
  const effect = new CanvasGrain(canvas, config);
  effect.start();

  // Cleanup on page navigation (View Transitions)
  document.addEventListener('astro:before-swap', () => {
    effect.destroy();
  });
</script>
```

## Avoid

- Running at 60fps when 30fps suffices (grain, noise)
- Full DPR on texture effects (wastes GPU)
- Animating when not visible
- Forgetting cleanup on unmount
- Creating new ImageData every frame (reuse it)
- Large influence radius calculations per-pixel (use grid sampling)
