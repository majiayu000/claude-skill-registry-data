---
name: Next.js 15+ Patterns
description: App Router, React Server Components, Server Actions (2025 best practices)
---

# Next.js 15+ Development Patterns

Modern Next.js development using App Router, React Server Components, and Server Actions.

## App Router Structure

### File-Based Routing

```
app/
├── layout.tsx          # Root layout (required)
├── page.tsx            # Home page
├── loading.tsx         # Loading UI
├── error.tsx           # Error UI
├── not-found.tsx       # 404 page
├── template.tsx        # Re-renders on navigation
├── (marketing)/        # Route group (doesn't affect URL)
│   ├── about/
│   │   └── page.tsx
│   └── contact/
│       └── page.tsx
├── blog/
│   ├── [slug]/         # Dynamic route
│   │   └── page.tsx
│   └── page.tsx
└── api/
    └── users/
        └── route.ts    # API route
```

### Routing Conventions

- `page.tsx` - UI for route
- `layout.tsx` - Shared UI for segment and children
- `loading.tsx` - Loading UI with Suspense
- `error.tsx` - Error UI with Error Boundary
- `not-found.tsx` - 404 UI
- `route.ts` - API endpoint

## Server vs Client Components

### Server Components (Default)

```tsx
// app/page.tsx - Server Component by default
import { db } from '@/lib/db';

export default async function HomePage() {
  // Can directly access database
  const posts = await db.post.findMany();

  return (
    <div>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
```

**Benefits**:
- Direct database access
- No client-side JS bundle
- Automatic code splitting
- Better SEO

**When to use**:
- Data fetching
- Backend logic
- Static content
- SEO-critical pages

### Client Components

```tsx
'use client'; // Required directive

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

**Require 'use client' when**:
- Using hooks (useState, useEffect, etc.)
- Event handlers (onClick, onChange, etc.)
- Browser APIs (window, localStorage, etc.)
- Third-party libraries that use hooks

**Best Practice**: Push 'use client' as deep as possible
```tsx
// ✅ Good: Only interactive part is client
export default async function Page() {
  const data = await fetchData(); // Server

  return (
    <div>
      <StaticHeader data={data} /> {/* Server */}
      <InteractiveButton /> {/* Client */}
    </div>
  );
}
```

## Server Actions

### Form Handling

```tsx
// app/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { db } from '@/lib/db';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;
  const content = formData.get('content') as string;

  // Validate
  if (!title || !content) {
    return { error: 'Title and content required' };
  }

  // Mutate
  await db.post.create({
    data: { title, content }
  });

  // Revalidate
  revalidatePath('/blog');

  return { success: true };
}
```

```tsx
// app/new-post/page.tsx
import { createPost } from '@/app/actions';

export default function NewPost() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit">Create</button>
    </form>
  );
}
```

**Progressive Enhancement**: Works without JavaScript!

### With useFormState (Client)

```tsx
'use client';

import { useFormState, useFormStatus } from 'react-dom';
import { createPost } from '@/app/actions';

export default function NewPostForm() {
  const [state, formAction] = useFormState(createPost, { error: null });

  return (
    <form action={formAction}>
      {state.error && <p className="error">{state.error}</p>}
      <input name="title" required />
      <textarea name="content" required />
      <SubmitButton />
    </form>
  );
}

function SubmitButton() {
  const { pending } = useFormStatus();

  return (
    <button type="submit" disabled={pending}>
      {pending ? 'Creating...' : 'Create'}
    </button>
  );
}
```

## Data Fetching

### Server Component Data Fetching

```tsx
// Automatic request deduplication
async function getPost(id: string) {
  const res = await fetch(`https://api.example.com/posts/${id}`, {
    next: { revalidate: 60 } // Revalidate every 60 seconds
  });

  return res.json();
}

export default async function PostPage({ params }: { params: { id: string } }) {
  const post = await getPost(params.id);

  return <div>{post.title}</div>;
}
```

### Parallel Data Fetching

```tsx
export default async function Page() {
  // Fetch in parallel
  const [user, posts, comments] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchComments()
  ]);

  return (
    <div>
      <UserProfile user={user} />
      <PostList posts={posts} />
      <Comments comments={comments} />
    </div>
  );
}
```

### Streaming with Suspense

```tsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>

      {/* Render immediately */}
      <Suspense fallback={<SkeletonUsers />}>
        <Users />
      </Suspense>

      {/* Stream when ready */}
      <Suspense fallback={<SkeletonPosts />}>
        <Posts />
      </Suspense>
    </div>
  );
}

async function Users() {
  const users = await fetchUsers(); // Can be slow
  return <UserList users={users} />;
}
```

## Caching & Revalidation

### Cache Strategies

```tsx
// Static (cache indefinitely)
fetch('https://api.example.com/data', {
  cache: 'force-cache'
});

// Dynamic (no cache)
fetch('https://api.example.com/data', {
  cache: 'no-store'
});

// Revalidate (cache with TTL)
fetch('https://api.example.com/data', {
  next: { revalidate: 3600 } // 1 hour
});

// Tag-based (revalidate by tag)
fetch('https://api.example.com/data', {
  next: { tags: ['posts'] }
});
```

### Revalidation Methods

```tsx
// app/actions.ts
'use server';

import { revalidatePath, revalidateTag } from 'next/cache';

export async function updatePost(id: string) {
  await db.post.update({ where: { id }, data: { ... } });

  // Revalidate specific path
  revalidatePath('/blog');
  revalidatePath(`/blog/${id}`);

  // Or revalidate by tag
  revalidateTag('posts');
}
```

## Metadata & SEO

### Static Metadata

```tsx
// app/blog/page.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Blog',
  description: 'My blog posts',
  openGraph: {
    title: 'Blog',
    description: 'My blog posts',
    images: ['/og-image.jpg']
  }
};

export default function BlogPage() {
  return <div>...</div>;
}
```

### Dynamic Metadata

```tsx
export async function generateMetadata({
  params
}: {
  params: { slug: string }
}): Promise<Metadata> {
  const post = await fetchPost(params.slug);

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [post.ogImage]
    }
  };
}
```

## Route Handlers (API Routes)

```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { db } from '@/lib/db';

export async function GET(request: NextRequest) {
  const users = await db.user.findMany();
  return NextResponse.json(users);
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  const user = await db.user.create({
    data: body
  });

  return NextResponse.json(user, { status: 201 });
}
```

### Dynamic Route Handlers

```tsx
// app/api/users/[id]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const user = await db.user.findUnique({
    where: { id: params.id }
  });

  if (!user) {
    return NextResponse.json(
      { error: 'User not found' },
      { status: 404 }
    );
  }

  return NextResponse.json(user);
}
```

## Performance Optimization

### Image Optimization

```tsx
import Image from 'next/image';

export default function Avatar() {
  return (
    <Image
      src="/avatar.jpg"
      alt="User avatar"
      width={200}
      height={200}
      priority // Above fold
      placeholder="blur" // Show blur while loading
      blurDataURL="data:image/..." // Inline blur
    />
  );
}
```

### Font Optimization

```tsx
// app/layout.tsx
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter'
});

export default function RootLayout({ children }) {
  return (
    <html className={inter.variable}>
      <body>{children}</body>
    </html>
  );
}
```

### Code Splitting

```tsx
import dynamic from 'next/dynamic';

// Lazy load heavy component
const HeavyChart = dynamic(() => import('@/components/Chart'), {
  loading: () => <p>Loading chart...</p>,
  ssr: false // Don't render on server
});
```

## Error Handling

### Error Boundaries

```tsx
// app/blog/error.tsx
'use client';

export default function Error({
  error,
  reset
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={() => reset()}>Try again</button>
    </div>
  );
}
```

### Not Found

```tsx
// app/blog/[slug]/not-found.tsx
export default function NotFound() {
  return <h2>Blog post not found</h2>;
}

// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation';

export default async function PostPage({ params }) {
  const post = await fetchPost(params.slug);

  if (!post) {
    notFound(); // Renders not-found.tsx
  }

  return <div>{post.title}</div>;
}
```

## Common Patterns

### Loading States

```tsx
// Use Suspense for granular loading
<Suspense fallback={<Skeleton />}>
  <SlowComponent />
</Suspense>

// Or loading.tsx for entire route
// app/dashboard/loading.tsx
export default function Loading() {
  return <DashboardSkeleton />;
}
```

### Optimistic Updates

```tsx
'use client';

import { useOptimistic } from 'react';
import { likePost } from '@/app/actions';

export default function LikeButton({ postId, likes }) {
  const [optimisticLikes, addOptimisticLike] = useOptimistic(
    likes,
    (state, newLike) => state + 1
  );

  async function handleLike() {
    addOptimisticLike(1); // Update UI immediately
    await likePost(postId); // Then update server
  }

  return (
    <button onClick={handleLike}>
      Likes: {optimisticLikes}
    </button>
  );
}
```

## Anti-Patterns to Avoid

❌ **Don't use 'use client' at root unnecessarily**
```tsx
// Bad - entire page is client
'use client';

export default function Page() {
  return <div>Static content</div>;
}
```

❌ **Don't fetch in Client Components**
```tsx
// Bad - defeats purpose of Server Components
'use client';

export default function Users() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    fetch('/api/users').then(/* ... */);
  }, []);

  // Use Server Component instead!
}
```

❌ **Don't forget revalidation after mutations**
```tsx
// Bad - stale data
export async function deletePost(id) {
  await db.post.delete({ where: { id } });
  // Missing: revalidatePath('/blog');
}
```

## Resources

See `resources/` directory for detailed patterns:
- [app-router.md](resources/app-router.md) - Advanced routing
- [server-components.md](resources/server-components.md) - Deep dive
- [server-actions.md](resources/server-actions.md) - Form handling
- [data-fetching.md](resources/data-fetching.md) - Caching strategies
- [performance.md](resources/performance.md) - Optimization techniques
