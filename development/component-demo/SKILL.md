---
name: "component demo"
description: "Create demonstration pages for components and hooks."
license: Proprietary
---

# Component Demo Skill

This skill guides the creation and maintenance of components and their demo pages in the Protobox component showcase.

## When to Use This Skill

Use this skill when:
- Creating new custom components in `src/components/`
- Creating new custom hooks in `src/hooks/`
- Updating existing components or hooks
- Planning feature additions that involve reusable components

## Component Development Workflow

### Phase 1: Planning - Ask About Demo Pages

**IMPORTANT:** When planning to create a new component or hook, ALWAYS ask the user:

> "Would you like me to create a demo page for this [component/hook] in the component showcase?"

Options to present:
1. **Yes, create demo page** - Create both the component and a showcase demo
2. **Yes, standalone demo** - Create component and a standalone demo page at `/[name]-demo`
3. **Yes, playground** - Create an interactive playground with props controls (Storybook-like)
4. **No demo needed** - Just create the component/hook

### Phase 2: Component Creation

Create the component in the appropriate location:
- Custom components: `src/components/[ComponentName].tsx`
- Custom hooks: `src/hooks/[hookName].tsx`
- UI components: Use `npx shadcn-ui@latest add [component]` for shadcn components

Follow component best practices from `src/components/README.md`:
- Simple default usage with sensible defaults
- Accept `style`, `className`, and native element props
- Use composition for icons (via props, not hardcoded)
- Standard heights: 16px, 20px, 40px
- Support dark mode with Tailwind `dark:` variants

### Phase 3: Demo Page Creation (if requested)

#### A. For Component Showcase (`/components/[name]`)

1. **Create Content Component** in `src/components/DemoShowcase/[Name]Content.tsx`:
   - Extract core demo functionality without page wrappers
   - Remove: `min-h-screen`, full-page padding, headers, back links
   - Keep: interactive elements, controls, examples
   - Use Card components to organize examples
   - Include usage code examples

2. **Register in Demo Registry** (`src/components/DemoShowcase/demoRegistry.tsx`):
   ```tsx
   // Add lazy import
   const [Name]Content = lazy(() => import('./[Name]Content'))

   // Add to DEMO_REGISTRY array
   {
     id: '[name]',
     label: '[Display Name]',
     section: 'Hooks' | 'Components',
     component: [Name]Content,
     description: 'Brief description',
     path: '/components/[name]',
   }
   ```

3. **Add Route** in `src/App.tsx`:
   ```tsx
   // Add lazy import at top
   const [Name]Content = lazy(() => import('./components/DemoShowcase/[Name]Content'))

   // Add route inside <Route path="/components"> nested routes
   <Route
     path="[name]"
     element={
       <Suspense fallback={<div>Loading...</div>}>
         <[Name]Content />
       </Suspense>
     }
   />
   ```

#### B. For Standalone Demo Page (`/[name]-demo`)

1. **Create Page Component** in `src/pages/[Name]Demo.tsx`:
   - Include full-page wrapper with proper styling
   - Add header with title and description
   - Organize examples using Card components
   - Include code examples showing usage
   - Add back link to home

2. **Add Route** in `src/App.tsx`:
   ```tsx
   import [Name]Demo from './pages/[Name]Demo'

   <Route path="/[name]-demo" Component={[Name]Demo} />
   ```

#### C. For Component Playground (`/components/[name]-playground`)

Playgrounds provide an interactive, Storybook-like environment with a canvas and props controls.

1. **Analyze Component Props:**
   - Read the target component's source file
   - Parse the TypeScript Props interface
   - Categorize props as controllable or complex

2. **Guide Prop Selection - Present to User:**
   > "I analyzed [ComponentName] and found these props:
   >
   > **Recommended for playground (controllable):**
   > - `variant`: 'default' | 'destructive' | 'outline' | 'secondary' | 'ghost' | 'link'
   > - `size`: 'default' | 'sm' | 'lg' | 'icon'
   > - `disabled`: boolean
   >
   > **Complex props (not controllable):**
   > - `onClick`: function
   > - `asChild`: boolean (affects render behavior)
   > - `ref`: React ref
   >
   > Which props would you like to expose in the playground?"

3. **Create Playground Content** in `src/components/DemoShowcase/[Name]PlaygroundContent.tsx`:
   ```tsx
   import PlaygroundCanvas, { PropSchema } from './PlaygroundCanvas'
   import { Button } from '@/components/ui/button'

   const propSchema: PropSchema = {
     variant: {
       type: 'select',
       options: ['default', 'destructive', 'outline', 'secondary', 'ghost', 'link'],
       defaultValue: 'default',
     },
     size: {
       type: 'select',
       options: ['default', 'sm', 'lg', 'icon'],
       defaultValue: 'default',
     },
     disabled: {
       type: 'boolean',
       defaultValue: false,
     },
     children: {
       type: 'string',
       defaultValue: 'Button',
     },
   }

   export default function ButtonPlaygroundContent() {
     return (
       <PlaygroundCanvas
         componentName="Button"
         propSchema={propSchema}
         defaultProps={{ children: 'Click Me' }}
       >
         {(props) => <Button {...props}>{props.children as string}</Button>}
       </PlaygroundCanvas>
     )
   }
   ```

4. **Register in Demo Registry** (`src/components/DemoShowcase/demoRegistry.tsx`):
   ```tsx
   // Add lazy import
   const [Name]PlaygroundContent = lazy(() => import('./[Name]PlaygroundContent'))

   // Add to DEMO_REGISTRY array
   {
     id: '[name]-playground',
     label: '[Name] Playground',
     section: 'Components',
     component: [Name]PlaygroundContent,
     description: 'Interactive playground for [Name]',
     path: '/components/[name]-playground',
     type: 'playground',
   }
   ```

5. **Add Route** in `src/App.tsx`:
   ```tsx
   const [Name]PlaygroundContent = lazy(() => import('./components/DemoShowcase/[Name]PlaygroundContent'))

   <Route
     path="[name]-playground"
     element={
       <Suspense fallback={<div>Loading...</div>}>
         <[Name]PlaygroundContent />
       </Suspense>
     }
   />
   ```

### Prop Type Mapping Reference

When analyzing TypeScript props, map types to Leva controls:

| TypeScript Type | PropSchema Type | Notes |
|-----------------|-----------------|-------|
| `string` | `'string'` | Text input |
| `number` | `'number'` | Slider (add min/max/step) |
| `boolean` | `'boolean'` | Checkbox toggle |
| `'a' \| 'b' \| 'c'` | `'select'` | Dropdown with options array |
| `enum Foo { A, B }` | `'select'` | Extract enum values as options |
| `React.ReactNode` | `'string'` | For simple text children |
| Color strings | `'color'` | Color picker |
| `() => void` | Skip | Not controllable |
| Complex objects | Skip | Not controllable |
| `React.Ref` | Skip | Not controllable |

### PropSchema Format

```tsx
import { PropSchema } from '@/components/DemoShowcase/PlaygroundCanvas'

const schema: PropSchema = {
  propName: {
    type: 'string' | 'number' | 'boolean' | 'select' | 'color',
    label?: string,           // Custom label (defaults to propName)
    defaultValue?: unknown,   // Initial value
    options?: string[],       // For 'select' type
    min?: number,             // For 'number' type
    max?: number,             // For 'number' type
    step?: number,            // For 'number' type
  }
}
```

### Phase 4: Component Updates - Check for Existing Demos

**CRITICAL:** When updating an existing component or hook, ALWAYS check if demo pages exist:

1. **Search for Demo Pages:**
   - Check `src/components/DemoShowcase/` for `[Name]Content.tsx` or `[Name]PlaygroundContent.tsx`
   - Check `src/pages/` for `[Name]Demo.tsx`
   - Check `demoRegistry.tsx` for entries (including `type: 'playground'`)

2. **If Demo Pages Exist:**
   - Update them to reflect new functionality
   - Add examples demonstrating new features
   - Update code examples
   - Test that demos still work correctly

3. **Prompt User:**
   > "I found existing demo pages for this [component/hook]. I'll update them to include the new [feature/changes]."

## Demo Content Best Practices

### Structure

Organize demo content with clear sections:

```tsx
<div className="space-y-8">
  {/* Example 1: Basic Usage */}
  <Card className="p-6 space-y-3">
    <div className="flex items-center gap-2">
      <Badge variant="secondary">Basic</Badge>
      <span className="text-xs text-zinc-500 dark:text-zinc-400">
        Configuration details
      </span>
    </div>
    {/* Demo content */}
  </Card>

  {/* More examples... */}

  {/* Code Example */}
  <Card className="p-6 space-y-3 bg-zinc-50 dark:bg-zinc-900">
    <Badge variant="outline">Usage Example</Badge>
    <pre className="text-xs text-zinc-700 dark:text-zinc-300 overflow-x-auto">
      <code>{`// Code example here`}</code>
    </pre>
  </Card>
</div>
```

### Example Categories

Include diverse examples:
1. **Basic** - Simple default usage
2. **Advanced** - Complex configurations
3. **Interactive** - User-controlled examples
4. **Variants** - Different visual styles or behaviors
5. **Edge Cases** - Boundary conditions
6. **Code Examples** - Implementation snippets

### Styling

- Use Card components for grouping examples
- Add Badge components for labeling examples
- Include configuration details in muted text
- Support dark mode throughout
- Add visual indicators for interactive elements
- Show state changes clearly

## Component Showcase Navigation

The navigation is automatically generated from `demoRegistry.tsx`:
- **Hooks** section: Custom React hooks
- **Components** section: UI components, libraries, demos

Demos are displayed in the order they appear in `DEMO_REGISTRY`.

## Testing Checklist

After creating or updating component demos:

- [ ] Navigate to the demo route
- [ ] Verify all examples render correctly
- [ ] Test interactive elements (buttons, inputs, controls)
- [ ] Check dark mode appearance
- [ ] Verify code examples are accurate
- [ ] Test on different screen sizes
- [ ] Check TypeScript compilation
- [ ] Verify navigation active state

### Additional Checks for Playgrounds

- [ ] Verify Leva props panel appears (top-right corner)
- [ ] Test that prop changes update the component in real-time
- [ ] Verify navigation collapse toggle works
- [ ] Check canvas centering at different sizes
- [ ] Test all prop controls (selects, inputs, toggles)

## Examples

### Example 1: Creating a New Hook with Demo

```
User: "Create a useDebounce hook"

Claude:
1. Asks: "Would you like me to create a demo page for this hook in the component showcase?"
2. User selects: "Yes, create demo page"
3. Creates:
   - src/hooks/useDebounce.tsx (the hook)
   - src/components/DemoShowcase/DebounceContent.tsx (demo)
   - Updates demoRegistry.tsx
   - Updates App.tsx with route
```

### Example 2: Updating Existing Component

```
User: "Add a 'size' prop to the Button component"

Claude:
1. Searches for existing demos
2. Finds: N/A (Button is shadcn component, no custom demo)
3. Updates Button usage examples in existing demos if needed
```

### Example 3: Updating Hook with Demo

```
User: "Add a 'delay' option to useTypewriter"

Claude:
1. Updates src/hooks/useTypewriter.tsx
2. Searches and finds: src/components/DemoShowcase/TypewriterContent.tsx
3. Announces: "I found the existing TypewriterContent demo. I'll add an example showing the new delay option."
4. Adds new Card with delay example
5. Updates code example to include delay option
```

### Example 4: Creating a Component Playground

```
User: "Create a playground for the Badge component"

Claude:
1. Asks: "Would you like me to create a demo page for this component?"
2. User selects: "Yes, playground"
3. Claude reads src/components/ui/badge.tsx
4. Analyzes BadgeProps interface and presents:
   "I found these props:

   **Controllable:**
   - variant: 'default' | 'secondary' | 'destructive' | 'outline'
   - children: ReactNode (as string)

   **Not controllable:**
   - className: styling (skip)

   Which props would you like to expose?"
5. User selects: "variant and children"
6. Creates:
   - src/components/DemoShowcase/BadgePlaygroundContent.tsx
   - Updates demoRegistry.tsx with type: 'playground'
   - Updates App.tsx with route
```

## File Locations Reference

- Component showcase layout: `src/pages/ComponentShowcase.tsx`
- Demo registry: `src/components/DemoShowcase/demoRegistry.tsx`
- Navigation: `src/components/DemoShowcase/DemoNavigation.tsx`
- Demo content: `src/components/DemoShowcase/[Name]Content.tsx`
- Playground content: `src/components/DemoShowcase/[Name]PlaygroundContent.tsx`
- Playground canvas: `src/components/DemoShowcase/PlaygroundCanvas.tsx`
- Standalone demos: `src/pages/[Name]Demo.tsx`
- Routes: `src/App.tsx`

## Key Principles

1. **Always ask** - Don't assume whether demos are wanted
2. **Always search** - Check for existing demos before updating
3. **Keep demos updated** - When components change, demos should reflect it
4. **Provide variety** - Show multiple use cases, not just basic usage
5. **Make it interactive** - Let users experiment with controls
6. **Include code** - Show implementation examples
7. **Support dark mode** - Test in both themes
8. **Organize clearly** - Use consistent structure across demos
