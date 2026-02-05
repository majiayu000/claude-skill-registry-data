---
name: component-development
description: Create and modify React components following project patterns. Use when building UI components, forms, layouts, navigation, or implementing React hooks. Includes DaisyUI, Tailwind CSS, and lucide-react icons.
---

# Component Development

## Overview
This skill helps you create and modify React components following the project's established patterns and conventions. The project uses React 19, TypeScript, DaisyUI, Tailwind CSS, and lucide-react icons.

## Project Structure

### Component Organization
```
src/
├── app/
│   └── admin/
│       ├── components/          # Reusable admin components
│       │   ├── inputs/          # Form input components
│       │   ├── skeleton/        # Loading skeletons
│       │   ├── left-menu.tsx    # Navigation menu
│       │   ├── top-bar.tsx      # Top navigation bar
│       │   ├── menu-item.tsx    # Menu item component
│       │   └── my-breadcrumbs.tsx # Breadcrumb navigation
│       ├── blogs/               # Blog-related pages
│       ├── categories/          # Category-related pages
│       ├── layout.tsx           # Admin layout wrapper
│       ├── layoutContext.tsx    # Layout context
│       └── layoutMain.tsx       # Main layout component
├── auth/                        # Auth components
│   ├── AuthContext.tsx          # Auth context provider
│   └── ProtectedRoute.tsx       # Route protection
└── domains/                     # Domain models/types
```

## Technology Stack

### Core
- **React**: 19.1.x (latest)
- **TypeScript**: 5.9.x
- **React Router**: 7.9.x for routing

### UI Framework
- **DaisyUI**: 5.0.x - Component library
- **Tailwind CSS**: 4.0.x - Utility-first CSS
- **lucide-react**: 0.476.x - Icon library

### Form Components
- **Quill**: 2.0.x - Rich text editor
- Custom form components in `src/app/admin/components/inputs/`

## Component Patterns

### Functional Components with TypeScript
```typescript
import { useState } from 'react';
import type { ComponentProps } from 'react';

interface MyComponentProps {
  title: string;
  onSubmit: (data: FormData) => void;
  optional?: string;
}

export default function MyComponent({
  title,
  onSubmit,
  optional
}: MyComponentProps) {
  const [state, setState] = useState('');

  return (
    <div className="container">
      <h1>{title}</h1>
      {/* Component JSX */}
    </div>
  );
}
```

### Named Exports for Utilities
```typescript
// For utility functions and constants
export function helperFunction() { }
export const CONSTANT_VALUE = 'value';

// Default export for main component
export default function MainComponent() { }
```

## DaisyUI Components

### Common DaisyUI Classes

#### Buttons
```tsx
<button className="btn btn-primary">Primary</button>
<button className="btn btn-secondary">Secondary</button>
<button className="btn btn-accent">Accent</button>
<button className="btn btn-ghost">Ghost</button>
<button className="btn btn-link">Link</button>
```

#### Forms
```tsx
<label className="form-control w-full">
  <div className="label">
    <span className="label-text">Label</span>
  </div>
  <input
    type="text"
    className="input input-bordered w-full"
    placeholder="Type here"
  />
</label>

<select className="select select-bordered w-full">
  <option disabled selected>Pick one</option>
  <option>Option 1</option>
</select>

<textarea
  className="textarea textarea-bordered w-full"
  placeholder="Enter text"
></textarea>
```

#### Cards
```tsx
<div className="card bg-base-100 shadow-xl">
  <div className="card-body">
    <h2 className="card-title">Card Title</h2>
    <p>Card content goes here</p>
    <div className="card-actions justify-end">
      <button className="btn btn-primary">Action</button>
    </div>
  </div>
</div>
```

#### Navigation
```tsx
<div className="navbar bg-base-100">
  <div className="navbar-start">
    <a className="btn btn-ghost text-xl">Brand</a>
  </div>
  <div className="navbar-center">
    {/* Menu items */}
  </div>
  <div className="navbar-end">
    <button className="btn">Button</button>
  </div>
</div>
```

#### Tables
```tsx
<div className="overflow-x-auto">
  <table className="table">
    <thead>
      <tr>
        <th>Name</th>
        <th>Job</th>
        <th>Company</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Cy Ganderton</td>
        <td>Quality Control Specialist</td>
        <td>Littel, Schaden and Vandervort</td>
      </tr>
    </tbody>
  </table>
</div>
```

#### Loading States
```tsx
<span className="loading loading-spinner loading-xs"></span>
<span className="loading loading-spinner loading-sm"></span>
<span className="loading loading-spinner loading-md"></span>
<span className="loading loading-spinner loading-lg"></span>
```

## Tailwind CSS Utilities

### Layout
```tsx
// Flexbox
<div className="flex flex-col gap-4">
<div className="flex items-center justify-between">

// Grid
<div className="grid grid-cols-3 gap-4">
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">

// Spacing
<div className="p-4 m-4">        // padding, margin
<div className="px-4 py-2">      // horizontal, vertical padding
<div className="space-y-4">      // gap between children
```

### Responsive Design
```tsx
// Mobile-first approach
<div className="w-full md:w-1/2 lg:w-1/3">
<div className="text-sm md:text-base lg:text-lg">
<div className="hidden md:block">  // Hide on mobile
```

## Icons with lucide-react

### Available Icons
```tsx
import {
  Info, ImagePlus, Tag, BookOpen, Save, FileText,
  Home, Settings, Users, LogOut, Menu, X,
  Edit, Trash, Plus, Check, AlertCircle
} from 'lucide-react';

// Usage
<Save className="w-4 h-4" />
<Edit className="w-5 h-5 text-blue-500" />
<Trash className="w-6 h-6 hover:text-red-500" />
```

### Icon Sizes
- `w-4 h-4` - Small (16px)
- `w-5 h-5` - Medium (20px)
- `w-6 h-6` - Large (24px)
- `w-8 h-8` - Extra Large (32px)

## React Hooks

### useState
```typescript
const [count, setCount] = useState(0);
const [user, setUser] = useState<User | null>(null);
```

### useEffect
```typescript
useEffect(() => {
  // Effect logic
  return () => {
    // Cleanup
  };
}, [dependencies]);
```

### Custom Hooks
```typescript
function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
```

### useNavigate (React Router)
```typescript
import { useNavigate } from 'react-router-dom';

function MyComponent() {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate('/admin/blogs');
  };
}
```

## Form Handling

### Controlled Inputs
```typescript
const [value, setValue] = useState('');

<input
  type="text"
  value={value}
  onChange={(e) => setValue(e.target.value)}
  className="input input-bordered"
/>
```

### Form Submission
```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  try {
    // Submit logic
  } catch (error) {
    console.error('Submit error:', error);
  }
};

<form onSubmit={handleSubmit}>
  {/* Form fields */}
  <button type="submit" className="btn btn-primary">
    Submit
  </button>
</form>
```

## Loading States

### Conditional Rendering
```typescript
if (loading) {
  return <LoadingSkeleton />;
}

if (error) {
  return <ErrorMessage error={error} />;
}

return <Content data={data} />;
```

### Skeleton Components
Use skeletons from `src/app/admin/components/skeleton/`:
```typescript
import TableSkeleton from '../components/skeleton/table-skeleton';

{loading ? <TableSkeleton /> : <DataTable data={data} />}
```

## Context Providers

### Creating Context
```typescript
import { createContext, useContext, useState } from 'react';

interface MyContextType {
  value: string;
  setValue: (value: string) => void;
}

const MyContext = createContext<MyContextType | undefined>(undefined);

export function MyProvider({ children }: { children: React.ReactNode }) {
  const [value, setValue] = useState('');

  return (
    <MyContext.Provider value={{ value, setValue }}>
      {children}
    </MyContext.Provider>
  );
}

export function useMyContext() {
  const context = useContext(MyContext);
  if (!context) {
    throw new Error('useMyContext must be used within MyProvider');
  }
  return context;
}
```

## Routing

### Route Configuration
```typescript
import { BrowserRouter, Routes, Route } from 'react-router-dom';

<BrowserRouter>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/admin" element={<AdminLayout />}>
      <Route path="blogs" element={<BlogList />} />
      <Route path="blogs/create" element={<BlogCreate />} />
      <Route path="blogs/edit/:id" element={<BlogEdit />} />
    </Route>
  </Routes>
</BrowserRouter>
```

### Protected Routes
```typescript
<ProtectedRoute>
  <AdminDashboard />
</ProtectedRoute>
```

## TypeScript Best Practices

### Props Types
```typescript
// Interface for props
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

// Or use type
type ButtonProps = {
  label: string;
  onClick: () => void;
}
```

### Event Types
```typescript
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => { };
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => { };
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => { };
```

### Children Props
```typescript
interface LayoutProps {
  children: React.ReactNode;
}
```

## Common Patterns

### List Rendering
```typescript
{items.map((item) => (
  <div key={item.id}>
    {item.name}
  </div>
))}
```

### Conditional Classes
```typescript
<button
  className={`btn ${isActive ? 'btn-primary' : 'btn-ghost'}`}
>
  Button
</button>

// Or use template literals
className={`btn ${loading ? 'loading' : ''}`}
```

### Error Boundaries
```typescript
try {
  // Risky operation
} catch (error) {
  console.error('Error:', error);
  // Show error to user
}
```

## Best Practices

1. **Use TypeScript types** for all props and state
2. **Destructure props** in function parameters
3. **Use meaningful variable names**
4. **Keep components small and focused**
5. **Extract reusable logic** into custom hooks
6. **Use DaisyUI classes** instead of custom CSS
7. **Follow Tailwind conventions** for styling
8. **Add loading states** for async operations
9. **Handle errors gracefully**
10. **Use path aliases** (`@/`) for imports

## Component Checklist

When creating a new component:

- [ ] Define TypeScript interface for props
- [ ] Use functional component syntax
- [ ] Add proper imports (React, icons, utilities)
- [ ] Implement loading states if fetching data
- [ ] Add error handling
- [ ] Use DaisyUI components where possible
- [ ] Apply responsive Tailwind classes
- [ ] Export component as default
- [ ] Add JSDoc comments for complex components
- [ ] Test component in browser

## Example Component

```typescript
import { useState, useEffect } from 'react';
import { Save, AlertCircle } from 'lucide-react';
import { useAuth } from '@/auth/AuthContext';
import { getApiUrl, authenticatedFetch } from '@/config/api.config';

interface BlogFormProps {
  id?: string;
  onSuccess?: () => void;
}

export default function BlogForm({ id, onSuccess }: BlogFormProps) {
  const { token } = useAuth();
  const [title, setTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      fetchBlog();
    }
  }, [id]);

  const fetchBlog = async () => {
    setLoading(true);
    try {
      const response = await authenticatedFetch(
        getApiUrl(`/posts/${id}`),
        token
      );
      if (response.ok) {
        const { data } = await response.json();
        setTitle(data.title);
      }
    } catch (err) {
      setError('Failed to load blog');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await authenticatedFetch(
        getApiUrl('/posts'),
        token,
        {
          method: 'POST',
          body: JSON.stringify({ title }),
        }
      );

      if (response.ok) {
        onSuccess?.();
      } else {
        setError('Failed to save blog');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  if (loading && id) {
    return (
      <div className="flex justify-center p-8">
        <span className="loading loading-spinner loading-lg"></span>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="alert alert-error">
          <AlertCircle className="w-5 h-5" />
          <span>{error}</span>
        </div>
      )}

      <label className="form-control w-full">
        <div className="label">
          <span className="label-text">Blog Title</span>
        </div>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="input input-bordered w-full"
          placeholder="Enter title"
          required
        />
      </label>

      <button
        type="submit"
        className={`btn btn-primary ${loading ? 'loading' : ''}`}
        disabled={loading}
      >
        {!loading && <Save className="w-4 h-4" />}
        {loading ? 'Saving...' : 'Save Blog'}
      </button>
    </form>
  );
}
```

This example demonstrates:
- TypeScript props interface
- State management with useState
- Data fetching with useEffect
- Form handling
- Loading states
- Error handling
- DaisyUI components
- Tailwind CSS classes
- lucide-react icons
- Authentication integration

## Form Handling with react-hook-form + zod

The project uses react-hook-form for form state management and zod for schema validation.

### Setup
```typescript
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

// Define schema
const formSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200),
  email: z.string().email('Invalid email'),
  published: z.boolean().default(false),
  tags: z.array(z.string()).default([]),
});

type FormData = z.infer<typeof formSchema>;
```

### Basic Form Component
```typescript
export default function MyForm() {
  const {
    register,
    handleSubmit,
    control,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      title: '',
      email: '',
      published: false,
      tags: [],
    },
  });

  const onSubmit = async (data: FormData) => {
    try {
      // Submit logic
      toast.success('Saved successfully');
    } catch (error) {
      toast.error('Failed to save');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* Simple input with register */}
      <input
        {...register('title')}
        className={`input input-bordered ${errors.title ? 'input-error' : ''}`}
      />
      {errors.title && (
        <span className="text-error">{errors.title.message}</span>
      )}

      {/* Complex input with Controller */}
      <Controller
        name="published"
        control={control}
        render={({ field }) => (
          <input
            type="checkbox"
            checked={field.value}
            onChange={field.onChange}
          />
        )}
      />

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Saving...' : 'Save'}
      </button>
    </form>
  );
}
```

### useFieldArray for Dynamic Lists
```typescript
import { useFieldArray } from 'react-hook-form';

const { fields, append, remove } = useFieldArray({
  control,
  name: 'translations',
});

// Render dynamic fields
{fields.map((field, index) => (
  <div key={field.id}>
    <input {...register(`translations.${index}.value`)} />
    <button onClick={() => remove(index)}>Remove</button>
  </div>
))}
<button onClick={() => append({ value: '' })}>Add</button>
```

### Zod Schema Patterns
```typescript
// Location: src/schemas/

// Basic string validation
title: z.string().min(1, 'Required').max(200, 'Too long')

// Enum validation
categoryType: z.nativeEnum(CategoryTypeEnum)

// Optional with default
published: z.boolean().default(false)

// Array validation
tags: z.array(z.string()).default([])

// Nested object
translation: z.object({
  id: z.string().optional(),
  languageCode: z.string().min(2),
  displayName: z.string().min(1),
})
```

## Toast Notifications with Sonner

The project uses sonner for toast notifications.

### Basic Usage
```typescript
import { toast } from 'sonner';

// Success
toast.success('Operation completed successfully');

// Error
toast.error('Something went wrong');

// Info
toast.info('Here is some information');

// Warning
toast.warning('Please check your input');
```

### With Options
```typescript
toast.success('Saved!', {
  duration: 5000,           // 5 seconds
  description: 'Your changes have been saved',
});

toast.error('Failed to save', {
  duration: Infinity,       // Won't auto-dismiss
  action: {
    label: 'Retry',
    onClick: () => handleRetry(),
  },
});
```

### Promise Toast
```typescript
toast.promise(saveData(), {
  loading: 'Saving...',
  success: 'Data saved successfully',
  error: 'Failed to save data',
});
```

### Custom Toast
```typescript
toast.custom((t) => (
  <div className="bg-base-100 p-4 rounded-lg shadow-lg">
    <h3>Custom Toast</h3>
    <button onClick={() => toast.dismiss(t)}>Close</button>
  </div>
));
```

## DaisyUI v5 CSS Variables

DaisyUI v5 uses new CSS variable naming. Use these when writing custom CSS:

### Color Variables
```css
/* Old DaisyUI v4 */
oklch(var(--p))           /* Primary */
oklch(var(--b1))          /* Base 100 */
oklch(var(--bc))          /* Base content */

/* New DaisyUI v5 */
var(--color-primary)      /* Primary */
var(--color-base-100)     /* Base 100 */
var(--color-base-content) /* Base content */
```

### Available Color Variables
```css
/* Base colors */
--color-base-100
--color-base-200
--color-base-300
--color-base-content

/* Semantic colors */
--color-primary
--color-primary-content
--color-secondary
--color-secondary-content
--color-accent
--color-accent-content
--color-neutral
--color-neutral-content

/* State colors */
--color-info
--color-success
--color-warning
--color-error
```

### Using with Opacity (color-mix)
```css
/* 20% opacity primary color */
background-color: color-mix(in oklch, var(--color-primary) 20%, transparent);

/* 50% opacity base content */
color: color-mix(in oklch, var(--color-base-content) 50%, transparent);
```

### Theme Configuration
```css
/* In App.css */
@plugin 'daisyui' {
  themes: emerald --default, dark;
}
```

```typescript
/* In rsbuild.config.ts */
html: {
  htmlAttrs: {
    'data-theme': 'emerald',
  },
},
```
