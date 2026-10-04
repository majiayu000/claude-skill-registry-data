---
name: "Stack: Svelte"
description: "Svelte 5 and SvelteKit: runes reactivity, component composition, routing, data loading, form handling."
when_to_use: "When writing or reviewing Svelte 5 / SvelteKit code: runes ($state, $derived, $effect), routing and data loading. Auto-loads only when work touches .svelte or +page/+layout files."
user-invocable: false
metadata:
  family: clod-stack
paths:
  - "**/*.svelte"
  - "**/+page.*"
  - "**/+layout.*"
allowed-tools:
  - Read
  - Glob
  - Grep
---

# Svelte/SvelteKit Patterns

Comprehensive guide to Svelte 5 and SvelteKit development patterns. Emphasises runes-based reactivity ($state, $derived, $effect, $props), component composition, SvelteKit routing, data loading, form handling and performance optimisation.

## When This Skill Applies

Use this skill when:
- Building Svelte components
- Managing reactive state with runes
- Implementing SvelteKit routes and pages
- Creating load functions or form actions
- Handling component composition
- Optimising Svelte/SvelteKit performance
- Questions about Svelte 5 patterns or SvelteKit conventions

## Svelte 5 Fundamentals

### Runes Overview

**Runes** are compiler instructions (marked with `$`) that enable explicit reactivity:
- `$state` - Reactive state
- `$derived` - Computed values
- `$effect` - Side effects
- `$props` - Component props
- `$bindable` - Two-way bindable props

**Key principle**: Reactivity is explicit, not implicit. Works in `.js`, `.ts`, and `.svelte` files.

## Reactive State with $state

### Basic State
```svelte
<script>
	let count = $state(0);
	
	function increment() {
		count++; // Just a number, no wrapper needed
	}
</script>

<button onclick={increment}>
	Clicks: {count}
</button>
```

**Key points**:
- `$state` creates reactive state
- State is the value itself (not `.value` or `getCount()`)
- Updates trigger UI re-renders

### Deep Reactivity
```svelte
<script>
	let todos = $state([
		{ id: 1, text: 'Learn Svelte 5', done: false }
	]);
	
	function toggle(id) {
		const todo = todos.find(t => t.id === id);
		todo.done = !todo.done; // Deep reactivity works
	}
	
	function addTodo(text) {
		todos.push({ id: Date.now(), text, done: false });
		// Array methods trigger reactivity
	}
</script>
```

**Deep reactivity**:
- Objects and arrays are automatically proxied
- Nested mutations trigger updates
- Array methods (`.push`, `.splice`, etc.) work reactively

### State in .svelte.js Files
```javascript
// counter.svelte.js
export function createCounter(initial = 0) {
	let count = $state(initial);
	
	return {
		get count() { return count; },
		increment: () => count++,
		reset: () => count = initial
	};
}
```
```svelte
<!-- App.svelte -->
<script>
	import { createCounter } from './counter.svelte.js';
	
	const counter = createCounter(5);
</script>

<button onclick={counter.increment}>
	Count: {counter.count}
</button>
```

**Benefits**:
- Share state logic across components
- Testable outside Svelte components
- No store boilerplate needed

## Derived State with $derived

### Basic Derivations
```svelte
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);
	let isEven = $derived(count % 2 === 0);
</script>

<p>{count} doubled is {doubled}</p>
<p>Count is {isEven ? 'even' : 'odd'}</p>
```

**Key points**:
- Automatically recalculates when dependencies change
- Memoised (only recalculates when needed)
- Must be free of side-effects

### Complex Derivations with $derived.by
```svelte
<script>
	let numbers = $state([1, 2, 3, 4, 5]);
	
	let stats = $derived.by(() => {
		const total = numbers.reduce((a, b) => a + b, 0);
		const average = total / numbers.length;
		return { total, average };
	});
</script>

<p>Total: {stats.total}, Average: {stats.average}</p>
```

**Use $derived.by when**:
- Logic doesn't fit in short expression
- Need multiple statements
- Complex calculations required

### $derived vs $effect

**$derived** - Computing values (pure, returns value):
```svelte
<script>
	let count = $state(0);
	let doubled = $derived(count * 2); // ✓ Good
</script>
```

**$effect** - Side effects (impure, no return value):
```svelte
<script>
	let count = $state(0);
	
	$effect(() => {
		console.log('Count changed:', count); // ✓ Good
	});
</script>
```

## Side Effects with $effect

### Basic Effects
```svelte
<script>
	let count = $state(0);
	
	$effect(() => {
		// Runs on mount and whenever count changes
		document.title = `Count: ${count}`;
	});
</script>
```

**When $effect runs**:
- Initially when component mounts
- Whenever dependencies change
- After DOM updates (unlike Svelte 4's `$:`)

### Effect Cleanup
```svelte
<script>
	let intervalId = $state(null);
	let elapsed = $state(0);
	
	$effect(() => {
		const id = setInterval(() => {
			elapsed++;
		}, 1000);
		
		// Cleanup runs when effect re-runs or component unmounts
		return () => clearInterval(id);
	});
</script>
```

### $effect.pre (Before DOM Update)
```svelte
<script>
	let messages = $state([]);
	let div;
	
	$effect.pre(() => {
		const isAtBottom = 
			div.scrollHeight - div.scrollTop === div.clientHeight;
		
		if (isAtBottom) {
			// After DOM updates, scroll to bottom
			$effect(() => {
				div.scrollTop = div.scrollHeight;
			});
		}
	});
</script>
```

### Common $effect Patterns

**Local storage sync**:
```svelte
<script>
	let preferences = $state(JSON.parse(
		localStorage.getItem('prefs') || '{}'
	));
	
	$effect(() => {
		localStorage.setItem('prefs', JSON.stringify(preferences));
	});
</script>
```

**API calls**:
```svelte
<script>
	let userId = $state('123');
	let user = $state(null);
	
	$effect(() => {
		fetch(`/api/users/${userId}`)
			.then(r => r.json())
			.then(data => user = data);
	});
</script>
```

**Avoid $effect for**:
- Derived values (use `$derived`)
- DOM manipulation Svelte handles (bindings, directives)
- Setting document.title (use `<svelte:head>`)

## Component Props with $props

### Basic Props
```svelte
<!-- Button.svelte -->
<script>
	let { label, variant = 'primary' } = $props();
</script>

<button class="btn btn--{variant}">
	{label}
</button>
```

**Usage**:
```svelte
<Button label="Click me" variant="secondary" />
```

### Props with TypeScript
```svelte
<script lang="ts">
	interface Props {
		label: string;
		variant?: 'primary' | 'secondary' | 'danger';
		onclick?: () => void;
	}
	
	let { label, variant = 'primary', onclick }: Props = $props();
</script>

<button class="btn btn--{variant}" {onclick}>
	{label}
</button>
```

### Rest Props
```svelte
<script>
	let { label, ...rest } = $props();
</script>

<button {...rest}>
	{label}
</button>
```

### Bindable Props with $bindable
```svelte
<!-- Input.svelte -->
<script>
	let { value = $bindable('') } = $props();
</script>

<input bind:value />
```

**Usage**:
```svelte
<script>
	let text = $state('');
</script>

<Input bind:value={text} />
<p>You typed: {text}</p>
```

## Additional resources

Deep-dive detail lives in supporting files, loaded only when needed:

- [component-patterns.md](component-patterns.md): slot patterns (basic, named, slot props) and composition (compound components, higher-order components)
- [sveltekit-routing-and-data.md](sveltekit-routing-and-data.md): file-based routing, dynamic/optional route params, load functions (client and server), streaming, form actions
- [performance-and-common-patterns.md](performance-and-common-patterns.md): lazy loading, list virtualisation, memoisation, keyed each blocks, form validation, modal management, debounced input

## Anti-Patterns

### Don't: Use $effect for Derived Values
```svelte
<!-- ✗ Bad -->
<script>
	let count = $state(0);
	let doubled = $state(0);
	
	$effect(() => {
		doubled = count * 2; // Wrong! Use $derived
	});
</script>

<!-- ✓ Good -->
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);
</script>
```

### Don't: Mutate Props Directly
```svelte
<!-- ✗ Bad -->
<script>
	let { user } = $props();
	
	function updateName() {
		user.name = 'New Name'; // Wrong! Props are read-only
	}
</script>

<!-- ✓ Good -->
<script>
	let { user, onUpdate } = $props();
	
	function updateName() {
		onUpdate({ ...user, name: 'New Name' });
	}
</script>
```

### Don't: Create Unnecessary $state
```svelte
<!-- ✗ Bad -->
<script>
	let count = $state(0);
	let doubled = $state(0);
	let isEven = $state(false);
	
	function increment() {
		count++;
		doubled = count * 2;     // Derived!
		isEven = count % 2 === 0; // Derived!
	}
</script>

<!-- ✓ Good -->
<script>
	let count = $state(0);
	let doubled = $derived(count * 2);
	let isEven = $derived(count % 2 === 0);
</script>
```

## Success Criteria

Svelte/SvelteKit code is well-structured when:
- Runes used appropriately ($state for state, $derived for computed, $effect for side effects)
- Components are composable and reusable
- Load functions fetch data efficiently
- Forms use progressive enhancement
- Performance optimised (lazy loading, memoisation)
- TypeScript types are accurate
- Code is maintainable and follows Svelte 5 conventions
