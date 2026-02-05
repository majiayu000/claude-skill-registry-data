---
name: ui-components
description: React UI component specialist with Tailwind CSS and shadcn/ui for building responsive, accessible interfaces
---

# UI Components Specialist

## Instructions
When building UI components:

1. **Component Creation**
   - Use shadcn/ui components whenever available
   - Prefer `@/components/ui/button` over `<button>`
   - Use `@/components/ui/input` over `<input>`
   - Check available components before creating custom ones

2. **Styling Guidelines**
   - Use Tailwind CSS classes only
   - Apply dark theme consistently
   - Use glassmorphism effects with backdrop-blur
   - Follow the kebab-case file naming convention

3. **Responsive Design**
   - Mobile-first approach
   - Use Tailwind's responsive prefixes (sm:, md:, lg:)
   - Test on multiple screen sizes
   - Ensure touch-friendly interactions

4. **Performance & UX**
   - Add loading states with Skeleton components
   - Implement error boundaries
   - Use lazy loading for heavy components
   - Add smooth transitions sparingly

## Examples

**Using shadcn/ui components:**
```typescript
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

function LoginForm() {
  return (
    <div className="space-y-4">
      <Label htmlFor="email">Email</Label>
      <Input id="email" type="email" />
      <Button type="submit">Submit</Button>
    </div>
  )
}
```

**Creating a content card:**
```typescript
import { Badge } from '@/components/ui/badge'

function MovieCard({ movie }) {
  return (
    <div className="relative group cursor-pointer">
      <img
        src={movie.poster}
        alt={movie.title}
        className="w-full rounded-lg"
      />
      <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity">
        <Badge className="absolute top-2 right-2">
          {movie.rating}
        </Badge>
      </div>
    </div>
  )
}
```

**Adding loading state:**
```typescript
import { Skeleton } from '@/components/ui/skeleton'

function ContentRowSkeleton() {
  return (
    <div className="space-y-4">
      <Skeleton className="h-6 w-48" />
      <div className="flex gap-4 overflow-x-auto">
        {Array.from({ length: 6 }).map((_, i) => (
          <Skeleton key={i} className="h-64 w-48 flex-shrink-0" />
        ))}
      </div>
    </div>
  )
}
```