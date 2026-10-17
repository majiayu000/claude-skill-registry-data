---
name: better-design-shadcn-themes
description: Install and use themed shadcn/ui components from 31+ design systems (Linear, Stripe, Apple, Notion, etc.) with one command
triggers:
  - install shadcn component with custom theme
  - add Linear styled button to my project
  - use better-design components
  - apply Stripe design system to shadcn
  - install themed shadcn components
  - browse available design systems for shadcn
  - add Apple themed UI components
  - customize shadcn with design system themes
---

# better-design-shadcn-themes

> Skill by [ara.so](https://ara.so) — Design Skills collection.

## Overview

Better Design provides 31+ production-ready design systems for shadcn/ui. Each design system includes ~89 fully themed components (buttons, cards, dialogs, forms, etc.) that you can install directly into your shadcn/ui project with a single CLI command. All design systems are MIT licensed and include popular styles like Linear, Stripe, Airbnb, Apple, Notion, Vercel, Supabase, and Figma.

Browse all design systems at: https://better-design.com/design-systems

## Installation

Better Design components install directly into existing shadcn/ui projects using the shadcn CLI. There's no separate package to install — you pull individual components on-demand.

### Prerequisites

Your project must already have shadcn/ui initialized:

```bash
npx shadcn@latest init
```

## Core Commands

### Install a Single Component

```bash
npx shadcn@latest add https://www.better-design.com/registry/<design-system>/<component>.json
```

**Examples:**

```bash
# Install Linear-styled button
npx shadcn@latest add https://www.better-design.com/registry/linear/button.json

# Install Stripe-styled card
npx shadcn@latest add https://www.better-design.com/registry/stripe/card.json

# Install Apple-styled dialog
npx shadcn@latest add https://www.better-design.com/registry/apple/dialog.json

# Install Notion-styled input
npx shadcn@latest add https://www.better-design.com/registry/notion/input.json
```

The CLI automatically:
- Downloads the component TypeScript file
- Installs required dependencies
- Updates CSS variables in `globals.css`
- Handles component dependencies

### Install Multiple Components

```bash
# Install several components from the same design system
npx shadcn@latest add \
  https://www.better-design.com/registry/linear/button.json \
  https://www.better-design.com/registry/linear/input.json \
  https://www.better-design.com/registry/linear/card.json
```

## Available Design Systems

| Design System Slug | Style | Best For |
|-------------------|-------|----------|
| `linear` | Clean, modern, dark | Project management, SaaS |
| `stripe` | Professional, minimal | Fintech, payments |
| `apple` | Polished, refined | Consumer apps |
| `notion` | Soft, approachable | Note-taking, docs |
| `vercel` | Sleek, high-contrast | Developer tools |
| `supabase` | Bold, green accent | Backend tools, dashboards |
| `figma` | Colorful, playful | Design tools |
| `airbnb` | Warm, friendly | Marketplace, social |
| `beam-lib` | Gradient, modern | Creative tools |
| `corporate-fintech` | Conservative, trust | Enterprise, finance |
| `glassmorphic-dark` | Frosted glass effect | Modern dark UIs |
| `minimal-light` | Ultra-clean light | Content-first apps |
| `midnight-glass` | Dark with glass | Premium apps |
| `vibrant-dark` | High-saturation dark | Gaming, entertainment |

Full list of 31 design systems: https://better-design.com/design-systems

## Component Usage Patterns

### Basic Component Import

After installing a component, import and use it like any shadcn component:

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"

export default function MyPage() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Linear-styled Card</CardTitle>
      </CardHeader>
      <CardContent>
        <Input placeholder="Enter text..." />
        <Button>Submit</Button>
      </CardContent>
    </Card>
  )
}
```

### Mixing Design Systems

You can install components from different design systems in the same project:

```tsx
// Linear button with Stripe card
import { Button } from "@/components/ui/button" // Linear
import { Card } from "@/components/ui/card" // Stripe

export default function MixedDesign() {
  return (
    <Card className="p-6">
      <h2>Checkout</h2>
      <Button>Pay with Linear button style</Button>
    </Card>
  )
}
```

**Note:** CSS variables may conflict when mixing design systems. For best results, stick to one design system per project or carefully test combinations.

### Form Components Example

```tsx
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

export default function ContactForm() {
  return (
    <form className="space-y-4">
      <div>
        <Label htmlFor="name">Name</Label>
        <Input id="name" placeholder="John Doe" />
      </div>
      
      <div>
        <Label htmlFor="email">Email</Label>
        <Input id="email" type="email" placeholder="john@example.com" />
      </div>
      
      <div>
        <Label htmlFor="topic">Topic</Label>
        <Select>
          <SelectTrigger id="topic">
            <SelectValue placeholder="Select a topic" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="support">Support</SelectItem>
            <SelectItem value="sales">Sales</SelectItem>
            <SelectItem value="feedback">Feedback</SelectItem>
          </SelectContent>
        </Select>
      </div>
      
      <div>
        <Label htmlFor="message">Message</Label>
        <Textarea id="message" placeholder="Your message..." />
      </div>
      
      <Button type="submit">Send Message</Button>
    </form>
  )
}
```

### Dialog Component Example

```tsx
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

export default function EditProfileDialog() {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline">Edit Profile</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Edit profile</DialogTitle>
          <DialogDescription>
            Make changes to your profile here. Click save when you're done.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="username" className="text-right">
              Username
            </Label>
            <Input id="username" defaultValue="@johndoe" className="col-span-3" />
          </div>
        </div>
        <DialogFooter>
          <Button type="submit">Save changes</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
```

### Data Table Example

```tsx
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"

const invoices = [
  { id: "INV001", status: "Paid", amount: "$250.00" },
  { id: "INV002", status: "Pending", amount: "$150.00" },
  { id: "INV003", status: "Paid", amount: "$350.00" },
]

export default function InvoiceTable() {
  return (
    <Table>
      <TableCaption>A list of your recent invoices.</TableCaption>
      <TableHeader>
        <TableRow>
          <TableHead>Invoice</TableHead>
          <TableHead>Status</TableHead>
          <TableHead>Amount</TableHead>
          <TableHead className="text-right">Actions</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {invoices.map((invoice) => (
          <TableRow key={invoice.id}>
            <TableCell className="font-medium">{invoice.id}</TableCell>
            <TableCell>
              <Badge variant={invoice.status === "Paid" ? "default" : "secondary"}>
                {invoice.status}
              </Badge>
            </TableCell>
            <TableCell>{invoice.amount}</TableCell>
            <TableCell className="text-right">
              <Button variant="ghost" size="sm">View</Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  )
}
```

## Available Components

Each design system includes ~89 components:

**Layout & Structure:**
- `accordion`, `card`, `separator`, `tabs`, `table`

**Forms & Input:**
- `button`, `input`, `textarea`, `checkbox`, `radio-group`, `select`, `slider`, `switch`, `form`, `label`

**Feedback & Overlays:**
- `dialog`, `alert-dialog`, `drawer`, `sheet`, `popover`, `tooltip`, `toast`, `alert`, `badge`, `progress`, `skeleton`

**Navigation:**
- `navigation-menu`, `menubar`, `dropdown-menu`, `context-menu`, `breadcrumb`, `pagination`, `command`

**Data Display:**
- `avatar`, `calendar`, `chart`, `carousel`, `collapsible`, `data-table`, `hover-card`, `aspect-ratio`

**Typography:**
- `typography`

## Configuration

### CSS Variables

Each design system uses CSS variables defined in `globals.css`. When you install your first component from a design system, the CLI updates `globals.css` with theme tokens:

```css
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 0 0% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 0 0% 3.9%;
    --primary: 0 0% 9%;
    --primary-foreground: 0 0% 98%;
    /* ... more variables */
  }

  .dark {
    --background: 0 0% 3.9%;
    --foreground: 0 0% 98%;
    /* ... dark mode overrides */
  }
}
```

These variables are automatically configured — you don't need to manually edit them.

### Tailwind Configuration

Better Design components use your existing shadcn Tailwind config. Ensure your `tailwind.config.ts` has the shadcn setup:

```typescript
import type { Config } from "tailwindcss"

const config: Config = {
  darkMode: ["class"],
  content: [
    "./pages/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./app/**/*.{ts,tsx}",
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        // ... other color definitions
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}

export default config
```

## Repository Structure

If forking or contributing to the Better Design repo:

```
registry/
  <design-system>/
    button.json        # Registry entry for shadcn CLI
    card.json
    input.json
    ...
  index.json           # Registry manifest

components/
  <design-system>/
    components/ui/     # Readable TypeScript source
      button.tsx
      card.tsx
      ...
    globals.css        # CSS variables for the theme
    lib/utils.ts       # cn() utility
```

- **`registry/`** — Source of truth for CLI installations (JSON format)
- **`components/`** — Human-readable `.tsx` files for browsing/copying

Both directories stay in sync. When forking, copy both the component and matching `globals.css`.

## Common Patterns

### Creating a Landing Page Hero

```tsx
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

export default function Hero() {
  return (
    <section className="flex min-h-screen flex-col items-center justify-center px-4">
      <h1 className="text-5xl font-bold tracking-tight">
        Ship faster with Better Design
      </h1>
      <p className="mt-4 text-xl text-muted-foreground">
        31+ design systems for shadcn/ui. Install with one command.
      </p>
      <div className="mt-8 flex gap-4">
        <Button size="lg">Get Started</Button>
        <Button size="lg" variant="outline">View Designs</Button>
      </div>
      <div className="mt-12 flex w-full max-w-md gap-2">
        <Input placeholder="Enter your email..." type="email" />
        <Button>Subscribe</Button>
      </div>
    </section>
  )
}
```

### Building a Dashboard Layout

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"

export default function Dashboard() {
  return (
    <div className="p-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <Button>Create New</Button>
      </div>

      <Tabs defaultValue="overview" className="mt-6">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="reports">Reports</TabsTrigger>
        </TabsList>
        <TabsContent value="overview" className="mt-6">
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <Card>
              <CardHeader>
                <CardTitle>Total Revenue</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">$45,231.89</div>
                <p className="text-xs text-muted-foreground">
                  +20.1% from last month
                </p>
                <Progress value={60} className="mt-2" />
              </CardContent>
            </Card>
            {/* More cards... */}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  )
}
```

### Authentication Form

```tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"

export default function LoginForm() {
  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Sign In</CardTitle>
        <CardDescription>
          Enter your email and password to access your account
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="email">Email</Label>
          <Input id="email" type="email" placeholder="name@example.com" />
        </div>
        <div className="space-y-2">
          <Label htmlFor="password">Password</Label>
          <Input id="password" type="password" />
        </div>
        <Button className="w-full">Sign In</Button>
        <div className="relative">
          <Separator />
          <span className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 bg-background px-2 text-xs text-muted-foreground">
            OR CONTINUE WITH
          </span>
        </div>
        <Button variant="outline" className="w-full">
          GitHub
        </Button>
      </CardContent>
      <CardFooter className="flex justify-center">
        <p className="text-sm text-muted-foreground">
          Don't have an account? <a href="#" className="underline">Sign up</a>
        </p>
      </CardFooter>
    </Card>
  )
}
```

## Troubleshooting

### Components Don't Match Preview

**Problem:** Installed component looks different from the Better Design website preview.

**Solutions:**
1. Ensure `globals.css` was updated by the CLI (check for CSS variables)
2. Verify your Tailwind config includes shadcn color definitions
3. Check that you're importing from the correct path: `@/components/ui/[component]`
4. Clear Next.js cache: `rm -rf .next` and restart dev server

### CSS Variables Not Applied

**Problem:** Components render but colors/spacing are wrong.

**Solution:** Check that `globals.css` is imported in your root layout:

```tsx
// app/layout.tsx or pages/_app.tsx
import "@/app/globals.css"
```

### Type Errors After Installation

**Problem:** TypeScript errors on component imports.

**Solutions:**
1. Restart TypeScript server in your editor
2. Check `tsconfig.json` has correct path alias:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```
3. Run `npm install` to ensure all dependencies are installed

### Mixing Design Systems

**Problem:** Components from different design systems clash visually.

**Best Practice:** Stick to one design system per project for consistency. If you must mix:
- Use different design systems for distinct sections (e.g., marketing site vs. app dashboard)
- Test thoroughly in both light and dark modes
- Be prepared to manually adjust CSS variables

### Component Dependencies Missing

**Problem:** Error about missing component dependency (e.g., Button needs Label).

**Solution:** Install the missing component from the same design system:
```bash
npx shadcn@latest add https://www.better-design.com/registry/linear/label.json
```

The shadcn CLI usually handles dependencies automatically, but occasionally you may need to manually install related components.

## Contributing

To contribute a new design system or component:

1. Fork the repository: https://github.com/marvkr/better-design
2. Create both `registry/<design-system>/` and `components/<design-system>/` directories
3. Add component JSON files to `registry/` following shadcn registry format
4. Add matching `.tsx` files to `components/<design-system>/components/ui/`
5. Include `globals.css` with theme CSS variables
6. Update `registry/index.json` manifest
7. Submit a pull request

All design systems must be MIT licensed and include at least 20+ core components.
