---
name: nuxt-realtime
description: Real-time features with Laravel Echo and WebSockets. Use when subscribing to channels, listening for events, implementing live updates, or managing channel subscriptions.
---

# Nuxt Real-time

WebSocket real-time updates via Laravel Echo.

## Core Concepts

**[realtime.md](references/realtime.md)** - Complete real-time patterns

## Configuration

```typescript
// nuxt.config.ts
export default defineNuxtConfig({
  modules: ['nuxt-laravel-echo'],

  runtimeConfig: {
    public: {
      echo: {
        key: undefined,    // NUXT_PUBLIC_ECHO_KEY
        host: undefined,   // NUXT_PUBLIC_ECHO_HOST
        scheme: undefined, // NUXT_PUBLIC_ECHO_SCHEME
        port: undefined,   // NUXT_PUBLIC_ECHO_PORT
      },
    },
  },
})
```

## Channel Subscriptions

```typescript
const { privateChannel, presenceChannel, leaveChannel } = useRealtime()

// Subscribe to channel
const channel = privateChannel('posts.{id}', postId)

// Listen for events
channel.on('PostUpdated', (event) => {
  refresh()
})

// Multiple events
channel.on(['PostCreated', 'PostUpdated', 'PostDeleted'], refresh)

// Cleanup
onUnmounted(() => {
  leaveChannel('posts.{id}', postId)
})
```

## Constants

```typescript
// app/constants/channels.ts
export const Posts = 'posts'
export const Post = 'post.{post}'

// app/constants/events.ts
export const PostCreated = 'PostCreated'
export const PostUpdated = 'PostUpdated'
```
