---
name: add-remotion-layer
description: Add a new Remotion export layer to ProAnimate. Covers layer component creation, VideoComposition.tsx registration, and frame-based rendering.
argument-hint: <layer-name>
---

# Add Remotion Export Layer to ProAnimate

Create a new Remotion layer for exporting a feature to video. Remotion layers render frame-by-frame during export and live preview.

## Steps

1. **Create the Remotion layer** at `src/remotion/Remotion<Name>Layer.tsx`

   ```tsx
   import { useFrame } from '@/engine'

   interface Remotion<Name>LayerProps {
     items: <ItemType>[]  // Data passed from VideoComposition
   }

   export function Remotion<Name>Layer({ items }: Remotion<Name>LayerProps) {
     const frame = useFrame()

     return (
       <>
         {items.map((item) => {
           // Skip invisible or out-of-range items
           if (!item.visible) return null
           if (frame < item.startFrame || frame >= item.endFrame) return null

           const style: React.CSSProperties = {
             position: 'absolute',
             left: item.position.x,
             top: item.position.y,
             opacity: item.opacity,
             zIndex: item.zIndex,
           }

           if (item.rotation !== 0) {
             style.transform = `rotate(${item.rotation}deg)`
           }

           return (
             <div key={item.id} style={style}>
               {/* Render the item */}
             </div>
           )
         })}
       </>
     )
   }
   ```

2. **Define props interface** in `src/remotion/types.ts`

   Add the data shape to `VideoCompositionProps`:
   ```ts
   export interface VideoCompositionProps {
     // ... existing props
     <name>Data?: <ItemType>[]
   }
   ```

3. **Register in VideoComposition** at `src/remotion/VideoComposition.tsx`

   Import the layer:
   ```tsx
   import { Remotion<Name>Layer } from './Remotion<Name>Layer'
   ```

   Add to the composition JSX (inside the CameraTransformWrapper):
   ```tsx
   {props.<name>Data && props.<name>Data.length > 0 && (
     <Remotion<Name>Layer items={props.<name>Data} />
   )}
   ```

4. **Pass data from stores** where VideoComposition is instantiated

   In the export pipeline, store data is read and serialized into the composition props. Find where `VideoCompositionProps` is assembled and add:
   ```ts
   <name>Data: use<Name>Store.getState().items,
   ```

## Key Patterns

### Frame-based rendering
```tsx
const frame = useFrame()  // Current frame number (from @/engine, NOT from 'remotion')

// Filter by frame range
if (frame < item.startFrame || frame >= item.endFrame) return null

// Compute progress within the item's range
const progress = (frame - item.startFrame) / (item.endFrame - item.startFrame)
```

### Keyframe interpolation
```tsx
import { useRemotionKeyframeValues } from './useRemotionKeyframes'

// Inside a component:
const kfValues = useRemotionKeyframeValues(keyframeData, 'my-type', item.id)
const x = kfValues.x ?? item.position.x
const y = kfValues.y ?? item.position.y
const opacity = kfValues.opacity ?? item.opacity
```

### Absolute positioning
All Remotion layers use absolute positioning within the composition frame:
```tsx
<div style={{
  position: 'absolute',
  left: item.position.x,
  top: item.position.y,
  width: displayWidth,
  height: displayHeight,
  opacity: item.opacity,
  zIndex: item.zIndex,
}}>
```

### Conditional rendering
Only render when there is data:
```tsx
{props.myData && props.myData.length > 0 && (
  <RemotionMyLayer items={props.myData} />
)}
```

## Key Files

| Purpose | Path |
|---------|------|
| Remotion layers directory | `src/remotion/` |
| VideoComposition (all layers) | `src/remotion/VideoComposition.tsx` |
| Remotion types | `src/remotion/types.ts` |
| Frame hook | `@/engine` (`useFrame`) |
| Keyframe interpolation | `src/remotion/useRemotionKeyframes.ts` |
| Camera wrapper | `src/remotion/CameraTransformWrapper.tsx` |

## Common Issues

- **Wrong frame import**: Use `useFrame()` from `@/engine`, NOT from the `remotion` package directly. The engine wraps Remotion's frame with the project's playback system.
- **Data not available**: Remotion layers receive data as props, not from stores. Store data must be serialized and passed through `VideoCompositionProps`.
- **Layer order**: zIndex on the layer's container `div` controls stacking. Existing layers use ranges like 1-10 for backgrounds, 5-8 for characters, 6-7 for shapes, 8-10 for text overlays.
- **Blank export**: If the layer renders nothing, check that `visible` and frame range filtering is correct. Also verify the data is actually passed to VideoComposition.
- **Performance**: Avoid heavy computation inside the render function. Pre-compute values or use memoization. Each frame triggers a re-render.

## Example

Reference: `src/remotion/RemotionArtCurveLayer.tsx`
- Accepts `ArtCurveComposition[]` as props
- Uses `useFrame()` from `@/engine`
- Filters by `visible`, `startFrame`, `endFrame`
- Renders with absolute positioning, opacity, zIndex, rotation transform
- Returns SVG content via `dangerouslySetInnerHTML`

Reference: `src/remotion/RemotionTextOverlay.tsx`
- Uses keyframe interpolation via `useRemotionKeyframeValues`
- Computes text animation presets per frame
- Renders text with full CSS styling
