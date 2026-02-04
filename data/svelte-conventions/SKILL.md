---
name: svelte-conventions
description: This skill describes common patterns and my prefered style to use when editing svelte code. This could be in .svelte files or .svelte.ts files.
---

# Conventions When Editing Svelte Code

**All code must use Svelte 5.** 

## Svelte MCP Server

**ALWAYS use the Svelte MCP server tools when working with Svelte code:**

1. Call `list-sections` first to understand available documentation
2. Use `get-documentation` to fetch relevant Svelte 5 docs for your task
3. Call `svelte-autofixer` to validate and fix components before sending code to the user

If you don't have access to the MCP server, tell the user that they should enable it.

## State

- Use svelte 5 runes for all state management (e.g. `$state` and `$derived`).
- Any complex state should be wrapped in a class with methods used to manipulate. For example:
```ts
class ProductPricing {
    #pax: number = $state(0);
    #single_rooms: number = $state(0);
    #room_price: number;
    #single_supplement: number;

    readonly price: number;

    constructor(room_price: number, single_supplement: number) {
        this.#room_price = room_price;
        this.#single_supplement = single_supplement;
    
        this.price = $derived(this.room_price * this.pax + this.single_supplement * this.single_rooms);
    }

    get single_rooms() {
        return this.pax;
    }

    set single_rooms(new_rooms: number) {
        // Don't allow more rooms than people
        this.#single_rooms = Math.max(Math.min(new_rooms, this.#pax), 0);
    }
}
```

## Components

### Typing Props
- Prefer `interface Props` over `type Props` when typing component props.
- The correct way to use the props types is: `const { ...props }: Props = $props()`, destructuring the values you need.
- Example:
```ts
interface Props {
    value: number;
    onchange?: (new_value: number) => void;
}

const { value, onchange }: Props = $props();
````
## Styling

- Use modern, conventional CSS. Never use tailwind.
- Make use of CSS nesting.
- Divs used to layout their contents have the class `.layout` by convention.
