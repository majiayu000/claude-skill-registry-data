---
name: reactive-md
description: Create functional markdown documents with embedded interactive components for product team collaboration using the reactive-md VS Code extension. Use when generating product specs, design prototypes, feature wireframes, user flows, or interactive documentation. Specializes in teaching the 'live fence' methodology (css|jsx|tsx live) to replace Figma/Storybook workflows. NOT for production code—only for idea communication and rapid prototyping.
license: MIT
---

# Reactive MD

Generate functional markdown documents with embedded interactive React components for product collaboration.

## When to Use This Skill

Use reactive-md when the user asks to create:

**Primary Use Cases:**
- Product specs with working prototypes
- Design system documentation with live examples  
- User flow wireframes with interactive demos
- Feature prototypes with visual concepts
- A/B test mockups with interactivity
- Wireframes, dashboards, or component galleries
- Interactive documentation or living specifications

**Recognized Keywords & Aliases:**

This skill responds to requests using any of these terms:
- **"reactive-md"** / **"reactive md"** (canonical name)
- **"live doc"** / **"living doc"** / **"live document"** (documentation style)
- **"prototype"** / **"proof-of-concept"** / **"POC"** (prototyping)
- **"interactive spec"** / **"interactive prototype"** (specification style)

All these terms refer to creating primary document types (`.md` or `.jsx/.tsx`) with embedded interactive components.

**Do NOT use** for production code, testing, deployment, or backend integration.

---

## Core Capabilities

Reactive-md documents support:

**Two Preview Modes:**
1. **Static Preview** (Markdown Preview): Offline, bundled packages only, server-side rendering
2. **Interactive Preview** (`Cmd+K P`): Browser-based webview, supports CDN packages and platform APIs

**Live Fences:**
- `` ```jsx live `` - JavaScript + JSX components
- `` ```tsx live `` - TypeScript + JSX components  
- `` ```css live `` - CSS stylesheets (custom properties, imports)

**File Types:**
- Markdown (`.md`) - Primary document only (entry point)
- JSX/TSX with exports - Can be primary OR imported
- CSS (`.css`) - Dependent only (imported by other files)
- JSON (`.json`) - Data files (imported or used inline)

**Hot Module Reload:** Edit `.jsx`, `.tsx`, `.css`, `.json` → preview updates automatically

---

## Package Constraints

### Bundled Packages (Always Available, Offline)

Use these in both preview modes:
- `dayjs` - Date manipulation (includes relativeTime, duration, utc, timezone plugins)
- `motion/react` - Animations (framer-motion)
- `lucide-react` - Icon library
- `clsx` - Class name utilities
- `es-toolkit` - Lodash alternative
- `uuid` - Unique identifiers

### CDN Packages (Interactive Preview Only, Online)

Require internet connection, only work in Interactive Preview:
- `@heroicons/react` - Heroicons
- `zustand` - State management
- `jotai` - Atomic state
- `tailwind-merge` - Tailwind utilities
- `react-hook-form` - Form handling

**Pro tip:** When you try unsupported packages, clear error messages show available alternatives, helping teams prototype within the tool's capabilities.

### Known Broken (Refuse These)

Do NOT suggest:
- ❌ `recharts` - Missing dependencies
- ❌ `swr` - Missing shims
- ❌ `@tanstack/react-query` - React instance conflicts

**Alternative:** Use native SVG or Canvas for data visualization instead of charting libraries.

---

## Data Loading Patterns

### ✅ Static JSON Imports (Local Files)

**USE THIS for local data files:**

```jsx live
import products from './data/products.json' with { type: 'json' };

function ProductList() {
  return <div>{products.map(p => <div key={p.id}>{p.name}</div>)}</div>;
}
```

✅ Works in both Static and Interactive preview
✅ Data loaded at build time
✅ No security restrictions

### ✅ Remote Fetch (External APIs)

**USE THIS for remote data:**

```jsx live
function Posts() {
  const [posts, setPosts] = React.useState([]);
  
  React.useEffect(() => {
    fetch('https://jsonplaceholder.typicode.com/posts?_limit=5')
      .then(r => r.json())
      .then(setPosts);
  }, []);
  
  return <div>{posts.map(p => <div key={p.id}>{p.title}</div>)}</div>;
}
```

✅ Works in Interactive Preview only
✅ Requires internet connection
✅ Use mock APIs: jsonplaceholder.typicode.com, reqres.in

### ❌ Runtime Fetch to Local Files (BLOCKED)

**DO NOT use fetch() for local files:**

```jsx
// ❌ THIS WILL FAIL - VS Code webview security blocks local fetch()
function BrokenExample() {
  React.useEffect(() => {
    fetch('./data/products.json')  // ❌ SECURITY BLOCKED
      .then(r => r.json())
      .then(setData);
  }, []);
}
```

**Why it fails:** VS Code webview security policy blocks runtime fetch() to local files

**Solution:** Use static import instead:
```jsx
import products from './data/products.json' with { type: 'json' };  // ✅ WORKS
```

---

## Error Handling & Guidance

Reactive MD provides contextual help when code uses unsupported features:

### Error Intercept Placeholders (EIP)
When code hits limitations, you'll see helpful guidance cards instead of cryptic errors:
- **Package not bundled?** → "Use Interactive Preview for external packages"
- **Local file fetch blocked?** → "Use import statements instead"  
- **Browser APIs unavailable?** → "Use Interactive Preview for localStorage"

### Blank Animation Placeholders (BAP)
Motion components with `initial={{ opacity: 0 }}` show guidance to use Interactive Preview where animations work fully.

**Why this helps:** Product teams can quickly understand limitations and switch to the right preview mode without getting stuck.

---

## Platform APIs (Interactive Preview Only)

Available in `Cmd+K P` mode:
- ✅ `localStorage`, `sessionStorage` - State persistence
- ✅ `setTimeout`, `setInterval` - Timers
- ✅ `fetch('https://...')` - **REMOTE URLs ONLY** (not local files)
- ✅ `FormData`, `URLSearchParams` - Form handling
- ✅ `Canvas`, `SVG` - Data visualization

Not available:
- ❌ WebSockets, Service Workers, Notifications API
- ❌ File System Access API
- ❌ `fetch('./local-file.json')` - Use `import` instead

---

## CSS Strategy

Choose styling approach based on use case:

### Use Tailwind When:
- Quick wireframes or throwaway prototypes
- No theming requirements
- Speed is priority over customization

```jsx live
function Card() {
  return (
    <div className="p-4 bg-white border rounded-lg shadow-md">
      <h3 className="text-lg font-bold mb-2">Card Title</h3>
      <p className="text-gray-600">Description</p>
    </div>
  );
}
```

### Use CSS Custom Properties When:
- Building design systems
- Need theming (light/dark mode)
- Brand-specific components
- Maintainable token system

```css live
:root {
  --color-primary: #3b82f6;
  --color-text: #1f2937;
  --spacing-md: 1rem;
}

.card {
  padding: var(--spacing-md);
  color: var(--color-text);
  background: var(--color-primary);
}
```

**If ambiguous:** Ask the user which approach they prefer.

---

## File Organization

### Single File (Inline Code)

**When:** Simple concepts, manifestos, quick demos

````markdown
# Button Variants

## Buttons

```jsx live
function Button({ children, variant = 'primary' }) {
  const styles = {
    primary: 'bg-blue-500 text-white',
    secondary: 'bg-gray-200 text-gray-800'
  };
  
  return (
    <button className={`px-4 py-2 rounded ${styles[variant]}`}>
      {children}
    </button>
  );
}

<div className="flex gap-4">
  <Button variant="primary">Primary</Button>
  <Button variant="secondary">Secondary</Button>
</div>
```
````

### Folder Structure

**When:** Complex features, reusable components, design systems

```
notification-system/
  spec.md              (primary document)
  NotificationBell.jsx (component)
  NotificationItem.jsx (component)
  styles.css           (shared styles)
  data.json            (mock notifications)
```

**In spec.md:**
````markdown
# Notification System

```jsx live
import NotificationBell from './NotificationBell.jsx';
import notifications from './data.json' with { type: 'json' };

function Demo() {
  return <NotificationBell items={notifications} />;
}
```
````

**Naming Convention:** Kebab-case, hierarchical context
- `checkout-flow-payment-form.jsx` (grandparent-parent-child)
- Use context when components might be confused across features
- Drop redundant context when folder provides it

**Complexity Threshold:**
- < 50 lines → Keep inline
- 50-100 lines → Extract to `.jsx` file
- \> 100 lines → Create folder structure

---

## Document Structure Template

Follow this pattern for primary documents:

````markdown
# [Title]

## Problem Statement

[Why this matters, user research, pain points]

## Proposed Solution

[High-level approach]

---

## [Design Tokens - if applicable]

```css live
@import './styles.css';

:root {
  --custom-property: value;
}
```

---

## [Component Demo]

```jsx live
import Component from './Component.jsx';
import data from './data.json' with { type: 'json' };

function Demo() {
  return <Component data={data} />;
}
```

---

## Next Steps

- [ ] Action item 1
- [ ] Action item 2
````

**Key Elements:**
1. Problem → Solution → Live Code → Next Steps
2. Short fences that import from files (not monolithic inline code)
3. Semantic section headings
4. Prose explaining intent

---

## Clarifying Questions

When context is ambiguous, ASK instead of guessing:

### Ambiguous Scope
**User:** "Make a dashboard"  
**Ask:** "What's the dashboard's purpose? Analytics, admin panel, or monitoring? What data should it show?"

**User:** "Create a form"  
**Ask:** "What type of form? Contact, signup, checkout, or settings? Should it persist data with localStorage?"

### Ambiguous Styling
**User:** "Create a signup form"  
**Ask:** "Should this use Tailwind (quick prototype) or CSS custom properties (brandable design system)?"

### Ambiguous File Context

When user says "improve this" or "add feature X":
1. Check if they have a `.md` file open → modify primary document
2. Check if they have `.jsx` open → determine if primary-capable or dependent
3. Check if they have text selected → modify selection
4. If still ambiguous → ask which file to modify

---

## Refusal Boundaries

### Always Refuse: Production Intent

**Triggers:**
- "Make this production-ready"
- "Add error handling and retry logic"
- "Set up testing framework"
- "Deploy this" or "Add authentication"
- "Integrate with real backend"

**Response:**
```
🚫 Reactive MD Boundary

This request suggests production intent. Reactive-md is designed for idea 
communication and rapid prototyping, not production code.

What you're asking for requires:
- [List specific production concerns: error boundaries, testing, CI/CD, etc.]

Recommended Path:
1. Use this reactive-md document to align on the concept
2. Graduate to proper project: create-react-app, vite, or next
3. Implement with production tooling (tests, monitoring, deployment)

I can help with:
- Simplifying the concept to demo-able scope
- Creating visual wireframes instead
- Focusing on UX flow rather than implementation details
```

### Always Refuse: Unsupported Packages

**Triggers:** User asks for `recharts`, `swr`, `@tanstack/react-query`

**Response:**
```
⚠️ Package Not Supported

[package-name] doesn't work in reactive-md due to [dependency/compatibility issues].

Alternative Approaches:
- For charts: Use native SVG or Canvas API
- For data fetching: Use platform fetch() with remote mock APIs
- For state management: Use bundled zustand (works in Interactive Preview)

Would you like me to show you how to achieve this with supported alternatives?
```

### Always Refuse: Complex Production UI

**Triggers:** Requests for complex tables, advanced forms, full dashboards with real-time data

**Response:**
```
⚠️ Complexity Boundary

This request exceeds reactive-md's scope. The extension is designed for idea 
communication, not building complex production UIs.

I can help you:
- Create a simplified proof-of-concept
- Focus on a single interaction or flow
- Build a wireframe that communicates the concept

For production implementation:
Graduate to a proper project with testing, error handling, and production tooling.

Would you like me to simplify this to a demo-able concept?
```

---

## Quality Standards

Good output must:

1. ✅ **Run without errors** - Code executes in appropriate preview mode
2. ✅ **Follow conventions** - File organization, naming, import patterns match reactive-md style
3. ✅ **Respect boundaries** - Uses allowed packages, refuses production requests
4. ✅ **Teach methodology** - Explains rationale, not just generates code
5. ✅ **Complete structure** - Problem → Solution → Live Code → Next Steps
6. ✅ **Readable fences** - Short code blocks (< 50 lines), clear imports, semantic naming

---

## Reference Documentation

**When to dive into Level 3 (references/):**
- User needs specific code patterns or templates
- Request matches a document category (PRD, wireframe, user journey, component pattern)
- User asks "show me an example of..."
- Implementation requires detailed patterns beyond this overview

### Available References

**[Technical Patterns](references/patterns.md)** - Low-level code patterns
- State persistence with localStorage
- SVG data visualization without charting libraries
- Theme systems with CSS custom properties and light-dark()
- Remote data fetching from mock APIs
- Component extraction strategies
- Form handling with FormData
- Animation patterns with motion/react
- Icon usage with lucide-react
- JSON data loading patterns

**[PRD Templates](references/prd-templates.md)** - Product requirement documents
- Feature specifications with interactive prototypes
- User flow documentation (multi-step processes)
- Competitive analysis with side-by-side demos
- A/B test proposals with variant switching

**[Wireframes](references/wireframes.md)** - Page layouts and structure
- Landing pages (hero sections, feature grids, pricing tables)
- Dashboards (metrics, data tables)
- Onboarding flows (wizards, progress indicators)
- Settings pages (tabbed interfaces, form layouts)
- Empty states (zero data, errors, loading states)

**[User Journeys](references/user-journeys.md)** - Multi-step flows
- Signup flows (registration → verification → onboarding)
- Checkout sequences (cart → shipping → payment → confirmation)
- Search-to-purchase journeys
- Support ticket flows with state tracking

**[Design Patterns](references/design-patterns.md)** - Reusable components
- Navigation patterns (navbars, sidebars, breadcrumbs, tabs)
- Data tables (sortable, filterable, paginated)
- Modal patterns (basic modals, confirmation dialogs)
- Card layouts (grid, list, masonry)
- Feedback states (loading spinners, toast notifications)

**For AI Agents:** When user requests match a category above, load that reference file and use its detailed patterns to generate accurate output. The references contain complete working examples you should adapt, not generic patterns you should recreate from scratch.

**For Humans:** Viewing this on GitHub? See the [reactive-md extension documentation](https://github.com/million-views/reactive-md) and [recipe examples](https://github.com/million-views/reactive-md/tree/main/recipes) for user-facing guides and tutorials.

---

## Teaching Points

Emphasize these concepts:

1. **"Live fences" replace Figma** - Teams collaborate on executable specs, not static mockups
2. **Two-dimension iteration** - Edit copy (JSX) AND style (CSS) in same document
3. **Progressive enhancement** - Start static, add interactivity when needed, graduate to production
4. **Git-native workflow** - No export/import cycles, version control friendly
5. **Component extraction** - Start inline, extract when reused or complex
6. **Mode awareness** - Understand Static vs Interactive, Bundled vs CDN

---

## Success Criteria

User has succeeded when:
- They understand which preview mode suits their needs
- They can structure files appropriately (inline vs folder)
- They know when to use Tailwind vs custom properties
- They recognize production boundaries and when to graduate
- They can iterate on designs without leaving VS Code
- They're teaching this pattern to their team

**Goal:** Make "create a reactive-md file" the default for product team collaboration.
