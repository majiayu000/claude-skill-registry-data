---
name: pinpoint-ui
description: shadcn/ui patterns, progressive enhancement, Server Components, Client Components, form handling, Tailwind CSS v4, accessibility. Use when building UI, forms, components, or when user mentions UI/styling/components/forms.
---

# PinPoint UI Guide

## When to Use This Skill

Use this skill when:
- Building or modifying UI components
- Creating forms
- Working with shadcn/ui components
- Styling with Tailwind CSS v4
- Implementing progressive enhancement
- Deciding between Server and Client Components
- User mentions: "UI", "component", "form", "styling", "Tailwind", "shadcn", "button", "input"

## Quick Reference

### Critical UI Rules
1. **Server Components first**: Default to Server Components, use "use client" only for interactivity
2. **Progressive enhancement**: Forms must work without JavaScript
3. **shadcn/ui only**: No MUI components
4. **Direct Server Action references**: No inline wrappers in forms
5. **Dropdown Server Actions**: Use `onSelect`, not forms
6. **Tailwind CSS v4**: Use CSS variables, no hardcoded hex colors

### Adding Components
```bash
npx shadcn@latest add [component]
```

## Detailed Documentation

Read these files for comprehensive UI guidance:

```bash
# Primary UI guide - the "Goto" manual for all UI work
cat docs/UI_GUIDE.md

# Specific UI implementation patterns
ls docs/ui-patterns/
cat docs/ui-patterns/*.md
```

## Core UI Patterns

### Server vs Client Components

```typescript
// ✅ Good: Server Component (default)
export default async function MachinesPage() {
  const machines = await getMachines();

  return (
    <div>
      {machines.map((machine) => (
        <MachineCard key={machine.id} machine={machine} />
      ))}
    </div>
  );
}

// ✅ Good: Client Component (only when needed)
"use client";
import { useState } from "react";

export function IssueFilter() {
  const [filter, setFilter] = useState("all");

  return (
    <select value={filter} onChange={(e) => setFilter(e.target.value)}>
      <option value="all">All Issues</option>
      <option value="open">Open</option>
      <option value="resolved">Resolved</option>
    </select>
  );
}
```

### Forms with Progressive Enhancement

```typescript
// ✅ Good: Direct Server Action reference
import { createIssue } from "~/server/actions/issues";

export function CreateIssueForm() {
  return (
    <form action={createIssue}>
      <input name="title" required />
      <textarea name="description" />
      <button type="submit">Create Issue</button>
    </form>
  );
}

// ❌ Bad: Inline wrapper (breaks Next.js form handling)
<form action={async () => { await createIssue(); }}>
```

### Forms with useActionState (React 19)

```typescript
"use client";
import { useActionState } from "react";
import { createIssue } from "~/server/actions/issues";

export function CreateIssueForm() {
  const [state, formAction] = useActionState(createIssue, { message: "" });

  return (
    <form action={formAction}>
      <input name="title" required />
      {state.message && <p className="text-red-500">{state.message}</p>}
      <button type="submit">Create Issue</button>
    </form>
  );
}
```

### Dropdowns with Server Actions

```typescript
"use client";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "~/components/ui/dropdown-menu";
import { deleteIssue } from "~/server/actions/issues";

export function IssueActionsMenu({ issueId }: { issueId: string }) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost">Actions</Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        {/* ✅ Good: Use onSelect */}
        <DropdownMenuItem
          onSelect={async () => {
            await deleteIssue(issueId);
          }}
        >
          Delete
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

// ❌ Bad: Form inside dropdown (unmounts before submission)
<DropdownMenuItem>
  <form action={deleteIssue}>
    <button>Delete</button>
  </form>
</DropdownMenuItem>
```

## Styling with Tailwind CSS v4

### CSS Variables (No Hardcoded Colors)

```typescript
// ✅ Good: Use CSS variables from globals.css
<div className="bg-background text-foreground">
  <p className="text-muted-foreground">Muted text</p>
</div>

// ❌ Bad: Hardcoded hex colors
<div style={{ backgroundColor: "#ffffff", color: "#000000" }}>
```

### Component Styling

```typescript
// ✅ Good: Use className with cn() for merging
import { cn } from "~/lib/utils";

export function Button({ className, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        "rounded-md bg-primary px-4 py-2 text-primary-foreground",
        className
      )}
      {...props}
    />
  );
}

// ❌ Bad: String concatenation (doesn't handle conflicts)
<button className={`base-classes ${className}`} />

// ❌ Bad: Inline styles
<button style={{ marginTop: '10px' }} />
```

### Global vs Local Styles

```typescript
// ✅ Global styles (globals.css)
// - Typography (headings, body text)
// - Theme variables (colors, spacing)

// ✅ Local styles (component className)
// - Component-specific layout
// - Responsive design
// - Interactive states (hover, focus)

// ❌ Bad: Hardcoded spacing in reusable components
export function Card({ children }: CardProps) {
  return <div className="m-4 p-4">{children}</div>; // Too opinionated
}

// ✅ Good: Allow className override
export function Card({ children, className }: CardProps) {
  return <div className={cn("rounded-lg border", className)}>{children}</div>;
}
```

## shadcn/ui Component Patterns

### Button Variants

```typescript
import { Button } from "~/components/ui/button";

<Button variant="default">Primary Action</Button>
<Button variant="secondary">Secondary Action</Button>
<Button variant="destructive">Delete</Button>
<Button variant="ghost">Subtle Action</Button>
<Button variant="link">Link Style</Button>
```

### Dialog (Modal) Pattern

```typescript
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "~/components/ui/dialog";

export function CreateIssueDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Create Issue</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Create New Issue</DialogTitle>
          <DialogDescription>
            Report a problem with a machine.
          </DialogDescription>
        </DialogHeader>
        <CreateIssueForm />
      </DialogContent>
    </Dialog>
  );
}
```

### Form with shadcn/ui

```typescript
import { Label } from "~/components/ui/label";
import { Input } from "~/components/ui/input";
import { Textarea } from "~/components/ui/textarea";
import { Button } from "~/components/ui/button";

export function IssueForm() {
  return (
    <form action={createIssue} className="space-y-4">
      <div>
        <Label htmlFor="title">Title</Label>
        <Input id="title" name="title" required />
      </div>
      <div>
        <Label htmlFor="description">Description</Label>
        <Textarea id="description" name="description" />
      </div>
      <Button type="submit">Create Issue</Button>
    </form>
  );
}
```

## Accessibility Patterns

### Semantic HTML

```typescript
// ✅ Good: Semantic HTML
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/machines">Machines</a></li>
    <li><a href="/issues">Issues</a></li>
  </ul>
</nav>

// ❌ Bad: Div soup
<div className="nav">
  <div className="nav-item">Machines</div>
  <div className="nav-item">Issues</div>
</div>
```

### ARIA Labels

```typescript
// ✅ Good: ARIA labels for screen readers
<Button aria-label="Delete issue">
  <TrashIcon className="h-4 w-4" />
</Button>

// ✅ Good: Label association
<Label htmlFor="email">Email</Label>
<Input id="email" name="email" type="email" />
```

## Progressive Enhancement

### CSS-Only Patterns

```typescript
// ✅ Good: CSS-only hover effects
<div className="group">
  <Button className="group-hover:bg-primary/90">
    Hover Me
  </Button>
</div>

// ✅ Good: Peer patterns for form validation
<Input className="peer" />
<p className="peer-invalid:visible invisible text-red-500">
  Invalid input
</p>
```

### Fallback for No JS

```typescript
// ✅ Good: Form works without JavaScript
<form action={createIssue} method="POST">
  <input name="title" required />
  <button type="submit">Submit</button>
  {/* No client-side validation required */}
</form>

// ❌ Bad: Requires JavaScript
<form onSubmit={(e) => {
  e.preventDefault();
  // Client-side only logic
}}>
```

## Layout Patterns

### Page Layout

```typescript
// ✅ Good: Consistent page structure
export default async function MachinesPage() {
  const machines = await getMachines();

  return (
    <div className="container mx-auto py-8">
      <div className="mb-8 flex items-center justify-between">
        <h1 className="text-3xl font-bold">Machines</h1>
        <Button asChild>
          <Link href="/machines/new">Add Machine</Link>
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {machines.map((machine) => (
          <MachineCard key={machine.id} machine={machine} />
        ))}
      </div>
    </div>
  );
}
```

### Responsive Grid

```typescript
// ✅ Good: Responsive grid with Tailwind
<div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {items.map((item) => (
    <Card key={item.id}>{item.name}</Card>
  ))}
</div>
```

## UI Anti-Patterns

### ❌ Don't Do These

**Global CSS Resets**:
```css
/* ❌ Bad: Breaks component internals */
* {
  margin: 0;
  padding: 0;
}

/* ✅ Good: Use Tailwind's Preflight */
@tailwind base;
```

**Hardcoded Spacing in Components**:
```typescript
// ❌ Bad: Rigid component
export function Card({ children }: CardProps) {
  return <div className="m-4 p-4">{children}</div>;
}

// ✅ Good: Flexible component
export function Card({ children, className }: CardProps) {
  return <div className={cn("rounded-lg", className)}>{children}</div>;
}
```

**Inline Styles**:
```typescript
// ❌ Bad: Inline styles
<div style={{ marginTop: '10px', color: '#ff0000' }}>

// ✅ Good: Tailwind utilities
<div className="mt-2.5 text-red-500">
```

## UI Checklist

Before committing UI code:

- [ ] Server Components by default (only "use client" when needed)
- [ ] Forms work without JavaScript
- [ ] Direct Server Action references (no inline wrappers)
- [ ] Dropdowns use `onSelect` for Server Actions
- [ ] CSS variables, no hardcoded colors
- [ ] `cn()` used for className merging
- [ ] Semantic HTML (nav, main, article, etc.)
- [ ] ARIA labels for icon-only buttons
- [ ] Responsive design (mobile-first)
- [ ] shadcn/ui components only (no MUI)

## Additional Resources

- UI guide: `docs/UI_GUIDE.md`
- UI patterns: `docs/ui-patterns/*.md`
- shadcn/ui docs: Use Context7 MCP for latest components
- Tailwind CSS v4 docs: Use Context7 MCP for latest utilities
