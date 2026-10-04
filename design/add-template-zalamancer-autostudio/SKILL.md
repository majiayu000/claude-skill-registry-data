---
name: add-template
description: Add a new motion graphics or kinetic typography template to ProAnimate. Covers KineticBase extension, registry, and builtin template creation.
argument-hint: <template-name>
---

# Add Template to ProAnimate

Create a new motion graphics template -- either a kinetic typography React component or an HTML motion graphics template.

## Option A: Kinetic Typography Template (React Component)

### Steps

1. **Create template file** in `src/motionGraphics/templates/Kinetic<Name>.tsx`

2. **Import KineticBase and registry**:
   ```tsx
   import { registerMotionGraphic } from '../registry'
   import { KineticBase, type KineticBaseConfig, type KineticAnimation, type WordRenderProps, type BackgroundRenderProps } from '../KineticBase'
   import type { MotionGraphicProps } from '@/types/motionGraphic'
   ```

3. **Define config interface** extending `KineticBaseConfig`:
   ```tsx
   interface MyConfig extends KineticBaseConfig {
     // Add custom config fields
     customParam: number
   }
   ```
   `KineticBaseConfig` provides: `words: string[]`, `colors: string[]`, `bgColor: string`, `cycleDuration: number`

4. **Define the animation object** implementing `KineticAnimation`:
   ```tsx
   const animation: KineticAnimation = {
     renderBackground: ({ bgColor, width, height, frame, fps, progress }: BackgroundRenderProps) => (
       <div style={{ position: 'absolute', inset: 0, background: bgColor }} />
     ),
     renderWord: ({ word, color, enterProgress, holdProgress, exitProgress, phase, index, width, height }: WordRenderProps) => {
       // Animate based on phase: 'enter' | 'hold' | 'exit'
       // enterProgress/holdProgress/exitProgress are 0..1
       let opacity = phase === 'exit' ? 1 - exitProgress : Math.min(1, enterProgress * 2)
       return (
         <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', opacity, color }}>
           {word}
         </div>
       )
     },
   }
   ```

5. **Create wrapper component**:
   ```tsx
   function MyComponent(props: MotionGraphicProps<MyConfig>) {
     return <KineticBase {...props} animation={animation} />
   }
   ```

6. **Register with the motion graphic registry** (self-registering on import):
   ```tsx
   registerMotionGraphic({
     id: 'tpl-kinetic-my-template',
     title: 'Kinetic My Template',
     description: 'Description of the visual effect',
     tags: ['kinetic', 'typography', 'relevant-tags'],
     category: 'captions',
     component: MyComponent as any,
     defaultConfig: {
       words: ['HELLO', 'WORLD'],
       colors: ['#FF6B6B', '#4ECDC4'],
       bgColor: '#1a1a2e',
       cycleDuration: 1,
       customParam: 100,
     },
     configSchema: [
       { key: 'words', label: 'Words', type: 'text-array', defaultValue: ['HELLO', 'WORLD'], group: 'Content' },
       { key: 'colors', label: 'Colors', type: 'text-array', defaultValue: ['#FF6B6B', '#4ECDC4'], group: 'Style' },
       { key: 'bgColor', label: 'Background', type: 'color', defaultValue: '#1a1a2e', group: 'Style' },
       { key: 'cycleDuration', label: 'Cycle Duration (s)', type: 'number', defaultValue: 1, min: 0.3, max: 5, group: 'Timing' },
       { key: 'customParam', label: 'Custom Param', type: 'number', defaultValue: 100, min: 0, max: 500, group: 'Animation' },
     ],
   })
   ```

7. **Ensure the file is imported** so registration runs. The template files in `src/motionGraphics/templates/` are auto-imported via the motion graphics index.

## Option B: HTML Motion Graphics Template

### Steps

1. **Create HTML file** in `src/data/templates/<template-name>.html`
   - Self-contained HTML/CSS/JS
   - Use `window.CONFIG` object for configurable properties
   - Listen for `postMessage` events to receive live config updates:
     ```js
     window.addEventListener('message', (e) => {
       if (e.data?.type === 'config-update') {
         Object.assign(window.CONFIG, e.data.config)
         render()
       }
     })
     ```

2. **Register in `src/data/builtinTemplates.ts`**:
   ```ts
   { id: 'tpl-my-template', title: 'My Template', description: 'What it does', filename: 'my-template.html', tags: ['category', 'style'] },
   ```

3. The template is automatically discovered by the template library panel and can be added to the canvas as an HTML template layer.

## Key Files

| Purpose | Path |
|---------|------|
| KineticBase component | `src/motionGraphics/KineticBase.tsx` |
| Motion graphic types | `src/types/motionGraphic.ts` |
| Registry | `src/motionGraphics/registry.ts` |
| Dynamic registry | `src/motionGraphics/dynamicRegistry.ts` |
| Template directory | `src/motionGraphics/templates/` |
| Builtin HTML templates | `src/data/builtinTemplates.ts` |
| HTML template files | `src/data/templates/*.html` |
| Canvas layer | `src/components/canvas/MotionGraphicLayer.tsx` |
| Store | `src/stores/useMotionGraphicStore.ts` |

## Common Issues

- **Template not appearing**: Ensure the file is imported (check the motionGraphics barrel export or templates index). For HTML templates, verify the entry is in `BUILTIN_TEMPLATES` array.
- **Config not reactive**: HTML templates must listen for `postMessage` config updates. React templates receive config as props automatically.
- **configSchema field types**: Supported types are `'text'`, `'color'`, `'number'`, `'boolean'`, `'text-array'`, `'select'`. Each field needs a `group` string for UI grouping.
- **Animation timing**: KineticBase handles word cycling automatically. Phase timing is 20% enter, 60% hold, 20% exit per word.

## Example

Reference implementation: `src/motionGraphics/templates/KineticBounce.tsx`
- Extends `KineticBaseConfig` with `bounceHeight`
- Implements `renderWord` with bounce easing, squash on impact, and idle bob
- Implements `renderBackground` as a solid color fill
- Registers with `registerMotionGraphic()` including `configSchema`
