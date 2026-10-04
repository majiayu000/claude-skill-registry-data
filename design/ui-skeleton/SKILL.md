---
name: ui-skeleton
description: Skeleton loading placeholders — gray-shape stand-ins that mirror final content dimensions, use subtle shimmer/pulse animation, and prevent layout shift. Use when replacing generic spinners with content-shaped placeholders, reducing perceived latency on slow routes, or preventing CLS on image-heavy cards.
when_to_use: Replacing generic spinners with content-shaped placeholders (CardSkeleton, ListSkeleton); preventing layout shift (CLS) during data load; designing shimmer/pulse animations; deciding when not to show a skeleton (<200ms loads).
paths:
  - "**/ui/skeletons/**/*.{jsx,tsx,vue,js,ts}"
  - "**/components/skeletons/**/*"
  - "**/*Skeleton*.{jsx,tsx,vue,js,ts}"
---

# Skeleton

## What is a Skeleton?

Skeletons are loading placeholders that mimic the structure of upcoming content—gray shapes showing where text, images, and UI elements will appear. They reduce perceived wait time and prevent layout shift.

## Key Principles

1. **Match Final Layout**: Skeleton shapes must mirror the actual content structure. If a card has title + 3 lines of text + image, the skeleton shows those exact placeholder shapes.

2. **Progressive Disclosure**: Replace skeleton with real content as data loads—don't wait for everything. Partial content is better than full skeleton.

3. **Reduce Perceived Latency**: Skeletons make waiting feel 30% shorter than spinners. Users process "content is coming" faster than "loading..."

## Best Practices

✅ **DO**:
- Match skeleton dimensions to actual content
- Use subtle pulse/shimmer animation
- Create component-specific skeletons (CardSkeleton, ListSkeleton)
- Replace progressively as data arrives
- Keep skeleton code lightweight

❌ **DON'T**:
- Use generic spinners where skeletons fit
- Create skeletons that don't match final layout
- Animate aggressively (distracting)
- Show skeleton for fast-loading content (<200ms)
- Cause layout shift when content replaces skeleton

## Code Patterns

### Recommended

```jsx
// CardSkeleton.jsx
const CardSkeleton = () => (
  <div className="card-skeleton">
    <div className="skeleton-image skeleton-pulse" />
    <div className="skeleton-content">
      <div className="skeleton-title skeleton-pulse" />
      <div className="skeleton-text skeleton-pulse" />
      <div className="skeleton-text skeleton-text--short skeleton-pulse" />
    </div>
  </div>
);

// Usage with loading state
const ProductCard = ({ product, loading }) => {
  if (loading) return <CardSkeleton />;
  return <Card product={product} />;
};
```

```css
/* Skeleton animation */
.skeleton-pulse {
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```

### Avoid

```jsx
// ❌ WRONG - Generic skeleton doesn't match content
const Loading = () => <div className="spinner" />;

// ✅ CORRECT - Skeleton matches actual card structure
const CardSkeleton = () => (
  <div className="card">
    <div className="skeleton skeleton--image" />
    <div className="skeleton skeleton--title" />
    <div className="skeleton skeleton--text" />
  </div>
);
```

## Related Terminologies

- **Component** (UI) - Skeletons are loading variants of components
- **Props** (UI) - Loading state often passed as prop
- **SSR** (Server) - Can prevent need for skeletons
- **Ajax** (State) - Data fetching triggers skeleton display

## Quality Gates

- [ ] Skeleton matches final content structure
- [ ] Subtle animation (not distracting)
- [ ] No layout shift on content load
- [ ] Used for content taking >200ms
- [ ] Component-specific (not generic)

**Source**: `/docs/ui/skeleton.md`
