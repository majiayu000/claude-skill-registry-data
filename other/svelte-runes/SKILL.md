---
name: svelte-runes
description: "Svelte 5 runes architecture ($state, $derived, $effect), snippet templates, and universal reactivity."
---

# Svelte 5 Runes Protocol

Master Svelte 5 reactivity and component composition.

---

## 1. Runes Primitives

1. State declarations: `let count = $state(0);`.
2. Derived values: `let double = $derived(count * 2);`.
3. Side effects: Use `$effect` strictly for external synchronization.

---

## 2. Snippets Over Slots

Use `{#snippet name(param)}` for flexible, scoped template rendering rather than legacy slots.
