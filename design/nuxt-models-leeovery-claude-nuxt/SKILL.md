---
name: nuxt-models
description: Domain model classes with automatic hydration, relations, and type casting. Use when creating models for API entities, defining relationships between models, casting properties to enums/dates, or creating value objects.
---

# Nuxt Models

Type-safe domain models with automatic hydration, relations, and property casting.

## Core Concepts

**[models.md](references/models.md)** - Complete model patterns, lifecycle, relations, casts
**[values.md](references/values.md)** - Value objects for typed wrappers (DateValue, etc.)

## Basic Model

```typescript
// app/models/Post.ts
import Model from '#layers/base/app/models/Model'
import type { Castable } from '#layers/base/app/types'
import PostStatus from '~/enums/PostStatus'
import DateValue from '~/values/DateValue'
import Author from '~/models/Author'

export default class Post extends Model {
  ulid: string
  title: string
  content: string
  status: PostStatus
  isDraft: boolean
  author: Author
  createdAt: DateValue

  public override primaryKey(): string {
    return 'ulid'
  }

  public override casts(): Record<string, Castable> {
    return {
      status: PostStatus,
      createdAt: DateValue,
    }
  }

  public override relations(): Record<string, typeof Model> {
    return {
      author: Author,
    }
  }

  public isPublished(): boolean {
    return !this.isDraft
  }
}
```

## Model Lifecycle

```
API Response → booting() → transform() → Property Assignment
     → Relations Hydrated → Casts Applied → booted() → Ready
```

## Usage

```typescript
// Hydrate from API response
const post = Post.hydrate(apiResponse.data)

// Hydrate collection
const posts = Post.collect(apiResponse.data)

// Access typed properties
post.status.color()           // Enum method
post.createdAt.format()       // Value object method
post.author.name              // Relation property

// Compare models
post.is(otherPost)            // Same primary key?
```
