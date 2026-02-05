---
name: UI Design Implementation
description: Design and implement user interfaces with Tailwind CSS, shadcn/ui components, and modern design patterns. Use when creating new UI screens, improving visual design, building design consistency, or implementing responsive layouts. Specializes in rapid prototyping and production-ready interfaces.
version: 1.0.0
---

# UI Design Implementation

## Design System

### Color Palette

```css
/* Primary - Brand */
primary: #8B5CF6 (purple-500)
primary-foreground: #FFFFFF

/* Secondary */
secondary: #64748B (slate-600)
secondary-foreground: #FFFFFF

/* Status Colors */
success: #10B981 (green-500)
warning: #F59E0B (amber-500)
error: #EF4444 (red-500)
info: #3B82F6 (blue-500)

/* Neutral */
background: #FFFFFF
foreground: #0F172A (slate-900)
muted: #F1F5F9 (slate-100)
muted-foreground: #64748B (slate-600)
border: #E2E8F0 (slate-200)
```

### Typography Scale

```typescript
// Headings
h1: text-3xl font-bold (30px)
h2: text-2xl font-semibold (24px)
h3: text-xl font-semibold (20px)
h4: text-lg font-medium (18px)

// Body
default: text-base (16px)
small: text-sm (14px)
tiny: text-xs (12px)

// Weights
font-normal: 400
font-medium: 500
font-semibold: 600
font-bold: 700
```

### Spacing System

```css
/* Tailwind spacing (4px base unit) */
1 = 4px    (0.25rem)
2 = 8px    (0.5rem)
3 = 12px   (0.75rem)
4 = 16px   (1rem)
6 = 24px   (1.5rem)
8 = 32px   (2rem)
12 = 48px  (3rem)
16 = 64px  (4rem)

/* Common usage */
gap-4      = 16px between items
py-8       = 32px vertical padding
mb-6       = 24px margin bottom
space-y-4  = 16px vertical spacing between children
```

### Border Radius

```css
rounded-sm  = 2px   (subtle corners)
rounded     = 4px   (default)
rounded-md  = 6px   (cards, inputs)
rounded-lg  = 8px   (buttons, larger cards)
rounded-xl  = 12px  (hero sections)
rounded-2xl = 16px  (emphasis)
rounded-full = 9999px (pills, avatars)
```

## Layout Patterns

### Container Pattern

```tsx
{/* Standard page container */}
<div className="container max-w-6xl mx-auto py-8">
  <h1 className="text-3xl font-bold mb-8">Page Title</h1>
  {/* Content */}
</div>

{/* Narrow content */}
<div className="container max-w-2xl mx-auto py-8">
  {/* Forms, single-column content */}
</div>

{/* Wide content */}
<div className="container max-w-7xl mx-auto py-8">
  {/* Dashboards, data tables */}
</div>
```

### Grid Layouts

```tsx
{/* 2-column responsive */}
<div className="grid gap-4 md:grid-cols-2">
  <Card>...</Card>
  <Card>...</Card>
</div>

{/* 3-column responsive */}
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
  <Card>...</Card>
  <Card>...</Card>
  <Card>...</Card>
</div>

{/* Auto-fit grid */}
<div className="grid gap-4 grid-cols-[repeat(auto-fit,minmax(300px,1fr))]">
  {/* Automatically wraps based on container width */}
</div>
```

### Flex Layouts

```tsx
{/* Horizontal spacing */}
<div className="flex items-center gap-4">
  <Icon />
  <span>Text</span>
</div>

{/* Space between */}
<div className="flex justify-between items-center">
  <h2>Title</h2>
  <Button>Action</Button>
</div>

{/* Vertical stack */}
<div className="flex flex-col gap-4">
  <Item />
  <Item />
</div>

{/* Centered content */}
<div className="flex items-center justify-center min-h-[400px]">
  <div>Centered content</div>
</div>
```

## Card Patterns

### Basic Card

```tsx
<Card>
  <CardHeader>
    <CardTitle>Card Title</CardTitle>
    <CardDescription>Optional description</CardDescription>
  </CardHeader>
  <CardContent>
    <p>Card content here</p>
  </CardContent>
</Card>
```

### Card with Actions

```tsx
<Card>
  <CardHeader>
    <div className="flex justify-between items-start">
      <div>
        <CardTitle>Title</CardTitle>
        <CardDescription>Description</CardDescription>
      </div>
      <Button size="sm">Action</Button>
    </div>
  </CardHeader>
  <CardContent>
    {/* Content */}
  </CardContent>
</Card>
```

### Stats Card

```tsx
<Card>
  <CardHeader className="flex flex-row items-center justify-between pb-2">
    <CardTitle className="text-sm font-medium">Total Revenue</CardTitle>
    <DollarSign className="h-4 w-4 text-muted-foreground" />
  </CardHeader>
  <CardContent>
    <div className="text-2xl font-bold">$45,231</div>
    <p className="text-xs text-muted-foreground">+20.1% from last month</p>
  </CardContent>
</Card>
```

## Form Design

### Standard Form Layout

```tsx
<form className="space-y-6">
  <div className="space-y-2">
    <Label htmlFor="name">Name</Label>
    <Input
      id="name"
      placeholder="Enter your name"
      value={name}
      onChange={(e) => setName(e.target.value)}
    />
  </div>

  <div className="space-y-2">
    <Label htmlFor="email">Email</Label>
    <Input
      id="email"
      type="email"
      placeholder="you@example.com"
    />
  </div>

  <Button type="submit" className="w-full">
    Submit
  </Button>
</form>
```

### Form with Validation

```tsx
<div className="space-y-2">
  <Label htmlFor="password">Password</Label>
  <Input
    id="password"
    type="password"
    className={error ? "border-destructive" : ""}
  />
  {error && (
    <p className="text-sm text-destructive">{error}</p>
  )}
</div>
```

## Button Patterns

### Button Variants

```tsx
{/* Primary action */}
<Button>Save Changes</Button>

{/* Secondary action */}
<Button variant="outline">Cancel</Button>

{/* Danger action */}
<Button variant="destructive">Delete</Button>

{/* Ghost (minimal) */}
<Button variant="ghost">Edit</Button>

{/* With icon */}
<Button>
  <Plus className="h-4 w-4 mr-2" />
  Add Item
</Button>

{/* Icon only */}
<Button size="icon" variant="ghost">
  <MoreVertical className="h-4 w-4" />
</Button>

{/* Loading state */}
<Button disabled>
  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
  Loading...
</Button>
```

## Navigation Patterns

### Tabs Navigation

```tsx
<Tabs value={activeTab} onValueChange={setActiveTab}>
  <TabsList>
    <TabsTrigger value="overview">Overview</TabsTrigger>
    <TabsTrigger value="analytics">Analytics</TabsTrigger>
    <TabsTrigger value="settings">Settings</TabsTrigger>
  </TabsList>

  <TabsContent value="overview">
    {/* Overview content */}
  </TabsContent>

  <TabsContent value="analytics">
    {/* Analytics content */}
  </TabsContent>
</Tabs>
```

## Data Display

### Table Layout

```tsx
<div className="rounded-md border">
  <table className="w-full">
    <thead>
      <tr className="border-b bg-muted/50">
        <th className="h-12 px-4 text-left font-medium">Name</th>
        <th className="h-12 px-4 text-left font-medium">Status</th>
        <th className="h-12 px-4 text-left font-medium">Date</th>
      </tr>
    </thead>
    <tbody>
      {items.map((item) => (
        <tr key={item.id} className="border-b">
          <td className="p-4">{item.name}</td>
          <td className="p-4">
            <Badge>{item.status}</Badge>
          </td>
          <td className="p-4">{item.date}</td>
        </tr>
      ))}
    </tbody>
  </table>
</div>
```

### List with Actions

```tsx
<div className="space-y-2">
  {items.map((item) => (
    <div
      key={item.id}
      className="flex items-center justify-between p-4 rounded-lg border hover:bg-muted/50 transition-colors"
    >
      <div>
        <h3 className="font-medium">{item.title}</h3>
        <p className="text-sm text-muted-foreground">{item.description}</p>
      </div>
      <div className="flex gap-2">
        <Button size="sm" variant="ghost">Edit</Button>
        <Button size="sm" variant="ghost">Delete</Button>
      </div>
    </div>
  ))}
</div>
```

## Status Indicators

### Badge Variants

```tsx
<Badge>Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="outline">Outline</Badge>
<Badge variant="destructive">Error</Badge>

{/* Custom colors */}
<Badge className="bg-green-100 text-green-800">Active</Badge>
<Badge className="bg-yellow-100 text-yellow-800">Pending</Badge>
<Badge className="bg-red-100 text-red-800">Inactive</Badge>
```

### Progress Indicators

```tsx
import { Progress } from '@/components/ui/progress';

<div className="space-y-2">
  <div className="flex justify-between text-sm">
    <span>Progress</span>
    <span className="text-muted-foreground">{progress}%</span>
  </div>
  <Progress value={progress} />
</div>
```

## Empty States

### No Data State

```tsx
<div className="flex flex-col items-center justify-center py-12 text-center">
  <div className="rounded-full bg-muted p-3 mb-4">
    <Inbox className="h-6 w-6 text-muted-foreground" />
  </div>
  <h3 className="text-lg font-semibold mb-2">No items yet</h3>
  <p className="text-muted-foreground mb-4">
    Get started by creating your first item
  </p>
  <Button>
    <Plus className="h-4 w-4 mr-2" />
    Create Item
  </Button>
</div>
```

## Loading States

### Skeleton Pattern

```tsx
<div className="space-y-4">
  <div className="space-y-2">
    <div className="h-4 bg-muted rounded w-3/4 animate-pulse" />
    <div className="h-4 bg-muted rounded w-1/2 animate-pulse" />
  </div>
  <div className="h-32 bg-muted rounded animate-pulse" />
</div>
```

### Spinner Pattern

```tsx
import { Loader2 } from 'lucide-react';

<div className="flex items-center justify-center py-8">
  <Loader2 className="h-8 w-8 animate-spin text-primary" />
</div>
```

## Responsive Design

### Mobile-First Breakpoints

```tsx
{/* Tailwind breakpoints */}
sm: 640px   // Small devices
md: 768px   // Tablets
lg: 1024px  // Laptops
xl: 1280px  // Desktops
2xl: 1536px // Large screens

{/* Usage */}
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
  {/* Stacks on mobile, 2 cols on tablet, 3 cols on desktop */}
</div>
```

### Hide/Show by Breakpoint

```tsx
{/* Hide on mobile, show on desktop */}
<div className="hidden md:block">Desktop content</div>

{/* Show on mobile, hide on desktop */}
<div className="md:hidden">Mobile content</div>

{/* Responsive text sizes */}
<h1 className="text-2xl md:text-3xl lg:text-4xl">Responsive Heading</h1>
```

## Animation Patterns

### Hover Effects

```tsx
{/* Card hover */}
<Card className="transition-all hover:shadow-lg hover:-translate-y-1">

{/* Button hover */}
<Button className="transition-colors hover:bg-primary/90">

{/* Border hover */}
<div className="border-2 border-transparent hover:border-primary transition-colors">
```

### Transitions

```tsx
{/* Fade in */}
<div className="opacity-0 animate-in fade-in duration-500">

{/* Slide in */}
<div className="translate-y-4 animate-in slide-in-from-bottom duration-300">

{/* Scale in */}
<div className="scale-95 animate-in zoom-in duration-200">
```

## Accessibility

### Semantic HTML

```tsx
{/* Use proper heading hierarchy */}
<h1>Main Title</h1>
<h2>Section Title</h2>
<h3>Subsection</h3>

{/* Use nav for navigation */}
<nav>
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>

{/* Use main for main content */}
<main>
  <article>{/* Content */}</article>
</main>
```

### ARIA Labels

```tsx
<Button aria-label="Delete item">
  <Trash2 className="h-4 w-4" />
</Button>

<Input
  aria-label="Search"
  aria-describedby="search-help"
  placeholder="Search..."
/>
<p id="search-help" className="text-sm text-muted-foreground">
  Enter keywords to search
</p>
```

## Design Checklist

Before implementing a new screen:
- [ ] Use container with appropriate max-width
- [ ] Apply consistent spacing (py-8, gap-4)
- [ ] Add responsive breakpoints (md:, lg:)
- [ ] Include loading states
- [ ] Add empty states
- [ ] Use semantic HTML
- [ ] Add proper ARIA labels
- [ ] Test on mobile viewport
- [ ] Verify color contrast
- [ ] Check keyboard navigation

## Common Mistakes

1. **Inconsistent spacing** - Use Tailwind's spacing scale
2. **No mobile testing** - Always check responsive layout
3. **Missing empty states** - Show helpful message when no data
4. **Poor contrast** - Use slate-600+ for text on white
5. **No loading feedback** - Add spinners or skeletons
6. **Hardcoded colors** - Use Tailwind color classes
7. **Overcomplicated designs** - Keep it simple and clean

## Quick Reference

- Tailwind Docs: https://tailwindcss.com/docs
- shadcn/ui: https://ui.shadcn.com/
- Lucide Icons: https://lucide.dev/
- Color Contrast: https://webaim.org/resources/contrastchecker/
