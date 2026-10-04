---
license: Apache-2.0
name: web-wave-designer
description: Creates realistic ocean and water wave effects for web using SVG filters (feTurbulence, feDisplacementMap), CSS animations, and layering techniques. Use for ocean backgrounds, underwater distortion, beach scenes, ripple effects, liquid glass, and water-themed UI. Activate on "ocean wave", "water effect", "SVG water", "ripple animation", "underwater distortion", "liquid glass", "wave animation", "feTurbulence water", "beach waves", "sea foam". NOT for 3D ocean simulation (use WebGL/Three.js), video water effects (use video editing), physics-based fluid simulation (use canvas/WebGL), or simple gradient backgrounds without wave motion.
allowed-tools: Read,Write,Edit,WebFetch,Bash
category: Design & Creative
tags:
  - svg
  - css
  - animation
  - water
  - ocean
  - visual-effects
  - web
pairs-with:
  - skill: web-cloud-designer
    reason: Complete atmospheric scenes with sky and water
  - skill: physics-rendering-expert
    reason: Realistic light refraction and caustics
  - skill: color-theory-palette-harmony-expert
    reason: Ocean palettes and depth gradients
  - skill: web-design-expert
    reason: Integrate water effects into overall web design
---

# Web Wave Designer

Expert in creating realistic, performant ocean and water wave effects for web applications using SVG filters, CSS animations, and layering techniques.

## Decision Points

### 1. Effect Type Selection

```
IF request mentions "background ocean", "seascape", "horizon"
  → Use multi-layer ocean with 3-4 wave layers, parallax movement
  → baseFrequency: [0.005, 0.05] to [0.01, 0.1] across layers
  → Scale: 15-25, Animation: 35-90s drift speeds

ELSE IF request mentions "looking through water", "underwater", "aquarium"
  → Use displacement-only filter on content
  → baseFrequency: [0.015, 0.08], Scale: 18-22
  → Add blue tint: feColorMatrix with boosted blue channel

ELSE IF request mentions "ripples", "pond", "pool"
  → Use equal baseFrequency values for circular patterns
  → baseFrequency: [0.02, 0.02], Scale: 8-15
  → Lower octaves (2-3) for cleaner shapes

ELSE IF request mentions "glass", "modern UI", "subtle"
  → Use low-scale displacement with blur
  → baseFrequency: [0.01, 0.05], Scale: 5-10
  → Add feGaussianBlur stdDeviation="0.5-1"

ELSE IF request mentions "beach", "shore", "foam"
  → Use high Y-frequency for breaking wave motion
  → baseFrequency: [0.008, 0.12], Add foam layer
  → Include fractalNoise for foam texture
```

### 2. Animation Strategy Selection

```
IF performance is critical OR mobile target
  → Use CSS transform animations only
  → Move wave layers, not filter parameters
  → will-change: transform on animated elements

ELSE IF smooth parameter changes needed
  → Use requestAnimationFrame for baseFrequency
  → Limit to 1-2 parameters changing simultaneously
  → Include performance monitoring

ELSE IF simple declarative animation acceptable
  → Use SVG animate on seed attribute
  → Avoid baseFrequency animation (expensive)
  → Use for background effects only
```

### 3. Layer Composition Strategy

```
IF simple single effect
  → One SVG filter applied directly
  → Single feTurbulence → feDisplacementMap chain

ELSE IF depth/realism needed
  → 3-layer system: back (slow), mid, front (fast)
  → Different opacity: 0.3, 0.5, 0.7
  → Staggered animation speeds: 80s, 55s, 35s

ELSE IF includes foam/whitecaps
  → Add 4th layer using fractalNoise for foam
  → High baseFrequency [0.02-0.03]
  → White/transparent gradient, screen blend mode
```

### 4. Color Treatment Decision

```
IF realistic ocean
  → Use linear gradient: deep blue (#0c4a6e) to surface (#0ea5e9)
  → Apply feComponentTransfer to boost blue channel

ELSE IF stylized/cartoon
  → Use flat colors, no gradients
  → Lower numOctaves (1-2) for bold shapes
  → High contrast, saturated palette

ELSE IF underwater tint needed
  → Apply feColorMatrix to entire effect
  → Reduce red (0.85), boost blue (1.1)
  → Add slight green tint for depth
```

### 5. Performance Optimization Decision

```
IF >768px viewport AND GPU available
  → Full multi-layer setup with all effects
  → numOctaves: 3-4, all animation types

ELSE IF mobile OR integrated graphics detected
  → Reduce to 2 layers maximum
  → numOctaves: 2-3, CSS-only animation
  → Add prefers-reduced-motion query

ELSE IF critical performance path
  → CSS gradient waves only, no SVG filters
  → Use radial gradients with transform animation
  → Fallback for low-end devices
```

## Failure Modes

### 1. Static Water (No Movement Anti-Pattern)

**Symptoms:** Water looks like a blue texture, lacks life and motion
**Detection Rule:** If no animation properties present AND no transform changes
**Fix:** 
- Add CSS transform animation: `animation: wave-drift 60s linear infinite`
- Or add SVG animate on seed: `<animate attributeName="seed" dur="20s">`
- Or implement requestAnimationFrame baseFrequency changes

### 2. Square Wave Syndrome (Wrong Noise Type)

**Symptoms:** Boxy, grid-like patterns instead of flowing water
**Detection Rule:** If `type="fractalNoise"` used for water effects
**Fix:**
- Change to `type="turbulence"` immediately
- Adjust baseFrequency to use two different values: `"0.01 0.1"`
- Increase numOctaves to 3-4 for smoother flow

### 3. Stuttering Animation (Filter Parameter Overload)

**Symptoms:** Choppy, low FPS animation especially on mobile
**Detection Rule:** If animating baseFrequency OR multiple filter attributes simultaneously
**Fix:**
- Replace with CSS transform animation on wave layers
- Use seed animation if parameter changes needed
- Add will-change: transform for GPU acceleration
- Implement performance detection with fallbacks

### 4. Edge Artifact Bleeding

**Symptoms:** Sharp cutoffs, rectangular boundaries visible around water effects
**Detection Rule:** If filter region at default 0% 0% 100% 100%
**Fix:**
- Expand filter region: `x="-10%" y="-10%" width="120%" height="120%"`
- For strong displacement, use: `x="-20%" y="-20%" width="140%" height="140%"`
- Ensure seamless wave layer width of 200% for drift animation

### 5. Performance Death Spiral (Octave Explosion)

**Symptoms:** Browser lag, high CPU usage, frame drops below 30fps
**Detection Rule:** If numOctaves > 4 OR scale > 40 OR multiple complex filters
**Fix:**
- Reduce numOctaves to 3 maximum
- Cap scale at 30 for realistic effects
- Implement performance tiers based on device capabilities
- Use @media (prefers-reduced-motion) to disable on request

## Worked Examples

### Complete Mobile Ocean Background Implementation

**Scenario:** Create a responsive ocean background that performs well on mobile devices while maintaining visual appeal.

**Initial Requirements Analysis:**
- Mobile performance constraint → CSS-first animation strategy
- Ocean background → Multi-layer approach needed
- Responsive → Performance detection and fallbacks required

**Step 1: Performance Detection**
```javascript
const detectPerformanceTier = () => {
  const canvas = document.createElement('canvas');
  const gl = canvas.getContext('webgl');
  if (!gl) return 'minimal';
  
  // Mobile user agent check
  if (/Mobile|Android|iPhone/i.test(navigator.userAgent)) return 'mobile';
  
  return 'desktop';
};
```

**Step 2: Tier-Appropriate Filter Design**
For mobile tier, expert chooses:
- Only 2 wave layers (not 3-4)
- numOctaves: 2 (not 4) - 75% performance improvement
- Scale: 15 (not 25) - reduces GPU load
- CSS-only animation - no JS parameter changes

```html
<svg style="position:absolute;width:0;height:0">
  <defs>
    <filter id="mobileWave1" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="turbulence" baseFrequency="0.006 0.06" 
                    numOctaves="2" seed="1"/>
      <feDisplacementMap in="SourceGraphic" scale="15"/>
    </filter>
    <filter id="mobileWave2" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="turbulence" baseFrequency="0.01 0.08" 
                    numOctaves="2" seed="2"/>
      <feDisplacementMap in="SourceGraphic" scale="18"/>
    </filter>
  </defs>
</svg>
```

**Step 3: Decision Point Navigation - Animation Strategy**
Expert recognizes mobile constraint → CSS transform only:
```css
.wave-mobile {
  width: 200%;
  height: 60%;
  position: absolute;
  bottom: 0;
  will-change: transform;
}

.wave-1 {
  filter: url(#mobileWave1);
  animation: wave-drift 70s linear infinite;
  opacity: 0.4;
}

.wave-2 {
  filter: url(#mobileWave2);
  animation: wave-drift 45s linear infinite;
  animation-delay: -15s;
  opacity: 0.6;
}

@keyframes wave-drift {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}

@media (prefers-reduced-motion: reduce) {
  .wave-1, .wave-2 {
    animation: none;
  }
}
```

**Step 4: What Novice Misses vs Expert Catches**

*Novice approach:*
- Uses desktop settings on mobile (numOctaves: 4, scale: 30)
- Animates baseFrequency with JavaScript
- Forgets will-change optimization
- No reduced-motion respect

*Expert catches:*
- Performance budget: 2 octaves max on mobile
- CSS-only animation for 60fps target
- GPU acceleration hints with will-change
- Accessibility with prefers-reduced-motion
- 200% width for seamless looping
- Proper filter region expansion to prevent edge artifacts

**Result:** Smooth 60fps ocean animation on mobile devices vs stuttering 20-30fps novice implementation.

## Quality Gates

**Motion Smoothness:**
- [ ] Animation maintains 45+ fps on target devices (measure with Performance tab)
- [ ] No visible stuttering during continuous playback for 30+ seconds
- [ ] Wave drift creates seamless loop without jump/reset moment
- [ ] Multiple wave layers move at different speeds (parallax depth)

**Color Accuracy:**
- [ ] Water appears blue-tinted, not gray or muddy (verify turbulence type)
- [ ] Depth gradient present from surface (lighter) to deep (darker)
- [ ] Transparency/opacity allows background content to show through
- [ ] Color contrast meets accessibility standards if text overlaid

**Performance Budget:**
- [ ] Total numOctaves across all filters ≤ 8 for mobile, ≤ 12 for desktop
- [ ] Filter regions expanded (-10% minimum) to prevent edge artifacts
- [ ] will-change: transform applied to all animated wave elements
- [ ] @media (prefers-reduced-motion) disables animation when requested

**Visual Realism:**
- [ ] baseFrequency uses two different values (X ≠ Y) for directional flow
- [ ] Scale values 10-30 range (realistic refraction, not psychedelic)
- [ ] Wave layers have varying opacity (0.3-0.8 range for depth)
- [ ] No square/grid patterns visible (confirms turbulence type correct)

**Integration Ready:**
- [ ] SVG filters defined in hidden <defs> block, not inline
- [ ] Unique filter IDs prevent conflicts with other components
- [ ] Responsive behavior tested on mobile/tablet/desktop viewports
- [ ] Works with existing CSS frameworks (no position/z-index conflicts)

## NOT-FOR Boundaries

**3D Ocean Rendering:** Volumetric water, realistic wave physics, underwater caustics with accurate light rays → Use WebGL libraries (Three.js Ocean, react-three-fiber water)

**Video Water Effects:** Compositing water onto video, motion tracking liquid → Use After Effects, Blender, or video editing software

**Physics Simulation:** Interactive water that responds to mouse/touch, splash dynamics, fluid collision → Use canvas with matter.js or Box2D physics engines

**High-Frequency Details:** Spray droplets, micro-foam bubbles, realistic surface tension → Use particle systems or WebGL shaders

**3D Integration:** Water that interacts with 3D models, accurate reflection/refraction of 3D scenes → Use WebGL/Three.js with proper lighting models