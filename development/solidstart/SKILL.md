---
name: solidstart
description: Builds full-stack applications with SolidStart, combining Solid's fine-grained reactivity with server functions and multiple rendering modes. Use when creating SolidJS applications with SSR/SSG, server functions, or when user mentions SolidStart or Solid meta-framework.
---

# SolidStart

Meta-framework for SolidJS combining fine-grained reactivity with full-stack capabilities, built on Vinxi (Vite + Nitro).

## Quick Start

```bash
# Create new project
npm init solid@latest my-app

# Select:
# - SolidStart
# - TypeScript (recommended)
# - SSR (default)

cd my-app
npm install
npm run dev
```

## Project Structure

```
my-app/
  app.config.ts       # App configuration
  src/
    app.tsx           # Root component
    entry-client.tsx  # Client entry
    entry-server.tsx  # Server entry
    routes/           # File-based routing
      index.tsx       # /
      about.tsx       # /about
      blog/
        index.tsx     # /blog
        [slug].tsx    # /blog/:slug
      api/
        users.ts      # /api/users endpoint
    components/       # Shared components
    lib/              # Utilities
  public/             # Static assets
```

## App Configuration

```typescript
// app.config.ts
import { defineConfig } from "@solidjs/start/config";

export default defineConfig({
  server: {
    preset: "vercel", // netlify, cloudflare-pages, node, etc.
  },
  vite: {
    // Vite configuration
    plugins: [],
  },
});
```

## Routing

### Basic Routes

```tsx
// src/routes/index.tsx
export default function Home() {
  return (
    <main>
      <h1>Welcome to SolidStart</h1>
      <p>Fine-grained reactivity meets full-stack</p>
    </main>
  );
}
```

### File System Routing

```
routes/
  index.tsx           # /
  about.tsx           # /about
  blog.tsx            # /blog (layout)
  blog/
    index.tsx         # /blog
    [slug].tsx        # /blog/:slug
    [...rest].tsx     # /blog/* (catch-all)
  (auth)/             # Route group (no URL segment)
    login.tsx         # /login
    register.tsx      # /register
```

### Dynamic Routes

```tsx
// src/routes/blog/[slug].tsx
import { useParams } from "@solidjs/router";

export default function BlogPost() {
  const params = useParams<{ slug: string }>();

  return (
    <article>
      <h1>Post: {params.slug}</h1>
    </article>
  );
}
```

### Route Groups & Layouts

```tsx
// src/routes/blog.tsx - Layout for /blog/*
import { RouteSectionProps } from "@solidjs/router";

export default function BlogLayout(props: RouteSectionProps) {
  return (
    <div class="blog-layout">
      <aside>
        <nav>Blog Navigation</nav>
      </aside>
      <main>{props.children}</main>
    </div>
  );
}
```

### Navigation

```tsx
import { A, useNavigate } from "@solidjs/router";

function Navigation() {
  const navigate = useNavigate();

  return (
    <nav>
      {/* Link component with active states */}
      <A href="/" activeClass="active" end>Home</A>
      <A href="/blog" activeClass="active">Blog</A>

      {/* Programmatic navigation */}
      <button onClick={() => navigate("/dashboard")}>
        Go to Dashboard
      </button>
    </nav>
  );
}
```

## Data Loading

### Server Functions with `query`

```tsx
// src/routes/users/index.tsx
import { createAsync, query } from "@solidjs/router";
import { For, Suspense } from "solid-js";

// Define server query
const getUsers = query(async () => {
  "use server";
  const users = await db.users.findMany();
  return users;
}, "users");

export default function UsersPage() {
  const users = createAsync(() => getUsers());

  return (
    <Suspense fallback={<div>Loading users...</div>}>
      <ul>
        <For each={users()}>
          {(user) => <li>{user.name}</li>}
        </For>
      </ul>
    </Suspense>
  );
}
```

### Parameterized Queries

```tsx
// src/routes/users/[id].tsx
import { createAsync, query, useParams } from "@solidjs/router";
import { Show, Suspense } from "solid-js";

const getUser = query(async (id: string) => {
  "use server";
  const user = await db.users.findUnique({ where: { id } });
  return user;
}, "user");

export default function UserPage() {
  const params = useParams<{ id: string }>();
  const user = createAsync(() => getUser(params.id));

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Show when={user()} fallback={<div>User not found</div>}>
        {(u) => (
          <div>
            <h1>{u().name}</h1>
            <p>{u().email}</p>
          </div>
        )}
      </Show>
    </Suspense>
  );
}
```

### Preloading Data

```tsx
// src/routes/products/[id].tsx
import { createAsync, query, type RouteDefinition } from "@solidjs/router";

const getProduct = query(async (id: string) => {
  "use server";
  return await db.products.findUnique({ where: { id } });
}, "product");

// Preload on hover/focus
export const route = {
  preload: ({ params }) => getProduct(params.id),
} satisfies RouteDefinition;

export default function ProductPage() {
  const params = useParams<{ id: string }>();
  const product = createAsync(() => getProduct(params.id));

  return (
    <Suspense>
      <Show when={product()}>
        {(p) => <ProductDetail product={p()} />}
      </Show>
    </Suspense>
  );
}
```

## Server Actions

### Basic Action

```tsx
// src/routes/contact.tsx
import { action, useSubmission } from "@solidjs/router";

const submitContact = action(async (formData: FormData) => {
  "use server";
  const email = formData.get("email") as string;
  const message = formData.get("message") as string;

  await sendEmail({ to: "support@example.com", from: email, body: message });

  return { success: true };
});

export default function ContactPage() {
  const submission = useSubmission(submitContact);

  return (
    <form action={submitContact} method="post">
      <input name="email" type="email" required />
      <textarea name="message" required />

      <button type="submit" disabled={submission.pending}>
        {submission.pending ? "Sending..." : "Send"}
      </button>

      <Show when={submission.result?.success}>
        <p class="success">Message sent!</p>
      </Show>
    </form>
  );
}
```

### Action with Validation

```tsx
import { action, redirect } from "@solidjs/router";
import { z } from "zod";

const createPostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(10),
});

const createPost = action(async (formData: FormData) => {
  "use server";

  const data = Object.fromEntries(formData);
  const result = createPostSchema.safeParse(data);

  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors };
  }

  const post = await db.posts.create({
    data: result.data,
  });

  throw redirect(`/blog/${post.slug}`);
});

export default function NewPost() {
  const submission = useSubmission(createPost);
  const errors = () => submission.result?.errors;

  return (
    <form action={createPost} method="post">
      <div>
        <input name="title" placeholder="Title" />
        <Show when={errors()?.title}>
          <span class="error">{errors()!.title![0]}</span>
        </Show>
      </div>

      <div>
        <textarea name="content" placeholder="Content" />
        <Show when={errors()?.content}>
          <span class="error">{errors()!.content![0]}</span>
        </Show>
      </div>

      <button type="submit">Create Post</button>
    </form>
  );
}
```

### Revalidation

```tsx
import { action, revalidate } from "@solidjs/router";

const deletePost = action(async (id: string) => {
  "use server";
  await db.posts.delete({ where: { id } });

  // Revalidate cached queries
  revalidate("posts");
  revalidate("user-posts");
});

// Usage
<button onClick={() => deletePost(post.id)}>Delete</button>
```

## API Routes

### GET Endpoint

```typescript
// src/routes/api/users.ts
import { json } from "@solidjs/router";
import type { APIEvent } from "@solidjs/start/server";

export async function GET(event: APIEvent) {
  const users = await db.users.findMany();

  return json(users, {
    headers: {
      "Cache-Control": "public, max-age=60",
    },
  });
}
```

### POST with Body

```typescript
// src/routes/api/users.ts
export async function POST(event: APIEvent) {
  const body = await event.request.json();

  const user = await db.users.create({
    data: body,
  });

  return json(user, { status: 201 });
}
```

### Dynamic API Routes

```typescript
// src/routes/api/users/[id].ts
import { json } from "@solidjs/router";
import type { APIEvent } from "@solidjs/start/server";

export async function GET(event: APIEvent) {
  const id = event.params.id;
  const user = await db.users.findUnique({ where: { id } });

  if (!user) {
    return json({ error: "Not found" }, { status: 404 });
  }

  return json(user);
}

export async function DELETE(event: APIEvent) {
  const id = event.params.id;
  await db.users.delete({ where: { id } });

  return new Response(null, { status: 204 });
}
```

## Middleware

```typescript
// src/middleware.ts
import { createMiddleware } from "@solidjs/start/middleware";

export default createMiddleware({
  onRequest: [
    // Authentication middleware
    async (event) => {
      const session = event.request.headers.get("Authorization");

      if (event.request.url.includes("/api/protected")) {
        if (!session) {
          return new Response("Unauthorized", { status: 401 });
        }
      }
    },

    // Logging middleware
    async (event) => {
      console.log(`${event.request.method} ${event.request.url}`);
    },
  ],
});
```

## Authentication Pattern

```tsx
// src/lib/auth.ts
import { query, action, redirect } from "@solidjs/router";
import { getRequestEvent } from "solid-js/web";

export const getUser = query(async () => {
  "use server";
  const event = getRequestEvent()!;
  const session = event.request.headers.get("cookie");

  if (!session) return null;

  return await validateSession(session);
}, "user");

export const login = action(async (formData: FormData) => {
  "use server";
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;

  const user = await authenticateUser(email, password);

  if (!user) {
    return { error: "Invalid credentials" };
  }

  const event = getRequestEvent()!;
  // Set cookie
  event.response.headers.set(
    "Set-Cookie",
    `session=${user.sessionId}; HttpOnly; Path=/`
  );

  throw redirect("/dashboard");
});

export const logout = action(async () => {
  "use server";
  const event = getRequestEvent()!;
  event.response.headers.set(
    "Set-Cookie",
    "session=; HttpOnly; Path=/; Max-Age=0"
  );

  throw redirect("/");
});
```

## SEO & Metadata

```tsx
// src/routes/blog/[slug].tsx
import { Title, Meta } from "@solidjs/meta";
import { createAsync, query, useParams } from "@solidjs/router";

const getPost = query(async (slug: string) => {
  "use server";
  return await db.posts.findUnique({ where: { slug } });
}, "post");

export default function BlogPost() {
  const params = useParams<{ slug: string }>();
  const post = createAsync(() => getPost(params.slug));

  return (
    <Suspense>
      <Show when={post()}>
        {(p) => (
          <>
            <Title>{p().title} | My Blog</Title>
            <Meta name="description" content={p().excerpt} />
            <Meta property="og:title" content={p().title} />
            <Meta property="og:description" content={p().excerpt} />
            <Meta property="og:image" content={p().image} />

            <article>
              <h1>{p().title}</h1>
              <div innerHTML={p().content} />
            </article>
          </>
        )}
      </Show>
    </Suspense>
  );
}
```

## Error Handling

```tsx
// src/routes/[...404].tsx
export default function NotFound() {
  return (
    <main>
      <h1>404 - Page Not Found</h1>
      <A href="/">Go Home</A>
    </main>
  );
}

// Error boundary in layout
import { ErrorBoundary } from "solid-js";

export default function RootLayout(props: RouteSectionProps) {
  return (
    <ErrorBoundary
      fallback={(err, reset) => (
        <div class="error">
          <h1>Something went wrong</h1>
          <pre>{err.message}</pre>
          <button onClick={reset}>Try Again</button>
        </div>
      )}
    >
      {props.children}
    </ErrorBoundary>
  );
}
```

## Rendering Modes

### SSR (Default)

```typescript
// app.config.ts
export default defineConfig({
  server: {
    preset: "node",
  },
});
```

### Static Site Generation (SSG)

```typescript
// app.config.ts
export default defineConfig({
  server: {
    preset: "static",
    prerender: {
      routes: ["/", "/about", "/blog"],
      // Or crawl from root
      crawlLinks: true,
    },
  },
});
```

### Client-Side Only

```tsx
import { clientOnly } from "@solidjs/start";

const Chart = clientOnly(() => import("./Chart"));

export default function Dashboard() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Chart fallback={<div>Loading chart...</div>} />
    </div>
  );
}
```

## Deployment

```bash
# Build for production
npm run build

# Deployment presets:
# - vercel
# - netlify
# - cloudflare-pages
# - cloudflare-workers
# - node
# - static
# - aws-lambda
# - deno

# Example: Vercel
npm run build
vercel deploy
```

## Reference Files

- [server-patterns.md](references/server-patterns.md) - Advanced server function patterns
- [streaming-ssr.md](references/streaming-ssr.md) - Streaming SSR and progressive rendering
