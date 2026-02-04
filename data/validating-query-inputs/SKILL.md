---
name: validating-query-inputs
description: Validate all external input with Zod before Prisma operations. Use when accepting user input, API requests, or form data.
allowed-tools: Read, Write, Edit
---

# Input Validation with Zod and Prisma 6

## Overview

Always validate external input with Zod before Prisma operations. Never trust user-provided data, API requests, or form submissions. Use type-safe validation pipelines that match Prisma schema types.

## Validation Pipeline

```
External Input → Zod Validation → Transform → Prisma Operation
```

### Pattern

```typescript
import { z } from 'zod'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().positive().optional()
})

async function createUser(rawInput: unknown) {
  const validatedData = createUserSchema.parse(rawInput)

  return await prisma.user.create({
    data: validatedData
  })
}
```

## Zod Schemas for Prisma Models

### Matching Prisma Types

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  phone     String?
  website   String?
  age       Int?
  createdAt DateTime @default(now())
}
```

```typescript
import { z } from 'zod'

const phoneRegex = /^\+?[1-9]\d{1,14}$/

const userCreateSchema = z.object({
  email: z.string().email().toLowerCase(),
  name: z.string().min(1).max(100).trim(),
  phone: z.string().regex(phoneRegex).optional(),
  website: z.string().url().optional(),
  age: z.number().int().min(0).max(150).optional()
})

const userUpdateSchema = userCreateSchema.partial()

type UserCreateInput = z.infer<typeof userCreateSchema>
type UserUpdateInput = z.infer<typeof userUpdateSchema>
```

### Common Validation Patterns

```typescript
const emailSchema = z.string().email().toLowerCase().trim()

const urlSchema = z.string().url().refine(
  (url) => url.startsWith('https://'),
  { message: 'URL must use HTTPS' }
)

const phoneSchema = z.string().regex(
  /^\+?[1-9]\d{1,14}$/,
  'Invalid phone number format'
)

const slugSchema = z.string()
  .min(1)
  .max(100)
  .regex(/^[a-z0-9-]+$/, 'Slug must contain only lowercase letters, numbers, and hyphens')

const dateSchema = z.coerce.date().refine(
  (date) => date > new Date(),
  { message: 'Date must be in the future' }
)
```

## Complete Validation Examples

### API Route with Validation

```typescript
import { z } from 'zod'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
  authorId: z.string().cuid(),
  published: z.boolean().default(false),
  tags: z.array(z.string()).max(10).optional()
})

export async function POST(request: Request) {
  try {
    const rawBody = await request.json()
    const validatedData = createPostSchema.parse(rawBody)

    const post = await prisma.post.create({
      data: validatedData
    })

    return Response.json(post)
  } catch (error) {
    if (error instanceof z.ZodError) {
      return Response.json(
        { errors: error.errors },
        { status: 400 }
      )
    }
    throw error
  }
}
```

### Form Data Validation

```typescript
import { z } from 'zod'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

const profileUpdateSchema = z.object({
  name: z.string().min(1).max(100).trim(),
  bio: z.string().max(500).trim().optional(),
  website: z.string().url().optional().or(z.literal('')),
  location: z.string().max(100).trim().optional(),
  birthDate: z.coerce.date().max(new Date()).optional()
})

async function updateProfile(userId: string, formData: FormData) {
  const rawData = {
    name: formData.get('name'),
    bio: formData.get('bio'),
    website: formData.get('website'),
    location: formData.get('location'),
    birthDate: formData.get('birthDate')
  }

  const validatedData = profileUpdateSchema.parse(rawData)

  return await prisma.user.update({
    where: { id: userId },
    data: validatedData
  })
}
```

### Nested Object Validation

```typescript
import { z } from 'zod'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

const addressSchema = z.object({
  street: z.string().min(1).max(200),
  city: z.string().min(1).max(100),
  state: z.string().length(2).toUpperCase(),
  zipCode: z.string().regex(/^\d{5}(-\d{4})?$/)
})

const createCompanySchema = z.object({
  name: z.string().min(1).max(200),
  email: z.string().email().toLowerCase(),
  website: z.string().url().optional(),
  address: addressSchema
})

async function createCompany(rawInput: unknown) {
  const validatedData = createCompanySchema.parse(rawInput)

  return await prisma.company.create({
    data: {
      name: validatedData.name,
      email: validatedData.email,
      website: validatedData.website,
      address: {
        create: validatedData.address
      }
    },
    include: {
      address: true
    }
  })
}
```

### Bulk Operation Validation

```typescript
import { z } from 'zod'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

const bulkUserSchema = z.object({
  users: z.array(
    z.object({
      email: z.string().email().toLowerCase(),
      name: z.string().min(1).max(100),
      role: z.enum(['USER', 'ADMIN'])
    })
  ).min(1).max(100)
})

async function createBulkUsers(rawInput: unknown) {
  const validatedData = bulkUserSchema.parse(rawInput)

  const uniqueEmails = new Set(validatedData.users.map(u => u.email))
  if (uniqueEmails.size !== validatedData.users.length) {
    throw new Error('Duplicate emails in bulk operation')
  }

  return await prisma.$transaction(
    validatedData.users.map(user =>
      prisma.user.create({ data: user })
    )
  )
}
```

## Advanced Patterns

### Custom Refinements

```typescript
import { z } from 'zod'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

const passwordSchema = z.string()
  .min(8)
  .refine((pwd) => /[A-Z]/.test(pwd), {
    message: 'Password must contain uppercase letter'
  })
  .refine((pwd) => /[a-z]/.test(pwd), {
    message: 'Password must contain lowercase letter'
  })
  .refine((pwd) => /[0-9]/.test(pwd), {
    message: 'Password must contain number'
  })

const registerSchema = z.object({
  email: z.string().email().toLowerCase(),
  password: passwordSchema,
  confirmPassword: z.string()
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword']
})
```

### Async Validation

```typescript
import { z } from 'zod'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

const createUserSchema = z.object({
  email: z.string().email().toLowerCase(),
  username: z.string().min(3).max(30).regex(/^[a-z0-9_]+$/)
})

async function createUserWithChecks(rawInput: unknown) {
  const validatedData = createUserSchema.parse(rawInput)

  const existing = await prisma.user.findFirst({
    where: {
      OR: [
        { email: validatedData.email },
        { username: validatedData.username }
      ]
    }
  })

  if (existing) {
    if (existing.email === validatedData.email) {
      throw new Error('Email already exists')
    }
    if (existing.username === validatedData.username) {
      throw new Error('Username already taken')
    }
  }

  return await prisma.user.create({
    data: validatedData
  })
}
```

### Safe Parsing

```typescript
import { z } from 'zod'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

const updateSettingsSchema = z.object({
  theme: z.enum(['light', 'dark']).default('light'),
  notifications: z.boolean().default(true),
  language: z.string().length(2).default('en')
})

async function updateSettings(userId: string, rawInput: unknown) {
  const result = updateSettingsSchema.safeParse(rawInput)

  if (!result.success) {
    return {
      success: false,
      errors: result.error.errors
    }
  }

  const settings = await prisma.userSettings.upsert({
    where: { userId },
    update: result.data,
    create: {
      userId,
      ...result.data
    }
  })

  return {
    success: true,
    data: settings
  }
}
```

## Security Checklist

- [ ] All external input validated before Prisma operations
- [ ] Zod schemas match Prisma model types
- [ ] Email addresses normalized (toLowerCase)
- [ ] String inputs trimmed where appropriate
- [ ] URLs validated and HTTPS enforced
- [ ] Phone numbers validated with regex
- [ ] Numeric ranges validated (min/max)
- [ ] Array lengths limited (prevent DoS)
- [ ] Unique constraints validated before bulk operations
- [ ] Async existence checks for unique fields
- [ ] Error messages don't leak sensitive data
- [ ] File uploads validated (type, size, content)

## Anti-Patterns

### Never Trust Input

```typescript
async function createUser(data: any) {
  return await prisma.user.create({ data })
}
```

### Never Skip Validation for "Internal" Data

```typescript
async function createUserFromAdmin(data: unknown) {
  return await prisma.user.create({ data })
}
```

### Never Validate After Database Operation

```typescript
async function createUser(data: unknown) {
  const user = await prisma.user.create({ data })
  const validated = schema.parse(user)
  return validated
}
```

## Type Safety Integration

```typescript
import { z } from 'zod'
import { Prisma } from '@prisma/client'

const userCreateSchema = z.object({
  email: z.string().email(),
  name: z.string()
}) satisfies z.Schema<Prisma.UserCreateInput>

type ValidatedUserInput = z.infer<typeof userCreateSchema>
```

## Related Skills

**Zod v4 Validation:**

- If normalizing string inputs (trim, toLowerCase), use the transforming-string-methods skill for Zod v4 built-in string transformations
- If using Zod for schema construction, use the validating-schema-basics skill from zod-4 for core validation patterns
- If customizing validation error messages, use the customizing-errors skill from zod-4 for error formatting strategies
- If validating string formats (email, UUID, URL), use the validating-string-formats skill from zod-4 for built-in validators

**TypeScript Validation:**

- If performing runtime type checking beyond Zod, use the using-runtime-checks skill from typescript for assertion patterns
- If validating external data sources, use the validating-external-data skill from typescript for comprehensive validation strategies
