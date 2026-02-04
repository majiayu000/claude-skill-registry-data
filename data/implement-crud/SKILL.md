---
name: implement-crud
description: Implement complete CRUD (Create, Read, Update, Delete) operations for Supabase tables with proper error handling, validation, and RLS. Triggers when user requests data operations, API endpoints, or database interactions.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# CRUD Implementation Skill

Implement comprehensive CRUD operations for Supabase tables with best practices.

## Purpose

Generate production-ready CRUD operations including queries, mutations, error handling, type safety, and RLS-aware implementations.

## When to Use

- User requests CRUD functionality
- Needs API endpoints for data operations
- Asks for database interaction code
- Wants to implement data management features
- Requests type-safe database operations

## Instructions

1. **Analyze Requirements**
   - Identify target table and columns
   - Understand relationships and foreign keys
   - Check RLS policies on table
   - Determine validation rules
   - Identify required permissions

2. **Implement Read Operations**
   - Single record fetch by ID
   - List with filtering and pagination
   - Search functionality
   - Include related data with joins
   - Handle not found cases

3. **Implement Create Operations**
   - Input validation
   - Required field checks
   - Foreign key validation
   - Return created record with ID
   - Handle duplicate key errors

4. **Implement Update Operations**
   - Partial update support
   - Optimistic locking if needed
   - Validate ownership via RLS
   - Return updated record
   - Handle not found cases

5. **Implement Delete Operations**
   - Soft delete vs hard delete
   - Cascade handling
   - Validate ownership
   - Return success confirmation
   - Handle foreign key violations

6. **Add Error Handling**
   - Wrap operations in try-catch
   - Provide meaningful error messages
   - Handle common Postgres errors
   - Return structured error responses
   - Log errors appropriately

## Examples

### TypeScript Implementation

```typescript
import { createClient } from '@supabase/supabase-js'
import type { Database } from './database.types'

const supabase = createClient<Database>(
  process.env.SUPABASE_URL!,
  process.env.SUPABASE_ANON_KEY!
)

// READ: Get single post by ID
export async function getPost(id: string) {
  const { data, error } = await supabase
    .from('posts')
    .select(`
      *,
      author:profiles!author_id(*),
      comments(count)
    `)
    .eq('id', id)
    .single()

  if (error) {
    throw new Error(`Failed to fetch post: ${error.message}`)
  }

  return data
}

// READ: List posts with pagination
export async function listPosts(options: {
  page?: number
  perPage?: number
  published?: boolean
}) {
  const { page = 1, perPage = 20, published } = options
  const start = (page - 1) * perPage
  const end = start + perPage - 1

  let query = supabase
    .from('posts')
    .select('*, author:profiles!author_id(username)', { count: 'exact' })

  if (published !== undefined) {
    query = query.eq('published', published)
  }

  const { data, error, count } = await query
    .order('created_at', { ascending: false })
    .range(start, end)

  if (error) {
    throw new Error(`Failed to list posts: ${error.message}`)
  }

  return {
    data,
    pagination: {
      page,
      perPage,
      total: count,
      totalPages: Math.ceil((count || 0) / perPage)
    }
  }
}

// CREATE: Insert new post
export async function createPost(input: {
  title: string
  content: string
  authorId: string
  published?: boolean
}) {
  const { data, error } = await supabase
    .from('posts')
    .insert({
      title: input.title,
      content: input.content,
      author_id: input.authorId,
      published: input.published ?? false,
      slug: generateSlug(input.title)
    })
    .select()
    .single()

  if (error) {
    if (error.code === '23505') {
      throw new Error('A post with this title already exists')
    }
    throw new Error(`Failed to create post: ${error.message}`)
  }

  return data
}

// UPDATE: Update existing post
export async function updatePost(
  id: string,
  updates: {
    title?: string
    content?: string
    published?: boolean
  }
) {
  const { data, error } = await supabase
    .from('posts')
    .update(updates)
    .eq('id', id)
    .select()
    .single()

  if (error) {
    if (error.code === 'PGRST116') {
      throw new Error('Post not found or access denied')
    }
    throw new Error(`Failed to update post: ${error.message}`)
  }

  return data
}

// DELETE: Remove post
export async function deletePost(id: string) {
  const { error } = await supabase
    .from('posts')
    .delete()
    .eq('id', id)

  if (error) {
    if (error.code === 'PGRST116') {
      throw new Error('Post not found or access denied')
    }
    throw new Error(`Failed to delete post: ${error.message}`)
  }

  return { success: true }
}

function generateSlug(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
}
```

## Output Format

Provide:
1. Complete CRUD function implementations
2. Proper TypeScript types
3. Error handling for all cases
4. Usage examples
5. Testing recommendations
