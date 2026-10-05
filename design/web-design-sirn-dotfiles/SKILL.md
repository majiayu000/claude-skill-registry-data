---
name: web-design
type: reference
description: Reference for accessible, consistent, clean web design, spacing discipline, strong UX, and anti-AI aesthetics. ALWAYS read before writing, refactoring, or reviewing web UI, CSS, stylesheets, design tokens, or component templates.
---

Web design guidelines for building simple, accessible, consistent, and user-focused web interfaces. Prioritize clear hierarchy, usability, and speed over decorative trends or AI-generated aesthetics.

### Core Layout & Spacing Rules

1. **Never use external margins on components or elements**:
   - Do not use `margin` to position or separate sibling elements.
   - Elements must never push outward onto their surroundings. Components that manage their own external spacing become brittle and cannot be reused cleanly across different contexts.
   - **CSS**: Do not write `margin`, `margin-top`, `margin-bottom`, `margin-inline`, or `margin-block` on components or element selectors.
   - **Tailwind**: Do not use `m-*`, `mt-*`, `mb-*`, `ml-*`, `mr-*`, `mx-*`, or `my-*` on components.

2. **Elements can only change internal padding**:
   - Use `padding` exclusively for an element's own internal breathing room.
   - Padding defines the space between the element's border/boundary and its child content.
   - **CSS**: Set `padding`, `padding-inline`, or `padding-block` on the container or card element itself.
   - **Tailwind**: Use `p-*`, `px-*`, `py-*`, `pt-*`, `pb-*`, `pl-*`, or `pr-*`.

3. **Parent containers manage spacing with Flexbox or Grid gap**:
   - Use layout containers (`display: flex`, `display: grid`) with `gap` to separate child elements.
   - Spacing is the responsibility of the layout container. Children remain modular and position-agnostic.
   - **CSS**: Use `display: flex; flex-direction: column; gap: var(--space-4);` or `display: grid; gap: var(--space-6);`.
   - **Tailwind**: Use `flex flex-col gap-4` or `grid gap-6`.

4. **The Prose Exception**:
   - The **only** acceptable use of margin is inside long-form prose and rich text (such as articles, blog posts, documentation flows, markdown rendering, or CMS copy) where paragraphs, headings, blockquotes, and lists flow sequentially in a single typographic stream.
   - **CSS**: Apply margins only inside scoped prose selectors (e.g. `.prose p`, `.article h2`).
   - **Tailwind**: Use typography plugins or scoped selectors (e.g. `prose`, `prose-slate`).

5. **Use predefined scale values — No ad-hoc or arbitrary sizing**:
   - Always use defined design tokens, theme scales, or consistent spacing scales for widths, heights, padding, and gaps.
   - Do not invent one-off pixel dimensions in element definitions.
   - If a layout requires a new dimension, define a reusable token in the design system or theme rather than inlining an ad-hoc value.
   - **CSS**: Use custom properties from the token scale (e.g. `var(--space-4)`, `var(--size-container-md)`).
   - **Tailwind**: Use standard scale classes (e.g. `w-80`, `p-4`, `gap-6`, `max-w-xl`). **Never** use arbitrary bracket values such as `[Npx]`, `[Nrem]`, `w-[320px]`, `p-[13px]`, or `gap-[15px]`.

6. **Strict Exception Policy**:
   - Only break these layout rules if the requirement is strictly justifiable and impossible to achieve with flex, grid, gap, or padding.
   - When an exception is necessary, add a code comment explaining the constraint and why standard container spacing could not solve the layout.

---

### Accessibility (A11y) Rules

- **Semantic HTML first**:
  - Use native HTML elements for their intended purpose (`<button>`, `<a>`, `<input>`, `<select>`, `<dialog>`, `<main>`, `<nav>`, `<header>`, `<aside>`).
  - Never use a `<div onclick="...">` when a `<button>` or `<a>` is appropriate.
- **Keyboard navigation & focus indicators**:
  - Ensure every interactive element is focusable and operates via keyboard (`Tab`, `Enter`, `Space`, arrow keys).
  - Never remove focus outlines without providing a distinct replacement.
  - Provide high-contrast visible focus rings (e.g., `focus-visible:ring-2 focus-visible:ring-offset-2`, `:focus-visible { outline: 2px solid var(--color-focus); outline-offset: 2px; }`).
- **Color contrast & legibility**:
  - Maintain a minimum contrast ratio of 4.5:1 for body text and 3:1 for large text / UI controls (WCAG AA).
  - Do not rely on color alone to convey state or status; pair color with icons or descriptive text.
  - Ensure dark gray text on dark backgrounds or light gray text on light backgrounds is strictly avoided.
- **Form usability & labeling**:
  - Every form input must have an associated, visible `<label>` using `for` / `id` or wrapping.
  - Never use `placeholder` text as a substitute for a label. Placeholders disappear when typed into.
  - Associate error messages and helper text with `aria-describedby` and use `aria-invalid="true"` on failed validation.
- **Touch & pointer target size**:
  - Interactive targets (buttons, links, form controls) must have a minimum clickable area of 44×44px on mobile and touch devices.
- **Motion sensitivity**:
  - Respect `prefers-reduced-motion`. Disable or simplify non-essential animations for users with motion sensitivity.
- **Prose line length**:
  - Limit text column width to 60–75 characters (`max-w-prose` or `max-inline-size: 65ch`) for optimal reading comprehension.

---

### UX & Functional Simplicity

- **Task-first clarity**:
  - Put primary actions and core information where users look first.
  - Do not hide common actions behind complex hover menus or nested dropdowns.
- **Complete interaction states**:
  - Every interactive component must define 6 states: default, hover, active (pressed), focus-visible, disabled, and loading.
  - Disabled controls must look distinct but retain readable contrast.
- **Immediate feedback & clear system state**:
  - Provide immediate visual confirmation when an action starts (loading spinners, disabled buttons during submission).
  - Provide descriptive, actionable error messages. Tell the user what went wrong and how to fix it.
  - Build informative empty states with a direct call to action (e.g., "No projects yet. Create your first project.").
- **Fast and stable rendering**:
  - Avoid layout shifts (CLS). Reserve space for dynamic content, images, and asynchronous data.
  - Prefer instant CSS transitions (100–200ms) over slow, elaborate multi-stage animations.

---

### Anti-AI Aesthetics & Visual Restraint

AI-generated web layouts often share generic, copy-paste visual tropes that make interfaces look cheap and unrefined. Avoid these clichés:

#### Clichés to Avoid

- **Gratuitous glow blobs and mesh gradients**: Avoid purple, indigo, or neon gradient blobs floating behind dark cards.
- **Glassmorphism overload**: Do not use heavy backdrop blurs with semi-transparent frosted borders on every surface.
- **Excessive drop shadows**: Avoid exaggerated, multi-layered ambient drop shadows on flat UI components.
- **Meaningless decorative badges**: Do not add pill chips ("✨ AI Powered", "🚀 Next-Gen", "⚡ Ultra Fast") above headings without functional purpose.
- **Floating 3D emojis and icons in colored circles**: Avoid circular badge containers with generic icons on every card header.
- **Nested border boxes**: Avoid wrapping cards inside cards with borders and subtle backgrounds that produce visual noise.
- **Monotonous hero sections**: Avoid the centered headline + purple gradient text + floating generic dashboard screenshot pattern.

#### Principles of Clean, Human Web Design

- **Functional restraint**: Remove every visual element that does not convey information or aid task completion. Let content provide structure.
- **Restricted typography scale**:
  - Pick a strict scale of 4–5 font sizes: caption, body, subheading, section title, page title.
  - Set appropriate line heights: tighter on large titles, relaxed on body text.
  - Limit font families to at most one or two clean typefaces.
- **Grounded color palette**:
  - Anchor the UI on clean, neutral scales (e.g. slate, zinc, gray, stone).
  - Use one primary accent color purposefully for primary actions and active states.
  - Reserve semantic colors (success, error, warning, info) strictly for system status.
- **Whitespace over borders**:
  - Group related items with smaller gaps.
  - Separate distinct sections with larger gaps.
  - Rely on whitespace rather than borders and box shadows to define layout boundaries.

---

### Layout Comparison Examples

#### Anti-Pattern: Component-Level Margin & AI Clichés

```html
<!-- BAD: Sibling components managing external margins, arbitrary values, decorative fluff -->
<div class="card-list">
  <div
    class="w-[340px] mb-6 rounded-2xl bg-white/10 backdrop-blur-md shadow-2xl p-[18px]"
  >
    <div class="h-8 w-8 rounded-full bg-purple-500/20 text-purple-400">✨</div>
    <h3
      class="mt-2 text-xl font-bold bg-gradient-to-r from-purple-400 to-pink-400 bg-clip-text text-transparent"
    >
      AI Feature
    </h3>
    <p class="mt-2 text-gray-400">Description here...</p>
    <button
      class="mt-4 w-full bg-gradient-to-r from-purple-600 to-indigo-600 p-2 rounded-xl"
    >
      Get Started
    </button>
  </div>
</div>
```

#### Correct Pattern: Container Gap, Semantic HTML, Accessible UI

```html
<!-- GOOD: Semantic HTML, container gap, clear hierarchy, accessible states -->
<!-- CSS Example -->
<main class="page-container">
  <section class="card-grid">
    <article class="card">
      <h2 class="card-title">Project Overview</h2>
      <p class="card-body">A simple summary of project activity and metrics.</p>
      <div class="card-actions">
        <button type="button" class="btn btn-secondary">View logs</button>
        <button type="button" class="btn btn-primary">Edit project</button>
      </div>
    </article>
  </section>
</main>

<style>
  .page-container {
    padding: var(--space-8);
    max-inline-size: var(--size-container-lg);
    margin-inline: auto; /* centered container */
  }
  .card-grid {
    display: grid;
    gap: var(--space-6);
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  }
  .card {
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
    padding: var(--space-6);
    background-color: var(--color-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
  }
  .card-title {
    font-size: var(--text-lg);
    font-weight: 600;
    color: var(--color-text-primary);
  }
  .card-body {
    font-size: var(--text-sm);
    line-height: 1.5;
    color: var(--color-text-secondary);
  }
  .card-actions {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-2);
  }
</style>

<!-- Tailwind Example -->
<main class="mx-auto max-w-5xl p-8">
  <section class="grid grid-cols-1 gap-6 sm:grid-cols-2">
    <article
      class="flex flex-col gap-4 rounded-lg border border-slate-200 bg-white p-6"
    >
      <h2 class="text-lg font-semibold text-slate-900">Project Overview</h2>
      <p class="text-sm leading-relaxed text-slate-600">
        A simple summary of project activity and metrics.
      </p>
      <div class="flex justify-end gap-2">
        <button
          type="button"
          class="rounded-md border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2"
        >
          View logs
        </button>
        <button
          type="button"
          class="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-slate-900 focus-visible:ring-offset-2"
        >
          Edit project
        </button>
      </div>
    </article>
  </section>
</main>
```

---

### Design & Usability Checklist

Before finalizing any UI implementation or template:

- [ ] **Layout**: Are all margins eliminated from components and child elements?
- [ ] **Spacing**: Is inter-element spacing managed by parent flex/grid containers with `gap`?
- [ ] **Scale**: Are all spacing, typography, and sizing values drawn from predefined design tokens or scales (no arbitrary bracket values like `[13px]`)?
- [ ] **Prose**: Is margin used only inside long-form prose and markdown content?
- [ ] **Accessibility**: Does the UI use semantic HTML elements (`<button>`, `<a>`, `<main>`, `<nav>`)?
- [ ] **Keyboard navigation**: Are all interactive elements focusable with clear `:focus-visible` indicators?
- [ ] **Contrast**: Do text colors meet WCAG AA contrast standards (minimum 4.5:1)?
- [ ] **Forms**: Does every input have a visible, associated `<label>` (not just placeholder text)?
- [ ] **Touch targets**: Are interactive targets at least 44×44px on mobile viewports?
- [ ] **Restraint**: Are unnecessary borders, decorative gradient blobs, glassmorphism, and excessive shadows removed?
- [ ] **Interaction states**: Are `hover`, `focus-visible`, `active`, and `disabled` states clearly styled?
