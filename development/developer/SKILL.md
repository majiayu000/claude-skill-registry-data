---
name: developer
description: Senior-level development guidance for this project. Use when writing code, implementing features, refactoring, reviewing code architecture, or when best practices and security considerations are needed. (project)
---

# Senior Developer Standards

## Tech Stack Expertise

This project uses:
- **Next.js 15** (App Router) - Server/client components, API routes, middleware
- **MongoDB** with Mongoose ODM - Document modeling, indexes, aggregations
- **NextAuth.js** - Authentication with credentials provider and JWT sessions
- **TypeScript** (strict mode) - Strong typing, generics, utility types
- **Zustand** - Client-side state management
- **Tailwind CSS** - Utility-first styling

## Project Architecture

### API Routes (`app/api/`)
All backend logic lives in Next.js API routes:
```typescript
// app/api/blog/posts/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from '@/lib/auth'
import { connectDB } from '@/lib/mongodb'
import BlogPost from '@/models/BlogPost'

export async function GET(req: NextRequest) {
  await connectDB()
  // Query logic...
  return NextResponse.json({ success: true, payload: data })
}

export async function POST(req: NextRequest) {
  const session = await getServerSession()
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }
  // Create logic...
}
```

### Mongoose Models (`models/`)
All database models use Mongoose schemas:
```typescript
import mongoose, { Schema, Document, Model } from 'mongoose'

export interface IUser extends Document {
  name: string
  email: string
  password: string
  roles: string[]
}

const userSchema = new Schema<IUser>({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true, select: false },
  roles: { type: [String], default: ['user'] },
}, { timestamps: true })

export default mongoose.models.User || mongoose.model<IUser>('User', userSchema)
```

### Authentication (`lib/auth.ts`)
NextAuth.js with credentials provider:
```typescript
import { getServerSession } from '@/lib/auth'

// In API routes
export async function POST(req: NextRequest) {
  const session = await getServerSession()
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // Check permissions
  if (!session.user.permissions.includes('BLOG.POST_CREATE')) {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 })
  }
}
```

### Permission System (`lib/permissions.ts`)
Role-based permissions:
```typescript
export const permissionByRole = {
  admin: ['USER.GET_SELF', 'BLOG.POST_CREATE', 'BLOG.POST_UPDATE', ...],
  user: [],
}

// Check permission
if (!session.user.permissions.includes('BLOG.POST_CREATE')) {
  return forbiddenResponse()
}
```

## Security Best Practices

### Password Handling
```typescript
// NEVER store plain text passwords
// ALWAYS use bcrypt for hashing (saltRounds: 10)

import bcrypt from 'bcryptjs'

userSchema.pre('save', async function (next) {
  if (!this.isModified('password')) return next()
  this.password = await bcrypt.hash(this.password, 10)
  next()
})

userSchema.methods.comparePassword = async function (password: string) {
  return bcrypt.compare(password, this.password)
}
```

### Environment Variables
```typescript
// NEVER commit secrets to version control
// ALWAYS use environment variables

// Required in .env.local:
// MONGODB_URI=mongodb://localhost:27017/freelancelyst
// NEXTAUTH_SECRET=your-secret-key
// NEXTAUTH_URL=http://localhost:3000
```

### Input Validation
```typescript
// ALWAYS validate user input
// Use Zod or manual validation

import { z } from 'zod'

const CreatePostSchema = z.object({
  slug: z.string().min(1).max(200),
  title: z.string().min(1).max(500),
  content: z.string().min(1),
  langCode: z.enum(['en', 'fa']),
})
```

## Translation Pattern

Blog entities use embedded translation arrays:
```typescript
// BlogPost model
const blogPostSchema = new Schema({
  slug: { type: String, required: true, unique: true },
  translations: [{
    langCode: { type: String, required: true },
    title: { type: String, required: true },
    content: { type: String, required: true },
    excerpt: { type: String, required: true },
  }],
})

// Querying with translation
const translation = post.translations.find(t => t.langCode === langCode)
  || post.translations.find(t => t.langCode === 'en')
  || post.translations[0]
```

## API Response Format

```typescript
// Success response
return NextResponse.json({
  success: true,
  message: 'Operation successful',
  payload: data,
  id: uuidv4(), // tracking ID
})

// Error response
return NextResponse.json({
  fail: true,
  message: 'Error description',
  id: uuidv4(),
}, { status: 400 })

// Paginated response
return NextResponse.json({
  success: true,
  payload: {
    posts,
    total,
    page,
    pageSize,
    totalPages: Math.ceil(total / pageSize),
  },
})
```

## Zustand Store Pattern

```typescript
import { create } from 'zustand'
import { getRequest, postRequest } from '@/utils/request/request'

interface IState {
  items: Item[]
  loading: boolean
  fetchItems: () => Promise<void>
}

export const useStore = create<IState>()((set, get) => ({
  items: [],
  loading: false,

  fetchItems: async () => {
    set({ loading: true })
    const response = await getRequest({ url: '/api/items' })
    set({ items: response.payload, loading: false })
  },
}))
```

## Code Quality Standards

### TypeScript
- Use strict mode
- Avoid `any` - use `unknown` for truly unknown types
- Define interfaces for all data shapes
- Use utility types (Omit, Pick, Partial)

### Error Handling
```typescript
try {
  await connectDB()
  // ... logic
} catch (error) {
  console.error('Operation failed:', error)
  return NextResponse.json({ error: 'Operation failed' }, { status: 500 })
}
```

### Async/Await
```typescript
// Use Promise.all for parallel operations
const [posts, categories, tags] = await Promise.all([
  BlogPost.find(query),
  BlogCategory.find(),
  BlogTag.find(),
])
```

## i18n Support

- Two languages: English (en, LTR) and Farsi (fa, RTL)
- Route structure: `/[lang]/page`
- Translations in `app/_utils/translation/`
- RTL support via `dir` attribute on HTML

## Domain Terminology

| Term | Definition |
|------|------------|
| BlogPost | Blog article with translations |
| BlogCategory | Post category with translations |
| BlogTag | Post tag with translations |
| ProjectApplication | Client project submission |
| FreelancerApplication | Freelancer job application |
