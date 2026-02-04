---
name: composable-svelte-ssr
description: Server-side rendering patterns for Composable Svelte. Use when implementing SSR, hydration, server rendering, isomorphic code, or working with meta tags and SEO. Covers renderToHTML, hydrateStore, server-side routing, state serialization, and avoiding common SSR pitfalls.
---

# Composable Svelte SSR

This skill covers server-side rendering (SSR) patterns for Composable Svelte applications.

---

## SSR APIs

### renderToHTML - Server Rendering

```typescript
import { renderToHTML } from '@composable-svelte/core/ssr';
import { createStore } from '@composable-svelte/core';
import App from './App.svelte';

app.get('/', async (req, res) => {
  // 1. Load data for this request
  const data = await loadData(req.user);

  // 2. Create store with pre-populated data
  const store = createStore({
    initialState: data,
    reducer: appReducer,
    dependencies: {}  // Empty on server - effects won't run
  });

  // 3. Render to HTML
  const html = renderToHTML(App, { store }, {
    head: `<link rel="stylesheet" href="/assets/index.css">`,
    clientScript: '/assets/index.js'
  });

  // 4. Send response
  res.send(html);
});
```

### hydrateStore - Client Hydration

```typescript
import { hydrateStore } from '@composable-svelte/core/ssr';
import { mount } from 'svelte';
import App from './App.svelte';

// 1. Read state from script tag
const stateJSON = document.getElementById('__COMPOSABLE_SVELTE_STATE__')?.textContent;

// 2. Hydrate with client dependencies
const store = hydrateStore(stateJSON, {
  reducer: appReducer,
  dependencies: {
    api: createAPIClient(),
    storage: createLocalStorage()
  }
});

// 3. Mount app (reuses existing DOM from SSR)
mount(App, { target: document.body, props: { store } });
```

---

## ISOMORPHIC PATTERNS

### Server vs Client Dependencies

**Key Pattern**: Server has empty dependencies, client has real implementations.

```typescript
// server.ts
const store = createStore({
  initialState: data,
  reducer: appReducer,
  dependencies: {} as AppDependencies  // Empty - effects won't run
  // ssr.deferEffects defaults to true, so effects are automatically skipped
});

// client.ts
const store = hydrateStore(stateJSON, {
  reducer: appReducer,
  dependencies: {
    api: createAPIClient(),      // Real API client
    storage: localStorage,        // Real storage
    clock: new SystemClock()      // Real clock
  }
});
```

**Why**: Server doesn't need to execute effects - it just renders initial state. Client needs real dependencies for interactivity.

---

### Router Pure Functions on Server

**Key Pattern**: Use router's pure functions (`parseDestination`, `matchPath`, `serializeDestination`) on both server and client.

```typescript
// routing.ts (shared between server and client)
export function parsePostFromURL(path: string, defaultId: number): number {
  const match = path.match(/^\/posts\/(\d+)$/);
  return match ? parseInt(match[1], 10) : defaultId;
}

// server.ts
async function renderApp(request: any, reply: any) {
  const posts = await loadPosts();
  const path = request.url;
  const requestedPostId = parsePostFromURL(path, posts[0]?.id || 1);

  const store = createStore({
    initialState: {
      posts,
      selectedPostId: requestedPostId,
      meta: computeMetaForPost(posts.find(p => p.id === requestedPostId))
    },
    reducer: appReducer,
    dependencies: {}
  });

  const html = renderToHTML(App, { store });
  reply.type('text/html').send(html);
}
```

---

## STATE INITIALIZATION FROM URL

### Pattern: Parse URL on Server, Initialize State

```typescript
// server.ts
import { parseDestination } from './shared/routing';

app.get('/posts/:id', async (req, res) => {
  const postId = parseInt(req.params.id, 10);

  // Load data based on URL
  const posts = await loadPosts();
  const selectedPost = posts.find(p => p.id === postId) || posts[0];

  // Initialize state with URL-driven selection
  const store = createStore({
    initialState: {
      posts,
      selectedPostId: selectedPost?.id || null,
      // Set initial meta based on URL-selected post
      meta: selectedPost
        ? {
            title: `${selectedPost.title} - Blog`,
            description: selectedPost.content.slice(0, 160),
            ogImage: `/og/post-${selectedPost.id}.jpg`,
            canonical: `https://example.com/posts/${selectedPost.id}`
          }
        : initialState.meta
    },
    reducer: appReducer,
    dependencies: {}
  });

  const html = renderToHTML(App, { store });
  res.send(html);
});
```

---

## STATE SERIALIZATION/DESERIALIZATION

### Automatic Serialization

When you call `renderToHTML`, the store state is automatically serialized and embedded in the HTML:

```typescript
const html = renderToHTML(App, { store });
// HTML contains: <script id="__COMPOSABLE_SVELTE_STATE__" type="application/json">...</script>
```

### Automatic Deserialization

When you call `hydrateStore`, the state is automatically deserialized:

```typescript
const stateJSON = document.getElementById('__COMPOSABLE_SVELTE_STATE__')?.textContent;
const store = hydrateStore(stateJSON, { reducer, dependencies });
```

### Custom Serialization (Advanced)

For complex types (Date, Map, Set), provide custom serializers:

```typescript
import { serializeState, parseState } from '@composable-svelte/core/ssr';

// Server
const serialized = serializeState(store.state, {
  customSerializers: {
    Date: (date) => ({ __type: 'Date', value: date.toISOString() }),
    Map: (map) => ({ __type: 'Map', entries: Array.from(map.entries()) })
  }
});

// Client
const state = parseState(serialized, {
  customParsers: {
    Date: (obj) => new Date(obj.value),
    Map: (obj) => new Map(obj.entries)
  }
});
```

---

## STATE-DRIVEN META TAGS

### Pattern: Compute Meta Tags in Reducer

**Best Practice**: Meta tags should be computed from state in the reducer, then rendered via `<svelte:head>` in components.

```typescript
// State
interface AppState {
  posts: Post[];
  selectedPostId: number | null;
  meta: MetaTags;
}

interface MetaTags {
  title: string;
  description: string;
  ogImage?: string;
  canonical?: string;
}

// Reducer computes meta tags
case 'selectPost': {
  const post = state.posts.find(p => p.id === action.postId);

  return [
    {
      ...state,
      selectedPostId: action.postId,
      meta: post
        ? {
            title: `${post.title} - Blog`,
            description: post.content.slice(0, 160),
            ogImage: `/og/post-${post.id}.jpg`,
            canonical: `https://example.com/posts/${post.id}`
          }
        : state.meta
    },
    Effect.none()
  ];
}

// Component renders meta tags
<svelte:head>
  <title>{$store.meta.title}</title>
  <meta name="description" content={$store.meta.description} />
  {#if $store.meta.ogImage}
    <meta property="og:title" content={$store.meta.title} />
    <meta property="og:description" content={$store.meta.description} />
    <meta property="og:image" content={$store.meta.ogImage} />
  {/if}
  {#if $store.meta.canonical}
    <link rel="canonical" href={$store.meta.canonical} />
  {/if}
</svelte:head>
```

**Why**: Meta tags are part of application state. Computing them in the reducer ensures they're consistent on server and client, and testable with TestStore.

---

## COMPLETE SSR EXAMPLE

### Server (Fastify)

```typescript
// server/index.ts
import Fastify from 'fastify';
import fastifyStatic from '@fastify/static';
import { createStore } from '@composable-svelte/core';
import { renderToHTML } from '@composable-svelte/core/ssr';
import App from '../shared/App.svelte';
import { appReducer } from '../shared/reducer';
import { initialState } from '../shared/types';
import { loadPosts } from './data';
import { parsePostFromURL } from '../shared/routing';

const app = Fastify({
  logger: {
    level: process.env.NODE_ENV === 'production' ? 'info' : 'debug'
  }
});

// Serve static files (client bundle)
app.register(fastifyStatic, {
  root: join(__dirname, '../client'),
  prefix: '/assets/'
});

// Main SSR route handler
async function renderAppRoute(request: any, reply: any) {
  try {
    // 1. Parse URL using router (same logic as client!)
    const posts = await loadPosts();
    const path = request.url;
    const requestedPostId = parsePostFromURL(path, posts[0]?.id || 1);

    // Find the requested post
    const selectedPost = posts.find((p) => p.id === requestedPostId) || posts[0];

    // 2. Create store with URL-driven state
    const store = createStore({
      initialState: {
        ...initialState,
        posts,
        selectedPostId: selectedPost?.id || null,
        // Set initial meta based on URL-selected post
        meta: selectedPost
          ? {
              title: `${selectedPost.title} - Blog`,
              description: selectedPost.content.slice(0, 160),
              ogImage: `/og/post-${selectedPost.id}.jpg`,
              canonical: `https://example.com/posts/${selectedPost.id}`
            }
          : initialState.meta
      },
      reducer: appReducer,
      dependencies: {}
      // ssr.deferEffects defaults to true, so effects are automatically skipped
    });

    // 3. Render component to HTML
    const html = renderToHTML(App, { store }, {
      head: `
        <link rel="stylesheet" href="/assets/index.css">
        <style>
          * { box-sizing: border-box; }
          body { margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; }
        </style>
      `,
      clientScript: '/assets/index.js'
    });

    // 4. Send response
    reply.type('text/html').send(html);
  } catch (error) {
    request.log.error(error);
    reply.status(500).send({
      error: 'Internal Server Error',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}

// Register routes
app.get('/', renderAppRoute);
app.get('/posts/:id', renderAppRoute);

// Start server
const start = async () => {
  try {
    const port = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;
    const host = process.env.HOST || '0.0.0.0';

    await app.listen({ port, host });
    console.log(`Server running at http://localhost:${port}`);
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

start();
```

### Client

```typescript
// client/index.ts
import { hydrate as hydrateComponent } from 'svelte';
import { hydrateStore } from '@composable-svelte/core/ssr';
import { syncBrowserHistory } from '@composable-svelte/core/routing';
import App from '../shared/App.svelte';
import { appReducer } from '../shared/reducer';
import type { AppDependencies, AppState, AppAction } from '../shared/types';
import { parserConfig, serializerConfig } from '../shared/routing';

// Client-side dependencies
const clientDependencies: AppDependencies = {
  fetchPosts: async () => {
    // In a real app, this would fetch from an API
    // For this example, we'll just return empty array
    // (the data is already loaded via SSR)
    return [];
  }
};

// Hydrate the application
function hydrate() {
  try {
    // 1. Read serialized state from the server
    const stateElement = document.getElementById('__COMPOSABLE_SVELTE_STATE__');

    if (!stateElement || !stateElement.textContent) {
      throw new Error('No hydration data found. Server-side rendering may have failed.');
    }

    // 2. Hydrate the store with client dependencies
    const store = hydrateStore<AppState, AppAction, AppDependencies>(
      stateElement.textContent,
      {
        reducer: appReducer,
        dependencies: clientDependencies
      }
    );

    // 3. Sync browser history with state (URL routing!)
    syncBrowserHistory(store, {
      serializers: serializerConfig.serializers,
      parsers: parserConfig.parsers,
      // Map state → destination for URL serialization
      getDestination: (state) => {
        if (state.selectedPostId !== null) {
          return { type: 'post' as const, state: { postId: state.selectedPostId } };
        }
        return null;
      },
      // Map destination → action for back/forward navigation
      destinationToAction: (dest) => {
        if (dest?.type === 'post') {
          return { type: 'selectPost', postId: dest.state.postId };
        }
        return null;
      }
    });

    // 4. Hydrate the app (reuse existing DOM from SSR)
    const app = hydrateComponent(App, {
      target: document.body,
      props: { store }
    });

    console.log('✅ Composable Svelte hydrated successfully with URL routing');

    // Cleanup on unmount (for HMR during development)
    if (import.meta.hot) {
      import.meta.hot.dispose(() => {
        app.$destroy?.();
      });
    }
  } catch (error) {
    console.error('❌ Hydration failed:', error);

    // Show error to user
    document.body.innerHTML = `
      <div style="display: flex; align-items: center; justify-content: center; min-height: 100vh; background: #fee; color: #c00; font-family: monospace; padding: 2rem;">
        <div>
          <h1>Hydration Error</h1>
          <p>${error instanceof Error ? error.message : 'Unknown error'}</p>
        </div>
      </div>
    `;
  }
}

// Start hydration when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', hydrate);
} else {
  hydrate();
}
```

---

## AVOIDING STATE LEAKS

### ❌ WRONG - Shared Store

```typescript
// server.ts
// ❌ BAD: Shared store across requests
const globalStore = createStore({
  initialState: {},
  reducer: appReducer,
  dependencies: {}
});

app.get('/', (req, res) => {
  // ❌ State leaks between requests!
  const html = renderToHTML(App, { store: globalStore });
  res.send(html);
});
```

### ✅ CORRECT - Per-Request Store

```typescript
// server.ts
// ✅ GOOD: Create new store for each request
app.get('/', async (req, res) => {
  const store = createStore({
    initialState: await loadDataForRequest(req),
    reducer: appReducer,
    dependencies: {}
  });

  const html = renderToHTML(App, { store });
  res.send(html);
});
```

**Why**: Each request needs its own store to prevent state leaking between users.

---

## I18N SSR PATTERNS

### Manual i18n Initialization (Fastify/Custom Servers)

**Key Pattern**: For non-SvelteKit servers (Fastify, Express, etc.), manually initialize i18n state and dependencies.

```typescript
import { createInitialI18nState, BundledTranslationLoader, createStaticLocaleDetector, serverDOM, browserDOM } from '@composable-svelte/core/i18n';

// Server: Detect locale from request
function detectLocale(request: any): string {
  // 1. Check query param (?lang=fr)
  const queryLang = request.query?.lang;
  if (queryLang && ['en', 'fr', 'es'].includes(queryLang)) {
    return queryLang;
  }

  // 2. Check Accept-Language header
  const acceptLanguage = request.headers?.['accept-language'];
  if (acceptLanguage && typeof acceptLanguage === 'string') {
    const languages = acceptLanguage.split(',')
      .map(lang => lang.trim().split(';')[0].split('-')[0]);

    for (const lang of languages) {
      if (['en', 'fr', 'es'].includes(lang)) {
        return lang;
      }
    }
  }

  // 3. Default to English
  return 'en';
}

// Server: Initialize i18n for SSR
async function renderApp(request, reply) {
  const locale = detectLocale(request);
  const i18nState = createInitialI18nState(locale, ['en', 'fr', 'es'], 'en');

  // Create translation loader
  const translationLoader = new BundledTranslationLoader({
    bundles: {
      en: { common: enTranslations },
      fr: { common: frTranslations },
      es: { common: esTranslations }
    }
  });

  // Preload translations for current locale
  const translations = await translationLoader.load('common', locale);
  const updatedI18nState = {
    ...i18nState,
    translations: { [`${locale}:common`]: translations }
  };

  // Create mock storage for server (no-op)
  const mockStorage = {
    getItem: (key: string) => null,
    setItem: (key: string, value: unknown) => {},
    removeItem: (key: string) => {},
    keys: () => [],
    has: (key: string) => false,
    clear: () => {}
  };

  // Create i18n dependencies for server
  const i18nDependencies = {
    translationLoader,
    localeDetector: createStaticLocaleDetector(locale, ['en', 'fr', 'es']),
    storage: mockStorage,
    dom: serverDOM
  };

  const store = createStore({
    initialState: {
      ...initialState,
      i18n: updatedI18nState
    },
    reducer: appReducer,
    dependencies: {
      ...otherDependencies,
      ...i18nDependencies
    }
  });

  const html = renderToHTML(App, { store });
  reply.type('text/html').send(html);
}
```

### Client i18n Hydration

```typescript
import { BundledTranslationLoader, createStaticLocaleDetector, browserDOM } from '@composable-svelte/core/i18n';

// Client: Hydrate with localStorage-backed storage
const clientStorage = {
  getItem: (key: string) => {
    try {
      return localStorage.getItem(key);
    } catch {
      return null;
    }
  },
  setItem: (key: string, value: unknown) => {
    try {
      localStorage.setItem(key, String(value));
    } catch {}
  },
  removeItem: (key: string) => {
    try {
      localStorage.removeItem(key);
    } catch {}
  },
  keys: () => {
    try {
      return Object.keys(localStorage);
    } catch {
      return [];
    }
  },
  has: (key: string) => {
    try {
      return localStorage.getItem(key) !== null;
    } catch {
      return false;
    }
  },
  clear: () => {
    try {
      localStorage.clear();
    } catch {}
  }
};

// Hydrate i18n on client
async function hydrate() {
  const stateElement = document.getElementById('__COMPOSABLE_SVELTE_STATE__');
  const parsedState = JSON.parse(stateElement.textContent);
  const locale = parsedState.i18n.currentLocale;

  const translationLoader = new BundledTranslationLoader({
    bundles: {
      en: { common: enTranslations },
      fr: { common: frTranslations },
      es: { common: esTranslations }
    }
  });

  const i18nDependencies = {
    translationLoader,
    localeDetector: createStaticLocaleDetector(locale, ['en', 'fr', 'es']),
    storage: clientStorage,  // Real localStorage
    dom: browserDOM
  };

  const store = hydrateStore(stateElement.textContent, {
    reducer: appReducer,
    dependencies: {
      ...otherDependencies,
      ...i18nDependencies
    }
  });

  hydrateComponent(App, { target: document.body, props: { store } });
}
```

### Storage Interface Requirements

**Critical**: The i18n system expects a `Storage` interface, not a `Map`.

```typescript
// ❌ WRONG - Map doesn't have setItem/getItem
const i18nDependencies = {
  storage: new Map()  // TypeError: storage.setItem is not a function
};

// ✅ CORRECT - Implement Storage interface
const mockStorage: Storage = {
  getItem: (key: string) => null,
  setItem: (key: string, value: unknown) => {},
  removeItem: (key: string) => {},
  keys: () => [],
  has: (key: string) => false,
  clear: () => {}
};
```

### i18n + URL Routing Pattern

Combine i18n with URL routing to support language selection via URL:

```typescript
// Server: Support ?lang=fr query parameter
app.get('/', async (req, res) => {
  const locale = detectLocale(req);  // Checks ?lang= first, then Accept-Language
  const destination = parseDestinationFromURL(req.url);

  const store = createStore({
    initialState: {
      destination,
      i18n: createInitialI18nState(locale, ['en', 'fr', 'es'])
      // ...
    }
  });
  // ...
});
```

**URL Pattern**: `http://localhost:3000/?lang=fr` or `http://localhost:3000/posts/1?lang=es`

---

## SSR PERFORMANCE CONSIDERATIONS

### 1. Defer Effects on Server

**Automatic**: Effects are automatically deferred on server (via `ssr.deferEffects: true` default).

```typescript
// No need to set this explicitly - it's the default
const store = createStore({
  initialState: data,
  reducer: appReducer,
  dependencies: {},
  // ssr: { deferEffects: true }  // Default
});
```

### 2. Load Data Once on Server

```typescript
app.get('/posts/:id', async (req, res) => {
  // Load data once
  const posts = await loadPosts();
  const postId = parseInt(req.params.id, 10);
  const selectedPost = posts.find(p => p.id === postId);

  // Initialize state with loaded data
  const store = createStore({
    initialState: {
      posts,  // Data already loaded
      selectedPostId: postId,
      meta: computeMeta(selectedPost)
    },
    reducer: appReducer,
    dependencies: {}
  });

  const html = renderToHTML(App, { store });
  res.send(html);
});
```

**Why**: Server pre-loads data, client hydrates with it. No need to fetch again on client.

---

## COMMON SSR PITFALLS

### 1. Using Browser APIs on Server

**❌ WRONG**:
```typescript
// reducer.ts
case 'init':
  const theme = localStorage.getItem('theme'); // ❌ localStorage not available on server!
  return [{ ...state, theme }, Effect.none()];
```

**✅ CORRECT**:
```typescript
// Use environment detection
import { isServer } from '@composable-svelte/core/ssr';

case 'init':
  const theme = isServer ? 'light' : localStorage.getItem('theme') || 'light';
  return [{ ...state, theme }, Effect.none()];
```

---

### 2. Not Handling Hydration Errors

**❌ WRONG**:
```typescript
// client.ts
const store = hydrateStore(stateJSON, { reducer, dependencies });
mount(App, { target: document.body, props: { store } });
// If hydration fails, user sees blank screen!
```

**✅ CORRECT**:
```typescript
try {
  const store = hydrateStore(stateJSON, { reducer, dependencies });
  mount(App, { target: document.body, props: { store } });
  console.log('✅ Hydrated successfully');
} catch (error) {
  console.error('❌ Hydration failed:', error);
  // Show error UI
  document.body.innerHTML = `<div class="error">Hydration failed: ${error.message}</div>`;
}
```

---

### 3. Forgetting to Set Meta Tags

**❌ WRONG**:
```typescript
// No meta tags in state, no <svelte:head> in component
// Search engines see generic meta tags
```

**✅ CORRECT**:
```typescript
// State includes meta tags
interface AppState {
  meta: { title: string; description: string; ogImage?: string };
}

// Component renders meta tags
<svelte:head>
  <title>{$store.meta.title}</title>
  <meta name="description" content={$store.meta.description} />
</svelte:head>
```

---

## SSR CHECKLIST

- [ ] 1. Create new store for each request (no shared state)
- [ ] 2. Use empty dependencies on server
- [ ] 3. Load data based on URL on server
- [ ] 4. Initialize state with loaded data
- [ ] 5. Compute meta tags in reducer
- [ ] 6. Render meta tags with `<svelte:head>`
- [ ] 7. Hydrate with real dependencies on client
- [ ] 8. Sync browser history on client (if using routing)
- [ ] 9. Handle hydration errors gracefully
- [ ] 10. Use environment detection for browser APIs

---

## STATIC SITE GENERATION (SSG)

### generateStaticSite - Build-Time Generation

```typescript
import { generateStaticSite } from '@composable-svelte/core/ssr';
import App from './App.svelte';
import { appReducer } from './reducer';

const posts = await loadPosts();

const result = await generateStaticSite(App, {
  routes: [
    { path: '/' },
    { path: '/about' },
    {
      path: '/posts/:id',
      paths: posts.map(p => `/posts/${p.id}`),
      getServerProps: async (path) => ({
        post: await loadPost(path)
      })
    }
  ],
  outDir: './dist',
  baseURL: 'https://example.com',
  onPageGenerated: (path, outPath) => {
    console.log(`Generated ${path} → ${outPath}`);
  }
}, {
  reducer: appReducer,
  dependencies: {},
  getInitialState: (path) => ({ /* compute state for path */ })
});

console.log(`Generated ${result.pagesGenerated} pages in ${result.duration}ms`);
```

### SSG Configuration

**Full-Site Generation**:
```typescript
// Generate all routes at build time
await generateStaticSite(App, {
  routes: [
    { path: '/' },                        // Static route
    { path: '/about' },                   // Static route
    {
      path: '/posts/:id',                 // Dynamic route
      paths: ['/posts/1', '/posts/2']     // Pre-rendered paths
    }
  ],
  outDir: './static'
}, { reducer, dependencies: {} });
```

**Selective Generation**:
```typescript
// Generate only specific pages
await generateStaticSite(App, {
  routes: [
    { path: '/' },                    // Only homepage
    { path: '/posts/1' }              // Only one post
  ],
  outDir: './static'
}, { reducer, dependencies: {} });
```

**Dynamic Path Generation**:
```typescript
// Fetch paths dynamically at build time
await generateStaticSite(App, {
  routes: [
    {
      path: '/posts/:id',
      paths: async () => {
        const posts = await loadAllPosts();
        return posts.map(p => `/posts/${p.id}`);
      }
    }
  ],
  outDir: './static'
}, { reducer, dependencies: {} });
```

### SSG + i18n Pattern

**Multi-Locale Static Generation**:
```typescript
const supportedLocales = ['en', 'fr', 'es'];
const posts = await loadPosts();

// Generate routes for each locale
const routes = [];
for (const locale of supportedLocales) {
  const localePrefix = locale === 'en' ? '' : `/${locale}`;

  // Home page
  routes.push({
    path: `${localePrefix}/`,
    getServerProps: async (path) => {
      const i18nState = await initI18n(locale);
      return { ...initialState, i18n: i18nState };
    }
  });

  // Post pages
  for (const post of posts) {
    routes.push({
      path: `${localePrefix}/posts/${post.id}`,
      getServerProps: async (path) => {
        const i18nState = await initI18n(locale);
        const post = await loadPost(post.id);
        return { ...initialState, post, i18n: i18nState };
      }
    });
  }
}

await generateStaticSite(App, { routes, outDir: './static' }, { reducer });
```

### SSG Build Script

**Create build script** (`src/build/ssg.ts`):
```typescript
import { generateStaticSite } from '@composable-svelte/core/ssr';
import App from '../shared/App.svelte';
import { appReducer } from '../shared/reducer';
import { loadPosts } from '../server/data';

async function build() {
  console.log('Starting SSG build...');

  const posts = await loadPosts();

  const result = await generateStaticSite(App, {
    routes: [
      { path: '/' },
      {
        path: '/posts/:id',
        paths: posts.map(p => `/posts/${p.id}`),
        getServerProps: async (path) => {
          const id = parseInt(path.split('/').pop()!);
          const post = await loadPost(id);
          return { posts: [post] };
        }
      }
    ],
    outDir: './static',
    baseURL: 'https://example.com'
  }, {
    reducer: appReducer,
    dependencies: {}
  });

  console.log(`✅ Generated ${result.pagesGenerated} pages in ${result.duration}ms`);
}

build().catch(console.error);
```

**Add script to package.json**:
```json
{
  "scripts": {
    "build:ssg": "vite build && tsx src/build/ssg.ts"
  }
}
```

**Run build**:
```bash
pnpm build:ssg
```

### SSG vs SSR Decision Matrix

| Use Case | Recommendation | Reason |
|----------|----------------|--------|
| Blog posts | SSG | Content rarely changes, many reads |
| User dashboards | SSR | Personalized, private data |
| Product catalog | SSG | Public, static content |
| Search results | SSR | Dynamic, user-specific |
| Marketing pages | SSG | Static, performance-critical |
| Admin panels | SSR | Dynamic, authenticated |

### Hybrid SSG + SSR Pattern

**Use SSG for static pages, SSR for dynamic**:

1. **Build-time** (SSG): Generate static pages
   ```bash
   pnpm build:ssg  # Generates /static/index.html, /static/posts/*/index.html
   ```

2. **Runtime** (SSR): Serve dynamic pages
   ```typescript
   // Server fallback for non-static routes
   app.get('*', async (req, res) => {
     // Try to serve static file first
     const staticPath = join(__dirname, '../static', req.url, 'index.html');
     if (existsSync(staticPath)) {
       return res.sendFile(staticPath);
     }

     // Fall back to SSR for dynamic routes
     const store = createStore({ /* ... */ });
     const html = renderToHTML(App, { store });
     res.send(html);
   });
   ```

---

## SUMMARY

This skill covers SSR and SSG patterns for Composable Svelte:

1. **SSR APIs**: renderToHTML, hydrateStore
2. **SSG APIs**: generateStaticSite, generateStaticPage
3. **Isomorphic Patterns**: Server vs client dependencies, router pure functions
4. **State Initialization**: Parse URL on server, initialize state
5. **State Serialization**: Automatic serialization/deserialization
6. **Meta Tags**: State-driven meta tags computed by reducer
7. **i18n SSR/SSG**: Manual i18n initialization, locale detection, multi-locale generation
8. **Complete Examples**: Fastify server + SSG build script + client hydration
9. **Avoiding Pitfalls**: Per-request stores, environment detection, error handling

**SSR Key Points**:
- Create new store for each request
- Use empty dependencies on server
- Hydrate with real dependencies on client
- State is serialized automatically

**SSG Key Points**:
- Generate static HTML at build time
- Support dynamic routes with path enumeration
- Use getServerProps to load data for each path
- Combine with i18n for multi-locale sites
- Ideal for content-heavy, rarely-changing sites

**i18n Key Points**:
- Use `BundledTranslationLoader` with `bundles` wrapper
- Server: Mock storage (no-op), `createStaticLocaleDetector`, `serverDOM`
- Client: localStorage-backed storage, `createStaticLocaleDetector`, `browserDOM`
- Detect locale from query param → Accept-Language → default
- Storage interface requires `getItem/setItem`, not Map's `get/set`

For core architecture, see **composable-svelte-core** skill.
For URL routing, see **composable-svelte-navigation** skill.
For testing SSR/SSG, see **composable-svelte-testing** skill.
