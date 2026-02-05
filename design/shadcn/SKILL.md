---
name: shadcn
description: >
  Implement shadcn/ui components for PhotoVault with accessibility and theming.
  Use when working with UI components, forms, dialogs, buttons, cards, tables,
  Tailwind styling, or fixing accessibility issues. Includes PhotoVault theme
  system and established UI patterns.
---

# ⚠️ MANDATORY WORKFLOW - DO NOT SKIP

**When this skill activates, you MUST follow the expert workflow before writing any code:**

1. **Spawn Domain Expert** using the Task tool with this prompt:
   ```
   Read the expert prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\shadcn-expert.md

   Then research the codebase and write an implementation plan to: docs/claude/plans/ui-[task-name]-plan.md

   Task: [describe the user's request]
   ```

2. **Spawn QA Critic** after expert returns, using Task tool:
   ```
   Read the QA critic prompt at: C:\Users\natha\Stone-Fence-Brain\VENTURES\PhotoVault\claude\experts\qa-critic-expert.md

   Review the plan at: docs/claude/plans/ui-[task-name]-plan.md
   Write critique to: docs/claude/plans/ui-[task-name]-critique.md
   ```

3. **Present BOTH plan and critique to user** - wait for approval before implementing

**DO NOT read files and start coding. DO NOT rationalize that "this is simple." Follow the workflow.**

---

# shadcn/ui Integration

## Core Principles

### Accessibility First, Always

Every interactive component MUST be keyboard navigable and screen reader friendly. shadcn/ui is built on Radix primitives which handle most accessibility out of the box.

```tsx
<Button aria-label="Close dialog" onClick={onClose}>
  <X className="h-4 w-4" />
</Button>
```

### Composition Over Configuration

shadcn/ui components are meant to be composed, not configured with dozens of props.

```tsx
// ✅ RIGHT: Compose components
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content here</CardContent>
  <CardFooter>
    <Button>Action</Button>
  </CardFooter>
</Card>

// ❌ WRONG: Mega-component with too many props
<Card title="Title" description="..." content="..." footerButton="Action" />
```

### Always Use Semantic Color Tokens

Never hardcode colors. Use semantic tokens for theming support.

```tsx
// ❌ WRONG: Hardcoded colors break theming
<div className="bg-white text-black" />

// ✅ RIGHT: Semantic tokens
<div className="bg-background text-foreground" />
```

## Anti-Patterns

**Not forwarding refs on custom components**
```tsx
// WRONG: Refs don't work
const CustomButton = ({ className, ...props }) => {
  return <Button className={className} {...props} />
}

// RIGHT: Forward refs
const CustomButton = React.forwardRef<
  HTMLButtonElement,
  React.ComponentPropsWithoutRef<typeof Button>
>(({ className, ...props }, ref) => {
  return <Button ref={ref} className={className} {...props} />
})
CustomButton.displayName = "CustomButton"
```

**Not using cn() for class merging**
```tsx
// WRONG: Classes override unpredictably
<Button className={`${baseClasses} ${conditionalClasses}`}>

// RIGHT: Use cn() for proper merging
import { cn } from "@/lib/utils"
<Button className={cn(baseClasses, conditionalClasses)}>
```

**Nesting interactive elements**
```tsx
// WRONG: Button inside clickable card (accessibility violation)
<Card onClick={handleClick}>
  <Button onClick={handleAction}>Action</Button>
</Card>

// RIGHT: Separate interactive areas
<Card>
  <CardContent onClick={handleClick}>...</CardContent>
  <CardFooter>
    <Button onClick={handleAction}>Action</Button>
  </CardFooter>
</Card>
```

**Not connecting labels to inputs**
```tsx
// WRONG: Label not connected
<Label>Email</Label>
<Input type="email" />

// RIGHT: Use FormField pattern
<FormField
  control={form.control}
  name="email"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Email</FormLabel>
      <FormControl>
        <Input {...field} />
      </FormControl>
      <FormMessage />
    </FormItem>
  )}
/>
```

## Button Variants

```tsx
<Button>Save Changes</Button>                    // Primary
<Button variant="secondary">Cancel</Button>      // Secondary
<Button variant="destructive">Delete</Button>    // Destructive
<Button variant="ghost">Edit</Button>            // Subtle
<Button variant="outline">View Details</Button>  // Outline

// Icon button with accessibility
<Button variant="ghost" size="icon" aria-label="Settings">
  <Settings className="h-4 w-4" />
</Button>

// Loading state
<Button disabled>
  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
  Please wait
</Button>
```

## Dialog Pattern

```tsx
import {
  Dialog, DialogContent, DialogDescription,
  DialogFooter, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog"

function ConfirmDialog({ onConfirm }: { onConfirm: () => void }) {
  const [open, setOpen] = useState(false)

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="destructive">Delete Item</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Are you sure?</DialogTitle>
          <DialogDescription>This action cannot be undone.</DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>Cancel</Button>
          <Button variant="destructive" onClick={() => { onConfirm(); setOpen(false) }}>
            Delete
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

## Form Pattern (react-hook-form + zod)

```tsx
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"

const formSchema = z.object({
  email: z.string().email("Please enter a valid email"),
  name: z.string().min(2, "Name must be at least 2 characters"),
})

function ContactForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { email: "", name: "" },
  })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="John Doe" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? "Submitting..." : "Submit"}
        </Button>
      </form>
    </Form>
  )
}
```

## Toast Notifications (Sonner)

```tsx
import { toast } from "sonner"

toast.success("Changes saved successfully")
toast.error("Failed to save changes")

// Promise toast
toast.promise(saveData(), {
  loading: "Saving...",
  success: "Data saved!",
  error: "Could not save data",
})
```

## PhotoVault Configuration

### Theme System

PhotoVault has 5 color themes in `src/lib/themes.ts`:
- **Warm Gallery** - Cream background, terracotta primary (default)
- **Cool Professional** - Cool slate, indigo primary
- **Gallery Dark** - Warm charcoal, amber accents
- **Soft Sage** - Sage green, emerald + pink accents
- **Original Teal** - Original PhotoVault theme

### PhotoVault UI Patterns

**Gallery Card:**
```tsx
<Card className="overflow-hidden transition-shadow hover:shadow-lg">
  <div className="aspect-[4/3] relative">
    <Image src={coverImage} alt={galleryName} fill className="object-cover" />
  </div>
  <CardContent className="p-4">
    <h3 className="font-semibold truncate">{galleryName}</h3>
    <p className="text-sm text-muted-foreground">{photoCount} photos</p>
  </CardContent>
</Card>
```

**Paywall UI:**
```tsx
<div className="text-center py-12 px-4">
  <Lock className="h-12 w-12 mx-auto text-muted-foreground mb-4" />
  <h2 className="text-2xl font-bold mb-2">Gallery Access Required</h2>
  <p className="text-muted-foreground mb-6">Pay to unlock all photos</p>
  <Button size="lg" onClick={handlePayment}>Pay Now - ${price}</Button>
</div>
```

### Semantic Color Tokens

| Token | Purpose |
|-------|---------|
| `bg-background` | Page background |
| `bg-card` | Card backgrounds |
| `bg-primary` | Primary buttons |
| `bg-secondary` | Secondary elements |
| `bg-destructive` | Delete/error actions |
| `text-muted-foreground` | Subtle text |
| `border-border` | Borders |

### Component Installation

```bash
npx shadcn@latest add button card dialog form input
```

## Debugging Checklist

1. Are you using semantic color tokens? Check for hardcoded colors
2. Is cn() being used for class merging?
3. Are refs being forwarded in custom components?
4. Is the component accessible? Test with keyboard
5. Are form fields properly connected to labels?
