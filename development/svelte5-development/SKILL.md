---
name: svelte5-development
description: Comprehensive Svelte 5 and SvelteKit development guidance. Use this skill when building Svelte components, working with runes, or developing SvelteKit applications. Covers reactive patterns, component architecture, routing, and data loading.
---

This skill provides guidance for Svelte 5 and SvelteKit development, covering runes, component patterns, routing, and common pitfalls.

## Svelte 5 Runes - Core Reactivity

### $state - Reactive State
Creates reactive state that updates the UI when changed.

```svelte
<script>
	let count = $state(0);
	let user = $state({ name: 'Alice', age: 30 });
</script>

<button onclick={() => count++}>Clicks: {count}</button>
<button onclick={() => user.age++}>Age: {user.age}</button>
```

**Deep Reactivity**: Objects and arrays become deeply reactive proxies. Mutations trigger updates:
```js
let todos = $state([{ done: false, text: 'learn svelte' }]);
todos[0].done = true; // triggers update
todos.push({ done: false, text: 'build app' }); // triggers update
```

**Classes**: Use $state in class fields:
```js
class Todo {
	done = $state(false);
	constructor(text) {
		this.text = $state(text);
	}
	reset = () => {
		this.text = '';
		this.done = false;
	}
}
```

**Important**: When you destructure reactive state, references are NOT reactive:
```js
let { done, text } = todos[0];
todos[0].done = true; // `done` variable won't update
```

**$state.raw**: Use for non-reactive objects (performance optimization):
```js
let data = $state.raw({ large: 'dataset' });
data.large = 'new value'; // no effect, must reassign entire object
data = { large: 'new value' }; // this works
```

### $derived - Computed Values
Creates values that automatically update when dependencies change.

```svelte
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);
	let tripled = $derived(count * 3);
</script>

<p>{count} × 2 = {doubled}</p>
<p>{count} × 3 = {tripled}</p>
```

**For complex logic, use $derived.by**:
```js
let numbers = $state([1, 2, 3]);
let total = $derived.by(() => {
	let sum = 0;
	for (const n of numbers) sum += n;
	return sum;
});
```

**Critical Rule**: NEVER update state inside $derived - it should be side-effect free.

**Overriding deriveds** (Svelte 5.25+): Useful for optimistic UI:
```js
let likes = $derived(post.likes);

async function onclick() {
	likes += 1; // optimistic update
	try {
		await likePost();
	} catch {
		likes -= 1; // rollback on error
	}
}
```

### $effect - Side Effects
Runs when state changes. Use for DOM manipulation, third-party libraries, analytics.

```svelte
<script>
	let size = $state(50);
	let canvas;

	$effect(() => {
		const ctx = canvas.getContext('2d');
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		// reruns when `size` changes
		ctx.fillRect(0, 0, size, size);
	});
</script>

<canvas bind:this={canvas} width="100" height="100"></canvas>
```

**Lifecycle**: Effects run after component mounts and after state changes (in microtask).

**Teardown functions**: Return a function to clean up:
```js
$effect(() => {
	const interval = setInterval(() => count++, 1000);
	return () => clearInterval(interval); // cleanup
});
```

**Dependencies**: Automatically tracks any $state/$derived read synchronously. Async reads (after await) are NOT tracked:
```js
$effect(() => {
	context.fillStyle = color; // tracked
	setTimeout(() => {
		context.fillRect(0, 0, size, size); // size NOT tracked!
	}, 0);
});
```

**Conditional dependencies**: Only depends on values read in the last run:
```js
$effect(() => {
	if (condition) {
		confetti({ colors: [color] }); // only depends on color if condition is true
	}
});
```

**$effect.pre**: Runs BEFORE DOM updates (rare, for things like autoscroll).

**CRITICAL - When NOT to use $effect**:
- ❌ Don't synchronize state (use $derived instead)
- ❌ Don't use for computed values
- ✅ DO use for: canvas drawing, third-party libs, analytics, intervals, DOM manipulation

```svelte
<!-- ❌ BAD - Don't do this -->
<script>
	let count = $state(0);
	let doubled = $state();
	$effect(() => {
		doubled = count * 2; // WRONG! Use $derived
	});
</script>

<!-- ✅ GOOD - Do this -->
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);
</script>
```

### $props - Component Props
Receives data from parent components.

```svelte
<!-- Parent.svelte -->
<Child message="hello" count={42} />

<!-- Child.svelte -->
<script>
	let { message, count = 0 } = $props(); // destructuring with defaults
</script>

<p>{message} - {count}</p>
```

**Renaming props** (for reserved words or invalid identifiers):
```js
let { super: trouper = 'default' } = $props();
```

**Rest props**:
```js
let { a, b, ...others } = $props();
```

**Type safety** (TypeScript):
```svelte
<script lang="ts">
	let { message }: { message: string } = $props();
	// or
	interface Props {
		message: string;
		count?: number;
	}
	let { message, count = 0 }: Props = $props();
</script>
```

**Important**: Props update reactively, but you should NOT mutate them (unless $bindable).

### $bindable - Two-Way Binding
Allows child components to update parent state.

```svelte
<!-- FancyInput.svelte -->
<script>
	let { value = $bindable(), ...props } = $props();
</script>

<input bind:value {...props} />

<!-- Parent.svelte -->
<script>
	import FancyInput from './FancyInput.svelte';
	let message = $state('hello');
</script>

<FancyInput bind:value={message} />
<p>{message}</p>
```

**Fallback values**:
```js
let { value = $bindable('default value') } = $props();
```

**Use sparingly**: Most components should use callback props instead of $bindable.

## Common Patterns and Pitfalls

### Effect vs Derived
```svelte
<script>
	let a = $state(1);
	let b = $state(2);

	// ✅ GOOD - Use $derived for computed values
	let sum = $derived(a + b);

	// ❌ BAD - Don't use $effect for this
	let sum2 = $state(0);
	$effect(() => {
		sum2 = a + b; // WRONG!
	});

	// ✅ GOOD - Use $effect for side effects only
	$effect(() => {
		console.log('Sum changed:', sum);
		analytics.track('calculation', { sum });
	});
</script>
```

### Navigation with Remote Functions
When using SvelteKit's `remoteFunctions` feature, standard `<a href>` links don't work for client-side navigation.

```svelte
<script>
	import { goto } from '$app/navigation';
</script>

<!-- ❌ DON'T use regular links with remote functions -->
<a href="/songs/{id}/edit">{title}</a>

<!-- ✅ DO use goto() -->
<button onclick={() => goto(`/songs/${id}/edit`)}>{title}</button>
```

Style buttons as links:
```css
.link-button {
	background: none;
	border: none;
	padding: 0;
	color: inherit;
	cursor: pointer;
	text-decoration: underline;
}
```

### Async Operations and Form Initialization
```svelte
<script>
	let song = $state({ current: null });
	let title = $state('');
	let initialized = $state(false);

	// ✅ GOOD - Use $effect for async initialization
	$effect(() => {
		if (song.current && !initialized) {
			title = song.current.title || '';
			initialized = true;
		}
	});
</script>
```

## SvelteKit Routing

### File Structure
- `+page.svelte` - Page component
- `+page.js` - Universal load (runs server + client)
- `+page.server.js` - Server-only load
- `+layout.svelte` - Layout component (wraps pages)
- `+layout.js` / `+layout.server.js` - Layout load functions
- `+error.svelte` - Error page
- `+server.js` - API endpoints

### Dynamic Routes
- `[slug]` - Single parameter
- `[...rest]` - Rest parameter (catches multiple segments)
- `[[optional]]` - Optional parameter

Example: `src/routes/blog/[slug]/+page.svelte` matches `/blog/hello-world`

### Loading Data

**Page Load** (`+page.js` or `+page.server.js`):
```js
/** @type {import('./$types').PageLoad} */
export function load({ params, url, fetch }) {
	return {
		post: {
			title: `Post ${params.slug}`,
			content: 'Content here'
		}
	};
}
```

**Layout Load** (`+layout.server.js`):
```js
/** @type {import('./$types').LayoutServerLoad} */
export async function load() {
	return {
		sections: [
			{ slug: 'profile', title: 'Profile' },
			{ slug: 'settings', title: 'Settings' }
		]
	};
}
```

**Accessing Data in Components**:
```svelte
<script>
	/** @type {import('./$types').PageProps} */
	let { data } = $props();
</script>

<h1>{data.post.title}</h1>
```

**Parent Data Access**:
```js
export async function load({ parent }) {
	const { user } = await parent();
	return { username: user.name };
}
```

### Universal vs Server Load

**Use `+page.js` (Universal) when**:
- Fetching from public APIs
- No private credentials needed
- Returning custom classes or constructors
- Running same logic server + client

**Use `+page.server.js` (Server) when**:
- Accessing database directly
- Using private environment variables
- Reading from filesystem
- Need to serialize data for client

**Server load returns must be serializable** (JSON + Date, Map, Set, RegExp, BigInt).

### Form Actions

```js
// +page.server.js
export const actions = {
	default: async ({ request }) => {
		const data = await request.formData();
		const email = data.get('email');
		// process form...
		return { success: true };
	}
};
```

```svelte
<!-- +page.svelte -->
<script>
	/** @type {import('./$types').PageProps} */
	let { form } = $props();
</script>

{#if form?.success}
	<p>Success!</p>
{/if}

<form method="POST">
	<input name="email" type="email" />
	<button>Submit</button>
</form>
```

### Real-time Updates (Server-Sent Events)

**Server** (`+server.js`):
```js
export function GET() {
	const stream = new ReadableStream({
		start(controller) {
			const encoder = new TextEncoder();
			const send = (data) => {
				controller.enqueue(encoder.encode(`data: ${JSON.stringify(data)}\n\n`));
			};
			// Send updates...
			setInterval(() => send({ time: Date.now() }), 1000);
		}
	});

	return new Response(stream, {
		headers: {
			'Content-Type': 'text/event-stream',
			'Cache-Control': 'no-cache'
		}
	});
}
```

**Client**:
```svelte
<script>
	let data = $state({ time: 0 });

	$effect(() => {
		const source = new EventSource('/updates');
		source.onmessage = (e) => {
			data = JSON.parse(e.data);
		};
		return () => source.close();
	});
</script>
```

## Environment Variables

**Public** (exposed to client):
```js
import { PUBLIC_STATION_NAME } from '$env/static/public';
```

**Private** (server-only):
```js
import { DATABASE_URL } from '$env/static/private';
```

## Component Patterns

### Snippets and Render
Reusable markup patterns:

```svelte
<script>
	let items = $state(['a', 'b', 'c']);
</script>

{#snippet listItem(item)}
	<li>{item}</li>
{/snippet}

<ul>
	{#each items as item}
		{@render listItem(item)}
	{/each}
</ul>
```

### Conditional Rendering
```svelte
{#if condition}
	<p>True</p>
{:else if otherCondition}
	<p>Other</p>
{:else}
	<p>False</p>
{/if}
```

### Lists
```svelte
{#each items as item, index (item.id)}
	<div>{index}: {item.name}</div>
{/each}
```

**Always use keys** (the `(item.id)` part) for dynamic lists!

### Async/Await (Svelte 5.36+)
Requires `experimental.async: true` in config:

```svelte
<script>
	async function fetchData() {
		const res = await fetch('/api/data');
		return res.json();
	}
</script>

<p>{await fetchData()}</p>

<!-- Or with #await -->
{#await fetchData()}
	Loading...
{:then data}
	<p>{data.message}</p>
{:catch error}
	<p>Error: {error.message}</p>
{/await}
```

## Best Practices

1. **Use $derived, not $effect, for computed values**
2. **Don't mutate props** (use callbacks or $bindable)
3. **Use $effect.pre only when necessary** (before DOM updates)
4. **Always provide keys in {#each} blocks** for dynamic lists
5. **Prefer server load functions** for sensitive data
6. **Use goto() for navigation** when remote functions are enabled
7. **Type your components** with `PageProps`, `LayoutProps`, etc.

## When to Consult External Resources

This skill covers the most common Svelte 5 and SvelteKit patterns. For advanced topics, refer to:
- SvelteKit adapters and deployment
- Advanced routing (route groups, breaking layouts)
- Hooks (handle, handleFetch, handleError)
- Service workers and offline support
- Custom Svelte stores (when not using runes)
- Migration from Svelte 4
- Testing strategies
- TypeScript advanced types

Remember: Start with the fundamentals in this skill, then explore advanced topics as needed.
