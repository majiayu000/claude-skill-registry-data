---
name: modern-frontend-design
description: Comprehensive frontend design system for creating distinctive, production-grade interfaces that avoid generic AI aesthetics. Use when users request web components, pages, applications, or any frontend interface. Provides design workflows, aesthetic guidelines, code patterns, animation libraries, typography systems, color theory, and anti-patterns to create memorable, context-specific designs that feel genuinely crafted rather than generated.
---

# Modern Frontend Design System

This skill provides a comprehensive system for creating distinctive, production-grade frontend interfaces that transcend generic AI aesthetics. Every design should feel intentionally crafted for its specific context.

## Core Philosophy

**Every interface tells a story.** Design is not decoration applied to functionality - it's the synthesis of purpose, emotion, and interaction into a cohesive experience.

Before writing any code, establish:
1. **Context**: What problem does this solve? Who uses it? What emotion should it evoke?
2. **Concept**: What's the core metaphor or idea that drives all design decisions?
3. **Commitment**: Choose a bold direction and execute it with precision throughout.

## Design Process Workflow

### Phase 1: Discovery & Concept (ALWAYS START HERE)

Understand the request deeply:
- What is the literal requirement?
- What is the underlying need?
- What emotional response should this evoke?
- What makes this different from everything else?

Choose ONE primary aesthetic direction from:
- **Neo-Brutalist**: Raw concrete textures, bold typography, harsh contrasts
- **Soft Minimalism**: Muted palettes, generous whitespace, subtle interactions
- **Retro-Futuristic**: CRT effects, scan lines, neon glows, cyberpunk elements
- **Editorial/Magazine**: Dynamic grids, mixed media, bold type treatments
- **Organic/Natural**: Flowing shapes, nature-inspired palettes, paper textures
- **Glass Morphism**: Translucent layers, backdrop filters, depth through transparency
- **Maximalist Chaos**: Information density, collage aesthetics, controlled disorder
- **Art Deco**: Geometric patterns, gold accents, vintage luxury
- **Memphis Design**: Bold patterns, primary colors, playful geometry
- **Swiss Design**: Grid systems, sans-serif type, functional beauty
- **Dark Academia**: Rich textures, serif typography, scholarly atmosphere
- **Y2K Revival**: Gradients, metallics, early-web nostalgia
- **Custom Hybrid**: Combine 2-3 directions for something unique

### Phase 2: Design System Definition

Define your design tokens BEFORE coding:
```css
/* Example: Neo-Brutalist System */
:root {
  /* Typography Scale */
  --font-display: 'Archivo Black', sans-serif;  /* Never use Inter/Roboto */
  --font-body: 'Work Sans', sans-serif;
  --scale-base: clamp(1rem, 2vw, 1.125rem);
  --scale-ratio: 1.333;  /* Perfect fourth */
  
  /* Spatial System */
  --space-unit: 0.5rem;
  --grid-columns: 12;
  --container-max: 1440px;
  
  /* Color Philosophy */
  --color-ink: #0A0A0A;
  --color-paper: #F7F3F0;
  --color-accent: #FF3E00;
  --color-bruise: #7B68EE;
  
  /* Animation Timing */
  --ease-out-expo: cubic-bezier(0.19, 1, 0.22, 1);
  --duration-base: 200ms;
  --stagger-delay: 50ms;
}
```

### Phase 3: Implementation Patterns

#### Typography Hierarchy

Never use default font stacks. Always pair fonts intentionally:
```css
/* Bad - Generic AI Slop */
font-family: Inter, system-ui, sans-serif;

/* Good - Intentional Pairing */
font-family: 'Instrument Serif', 'Crimson Pro', serif;  /* Editorial */
font-family: 'Space Mono', 'JetBrains Mono', monospace;  /* Tech */
font-family: 'Bebas Neue', 'Oswald', sans-serif;  /* Bold Display */
font-family: 'Playfair Display', 'Libre Baskerville', serif;  /* Luxury */
```

#### Color Usage

Avoid predictable gradients. Use color with intention:
```css
/* Bad - Overused Purple Gradient */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* Good - Context-Specific Approaches */
/* Risograph-inspired duotone */
background: 
  linear-gradient(45deg, #FF6B6B 0%, transparent 70%),
  linear-gradient(-45deg, #4ECDC4 0%, transparent 70%),
  #F7FFF7;

/* Noise texture overlay */
background: 
  url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www[.]w3[.]org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.02'/%3E%3C/svg%3E"),
  linear-gradient(180deg, #0A0E27 0%, #151B3D 100%);
```

#### Layout Strategies

Break the grid intentionally:
```css
/* Dynamic asymmetric grid */
.container {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 3fr 1fr;
  grid-template-rows: auto 1fr auto;
  gap: clamp(1rem, 3vw, 2rem);
}

.hero-content {
  grid-column: 1 / span 3;
  grid-row: 2;
  z-index: 2;
}

.hero-visual {
  grid-column: 3 / -1;
  grid-row: 1 / span 2;
  margin-top: -10vh;  /* Break container boundaries */
}
```

### Phase 4: Animation & Interaction

#### Entrance Animations

One orchestrated entrance beats scattered micro-interactions:
```css
[@]keyframes revealUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.98);
  }
}

.hero > * {
  animation: revealUp 800ms var(--ease-out-expo) both;
}

.hero > *:nth-child(1) { animation-delay: 0ms; }
.hero > *:nth-child(2) { animation-delay: 80ms; }
.hero > *:nth-child(3) { animation-delay: 160ms; }
```

#### Scroll-Triggered Effects
```javascript
// Parallax with Intersection Observer
const parallaxElements = document.querySelectorAll('[data-parallax]');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const scrolled = window.pageYOffset;
      const rate = scrolled * entry[.]target.dataset.parallax;
      entry[.]target[.]style.transform = `translateY(${rate}px)`;
    }
  });
});
parallaxElements.forEach(el => observer.observe(el));
```

#### Hover States That Surprise
```css
.card {
  transition: transform 200ms var(--ease-out-expo);
}

.card:hover {
  transform: perspective(1000px) rotateX(5deg) scale(1.02);
}

.card:hover::before {
  /* Reveal hidden layer */
  opacity: 1;
  transform: translate(-5px, -5px);
}
```

## Critical Anti-Patterns to Avoid

### The "AI Look" Checklist

NEVER do all of these together:
- ❌ Purple/blue gradient backgrounds
- ❌ Inter or system fonts
- ❌ Centered hero with subheading
- ❌ 3-column feature cards
- ❌ Rounded corners on everything
- ❌ Drop shadows on all cards
- ❌ #6366F1 as primary color
- ❌ 16px border radius
- ❌ "Modern", "Clean", "Simple" as only descriptors

### Common Pitfalls

1. **Over-animation**: Not everything needs to move. Choose moments.
2. **Timid Choices**: Commit fully to your aesthetic direction.
3. **Mismatched Complexity**: Minimal designs need perfect details, not elaborate code.
4. **Context Ignorance**: A banking app shouldn't look like a music festival site.
5. **Trend Chasing**: Glass morphism everywhere is the new purple gradient.

## Framework-Specific Guidelines

### React Components

For React, emphasize composition and state management:
```jsx
// Use compound components for complex UI
const Card = ({ children }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  return (
    <CardContext.Provider value={{ isExpanded, setIsExpanded }}>
      <article className="card" data-expanded={isExpanded}>
        {children}
      </article>
    </CardContext.Provider>
  );
};

Card.Header = ({ children }) => {
  const { setIsExpanded } = useContext(CardContext);
  return (
    <header onClick={() => setIsExpanded(prev => !prev)}>
      {children}
    </header>
  );
};
```

### Vue Composition

For Vue, leverage reactive design:
```vue
<script setup>
import { ref, computed } from 'vue'

const theme = ref('dark')
const themeClasses = computed(() => ({
  'theme-dark': theme.value === 'dark',
  'theme-light': theme.value === 'light'
}))
</script>
```

## Quality Checklist

Before delivering any frontend:

### Visual Impact
- [ ] Does it have a clear point of view?
- [ ] Would someone remember this tomorrow?
- [ ] Does it avoid all generic AI patterns?

### Technical Excellence
- [ ] Responsive across all breakpoints?
- [ ] Accessible (ARIA labels, keyboard navigation)?
- [ ] Performance optimized (lazy loading, code splitting)?
- [ ] Cross-browser tested?

### Attention to Detail
- [ ] Custom focus states defined?
- [ ] Loading and error states designed?
- [ ] Micro-interactions enhance usability?
- [ ] Typography hierarchy consistent?

## Resource Usage

### Scripts
- **generate-palette[.]py**: Create cohesive color systems from a base color
- **optimize-animations[.]py**: Convert CSS animations to GPU-accelerated transforms
- **accessibility-check[.]py**: Validate WCAG compliance

### References
- **aesthetic-systems[.]md**: Deep dive into each design direction with examples
- **typography-pairings[.]md**: Curated font combinations by mood and purpose
- **animation-curves[.]md**: Custom easing functions and timing patterns
- **color-psychology[.]md**: Emotional impact of color choices

### Assets
- **reset-styles/**: Modern CSS reset variations
- **grid-systems/**: Flexible grid templates
- **icon-sets/**: Custom SVG icon libraries
- **texture-library/**: Background patterns and noise textures

## Final Reminder

You are not generating "a frontend" - you are crafting an experience. Every choice should serve the concept. Every detail should reinforce the story. The user should feel something when they see it.

Make it memorable. Make it distinctive. Make it feel designed, not generated.
