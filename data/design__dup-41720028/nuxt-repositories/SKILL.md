---
name: nuxt-repositories
description: Repository pattern for API access with automatic model hydration. Use when creating repositories for API resources, configuring model hydration, adding custom API methods, or registering repositories in app config.
---

# Nuxt Repositories

Data access layer with CRUD operations and automatic model hydration.

## Core Concepts

**[repositories.md](references/repositories.md)** - Complete repository patterns, registration, custom methods

## Basic Repository

```typescript
// app/repositories/PostRepository.ts
import { BaseRepository } from '#layers/base/app/repositories/base-repository'
import { ModelHydrator } from '#layers/base/app/repositories/hydrators/model-hydrator'
import Post from '~/models/Post'

export default class PostRepository extends BaseRepository<Post> {
  protected resource = '/api/posts'
  protected hydration = true
  protected hydrator = new ModelHydrator(Post)

  // Custom method
  async listByAuthor(authorUlid: string) {
    return this.jsonGet(`/api/authors/${authorUlid}/posts`)
  }
}
```

## Registration

```typescript
// app/app.config.ts
export default defineAppConfig({
  repositories: {
    posts: PostRepository,
    authors: AuthorRepository,
  },
})
```

## Usage

```typescript
// Get typed repository instance
const postApi = useRepository('posts')

// CRUD operations (returns hydrated models)
const { data: posts } = await postApi.list()
const { data: post } = await postApi.get('ulid123')
const { data: newPost } = await postApi.create({ title: 'Hello' })
await postApi.update('ulid123', { title: 'Updated' })
await postApi.delete('ulid123')

// With query params
const { data: posts } = await postApi.list({
  include: 'author,comments',
  filter: { status: 'published' },
})
```
