---
name: mobile-ui-standards
description: Enforce mobile-first design with compact elements, smaller fonts, and responsive layouts optimized for mobile screens. Use when working on UI, mobile views, responsive design, or when user mentions mobile, UI, layout, or design.
version: 1.0.0
---

# Mobile UI Standards

Mobile-first design principles with compact, optimized layouts for small screens.

## Core Principle: Mobile-First Design

**ALWAYS implement mobile-first design principle.**

Start with mobile, then scale up to desktop:

```css
/* ✅ Mobile-first approach */
.container {
  /* Base styles for mobile */
  padding: 12px;
  font-size: 14px;
}

@media (min-width: 768px) {
  /* Tablet and larger */
  .container {
    padding: 24px;
    font-size: 16px;
  }
}

@media (min-width: 1024px) {
  /* Desktop */
  .container {
    padding: 32px;
    font-size: 18px;
  }
}
```

```css
/* ❌ Desktop-first (avoid) */
.container {
  /* Desktop styles */
  padding: 32px;
  font-size: 18px;
}

@media (max-width: 1024px) {
  /* Scales down */
  .container {
    padding: 24px;
  }
}
```

## Mobile Screen Optimization

### Make Elements Compact

**Mobile screens are small - elements must be compact:**

**Bad - Too large for mobile:**
```tsx
<div className="p-8 my-6">
  <h1 className="text-4xl font-bold mb-6">
    Title
  </h1>
  <p className="text-xl leading-relaxed">
    Content with lots of spacing
  </p>
  <button className="px-8 py-4 text-lg">
    Click Me
  </button>
</div>
```

**Good - Compact for mobile:**
```tsx
<div className="p-3 my-2">
  <h1 className="text-xl font-bold mb-2">
    Title
  </h1>
  <p className="text-sm leading-snug">
    Content with compact spacing
  </p>
  <button className="px-4 py-2 text-sm">
    Click Me
  </button>
</div>
```

### Font Size Guidelines

**Mobile font sizes should be smaller:**

```typescript
// Font size scale for mobile
const mobileFontSizes = {
  xs: '10px',    // Small labels, captions
  sm: '12px',    // Secondary text, helper text
  base: '14px',  // Body text (default)
  lg: '16px',    // Emphasized text
  xl: '18px',    // Subheadings
  '2xl': '20px', // Headings
  '3xl': '24px', // Large headings
  '4xl': '28px'  // Hero text (max for mobile)
};

// Desktop can go larger
const desktopFontSizes = {
  xs: '12px',
  sm: '14px',
  base: '16px',
  lg: '18px',
  xl: '20px',
  '2xl': '24px',
  '3xl': '30px',
  '4xl': '36px',
  '5xl': '48px'
};
```

**Tailwind CSS mobile-first example:**

```tsx
// Responsive font sizes
<h1 className="text-2xl md:text-3xl lg:text-4xl">
  Heading
</h1>

<p className="text-sm md:text-base lg:text-lg">
  Body text
</p>

<span className="text-xs md:text-sm">
  Small text
</span>
```

### Spacing Guidelines

**Mobile spacing should be tighter:**

```typescript
// Mobile spacing scale
const mobileSpacing = {
  xs: '4px',
  sm: '8px',
  md: '12px',
  lg: '16px',
  xl: '20px',
  '2xl': '24px'
};

// Desktop spacing can be more generous
const desktopSpacing = {
  xs: '8px',
  sm: '12px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  '2xl': '48px'
};
```

**Example:**

```tsx
// Mobile-first spacing
<div className="space-y-2 md:space-y-4 lg:space-y-6">
  <Card className="p-3 md:p-4 lg:p-6" />
  <Card className="p-3 md:p-4 lg:p-6" />
</div>
```

## Touch Target Sizes

**Minimum touch target: 44x44 pixels (iOS) / 48x48 pixels (Android)**

**Bad - Touch targets too small:**
```tsx
<button className="px-2 py-1 text-xs">
  Tap Me
</button>
// Results in ~30x24px button - too small!
```

**Good - Adequate touch targets:**
```tsx
<button className="min-h-[44px] min-w-[44px] px-4 py-2">
  Tap Me
</button>
// At least 44x44px for comfortable tapping
```

**Icon buttons:**
```tsx
// Bad
<button className="p-1">
  <Icon size={16} />
</button>

// Good
<button className="p-3 min-h-[44px] min-w-[44px] flex items-center justify-center">
  <Icon size={20} />
</button>
```

## Mobile Layout Patterns

### Stack on Mobile, Row on Desktop

```tsx
// Stack vertically on mobile, horizontal on larger screens
<div className="flex flex-col md:flex-row gap-3 md:gap-4">
  <div className="flex-1">Column 1</div>
  <div className="flex-1">Column 2</div>
  <div className="flex-1">Column 3</div>
</div>
```

### Full-Width on Mobile

```tsx
// Full-width container on mobile, constrained on desktop
<div className="w-full md:max-w-2xl lg:max-w-4xl mx-auto px-4">
  Content
</div>
```

### Hide/Show Based on Screen Size

```tsx
// Mobile menu icon, desktop navigation
<div className="flex items-center">
  {/* Mobile menu button */}
  <button className="md:hidden">
    <MenuIcon />
  </button>

  {/* Desktop navigation */}
  <nav className="hidden md:flex gap-4">
    <Link href="/home">Home</Link>
    <Link href="/about">About</Link>
  </nav>
</div>
```

## Compact Component Examples

### Card Component

```tsx
// Mobile-optimized card
function MobileCard({ title, description, action }: CardProps) {
  return (
    <div className="
      p-3 md:p-4 lg:p-6
      rounded-lg
      space-y-2 md:space-y-3
    ">
      <h3 className="text-base md:text-lg font-semibold">
        {title}
      </h3>
      <p className="text-sm md:text-base text-gray-600">
        {description}
      </p>
      <button className="
        px-4 py-2
        text-sm md:text-base
        min-h-[44px]
      ">
        {action}
      </button>
    </div>
  );
}
```

### Form Inputs

```tsx
// Mobile-friendly form
function MobileForm() {
  return (
    <form className="space-y-3 md:space-y-4">
      <div>
        <label className="block text-sm md:text-base mb-1">
          Email
        </label>
        <input
          type="email"
          className="
            w-full
            px-3 py-2 md:px-4 md:py-3
            text-sm md:text-base
            min-h-[44px]
            rounded-md
          "
        />
      </div>

      <button className="
        w-full
        px-4 py-3
        text-sm md:text-base
        min-h-[44px]
      ">
        Submit
      </button>
    </form>
  );
}
```

### Navigation

```tsx
// Mobile bottom nav, desktop sidebar
function Navigation() {
  return (
    <>
      {/* Mobile bottom nav */}
      <nav className="
        md:hidden
        fixed bottom-0 left-0 right-0
        flex justify-around
        p-2
        bg-white border-t
      ">
        <NavItem icon={<Home />} label="Home" />
        <NavItem icon={<Search />} label="Search" />
        <NavItem icon={<User />} label="Profile" />
      </nav>

      {/* Desktop sidebar */}
      <aside className="
        hidden md:block
        w-64
        p-4
        space-y-2
      ">
        <NavLink href="/">Home</NavLink>
        <NavLink href="/search">Search</NavLink>
        <NavLink href="/profile">Profile</NavLink>
      </aside>
    </>
  );
}
```

## Typography for Mobile

### Line Length

**Mobile line length should be shorter:**

```tsx
// Constrain text width for readability
<p className="max-w-full md:max-w-prose text-sm md:text-base">
  Long paragraphs of text should be constrained to prevent
  lines from becoming too long on mobile devices.
</p>
```

### Line Height

**Tighter line height on mobile:**

```tsx
<p className="
  leading-snug md:leading-normal
  text-sm md:text-base
">
  Text content with responsive line height
</p>
```

### Text Truncation

**Truncate long text on mobile:**

```tsx
// Single line truncation
<h3 className="truncate text-sm md:text-base">
  Very long title that gets truncated on small screens
</h3>

// Multi-line truncation
<p className="line-clamp-2 md:line-clamp-3 text-sm">
  Long description that gets clamped to 2 lines on mobile
  and 3 lines on larger screens.
</p>
```

## Images and Media

### Responsive Images

```tsx
// Different image sizes for different screens
<img
  src="/image-mobile.jpg"
  srcSet="
    /image-mobile.jpg 640w,
    /image-tablet.jpg 1024w,
    /image-desktop.jpg 1920w
  "
  sizes="
    (max-width: 640px) 640px,
    (max-width: 1024px) 1024px,
    1920px
  "
  className="w-full h-auto"
  alt="Responsive image"
/>
```

### Aspect Ratios

```tsx
// Maintain aspect ratio across devices
<div className="
  aspect-square md:aspect-video
  bg-gray-200
  rounded-lg
  overflow-hidden
">
  <img src="/image.jpg" className="w-full h-full object-cover" />
</div>
```

## Performance for Mobile

### Lazy Loading

```tsx
// Lazy load images on mobile
<img
  src="/image.jpg"
  loading="lazy"
  className="w-full h-auto"
/>
```

### Reduce Bundle Size for Mobile

```typescript
// Dynamic imports for mobile
const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
  loading: () => <Spinner />,
  ssr: false // Don't load on mobile if not needed
});
```

## Accessibility on Mobile

### Readable Font Sizes

**Never go below 12px:**

```tsx
// Minimum 12px for readability
<p className="text-xs">  {/* 12px on mobile */}
  Small text but still readable
</p>
```

### Contrast Ratios

**Higher contrast for mobile (outdoor viewing):**

```tsx
// Good contrast for mobile
<div className="bg-white text-gray-900"> {/* High contrast */}
  Content
</div>

// Avoid low contrast
<div className="bg-gray-100 text-gray-400"> {/* ❌ Too low */}
  Hard to read in sunlight
</div>
```

## Mobile-First Checklist

Before deploying mobile UI:

- [ ] Started with mobile styles, scaled up to desktop
- [ ] Font sizes are appropriate for mobile (14px base)
- [ ] Elements are compact and space-efficient
- [ ] Touch targets are at least 44x44px
- [ ] Spacing is tighter on mobile
- [ ] Layout stacks vertically on small screens
- [ ] Text is readable (min 12px)
- [ ] Images are responsive and optimized
- [ ] Navigation works on small screens
- [ ] Forms are easy to fill on mobile
- [ ] Tested on actual mobile devices
- [ ] Performance is good on slower connections

## Responsive Design Breakpoints

**Standard breakpoints:**

```typescript
const breakpoints = {
  sm: '640px',   // Mobile landscape
  md: '768px',   // Tablet
  lg: '1024px',  // Desktop
  xl: '1280px',  // Large desktop
  '2xl': '1536px' // Extra large desktop
};
```

**Tailwind CSS usage:**

```tsx
<div className="
  w-full          {/* Mobile: 100% width */}
  sm:w-auto       {/* Small: auto width */}
  md:w-1/2        {/* Medium: 50% width */}
  lg:w-1/3        {/* Large: 33% width */}
">
  Responsive width
</div>
```

## Common Mobile UI Patterns

### Bottom Sheet / Modal

```tsx
// Mobile: slide from bottom, Desktop: center modal
function Modal({ children, isOpen }: ModalProps) {
  return (
    <div className={`
      fixed inset-0 z-50
      ${isOpen ? 'block' : 'hidden'}
    `}>
      <div className="absolute inset-0 bg-black/50" />
      <div className="
        absolute
        bottom-0 md:bottom-auto md:top-1/2 md:left-1/2
        md:-translate-x-1/2 md:-translate-y-1/2
        w-full md:w-auto md:min-w-[400px] md:max-w-2xl
        bg-white
        rounded-t-2xl md:rounded-2xl
        p-4 md:p-6
      ">
        {children}
      </div>
    </div>
  );
}
```

### Pull to Refresh

```tsx
// Mobile-specific interaction
function MobileList() {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await fetchData();
    setIsRefreshing(false);
  };

  return (
    <div className="md:hidden"> {/* Mobile only */}
      <PullToRefresh onRefresh={handleRefresh}>
        <ListItems />
      </PullToRefresh>
    </div>
  );
}
```

## Summary: Think Mobile First

**Golden Rules:**

1. **Mobile-First Always**
   - Start with mobile styles
   - Scale up to desktop
   - Test on real devices

2. **Compact and Efficient**
   - Smaller fonts (14px base)
   - Tighter spacing
   - Efficient use of space

3. **Touch-Friendly**
   - 44x44px minimum touch targets
   - Adequate spacing between interactive elements
   - Clear visual feedback

4. **Performance Matters**
   - Optimize images
   - Lazy load content
   - Reduce bundle size

5. **Responsive Everything**
   - Flexible layouts
   - Responsive typography
   - Adaptive components

**Remember:** Mobile screens are small. Every pixel counts. Make it compact, make it clear, make it touch-friendly.
