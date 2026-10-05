---
name: forms
description: Form validation, multi-step forms, React Hook Form with Zod, server actions, and accessible form patterns
layer: domain
category: frontend
triggers:
  - "form"
  - "form validation"
  - "multi-step form"
  - "react hook form"
  - "zod schema"
  - "form builder"
  - "input validation"
inputs:
  - requirements: Form fields, validation rules, submission behavior
  - framework: React Hook Form | Formik | native (optional, defaults to RHF)
  - validation: Zod | Yup | native (optional, defaults to Zod)
  - features: Multi-step, file upload, conditional fields, server validation
outputs:
  - form_component: Complete form implementation with validation
  - schema: Zod/Yup validation schema
  - types: TypeScript types inferred from schema
  - server_action: Server-side validation and submission handler
linksTo:
  - react
  - nextjs
  - tailwindcss
  - ui-ux-pro
  - api-designer
linkedFrom:
  - cook
  - react
  - nextjs
preferredNextSkills:
  - react
  - api-designer
fallbackSkills:
  - ui-ux-pro
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# Forms Skill

## Purpose

Build accessible, validated, performant forms using React Hook Form and Zod. This skill covers single-page and multi-step forms, client-side and server-side validation, file uploads, dynamic/conditional fields, and optimistic form submissions. Forms are the primary way users input data -- they must be correct, accessible, and pleasant to use.

## Key Concepts

### Form Architecture

```
CLIENT VALIDATION (fast feedback):
  Zod schema validates on change/blur
  React Hook Form manages state and re-renders
  Errors displayed inline next to fields

SERVER VALIDATION (source of truth):
  Server action or API route validates again
  Business logic validation (uniqueness, permissions)
  Returns field-level errors for display

PRINCIPLE: Validate on client for UX, validate on server for security.
Never trust client-side validation alone.
```

### Zod Schema Design

```typescript
import { z } from 'zod';

// User registration schema
export const registerSchema = z.object({
  email: z
    .string()
    .min(1, 'Email is required')
    .email('Please enter a valid email address'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain an uppercase letter')
    .regex(/[0-9]/, 'Password must contain a number'),
  confirmPassword: z.string(),
  name: z
    .string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name must be under 100 characters'),
  agreeToTerms: z.literal(true, {
    errorMap: () => ({ message: 'You must agree to the terms' }),
  }),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

// Infer TypeScript type from schema
export type RegisterInput = z.infer<typeof registerSchema>;
```

## Patterns

### Pattern 1: Basic Form with React Hook Form + Zod

```typescript
'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { registerSchema, type RegisterInput } from '@/lib/schemas';

export function RegisterForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterInput>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
      name: '',
    },
  });

  async function onSubmit(data: RegisterInput) {
    const result = await registerUser(data);
    if (!result.ok) {
      // Handle server-side errors
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-6">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
          className="mt-1 w-full px-4 py-3 rounded-lg border transition-all duration-200
                     focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500"
          {...register('email')}
        />
        {errors.email && (
          <p id="email-error" role="alert" className="mt-1 text-sm text-red-600">
            {errors.email.message}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full px-6 py-4 min-h-[2.625rem] text-base font-medium rounded-lg
                   bg-blue-600 text-white hover:bg-blue-700
                   focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-blue-500
                   disabled:opacity-50 disabled:cursor-not-allowed
                   transition-all duration-200 motion-reduce:transition-none"
      >
        {isSubmitting ? 'Creating account...' : 'Create account'}
      </button>
    </form>
  );
}
```

### Pattern 2: Multi-Step Form

```typescript
'use client';

import { useState } from 'react';
import { useForm, FormProvider } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

// Step schemas
const step1Schema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
});

const step2Schema = z.object({
  company: z.string().min(1),
  role: z.string().min(1),
});

const step3Schema = z.object({
  plan: z.enum(['free', 'pro', 'enterprise']),
});

const fullSchema = step1Schema.merge(step2Schema).merge(step3Schema);
type FormData = z.infer<typeof fullSchema>;

const STEPS = [
  { schema: step1Schema, title: 'Account' },
  { schema: step2Schema, title: 'Company' },
  { schema: step3Schema, title: 'Plan' },
];

export function OnboardingForm() {
  const [currentStep, setCurrentStep] = useState(0);
  const methods = useForm<FormData>({
    resolver: zodResolver(STEPS[currentStep].schema),
    mode: 'onBlur',
  });

  async function handleNext() {
    const isValid = await methods.trigger();
    if (isValid && currentStep < STEPS.length - 1) {
      setCurrentStep((s) => s + 1);
    }
  }

  function handleBack() {
    setCurrentStep((s) => Math.max(0, s - 1));
  }

  async function onSubmit(data: FormData) {
    await submitOnboarding(data);
  }

  return (
    <FormProvider {...methods}>
      {/* Step indicator */}
      <nav aria-label="Progress">
        <ol className="flex gap-4">
          {STEPS.map((step, i) => (
            <li key={step.title} className={i <= currentStep ? 'text-blue-600' : 'text-gray-400'}>
              {step.title}
            </li>
          ))}
        </ol>
      </nav>

      <form onSubmit={methods.handleSubmit(onSubmit)}>
        {/* Render current step fields */}
        {currentStep === 0 && <Step1Fields />}
        {currentStep === 1 && <Step2Fields />}
        {currentStep === 2 && <Step3Fields />}

        <div className="flex gap-4 mt-8">
          {currentStep > 0 && (
            <button type="button" onClick={handleBack}>Back</button>
          )}
          {currentStep < STEPS.length - 1 ? (
            <button type="button" onClick={handleNext}>Next</button>
          ) : (
            <button type="submit">Submit</button>
          )}
        </div>
      </form>
    </FormProvider>
  );
}
```

### Pattern 3: Server Action Validation

```typescript
// app/actions/register.ts
'use server';

import { registerSchema } from '@/lib/schemas';

type ActionState = {
  success: boolean;
  errors?: Record<string, string[]>;
  message?: string;
};

export async function registerAction(
  prevState: ActionState,
  formData: FormData,
): Promise<ActionState> {
  const raw = Object.fromEntries(formData);
  const parsed = registerSchema.safeParse(raw);

  if (!parsed.success) {
    return {
      success: false,
      errors: parsed.error.flatten().fieldErrors,
    };
  }

  // Server-side business validation
  const existingUser = await db.user.findUnique({
    where: { email: parsed.data.email },
  });

  if (existingUser) {
    return {
      success: false,
      errors: { email: ['This email is already registered'] },
    };
  }

  await db.user.create({ data: parsed.data });
  return { success: true, message: 'Account created' };
}
```

## Accessibility Checklist

```
REQUIRED:
  - [ ] Every input has a visible <label> (not just placeholder)
  - [ ] Errors use role="alert" for screen reader announcement
  - [ ] aria-invalid={true} on fields with errors
  - [ ] aria-describedby links input to its error message
  - [ ] Form can be submitted with Enter key
  - [ ] Focus moves to first error field on submission failure
  - [ ] Required fields marked with aria-required="true"
  - [ ] Error messages are descriptive ("Email is required" not "Required")

RECOMMENDED:
  - [ ] Autocomplete attributes on common fields (email, name, password)
  - [ ] Input type matches content (email, tel, url, number)
  - [ ] Tab order is logical (top to bottom, left to right)
  - [ ] Loading state announced to screen readers
```

## Best Practices

1. **Validate on server, enhance on client** -- client validation is UX, server validation is security
2. **Show errors inline** -- next to the field, not in a banner at the top
3. **Validate on blur, not on every keystroke** -- let users finish typing before showing errors
4. **Preserve user input on error** -- never clear the form on validation failure
5. **Use Zod for shared schemas** -- same schema validates client and server
6. **Debounce async validation** -- uniqueness checks should not fire on every keystroke
7. **Disable submit during submission** -- prevent double-submits
8. **Show loading state** -- button text or spinner during async submission
9. **Use `autoComplete` attributes** -- browsers and password managers need these
10. **Progressive enhancement** -- forms should work without JavaScript (server actions)

## Common Pitfalls

| Pitfall | Impact | Fix |
|---------|--------|-----|
| Client-only validation | Security bypass | Always validate on server |
| Missing labels | Inaccessible to screen readers | Use `<label htmlFor>` |
| Clearing form on error | User loses all input | Preserve state on failure |
| No loading state | User clicks submit multiple times | Disable button + show spinner |
| Placeholder as label | Disappears on input, fails accessibility | Use visible labels |
| Missing `noValidate` | Browser and RHF validation conflict | Add `noValidate` to form tag |
