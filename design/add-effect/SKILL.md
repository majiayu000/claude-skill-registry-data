---
name: add-effect
description: Add a new visual effect to ProAnimate. Covers effect function creation, dispatcher registration, and style filter integration.
argument-hint: <effect-name>
---

# Add Visual Effect to ProAnimate

Create a new canvas-based visual effect that processes character sprites or images. Effects use an LRU cache system for sync lookups during RAF rendering.

## Steps

1. **Define effect settings** in `src/types/styleEffects.ts`

   Add a new settings interface:
   ```ts
   export interface MyEffectSettings {
     enabled: boolean
     // Effect-specific parameters with ranges in comments
     intensity: number    // (0-1)
     someParam: number    // (min-max)
   }
   ```

   Add the effect type to the `StyleEffectType` union:
   ```ts
   export type StyleEffectType = 'pixel-art' | 'woodcut' | ... | 'my-effect'
   ```

   Add to the `ActiveStyleEffect` settings union and the `DEFAULT_SETTINGS` map.

   If the effect is animated (changes per frame), add it to the `ANIMATED_EFFECTS` set.

2. **Create effect file** in `src/services/effects/<myEffect>Effect.ts`

   Use the `createEffectCache` factory:
   ```ts
   import type { MyEffectSettings } from '@/types/styleEffects'
   import { createEffectCache, loadImage } from '@/services/styleEffectCache'

   function processImage(
     img: HTMLImageElement,
     settings: MyEffectSettings,
     seed?: number,
   ): string {
     const canvas = document.createElement('canvas')
     canvas.width = img.naturalWidth
     canvas.height = img.naturalHeight
     const ctx = canvas.getContext('2d')!

     // Draw original image
     ctx.drawImage(img, 0, 0)

     // Get pixel data
     const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height)
     const data = imageData.data

     // Apply effect to pixel data...
     // ...

     ctx.putImageData(imageData, 0, 0)
     return canvas.toDataURL('image/png')
   }

   export const myEffectCache = createEffectCache<MyEffectSettings>({
     name: 'my-effect',
     maxEntries: 200,
     cacheKeyFn: (src, settings, seed) =>
       `my-effect:${src}:${settings.intensity}:${settings.someParam}:${seed ?? 0}`,
     processFn: async (src, settings, seed) => {
       const img = await loadImage(src)
       return processImage(img, settings, seed)
     },
     // Optional: canvas overlay for rigged character mode
     overlayFn: (source, output, settings, seed) => {
       // Process source canvas directly onto output canvas
       // Return true if applied, false if skipped
       return true
     },
   })
   ```

3. **Register in the effect dispatcher** at `src/services/effects/effectDispatcher.ts`

   Import the cache:
   ```ts
   import { myEffectCache } from './myEffectEffect'
   ```

   Add to the `getCache()` switch:
   ```ts
   case 'my-effect': return myEffectCache
   ```

   Add to `clearEffectCache()`:
   ```ts
   myEffectCache.clear()
   ```

4. **Add SVG filter** (optional) in `src/services/styleEffectFilters.ts`

   If the effect can also be expressed as an SVG filter for DOM-based rendering (Remotion export), add a filter definition and register it in `isSVGFilterEffect()` and `getStyleEffectFilterStyle()`.

5. **Add UI controls** in the Style & Effects panel

   The effect settings panel at `src/components/panels/` (mixed-media tab) should include controls for the new effect's settings. Add a section with sliders/toggles matching the settings interface.

## Key Files

| Purpose | Path |
|---------|------|
| Effect types & settings | `src/types/styleEffects.ts` |
| Cache factory | `src/services/styleEffectCache.ts` |
| Effect implementation | `src/services/effects/<myEffect>Effect.ts` |
| Effect dispatcher | `src/services/effects/effectDispatcher.ts` |
| SVG filter integration | `src/services/styleEffectFilters.ts` |
| SVG filter components | `src/components/canvas/StyleEffectFilters.tsx` |
| Remotion filter export | `src/remotion/RemotionStyleFilter.tsx` |

## Cache System Architecture

The effect system uses a three-tier approach:
- **`createEffectCache()`** -- LRU cache factory with inflight dedup and batch pre-cache
- **`effectDispatcher.ts`** -- Routes all effect calls to the correct cache by type string
- **Canvas components** call `getEffectFromCache()` synchronously during RAF for zero-flicker rendering

Key cache factory config (`EffectCacheConfig`):
- `name` -- debug label
- `maxEntries` -- LRU limit (typically 200)
- `cacheKeyFn` -- builds unique key from src + settings + seed
- `processFn` -- async image processing function
- `overlayFn` -- optional sync canvas-to-canvas for rigged mode

## Common Issues

- **Effect not appearing**: Verify the type string matches exactly in `StyleEffectType`, `getCache()` switch, and `clearEffectCache()`.
- **Flickering**: The effect must be pre-cached before rendering. Use `preCacheEffect()` when the effect is enabled or settings change.
- **Animated effects**: Must be in the `ANIMATED_EFFECTS` set. The seed changes per frame based on `speed` setting via `getAnimatedSeed()`.
- **Performance**: Keep `processFn` fast. Large images may need downscaling. The overlay path processes at source resolution.

## Example

Reference: `src/services/effects/woodcutEffect.ts`
- Implements line pattern generation with configurable angle, weight, spacing
- Uses `createEffectCache` with custom `cacheKeyFn` incorporating all settings
- Provides both `processFn` (async, returns data URL) and `overlayFn` (sync, canvas-to-canvas)
- Registered in `effectDispatcher.ts` switch as `'woodcut': return woodcutCache`
