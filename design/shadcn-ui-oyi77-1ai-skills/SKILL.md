---
name: shadcn-ui
description: Use when shadcn/ui component library — copy-paste React components, Tailwind
  CSS, Radix primitives, theming. Use when working with shadcn ui.
domain: content
author: oyi77
license: Apache-2.0
subdomain: content-creation
tags:
- content-creation
- digital-content
- media
- shadcn
version: 1.0.0
category: content
---




## Overview

shadcn/ui is a collection of reusable components built with Radix UI and Tailwind CSS. Components are copied into your project, not installed as dependencies — giving you full control over customization.

## Capabilities

- CLI-based component installation into your project
- Full source code ownership — components live in your codebase
- Theming via CSS variables and Tailwind config
- Dark mode support out of the box
- Forms with React Hook Form + Zod validation
- Data tables with TanStack Table integration

## When to Use

**Trigger phrases:**
- "shadcn ui"
- "Starting a new React/Next"
- "Need accessible components without vendor lock-in"
- "Want Tailwind-native components with full customization"


- Starting a new React/Next.js project with polished UI
- Need accessible components without vendor lock-in
- Want Tailwind-native components with full customization
- Building admin dashboards, SaaS apps, or marketing sites

## When NOT to Use

- Task is about content strategy, not creation (use strategy skills)
- Task is about content distribution (use distribution skills)
- You need to analyze content performance (use analytics skills)
- Task is about content moderation (use moderation tools)
- You don't have content guidelines
- Task requires domain expertise (consult experts)


## Pseudo Code

The shadcn-ui workflow follows a standard pipeline pattern.

Core flow:
```
# shadcn-ui primary flow
input = prepare(raw_data)
result = process(input, config={component, components, copy, library, paste})
validate(result)
deliver(result)
```

Error handling:
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Core Workflow
```
# shadcn-ui primary flow
input = prepare(raw_data)
result = process(input, config={component, components, copy, library, paste})
validate(result)
deliver(result)
```

### Error Handling
```
on error:
  log(error_details)
  retry_with_backoff(max=3)
  if still_failing: alert_and_escalate()
```


### Installation
```bash
npx shadcn@latest init
npx shadcn@latest add button card form dialog table
```

### Theme Configuration
```css
/* globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --radius: 0.5rem;
  }
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
  }
}
```

### Component Usage
```tsx
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog"

export function Dashboard() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Dashboard</CardTitle>
      </CardHeader>
      <CardContent>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="outline">Open Settings</Button>
          </DialogTrigger>
          <DialogContent>Settings content</DialogContent>
        </Dialog>
      </CardContent>
    </Card>
  )
}
```

### Form with Validation
```tsx
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const schema = z.object({ email: z.string().email() })

export function LoginForm() {
  const form = useForm({ resolver: zodResolver(schema) })
  return (
    <Form {...form}>
      <FormField control={form.control} name="email" render={({ field }) => (
        <FormItem>
          <FormLabel>Email</FormLabel>
          <FormControl><Input {...field} /></FormControl>
          <FormMessage />
        </FormItem>
      )} />
    </Form>
  )
}
```

## Common Patterns

- **Variant system**: `className={cn(buttonVariants({ variant: "outline", size: "sm" }))}`
- **Composition**: Combine primitives (Dialog + Form + Button) for complex flows
- **Theming**: Override CSS variables for brand colors, spacing, radius
- **Responsive**: Use Tailwind breakpoints directly in component className
- **Data tables**: Pair with `@tanstack/react-table` for sortable, filterable tables

## How to Use

1. Define content goal (traffic, engagement, conversion, brand awareness)
2. Research target audience pain points and search intent
3. Generate content using appropriate AI tools
4. Edit and humanize output for authenticity
5. Optimize for target platform (SEO, hashtags, format)
6. Schedule and distribute across channels
7. Measure performance and iterate

## Red Flags

- **AI-generated content sounds robotic**: Always run through humanizer before publishing
- **Engagement dropping week-over-week**: Content fatigue or algorithm change — vary formats
- **Duplicate content across platforms**: Adapt content per platform, don't just cross-post
- **No content calendar**: Sporadic posting kills audience retention
- **Ignoring analytics**: Content without measurement is just publishing, not marketing

## Verification

- [ ] Skill output matches expected behavior

## Process

1. Analyze the task requirements
2. Apply domain expertise
3. Verify output quality

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "Good enough content works" | Quality content drives engagement. Mediocre content gets ignored. |
| "I will optimize later" | SEO and distribution need optimization from the start. |
| "Templates are good enough" | Templates are a starting point. Custom content outperforms generic. |

## Video / Motion Graphics

shadcn-ui components (Card, Badge, Button) work as visual building blocks in [Remotion](../video/remotion/SKILL.md) compositions. Use for product demo mockups, dashboard showcases, and feature highlight videos. Style with inline CSS for animation compatibility — Tailwind animation classes are forbidden in Remotion; use `interpolate()` instead.