---
name: svelte5-runes
description: Svelte 5 runes syntax and patterns. Use when writing Svelte components, managing state, or working with reactive values. Triggers on Svelte files, component creation, or mentions of $state, $derived, $effect, $props, or Svelte state management.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# Svelte 5 Runes Guide

This project uses **Svelte 5 with runes**. Never use the old store API (`writable`, `readable`, `derived` from 'svelte/store').

## Core Runes

### $props() - Component Props

```svelte
<script lang="ts">
  // Destructure with types and defaults
  let {
    title,
    count = 0,
    disabled = false,
    children,  // Snippet for slot content
    onclick
  }: {
    title: string;
    count?: number;
    disabled?: boolean;
    children?: Snippet;
    onclick?: () => void;
  } = $props();
</script>
```

### $state() - Reactive State

```svelte
<script lang="ts">
  // Primitive state
  let isOpen = $state(false);
  let count = $state(0);

  // Array state (deeply reactive)
  let items = $state<string[]>([]);

  // Object state
  let user = $state<User | null>(null);

  // Mutate directly - it's reactive!
  function addItem(item: string) {
    items.push(item);  // This triggers updates
  }
</script>
```

### $derived() - Computed Values

```svelte
<script lang="ts">
  let items = $state<string[]>([]);
  let filter = $state('');

  // Simple derived
  let count = $derived(items.length);

  // Complex derived
  let filteredItems = $derived(
    items.filter(item => item.includes(filter))
  );

  // Derived from multiple sources
  let summary = $derived(`${count} items, ${filteredItems.length} shown`);
</script>
```

### $effect() - Side Effects

```svelte
<script lang="ts">
  let query = $state('');

  // Runs when dependencies change
  $effect(() => {
    console.log('Query changed:', query);
    // Dependencies are auto-tracked
  });

  // With cleanup (like useEffect return)
  $effect(() => {
    const controller = new AbortController();
    fetchData(query, controller.signal);

    return () => controller.abort();
  });

  // Pre-effect (runs before DOM updates)
  $effect.pre(() => {
    // Scroll position preservation, etc.
  });
</script>
```

### $bindable() - Two-Way Binding Props

```svelte
<script lang="ts">
  // In child component
  let { value = $bindable() }: { value?: string } = $props();
</script>

<!-- In parent -->
<Input bind:value={searchQuery} />
```

## Event Handling (Svelte 5 Syntax)

```svelte
<!-- Use lowercase event handlers -->
<button onclick={handleClick}>Click</button>
<input oninput={(e) => query = e.currentTarget.value} />
<div onmouseenter={handleEnter} onmouseleave={handleLeave}>
  Hover me
</div>

<!-- NOT the old on:click syntax -->
```

## Snippets (Replace Slots)

```svelte
<!-- Define a snippet -->
{#snippet row(item)}
  <tr>
    <td>{item.name}</td>
    <td>{item.value}</td>
  </tr>
{/snippet}

<!-- Render it -->
{#each items as item}
  {@render row(item)}
{/each}

<!-- Pass as prop -->
<Table {row} {items} />
```

## Global State with Context

```typescript
// src/lib/state/player.svelte.ts
export function createPlayerState() {
  let currentTrack = $state<Track | null>(null);
  let isPlaying = $state(false);
  let volume = $state(0.8);

  return {
    get currentTrack() { return currentTrack; },
    get isPlaying() { return isPlaying; },
    get volume() { return volume; },

    play(track: Track) {
      currentTrack = track;
      isPlaying = true;
    },
    pause() {
      isPlaying = false;
    },
    setVolume(v: number) {
      volume = Math.max(0, Math.min(1, v));
    }
  };
}

// In +layout.svelte
import { setContext } from 'svelte';
const player = createPlayerState();
setContext('player', player);

// In any component
import { getContext } from 'svelte';
const player = getContext('player');
```

## Migration from Svelte 4

| Svelte 4 | Svelte 5 |
|----------|----------|
| `export let prop` | `let { prop } = $props()` |
| `let count = 0` (reactive) | `let count = $state(0)` |
| `$: doubled = count * 2` | `let doubled = $derived(count * 2)` |
| `$: console.log(count)` | `$effect(() => console.log(count))` |
| `on:click={handler}` | `onclick={handler}` |
| `<slot />` | `{@render children?.()}` |
| `<slot name="x" />` | `{@render x?.()}` |

## Common Patterns

### Debounced Search

```svelte
<script lang="ts">
  let query = $state('');
  let debouncedQuery = $state('');

  $effect(() => {
    const timeout = setTimeout(() => {
      debouncedQuery = query;
    }, 300);

    return () => clearTimeout(timeout);
  });

  let results = $derived.by(async () => {
    if (!debouncedQuery) return [];
    return await searchAPI(debouncedQuery);
  });
</script>
```

### Toggle with Derived

```svelte
<script lang="ts">
  let isOpen = $state(false);
  let buttonText = $derived(isOpen ? 'Close' : 'Open');
  let ariaExpanded = $derived(isOpen ? 'true' : 'false');

  function toggle() {
    isOpen = !isOpen;
  }
</script>
```
