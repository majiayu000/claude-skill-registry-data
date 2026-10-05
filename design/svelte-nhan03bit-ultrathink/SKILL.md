---
name: svelte
description: SvelteKit development patterns — runes, component architecture, server-side rendering, form actions, and reactive state
layer: domain
category: frontend
triggers:
  - "svelte"
  - "sveltekit"
  - "svelte component"
  - "svelte rune"
  - "$state"
  - "$derived"
  - "$effect"
  - "+page.svelte"
  - "+server.ts"
  - "svelte action"
inputs:
  - "SvelteKit page or component requirements"
  - "Svelte reactivity patterns"
  - "SvelteKit routing and data loading"
  - "Form handling in SvelteKit"
outputs:
  - "SvelteKit pages, layouts, and endpoints"
  - "Svelte 5 rune-based components"
  - "Server-side data loading patterns"
  - "Form action implementations"
linksTo:
  - typescript-frontend
  - css-architecture
  - animation
  - forms
linkedFrom:
  - code-writer
  - architect
preferredNextSkills:
  - typescript-frontend
  - css-architecture
  - forms
fallbackSkills:
  - react
  - vue
riskLevel: low
memoryReadPolicy: selective
memoryWritePolicy: none
sideEffects: []
---

# SvelteKit Development Patterns

## Purpose

Provide expert guidance on SvelteKit application development using Svelte 5 runes, component architecture, server-side rendering, data loading, form actions, and deployment patterns. Focus on idiomatic Svelte patterns that leverage the compiler for optimal performance.

## Key Patterns

### Svelte 5 Runes

Svelte 5 replaces the implicit reactivity system with explicit runes:

**`$state` — Reactive state declaration:**

```svelte
<script lang="ts">
  let count = $state(0);
  let items = $state<string[]>([]);
  let user = $state<{ name: string; email: string }>({
    name: '',
    email: '',
  });

  function increment() {
    count++;  // Direct mutation is reactive
  }

  function addItem(item: string) {
    items.push(item);  // Array mutations are reactive with $state
  }

  function updateName(name: string) {
    user.name = name;  // Deep property mutations are reactive
  }
</script>

<button
  onclick={increment}
  class="px-6 py-4 text-base rounded-lg bg-blue-600 text-white transition-all duration-200 hover:bg-blue-700 focus-visible:ring-2 focus-visible:ring-offset-2"
>
  Count: {count}
</button>
```

**`$derived` — Computed values:**

```svelte
<script lang="ts">
  let items = $state<{ name: string; done: boolean }[]>([]);

  // Simple derivation
  let total = $derived(items.length);
  let completed = $derived(items.filter(i => i.done).length);
  let remaining = $derived(total - completed);

  // Complex derivation with $derived.by
  let stats = $derived.by(() => {
    const done = items.filter(i => i.done);
    const pending = items.filter(i => !i.done);
    return {
      done: done.length,
      pending: pending.length,
      percentComplete: items.length ? Math.round((done.length / items.length) * 100) : 0,
    };
  });
</script>

<p class="text-base">{remaining} items remaining ({stats.percentComplete}% complete)</p>
```

**`$effect` — Side effects:**

```svelte
<script lang="ts">
  let searchQuery = $state('');
  let results = $state<SearchResult[]>([]);

  // Runs when searchQuery changes (auto-tracked)
  $effect(() => {
    if (searchQuery.length < 2) {
      results = [];
      return;
    }

    const controller = new AbortController();

    fetch(`/api/search?q=${encodeURIComponent(searchQuery)}`, {
      signal: controller.signal,
    })
      .then(r => r.json())
      .then(data => { results = data; })
      .catch(() => {});

    // Cleanup function
    return () => controller.abort();
  });

  // Pre-effect for DOM measurements
  $effect.pre(() => {
    // Runs before DOM update
  });
</script>
```

**`$props` — Component props:**

```svelte
<script lang="ts">
  interface Props {
    variant?: 'primary' | 'secondary' | 'ghost';
    size?: 'sm' | 'md' | 'lg';
    disabled?: boolean;
    onclick?: (e: MouseEvent) => void;
    children: import('svelte').Snippet;
  }

  let {
    variant = 'primary',
    size = 'md',
    disabled = false,
    onclick,
    children,
    ...restProps
  }: Props = $props();
</script>

<button
  class="px-6 py-4 text-base rounded-lg transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2"
  class:bg-blue-600={variant === 'primary'}
  class:bg-white={variant === 'secondary'}
  {disabled}
  {onclick}
  {...restProps}
>
  {@render children()}
</button>
```

### SvelteKit Routing & Data Loading

**File structure:**

```
src/routes/
  +layout.svelte        # Root layout
  +layout.server.ts     # Root layout data
  +page.svelte          # Home page /
  +page.server.ts       # Home page data loader
  +error.svelte         # Error boundary

  dashboard/
    +layout.svelte      # Dashboard layout
    +page.svelte        # /dashboard
    +page.server.ts     # Dashboard data

    settings/
      +page.svelte      # /dashboard/settings
      +page.server.ts

    [teamId]/
      +page.svelte      # /dashboard/:teamId
      +page.server.ts

  api/
    search/
      +server.ts        # GET /api/search
```

**Server load function:**

```ts
// src/routes/dashboard/+page.server.ts
import type { PageServerLoad } from './$types';
import { error } from '@sveltejs/kit';

export const load: PageServerLoad = async ({ locals, depends }) => {
  const session = locals.session;
  if (!session) throw error(401, 'Unauthorized');

  // Tag for invalidation
  depends('app:dashboard');

  // Parallel data fetching
  const [stats, recentActivity] = await Promise.all([
    getDashboardStats(session.userId),
    getRecentActivity(session.userId),
  ]);

  return {
    stats,
    recentActivity,
  };
};
```

**Page component consuming data:**

```svelte
<!-- src/routes/dashboard/+page.svelte -->
<script lang="ts">
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();
</script>

<section class="py-16">
  <h1 class="text-2xl font-bold mb-8">Dashboard</h1>

  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
    {#each data.stats as stat}
      <div class="p-6 rounded-xl shadow-sm border">
        <p class="text-sm text-gray-500">{stat.label}</p>
        <p class="text-2xl font-bold mt-1">{stat.value}</p>
      </div>
    {/each}
  </div>
</section>
```

### Form Actions

```ts
// src/routes/posts/new/+page.server.ts
import type { Actions, PageServerLoad } from './$types';
import { fail, redirect } from '@sveltejs/kit';
import { z } from 'zod';

const PostSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200),
  content: z.string().min(1, 'Content is required'),
});

export const actions: Actions = {
  create: async ({ request, locals }) => {
    const formData = await request.formData();
    const parsed = PostSchema.safeParse({
      title: formData.get('title'),
      content: formData.get('content'),
    });

    if (!parsed.success) {
      return fail(400, {
        errors: parsed.error.flatten().fieldErrors,
        values: { title: formData.get('title') as string },
      });
    }

    const post = await db.post.create({
      data: { ...parsed.data, authorId: locals.session!.userId },
    });

    throw redirect(303, `/posts/${post.id}`);
  },
};
```

```svelte
<!-- src/routes/posts/new/+page.svelte -->
<script lang="ts">
  import { enhance } from '$app/forms';
  import type { ActionData } from './$types';

  let { form }: { form: ActionData } = $props();
  let submitting = $state(false);
</script>

<form
  method="POST"
  action="?/create"
  use:enhance={() => {
    submitting = true;
    return async ({ update }) => {
      submitting = false;
      await update();
    };
  }}
  class="space-y-6 max-w-2xl"
>
  <div>
    <label for="title" class="block text-base font-medium mb-2">Title</label>
    <input
      id="title"
      name="title"
      value={form?.values?.title ?? ''}
      class="w-full px-4 py-3 rounded-lg border transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2"
    />
    {#if form?.errors?.title}
      <p class="text-red-600 text-sm mt-1">{form.errors.title[0]}</p>
    {/if}
  </div>

  <div>
    <label for="content" class="block text-base font-medium mb-2">Content</label>
    <textarea
      id="content"
      name="content"
      rows="6"
      class="w-full px-4 py-3 rounded-lg border transition-all duration-200 focus-visible:ring-2 focus-visible:ring-offset-2"
    ></textarea>
    {#if form?.errors?.content}
      <p class="text-red-600 text-sm mt-1">{form.errors.content[0]}</p>
    {/if}
  </div>

  <button
    type="submit"
    disabled={submitting}
    class="px-6 py-4 text-base rounded-lg bg-blue-600 text-white transition-all duration-200 hover:bg-blue-700 focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50"
  >
    {submitting ? 'Creating...' : 'Create Post'}
  </button>
</form>
```

### Snippets (Svelte 5 Slots Replacement)

```svelte
<!-- Card.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    header: Snippet;
    children: Snippet;
    footer?: Snippet;
  }

  let { header, children, footer }: Props = $props();
</script>

<div class="rounded-xl shadow-sm border overflow-hidden">
  <div class="p-6 border-b">
    {@render header()}
  </div>
  <div class="p-6">
    {@render children()}
  </div>
  {#if footer}
    <div class="p-6 border-t bg-gray-50">
      {@render footer()}
    </div>
  {/if}
</div>

<!-- Usage -->
<Card>
  {#snippet header()}
    <h3 class="text-lg font-semibold">Card Title</h3>
  {/snippet}

  <p class="text-base text-gray-600">Card content goes here.</p>

  {#snippet footer()}
    <button class="px-6 py-4 text-base rounded-lg bg-blue-600 text-white">Action</button>
  {/snippet}
</Card>
```

### Svelte Actions (DOM Directives)

```svelte
<script lang="ts">
  // Click outside directive
  function clickOutside(node: HTMLElement, callback: () => void) {
    function handleClick(e: MouseEvent) {
      if (!node.contains(e.target as Node)) {
        callback();
      }
    }

    document.addEventListener('click', handleClick, true);

    return {
      destroy() {
        document.removeEventListener('click', handleClick, true);
      },
    };
  }

  // Intersection observer directive
  function inView(
    node: HTMLElement,
    params: { callback: (entry: IntersectionObserverEntry) => void; threshold?: number }
  ) {
    const observer = new IntersectionObserver(
      ([entry]) => params.callback(entry),
      { threshold: params.threshold ?? 0.5 }
    );

    observer.observe(node);

    return {
      destroy() {
        observer.disconnect();
      },
    };
  }

  let isOpen = $state(false);
</script>

<div use:clickOutside={() => { isOpen = false; }}>
  <button onclick={() => { isOpen = !isOpen; }}>Toggle Menu</button>
  {#if isOpen}
    <div class="p-6 rounded-xl shadow-lg">Menu content</div>
  {/if}
</div>

<div use:inView={{ callback: (entry) => { /* animate on view */ }, threshold: 0.3 }}>
  Observe me
</div>
```

## Best Practices

1. **Use runes exclusively** — Svelte 5's `$state`, `$derived`, `$effect` replace `let`, `$:`, and reactive statements.
2. **Server-first data loading** — Use `+page.server.ts` for data; avoid client-side fetching in `onMount`.
3. **Progressive enhancement** — Forms work without JavaScript via `use:enhance`.
4. **Type everything** — Use TypeScript with generated `$types` for full type safety on load functions and actions.
5. **Keep effects minimal** — `$effect` should be rare. Prefer `$derived` for computed values.
6. **Snippets over slots** — Svelte 5 replaces slots with typed snippets for better composition.
7. **Actions for DOM behavior** — Use Svelte actions (`use:directive`) for reusable DOM interactions.
8. **Invalidate, don't refetch** — Use `invalidate('app:data')` to trigger re-running load functions.
9. **Stream with await blocks** — Use `{#await promise}` for inline loading states.
10. **Preload on hover** — SvelteKit automatically preloads links on hover for instant navigation.

## Common Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Mixing old reactive syntax | `$:` and runes don't mix in same component | Migrate fully to runes |
| `$effect` for derived values | Unnecessary effect, should be computed | Use `$derived` or `$derived.by` |
| Missing `use:enhance` on forms | Full page reload on submit | Add `use:enhance` for progressive enhancement |
| Client-side data fetching | Waterfall, no SSR benefit | Move to `+page.server.ts` load function |
| Mutable state in `$derived` | Unexpected behavior | `$derived` must be pure, no side effects |
| Not using `$props()` | Props not reactive in Svelte 5 | Always destructure from `$props()` |
| Forgetting action cleanup | Memory leaks on DOM directives | Return `destroy()` from Svelte actions |
| Large stores in context | Unnecessary re-renders | Use fine-grained `$state` objects, not monolithic stores |
