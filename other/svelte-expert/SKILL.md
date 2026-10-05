---
name: svelte-expert
description: Deep Svelte 5 and SvelteKit expertise for runes reactivity, component patterns, server-side rendering, form actions, and deployment. Use when building.
---

# Svelte Expert

Specialized expertise in Svelte 5 and SvelteKit development, providing deep guidance on the runes reactivity system, component composition with snippets, SvelteKit file-based routing, server-side data loading, form actions with progressive enhancement, state management, hooks and middleware, performance optimization, and testing with Vitest and Playwright.

## When to Use This Skill

Use this skill for:

- Building new SvelteKit applications with Svelte 5 runes
- Migrating from Svelte 4 stores to Svelte 5 runes reactivity
- Designing component architectures with snippets, two-way binding, and composition
- Implementing server-side data loading with load functions
- Building form mutations with form actions and progressive enhancement
- Managing shared state with rune-based stores and context API
- Configuring SvelteKit hooks for authentication, error handling, and request modification
- Optimizing performance with fine-grained reactivity, prerendering, and adapter selection
- Writing component tests with @testing-library/svelte and E2E tests with Playwright

**Trigger phrases**: "svelte", "sveltekit", "svelte 5", "runes", "$state", "$derived", "$effect", "$props", "svelte component", "svelte routing", "svelte form actions", "svelte load function", "svelte store", "svelte hooks", "svelte transition", "svelte animation"

## What This Skill Does

Provides Svelte 5 and SvelteKit expertise including:

- **Runes Reactivity**: $state, $derived, $effect, $props, $bindable, $inspect for fine-grained reactivity
- **Component Patterns**: Snippets, event handling, two-way binding, component composition
- **SvelteKit Routing**: File-based routing, layouts, route params, groups, error pages
- **Data Loading**: Load functions, form actions, progressive enhancement, streaming
- **State Management**: Shared rune stores, context API with getContext/setContext, derived state
- **Hooks and Middleware**: handle, handleFetch, handleError, environment variables, service workers
- **Performance**: Fine-grained reactivity, transitions, animations, lazy loading, prerendering, adapters
- **Testing**: Component testing with Vitest and @testing-library/svelte, E2E with Playwright

## Instructions

### Step 1: Master Svelte 5 Runes Fundamentals

Svelte 5 replaces stores and reactive declarations with runes, a set of compiler-level primitives for fine-grained reactivity.

**$state: reactive state declaration**:

```svelte
<script lang="ts">
  let count = $state(0);
  let user = $state<{ name: string; email: string }>({
    name: "Alice",
    email: "alice@example.com",
  });

  // $state creates deeply reactive objects; nested mutations trigger updates
  function updateEmail(email: string) {
    user.email = email; // Triggers reactivity without reassignment
  }
</script>

<button onclick={() => count++}>
  Clicked {count} {count === 1 ? "time" : "times"}
</button>
<p>{user.name} ({user.email})</p>
```

**$state.raw: non-deeply-reactive state for large objects**:

```svelte
<script lang="ts">
  // Use $state.raw when you do not need deep reactivity (large arrays, immutable data)
  let items = $state.raw<string[]>([]);

  function setItems(newItems: string[]) {
    items = newItems; // Must reassign the entire value; mutations are not tracked
  }
</script>
```

**$derived: computed values that update automatically**:

```svelte
<script lang="ts">
  let items = $state<{ name: string; price: number; quantity: number }[]>([
    { name: "Widget", price: 9.99, quantity: 3 },
    { name: "Gadget", price: 24.99, quantity: 1 },
  ]);

  let total = $derived(
    items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  );

  let formattedTotal = $derived(`$${total.toFixed(2)}`);

  // $derived.by for multi-statement computations
  let summary = $derived.by(() => {
    const count = items.length;
    const avgPrice = count > 0 ? total / count : 0;
    return { count, avgPrice, total };
  });
</script>

<p>Cart: {summary.count} items, total {formattedTotal}</p>
```

**$effect: side effects that run when dependencies change**:

```svelte
<script lang="ts">
  let query = $state("");
  let results = $state<string[]>([]);

  // $effect tracks which reactive values are read and reruns when they change
  $effect(() => {
    if (query.length < 2) {
      results = [];
      return;
    }

    const controller = new AbortController();

    fetch(`/api/search?q=${encodeURIComponent(query)}`, {
      signal: controller.signal,
    })
      .then((res) => res.json())
      .then((data) => {
        results = data.items;
      })
      .catch((err) => {
        if (err.name !== "AbortError") console.error(err);
      });

    // Return a cleanup function (runs before the effect re-executes)
    return () => controller.abort();
  });
</script>

<input bind:value={query} placeholder="Search..." />
<ul>
  {#each results as result}
    <li>{result}</li>
  {/each}
</ul>
```

**$props and $bindable: component inputs**:

```ts
// UserCard.svelte
<script lang="ts">
  interface Props {
    name: string;
    email: string;
    role?: "admin" | "user";
    onSave?: (data: { name: string; email: string }) => void;
  }

  let { name, email, role = "user", onSave }: Props = $props();
</script>

<div class="card">
  <h3>{name}</h3>
  <p>{email} ({role})</p>
  {#if onSave}
    <button onclick={() => onSave?.({ name, email })}>Save</button>
  {/if}
</div>
```

**$bindable: props that support two-way binding**:

```svelte
<!-- TextInput.svelte -->
<script lang="ts">
  interface Props {
    value: string;
    placeholder?: string;
  }

  let { value = $bindable(""), placeholder = "" }: Props = $props();
</script>

<input bind:value {placeholder} />

<!-- Parent.svelte -->
<script lang="ts">
  import TextInput from "./TextInput.svelte";

  let searchQuery = $state("");
</script>

<TextInput bind:value={searchQuery} placeholder="Search..." />
<p>Current query: {searchQuery}</p>
```

### Step 2: Build Component Patterns

**Snippets: the Svelte 5 replacement for slots**:

```svelte
<!-- Card.svelte -->
<script lang="ts">
  import type { Snippet } from "svelte";

  interface Props {
    header: Snippet;
    children: Snippet;
    footer?: Snippet;
  }

  let { header, children, footer }: Props = $props();
</script>

<div class="card">
  <div class="card-header">
    {@render header()}
  </div>
  <div class="card-body">
    {@render children()}
  </div>
  {#if footer}
    <div class="card-footer">
      {@render footer()}
    </div>
  {/if}
</div>

<!-- Usage -->
<script lang="ts">
  import Card from "./Card.svelte";
</script>

<Card>
  {#snippet header()}
    <h2>User Profile</h2>
  {/snippet}

  <p>This is the card body content.</p>

  {#snippet footer()}
    <button>Save Changes</button>
  {/snippet}
</Card>
```

**Typed snippets with parameters**:

```svelte
<!-- DataList.svelte -->
<script lang="ts" generics="T">
  import type { Snippet } from "svelte";

  interface Props {
    items: T[];
    renderItem: Snippet<[T, number]>;
    empty?: Snippet;
  }

  let { items, renderItem, empty }: Props = $props();
</script>

{#if items.length === 0}
  {#if empty}
    {@render empty()}
  {:else}
    <p>No items found.</p>
  {/if}
{:else}
  <ul>
    {#each items as item, index}
      <li>{@render renderItem(item, index)}</li>
    {/each}
  </ul>
{/if}

<!-- Usage -->
<script lang="ts">
  import DataList from "./DataList.svelte";

  interface User {
    id: string;
    name: string;
    email: string;
  }

  let users = $state<User[]>([
    { id: "1", name: "Alice", email: "alice@example.com" },
    { id: "2", name: "Bob", email: "bob@example.com" },
  ]);
</script>

<DataList items={users}>
  {#snippet renderItem(user, index)}
    <span>{index + 1}. {user.name} ({user.email})</span>
  {/snippet}
  {#snippet empty()}
    <p>No users registered yet.</p>
  {/snippet}
</DataList>
```

**Event handling and component composition**:

```svelte
<!-- SearchForm.svelte -->
<script lang="ts">
  interface Props {
    onSearch: (query: string) => void;
    initialQuery?: string;
  }

  let { onSearch, initialQuery = "" }: Props = $props();
  let query = $state(initialQuery);
  let inputRef = $state<HTMLInputElement | null>(null);

  function handleSubmit(event: SubmitEvent) {
    event.preventDefault();
    const trimmed = query.trim();
    if (trimmed.length > 0) {
      onSearch(trimmed);
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      query = "";
      inputRef?.focus();
    }
  }

  // Focus input on mount
  $effect(() => {
    inputRef?.focus();
  });
</script>

<form onsubmit={handleSubmit}>
  <input
    bind:this={inputRef}
    bind:value={query}
    onkeydown={handleKeydown}
    placeholder="Search..."
    aria-label="Search"
  />
  <button type="submit">Search</button>
</form>
```

**Two-way binding with custom components**:

```svelte
<!-- ColorPicker.svelte -->
<script lang="ts">
  interface Props {
    color: string;
    label?: string;
  }

  let { color = $bindable("#000000"), label = "Color" }: Props = $props();

  let hue = $derived(hexToHue(color));

  function hexToHue(hex: string): number {
    // Simplified hex-to-hue conversion
    const r = parseInt(hex.slice(1, 3), 16) / 255;
    const g = parseInt(hex.slice(3, 5), 16) / 255;
    const b = parseInt(hex.slice(5, 7), 16) / 255;
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    if (max === min) return 0;
    const d = max - min;
    let h = 0;
    if (max === r) h = ((g - b) / d + 6) % 6;
    else if (max === g) h = (b - r) / d + 2;
    else h = (r - g) / d + 4;
    return Math.round(h * 60);
  }
</script>

<label>
  {label} (hue: {hue})
  <input type="color" bind:value={color} />
</label>
```

### Step 3: Structure SvelteKit Routing

**Standard SvelteKit file structure**:

```
src/
  routes/
    +page.svelte              # Home page (/)
    +layout.svelte            # Root layout
    +layout.server.ts         # Root layout server load
    +error.svelte             # Root error page
    about/
      +page.svelte            # /about
    blog/
      +page.svelte            # /blog (list)
      +page.server.ts         # Blog list data loading
      [slug]/
        +page.svelte          # /blog/:slug (dynamic)
        +page.server.ts       # Single post data loading
    dashboard/
      +layout.svelte          # Dashboard layout (nested)
      +layout.server.ts       # Dashboard auth check
      +page.svelte            # /dashboard
      settings/
        +page.svelte          # /dashboard/settings
    api/
      health/
        +server.ts            # GET /api/health
      users/
        +server.ts            # GET/POST /api/users
        [id]/
          +server.ts          # GET/PUT/DELETE /api/users/:id
    (marketing)/              # Route group (no URL segment)
      pricing/
        +page.svelte          # /pricing
      contact/
        +page.svelte          # /contact
  lib/
    server/                   # Server-only modules ($lib/server/)
      db.ts
      auth.ts
    components/               # Shared components ($lib/components/)
    stores/                   # Shared state ($lib/stores/)
```

**Root layout with navigation**:

```svelte
<!-- src/routes/+layout.svelte -->
<script lang="ts">
  import type { LayoutData } from "./$types";
  import { page } from "$app/stores";

  let { data, children }: { data: LayoutData; children: any } = $props();
</script>

<div class="app">
  <header>
    <nav aria-label="Main navigation">
      <a href="/" class:active={$page.url.pathname === "/"}>Home</a>
      <a href="/blog" class:active={$page.url.pathname.startsWith("/blog")}>Blog</a>
      <a href="/dashboard" class:active={$page.url.pathname.startsWith("/dashboard")}>
        Dashboard
      </a>
      {#if data.user}
        <span>Welcome, {data.user.name}</span>
      {:else}
        <a href="/login">Sign In</a>
      {/if}
    </nav>
  </header>
  <main>
    {@render children()}
  </main>
  <footer>
    <p>Built with SvelteKit</p>
  </footer>
</div>

<style>
  .active {
    font-weight: bold;
    text-decoration: underline;
  }
</style>
```

**Dynamic route with params and error handling**:

```svelte
<!-- src/routes/blog/[slug]/+page.svelte -->
<script lang="ts">
  import type { PageData } from "./$types";

  let { data }: { data: PageData } = $props();
</script>

<svelte:head>
  <title>{data.post.title} | My Blog</title>
  <meta name="description" content={data.post.excerpt} />
</svelte:head>

<article>
  <h1>{data.post.title}</h1>
  <time datetime={data.post.publishedAt}>
    {new Date(data.post.publishedAt).toLocaleDateString()}
  </time>
  <div class="content">
    {@html data.post.htmlContent}
  </div>
</article>
```

**Route groups and layout resets**:

```svelte
<!-- src/routes/(marketing)/+layout.svelte -->
<script lang="ts">
  // Marketing pages get a different layout than the dashboard
  let { children }: { children: any } = $props();
</script>

<div class="marketing-layout">
  <header class="marketing-header">
    <a href="/">Brand Logo</a>
    <a href="/pricing">Pricing</a>
    <a href="/contact">Contact</a>
  </header>
  {@render children()}
</div>
```

**API route handlers (+server.ts)**:

```ts
// src/routes/api/users/+server.ts
import { json, error } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";
import { db } from "$lib/server/db";

export const GET: RequestHandler = async ({ url }) => {
  const page = parseInt(url.searchParams.get("page") ?? "1", 10);
  const limit = parseInt(url.searchParams.get("limit") ?? "20", 10);

  const users = await db.user.findMany({
    skip: (page - 1) * limit,
    take: limit,
  });

  return json({ data: users, page, limit });
};

export const POST: RequestHandler = async ({ request }) => {
  const body = await request.json();

  if (!body.email || !body.name) {
    error(400, { message: "Name and email are required" });
  }

  const user = await db.user.create({ data: body });
  return json(user, { status: 201 });
};
```

### Step 4: Implement Data Loading and Form Actions

**Server load functions (+page.server.ts)**:

```ts
// src/routes/blog/+page.server.ts
import type { PageServerLoad } from "./$types";
import { db } from "$lib/server/db";

export const load: PageServerLoad = async ({ url, depends }) => {
  const page = parseInt(url.searchParams.get("page") ?? "1", 10);
  const limit = 10;

  // depends() registers a custom invalidation key
  depends("app:posts");

  const [posts, total] = await Promise.all([
    db.post.findMany({
      skip: (page - 1) * limit,
      take: limit,
      orderBy: { publishedAt: "desc" },
      select: { slug: true, title: true, excerpt: true, publishedAt: true },
    }),
    db.post.count(),
  ]);

  return {
    posts,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  };
};
```

**Dynamic route load with error handling**:

```ts
// src/routes/blog/[slug]/+page.server.ts
import { error } from "@sveltejs/kit";
import type { PageServerLoad } from "./$types";
import { db } from "$lib/server/db";

export const load: PageServerLoad = async ({ params }) => {
  const post = await db.post.findUnique({
    where: { slug: params.slug },
  });

  if (!post) {
    error(404, { message: `Post "${params.slug}" not found` });
  }

  return { post };
};
```

**Form actions with progressive enhancement**:

```ts
// src/routes/blog/new/+page.server.ts
import { fail, redirect } from "@sveltejs/kit";
import type { Actions, PageServerLoad } from "./$types";
import { db } from "$lib/server/db";
import { z } from "zod";

const CreatePostSchema = z.object({
  title: z.string().min(1, "Title is required").max(200),
  content: z.string().min(10, "Content must be at least 10 characters"),
  published: z.boolean().default(false),
});

export const load: PageServerLoad = async ({ locals }) => {
  if (!locals.user) {
    redirect(302, "/login");
  }
  return {};
};

export const actions = {
  default: async ({ request, locals }) => {
    const formData = await request.formData();

    const parsed = CreatePostSchema.safeParse({
      title: formData.get("title"),
      content: formData.get("content"),
      published: formData.has("published"),
    });

    if (!parsed.success) {
      return fail(400, {
        errors: parsed.error.flatten().fieldErrors,
        values: {
          title: formData.get("title") as string,
          content: formData.get("content") as string,
        },
      });
    }

    const post = await db.post.create({
      data: {
        ...parsed.data,
        slug: parsed.data.title.toLowerCase().replace(/\s+/g, "-"),
        authorId: locals.user!.id,
      },
    });

    redirect(303, `/blog/${post.slug}`);
  },
} satisfies Actions;
```

**Form component with progressive enhancement**:

```svelte
<!-- src/routes/blog/new/+page.svelte -->
<script lang="ts">
  import { enhance } from "$app/forms";
  import type { ActionData } from "./$types";

  let { form }: { form: ActionData } = $props();
  let submitting = $state(false);
</script>

<h1>New Blog Post</h1>

<form
  method="POST"
  use:enhance={() => {
    submitting = true;
    return async ({ update }) => {
      submitting = false;
      await update();
    };
  }}
>
  <label for="title">Title</label>
  <input
    id="title"
    name="title"
    value={form?.values?.title ?? ""}
    required
    aria-invalid={form?.errors?.title ? "true" : undefined}
    aria-describedby={form?.errors?.title ? "title-error" : undefined}
  />
  {#if form?.errors?.title}
    <p id="title-error" class="error">{form.errors.title[0]}</p>
  {/if}

  <label for="content">Content</label>
  <textarea
    id="content"
    name="content"
    required
    aria-invalid={form?.errors?.content ? "true" : undefined}
    aria-describedby={form?.errors?.content ? "content-error" : undefined}
  >{form?.values?.content ?? ""}</textarea>
  {#if form?.errors?.content}
    <p id="content-error" class="error">{form.errors.content[0]}</p>
  {/if}

  <label>
    <input type="checkbox" name="published" />
    Publish immediately
  </label>

  <button type="submit" disabled={submitting}>
    {submitting ? "Creating..." : "Create Post"}
  </button>
</form>
```

**Streaming with promises in load functions**:

```ts
// src/routes/dashboard/+page.server.ts
import type { PageServerLoad } from "./$types";
import { db } from "$lib/server/db";

export const load: PageServerLoad = async ({ locals }) => {
  // Return fast data immediately, stream slow data
  const quickStats = await db.stats.getQuick(locals.user!.id);

  return {
    stats: quickStats,
    // These promises stream to the client as they resolve
    recentActivity: db.activity.findRecent(locals.user!.id),
    recommendations: db.recommendations.generate(locals.user!.id),
  };
};
```

```svelte
<!-- src/routes/dashboard/+page.svelte -->
<script lang="ts">
  import type { PageData } from "./$types";

  let { data }: { data: PageData } = $props();
</script>

<h1>Dashboard</h1>

<!-- Immediately available -->
<div class="stats">
  <p>Total posts: {data.stats.postCount}</p>
  <p>Total views: {data.stats.viewCount}</p>
</div>

<!-- Streamed in when ready -->
{#await data.recentActivity}
  <div class="skeleton">Loading recent activity...</div>
{:then activity}
  <ul>
    {#each activity as item}
      <li>{item.description} - {item.timestamp}</li>
    {/each}
  </ul>
{:catch error}
  <p class="error">Failed to load activity: {error.message}</p>
{/await}

{#await data.recommendations}
  <div class="skeleton">Generating recommendations...</div>
{:then recs}
  <ul>
    {#each recs as rec}
      <li>{rec.title}</li>
    {/each}
  </ul>
{:catch}
  <p class="error">Could not generate recommendations.</p>
{/await}
```

### Step 5: Manage State

**Shared rune-based stores**:

```ts
// src/lib/stores/cart.svelte.ts
interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

function createCartStore() {
  let items = $state<CartItem[]>([]);

  let total = $derived(
    items.reduce((sum, item) => sum + item.price * item.quantity, 0)
  );

  let count = $derived(
    items.reduce((sum, item) => sum + item.quantity, 0)
  );

  function addItem(product: Omit<CartItem, "quantity">) {
    const existing = items.find((item) => item.id === product.id);
    if (existing) {
      existing.quantity += 1;
    } else {
      items.push({ ...product, quantity: 1 });
    }
  }

  function removeItem(id: string) {
    const index = items.findIndex((item) => item.id === id);
    if (index !== -1) {
      items.splice(index, 1);
    }
  }

  function updateQuantity(id: string, quantity: number) {
    const item = items.find((i) => i.id === id);
    if (item) {
      item.quantity = Math.max(0, quantity);
      if (item.quantity === 0) removeItem(id);
    }
  }

  function clear() {
    items.length = 0;
  }

  return {
    get items() { return items; },
    get total() { return total; },
    get count() { return count; },
    addItem,
    removeItem,
    updateQuantity,
    clear,
  };
}

export const cart = createCartStore();
```

```svelte
<!-- CartWidget.svelte -->
<script lang="ts">
  import { cart } from "$lib/stores/cart.svelte";
</script>

<div class="cart-widget">
  <span>Cart ({cart.count} items): ${cart.total.toFixed(2)}</span>
  {#each cart.items as item}
    <div class="cart-item">
      <span>{item.name} x {item.quantity}</span>
      <button onclick={() => cart.updateQuantity(item.id, item.quantity - 1)}>-</button>
      <button onclick={() => cart.updateQuantity(item.id, item.quantity + 1)}>+</button>
      <button onclick={() => cart.removeItem(item.id)}>Remove</button>
    </div>
  {/each}
  {#if cart.count > 0}
    <button onclick={() => cart.clear()}>Clear Cart</button>
  {/if}
</div>
```

**Context API with getContext/setContext**:

```svelte
<!-- ThemeProvider.svelte -->
<script lang="ts">
  import { setContext } from "svelte";

  interface ThemeContext {
    theme: string;
    toggleTheme: () => void;
  }

  let theme = $state<"light" | "dark">("light");

  function toggleTheme() {
    theme = theme === "light" ? "dark" : "light";
  }

  // Context is available to all descendants
  setContext<ThemeContext>("theme", {
    get theme() { return theme; },
    toggleTheme,
  });

  let { children }: { children: any } = $props();
</script>

<div class="app" data-theme={theme}>
  {@render children()}
</div>

<!-- ThemeToggle.svelte (descendant component) -->
<script lang="ts">
  import { getContext } from "svelte";

  interface ThemeContext {
    theme: string;
    toggleTheme: () => void;
  }

  const { theme, toggleTheme } = getContext<ThemeContext>("theme");
</script>

<button onclick={toggleTheme}>
  Current theme: {theme}. Click to toggle.
</button>
```

**Derived state across multiple stores**:

```ts
// src/lib/stores/filters.svelte.ts
interface FilterState {
  category: string;
  minPrice: number;
  maxPrice: number;
  searchQuery: string;
}

function createFilterStore() {
  let filters = $state<FilterState>({
    category: "all",
    minPrice: 0,
    maxPrice: Infinity,
    searchQuery: "",
  });

  let activeFilterCount = $derived(
    [
      filters.category !== "all",
      filters.minPrice > 0,
      filters.maxPrice < Infinity,
      filters.searchQuery.length > 0,
    ].filter(Boolean).length
  );

  let queryParams = $derived.by(() => {
    const params = new URLSearchParams();
    if (filters.category !== "all") params.set("category", filters.category);
    if (filters.minPrice > 0) params.set("minPrice", String(filters.minPrice));
    if (filters.maxPrice < Infinity) params.set("maxPrice", String(filters.maxPrice));
    if (filters.searchQuery) params.set("q", filters.searchQuery);
    return params.toString();
  });

  function setCategory(category: string) {
    filters.category = category;
  }

  function setPriceRange(min: number, max: number) {
    filters.minPrice = min;
    filters.maxPrice = max;
  }

  function setSearch(query: string) {
    filters.searchQuery = query;
  }

  function reset() {
    filters.category = "all";
    filters.minPrice = 0;
    filters.maxPrice = Infinity;
    filters.searchQuery = "";
  }

  return {
    get filters() { return filters; },
    get activeFilterCount() { return activeFilterCount; },
    get queryParams() { return queryParams; },
    setCategory,
    setPriceRange,
    setSearch,
    reset,
  };
}

export const filterStore = createFilterStore();
```

### Step 6: Configure SvelteKit Hooks and Middleware

**Server hooks (src/hooks.server.ts)**:

```ts
// src/hooks.server.ts
import type { Handle, HandleFetch, HandleServerError } from "@sveltejs/kit";
import { db } from "$lib/server/db";
import { verifySession } from "$lib/server/auth";
import { sequence } from "@sveltejs/kit/hooks";

// Authentication hook
const authHandle: Handle = async ({ event, resolve }) => {
  const sessionToken = event.cookies.get("session");

  if (sessionToken) {
    try {
      const user = await verifySession(sessionToken);
      event.locals.user = user;
    } catch {
      // Invalid session; clear the cookie
      event.cookies.delete("session", { path: "/" });
    }
  }

  return resolve(event);
};

// Security headers hook
const securityHandle: Handle = async ({ event, resolve }) => {
  const response = await resolve(event);

  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  response.headers.set(
    "Permissions-Policy",
    "camera=(), microphone=(), geolocation=()"
  );

  return response;
};

// Protected routes hook
const protectedRoutes: Handle = async ({ event, resolve }) => {
  const protectedPaths = ["/dashboard", "/settings", "/admin"];
  const isProtected = protectedPaths.some((p) =>
    event.url.pathname.startsWith(p)
  );

  if (isProtected && !event.locals.user) {
    const redirectUrl = `/login?redirect=${encodeURIComponent(event.url.pathname)}`;
    return new Response(null, {
      status: 302,
      headers: { location: redirectUrl },
    });
  }

  if (event.url.pathname.startsWith("/admin")) {
    if (event.locals.user?.role !== "admin") {
      return new Response("Forbidden", { status: 403 });
    }
  }

  return resolve(event);
};

// Chain hooks with sequence
export const handle = sequence(authHandle, securityHandle, protectedRoutes);

// Modify outgoing fetch requests (e.g., attach auth headers to API calls)
export const handleFetch: HandleFetch = async ({ event, request, fetch }) => {
  if (request.url.startsWith("https://api.internal.example.com")) {
    request.headers.set(
      "Authorization",
      `Bearer ${event.locals.user?.apiToken ?? ""}`
    );
  }
  return fetch(request);
};

// Global error handler
export const handleError: HandleServerError = async ({ error, event, status, message }) => {
  const errorId = crypto.randomUUID();

  console.error(`[${errorId}] Unhandled error on ${event.url.pathname}:`, error);

  // Report to error tracking service
  // await reportError({ errorId, error, url: event.url.pathname });

  return {
    message: "An unexpected error occurred",
    errorId,
  };
};
```

**App.d.ts type declarations**:

```ts
// src/app.d.ts
declare global {
  namespace App {
    interface Error {
      message: string;
      errorId?: string;
    }
    interface Locals {
      user: {
        id: string;
        name: string;
        email: string;
        role: "admin" | "user";
        apiToken?: string;
      } | null;
    }
    interface PageData {
      user: App.Locals["user"];
    }
    interface PageState {}
    interface Platform {}
  }
}

export {};
```

**Environment variables**:

```ts
// Access public env variables (available on client and server)
import { PUBLIC_API_URL, PUBLIC_APP_NAME } from "$env/static/public";

// Access private env variables (server-only, build-time)
import { DATABASE_URL, JWT_SECRET } from "$env/static/private";

// Dynamic env variables (read at runtime, not inlined at build)
import { env } from "$env/dynamic/private";
const dbUrl = env.DATABASE_URL;

// SvelteKit will throw a build error if you try to import
// private env variables into client-side code
```

**Custom error page**:

```svelte
<!-- src/routes/+error.svelte -->
<script lang="ts">
  import { page } from "$app/stores";
</script>

<svelte:head>
  <title>Error {$page.status}</title>
</svelte:head>

<div class="error-page">
  <h1>{$page.status}</h1>
  <p>{$page.error?.message ?? "Something went wrong"}</p>
  {#if $page.error?.errorId}
    <p class="error-id">Error ID: {$page.error.errorId}</p>
  {/if}
  <a href="/">Go home</a>
</div>
```

### Step 7: Optimize Performance

**Fine-grained reactivity with runes**:

```svelte
<script lang="ts">
  // Svelte 5 runes provide fine-grained reactivity at the signal level.
  // Only the specific DOM nodes that depend on a changed value will update.

  let firstName = $state("Alice");
  let lastName = $state("Smith");

  // Only elements reading fullName re-render when firstName or lastName changes
  let fullName = $derived(`${firstName} ${lastName}`);

  // Avoid $effect for derived state; use $derived instead
  // WRONG: $effect(() => { fullName = `${firstName} ${lastName}` });
  // RIGHT: let fullName = $derived(`${firstName} ${lastName}`);
</script>

<input bind:value={firstName} /> <!-- Updating this does NOT re-render the lastName input -->
<input bind:value={lastName} />
<p>Hello, {fullName}</p>
```

**Transitions and animations**:

```svelte
<script lang="ts">
  import { fade, fly, slide, scale } from "svelte/transition";
  import { flip } from "svelte/animate";
  import { quintOut } from "svelte/easing";

  let items = $state<{ id: string; text: string }[]>([]);
  let showPanel = $state(false);

  function addItem() {
    items.push({ id: crypto.randomUUID(), text: `Item ${items.length + 1}` });
  }

  function removeItem(id: string) {
    const index = items.findIndex((i) => i.id === id);
    if (index !== -1) items.splice(index, 1);
  }
</script>

<button onclick={() => (showPanel = !showPanel)}>Toggle Panel</button>

{#if showPanel}
  <div transition:slide={{ duration: 300, easing: quintOut }}>
    <p>This panel slides in and out.</p>
  </div>
{/if}

<button onclick={addItem}>Add Item</button>

<ul>
  {#each items as item (item.id)}
    <li
      animate:flip={{ duration: 200 }}
      in:fly={{ y: 20, duration: 200 }}
      out:fade={{ duration: 150 }}
    >
      {item.text}
      <button onclick={() => removeItem(item.id)}>Remove</button>
    </li>
  {/each}
</ul>
```

**Lazy loading with dynamic imports**:

```svelte
<script lang="ts">
  let showChart = $state(false);
  let ChartComponent: any = $state(null);

  async function loadChart() {
    showChart = true;
    // Dynamic import splits the chart library into a separate chunk
    const module = await import("$lib/components/HeavyChart.svelte");
    ChartComponent = module.default;
  }
</script>

<button onclick={loadChart}>Show Analytics</button>

{#if showChart}
  {#if ChartComponent}
    <ChartComponent data={chartData} />
  {:else}
    <p>Loading chart...</p>
  {/if}
{/if}
```

**Prerendering and adapter selection**:

```ts
// svelte.config.js
import adapter from "@sveltejs/adapter-auto"; // Auto-detects Vercel, Netlify, Cloudflare
// import adapter from "@sveltejs/adapter-node";     // Self-hosted Node.js
// import adapter from "@sveltejs/adapter-static";   // Fully static site
// import adapter from "@sveltejs/adapter-vercel";   // Vercel-specific features

import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter(),
    prerender: {
      // Prerender these routes at build time
      entries: ["/", "/about", "/pricing", "/blog"],
    },
    csp: {
      directives: {
        "script-src": ["self"],
        "style-src": ["self", "unsafe-inline"],
      },
    },
    alias: {
      $components: "src/lib/components",
      $stores: "src/lib/stores",
    },
  },
};

export default config;
```

**Per-page prerendering and SSR control**:

```ts
// src/routes/about/+page.ts
// Static page: prerender at build time
export const prerender = true;

// src/routes/dashboard/+page.ts
// Dynamic page: never prerender, always SSR
export const prerender = false;
export const ssr = true;

// src/routes/app/+page.ts
// SPA page: disable SSR, render client-only
export const ssr = false;
export const csr = true;
```

### Step 8: Test with Vitest and Playwright

**Component testing with @testing-library/svelte**:

```ts
// src/lib/components/Counter.test.ts
import { render, screen } from "@testing-library/svelte";
import userEvent from "@testing-library/user-event";
import { describe, it, expect } from "vitest";
import Counter from "./Counter.svelte";

describe("Counter", () => {
  it("renders initial count", () => {
    render(Counter, { props: { initial: 5 } });
    expect(screen.getByText("Count: 5")).toBeInTheDocument();
  });

  it("increments count on button click", async () => {
    const user = userEvent.setup();
    render(Counter, { props: { initial: 0 } });

    const button = screen.getByRole("button", { name: /increment/i });
    await user.click(button);

    expect(screen.getByText("Count: 1")).toBeInTheDocument();
  });

  it("decrements count but not below zero", async () => {
    const user = userEvent.setup();
    render(Counter, { props: { initial: 0 } });

    const button = screen.getByRole("button", { name: /decrement/i });
    await user.click(button);

    expect(screen.getByText("Count: 0")).toBeInTheDocument();
  });

  it("calls onChange callback when count changes", async () => {
    const user = userEvent.setup();
    const onChange = vi.fn();
    render(Counter, { props: { initial: 0, onChange } });

    await user.click(screen.getByRole("button", { name: /increment/i }));

    expect(onChange).toHaveBeenCalledWith(1);
  });
});
```

**Testing components with context and stores**:

```ts
// src/lib/components/CartSummary.test.ts
import { render, screen } from "@testing-library/svelte";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, beforeEach } from "vitest";
import CartSummary from "./CartSummary.svelte";
import { cart } from "$lib/stores/cart.svelte";

describe("CartSummary", () => {
  beforeEach(() => {
    cart.clear();
  });

  it("shows empty cart message when no items", () => {
    render(CartSummary);
    expect(screen.getByText(/cart is empty/i)).toBeInTheDocument();
  });

  it("displays item count and total after adding items", async () => {
    cart.addItem({ id: "1", name: "Widget", price: 9.99 });
    cart.addItem({ id: "2", name: "Gadget", price: 24.99 });

    render(CartSummary);

    expect(screen.getByText(/2 items/i)).toBeInTheDocument();
    expect(screen.getByText(/\$34\.98/)).toBeInTheDocument();
  });

  it("removes item when remove button is clicked", async () => {
    const user = userEvent.setup();
    cart.addItem({ id: "1", name: "Widget", price: 9.99 });

    render(CartSummary);
    await user.click(screen.getByRole("button", { name: /remove widget/i }));

    expect(screen.getByText(/cart is empty/i)).toBeInTheDocument();
  });
});
```

**Testing load functions in isolation**:

```ts
// src/routes/blog/[slug]/+page.server.test.ts
import { describe, it, expect, vi } from "vitest";
import { load } from "./+page.server";

vi.mock("$lib/server/db", () => ({
  db: {
    post: {
      findUnique: vi.fn(),
    },
  },
}));

import { db } from "$lib/server/db";

describe("blog post load function", () => {
  it("returns post data for a valid slug", async () => {
    const mockPost = {
      slug: "hello-world",
      title: "Hello World",
      htmlContent: "<p>Content</p>",
      publishedAt: "2026-01-15",
      excerpt: "A hello world post",
    };

    vi.mocked(db.post.findUnique).mockResolvedValue(mockPost);

    const result = await load({
      params: { slug: "hello-world" },
    } as any);

    expect(result.post).toEqual(mockPost);
    expect(db.post.findUnique).toHaveBeenCalledWith({
      where: { slug: "hello-world" },
    });
  });

  it("throws 404 error for a missing slug", async () => {
    vi.mocked(db.post.findUnique).mockResolvedValue(null);

    await expect(
      load({ params: { slug: "nonexistent" } } as any)
    ).rejects.toMatchObject({
      status: 404,
    });
  });
});
```

**End-to-end testing with Playwright**:

```ts
// tests/e2e/blog.test.ts
import { test, expect } from "@playwright/test";

test.describe("Blog", () => {
  test("displays list of blog posts", async ({ page }) => {
    await page.goto("/blog");

    await expect(page.getByRole("heading", { name: /blog/i })).toBeVisible();
    await expect(page.getByRole("article").first()).toBeVisible();
  });

  test("navigates to individual post and back", async ({ page }) => {
    await page.goto("/blog");

    const firstPost = page.getByRole("article").first();
    const postTitle = await firstPost.getByRole("heading").textContent();
    await firstPost.getByRole("link").click();

    await expect(page.getByRole("heading", { name: postTitle! })).toBeVisible();

    await page.goBack();
    await expect(page.getByRole("heading", { name: /blog/i })).toBeVisible();
  });

  test("creates a new blog post via form", async ({ page }) => {
    // Log in first
    await page.goto("/login");
    await page.getByLabel(/email/i).fill("admin@example.com");
    await page.getByLabel(/password/i).fill("testpassword");
    await page.getByRole("button", { name: /sign in/i }).click();

    await page.goto("/blog/new");
    await page.getByLabel(/title/i).fill("E2E Test Post");
    await page.getByLabel(/content/i).fill("This post was created by an E2E test to verify form submission.");
    await page.getByRole("button", { name: /create post/i }).click();

    // Should redirect to the new post
    await expect(page.getByRole("heading", { name: "E2E Test Post" })).toBeVisible();
  });

  test("shows validation errors for empty form", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel(/email/i).fill("admin@example.com");
    await page.getByLabel(/password/i).fill("testpassword");
    await page.getByRole("button", { name: /sign in/i }).click();

    await page.goto("/blog/new");
    await page.getByRole("button", { name: /create post/i }).click();

    await expect(page.getByText(/title is required/i)).toBeVisible();
  });
});

test.describe("Dashboard", () => {
  test("redirects unauthenticated users to login", async ({ page }) => {
    await page.goto("/dashboard");
    await expect(page).toHaveURL(/\/login/);
  });

  test("displays dashboard stats for authenticated users", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel(/email/i).fill("admin@example.com");
    await page.getByLabel(/password/i).fill("testpassword");
    await page.getByRole("button", { name: /sign in/i }).click();

    await page.goto("/dashboard");
    await expect(page.getByRole("heading", { name: /dashboard/i })).toBeVisible();
    await expect(page.getByText(/total posts/i)).toBeVisible();
  });
});
```

**Vitest configuration for SvelteKit**:

```ts
// vite.config.ts
import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [sveltekit()],
  test: {
    include: ["src/**/*.{test,spec}.{js,ts}"],
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/tests/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "html", "lcov"],
      include: ["src/lib/**/*.{ts,svelte}", "src/routes/**/*.{ts,svelte}"],
      thresholds: {
        lines: 80,
        branches: 70,
      },
    },
  },
});
```

```ts
// src/tests/setup.ts
import "@testing-library/jest-dom/vitest";
```

**Playwright configuration**:

```ts
// playwright.config.ts
import type { PlaywrightTestConfig } from "@playwright/test";

const config: PlaywrightTestConfig = {
  webServer: {
    command: "npm run build && npm run preview",
    port: 4173,
    reuseExistingServer: !process.env.CI,
  },
  testDir: "tests/e2e",
  testMatch: /(.+\.)?(test|spec)\.[jt]s/,
  use: {
    baseURL: "http://localhost:4173",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  retries: process.env.CI ? 2 : 0,
  reporter: process.env.CI ? "github" : "list",
};

export default config;
```

## Best Practices

- **Use runes, not stores**: Svelte 5 runes ($state, $derived, $effect) replace writable/readable/derived stores with simpler, more performant primitives
- **Prefer $derived over $effect for computed values**: $effect is for side effects (fetches, DOM manipulation, logging); $derived is for transformations
- **Use progressive enhancement**: SvelteKit forms work without JavaScript by default; add `use:enhance` for a smoother UX, not as a requirement
- **Colocate data loading with routes**: each +page.server.ts loads only the data its +page.svelte needs
- **Stream slow data**: return promises from load functions and use `{#await}` blocks so the page renders immediately
- **Choose the right adapter**: adapter-auto for most deployments; adapter-node for self-hosted; adapter-static for fully prerendered sites
- **Keep components small**: extract logic into .svelte.ts modules and rendering into child components
- **Type your props with interfaces**: use the Props interface pattern with $props() for full TypeScript safety

## Common Patterns

### Pattern 1: Debounced Search with Runes

```svelte
<script lang="ts">
  let query = $state("");
  let results = $state<string[]>([]);
  let debounceTimer: ReturnType<typeof setTimeout> | undefined;

  $effect(() => {
    clearTimeout(debounceTimer);

    if (query.length < 2) {
      results = [];
      return;
    }

    debounceTimer = setTimeout(async () => {
      const res = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
      if (res.ok) {
        results = await res.json();
      }
    }, 300);

    return () => clearTimeout(debounceTimer);
  });
</script>

<input bind:value={query} placeholder="Search..." />
{#each results as result}
  <p>{result}</p>
{/each}
```

### Pattern 2: Authenticated Layout with Redirect

```ts
// src/routes/dashboard/+layout.server.ts
import { redirect } from "@sveltejs/kit";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async ({ locals }) => {
  if (!locals.user) {
    redirect(302, "/login");
  }

  return {
    user: locals.user,
  };
};
```

```svelte
<!-- src/routes/dashboard/+layout.svelte -->
<script lang="ts">
  import type { LayoutData } from "./$types";

  let { data, children }: { data: LayoutData; children: any } = $props();
</script>

<div class="dashboard-layout">
  <aside>
    <nav>
      <p>Signed in as {data.user.name}</p>
      <a href="/dashboard">Overview</a>
      <a href="/dashboard/settings">Settings</a>
    </nav>
  </aside>
  <div class="dashboard-content">
    {@render children()}
  </div>
</div>
```

## Quality Checklist

- [ ] All reactive state uses $state (not Svelte 4 stores or let-assignment reactivity)
- [ ] Computed values use $derived, not $effect with assignment
- [ ] $effect cleanup functions handle abort controllers and timers
- [ ] Components use $props() with typed interfaces
- [ ] Snippets replace all slot usage (Svelte 5 pattern)
- [ ] Load functions validate params and return typed data
- [ ] Form actions validate input with Zod and return fail() on error
- [ ] Forms use use:enhance for progressive enhancement
- [ ] hooks.server.ts applies auth checks and security headers
- [ ] Private env variables are never imported in client code
- [ ] Transitions use easing functions for smooth motion
- [ ] Prerender is configured for static pages
- [ ] Component tests use @testing-library/svelte with accessible queries
- [ ] E2E tests cover critical user flows (auth, form submission, navigation)
- [ ] Vitest coverage meets 80% line threshold

## Related Skills

- `react-expert` - React component architecture and hooks (for comparison)
- `nextjs-expert` - Next.js App Router patterns (SvelteKit equivalent concepts)
- `typescript-expert` - Advanced TypeScript for typed components and stores
- `unit-tests` - General unit testing strategies
- `e2e-testing-automation` - End-to-end testing patterns with Playwright

---

**Version**: 1.0.0
**Last Updated**: March 2026

### Iterative Refinement Strategy
This skill is optimized for an iterative approach:
1. **Execute**: Perform the core steps defined above.
2. **Review**: Critically analyze the output (coverage, quality, completeness).
3. **Refine**: If targets aren't met, repeat the specific implementation steps with improved context.
4. **Loop**: Continue until the definition of done is satisfied.
