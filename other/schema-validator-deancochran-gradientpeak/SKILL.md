---
name: schema-validator
description: Creates and validates Zod schemas for data structures, ensuring type safety and runtime validation.
---

# Schema Validator Skill

## When to Use

- User needs to create a new data schema
- User wants to add validation to forms
- User needs to validate API inputs
- User asks to update existing schemas

## What This Skill Does

1. Creates Zod schemas with proper validation
2. Infers TypeScript types from schemas
3. Adds custom validation rules
4. Implements refined schemas with dependencies
5. Creates form-specific sub-schemas

## Basic Schema Pattern

```typescript
import { z } from "zod";

export const activitySchema = z
  .object({
    id: z.string().uuid(),
    name: z.string().min(1, "Name is required"),
    type: z.enum(["run", "bike", "swim", "other"]),
    distance: z.number().positive().optional(),
    duration: z.number().int().positive("Duration must be positive"),
    startTime: z.date(),
    endTime: z.date(),
  })
  .refine((data) => data.endTime > data.startTime, {
    message: "End time must be after start time",
    path: ["endTime"],
  });

export type Activity = z.infer<typeof activitySchema>;
```

## Form Schema Pattern

```typescript
export const createActivitySchema = activitySchema
  .omit({
    id: true,
  })
  .extend({
    // Form-specific fields
    notes: z.string().max(500).optional(),
    isPrivate: z.boolean().default(false),
  });

export type CreateActivityInput = z.infer<typeof createActivitySchema>;
```

## Validation in Forms

```typescript
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { createActivitySchema } from "@repo/core/schemas";

export function useCreateActivityForm() {
  const form = useForm({
    resolver: zodResolver(createActivitySchema),
    defaultValues: {
      name: "",
      type: "run",
      distance: undefined,
      duration: 0,
      startTime: new Date(),
      endTime: new Date(),
      notes: "",
      isPrivate: false,
    },
  });

  return form;
}
```

## API Input Validation

```typescript
export const activityListInput = z.object({
  limit: z.number().min(1).max(100).default(20),
  offset: z.number().min(0).default(0),
  type: z.enum(["run", "bike", "swim", "other"]).optional(),
  search: z.string().optional(),
});
```

## Custom Validation

```typescript
export const profileSchema = z
  .object({
    name: z.string().min(1).max(100),
    email: z.string().email(),
    ftp: z.number().min(50).max(500).optional(),
  })
  .refine(
    (data) => {
      if (data.email.includes("+")) {
        return data.name.length > 5;
      }
      return true;
    },
    {
      message: "Name must be longer for email aliases",
      path: ["name"],
    },
  );
```
