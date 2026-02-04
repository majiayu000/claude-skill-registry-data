---
name: integrating-formspree-forms
description: Use when adding forms to static websites using Formspree - provides contact forms, newsletter signups, validation, and spam protection without backend code
---

# Integrating Formspree Forms

## Overview

Form handling for static sites using **Formspree** - no backend needed.

## Why Formspree

- Dead simple setup
- Email notifications built-in
- Spam protection included
- Free tier: 50 submissions/month
- Paid tier: $10/mo for 1000 submissions

## Setup

**1. Create Formspree account** at https://formspree.io

**2. Install dependencies:**
```bash
pnpm add @formspree/react
```

**3. Get your form ID** from Formspree dashboard

## Basic Contact Form

```typescript
// components/forms/ContactForm.tsx
'use client'

import { useForm, ValidationError } from '@formspree/react'

export default function ContactForm() {
  const [state, handleSubmit] = useForm("YOUR_FORM_ID")

  if (state.succeeded) {
    return <p>Thanks for your message! We'll get back to you soon.</p>
  }

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="name">Name</label>
        <input id="name" type="text" name="name" required />
        <ValidationError prefix="Name" field="name" errors={state.errors} />
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input id="email" type="email" name="email" required />
        <ValidationError prefix="Email" field="email" errors={state.errors} />
      </div>

      <div>
        <label htmlFor="message">Message</label>
        <textarea id="message" name="message" rows={6} required />
        <ValidationError prefix="Message" field="message" errors={state.errors} />
      </div>

      <button type="submit" disabled={state.submitting}>
        {state.submitting ? 'Sending...' : 'Send Message'}
      </button>
    </form>
  )
}
```

## Newsletter Form

```typescript
'use client'

import { useForm, ValidationError } from '@formspree/react'

export default function NewsletterForm() {
  const [state, handleSubmit] = useForm("YOUR_NEWSLETTER_FORM_ID")

  if (state.succeeded) {
    return <p>Thanks for subscribing!</p>
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="email"
        name="email"
        placeholder="Email Address"
        required
      />
      <ValidationError prefix="Email" field="email" errors={state.errors} />

      <button type="submit" disabled={state.submitting}>
        {state.submitting ? 'Subscribing...' : 'Sign Up'}
      </button>

      {/* Honeypot for spam protection */}
      <input
        type="text"
        name="_gotcha"
        style={{ display: 'none' }}
        tabIndex={-1}
      />
    </form>
  )
}
```

## Enhanced Validation (React Hook Form + Zod)

```bash
pnpm add react-hook-form @hookform/resolvers zod
```

```typescript
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useForm as useFormspree } from '@formspree/react'

const contactSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Please enter a valid email'),
  message: z.string().min(10, 'Message must be at least 10 characters'),
})

type ContactFormData = z.infer<typeof contactSchema>

export default function ContactFormEnhanced() {
  const [formspreeState, submitToFormspree] = useFormspree("YOUR_FORM_ID")

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<ContactFormData>({
    resolver: zodResolver(contactSchema),
  })

  const onSubmit = async (data: ContactFormData) => {
    await submitToFormspree(data)
    if (formspreeState.succeeded) reset()
  }

  if (formspreeState.succeeded) {
    return <p>Thanks for your message!</p>
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="name">Name</label>
        <input {...register('name')} id="name" type="text" />
        {errors.name && <p>{errors.name.message}</p>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input {...register('email')} id="email" type="email" />
        {errors.email && <p>{errors.email.message}</p>}
      </div>

      <div>
        <label htmlFor="message">Message</label>
        <textarea {...register('message')} id="message" rows={6} />
        {errors.message && <p>{errors.message.message}</p>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Sending...' : 'Send Message'}
      </button>
    </form>
  )
}
```

## Spam Protection

**Honeypot field:**
```jsx
<input
  type="text"
  name="_gotcha"
  style={{ display: 'none' }}
  tabIndex={-1}
  autoComplete="off"
  aria-hidden="true"
/>
```

**reCAPTCHA:** Configure in Formspree dashboard for additional protection.

## Environment Variables

```bash
# .env.local
NEXT_PUBLIC_FORMSPREE_CONTACT_ID=abcd1234
NEXT_PUBLIC_FORMSPREE_NEWSLETTER_ID=efgh5678
```

```typescript
const [state, handleSubmit] = useForm(
  process.env.NEXT_PUBLIC_FORMSPREE_CONTACT_ID!
)
```

## Testing

**E2E test with Playwright:**
```typescript
import { test, expect } from '@playwright/test'

test('contact form submission works', async ({ page }) => {
  await page.goto('/contact')

  await page.fill('input[name="name"]', 'Test User')
  await page.fill('input[name="email"]', 'test@example.com')
  await page.fill('textarea[name="message"]', 'Test message')

  await page.click('button[type="submit"]')

  await expect(page.locator('text=Thanks for your message')).toBeVisible()
})
```

## Accessibility

```typescript
<form aria-label="Contact form">
  <div>
    <label htmlFor="email">
      Email <span className="sr-only">(required)</span>
    </label>
    <input
      id="email"
      type="email"
      name="email"
      required
      aria-required="true"
      aria-invalid={!!errors.email}
      aria-describedby={errors.email ? "email-error" : undefined}
    />
    {errors.email && (
      <p id="email-error" role="alert">
        {errors.email.message}
      </p>
    )}
  </div>

  <button type="submit" aria-disabled={isSubmitting}>
    {isSubmitting ? 'Sending...' : 'Send Message'}
  </button>
</form>
```

## Best Practices

1. **Always validate client-side** - Better UX
2. **Use honeypot fields** - Simple spam protection
3. **Show loading states** - User feedback during submission
4. **Clear success messages** - Confirm submission worked
5. **Accessible labels** - All inputs need labels
6. **Error handling** - Show helpful error messages
7. **Environment variables** - Keep form IDs out of code
8. **Test thoroughly** - E2E tests for critical forms
