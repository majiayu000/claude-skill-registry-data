---
name: supabase-queries
description: Apply when writing Supabase client queries for CRUD operations, filtering, joins, and real-time subscriptions.
version: 1.0.0
tokens: ~700
confidence: high
sources:
  - https://supabase.com/docs/reference/javascript/select
  - https://supabase.com/docs/reference/javascript/insert
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [supabase, database, queries, javascript]
---

## When to Use

Apply when writing Supabase client queries for CRUD operations, filtering, joins, and real-time subscriptions.

## Patterns

### Pattern 1: Select with Filters
```typescript
// Source: https://supabase.com/docs/reference/javascript/select
const { data, error } = await supabase
  .from('todos')
  .select('id, title, completed')
  .eq('user_id', userId)
  .order('created_at', { ascending: false })
  .limit(10);
```

### Pattern 2: Insert with Return
```typescript
// Source: https://supabase.com/docs/reference/javascript/insert
const { data, error } = await supabase
  .from('todos')
  .insert({ title: 'New todo', user_id: userId })
  .select()
  .single();
```

### Pattern 3: Update with Match
```typescript
// Source: https://supabase.com/docs/reference/javascript/update
const { data, error } = await supabase
  .from('todos')
  .update({ completed: true })
  .eq('id', todoId)
  .select()
  .single();
```

### Pattern 4: Select with Relations (JOIN)
```typescript
// Source: https://supabase.com/docs/reference/javascript/select
const { data, error } = await supabase
  .from('posts')
  .select(`
    id,
    title,
    author:profiles(name, avatar_url),
    comments(id, content)
  `)
  .eq('published', true);
```

### Pattern 5: Upsert (Insert or Update)
```typescript
// Source: https://supabase.com/docs/reference/javascript/upsert
const { data, error } = await supabase
  .from('profiles')
  .upsert({ id: userId, name: 'New Name' })
  .select()
  .single();
```

### Pattern 6: Count Query
```typescript
// Source: https://supabase.com/docs/reference/javascript/select
const { count, error } = await supabase
  .from('todos')
  .select('*', { count: 'exact', head: true })
  .eq('completed', false);
```

## Anti-Patterns

- **Not handling errors** - Always check `error` before using `data`
- **Select * in production** - Specify columns explicitly for performance
- **Missing .single()** - Use when expecting one row, prevents array return
- **Chaining after await** - Build query first, then await

## Verification Checklist

- [ ] Error handling: `if (error) throw error`
- [ ] Specific columns selected (not `*`)
- [ ] `.single()` used for single-row queries
- [ ] RLS policies allow the operation
- [ ] Types match database schema
