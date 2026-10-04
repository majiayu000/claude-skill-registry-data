---
name: publish-social
description: Publish video to social media platforms with metadata, thumbnails, and platform-specific optimization.
---

# Publish to Social Media

Publish an exported video to social media platforms (TikTok, YouTube, Instagram, Facebook, X/Twitter) with AI-generated metadata, platform-specific optimization, and scheduling.

## Purpose

After exporting a video, publish it to connected social media accounts with optimized titles, descriptions, hashtags, and posting times. Handles OAuth flows, platform compliance, auto-reframe for different aspect ratios, and scheduled publishing.

## Steps

1. **Connect social accounts** via OAuth popup flow:
   - Call `connectPlatform('tiktok')` to initiate OAuth in a popup window.
   - The backend (`/api/social/auth/:platform`) provides the authorization URL.
   - Tokens are stored server-side -- the frontend only sends its Supabase JWT.
   - Available platforms: `facebook`, `instagram`, `tiktok`, `x`, `youtube`.

2. **Generate platform-optimized metadata**:
   - `generatePublishMetadata(contentSummary, platform, tone)` calls Gemini to produce:
     - `title` -- short catchy title (max 100 chars).
     - `description` -- engaging description (max 300 chars for TikTok/IG, 500 for YouTube).
     - `hashtags` -- 5 relevant hashtags.
     - `suggestedPostingTime` -- best time to post in 24h format.
   - Falls back to simple heuristic metadata if Gemini API key is not configured.

3. **Check platform compliance** before publishing:
   - Each platform has specific requirements defined in `PLATFORM_PROFILES`:
     - TikTok: 9:16, 15-60s, max 287MB, hook in first 3s, bottom 20% safe zone.
     - YouTube Shorts: 9:16, 30-60s, max 256MB, hook in first 5s.
     - Instagram Reels: 9:16, 15-90s, max 250MB, hook in first 3s, bottom 20% safe zone.
     - YouTube: 16:9, 60-600s, max 12GB.
     - Instagram Feed: 1:1 or 4:5, 3-60s, max 100MB.
   - `analyzePlatformFit()` returns a `PlatformFitResult` with compliance score and adjustments.

4. **Auto-reframe for target platform** (if aspect ratio differs):
   - `autoReframe.ts` computes layout transforms: center-crop for backgrounds, repositions characters/text within platform safe zones.
   - Supports batch export to multiple aspect ratios simultaneously.

5. **Publish the video**:
   - Upload the exported video blob to the platform via `/api/social/publish/:platform`.
   - Pass platform-specific options (privacy, disable comments, etc.).
   - Returns a `PublishResult` with post URL and status.

6. **Schedule posts** (optional):
   - Use `autoPublishService.ts` for scheduling posts at optimal times.
   - `postingTimeHeuristics.ts` provides optimal posting time recommendations per platform.

## Key Files

| Purpose | Path |
|---------|------|
| Social publishing service | `src/services/socialPublish.ts` |
| Metadata generator (Gemini) | `src/services/publishMetadataGenerator.ts` |
| Platform optimizer | `src/services/platformOptimizer.ts` |
| Auto-reframe service | `src/services/autoReframe.ts` |
| Posting time heuristics | `src/services/postingTimeHeuristics.ts` |
| Auto-publish scheduler | `src/services/autoPublishService.ts` |
| Social types | `src/types/social.ts` |
| Platform optimization types | `src/types/platformOptimization.ts` |
| Share panel UI | `src/components/panels/SharePanel.tsx` |
| Auto-publish panel | `src/components/panels/AutoPublishPanel.tsx` |
| Server social routes | `server/routes/social.ts` |
| Server auto-publish routes | `server/routes/autoPublish.ts` |

## Common Issues

- **OAuth popup blocked**: Browser blocks the popup. User must allow popups for the site. The service returns `{ success: false, error: 'Popup was blocked' }`.
- **401 from social endpoints**: Supabase JWT expired. The user needs to re-authenticate. `getAuthHeaders()` throws if `session.access_token` is missing.
- **Platform compliance failures**: Video does not meet platform requirements (wrong aspect ratio, too long, file too large). Run `analyzePlatformFit()` before publishing to catch issues.
- **Metadata generation fails**: Gemini API key not set or API error. Falls back to `fallbackMetadata()` which extracts first 10 words as title.
- **Auto-reframe distortion**: Characters or text placed outside safe zones get cropped. Use `compositionEngine.ts` safe zone functions to verify placement.

## Examples

Connect TikTok account:
```ts
import { connectPlatform } from '@/services/socialPublish'
const result = await connectPlatform('tiktok')
if (result.success) console.log('Connected!')
```

Generate metadata:
```ts
import { generatePublishMetadata } from '@/services/publishMetadataGenerator'
const meta = await generatePublishMetadata(
  'AI tools that save time for developers',
  'tiktok',
  'energetic'
)
// { title: '5 AI Tools Devs Need NOW', hashtags: ['#AI', '#DevTools', ...], ... }
```

Check platform fit:
```ts
import { analyzePlatformFit } from '@/services/platformOptimizer'
const fit = analyzePlatformFit('tiktok', {
  aspectRatio: '9:16', durationSeconds: 30, width: 1080, height: 1920
})
// fit.score, fit.adjustments, fit.passed
```
