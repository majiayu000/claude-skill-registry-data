---
name: ui-component-generation
description: Generate framework-specific UI components by prompting the agent's own LLM directly - no external generation service or MCP required
---

# UI Component Generation

Generate UI components by prompting the agent's own LLM directly. Zero code, zero MCP, zero external service. This skill replaces one common class of third-party MCPs that route component specs and design intent to a generation-as-service vendor - under the MCP Registry Policy (see `AGENTS.md`), capabilities achievable via the agent's LLM should ship as skills, not MCPs.

## When to Use This Skill

Use this skill when:

- The user asks for a new UI component with a defined contract (props, variants, states).
- The user asks for iteration on an existing component (add a variant, tighten types, add loading states).
- The user needs bulk generation of design-system primitives (Button, Card, Input, Badge variants).
- The user needs a one-off component for an experiment or prototype.
- The request includes framework specifics (React + TypeScript, Vue 3 + Composition API, Svelte 5 + runes, Astro islands, plain HTML + CSS).

**When NOT to use**:

- Multi-component layouts, routing, state management, or architecture questions -> use `frontend-ui-engineering`.
- Visual design exploration without a prop contract (the prompt is too ambiguous; ask the user to define the contract first).
- Server-rendered page templates with significant business logic -> use the framework-specialist skill (`react-expert`, `nextjs-expert`, `vue-expert`, `svelte-expert`, `astro-expert`).

## Instructions

### Step 1: Elicit or confirm the component contract

Before generating, the agent must have:

1. **Component name** (PascalCase, noun form; e.g. `PrimaryButton`, `UserCard`).
2. **Props and their types** (use TypeScript-flavored notation even for non-TS frameworks for clarity).
3. **Variants / states** (loading, disabled, error, size variants, theme variants).
4. **Framework + styling approach** (e.g. "React + TypeScript with Tailwind", "Svelte 5 with CSS modules", "Vue 3 with unstyled primitives").
5. **Accessibility baseline** (keyboard handling, ARIA attributes, focus management).

If any of these are missing, ask the user in a single batched question before generating.

### Step 2: Generate the component

Emit a single code block with the component, followed by a short prose block listing:

- The file path where the component should live.
- A one-line usage example.
- Any caveats about accessibility, theming, or state the user should know.

### Step 3: Accessibility baseline checklist

Before returning, verify:

- [ ] Interactive elements have accessible names (text content, `aria-label`, or `aria-labelledby`).
- [ ] Buttons use `<button>` (not clickable `<div>`). Links use `<a>` with a real `href`.
- [ ] Keyboard interaction works: Tab / Shift+Tab for focus, Enter / Space for activation, Escape for dismissal where relevant.
- [ ] Focus indicators are visible (no `outline: none` without a replacement).
- [ ] Color contrast meets WCAG AA (4.5:1 for normal text, 3:1 for large text and UI components).
- [ ] Form inputs have `<label>` associated via `for` / `id` or as a wrapping element.
- [ ] Dynamic content changes are announced (`aria-live="polite"` for non-urgent, `"assertive"` for errors).

### Step 4: Type safety baseline

For TypeScript frameworks:

- [ ] Component props use `interface` or `type` declarations with explicit types (no `any`).
- [ ] Union types for variant / state / size props use literal string unions, not loose strings.
- [ ] Event handlers use framework-appropriate types (`React.MouseEventHandler<HTMLButtonElement>` vs generic `() => void`).
- [ ] Default prop values are documented.

### Step 5: Framework conventions

Match the framework's idiomatic patterns:

- **React / Next.js**: function components, hooks for state, `className` prop, `forwardRef` for elements that receive refs, no class components.
- **Vue 3**: `<script setup lang="ts">`, Composition API, typed `defineProps` / `defineEmits`.
- **Svelte 5**: runes (`$state`, `$props`, `$derived`), `$bindable` for two-way binding, `$effect` sparingly.
- **Astro**: `.astro` files for static, client islands via `client:*` directives only where reactivity is needed.
- **Plain HTML + CSS**: semantic HTML, BEM or logical-properties CSS, no dependencies.

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We need the external service for good components" | The agent is the same class of LLM that powers most external component generators. The external service adds a network hop, a new data processor for your design intent, and usually a recurring cost. Direct prompting gives you equal or better output with zero data leak. |
| "The external service has pre-tuned prompts" | You can write a reusable prompt template in your own repo (a markdown file, a snippet, a /command in DevAI-Hub). The external service's advantage is a first-draft prompt; that prompt can be reverse-engineered once and reused forever. |
| "The external service gives us a UI library" | The external service gives you a generator, not a maintained UI library. Real UI libraries (shadcn/ui, Radix, Headless UI) are separate artifacts with versioned source code; adopt those as open-source deps without going through a generation service. |

## Verification

- [ ] The component matches the contract (every prop, variant, and state from Step 1 is implemented).
- [ ] Accessibility baseline checklist (Step 3) passes.
- [ ] Type safety baseline (Step 4) passes for TypeScript frameworks.
- [ ] The generated code compiles / parses in the target framework (run the framework's type-checker and linter).
- [ ] A one-paragraph usage example is included.
- [ ] No external service call was made; the generation was done entirely by the agent's own LLM.

## Related Skills

- `frontend-ui-engineering` - multi-component architecture, state management, accessibility at the page level.
- `react-expert` - React-specific idioms and patterns.
- `vue-expert` - Vue-specific patterns.
- `svelte-expert` - Svelte runes and SvelteKit.
- `astro-expert` - Astro islands and content collections.
- `nextjs-expert` - Next.js App Router and server components.
