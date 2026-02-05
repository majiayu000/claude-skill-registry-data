---
name: educational-lab-ui
description: Educational Lab UI Design System - A polished, approachable design aesthetic for educational and learning applications. Combines scientific precision with warmth and accessibility for student-facing interfaces (ages 13+).
license: Complete terms in LICENSE.txt
---

## Educational Lab UI Design System

A refined, production-grade design system for educational applications that balances professional precision with approachable warmth. Perfect for student-facing learning tools, data science education, coding platforms, and academic applications.

### Design Philosophy

**"Scientific precision meets friendly guidance"**

- **Professional yet approachable**: Clean lines and structure without feeling cold or intimidating
- **Clarity first**: Information hierarchy that guides users naturally through complex workflows
- **Trust through polish**: Refined details that build confidence in the learning experience
- **Accessibility-minded**: High contrast, readable typography, clear interactive states

### Color System

Use CSS custom properties for consistency and easy theming:

```css
:root {
  /* Primary: Deep blue (authority, trust, calm) */
  --color-primary: #0A4D8C;
  --color-primary-light: #1E6BB8;
  --color-primary-dark: #083A6B;
  
  /* Accent: Warm orange (energy, action, creativity) */
  --color-accent: #FF6B35;
  --color-accent-light: #FF8B61;
  
  /* Success: Forest green (achievement, progress) */
  --color-success: #0C8B4F;
  
  /* Warning: Amber (caution, attention) */
  --color-warning: #F59E0B;
  
  /* Surfaces: Subtle greys (depth without distraction) */
  --color-surface: #FAFBFC;
  --color-surface-alt: #F3F5F7;
  
  /* Text: Deep slate (readability, hierarchy) */
  --color-text: #1A2332;
  --color-text-muted: #5F6C7B;
  
  /* Shadows: Soft with primary tint */
  --shadow-sm: 0 1px 3px rgba(10, 77, 140, 0.06), 0 1px 2px rgba(10, 77, 140, 0.04);
  --shadow-md: 0 4px 8px rgba(10, 77, 140, 0.08), 0 2px 4px rgba(10, 77, 140, 0.05);
  --shadow-lg: 0 12px 24px rgba(10, 77, 140, 0.12), 0 4px 8px rgba(10, 77, 140, 0.06);
  
  /* Radius: Consistent rounding */
  --radius: 12px;
  --radius-sm: 8px;
  
  /* Typography */
  --font-display: 'DM Sans', -apple-system, system-ui, sans-serif;
  --font-body: 'Inter', -apple-system, system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', 'Courier New', monospace;
}
```

**Color Usage Guidelines:**
- **Primary**: Navigation, key actions, active states, links
- **Accent**: CTAs, important buttons, highlights
- **Success**: Completion indicators, achievements, positive feedback
- **Warning**: Alerts, caution messages, incomplete states
- **Surfaces**: Card backgrounds, input backgrounds, subtle separation
- **Text**: Body copy (--color-text), labels/hints (--color-text-muted)

### Typography

**Font Stack:**
```html
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
```

**DM Sans** (Display/Headings):
- Modern geometric sans-serif with excellent proportions
- Use for: Page titles, section headings, card headers
- Weights: 500 (medium), 600 (semibold), 700-800 (bold/extrabold)
- Apply `.heading` class for consistent styling

**Inter** (Body):
- Highly readable UI font with excellent metrics
- Use for: Body text, labels, descriptions, UI elements
- Weights: 300-800 (use 400 for body, 500-600 for emphasis, 700+ sparingly)

**JetBrains Mono** (Code/Technical):
- Clear monospace font for code and technical content
- Use for: Code blocks, file names, technical identifiers, timestamps
- Weights: 400 (regular), 500-600 (medium/semibold)

**Type Scale:**
- **text-xs** (0.75rem/12px): Metadata, timestamps, micro-labels (use sparingly)
- **text-sm** (0.875rem/14px): Helper text, descriptions, secondary information
- **text-base** (1rem/16px): Body text, form inputs, standard content
- **text-lg** (1.125rem/18px): Subheadings, emphasized text
- **text-xl-2xl** (1.25-1.5rem): Section titles
- **text-2xl-3xl** (1.5-1.875rem): Page titles, major headings

**Typography Rules:**
1. Use `text-sm` for all helper/descriptive text (NOT text-xs unless truly micro-content)
2. Apply `leading-relaxed` (1.625) to improve readability
3. Use `.heading` class for display font: `font-family: var(--font-display); letter-spacing: -0.02em;`
4. Maintain consistent spacing: `mt-1` for tight, `mt-2` for standard, `mt-4+` for sections

### Layout & Spacing

**Background:**
```css
body {
  background: linear-gradient(135deg, #F0F4F8 0%, #E6EDF3 100%);
  background-attachment: fixed;
}
```

**Surface Cards:**
```css
.surface {
  background: white;
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  border: 1px solid rgba(10, 77, 140, 0.08);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.surface:hover {
  box-shadow: var(--shadow-md);
  border-color: rgba(10, 77, 140, 0.12);
}
```

**Spacing Scale:**
- Compact elements: `p-4` to `p-5` (1-1.25rem)
- Standard cards: `p-6` to `p-7` (1.5-1.75rem)
- Spacious sections: `p-8` (2rem)
- Section gaps: `space-y-6` (1.5rem) for related content
- Use `gap-3` to `gap-4` for flexbox/grid spacing

**Rounding:**
- Buttons, inputs, small elements: `rounded-xl` (--radius: 12px)
- Cards, panels: `rounded-xl` to `rounded-2xl`
- Pills/badges: `rounded-full`
- Avoid `rounded-lg` (9px) - use `rounded-xl` (12px) for consistency

### Components

#### Buttons

**Primary Action:**
```html
<button class="px-5 py-2.5 bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-primary-light)] hover:shadow-lg text-white rounded-xl font-semibold transition-all active:scale-95 shadow-md">
  Action
</button>
```

**Secondary Action:**
```html
<button class="px-4 py-2.5 bg-[var(--color-surface)] hover:bg-[var(--color-surface-alt)] text-[var(--color-text)] border-2 border-[var(--color-primary)]/20 hover:border-[var(--color-primary)]/40 rounded-xl font-semibold transition-all">
  Secondary
</button>
```

**Accent CTA:**
```html
<button class="px-5 py-3.5 bg-gradient-to-r from-[var(--color-accent)] to-[var(--color-accent-light)] hover:shadow-lg text-white rounded-xl font-semibold transition-all active:scale-95 shadow-md">
  <i data-lucide="sparkles" class="w-4 h-4"></i>
  Generate
</button>
```

**Icon Button:**
```html
<button class="w-11 h-11 rounded-xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-primary-light)] hover:shadow-lg text-white flex items-center justify-center transition-all active:scale-95 shadow-md">
  <i data-lucide="send" class="w-4 h-4"></i>
</button>
```

#### Form Inputs

**Text Input:**
```html
<input type="text" 
  class="w-full bg-[var(--color-surface)] border-2 border-transparent focus:border-[var(--color-primary)] rounded-xl px-4 py-3 text-sm focus:outline-none transition-all" 
  placeholder="Enter text…" />
```

**Textarea:**
```html
<textarea 
  class="w-full min-h-[160px] bg-[var(--color-surface)] border-2 border-transparent focus:border-[var(--color-primary)] rounded-xl px-4 py-3 text-sm focus:outline-none transition-all resize-none" 
  placeholder="Enter details…"></textarea>
```

**Select:**
```html
<div class="relative">
  <select class="appearance-none bg-[var(--color-surface)] border-2 border-[var(--color-primary)]/20 text-[var(--color-text)] rounded-xl p-3 pr-10 cursor-pointer font-medium">
    <option>Option 1</option>
  </select>
  <i data-lucide="chevron-down" class="absolute right-3 top-3.5 w-4 h-4 text-[var(--color-primary)] pointer-events-none"></i>
</div>
```

#### Badges & Pills

**Status Badge:**
```html
<span class="text-xs font-bold text-[var(--color-primary)] bg-[var(--color-primary)]/10 px-3 py-1.5 rounded-full">
  Active
</span>
```

**Stage Badge (Active):**
```html
<div class="w-9 h-9 rounded-xl bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-primary-light)] text-white flex items-center justify-center font-bold text-sm shadow-md stage-badge-active">
  1
</div>
```

**Success Badge:**
```html
<div class="w-9 h-9 rounded-xl bg-gradient-to-br from-[var(--color-success)] to-emerald-600 text-white flex items-center justify-center font-bold text-sm shadow-md">
  <i data-lucide="check" class="w-4 h-4"></i>
</div>
```

#### Message Bubbles (Chat)

**User Message:**
```html
<div class="max-w-[92%] ml-auto message-bubble">
  <div class="px-4 py-3 rounded-2xl text-sm leading-relaxed bg-gradient-to-br from-[var(--color-primary)] to-[var(--color-primary-light)] text-white border-2 border-transparent shadow-md">
    Message content
  </div>
  <div class="mt-2 text-[11px] font-mono text-[var(--color-text-muted)] text-right">
    Metadata
  </div>
</div>
```

**Assistant Message:**
```html
<div class="max-w-[92%] mr-auto message-bubble">
  <div class="px-4 py-3 rounded-2xl text-sm leading-relaxed bg-white text-[var(--color-text)] border-2 border-[var(--color-primary)]/10 shadow-sm">
    Response content
  </div>
  <div class="mt-2 text-[11px] font-mono text-[var(--color-text-muted)] text-left">
    Metadata
  </div>
</div>
```

#### Progress Bar

```html
<div class="h-3 rounded-full bg-[var(--color-surface-alt)] overflow-hidden shadow-inner">
  <div class="progress-bar h-full" style="width: 60%"></div>
</div>
```

```css
.progress-bar {
  background: linear-gradient(90deg, var(--color-primary), var(--color-primary-light));
  transition: width 0.5s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  overflow: hidden;
}

.progress-bar::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 2s infinite;
  background-size: 200% 100%;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
```

#### Modal

```html
<div class="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
  <div class="bg-white rounded-2xl shadow-2xl w-full max-w-lg border-2 border-[var(--color-primary)]/10 scale-in">
    <div class="p-6 border-b-2 border-[var(--color-primary)]/10 flex items-start justify-between gap-3">
      <div>
        <h3 class="heading text-xl font-semibold text-[var(--color-text)]">Modal Title</h3>
        <p class="text-sm text-[var(--color-text-muted)] mt-2 leading-relaxed">Description text</p>
      </div>
      <button class="text-[var(--color-text-muted)] hover:text-[var(--color-text)] transition-colors">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>
    </div>
    <div class="p-6">
      <div class="flex justify-end gap-3">
        <button class="px-5 py-2.5 bg-white hover:bg-[var(--color-surface)] text-[var(--color-text)] border-2 border-[var(--color-primary)]/20 hover:border-[var(--color-primary)]/40 rounded-xl text-sm font-semibold transition-all">Cancel</button>
        <button class="px-5 py-2.5 bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-primary-light)] hover:shadow-lg text-white rounded-xl text-sm font-semibold transition-all active:scale-95 shadow-md">Confirm</button>
      </div>
    </div>
  </div>
</div>
```

### Animations & Transitions

**Easing:**
Use `cubic-bezier(0.16, 1, 0.3, 1)` for smooth, natural motion (easeOutExpo)

**Entry Animations:**
```css
.scale-in { animation: scaleIn 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.fade-in { animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
.slide-in-from-top-2 { animation: slideIn 0.35s cubic-bezier(0.16, 1, 0.3, 1); }

@keyframes scaleIn {
  from { transform: scale(0.96); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

@keyframes fadeIn { 
  from { opacity: 0; } 
  to { opacity: 1; } 
}

@keyframes slideIn { 
  from { transform: translateY(-8px); opacity: 0; } 
  to { transform: translateY(0); opacity: 1; } 
}
```

**Stagger Delays:**
```html
<div class="scale-in" style="animation-delay: 0.05s;">Panel 1</div>
<div class="scale-in" style="animation-delay: 0.1s;">Panel 2</div>
<div class="scale-in" style="animation-delay: 0.15s;">Panel 3</div>
```

**Message Animation:**
```css
.message-bubble {
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
```

**Interactive States:**
- Hover: Add `shadow-md` or `shadow-lg` lift
- Active: `scale-95` for tactile feedback
- Focus: 2px outline with `focus:outline-2 focus:outline-[var(--color-primary)] focus:outline-offset-2`
- Disabled: `opacity-50 cursor-not-allowed`

### Special Effects

**Texture Overlay (Header/Hero):**
```css
.texture-overlay {
  position: relative;
}

.texture-overlay::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%230A4D8C' fill-opacity='0.02'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  pointer-events: none;
  border-radius: inherit;
}
```

**Gradient Text:**
```css
.gradient-text {
  background: linear-gradient(135deg, var(--color-primary), var(--color-primary-light));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

**Stage Badge Glow (Active):**
```css
.stage-badge-active {
  box-shadow: 0 0 0 3px rgba(10, 77, 140, 0.1),
              0 2px 8px rgba(10, 77, 140, 0.15);
}
```

**Custom Scrollbar:**
```css
.nice-scroll::-webkit-scrollbar { width: 8px; height: 8px; }
.nice-scroll::-webkit-scrollbar-thumb { 
  background: linear-gradient(180deg, var(--color-primary-light), var(--color-primary));
  border-radius: 999px; 
  border: 2px solid transparent;
  background-clip: padding-box;
}
.nice-scroll::-webkit-scrollbar-thumb:hover { 
  background: linear-gradient(180deg, var(--color-primary), var(--color-primary-dark));
  background-clip: padding-box;
}
.nice-scroll::-webkit-scrollbar-track { 
  background: var(--color-surface-alt);
  border-radius: 999px;
}
```

### Accessibility

**Contrast:**
- Text on white: Use `--color-text` (1A2332) - AAA rated
- Muted text: Use `--color-text-muted` (5F6C7B) - AA rated (minimum 14px)
- Button text on primary: White text on primary blue - AAA rated

**Focus States:**
All interactive elements must have visible focus:
```css
button:focus-visible, input:focus-visible, textarea:focus-visible, select:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

**ARIA Labels:**
- Add `aria-label` to icon-only buttons
- Use `aria-current="step"` for active navigation items
- Use `aria-hidden="true"` for decorative elements

**Motion:**
Respect `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Implementation Checklist

When implementing Educational Lab UI:

- [ ] Install fonts: DM Sans, Inter, JetBrains Mono
- [ ] Define CSS custom properties in `:root`
- [ ] Set body gradient background
- [ ] Apply `.surface` class to card components
- [ ] Use `.heading` class for display typography
- [ ] Standardize spacing: p-6/p-7 for cards, gap-3/gap-4 for layouts
- [ ] Use `rounded-xl` consistently (not rounded-lg)
- [ ] Apply border-2 to inputs (not border)
- [ ] Use text-sm for all helper text (not text-xs)
- [ ] Add staggered `scale-in` animations (0.05s-0.3s delays)
- [ ] Implement custom scrollbar styles
- [ ] Add hover shadow elevation
- [ ] Use active:scale-95 for tactile button feedback
- [ ] Define focus states with 2px outline
- [ ] Test color contrast (WCAG AA minimum)
- [ ] Add ARIA labels to icon buttons
- [ ] Verify responsive behavior (mobile-first)

### When to Use This System

**Perfect for:**
- Educational platforms and learning management systems
- Data science tools and analytics dashboards
- Student-facing applications (ages 13+)
- Academic project builders and submission systems
- STEM learning environments
- Coding education platforms
- Research and scientific tools
- Proposal generators and documentation systems

**Less suitable for:**
- Marketing landing pages (consider more expressive designs)
- Creative portfolios (too structured)
- Gaming or entertainment apps (needs more personality)
- Financial/enterprise software (may need more formal aesthetic)

### Customization

To adapt for different domains:

**More playful (younger audiences):**
- Increase color saturation by 10-15%
- Use `rounded-2xl` instead of `rounded-xl`
- Add more accent colors (purple, teal)
- Increase animation scale (0.94 instead of 0.96)

**More formal (enterprise/academic):**
- Reduce saturation by 10%
- Use single-color buttons (no gradients)
- Decrease animation speed (0.4s instead of 0.3s)
- Increase spacing (p-8 instead of p-7)

**Dark mode adaptation:**
```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-surface: #1A2332;
    --color-surface-alt: #242D3C;
    --color-text: #E6EDF3;
    --color-text-muted: #9BA6B2;
    /* Adjust other colors as needed */
  }
  
  body {
    background: linear-gradient(135deg, #0D1117 0%, #1A2332 100%);
  }
}
```

---

## Example: Complete Card Component

```html
<div class="surface p-7 scale-in" style="animation-delay: 0.2s;">
  <!-- Header -->
  <div class="flex items-center justify-between">
    <h3 class="text-sm font-bold text-[var(--color-text-muted)] uppercase tracking-wider">
      Section Title
    </h3>
    <span class="text-xs font-bold text-[var(--color-primary)] bg-[var(--color-primary)]/10 px-3 py-1.5 rounded-full">
      2 / 5
    </span>
  </div>
  
  <!-- Description -->
  <p class="text-sm text-[var(--color-text-muted)] mt-2 leading-relaxed">
    Helper text that explains what this section does.
  </p>
  
  <!-- Content -->
  <div class="mt-4 space-y-3">
    <input type="text" 
      class="w-full bg-[var(--color-surface)] border-2 border-transparent focus:border-[var(--color-primary)] rounded-xl px-4 py-3 text-sm focus:outline-none transition-all" 
      placeholder="Enter information…" />
      
    <textarea 
      class="w-full min-h-[120px] bg-[var(--color-surface)] border-2 border-transparent focus:border-[var(--color-primary)] rounded-xl px-4 py-3 text-sm focus:outline-none transition-all resize-none" 
      placeholder="Enter details…"></textarea>
  </div>
  
  <!-- Actions -->
  <div class="mt-4 flex items-center justify-between">
    <button class="text-sm text-[var(--color-text-muted)] hover:text-[var(--color-text)] font-semibold">
      Secondary action
    </button>
    <button class="px-5 py-2.5 bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-primary-light)] hover:shadow-lg text-white rounded-xl font-semibold transition-all active:scale-95 shadow-md">
      Primary action
    </button>
  </div>
</div>
```

---

This design system provides a complete, cohesive foundation for building polished educational interfaces that feel both professional and approachable.
