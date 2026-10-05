---
name: implement-design
description: >-
  Translate Figma designs into production-ready code. Use when the user says "implement design",
  "build from Figma", "code this component", "implement this screen", or pastes a Figma URL
  (figma.com/design/...). Fetches design context, discovers project conventions, and generates
  code that matches existing patterns using design tokens instead of hardcoded values.
---

# Implement Design Skill

Translate Figma designs into production-ready code using MCP tools and project convention auto-discovery.

For detailed reference on URL parsing, MCP tool parameters, auto-discovery commands, and mapping tables, see [workflow-details.md](references/workflow-details.md).

## Workflow

### Step 1: Parse Figma Input

Extract `fileKey` and `nodeId` from the user's input.

**URL formats:**
- Standard: `https://figma.com/design/:fileKey/:fileName?node-id=:int1-:int2`
- Branch: `https://figma.com/design/:fileKey/branch/:branchKey/:fileName` (use `branchKey` as fileKey)
- Make: `https://figma.com/make/:makeFileKey/:makeFileName`

**Node ID conversion:** Always convert URL format `1-2` to API format `1:2` (replace `-` with `:`).

If the user provides a URL, extract both values. If they describe a component by name, ask for the Figma URL.

### Step 2: Fetch Design Context

Call `get_design_context` with the extracted `fileKey` and `nodeId`:

```
get_design_context(fileKey, nodeId)
```

This returns:
- **Layout structure** - auto-layout direction, spacing, padding, constraints
- **Typography** - font family, size, weight, line height, letter spacing
- **Colors** - fills, strokes, opacity values
- **Generated code** - starter code adapted from the design
- **`downloadUrls`** - JSON mapping of asset names to download URLs

Save the returned data -- it's the primary source for implementation.

### Step 3: Capture Visual Reference

Call `get_screenshot` as ground truth for visual validation:

```
get_screenshot(fileKey, nodeId)
```

Use this image throughout implementation to verify your output matches the design. Return to it during the validation step.

### Step 4: Fetch Design Tokens

Call both tools to get token mappings:

```
get_variable_defs(fileKey, nodeId)     # Color, spacing, typography tokens
get_code_connect_map(fileKey, nodeId)  # Existing component-to-code mappings
```

- `get_variable_defs` returns variable names and resolved values (e.g., `icon/default/secondary` -> `#949494`)
- `get_code_connect_map` returns `{ nodeId: { codeConnectSrc, codeConnectName } }` for mapped components

If Code Connect mappings exist, use the mapped component directly from the codebase. Read the source file to understand its props API.

### Step 5: Discover Project Conventions

Before writing any code, auto-discover the project's patterns. Run these searches in parallel:

**UI Library & Component Structure:**
```
Glob: **/components/ui/**/*.{tsx,vue,svelte}      # UI primitives
Glob: **/components/**/{Button,Card,Input}.*       # Common components
Grep: "from '@/components"  OR  "from '~/components"  # Import patterns
```

**Design Tokens & Styling:**
```
Glob: **/{tokens,theme,variables}.{css,ts,js}      # Token files
Glob: **/tailwind.config.{js,ts,mjs,cjs}           # Tailwind config
Grep: "--color-" OR "colors:" in tailwind config    # Color tokens
```

**File Naming & Structure:**
```
Glob: **/components/**/index.{ts,tsx}               # Barrel exports
Grep: "export.*from" in component directories       # Re-export patterns
```

**Icon Library:**
```
Grep: "lucide-react\|@heroicons\|react-icons\|@phosphor-icons"  # Icon imports
Glob: **/icons/**/*.{tsx,svg}                       # Custom icons
```

**Similar Components (find reference implementations):**
```
Glob: **/components/**/*.{tsx,vue,svelte}           # All components
```
Find a component similar to what you're building and use it as a structural reference.

### Step 6: Implement Code

Map Figma properties to project patterns:

| Figma Concept | Code Pattern |
|---|---|
| Auto-layout (horizontal) | `flex` / `flex-row` |
| Auto-layout (vertical) | `flex` / `flex-col` |
| Auto-layout gap | `gap-{n}` (map to nearest token) |
| Fill container | `flex-1` / `w-full` |
| Fixed size | `w-[{n}px]` / `h-[{n}px]` (prefer tokens) |
| Padding | `p-{n}`, `px-{n}`, `py-{n}` |
| Corner radius | `rounded-{n}` |
| Color fills | Map to design token variable, not hex |
| Text styles | Map to typography system classes |
| Component instances | Use existing UI components from Step 5 |
| Shadows | `shadow-{sm,md,lg}` or custom token |

**Implementation rules:**
1. **Tokens over hardcoded values.** Map every color, spacing, and font to the project's token system. Only use raw values if no token matches within 2px/shades.
2. **Reuse over create.** If a UI primitive exists (Button, Card, Input, Badge, etc.), use it. Don't recreate.
3. **Adapt generated code.** The code from `get_design_context` is a starting point -- adapt it to match project conventions (imports, naming, component API patterns).
4. **Download assets.** Use `downloadUrls` from Step 2 to download images/icons. Check if equivalent assets already exist before downloading. Place in the project's asset directory.
5. **Follow project file structure.** Put the new component where similar components live. Match the naming convention (PascalCase, kebab-case, etc.).
6. **Accessibility.** Add proper semantic HTML, ARIA labels for interactive elements, alt text for images, keyboard navigation for focusable elements.

### Step 7: Validate

Compare your implementation against the screenshot from Step 3.

**Checklist:**
- [ ] No hardcoded colors, spacing, or font sizes (all use tokens/theme)
- [ ] Existing UI components reused where applicable
- [ ] Responsive behavior considered (even if Figma shows single viewport)
- [ ] Semantic HTML and accessibility attributes present
- [ ] File placed in correct directory following project conventions
- [ ] Import paths use project aliases (`@/`, `~/`, etc.)
- [ ] Component API follows project patterns (props interface, default exports, etc.)

## Key Principles

1. **Design tokens are non-negotiable.** Never hardcode a color like `#3B82F6` when a token like `text-primary` or `var(--color-primary)` exists.
2. **The screenshot is truth.** When the design context data and screenshot disagree, trust the screenshot.
3. **Convention over configuration.** Match existing project patterns exactly. If the project uses `className` props, don't introduce `style` objects. If it uses CSS modules, don't introduce Tailwind.
4. **Minimal footprint.** Only create what the design requires. Don't add hover states, animations, or variants unless they're in the design or explicitly requested.
