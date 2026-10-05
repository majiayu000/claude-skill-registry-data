---
name: nextjs
description: Use when building Next.js applications with the App Router. Covers server and client component boundaries, data fetching and caching, server actions, streaming, and rendering strategy.
metadata:
  category: frontend
  version: 1.0.0
  tags: [nextjs, react, ssr, rsc, caching]
---

# Next.js

## Purpose

Build Next.js applications where the server/client boundary is drawn deliberately, caching is understood rather than fought, and the rendering strategy matches what the page actually needs.

## When to Use

- Building or reviewing a Next.js App Router application.
- Deciding what renders on the server versus the client.
- Debugging stale data or unexpectedly dynamic rendering.
- Implementing mutations with server actions.

## Capabilities

- Server and client component composition.
- Data fetching, caching, and revalidation (time-based and tag-based).
- Server actions for mutations, with validation and revalidation.
- Streaming with Suspense and loading boundaries.
- Rendering strategy: static, dynamic, ISR, partial prerendering.

## Inputs

- The page, its data dependencies, and how fresh each must be.
- Which parts are genuinely interactive.
- Auth model and whether the page is personalized.

## Outputs

- A component tree with `"use client"` pushed as far down as possible.
- Explicit cache and revalidation settings per fetch.
- Mutations that revalidate exactly what they changed.

## Workflow

1. **Default to server components** — They ship no JavaScript. Add `"use client"` only where you need state, effects, or browser APIs — and add it to the leaf, not the page.
2. **Fetch where you render** — Fetch data in the component that needs it. Requests are deduplicated within a render pass; prop-drilling data down from the page is unnecessary.
3. **Set the cache explicitly** — Every `fetch` gets a deliberate `cache` or `next.revalidate`. Relying on the framework default is how you ship stale prices.
4. **Stream the slow parts** — Wrap slow sections in `<Suspense>` with a meaningful fallback so the shell renders immediately.
5. **Mutate with server actions** — Validate the input (it is a public endpoint, whatever it looks like), perform the write, then `revalidateTag` or `revalidatePath` for exactly what changed.

## Best Practices

- `"use client"` at the top of a page turns the entire subtree into client components. Push it to the interactive leaf — the button, not the layout.
- A server action is an HTTP endpoint. It has no implicit authorization. Check the session inside it, every time.
- Reading `cookies()`, `headers()`, or `searchParams` opts the route into dynamic rendering. If a page unexpectedly stopped being static, this is why.
- Tag-based revalidation (`revalidateTag`) is far more precise than path-based. Tag by entity, invalidate on write.
- Never put a secret in a component that could be a client component. If it is imported by anything with `"use client"`, it ships to the browser.
- Use `loading.tsx` and `error.tsx` at every route segment. The defaults are a blank screen and a crash.

## Examples

**Server component with explicit caching, streaming a slow section:**

```tsx
// app/orders/[id]/page.tsx  — a server component by default
export default async function OrderPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  const order = await fetch(`${API}/orders/${id}`, {
    next: { tags: [`order:${id}`], revalidate: 60 },
  }).then((r) => r.json());

  return (
    <main>
      <OrderHeader order={order} />

      {/* Shell renders immediately; this streams in when ready. */}
      <Suspense fallback={<TimelineSkeleton />}>
        <OrderTimeline orderId={id} />
      </Suspense>

      {/* Only this leaf ships JavaScript. */}
      <RefundButton orderId={id} />
    </main>
  );
}
```

**Server action: authorize, validate, mutate, revalidate:**

```tsx
"use server";

export async function refundOrder(orderId: string, formData: FormData) {
  const session = await auth();
  if (!session) throw new Error("Unauthorized");     // a server action is a public endpoint

  const parsed = RefundSchema.safeParse({
    amountCents: formData.get("amountCents"),
  });
  if (!parsed.success) {
    return { error: parsed.error.flatten().fieldErrors };
  }

  await orders.refund(orderId, parsed.data.amountCents, session.user.id);
  revalidateTag(`order:${orderId}`);                  // precise invalidation
  return { ok: true };
}
```

## Notes

- Next.js caching changed materially between versions 14 and 15 — `fetch` is no longer cached by default in 15. Never rely on remembered defaults; set them.
- Partial prerendering serves a static shell with dynamic holes streamed in. It is the right default for pages that are mostly static with a personalized corner.
- A client component can render server components passed as `children`. That composition pattern lets you keep an interactive wrapper without dragging the whole subtree to the client.
