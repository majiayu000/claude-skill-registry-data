---
name: Frontend Component Builder
description: Generate and refactor React + TypeScript components with Tailwind CSS for Medellin Spark. Use when building new UI components, creating dashboards, forms, cards, or wizards. Automatically includes accessibility, responsive design, and Vite-compatible code with optional tests.
---

# Frontend Component Builder

Automates creation of production-ready React components following Medellin Spark conventions.

## Quick Start

### Generate Component

```
Create component: EventCard
Props: title (string), date (string), imageUrl (string)
Purpose: Display event details with date and image
```

### Refactor Component

```
Refactor src/components/UserCard.tsx to use Grid layout instead of Flex
```

### Add Tests

```
Generate Vitest tests for src/components/Dashboard.tsx
```

## Component Generation

### Standard Component Template

```typescript
/**
 * ComponentName - Brief description
 *
 * @example
 * <ComponentName prop1="value" prop2={data} />
 */

import { FC } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface ComponentNameProps {
  prop1: string;
  prop2?: string;
  className?: string;
}

export const ComponentName: FC<ComponentNameProps> = ({
  prop1,
  prop2,
  className = '',
}) => {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>{prop1}</CardTitle>
      </CardHeader>
      <CardContent>
        {/* Component content */}
      </CardContent>
    </Card>
  );
};
```

### File Location Rules

```
src/components/         # Reusable components
src/components/ui/      # shadcn/ui components (don't modify)
src/pages/              # Page-level components (routes)
src/components/[feature]/ # Feature-specific components
```

Example:
- Reusable card → `src/components/EventCard.tsx`
- Dashboard widget → `src/components/dashboard/StatsWidget.tsx`
- Page component → `src/pages/Events.tsx`

## Props Interface Patterns

### Basic Props

```typescript
interface ComponentProps {
  title: string;
  description?: string;
  className?: string;
  children?: React.ReactNode;
}
```

### Data Props

```typescript
interface UserCardProps {
  user: {
    id: string;
    name: string;
    email: string;
    avatar?: string;
  };
  onEdit?: (id: string) => void;
  onDelete?: (id: string) => void;
}
```

### Array Props

```typescript
interface ListProps {
  items: Array<{
    id: string;
    title: string;
    status: 'active' | 'pending' | 'complete';
  }>;
  onItemClick?: (id: string) => void;
}
```

## Tailwind CSS Conventions

### Responsive Design (Mobile-First)

```tsx
{/* Stack on mobile, 2 cols on tablet, 3 cols on desktop */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

{/* Hide on mobile */}
<div className="hidden md:block">

{/* Full width on mobile, auto on desktop */}
<Button className="w-full md:w-auto">
```

### Standard Spacing

```tsx
{/* Container padding */}
className="container max-w-6xl mx-auto py-8"

{/* Section spacing */}
className="space-y-6"

{/* Item spacing */}
className="flex gap-4 items-center"

{/* Card spacing */}
className="p-6 rounded-lg"
```

### Color Classes

```tsx
{/* Text colors */}
className="text-foreground"        // Default text
className="text-muted-foreground"  // Secondary text
className="text-destructive"       // Error text
className="text-primary"           // Brand color

{/* Background colors */}
className="bg-background"     // Default background
className="bg-muted"          // Subtle background
className="bg-primary"        // Brand background
className="bg-destructive"    // Error background
```

## Accessibility Requirements

### ARIA Labels

```tsx
{/* Icon-only buttons */}
<Button aria-label="Delete event" variant="ghost" size="icon">
  <Trash2 className="h-4 w-4" />
</Button>

{/* Form inputs */}
<Input
  id="email"
  type="email"
  aria-label="Email address"
  aria-required="true"
  aria-invalid={hasError}
  aria-describedby={hasError ? "email-error" : undefined}
/>
{hasError && (
  <p id="email-error" className="text-sm text-destructive">
    {errorMessage}
  </p>
)}
```

### Semantic HTML

```tsx
{/* Use semantic elements */}
<article>
  <header>
    <h1>Title</h1>
  </header>
  <section>
    <h2>Section Title</h2>
    {/* Content */}
  </section>
</article>

{/* Navigation */}
<nav aria-label="Main navigation">
  <ul>
    <li><a href="/">Home</a></li>
  </ul>
</nav>
```

### Keyboard Navigation

```tsx
{/* Focusable interactive elements */}
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  }}
  className="cursor-pointer focus:outline-none focus:ring-2 focus:ring-primary"
>
  Clickable content
</div>
```

## Component Patterns Library

### Card Component

```typescript
interface CardProps {
  title: string;
  description?: string;
  imageUrl?: string;
  footer?: React.ReactNode;
  onClick?: () => void;
}

export const CustomCard: FC<CardProps> = ({
  title,
  description,
  imageUrl,
  footer,
  onClick,
}) => {
  return (
    <Card
      className="cursor-pointer hover:shadow-lg transition-shadow"
      onClick={onClick}
    >
      {imageUrl && (
        <div className="aspect-video w-full overflow-hidden rounded-t-lg">
          <img
            src={imageUrl}
            alt={title}
            className="w-full h-full object-cover"
          />
        </div>
      )}
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && (
          <CardDescription>{description}</CardDescription>
        )}
      </CardHeader>
      {footer && (
        <CardContent className="pt-0">
          {footer}
        </CardContent>
      )}
    </Card>
  );
};
```

### Form Component

```typescript
interface FormFieldProps {
  label: string;
  name: string;
  type?: 'text' | 'email' | 'password' | 'textarea';
  required?: boolean;
  error?: string;
  value: string;
  onChange: (value: string) => void;
}

export const FormField: FC<FormFieldProps> = ({
  label,
  name,
  type = 'text',
  required = false,
  error,
  value,
  onChange,
}) => {
  const id = `field-${name}`;
  const errorId = `${id}-error`;

  return (
    <div className="space-y-2">
      <Label htmlFor={id}>
        {label}
        {required && <span className="text-destructive ml-1">*</span>}
      </Label>
      {type === 'textarea' ? (
        <Textarea
          id={id}
          name={name}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          aria-required={required}
          aria-invalid={!!error}
          aria-describedby={error ? errorId : undefined}
          className={error ? 'border-destructive' : ''}
        />
      ) : (
        <Input
          id={id}
          name={name}
          type={type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          aria-required={required}
          aria-invalid={!!error}
          aria-describedby={error ? errorId : undefined}
          className={error ? 'border-destructive' : ''}
        />
      )}
      {error && (
        <p id={errorId} className="text-sm text-destructive">
          {error}
        </p>
      )}
    </div>
  );
};
```

### List Component

```typescript
interface ListItemProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  keyExtractor: (item: T) => string;
  emptyMessage?: string;
  className?: string;
}

export function List<T>({
  items,
  renderItem,
  keyExtractor,
  emptyMessage = 'No items found',
  className = '',
}: ListItemProps<T>) {
  if (items.length === 0) {
    return (
      <div className="text-center py-12 text-muted-foreground">
        <p>{emptyMessage}</p>
      </div>
    );
  }

  return (
    <div className={`space-y-2 ${className}`}>
      {items.map((item, index) => (
        <div key={keyExtractor(item)}>
          {renderItem(item, index)}
        </div>
      ))}
    </div>
  );
}
```

### Modal/Dialog Component

```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  footer?: React.ReactNode;
}

export const Modal: FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  footer,
}) => {
  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
        </DialogHeader>
        <div className="py-4">
          {children}
        </div>
        {footer && (
          <DialogFooter>
            {footer}
          </DialogFooter>
        )}
      </DialogContent>
    </Dialog>
  );
};
```

## Testing with Vitest

### Component Test Template

```typescript
// ComponentName.test.tsx
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ComponentName } from './ComponentName';

describe('ComponentName', () => {
  it('renders with required props', () => {
    render(<ComponentName title="Test Title" />);
    expect(screen.getByText('Test Title')).toBeInTheDocument();
  });

  it('handles click events', () => {
    const handleClick = vi.fn();
    render(<ComponentName title="Test" onClick={handleClick} />);

    fireEvent.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('applies custom className', () => {
    const { container } = render(
      <ComponentName title="Test" className="custom-class" />
    );
    expect(container.firstChild).toHaveClass('custom-class');
  });

  it('renders children when provided', () => {
    render(
      <ComponentName title="Test">
        <span>Child content</span>
      </ComponentName>
    );
    expect(screen.getByText('Child content')).toBeInTheDocument();
  });
});
```

### Test with React Query

```typescript
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
});

describe('DataComponent', () => {
  it('fetches and displays data', async () => {
    const queryClient = createTestQueryClient();

    render(
      <QueryClientProvider client={queryClient}>
        <DataComponent />
      </QueryClientProvider>
    );

    expect(await screen.findByText('Expected Data')).toBeInTheDocument();
  });
});
```

## Code Generation Workflow

When generating a component:

1. **Analyze requirements**
   - Component type (card, form, list, etc.)
   - Required props
   - Interactive features
   - Data dependencies

2. **Create file structure**
   ```
   src/components/ComponentName.tsx
   src/components/ComponentName.test.tsx (if tests requested)
   ```

3. **Generate component**
   - TypeScript interface for props
   - Functional component with proper typing
   - Tailwind CSS classes (responsive)
   - ARIA attributes
   - Documentation comment

4. **Add imports**
   ```typescript
   import { FC } from 'react';
   import { Button } from '@/components/ui/button';
   import { Card, CardContent } from '@/components/ui/card';
   import { IconName } from 'lucide-react';
   ```

5. **Verify conventions**
   - Uses `FC<Props>` type
   - Includes `className?: string` prop
   - Mobile-first responsive design
   - Accessibility attributes
   - Proper semantic HTML

## Refactoring Guidelines

### When refactoring existing components:

1. **Read existing file** first to understand structure
2. **Preserve functionality** - don't break existing features
3. **Update imports** if adding new dependencies
4. **Maintain prop interface** or document breaking changes
5. **Add comments** for complex refactoring logic
6. **Run type check** to verify TypeScript compatibility

### Common refactoring requests:

- Convert class component → functional component
- Add TypeScript types to JavaScript component
- Extract reusable logic into custom hook
- Split large component into smaller components
- Add responsive design breakpoints
- Improve accessibility
- Optimize performance with memoization

## Project-Specific Rules

### Import Paths

```typescript
// ✅ Correct - Use @ alias
import { Button } from '@/components/ui/button';
import { supabase } from '@/integrations/supabase/client';
import { useToast } from '@/hooks/use-toast';

// ❌ Incorrect - Avoid relative imports for shared code
import { Button } from '../../ui/button';
```

### Database Integration

```typescript
// Always use profile_id, not user_id
const { data: { user } } = await supabase.auth.getUser();

const { data } = await supabase
  .from('table_name')
  .select('*')
  .eq('profile_id', user.id);  // ✅ profile_id
```

### State Management

```typescript
// Use React Query for server state
import { useQuery } from '@tanstack/react-query';

const { data, isLoading } = useQuery({
  queryKey: ['key'],
  queryFn: fetchFunction,
});

// Use useState for UI state
import { useState } from 'react';
const [isOpen, setIsOpen] = useState(false);
```

## Component Checklist

Before completing component generation:

- [ ] TypeScript interface defined
- [ ] Props include `className?: string`
- [ ] Responsive design applied (sm:, md:, lg:)
- [ ] ARIA labels on interactive elements
- [ ] Loading and error states (if data fetching)
- [ ] Empty state (if displaying lists)
- [ ] Semantic HTML elements
- [ ] Keyboard navigation support
- [ ] Documentation comment at top
- [ ] Imports use @ path alias
- [ ] File saved in correct directory

## Example Generations

### Example 1: Event Card

**Request**: "Create EventCard component with title, date, imageUrl, onClick"

**Output**: `src/components/EventCard.tsx`

```typescript
/**
 * EventCard - Display event details with image, title, and date
 *
 * @example
 * <EventCard
 *   title="Tech Conference 2025"
 *   date="2025-03-15"
 *   imageUrl="/events/conference.jpg"
 *   onClick={() => navigate('/event/123')}
 * />
 */

import { FC } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Calendar } from 'lucide-react';

interface EventCardProps {
  title: string;
  date: string;
  imageUrl?: string;
  onClick?: () => void;
  className?: string;
}

export const EventCard: FC<EventCardProps> = ({
  title,
  date,
  imageUrl,
  onClick,
  className = '',
}) => {
  const formattedDate = new Date(date).toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  });

  return (
    <Card
      className={`cursor-pointer hover:shadow-lg transition-all hover:-translate-y-1 ${className}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if ((e.key === 'Enter' || e.key === ' ') && onClick) {
          e.preventDefault();
          onClick();
        }
      }}
    >
      {imageUrl && (
        <div className="aspect-video w-full overflow-hidden rounded-t-lg">
          <img
            src={imageUrl}
            alt={title}
            className="w-full h-full object-cover"
          />
        </div>
      )}
      <CardHeader>
        <CardTitle className="line-clamp-2">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Calendar className="h-4 w-4" />
          <time dateTime={date}>{formattedDate}</time>
        </div>
      </CardContent>
    </Card>
  );
};
```

### Example 2: Dashboard Stats Widget

**Request**: "Create StatsWidget for dashboard with label, value, icon, trend"

**Output**: `src/components/dashboard/StatsWidget.tsx`

```typescript
/**
 * StatsWidget - Dashboard statistics card with trend indicator
 *
 * @example
 * <StatsWidget
 *   label="Total Users"
 *   value="1,234"
 *   icon={Users}
 *   trend={{ value: 12.5, direction: 'up' }}
 * />
 */

import { FC } from 'react';
import { LucideIcon, TrendingUp, TrendingDown } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface StatsWidgetProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  trend?: {
    value: number;
    direction: 'up' | 'down';
  };
  className?: string;
}

export const StatsWidget: FC<StatsWidgetProps> = ({
  label,
  value,
  icon: Icon,
  trend,
  className = '',
}) => {
  return (
    <Card className={className}>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {label}
        </CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" aria-hidden="true" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {trend && (
          <p
            className={`text-xs flex items-center gap-1 mt-1 ${
              trend.direction === 'up'
                ? 'text-green-600'
                : 'text-red-600'
            }`}
          >
            {trend.direction === 'up' ? (
              <TrendingUp className="h-3 w-3" />
            ) : (
              <TrendingDown className="h-3 w-3" />
            )}
            <span>{Math.abs(trend.value)}% from last month</span>
          </p>
        )}
      </CardContent>
    </Card>
  );
};
```

## Quick Commands

```bash
# Generate component
"Create [ComponentName] component with [props]"

# Add tests
"Generate tests for [ComponentName]"

# Refactor
"Refactor [ComponentName] to [changes]"

# Add feature
"Add [feature] to [ComponentName]"

# Fix accessibility
"Improve accessibility for [ComponentName]"
```

## Common Imports Reference

```typescript
// React
import { FC, useState, useEffect, useCallback, useMemo } from 'react';

// React Query
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

// Supabase
import { supabase } from '@/integrations/supabase/client';

// UI Components
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';

// Icons
import { Plus, Edit, Trash2, Star, Heart } from 'lucide-react';

// Hooks
import { useToast } from '@/hooks/use-toast';
```
