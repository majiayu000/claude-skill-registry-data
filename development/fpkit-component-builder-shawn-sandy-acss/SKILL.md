---
name: fpkit-component-builder
description: Build React components using @fpkit/acss library patterns. Scaffolds complete component structures (tsx, types, scss, stories, tests), validates CSS variables follow naming conventions (--component-property with rem units), enforces TypeScript patterns, accessibility standards (WCAG 2.1 AA), and Storybook documentation. Use when building new components, generating boilerplate, or refactoring to use fpkit primitives. Includes automation scripts, reference guides, and templates.
---

# fpkit Component Builder

Build React components using the @fpkit/acss component library following project patterns, conventions, and best practices.

## When to Use This Skill

Use this skill when:
- **Building new components** using fpkit primitives (Button, Card, etc.)
- **Scaffolding component boilerplate** with all required files
- **Refactoring existing components** to use fpkit patterns
- **Need guidance on** fpkit architecture, styling, accessibility, or testing
- **Validating CSS variables** follow naming conventions
- **Adding component exports** to index.ts

## Component Development Workflow

### Step 0: Detect & Analyze (Component Reuse) 🆕

**IMPORTANT**: Before creating any component, always check for reuse opportunities. This step prioritizes composition over duplication.

#### Run Component Analysis

```bash
# Analyze requested component and get recommendations
python3 scripts/recommend_approach.py ComponentName
```

This script will:
1. Scan existing fpkit components (25+ components)
2. Detect similar or related components that could be reused
3. Recommend one of three approaches:
   - **Compose**: Build from existing components
   - **Extend**: Add variant/feature to existing component
   - **Scaffold**: Create new component (last resort)

#### Understanding the Recommendations

**🔧 Compose (Preferred)**
- Requested component can be built by combining existing components
- Example: "StatusButton" = Button + Badge
- Action: Use composition template and import existing components

**📝 Extend**
- Component already exists or is very similar to existing
- Example: "EnhancedAlert" extends existing "Alert"
- Action: Add variant or new prop to existing component

**⚡ Scaffold New**
- Truly novel component with no reuse opportunities
- Action: Proceed with standard scaffolding

#### Quick Analysis Examples

```bash
# Example 1: AlertDialog (will suggest compose from Alert + Dialog)
python3 scripts/recommend_approach.py AlertDialog

# Example 2: IconButton (will suggest compose from Button + Icon)
python3 scripts/recommend_approach.py IconButton

# Example 3: LoadingButton (will suggest extend Button)
python3 scripts/recommend_approach.py LoadingButton
```

#### Decision Tree

```
Component Request
       ↓
┌──────────────┐
│ Run Analysis │  python3 scripts/recommend_approach.py ComponentName
└──────┬───────┘
       ↓
  ┌────────────────┐
  │ Recommendation │
  └────┬───────────┘
       ↓
   ┌───┴────┐
   ↓        ↓        ↓
COMPOSE   EXTEND   SCAFFOLD
   ↓        ↓        ↓
 Step 1a  Step 1b  Step 1c
```

**When to skip this step:**
- Modifying existing component (not creating new)
- Explicitly told to scaffold
- Building quick prototypes

**Reference:** Load `references/composition-patterns.md` for detailed composition strategies.

---

### Step 1a: Scaffold Composed Component

**Use when**: Analysis recommends COMPOSE approach.

Generate component using composition template:

```bash
python3 scripts/scaffold_component.py ComponentName \
  --mode compose \
  --uses Component1,Component2 \
  --path ./packages/fpkit/src/components/component-name
```

**Example: StatusButton composed from Badge + Button**

```bash
python3 scripts/scaffold_component.py StatusButton \
  --mode compose \
  --uses Badge,Button \
  --path ./packages/fpkit/src/components/status-button
```

This creates:
- `status-button.tsx` with composition template (imports Badge, Button)
- `status-button.types.ts`
- `status-button.scss` (minimal, reuses base component styles)
- `status-button.stories.tsx`
- `status-button.test.tsx`

**Then**: Implement composition logic by combining imported components.

**Reference:** Load `references/composition-patterns.md` for composition examples.

---

### Step 1b: Extend Existing Component

**Use when**: Analysis recommends EXTEND approach.

Generate component using extension template:

```bash
python3 scripts/scaffold_component.py ComponentName \
  --mode extend \
  --uses BaseComponent \
  --path ./packages/fpkit/src/components/component-name
```

**Example: EnhancedAlert extending Alert**

```bash
python3 scripts/scaffold_component.py EnhancedAlert \
  --mode extend \
  --uses Alert \
  --path ./packages/fpkit/src/components/enhanced-alert
```

**Alternative**: Consider adding variant to existing component instead of creating new one.

**Then**: Implement extension logic that enhances the base component.

---

### Step 1c: Scaffold New Component

**Use when**: Analysis recommends SCAFFOLD approach (no reuse opportunities).

```bash
python3 scripts/scaffold_component.py AlertBox --path ./packages/fpkit/src/components/alert-box
```

This creates:
- `alert-box.tsx` - Main component file
- `alert-box.types.ts` - TypeScript type definitions
- `alert-box.scss` - Styles with CSS variables
- `alert-box.stories.tsx` - Storybook stories
- `alert-box.test.tsx` - Vitest tests

**When to scaffold:**
- Starting a completely new component
- Need boilerplate for all files at once
- Want to ensure consistent file structure

**When to skip scaffolding:**
- Modifying existing components
- Building simple one-off components
- Only need specific files (create manually)

### Step 2: Implement Component Logic

Implement the component following fpkit patterns:

1. **Review component-patterns.md** for architecture guidance
2. **Build on the UI component** for polymorphic rendering
3. **Extend `React.ComponentProps<typeof UI>`** for type safety
4. **Add comprehensive JSDoc** documentation with examples
5. **Set displayName** for debugging
6. **Handle accessibility** (ARIA attributes, keyboard navigation)

**Key patterns to follow:**
- Use the polymorphic UI base component
- Support `as` prop for flexible rendering
- Include proper TypeScript types
- Add accessibility attributes
- Implement keyboard navigation for interactive components

**Reference:** Load `references/component-patterns.md` for detailed guidance.

### Step 3: Define TypeScript Types

Define component props following fpkit conventions:

1. **Extend UI component props**: `React.ComponentProps<typeof UI>`
2. **Use separate types file** for complex components (>50 lines of types)
3. **Add JSDoc comments** to props for documentation
4. **Export both component and types** from component file

**Simple component (inline types):**
```typescript
export type AlertProps = Partial<React.ComponentProps<typeof UI>> & {
  variant?: 'error' | 'warning' | 'success' | 'info'
  children?: React.ReactNode
}
```

**Complex component (separate types file):**
- Create `component.types.ts` for compound components
- Export all sub-component types
- Import types in main component file

**Reference:** Load `references/component-patterns.md` for type patterns.

### Step 4: Style with SCSS and CSS Variables

Create styles following fpkit CSS variable conventions:

1. **Review css-variable-guide.md** for naming standards
2. **Use rem units only** (not px) - base 16px = 1rem
3. **Follow naming pattern**: `--{component}-{property}`
4. **Use logical properties**: `padding-inline`, `padding-block` (not px/py)
5. **Avoid forbidden abbreviations**: Use `width` (not `w`), `padding` (not `p`)
6. **Validate with validate_css_vars.py** before committing

**CSS Variable Naming Pattern:**
```scss
// Base properties
--component-property: value

// Variants
--component-variant-property: value

// States
--component-state-property: value

// Elements
--component-element-property: value
```

**Validation:**
```bash
python3 scripts/validate_css_vars.py ./packages/fpkit/src/components/alert-box/alert-box.scss
```

**Approved abbreviations:** `bg`, `fs`, `fw`, `radius`, `gap`

**Forbidden abbreviations:** `px/py` (use `padding-inline/block`), `w/h` (use `width/height`), `cl` (use `color`), `dsp` (use `display`), `bdr` (use `border`)

**Reference:** Load `references/css-variable-guide.md` for complete guide.

### Step 5: Create Storybook Stories

Document the component with interactive Storybook stories:

1. **Review storybook-patterns.md** for story structure
2. **Import component styles**: `import './component.scss'`
3. **Configure meta object** with title, tags, args
4. **Create story variants** (default, variants, sizes, states)
5. **Add play functions** to test interactions
6. **Test keyboard navigation** in play functions
7. **Document CSS variables** in Customization story

**Story organization:**
- Default/Basic
- Variants (primary, secondary, etc.)
- Sizes (small, medium, large)
- States (disabled, loading, error)
- Compositions (with icon, multiple components)
- Customization (CSS variables demo)

**Play function testing:**
- Component rendering
- Click events
- Keyboard navigation (Tab, Enter, Space)
- Accessibility attributes
- State changes

**Reference:** Load `references/storybook-patterns.md` for detailed patterns.

### Step 6: Write Tests

Create comprehensive tests with Vitest and React Testing Library:

1. **Review testing-patterns.md** for test structure
2. **Test rendering** (children, custom props, polymorphism)
3. **Test variants and sizes** (data attributes, styles)
4. **Test event handling** (click, keyboard, pointer)
5. **Test accessibility** (ARIA attributes, focus management)
6. **Test disabled states** (aria-disabled behavior)

**Test organization:**
```typescript
describe('ComponentName', () => {
  describe('Basic Rendering', () => { /* ... */ })
  describe('Variants', () => { /* ... */ })
  describe('Event Handling', () => { /* ... */ })
  describe('Accessibility', () => { /* ... */ })
})
```

**Coverage goals:**
- Statements: >80%
- Branches: >75%
- Functions: >80%

**Reference:** Load `references/testing-patterns.md` for patterns and examples.

### Step 7: Export Component

Add component exports to `src/index.ts`:

```bash
python3 scripts/add_to_exports.py AlertBox ./components/alert-box/alert-box --index ./packages/fpkit/src/index.ts
```

**Manual export format:**
```typescript
// Core UI components
export { AlertBox, type AlertBoxProps } from "./components/alert-box/alert-box";
```

**Compound components:**
```typescript
export {
  Card,
  Title as CardTitle,
  Content as CardContent,
  type CardProps,
} from "./components/cards/card";
```

### Step 8: Validate and Build

Validate the component before committing:

```bash
# Validate CSS variables
python3 scripts/validate_css_vars.py ./packages/fpkit/src/components/alert-box/alert-box.scss

# Run linter
npm run lint

# Run type checker
npx tsc --noEmit

# Run tests
npm test alert-box

# Build package
npm run build
```

**Validation checklist:**
- [ ] CSS variables follow naming pattern
- [ ] All units are rem (not px)
- [ ] TypeScript types are correct
- [ ] Tests pass with >80% coverage
- [ ] Storybook stories render correctly
- [ ] Accessibility tests pass
- [ ] Component exported from index.ts
- [ ] Build succeeds without errors

## Bundled Resources

### Automation Scripts

#### recommend_approach.py 🆕

Analyze component requests and recommend the best development approach.

**Usage:**
```bash
python3 scripts/recommend_approach.py <ComponentName> [--format <text|json>]
```

**Example:**
```bash
python3 scripts/recommend_approach.py StatusButton
```

**Output:**
- Recommended approach (compose/extend/scaffold)
- Reasoning for recommendation
- Components to reuse (if applicable)
- Actionable next steps
- Example code (for composition)

**When to use:**
- **Always** before creating a new component
- When unsure whether to reuse existing components
- To discover similar components in the library

**What it analyzes:**
- Exact name matches (component already exists)
- Similar component names (>70% similarity)
- Composite component detection ("AlertDialog" = Alert + Dialog)
- Recommended building blocks based on patterns

---

#### analyze_components.py 🆕

Scan fpkit component library and build a searchable catalog.

**Usage:**
```bash
python3 scripts/analyze_components.py [--output <file.json>] [--verbose]
```

**Example:**
```bash
python3 scripts/analyze_components.py --output catalog.json --verbose
```

**What it catalogs:**
- Component names and file paths
- Exported types and interfaces
- Component complexity (simple/moderate/complex)
- Available variants (from SCSS)
- Component dependencies
- Sub-components (for compound components)

**Used by:**
- `recommend_approach.py` for intelligent analysis
- `suggest_reuse.py` for similarity matching

---

#### suggest_reuse.py 🆕

Suggest existing components that could be reused or composed.

**Usage:**
```bash
python3 scripts/suggest_reuse.py <ComponentName> [--threshold <0-100>]
```

**Example:**
```bash
python3 scripts/suggest_reuse.py IconButton --threshold 50
```

**What it suggests:**
- Exact matches (component already exists)
- Similar components (by name similarity)
- Composite parts (components that make up the name)
- Building blocks (UI primitives that could be used)

**Threshold:**
- Minimum similarity score (0-100)
- Default: 30 (suggests fairly similar components)
- Higher values (70+): Only very similar components

**Used by:**
- `recommend_approach.py` for decision-making

---

#### scaffold_component.py (Enhanced 🆕)

Generate complete component structure from templates with support for composition and extension modes.

**Usage:**
```bash
python3 scripts/scaffold_component.py <ComponentName> \
  [--path <output-directory>] \
  [--mode <new|compose|extend>] \
  [--uses <Component1,Component2>]
```

**Examples:**

```bash
# New component (default)
python3 scripts/scaffold_component.py AlertBox --path ./packages/fpkit/src/components/alert-box

# Composed component
python3 scripts/scaffold_component.py StatusButton \
  --mode compose \
  --uses Badge,Button \
  --path ./packages/fpkit/src/components/status-button

# Extended component
python3 scripts/scaffold_component.py EnhancedAlert \
  --mode extend \
  --uses Alert \
  --path ./packages/fpkit/src/components/enhanced-alert
```

**Modes:**
- `new` (default): Create brand new component from scratch
- `compose`: Create component by composing existing components
- `extend`: Create component that extends existing component

**What it creates:**
- `component.tsx` with appropriate template (new/composed/extended)
- `component.types.ts` with Props interface
- `component.scss` with CSS variables
- `component.stories.tsx` with play functions
- `component.test.tsx` with test structure

**New in composition mode:**
- Auto-generates imports for components specified in `--uses`
- Uses composition template with TODOs for implementation
- Includes inline examples of composition patterns

**New in extension mode:**
- Auto-generates import for base component
- Uses extension template with enhancement guidelines
- Includes examples of wrapping/enhancing base component

#### validate_css_vars.py

Validate CSS variable naming and rem units.

**Usage:**
```bash
python3 scripts/validate_css_vars.py <file.scss>
```

**What it checks:**
- CSS variable naming follows `--{component}-{property}` pattern
- All spacing/sizing uses rem (not px)
- Logical properties used (padding-inline, not px)
- No forbidden abbreviations (w/h, px/py, cl, dsp, bdr)

**When to use:**
- Before committing SCSS changes
- When refactoring component styles
- To ensure consistency across components

#### add_to_exports.py

Add component exports to index.ts.

**Usage:**
```bash
python3 scripts/add_to_exports.py <ComponentName> <component-path> [--index <index-path>]
```

**Example:**
```bash
python3 scripts/add_to_exports.py AlertBox ./components/alert-box/alert-box --index ./packages/fpkit/src/index.ts
```

**Options:**
- `--section`: Section comment to insert after
- `--no-types`: Don't export Props type
- `--dry-run`: Preview without modifying

### Reference Documentation

Load these references as needed for detailed guidance:

#### references/composition-patterns.md 🆕

Component composition strategies and patterns for reusing existing components.

**What it covers:**
- Why composition over duplication
- Composition vs creation decision tree
- Common composition patterns (Container + Content, Conditional, Enhanced Wrapper, List, Compound)
- Anti-patterns to avoid (over-composition, prop drilling, duplication)
- Real-world examples (AlertDialog, IconButton, TagInput)
- Guidelines summary table

**Load when:**
- Building components by composing existing ones
- Need examples of composition patterns
- Want to understand when to compose vs create new
- Following Step 0 analysis recommendation to compose
- Learning best practices for component reuse

---

#### references/css-variable-guide.md

Complete CSS variable naming standard with:
- Naming pattern (`--{component}-{property}`)
- Approved/forbidden abbreviations
- rem unit conversion guide
- Variant, state, and element patterns
- Customization examples

**Load when:**
- Creating or modifying SCSS files
- Need CSS variable naming guidance
- Customizing component styles
- Validating CSS conventions

#### references/component-patterns.md (Updated 🆕)

Architectural patterns for fpkit components:
- **Component Reuse Strategies** 🆕 (Composition/Extension/Creation decision matrix)
- UI component foundation
- Simple vs compound component patterns
- Hook integration patterns
- Polymorphic rendering
- Export patterns
- Automated reuse detection tools

**Load when:**
- Building new components
- Need architecture guidance
- Creating compound components
- Understanding component structure
- **Learning reuse strategies** 🆕
- **Deciding whether to compose, extend, or create new** 🆕

#### references/accessibility-patterns.md

Accessibility standards and ARIA patterns:
- WCAG 2.1 Level AA requirements
- ARIA attributes and usage
- Keyboard navigation patterns
- Focus management
- Screen reader support

**Load when:**
- Implementing interactive components
- Adding accessibility features
- Testing keyboard navigation
- Ensuring WCAG compliance

#### references/testing-patterns.md

Vitest and React Testing Library patterns:
- Test structure and organization
- Query patterns (getByRole, getByLabelText)
- Event testing (click, keyboard, pointer)
- Accessibility testing
- Async and state testing

**Load when:**
- Writing component tests
- Need testing examples
- Testing interactions
- Achieving coverage goals

#### references/storybook-patterns.md

Storybook story structure and play functions:
- Story file organization
- Meta configuration
- Play function patterns
- Keyboard navigation testing
- Documentation patterns

**Load when:**
- Creating Storybook stories
- Adding play function tests
- Documenting components
- Testing in Storybook

### Template Assets

Component templates used by scaffold_component.py:

- `assets/templates/component.template.tsx`
- `assets/templates/component.template.types.ts`
- `assets/templates/component.template.scss`
- `assets/templates/component.template.stories.tsx`
- `assets/templates/component.template.test.tsx`

**Placeholders:**
- `{{ComponentName}}` - PascalCase component name
- `{{componentName}}` - camelCase component name
- `{{component-name}}` - kebab-case component name
- `{{COMPONENT_NAME}}` - UPPERCASE component name

## Best Practices

### ✅ Do

- Use scaffold script for new components
- Follow the 5-file structure consistently
- Build on the UI component
- Use CSS variables with rem units
- Follow naming conventions strictly
- Add comprehensive JSDoc documentation
- Test accessibility (ARIA, keyboard)
- Create Storybook stories with play functions
- Validate CSS before committing
- Export from index.ts
- Test with >80% coverage

### ❌ Don't

- Skip validation scripts
- Use px units (use rem)
- Use forbidden abbreviations
- Forget to import styles in stories
- Skip accessibility testing
- Create components without tests
- Ignore TypeScript errors
- Forget displayName
- Skip JSDoc documentation

## Common Tasks

### Building a Simple Component (Badge, Tag)

1. Scaffold: `python3 scripts/scaffold_component.py Tag`
2. Implement in `tag.tsx` (extend UI component)
3. Define inline types (no separate types file needed)
4. Style in `tag.scss` with CSS variables
5. Create stories in `tag.stories.tsx`
6. Write tests in `tag.test.tsx`
7. Validate CSS: `python3 scripts/validate_css_vars.py tag.scss`
8. Export: `python3 scripts/add_to_exports.py Tag ...`

### Building a Compound Component (Card, Dialog)

1. Scaffold: `python3 scripts/scaffold_component.py Card`
2. Create separate `card.types.ts` for complex types
3. Implement main component and sub-components
4. Attach sub-components as static properties
5. Style with element-specific CSS variables
6. Test compound component structure
7. Export main and sub-components

### Refactoring to fpkit Patterns

1. Review `references/component-patterns.md`
2. Replace hardcoded elements with UI component
3. Update CSS to use CSS variables
4. Validate naming: `python3 scripts/validate_css_vars.py ...`
5. Add accessibility attributes
6. Update tests to check new patterns
7. Update Storybook stories

### Validating Component Quality

```bash
# CSS validation
python3 scripts/validate_css_vars.py component.scss

# Linting
npm run lint

# Type checking
npx tsc --noEmit

# Tests with coverage
npm run test:coverage

# Build verification
npm run build

# Storybook visual check
npm run storybook
```

## Troubleshooting

### CSS Validation Errors

**Error: "Use rem units instead of px"**
- Convert px to rem: px / 16 = rem
- Example: 24px = 1.5rem

**Error: "Forbidden abbreviation 'px'"**
- Use `padding-inline` instead of `px`
- Use `padding-block` instead of `py`

**Error: "Variable should follow --{component}-{property} pattern"**
- Check component prefix matches file name
- Follow: `--alert-bg` not `--alert-background-color`

### Scaffold Script Issues

**Error: "Template not found"**
- Ensure templates exist in `assets/templates/`
- Check template file names match expectations

**Error: "Output directory exists"**
- Remove existing directory or use different name
- Or modify existing files manually

### Export Script Issues

**Error: "Export already exists"**
- Component already exported in index.ts
- Check existing exports before running script

### Build Errors

**TypeScript errors:**
- Check type definitions in `.types.ts` file
- Ensure UI component is imported correctly
- Verify all props are typed

**SCSS errors:**
- Check for syntax errors in SCSS
- Ensure all CSS variables are defined
- Validate with validate_css_vars.py

## Project Context

### fpkit Component Library

- **Location**: `packages/fpkit/`
- **Built with**: React 18+, TypeScript, SCSS
- **Build tool**: tsup (generates ESM and CJS)
- **Test framework**: Vitest + React Testing Library
- **Documentation**: Storybook with play functions
- **Styling**: CSS custom properties (not Tailwind)

### File Paths

- **Components**: `packages/fpkit/src/components/`
- **Main export**: `packages/fpkit/src/index.ts`
- **Styles**: Component SCSS compiled to `libs/components/`
- **Tests**: Co-located with components (`.test.tsx`)
- **Stories**: Co-located with components (`.stories.tsx`)

### Build Commands

```bash
# Development
npm start                 # Build + watch
npm run dev              # Vite dev server

# Production
npm run build            # Full build (TS + SCSS + CSS)
npm run package          # Build TypeScript with tsup

# Testing
npm test                 # Run tests
npm run test:coverage    # With coverage
npm run test:ui          # With UI

# Linting
npm run lint             # Check code style
npm run lint-fix         # Auto-fix issues

# Validation
python3 scripts/validate_css_vars.py <file.scss>
```

## Summary

To build a new fpkit component with the updated workflow:

**0. Detect & Analyze (🆕 ALWAYS START HERE)**
   - Run `recommend_approach.py ComponentName`
   - Review recommendation: Compose / Extend / Scaffold
   - Load `composition-patterns.md` if composing

**1. Scaffold (based on recommendation)**
   - Compose: `scaffold_component.py --mode compose --uses ...`
   - Extend: `scaffold_component.py --mode extend --uses ...`
   - New: `scaffold_component.py ComponentName`

**2. Implement** following component-patterns.md
   - Compose: Combine imported components
   - Extend: Enhance base component
   - New: Build from UI primitive

**3. Define types** extending UI component props or base component props

**4. Style** with CSS variables (rem units only)
   - Compose: Minimal styles, reuse base component styles
   - Extend: Import base styles, add only new variants
   - New: Full SCSS with CSS variables

**5. Validate** with `validate_css_vars.py`

**6. Document** in Storybook with play functions
   - Document composition/extension in JSDoc

**7. Test** with Vitest (>80% coverage)
   - Compose: Test integration of composed components
   - Extend: Test both base and enhanced features

**8. Export** with `add_to_exports.py`

**9. Build** and verify no errors

**Key Principle**: **Composition over duplication** - Always check for reuse opportunities before creating new components.

Load reference documentation as needed for detailed guidance on composition, patterns, accessibility, testing, and Storybook.
