---
name: managing-server-vs-client-boundaries
description: Teaches when to use Server Components vs Client Components in React 19, including the 'use client' directive and boundary patterns. Use when architecting components, choosing component types, or working with Server Components.
allowed-tools: Read, Write, Edit, Glob, Grep
version: 1.0.0
---

# Server vs Client Component Boundaries

**Role**: Choose between Server and Client Components effectively and manage boundaries between them.

## When to Activate

- User mentions Server Components, Client Components, or `'use client'`
- Architecting component hierarchy
- Accessing server-only or client-only APIs
- Working with React Server Components frameworks (Next.js, Remix)
- Errors about hooks or browser APIs in Server Components

## Component Comparison

| Feature                             | Server Component | Client Component      |
| ----------------------------------- | ---------------- | --------------------- |
| Directive                           | None (default)   | `'use client'`        |
| Hooks; Event handlers; Browser APIs | ❌               | ✅                    |
| Async/await (top-level)             | ✅               | ⚠️ Limited            |
| Database/server APIs                | ✅ Direct        | ❌ Use Server Actions |
| Import Server Components            | ✅               | ❌ Pass as children   |
| Bundle impact                       | 📦 Zero          | 📦 Sent to client     |
| Bundle reduction                    | 20%-90%          | —                     |

**Key Decision**: Needs interactivity/hooks/browser APIs → Client Component; static/server-only data → Server Component

## Quick Checklist

Choose **Client Component** if: needs hooks, event handlers, browser APIs, or state management.

Choose **Server Component** if: purely presentational, fetches server data, accesses databases/server APIs.

## Implementing Components

**Step 1: Add `'use client'` at file top** (Client Components only)

```javascript
'use client';

import { useState } from 'react';

export function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(count + 1)}>Count: {count}</button>;
}
```

**Step 2: Compose Server + Client**

Server Components import Client Components; pass Server Components as children to avoid circular imports:

```javascript
// Server Component: Can fetch data, import CC
import { Counter } from './Counter';

async function Page() {
  const data = await db.getData();
  return (
    <div>
      <h1>{data.title}</h1>
      <Counter />
    </div>
  );
}

// ❌ WRONG: Client Component importing Server Component
('use client');
import ServerComponent from './ServerComponent'; // ERROR

// ✅ RIGHT: Pass Server Component as children
<ClientWrapper>
  <ServerComponent />
</ClientWrapper>;
```

## Common Patterns

**Interactivity at leaf nodes**: Server Component fetches data, passes to Client Component for interaction

```javascript
async function ProductPage({ id }) {
  const product = await db.products.find(id);
  return (
    <>
      <ProductDetails product={product} />
      <AddToCartButton productId={id} />
    </>
  );
}
```

**Server data in Client Component**: Pass as props (serialize data)

```javascript
async function ServerComponent() {
  const data = await fetchData();
  return <ClientComponent data={data} />;
}
```

**Server logic from Client**: Use Server Actions

```javascript
async function ServerComponent() {
  async function serverAction() {
    'use server';
    await db.update(...);
  }
  return <ClientForm action

={serverAction} />;
}
```

## Example: Product Page with Cart

```javascript
// Server Component
import { AddToCart } from './AddToCart';
import { Reviews } from './Reviews';

async function ProductPage({ productId }) {
  const product = await db.products.find(productId);
  const reviews = await db.reviews.findByProduct(productId);

  return (
    <main>
      <img src={product.image} alt={product.name} />
      <section>
        <h1>{product.name}</h1>
        <p>{product.description}</p>
        <p>${product.price}</p>
        <AddToCart productId={productId} />
      </section>
      <Reviews reviews={reviews} />
    </main>
  );
}

// Client Component
('use client');
import { useState } from 'react';

export function AddToCart({ productId }) {
  const [adding, setAdding] = useState(false);

  async function handleAdd() {
    setAdding(true);
    await fetch('/api/cart', {
      method: 'POST',
      body: JSON.stringify({ productId }),
    });
    setAdding(false);
  }

  return (
    <button onClick={handleAdd} disabled={adding}>
      {adding ? 'Adding...' : 'Add to Cart'}
    </button>
  );
}

// Server Component with real-time Client
async function Dashboard() {
  const stats = await db.stats.getLatest();
  return (
    <>
      <DashboardStats stats={stats} />
      <LiveMetrics />
    </>
  );
}

// Client Component with WebSocket
('use client');
import { useEffect, useState } from 'react';

export function LiveMetrics() {
  const [metrics, setMetrics] = useState(null);

  useEffect(() => {
    const ws = new WebSocket('/api/metrics');
    ws.onmessage = (event) => setMetrics(JSON.parse(event.data));
    return () => ws.close();
  }, []);

  return metrics ? <div>Active Users: {metrics.activeUsers}</div> : <div>Connecting...</div>;
}

// Server Component with Server Action
async function ContactPage() {
  async function submitContact(formData) {
    'use server';
    await db.contacts.create({
      email: formData.get('email'),
      message: formData.get('message'),
    });
  }

  return (
    <form action={submitContact}>
      <input name="email" type="email" />
      <textarea name="message" />
      <button type="submit">Send</button>
    </form>
  );
}
```

## Requirements

**MUST**: `'use client'` at file top for Client Components; before any imports; serialize props (Server → Client); use Server Actions for server-side logic from Client

**SHOULD**: Keep most components as Server Components (smaller bundle); place `'use client'` at leaf nodes (smallest boundary); use Server Components for data fetching; use Client Components only for interactivity

**NEVER**: Import Server Components into Client Components; use hooks in Server Components; access browser APIs in Server Components; pass non-serializable props (functions, classes, symbols); om

it `'use client'` directive

## Validation Checklist

1. **Component Types**: Client Components have `'use client'` at top; Server Components have no directive; no hooks/event handlers in Server Components
2. **Data Flow**: Server → Client props are serializable; Client → Server uses Server Actions; no Server Components imported in Client
3. **Functionality**: Server Components fetch data correctly; Client Components handle interaction; no hydration mismatches; no runtime errors about hooks/browser APIs
4. **Bundle**: Only necessary components are Client Components; most stay on server; JavaScript minimized

## References

- **Server Components**: `research/react-19-comprehensive.md` (lines 71-82)
- **Server Actions**: `forms/skills/server-actions/SKILL.md`
- **Component Composition**: `component-composition/SKILL.md`
