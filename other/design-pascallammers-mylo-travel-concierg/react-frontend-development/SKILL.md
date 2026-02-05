---
name: React Frontend Development
description: Build React components with TypeScript, Tailwind CSS, and React Query for the Medellin Spark platform. Use when implementing UI features, creating components, managing state, or optimizing frontend performance. Specializes in React hooks, shadcn/ui components, and Supabase integration.
version: 1.0.0
---

# React Frontend Development

## Stack Overview

- **Framework**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS + shadcn/ui components
- **State**: React Query (@tanstack/react-query)
- **Backend**: Supabase (auth, database, edge functions)
- **Icons**: Lucide React
- **Forms**: React Hook Form (when needed)

## Component Patterns

### Standard Component Structure

```typescript
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { supabase } from '@/integrations/supabase/client';
import { useToast } from '@/hooks/use-toast';

export default function MyComponent() {
  const [state, setState] = useState('');
  const { toast } = useToast();

  const { data, isLoading } = useQuery({
    queryKey: ['my-data'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('table_name')
        .select('*');

      if (error) throw error;
      return data;
    },
  });

  if (isLoading) return <div>Loading...</div>;

  return (
    <div className="container max-w-4xl mx-auto py-8">
      <Card>
        <CardHeader>
          <CardTitle>Title</CardTitle>
        </CardHeader>
        <CardContent>
          {/* Content here */}
        </CardContent>
      </Card>
    </div>
  );
}
```

## React Query Hooks

### Data Fetching Pattern

```typescript
// src/hooks/useMyData.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';

export function useMyData() {
  return useQuery({
    queryKey: ['my-data'],
    queryFn: async () => {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) return [];

      const { data, error } = await supabase
        .from('table_name')
        .select('*')
        .eq('profile_id', user.id)
        .order('created_at', { ascending: false });

      if (error) throw error;
      return data;
    },
  });
}

export function useCreateData() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (payload: any) => {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) throw new Error('Not authenticated');

      const { data, error } = await supabase
        .from('table_name')
        .insert({ ...payload, profile_id: user.id })
        .select()
        .single();

      if (error) throw error;
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['my-data'] });
    },
  });
}
```

## Supabase Integration

### Authentication Check

```typescript
const { data: { user } } = await supabase.auth.getUser();
if (!user) throw new Error('Not authenticated');
```

### Database Queries

```typescript
// Select with filters
const { data, error } = await supabase
  .from('table_name')
  .select('*')
  .eq('status', 'active')
  .order('created_at', { ascending: false });

// Insert
const { data, error } = await supabase
  .from('table_name')
  .insert({ field: 'value' })
  .select()
  .single();

// Update
const { error } = await supabase
  .from('table_name')
  .update({ field: 'new_value' })
  .eq('id', itemId);

// Delete
const { error } = await supabase
  .from('table_name')
  .delete()
  .eq('id', itemId);
```

## Tailwind CSS Patterns

### Common Layouts

```tsx
{/* Container with max width */}
<div className="container max-w-6xl mx-auto py-8">

{/* Grid responsive */}
<div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">

{/* Flex spacing */}
<div className="flex items-center justify-between gap-4">

{/* Card grid */}
<div className="space-y-4">
  <Card>...</Card>
  <Card>...</Card>
</div>
```

## shadcn/ui Components

### Button Variants

```tsx
<Button>Primary</Button>
<Button variant="outline">Outline</Button>
<Button variant="ghost">Ghost</Button>
<Button variant="destructive">Delete</Button>
<Button size="sm">Small</Button>
<Button size="lg">Large</Button>
```

### Form Components

```tsx
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

<div className="space-y-4">
  <div>
    <Label>Name</Label>
    <Input placeholder="Enter name" value={name} onChange={(e) => setName(e.target.value)} />
  </div>

  <div>
    <Label>Description</Label>
    <Textarea placeholder="Enter description" />
  </div>

  <div>
    <Label>Category</Label>
    <Select value={category} onValueChange={setCategory}>
      <SelectTrigger>
        <SelectValue placeholder="Select category" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="option1">Option 1</SelectItem>
        <SelectItem value="option2">Option 2</SelectItem>
      </SelectContent>
    </Select>
  </div>
</div>
```

## Toast Notifications

```typescript
import { useToast } from '@/hooks/use-toast';

const { toast } = useToast();

// Success
toast({
  title: 'Success!',
  description: 'Item created successfully',
});

// Error
toast({
  title: 'Error',
  description: 'Failed to create item',
  variant: 'destructive',
});
```

## Performance Optimization

### Lazy Loading

```typescript
import { lazy, Suspense } from 'react';

const HeavyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <HeavyComponent />
    </Suspense>
  );
}
```

### Memoization

```typescript
import { useMemo, useCallback } from 'react';

// Expensive computation
const expensiveValue = useMemo(() => {
  return items.filter(item => item.active).map(item => item.value);
}, [items]);

// Callback for child components
const handleClick = useCallback(() => {
  doSomething(id);
}, [id]);
```

## TypeScript Best Practices

### Type Interfaces

```typescript
interface User {
  id: string;
  email: string;
  full_name: string | null;
  created_at: string;
}

interface Job {
  id: string;
  title: string;
  company_name: string;
  skills: string[];
  is_active: boolean;
}
```

### Component Props

```typescript
interface MyComponentProps {
  title: string;
  items: Job[];
  onSelect?: (id: string) => void;
  className?: string;
}

export function MyComponent({ title, items, onSelect, className }: MyComponentProps) {
  // Component implementation
}
```

## Common Patterns

### Loading States

```tsx
if (isLoading) {
  return <div className="flex items-center justify-center py-8">Loading...</div>;
}

if (error) {
  return <div className="text-destructive">Error: {error.message}</div>;
}
```

### Empty States

```tsx
{items.length === 0 ? (
  <div className="text-center py-12 text-muted-foreground">
    <p>No items found</p>
  </div>
) : (
  <div className="grid gap-4">
    {items.map(item => <ItemCard key={item.id} item={item} />)}
  </div>
)}
```

### Responsive Design

```tsx
{/* Mobile-first responsive */}
<div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
  {/* Cards */}
</div>

{/* Hide on mobile */}
<div className="hidden md:block">Desktop only content</div>

{/* Show on mobile only */}
<div className="md:hidden">Mobile only content</div>
```

## Icons with Lucide

```tsx
import { Star, Heart, Trash2, Edit, Plus } from 'lucide-react';

<Button>
  <Plus className="h-4 w-4 mr-2" />
  Add Item
</Button>

<Star className="h-5 w-5 text-yellow-500" />
```

## File Structure

```
src/
├── components/       # Reusable UI components
│   ├── ui/          # shadcn/ui components (auto-generated)
│   └── *.tsx        # Custom components
├── pages/           # Route components
├── hooks/           # Custom React hooks (useMyData, etc.)
├── lib/             # Utilities, helpers
├── types/           # TypeScript types/interfaces
└── integrations/    # Supabase client
```

## Quick Checklist

Before creating a component:
- [ ] Use existing shadcn/ui components
- [ ] Create custom hook for data fetching
- [ ] Add loading and error states
- [ ] Use TypeScript interfaces
- [ ] Apply Tailwind responsive classes
- [ ] Add toast notifications for actions
- [ ] Test on mobile viewport
- [ ] Verify authentication checks

## Common Mistakes to Avoid

1. **Don't use user_id** - Always use `profile_id` for foreign keys
2. **Don't skip error handling** - Always check `error` from Supabase
3. **Don't forget auth checks** - Verify user is authenticated
4. **Don't hardcode values** - Use env variables for URLs/keys
5. **Don't skip TypeScript** - Define proper interfaces
6. **Don't ignore RLS** - Ensure Row Level Security is enabled

## Reference

- shadcn/ui: https://ui.shadcn.com/
- Tailwind CSS: https://tailwindcss.com/docs
- React Query: https://tanstack.com/query/latest
- Lucide Icons: https://lucide.dev/
- Supabase: https://supabase.com/docs
