---
name: custom-global-events
description: Guidelines for creating/using the app’s typed global events system.
---

# Overview

Global events are used for cross-component communication without React context dependencies, allowing for simple function calls to trigger events across different parts of the application.

# Global Events Guidelines

Global events are used for cross-component communication without React context dependencies, allowing for simple function calls to trigger events across different parts of the application.

# Overview

The global events system lives at [global-event.tsx](../../../packages/app/src/lib/global-event.tsx) and is built on a typed `Event` subclass (`XCustomEvent`).

It exposes:

- `global_event_Event`: the canonical type map of event keys → `detail` payload types
- `global_event_dispatch(event, payload)`: dispatch a typed event (works outside React)
- `global_event_listen(event, handler, options?)`: listen with typed handler (works outside React)
- `useGlobalEvent(event, handler)`: React hook for subscriptions with stale-closure protection

# Event key naming

Event keys are string literals using the pattern:

(`module::event_name`), for example `ai_chat::open_canvas`.

# How to add or modify an event

When the user requests a new global event, you must:

# Update the event map

Add the new event key to the `global_event_Event` map in [global-event.tsx](../../../packages/app/src/lib/global-event.tsx).

Example:

```ts
export class global_event_Event extends XCustomEvent<{
	"ai_chat::open_canvas": {
		pageId: app_convex_Id<"pages">;
		mode: "diff" | "editor";
		modifiedContent?: string;
		threadId: string;
	};
	"ai_chat::open_canvas_by_path": {
		path: string;
	};
	"docs::focus_path": {
		path: string;
	};
}> {}
```

# Keep all event keys centralized

All supported global event keys must be declared in that `global_event_Event` type map. Do not introduce ad-hoc stringly-typed events elsewhere.

# Use the exported helpers

Prefer `global_event_dispatch` / `global_event_listen` / `useGlobalEvent` rather than calling `window.dispatchEvent(new CustomEvent(...))` directly.

# Usage patterns

## React components

Use `useGlobalEvent(eventName, handler)` to subscribe. The handler receives a typed event object, and the payload is on `event.detail`.

Example (from [canvas.tsx](../../../packages/app/src/components/canvas/canvas.tsx)):

```ts
useGlobalEvent("ai_chat::open_canvas", (e) => {
	const payload = e.detail;
	// payload.pageId, payload.mode, payload.modifiedContent, payload.threadId
});
```

## Non-React code (or manual lifecycle control)

Use `global_event_listen` directly when you need to wire AbortController, or you are outside React.

```ts
const controller = new AbortController();

const cleanup = global_event_listen(
	"ai_chat::open_canvas_by_path",
	(e) => {
		console.info("path:", e.detail.path);
	},
	{ signal: controller.signal },
);

// later:
controller.abort();
cleanup();
```

## Dispatching

Use `global_event_dispatch(eventName, payload)` from anywhere client-side.

Example (from [app-ai-chat.tsx](../../../packages/app/src/components/app-ai-chat.tsx)):

```ts
global_event_dispatch("ai_chat::open_canvas_by_path", { path: args.path });
```

# Handler typing and payload access

Handlers receive the typed event object, not the payload directly:

```ts
useGlobalEvent("ai_chat::open_canvas", (e) => {
	const payload = e.detail;
});
```

# Files and references

- Core implementation: [global-event.tsx](../../../packages/app/src/lib/global-event.tsx)
- Typed event base: `XCustomEvent` in [utils.ts](../../../packages/app/src/lib/utils.ts)
- Hook helper: `useLiveRef` in [utils-hooks.ts](../../../packages/app/src/hooks/utils-hooks.ts)
- Example consumers: [app-ai-chat.tsx](../../../packages/app/src/components/app-ai-chat.tsx), [canvas.tsx](../../../packages/app/src/components/canvas/canvas.tsx)
