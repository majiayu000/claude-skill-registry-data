---
name: reactive-md
description: Literate UI/UX for product teams - accelerate from idea to working prototype in minutes using markdown with embedded interactive React components. Use for fast iteration and async collaboration on product specs, wireframes, user flows, feature demos, and design documentation. Replaces Figma/Storybook with executable specs in version control.
license: MIT
metadata:
  version: "1.0.0"
  author: million-views (https://m5nv.com)
---

# Reactive MD

Generate functional markdown documents with embedded interactive React components for product design collaboration.

## Reference Documentation

**[GUIDE.md](references/GUIDE.md)** - Complete technical reference, troubleshooting, patterns, and dos/donts
**[use-cases.md](references/use-cases.md)** - Example implementations for each primary use case

(Consult these resources throughout for detailed guidance, pattern examples, and reference implementations.)

## When to Use This Skill

Use reactive-md when the user asks to create:

**Primary Use Cases:**
- Product specs with working prototypes
- User flow wireframes and interactive demos
- Feature prototypes, concept exploration, and visual demos
- A/B tests, dashboards, component galleries
- Interactive documentation and living specifications

**Aliases**: "live doc", "prototype", "POC", "interactive spec" all refer to reactive-md documents.

## Core Capabilities

Reactive-md documents support:

**Two Preview Modes:**
1. **Static Preview** (Markdown Preview): Offline, bundled packages only, server-side rendering
2. **Interactive Preview** (`Cmd+K P`): Browser-based webview, supports CDN packages and platform APIs

**Live Fences (CRITICAL):**

**When to use `live` annotation:**
- User wants to **see/interact** with the component
- Creating a working demo or prototype
- Showing how something works in practice
- All primary use cases (prototypes, concept exploration, specs, wireframes, demos)

**When to use regular fences (no `live`):**
- Explaining **how** something works (discourse about the code)
- Showing anti-patterns or broken examples
- Comparing different approaches side-by-side
- Code snippets that are incomplete or won't run standalone

**Syntax:**
- `` ```jsx live `` - JavaScript + JSX components (executable)
- `` ```tsx live `` - TypeScript + JSX components (executable)
- `` ```css live `` - CSS stylesheets (executable)
- `` ```jsx `` - Code examples for discussion (non-executable)
- `` ```tsx `` - Code snippets for illustration (non-executable)
- `` ```css `` - CSS snippets for illustration (non-executable)

**For Anti-Patterns and Discourse:**
When showing anti-patterns or broken examples in documentation, wrap the code fence in markdown backticks to prevent execution:

````markdown
<!-- ❌ Wrong: Top-level JSX with imports doesn't work -->
```jsx live
import Card from './Card.jsx';
<Card />
```
````

This clearly signals the wrapped code fence is for **illustration only** (showing what NOT to do), not for execution.

**The correct pattern** always wraps imports + JSX in a component function:
```jsx live
import Card from './Card.jsx';
export default function Demo() {
  return <Card />;
}
```

**Default behavior:** When in doubt, use `live` - reactive-md's purpose is interactive demos.

**File Types:**
- **Markdown (`.md`)** - Primary document only (entry point for preview)
- **JSX/TSX (`.jsx`, `.tsx`)** - Primary viewable OR dependent (can be imported)
- **CSS (`.css`)** - Dependent only (imported by JSX or via `css live` blocks)
- **JSON (`.json`)** - Dependent only (imported by JSX/TSX)

**Hot Module Reload:** Edit any file → preview updates automatically

**Import Patterns (Where and How):**
- **In `.jsx`/`.tsx` files or `jsx live` blocks:** Use `import './style.css'` or `import data from './data.json' with { type: 'json' }`
- **In `.css` files or `css live` blocks:** Use `@import './other.css'`

## Package & Data Loading

**Bundled Packages (Both Preview Modes):**
Always available in both Markdown Preview AND Interactive Preview:
- `dayjs`, `motion/react`, `lucide-react`, `clsx`, `uuid`, `es-toolkit`

**CDN Packages (Interactive Preview Only):**
Require `Cmd+K P` to load from esm.sh:
- `@heroicons/react`, `zustand`, `jotai`, `tailwind-merge`, `react-hook-form`

**Data Loading & Platform APIs:**
- ✅ Local JSON imports: `import data from './data.json' with { type: 'json' }` (both modes)
- ✅ Remote APIs: `fetch()` in `useEffect` (Static Preview shows initial state; Interactive Preview fetches)
- ✅ Platform APIs: `localStorage`, `sessionStorage` (Interactive Preview only)
- ❌ Local file fetch: Blocked by webview security (use `import` instead)

**Pattern for Remote Data:** Always fetch inside `useEffect`, initialize state with default values. Component renders safely in Static Preview while showing loading UI, then fetches in Interactive Preview.

```jsx live
// This pattern works in both preview modes
const [data, setData] = React.useState(null);
const [loading, setLoading] = React.useState(true);

React.useEffect(() => {
  fetch('https://api.example.com/data')
    .then(res => res.json())
    .then(data => { setData(data); setLoading(false); });
}, []);

// Renders: "Loading..." in Static, actual data in Interactive
return <div>{loading ? 'Loading...' : <pre>{JSON.stringify(data)}</pre>}</div>;
```

For React import rules, package details, and data loading patterns, consult the GUIDE in the references above.

## Styling Approach

Choose ANY styling approach that fits the task:
- **Tailwind CSS** - Fast, utility-first (use for quick prototypes)
- **Inline styles** - Simple, self-contained (use for minimal examples)
- **Plain CSS** - `css live` blocks or external `.css` files (use for semantic, maintainable styles)
- **Design system tokens** - When available, compose with design systems for consistent theming

Focus on document structure and interactive patterns. Styling is secondary to demonstrating reactive-md capabilities.

## File Organization

### Single File (Inline Code)

**When:** Simple concepts (< 50 lines total)

✅ **With helper components** - Wrap in parent function
✅ **Without helpers** - Pure JSX at top level
❌ **Don't mix** helper functions with top-level JSX (ambiguous entry point)

### Multi-File Structure

**When:** Complex features (> 50 lines) or reusable components

**The agent will create these files for you** using the `write_file` tool. Each file is self-contained:

**Example structure:**
```
feature-name/
  README.md            (primary document with live fences)
  Component.jsx        (imported component)
  styles.css           (imported styles)
  data.json            (imported data)
```

**Import pattern in your primary/main .md file (typically README.md or spec.md):**
```jsx live
import Component from './Component.jsx';
import './styles.css';
import data from './data.json' with { type: 'json' };

export default function Demo() {
  return <Component />;
}
```

**Critical:** Always wrap imports + JSX in a component function. Top-level JSX mixed with imports will fail.

**Naming:** Kebab-case, hierarchical context (e.g., `checkout-flow-payment-form.jsx`)

**Agent workflow:**
1. Agent analyzes the task and identifies files needed (components, styles, data)
2. Agent creates primary document (README.md or spec.md typically) with live fence showing imports
3. Agent uses `write_file` tool to create supporting files (Component.jsx, styles.css, data.json)
4. You get complete, working multi-file structure ready to use

**For working examples:** Study the recipes below

## Examples

**Read example files in [references/recipes/](references/recipes/) to see how to write functional live docs:**

- **[references/recipes/feature-spec/](references/recipes/feature-spec/)** - Product specification with working components and edge case handling
- **[references/recipes/a-b-test-proposal/](references/recipes/a-b-test-proposal/)** - A/B test methodology with business metrics and comparison widget
- **[references/recipes/competitive-analysis/](references/recipes/competitive-analysis/)** - Market positioning with competitor scoring and feature matrix
- **[references/recipes/user-flow/](references/recipes/user-flow/)** - Multi-step flows with validation, error handling, and success states
- **[references/recipes/dark-mode-toggle/](references/recipes/dark-mode-toggle/)** - Multi-file imports, external `.jsx` and `.css` files
- **[references/recipes/notification-system/](references/recipes/notification-system/)** - Multi-component architecture, folder organization
- **[references/recipes/data-loading/](references/recipes/data-loading/)** - JSON imports and API fetch patterns

## Clarifying Questions

When context is ambiguous, ASK instead of guessing:

- **Scope**: "Make a dashboard" → Ask purpose (analytics? admin? monitoring?) and data source
- **File context**: User says "improve this" → Check which file is open or selected
- **Data**: User wants working demo → Ask if they want mock data or real API

## Refusal Boundaries

Reactive-md is a powerful prototyping tool. Refuse only when requests require infrastructure or services outside the extension's scope.

### What Reactive-MD CAN Do

Complex interactive UIs, real API integration, error handling, authentication UI, data persistence (localStorage), form validation, complex state management.

### Refuse: Infrastructure & Backend

**Triggers:** Deploy, CI/CD, Docker, cloud platforms, backend implementation, databases, auth services, test frameworks.

**Response template:**
```
🚫 [Infrastructure/Backend/Testing] Boundary

Reactive-md prototypes run in VS Code, not production infrastructure.

This prototype CAN demonstrate: [UI/UX flow, API integration, interactive behavior]

To productionize: Graduate to proper project with infrastructure tooling.
```

### Refuse: Known-Broken Packages (esm.sh Limitations)

The following packages cannot be loaded via esm.sh due to dependency resolution issues. Refuse these requests in Interactive Preview:

**`recharts`** - Charting library
- **Issue:** Missing transitive dependency (`clsx` not resolved by esm.sh)
- **Refuse:** "recharts doesn't load in Interactive Preview. For charts, use native SVG or plan a full project setup."

**`swr`** - Data fetching/caching
- **Issue:** Missing React context shim (`use-sync-external-store`)
- **Refuse:** "swr isn't available in Interactive Preview. For data fetching, use `fetch()` directly or `zustand` for local state."

**`@tanstack/react-query`** - Complex data/state management
- **Issue:** Multiple React instance conflicts with esm.sh import isolation
- **Refuse:** "@tanstack/react-query requires a full project setup. Use `zustand` or `jotai` for state management in prototypes."

### Refuse: Real-Time & Server Infrastructure

The following require server infrastructure beyond a VS Code extension:

**WebSockets** - Real-time bidirectional communication
- **Issue:** Requires persistent backend server connection
- **Refuse:** "WebSockets need a backend server. For prototypes, use `fetch()` polling or plan a full project setup."

**Service Workers** - Background processing & offline support
- **Issue:** Requires application-level service worker infrastructure
- **Refuse:** "Service Workers need full project setup. For prototypes, use `localStorage` for persistence."

## Quality Standards

Good output must:

1. ✅ **Run without errors** - Code executes in preview
2. ✅ **Follow conventions** - File organization, naming, live fence syntax
3. ✅ **Respect boundaries** - Refuse infrastructure/backend only
4. ✅ **Complete structure** - Context → Problem → Solution → Code → Next Steps
5. ✅ **Use imports** - External files for reusable components/styles (not massive inline fences)

## Success Criteria

**Primary success**: User goes from idea to working prototype in < 10 minutes.

**Key outcomes**:
1. Iterate fast (minutes, not days)
2. Communicate visually (executable specs vs static mocks)
3. Collaborate async (version-controlled `.md` files)
4. Make decisions faster (working prototypes resolve debates)
5. Ship confident specs (living documentation shows exact behavior)

**Goal:** Make reactive-md the fastest path from product idea to shared understanding.
