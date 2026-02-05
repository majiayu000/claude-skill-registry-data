---
name: page-layout-patterns
description: Standardize page structure - always use MainLayout wrapper, space-y-32 for sections, px-8 py-16 for page padding, responsive grid patterns
---

# Page Layout Patterns

This skill defines standardized page structure patterns for maintaining consistency across the application. All pages follow predictable spacing, layout, and wrapper conventions.

## Table of Contents

1. [Standard Page Wrapper](#standard-page-wrapper)
2. [Page Structure Pattern](#page-structure-pattern)
3. [Spacing Conventions](#spacing-conventions)
4. [Responsive Grid Patterns](#responsive-grid-patterns)
5. [Hero Section Pattern](#hero-section-pattern)
6. [Content Section Patterns](#content-section-patterns)
7. [Common Layout Recipes](#common-layout-recipes)
8. [Real Project Examples](#real-project-examples)

---

## Standard Page Wrapper

### Always Use MainLayout

**IMPORTANT:** All pages must be rendered within `MainLayout`. Never create standalone pages without this wrapper.

**What MainLayout Provides:**
- Sticky header with navigation
- Active route indicators with underline animation
- Max-width container (`max-w-7xl`) for content
- Consistent horizontal padding (`px-8`)
- Vertical page padding (`py-16`)
- White background with backdrop blur
- Proper z-index management

**Your Responsibility:**
Pages only define content structure, not chrome (header, navigation, container).

```tsx
// ✅ CORRECT - MainLayout wraps all routes in App.tsx
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

// ✅ CORRECT - Page component only defines content
export function MyPage() {
  return (
    <div className="space-y-32">
      {/* Page content here */}
    </div>
  );
}

// ❌ WRONG - Don't recreate navigation or container
export function MyPage() {
  return (
    <div className="min-h-screen">
      <header>
        <nav>{/* navigation */}</nav>
      </header>
      <main className="max-w-7xl mx-auto px-8 py-16">
        {/* content */}
      </main>
    </div>
  );
}
```

**MainLayout Implementation Reference:**

```tsx
// src/layouts/MainLayout.tsx
export function MainLayout() {
  return (
    <div className="min-h-screen bg-white">
      {/* Sticky Navigation Header */}
      <header className="sticky top-0 z-50 border-b border-gray-200 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <div className="mx-auto max-w-7xl px-8 py-4">
          <nav className="flex items-center justify-end">
            <div className="flex items-center gap-8">
              {/* Navigation links with active state */}
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content with container and padding */}
      <main className="mx-auto max-w-7xl px-8 py-16">
        <Outlet /> {/* Your page renders here */}
      </main>
    </div>
  );
}
```

---

## Page Structure Pattern

### Standard Multi-Section Page

Use `space-y-32` as the root spacing between major page sections:

```tsx
export function PageName() {
  return (
    <div className="space-y-32">
      {/* Hero section - largest, most prominent */}
      <section className="relative overflow-hidden">
        <div className="relative px-6 py-32 text-center">
          <h1>Hero Title</h1>
          <p>Hero description</p>
        </div>
      </section>

      {/* Main content sections - separated by 128px (space-y-32) */}
      <section>
        <h2>Section Title</h2>
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
          {/* Cards or content */}
        </div>
      </section>

      {/* Additional sections */}
      <section>
        {/* More content */}
      </section>
    </div>
  );
}
```

**Key Points:**
- Root container uses `space-y-32` for major section separation
- Use semantic HTML (`<section>`, `<article>`)
- Hero sections get special treatment (see Hero Section Pattern)
- Each section is self-contained

---

## Spacing Conventions

### Spacing Scale Quick Reference

Follow this consistent spacing hierarchy throughout the application:

```tsx
// ✅ CORRECT USAGE

// Page container (applied by MainLayout)
<main className="mx-auto max-w-7xl px-8 py-16">

// Between major page sections (hero, features, content blocks)
<div className="space-y-32"> {/* 128px */}

// Between subsections within a major section
<div className="space-y-16"> {/* 64px */}

// Between related items (paragraphs, list items, form fields)
<div className="space-y-8"> {/* 32px */}

// Between tightly related items (label + input, icon + text)
<div className="space-y-4"> {/* 16px */}

// Card grids
<div className="grid gap-8 md:grid-cols-2"> {/* 32px gap */}

// Navigation items
<nav className="flex gap-8"> {/* 32px gap */}
```

### Visual Spacing Hierarchy

```
┌─────────────────────────────────────────┐
│ MainLayout: px-8 py-16                  │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Section 1                       │   │
│  │                                 │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ↕ space-y-32 (128px)                   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │ Section 2                       │   │
│  │  ┌─────────────────────────┐   │   │
│  │  │ Subsection A            │   │   │
│  │  └─────────────────────────┘   │   │
│  │                                 │   │
│  │  ↕ space-y-16 (64px)            │   │
│  │                                 │   │
│  │  ┌─────────────────────────┐   │   │
│  │  │ Subsection B            │   │   │
│  │  │  - Item 1               │   │   │
│  │  │  ↕ space-y-8 (32px)     │   │   │
│  │  │  - Item 2               │   │   │
│  │  └─────────────────────────┘   │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### Before/After Example: Proper Spacing

```tsx
// ❌ BEFORE - Inconsistent spacing
export function BadPage() {
  return (
    <div className="space-y-12">
      <section className="py-8">
        <h1>Title</h1>
        <p className="mt-2">Description</p>
      </section>

      <section className="py-24">
        <div className="grid gap-4 grid-cols-3">
          {/* cards too close together */}
        </div>
      </section>
    </div>
  );
}

// ✅ AFTER - Consistent, standardized spacing
export function GoodPage() {
  return (
    <div className="space-y-32">
      <section>
        <div className="space-y-4">
          <h1>Title</h1>
          <p>Description</p>
        </div>
      </section>

      <section>
        <div className="grid gap-8 md:grid-cols-3">
          {/* cards with proper breathing room */}
        </div>
      </section>
    </div>
  );
}
```

---

## Responsive Grid Patterns

### Three-Column Grid (Most Common)

Single column on mobile, 2 on tablet, 3 on desktop:

```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
  {items.map((item) => (
    <Card key={item.id}>
      {/* Card content */}
    </Card>
  ))}
</div>
```

**Equal Height Cards:**
Grid automatically makes cards equal height. No additional CSS needed.

```tsx
// ✅ Cards will automatically stretch to match tallest card
<div className="grid gap-8 md:grid-cols-3">
  <Card>Short content</Card>
  <Card>Very long content that makes this card taller...</Card>
  <Card>Medium content</Card>
</div>
```

### Two-Column Grid

```tsx
// Equal columns
<div className="grid gap-8 md:grid-cols-2">
  <div>Column 1</div>
  <div>Column 2</div>
</div>
```

### Asymmetric Layouts (Sidebar Pattern)

2/3 main content, 1/3 sidebar:

```tsx
<div className="grid gap-8 md:grid-cols-3">
  {/* Main Content - Takes 2 columns */}
  <div className="space-y-8 md:col-span-2">
    <h1>Main Content</h1>
    <p>Primary content area...</p>
  </div>

  {/* Sidebar - Takes 1 column */}
  <div className="md:col-span-1">
    <Card className="sticky top-20">
      <CardHeader>
        <CardTitle>Sidebar</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Sidebar content */}
      </CardContent>
    </Card>
  </div>
</div>
```

**Alternative syntax using grid template columns:**

```tsx
<div className="grid gap-8 md:grid-cols-[2fr_1fr]">
  <div>{/* Main content */}</div>
  <div>{/* Sidebar */}</div>
</div>
```

### Four-Column Grid

```tsx
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
  {items.map((item) => (
    <Card key={item.id}>{/* Card content */}</Card>
  ))}
</div>
```

### Grid Breakpoint Reference

```
Mobile:  grid-cols-1      (< 768px)
Tablet:  md:grid-cols-2   (≥ 768px)
Desktop: lg:grid-cols-3   (≥ 1024px)
Wide:    xl:grid-cols-4   (≥ 1280px)
```

---

## Hero Section Pattern

Hero sections are the primary visual focus of a page. They require special treatment:

### Standard Hero Structure

```tsx
<section className="relative overflow-hidden">
  {/* Background gradient blobs */}
  <div className="absolute inset-0 -z-10">
    <div className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/2">
      <div className="h-[600px] w-[600px] rounded-full bg-gradient-to-br from-blue-400/20 via-purple-400/20 to-pink-400/20 blur-3xl" />
    </div>
    <div className="absolute right-0 top-1/2 translate-x-1/2">
      <div className="h-[400px] w-[400px] rounded-full bg-gradient-to-br from-cyan-400/20 via-blue-400/20 to-indigo-400/20 blur-3xl" />
    </div>
  </div>

  {/* Hero content */}
  <div className="relative px-6 py-32 text-center">
    <div className="mx-auto max-w-4xl">
      {/* Optional decorative icon */}
      <div className="mb-6 flex justify-center">
        <div className="rounded-full bg-gradient-to-br from-blue-500 to-purple-600 p-3 shadow-lg shadow-blue-500/50">
          <Icon className="h-8 w-8 text-white" />
        </div>
      </div>

      {/* Main heading with gradient text */}
      <h1 className="mb-6 bg-gradient-to-r from-gray-900 via-blue-900 to-purple-900 bg-clip-text text-6xl font-extrabold tracking-tight text-transparent sm:text-7xl md:text-8xl">
        Hero Title
      </h1>

      {/* Subtitle */}
      <p className="mx-auto mb-12 max-w-3xl text-xl leading-relaxed text-gray-600 sm:text-2xl">
        Compelling description with <span className="font-semibold text-blue-600">highlighted</span> keywords
      </p>
    </div>
  </div>
</section>
```

### Hero Anatomy

```
┌─────────────────────────────────────────────────┐
│ <section> relative overflow-hidden             │
│                                                 │
│  ┌────────────────────────────────────────┐    │
│  │ Background: absolute inset-0 -z-10    │    │
│  │ - Gradient blobs positioned absolute  │    │
│  │ - Multiple layers for depth           │    │
│  └────────────────────────────────────────┘    │
│                                                 │
│  ┌────────────────────────────────────────┐    │
│  │ Content: relative px-6 py-32          │    │
│  │                                        │    │
│  │  ┌──────────────────────────────┐     │    │
│  │  │ max-w-4xl mx-auto           │     │    │
│  │  │                              │     │    │
│  │  │  - Decorative icon           │     │    │
│  │  │  - Large gradient heading    │     │    │
│  │  │  - Subtitle paragraph        │     │    │
│  │  └──────────────────────────────┘     │    │
│  └────────────────────────────────────────┘    │
└─────────────────────────────────────────────────┘
```

### Key Hero Principles

1. **Relative positioning** - Section is `relative` to contain absolute backgrounds
2. **Overflow hidden** - Prevents gradient blobs from creating scrollbars
3. **Absolute backgrounds** - Positioned with `absolute inset-0 -z-10`
4. **Relative content** - Content div is `relative` to sit above backgrounds
5. **Generous padding** - `py-32` gives hero sections breathing room
6. **Centered text** - `text-center` with `mx-auto max-w-4xl` for readability
7. **Gradient text** - Use `bg-gradient-to-r`, `bg-clip-text`, `text-transparent`

---

## Content Section Patterns

### Standard Content Section

```tsx
<section>
  <div className="space-y-8">
    <div className="space-y-4">
      <h2 className="text-3xl font-bold text-gray-900">Section Title</h2>
      <p className="text-lg leading-relaxed text-gray-600">
        Section introduction or description
      </p>
    </div>

    {/* Section content */}
    <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
      {/* Cards or content items */}
    </div>
  </div>
</section>
```

### Text-Heavy Content Section

Use consistent heading hierarchy and spacing:

```tsx
<section>
  <div className="space-y-16">
    {/* Section header */}
    <div className="space-y-4">
      <h2 className="text-3xl font-bold text-gray-900">Main Section</h2>
      <p className="leading-relaxed text-gray-600">
        Introduction paragraph
      </p>
    </div>

    {/* Subsections */}
    <div className="space-y-8">
      <div className="space-y-4">
        <h3 className="text-2xl font-bold text-gray-900">Subsection Title</h3>
        <p className="leading-relaxed text-gray-600">
          Subsection content with proper spacing
        </p>
      </div>

      <div className="space-y-4">
        <h3 className="text-2xl font-bold text-gray-900">Another Subsection</h3>
        <p className="leading-relaxed text-gray-600">
          More content
        </p>
      </div>
    </div>
  </div>
</section>
```

### Card Grid Section

```tsx
<section>
  <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
    {items.map((item) => (
      <Card key={item.id} className="group hover:-translate-y-2 transition-transform">
        <CardHeader className="space-y-4">
          {/* Card content */}
        </CardHeader>
      </Card>
    ))}
  </div>
</section>
```

---

## Common Layout Recipes

### Recipe 1: Hero + Feature Grid (Homepage Pattern)

```tsx
export function Home() {
  return (
    <div className="space-y-32">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 -z-10">
          {/* Background gradients */}
        </div>
        <div className="relative px-6 py-32 text-center">
          <h1>Welcome</h1>
          <p>Description</p>
        </div>
      </section>

      {/* Features Grid */}
      <section>
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature) => (
            <Card key={feature.id}>{/* Feature card */}</Card>
          ))}
        </div>
      </section>
    </div>
  );
}
```

### Recipe 2: Two-Column Content + Sidebar

```tsx
export function About() {
  return (
    <div className="grid gap-8 md:grid-cols-3">
      {/* Main Content (2/3) */}
      <div className="space-y-8 md:col-span-2">
        <div className="space-y-4">
          <h1 className="text-4xl font-bold">Page Title</h1>
          <p className="text-lg text-gray-600">Introduction</p>
        </div>

        <Separator />

        <div className="space-y-16">
          <div className="space-y-4">
            <h2 className="text-3xl font-bold">Section</h2>
            <p>Content</p>
          </div>
        </div>
      </div>

      {/* Sticky Sidebar (1/3) */}
      <div className="md:col-span-1">
        <Card className="sticky top-20">
          <CardHeader>
            <CardTitle>Sidebar Title</CardTitle>
            <CardDescription>Description</CardDescription>
          </CardHeader>
          <CardContent>
            {/* Sidebar content */}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
```

### Recipe 3: Centered Content (Error Pages, Forms)

```tsx
export function NotFound() {
  return (
    <div className="flex min-h-[60vh] items-center justify-center">
      <Card className="w-full max-w-md text-center">
        <CardHeader>
          <div className="mb-4">
            <h1 className="text-8xl font-bold text-blue-600">404</h1>
          </div>
          <CardTitle className="text-2xl">Page Not Found</CardTitle>
          <CardDescription className="text-base">
            Error message
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button>Take Action</Button>
        </CardContent>
      </Card>
    </div>
  );
}
```

### Recipe 4: Multi-Section Content Page

```tsx
export function ContentPage() {
  return (
    <div className="space-y-32">
      {/* Introduction Section */}
      <section>
        <div className="space-y-4 text-center">
          <h1 className="text-5xl font-bold">Page Title</h1>
          <p className="text-xl text-gray-600">Subtitle</p>
        </div>
      </section>

      {/* Content Section 1 */}
      <section>
        <div className="space-y-8">
          <h2 className="text-3xl font-bold">Section 1</h2>
          <div className="grid gap-8 md:grid-cols-2">
            {/* Content */}
          </div>
        </div>
      </section>

      {/* Content Section 2 */}
      <section>
        <div className="space-y-8">
          <h2 className="text-3xl font-bold">Section 2</h2>
          {/* Content */}
        </div>
      </section>
    </div>
  );
}
```

---

## Real Project Examples

### Example 1: Home Page (Hero + Grid)

**File:** `src/pages/Home.tsx`

This page demonstrates the hero + feature grid pattern:

```tsx
export function Home() {
  return (
    <div className="space-y-32">
      {/* Hero Section with gradient backgrounds */}
      <div className="relative overflow-hidden">
        {/* Background gradient blobs */}
        <div className="absolute inset-0 -z-10">
          <div className="absolute left-1/2 top-0 -translate-x-1/2 -translate-y-1/2">
            <div className="h-[600px] w-[600px] rounded-full bg-gradient-to-br from-blue-400/20 via-purple-400/20 to-pink-400/20 blur-3xl" />
          </div>
          <div className="absolute right-0 top-1/2 translate-x-1/2">
            <div className="h-[400px] w-[400px] rounded-full bg-gradient-to-br from-cyan-400/20 via-blue-400/20 to-indigo-400/20 blur-3xl" />
          </div>
        </div>

        <div className="relative px-6 py-32 text-center">
          <div className="mx-auto max-w-4xl">
            {/* Decorative icon */}
            <div className="mb-6 flex justify-center">
              <div className="rounded-full bg-gradient-to-br from-blue-500 to-purple-600 p-3 shadow-lg shadow-blue-500/50">
                <Sparkles className="h-8 w-8 text-white" />
              </div>
            </div>

            {/* Gradient heading */}
            <h1 className="mb-6 bg-gradient-to-r from-gray-900 via-blue-900 to-purple-900 bg-clip-text text-6xl font-extrabold tracking-tight text-transparent sm:text-7xl md:text-8xl">
              {APP_NAME}
            </h1>

            <p className="mx-auto mb-12 max-w-3xl text-xl leading-relaxed text-gray-600 sm:text-2xl">
              A modern, production-ready React TypeScript starter template
            </p>
          </div>
        </div>
      </div>

      {/* Features Grid - 3 columns with equal height cards */}
      <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        {features.map((feature) => (
          <Card key={feature.title} className="group hover:-translate-y-2 transition-all">
            <CardHeader className="space-y-4">
              <div className="flex items-start justify-between">
                <div className={`rounded-xl bg-gradient-to-br ${feature.gradient} p-3`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
                <Badge>{feature.badge}</Badge>
              </div>
              <div>
                <CardTitle className="mb-2 text-2xl">{feature.title}</CardTitle>
                <CardDescription>{feature.description}</CardDescription>
              </div>
            </CardHeader>
          </Card>
        ))}
      </div>
    </div>
  );
}
```

**Key Patterns Used:**
- `space-y-32` between hero and features
- `relative overflow-hidden` for hero background effects
- `gap-8` for card grid spacing
- Three-column responsive grid: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- Equal height cards (automatic with grid)

### Example 2: About Page (Sidebar Layout)

**File:** `src/pages/About.tsx`

This page demonstrates the 2/3 + 1/3 sidebar pattern:

```tsx
export function About() {
  return (
    <div className="grid gap-8 md:grid-cols-3">
      {/* Main Content - 2 columns */}
      <div className="space-y-8 md:col-span-2">
        <div>
          <h1 className="mb-4 text-4xl font-bold tracking-tight text-gray-900">
            About This Project
          </h1>
          <p className="text-lg leading-relaxed text-gray-600">
            Introduction paragraph
          </p>
        </div>

        <Separator />

        <div className="space-y-4">
          <h2 className="text-3xl font-bold text-gray-900">Features</h2>
          <p className="leading-relaxed text-gray-600">Description</p>
        </div>

        <div className="space-y-4">
          <h3 className="text-2xl font-bold text-gray-900">Subsection</h3>
          <p className="leading-relaxed text-gray-600">Content</p>
        </div>
      </div>

      {/* Sidebar - 1 column, sticky */}
      <div className="md:col-span-1">
        <Card className="sticky top-20">
          <CardHeader>
            <CardTitle>Tech Stack</CardTitle>
            <CardDescription>Core technologies</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-wrap gap-2">
              {technologies.map((tech) => (
                <Badge key={tech} variant="outline">{tech}</Badge>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
```

**Key Patterns Used:**
- `grid gap-8 md:grid-cols-3` for asymmetric layout
- `md:col-span-2` for main content (2/3 width)
- `md:col-span-1` for sidebar (1/3 width)
- `sticky top-20` keeps sidebar visible during scroll
- `space-y-8` between content sections
- `space-y-4` between related items (heading + paragraph)

### Example 3: NotFound Page (Centered Content)

**File:** `src/pages/NotFound.tsx`

This page demonstrates centered content for simple pages:

```tsx
export function NotFound() {
  return (
    <div className="flex min-h-[60vh] items-center justify-center">
      <Card className="w-full max-w-md text-center">
        <CardHeader>
          <div className="mb-4">
            <h1 className="text-8xl font-bold text-blue-600">404</h1>
          </div>
          <CardTitle className="text-2xl">Page Not Found</CardTitle>
          <CardDescription className="text-base">
            The page you're looking for doesn't exist or has been moved.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Link to="/">
            <Button size="lg" className="w-full">
              Return Home
            </Button>
          </Link>
        </CardContent>
      </Card>
    </div>
  );
}
```

**Key Patterns Used:**
- `flex min-h-[60vh] items-center justify-center` for vertical/horizontal centering
- `max-w-md` constrains card width
- `text-center` for centered text
- Single Card component contains all content

### Example 4: MainLayout Structure

**File:** `src/layouts/MainLayout.tsx`

The wrapper all pages inherit:

```tsx
export function MainLayout() {
  return (
    <div className="min-h-screen bg-white">
      {/* Sticky Navigation Header */}
      <header className="sticky top-0 z-50 border-b border-gray-200 bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/60">
        <div className="mx-auto max-w-7xl px-8 py-4">
          <nav className="flex items-center justify-end">
            <div className="flex items-center gap-8">
              <Link to="/" className="relative px-4 py-2 text-base font-medium">
                Home
                {isActive('/') && (
                  <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600" />
                )}
              </Link>
              <Link to="/about" className="relative px-4 py-2 text-base font-medium">
                About
                {isActive('/about') && (
                  <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600" />
                )}
              </Link>
            </div>
          </nav>
        </div>
      </header>

      {/* Main Content Container */}
      <main className="mx-auto max-w-7xl px-8 py-16">
        <Outlet /> {/* Pages render here */}
      </main>
    </div>
  );
}
```

**What It Provides:**
- `min-h-screen` ensures full viewport height
- `sticky top-0 z-50` header stays visible on scroll
- `max-w-7xl` constrains content width
- `px-8 py-16` provides consistent page padding
- `gap-8` between navigation items
- Active route indicators with underline
- Backdrop blur effect on header

---

## Quick Reference Checklist

When creating a new page, verify:

- [ ] Page is wrapped in MainLayout (via route definition)
- [ ] Page component starts with `<div className="space-y-32">`
- [ ] Major sections use `<section>` tags
- [ ] Hero sections use `relative overflow-hidden`
- [ ] Hero backgrounds use `absolute inset-0 -z-10`
- [ ] Subsections use `space-y-16` or `space-y-8`
- [ ] Card grids use `gap-8`
- [ ] Responsive grids: `grid-cols-1 md:grid-cols-2 lg:grid-cols-3`
- [ ] Sticky sidebars use `sticky top-20`
- [ ] Text uses consistent heading hierarchy (h1 → h2 → h3)
- [ ] Leading-relaxed for body text readability
- [ ] Centered content uses flex with items-center justify-center

---

## Common Mistakes to Avoid

### Mistake 1: Recreating Navigation

```tsx
// ❌ WRONG - Don't recreate header/nav
export function MyPage() {
  return (
    <div>
      <header>
        <nav>{/* navigation */}</nav>
      </header>
      <div>{/* content */}</div>
    </div>
  );
}

// ✅ CORRECT - MainLayout provides navigation
export function MyPage() {
  return (
    <div className="space-y-32">
      {/* Just content */}
    </div>
  );
}
```

### Mistake 2: Inconsistent Spacing

```tsx
// ❌ WRONG - Random spacing values
<div className="space-y-6">
  <section className="py-12">{/* ... */}</section>
  <section className="py-20">{/* ... */}</section>
</div>

// ✅ CORRECT - Use standard scale
<div className="space-y-32">
  <section>{/* ... */}</section>
  <section>{/* ... */}</section>
</div>
```

### Mistake 3: Non-Responsive Grids

```tsx
// ❌ WRONG - Fixed columns, doesn't adapt to mobile
<div className="grid grid-cols-3 gap-8">

// ✅ CORRECT - Responsive columns
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
```

### Mistake 4: Missing Relative Parent for Absolute Children

```tsx
// ❌ WRONG - Absolute backgrounds without relative parent
<section className="overflow-hidden">
  <div className="absolute inset-0">{/* Will be positioned wrong */}</div>
</section>

// ✅ CORRECT - Relative parent contains absolute children
<section className="relative overflow-hidden">
  <div className="absolute inset-0 -z-10">{/* Properly contained */}</div>
</section>
```

---

## Summary

**Core Principles:**

1. **Always use MainLayout** - Never recreate navigation or containers
2. **Consistent spacing scale** - 32, 16, 8, 4 (space-y-32/16/8/4)
3. **Responsive grids** - Always include mobile-first breakpoints
4. **Semantic HTML** - Use section, article, header appropriately
5. **Hero sections** - relative + overflow-hidden with absolute backgrounds
6. **Equal height cards** - Grid handles automatically
7. **Sticky sidebars** - Use `sticky top-20` for sidebar cards

**Spacing Hierarchy:**
- Major sections: `space-y-32` (128px)
- Subsections: `space-y-16` (64px)
- Related items: `space-y-8` (32px)
- Tight groups: `space-y-4` (16px)
- Card grids: `gap-8` (32px)

**Grid Patterns:**
- Three-column: `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8`
- Sidebar layout: `grid gap-8 md:grid-cols-3` with `md:col-span-2` + `md:col-span-1`
- Centered: `flex min-h-[60vh] items-center justify-center`

By following these patterns, all pages will have consistent structure, spacing, and responsive behavior.
