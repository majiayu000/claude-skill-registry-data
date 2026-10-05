---
name: react-form-validator
description: This skill should be used when the user asks to "create a form", "add validation", "handle form submission", "use React Hook Form", or when creating login, signup, or data entry forms. Enforces React Hook Form + Zod pattern.
---

# React Form Validator

Auto-enforces React Hook Form + Zod validation pattern for ALL forms in Next.js/React applications.

## Activation Triggers

This skill activates when:
- Creating form components
- Using `<form>`, `<input>`, form elements
- Mentioning "form", "validation", "submit", "input"
- Handling form state or submission
- Creating login, signup, or data entry forms

## Required Form Pattern (MANDATORY)

ALL forms MUST use:
- ✅ **React Hook Form** for form state management
- ✅ **Zod** for schema validation
- ✅ **TypeScript** types inferred from Zod schema
- ✅ **Error handling** with accessible error messages
- ✅ **Loading states** during submission

## Auto-Validation Process

### Step 1: Detect Form Without Pattern

When detecting a form being created:

```tsx
// ❌ WRONG - Uncontrolled form, no validation
function LoginForm() {
  const handleSubmit = (e) => {
    e.preventDefault()
    const email = e.target.email.value  // No validation!
    const password = e.target.password.value
    // Submit...
  }

  return (
    <form onSubmit={handleSubmit}>
      <input name="email" type="email" />
      <input name="password" type="password" />
      <button>Login</button>
    </form>
  )
}
```

### Step 2: Identify Missing Requirements

Detect:
- ❌ No React Hook Form
- ❌ No Zod validation
- ❌ No TypeScript types
- ❌ No error display
- ❌ No loading state

### Step 3: Auto-Fix to Correct Pattern

**After (Correct Pattern):**
```tsx
'use client'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'

// 1. Define Zod schema
const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
})

// 2. Infer TypeScript type from schema
type LoginFormData = z.infer<typeof loginSchema>

function LoginForm() {
  // 3. Set up React Hook Form with Zod resolver
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  // 4. Type-safe submit handler
  const onSubmit = async (data: LoginFormData) => {
    try {
      await loginUser(data)
      // Handle success
    } catch (error) {
      // Handle error
    }
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {/* Email field */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          {...register('email')}
          id="email"
          type="email"
          className="mt-1 block w-full rounded-md border-gray-300"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && (
          <p id="email-error" className="mt-1 text-sm text-red-600" role="alert">
            {errors.email.message}
          </p>
        )}
      </div>

      {/* Password field */}
      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          {...register('password')}
          id="password"
          type="password"
          className="mt-1 block w-full rounded-md border-gray-300"
          aria-invalid={!!errors.password}
          aria-describedby={errors.password ? 'password-error' : undefined}
        />
        {errors.password && (
          <p id="password-error" className="mt-1 text-sm text-red-600" role="alert">
            {errors.password.message}
          </p>
        )}
      </div>

      {/* Submit button with loading state */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  )
}
```

### Step 4: Explain Pattern

> **Form Pattern Applied**
>
> **Added:**
> 1. ✅ Zod schema for validation
> 2. ✅ TypeScript types inferred from schema
> 3. ✅ React Hook Form for state management
> 4. ✅ zodResolver connects Zod to React Hook Form
> 5. ✅ Error messages displayed accessibly
> 6. ✅ Loading state during submission
>
> **Why:**
> - Zod provides runtime type validation
> - React Hook Form handles form state efficiently
> - Type safety prevents bugs
> - Accessible error messages help all users

## Complete Form Patterns

### Pattern 1: Simple Contact Form

```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'

const contactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  message: z.string().min(10, 'Message must be at least 10 characters'),
})

type ContactFormData = z.infer<typeof contactSchema>

export function ContactForm() {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting, isSubmitSuccessful },
  } = useForm<ContactFormData>({
    resolver: zodResolver(contactSchema),
  })

  const onSubmit = async (data: ContactFormData) => {
    await sendContactMessage(data)
    reset() // Clear form after success
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <div>
        <label htmlFor="name">Name</label>
        <input {...register('name')} id="name" type="text" />
        {errors.name && <p role="alert">{errors.name.message}</p>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input {...register('email')} id="email" type="email" />
        {errors.email && <p role="alert">{errors.email.message}</p>}
      </div>

      <div>
        <label htmlFor="message">Message</label>
        <textarea {...register('message')} id="message" rows={4} />
        {errors.message && <p role="alert">{errors.message.message}</p>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Sending...' : 'Send Message'}
      </button>

      {isSubmitSuccessful && (
        <p className="text-green-600">Message sent successfully!</p>
      )}
    </form>
  )
}
```

### Pattern 2: Complex Registration Form

```tsx
const registerSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).regex(/[A-Z]/, 'Must contain uppercase letter'),
  confirmPassword: z.string(),
  firstName: z.string().min(2),
  lastName: z.string().min(2),
  terms: z.boolean().refine((val) => val === true, {
    message: 'You must accept the terms and conditions',
  }),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
})

type RegisterFormData = z.infer<typeof registerSchema>

export function RegisterForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  })

  const onSubmit = async (data: RegisterFormData) => {
    await createUser(data)
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      {/* Email */}
      <div>
        <label htmlFor="email">Email</label>
        <input {...register('email')} id="email" type="email" />
        {errors.email && <p role="alert">{errors.email.message}</p>}
      </div>

      {/* Password */}
      <div>
        <label htmlFor="password">Password</label>
        <input {...register('password')} id="password" type="password" />
        {errors.password && <p role="alert">{errors.password.message}</p>}
      </div>

      {/* Confirm Password */}
      <div>
        <label htmlFor="confirmPassword">Confirm Password</label>
        <input {...register('confirmPassword')} id="confirmPassword" type="password" />
        {errors.confirmPassword && <p role="alert">{errors.confirmPassword.message}</p>}
      </div>

      {/* First Name */}
      <div>
        <label htmlFor="firstName">First Name</label>
        <input {...register('firstName')} id="firstName" type="text" />
        {errors.firstName && <p role="alert">{errors.firstName.message}</p>}
      </div>

      {/* Last Name */}
      <div>
        <label htmlFor="lastName">Last Name</label>
        <input {...register('lastName')} id="lastName" type="text" />
        {errors.lastName && <p role="alert">{errors.lastName.message}</p>}
      </div>

      {/* Terms checkbox */}
      <div>
        <label className="flex items-center">
          <input {...register('terms')} type="checkbox" className="mr-2" />
          I accept the terms and conditions
        </label>
        {errors.terms && <p role="alert">{errors.terms.message}</p>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Creating account...' : 'Sign Up'}
      </button>
    </form>
  )
}
```

### Pattern 3: Multi-Step Form

```tsx
const step1Schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
})

const step2Schema = z.object({
  firstName: z.string().min(2),
  lastName: z.string().min(2),
  phone: z.string().optional(),
})

type Step1Data = z.infer<typeof step1Schema>
type Step2Data = z.infer<typeof step2Schema>

export function MultiStepForm() {
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState<Partial<Step1Data & Step2Data>>({})

  const step1Form = useForm<Step1Data>({
    resolver: zodResolver(step1Schema),
  })

  const step2Form = useForm<Step2Data>({
    resolver: zodResolver(step2Schema),
  })

  const handleStep1 = (data: Step1Data) => {
    setFormData({ ...formData, ...data })
    setStep(2)
  }

  const handleStep2 = async (data: Step2Data) => {
    const finalData = { ...formData, ...data }
    await submitRegistration(finalData)
  }

  return (
    <div>
      {step === 1 && (
        <form onSubmit={step1Form.handleSubmit(handleStep1)}>
          {/* Step 1 fields */}
          <button type="submit">Next</button>
        </form>
      )}

      {step === 2 && (
        <form onSubmit={step2Form.handleSubmit(handleStep2)}>
          {/* Step 2 fields */}
          <button type="button" onClick={() => setStep(1)}>
            Back
          </button>
          <button type="submit">Submit</button>
        </form>
      )}
    </div>
  )
}
```

## Advanced Zod Patterns

### Custom Validation

```tsx
const userSchema = z.object({
  username: z.string()
    .min(3)
    .max(20)
    .regex(/^[a-zA-Z0-9_]+$/, 'Only letters, numbers, and underscores allowed'),
  age: z.number()
    .int()
    .min(18, 'Must be 18 or older')
    .max(120),
  website: z.string().url().optional(),
})
```

### Async Validation

```tsx
const emailSchema = z.string().email().refine(
  async (email) => {
    const available = await checkEmailAvailability(email)
    return available
  },
  { message: 'Email already in use' }
)
```

### Conditional Fields

```tsx
const shippingSchema = z.object({
  sameAsBilling: z.boolean(),
  address: z.string().optional(),
  city: z.string().optional(),
  zip: z.string().optional(),
}).refine(
  (data) => {
    if (!data.sameAsBilling) {
      return !!data.address && !!data.city && !!data.zip
    }
    return true
  },
  {
    message: 'Shipping address is required',
    path: ['address'],
  }
)
```

## Form Component Reusability

```tsx
// Reusable FormField component
interface FormFieldProps {
  label: string
  name: string
  type?: string
  register: UseFormRegister<any>
  error?: FieldError
  required?: boolean
}

function FormField({ label, name, type = 'text', register, error, required }: FormFieldProps) {
  const id = `field-${name}`

  return (
    <div>
      <label htmlFor={id} className="block text-sm font-medium">
        {label} {required && <span className="text-red-600">*</span>}
      </label>
      <input
        {...register(name)}
        id={id}
        type={type}
        className="mt-1 block w-full rounded-md border-gray-300"
        aria-invalid={!!error}
        aria-describedby={error ? `${id}-error` : undefined}
        aria-required={required}
      />
      {error && (
        <p id={`${id}-error`} className="mt-1 text-sm text-red-600" role="alert">
          {error.message}
        </p>
      )}
    </div>
  )
}

// Usage
function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  })

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <FormField
        label="Email"
        name="email"
        type="email"
        register={register}
        error={errors.email}
        required
      />
      <FormField
        label="Password"
        name="password"
        type="password"
        register={register}
        error={errors.password}
        required
      />
      <button type="submit">Login</button>
    </form>
  )
}
```

## Server Actions & React 19 Integration

React 19 / Next.js 15 provides native Server Actions with `useActionState` and `useOptimistic`, combined with Zod validation.

### Server Action with Zod Schema Validation

```tsx
'use server'
import { z } from 'zod'

const contactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address'),
  message: z.string().min(10, 'Message must be at least 10 characters'),
})

export type FormState = {
  success?: boolean
  errors?: Record<string, string[]>
  message?: string
}

export async function submitContact(
  prevState: FormState,
  formData: FormData
): Promise<FormState> {
  const data = {
    name: formData.get('name'),
    email: formData.get('email'),
    message: formData.get('message'),
  }

  const result = contactSchema.safeParse(data)

  if (!result.success) {
    return {
      success: false,
      errors: result.error.flatten().fieldErrors,
    }
  }

  // Process valid data securely on server
  await saveContact(result.data)
  return { success: true, message: 'Message sent successfully!' }
}
```

### Client Form with React 19 `useActionState` & `useOptimistic`

```tsx
'use client'

import { useActionState, useOptimistic } from 'react'
import { submitContact, type FormState } from './actions'

const initialState: FormState = {}

export function ContactForm() {
  const [state, formAction, isPending] = useActionState(submitContact, initialState)
  const [optimisticStatus, setOptimisticStatus] = useOptimistic(
    isPending,
    (_, pending: boolean) => pending
  )

  return (
    <form action={formAction} className="space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium">Name</label>
        <input
          id="name"
          name="name"
          type="text"
          aria-invalid={!!state.errors?.name}
          aria-describedby={state.errors?.name ? 'name-error' : undefined}
          className="mt-1 block w-full rounded-md border-gray-300"
        />
        {state.errors?.name && (
          <p id="name-error" className="mt-1 text-sm text-red-600" role="alert">
            {state.errors.name[0]}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          aria-invalid={!!state.errors?.email}
          aria-describedby={state.errors?.email ? 'email-error' : undefined}
          className="mt-1 block w-full rounded-md border-gray-300"
        />
        {state.errors?.email && (
          <p id="email-error" className="mt-1 text-sm text-red-600" role="alert">
            {state.errors.email[0]}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="message" className="block text-sm font-medium">Message</label>
        <textarea
          id="message"
          name="message"
          rows={4}
          aria-invalid={!!state.errors?.message}
          aria-describedby={state.errors?.message ? 'message-error' : undefined}
          className="mt-1 block w-full rounded-md border-gray-300"
        />
        {state.errors?.message && (
          <p id="message-error" className="mt-1 text-sm text-red-600" role="alert">
            {state.errors.message[0]}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={optimisticStatus}
        className="py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {optimisticStatus ? 'Sending...' : 'Send Message'}
      </button>

      {state.success && (
        <p className="text-sm text-green-600" role="status">
          {state.message}
        </p>
      )}
    </form>
  )
}
```

## Success Criteria

✅ ALL forms use React Hook Form
✅ ALL forms use Zod validation
✅ TypeScript types inferred from schemas
✅ Error messages displayed accessibly
✅ Loading states during submission
✅ Forms are keyboard accessible
✅ ARIA attributes for errors

## Behavior

**Proactive enforcement:**
- Detect forms without being asked
- Add React Hook Form + Zod automatically
- Generate complete form code
- Explain benefits of the pattern
- Ensure accessibility

**Never:**
- Allow unvalidated forms
- Accept useState for form state
- Allow inline validation logic
- Skip TypeScript types

**Block completion if:**
- Form lacks validation
- No error handling
- Missing loading states
- Not using React Hook Form + Zod

This ensures all forms are type-safe, validated, and accessible from day one.
