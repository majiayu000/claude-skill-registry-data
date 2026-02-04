---
name: shadcn-ui-designer
description: Design and build modern UI components and pages using shadcn/ui. Creates clean, accessible interfaces with Tailwind CSS following shadcn principles. Use when building UI components, pages, forms, dashboards, or any interface work.
---

# Shadcn UI Designer

Build production-ready UI components using shadcn/ui principles: minimal, accessible, composable, and beautiful by default.

## Core Philosophy

**Design modern, minimal interfaces** with:
- Clean typography (Inter/system fonts, 2-3 weights max)
- Ample whitespace (4px-based spacing: p-1 through p-8)
- Subtle shadows (shadow-sm/md/lg only)
- Accessible contrast (WCAG AA minimum)
- Smooth micro-interactions (200-300ms transitions)
- Professional neutrals (slate/zinc scale) with subtle accents

**Build composable components** that work together seamlessly.

## Quick Start Pattern

```tsx
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export function MyComponent() {
  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="space-y-2">
        <h1 className="text-2xl font-semibold">Title</h1>
        <p className="text-sm text-muted-foreground">Description</p>
      </div>

      <Card className="shadow-sm">
        <CardHeader>
          <CardTitle>Section</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {/* Content here */}
        </CardContent>
      </Card>
    </div>
  )
}
```

## Design System Rules

### Typography
- **Hierarchy**: `text-2xl` (headings) → `text-base` (body) → `text-sm` (secondary)
- **Weights**: `font-semibold` (600) for emphasis, `font-medium` (500) for labels, `font-normal` (400) for body
- **Colors**: `text-foreground` (primary), `text-muted-foreground` (secondary)

```tsx
<h1 className="text-2xl font-semibold">Page Title</h1>
<p className="text-muted-foreground">Supporting text</p>
```

### Spacing
Use consistent spacing scale:
- **Micro**: `space-y-2` (8px) - within sections
- **Small**: `space-y-4` (16px) - between elements
- **Medium**: `space-y-6` (24px) - between sections
- **Large**: `space-y-8` (32px) - major divisions

```tsx
<div className="container mx-auto p-6 space-y-6">
  <section className="space-y-4">
    <div className="space-y-2">
      {/* Related elements */}
    </div>
  </section>
</div>
```

### Colors
Use semantic color tokens:
- **Background**: `bg-background`, `bg-card`, `bg-muted`
- **Foreground**: `text-foreground`, `text-muted-foreground`
- **Borders**: `border-border`, `border-input`
- **Primary**: `bg-primary`, `text-primary-foreground`
- **Destructive**: `bg-destructive`, `text-destructive-foreground`

```tsx
<Card className="bg-card text-card-foreground border-border">
  <Button className="bg-primary text-primary-foreground">
    Primary Action
  </Button>
  <div className="bg-muted/50 text-muted-foreground">
    Subtle highlight
  </div>
</Card>
```

### Shadows & Elevation
Three levels only:
- `shadow-sm`: Cards, raised sections (0 1px 2px)
- `shadow-md`: Dropdowns, popovers (0 4px 6px)
- `shadow-lg`: Modals, dialogs (0 10px 15px)

```tsx
<Card className="shadow-sm hover:shadow-md transition-shadow" />
```

### Animations
- **Duration**: 200-300ms
- **Easing**: ease-in-out
- **Use cases**: Hover states, loading states, reveals

```tsx
<Button className="transition-colors duration-200 hover:bg-primary/90">
<Card className="transition-all duration-200 hover:shadow-md hover:scale-[1.02]">
```

### Accessibility
Always include:
- Semantic HTML (`<main>`, `<nav>`, `<article>`)
- ARIA labels on icons/actions
- Focus states (`:focus-visible:ring-2`)
- Keyboard navigation
- WCAG AA contrast (4.5:1 minimum)

```tsx
<button
  aria-label="Close dialog"
  className="focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2"
>
  <X className="h-4 w-4" />
</button>
```

## Component Patterns

### Dashboard Cards
```tsx
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
  {stats.map(stat => (
    <Card key={stat.id} className="shadow-sm">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium">
          {stat.label}
        </CardTitle>
        {stat.icon}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{stat.value}</div>
        <p className="text-xs text-muted-foreground">
          {stat.change}
        </p>
      </CardContent>
    </Card>
  ))}
</div>
```

### Forms
```tsx
<form className="space-y-6">
  <div className="space-y-4">
    <div className="space-y-2">
      <Label htmlFor="name">Full Name</Label>
      <Input 
        id="name" 
        placeholder="Enter your name"
        className="max-w-md"
      />
    </div>
    
    <div className="space-y-2">
      <Label htmlFor="email">Email</Label>
      <Input 
        id="email" 
        type="email"
        placeholder="name@example.com"
        className="max-w-md"
      />
    </div>
  </div>

  <div className="flex gap-3">
    <Button type="submit">Submit</Button>
    <Button type="button" variant="outline">Cancel</Button>
  </div>
</form>
```

### Data Tables
```tsx
<Card className="shadow-sm">
  <CardHeader>
    <CardTitle>Recent Orders</CardTitle>
  </CardHeader>
  <CardContent>
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>Order</TableHead>
          <TableHead>Customer</TableHead>
          <TableHead>Status</TableHead>
          <TableHead className="text-right">Amount</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {orders.map(order => (
          <TableRow 
            key={order.id}
            className="hover:bg-muted/50 transition-colors"
          >
            <TableCell className="font-medium">{order.id}</TableCell>
            <TableCell>{order.customer}</TableCell>
            <TableCell>
              <Badge variant={order.statusVariant}>
                {order.status}
              </Badge>
            </TableCell>
            <TableCell className="text-right">
              {order.amount}
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </CardContent>
</Card>
```

### Modals/Dialogs
```tsx
<Dialog>
  <DialogTrigger asChild>
    <Button>Open Dialog</Button>
  </DialogTrigger>
  <DialogContent className="sm:max-w-[425px]">
    <DialogHeader>
      <DialogTitle>Edit Profile</DialogTitle>
      <DialogDescription>
        Make changes to your profile here. Click save when done.
      </DialogDescription>
    </DialogHeader>
    <div className="space-y-4 py-4">
      {/* Form fields */}
    </div>
    <DialogFooter>
      <Button type="submit">Save changes</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### Loading States
```tsx
// Skeleton loading
<Card className="shadow-sm">
  <CardHeader>
    <Skeleton className="h-4 w-[200px]" />
  </CardHeader>
  <CardContent className="space-y-3">
    <Skeleton className="h-4 w-full" />
    <Skeleton className="h-4 w-[80%]" />
  </CardContent>
</Card>

// Loading button
<Button disabled>
  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
  Please wait
</Button>
```

### Empty States
```tsx
<Card className="shadow-sm">
  <CardContent className="flex flex-col items-center justify-center py-12 space-y-3">
    <div className="p-4 bg-muted rounded-full">
      <FileX className="h-8 w-8 text-muted-foreground" />
    </div>
    <div className="text-center space-y-1">
      <h3 className="font-semibold">No results found</h3>
      <p className="text-sm text-muted-foreground">
        Try adjusting your search
      </p>
    </div>
    <Button variant="outline" size="sm">
      Clear filters
    </Button>
  </CardContent>
</Card>
```

## Layout Patterns

### Container Widths
```tsx
// Full width with constraints
<div className="container mx-auto px-4 max-w-7xl">

// Content-focused (prose)
<div className="container mx-auto px-4 max-w-3xl">

// Form-focused
<div className="container mx-auto px-4 max-w-2xl">
```

### Responsive Grids
```tsx
// Dashboard grid
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">

// Content + sidebar
<div className="grid gap-6 lg:grid-cols-[1fr_300px]">
  <main>{/* Content */}</main>
  <aside>{/* Sidebar */}</aside>
</div>

// Two column split
<div className="grid gap-6 md:grid-cols-2">
```

### Navigation
```tsx
<header className="border-b border-border">
  <div className="container mx-auto flex h-16 items-center justify-between px-4">
    <div className="flex items-center gap-6">
      <Logo />
      <nav className="hidden md:flex gap-6">
        <a href="#" className="text-sm font-medium transition-colors hover:text-primary">
          Dashboard
        </a>
        <a href="#" className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground">
          Projects
        </a>
      </nav>
    </div>
    
    <div className="flex items-center gap-4">
      <Button variant="ghost" size="sm">
        <Bell className="h-4 w-4" />
      </Button>
      <Avatar>
        <AvatarImage src={user.avatar} />
        <AvatarFallback>{user.initials}</AvatarFallback>
      </Avatar>
    </div>
  </div>
</header>
```

## Best Practices

### Component Organization
```tsx
// ✅ Good: Small, focused components
export function UserCard({ user }) {
  return (
    <Card>
      <CardHeader>
        <UserAvatar user={user} />
        <UserDetails user={user} />
      </CardHeader>
    </Card>
  )
}

// ❌ Avoid: Large monolithic components
export function DashboardPage() {
  // 500 lines of JSX...
}
```

### Composability
```tsx
// ✅ Compose shadcn components
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="ghost" size="icon">
      <MoreVertical className="h-4 w-4" />
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent align="end">
    <DropdownMenuItem>Edit</DropdownMenuItem>
    <DropdownMenuItem>Share</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem className="text-destructive">
      Delete
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

### State Management
```tsx
// Form state
const [formData, setFormData] = useState({ name: '', email: '' })

// Loading states
const [isLoading, setIsLoading] = useState(false)

// UI states
const [isOpen, setIsOpen] = useState(false)
```

### Error Handling
```tsx
<form onSubmit={handleSubmit} className="space-y-4">
  <div className="space-y-2">
    <Label htmlFor="email">Email</Label>
    <Input
      id="email"
      type="email"
      className={errors.email ? "border-destructive" : ""}
    />
    {errors.email && (
      <p className="text-sm text-destructive">{errors.email}</p>
    )}
  </div>
</form>
```

## Common Shadcn Components

### Essential Components
- **Layout**: Card, Tabs, Sheet, Dialog, Popover, Separator
- **Forms**: Input, Textarea, Select, Checkbox, Radio, Switch, Label
- **Buttons**: Button, Toggle, ToggleGroup
- **Display**: Badge, Avatar, Skeleton, Table
- **Feedback**: Alert, Toast, Progress
- **Navigation**: NavigationMenu, DropdownMenu, Command

### Button Variants
```tsx
<Button>Primary</Button>
<Button variant="secondary">Secondary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="link">Link</Button>
<Button variant="destructive">Delete</Button>
```

### Badge Variants
```tsx
<Badge>Default</Badge>
<Badge variant="secondary">Secondary</Badge>
<Badge variant="outline">Outline</Badge>
<Badge variant="destructive">Error</Badge>
```

## Workflow

1. **Understand requirements** - What component/page is needed?
2. **Choose components** - Which shadcn/ui components fit?
3. **Build structure** - Layout and hierarchy first
4. **Apply styling** - Typography, spacing, colors
5. **Add interactions** - Hover states, transitions, focus
6. **Ensure accessibility** - ARIA, keyboard, contrast
7. **Test responsive** - Mobile, tablet, desktop

## Quality Checklist

Before completing:
- [ ] Uses shadcn/ui components appropriately
- [ ] Follows 4px spacing scale (p-2, p-4, p-6, etc.)
- [ ] Uses semantic color tokens (bg-card, text-foreground, etc.)
- [ ] Limited shadow usage (shadow-sm/md/lg only)
- [ ] Smooth transitions (200-300ms duration)
- [ ] ARIA labels on interactive elements
- [ ] Keyboard focus visible (ring-2 ring-primary)
- [ ] WCAG AA contrast ratios
- [ ] Mobile-responsive layout
- [ ] Loading and error states handled

## References

- [Shadcn UI](https://ui.shadcn.com) - Component library
- [Tailwind CSS](https://tailwindcss.com) - Utility classes
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/) - Accessibility standards
