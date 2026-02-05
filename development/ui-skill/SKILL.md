---
name: ui-skill
description: UI implementation best practices and conventions for building user interfaces. Use this skill when implementing UI.
---

### Technologies
- Use the following tech to implement the UI:
    - React 18+
    - Next.js 16+
    - Tailwind CSS
    - Shadcn UI
    - Framer Motion
    - Lucide Icons

## Workflow

1. Planing
- Thoroughly understand the requirements
- Investigate the codebase for existing components and patterns that can be reused
- Locate where to implement the new UI following the project [Page, Layout and Component Structure](./PAGE_LAYOUT_COMPONENT_STRUCTURE.md)
- Identify shadcn components and/or blocks that can be used directly or as bases for new components following the [Shadcn UI Components exploration and selection workflow](#shadcn-ui-components-exploration-and-selection-workflow)
- Suggest user with at least 2 design options refereing the design best practices.

2. Implement the pieces
- Install any shadcn components that has been selected in the planning phase following the [Shadcn UI Components installation and usage workflow](#shadcn-ui-components-installation-and-usage-workflow)
- Create new components if needed.

4. Building the UI
- Implement the final UI by composing the selected shadcn components and/or newly created components.


## Server and Client Components

### Default Behavior
- All components in `app/` are React Server Components by default
- Server Components render on the server and can be cached
- Client Components execute in the browser and enable interactivity

### When to Use Client Components
Use the `"use client"` directive at the top of a file when you need:
- State management (`useState`, `useReducer`)
- Event handlers (`onClick`, `onChange`, etc.)
- Lifecycle hooks (`useEffect`, `useLayoutEffect`)
- Browser-only APIs (`window`, `localStorage`, geolocation)
- Custom React hooks that depend on state/effects

### When to Use Server Components (default)
Keep components as Server Components when:
- Fetching data from databases or APIs
- Accessing backend resources directly
- Keeping sensitive information secure (API keys, tokens)
- Reducing JavaScript bundle size

### Best Practices
- **Minimize Client Components** - Only mark components that need interactivity as Client Components
- **Push "use client" Deep** - Add the directive to the lowest component that needs it, not parent containers
- **Composition Pattern** - Pass Server Components as `children` props to Client Components to keep server-rendered content
- **Data Passing** - Server Components can pass serializable data as props to Client Components
- **Context Providers** - Wrap providers in Client Components and import into Server Components
- **Third-Party Libraries** - If a library requires browser APIs, wrap it in your own Client Component

### Security
- Only environment variables prefixed with `NEXT_PUBLIC_` are exposed to the browser
- Use the `server-only` package to prevent accidental server code imports in Client Components


## Shadcn UI Components exploration and selection workflow

Notes: The registry name is ALWAYS @shadcn when using shadcn tools.

1. Use the mcp__shadcn__list_items_in_registries tool to list components in the @shadcn registry
2. Use the mcp__shadcn__search_items_in_registries to fuzzy search for components in the @shadcn registry using keywords

### Shadcn UI Components installation and usage workflow

3. Check if the component has already been installed by running `ls components/ui/' in the project root/
4. For components that is not installed install them using `pnpm dlx shadcn@latest add [component]` e.g. pnpm dlx shadcn@latest add button card
5. Before using the component read docuemntion:
      - Use the mcp__shadcn__get_item_examples_from_registries tool to get usage examples for the component from the @shadcn registry
      - Check the component source code in the `components/ui/[component]` folder


## Page, Layout and Component Structure

### Layout
- Layouts are used for shared UI, logic and data fetching that is common across multiple pages.
- Try to make the layout as static as possible, avoid adding dynamic content or data fetching in the layout.
- Make the higher order layout be shared across the most pages possible.
- Create new nested layouts when needed to avoid making the higher order layout dynamic.


### Page
- Pages are used for specific routes and can contain dynamic content and data fetching.


### Components
- Components are used for reusable UI pieces that can be shared across pages and layouts.
- ONLY create components for UI pieces that are reused in at least 2 places or you expect to reuse them in the future.
- For pieces of code that will not be reused, create them directly in the page or layout file.
- **Keep Server Components by default** - Only add `"use client"` to components that need interactivity
- **Push interactivity deep** - Add the `"use client"` directive to the lowest component that needs it (e.g., a button), not the parent container
- **Example**: A card with a clickable button → Card is Server Component, Button is Client Component


### Styling
- Use Tailwind CSS utility classes for styling.
- ALWAYS reach for shadcn token variables when styling e.g. bg-primary, text-secondary, etc. first before using raw Tailwind CSS classes.
- If variation of the shadcn token variables is needed use bg-primary/50, text-secondary/80, etc. to adjust opacity.

#### Shadcn varialbes


### **Global**

| Token        | Meaning      | Use                              |
| ------------ | ------------ | -------------------------------- |
| `background` | Base canvas  | Page background, global surfaces |
| `foreground` | Primary text | Main body text, default icons    |

### **Surfaces / Elevation**

| Token                | Meaning              | Use                                     |
| -------------------- | -------------------- | --------------------------------------- |
| `card`               | Elevated container   | Cards, panels, modular content sections |
| `card-foreground`    | Text inside card     | Headlines & body inside cards           |
| `popover`            | Floating surface     | Menus, dropdowns, tooltips              |
| `popover-foreground` | Text inside popovers | Menu text, tooltip text                 |

### **Tone / Quiet Content**

| Token              | Meaning        | Use                                           |
| ------------------ | -------------- | --------------------------------------------- |
| `muted`            | Subtle surface | Low-attention UI, placeholders, subtle blocks |
| `muted-foreground` | Subtle text    | Metadata, timestamps, helper labels           |

### **Actions / Brand Hierarchy**

| Token                  | Meaning                     | Use                                                |
| ---------------------- | --------------------------- | -------------------------------------------------- |
| `primary`              | Main brand / primary action | Primary buttons, strongest calls-to-action         |
| `primary-foreground`   | Text on primary             | Button text/icons on primary                       |
| `secondary`            | Supporting action           | Secondary buttons, low-priority actions            |
| `secondary-foreground` | Text on secondary           | Text/icons on secondary surfaces                   |
| `accent`               | Highlight / selection       | Hover states, selected list items, subtle emphasis |
| `accent-foreground`    | Text on accent              | Text inside accent states                          |

### **Danger / Errors**

| Token                    | Meaning             | Use                                 |
| ------------------------ | ------------------- | ----------------------------------- |
| `destructive`            | Critical danger     | Delete actions, destructive buttons |
| `destructive-foreground` | Text on destructive | Text/icons on danger surfaces       |

### **Structure / Inputs**

| Token    | Meaning          | Use                                          |
| -------- | ---------------- | -------------------------------------------- |
| `border` | Structural lines | Dividers, container edges, card borders      |
| `input`  | Form affordance  | Input borders/backgrounds                    |
| `ring`   | Focus halo       | Keyboard focus states, accessibility outline |

### **Navigation / Sidebar**

| Token                        | Meaning                      | Use                       |
| ---------------------------- | ---------------------------- | ------------------------- |
| `sidebar`                    | App nav surface              | Left nav panel background |
| `sidebar-foreground`         | Nav text                     | Sidebar labels & icons    |
| `sidebar-primary`            | Nav primary action/highlight | Active item, nav CTA      |
| `sidebar-primary-foreground` | Text on sidebar primary      | Text/icons in active nav  |
| `sidebar-accent`             | Hover/selection in nav       | Hover, sub-selection      |
| `sidebar-accent-foreground`  | Text on nav accent           | Text/icons                |
| `sidebar-border`             | Nav separators               | Sidebar boundaries        |
| `sidebar-ring`               | Nav focus                    | Focus in navigation area  |

### **Data**

| Token        | Meaning                 | Use                               |
| ------------ | ----------------------- | --------------------------------- |
| `chart-1..5` | Categorical data colors | Data visualizations only (not UI) |

### **Shape**

| Token    | Meaning        | Use                                  |
| -------- | -------------- | ------------------------------------ |
| `radius` | Base curvature | Global rounding scale for components |





