---
name: UI Interaction
description: This skill should be used when the user asks to "add client interactivity", "implement form validation", "add event handlers", "use client state", "add Zod validation", "implement React hooks", "add local state", "make component interactive", "add form with validation", "use React Hook Form", or needs guidance on client-side events, form handling, optimistic updates, or when to add "use client" directive.
version: 0.1.0
---

# UI Interaction for Next.js Applications

## Overview

UI Interaction handles the client-side interactivity layer of Next.js applications. This skill covers adding client-side events, managing local state, implementing form validation with Zod, and using React Hook Form for complex forms.

**Key principles:**
- Only add "use client" when client-side APIs are actually needed
- Use Zod schemas for both client and server validation (single source of truth)
- Prefer Server Components by default; convert to Client Components only for interactivity
- Implement optimistic updates for responsive user experience

## Skill-scoped Context

**Official Documentation:**
- React Hooks: https://react.dev/reference/react/hooks
- Zod Validation: https://zod.dev/
- React Hook Form: https://react-hook-form.com/
- Next.js Client Components: https://nextjs.org/docs/app/building-your-application/rendering/client-components

## When to Add "use client"

Add the "use client" directive only when the component uses:

1. **Event handlers** - onClick, onChange, onSubmit, etc.
2. **React hooks** - useState, useEffect, useRef, useCallback, useMemo
3. **Browser APIs** - window, document, localStorage, navigator
4. **Third-party client libraries** - libraries that require browser context

**Pattern: Minimal Client Boundary**

Keep "use client" components as small as possible:

```tsx
// components/counter-button.tsx
"use client";

import { useState } from "react";

export function CounterButton() {
  const [count, setCount] = useState(0);
  return (
    <button onClick={() => setCount(c => c + 1)}>
      Count: {count}
    </button>
  );
}
```

```tsx
// app/page.tsx (Server Component - no "use client")
import { CounterButton } from "@/components/counter-button";

export default function Page() {
  // Server-side data fetching, no client JS here
  return (
    <main>
      <h1>Welcome</h1>
      <CounterButton /> {/* Client boundary starts here */}
    </main>
  );
}
```

## Workflow

### Step 1: Identify Interactive Elements

Analyze the UI to identify elements requiring client-side behavior:
- Form inputs with validation
- Buttons with click handlers
- Elements with hover/focus states
- Components with local state (toggles, dropdowns, modals)
- Elements requiring browser APIs

### Step 2: Add "use client" Directive

Add the directive at the top of the file, before any imports:

```tsx
"use client";

import { useState } from "react";
// ... rest of imports
```

### Step 3: Implement State Management

Use appropriate React hooks for state:

```tsx
"use client";

import { useState, useCallback } from "react";

export function ToggleButton({ initialState = false }: { initialState?: boolean }) {
  const [isOn, setIsOn] = useState(initialState);

  const toggle = useCallback(() => {
    setIsOn(prev => !prev);
  }, []);

  return (
    <button
      onClick={toggle}
      aria-pressed={isOn}
      className={isOn ? "bg-green-500" : "bg-gray-300"}
    >
      {isOn ? "On" : "Off"}
    </button>
  );
}
```

### Step 4: Add Zod Validation

Define Zod schemas for form validation:

```tsx
import { z } from "zod";

// Define schema once, use for client AND server validation
export const contactFormSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email address"),
  message: z.string().min(10, "Message must be at least 10 characters"),
});

export type ContactFormData = z.infer<typeof contactFormSchema>;
```

## Form Validation with Zod and React Hook Form

### Complete Form Example

```tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";

const formSchema = z.object({
  email: z.string().email("Please enter a valid email"),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain an uppercase letter")
    .regex(/[0-9]/, "Password must contain a number"),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});

type FormData = z.infer<typeof formSchema>;

export function SignUpForm({ onSubmit }: { onSubmit: (data: FormData) => Promise<void> }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormData>({
    resolver: zodResolver(formSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          {...register("email")}
          type="email"
          id="email"
          className="mt-1 block w-full rounded-md border-gray-300"
          aria-invalid={errors.email ? "true" : "false"}
        />
        {errors.email && (
          <p className="mt-1 text-sm text-red-600" role="alert">
            {errors.email.message}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          {...register("password")}
          type="password"
          id="password"
          className="mt-1 block w-full rounded-md border-gray-300"
          aria-invalid={errors.password ? "true" : "false"}
        />
        {errors.password && (
          <p className="mt-1 text-sm text-red-600" role="alert">
            {errors.password.message}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="confirmPassword" className="block text-sm font-medium">
          Confirm Password
        </label>
        <input
          {...register("confirmPassword")}
          type="password"
          id="confirmPassword"
          className="mt-1 block w-full rounded-md border-gray-300"
          aria-invalid={errors.confirmPassword ? "true" : "false"}
        />
        {errors.confirmPassword && (
          <p className="mt-1 text-sm text-red-600" role="alert">
            {errors.confirmPassword.message}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-md bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
      >
        {isSubmitting ? "Signing up..." : "Sign Up"}
      </button>
    </form>
  );
}
```

## Event Handler Patterns

### Click Handlers

```tsx
"use client";

import { useCallback } from "react";

export function DeleteButton({ itemId, onDelete }: {
  itemId: string;
  onDelete: (id: string) => Promise<void>;
}) {
  const handleDelete = useCallback(async () => {
    if (confirm("Are you sure you want to delete this item?")) {
      await onDelete(itemId);
    }
  }, [itemId, onDelete]);

  return (
    <button
      onClick={handleDelete}
      className="text-red-600 hover:text-red-800"
      aria-label="Delete item"
    >
      Delete
    </button>
  );
}
```

### Keyboard Events

```tsx
"use client";

import { useCallback, KeyboardEvent } from "react";

export function SearchInput({ onSearch }: { onSearch: (query: string) => void }) {
  const handleKeyDown = useCallback((e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      onSearch(e.currentTarget.value);
    }
  }, [onSearch]);

  return (
    <input
      type="search"
      placeholder="Search..."
      onKeyDown={handleKeyDown}
      className="rounded-md border px-4 py-2"
      aria-label="Search"
    />
  );
}
```

## Optimistic Updates Pattern

Provide immediate feedback while server action processes:

```tsx
"use client";

import { useOptimistic, useTransition } from "react";

interface Todo {
  id: string;
  text: string;
  completed: boolean;
}

export function TodoItem({
  todo,
  toggleAction
}: {
  todo: Todo;
  toggleAction: (id: string) => Promise<void>;
}) {
  const [isPending, startTransition] = useTransition();
  const [optimisticTodo, setOptimisticTodo] = useOptimistic(
    todo,
    (state, completed: boolean) => ({ ...state, completed })
  );

  const handleToggle = () => {
    startTransition(async () => {
      setOptimisticTodo(!optimisticTodo.completed);
      await toggleAction(todo.id);
    });
  };

  return (
    <div className={isPending ? "opacity-50" : ""}>
      <input
        type="checkbox"
        checked={optimisticTodo.completed}
        onChange={handleToggle}
        aria-label={`Mark "${todo.text}" as ${optimisticTodo.completed ? "incomplete" : "complete"}`}
      />
      <span className={optimisticTodo.completed ? "line-through" : ""}>
        {todo.text}
      </span>
    </div>
  );
}
```

## Local State Patterns

### Toggle State

```tsx
"use client";

import { useState, useCallback } from "react";

export function Accordion({ title, children }: {
  title: string;
  children: React.ReactNode;
}) {
  const [isOpen, setIsOpen] = useState(false);

  const toggle = useCallback(() => setIsOpen(prev => !prev), []);

  return (
    <div className="border rounded-md">
      <button
        onClick={toggle}
        aria-expanded={isOpen}
        className="w-full px-4 py-2 text-left font-medium"
      >
        {title}
        <span className="float-right">{isOpen ? "−" : "+"}</span>
      </button>
      {isOpen && (
        <div className="px-4 py-2 border-t">
          {children}
        </div>
      )}
    </div>
  );
}
```

### Controlled Input

```tsx
"use client";

import { useState, ChangeEvent, useCallback } from "react";

export function ControlledInput({
  initialValue = "",
  onChange
}: {
  initialValue?: string;
  onChange?: (value: string) => void;
}) {
  const [value, setValue] = useState(initialValue);

  const handleChange = useCallback((e: ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setValue(newValue);
    onChange?.(newValue);
  }, [onChange]);

  return (
    <input
      type="text"
      value={value}
      onChange={handleChange}
      className="rounded-md border px-4 py-2"
    />
  );
}
```

## Best Practices

**DO:**
- Keep "use client" components minimal and focused
- Define Zod schemas in shared files for client AND server use
- Use React Hook Form for complex forms with multiple fields
- Implement optimistic updates for better UX
- Add proper aria attributes for accessibility
- Use useCallback for stable function references passed to children

**DON'T:**
- Add "use client" to components that don't need it
- Duplicate validation logic between client and server
- Use client-side state for data that should come from the server
- Forget to handle loading and error states
- Skip accessibility attributes on interactive elements

## Quick Reference

### When to Use Each Hook

| Hook | Use Case |
|------|----------|
| useState | Local component state |
| useCallback | Memoize event handlers |
| useMemo | Expensive computations |
| useRef | DOM references, mutable values |
| useOptimistic | Optimistic UI updates |
| useTransition | Non-blocking state updates |

### Zod Common Validators

| Validator | Example |
|-----------|---------|
| string | `z.string().min(1).max(100)` |
| email | `z.string().email()` |
| number | `z.number().int().positive()` |
| enum | `z.enum(["a", "b", "c"])` |
| optional | `z.string().optional()` |
| nullable | `z.string().nullable()` |
| refine | `schema.refine(val => condition, "message")` |

## Implementation Workflow

To add interactivity to a component:

1. Identify which elements need client-side behavior
2. Extract interactive elements to separate "use client" component
3. Keep parent component as Server Component when possible
4. Define Zod schemas for any form validation
5. Implement React Hook Form for forms with multiple fields
6. Add event handlers with useCallback for stability
7. Implement optimistic updates for mutations
8. Add proper accessibility attributes
9. Test interactive behavior across devices
