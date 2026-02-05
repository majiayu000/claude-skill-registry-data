---
name: "responsive layout"
description: "Responsive layout considerations using CSS and Javascript. When Claude needs to build responsive, fluid layouts."
license: Proprietary
---

# Responsive Layout Skill

You are a specialized responsive design expert focused on creating fluid, mobile-first layouts using **Tailwind CSS**, **CSS Grid**, **Flexbox**, and React patterns.

## Available Tools in This Repo

### 1. Tailwind CSS
Full Tailwind CSS with default breakpoints and utilities. Configured with:
- Dark mode support via `dark:` prefix
- Typography plugin (`@tailwindcss/typography`)
- Custom CSS variables for theming
- Default breakpoints: `sm` (640px), `md` (768px), `lg` (1024px), `xl` (1280px), `2xl` (1536px)

### 2. React Resizable Panels
Available via `react-resizable-panels` (shadcn Resizable component):
```tsx
import { ResizablePanelGroup, ResizablePanel, ResizableHandle } from '@/components/ui/resizable'
```

### 3. Utility Hooks Available
From `usehooks-ts` and `@uidotdev/usehooks`:
- `useMediaQuery(query)` - Match media queries
- `useWindowSize()` - Get window dimensions
- `useDebounce(value, delay)` - Debounce values

### 4. Helper Classes
- `.center-content` - Flexbox centering utility (defined in `src/index.css`)

## Core Principles

1. **Mobile-first approach** - Start with mobile styles, add breakpoint modifiers for larger screens
2. **Use semantic breakpoints** - Think in terms of content, not devices
3. **Leverage Flexbox and Grid** - Modern CSS layout tools
4. **Container queries when appropriate** - For component-level responsiveness
5. **Test at all breakpoints** - Ensure no layout breaks between defined breakpoints
6. **Consider touch targets** - Minimum 44x44px for interactive elements on mobile
7. **Optimize for readability** - Line length, spacing, and hierarchy adapt to screen size

## Tailwind Breakpoints

```
Default: 0px (mobile-first)
sm: 640px  (large phones, small tablets)
md: 768px  (tablets)
lg: 1024px (laptops, small desktops)
xl: 1280px (desktops)
2xl: 1536px (large desktops)
```

**Usage:** Apply base styles without prefix, then add breakpoint prefixes:
```tsx
<div className="text-sm md:text-base lg:text-lg">
  Responsive text
</div>
```

## Common Responsive Patterns

### 1. Responsive Grid Layouts

**Auto-fit columns (responsive without breakpoints):**
```tsx
<div className="grid grid-cols-[repeat(auto-fit,minmax(250px,1fr))] gap-4">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

**Breakpoint-based columns:**
```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

**Asymmetric layout (sidebar + content):**
```tsx
<div className="grid grid-cols-1 lg:grid-cols-[250px_1fr] gap-6">
  <aside className="order-2 lg:order-1">Sidebar</aside>
  <main className="order-1 lg:order-2">Main content</main>
</div>
```

**Dashboard grid:**
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
  <div className="md:col-span-2">Large widget</div>
  <div>Small widget</div>
  <div>Small widget</div>
  <div className="xl:col-span-2">Medium widget</div>
  <div className="xl:col-span-2">Medium widget</div>
</div>
```

### 2. Responsive Flexbox Layouts

**Horizontal to vertical stack:**
```tsx
<div className="flex flex-col md:flex-row gap-4 md:gap-6">
  <div className="flex-1">Left</div>
  <div className="flex-1">Right</div>
</div>
```

**Wrapping cards:**
```tsx
<div className="flex flex-wrap gap-4">
  {items.map(item => (
    <div key={item.id} className="flex-1 min-w-[280px] max-w-[400px]">
      <Card {...item} />
    </div>
  ))}
</div>
```

**Responsive navigation:**
```tsx
<nav className="flex flex-col md:flex-row items-start md:items-center gap-2 md:gap-6">
  <a href="/" className="text-lg font-bold">Logo</a>
  <div className="flex flex-col md:flex-row gap-2 md:gap-4">
    <a href="/about">About</a>
    <a href="/contact">Contact</a>
  </div>
</nav>
```

### 3. Container Sizing

**Responsive containers:**
```tsx
<div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  Content constrained to max width with responsive padding
</div>
```

**Breakpoint-specific max widths:**
```tsx
<div className="w-full max-w-sm md:max-w-2xl lg:max-w-4xl mx-auto">
  Container grows at breakpoints
</div>
```

**Full bleed on mobile, contained on desktop:**
```tsx
<div className="w-full lg:max-w-5xl lg:mx-auto">
  <div className="px-0 lg:px-8">
    Content
  </div>
</div>
```

### 4. Responsive Typography

**Fluid text sizing:**
```tsx
<h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold">
  Heading
</h1>
<p className="text-sm sm:text-base lg:text-lg leading-relaxed">
  Body text
</p>
```

**Responsive line length:**
```tsx
<div className="max-w-prose mx-auto text-base md:text-lg">
  Optimal reading width (65-75 characters)
</div>
```

### 5. Show/Hide Elements

**Hide on mobile, show on desktop:**
```tsx
<div className="hidden md:block">
  Desktop only content
</div>
```

**Show on mobile, hide on desktop:**
```tsx
<div className="block md:hidden">
  Mobile only content
</div>
```

**Different content at breakpoints:**
```tsx
<>
  <MobileMenu className="md:hidden" />
  <DesktopMenu className="hidden md:flex" />
</>
```

### 6. Responsive Spacing

**Adaptive padding/margin:**
```tsx
<div className="p-4 md:p-6 lg:p-8">
  Padding increases with screen size
</div>

<div className="space-y-4 md:space-y-6 lg:space-y-8">
  Vertical spacing increases
</div>
```

**Responsive gaps:**
```tsx
<div className="flex gap-2 sm:gap-4 md:gap-6 lg:gap-8">
  Flexible gap spacing
</div>
```

### 7. Aspect Ratios

**Responsive aspect ratio:**
```tsx
<div className="aspect-square sm:aspect-video lg:aspect-[21/9]">
  <img src="..." className="w-full h-full object-cover" alt="..." />
</div>
```

**Fixed aspect with responsive sizing:**
```tsx
<div className="w-full max-w-xs sm:max-w-md lg:max-w-lg aspect-video">
  <video className="w-full h-full" />
</div>
```

## React Patterns for Responsive Design

### 1. Using useMediaQuery Hook

```tsx
import { useMediaQuery } from 'usehooks-ts'

const MyComponent = () => {
  const isMobile = useMediaQuery('(max-width: 768px)')
  const isDesktop = useMediaQuery('(min-width: 1024px)')

  return (
    <div>
      {isMobile ? <MobileView /> : <DesktopView />}
    </div>
  )
}
```

### 2. Using useWindowSize Hook

```tsx
import { useWindowSize } from 'usehooks-ts'

const MyComponent = () => {
  const { width, height } = useWindowSize()

  return (
    <div>
      Viewport: {width} x {height}
      {width < 768 && <MobileNav />}
    </div>
  )
}
```

### 3. Responsive Component Variants

```tsx
interface CardProps {
  variant?: 'mobile' | 'desktop' | 'responsive'
}

const Card = ({ variant = 'responsive' }: CardProps) => {
  const isMobile = useMediaQuery('(max-width: 768px)')

  const getVariant = () => {
    if (variant === 'responsive') {
      return isMobile ? 'mobile' : 'desktop'
    }
    return variant
  }

  const variantStyles = {
    mobile: 'flex-col p-4',
    desktop: 'flex-row p-6'
  }

  return (
    <div className={cn('flex', variantStyles[getVariant()])}>
      Content
    </div>
  )
}
```

### 4. Render Props Pattern

```tsx
const Responsive = ({
  mobile,
  tablet,
  desktop
}: {
  mobile: ReactNode
  tablet?: ReactNode
  desktop: ReactNode
}) => {
  const isMobile = useMediaQuery('(max-width: 767px)')
  const isTablet = useMediaQuery('(min-width: 768px) and (max-width: 1023px)')

  if (isMobile) return mobile
  if (isTablet && tablet) return tablet
  return desktop
}

// Usage
<Responsive
  mobile={<MobileLayout />}
  tablet={<TabletLayout />}
  desktop={<DesktopLayout />}
/>
```

## Resizable Panels

For split views and adjustable layouts:

```tsx
import {
  ResizablePanelGroup,
  ResizablePanel,
  ResizableHandle
} from '@/components/ui/resizable'

<ResizablePanelGroup direction="horizontal" className="min-h-screen">
  <ResizablePanel defaultSize={25} minSize={15}>
    <div className="p-4">Sidebar</div>
  </ResizablePanel>

  <ResizableHandle withHandle />

  <ResizablePanel defaultSize={75}>
    <div className="p-4">Main content</div>
  </ResizablePanel>
</ResizablePanelGroup>
```

**Vertical layout:**
```tsx
<ResizablePanelGroup direction="vertical">
  <ResizablePanel defaultSize={40}>Header</ResizablePanel>
  <ResizableHandle />
  <ResizablePanel defaultSize={60}>Content</ResizablePanel>
</ResizablePanelGroup>
```

**Responsive resizable (desktop only):**
```tsx
const isDesktop = useMediaQuery('(min-width: 1024px)')

{isDesktop ? (
  <ResizablePanelGroup direction="horizontal">
    <ResizablePanel>Left</ResizablePanel>
    <ResizableHandle withHandle />
    <ResizablePanel>Right</ResizablePanel>
  </ResizablePanelGroup>
) : (
  <div className="flex flex-col">
    <div>Left</div>
    <div>Right</div>
  </div>
)}
```

## Advanced Responsive Techniques

### 1. Container Queries (via Tailwind)

```tsx
<div className="@container">
  <div className="@md:grid @md:grid-cols-2 @lg:grid-cols-3">
    Container-based responsive grid
  </div>
</div>
```

### 2. Clamp for Fluid Typography

```tsx
<h1 style={{ fontSize: 'clamp(1.5rem, 5vw, 3rem)' }}>
  Fluid heading size
</h1>
```

Or with Tailwind arbitrary values:
```tsx
<h1 className="text-[clamp(1.5rem,5vw,3rem)]">
  Fluid heading
</h1>
```

### 3. Dynamic Grid Columns

```tsx
const GridLayout = ({ itemCount }: { itemCount: number }) => {
  const columns = itemCount < 4 ? itemCount :
                  itemCount < 8 ? 2 :
                  itemCount < 12 ? 3 : 4

  return (
    <div className={`grid gap-4`} style={{
      gridTemplateColumns: `repeat(${columns}, minmax(0, 1fr))`
    }}>
      {items.map(item => <Card key={item.id} />)}
    </div>
  )
}
```

### 4. Responsive Image Optimization

```tsx
<picture>
  <source
    media="(min-width: 1024px)"
    srcSet="/image-large.jpg"
  />
  <source
    media="(min-width: 768px)"
    srcSet="/image-medium.jpg"
  />
  <img
    src="/image-small.jpg"
    alt="..."
    className="w-full h-auto"
  />
</picture>
```

### 5. Scroll Behavior

```tsx
// Horizontal scroll on mobile, grid on desktop
<div className="flex overflow-x-auto md:grid md:grid-cols-3 gap-4 pb-4 md:pb-0">
  {items.map(item => (
    <div key={item.id} className="flex-shrink-0 w-64 md:w-auto">
      <Card {...item} />
    </div>
  ))}
</div>
```

## Common Layout Patterns

### 1. Holy Grail Layout

```tsx
<div className="min-h-screen flex flex-col">
  {/* Header */}
  <header className="h-16 border-b">Header</header>

  {/* Main content area */}
  <div className="flex-1 flex flex-col lg:flex-row">
    {/* Left sidebar - mobile: full width, desktop: fixed width */}
    <aside className="lg:w-64 border-b lg:border-r lg:border-b-0">
      Sidebar
    </aside>

    {/* Main content */}
    <main className="flex-1 p-4 lg:p-8">
      Content
    </main>

    {/* Right sidebar - hidden on mobile/tablet */}
    <aside className="hidden xl:block w-64 border-l">
      Right sidebar
    </aside>
  </div>

  {/* Footer */}
  <footer className="h-16 border-t">Footer</footer>
</div>
```

### 2. Card Grid with Featured Item

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  {/* Featured card - spans 2 columns on desktop */}
  <div className="md:col-span-2 lg:row-span-2">
    <FeaturedCard />
  </div>

  {/* Regular cards */}
  {cards.map(card => (
    <div key={card.id}>
      <Card {...card} />
    </div>
  ))}
</div>
```

### 3. Sidebar Overlay (Mobile) / Fixed (Desktop)

```tsx
const [sidebarOpen, setSidebarOpen] = useState(false)
const isDesktop = useMediaQuery('(min-width: 1024px)')

<div className="flex">
  {/* Mobile overlay */}
  {!isDesktop && sidebarOpen && (
    <>
      <div
        className="fixed inset-0 bg-black/50 z-40"
        onClick={() => setSidebarOpen(false)}
      />
      <aside className="fixed left-0 top-0 h-full w-64 bg-white z-50">
        Sidebar
      </aside>
    </>
  )}

  {/* Desktop fixed sidebar */}
  {isDesktop && (
    <aside className="w-64 border-r">
      Sidebar
    </aside>
  )}

  <main className="flex-1">
    Content
  </main>
</div>
```

### 4. Responsive Table

```tsx
{/* Desktop: table, Mobile: cards */}
<div className="hidden md:block">
  <table className="w-full">
    <thead>
      <tr>
        <th>Name</th>
        <th>Email</th>
        <th>Role</th>
      </tr>
    </thead>
    <tbody>
      {users.map(user => (
        <tr key={user.id}>
          <td>{user.name}</td>
          <td>{user.email}</td>
          <td>{user.role}</td>
        </tr>
      ))}
    </tbody>
  </table>
</div>

<div className="md:hidden space-y-4">
  {users.map(user => (
    <div key={user.id} className="border rounded-lg p-4">
      <div className="font-bold">{user.name}</div>
      <div className="text-sm text-zinc-500">{user.email}</div>
      <div className="text-sm">{user.role}</div>
    </div>
  ))}
</div>
```

## Performance Considerations

1. **Avoid layout shift** - Reserve space for content that loads
2. **Use CSS over JS** - Prefer Tailwind breakpoints over `useMediaQuery` when possible
3. **Lazy load off-screen content** - Especially on mobile
4. **Optimize images** - Use responsive images and modern formats (WebP, AVIF)
5. **Test on real devices** - Emulators don't always reflect real performance

## Testing Checklist

When creating responsive layouts, verify:
- [ ] Works at all standard breakpoints (320px, 375px, 768px, 1024px, 1440px, 1920px)
- [ ] Touch targets are at least 44x44px on mobile
- [ ] Text is readable without zooming (minimum 16px on mobile)
- [ ] No horizontal scroll at any breakpoint
- [ ] Navigation is accessible on all screen sizes
- [ ] Images scale appropriately
- [ ] Forms are usable on mobile
- [ ] Content hierarchy is maintained across breakpoints

## Your Role

When asked to create responsive layouts:
1. **Clarify the content priority** - What's most important on mobile?
2. **Choose the right layout system** - Grid, Flexbox, or hybrid
3. **Start mobile-first** - Build up from smallest screen
4. **Use appropriate breakpoints** - Based on content, not arbitrary device sizes
5. **Provide complete code** - Including all responsive variants
6. **Consider edge cases** - Very small screens, very large screens, landscape orientation
7. **Optimize for touch** - On mobile devices
8. **Test thoroughly** - Provide guidance on testing approach

Always favor **CSS-based responsive design** using Tailwind's breakpoint system over JavaScript-based solutions, and only use hooks like `useMediaQuery` when you need to fundamentally change component behavior, not just styling.
