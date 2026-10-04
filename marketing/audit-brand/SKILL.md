---
name: audit-brand
description: Audit a clip for brand consistency including color palette, typography, tone, and visual style adherence to brand kit.
---

# Audit Brand

Audit a ProAnimate clip for brand consistency by checking color palette usage, typography adherence, logo/watermark presence, and tone alignment against a configured brand kit.

## Purpose

Ensure that clips maintain consistent branding across all visual and textual elements. The brand system provides both manual brand kit configuration and AI-powered brand extraction from URLs, then enforces brand rules across the composition.

## Steps

1. **Set up a brand kit** via `brandKitService.ts`:
   - A `BrandKit` contains: `name`, `colors` (primary, secondary, accent, background, text), `fonts` (heading, body), `logoUrl`, `watermarkUrl`, `tone`, `style` preferences.
   - Create a brand kit: `upsertBrandKit(kit)` persists to Supabase.
   - Upload brand assets: `uploadBrandAsset(file, kitId, 'logo')` uploads to Supabase Storage.
   - Fetch user's kits: `fetchUserBrandKits(userId)`.

2. **Auto-extract brand from URL** (AI-powered):
   - `analyzeBusinessURL(url)` in `brandDirector.ts` calls the server endpoint `/api/brand-director/analyze-url`.
   - Server scrapes the website and uses Gemini vision to extract:
     - Color palette (primary, secondary, accent colors).
     - Typography (font families, weights).
     - Brand images (logos, hero images).
     - Industry and niche classification.
     - Tone and style attributes.
   - Returns an `AnalyzeURLResponse` with a `BrandProfile`.

3. **Check color palette adherence**:
   - Compare colors used in text overlays, shapes, backgrounds against brand kit colors.
   - `useTextOverlayStore` -- check each overlay's `color` and `backgroundColor`.
   - `useShapeStore` -- check each shape's `fill` and `stroke` colors.
   - `useCanvasStore` -- check `backgroundColor`.
   - Flag colors that do not match any brand kit color within a reasonable tolerance.

4. **Check typography adherence**:
   - Compare font families and weights used in text overlays against brand kit fonts.
   - Brand kit specifies `headingFont` and `bodyFont`.
   - Check: `overlay.fontFamily` against `brandKit.fonts.heading` and `brandKit.fonts.body`.
   - Flag non-brand fonts used in the composition.

5. **Check logo/watermark presence**:
   - Verify that the brand logo or watermark is present in the composition.
   - Check `watermarkRenderer.ts` settings for watermark placement.
   - Verify logo is visible and not obscured by other elements.

6. **Check tone alignment** (AI-powered):
   - `brandDirector.ts` can generate video ideas that match the brand's tone.
   - `buildBrandAwarePrompt()` constructs orchestrator prompts that incorporate brand voice.
   - Compare dialogue tone against brand profile's tone attributes (professional, casual, playful, authoritative).

7. **Generate brand-compliant content**:
   - Use `buildBrandAwarePrompt(idea, brand)` to create orchestrator prompts that enforce brand guidelines.
   - Brand colors can be applied to text overlays, shapes, and backgrounds automatically.
   - Brand fonts can be enforced via the text overlay defaults.

8. **Use Brand Intelligence features**:
   - **Social presence analysis**: `fetchSocialPresence(brandName, url)` analyzes the brand's social media footprint.
   - **Competitor analysis**: `fetchCompetitiveAnalysis(brandName)` identifies competitors and their content strategies.
   - **Mentions summary**: tracks brand mentions across platforms.
   - **Video idea generation**: `generateVideoIdeas(brand, trends)` creates brand-aligned content ideas.

## Key Files

| Purpose | Path |
|---------|------|
| Brand kit CRUD service | `src/services/brandKitService.ts` |
| Brand director (AI analysis) | `src/services/brandDirector.ts` |
| Brand kit types | `src/types/brandKit.ts` |
| Brand director types | `src/types/brandDirector.ts` |
| Brand kit store | `src/stores/useBrandKitStore.ts` |
| Brand store | `src/stores/useBrandStore.ts` |
| Brand director store | `src/stores/useBrandDirectorStore.ts` |
| Brand intel store | `src/stores/useBrandIntelStore.ts` |
| Brand kit panel UI | `src/components/panels/BrandKitPanel.tsx` |
| Brand panel UI | `src/components/panels/BrandPanel.tsx` |
| Brand intel page | `src/components/pages/BrandIntelPage.tsx` |
| Watermark renderer | `src/services/watermarkRenderer.ts` |
| Color extraction | `src/services/colorExtraction.ts` |
| Server brand director routes | `server/routes/brandDirector.ts` |

## Common Issues

- **Brand kit not persisting**: Supabase connection is not configured. Check `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` in `.env`. The service returns the input kit unchanged when Supabase is unavailable.
- **URL analysis fails**: Server endpoint `/api/brand-director/analyze-url` returns an error. Common causes: URL is unreachable, CORS issues on server-side scraping, Gemini vision API error.
- **Colors do not match exactly**: Use color distance (CIE Delta E or simple RGB Euclidean distance) with a tolerance threshold rather than exact hex comparison.
- **Brand fonts not available**: Web fonts must be loaded in the browser before they appear in text overlays. Check that the font is included in the 26 supported font families in `useTextOverlayStore.ts`.
- **Logo upload fails**: Supabase Storage bucket `brand-assets` may not exist. Falls back to base64 data URL for offline mode.
- **Social presence analysis returns empty**: The server endpoint requires specific API keys for social media platform access.
- **Competitor analysis incomplete**: Limited by Gemini's real-time search capabilities. Results may not cover all competitors.

## Examples

Create a brand kit:
```ts
import { upsertBrandKit } from '@/services/brandKitService'
const kit = await upsertBrandKit({
  id: 'kit-1',
  name: 'My Brand',
  colors: { primary: '#FF6B00', secondary: '#1A1A2E', accent: '#00D4FF' },
  fonts: { heading: 'Montserrat', body: 'Inter' },
  tone: 'professional',
})
```

Analyze a business URL:
```ts
import { analyzeBusinessURL } from '@/services/brandDirector'
const result = await analyzeBusinessURL('https://example.com')
console.log('Brand:', result.brand.name)
console.log('Colors:', result.brand.colors)
console.log('Industry:', result.brand.industry)
```

Audit text overlays against brand:
```ts
const brandKit = useBrandKitStore.getState().activeKit
const overlays = useTextOverlayStore.getState().overlays
const brandColors = Object.values(brandKit.colors)
for (const overlay of overlays) {
  const isOnBrand = brandColors.includes(overlay.color)
  if (!isOnBrand) console.warn(`Off-brand color: ${overlay.color} on "${overlay.text}"`)
}
```
