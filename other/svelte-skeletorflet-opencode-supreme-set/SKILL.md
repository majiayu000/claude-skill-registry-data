---
name: svelte
description: Svelte 5 runes ($state, $derived, $effect, $props), component props, event handling, logic blocks, stores, snippets, transitions, actions, and reactivity. Use when building Svelte components.
---

## svelte

Svelte shifts reactivity from runtime to compile time.

### Core Concepts
- Svelte 5 runes: $state for reactive state, $derived for computed values
- $effect for side effects that auto-track dependencies
- $props for component inputs with type safety

### Common Patterns
- Logic blocks: {#if}, {#each}, {#await} for declarative control flow
- Stores: writable, derived, readable for cross-component state
- Snippets (Svelte 5) replace slots for content projection

### Best Practices
- Prefer runes over stores for local component state
- Use $derived instead of $effect for computations
- Apply transitions sparingly for deliberate UX polish

### Common Code Patterns
- on:click, on:submit for native DOM event handling
- use:action for DOM element behavior encapsulation
- Transition directives: transition:fade, transition:fly for animations
