---
name: navbar-animation1
description: Production-ready navbar animations for desktop and mobile. Use when creating animated navigation bars with scroll-triggered effects, mobile menu slide-in panels, staggered link animations, or responsive hamburger menus. Includes React/Next.js components with Tailwind CSS and pure CSS keyframe animations.
---

# Navbar Animation Patterns

Production-tested navbar animations from ArchiKunszt project. Smooth, accessible, performant.

## Animation Categories

| Category | Effect | Trigger |
|----------|--------|---------|
| Desktop scroll | Logo/nav/CTA slide out + fade | `window.scrollY > 50` |
| Desktop expand | Reverse slide-in on hamburger click | User click (when scrolled) |
| Mobile panel | Full-screen slide from left | Menu toggle |
| Mobile links | Staggered slide from right | Panel open |
| Mobile CTAs | Staggered slide from bottom | Panel open |
| Nav link hover | Underline grows left-to-right | Hover |

## Key Behavior: Scroll + Hamburger Expand

**Flow:**
1. **Top of page** → Full navbar visible (logo text + nav links + CTA)
2. **User scrolls down** → Elements collapse/hide, hamburger appears
3. **User clicks hamburger** → Elements expand back (without scrolling to top)
4. **User scrolls back to top** → Hamburger hides, expanded state resets

This allows quick menu access while scrolled without returning to top.

## Core Easing Function

All animations use this cubic-bezier for smooth deceleration:
```css
cubic-bezier(0.16, 1, 0.3, 1)
```

## Quick Implementation

### 1. Desktop Scroll-Triggered Collapse

React/Next.js with Tailwind:
```tsx
const [isScrolled, setIsScrolled] = useState(false);
const [isExpanded, setIsExpanded] = useState(false);

useEffect(() => {
  const handleScroll = () => {
    const scrolled = window.scrollY > 50;
    setIsScrolled(scrolled);
    if (!scrolled) setIsExpanded(false);
  };
  window.addEventListener("scroll", handleScroll, { passive: true });
  return () => window.removeEventListener("scroll", handleScroll);
}, []);

const showFullNav = !isScrolled || isExpanded;
```

Apply to elements:
```tsx
{/* Logo text - slides left */}
<span className={cn(
  "transition-all duration-500 ease-out",
  showFullNav
    ? "max-w-[200px] opacity-100 translate-x-0"
    : "max-w-0 opacity-0 -translate-x-4"
)}>
  Logo Text
</span>

{/* Nav links - slide right */}
<nav className={cn(
  "transition-all duration-500 ease-out overflow-hidden",
  showFullNav
    ? "max-w-[600px] opacity-100 translate-x-0"
    : "max-w-0 opacity-0 translate-x-8"
)}>
```

### 2. Mobile Menu Panel

CSS keyframes for panel + staggered children:
```css
@keyframes slideInFromLeft {
  from { transform: translateX(-100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

@keyframes slideInFromRight {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

@keyframes slideInFromBottom {
  from { transform: translateY(100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.mobile-menu-panel {
  animation: slideInFromLeft 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.mobile-nav-link {
  opacity: 0;
  animation: slideInFromRight 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.mobile-nav-link:nth-child(1) { animation-delay: 0.1s; }
.mobile-nav-link:nth-child(2) { animation-delay: 0.175s; }
.mobile-nav-link:nth-child(3) { animation-delay: 0.25s; }
.mobile-nav-link:nth-child(4) { animation-delay: 0.325s; }
.mobile-nav-link:nth-child(5) { animation-delay: 0.4s; }

.mobile-cta {
  opacity: 0;
  animation: slideInFromBottom 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.mobile-cta:nth-child(1) { animation-delay: 0.5s; }
.mobile-cta:nth-child(2) { animation-delay: 0.6s; }
.mobile-cta:nth-child(3) { animation-delay: 0.7s; }
```

### 3. Nav Link Underline Hover

```css
.nav-link {
  position: relative;
}
.nav-link::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--accent-color);
  transition: width 0.3s ease;
}
.nav-link:hover::after {
  width: 100%;
}
```

## Accessibility

Always include reduced motion support:
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## References

- **Complete React component**: See [references/header-component.tsx](references/header-component.tsx)
- **Full CSS animations**: See [references/animations.css](references/animations.css)
